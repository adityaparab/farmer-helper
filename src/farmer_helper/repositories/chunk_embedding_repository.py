from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import ChunkEmbedding


class ChunkEmbeddingRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for chunk-embedding-repository repository persistence workflows.

        This ChunkEmbeddingRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def list_for_document(self, document_id: int) -> list[ChunkEmbedding]:
        """List for document for chunk-embedding-repository repository persistence workflows.

        This ChunkEmbeddingRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        document_id. It runs synchronously and returns after local processing is complete. It
        returns list[ChunkEmbedding] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = (
            select(ChunkEmbedding)
            .where(ChunkEmbedding.document_id == document_id)
            .order_by(ChunkEmbedding.chunk_index.asc())
        )
        return list(self._session.scalars(stmt))

    def list_for_retrieval(
        self,
        provider: str,
        model: str,
        version: str,
    ) -> list[ChunkEmbedding]:
        """List for retrieval for chunk-embedding-repository repository persistence workflows.

        This ChunkEmbeddingRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        provider, model, version. It runs synchronously and returns after local processing is
        complete. It returns list[ChunkEmbedding] for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        stmt = (
            select(ChunkEmbedding)
            .where(
                ChunkEmbedding.provider == provider,
                ChunkEmbedding.model == model,
                ChunkEmbedding.version == version,
            )
            .order_by(ChunkEmbedding.document_id.asc(), ChunkEmbedding.chunk_index.asc())
        )
        return list(self._session.scalars(stmt))

    def upsert(
        self,
        document_id: int,
        chunk_index: int,
        provider: str,
        model: str,
        version: str,
        dimensions: int,
        vector: list[float],
        content_hash: str,
        chunk_text: str,
    ) -> ChunkEmbedding:
        """Upsert for chunk-embedding-repository repository persistence workflows.

        This ChunkEmbeddingRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        document_id, chunk_index, provider, model, version, dimensions, vector, content_hash,
        chunk_text. It runs synchronously and returns after local processing is complete. It
        returns ChunkEmbedding for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        existing = self._session.scalar(
            select(ChunkEmbedding).where(
                ChunkEmbedding.document_id == document_id,
                ChunkEmbedding.chunk_index == chunk_index,
                ChunkEmbedding.provider == provider,
                ChunkEmbedding.model == model,
                ChunkEmbedding.version == version,
            )
        )

        if existing is None:
            record = ChunkEmbedding(
                document_id=document_id,
                chunk_index=chunk_index,
                provider=provider,
                model=model,
                version=version,
                dimensions=dimensions,
                chunk_text=chunk_text,
                vector_json=vector,
                content_hash=content_hash,
            )
            self._session.add(record)
        else:
            existing.dimensions = dimensions
            existing.chunk_text = chunk_text
            existing.vector_json = vector
            existing.content_hash = content_hash
            self._session.add(existing)
            record = existing

        self._session.commit()
        self._session.refresh(record)
        return record
