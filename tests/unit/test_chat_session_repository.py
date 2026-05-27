from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_chat_session_repository_creates_session() -> None:
    session = _session()
    repository = ChatSessionRepository(session)

    created = repository.create_session(
        session_key="session-001",
        user_id="user-1",
        title="Irrigation planning",
    )

    assert created.id > 0
    assert created.session_key == "session-001"
    assert created.status == "active"


def test_chat_session_repository_get_by_key() -> None:
    session = _session()
    repository = ChatSessionRepository(session)

    repository.create_session(session_key="session-lookup")
    fetched = repository.get_session_by_key("session-lookup")

    assert fetched is not None
    assert fetched.session_key == "session-lookup"


def test_chat_session_repository_appends_turn_index_sequentially() -> None:
    session = _session()
    repository = ChatSessionRepository(session)

    chat_session = repository.create_session(session_key="session-turns")
    first = repository.append_message(
        session_id=chat_session.id,
        role="user",
        content="How often should I water tomatoes?",
    )
    second = repository.append_message(
        session_id=chat_session.id,
        role="assistant",
        content="Water based on soil moisture and weather.",
    )

    assert first.turn_index == 0
    assert second.turn_index == 1

    listed = repository.list_messages(session_id=chat_session.id)
    assert len(listed) == 2
    assert [message.turn_index for message in listed] == [0, 1]


def test_chat_session_repository_message_metadata_persists() -> None:
    session = _session()
    repository = ChatSessionRepository(session)

    chat_session = repository.create_session(session_key="session-metadata")
    message = repository.append_message(
        session_id=chat_session.id,
        role="user",
        content="Need irrigation plan.",
        metadata={"source": "mobile"},
    )

    assert message.metadata_json == {"source": "mobile"}
