# P7-T06 - Add failure injection tests

## Sub-issue description
### Objective
Add deterministic failure-injection coverage to verify resilience behavior under provider outages, timeouts, and degradation/fallback scenarios.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added deterministic failure-injection route tests for degraded answer-generation behavior.
2. Added deterministic failure-injection route tests for degraded embedding-trigger behavior.
3. Added idempotent replay tests for degraded responses in both routes.
4. Asserted normalized reliability fields in injected failure outcomes.

## Decisions made
- Failure injection tests should focus on deterministic service doubles and route-level behavior.
- Reliability contract fields should be asserted in all injected failure outcomes.
