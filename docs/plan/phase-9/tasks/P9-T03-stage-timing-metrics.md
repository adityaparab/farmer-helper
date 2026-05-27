# P9-T03 - Add stage-level timing metrics

## Sub-issue description
### Objective
Add or extend timing telemetry for critical API stages to aid latency diagnosis.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added route-level duration timing metrics for answers and embeddings routes.
2. Kept existing retrieval/answer service timing metrics in place.
3. Standardized timing field naming and fixed precision for deterministic logs.
