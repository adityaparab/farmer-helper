# P8-T03 - Build offline eval reporting

## Sub-issue description
### Objective
Produce deterministic offline evaluation reports from eval runner outputs with stable summary metrics and per-item breakdowns suitable for CI consumption.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added typed offline report schemas in `src/farmer_helper/schemas/evaluation.py`.
2. Added deterministic report builder in `src/farmer_helper/services/evaluation/reporting.py`.
3. Added unit tests for deterministic timestamps, metric consistency, and stable JSON serialization.
4. Kept report contract machine-readable for CI integration in the next step.

## Decisions made
- Reporting should consume typed runner outputs without re-scoring.
- Output should be deterministic and machine-readable.
