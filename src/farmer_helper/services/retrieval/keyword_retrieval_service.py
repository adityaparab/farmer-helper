import re

from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.retrieval import (
    KeywordRetrievalRequest,
    KeywordRetrievalResponse,
    VectorRetrievalItem,
)


class KeywordRetrievalService:
    def __init__(self, repository: ChunkEmbeddingRepository) -> None:
        self._repository = repository

    def retrieve(self, request: KeywordRetrievalRequest) -> KeywordRetrievalResponse:
        query_terms = self._terms(request.query_text)
        if not query_terms:
            return KeywordRetrievalResponse(items=[])

        candidates = self._repository.list_for_retrieval(
            provider=request.provider,
            model=request.model,
            version=request.version,
        )

        scored: list[VectorRetrievalItem] = []
        for candidate in candidates:
            score = self._score_text(candidate.chunk_text, query_terms)
            if score <= 0:
                continue
            scored.append(
                VectorRetrievalItem(
                    document_id=candidate.document_id,
                    chunk_index=candidate.chunk_index,
                    score=float(score),
                    content_hash=candidate.content_hash,
                )
            )

        scored.sort(key=lambda item: (-item.score, item.document_id, item.chunk_index))
        return KeywordRetrievalResponse(items=scored[: request.top_k])

    @staticmethod
    def _terms(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    @staticmethod
    def _score_text(chunk_text: str, query_terms: list[str]) -> int:
        haystack_terms = KeywordRetrievalService._terms(chunk_text)
        if not haystack_terms:
            return 0

        score = 0
        for term in query_terms:
            score += haystack_terms.count(term)
        return score
