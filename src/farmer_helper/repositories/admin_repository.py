from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import (
    AccessAuditLog,
    GoldAnswerRecord,
    IngestionJob,
    QaReviewQueueItem,
    VersionTrackingRecord,
)


class VersionTrackingRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for admin-repository repository persistence workflows.

        This VersionTrackingRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create(
        self,
        *,
        content_version: str,
        model_version: str,
        pipeline_version: str,
        notes: str | None,
        created_by: str | None,
    ) -> VersionTrackingRecord:
        """Create for admin-repository repository persistence workflows.

        This VersionTrackingRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are content_version, model_version, pipeline_version, notes, created_by. It runs
        synchronously and returns after local processing is complete. It returns
        VersionTrackingRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = VersionTrackingRecord(
            content_version=content_version,
            model_version=model_version,
            pipeline_version=pipeline_version,
            notes=notes,
            created_by=created_by,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def list_recent(self, limit: int = 50) -> list[VersionTrackingRecord]:
        """List recent for admin-repository repository persistence workflows.

        This VersionTrackingRepository method documents a stable application boundary used by
        API handlers, service orchestration, validation, persistence, or runtime setup. Inputs
        are limit. It runs synchronously and returns after local processing is complete. It
        returns list[VersionTrackingRecord] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(VersionTrackingRecord).order_by(VersionTrackingRecord.id.desc()).limit(limit)
        return list(self._session.scalars(stmt).all())


class GoldAnswerRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for admin-repository repository persistence workflows.

        This GoldAnswerRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create(
        self,
        *,
        question: str,
        answer: str,
        metadata: dict[str, str] | None,
        editor_id: str | None,
    ) -> GoldAnswerRecord:
        """Create for admin-repository repository persistence workflows.

        This GoldAnswerRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        question, answer, metadata, editor_id. It runs synchronously and returns after local
        processing is complete. It returns GoldAnswerRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = GoldAnswerRecord(
            question=question,
            answer=answer,
            status="draft",
            metadata_json=metadata,
            editor_id=editor_id,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def get(self, answer_id: int) -> GoldAnswerRecord | None:
        """Retrieve for admin-repository repository persistence workflows.

        This GoldAnswerRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        answer_id. It runs synchronously and returns after local processing is complete. It
        returns GoldAnswerRecord | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        return self._session.get(GoldAnswerRecord, answer_id)

    def update(
        self,
        *,
        answer_id: int,
        status: str,
        editor_id: str | None,
        answer_text: str | None,
    ) -> GoldAnswerRecord:
        """Update for admin-repository repository persistence workflows.

        This GoldAnswerRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        answer_id, status, editor_id, answer_text. It runs synchronously and returns after local
        processing is complete. It returns GoldAnswerRecord for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = self._session.get(GoldAnswerRecord, answer_id)
        if record is None:
            raise ValueError(f"Gold answer not found: {answer_id}")

        record.status = status
        record.editor_id = editor_id
        if answer_text is not None:
            record.answer = answer_text

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def list_recent(self, limit: int = 50) -> list[GoldAnswerRecord]:
        """List recent for admin-repository repository persistence workflows.

        This GoldAnswerRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        limit. It runs synchronously and returns after local processing is complete. It returns
        list[GoldAnswerRecord] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(GoldAnswerRecord).order_by(GoldAnswerRecord.id.desc()).limit(limit)
        return list(self._session.scalars(stmt).all())


class QaReviewRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for admin-repository repository persistence workflows.

        This QaReviewRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create(
        self,
        *,
        document_id: int | None,
        source_path: str | None,
        issue_type: str,
        details: str,
    ) -> QaReviewQueueItem:
        """Create for admin-repository repository persistence workflows.

        This QaReviewRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        document_id, source_path, issue_type, details. It runs synchronously and returns after
        local processing is complete. It returns QaReviewQueueItem for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        item = QaReviewQueueItem(
            document_id=document_id,
            source_path=source_path,
            issue_type=issue_type,
            details=details,
            status="pending",
        )
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def update(
        self,
        *,
        item_id: int,
        status: str,
        assigned_to: str | None,
        resolution_notes: str | None,
    ) -> QaReviewQueueItem:
        """Update for admin-repository repository persistence workflows.

        This QaReviewRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        item_id, status, assigned_to, resolution_notes. It runs synchronously and returns after
        local processing is complete. It returns QaReviewQueueItem for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        item = self._session.get(QaReviewQueueItem, item_id)
        if item is None:
            raise ValueError(f"Review queue item not found: {item_id}")

        item.status = status
        item.assigned_to = assigned_to
        item.resolution_notes = resolution_notes

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def list_recent(self, limit: int = 100) -> list[QaReviewQueueItem]:
        """List recent for admin-repository repository persistence workflows.

        This QaReviewRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        limit. It runs synchronously and returns after local processing is complete. It returns
        list[QaReviewQueueItem] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(QaReviewQueueItem).order_by(QaReviewQueueItem.id.desc()).limit(limit)
        return list(self._session.scalars(stmt).all())


class AccessAuditLogRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for admin-repository repository persistence workflows.

        This AccessAuditLogRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create(
        self,
        *,
        actor_id: str,
        action: str,
        target_type: str,
        target_id: str,
        request_id: str | None,
        details: dict[str, str] | None,
    ) -> AccessAuditLog:
        """Create for admin-repository repository persistence workflows.

        This AccessAuditLogRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        actor_id, action, target_type, target_id, request_id, details. It runs synchronously and
        returns after local processing is complete. It returns AccessAuditLog for downstream
        callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        item = AccessAuditLog(
            actor_id=actor_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            request_id=request_id,
            details_json=details,
        )
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def list_recent(self, limit: int = 100) -> list[AccessAuditLog]:
        """List recent for admin-repository repository persistence workflows.

        This AccessAuditLogRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        limit. It runs synchronously and returns after local processing is complete. It returns
        list[AccessAuditLog] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(AccessAuditLog).order_by(AccessAuditLog.id.desc()).limit(limit)
        return list(self._session.scalars(stmt).all())


class AdminJobRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for admin-repository repository persistence workflows.

        This AdminJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def get(self, job_id: int) -> IngestionJob | None:
        """Retrieve for admin-repository repository persistence workflows.

        This AdminJobRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        job_id. It runs synchronously and returns after local processing is complete. It returns
        IngestionJob | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        return self._session.get(IngestionJob, job_id)
