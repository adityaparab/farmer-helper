from pydantic import BaseModel

from farmer_helper.repositories.document_repository import DocumentRepository


class IdempotencyResult(BaseModel):
    document_id: int
    created: bool


class IngestionIdempotencyService:
    def __init__(self, repository: DocumentRepository) -> None:
        """Init for ingestion workflows.

        Initialize IngestionIdempotencyService for ingestion workflows. Inputs are repository.
        It runs synchronously and returns when local processing is complete. The operation is
        executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository = repository

    def ensure_document(
        self,
        source_path: str,
        content_hash: str,
        version: str = "v1",
    ) -> IdempotencyResult:
        """Ensure document for ingestion workflows.

        This IngestionIdempotencyService method belongs to the ingestion service layer. Inputs
        are source_path, content_hash, version. It runs synchronously and returns when local
        processing is complete. Returns a IdempotencyResult value that downstream API or
        orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
