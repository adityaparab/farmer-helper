from pathlib import Path

import pytest

from farmer_helper.services.ingestion.file_validator import FileValidator, IngestionValidationError


def test_file_validator_success(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    file_path.write_text("dummy pdf content")

    validator = FileValidator()
    result = validator.validate(str(file_path))

    assert result.extension == ".pdf"
    assert result.size_bytes > 0
    assert result.file_path.endswith("sample.pdf")


def test_file_validator_missing_file(tmp_path: Path) -> None:
    validator = FileValidator()

    with pytest.raises(IngestionValidationError) as exc:
        validator.validate(str(tmp_path / "missing.pdf"))

    assert exc.value.code == "INGESTION_INPUT_NOT_FOUND"


def test_file_validator_rejects_directory(tmp_path: Path) -> None:
    validator = FileValidator()

    with pytest.raises(IngestionValidationError) as exc:
        validator.validate(str(tmp_path))

    assert exc.value.code == "INGESTION_INPUT_NOT_FILE"


def test_file_validator_rejects_extension(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("text")

    validator = FileValidator()
    with pytest.raises(IngestionValidationError) as exc:
        validator.validate(str(file_path))

    assert exc.value.code == "INGESTION_INPUT_UNSUPPORTED_EXTENSION"


def test_file_validator_rejects_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.pdf"
    file_path.write_text("")

    validator = FileValidator()
    with pytest.raises(IngestionValidationError) as exc:
        validator.validate(str(file_path))

    assert exc.value.code == "INGESTION_INPUT_EMPTY_FILE"


def test_file_validator_rejects_oversized_file(tmp_path: Path) -> None:
    file_path = tmp_path / "big.pdf"
    file_path.write_text("0123456789")

    validator = FileValidator(max_file_size_bytes=5)
    with pytest.raises(IngestionValidationError) as exc:
        validator.validate(str(file_path))

    assert exc.value.code == "INGESTION_INPUT_FILE_TOO_LARGE"
