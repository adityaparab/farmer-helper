from farmer_helper.schemas.ingestion import ChunkingConfig, ExtractedDocument, ExtractedPage
from farmer_helper.services.ingestion.text_chunker import TextChunker


def test_chunk_document_preserves_page_provenance() -> None:
    doc = ExtractedDocument(
        file_path="sample.pdf",
        pages=[
            ExtractedPage(page_number=1, text="A" * 50),
            ExtractedPage(page_number=2, text="B" * 50),
        ],
    )

    chunker = TextChunker(config=ChunkingConfig(chunk_size_chars=30, overlap_chars=10))
    chunks = chunker.chunk_document(doc)

    assert len(chunks) == 4
    assert chunks[0].page_start == 1
    assert chunks[1].page_start == 1
    assert chunks[2].page_start == 2
    assert chunks[-1].page_end == 2


def test_chunk_document_overlap_behavior() -> None:
    text = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    doc = ExtractedDocument(
        file_path="sample.pdf",
        pages=[ExtractedPage(page_number=1, text=text)],
    )

    chunker = TextChunker(config=ChunkingConfig(chunk_size_chars=10, overlap_chars=3))
    chunks = chunker.chunk_document(doc)

    assert chunks[0].text == "0123456789"
    assert chunks[1].text.startswith("789")


def test_chunk_document_skips_empty_page_text() -> None:
    doc = ExtractedDocument(
        file_path="sample.pdf",
        pages=[ExtractedPage(page_number=1, text="   ")],
    )

    chunker = TextChunker()
    chunks = chunker.chunk_document(doc)
    assert chunks == []
