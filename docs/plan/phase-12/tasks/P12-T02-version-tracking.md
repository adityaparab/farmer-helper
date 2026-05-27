# P12-T02 - Add versioned content/model/pipeline tracking

## Sub-issue description
### Objective
Track operationally relevant content/model/pipeline version records for maintainability and rollback context.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added version tracking persistence model and migration.
2. Added `POST /admin/versions` to register new version records.
3. Added `GET /admin/versions` to list recent records.
