# P2-T03 - Normalize and clean extracted text

## Sub-issue description
### Objective
Normalize raw extracted text into consistent clean text suitable for chunking and metadata enrichment.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/services/ingestion/text_normalizer.py`.
2. Added normalization config schema in `src/farmer_helper/schemas/ingestion.py`.
3. Added tests in `tests/unit/test_text_normalizer.py`.

## Decisions made
- Keep normalization deterministic and config-driven.
- Preserve page boundaries and page numbering while normalizing text payloads.
