# P7-T01 - Add timeout and retry policies to external calls

## Sub-issue description
### Objective
Apply explicit, deterministic timeout and retry controls at external provider boundaries for embedding and answer generation workflows.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added external call policy settings for timeout and retry attempts in `src/farmer_helper/core/config.py`.
2. Added timeout wrapper providers:
   - `src/farmer_helper/services/embedding/timeout_provider.py`
   - `src/farmer_helper/services/answering/timeout_provider.py`
3. Added LLM retry wrapper provider:
   - `src/farmer_helper/services/answering/retrying_provider.py`
4. Wired timeout and retry policies into:
   - `src/farmer_helper/api/routes/embeddings.py`
   - `src/farmer_helper/api/routes/answers.py`
5. Added deterministic unit tests for new timeout/retry behavior.

## Decisions made
- Timeouts are surfaced as retryable provider errors to preserve deterministic fallback handling in upper layers.
- Retries only re-attempt retryable provider failures and fail fast on non-retryable errors.
- Policy values remain configuration-driven via settings fields.
