# P3-T01 - Create embedding provider abstraction

## Sub-issue description
### Objective
Define an embedding provider interface and baseline implementation boundary for pluggable embedding backends.

## Implementation status
- Status: In progress
- Started: 2026-05-26
- Completed: -

## Next work
1. Define provider input/output contracts and error semantics.
2. Add provider abstraction module with clear extension points.
3. Add unit tests for contract behavior and edge cases.

## Decisions made
- Keep provider abstraction backend-agnostic to support future provider switching.
- Separate provider contract from orchestration logic for testability.
