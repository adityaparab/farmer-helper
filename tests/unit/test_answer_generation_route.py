from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.schemas.answering import AnswerGenerationResponse
from farmer_helper.services.answering.provider import LLMProviderError


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


def test_answer_generation_route_success(monkeypatch) -> None:
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda: FakeSuccessService(),
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
    from farmer_helper.api.routes import answers as answers_route

    monkeypatch.setattr(
        answers_route,
        "build_answer_generation_service",
        lambda: FakeFailService(),
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
