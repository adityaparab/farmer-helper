import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.status_service import IngestionStatusService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_status_service_emits_lifecycle_trace_events(caplog) -> None:
    session = _session()
    repository = IngestionJobRepository(session)
    service = IngestionStatusService(repository)

    caplog.set_level(logging.INFO)

    job_id = service.start_job(document_id=10, metadata={"source": "sample.pdf"})
    service.mark_processing(job_id)
    service.mark_succeeded(job_id)

    messages = [record.getMessage() for record in caplog.records]
    assert "ingestion.job.started" in messages
    assert "ingestion.job.processing" in messages
    assert "ingestion.job.succeeded" in messages

    started_record = next(
        record for record in caplog.records if record.getMessage() == "ingestion.job.started"
    )
    assert started_record.job_id == job_id
    assert started_record.document_id == 10
    assert started_record.ingestion_status == "pending"


def test_status_service_emits_failed_trace_event_with_error_fields(caplog) -> None:
    session = _session()
    repository = IngestionJobRepository(session)
    service = IngestionStatusService(repository)

    caplog.set_level(logging.INFO)

    job_id = service.start_job(document_id=20)
    service.mark_processing(job_id)
    service.mark_failed(
        job_id,
        error_code="INGESTION_PDF_READ_ERROR",
        error_message="decode failure",
    )

    failed_record = next(
        record for record in caplog.records if record.getMessage() == "ingestion.job.failed"
    )
    assert failed_record.job_id == job_id
    assert failed_record.document_id == 20
    assert failed_record.ingestion_status == "failed"
    assert failed_record.error_code == "INGESTION_PDF_READ_ERROR"
    assert failed_record.error_message == "decode failure"
