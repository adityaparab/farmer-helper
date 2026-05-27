# P6-T02 - Add follow-up context resolution

## Sub-issue description
### Objective
Resolve follow-up questions by retrieving bounded recent session context and normalizing it for retrieval and answering layers.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `FollowUpContextRequest`/`FollowUpContextResponse` contracts in `src/farmer_helper/schemas/session.py`.
2. Added `FollowUpContextResolver` in `src/farmer_helper/services/session/context_resolver.py`.
3. Implemented bounded context selection by turn window and message limit.
4. Added deterministic unit tests in `tests/unit/test_follow_up_context_resolver.py`.

## Decisions made
- Follow-up context should be bounded by configurable turn/message limits.
- Context selection must remain deterministic for regression testing.
