from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.answering import AnswerGenerationRequest, AnswerGenerationResponse
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
from farmer_helper.services.session.context_resolver import FollowUpContextResolver

router = APIRouter(prefix="/answers", tags=["answers"])


def build_answer_generation_service(db: Session) -> AnswerGenerationService:
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
    service = build_answer_generation_service(db)
    try:
        return service.generate(request)
    except LLMProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error_code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable,
            },
        ) from exc
