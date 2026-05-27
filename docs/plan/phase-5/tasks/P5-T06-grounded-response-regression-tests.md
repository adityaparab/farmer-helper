# P5-T06 - Add grounded-response regression tests

## Sub-issue description
### Objective
Add deterministic regression tests that validate grounding, citation presence, and policy behavior across representative answer-generation scenarios.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added table-driven integration regression scenarios in `tests/integration/test_answer_generation_regression.py`.
2. Validated answer, clarify, and refuse decisions with deterministic policy code expectations.
3. Added citation shape assertions for grounded answer responses.

## Decisions made
- Regression tests should avoid external dependencies and use deterministic provider behavior.
- Scenario fixtures should be easy to expand for future model/provider changes.
