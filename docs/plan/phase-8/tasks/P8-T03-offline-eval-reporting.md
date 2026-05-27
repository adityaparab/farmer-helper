# P8-T03 - Build offline eval reporting

## Sub-issue description
### Objective
Produce deterministic offline evaluation reports from eval runner outputs with stable summary metrics and per-item breakdowns suitable for CI consumption.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define report schema and serialization format.
2. Implement report builder for runner outputs.
3. Add tests for deterministic ordering and metric totals.
4. Ensure compatibility with future CI integration step.

## Decisions made
- Reporting should consume typed runner outputs without re-scoring.
- Output should be deterministic and machine-readable.
