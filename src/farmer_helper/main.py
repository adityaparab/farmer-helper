import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from farmer_helper.api.middleware.request_id import request_id_middleware
from farmer_helper.api.routes.admin import router as admin_router
from farmer_helper.api.routes.answers import router as answers_router
from farmer_helper.api.routes.auth import router as auth_router
from farmer_helper.api.routes.embeddings import router as embeddings_router
from farmer_helper.api.routes.health import router as health_router
from farmer_helper.api.routes.retrieval import router as retrieval_router
from farmer_helper.core.config import get_settings
from farmer_helper.core.logging import RequestContextFilter, configure_logging
from farmer_helper.core.observability import configure_sentry
from farmer_helper.core.request_context import get_request_id

OPENAPI_DESCRIPTION = """
Farmer Helper is a backend-first agricultural question-answering API.

The API exposes health checks, administrative maintenance workflows, embedding
generation, retrieval, answer generation, feedback collection, and session-aware
follow-up behavior. Endpoint descriptions are intentionally detailed so Swagger
UI, OpenAPI clients, and future MCP server tooling can discover each operation's
purpose, inputs, outputs, and reliability behavior from the generated schema.
""".strip()

OPENAPI_TAGS = [
    {
        "name": "health",
        "description": "Liveness and readiness probes for runtime and database health checks.",
    },
    {
        "name": "auth",
        "description": "User registration, login, JWT session, and current-user endpoints.",
    },
    {
        "name": "admin",
        "description": (
            "Operational maintenance endpoints for ingestion jobs, reindexing, version "
            "tracking, gold answers, review queues, and access audit logs."
        ),
    },
    {
        "name": "embeddings",
        "description": (
            "Synchronous and asynchronous embedding generation endpoints that persist "
            "chunk vectors and expose job status for long-running work."
        ),
    },
    {
        "name": "retrieval",
        "description": (
            "Hybrid retrieval endpoints that combine vector search, keyword search, "
            "fusion, reranking, caching, and optional session context."
        ),
    },
    {
        "name": "answers",
        "description": (
            "Grounded answer-generation endpoints with citation-aware responses, "
            "streaming output, feedback capture, idempotency, caching, and reliability fallbacks."
        ),
    },
]


def generate_stable_operation_id(route: APIRoute) -> str:
    """Generate deterministic OpenAPI operation identifiers for clients and MCP tooling.

    FastAPI can derive operation IDs from route paths and methods, but those values are more
    likely to drift as URL shapes evolve. This helper keeps the operation ID anchored to the
    first route tag and Python route handler name, producing stable tool-like identifiers
    such as ``answers_generate_answer``. Future MCP adapters can use these identifiers as
    canonical tool names when translating the OpenAPI schema into callable capabilities.
    """
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}_{route.name}".replace("-", "_")


async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for main.py workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are _, exc. It
    runs asynchronously and may await downstream I/O before returning. It returns
    JSONResponse for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    logging.getLogger(__name__).exception("Unhandled exception", extra={"error": str(exc)})
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_UNHANDLED_ERROR",
            "message": "An unexpected error occurred",
            "request_id": get_request_id(),
        },
    )


def create_app() -> FastAPI:
    """Create app for main.py workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. The function does not
    require explicit caller-supplied arguments. It runs synchronously and returns after
    local processing is complete. It returns FastAPI for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    settings = get_settings()
    configure_logging(settings.app_log_level)
    configure_sentry(settings)
    logging.getLogger().addFilter(RequestContextFilter(get_request_id))

    app = FastAPI(
        title="Farmer Helper API",
        summary="Grounded agricultural question-answering backend.",
        description=OPENAPI_DESCRIPTION,
        version="0.1.0",
        openapi_tags=OPENAPI_TAGS,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_parameters={
            "docExpansion": "none",
            "displayRequestDuration": True,
            "filter": True,
            "operationsSorter": "alpha",
            "tagsSorter": "alpha",
        },
        generate_unique_id_function=generate_stable_operation_id,
    )
    app.middleware("http")(request_id_middleware)
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(embeddings_router)
    app.include_router(retrieval_router)
    app.include_router(answers_router)
    _register_frontend_routes(app, settings)

    app.add_exception_handler(Exception, global_exception_handler)

    return app


def _register_frontend_routes(app: FastAPI, settings: object) -> None:
    """Register static and fallback routes for the built web frontend when available."""
    frontend_serve_enabled = bool(getattr(settings, "frontend_serve_enabled", False))
    if not frontend_serve_enabled:
        return

    dist_dir = Path(getattr(settings, "frontend_dist_dir", "frontend/dist")).resolve()
    index_file = dist_dir / "index.html"
    assets_dir = dist_dir / "assets"

    if not index_file.exists() or not dist_dir.exists():
        logging.getLogger(__name__).info(
            "frontend.static.disabled",
            extra={"frontend_dist_dir": str(dist_dir), "reason": "missing_dist_or_index"},
        )
        return

    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="frontend-assets")

    app.mount("/frontend-static", StaticFiles(directory=str(dist_dir)), name="frontend-static")

    api_prefixes = (
        "health",
        "admin",
        "embeddings",
        "retrieval",
        "answers",
        "auth",
        "docs",
        "redoc",
        "openapi.json",
    )

    @app.get("/", include_in_schema=False)
    def frontend_index() -> FileResponse:  # pyright: ignore[reportUnusedFunction]
        return FileResponse(index_file)

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend_fallback(full_path: str) -> FileResponse:  # pyright: ignore[reportUnusedFunction]
        if any(
            full_path == prefix or full_path.startswith(f"{prefix}/")
            for prefix in api_prefixes
        ):
            raise HTTPException(status_code=404, detail="Not Found")

        candidate = dist_dir / full_path
        if candidate.exists() and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(index_file)


app = create_app()
