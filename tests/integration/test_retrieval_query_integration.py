from fastapi.testclient import TestClient

from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def test_retrieval_query_end_to_end_with_metrics() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)

    for document_id, chunks in [
        (
            9301,
            [
                {"chunk_index": 0, "text": "soil moisture helps crops", "content_hash": "d1c0"},
                {
                    "chunk_index": 1,
                    "text": "water schedule and irrigation",
                    "content_hash": "d1c1",
                },
            ],
        ),
        (
            9302,
            [
                {
                    "chunk_index": 0,
                    "text": "soil soil nutrients and moisture",
                    "content_hash": "d2c0",
                },
                {"chunk_index": 1, "text": "pest control notes", "content_hash": "d2c1"},
            ],
        ),
    ]:
        trigger_response = client.post(
            "/embeddings/trigger",
            json={
                "document_id": document_id,
                "model": "mock-embedding-v1",
                "provider": "mock-provider",
                "version": "v1",
                "batch_size": 2,
                "dimensions": 8,
                "chunks": chunks,
            },
        )
        assert trigger_response.status_code == 200

    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [0.2] * 8,
            "top_k": 3,
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
    items = payload["items"]
    metrics = payload["metrics"]

    assert len(items) >= 2
    assert items[0]["document_id"] == 9302
    assert items[0]["chunk_index"] == 0
    assert items[0]["citation"]["content_hash"] == "d2c0"

    assert metrics["returned_count"] == len(items)
    assert metrics["fused_count"] >= metrics["returned_count"]
    assert metrics["vector_count"] <= 3
    assert metrics["keyword_count"] <= 3
