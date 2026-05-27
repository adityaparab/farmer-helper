from logging import LogRecord

from fastapi.testclient import TestClient
from pytest import LogCaptureFixture

from farmer_helper.main import app


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


def test_request_middleware_sets_request_headers_and_logs(caplog: LogCaptureFixture) -> None:
    caplog.set_level("INFO")
    client = TestClient(app)

    response = client.get("/health/live", headers={"x-request-id": "req-123"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-123"
    assert int(response.headers["x-response-time-ms"]) >= 0

    record = _find_record(caplog.records, "http.request.completed")
    assert record.__dict__["http_method"] == "GET"
    assert record.__dict__["http_route"] == "/health/live"
    assert record.__dict__["http_status_code"] == 200
    assert record.__dict__["http_latency_ms"] >= 0
    assert record.__dict__["request_id"] == "req-123"
