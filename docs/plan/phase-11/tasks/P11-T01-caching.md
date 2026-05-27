# P11-T01 - Add caching for retrieval and answers where appropriate

## Sub-issue description
### Objective
Reduce repeated computation for deterministic requests by caching route responses where safe.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added reusable in-memory TTL cache utility.
2. Added retrieval route caching for non-session requests.
3. Added answer route caching for non-session, non-idempotent requests.
4. Added cache hit/miss structured observability logs.
