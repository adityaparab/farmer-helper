import math

from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.retrieval import (
    VectorRetrievalItem,
    VectorRetrievalRequest,
    VectorRetrievalResponse,
)


class VectorRetrievalService:
    def __init__(self, repository: ChunkEmbeddingRepository) -> None:
        self._repository = repository

    def retrieve(self, request: VectorRetrievalRequest) -> VectorRetrievalResponse:
        candidates = self._repository.list_for_retrieval(
            provider=request.provider,
            model=request.model,
            version=request.version,
        )

        query_norm = self._norm(request.query_vector)
        if query_norm == 0:
            return VectorRetrievalResponse(items=[])

        scored: list[VectorRetrievalItem] = []
        for candidate in candidates:
            vector = candidate.vector_json
            if len(vector) != len(request.query_vector):
                continue

            score = self._cosine_similarity(request.query_vector, vector, query_norm)
            scored.append(
                VectorRetrievalItem(
                    document_id=candidate.document_id,
                    chunk_index=candidate.chunk_index,
                    score=score,
                    content_hash=candidate.content_hash,
                )
            )

        scored.sort(key=lambda item: (-item.score, item.document_id, item.chunk_index))
        return VectorRetrievalResponse(items=scored[: request.top_k])

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float], left_norm: float) -> float:
        right_norm = VectorRetrievalService._norm(right)
        if right_norm == 0:
            return 0.0

        dot = sum(
            left_value * right_value for left_value, right_value in zip(left, right, strict=True)
        )
        return dot / (left_norm * right_norm)

    @staticmethod
    def _norm(vector: list[float]) -> float:
        return math.sqrt(sum(value * value for value in vector))
