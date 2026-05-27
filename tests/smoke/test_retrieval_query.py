from fastapi.testclient import TestClient

from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def test_retrieval_query_smoke_success() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)
    trigger_response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 9401,
            "model": "mock-embedding-v1",
            "provider": "mock-provider",
            "version": "v1",
            "batch_size": 2,
            "dimensions": 8,
            "chunks": [
                {"chunk_index": 0, "text": "soil moisture", "content_hash": "s0"},
                {"chunk_index": 1, "text": "irrigation schedule", "content_hash": "s1"},
            ],
        },
    )
    assert trigger_response.status_code == 200

    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [0.1] * 8,
            "top_k": 2,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "vector_weight": 0.0,
            "keyword_weight": 1.0,
            "reranker": "none",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
    assert payload["items"][0]["citation"]["document_id"] == 9401
    assert payload["metrics"]["returned_count"] >= 1
    assert response.headers.get("x-request-id") is not None
