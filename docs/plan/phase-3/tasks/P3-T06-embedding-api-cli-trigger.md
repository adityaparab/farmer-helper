# P3-T06 - Add API/CLI trigger for embeddings

## Sub-issue description
### Objective
Expose embedding pipeline execution through API and CLI entrypoints for controlled operational triggering.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add API route handler for embedding trigger requests.
2. Add service wiring from trigger endpoint to embedding orchestration.
3. Add CLI script for local/manual execution of embedding trigger.

## Decisions made
- Keep trigger surface minimal and typed.
- Reuse shared orchestration services for API and CLI paths.
