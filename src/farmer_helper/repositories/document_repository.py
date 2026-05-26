from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import Document


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_content_hash_version(self, content_hash: str, version: str) -> Document | None:
        stmt = select(Document).where(
            Document.content_hash == content_hash,
            Document.version == version,
        )
        return self._session.scalar(stmt)

    def create(self, source_path: str, content_hash: str, version: str) -> Document:
        document = Document(source_path=source_path, content_hash=content_hash, version=version)
        self._session.add(document)
        self._session.commit()
        self._session.refresh(document)
        return document
