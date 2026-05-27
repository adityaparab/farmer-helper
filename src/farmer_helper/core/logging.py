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
    """Is sensitive key for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are name. It
    runs synchronously and returns after local processing is complete. It returns bool for
    downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    normalized = name.strip().lower()
    return any(keyword in normalized for keyword in _SENSITIVE_KEYWORDS)


def _redact_nested(value: Any) -> Any:
    """Redact nested for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are value. It
    runs synchronously and returns after local processing is complete. It returns Any for
    downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
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
        """Filter for core runtime workflows.

        This SensitiveDataFilter method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        record. It runs synchronously and returns after local processing is complete. It returns
        bool for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        for key, value in list(record.__dict__.items()):
            if _is_sensitive_key(key):
                record.__dict__[key] = REDACTED_VALUE
                continue
            record.__dict__[key] = _redact_nested(value)
        return True


def configure_logging(level: str) -> None:
    """Configure logging for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are level. It
    runs synchronously and returns after local processing is complete. It performs its work
    through side effects and returns no payload.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
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
        """Initialize the object for core runtime workflows.

        This RequestContextFilter method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        request_id_provider. It runs synchronously and returns after local processing is
        complete. It performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        super().__init__()
        self._request_id_provider = request_id_provider

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter for core runtime workflows.

        This RequestContextFilter method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        record. It runs synchronously and returns after local processing is complete. It returns
        bool for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        request_id = self._request_id_provider()
        record.request_id = request_id or "-"
        return True
