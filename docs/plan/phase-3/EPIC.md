# Epic: Phase 3 - Embedding pipeline and pgvector integration

## Summary
Provide cloud-API embeddings for all chunks and store vectors in pgvector.

## Scope
This Epic maps to Phase 3 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-26

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P3-T01 | Create embedding provider abstraction | Completed | 2026-05-27 | Added typed contracts, provider interface, and unit tests |
| P3-T02 | Add batch embedding logic | Completed | 2026-05-27 | Added deterministic batching service with ordering and response validation tests |
| P3-T03 | Extend schema for vector persistence/upsert | Completed | 2026-05-27 | Added chunk embedding model, migration, and upsert repository with tests |
| P3-T04 | Add retry and error handling for embedding jobs | Completed | 2026-05-27 | Added retry policy/provider wrapper with retryable/non-retryable tests |
| P3-T05 | Add async-safe job orchestration | In progress | 2026-05-27 | Next active task |
| P3-T06 | Add API/CLI trigger for embeddings | Not started | - | Pending |
| P3-T07 | Add integration and smoke tests with coverage target | Not started | - | Pending |
| P3-T08 | Document provider versioning and extension path | Not started | - | Pending |
