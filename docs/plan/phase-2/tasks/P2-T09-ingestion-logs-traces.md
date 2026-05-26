# P2-T09 - Add ingestion logs and processing traces

## Sub-issue description
### Objective
Add structured ingestion logs and trace events so document processing can be observed and debugged reliably.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/services/ingestion/trace_logger.py` for structured ingestion lifecycle events.
2. Updated `src/farmer_helper/services/ingestion/status_service.py` to emit started/processing/succeeded/failed trace events.
3. Added `tests/unit/test_ingestion_trace_logging.py` to validate event names and correlation/error fields.

## Decisions made
- Reused existing structured logging infrastructure and request context propagation.
- Standardized deterministic event names for downstream filtering and alerting.
