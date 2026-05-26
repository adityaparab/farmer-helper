from farmer_helper.schemas.ingestion import IngestionChunk
from farmer_helper.services.ingestion.chunk_metadata_enricher import ChunkMetadataEnricher


def test_chunk_metadata_enrichment_attaches_required_fields() -> None:
    chunks = [
        IngestionChunk(
            chunk_index=0,
            page_start=2,
            page_end=2,
            text="soil moisture guidance",
            char_count=22,
        )
    ]

    enricher = ChunkMetadataEnricher(version="v2")
    enriched = enricher.enrich(chunks, headings_by_page={2: "Irrigation Basics"})

    assert len(enriched) == 1
    item = enriched[0]
    assert item.metadata.page_start == 2
    assert item.metadata.page_end == 2
    assert item.metadata.heading == "Irrigation Basics"
    assert item.metadata.version == "v2"
    assert len(item.metadata.content_hash) == 64


def test_chunk_metadata_enrichment_is_deterministic() -> None:
    chunk = IngestionChunk(
        chunk_index=1,
        page_start=1,
        page_end=1,
        text="consistent text",
        char_count=15,
    )

    enricher = ChunkMetadataEnricher(version="v1")
    first = enricher.enrich([chunk])[0]
    second = enricher.enrich([chunk])[0]

    assert first.metadata.content_hash == second.metadata.content_hash
    assert first.metadata.version == second.metadata.version
