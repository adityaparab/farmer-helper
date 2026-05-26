# P3-T07 - Add integration and smoke tests with coverage target

## Sub-issue description
### Objective
Expand embedding pipeline verification with integration and smoke-level tests covering end-to-end trigger behavior.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added integration test `tests/integration/test_embedding_trigger_integration.py`.
2. Added smoke tests `tests/smoke/test_embedding_trigger.py`.
3. Verified trigger-to-persistence flow and validation behavior.

## Decisions made
- Reuse deterministic mock provider paths for stable test outcomes.
- Prioritize end-to-end behavior checks over provider-specific internals.
