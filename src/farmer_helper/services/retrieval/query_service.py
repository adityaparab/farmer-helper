import time

from farmer_helper.schemas.retrieval import (
    FusedRetrievalRequest,
    KeywordRetrievalRequest,
    RerankRequest,
    RetrievalCitation,
    RetrievalItem,
    RetrievalMetrics,
    RetrievalRequest,
    RetrievalResponse,
    VectorRetrievalRequest,
)
from farmer_helper.services.retrieval.diagnostics_logger import RetrievalDiagnosticsLogger
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
        diagnostics_logger: RetrievalDiagnosticsLogger | None = None,
    ) -> None:
        self._vector_service = vector_service
        self._keyword_service = keyword_service
        self._fusion_service = fusion_service
        self._reranker = reranker
        self._diagnostics_logger = diagnostics_logger or RetrievalDiagnosticsLogger()

    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        total_start = time.perf_counter()

        vector_start = time.perf_counter()
        vector_response = self._vector_service.retrieve(
            VectorRetrievalRequest(
                query_vector=request.query_vector,
                top_k=request.top_k,
                provider=request.provider,
                model=request.model,
                version=request.version,
            )
        )
        vector_ms = (time.perf_counter() - vector_start) * 1000

        keyword_start = time.perf_counter()
        keyword_response = self._keyword_service.retrieve(
            KeywordRetrievalRequest(
                query_text=request.query_text,
                top_k=request.top_k,
                provider=request.provider,
                model=request.model,
                version=request.version,
            )
        )
        keyword_ms = (time.perf_counter() - keyword_start) * 1000

        fusion_start = time.perf_counter()
        fused = self._fusion_service.fuse(
            FusedRetrievalRequest(
                vector_results=vector_response.items,
                keyword_results=keyword_response.items,
                top_k=request.top_k,
                vector_weight=request.vector_weight,
                keyword_weight=request.keyword_weight,
            )
        )
        fusion_ms = (time.perf_counter() - fusion_start) * 1000

        ranked_items = fused.items
        rerank_ms = 0.0
        if self._reranker is not None:
            rerank_start = time.perf_counter()
            ranked_items = self._reranker.rerank(
                RerankRequest(
                    query_text=request.query_text,
                    items=ranked_items,
                    top_k=request.top_k,
                )
            ).items
            rerank_ms = (time.perf_counter() - rerank_start) * 1000

        total_ms = (time.perf_counter() - total_start) * 1000
        self._diagnostics_logger.query_completed(
            provider=request.provider,
            model=request.model,
            version=request.version,
            top_k=request.top_k,
            reranker=request.reranker,
            vector_weight=request.vector_weight,
            keyword_weight=request.keyword_weight,
            vector_count=len(vector_response.items),
            keyword_count=len(keyword_response.items),
            fused_count=len(fused.items),
            returned_count=len(ranked_items),
            vector_ms=vector_ms,
            keyword_ms=keyword_ms,
            fusion_ms=fusion_ms,
            rerank_ms=rerank_ms,
            total_ms=total_ms,
        )

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
            ],
            metrics=RetrievalMetrics(
                vector_count=len(vector_response.items),
                keyword_count=len(keyword_response.items),
                fused_count=len(fused.items),
                returned_count=len(ranked_items),
            ),
        )
