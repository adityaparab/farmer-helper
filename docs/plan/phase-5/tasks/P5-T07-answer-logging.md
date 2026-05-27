# P5-T07 - Add usage, latency, and confidence logging

## Sub-issue description
### Objective
Add structured answer-generation diagnostics that capture latency, token usage, decision paths, and confidence metadata.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added structured diagnostics logger in `src/farmer_helper/services/answering/diagnostics_logger.py`.
2. Added latency, usage, and confidence logging in `src/farmer_helper/services/answering/generation_service.py`.
3. Added deterministic diagnostics tests in `tests/unit/test_answer_diagnostics_logging.py`.

## Decisions made
- Diagnostics fields should be stable and low-cardinality.
- Logging should include decision paths for answer, clarify, and refuse outcomes.
