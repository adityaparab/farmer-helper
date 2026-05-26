from pydantic import BaseModel

from farmer_helper.repositories.document_repository import DocumentRepository


class IdempotencyResult(BaseModel):
    document_id: int
    created: bool


class IngestionIdempotencyService:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    def ensure_document(
        self,
        source_path: str,
        content_hash: str,
        version: str = "v1",
    ) -> IdempotencyResult:
        existing = self._repository.get_by_content_hash_version(
            content_hash=content_hash,
            version=version,
        )
        if existing is not None:
            return IdempotencyResult(document_id=existing.id, created=False)

        created = self._repository.create(
            source_path=source_path,
            content_hash=content_hash,
            version=version,
        )
        return IdempotencyResult(document_id=created.id, created=True)
