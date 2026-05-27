import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from farmer_helper.core.config import Settings

logger = logging.getLogger(__name__)


def configure_sentry(settings: "Settings") -> bool:
    """Configure sentry for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are settings.
    It runs synchronously and returns after local processing is complete. It returns bool
    for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    if not settings.sentry_dsn:
        return False

    try:
        import sentry_sdk
    except ImportError:
        logger.warning(
            "observability.sentry.unavailable",
            extra={"sentry_configured": True},
        )
        return False

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        environment=settings.sentry_environment or settings.app_env,
    )
    logger.info(
        "observability.sentry.enabled",
        extra={
            "sentry_configured": True,
            "sentry_environment": settings.sentry_environment or settings.app_env,
            "sentry_traces_sample_rate": settings.sentry_traces_sample_rate,
        },
    )
    return True
