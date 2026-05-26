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


class ChunkingConfig(BaseModel):
    chunk_size_chars: int = 800
    overlap_chars: int = 120


class IngestionChunk(BaseModel):
    chunk_index: int
    page_start: int
    page_end: int
    text: str
    char_count: int
