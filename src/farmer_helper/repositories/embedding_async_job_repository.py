from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import EmbeddingAsyncJobRecord


class EmbeddingAsyncJobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self, *, job_id: str, request_payload: dict[str, object] | None
    ) -> EmbeddingAsyncJobRecord:
        record = EmbeddingAsyncJobRecord(
            job_id=job_id,
            status="queued",
            request_json=request_payload,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def get(self, job_id: str) -> EmbeddingAsyncJobRecord | None:
        return self._session.get(EmbeddingAsyncJobRecord, job_id)

    def mark_running(self, job_id: str) -> EmbeddingAsyncJobRecord:
        record = self._session.get(EmbeddingAsyncJobRecord, job_id)
        if record is None:
            raise ValueError(f"Embedding job not found: {job_id}")

        record.status = "running"
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def mark_completed(
        self,
        *,
        job_id: str,
        result_payload: dict[str, object],
    ) -> EmbeddingAsyncJobRecord:
        record = self._session.get(EmbeddingAsyncJobRecord, job_id)
        if record is None:
            raise ValueError(f"Embedding job not found: {job_id}")

        record.status = "completed"
        record.result_json = result_payload
        record.error = None
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def mark_failed(self, *, job_id: str, error: str) -> EmbeddingAsyncJobRecord:
        record = self._session.get(EmbeddingAsyncJobRecord, job_id)
        if record is None:
            raise ValueError(f"Embedding job not found: {job_id}")

        record.status = "failed"
        record.error = error
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record
