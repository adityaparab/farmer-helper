# Embedding Provider Versioning and Extension Guide

## Purpose
This document defines how embedding provider identity and versioning are represented, and how to extend Farmer Helper with additional embedding providers safely.

## Current provider stack
Current trigger execution path uses:
1. `MockEmbeddingProvider` for deterministic vector generation in local/test environments.
2. `RetryingEmbeddingProvider` for bounded retry behavior.
3. `EmbeddingBatchService` for stable batching and response validation.
4. `EmbeddingOrchestrationService` for persistence orchestration.

## Versioning fields and semantics
Provider/version identity is explicit across API requests and persistence records:
- Trigger request fields (`EmbeddingTriggerRequest`):
  - `provider`
  - `version`
  - `model`
- Persistence identity fields (`ChunkEmbedding`):
  - `document_id`
  - `chunk_index`
  - `provider`
  - `model`
  - `version`

Unique upsert identity:
`document_id + chunk_index + provider + model + version`

This allows multiple embedding generations for the same chunk under different provider/model/version combinations without collision.

## Compatibility guidance
1. Treat `provider + model + version` as immutable identity for downstream retrieval behavior.
2. Increment `version` when embedding generation semantics change (tokenization, normalization, vector dimensions, or provider-side behavior changes).
3. Keep `dimensions` consistent within a single embedding run; batching layer rejects inconsistent provider responses.

## Adding a new provider
1. Implement `EmbeddingProvider` in a dedicated module under `src/farmer_helper/services/embedding/`.
2. Raise `EmbeddingProviderError` with accurate `code` and `retryable` semantics.
3. Validate provider behavior using unit tests for:
   - Success path
   - Retryable failures
   - Non-retryable failures
   - Response contract validity (counts/indexes/dimensions)
4. Wire provider into trigger construction paths:
   - API route (`src/farmer_helper/api/routes/embeddings.py`)
   - CLI trigger (`scripts/trigger-embeddings.py`)

## Migration path toward external providers
When introducing external API providers:
1. Keep `MockEmbeddingProvider` as deterministic fallback for local development and tests.
2. Add provider-specific config through `Settings` (API keys, endpoints, model defaults).
3. Preserve existing contract models to avoid trigger or persistence API churn.
4. Keep retry behavior bounded through `EmbeddingRetryPolicy`.

## Operational checks
Before enabling a new provider in production-like environments:
1. Run full quality gates:
   - `ruff check src tests alembic scripts/trigger-embeddings.py`
   - `black --check src tests alembic scripts/trigger-embeddings.py`
   - `mypy src`
   - `pytest -q`
2. Validate trigger route behavior for success and provider-failure responses.
3. Verify persisted embeddings include expected `provider`, `model`, and `version` metadata.
