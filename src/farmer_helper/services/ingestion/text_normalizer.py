import re

from farmer_helper.schemas.ingestion import (
    ExtractedDocument,
    ExtractedPage,
    TextNormalizationConfig,
)


class TextNormalizer:
    def __init__(self, config: TextNormalizationConfig | None = None) -> None:
        self._config = config or TextNormalizationConfig()

    def normalize_document(self, extracted: ExtractedDocument) -> ExtractedDocument:
        normalized_pages = [
            ExtractedPage(page_number=page.page_number, text=self.normalize_text(page.text))
            for page in extracted.pages
        ]
        return ExtractedDocument(file_path=extracted.file_path, pages=normalized_pages)

    def normalize_text(self, text: str) -> str:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = self._remove_control_chars(normalized)

        if self._config.collapse_whitespace:
            # Collapse consecutive spaces/tabs while preserving newline boundaries.
            normalized = re.sub(r"[\t ]+", " ", normalized)

        if self._config.collapse_blank_lines:
            normalized = re.sub(r"\n{3,}", "\n\n", normalized)

        if not self._config.keep_newlines:
            normalized = normalized.replace("\n", " ")

        if self._config.trim_edges:
            normalized = normalized.strip()

        return normalized

    @staticmethod
    def _remove_control_chars(text: str) -> str:
        return "".join(
            ch for ch in text if ch == "\n" or ch == "\t" or (ord(ch) >= 32 and ord(ch) != 127)
        )
