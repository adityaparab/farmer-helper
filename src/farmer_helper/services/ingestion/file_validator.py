from pathlib import Path

from farmer_helper.schemas.ingestion import ValidatedIngestionFile


class IngestionValidationError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class FileValidator:
    def __init__(
        self,
        allowed_extensions: tuple[str, ...] = (".pdf",),
        max_file_size_bytes: int = 25 * 1024 * 1024,
    ) -> None:
        self._allowed_extensions = tuple(ext.lower() for ext in allowed_extensions)
        self._max_file_size_bytes = max_file_size_bytes

    def validate(self, candidate_path: str) -> ValidatedIngestionFile:
        path = Path(candidate_path)

        if not path.exists():
            raise IngestionValidationError(
                code="INGESTION_INPUT_NOT_FOUND",
                message=f"Input file does not exist: {candidate_path}",
            )

        if not path.is_file():
            raise IngestionValidationError(
                code="INGESTION_INPUT_NOT_FILE",
                message=f"Input path is not a file: {candidate_path}",
            )

        extension = path.suffix.lower()
        if extension not in self._allowed_extensions:
            raise IngestionValidationError(
                code="INGESTION_INPUT_UNSUPPORTED_EXTENSION",
                message=(
                    f"Unsupported file extension '{extension}'. "
                    f"Allowed: {', '.join(self._allowed_extensions)}"
                ),
            )

        size_bytes = path.stat().st_size
        if size_bytes <= 0:
            raise IngestionValidationError(
                code="INGESTION_INPUT_EMPTY_FILE",
                message=f"Input file is empty: {candidate_path}",
            )

        if size_bytes > self._max_file_size_bytes:
            raise IngestionValidationError(
                code="INGESTION_INPUT_FILE_TOO_LARGE",
                message=(
                    f"Input file exceeds max size ({self._max_file_size_bytes} bytes): "
                    f"{candidate_path}"
                ),
            )

        return ValidatedIngestionFile(
            file_path=str(path.resolve()),
            extension=extension,
            size_bytes=size_bytes,
        )
