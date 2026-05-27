# Epic: Phase 11 - Performance optimization and cost controls

## Summary
Improve runtime efficiency and control model/provider usage costs while preserving determinism and testability.

## Scope
This Epic maps to Phase 11 in docs/plan/PHASES.md and tracks local sub-issue status.

## Epic status
- Status: Completed
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P11-T01 | Add caching for retrieval and answers where appropriate | Completed | 2026-05-27 | Added configurable TTL caches for retrieval and answer routes |
| P11-T02 | Add model tiering/routing | Completed | 2026-05-27 | Added auto model router with low-cost/high-quality routing policy |
| P11-T03 | Add context trimming and deduplication | Completed | 2026-05-27 | Added bounded context compaction and duplicate message elimination |
| P11-T04 | Move heavy work off request path asynchronously | Completed | 2026-05-27 | Added async embeddings trigger endpoint with background job status tracking |
| P11-T05 | Add performance and cost regression tests | Completed | 2026-05-27 | Added cache/routing/async regression tests for call and latency-sensitive paths |
| P11-T06 | Document tuning and cost-control levers | Completed | 2026-05-27 | Added performance runbook and config tuning references |
