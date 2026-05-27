# P11-T04 - Move heavy work off request path asynchronously

## Sub-issue description
### Objective
Reduce synchronous request latency by moving heavy embedding orchestration to background execution.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `POST /embeddings/trigger-async` queued execution endpoint.
2. Added async embedding job status endpoint `GET /embeddings/jobs/{job_id}`.
3. Added in-memory job tracking store for queued/running/completed/failed states.
4. Added async route regression tests.
