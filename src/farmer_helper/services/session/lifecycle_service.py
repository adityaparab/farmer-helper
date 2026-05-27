from datetime import datetime

from farmer_helper.repositories.chat_session_repository import ChatSessionRepository


class SessionLifecycleService:
    def __init__(self, repository: ChatSessionRepository) -> None:
        self._repository = repository

    def archive(self, session_key: str) -> None:
        self._repository.archive_session(session_key=session_key)

    def expire_stale_sessions(self, updated_before: datetime) -> int:
        return self._repository.expire_active_sessions(updated_before=updated_before)
