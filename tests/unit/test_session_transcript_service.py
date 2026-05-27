from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import TranscriptImportRequest
from farmer_helper.services.session.transcript_service import SessionTranscriptService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def _seed_session(repository: ChatSessionRepository, session_key: str) -> None:
    session = repository.create_session(session_key=session_key, user_id="u1", title="Plan")
    repository.append_message(session.id, role="user", content="First question")
    repository.append_message(session.id, role="assistant", content="First answer")


def test_transcript_service_exports_ordered_messages() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    _seed_session(repository, session_key="tx-001")

    service = SessionTranscriptService(repository)
    transcript = service.export_transcript("tx-001")

    assert transcript.session_key == "tx-001"
    assert [message.turn_index for message in transcript.messages] == [0, 1]


def test_transcript_service_imports_round_trip_with_override() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    _seed_session(repository, session_key="tx-source")

    service = SessionTranscriptService(repository)
    exported = service.export_transcript("tx-source")

    service.import_transcript(
        TranscriptImportRequest(
            transcript=exported,
            session_key_override="tx-copy",
        )
    )

    copied = service.export_transcript("tx-copy")
    assert copied.session_key == "tx-copy"
    assert [message.content for message in copied.messages] == [
        "First question",
        "First answer",
    ]


def test_transcript_service_rejects_import_when_target_exists() -> None:
    session = _session()
    repository = ChatSessionRepository(session)
    _seed_session(repository, session_key="tx-existing")

    service = SessionTranscriptService(repository)
    exported = service.export_transcript("tx-existing")

    try:
        service.import_transcript(TranscriptImportRequest(transcript=exported))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert "already exists" in str(exc)
