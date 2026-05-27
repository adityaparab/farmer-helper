from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from farmer_helper.db.base import SessionLocal, get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.session import FollowUpContextRequest, SessionSummaryRequest
from farmer_helper.services.session.context_resolver import FollowUpContextResolver
from farmer_helper.services.session.lifecycle_service import SessionLifecycleService
from farmer_helper.services.session.summarizer import SessionSummarizer


def _reset_schema() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _seed_turns(repository: ChatSessionRepository, session_id: int, count: int) -> None:
    for index in range(count):
        role = "user" if index % 2 == 0 else "assistant"
        repository.append_message(
            session_id=session_id,
            role=role,
            content=f"Turn {index} content for irrigation planning.",
        )


def test_multi_turn_answer_and_retrieval_use_session_context() -> None:
    _reset_schema()

    session = SessionLocal()
    try:
        repository = ChatSessionRepository(session)
        chat_session = repository.create_session(session_key="mt-session-1")
        _seed_turns(repository, chat_session.id, count=6)
    finally:
        session.close()

    client = TestClient(app)

    answer_response = client.post(
        "/answers/generate",
        json={
            "session_key": "mt-session-1",
            "question": "What should I do next?",
            "retrieved_chunks": [
                {
                    "citation": {
                        "document_id": 1,
                        "chunk_index": 0,
                        "content_hash": "h-1-0",
                    },
                    "text": "Use mulch and monitor soil moisture.",
                    "score": 0.9,
                }
            ],
        },
    )

    assert answer_response.status_code == 200
    answer_payload = answer_response.json()
    assert answer_payload["decision"] == "answer"
    assert answer_payload["citations"]

    retrieval_response = client.post(
        "/retrieval/query",
        json={
            "session_key": "mt-session-1",
            "query_text": "soil moisture",
            "query_vector": [0.1, 0.2, 0.3],
            "top_k": 3,
            "provider": "mock-provider",
            "model": "mock-embedding-v1",
            "version": "v1",
            "reranker": "none",
        },
    )

    assert retrieval_response.status_code == 200
    retrieval_payload = retrieval_response.json()
    assert "metrics" in retrieval_payload


def test_multi_turn_summarization_and_expiry_interactions() -> None:
    _reset_schema()

    session = SessionLocal()
    try:
        repository = ChatSessionRepository(session)
        chat_session = repository.create_session(session_key="mt-session-2")
        _seed_turns(repository, chat_session.id, count=14)

        summarizer = SessionSummarizer(repository)
        summary = summarizer.summarize(
            SessionSummaryRequest(
                session_key="mt-session-2",
                min_messages=10,
                max_messages_in_summary=12,
                max_points=5,
            )
        )
        assert summary.applied is True
        assert summary.summary is not None

        lifecycle = SessionLifecycleService(repository)
        expired_count = lifecycle.expire_stale_sessions(
            updated_before=datetime.now() + timedelta(days=1)
        )
        assert expired_count >= 1

        resolver = FollowUpContextResolver(repository)
        context = resolver.resolve(
            request=FollowUpContextRequest(
                session_key="mt-session-2",
                question="Follow-up?",
                max_messages=4,
                max_turns=6,
            )
        )
        assert context.messages
    finally:
        session.close()
