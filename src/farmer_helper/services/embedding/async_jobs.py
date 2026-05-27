from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Literal, cast
from uuid import uuid4

from farmer_helper.db.base import SessionLocal, get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.db.models.foundation import EmbeddingAsyncJobRecord
from farmer_helper.repositories.embedding_async_job_repository import EmbeddingAsyncJobRepository
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult


@dataclass
class EmbeddingAsyncJob:
    job_id: str
    status: Literal["queued", "running", "completed", "failed"]
    result: EmbeddingOrchestrationResult | None = None
    error: str | None = None


class EmbeddingAsyncJobStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._bootstrapped = False

    def _ensure_table(self) -> None:
        with self._lock:
            if self._bootstrapped:
                return
            Base.metadata.create_all(bind=get_engine())
            self._bootstrapped = True

    @staticmethod
    def _to_contract(record: EmbeddingAsyncJobRecord) -> EmbeddingAsyncJob:
        result: EmbeddingOrchestrationResult | None = None
        if record.result_json is not None:
            result = EmbeddingOrchestrationResult.model_validate(record.result_json)
        return EmbeddingAsyncJob(
            job_id=record.job_id,
            status=cast(Literal["queued", "running", "completed", "failed"], record.status),
            result=result,
            error=record.error,
        )

    def create(self, *, request_payload: dict[str, object] | None = None) -> EmbeddingAsyncJob:
        self._ensure_table()
        job = EmbeddingAsyncJob(job_id=str(uuid4()), status="queued")
        with SessionLocal() as session:
            repo = EmbeddingAsyncJobRepository(session)
            record = repo.create(job_id=job.job_id, request_payload=request_payload)
        return self._to_contract(record)

    def get(self, job_id: str) -> EmbeddingAsyncJob | None:
        self._ensure_table()
        with SessionLocal() as session:
            repo = EmbeddingAsyncJobRepository(session)
            record = repo.get(job_id)
        if record is None:
            return None
        return self._to_contract(record)

    def mark_running(self, job_id: str) -> None:
        self._ensure_table()
        with SessionLocal() as session:
            repo = EmbeddingAsyncJobRepository(session)
            repo.mark_running(job_id)

    def mark_completed(self, job_id: str, result: EmbeddingOrchestrationResult) -> None:
        self._ensure_table()
        with SessionLocal() as session:
            repo = EmbeddingAsyncJobRepository(session)
            repo.mark_completed(job_id=job_id, result_payload=result.model_dump(mode="json"))

    def mark_failed(self, job_id: str, error: str) -> None:
        self._ensure_table()
        with SessionLocal() as session:
            repo = EmbeddingAsyncJobRepository(session)
            repo.mark_failed(job_id=job_id, error=error)


class QueueCapacityError(RuntimeError):
    pass


class EmbeddingWorkQueue:
    def __init__(self) -> None:
        self._running = 0
        self._lock = Lock()

    def reserve(self, limit: int) -> None:
        with self._lock:
            if self._running >= limit:
                raise QueueCapacityError("Embedding worker queue is at capacity")
            self._running += 1

    def release(self) -> None:
        with self._lock:
            self._running = max(0, self._running - 1)


_job_store = EmbeddingAsyncJobStore()
_work_queue = EmbeddingWorkQueue()


def get_embedding_work_queue() -> EmbeddingWorkQueue:
    return _work_queue


def get_embedding_async_job_store() -> EmbeddingAsyncJobStore:
    return _job_store
