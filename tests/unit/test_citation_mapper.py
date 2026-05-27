from farmer_helper.schemas.answering import Citation, RetrievedChunk
from farmer_helper.services.answering.citation_mapper import CitationMapper


def _chunk(document_id: int, chunk_index: int, content_hash: str, score: float) -> RetrievedChunk:
    return RetrievedChunk(
        citation=Citation(
            document_id=document_id,
            chunk_index=chunk_index,
            content_hash=content_hash,
        ),
        text=f"chunk-{document_id}-{chunk_index}",
        score=score,
    )


def test_citation_mapper_deduplicates_and_uses_best_score() -> None:
    mapper = CitationMapper()
    citations = mapper.map_citations(
        chunks=[
            _chunk(1, 0, "h1", 0.7),
            _chunk(1, 0, "h1", 0.9),
            _chunk(2, 0, "h2", 0.8),
        ],
        max_citations=5,
    )

    assert len(citations) == 2
    assert [(c.document_id, c.chunk_index, c.content_hash) for c in citations] == [
        (1, 0, "h1"),
        (2, 0, "h2"),
    ]


def test_citation_mapper_applies_deterministic_tie_breaks() -> None:
    mapper = CitationMapper()
    citations = mapper.map_citations(
        chunks=[
            _chunk(2, 1, "h21", 0.8),
            _chunk(1, 3, "h13", 0.8),
            _chunk(1, 1, "h11", 0.8),
        ],
        max_citations=5,
    )

    assert [(c.document_id, c.chunk_index) for c in citations] == [(1, 1), (1, 3), (2, 1)]


def test_citation_mapper_respects_max_citations() -> None:
    mapper = CitationMapper()
    citations = mapper.map_citations(
        chunks=[
            _chunk(1, 0, "h10", 0.9),
            _chunk(1, 1, "h11", 0.8),
            _chunk(1, 2, "h12", 0.7),
        ],
        max_citations=2,
    )

    assert len(citations) == 2
    assert [(c.document_id, c.chunk_index) for c in citations] == [(1, 0), (1, 1)]
