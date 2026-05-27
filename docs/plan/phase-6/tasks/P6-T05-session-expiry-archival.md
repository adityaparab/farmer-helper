# P6-T05 - Add expiry or archival rules

## Sub-issue description
### Objective
Introduce deterministic session lifecycle rules for expiring or archiving stale sessions and preserving traceability.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added repository lifecycle methods in `src/farmer_helper/repositories/chat_session_repository.py`.
2. Added lifecycle service in `src/farmer_helper/services/session/lifecycle_service.py`.
3. Added lifecycle tests in `tests/unit/test_chat_session_repository.py` and `tests/unit/test_session_lifecycle_service.py`.

## Decisions made
- Lifecycle rules should be deterministic and auditable.
- Existing active-session flows must remain backward compatible.
