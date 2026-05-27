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


class RerankRequest(BaseModel):
    query_text: str = Field(min_length=1)
    items: list[FusedRetrievalItem]
    top_k: int = Field(ge=1, le=100, default=5)


class RerankResponse(BaseModel):
    items: list[FusedRetrievalItem]


class RetrievalRequest(BaseModel):
    query_text: str = Field(min_length=1)
    query_vector: list[float] = Field(min_length=1)
    session_key: str | None = Field(default=None, min_length=1, max_length=64)
    context_max_messages: int = Field(ge=1, le=50, default=8)
    context_max_turns: int = Field(ge=1, le=50, default=8)
    top_k: int = Field(ge=1, le=100, default=5)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    version: str = Field(min_length=1, default="v1")
    vector_weight: float = Field(ge=0.0, le=1.0, default=0.7)
    keyword_weight: float = Field(ge=0.0, le=1.0, default=0.3)
    reranker: str = Field(min_length=1, default="none")


class RetrievalCitation(BaseModel):
    document_id: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    content_hash: str = Field(min_length=1)


class RetrievalItem(BaseModel):
    document_id: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    content_hash: str = Field(min_length=1)
    score: float
    vector_score: float
    keyword_score: float
    fused_score: float
    citation: RetrievalCitation


class RetrievalMetrics(BaseModel):
    vector_count: int = Field(ge=0)
    keyword_count: int = Field(ge=0)
    fused_count: int = Field(ge=0)
    returned_count: int = Field(ge=0)


class RetrievalResponse(BaseModel):
    items: list[RetrievalItem]
    metrics: RetrievalMetrics
