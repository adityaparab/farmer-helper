# P13-T02 - Move background jobs to worker queue

## Sub-issue description
### Objective
Harden async embedding execution by introducing queue-capacity protection and durable job-status persistence.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added persistent `embedding_async_jobs` data model and repository.
2. Swapped async job state from in-memory map to DB-backed store.
3. Added queue-capacity guard for async trigger endpoint with deterministic `503` response.
4. Added route test coverage for queue-capacity rejection.
