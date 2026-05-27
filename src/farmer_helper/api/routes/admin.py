from typing import cast

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.admin_repository import (
    AccessAuditLogRepository,
    AdminJobRepository,
    GoldAnswerRepository,
    QaReviewRepository,
    VersionTrackingRepository,
)
from farmer_helper.repositories.document_repository import DocumentRepository
from farmer_helper.repositories.ingestion_job_repository import IngestionJobRepository
from farmer_helper.schemas.admin import (
    AccessAuditLogResponse,
    AdminIngestionJobCreateRequest,
    AdminJobResponse,
    AdminJobStatus,
    AdminJobStatusUpdateRequest,
    AdminReindexJobCreateRequest,
    GoldAnswerCreateRequest,
    GoldAnswerResponse,
    GoldAnswerStatus,
    GoldAnswerUpdateRequest,
    QaReviewCreateRequest,
    QaReviewResponse,
    QaReviewStatus,
    QaReviewUpdateRequest,
    VersionTrackingCreateRequest,
    VersionTrackingResponse,
)
from farmer_helper.services.ingestion.status_service import IngestionStatusService
from farmer_helper.services.ingestion.trace_logger import IngestionTraceLogger

router = APIRouter(prefix="/admin", tags=["admin"])


def _actor_id(x_actor_id: str | None) -> str:
    return (x_actor_id or "system").strip() or "system"


def _audit(
    *,
    db: Session,
    request: Request,
    actor_id: str,
    action: str,
    target_type: str,
    target_id: str,
    details: dict[str, str] | None = None,
) -> None:
    AccessAuditLogRepository(db).create(
        actor_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        request_id=request.headers.get("x-request-id"),
        details=details,
    )


@router.post("/ingestion/jobs", response_model=AdminJobResponse, status_code=201)
def create_ingestion_job(
    payload: AdminIngestionJobCreateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> AdminJobResponse:  # noqa: B008
    document = DocumentRepository(db).create(
        source_path=payload.source_path,
        content_hash=payload.content_hash,
        version=payload.content_version,
    )
    status_service = IngestionStatusService(
        repository=IngestionJobRepository(db),
        trace_logger=IngestionTraceLogger(),
    )
    job_id = status_service.start_job(document_id=document.id, metadata=payload.metadata)

    actor = _actor_id(x_actor_id)
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.ingestion.start",
        target_type="ingestion_job",
        target_id=str(job_id),
        details={"document_id": str(document.id)},
    )

    return AdminJobResponse(job_id=job_id, document_id=document.id, status="pending")


@router.post("/reindex/jobs", response_model=AdminJobResponse, status_code=201)
def create_reindex_job(
    payload: AdminReindexJobCreateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> AdminJobResponse:  # noqa: B008
    status_service = IngestionStatusService(
        repository=IngestionJobRepository(db),
        trace_logger=IngestionTraceLogger(),
    )
    job_id = status_service.start_job(
        document_id=payload.document_id,
        metadata={
            "workflow": "reindex",
            "pipeline_version": payload.pipeline_version,
            "model_version": payload.model_version,
        },
    )

    actor = _actor_id(x_actor_id)
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.reindex.start",
        target_type="ingestion_job",
        target_id=str(job_id),
        details={"document_id": str(payload.document_id)},
    )

    return AdminJobResponse(job_id=job_id, document_id=payload.document_id, status="pending")


@router.post("/jobs/{job_id}/status", response_model=AdminJobResponse)
def update_job_status(
    job_id: int,
    payload: AdminJobStatusUpdateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> AdminJobResponse:  # noqa: B008
    status_service = IngestionStatusService(
        repository=IngestionJobRepository(db),
        trace_logger=IngestionTraceLogger(),
    )
    if payload.status == "processing":
        status_service.mark_processing(job_id)
    elif payload.status == "succeeded":
        status_service.mark_succeeded(job_id)
    elif payload.status == "failed":
        if payload.error_code is None or payload.error_message is None:
            raise HTTPException(
                status_code=400,
                detail="error_code and error_message are required for failed status",
            )
        status_service.mark_failed(job_id, payload.error_code, payload.error_message)
    elif payload.status == "pending":
        raise HTTPException(status_code=400, detail="Cannot transition back to pending")

    repo = AdminJobRepository(db)
    job = repo.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")

    actor = _actor_id(x_actor_id)
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.job.status_update",
        target_type="ingestion_job",
        target_id=str(job_id),
        details={"status": payload.status},
    )

    return AdminJobResponse(
        job_id=job.id,
        document_id=job.document_id,
        status=cast(AdminJobStatus, job.status),
    )


@router.post("/versions", response_model=VersionTrackingResponse, status_code=201)
def create_version_tracking_record(
    payload: VersionTrackingCreateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> VersionTrackingResponse:  # noqa: B008
    actor = _actor_id(x_actor_id)
    record = VersionTrackingRepository(db).create(
        content_version=payload.content_version,
        model_version=payload.model_version,
        pipeline_version=payload.pipeline_version,
        notes=payload.notes,
        created_by=actor,
    )
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.version.create",
        target_type="version_record",
        target_id=str(record.id),
    )

    return VersionTrackingResponse(
        id=record.id,
        content_version=record.content_version,
        model_version=record.model_version,
        pipeline_version=record.pipeline_version,
        notes=record.notes,
        created_by=record.created_by,
        created_at=record.created_at,
    )


@router.get("/versions", response_model=list[VersionTrackingResponse])
def list_version_tracking_records(
    db: Session = Depends(get_db_session),
) -> list[VersionTrackingResponse]:  # noqa: B008
    records = VersionTrackingRepository(db).list_recent()
    return [
        VersionTrackingResponse(
            id=item.id,
            content_version=item.content_version,
            model_version=item.model_version,
            pipeline_version=item.pipeline_version,
            notes=item.notes,
            created_by=item.created_by,
            created_at=item.created_at,
        )
        for item in records
    ]


@router.post("/gold-answers", response_model=GoldAnswerResponse, status_code=201)
def create_gold_answer(
    payload: GoldAnswerCreateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> GoldAnswerResponse:  # noqa: B008
    actor = _actor_id(x_actor_id)
    item = GoldAnswerRepository(db).create(
        question=payload.question,
        answer=payload.answer,
        metadata=payload.metadata,
        editor_id=actor,
    )
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.gold_answer.create",
        target_type="gold_answer",
        target_id=str(item.id),
    )

    return GoldAnswerResponse(
        id=item.id,
        question=item.question,
        answer=item.answer,
        status=cast(GoldAnswerStatus, item.status),
        editor_id=item.editor_id,
        metadata=item.metadata_json,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.post("/gold-answers/{answer_id}", response_model=GoldAnswerResponse)
def update_gold_answer(
    answer_id: int,
    payload: GoldAnswerUpdateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> GoldAnswerResponse:  # noqa: B008
    actor = _actor_id(x_actor_id)
    try:
        item = GoldAnswerRepository(db).update(
            answer_id=answer_id,
            status=payload.status,
            editor_id=actor,
            answer_text=payload.answer,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.gold_answer.update",
        target_type="gold_answer",
        target_id=str(item.id),
        details={"status": item.status},
    )

    return GoldAnswerResponse(
        id=item.id,
        question=item.question,
        answer=item.answer,
        status=cast(GoldAnswerStatus, item.status),
        editor_id=item.editor_id,
        metadata=item.metadata_json,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.get("/gold-answers", response_model=list[GoldAnswerResponse])
def list_gold_answers(
    db: Session = Depends(get_db_session),
) -> list[GoldAnswerResponse]:  # noqa: B008
    records = GoldAnswerRepository(db).list_recent()
    return [
        GoldAnswerResponse(
            id=item.id,
            question=item.question,
            answer=item.answer,
            status=cast(GoldAnswerStatus, item.status),
            editor_id=item.editor_id,
            metadata=item.metadata_json,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in records
    ]


@router.post("/review-queue", response_model=QaReviewResponse, status_code=201)
def create_review_queue_item(
    payload: QaReviewCreateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> QaReviewResponse:  # noqa: B008
    actor = _actor_id(x_actor_id)
    item = QaReviewRepository(db).create(
        document_id=payload.document_id,
        source_path=payload.source_path,
        issue_type=payload.issue_type,
        details=payload.details,
    )
    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.review_queue.create",
        target_type="review_queue_item",
        target_id=str(item.id),
    )

    return QaReviewResponse(
        id=item.id,
        document_id=item.document_id,
        source_path=item.source_path,
        issue_type=item.issue_type,
        details=item.details,
        status=cast(QaReviewStatus, item.status),
        assigned_to=item.assigned_to,
        resolution_notes=item.resolution_notes,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.post("/review-queue/{item_id}", response_model=QaReviewResponse)
def update_review_queue_item(
    item_id: int,
    payload: QaReviewUpdateRequest,
    request: Request,
    db: Session = Depends(get_db_session),
    x_actor_id: str | None = Header(default=None),
) -> QaReviewResponse:  # noqa: B008
    actor = _actor_id(x_actor_id)
    try:
        item = QaReviewRepository(db).update(
            item_id=item_id,
            status=payload.status,
            assigned_to=payload.assigned_to,
            resolution_notes=payload.resolution_notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    _audit(
        db=db,
        request=request,
        actor_id=actor,
        action="admin.review_queue.update",
        target_type="review_queue_item",
        target_id=str(item.id),
        details={"status": item.status},
    )

    return QaReviewResponse(
        id=item.id,
        document_id=item.document_id,
        source_path=item.source_path,
        issue_type=item.issue_type,
        details=item.details,
        status=cast(QaReviewStatus, item.status),
        assigned_to=item.assigned_to,
        resolution_notes=item.resolution_notes,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.get("/review-queue", response_model=list[QaReviewResponse])
def list_review_queue_items(
    db: Session = Depends(get_db_session),
) -> list[QaReviewResponse]:  # noqa: B008
    records = QaReviewRepository(db).list_recent()
    return [
        QaReviewResponse(
            id=item.id,
            document_id=item.document_id,
            source_path=item.source_path,
            issue_type=item.issue_type,
            details=item.details,
            status=cast(QaReviewStatus, item.status),
            assigned_to=item.assigned_to,
            resolution_notes=item.resolution_notes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in records
    ]


@router.get("/access-audit", response_model=list[AccessAuditLogResponse])
def list_access_audit_logs(
    db: Session = Depends(get_db_session),
) -> list[AccessAuditLogResponse]:  # noqa: B008
    records = AccessAuditLogRepository(db).list_recent()
    return [
        AccessAuditLogResponse(
            id=item.id,
            actor_id=item.actor_id,
            action=item.action,
            target_type=item.target_type,
            target_id=item.target_id,
            request_id=item.request_id,
            details=item.details_json,
            created_at=item.created_at,
        )
        for item in records
    ]
