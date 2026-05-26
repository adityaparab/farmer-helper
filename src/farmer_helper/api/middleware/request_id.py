import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from farmer_helper.core.request_context import set_request_id


async def request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    set_request_id(request_id)

    started_at = time.perf_counter()
    response = await call_next(request)
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    response.headers["x-request-id"] = request_id
    response.headers["x-response-time-ms"] = str(latency_ms)
    return response
