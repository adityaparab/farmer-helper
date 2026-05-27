from pydantic import ValidationError

from farmer_helper.schemas.session import ChatMessageCreateRequest, ChatSessionCreateRequest


def test_chat_session_create_request_rejects_blank_session_key() -> None:
    try:
        ChatSessionCreateRequest(session_key="   ")
        raise AssertionError("Expected ValidationError")
    except ValidationError:
        pass


def test_chat_message_create_request_rejects_blank_content() -> None:
    try:
        ChatMessageCreateRequest(role="user", content=" ")
        raise AssertionError("Expected ValidationError")
    except ValidationError:
        pass


def test_chat_message_create_request_accepts_valid_message() -> None:
    request = ChatMessageCreateRequest(
        role="assistant",
        content="Use mulch and monitor moisture.",
        metadata={"intent": "advice"},
    )

    assert request.role == "assistant"
    assert request.metadata == {"intent": "advice"}
