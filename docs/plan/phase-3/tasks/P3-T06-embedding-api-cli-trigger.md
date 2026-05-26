# P3-T06 - Add API/CLI trigger for embeddings

## Sub-issue description
### Objective
Expose embedding pipeline execution through API and CLI entrypoints for controlled operational triggering.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added embedding trigger route in `src/farmer_helper/api/routes/embeddings.py`.
2. Wired route into app startup in `src/farmer_helper/main.py`.
3. Added CLI trigger script `scripts/trigger-embeddings.py`.
4. Added route tests in `tests/unit/test_embedding_trigger_route.py`.

## Decisions made
- Keep trigger surface minimal and typed.
- Reuse shared orchestration services for API and CLI paths.
