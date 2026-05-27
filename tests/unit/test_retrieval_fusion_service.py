import pytest

from farmer_helper.schemas.retrieval import FusedRetrievalRequest, VectorRetrievalItem
from farmer_helper.services.retrieval.fusion_service import RetrievalFusionService


def test_fusion_merges_and_deduplicates_same_chunk_identity() -> None:
    service = RetrievalFusionService()

    response = service.fuse(
        FusedRetrievalRequest(
            vector_results=[
                VectorRetrievalItem(document_id=1, chunk_index=0, score=0.9, content_hash="h1"),
                VectorRetrievalItem(document_id=2, chunk_index=0, score=0.8, content_hash="h2"),
            ],
            keyword_results=[
                VectorRetrievalItem(document_id=1, chunk_index=0, score=2.0, content_hash="h1"),
                VectorRetrievalItem(document_id=3, chunk_index=0, score=1.0, content_hash="h3"),
            ],
            top_k=5,
            vector_weight=0.7,
            keyword_weight=0.3,
        )
    )

    assert len(response.items) == 3
    doc_chunk_pairs = [(item.document_id, item.chunk_index) for item in response.items]
    assert doc_chunk_pairs.count((1, 0)) == 1


def test_fusion_ranking_is_deterministic_on_score_ties() -> None:
    service = RetrievalFusionService()

    response = service.fuse(
        FusedRetrievalRequest(
            vector_results=[
                VectorRetrievalItem(document_id=2, chunk_index=0, score=1.0, content_hash="h2"),
                VectorRetrievalItem(document_id=1, chunk_index=1, score=1.0, content_hash="h1"),
            ],
            keyword_results=[],
            top_k=5,
            vector_weight=1.0,
            keyword_weight=0.0,
        )
    )

    assert [(item.document_id, item.chunk_index) for item in response.items] == [(1, 1), (2, 0)]


def test_fusion_applies_top_k_limit() -> None:
    service = RetrievalFusionService()

    response = service.fuse(
        FusedRetrievalRequest(
            vector_results=[
                VectorRetrievalItem(document_id=1, chunk_index=0, score=0.9, content_hash="h1"),
                VectorRetrievalItem(document_id=2, chunk_index=0, score=0.8, content_hash="h2"),
                VectorRetrievalItem(document_id=3, chunk_index=0, score=0.7, content_hash="h3"),
            ],
            keyword_results=[],
            top_k=2,
            vector_weight=1.0,
            keyword_weight=0.0,
        )
    )

    assert len(response.items) == 2
    assert [item.document_id for item in response.items] == [1, 2]


def test_fusion_rejects_all_zero_weights() -> None:
    service = RetrievalFusionService()

    with pytest.raises(ValueError):
        service.fuse(
            FusedRetrievalRequest(
                vector_results=[],
                keyword_results=[],
                top_k=5,
                vector_weight=0.0,
                keyword_weight=0.0,
            )
        )
