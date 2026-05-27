# P12-T05 - Add access audit logs

## Sub-issue description
### Objective
Persist and surface admin access audit records to improve traceability and governance.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added access audit persistence model and migration.
2. Added automatic audit writes across admin mutations.
3. Added `GET /admin/access-audit` listing endpoint for operational review.
