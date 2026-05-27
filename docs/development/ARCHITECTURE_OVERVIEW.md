# Architecture Overview

## Layering
1. API layer: `src/farmer_helper/api/`
2. Service layer: `src/farmer_helper/services/`
3. Repository layer: `src/farmer_helper/repositories/`
4. Schema layer: `src/farmer_helper/schemas/`
5. Core/config/logging: `src/farmer_helper/core/`
6. Persistence models: `src/farmer_helper/db/models/`

## Current capabilities
1. FastAPI app shell with app factory.
2. Health endpoints (`/health/live`, `/health/ready`).
3. Structured JSON logging with request ID propagation.
4. Foundational schema and migration path via Alembic.
5. Deterministic ingestion pipeline with status persistence and trace logging.
6. Embedding pipeline foundation with provider abstraction, batching, retries, orchestration, and API/CLI triggers.
7. Hybrid retrieval foundation with vector retrieval, keyword retrieval, fusion, optional reranking, retrieval API, and diagnostics logging.
8. Answer-generation prompt builder foundation with deterministic refusal and clarification policy.
9. Answer-generation API foundation with provider abstraction and deterministic mock provider.
10. Answer-generation diagnostics logging for latency, token usage, decision path, and confidence fields.
11. Session-memory foundation with chat session/message schemas and repository persistence.
12. Follow-up context resolution with bounded deterministic message-window selection.
13. Optional long-session summarization with threshold-based activation.
14. Bounded session-context propagation into retrieval and answer-generation request flows.
15. Session lifecycle management with deterministic archival and expiry transitions.
16. Session transcript export/import with deterministic round-trip behavior.
17. External call resilience baseline with timeout policies and deterministic retries for embedding and LLM providers.
18. Circuit-breaker and fallback-provider strategy for external embedding and LLM call boundaries.
19. Deterministic idempotency key replay/conflict handling for reliability-sensitive API operations.
20. Deterministic graceful degradation responses for provider failures in embedding and answer-generation APIs.
21. Normalized internal-to-user reliability contracts for degraded outcomes and conflict errors.
22. Deterministic failure-injection test coverage for degraded flows and idempotent replay under provider faults.
23. Structured reliability observability fields for degraded and conflict paths with low-cardinality codes.
24. Evaluation dataset loading foundation with strict typed validation for JSON/JSONL inputs.
25. Deterministic eval runner foundation with typed per-item scoring and aggregate pass/fail metrics.
26. Deterministic offline eval reporting foundation with stable JSON serialization output.
27. CI-integrated eval regression gate with deterministic threshold checks and report artifact generation.
28. Typed online feedback signal capture endpoint with structured low-cardinality observability logs.
29. Incrementally expanded seed eval dataset with deterministic ID ordering and integrity coverage tests.
30. Evaluation maintenance runbook for CI triage, metric interpretation, and dataset expansion policy.
31. Observability baseline with request lifecycle logs, route-level timings, and optional Sentry initialization.
32. Centralized log privacy redaction filter for sensitive top-level and nested fields.
33. Security guard baseline with configurable API-key auth and in-memory rate limiting for non-health routes.
34. Prompt-injection refusal path with deterministic refusal code and structured security audit events.
35. Security schema hardening with bounded lengths and strict non-blank validators.

## Operational references
1. Ingestion flow guide: `docs/development/INGESTION_PIPELINE.md`
2. Embedding provider guide: `docs/development/EMBEDDING_PROVIDERS.md`
3. Retrieval pipeline guide: `docs/development/RETRIEVAL_PIPELINE.md`
4. Answering pipeline guide: `docs/development/ANSWERING_PIPELINE.md`
5. Session behavior guide: `docs/development/SESSION_BEHAVIOR.md`
6. Reliability runbook: `docs/development/RELIABILITY_RUNBOOK.md`
7. Evaluation runbook: `docs/development/EVALUATION_RUNBOOK.md`
8. Observability runbook: `docs/development/OBSERVABILITY_RUNBOOK.md`
9. Security runbook: `docs/development/SECURITY_RUNBOOK.md`

## Next phases
1. Hybrid retrieval and reranking pipeline.
2. Grounded answer generation with citations.
3. Session memory and multi-turn handling.
