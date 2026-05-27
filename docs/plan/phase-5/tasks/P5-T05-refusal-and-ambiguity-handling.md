# P5-T05 - Add refusal and ambiguity handling

## Sub-issue description
### Objective
Harden answer-generation behavior for unsafe or ambiguous requests with explicit, user-facing refusal and clarification handling.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define stable refusal and clarification response payload semantics.
2. Improve policy coverage for harmful and ambiguous query patterns.
3. Add regression unit tests for refusal and clarification outcomes at service and route levels.

## Decisions made
- Decision outputs must remain deterministic for testability.
- Policy handling should not invoke LLM provider when refusal or clarification is selected.
