import logging

from farmer_helper.core.logging import REDACTED_VALUE, SensitiveDataFilter


def test_sensitive_data_filter_redacts_sensitive_top_level_fields() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="event",
        args=(),
        exc_info=None,
    )
    record.authorization = "Bearer super-secret-token"
    record.database_url = "postgres://user:password@host/db"
    record.safe_field = "ok"

    assert SensitiveDataFilter().filter(record) is True
    assert record.authorization == REDACTED_VALUE
    assert record.database_url == REDACTED_VALUE
    assert record.safe_field == "ok"


def test_sensitive_data_filter_redacts_nested_mapping_fields() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="event",
        args=(),
        exc_info=None,
    )
    record.payload = {
        "request": {
            "api_key": "secret-key",
            "meta": {"note": "keep", "token": "nested-secret"},
        },
        "items": [{"secret": "one"}, {"name": "ok"}],
    }

    assert SensitiveDataFilter().filter(record) is True
    assert record.payload["request"]["api_key"] == REDACTED_VALUE
    assert record.payload["request"]["meta"]["token"] == REDACTED_VALUE
    assert record.payload["request"]["meta"]["note"] == "keep"
    assert record.payload["items"][0]["secret"] == REDACTED_VALUE
    assert record.payload["items"][1]["name"] == "ok"
