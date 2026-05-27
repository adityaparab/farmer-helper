from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from farmer_helper.db.base import get_db_session
from farmer_helper.repositories.chat_session_repository import ChatSessionRepository
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.retrieval import RetrievalRequest, RetrievalResponse
from farmer_helper.schemas.session import FollowUpContextRequest
from farmer_helper.services.retrieval.fusion_service import RetrievalFusionService
from farmer_helper.services.retrieval.keyword_retrieval_service import KeywordRetrievalService
from farmer_helper.services.retrieval.query_service import RetrievalQueryService
from farmer_helper.services.retrieval.reranker import (
    KeywordBoostReranker,
    PassThroughReranker,
    Reranker,
)
from farmer_helper.services.retrieval.vector_retrieval_service import VectorRetrievalService
from farmer_helper.services.session.context_resolver import FollowUpContextResolver

router = APIRouter(prefix="/retrieval", tags=["retrieval"])


def _build_reranker(name: str) -> Reranker | None:
    normalized = name.strip().lower()
    if normalized in {"", "none", "disabled"}:
        return None
    if normalized in {"pass_through", "passthrough"}:
        return PassThroughReranker()
    if normalized in {"keyword_boost", "keyword"}:
        return KeywordBoostReranker(boost=0.1)
    raise ValueError(f"Unsupported reranker: {name}")


def build_retrieval_service(db: Session, reranker_name: str) -> RetrievalQueryService:
    repository = ChunkEmbeddingRepository(db)
    return RetrievalQueryService(
        vector_service=VectorRetrievalService(repository=repository),
        keyword_service=KeywordRetrievalService(repository=repository),
        fusion_service=RetrievalFusionService(),
        reranker=_build_reranker(reranker_name),
    )


@router.post("/query", response_model=RetrievalResponse)
def query_retrieval(
    request: RetrievalRequest,
    db: Session = Depends(get_db_session),
) -> RetrievalResponse:  # noqa: B008
    try:
        effective_request = request
        if request.session_key:
            context = FollowUpContextResolver(ChatSessionRepository(db)).resolve(
                FollowUpContextRequest(
                    session_key=request.session_key,
                    question=request.query_text,
                    max_messages=request.context_max_messages,
                    max_turns=request.context_max_turns,
                )
            )
            if context.context_text:
                effective_request = request.model_copy(
                    update={
                        "query_text": (
                            "Follow-up context:\n"
                            f"{context.context_text}\n\n"
                            "Current question:\n"
                            f"{request.query_text}"
                        )
                    }
                )

        service = build_retrieval_service(db=db, reranker_name=request.reranker)
        return service.retrieve(effective_request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
