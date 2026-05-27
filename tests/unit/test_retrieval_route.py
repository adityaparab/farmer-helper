from typing import Any

import pytest
from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.retrieval import (
    RetrievalCitation,
    RetrievalItem,
    RetrievalMetrics,
    RetrievalResponse,
)


class FakeRetrievalService:
    calls = 0

    def retrieve(self, request):  # type: ignore[no-untyped-def]
        del request
        FakeRetrievalService.calls += 1
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
            ],
            metrics=RetrievalMetrics(
                vector_count=2,
                keyword_count=1,
                fused_count=1,
                returned_count=1,
            ),
        )


def test_retrieval_query_route_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from farmer_helper.api.routes import retrieval as retrieval_route

    monkeypatch.setattr(
        retrieval_route,
        "build_retrieval_service",
        lambda **_kwargs: FakeRetrievalService(),
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
    assert payload["metrics"]["returned_count"] == 1


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


def test_retrieval_query_route_rejects_missing_session_context() -> None:
    client = TestClient(app)
    response = client.post(
        "/retrieval/query",
        json={
            "query_text": "soil moisture",
            "query_vector": [0.1, 0.2, 0.3],
            "session_key": "missing-session",
            "top_k": 3,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "reranker": "none",
        },
    )

    assert response.status_code == 400
    assert "Session not found" in response.json()["detail"]


def test_retrieval_query_route_uses_cache_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from farmer_helper.api.routes import retrieval as retrieval_route

    class FakeSettings:
        retrieval_cache_ttl_seconds = 60

    FakeRetrievalService.calls = 0
    monkeypatch.setattr(retrieval_route, "get_settings", lambda: FakeSettings())
    monkeypatch.setattr(
        retrieval_route,
        "build_retrieval_service",
        lambda **_kwargs: FakeRetrievalService(),
    )

    client = TestClient(app)
    payload: dict[str, Any] = {
        "query_text": "soil moisture",
        "query_vector": [0.1, 0.2, 0.3],
        "top_k": 3,
        "provider": "mock-provider",
        "model": "mock-embedding-v1",
        "version": "v1",
        "reranker": "none",
    }
    first = client.post("/retrieval/query", json=payload)
    second = client.post("/retrieval/query", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert FakeRetrievalService.calls == 1
