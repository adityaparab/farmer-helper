import pytest

from farmer_helper.schemas.retrieval import FusedRetrievalItem, RerankRequest
from farmer_helper.services.retrieval.reranker import KeywordBoostReranker, PassThroughReranker


def test_pass_through_reranker_preserves_deterministic_order() -> None:
    reranker = PassThroughReranker()
    response = reranker.rerank(
        RerankRequest(
            query_text="soil",
            top_k=3,
            items=[
                FusedRetrievalItem(
                    document_id=2,
                    chunk_index=0,
                    content_hash="h2",
                    score=0.8,
                    vector_score=0.8,
                    keyword_score=0.0,
                    fused_score=0.8,
                ),
                FusedRetrievalItem(
                    document_id=1,
                    chunk_index=1,
                    content_hash="h1",
                    score=0.8,
                    vector_score=0.8,
                    keyword_score=0.0,
                    fused_score=0.8,
                ),
            ],
        )
    )

    assert [(item.document_id, item.chunk_index) for item in response.items] == [(1, 1), (2, 0)]


def test_keyword_boost_reranker_boosts_keyword_hits() -> None:
    reranker = KeywordBoostReranker(boost=0.2)
    response = reranker.rerank(
        RerankRequest(
            query_text="soil moisture",
            top_k=2,
            items=[
                FusedRetrievalItem(
                    document_id=1,
                    chunk_index=0,
                    content_hash="h1",
                    score=0.7,
                    vector_score=0.7,
                    keyword_score=0.0,
                    fused_score=0.7,
                ),
                FusedRetrievalItem(
                    document_id=2,
                    chunk_index=0,
                    content_hash="h2",
                    score=0.65,
                    vector_score=0.5,
                    keyword_score=1.0,
                    fused_score=0.65,
                ),
            ],
        )
    )

    assert [item.document_id for item in response.items] == [2, 1]
    assert response.items[0].fused_score > response.items[1].fused_score


def test_keyword_boost_reranker_rejects_negative_boost() -> None:
    with pytest.raises(ValueError):
        KeywordBoostReranker(boost=-0.1)
