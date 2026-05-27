from pydantic import BaseModel, Field


class VectorRetrievalRequest(BaseModel):
    query_vector: list[float] = Field(min_length=1)
    top_k: int = Field(ge=1, le=100, default=5)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    version: str = Field(min_length=1, default="v1")


class VectorRetrievalItem(BaseModel):
    document_id: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    score: float
    content_hash: str = Field(min_length=1)


class VectorRetrievalResponse(BaseModel):
    items: list[VectorRetrievalItem]


class KeywordRetrievalRequest(BaseModel):
    query_text: str = Field(min_length=1)
    top_k: int = Field(ge=1, le=100, default=5)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    version: str = Field(min_length=1, default="v1")


class KeywordRetrievalResponse(BaseModel):
    items: list[VectorRetrievalItem]


class FusedRetrievalRequest(BaseModel):
    vector_results: list[VectorRetrievalItem]
    keyword_results: list[VectorRetrievalItem]
    top_k: int = Field(ge=1, le=100, default=5)
    vector_weight: float = Field(ge=0.0, le=1.0, default=0.7)
    keyword_weight: float = Field(ge=0.0, le=1.0, default=0.3)


class FusedRetrievalItem(VectorRetrievalItem):
    vector_score: float = 0.0
    keyword_score: float = 0.0
    fused_score: float


class FusedRetrievalResponse(BaseModel):
    items: list[FusedRetrievalItem]
