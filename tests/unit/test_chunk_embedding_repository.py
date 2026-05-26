from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_chunk_embedding_repository_inserts_new_record() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)

    created = repository.upsert(
        document_id=1,
        chunk_index=0,
        provider="test-provider",
        model="test-model",
        version="v1",
        dimensions=3,
        vector=[0.1, 0.2, 0.3],
        content_hash="hash-a",
    )

    assert created.id > 0
    assert created.document_id == 1
    assert created.chunk_index == 0
    assert created.vector_json == [0.1, 0.2, 0.3]


def test_chunk_embedding_repository_updates_existing_identity() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)

    first = repository.upsert(
        document_id=2,
        chunk_index=1,
        provider="test-provider",
        model="test-model",
        version="v1",
        dimensions=2,
        vector=[1.0, 2.0],
        content_hash="hash-b",
    )

    second = repository.upsert(
        document_id=2,
        chunk_index=1,
        provider="test-provider",
        model="test-model",
        version="v1",
        dimensions=2,
        vector=[3.0, 4.0],
        content_hash="hash-c",
    )

    assert first.id == second.id
    assert second.vector_json == [3.0, 4.0]
    assert second.content_hash == "hash-c"

    all_for_document = repository.list_for_document(document_id=2)
    assert len(all_for_document) == 1


def test_chunk_embedding_repository_keeps_distinct_identities() -> None:
    session = _session()
    repository = ChunkEmbeddingRepository(session)

    repository.upsert(
        document_id=3,
        chunk_index=0,
        provider="test-provider",
        model="test-model",
        version="v1",
        dimensions=2,
        vector=[0.0, 0.1],
        content_hash="hash-1",
    )
    repository.upsert(
        document_id=3,
        chunk_index=1,
        provider="test-provider",
        model="test-model",
        version="v1",
        dimensions=2,
        vector=[0.2, 0.3],
        content_hash="hash-2",
    )

    all_for_document = repository.list_for_document(document_id=3)
    assert len(all_for_document) == 2
    assert [item.chunk_index for item in all_for_document] == [0, 1]
