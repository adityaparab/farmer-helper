from farmer_helper.db.models.foundation import IngestionJob
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.services.ingestion.trace_logger import IngestionTraceLogger


class IngestionStatusService:
    def __init__(
        self,
        repository: IngestionJobRepository,
        trace_logger: IngestionTraceLogger | None = None,
    ) -> None:
        """Init for ingestion workflows.

        Initialize IngestionStatusService for ingestion workflows. Inputs are repository,
        trace_logger. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository = repository
        self._trace_logger = trace_logger or IngestionTraceLogger()

    def start_job(self, document_id: int, metadata: dict[str, str] | None = None) -> int:
        """Start job for ingestion workflows.

        This IngestionStatusService method belongs to the ingestion service layer. Inputs are
        document_id, metadata. It runs synchronously and returns when local processing is
        complete. Returns a int value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        job = self._repository.create_job(
            document_id=document_id,
            status="pending",
            metadata=metadata,
        )
        self._trace_logger.job_started(job_id=job.id, document_id=job.document_id)
        return job.id

    def mark_processing(self, job_id: int) -> None:
        """Mark processing for ingestion workflows.

        This IngestionStatusService method belongs to the ingestion service layer. Inputs are
        job_id. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        job = self._require(job_id)
        if job.status != "pending":
            raise ValueError(f"Invalid transition from {job.status} to processing")
        self._repository.update_status(job_id, "processing")
        self._trace_logger.processing_started(job_id=job.id, document_id=job.document_id)

    def mark_succeeded(self, job_id: int) -> None:
        """Mark succeeded for ingestion workflows.

        This IngestionStatusService method belongs to the ingestion service layer. Inputs are
        job_id. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        job = self._require(job_id)
        if job.status != "processing":
            raise ValueError(f"Invalid transition from {job.status} to succeeded")
        self._repository.update_status(job_id, "succeeded")
        self._trace_logger.job_succeeded(job_id=job.id, document_id=job.document_id)

    def mark_failed(self, job_id: int, error_code: str, error_message: str) -> None:
        """Mark failed for ingestion workflows.

        This IngestionStatusService method belongs to the ingestion service layer. Inputs are
        job_id, error_code, error_message. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
        """Require for ingestion workflows.

        This private helper belongs to the ingestion service layer. Inputs are job_id. It runs
        synchronously and returns when local processing is complete. Returns a IngestionJob
        value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        job = self._repository.get_job(job_id)
        if job is None:
            raise ValueError(f"Ingestion job not found: {job_id}")
        return job
