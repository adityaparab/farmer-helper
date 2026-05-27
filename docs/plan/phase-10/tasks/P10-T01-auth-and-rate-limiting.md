# P10-T01 - Add auth and rate limiting

## Sub-issue description
### Objective
Require API authentication for protected routes and enforce rate limiting to reduce abuse risk.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added API key enforcement for non-health routes via request security guard.
2. Added in-memory per-principal rate limiting with configurable window/limit.
3. Added deterministic 401/429 error contracts and `Retry-After` support.
