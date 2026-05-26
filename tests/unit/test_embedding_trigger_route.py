from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult
from farmer_helper.services.embedding.provider import EmbeddingProviderError


class FakeSuccessService:
    async def embed_and_persist(self, **kwargs) -> EmbeddingOrchestrationResult:  # type: ignore[no-untyped-def]
        return EmbeddingOrchestrationResult(
            document_id=kwargs["document_id"],
            model=kwargs["model"],
            provider="mock-provider",
            version="v1",
            dimensions=8,
            persisted_count=len(kwargs["chunks"]),
        )


class FakeFailService:
    async def embed_and_persist(self, **kwargs) -> EmbeddingOrchestrationResult:  # type: ignore[no-untyped-def]
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


def test_embedding_trigger_route_success(monkeypatch) -> None:
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        lambda **_: FakeSuccessService(),
    )

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 42,
            "model": "test-model",
            "chunks": [
                {"chunk_index": 0, "text": "soil", "content_hash": "h0"},
                {"chunk_index": 1, "text": "water", "content_hash": "h1"},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["document_id"] == 42
    assert payload["persisted_count"] == 2


def test_embedding_trigger_route_provider_failure(monkeypatch) -> None:
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        lambda **_: FakeFailService(),
    )

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 43,
            "model": "test-model",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert response.status_code == 502
    payload = response.json()["detail"]
    assert payload["error_code"] == "EMBEDDING_PROVIDER_UNAVAILABLE"
    assert payload["retryable"] is True
