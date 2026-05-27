# Epic: Phase 7 - Reliability and fault tolerance

## Summary
Make failure handling explicit, safe, and observable across external dependency boundaries.

## Scope
This Epic maps to Phase 7 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P7-T01 | Add timeout and retry policies to external calls | Completed | 2026-05-27 | Added timeout wrappers and retry policies for embedding and LLM provider boundaries with deterministic tests |
| P7-T02 | Add circuit breaker and fallback strategy | Completed | 2026-05-27 | Added deterministic circuit-breaker wrappers with fallback-provider support and transition tests |
| P7-T03 | Add idempotency protections | Completed | 2026-05-27 | Added deterministic idempotency key replay/conflict handling for answers and embeddings routes with tests |
| P7-T04 | Implement graceful degradation paths | Completed | 2026-05-27 | Added deterministic degraded responses for answer and embedding provider failures with tests |
| P7-T05 | Normalize internal-to-user error responses | Completed | 2026-05-27 | Added normalized reliability response fields and shared error-detail contract across routes |
| P7-T06 | Add failure injection tests | Completed | 2026-05-27 | Added deterministic failure injection coverage for degraded and idempotent replay paths |
| P7-T07 | Add failure observability fields | In progress | 2026-05-27 | Next active task |
| P7-T08 | Document resilience and runbook guidance | Not started | - | Pending |
