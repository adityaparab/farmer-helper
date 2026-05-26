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
