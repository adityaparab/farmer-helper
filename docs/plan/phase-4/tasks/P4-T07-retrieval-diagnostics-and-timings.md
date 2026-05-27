# P4-T07 - Log retrieval diagnostics and timings

## Sub-issue description
### Objective
Add structured diagnostics and timing logs for retrieval pipeline stages to improve observability and debugging.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `RetrievalDiagnosticsLogger` in `src/farmer_helper/services/retrieval/diagnostics_logger.py`.
2. Added per-stage timing capture and structured diagnostics logging in `src/farmer_helper/services/retrieval/query_service.py`.
3. Added diagnostics log payload tests in `tests/unit/test_retrieval_diagnostics_logging.py`.

## Decisions made
- Logging should remain structured and avoid high-cardinality payload fields.
- Timing metrics for this step are API-facing diagnostics only, not external metrics backend integration.
