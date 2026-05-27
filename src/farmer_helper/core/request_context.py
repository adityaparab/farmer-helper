from contextvars import ContextVar

_request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str | None) -> None:
    """Set request id for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are request_id.
    It runs synchronously and returns after local processing is complete. It performs its
    work through side effects and returns no payload.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    _request_id_ctx_var.set(request_id)


def get_request_id() -> str | None:
    """Retrieve request id for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. The function does not
    require explicit caller-supplied arguments. It runs synchronously and returns after
    local processing is complete. It returns str | None for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    return _request_id_ctx_var.get()
