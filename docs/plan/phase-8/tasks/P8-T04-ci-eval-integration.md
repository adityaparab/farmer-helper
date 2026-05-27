# P8-T04 - Integrate evals into CI

## Sub-issue description
### Objective
Integrate deterministic offline evaluation execution into CI so material quality regressions fail the pipeline.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add CI task wiring for eval dataset load, run, and report generation.
2. Define regression thresholds and failure conditions.
3. Ensure deterministic artifact generation for debugging.
4. Add tests/docs updates for CI behavior.

## Decisions made
- CI integration should consume existing typed loader/runner/reporting contracts.
- Failure criteria should be explicit and stable.
