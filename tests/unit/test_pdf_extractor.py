from pathlib import Path

import pytest
from pypdf import PdfWriter

from farmer_helper.services.ingestion.pdf_extractor import PdfExtractionError, PdfExtractor


def _create_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with path.open("wb") as fp:
        writer.write(fp)


def test_pdf_extractor_success(tmp_path: Path) -> None:
    path = tmp_path / "sample.pdf"
    _create_pdf(path)

    extractor = PdfExtractor()
    result = extractor.extract(str(path))

    assert result.file_path.endswith("sample.pdf")
    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1


def test_pdf_extractor_missing_file(tmp_path: Path) -> None:
    extractor = PdfExtractor()

    with pytest.raises(PdfExtractionError) as exc:
        extractor.extract(str(tmp_path / "missing.pdf"))

    assert exc.value.code == "INGESTION_INPUT_NOT_FOUND"


def test_pdf_extractor_corrupt_file(tmp_path: Path) -> None:
    path = tmp_path / "corrupt.pdf"
    path.write_text("not-a-real-pdf")

    extractor = PdfExtractor()

    with pytest.raises(PdfExtractionError) as exc:
        extractor.extract(str(path))

    assert exc.value.code in {"INGESTION_PDF_CORRUPT_OR_UNREADABLE", "INGESTION_PDF_READ_ERROR"}
