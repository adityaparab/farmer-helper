import logging
import time

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.embedding import (
    EmbeddingAsyncJobStatusResponse,
    EmbeddingAsyncTriggerResponse,
    EmbeddingOrchestrationResult,
    EmbeddingTriggerRequest,
)
from farmer_helper.services.embedding.async_jobs import get_embedding_async_job_store
from farmer_helper.services.embedding.batch_service import EmbeddingBatchService
from farmer_helper.services.embedding.circuit_breaker_provider import (
    CircuitBreakerEmbeddingProvider,
    EmbeddingCircuitBreakerPolicy,
)
from farmer_helper.services.embedding.mock_provider import MockEmbeddingProvider
from farmer_helper.services.embedding.orchestration_service import EmbeddingOrchestrationService
from farmer_helper.services.embedding.provider import EmbeddingProviderError
from farmer_helper.services.embedding.retrying_provider import (
    EmbeddingRetryPolicy,
    RetryingEmbeddingProvider,
)
from farmer_helper.services.embedding.timeout_provider import (
    EmbeddingTimeoutPolicy,
    TimeoutEmbeddingProvider,
)
from farmer_helper.services.reliability.idempotency import (
    IdempotencyConflictError,
    compute_request_hash,
    get_idempotency_store,
)
from farmer_helper.services.reliability.response_contracts import build_error_detail

router = APIRouter(prefix="/embeddings", tags=["embeddings"])
logger = logging.getLogger(__name__)


def build_orchestration_service(
    db: Session,
    provider_name: str,
    version: str,
    batch_size: int,
    dimensions: int,
) -> EmbeddingOrchestrationService:
    settings = get_settings()
    primary_provider = RetryingEmbeddingProvider(
        provider=TimeoutEmbeddingProvider(
            provider=MockEmbeddingProvider(dimensions=dimensions),
            policy=EmbeddingTimeoutPolicy(
                timeout_seconds=settings.external_call_timeout_seconds,
            ),
        ),
        policy=EmbeddingRetryPolicy(max_attempts=settings.embedding_retry_max_attempts),
    )
    provider = CircuitBreakerEmbeddingProvider(
        provider=primary_provider,
        policy=EmbeddingCircuitBreakerPolicy(
            failure_threshold=settings.embedding_circuit_breaker_failure_threshold,
            recovery_timeout_seconds=settings.embedding_circuit_breaker_recovery_timeout_seconds,
        ),
        fallback_provider=MockEmbeddingProvider(dimensions=dimensions),
    )
    batch_service = EmbeddingBatchService(provider=provider, batch_size=batch_size)
    return EmbeddingOrchestrationService(
        batch_service=batch_service,
        embedding_repository=ChunkEmbeddingRepository(db),
        provider=provider_name,
        version=version,
    )


@router.post("/trigger", response_model=EmbeddingOrchestrationResult)
async def trigger_embeddings(
    request: EmbeddingTriggerRequest,
    db: Session = Depends(get_db_session),
) -> EmbeddingOrchestrationResult:  # noqa: B008
    started_at = time.perf_counter()

    def _log_route_completed(response: EmbeddingOrchestrationResult) -> None:
        route_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "embeddings.route.completed",
            extra={
                "route": "embeddings.trigger",
                "embeddings_route_reliability_status": response.reliability_status,
                "embeddings_route_persisted_count": response.persisted_count,
                "embeddings_route_total_ms": round(route_ms, 4),
            },
        )

    if request.idempotency_key is not None:
        store = get_idempotency_store()
        request_hash = compute_request_hash(request.model_dump(mode="json"))
        try:
            replay_payload = store.replay_or_raise(
                operation="embeddings.trigger",
                key=request.idempotency_key,
                request_hash=request_hash,
            )
        except IdempotencyConflictError as exc:
            logger.warning(
                "reliability.conflict",
                extra={
                    "route": "embeddings.trigger",
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
            replay_response = EmbeddingOrchestrationResult.model_validate(replay_payload)
            _log_route_completed(replay_response)
            return replay_response

    service = build_orchestration_service(
        db=db,
        provider_name=request.provider,
        version=request.version,
        batch_size=request.batch_size,
        dimensions=request.dimensions,
    )

    try:
        response = await service.embed_and_persist(
            document_id=request.document_id,
            model=request.model,
            chunks=request.chunks,
        )
    except EmbeddingProviderError as exc:
        logger.warning(
            "reliability.degraded",
            extra={
                "route": "embeddings.trigger",
                "reliability_status": "degraded",
                "reliability_code": exc.code,
                "reliability_retryable": exc.retryable,
            },
        )
        response = EmbeddingOrchestrationResult(
            document_id=request.document_id,
            model=request.model,
            provider=request.provider,
            version=request.version,
            dimensions=request.dimensions,
            persisted_count=0,
            reliability_status="degraded",
            reliability_retryable=exc.retryable,
            reliability_code=exc.code,
            degraded=True,
            degradation_code=exc.code,
        )

    if request.idempotency_key is not None:
        store = get_idempotency_store()
        store.save(
            operation="embeddings.trigger",
            key=request.idempotency_key,
            request_hash=compute_request_hash(request.model_dump(mode="json")),
            response_payload=response.model_dump(mode="json"),
        )
    _log_route_completed(response)
    return response


async def _run_async_embedding_job(
    *,
    job_id: str,
    service: EmbeddingOrchestrationService,
    request: EmbeddingTriggerRequest,
) -> None:
    store = get_embedding_async_job_store()
    store.mark_running(job_id)
    try:
        result = await service.embed_and_persist(
            document_id=request.document_id,
            model=request.model,
            chunks=request.chunks,
        )
    except Exception as exc:  # pragma: no cover - exercised in tests with status assertions
        store.mark_failed(job_id, str(exc))
        return

    store.mark_completed(job_id, result)


@router.post("/trigger-async", response_model=EmbeddingAsyncTriggerResponse, status_code=202)
async def trigger_embeddings_async(
    request: EmbeddingTriggerRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session),
) -> EmbeddingAsyncTriggerResponse:  # noqa: B008
    service = build_orchestration_service(
        db=db,
        provider_name=request.provider,
        version=request.version,
        batch_size=request.batch_size,
        dimensions=request.dimensions,
    )
    store = get_embedding_async_job_store()
    job = store.create()
    background_tasks.add_task(
        _run_async_embedding_job,
        job_id=job.job_id,
        service=service,
        request=request,
    )
    return EmbeddingAsyncTriggerResponse(job_id=job.job_id)


@router.get("/jobs/{job_id}", response_model=EmbeddingAsyncJobStatusResponse)
def get_async_embedding_job(job_id: str) -> EmbeddingAsyncJobStatusResponse:
    store = get_embedding_async_job_store()
    job = store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Embedding job not found: {job_id}")

    return EmbeddingAsyncJobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        result=job.result,
        error=job.error,
    )
