import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from farmer_helper.core.request_context import set_request_id
from farmer_helper.services.security.guard import evaluate_request_security

logger = logging.getLogger(__name__)


async def request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    set_request_id(request_id)

    started_at = time.perf_counter()
    security_response = evaluate_request_security(request)
    response: Response
    if security_response is not None:
        response = security_response
    else:
        response = await call_next(request)
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    response.headers["x-request-id"] = request_id
    response.headers["x-response-time-ms"] = str(latency_ms)
    logger.info(
        "http.request.completed",
        extra={
            "request_id": request_id,
            "http_method": request.method,
            "http_route": request.url.path,
            "http_status_code": response.status_code,
            "http_latency_ms": latency_ms,
        },
    )
    return response
