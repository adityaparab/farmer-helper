from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Literal
from uuid import uuid4

from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult


@dataclass
class EmbeddingAsyncJob:
    job_id: str
    status: Literal["queued", "running", "completed", "failed"]
    result: EmbeddingOrchestrationResult | None = None
    error: str | None = None


class EmbeddingAsyncJobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, EmbeddingAsyncJob] = {}
        self._lock = Lock()

    def create(self) -> EmbeddingAsyncJob:
        job = EmbeddingAsyncJob(job_id=str(uuid4()), status="queued")
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get(self, job_id: str) -> EmbeddingAsyncJob | None:
        with self._lock:
            return self._jobs.get(job_id)

    def mark_running(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.status = "running"

    def mark_completed(self, job_id: str, result: EmbeddingOrchestrationResult) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.status = "completed"
            job.result = result

    def mark_failed(self, job_id: str, error: str) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.status = "failed"
            job.error = error


_job_store = EmbeddingAsyncJobStore()


def get_embedding_async_job_store() -> EmbeddingAsyncJobStore:
    return _job_store
