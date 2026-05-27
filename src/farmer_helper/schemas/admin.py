from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

AdminJobStatus = Literal["pending", "processing", "succeeded", "failed"]
GoldAnswerStatus = Literal["draft", "approved", "archived"]
QaReviewStatus = Literal["pending", "in_review", "resolved"]


class AdminIngestionJobCreateRequest(BaseModel):
    source_path: str = Field(min_length=1, max_length=512)
    content_hash: str = Field(min_length=1, max_length=128)
    content_version: str = Field(min_length=1, max_length=64, default="v1")
    metadata: dict[str, str] | None = None


class AdminReindexJobCreateRequest(BaseModel):
    document_id: int = Field(ge=1)
    pipeline_version: str = Field(min_length=1, max_length=64, default="v1")
    model_version: str = Field(min_length=1, max_length=128, default="mock-embedding-v1")


class AdminJobResponse(BaseModel):
    job_id: int
    document_id: int
    status: AdminJobStatus


class AdminPdfUploadResponse(BaseModel):
    job_id: int
    document_id: int
    status: AdminJobStatus
    source_path: str
    content_hash: str
    size_bytes: int
    document_created: bool


class AdminJobStatusUpdateRequest(BaseModel):
    status: AdminJobStatus
    error_code: str | None = None
    error_message: str | None = None


class VersionTrackingCreateRequest(BaseModel):
    content_version: str = Field(min_length=1, max_length=64)
    model_version: str = Field(min_length=1, max_length=128)
    pipeline_version: str = Field(min_length=1, max_length=64)
    notes: str | None = None


class VersionTrackingResponse(BaseModel):
    id: int
    content_version: str
    model_version: str
    pipeline_version: str
    notes: str | None
    created_by: str | None
    created_at: datetime


class GoldAnswerCreateRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    answer: str = Field(min_length=1, max_length=4000)
    metadata: dict[str, str] | None = None


class GoldAnswerUpdateRequest(BaseModel):
    status: GoldAnswerStatus
    answer: str | None = None


class GoldAnswerResponse(BaseModel):
    id: int
    question: str
    answer: str
    status: GoldAnswerStatus
    editor_id: str | None
    metadata: dict[str, str] | None
    created_at: datetime
    updated_at: datetime


class QaReviewCreateRequest(BaseModel):
    document_id: int | None = Field(default=None, ge=1)
    source_path: str | None = Field(default=None, max_length=512)
    issue_type: str = Field(min_length=1, max_length=64)
    details: str = Field(min_length=1, max_length=2000)


class QaReviewUpdateRequest(BaseModel):
    status: QaReviewStatus
    assigned_to: str | None = Field(default=None, max_length=128)
    resolution_notes: str | None = Field(default=None, max_length=2000)


class QaReviewResponse(BaseModel):
    id: int
    document_id: int | None
    source_path: str | None
    issue_type: str
    details: str
    status: QaReviewStatus
    assigned_to: str | None
    resolution_notes: str | None
    created_at: datetime
    updated_at: datetime


class AccessAuditLogResponse(BaseModel):
    id: int
    actor_id: str
    action: str
    target_type: str
    target_id: str
    request_id: str | None
    details: dict[str, str] | None
    created_at: datetime


class AdminDashboardMetricCard(BaseModel):
    label: str
    value: int


class AdminDashboardMetricsResponse(BaseModel):
    cards: list[AdminDashboardMetricCard]
    ingestion_jobs_by_status: dict[str, int]
    chat_sessions_by_status: dict[str, int]
    gold_answers_by_status: dict[str, int]
    qa_review_items_by_status: dict[str, int]
    embedding_jobs_by_status: dict[str, int]
