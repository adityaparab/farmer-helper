# P4-T04 - Add pluggable reranker interface

## Sub-issue description
### Objective
Add a provider-agnostic reranker contract and default no-op implementation that can be composed after retrieval fusion.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added reranker schema contracts in `src/farmer_helper/schemas/retrieval.py`.
2. Added pluggable reranker interface and baseline implementations in `src/farmer_helper/services/retrieval/reranker.py`.
3. Added unit tests in `tests/unit/test_reranker.py`.

## Decisions made
- Reranker must be optional and configuration-driven.
- Baseline implementation should preserve deterministic ordering when disabled.
