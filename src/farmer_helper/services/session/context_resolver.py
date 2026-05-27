from typing import cast

from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import (
    FollowUpContextMessage,
    FollowUpContextRequest,
    FollowUpContextResponse,
    MessageRole,
)


class FollowUpContextResolver:
    def __init__(self, repository: ChatSessionRepository) -> None:
        self._repository = repository

    def resolve(self, request: FollowUpContextRequest) -> FollowUpContextResponse:
        session = self._repository.get_session_by_key(request.session_key)
        if session is None:
            raise ValueError(f"Session not found: {request.session_key}")

        all_messages = self._repository.list_messages(session_id=session.id)
        if not all_messages:
            return FollowUpContextResponse(
                session_key=request.session_key,
                messages=[],
                context_text="",
            )

        max_turn = all_messages[-1].turn_index
        min_turn = max(0, max_turn - request.max_turns + 1)
        turn_window = [message for message in all_messages if message.turn_index >= min_turn]
        bounded_messages = turn_window[-request.max_messages :]

        payload_messages = [
            FollowUpContextMessage(
                turn_index=message.turn_index,
                role=self._to_message_role(message.role),
                content=message.content,
            )
            for message in bounded_messages
        ]

        context_text = "\n".join(
            f"[{item.turn_index}] {item.role}: {item.content}" for item in payload_messages
        )

        return FollowUpContextResponse(
            session_key=request.session_key,
            messages=payload_messages,
            context_text=context_text,
        )

    @staticmethod
    def _to_message_role(role: str) -> MessageRole:
        if role not in {"system", "user", "assistant"}:
            raise ValueError(f"Unsupported message role: {role}")
        return cast(MessageRole, role)
