from typing import cast

from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import (
    MessageRole,
    SessionStatus,
    SessionTranscript,
    TranscriptImportRequest,
    TranscriptMessage,
)


class SessionTranscriptService:
    def __init__(self, repository: ChatSessionRepository) -> None:
        """Init for session-memory workflows.

        Initialize SessionTranscriptService for session-memory workflows. Inputs are repository.
        It runs synchronously and returns when local processing is complete. The operation is
        executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository = repository

    def export_transcript(self, session_key: str) -> SessionTranscript:
        """Export transcript for session-memory workflows.

        This SessionTranscriptService method belongs to the session-memory service layer. Inputs
        are session_key. It runs synchronously and returns when local processing is complete.
        Returns a SessionTranscript value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        session = self._repository.get_session_by_key(session_key)
        if session is None:
            raise ValueError(f"Session not found: {session_key}")

        messages = self._repository.list_messages(session_id=session.id)
        transcript_messages = [
            TranscriptMessage(
                turn_index=message.turn_index,
                role=cast(MessageRole, message.role),
                content=message.content,
                metadata=message.metadata_json,
            )
            for message in messages
        ]

        return SessionTranscript(
            session_key=session.session_key,
            user_id=session.user_id,
            title=session.title,
            status=cast(SessionStatus, session.status),
            messages=transcript_messages,
        )

    def import_transcript(self, request: TranscriptImportRequest) -> None:
        """Import transcript for session-memory workflows.

        This SessionTranscriptService method belongs to the session-memory service layer. Inputs
        are request. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        target_key = request.session_key_override or request.transcript.session_key
        if self._repository.get_session_by_key(target_key) is not None:
            raise ValueError(f"Session already exists: {target_key}")

        session = self._repository.create_session(
            session_key=target_key,
            user_id=request.transcript.user_id,
            title=request.transcript.title,
            status=request.transcript.status,
        )

        ordered_messages = sorted(request.transcript.messages, key=lambda item: item.turn_index)
        for message in ordered_messages:
            self._repository.append_message(
                session_id=session.id,
                role=message.role,
                content=message.content,
                metadata=message.metadata,
            )
