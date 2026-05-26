import hashlib

from farmer_helper.schemas.ingestion import ChunkMetadata, EnrichedIngestionChunk, IngestionChunk


class ChunkMetadataEnricher:
    def __init__(self, version: str = "v1") -> None:
        self._version = version

    def enrich(
        self,
        chunks: list[IngestionChunk],
        headings_by_page: dict[int, str] | None = None,
    ) -> list[EnrichedIngestionChunk]:
        headings = headings_by_page or {}

        enriched: list[EnrichedIngestionChunk] = []
        for chunk in chunks:
            heading = headings.get(chunk.page_start)
            content_hash = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()

            enriched.append(
                EnrichedIngestionChunk(
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    char_count=chunk.char_count,
                    metadata=ChunkMetadata(
                        page_start=chunk.page_start,
                        page_end=chunk.page_end,
                        heading=heading,
                        version=self._version,
                        content_hash=content_hash,
                    ),
                )
            )

        return enriched
