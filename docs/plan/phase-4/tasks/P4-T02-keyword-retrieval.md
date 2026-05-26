# P4-T02 - Implement keyword retrieval

## Sub-issue description
### Objective
Implement deterministic keyword retrieval over chunk text signals to complement vector retrieval.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add keyword retrieval request/response schema contracts.
2. Implement keyword scoring and ranking service.
3. Add unit tests for ranking and tie-break determinism.

## Decisions made
- Keep keyword retrieval implementation deterministic and dependency-light.
- Align keyword result contract with vector retrieval structure for fusion compatibility.
