from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.schemas.answering import AnswerGenerationRequest, AnswerGenerationResponse
from farmer_helper.services.answering.generation_service import AnswerGenerationService
from farmer_helper.services.answering.mock_provider import MockLLMProvider
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProviderError
from farmer_helper.services.session.context_resolver import FollowUpContextResolver

router = APIRouter(prefix="/answers", tags=["answers"])


def build_answer_generation_service(db: Session) -> AnswerGenerationService:
    return AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=MockLLMProvider(),
        context_resolver=FollowUpContextResolver(ChatSessionRepository(db)),
    )


@router.post("/generate", response_model=AnswerGenerationResponse)
def generate_answer(
    request: AnswerGenerationRequest,
    db: Session = Depends(get_db_session),
) -> AnswerGenerationResponse:  # noqa: B008
    service = build_answer_generation_service(db)
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
