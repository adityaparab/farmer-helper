# Epic: Phase 2 - Document ingestion pipeline

## Summary
Build a reliable, idempotent, and testable ingestion pipeline for source documents.

## Scope
This Epic maps to Phase 2 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: In progress
- Started on: 2026-05-26

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P2-T01 | Validate input files before ingestion | Completed | 2026-05-26 | File validator implemented with deterministic error codes and tests |
| P2-T02 | Extract text from PDFs with deterministic error handling | Completed | 2026-05-26 | PDF extractor implemented with deterministic error codes and tests |
| P2-T03 | Normalize and clean extracted text | Completed | 2026-05-26 | Deterministic text normalizer implemented with tests |
| P2-T04 | Chunk text with page-aware, configurable chunking | Completed | 2026-05-26 | Page-aware chunker implemented with configurable size and overlap |
| P2-T05 | Attach metadata including page ranges and content hash | Completed | 2026-05-26 | Metadata enricher implemented with content hash and versioning |
| P2-T06 | Persist ingestion status and error state | In progress | 2026-05-26 | Next active task |
| P2-T07 | Enforce idempotent re-ingestion behavior | Not started | - | Pending |
| P2-T08 | Add unit, integration, and failure-path tests | Not started | - | Pending |
| P2-T09 | Add ingestion logs and processing traces | Not started | - | Pending |
| P2-T10 | Document ingestion flow and operational guidance | Not started | - | Pending |
