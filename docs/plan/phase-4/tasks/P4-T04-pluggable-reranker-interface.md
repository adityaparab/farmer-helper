# P4-T04 - Add pluggable reranker interface

## Sub-issue description
### Objective
Add a provider-agnostic reranker contract and default no-op implementation that can be composed after retrieval fusion.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define reranker request/response schema contracts.
2. Add pluggable reranker interface and baseline implementation.
3. Add unit tests for reranker contract behavior.

## Decisions made
- Reranker must be optional and configuration-driven.
- Baseline implementation should preserve deterministic ordering when disabled.
