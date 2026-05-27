from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.health_repository import HealthRepository
from farmer_helper.schemas.health import HealthLiveResponse, HealthReadyResponse
from farmer_helper.services.health_service import HealthService
from farmer_helper.services.reliability.response_contracts import build_error_detail

router = APIRouter(prefix="/health", tags=["health"])


def get_health_service(db: Session = Depends(get_db_session)) -> HealthService:  # noqa: B008
    """Build the health service dependency for health-check endpoints.

    This dependency adapts the active SQLAlchemy session into a HealthRepository and then
    into a HealthService. Keeping the construction here makes the readiness endpoint easy
    for OpenAPI and future MCP tooling to identify as database-backed.

    Returns:
        HealthService configured with the request-scoped database session.
    """
    return HealthService(repository=HealthRepository(session=db))


@router.get("/live", response_model=HealthLiveResponse)
def live() -> HealthLiveResponse:
    """Report whether the API process is alive.

    This lightweight probe does not touch external dependencies. Load balancers, container
    orchestrators, Swagger users, and future MCP health adapters can call it to confirm that
    the application process is accepting requests.

    Returns:
        HealthLiveResponse with status set to ``ok`` when the process is running.
    """
    return HealthLiveResponse(status="ok")


@router.get("/ready", response_model=HealthReadyResponse)
def ready(
    service: HealthService = Depends(get_health_service),
) -> HealthReadyResponse:  # noqa: B008
    """Report whether the API is ready to serve database-backed traffic.

    The endpoint checks the configured database through HealthService and returns a 503
    response when storage is unavailable. It is suitable for readiness probes, release
    gates, and MCP server startup checks that need to avoid calling richer business
    endpoints before dependencies are ready.

    Returns:
        HealthReadyResponse describing API and database readiness.

    Raises:
        HTTPException: 503 when the database readiness check fails.
    """
    try:
        ready_state = service.is_ready()
    except Exception as exc:  # pragma: no cover - readiness failure path tested via API behavior
        raise HTTPException(
            status_code=503,
            detail=build_error_detail(
                code="DATABASE_NOT_READY",
                message="Database not ready",
                retryable=True,
            ),
        ) from exc

    if not ready_state:
        raise HTTPException(
            status_code=503,
            detail=build_error_detail(
                code="DATABASE_NOT_READY",
                message="Database not ready",
                retryable=True,
            ),
        )

    return HealthReadyResponse(status="ok", database="up")
