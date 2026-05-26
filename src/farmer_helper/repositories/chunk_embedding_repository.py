from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import ChunkEmbedding


class ChunkEmbeddingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_document(self, document_id: int) -> list[ChunkEmbedding]:
        stmt = (
            select(ChunkEmbedding)
            .where(ChunkEmbedding.document_id == document_id)
            .order_by(ChunkEmbedding.chunk_index.asc())
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
    ) -> ChunkEmbedding:
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
                vector_json=vector,
                content_hash=content_hash,
            )
            self._session.add(record)
        else:
            existing.dimensions = dimensions
            existing.vector_json = vector
            existing.content_hash = content_hash
            self._session.add(existing)
            record = existing

        self._session.commit()
        self._session.refresh(record)
        return record
