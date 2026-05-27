from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import SessionSummaryRequest, SessionSummaryResponse


class SessionSummarizer:
    def __init__(self, repository: ChatSessionRepository) -> None:
        self._repository = repository

    def summarize(self, request: SessionSummaryRequest) -> SessionSummaryResponse:
        session = self._repository.get_session_by_key(request.session_key)
        if session is None:
            raise ValueError(f"Session not found: {request.session_key}")

        messages = self._repository.list_messages(session_id=session.id)
        message_count = len(messages)
        if message_count < request.min_messages:
            return SessionSummaryResponse(
                session_key=request.session_key,
                applied=False,
                message_count=message_count,
                summary=None,
            )

        bounded = messages[-request.max_messages_in_summary :]
        points: list[str] = []
        for message in bounded:
            compact = self._compact(message.content)
            points.append(f"- [{message.turn_index}] {message.role}: {compact}")

        summary = "\n".join(points[-request.max_points :])
        return SessionSummaryResponse(
            session_key=request.session_key,
            applied=True,
            message_count=message_count,
            summary=summary,
        )

    @staticmethod
    def _compact(text: str, limit: int = 120) -> str:
        cleaned = " ".join(text.split())
        if len(cleaned) <= limit:
            return cleaned
        return f"{cleaned[: limit - 3]}..."
