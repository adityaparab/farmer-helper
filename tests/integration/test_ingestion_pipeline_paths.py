from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.db.models.foundation import IngestionJob
from farmer_helper.repositories.document_repository import DocumentRepository
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.file_validator import FileValidator, IngestionValidationError
from farmer_helper.services.ingestion.idempotency_service import IngestionIdempotencyService
from farmer_helper.services.ingestion.status_service import IngestionStatusService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_reingestion_reuses_document_and_completes_jobs() -> None:
    session = _session()
    document_repository = DocumentRepository(session)
    job_repository = IngestionJobRepository(session)
    idempotency = IngestionIdempotencyService(document_repository)
    status = IngestionStatusService(job_repository)

    first_doc = idempotency.ensure_document(
        source_path="docs/guide-v1.pdf",
        content_hash="same-hash",
        version="v1",
    )
    first_job_id = status.start_job(document_id=first_doc.document_id)
    status.mark_processing(first_job_id)
    status.mark_succeeded(first_job_id)

    second_doc = idempotency.ensure_document(
        source_path="docs/guide-v1-copy.pdf",
        content_hash="same-hash",
        version="v1",
    )
    second_job_id = status.start_job(document_id=second_doc.document_id)
    status.mark_processing(second_job_id)
    status.mark_succeeded(second_job_id)

    assert first_doc.document_id == second_doc.document_id
    assert second_doc.created is False

    jobs = session.scalars(select(IngestionJob).order_by(IngestionJob.id)).all()
    assert len(jobs) == 2
    assert jobs[0].status == "succeeded"
    assert jobs[1].status == "succeeded"


def test_failure_path_marks_job_failed_on_validation_error() -> None:
    session = _session()
    document_repository = DocumentRepository(session)
    job_repository = IngestionJobRepository(session)
    idempotency = IngestionIdempotencyService(document_repository)
    status = IngestionStatusService(job_repository)
    validator = FileValidator()

    doc = idempotency.ensure_document(
        source_path="docs/invalid.pdf",
        content_hash="missing-file-hash",
        version="v1",
    )
    job_id = status.start_job(document_id=doc.document_id)
    status.mark_processing(job_id)

    try:
        validator.validate("does-not-exist.pdf")
    except IngestionValidationError as exc:
        status.mark_failed(job_id, error_code=exc.code, error_message=exc.message)

    job = job_repository.get_job(job_id)
    assert job is not None
    assert job.status == "failed"
    assert job.error_code == "INGESTION_INPUT_NOT_FOUND"
