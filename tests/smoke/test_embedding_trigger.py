from fastapi.testclient import TestClient

from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def test_embedding_trigger_smoke_success() -> None:
    Base.metadata.create_all(bind=get_engine())

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 9201,
            "model": "mock-embedding-v1",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["document_id"] == 9201
    assert payload["persisted_count"] == 1
    assert response.headers.get("x-request-id") is not None


def test_embedding_trigger_smoke_validation_error() -> None:
    Base.metadata.create_all(bind=get_engine())

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 9202,
            "model": "mock-embedding-v1",
            "chunks": [],
        },
    )

    assert response.status_code == 422
