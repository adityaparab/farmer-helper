from fastapi.testclient import TestClient

from farmer_helper.main import app


def test_live_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers.get("x-request-id") is not None


def test_ready_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health/ready")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "up"
