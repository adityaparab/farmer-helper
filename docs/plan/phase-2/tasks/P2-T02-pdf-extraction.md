# P2-T02 - Extract text from PDFs with deterministic error handling

## Sub-issue description
### Objective
Extract text from PDF inputs with deterministic error handling and stable output contracts for downstream normalization and chunking stages.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added deterministic extractor in `src/farmer_helper/services/ingestion/pdf_extractor.py`.
2. Added extraction output schemas in `src/farmer_helper/schemas/ingestion.py`.
3. Added tests in `tests/unit/test_pdf_extractor.py`.

## Decisions made
- Reuse file validator before extraction for deterministic preconditions.
- Emit stable extraction error codes for unreadable/encrypted and generic read failures.
