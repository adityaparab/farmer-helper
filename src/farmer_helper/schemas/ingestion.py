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
