from farmer_helper.schemas.retrieval import (
    FusedRetrievalItem,
    KeywordRetrievalResponse,
    RetrievalRequest,
    VectorRetrievalItem,
    VectorRetrievalResponse,
)
from farmer_helper.services.retrieval.query_service import RetrievalQueryService


class FakeVectorService:
    def retrieve(self, _request):  # type: ignore[no-untyped-def]
        return VectorRetrievalResponse(
            items=[
                VectorRetrievalItem(
                    document_id=1,
                    chunk_index=0,
                    content_hash="h1",
                    score=0.9,
                )
            ]
        )


class FakeKeywordService:
    def retrieve(self, _request):  # type: ignore[no-untyped-def]
        return KeywordRetrievalResponse(
            items=[
                VectorRetrievalItem(
                    document_id=1,
                    chunk_index=0,
                    content_hash="h1",
                    score=1.0,
                )
            ]
        )


class FakeFusionService:
    def fuse(self, _request):  # type: ignore[no-untyped-def]
        from farmer_helper.schemas.retrieval import FusedRetrievalResponse

        return FusedRetrievalResponse(
            items=[
                FusedRetrievalItem(
                    document_id=1,
                    chunk_index=0,
                    content_hash="h1",
                    score=0.93,
                    vector_score=0.9,
                    keyword_score=1.0,
                    fused_score=0.93,
                ),
                FusedRetrievalItem(
                    document_id=2,
                    chunk_index=0,
                    content_hash="h2",
                    score=0.85,
                    vector_score=0.82,
                    keyword_score=0.9,
                    fused_score=0.85,
                ),
            ]
        )


class ReverseReranker:
    def rerank(self, request):  # type: ignore[no-untyped-def]
        from farmer_helper.schemas.retrieval import RerankResponse

        return RerankResponse(items=list(reversed(request.items)))


def _request() -> RetrievalRequest:
    return RetrievalRequest(
        query_text="soil moisture",
        query_vector=[0.1, 0.2, 0.3],
        top_k=3,
        provider="mock-provider",
        model="mock-embedding-v1",
        version="v1",
        reranker="none",
    )


def test_retrieval_query_service_returns_citation_metadata() -> None:
    service = RetrievalQueryService(
        vector_service=FakeVectorService(),
        keyword_service=FakeKeywordService(),
        fusion_service=FakeFusionService(),
        reranker=None,
    )

    response = service.retrieve(_request())

    assert len(response.items) == 2
    item = response.items[0]
    assert item.score == item.fused_score
    assert item.citation.document_id == item.document_id
    assert item.citation.chunk_index == item.chunk_index
    assert item.citation.content_hash == item.content_hash
    assert response.metrics.vector_count == 1
    assert response.metrics.keyword_count == 1
    assert response.metrics.fused_count == 2
    assert response.metrics.returned_count == 2


def test_retrieval_query_service_invokes_optional_reranker() -> None:
    service = RetrievalQueryService(
        vector_service=FakeVectorService(),
        keyword_service=FakeKeywordService(),
        fusion_service=FakeFusionService(),
        reranker=ReverseReranker(),
    )

    response = service.retrieve(_request())
    assert len(response.items) == 2
    assert [item.document_id for item in response.items] == [2, 1]
