from collections.abc import Sequence

from farmer_helper.schemas.answering import Citation, RetrievedChunk


class CitationMapper:
    def map_citations(
        self,
        chunks: Sequence[RetrievedChunk],
        max_citations: int,
    ) -> list[Citation]:
        """Map citations for answer-generation workflows.

        This CitationMapper method belongs to the answer-generation service layer. Inputs are
        chunks, max_citations. It runs synchronously and returns when local processing is
        complete. Returns a list[Citation] value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        best_by_key: dict[tuple[int, int, str], RetrievedChunk] = {}

        for chunk in chunks:
            key = (
                chunk.citation.document_id,
                chunk.citation.chunk_index,
                chunk.citation.content_hash,
            )
            existing = best_by_key.get(key)
            if existing is None or chunk.score > existing.score:
                best_by_key[key] = chunk

        ranked = sorted(
            best_by_key.values(),
            key=lambda chunk: (
                -chunk.score,
                chunk.citation.document_id,
                chunk.citation.chunk_index,
                chunk.citation.content_hash,
            ),
        )

        return [
            Citation(
                document_id=chunk.citation.document_id,
                chunk_index=chunk.citation.chunk_index,
                content_hash=chunk.citation.content_hash,
            )
            for chunk in ranked[:max_citations]
        ]
