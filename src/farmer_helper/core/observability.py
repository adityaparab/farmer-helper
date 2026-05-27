import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from farmer_helper.core.config import Settings

logger = logging.getLogger(__name__)


def configure_sentry(settings: "Settings") -> bool:
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
