from fastapi import APIRouter, HTTPException

from farmer_helper.schemas.answering import AnswerGenerationRequest, AnswerGenerationResponse
from farmer_helper.services.answering.generation_service import AnswerGenerationService
from farmer_helper.services.answering.mock_provider import MockLLMProvider
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProviderError

router = APIRouter(prefix="/answers", tags=["answers"])


def build_answer_generation_service() -> AnswerGenerationService:
    return AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=MockLLMProvider(),
    )


@router.post("/generate", response_model=AnswerGenerationResponse)
def generate_answer(request: AnswerGenerationRequest) -> AnswerGenerationResponse:
    service = build_answer_generation_service()
    try:
        return service.generate(request)
    except LLMProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error_code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable,
            },
        ) from exc
