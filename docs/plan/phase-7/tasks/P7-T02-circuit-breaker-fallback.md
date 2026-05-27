# P7-T02 - Add circuit breaker and fallback strategy

## Sub-issue description
### Objective
Add deterministic circuit-breaker controls and fallback strategy around external provider usage to prevent cascading failure under repeated provider outages.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add circuit-breaker state model with deterministic transitions.
2. Integrate breaker checks into provider wrappers and route-level builders.
3. Implement bounded fallback behavior when breaker is open.
4. Add unit tests for closed/open/half-open transitions.

## Decisions made
- Circuit-breaker behavior should compose with existing timeout and retry wrappers.
- Fallback behavior must be explicit and observable.
