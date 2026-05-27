from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

SessionStatus = Literal["active", "archived", "expired"]
MessageRole = Literal["system", "user", "assistant"]


class ChatSessionCreateRequest(BaseModel):
    session_key: str = Field(min_length=1, max_length=64)
    user_id: str | None = Field(default=None, min_length=1, max_length=128)
    title: str | None = Field(default=None, min_length=1, max_length=256)

    @field_validator("session_key")
    @classmethod
    def validate_session_key(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("session_key must not be blank")
        return cleaned


class ChatSessionResponse(BaseModel):
    id: int = Field(ge=1)
    session_key: str = Field(min_length=1)
    user_id: str | None = None
    title: str | None = None
    status: SessionStatus = "active"
    created_at: datetime
    updated_at: datetime


class ChatMessageCreateRequest(BaseModel):
    role: MessageRole
    content: str = Field(min_length=1)
    metadata: dict[str, str] | None = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("content must not be blank")
        return cleaned


class ChatMessageResponse(BaseModel):
    id: int = Field(ge=1)
    session_id: int = Field(ge=1)
    turn_index: int = Field(ge=0)
    role: MessageRole
    content: str = Field(min_length=1)
    metadata: dict[str, str] | None = None
    created_at: datetime


class FollowUpContextRequest(BaseModel):
    session_key: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1)
    max_messages: int = Field(ge=1, le=50, default=8)
    max_turns: int = Field(ge=1, le=50, default=8)


class FollowUpContextMessage(BaseModel):
    turn_index: int = Field(ge=0)
    role: MessageRole
    content: str = Field(min_length=1)


class FollowUpContextResponse(BaseModel):
    session_key: str = Field(min_length=1)
    messages: list[FollowUpContextMessage]
    context_text: str


class SessionSummaryRequest(BaseModel):
    session_key: str = Field(min_length=1, max_length=64)
    min_messages: int = Field(ge=1, le=200, default=12)
    max_messages_in_summary: int = Field(ge=1, le=100, default=16)
    max_points: int = Field(ge=1, le=20, default=6)


class SessionSummaryResponse(BaseModel):
    session_key: str = Field(min_length=1)
    applied: bool
    message_count: int = Field(ge=0)
    summary: str | None = None


class TranscriptMessage(BaseModel):
    turn_index: int = Field(ge=0)
    role: MessageRole
    content: str = Field(min_length=1)
    metadata: dict[str, str] | None = None


class SessionTranscript(BaseModel):
    session_key: str = Field(min_length=1)
    user_id: str | None = None
    title: str | None = None
    status: SessionStatus = "active"
    messages: list[TranscriptMessage] = Field(default_factory=list)


class TranscriptImportRequest(BaseModel):
    transcript: SessionTranscript
    session_key_override: str | None = Field(default=None, min_length=1, max_length=64)
