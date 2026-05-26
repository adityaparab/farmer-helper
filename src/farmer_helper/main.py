import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from farmer_helper.api.middleware.request_id import request_id_middleware
from farmer_helper.api.routes.health import router as health_router
from farmer_helper.core.config import get_settings
from farmer_helper.core.logging import RequestContextFilter, configure_logging
from farmer_helper.core.request_context import get_request_id


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.app_log_level)
    logging.getLogger().addFilter(RequestContextFilter(get_request_id))

    app = FastAPI(title=settings.app_name)
    app.middleware("http")(request_id_middleware)
    app.include_router(health_router)

    @app.exception_handler(Exception)
    async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logging.getLogger(__name__).exception("Unhandled exception", extra={"error": str(exc)})
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "INTERNAL_UNHANDLED_ERROR",
                "message": "An unexpected error occurred",
                "request_id": get_request_id(),
            },
        )

    return app


app = create_app()
