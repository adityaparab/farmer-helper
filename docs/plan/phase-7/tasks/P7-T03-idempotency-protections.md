# P7-T03 - Add idempotency protections

## Sub-issue description
### Objective
Introduce deterministic idempotency protections for reliability-sensitive operations to prevent duplicate side effects under retries and transient failures.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added deterministic in-memory idempotency store and request hashing utility in `src/farmer_helper/services/reliability/idempotency.py`.
2. Added optional `idempotency_key` request fields to answer-generation and embedding-trigger schemas.
3. Added route-level idempotency replay behavior for matching requests.
4. Added route-level idempotency conflict handling (`409`) for key reuse with different payloads.
5. Added unit tests for idempotency store behavior and route replay/conflict scenarios.

## Decisions made
- Idempotency behavior must be deterministic and explicit across retries.
- Error and replay semantics should preserve current API contracts.
