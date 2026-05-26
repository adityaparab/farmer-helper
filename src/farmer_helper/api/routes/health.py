from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.health_repository import HealthRepository
from farmer_helper.schemas.health import HealthLiveResponse, HealthReadyResponse
from farmer_helper.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])


def get_health_service(db: Session = Depends(get_db_session)) -> HealthService:  # noqa: B008
    return HealthService(repository=HealthRepository(session=db))


@router.get("/live", response_model=HealthLiveResponse)
def live() -> HealthLiveResponse:
    return HealthLiveResponse(status="ok")


@router.get("/ready", response_model=HealthReadyResponse)
def ready(
    service: HealthService = Depends(get_health_service),
) -> HealthReadyResponse:  # noqa: B008
    try:
        ready_state = service.is_ready()
    except Exception as exc:  # pragma: no cover - readiness failure path tested via API behavior
        raise HTTPException(status_code=503, detail="Database not ready") from exc

    if not ready_state:
        raise HTTPException(status_code=503, detail="Database not ready")

    return HealthReadyResponse(status="ok", database="up")
