from abc import ABC, abstractmethod

from farmer_helper.schemas.retrieval import FusedRetrievalItem, RerankRequest, RerankResponse


class Reranker(ABC):
    @abstractmethod
    def rerank(self, request: RerankRequest) -> RerankResponse:
        """Rerank for retrieval workflows.

        This Reranker method belongs to the retrieval service layer. Inputs are request. It runs
        synchronously and returns when local processing is complete. Returns a RerankResponse
        value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        raise NotImplementedError


class PassThroughReranker(Reranker):
    def rerank(self, request: RerankRequest) -> RerankResponse:
        """Rerank for retrieval workflows.

        This PassThroughReranker method belongs to the retrieval service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        RerankResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        items = sorted(
            request.items,
            key=lambda item: (
                -item.fused_score,
                -item.vector_score,
                -item.keyword_score,
                item.document_id,
                item.chunk_index,
            ),
        )
        return RerankResponse(items=items[: request.top_k])


class KeywordBoostReranker(Reranker):
    def __init__(self, boost: float = 0.1) -> None:
        """Init for retrieval workflows.

        Initialize KeywordBoostReranker for retrieval workflows. Inputs are boost. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if boost < 0:
            raise ValueError("boost must be non-negative")
        self._boost = boost

    def rerank(self, request: RerankRequest) -> RerankResponse:
        """Rerank for retrieval workflows.

        This KeywordBoostReranker method belongs to the retrieval service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        RerankResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        query_terms = self._terms(request.query_text)
        rescored: list[FusedRetrievalItem] = []

        for item in request.items:
            bonus = self._boost if item.keyword_score > 0 and query_terms else 0.0
            updated = item.model_copy(
                update={
                    "fused_score": item.fused_score + bonus,
                    "score": item.fused_score + bonus,
                }
            )
            rescored.append(updated)

        rescored.sort(
            key=lambda item: (
                -item.fused_score,
                -item.vector_score,
                -item.keyword_score,
                item.document_id,
                item.chunk_index,
            )
        )
        return RerankResponse(items=rescored[: request.top_k])

    @staticmethod
    def _terms(query_text: str) -> list[str]:
        """Terms for retrieval workflows.

        This private helper belongs to the retrieval service layer. Inputs are query_text. It
        runs synchronously and returns when local processing is complete. Returns a list[str]
        value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        return [term for term in query_text.lower().split() if term]
