from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from farmer_helper.main import app
from farmer_helper.schemas.answering import (
    AnswerGenerationRequest,
    AnswerGenerationResponse,
    Citation,
)
from farmer_helper.services.answering.provider import LLMProviderError
from farmer_helper.services.reliability.idempotency import reset_idempotency_store


class FakeSuccessService:
    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        del request
        return AnswerGenerationResponse(
            decision="answer",
            answer="Use mulch and compost.",
            citations=[Citation(document_id=1, chunk_index=0, content_hash="h-1-0")],
            model="mock-chat-v1",
            finish_reason="stop",
            input_tokens=8,
            output_tokens=4,
        )


class FakeFailService:
    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        del request
        raise LLMProviderError(
            code="LLM_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


class CountingFailService:
    def __init__(self, code: str) -> None:
        self.code = code
        self.calls = 0

    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        del request
        self.calls += 1
        raise LLMProviderError(
            code=self.code,
            message="provider unavailable",
            retryable=True,
        )


class FakeClarifyService:
    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        del request
        return AnswerGenerationResponse(
            decision="clarify",
            clarification_message="Please provide more detail.",
            clarification_code="CLARIFY_NEED_DETAIL",
        )


def _build_fake_success(_db: Session) -> FakeSuccessService:
    del _db
    return FakeSuccessService()


def _build_fake_fail(_db: Session) -> FakeFailService:
    del _db
    return FakeFailService()


def _build_fake_clarify(_db: Session) -> FakeClarifyService:
    del _db
    return FakeClarifyService()


def test_answer_generation_route_success(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_success)

    client = TestClient(app)
    response = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve soil moisture retention?",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["decision"] == "answer"
    assert payload["citations"][0]["document_id"] == 1


def test_answer_generation_route_provider_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_fail)

    client = TestClient(app)
    response = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve soil moisture retention?",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["decision"] == "clarify"
    assert payload["clarification_code"] == "CLARIFY_SERVICE_DEGRADED"
    assert payload["reliability_status"] == "degraded"
    assert payload["reliability_retryable"] is True
    assert payload["reliability_code"] == "LLM_PROVIDER_UNAVAILABLE"
    assert payload["degraded"] is True
    assert payload["degradation_code"] == "LLM_PROVIDER_UNAVAILABLE"


def test_answer_generation_route_clarification_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_clarify)

    client = TestClient(app)
    response = client.post(
        "/answers/generate",
        json={
            "question": "Help?",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["decision"] == "clarify"
    assert payload["clarification_code"] == "CLARIFY_NEED_DETAIL"


def test_answer_generation_route_idempotent_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    class CountingService:
        def __init__(self) -> None:
            self.calls = 0

        def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
            del request
            self.calls += 1
            return AnswerGenerationResponse(
                decision="answer",
                answer=f"Use mulch and compost ({self.calls}).",
                citations=[Citation(document_id=1, chunk_index=0, content_hash="h-1-0")],
                model="mock-chat-v1",
                finish_reason="stop",
                input_tokens=8,
                output_tokens=4,
            )

    service = CountingService()

    def _build_service(_db: Session) -> CountingService:
        del _db
        return service

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_service)

    request_payload: dict[str, Any] = {
        "question": "How can I improve soil moisture retention?",
        "idempotency_key": "answer-1",
        "retrieved_chunks": [
            {
                "citation": {
                    "document_id": 1,
                    "chunk_index": 0,
                    "content_hash": "h-1-0",
                },
                "text": "Mulching helps reduce evaporation.",
                "score": 0.9,
            }
        ],
    }

    client = TestClient(app)
    first = client.post("/answers/generate", json=request_payload)
    second = client.post("/answers/generate", json=request_payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert service.calls == 1


def test_answer_generation_route_idempotency_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_success)

    client = TestClient(app)
    first = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve soil moisture retention?",
            "idempotency_key": "answer-conflict-1",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    second = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve irrigation timing?",
            "idempotency_key": "answer-conflict-1",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert first.status_code == 200
    assert second.status_code == 409
    payload = second.json()["detail"]
    assert payload["status"] == "error"
    assert payload["error_code"] == "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST"


def test_answer_generation_route_idempotent_replay_for_degraded_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    service = CountingFailService(code="LLM_PROVIDER_TIMEOUT")

    def _build_service(_db: Session) -> CountingFailService:
        del _db
        return service

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_service)

    request_payload: dict[str, Any] = {
        "question": "How can I improve soil moisture retention?",
        "idempotency_key": "answer-degraded-1",
        "retrieved_chunks": [
            {
                "citation": {
                    "document_id": 1,
                    "chunk_index": 0,
                    "content_hash": "h-1-0",
                },
                "text": "Mulching helps reduce evaporation.",
                "score": 0.9,
            }
        ],
    }

    client = TestClient(app)
    first = client.post("/answers/generate", json=request_payload)
    second = client.post("/answers/generate", json=request_payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["reliability_code"] == "LLM_PROVIDER_TIMEOUT"
    assert service.calls == 1


def test_answer_generation_route_logs_degraded_observability(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    reset_idempotency_store()
    caplog.set_level("WARNING")
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_fail)

    client = TestClient(app)
    response = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve soil moisture retention?",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert response.status_code == 200
    assert any(
        record.message == "reliability.degraded"
        and getattr(record, "route", None) == "answers.generate"
        and getattr(record, "reliability_status", None) == "degraded"
        and getattr(record, "reliability_code", None) == "LLM_PROVIDER_UNAVAILABLE"
        for record in caplog.records
    )


def test_answer_generation_route_logs_conflict_observability(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    reset_idempotency_store()
    caplog.set_level("WARNING")
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(answers_route, "build_answer_generation_service", _build_fake_success)

    client = TestClient(app)
    first = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve soil moisture retention?",
            "idempotency_key": "answer-conflict-observe-1",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )
    second = client.post(
        "/answers/generate",
        json={
            "question": "How can I improve irrigation timing?",
            "idempotency_key": "answer-conflict-observe-1",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Mulching helps reduce evaporation.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert first.status_code == 200
    assert second.status_code == 409
    assert any(
        record.message == "reliability.conflict"
        and getattr(record, "route", None) == "answers.generate"
        and getattr(record, "reliability_code", None) == "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST"
        for record in caplog.records
    )
