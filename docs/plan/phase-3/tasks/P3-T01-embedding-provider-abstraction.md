# P3-T01 - Create embedding provider abstraction

## Sub-issue description
### Objective
Define an embedding provider interface and baseline implementation boundary for pluggable embedding backends.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-27

## What was done
1. Added typed embedding contracts in `src/farmer_helper/schemas/embedding.py`.
2. Added provider abstraction and provider error semantics in `src/farmer_helper/services/embedding/provider.py`.
3. Added contract and edge-case tests in `tests/unit/test_embedding_provider_abstraction.py`.

## Decisions made
- Keep provider abstraction backend-agnostic to support future provider switching.
- Separate provider contract from orchestration logic for testability.
