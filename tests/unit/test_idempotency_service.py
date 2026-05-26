from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from farmer_helper.db.models.base import Base
from farmer_helper.repositories.document_repository import DocumentRepository
from farmer_helper.services.ingestion.idempotency_service import IngestionIdempotencyService


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_idempotency_creates_document_when_missing() -> None:
    session = _session()
    repository = DocumentRepository(session)
    service = IngestionIdempotencyService(repository)

    result = service.ensure_document(
        source_path="docs/a.pdf",
        content_hash="hash-1",
        version="v1",
    )

    assert result.created is True
    assert result.document_id > 0


def test_idempotency_returns_existing_for_same_hash_version() -> None:
    session = _session()
    repository = DocumentRepository(session)
    service = IngestionIdempotencyService(repository)

    first = service.ensure_document(source_path="docs/a.pdf", content_hash="hash-2", version="v1")
    second = service.ensure_document(source_path="docs/b.pdf", content_hash="hash-2", version="v1")

    assert first.created is True
    assert second.created is False
    assert first.document_id == second.document_id


def test_idempotency_allows_same_hash_different_version() -> None:
    session = _session()
    repository = DocumentRepository(session)
    service = IngestionIdempotencyService(repository)

    first = service.ensure_document(source_path="docs/a.pdf", content_hash="hash-3", version="v1")
    second = service.ensure_document(source_path="docs/b.pdf", content_hash="hash-3", version="v2")

    assert first.created is True
    assert second.created is True
    assert first.document_id != second.document_id
