# Epic: Phase 6 - Session memory and multi-turn handling

## Summary
Support bounded, traceable conversation memory and follow-up questions.

## Scope
This Epic maps to Phase 6 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P6-T01 | Add session and message schemas | Completed | 2026-05-27 | Added session/message DB models, schemas, repository, and tests |
| P6-T02 | Add follow-up context resolution | Completed | 2026-05-27 | Added bounded follow-up context resolver with deterministic ordering tests |
| P6-T03 | Add optional summarization for long sessions | Completed | 2026-05-27 | Added deterministic optional session summarizer and threshold-based tests |
| P6-T04 | Pass bounded context through retrieval and answering | Completed | 2026-05-27 | Added bounded session-context propagation into retrieval and answer-generation flows |
| P6-T05 | Add expiry or archival rules | Completed | 2026-05-27 | Added deterministic archive/expiry lifecycle transitions and tests |
| P6-T06 | Add multi-turn integration tests | Completed | 2026-05-27 | Added deterministic multi-turn integration coverage across answer/retrieval/session services |
| P6-T07 | Add transcript export/import | In progress | 2026-05-27 | Next active task |
| P6-T08 | Document session behavior and extension points | Not started | - | Pending |
