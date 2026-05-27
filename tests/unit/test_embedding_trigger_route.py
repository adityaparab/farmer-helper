from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult
from farmer_helper.services.embedding.provider import EmbeddingProviderError
from farmer_helper.services.reliability.idempotency import reset_idempotency_store


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
    reset_idempotency_store()
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
    reset_idempotency_store()
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

    assert response.status_code == 200
    payload = response.json()
    assert payload["persisted_count"] == 0
    assert payload["reliability_status"] == "degraded"
    assert payload["reliability_retryable"] is True
    assert payload["reliability_code"] == "EMBEDDING_PROVIDER_UNAVAILABLE"
    assert payload["degraded"] is True
    assert payload["degradation_code"] == "EMBEDDING_PROVIDER_UNAVAILABLE"


def test_embedding_trigger_route_idempotent_replay(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    class CountingService:
        def __init__(self) -> None:
            self.calls = 0

        async def embed_and_persist(self, **kwargs) -> EmbeddingOrchestrationResult:  # type: ignore[no-untyped-def]
            self.calls += 1
            return EmbeddingOrchestrationResult(
                document_id=kwargs["document_id"],
                model=kwargs["model"],
                provider="mock-provider",
                version="v1",
                dimensions=8,
                persisted_count=len(kwargs["chunks"]),
            )

    service = CountingService()
    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        lambda **_: service,
    )

    client = TestClient(app)
    request_payload = {
        "document_id": 52,
        "model": "test-model",
        "idempotency_key": "embed-1",
        "chunks": [
            {"chunk_index": 0, "text": "soil", "content_hash": "h0"},
            {"chunk_index": 1, "text": "water", "content_hash": "h1"},
        ],
    }

    first = client.post("/embeddings/trigger", json=request_payload)
    second = client.post("/embeddings/trigger", json=request_payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert service.calls == 1


def test_embedding_trigger_route_idempotency_conflict(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        lambda **_: FakeSuccessService(),
    )

    client = TestClient(app)
    first = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 53,
            "model": "test-model",
            "idempotency_key": "embed-conflict-1",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    second = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 54,
            "model": "test-model",
            "idempotency_key": "embed-conflict-1",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert first.status_code == 200
    assert second.status_code == 409
    payload = second.json()["detail"]
    assert payload["status"] == "error"
    assert payload["error_code"] == "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST"
