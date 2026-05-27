import hashlib

from farmer_helper.schemas.ingestion import ChunkMetadata, EnrichedIngestionChunk, IngestionChunk


class ChunkMetadataEnricher:
    def __init__(self, version: str = "v1") -> None:
        """Init for ingestion workflows.

        Initialize ChunkMetadataEnricher for ingestion workflows. Inputs are version. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._version = version

    def enrich(
        self,
        chunks: list[IngestionChunk],
        headings_by_page: dict[int, str] | None = None,
    ) -> list[EnrichedIngestionChunk]:
        """Enrich for ingestion workflows.

        This ChunkMetadataEnricher method belongs to the ingestion service layer. Inputs are
        chunks, headings_by_page. It runs synchronously and returns when local processing is
        complete. Returns a list[EnrichedIngestionChunk] value that downstream API or
        orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
