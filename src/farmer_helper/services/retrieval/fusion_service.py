from farmer_helper.schemas.retrieval import (
    FusedRetrievalItem,
    FusedRetrievalRequest,
    FusedRetrievalResponse,
    VectorRetrievalItem,
)


class RetrievalFusionService:
    def fuse(self, request: FusedRetrievalRequest) -> FusedRetrievalResponse:
        """Combine for retrieval workflows.

        This RetrievalFusionService method belongs to the retrieval service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        FusedRetrievalResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if request.vector_weight == 0 and request.keyword_weight == 0:
            raise ValueError("At least one fusion weight must be > 0")

        merged: dict[tuple[int, int, str], FusedRetrievalItem] = {}

        for item in request.vector_results:
            key = self._key(item)
            fused = merged.get(key)
            if fused is None:
                fused = FusedRetrievalItem(
                    document_id=item.document_id,
                    chunk_index=item.chunk_index,
                    content_hash=item.content_hash,
                    score=0.0,
                    vector_score=item.score,
                    keyword_score=0.0,
                    fused_score=0.0,
                )
                merged[key] = fused
            else:
                fused.vector_score = max(fused.vector_score, item.score)

        for item in request.keyword_results:
            key = self._key(item)
            fused = merged.get(key)
            if fused is None:
                fused = FusedRetrievalItem(
                    document_id=item.document_id,
                    chunk_index=item.chunk_index,
                    content_hash=item.content_hash,
                    score=0.0,
                    vector_score=0.0,
                    keyword_score=item.score,
                    fused_score=0.0,
                )
                merged[key] = fused
            else:
                fused.keyword_score = max(fused.keyword_score, item.score)

        for fused in merged.values():
            fused.fused_score = (
                fused.vector_score * request.vector_weight
                + fused.keyword_score * request.keyword_weight
            )
            fused.score = fused.fused_score

        ranked = sorted(
            merged.values(),
            key=lambda item: (
                -item.fused_score,
                -item.vector_score,
                -item.keyword_score,
                item.document_id,
                item.chunk_index,
            ),
        )
        return FusedRetrievalResponse(items=ranked[: request.top_k])

    @staticmethod
    def _key(item: VectorRetrievalItem) -> tuple[int, int, str]:
        """Key for retrieval workflows.

        This private helper belongs to the retrieval service layer. Inputs are item. It runs
        synchronously and returns when local processing is complete. Returns a tuple[int, int,
        str] value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        return (item.document_id, item.chunk_index, item.content_hash)
