from pydantic import BaseModel, Field, field_validator, model_validator


class EmbeddingRequest(BaseModel):
    texts: list[str] = Field(min_length=1)
    model: str = Field(min_length=1)

    @field_validator("texts")
    @classmethod
    def validate_texts(cls, value: list[str]) -> list[str]:
        for text in value:
            if not text.strip():
                raise ValueError("texts must not contain blank values")
        return value


class EmbeddingItem(BaseModel):
    index: int = Field(ge=0)
    vector: list[float] = Field(min_length=1)


class EmbeddingResponse(BaseModel):
    model: str = Field(min_length=1)
    items: list[EmbeddingItem] = Field(min_length=1)
    dimensions: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_dimensions(self) -> "EmbeddingResponse":
        expected = self.dimensions
        for item in self.items:
            if len(item.vector) != expected:
                raise ValueError("all embedding vectors must match 'dimensions' value")
        return self


class EmbeddingSourceChunk(BaseModel):
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)


class EmbeddingOrchestrationResult(BaseModel):
    document_id: int = Field(ge=1)
    model: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    version: str = Field(min_length=1)
    dimensions: int = Field(ge=1)
    persisted_count: int = Field(ge=0)
    degraded: bool = False
    degradation_code: str | None = None


class EmbeddingTriggerRequest(BaseModel):
    document_id: int = Field(ge=1)
    model: str = Field(min_length=1)
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=128)
    provider: str = Field(min_length=1, default="mock-provider")
    version: str = Field(min_length=1, default="v1")
    batch_size: int = Field(ge=1, le=256, default=32)
    dimensions: int = Field(ge=1, le=4096, default=8)
    chunks: list[EmbeddingSourceChunk] = Field(min_length=1)
