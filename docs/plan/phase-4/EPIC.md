# Epic: Phase 4 - Hybrid retrieval and reranking

## Summary
Retrieve top-K relevant chunks via vector and keyword search with optional reranking.

## Scope
This Epic maps to Phase 4 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P4-T01 | Implement vector retrieval | Completed | 2026-05-27 | Added vector retrieval schemas, service scoring, and unit tests |
| P4-T02 | Implement keyword retrieval | Completed | 2026-05-27 | Added keyword retrieval service with deterministic ranking tests |
| P4-T03 | Merge and deduplicate results with explicit fusion logic | Completed | 2026-05-27 | Added deterministic fusion service with explicit dedup and tie-break rules |
| P4-T04 | Add pluggable reranker interface | Completed | 2026-05-27 | Added reranker contracts and baseline implementations with tests |
| P4-T05 | Add retrieval API endpoint with score and citation metadata | In progress | 2026-05-27 | Next active task |
| P4-T06 | Add end-to-end retrieval tests and metrics | Not started | - | Pending |
| P4-T07 | Log retrieval diagnostics and timings | Not started | - | Pending |
| P4-T08 | Document fusion and reranking behavior | Not started | - | Pending |
