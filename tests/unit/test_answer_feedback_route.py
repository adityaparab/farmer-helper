from fastapi.testclient import TestClient

from farmer_helper.main import app


def test_answer_feedback_route_accepts_feedback_signal() -> None:
    client = TestClient(app)
    response = client.post(
        "/answers/feedback",
        json={
            "session_key": "session-1",
            "question": "How can I reduce fungal outbreak risk?",
            "decision": "answer",
            "sentiment": "helpful",
            "reliability_status": "normal",
            "had_citations": True,
            "degraded": False,
            "reason": "other",
            "model": "mock-chat-v1",
        },
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}


def test_answer_feedback_route_rejects_invalid_sentiment() -> None:
    client = TestClient(app)
    response = client.post(
        "/answers/feedback",
        json={
            "question": "How can I reduce fungal outbreak risk?",
            "decision": "answer",
            "sentiment": "neutral",
        },
    )

    assert response.status_code == 422
