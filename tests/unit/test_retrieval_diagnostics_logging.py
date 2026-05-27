import logging
from logging import LogRecord

from pytest import LogCaptureFixture

from farmer_helper.schemas.retrieval import (
    FusedRetrievalItem,
    FusedRetrievalResponse,
    KeywordRetrievalResponse,
    RerankResponse,
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
                    score=0.5,
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
        return FusedRetrievalResponse(
            items=[
                FusedRetrievalItem(
                    document_id=1,
                    chunk_index=0,
                    content_hash="h1",
                    score=0.8,
                    vector_score=0.5,
                    keyword_score=1.0,
                    fused_score=0.8,
                )
            ]
        )


class FakeReranker:
    def rerank(self, request):  # type: ignore[no-untyped-def]
        return RerankResponse(items=request.items)


def _request(reranker: str) -> RetrievalRequest:
    return RetrievalRequest(
        query_text="soil",
        query_vector=[0.1, 0.2, 0.3],
        top_k=3,
        provider="mock-provider",
        model="mock-model",
        version="v1",
        reranker=reranker,
    )


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


def test_retrieval_query_logs_diagnostics_without_reranker(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    service = RetrievalQueryService(
        vector_service=FakeVectorService(),
        keyword_service=FakeKeywordService(),
        fusion_service=FakeFusionService(),
        reranker=None,
    )

    _ = service.retrieve(_request(reranker="none"))
    record = _find_record(caplog.records, "retrieval.query.completed")

    assert record.__dict__["retrieval_provider"] == "mock-provider"
    assert record.__dict__["retrieval_reranker"] == "none"
    assert record.__dict__["retrieval_vector_count"] == 1
    assert record.__dict__["retrieval_keyword_count"] == 1
    assert record.__dict__["retrieval_fused_count"] == 1
    assert record.__dict__["retrieval_returned_count"] == 1
    assert record.__dict__["retrieval_rerank_ms"] == 0.0
    assert record.__dict__["retrieval_total_ms"] >= 0.0


def test_retrieval_query_logs_diagnostics_with_reranker(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    service = RetrievalQueryService(
        vector_service=FakeVectorService(),
        keyword_service=FakeKeywordService(),
        fusion_service=FakeFusionService(),
        reranker=FakeReranker(),
    )

    _ = service.retrieve(_request(reranker="pass_through"))
    record = _find_record(caplog.records, "retrieval.query.completed")

    assert record.__dict__["retrieval_reranker"] == "pass_through"
    assert record.__dict__["retrieval_rerank_ms"] >= 0.0
