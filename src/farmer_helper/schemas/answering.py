from typing import Literal

from pydantic import BaseModel, Field, field_validator

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
    clarification_code: str | None = None
    refusal_reason: str | None = None
    refusal_code: str | None = None


Role = Literal["system", "user", "assistant"]


class LLMMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message content must not be blank")
        return value


class LLMGenerateRequest(BaseModel):
    model: str = Field(min_length=1)
    messages: list[LLMMessage] = Field(min_length=1)
    max_tokens: int = Field(ge=1, le=4096, default=512)
    temperature: float = Field(ge=0.0, le=1.0, default=0.0)


class LLMGenerateResponse(BaseModel):
    model: str = Field(min_length=1)
    text: str = Field(min_length=1)
    finish_reason: Literal["stop", "length", "content_filter"]
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)


class AnswerGenerationRequest(BaseModel):
    question: str = Field(min_length=1)
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=128)
    session_key: str | None = Field(default=None, min_length=1, max_length=64)
    context_max_messages: int = Field(ge=1, le=50, default=8)
    context_max_turns: int = Field(ge=1, le=50, default=8)
    model: str = Field(min_length=1, default="mock-chat-v1")
    max_chunks: int = Field(ge=1, le=20, default=5)
    max_answer_tokens: int = Field(ge=1, le=4096, default=512)
    temperature: float = Field(ge=0.0, le=1.0, default=0.0)


class AnswerGenerationResponse(BaseModel):
    decision: Decision
    answer: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    clarification_message: str | None = None
    clarification_code: str | None = None
    refusal_reason: str | None = None
    refusal_code: str | None = None
    model: str | None = None
    finish_reason: Literal["stop", "length", "content_filter"] | None = None
    input_tokens: int = Field(ge=0, default=0)
    output_tokens: int = Field(ge=0, default=0)
