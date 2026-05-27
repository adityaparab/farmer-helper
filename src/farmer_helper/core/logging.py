import logging
from collections.abc import Mapping, Sequence
from typing import Any

from pythonjsonlogger.json import JsonFormatter

REDACTED_VALUE = "[REDACTED]"
_SENSITIVE_KEYWORDS = (
    "password",
    "token",
    "secret",
    "authorization",
    "api_key",
    "database_url",
    "dsn",
)


def _is_sensitive_key(name: str) -> bool:
    normalized = name.strip().lower()
    return any(keyword in normalized for keyword in _SENSITIVE_KEYWORDS)


def _redact_nested(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            key: REDACTED_VALUE if _is_sensitive_key(str(key)) else _redact_nested(nested)
            for key, nested in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_redact_nested(item) for item in value]
    return value


class SensitiveDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in list(record.__dict__.items()):
            if _is_sensitive_key(key):
                record.__dict__[key] = REDACTED_VALUE
                continue
            record.__dict__[key] = _redact_nested(value)
        return True


def configure_logging(level: str) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.filters.clear()
    root.setLevel(level.upper())

    handler = logging.StreamHandler()
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.addFilter(SensitiveDataFilter())


class RequestContextFilter(logging.Filter):
    def __init__(self, request_id_provider: Any) -> None:
        super().__init__()
        self._request_id_provider = request_id_provider

    def filter(self, record: logging.LogRecord) -> bool:
        request_id = self._request_id_provider()
        record.request_id = request_id or "-"
        return True
