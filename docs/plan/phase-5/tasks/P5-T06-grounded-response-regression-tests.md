# P5-T06 - Add grounded-response regression tests

## Sub-issue description
### Objective
Add deterministic regression tests that validate grounding, citation presence, and policy behavior across representative answer-generation scenarios.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add table-driven regression scenarios for answer, clarify, and refuse outcomes.
2. Validate citation output shape and policy codes across scenarios.
3. Add focused integration coverage for `/answers/generate` grounding behavior.

## Decisions made
- Regression tests should avoid external dependencies and use deterministic provider behavior.
- Scenario fixtures should be easy to expand for future model/provider changes.
