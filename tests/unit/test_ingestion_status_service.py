import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.status_service import IngestionStatusService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_status_service_success_path() -> None:
    session = _session()
    repository = IngestionJobRepository(session)
    service = IngestionStatusService(repository)

    job_id = service.start_job(document_id=1, metadata={"source": "sample.pdf"})
    service.mark_processing(job_id)
    service.mark_succeeded(job_id)

    job = repository.get_job(job_id)
    assert job is not None
    assert job.status == "succeeded"
    assert job.error_code is None


def test_status_service_failure_path_persists_error() -> None:
    session = _session()
    repository = IngestionJobRepository(session)
    service = IngestionStatusService(repository)

    job_id = service.start_job(document_id=2)
    service.mark_failed(
        job_id,
        error_code="INGESTION_PDF_READ_ERROR",
        error_message="decode failure",
    )

    job = repository.get_job(job_id)
    assert job is not None
    assert job.status == "failed"
    assert job.error_code == "INGESTION_PDF_READ_ERROR"
    assert job.error_message == "decode failure"


def test_status_service_rejects_invalid_transition() -> None:
    session = _session()
    repository = IngestionJobRepository(session)
    service = IngestionStatusService(repository)

    job_id = service.start_job(document_id=3)
    service.mark_failed(job_id, error_code="X", error_message="Y")

    with pytest.raises(ValueError) as exc:
        service.mark_succeeded(job_id)
    assert "Invalid transition" in str(exc.value)
