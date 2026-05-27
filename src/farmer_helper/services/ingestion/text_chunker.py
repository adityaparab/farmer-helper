from farmer_helper.schemas.ingestion import ChunkingConfig, ExtractedDocument, IngestionChunk


class TextChunker:
    def __init__(self, config: ChunkingConfig | None = None) -> None:
        """Init for ingestion workflows.

        Initialize TextChunker for ingestion workflows. Inputs are config. It runs synchronously
        and returns when local processing is complete. The operation is executed for its side
        effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._config = config or ChunkingConfig()
        if self._config.chunk_size_chars <= 0:
            raise ValueError("chunk_size_chars must be positive")
        if self._config.overlap_chars < 0:
            raise ValueError("overlap_chars must be non-negative")
        if self._config.overlap_chars >= self._config.chunk_size_chars:
            raise ValueError("overlap_chars must be smaller than chunk_size_chars")

    def chunk_document(self, normalized_doc: ExtractedDocument) -> list[IngestionChunk]:
        """Split document for ingestion workflows.

        This TextChunker method belongs to the ingestion service layer. Inputs are
        normalized_doc. It runs synchronously and returns when local processing is complete.
        Returns a list[IngestionChunk] value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        chunks: list[IngestionChunk] = []
        chunk_index = 0

        for page in normalized_doc.pages:
            page_chunks = self._chunk_text(page.text)
            for text in page_chunks:
                chunks.append(
                    IngestionChunk(
                        chunk_index=chunk_index,
                        page_start=page.page_number,
                        page_end=page.page_number,
                        text=text,
                        char_count=len(text),
                    )
                )
                chunk_index += 1

        return chunks

    def _chunk_text(self, text: str) -> list[str]:
        """Split text for ingestion workflows.

        This private helper belongs to the ingestion service layer. Inputs are text. It runs
        synchronously and returns when local processing is complete. Returns a list[str] value
        that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        stripped = text.strip()
        if not stripped:
            return []

        chunks: list[str] = []
        start = 0
        step = self._config.chunk_size_chars - self._config.overlap_chars

        while start < len(stripped):
            end = min(start + self._config.chunk_size_chars, len(stripped))
            chunk = stripped[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= len(stripped):
                break
            start += step

        return chunks
