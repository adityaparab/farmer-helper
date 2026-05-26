# P2-T04 - Chunk text with page-aware, configurable chunking

## Sub-issue description
### Objective
Chunk normalized extracted text into deterministic, page-aware segments with configurable sizing and overlap.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/services/ingestion/text_chunker.py`.
2. Added chunking schemas/config in `src/farmer_helper/schemas/ingestion.py`.
3. Added tests in `tests/unit/test_text_chunker.py`.

## Decisions made
- Keep chunking deterministic by character windows with configurable overlap.
- Preserve page provenance at chunk level for downstream citation mapping.
