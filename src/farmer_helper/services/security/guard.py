from __future__ import annotations

import logging
import time
from collections import deque
from hmac import compare_digest
from threading import Lock

from fastapi import Request
from fastapi.responses import JSONResponse

from farmer_helper.core.config import get_settings
from farmer_helper.core.request_context import get_request_id

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._windows: dict[str, deque[float]] = {}
        self._lock = Lock()

    def check_allowance(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        now: float | None = None,
    ) -> tuple[bool, int]:
        now_value = time.time() if now is None else now
        window_start = now_value - float(window_seconds)

        with self._lock:
            values = self._windows.setdefault(key, deque())
            while values and values[0] < window_start:
                values.popleft()

            if len(values) >= limit:
                retry_after = max(1, int(values[0] + float(window_seconds) - now_value))
                return False, retry_after

            values.append(now_value)
            return True, 0


_rate_limiter = InMemoryRateLimiter()


def reset_rate_limiter() -> None:
    with _rate_limiter._lock:
        _rate_limiter._windows.clear()


def _security_principal(request: Request) -> str:
    api_key = request.headers.get("x-api-key")
    if api_key:
        return f"api-key:{api_key[:6]}"

    host = request.client.host if request.client is not None else "unknown"
    return f"ip:{host}"


def _audit(event: str, outcome: str, request: Request, detail: str) -> None:
    logger.warning(
        "security.audit",
        extra={
            "security_event": event,
            "security_outcome": outcome,
            "security_route": request.url.path,
            "security_method": request.method,
            "security_principal": _security_principal(request),
            "security_detail": detail,
        },
    )


def evaluate_request_security(request: Request) -> JSONResponse | None:
    if request.url.path.startswith("/health"):
        return None

    settings = get_settings()
    expected_api_key = settings.security_api_key
    provided_api_key = request.headers.get("x-api-key")

    if expected_api_key is not None and (
        provided_api_key is None or not compare_digest(provided_api_key, expected_api_key)
    ):
        _audit("auth.api_key", "rejected", request, "missing_or_invalid_api_key")
        return JSONResponse(
            status_code=401,
            content={
                "error_code": "AUTH_REQUIRED",
                "message": "Valid API key is required",
                "request_id": get_request_id(),
            },
        )

    if settings.security_rate_limit_requests > 0:
        key = _security_principal(request)
        allowed, retry_after = _rate_limiter.check_allowance(
            key=key,
            limit=settings.security_rate_limit_requests,
            window_seconds=settings.security_rate_limit_window_seconds,
        )
        if not allowed:
            _audit("rate_limit", "rejected", request, f"retry_after={retry_after}")
            return JSONResponse(
                status_code=429,
                content={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests",
                    "retry_after_seconds": retry_after,
                    "request_id": get_request_id(),
                },
                headers={"Retry-After": str(retry_after)},
            )

    return None
