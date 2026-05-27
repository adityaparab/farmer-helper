from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import Document


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for document-repository repository persistence workflows.

        This DocumentRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def get_by_content_hash_version(self, content_hash: str, version: str) -> Document | None:
        """Retrieve by content hash version for document-repository repository persistence
        workflows.

        This DocumentRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        content_hash, version. It runs synchronously and returns after local processing is
        complete. It returns Document | None for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = select(Document).where(
            Document.content_hash == content_hash,
            Document.version == version,
        )
        return self._session.scalar(stmt)

    def create(self, source_path: str, content_hash: str, version: str) -> Document:
        """Create for document-repository repository persistence workflows.

        This DocumentRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        source_path, content_hash, version. It runs synchronously and returns after local
        processing is complete. It returns Document for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        document = Document(source_path=source_path, content_hash=content_hash, version=version)
        self._session.add(document)
        self._session.commit()
        self._session.refresh(document)
        return document
