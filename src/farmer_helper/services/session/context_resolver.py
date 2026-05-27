from typing import cast

from farmer_helper.core.config import get_settings
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

        max_chars = get_settings().session_context_max_chars_per_message
        payload_messages: list[FollowUpContextMessage] = []
        seen_signatures: set[tuple[MessageRole, str]] = set()
        for message in bounded_messages:
            role = self._to_message_role(message.role)
            compact = self._compact(message.content, limit=max_chars)
            signature = (role, compact)
            if signature in seen_signatures:
                continue
            seen_signatures.add(signature)
            payload_messages.append(
                FollowUpContextMessage(
                    turn_index=message.turn_index,
                    role=role,
                    content=compact,
                )
            )

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

    @staticmethod
    def _compact(text: str, limit: int) -> str:
        normalized = " ".join(text.split())
        if len(normalized) <= limit:
            return normalized
        return f"{normalized[: limit - 3]}..."
