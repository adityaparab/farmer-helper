# P4-T02 - Implement keyword retrieval

## Sub-issue description
### Objective
Implement deterministic keyword retrieval over chunk text signals to complement vector retrieval.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added keyword retrieval schema contracts in `src/farmer_helper/schemas/retrieval.py`.
2. Added keyword retrieval service in `src/farmer_helper/services/retrieval/keyword_retrieval_service.py`.
3. Added unit tests in `tests/unit/test_keyword_retrieval_service.py`.
4. Extended embedding persistence to store `chunk_text` for keyword scoring.

## Decisions made
- Keep keyword retrieval implementation deterministic and dependency-light.
- Align keyword result contract with vector retrieval structure for fusion compatibility.
