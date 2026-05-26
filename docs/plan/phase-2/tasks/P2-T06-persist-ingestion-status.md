# P2-T06 - Persist ingestion status and error state

## Sub-issue description
### Objective
Persist ingestion pipeline execution status and error state transitions with deterministic status semantics.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/repositories/ingestion_job_repository.py`.
2. Added `src/farmer_helper/services/ingestion/status_service.py`.
3. Added transition tests in `tests/unit/test_ingestion_status_service.py`.

## Decisions made
- Use explicit state transitions: `pending -> processing -> succeeded` and `{pending|processing} -> failed`.
- Persist error code and message on failed terminal state.
