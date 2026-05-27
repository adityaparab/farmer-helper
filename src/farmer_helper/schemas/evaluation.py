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


class EvalScoreBreakdown(BaseModel):
    retrieval_relevance: int = Field(ge=0, le=2)
    groundedness: int = Field(ge=0, le=2)
    citation_correctness: int = Field(ge=0, le=2)
    safety_refusal: int = Field(ge=0, le=2)
    clarity_actionability: int = Field(ge=0, le=2)

    def total(self) -> int:
        return (
            self.retrieval_relevance
            + self.groundedness
            + self.citation_correctness
            + self.safety_refusal
            + self.clarity_actionability
        )


class EvalRunConfig(BaseModel):
    pass_threshold: int = Field(ge=0, le=10, default=6)


class EvalItemRunResult(BaseModel):
    id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    difficulty: Difficulty
    must_cite_source: bool
    score_breakdown: EvalScoreBreakdown
    total_score: int = Field(ge=0, le=10)
    max_score: int = Field(ge=1, default=10)
    passed: bool


class EvalRunResult(BaseModel):
    dataset_version: str = Field(min_length=1)
    total_items: int = Field(ge=1)
    passed_items: int = Field(ge=0)
    failed_items: int = Field(ge=0)
    average_score: float = Field(ge=0.0, le=10.0)
    item_results: list[EvalItemRunResult] = Field(min_length=1)


class EvalOfflineReportSummary(BaseModel):
    total_items: int = Field(ge=1)
    passed_items: int = Field(ge=0)
    failed_items: int = Field(ge=0)
    average_score: float = Field(ge=0.0, le=10.0)


class EvalOfflineReportItem(BaseModel):
    id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    difficulty: Difficulty
    must_cite_source: bool
    total_score: int = Field(ge=0, le=10)
    max_score: int = Field(ge=1)
    passed: bool
    score_breakdown: EvalScoreBreakdown


class EvalOfflineReport(BaseModel):
    generated_at_utc: str = Field(min_length=1)
    dataset_version: str = Field(min_length=1)
    summary: EvalOfflineReportSummary
    items: list[EvalOfflineReportItem] = Field(min_length=1)
