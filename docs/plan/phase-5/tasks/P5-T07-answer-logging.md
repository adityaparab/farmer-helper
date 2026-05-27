# P5-T07 - Add usage, latency, and confidence logging

## Sub-issue description
### Objective
Add structured answer-generation diagnostics that capture latency, token usage, decision paths, and confidence metadata.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add structured diagnostics logger for answer-generation outcomes.
2. Capture generation latency and token usage metadata in service flow.
3. Add tests for deterministic diagnostics payload fields.

## Decisions made
- Diagnostics fields should be stable and low-cardinality.
- Logging should include decision paths for answer, clarify, and refuse outcomes.
