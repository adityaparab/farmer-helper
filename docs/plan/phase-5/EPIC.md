# Epic: Phase 5 - Grounded answer generation and citations

## Summary
Generate grounded, citation-rich answers using retrieved chunks with explicit refusal and clarification behavior.

## Scope
This Epic maps to Phase 5 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P5-T01 | Build prompt builder with refusal and clarification policy | Completed | 2026-05-27 | Added prompt builder service, schemas, and unit tests |
| P5-T02 | Add LLM provider abstraction | Completed | 2026-05-27 | Added LLM provider contracts, error semantics, and unit tests |
| P5-T03 | Build end-to-end answer generation API | Completed | 2026-05-27 | Added answer generation service, API route, and unit tests |
| P5-T04 | Add deterministic citation mapping | Completed | 2026-05-27 | Added deterministic citation mapper with deduplication and ordering tests |
| P5-T05 | Add refusal and ambiguity handling | Completed | 2026-05-27 | Added policy codes and regression tests for refusal/clarification outcomes |
| P5-T06 | Add grounded-response regression tests | Completed | 2026-05-27 | Added table-driven integration regression scenarios for answer/clarify/refuse paths |
| P5-T07 | Add usage, latency, and confidence logging | In progress | 2026-05-27 | Next active task |
| P5-T08 | Document prompting and provider switching | Not started | - | Pending |
