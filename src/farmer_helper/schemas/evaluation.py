from typing import Literal

from pydantic import BaseModel, Field, field_validator

Difficulty = Literal["easy", "medium", "hard"]


class EvalDatasetItem(BaseModel):
    id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    expected_topics: list[str] = Field(min_length=1)
    expected_keywords: list[str] = Field(default_factory=list)
    must_cite_source: bool
    difficulty: Difficulty
    notes: str | None = None

    @field_validator("id", "question")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value

    @field_validator("expected_topics", "expected_keywords")
    @classmethod
    def validate_terms(cls, value: list[str]) -> list[str]:
        for term in value:
            if not term.strip():
                raise ValueError("terms must not contain blank values")
        return value


class EvalDataset(BaseModel):
    version: str = Field(min_length=1, default="v1")
    items: list[EvalDatasetItem] = Field(min_length=1)
