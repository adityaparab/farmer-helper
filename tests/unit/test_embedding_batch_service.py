from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.batch_service import EmbeddingBatchService
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


class RecordingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.calls: list[EmbeddingRequest] = []

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        self.calls.append(request)
        items = [
            EmbeddingItem(index=index, vector=[float(len(text)), float(index)])
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=2)


class InvalidIndexProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        items = [
            EmbeddingItem(index=1, vector=[1.0, 1.0]),
            EmbeddingItem(index=2, vector=[2.0, 2.0]),
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=2)


class InconsistentDimensionsProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self._calls = 0

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        self._calls += 1
        dimensions = 2 if self._calls == 1 else 3
        items = [
            EmbeddingItem(index=index, vector=[float(index)] * dimensions)
            for index, _ in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=dimensions)


def test_batch_service_batches_requests_and_preserves_global_order() -> None:
    provider = RecordingProvider()
    service = EmbeddingBatchService(provider, batch_size=2)

    response = service.embed_texts(
        texts=["soil", "rainfall", "fertilizer", "mulch", "irrigation"],
        model="test-model",
    )

    assert [len(call.texts) for call in provider.calls] == [2, 2, 1]
    assert response.model == "test-model"
    assert response.dimensions == 2
    assert [item.index for item in response.items] == [0, 1, 2, 3, 4]


def test_batch_service_rejects_invalid_provider_indexes() -> None:
    provider = InvalidIndexProvider()
    service = EmbeddingBatchService(provider, batch_size=2)

    try:
        service.embed_texts(texts=["a", "b"], model="test-model")
    except EmbeddingProviderError as exc:
        assert exc.code == "EMBEDDING_PROVIDER_INVALID_INDEXES"
    else:
        raise AssertionError("Expected EmbeddingProviderError for invalid indexes")


def test_batch_service_rejects_inconsistent_dimensions_across_batches() -> None:
    provider = InconsistentDimensionsProvider()
    service = EmbeddingBatchService(provider, batch_size=1)

    try:
        service.embed_texts(texts=["alpha", "beta"], model="test-model")
    except EmbeddingProviderError as exc:
        assert exc.code == "EMBEDDING_PROVIDER_INCONSISTENT_DIMENSIONS"
    else:
        raise AssertionError("Expected EmbeddingProviderError for inconsistent dimensions")
