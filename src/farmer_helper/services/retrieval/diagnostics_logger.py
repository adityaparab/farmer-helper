import logging


class RetrievalDiagnosticsLogger:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def query_completed(
        self,
        *,
        provider: str,
        model: str,
        version: str,
        top_k: int,
        reranker: str,
        vector_weight: float,
        keyword_weight: float,
        vector_count: int,
        keyword_count: int,
        fused_count: int,
        returned_count: int,
        vector_ms: float,
        keyword_ms: float,
        fusion_ms: float,
        rerank_ms: float,
        total_ms: float,
    ) -> None:
        self._logger.info(
            "retrieval.query.completed",
            extra={
                "retrieval_provider": provider,
                "retrieval_model": model,
                "retrieval_version": version,
                "retrieval_top_k": top_k,
                "retrieval_reranker": reranker,
                "retrieval_vector_weight": vector_weight,
                "retrieval_keyword_weight": keyword_weight,
                "retrieval_vector_count": vector_count,
                "retrieval_keyword_count": keyword_count,
                "retrieval_fused_count": fused_count,
                "retrieval_returned_count": returned_count,
                "retrieval_vector_ms": round(vector_ms, 4),
                "retrieval_keyword_ms": round(keyword_ms, 4),
                "retrieval_fusion_ms": round(fusion_ms, 4),
                "retrieval_rerank_ms": round(rerank_ms, 4),
                "retrieval_total_ms": round(total_ms, 4),
            },
        )
