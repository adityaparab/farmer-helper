from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult, EmbeddingTriggerRequest
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

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


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
            raise HTTPException(
                status_code=409,
                detail={
                    "error_code": "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST",
                    "message": str(exc),
                    "retryable": False,
                },
            ) from exc

        if replay_payload is not None:
            return EmbeddingOrchestrationResult.model_validate(replay_payload)

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
        raise HTTPException(
            status_code=502,
            detail={
                "error_code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable,
            },
        ) from exc

    if request.idempotency_key is not None:
        store = get_idempotency_store()
        store.save(
            operation="embeddings.trigger",
            key=request.idempotency_key,
            request_hash=compute_request_hash(request.model_dump(mode="json")),
            response_payload=response.model_dump(mode="json"),
        )
    return response
