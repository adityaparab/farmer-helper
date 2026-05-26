# Epic: Phase 2 - Document ingestion pipeline

## Summary
Build a reliable, idempotent, and testable ingestion pipeline for source documents.

## Scope
This Epic maps to Phase 2 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: Completed
- Started on: 2026-05-26
- Completed on: 2026-05-26

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P2-T01 | Validate input files before ingestion | Completed | 2026-05-26 | File validator implemented with deterministic error codes and tests |
| P2-T02 | Extract text from PDFs with deterministic error handling | Completed | 2026-05-26 | PDF extractor implemented with deterministic error codes and tests |
| P2-T03 | Normalize and clean extracted text | Completed | 2026-05-26 | Deterministic text normalizer implemented with tests |
| P2-T04 | Chunk text with page-aware, configurable chunking | Completed | 2026-05-26 | Page-aware chunker implemented with configurable size and overlap |
| P2-T05 | Attach metadata including page ranges and content hash | Completed | 2026-05-26 | Metadata enricher implemented with content hash and versioning |
| P2-T06 | Persist ingestion status and error state | Completed | 2026-05-26 | Status persistence repository/service with transition tests implemented |
| P2-T07 | Enforce idempotent re-ingestion behavior | Completed | 2026-05-26 | Content hash/version idempotency guard implemented with tests |
| P2-T08 | Add unit, integration, and failure-path tests | Completed | 2026-05-26 | Added integration/failure-path tests for idempotency + status collaboration |
| P2-T09 | Add ingestion logs and processing traces | Completed | 2026-05-26 | Added structured ingestion lifecycle trace logging with correlation fields + tests |
| P2-T10 | Document ingestion flow and operational guidance | Completed | 2026-05-26 | Added ingestion flow/operations guide and README references |
