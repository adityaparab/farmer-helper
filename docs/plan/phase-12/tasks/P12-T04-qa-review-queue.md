# P12-T04 - Add QA/corpus review queue

## Sub-issue description
### Objective
Create structured queue workflows for corpus and QA review operations.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added QA review queue persistence model and migration.
2. Added `POST /admin/review-queue` create flow.
3. Added `POST /admin/review-queue/{item_id}` update flow.
4. Added `GET /admin/review-queue` listing endpoint.
