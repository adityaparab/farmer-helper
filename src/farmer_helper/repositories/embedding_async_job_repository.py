from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import EmbeddingAsyncJobRecord


class EmbeddingAsyncJobRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for embedding-async-job-repository repository persistence
        workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create(
        self, *, job_id: str, request_payload: dict[str, object] | None
    ) -> EmbeddingAsyncJobRecord:
        """Create for embedding-async-job-repository repository persistence workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are job_id, request_payload. It runs synchronously and returns after local processing is
        complete. It returns EmbeddingAsyncJobRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
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
        """Retrieve for embedding-async-job-repository repository persistence workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are job_id. It runs synchronously and returns after local processing is complete. It
        returns EmbeddingAsyncJobRecord | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        return self._session.get(EmbeddingAsyncJobRecord, job_id)

    def mark_running(self, job_id: str) -> EmbeddingAsyncJobRecord:
        """Mark running for embedding-async-job-repository repository persistence workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are job_id. It runs synchronously and returns after local processing is complete. It
        returns EmbeddingAsyncJobRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
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
        """Mark completed for embedding-async-job-repository repository persistence workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are job_id, result_payload. It runs synchronously and returns after local processing is
        complete. It returns EmbeddingAsyncJobRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
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
        """Mark failed for embedding-async-job-repository repository persistence workflows.

        This EmbeddingAsyncJobRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are job_id, error. It runs synchronously and returns after local processing is complete.
        It returns EmbeddingAsyncJobRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = self._session.get(EmbeddingAsyncJobRecord, job_id)
        if record is None:
            raise ValueError(f"Embedding job not found: {job_id}")

        record.status = "failed"
        record.error = error
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record
