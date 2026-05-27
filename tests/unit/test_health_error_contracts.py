from fastapi.testclient import TestClient

from farmer_helper.main import app


def test_health_ready_returns_structured_error_when_not_ready() -> None:
    from farmer_helper.api.routes import health as health_route

    class FakeHealthService:
        def is_ready(self) -> bool:
            return False

    app.dependency_overrides[health_route.get_health_service] = lambda: FakeHealthService()
    try:
        client = TestClient(app)
        response = client.get("/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["status"] == "error"
    assert detail["error_code"] == "DATABASE_NOT_READY"
    assert detail["retryable"] is True
