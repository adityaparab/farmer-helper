# P7-T06 - Add failure injection tests

## Sub-issue description
### Objective
Add deterministic failure-injection coverage to verify resilience behavior under provider outages, timeouts, and degradation/fallback scenarios.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add failure-injection tests across timeout, retry, circuit-breaker, and degraded route paths.
2. Cover idempotency replay/conflict behavior under failure conditions.
3. Ensure tests assert stable reliability fields and contracts.
4. Keep scenarios deterministic and non-flaky.

## Decisions made
- Failure injection tests should focus on deterministic service doubles and route-level behavior.
- Reliability contract fields should be asserted in all injected failure outcomes.
