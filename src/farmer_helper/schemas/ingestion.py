from pydantic import BaseModel


class ValidatedIngestionFile(BaseModel):
    file_path: str
    extension: str
    size_bytes: int


class ExtractedPage(BaseModel):
    page_number: int
    text: str


class ExtractedDocument(BaseModel):
    file_path: str
    pages: list[ExtractedPage]


class TextNormalizationConfig(BaseModel):
    collapse_whitespace: bool = True
    collapse_blank_lines: bool = True
    trim_edges: bool = True
    keep_newlines: bool = True
