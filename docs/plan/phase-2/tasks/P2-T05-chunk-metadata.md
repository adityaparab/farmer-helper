# P2-T05 - Attach metadata such as page ranges, headings, version, and content hash

## Sub-issue description
### Objective
Attach deterministic metadata to each chunk, including provenance, heading context, versioning, and content hash identifiers.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added metadata schemas in `src/farmer_helper/schemas/ingestion.py`.
2. Added `src/farmer_helper/services/ingestion/chunk_metadata_enricher.py`.
3. Added tests in `tests/unit/test_chunk_metadata_enricher.py`.

## Decisions made
- Use SHA-256 hash of chunk text as deterministic content hash.
- Include version and heading context in metadata for downstream traceability.
