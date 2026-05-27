from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.answering import AnswerGenerationResponse
from farmer_helper.services.answering.provider import LLMProviderError
from farmer_helper.services.reliability.idempotency import reset_idempotency_store


class FakeSuccessService:
    def generate(self, request):  # type: ignore[no-untyped-def]
        return AnswerGenerationResponse(
            decision="answer",
            answer="Use mulch and compost.",
            citations=[
                {
                    "document_id": 1,
                    "chunk_index": 0,
                    "content_hash": "h-1-0",
                }
            ],
            model="mock-chat-v1",
            finish_reason="stop",
            input_tokens=8,
            output_tokens=4,
        )


class FakeFailService:
    def generate(self, request):  # type: ignore[no-untyped-def]
        raise LLMProviderError(
            code="LLM_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


class FakeClarifyService:
    def generate(self, request):  # type: ignore[no-untyped-def]
        return AnswerGenerationResponse(
            decision="clarify",
            clarification_message="Please provide more detail.",
            clarification_code="CLARIFY_NEED_DETAIL",
        )


def test_answer_generation_route_success(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda _db: FakeSuccessService(),
    )

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


def test_answer_generation_route_provider_failure(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda _db: FakeFailService(),
    )

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

    assert response.status_code == 502
    payload = response.json()["detail"]
    assert payload["error_code"] == "LLM_PROVIDER_UNAVAILABLE"
    assert payload["retryable"] is True


def test_answer_generation_route_clarification_payload(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda _db: FakeClarifyService(),
    )

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


def test_answer_generation_route_idempotent_replay(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    class CountingService:
        def __init__(self) -> None:
            self.calls = 0

        def generate(self, request):  # type: ignore[no-untyped-def]
            self.calls += 1
            return AnswerGenerationResponse(
                decision="answer",
                answer=f"Use mulch and compost ({self.calls}).",
                citations=[
                    {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    }
                ],
                model="mock-chat-v1",
                finish_reason="stop",
                input_tokens=8,
                output_tokens=4,
            )

    service = CountingService()
    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda _db: service,
    )

    request_payload = {
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


def test_answer_generation_route_idempotency_conflict(monkeypatch) -> None:
    reset_idempotency_store()
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda _db: FakeSuccessService(),
    )

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
    assert payload["error_code"] == "IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST"
