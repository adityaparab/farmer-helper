from farmer_helper.db.models.foundation import IngestionJob
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.trace_logger import IngestionTraceLogger


class IngestionStatusService:
    def __init__(
        self,
        repository: IngestionJobRepository,
        trace_logger: IngestionTraceLogger | None = None,
    ) -> None:
        self._repository = repository
        self._trace_logger = trace_logger or IngestionTraceLogger()

    def start_job(self, document_id: int, metadata: dict[str, str] | None = None) -> int:
        job = self._repository.create_job(
            document_id=document_id,
            status="pending",
            metadata=metadata,
        )
        self._trace_logger.job_started(job_id=job.id, document_id=job.document_id)
        return job.id

    def mark_processing(self, job_id: int) -> None:
        job = self._require(job_id)
        if job.status != "pending":
            raise ValueError(f"Invalid transition from {job.status} to processing")
        self._repository.update_status(job_id, "processing")
        self._trace_logger.processing_started(job_id=job.id, document_id=job.document_id)

    def mark_succeeded(self, job_id: int) -> None:
        job = self._require(job_id)
        if job.status != "processing":
            raise ValueError(f"Invalid transition from {job.status} to succeeded")
        self._repository.update_status(job_id, "succeeded")
        self._trace_logger.job_succeeded(job_id=job.id, document_id=job.document_id)

    def mark_failed(self, job_id: int, error_code: str, error_message: str) -> None:
        job = self._require(job_id)
        if job.status not in {"pending", "processing"}:
            raise ValueError(f"Invalid transition from {job.status} to failed")
        self._repository.update_status(
            job_id,
            "failed",
            error_code=error_code,
            error_message=error_message,
        )
        self._trace_logger.job_failed(
            job_id=job.id,
            document_id=job.document_id,
            error_code=error_code,
            error_message=error_message,
        )

    def _require(self, job_id: int) -> IngestionJob:
        job = self._repository.get_job(job_id)
        if job is None:
            raise ValueError(f"Ingestion job not found: {job_id}")
        return job
