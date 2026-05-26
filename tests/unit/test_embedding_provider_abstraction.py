import pytest
from pydantic import ValidationError

from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        items = [
            EmbeddingItem(index=index, vector=[float(len(text)), float(index)])
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=2)


class FailingEmbeddingProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_RATE_LIMIT",
            message=f"Rate limited for model {request.model}",
            retryable=True,
        )


def test_embedding_request_rejects_empty_texts() -> None:
    with pytest.raises(ValidationError):
        EmbeddingRequest(texts=[], model="test-model")


def test_embedding_request_rejects_blank_text_entries() -> None:
    with pytest.raises(ValidationError):
        EmbeddingRequest(texts=["valid", "   "], model="test-model")


def test_embedding_response_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValidationError):
        EmbeddingResponse(
            model="test-model",
            items=[
                EmbeddingItem(index=0, vector=[0.1, 0.2]),
                EmbeddingItem(index=1, vector=[0.3]),
            ],
            dimensions=2,
        )


def test_embedding_provider_contract_success() -> None:
    provider = FakeEmbeddingProvider()
    request = EmbeddingRequest(texts=["soil health", "crop rotation"], model="test-model")

    response = provider.embed(request)

    assert response.model == "test-model"
    assert response.dimensions == 2
    assert len(response.items) == 2
    assert response.items[0].index == 0
    assert response.items[1].index == 1


def test_embedding_provider_error_semantics() -> None:
    provider = FailingEmbeddingProvider()
    request = EmbeddingRequest(texts=["rainfall"], model="test-model")

    with pytest.raises(EmbeddingProviderError) as exc:
        provider.embed(request)

    assert exc.value.code == "EMBEDDING_PROVIDER_RATE_LIMIT"
    assert exc.value.retryable is True
    assert "Rate limited" in exc.value.message
