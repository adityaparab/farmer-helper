from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import SessionSummaryRequest
from farmer_helper.services.session.summarizer import SessionSummarizer


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def _seed_messages(repository: ChatSessionRepository, session_id: int, count: int) -> None:
    for index in range(count):
        role = "user" if index % 2 == 0 else "assistant"
        repository.append_message(
            session_id=session_id,
            role=role,
            content=f"Message {index} content for planning follow-up actions.",
        )


def test_session_summarizer_applies_for_long_sessions() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    record = repository.create_session(session_key="sum-001")
    _seed_messages(repository, record.id, count=14)

    summarizer = SessionSummarizer(repository)
    response = summarizer.summarize(
        SessionSummaryRequest(
            session_key="sum-001",
            min_messages=10,
            max_messages_in_summary=12,
            max_points=4,
        )
    )

    assert response.applied is True
    assert response.summary is not None
    assert response.summary.count("\n") <= 3
    assert "[13]" in response.summary


def test_session_summarizer_noop_when_below_threshold() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    record = repository.create_session(session_key="sum-002")
    _seed_messages(repository, record.id, count=5)

    summarizer = SessionSummarizer(repository)
    response = summarizer.summarize(SessionSummaryRequest(session_key="sum-002", min_messages=10))

    assert response.applied is False
    assert response.summary is None
    assert response.message_count == 5


def test_session_summarizer_raises_when_session_missing() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    summarizer = SessionSummarizer(repository)

    try:
        summarizer.summarize(SessionSummaryRequest(session_key="missing"))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert "Session not found" in str(exc)
