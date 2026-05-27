from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import FollowUpContextRequest
from farmer_helper.services.session.context_resolver import FollowUpContextResolver


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def _build_messages(repository: ChatSessionRepository, session_id: int) -> None:
    repository.append_message(session_id=session_id, role="user", content="Turn 0 user")
    repository.append_message(session_id=session_id, role="assistant", content="Turn 1 assistant")
    repository.append_message(session_id=session_id, role="user", content="Turn 2 user")
    repository.append_message(session_id=session_id, role="assistant", content="Turn 3 assistant")
    repository.append_message(session_id=session_id, role="user", content="Turn 4 user")


def test_follow_up_context_resolver_returns_bounded_messages() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    created = repository.create_session(session_key="ctx-001")
    _build_messages(repository, created.id)

    resolver = FollowUpContextResolver(repository)
    response = resolver.resolve(
        FollowUpContextRequest(
            session_key="ctx-001",
            question="What should I do next?",
            max_messages=3,
            max_turns=4,
        )
    )

    assert len(response.messages) == 3
    assert [message.turn_index for message in response.messages] == [2, 3, 4]
    assert "[4] user: Turn 4 user" in response.context_text


def test_follow_up_context_resolver_returns_empty_for_no_messages() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    repository.create_session(session_key="ctx-empty")

    resolver = FollowUpContextResolver(repository)
    response = resolver.resolve(
        FollowUpContextRequest(session_key="ctx-empty", question="Any context?")
    )

    assert response.messages == []
    assert response.context_text == ""


def test_follow_up_context_resolver_raises_when_session_missing() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    resolver = FollowUpContextResolver(repository)

    try:
        resolver.resolve(FollowUpContextRequest(session_key="missing", question="Hello"))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert "Session not found" in str(exc)
