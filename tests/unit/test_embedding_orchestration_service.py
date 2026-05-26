import asyncio

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.embedding import (
    EmbeddingItem,
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingSourceChunk,
)
from farmer_helper.services.embedding.batch_service import EmbeddingBatchService
from farmer_helper.services.embedding.orchestration_service import EmbeddingOrchestrationService
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


class StableProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        items = [
            EmbeddingItem(index=index, vector=[float(index), float(len(text))])
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=2)


class AlwaysFailProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_orchestration_persists_embeddings_for_all_chunks() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    batch_service = EmbeddingBatchService(StableProvider(), batch_size=2)
    service = EmbeddingOrchestrationService(
        batch_service=batch_service,
        embedding_repository=repository,
        provider="test-provider",
        version="v1",
    )

    async def run() -> None:
        result = await service.embed_and_persist(
            document_id=10,
            model="test-model",
            chunks=[
                EmbeddingSourceChunk(chunk_index=0, text="soil", content_hash="h0"),
                EmbeddingSourceChunk(chunk_index=1, text="rain", content_hash="h1"),
                EmbeddingSourceChunk(chunk_index=2, text="water", content_hash="h2"),
            ],
        )
        assert result.document_id == 10
        assert result.persisted_count == 3
        assert result.dimensions == 2

    asyncio.run(run())

    persisted = repository.list_for_document(document_id=10)
    assert len(persisted) == 3
    assert [item.chunk_index for item in persisted] == [0, 1, 2]


def test_orchestration_propagates_provider_error_without_partial_writes() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    batch_service = EmbeddingBatchService(AlwaysFailProvider(), batch_size=2)
    service = EmbeddingOrchestrationService(
        batch_service=batch_service,
        embedding_repository=repository,
        provider="test-provider",
        version="v1",
    )

    async def run() -> None:
        with pytest.raises(EmbeddingProviderError):
            await service.embed_and_persist(
                document_id=11,
                model="test-model",
                chunks=[
                    EmbeddingSourceChunk(chunk_index=0, text="soil", content_hash="h0"),
                    EmbeddingSourceChunk(chunk_index=1, text="rain", content_hash="h1"),
                ],
            )

    asyncio.run(run())

    persisted = repository.list_for_document(document_id=11)
    assert persisted == []
