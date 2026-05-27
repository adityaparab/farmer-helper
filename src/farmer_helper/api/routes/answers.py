import json
import logging
import time
from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.answering import (
    AnswerFeedbackRequest,
    AnswerFeedbackResponse,
    AnswerGenerationRequest,
    AnswerGenerationResponse,
)
from farmer_helper.services.answering.circuit_breaker_provider import (
    CircuitBreakerLLMProvider,
    LLMCircuitBreakerPolicy,
)
from farmer_helper.services.answering.generation_service import AnswerGenerationService
from farmer_helper.services.answering.mock_provider import MockLLMProvider
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProviderError
from farmer_helper.services.answering.retrying_provider import LLMRetryPolicy, RetryingLLMProvider
from farmer_helper.services.answering.timeout_provider import LLMTimeoutPolicy, TimeoutLLMProvider
from farmer_helper.services.evaluation.feedback_signals import OnlineFeedbackSignalLogger
from farmer_helper.services.performance.cache import TTLCache
from farmer_helper.services.reliability.idempotency import (
    IdempotencyConflictError,
    compute_request_hash,
    get_idempotency_store,
)
from farmer_helper.services.reliability.response_contracts import build_error_detail
from farmer_helper.services.session.context_resolver import FollowUpContextResolver

router = APIRouter(prefix="/answers", tags=["answers"])
logger = logging.getLogger(__name__)
feedback_signal_logger = OnlineFeedbackSignalLogger(logger)
_answer_cache: TTLCache[str, AnswerGenerationResponse] = TTLCache(max_entries=512)


def _to_concise_text(answer: str) -> str:
    """Trim generated answer text to the concise response contract.

    The helper preserves short answers unchanged and truncates longer answers to a bounded
    preview with an ellipsis. It supports accessibility and compact-client modes without
    changing the underlying answer-generation service.
    """
    trimmed = answer.strip()
    if len(trimmed) <= 280:
        return trimmed
    return f"{trimmed[:277].rstrip()}..."


def _apply_accessibility_contract(
    response: AnswerGenerationResponse,
    request: AnswerGenerationRequest,
) -> AnswerGenerationResponse:
    """Apply response-mode and language metadata to an answer response.

    The helper enforces concise output when requested and mirrors the caller's response mode
    and language selections onto the response. Keeping this logic in a single helper makes
    the generated and streamed answer endpoints consistent for Swagger, OpenAPI clients, and
    future MCP adapters.

    Returns:
        AnswerGenerationResponse adjusted to the requested presentation contract.
    """
    updated = response
    if request.response_mode == "concise" and response.answer is not None:
        updated = updated.model_copy(update={"answer": _to_concise_text(response.answer)})
    return updated.model_copy(
        update={
            "response_mode": request.response_mode,
            "language": request.language,
        }
    )


def build_answer_generation_service(db: Session) -> AnswerGenerationService:
    """Assemble the answer-generation service stack for a request.

    The stack includes prompt construction, session follow-up context resolution, a mock LLM
    provider, timeout protection, retries, and circuit-breaker fallback. The function
    documents the service boundary behind answer endpoints so future MCP tooling can
    understand where grounded response generation is orchestrated.

    Returns:
        AnswerGenerationService ready to process answer-generation requests.
    """
    settings = get_settings()
    primary_provider = RetryingLLMProvider(
        provider=TimeoutLLMProvider(
            provider=MockLLMProvider(),
            policy=LLMTimeoutPolicy(timeout_seconds=settings.external_call_timeout_seconds),
        ),
        policy=LLMRetryPolicy(max_attempts=settings.llm_retry_max_attempts),
    )
    provider = CircuitBreakerLLMProvider(
        provider=primary_provider,
        policy=LLMCircuitBreakerPolicy(
            failure_threshold=settings.llm_circuit_breaker_failure_threshold,
            recovery_timeout_seconds=settings.llm_circuit_breaker_recovery_timeout_seconds,
        ),
        fallback_provider=MockLLMProvider(),
    )

    return AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=provider,
        context_resolver=FollowUpContextResolver(ChatSessionRepository(db)),
    )


@router.post("/generate", response_model=AnswerGenerationResponse)
def generate_answer(
    request: AnswerGenerationRequest,
    db: Session = Depends(get_db_session),
) -> AnswerGenerationResponse:  # noqa: B008
    """Generate a grounded answer for a user question.

    The endpoint supports response-mode and language contracts, idempotent replay, optional
    response caching, follow-up session context, citation-aware answer construction, and
    reliability fallbacks. Provider degradation returns a structured clarification response
    so clients and future MCP tools can decide whether to retry or ask the user for a
    narrower request.

    Returns:
        AnswerGenerationResponse with answer, clarification, citation, and reliability
        fields as applicable.

    Raises:
        HTTPException: 409 when an idempotency key is reused with a different request.
    """
    started_at = time.perf_counter()

    def _log_route_completed(response: AnswerGenerationResponse) -> None:
        """Record completion telemetry for answer generation.

        The helper logs route duration, generation decision, and reliability status for
        observability. These fields help operations staff and future MCP adapters explain
        whether an answer was produced, clarified, cached, or degraded.
        """
        route_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "answers.route.completed",
            extra={
                "route": "answers.generate",
                "answer_route_decision": response.decision,
                "answer_route_reliability_status": response.reliability_status,
                "answer_route_total_ms": round(route_ms, 4),
            },
        )

    settings = get_settings()
    answer_cache_ttl = settings.answer_cache_ttl_seconds
    cache_key: str | None = None
    if answer_cache_ttl > 0 and request.idempotency_key is None and request.session_key is None:
        cache_key = compute_request_hash(request.model_dump(mode="json"))
        cached = _answer_cache.get(cache_key)
        if cached is not None:
            logger.info("answers.cache.hit", extra={"route": "answers.generate"})
            contracted_cached = _apply_accessibility_contract(cached, request)
            _log_route_completed(contracted_cached)
            return contracted_cached

    if request.idempotency_key is not None:
        store = get_idempotency_store()
        request_hash = compute_request_hash(request.model_dump(mode="json"))
        try:
            replay_payload = store.replay_or_raise(
                operation="answers.generate",
                key=request.idempotency_key,
                request_hash=request_hash,
            )
        except IdempotencyConflictError as exc:
            logger.warning(
                "reliability.conflict",
                extra={
                    "route": "answers.generate",
                    "reliability_status": "error",
                    "reliability_code": "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST",
                    "reliability_retryable": False,
                },
            )
            raise HTTPException(
                status_code=409,
                detail=build_error_detail(
                    code="IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST",
                    message=str(exc),
                    retryable=False,
                ),
            ) from exc

        if replay_payload is not None:
            replay_response = AnswerGenerationResponse.model_validate(replay_payload)
            contracted_replay = _apply_accessibility_contract(replay_response, request)
            _log_route_completed(contracted_replay)
            return contracted_replay

    service = build_answer_generation_service(db)
    try:
        response = service.generate(request)
    except LLMProviderError as exc:
        logger.warning(
            "reliability.degraded",
            extra={
                "route": "answers.generate",
                "reliability_status": "degraded",
                "reliability_code": exc.code,
                "reliability_retryable": exc.retryable,
            },
        )
        response = AnswerGenerationResponse(
            decision="clarify",
            clarification_message=(
                "Answer generation is temporarily degraded. " "Please retry this request shortly."
            ),
            clarification_code="CLARIFY_SERVICE_DEGRADED",
            reliability_status="degraded",
            reliability_retryable=exc.retryable,
            reliability_code=exc.code,
            degraded=True,
            degradation_code=exc.code,
        )

    response = _apply_accessibility_contract(response, request)

    if request.idempotency_key is not None:
        store = get_idempotency_store()
        store.save(
            operation="answers.generate",
            key=request.idempotency_key,
            request_hash=compute_request_hash(request.model_dump(mode="json")),
            response_payload=response.model_dump(mode="json"),
        )
    if cache_key is not None:
        _answer_cache.set(cache_key, response, ttl_seconds=answer_cache_ttl)
        logger.info("answers.cache.miss", extra={"route": "answers.generate"})
    _log_route_completed(response)
    return response


@router.post("/generate-stream")
def generate_answer_stream(
    request: AnswerGenerationRequest,
    db: Session = Depends(get_db_session),
) -> StreamingResponse:  # noqa: B008
    """Stream a generated answer as newline-delimited JSON events.

    The endpoint runs the same generation pipeline as the standard answer endpoint and emits
    metadata, answer chunks, and a final response event. It is designed for clients that
    want incremental display while preserving a machine-readable final payload for OpenAPI
    and future MCP bridge implementations.

    Returns:
        StreamingResponse with ``application/x-ndjson`` event records.
    """
    service = build_answer_generation_service(db)
    try:
        response = service.generate(request)
    except LLMProviderError as exc:
        response = AnswerGenerationResponse(
            decision="clarify",
            clarification_message=(
                "Answer generation is temporarily degraded. " "Please retry this request shortly."
            ),
            clarification_code="CLARIFY_SERVICE_DEGRADED",
            reliability_status="degraded",
            reliability_retryable=exc.retryable,
            reliability_code=exc.code,
            degraded=True,
            degradation_code=exc.code,
        )

    contracted = _apply_accessibility_contract(response, request)
    payload = contracted.model_dump(mode="json")

    def _event_stream() -> Iterator[str]:
        """Yield answer-generation streaming events.

        The generator emits an initial metadata event, zero or more answer text chunks, and a
        final event containing the complete response payload. Keeping the event schema explicit
        makes downstream streaming clients and MCP transports easier to implement consistently.
        """
        yield json.dumps(
            {
                "event": "metadata",
                "response_mode": payload["response_mode"],
                "language": payload["language"],
                "decision": payload["decision"],
            }
        ) + "\n"

        answer_text = payload.get("answer")
        if isinstance(answer_text, str) and answer_text:
            words = answer_text.split()
            for index in range(0, len(words), 12):
                chunk = " ".join(words[index : index + 12])
                yield json.dumps({"event": "chunk", "text": chunk}) + "\n"

        yield json.dumps({"event": "final", "response": payload}) + "\n"

    return StreamingResponse(_event_stream(), media_type="application/x-ndjson")


@router.post("/feedback", response_model=AnswerFeedbackResponse, status_code=202)
def submit_answer_feedback(request: AnswerFeedbackRequest) -> AnswerFeedbackResponse:
    """Record user feedback for an answer-generation result.

    The endpoint accepts feedback signals that can be used by evaluation, monitoring, and
    future improvement workflows. It intentionally returns quickly with an accepted response
    so UI clients and MCP tools can submit feedback without waiting for offline analysis.

    Returns:
        AnswerFeedbackResponse acknowledging that the feedback signal was accepted.
    """
    feedback_signal_logger.log_answer_feedback(request)
    return AnswerFeedbackResponse()
