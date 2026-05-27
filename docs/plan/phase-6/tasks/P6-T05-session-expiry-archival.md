# P6-T05 - Add expiry or archival rules

## Sub-issue description
### Objective
Introduce deterministic session lifecycle rules for expiring or archiving stale sessions and preserving traceability.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add session status transition rules for archival and expiry.
2. Add repository/service methods to mark sessions archived or expired by policy.
3. Add unit tests for lifecycle transition behavior.

## Decisions made
- Lifecycle rules should be deterministic and auditable.
- Existing active-session flows must remain backward compatible.
