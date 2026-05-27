# P12-T03 - Add gold-answer/editor workflow

## Sub-issue description
### Objective
Support editable gold-answer records for curated answer quality workflows.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added gold-answer persistence model and migration.
2. Added `POST /admin/gold-answers` create flow.
3. Added `POST /admin/gold-answers/{answer_id}` update flow with status/editor attribution.
4. Added `GET /admin/gold-answers` listing endpoint.
