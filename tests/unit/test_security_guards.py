from logging import LogRecord
from typing import Any

import pytest
from fastapi.testclient import TestClient

from farmer_helper.main import app
from farmer_helper.services.security import guard


def _feedback_payload() -> dict[str, Any]:
    return {
        "question": "How can I reduce fungal outbreak risk?",
        "decision": "answer",
        "sentiment": "helpful",
    }


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


class _FakeSettings:
    def __init__(
        self,
        *,
        security_api_key: str | None,
        security_rate_limit_requests: int,
        security_rate_limit_window_seconds: int,
    ) -> None:
        self.security_api_key = security_api_key
        self.security_rate_limit_requests = security_rate_limit_requests
        self.security_rate_limit_window_seconds = security_rate_limit_window_seconds


def test_api_key_auth_blocks_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    guard.reset_rate_limiter()
    monkeypatch.setattr(
        guard,
        "get_settings",
        lambda: _FakeSettings(
            security_api_key="secret-key",
            security_rate_limit_requests=0,
            security_rate_limit_window_seconds=60,
        ),
    )

    client = TestClient(app)
    response = client.post("/answers/feedback", json=_feedback_payload())

    assert response.status_code == 401
    assert response.json()["error_code"] == "AUTH_REQUIRED"


def test_rate_limit_blocks_excess_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    guard.reset_rate_limiter()
    monkeypatch.setattr(
        guard,
        "get_settings",
        lambda: _FakeSettings(
            security_api_key=None,
            security_rate_limit_requests=1,
            security_rate_limit_window_seconds=60,
        ),
    )

    client = TestClient(app)
    first = client.post("/answers/feedback", json=_feedback_payload())
    second = client.post("/answers/feedback", json=_feedback_payload())

    assert first.status_code == 202
    assert second.status_code == 429
    assert second.json()["error_code"] == "RATE_LIMIT_EXCEEDED"
    assert int(second.headers["Retry-After"]) >= 1


def test_security_audit_log_emitted_for_auth_rejection(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    guard.reset_rate_limiter()
    caplog.set_level("WARNING")
    monkeypatch.setattr(
        guard,
        "get_settings",
        lambda: _FakeSettings(
            security_api_key="secret-key",
            security_rate_limit_requests=0,
            security_rate_limit_window_seconds=60,
        ),
    )

    client = TestClient(app)
    _ = client.post("/answers/feedback", json=_feedback_payload())

    record = _find_record(caplog.records, "security.audit")
    assert record.__dict__["security_event"] == "auth.api_key"
    assert record.__dict__["security_outcome"] == "rejected"
    assert record.__dict__["security_route"] == "/answers/feedback"
