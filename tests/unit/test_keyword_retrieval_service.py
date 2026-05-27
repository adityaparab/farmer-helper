from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.retrieval import KeywordRetrievalRequest
from farmer_helper.services.retrieval.keyword_retrieval_service import KeywordRetrievalService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_keyword_retrieval_scores_and_orders_results() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = KeywordRetrievalService(repository)

    repository.upsert(
        document_id=1,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=2,
        vector=[0.1, 0.2],
        content_hash="h1",
        chunk_text="soil health and soil moisture",
    )
    repository.upsert(
        document_id=2,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=2,
        vector=[0.3, 0.4],
        content_hash="h2",
        chunk_text="water management for crops",
    )
    repository.upsert(
        document_id=3,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=2,
        vector=[0.5, 0.6],
        content_hash="h3",
        chunk_text="soil preparation guidance",
    )

    response = service.retrieve(
        KeywordRetrievalRequest(
            query_text="soil moisture",
            top_k=2,
            provider="mock-provider",
            model="mock-embedding-v1",
            version="v1",
        )
    )

    assert len(response.items) == 2
    assert [item.document_id for item in response.items] == [1, 3]
    assert response.items[0].score > response.items[1].score


def test_keyword_retrieval_applies_filtering() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = KeywordRetrievalService(repository)

    repository.upsert(
        document_id=10,
        chunk_index=0,
        provider="provider-a",
        model="model-a",
        version="v1",
        dimensions=2,
        vector=[0.0, 0.0],
        content_hash="ha",
        chunk_text="soil nutrient plan",
    )
    repository.upsert(
        document_id=11,
        chunk_index=0,
        provider="provider-b",
        model="model-a",
        version="v1",
        dimensions=2,
        vector=[0.0, 0.0],
        content_hash="hb",
        chunk_text="soil nutrient plan",
    )

    response = service.retrieve(
        KeywordRetrievalRequest(
            query_text="soil",
            top_k=5,
            provider="provider-a",
            model="model-a",
            version="v1",
        )
    )

    assert len(response.items) == 1
    assert response.items[0].document_id == 10


def test_keyword_retrieval_returns_empty_for_no_matches() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)
    service = KeywordRetrievalService(repository)

    repository.upsert(
        document_id=20,
        chunk_index=0,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        dimensions=2,
        vector=[0.1, 0.2],
        content_hash="hc",
        chunk_text="irrigation guide",
    )

    response = service.retrieve(
        KeywordRetrievalRequest(
            query_text="fertilizer",
            top_k=5,
            provider="mock-provider",
            model="mock-embedding-v1",
            version="v1",
        )
    )

    assert response.items == []
