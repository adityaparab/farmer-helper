# P12-T01 - Add admin API for ingestion and reindex workflows

## Sub-issue description
### Objective
Create admin endpoints to initialize ingestion/reindex workflows and manage job progression states.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `POST /admin/ingestion/jobs` for ingestion workflow starts.
2. Added `POST /admin/reindex/jobs` for reindex workflow starts.
3. Added `POST /admin/jobs/{job_id}/status` for controlled job status transitions.
