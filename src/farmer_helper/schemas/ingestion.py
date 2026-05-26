from pydantic import BaseModel


class ValidatedIngestionFile(BaseModel):
    file_path: str
    extension: str
    size_bytes: int
