# P6-T06 - Add multi-turn integration tests

## Sub-issue description
### Objective
Validate end-to-end multi-turn behavior including session context resolution, summarization triggers, and bounded context propagation.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add integration test flows across multiple session turns.
2. Validate bounded context and policy outputs in multi-turn scenarios.
3. Add deterministic assertions for session lifecycle interactions.

## Decisions made
- Integration tests should be deterministic and use local mock providers.
- Multi-turn scenarios should cover both normal and edge-case conversation paths.
