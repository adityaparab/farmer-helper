from farmer_helper.schemas.retrieval import (
    FusedRetrievalRequest,
    KeywordRetrievalRequest,
    RerankRequest,
    RetrievalCitation,
    RetrievalItem,
    RetrievalRequest,
    RetrievalResponse,
    VectorRetrievalRequest,
)
from farmer_helper.services.retrieval.fusion_service import RetrievalFusionService
from farmer_helper.services.retrieval.keyword_retrieval_service import KeywordRetrievalService
from farmer_helper.services.retrieval.reranker import Reranker
from farmer_helper.services.retrieval.vector_retrieval_service import VectorRetrievalService


class RetrievalQueryService:
    def __init__(
        self,
        vector_service: VectorRetrievalService,
        keyword_service: KeywordRetrievalService,
        fusion_service: RetrievalFusionService,
        reranker: Reranker | None = None,
    ) -> None:
        self._vector_service = vector_service
        self._keyword_service = keyword_service
        self._fusion_service = fusion_service
        self._reranker = reranker

    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        vector_response = self._vector_service.retrieve(
            VectorRetrievalRequest(
                query_vector=request.query_vector,
                top_k=request.top_k,
                provider=request.provider,
                model=request.model,
                version=request.version,
            )
        )
        keyword_response = self._keyword_service.retrieve(
            KeywordRetrievalRequest(
                query_text=request.query_text,
                top_k=request.top_k,
                provider=request.provider,
                model=request.model,
                version=request.version,
            )
        )
        fused = self._fusion_service.fuse(
            FusedRetrievalRequest(
                vector_results=vector_response.items,
                keyword_results=keyword_response.items,
                top_k=request.top_k,
                vector_weight=request.vector_weight,
                keyword_weight=request.keyword_weight,
            )
        )

        ranked_items = fused.items
        if self._reranker is not None:
            ranked_items = self._reranker.rerank(
                RerankRequest(
                    query_text=request.query_text,
                    items=ranked_items,
                    top_k=request.top_k,
                )
            ).items

        return RetrievalResponse(
            items=[
                RetrievalItem(
                    document_id=item.document_id,
                    chunk_index=item.chunk_index,
                    content_hash=item.content_hash,
                    score=item.fused_score,
                    vector_score=item.vector_score,
                    keyword_score=item.keyword_score,
                    fused_score=item.fused_score,
                    citation=RetrievalCitation(
                        document_id=item.document_id,
                        chunk_index=item.chunk_index,
                        content_hash=item.content_hash,
                    ),
                )
                for item in ranked_items
            ]
        )
