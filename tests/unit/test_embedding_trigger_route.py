from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from farmer_helper.main import app
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult, EmbeddingSourceChunk
from farmer_helper.services.embedding.provider import EmbeddingProviderError
from farmer_helper.services.reliability.idempotency import reset_idempotency_store


class FakeSuccessService:
    async def embed_and_persist(
        self,
        document_id: int,
        model: str,
        chunks: list[EmbeddingSourceChunk],
    ) -> EmbeddingOrchestrationResult:
        return EmbeddingOrchestrationResult(
            document_id=document_id,
            model=model,
            provider="mock-provider",
            version="v1",
            dimensions=8,
            persisted_count=len(chunks),
        )


class FakeFailService:
    async def embed_and_persist(
        self,
        document_id: int,
        model: str,
        chunks: list[EmbeddingSourceChunk],
    ) -> EmbeddingOrchestrationResult:
        del document_id, model, chunks
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


class CountingFailService:
    def __init__(self, code: str) -> None:
        self.code = code
        self.calls = 0

    async def embed_and_persist(
        self,
        document_id: int,
        model: str,
        chunks: list[EmbeddingSourceChunk],
    ) -> EmbeddingOrchestrationResult:
        del document_id, model, chunks
        self.calls += 1
        raise EmbeddingProviderError(
            code=self.code,
            message="provider unavailable",
            retryable=True,
        )


def _build_fake_success_service(
    db: Session,
    provider_name: str,
    version: str,
    batch_size: int,
    dimensions: int,
) -> FakeSuccessService:
    del db, provider_name, version, batch_size, dimensions
    return FakeSuccessService()


def _build_fake_fail_service(
    db: Session,
    provider_name: str,
    version: str,
    batch_size: int,
    dimensions: int,
) -> FakeFailService:
    del db, provider_name, version, batch_size, dimensions
    return FakeFailService()


def test_embedding_trigger_route_success(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_success_service,
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


def test_embedding_trigger_route_uses_env_model_and_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    class FakeSettings:
        embedding_provider = "env-provider"
        embedding_model = "env-embedding-model"

    monkeypatch.setattr(embeddings_route, "get_settings", lambda: FakeSettings())

    class CapturingService:
        def __init__(self, provider_name: str) -> None:
            self.provider_name = provider_name

        async def embed_and_persist(
            self,
            document_id: int,
            model: str,
            chunks: list[EmbeddingSourceChunk],
        ) -> EmbeddingOrchestrationResult:
            return EmbeddingOrchestrationResult(
                document_id=document_id,
                model=model,
                provider=self.provider_name,
                version="v1",
                dimensions=8,
                persisted_count=len(chunks),
            )

    def _build_env_service(
        db: Session,
        provider_name: str,
        version: str,
        batch_size: int,
        dimensions: int,
    ) -> CapturingService:
        del db, version, batch_size, dimensions
        return CapturingService(provider_name)

    monkeypatch.setattr(embeddings_route, "build_orchestration_service", _build_env_service)

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 420,
            "model": "client-model-ignored",
            "provider": "client-provider-ignored",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["model"] == "env-embedding-model"
    assert payload["provider"] == "env-provider"


def test_embedding_trigger_route_provider_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_fail_service,
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


def test_embedding_trigger_route_idempotent_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    class CountingService:
        def __init__(self) -> None:
            self.calls = 0

        async def embed_and_persist(
            self,
            document_id: int,
            model: str,
            chunks: list[EmbeddingSourceChunk],
        ) -> EmbeddingOrchestrationResult:
            self.calls += 1
            return EmbeddingOrchestrationResult(
                document_id=document_id,
                model=model,
                provider="mock-provider",
                version="v1",
                dimensions=8,
                persisted_count=len(chunks),
            )

    service = CountingService()

    def _build_service(
        db: Session,
        provider_name: str,
        version: str,
        batch_size: int,
        dimensions: int,
    ) -> CountingService:
        del db, provider_name, version, batch_size, dimensions
        return service

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_service,
    )

    client = TestClient(app)
    request_payload: dict[str, Any] = {
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


def test_embedding_trigger_route_idempotency_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_success_service,
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


def test_embedding_trigger_route_idempotent_replay_for_degraded_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    service = CountingFailService(code="EMBEDDING_PROVIDER_TIMEOUT")

    def _build_service(
        db: Session,
        provider_name: str,
        version: str,
        batch_size: int,
        dimensions: int,
    ) -> CountingFailService:
        del db, provider_name, version, batch_size, dimensions
        return service

    monkeypatch.setattr(embeddings_route, "build_orchestration_service", _build_service)

    request_payload: dict[str, Any] = {
        "document_id": 60,
        "model": "test-model",
        "idempotency_key": "embed-degraded-1",
        "chunks": [
            {"chunk_index": 0, "text": "soil", "content_hash": "h0"},
            {"chunk_index": 1, "text": "water", "content_hash": "h1"},
        ],
    }

    client = TestClient(app)
    first = client.post("/embeddings/trigger", json=request_payload)
    second = client.post("/embeddings/trigger", json=request_payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["reliability_code"] == "EMBEDDING_PROVIDER_TIMEOUT"
    assert service.calls == 1


def test_embedding_trigger_route_logs_degraded_observability(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    reset_idempotency_store()
    caplog.set_level("WARNING")
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_fail_service,
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
    assert any(
        record.message == "reliability.degraded"
        and getattr(record, "route", None) == "embeddings.trigger"
        and getattr(record, "reliability_status", None) == "degraded"
        and getattr(record, "reliability_code", None) == "EMBEDDING_PROVIDER_UNAVAILABLE"
        for record in caplog.records
    )


def test_embedding_trigger_route_logs_conflict_observability(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    reset_idempotency_store()
    caplog.set_level("WARNING")
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_success_service,
    )

    client = TestClient(app)
    first = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 53,
            "model": "test-model",
            "idempotency_key": "embed-conflict-observe-1",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )
    second = client.post(
        "/embeddings/trigger",
        json={
            "document_id": 54,
            "model": "test-model",
            "idempotency_key": "embed-conflict-observe-1",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert first.status_code == 200
    assert second.status_code == 409
    assert any(
        record.message == "reliability.conflict"
        and getattr(record, "route", None) == "embeddings.trigger"
        and getattr(record, "reliability_code", None) == "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST"
        for record in caplog.records
    )


def test_embedding_trigger_async_route_queues_job(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import embeddings as embeddings_route

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_success_service,
    )

    client = TestClient(app)
    queued = client.post(
        "/embeddings/trigger-async",
        json={
            "document_id": 77,
            "model": "test-model",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert queued.status_code == 202
    payload = queued.json()
    assert payload["status"] == "queued"
    status = client.get(f"/embeddings/jobs/{payload['job_id']}")
    assert status.status_code == 200
    status_payload = status.json()
    assert status_payload["status"] in {"queued", "running", "completed"}


def test_embedding_trigger_async_route_rejects_when_queue_is_full(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from farmer_helper.api.routes import embeddings as embeddings_route

    class FakeQueue:
        def reserve(self, limit: int) -> None:
            del limit
            raise embeddings_route.QueueCapacityError("Embedding worker queue is at capacity")

    monkeypatch.setattr(
        embeddings_route,
        "build_orchestration_service",
        _build_fake_success_service,
    )
    monkeypatch.setattr(embeddings_route, "get_embedding_work_queue", lambda: FakeQueue())

    client = TestClient(app)
    response = client.post(
        "/embeddings/trigger-async",
        json={
            "document_id": 78,
            "model": "test-model",
            "chunks": [{"chunk_index": 0, "text": "soil", "content_hash": "h0"}],
        },
    )

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["status"] == "error"
    assert detail["error_code"] == "EMBEDDING_QUEUE_CAPACITY_EXCEEDED"
    assert "at capacity" in detail["message"]


def test_embedding_async_job_status_not_found_returns_structured_error() -> None:
    client = TestClient(app)
    response = client.get("/embeddings/jobs/missing-job")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["status"] == "error"
    assert detail["error_code"] == "EMBEDDING_JOB_NOT_FOUND"
