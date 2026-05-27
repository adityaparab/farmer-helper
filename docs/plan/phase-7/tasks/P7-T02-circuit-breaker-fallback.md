# P7-T02 - Add circuit breaker and fallback strategy

## Sub-issue description
### Objective
Add deterministic circuit-breaker controls and fallback strategy around external provider usage to prevent cascading failure under repeated provider outages.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added circuit-breaker wrappers for embedding and LLM provider boundaries.
2. Added deterministic state transitions (closed/open/half-open) with configurable thresholds and recovery windows.
3. Added optional fallback-provider strategy for open-circuit behavior.
4. Wired circuit-breaker wrappers into embeddings and answers route-level provider construction.
5. Added deterministic unit tests for opening behavior, half-open recovery, and no-fallback open-circuit errors.

## Decisions made
- Circuit-breaker behavior should compose with existing timeout and retry wrappers.
- Fallback behavior must be explicit and observable.
