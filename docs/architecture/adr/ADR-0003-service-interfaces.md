# ADR-0003: Service interface and provider abstraction contracts

- Status: Accepted
- Date: 2026-05-26
- Owners: Platform/Backend

## Context
Later phases introduce multiple external providers (embeddings, LLM, reranking, observability sinks). Tight coupling to one provider would increase migration risk and reduce reliability options.

## Decision
Define explicit service interfaces and adapter contracts:
- Ingestion service contract: validate -> extract -> normalize -> chunk -> persist status.
- Embedding service contract: enqueue/select chunks -> batch embed -> persist vectors -> mark outcomes.
- Retrieval service contract: vector search + keyword search -> fusion -> optional rerank.
- Generation service contract: prompt build -> grounded answer generation -> citation map.

Provider adapters must implement typed interfaces with:
- Timeouts, retries, and error normalization.
- Deterministic request/response models.
- Usage/latency/cost telemetry hooks.

Configuration is injected through settings, not hardcoded.

## Consequences
### Positive
- Easier provider swaps and A/B validation.
- Better testability with fake/mock adapters.
- Failure and fallback behavior can be standardized.

### Trade-offs
- Interface design requires additional upfront effort.
- Adapter layers add some boilerplate.

### Follow-up constraints
- Error taxonomy and fallback matrix must align with these contracts (Phase 0 Task 6).
- KPI and evaluation framework should consume standardized telemetry fields (Phase 0 Task 5 and Phase 8).