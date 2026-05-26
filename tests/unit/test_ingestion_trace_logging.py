import logging
from logging import LogRecord

from pytest import LogCaptureFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.status_service import IngestionStatusService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


def _record_int(record: LogRecord, key: str) -> int:
    value = record.__dict__.get(key)
    if not isinstance(value, int):
        raise AssertionError(f"Expected int '{key}' in log record")
    return value


def _record_str(record: LogRecord, key: str) -> str:
    value = record.__dict__.get(key)
    if not isinstance(value, str):
        raise AssertionError(f"Expected str '{key}' in log record")
    return value


def test_status_service_emits_lifecycle_trace_events(caplog: LogCaptureFixture) -> None:
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

    started_record = _find_record(caplog.records, "ingestion.job.started")
    assert _record_int(started_record, "job_id") == job_id
    assert _record_int(started_record, "document_id") == 10
    assert _record_str(started_record, "ingestion_status") == "pending"


def test_status_service_emits_failed_trace_event_with_error_fields(
    caplog: LogCaptureFixture,
) -> None:
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

    failed_record = _find_record(caplog.records, "ingestion.job.failed")
    assert _record_int(failed_record, "job_id") == job_id
    assert _record_int(failed_record, "document_id") == 20
    assert _record_str(failed_record, "ingestion_status") == "failed"
    assert _record_str(failed_record, "error_code") == "INGESTION_PDF_READ_ERROR"
    assert _record_str(failed_record, "error_message") == "decode failure"
