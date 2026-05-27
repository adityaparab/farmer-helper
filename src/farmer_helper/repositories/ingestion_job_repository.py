from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import IngestionJob
from farmer_helper.schemas.ingestion import IngestionJobStatus


class IngestionJobRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for ingestion-job-repository repository persistence workflows.

        This IngestionJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create_job(
        self,
        document_id: int,
        status: IngestionJobStatus = "pending",
        metadata: dict[str, str] | None = None,
    ) -> IngestionJob:
        """Create job for ingestion-job-repository repository persistence workflows.

        This IngestionJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        document_id, status, metadata. It runs synchronously and returns after local processing
        is complete. It returns IngestionJob for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        job = IngestionJob(
            document_id=document_id,
            status=status,
            metadata_json=metadata,
        )
        self._session.add(job)
        self._session.commit()
        self._session.refresh(job)
        return job

    def get_job(self, job_id: int) -> IngestionJob | None:
        """Retrieve job for ingestion-job-repository repository persistence workflows.

        This IngestionJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        job_id. It runs synchronously and returns after local processing is complete. It returns
        IngestionJob | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        return self._session.get(IngestionJob, job_id)

    def update_status(
        self,
        job_id: int,
        status: IngestionJobStatus,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> IngestionJob:
        """Update status for ingestion-job-repository repository persistence workflows.

        This IngestionJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        job_id, status, error_code, error_message. It runs synchronously and returns after local
        processing is complete. It returns IngestionJob for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        job = self._session.get(IngestionJob, job_id)
        if job is None:
            raise ValueError(f"Ingestion job not found: {job_id}")

        job.status = status
        job.error_code = error_code
        job.error_message = error_message

        self._session.add(job)
        self._session.commit()
        self._session.refresh(job)
        return job
