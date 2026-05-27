from typing import Literal

from pydantic import BaseModel, Field

Decision = Literal["answer", "clarify", "refuse"]


class Citation(BaseModel):
    document_id: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    content_hash: str = Field(min_length=1)


class RetrievedChunk(BaseModel):
    citation: Citation
    text: str = Field(min_length=1)
    score: float


class PromptBuildRequest(BaseModel):
    question: str = Field(min_length=1)
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)
    max_chunks: int = Field(ge=1, le=20, default=5)


class PromptBuildResult(BaseModel):
    decision: Decision
    system_prompt: str
    user_prompt: str
    clarification_message: str | None = None
    refusal_reason: str | None = None
