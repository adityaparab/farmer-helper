from farmer_helper.schemas.ingestion import (
    ExtractedDocument,
    ExtractedPage,
    TextNormalizationConfig,
)
from farmer_helper.services.ingestion.text_normalizer import TextNormalizer


def test_normalize_text_collapses_whitespace_and_blank_lines() -> None:
    normalizer = TextNormalizer()
    raw = "Line 1\t\twith   spaces\r\n\r\n\r\nLine 2"

    normalized = normalizer.normalize_text(raw)

    assert normalized == "Line 1 with spaces\n\nLine 2"


def test_normalize_text_removes_control_chars() -> None:
    normalizer = TextNormalizer()
    raw = "A\x00B\x1fC\nD"

    normalized = normalizer.normalize_text(raw)

    assert normalized == "ABC\nD"


def test_normalize_document_preserves_page_numbers() -> None:
    doc = ExtractedDocument(
        file_path="/tmp/sample.pdf",
        pages=[
            ExtractedPage(page_number=1, text=" Page 1\r\n\r\nText"),
            ExtractedPage(page_number=2, text="\tPage 2   Text  "),
        ],
    )

    normalizer = TextNormalizer(config=TextNormalizationConfig())
    result = normalizer.normalize_document(doc)

    assert [p.page_number for p in result.pages] == [1, 2]
    assert result.pages[0].text == "Page 1\n\nText"
    assert result.pages[1].text == "Page 2 Text"
