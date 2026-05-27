from datetime import datetime

from farmer_helper.repositories.chat_session_repository import ChatSessionRepository


class SessionLifecycleService:
    def __init__(self, repository: ChatSessionRepository) -> None:
        """Init for session-memory workflows.

        Initialize SessionLifecycleService for session-memory workflows. Inputs are repository.
        It runs synchronously and returns when local processing is complete. The operation is
        executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository = repository

    def archive(self, session_key: str) -> None:
        """Archive for session-memory workflows.

        This SessionLifecycleService method belongs to the session-memory service layer. Inputs
        are session_key. It runs synchronously and returns when local processing is complete.
        The operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository.archive_session(session_key=session_key)

    def expire_stale_sessions(self, updated_before: datetime) -> int:
        """Expire stale sessions for session-memory workflows.

        This SessionLifecycleService method belongs to the session-memory service layer. Inputs
        are updated_before. It runs synchronously and returns when local processing is complete.
        Returns a int value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        return self._repository.expire_active_sessions(updated_before=updated_before)
