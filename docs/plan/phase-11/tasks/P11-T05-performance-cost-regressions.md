# P11-T05 - Add performance and cost regression tests

## Sub-issue description
### Objective
Lock in efficiency behavior through deterministic regression tests.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added answer cache test ensuring repeated requests avoid extra generation calls.
2. Added retrieval cache test ensuring repeated requests avoid extra retrieval calls.
3. Added model router test to verify cheap/high-quality model selection.
4. Added async embedding job route/status coverage and context-trim regression tests.
