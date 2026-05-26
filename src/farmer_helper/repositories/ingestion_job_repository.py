from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import IngestionJob
from farmer_helper.schemas.ingestion import IngestionJobStatus


class IngestionJobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_job(
        self,
        document_id: int,
        status: IngestionJobStatus = "pending",
        metadata: dict[str, str] | None = None,
    ) -> IngestionJob:
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
        return self._session.get(IngestionJob, job_id)

    def update_status(
        self,
        job_id: int,
        status: IngestionJobStatus,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> IngestionJob:
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
