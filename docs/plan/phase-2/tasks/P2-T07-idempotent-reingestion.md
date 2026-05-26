# P2-T07 - Enforce idempotent re-ingestion behavior

## Sub-issue description
### Objective
Ensure repeated ingestion of the same document content does not duplicate downstream artifacts.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/repositories/document_repository.py`.
2. Added `src/farmer_helper/services/ingestion/idempotency_service.py`.
3. Added tests in `tests/unit/test_idempotency_service.py`.

## Decisions made
- Idempotency key is `content_hash + version`.
- Re-ingestion with same key reuses existing document record and avoids duplication.
