from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.retrieval import VectorRetrievalRequest
from farmer_helper.services.retrieval.vector_retrieval_service import VectorRetrievalService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_vector_retrieval_returns_top_k_in_deterministic_order() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = VectorRetrievalService(repository)

    repository.upsert(
        document_id=1,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=3,
        vector=[1.0, 0.0, 0.0],
        content_hash="h1",
    )
    repository.upsert(
        document_id=2,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=3,
        vector=[0.8, 0.2, 0.0],
        content_hash="h2",
    )
    repository.upsert(
        document_id=3,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=3,
        vector=[0.0, 1.0, 0.0],
        content_hash="h3",
    )

    response = service.retrieve(
        VectorRetrievalRequest(
            query_vector=[1.0, 0.0, 0.0],
            top_k=2,
            provider="mock-provider",
            model="mock-embedding-v1",
            version="v1",
        )
    )

    assert len(response.items) == 2
    assert [item.document_id for item in response.items] == [1, 2]
    assert response.items[0].score >= response.items[1].score


def test_vector_retrieval_filters_by_provider_model_version() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = VectorRetrievalService(repository)

    repository.upsert(
        document_id=10,
        chunk_index=0,
        provider="provider-a",
        model="model-a",
        version="v1",
        dimensions=2,
        vector=[1.0, 0.0],
        content_hash="ha",
    )
    repository.upsert(
        document_id=11,
        chunk_index=0,
        provider="provider-b",
        model="model-a",
        version="v1",
        dimensions=2,
        vector=[1.0, 0.0],
        content_hash="hb",
    )

    response = service.retrieve(
        VectorRetrievalRequest(
            query_vector=[1.0, 0.0],
            top_k=5,
            provider="provider-a",
            model="model-a",
            version="v1",
        )
    )

    assert len(response.items) == 1
    assert response.items[0].document_id == 10


def test_vector_retrieval_skips_dimension_mismatch_candidates() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = VectorRetrievalService(repository)

    repository.upsert(
        document_id=20,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=3,
        vector=[1.0, 0.0, 0.0],
        content_hash="hc",
    )

    response = service.retrieve(
        VectorRetrievalRequest(
            query_vector=[1.0, 0.0],
            top_k=5,
            provider="mock-provider",
            model="mock-embedding-v1",
            version="v1",
        )
    )

    assert response.items == []
