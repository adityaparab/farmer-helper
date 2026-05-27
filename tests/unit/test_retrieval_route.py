from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.retrieval import RetrievalCitation, RetrievalItem, RetrievalResponse


class FakeRetrievalService:
    def retrieve(self, request):  # type: ignore[no-untyped-def]
        return RetrievalResponse(
            items=[
                RetrievalItem(
                    document_id=42,
                    chunk_index=0,
                    content_hash="h42",
                    score=0.91,
                    vector_score=0.9,
                    keyword_score=0.95,
                    fused_score=0.91,
                    citation=RetrievalCitation(
                        document_id=42,
                        chunk_index=0,
                        content_hash="h42",
                    ),
                )
            ]
        )


def test_retrieval_query_route_success(monkeypatch) -> None:
    from farmer_helper.api.routes import retrieval as retrieval_route

    monkeypatch.setattr(
        retrieval_route,
        "build_retrieval_service",
        lambda **_: FakeRetrievalService(),
    )

    client = TestClient(app)
    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [0.1, 0.2, 0.3],
            "top_k": 3,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "reranker": "none",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 1
    assert payload["items"][0]["citation"]["document_id"] == 42
    assert payload["items"][0]["fused_score"] == payload["items"][0]["score"]


def test_retrieval_query_route_rejects_unsupported_reranker() -> None:
    client = TestClient(app)
    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [0.1, 0.2, 0.3],
            "top_k": 3,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "reranker": "unknown",
        },
    )

    assert response.status_code == 400
    assert "Unsupported reranker" in response.json()["detail"]


def test_retrieval_query_route_requires_query_vector() -> None:
    client = TestClient(app)
    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [],
            "top_k": 3,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "reranker": "none",
        },
    )

    assert response.status_code == 422
