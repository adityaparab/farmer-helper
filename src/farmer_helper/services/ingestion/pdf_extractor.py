from pypdf import PdfReader
from pypdf.errors import PdfReadError

from farmer_helper.schemas.ingestion import ExtractedDocument, ExtractedPage
from farmer_helper.services.ingestion.file_validator import FileValidator, IngestionValidationError


class PdfExtractionError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class PdfExtractor:
    def __init__(self, validator: FileValidator | None = None) -> None:
        self._validator = validator or FileValidator(allowed_extensions=(".pdf",))

    def extract(self, file_path: str) -> ExtractedDocument:
        try:
            validated = self._validator.validate(file_path)
        except IngestionValidationError as exc:
            raise PdfExtractionError(code=exc.code, message=exc.message) from exc

        try:
            reader = PdfReader(validated.file_path)
        except PdfReadError as exc:
            raise PdfExtractionError(
                code="INGESTION_PDF_CORRUPT_OR_UNREADABLE",
                message=f"Unable to read PDF: {validated.file_path}",
            ) from exc
        except Exception as exc:
            raise PdfExtractionError(
                code="INGESTION_PDF_READ_ERROR",
                message=f"Unexpected PDF read failure: {validated.file_path}",
            ) from exc

        if reader.is_encrypted:
            raise PdfExtractionError(
                code="INGESTION_PDF_ENCRYPTED",
                message=f"Encrypted PDF is not supported: {validated.file_path}",
            )

        pages: list[ExtractedPage] = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(ExtractedPage(page_number=index, text=text))

        return ExtractedDocument(file_path=validated.file_path, pages=pages)
