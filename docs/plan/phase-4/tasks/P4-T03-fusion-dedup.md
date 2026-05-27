# P4-T03 - Merge and deduplicate results with explicit fusion logic

## Sub-issue description
### Objective
Merge vector and keyword retrieval outputs into a single deterministic ranked list with explicit fusion and deduplication semantics.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added fused retrieval schemas in `src/farmer_helper/schemas/retrieval.py`.
2. Added explicit fusion and dedup service in `src/farmer_helper/services/retrieval/fusion_service.py`.
3. Added deterministic ordering and dedup tests in `tests/unit/test_retrieval_fusion_service.py`.

## Decisions made
- Fusion must preserve deterministic tie-break rules.
- Deduplication key should align with persisted chunk identity.
