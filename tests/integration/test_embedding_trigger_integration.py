from fastapi.testclient import TestClient

from farmer_helper.db.base import SessionLocal, get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository


def test_embedding_trigger_persists_vectors_end_to_end() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    document_id = 9101
    cleanup_session = SessionLocal()
    try:
        cleanup_repo = ChunkEmbeddingRepository(cleanup_session)
        existing = cleanup_repo.list_for_document(document_id=document_id)
        for item in existing:
            cleanup_session.delete(item)
        cleanup_session.commit()
    finally:
        cleanup_session.close()

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": document_id,
            "model": "mock-embedding-v1",
            "provider": "mock-provider",
            "version": "v1",
            "batch_size": 2,
            "dimensions": 8,
            "chunks": [
                {"chunk_index": 0, "text": "soil health", "content_hash": "h0"},
                {"chunk_index": 1, "text": "water usage", "content_hash": "h1"},
                {"chunk_index": 2, "text": "crop rotation", "content_hash": "h2"},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["document_id"] == document_id
    assert payload["persisted_count"] == 3
    assert payload["dimensions"] == 8

    verify_session = SessionLocal()
    try:
        verify_repo = ChunkEmbeddingRepository(verify_session)
        persisted = verify_repo.list_for_document(document_id=document_id)
        assert len(persisted) == 3
        assert [item.chunk_index for item in persisted] == [0, 1, 2]
    finally:
        verify_session.close()
