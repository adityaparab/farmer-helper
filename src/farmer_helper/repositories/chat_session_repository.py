from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import ChatMessage, ChatSession


class ChatSessionRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def create_session(
        self,
        session_key: str,
        user_id: str | None = None,
        title: str | None = None,
        status: str = "active",
    ) -> ChatSession:
        """Create session for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_key, user_id, title, status. It runs synchronously and returns after local
        processing is complete. It returns ChatSession for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = ChatSession(
            session_key=session_key,
            user_id=user_id,
            title=title,
            status=status,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def get_session_by_key(self, session_key: str) -> ChatSession | None:
        """Retrieve session by key for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_key. It runs synchronously and returns after local processing is complete. It
        returns ChatSession | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(ChatSession).where(ChatSession.session_key == session_key)
        return self._session.scalar(stmt)

    def update_session_status(self, session_id: int, status: str) -> ChatSession:
        """Update session status for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_id, status. It runs synchronously and returns after local processing is
        complete. It returns ChatSession for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = self._session.get(ChatSession, session_id)
        if record is None:
            raise ValueError(f"Chat session not found: {session_id}")

        record.status = status
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def archive_session(self, session_key: str) -> ChatSession:
        """Archive session for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_key. It runs synchronously and returns after local processing is complete. It
        returns ChatSession for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        record = self.get_session_by_key(session_key)
        if record is None:
            raise ValueError(f"Chat session not found: {session_key}")
        return self.update_session_status(session_id=record.id, status="archived")

    def expire_active_sessions(self, updated_before: datetime) -> int:
        """Expire active sessions for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        updated_before. It runs synchronously and returns after local processing is complete. It
        returns int for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(ChatSession).where(
            ChatSession.status == "active",
            ChatSession.updated_at < updated_before,
        )
        candidates = list(self._session.scalars(stmt))
        for record in candidates:
            record.status = "expired"
            self._session.add(record)

        self._session.commit()
        return len(candidates)

    def append_message(
        self,
        session_id: int,
        role: str,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> ChatMessage:
        """Append message for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_id, role, content, metadata. It runs synchronously and returns after local
        processing is complete. It returns ChatMessage for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        turn_index = self._next_turn_index(session_id)
        record = ChatMessage(
            session_id=session_id,
            turn_index=turn_index,
            role=role,
            content=content,
            metadata_json=metadata,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def list_messages(self, session_id: int) -> list[ChatMessage]:
        """List messages for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_id. It runs synchronously and returns after local processing is complete. It
        returns list[ChatMessage] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.turn_index.asc())
        )
        return list(self._session.scalars(stmt))

    def _next_turn_index(self, session_id: int) -> int:
        """Next turn index for chat-session-repository repository persistence workflows.

        This ChatSessionRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session_id. It runs synchronously and returns after local processing is complete. It
        returns int for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(func.max(ChatMessage.turn_index)).where(ChatMessage.session_id == session_id)
        current_max = self._session.scalar(stmt)
        if current_max is None:
            return 0
        return int(current_max) + 1
