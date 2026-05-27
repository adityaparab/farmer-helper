# P6-T02 - Add follow-up context resolution

## Sub-issue description
### Objective
Resolve follow-up questions by retrieving bounded recent session context and normalizing it for retrieval and answering layers.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add service for bounded recent-message context resolution.
2. Define deterministic ordering and turn-window behavior.
3. Add unit tests for context-window and edge-case handling.

## Decisions made
- Follow-up context should be bounded by configurable turn/message limits.
- Context selection must remain deterministic for regression testing.
