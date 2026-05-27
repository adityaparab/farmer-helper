# P10-T05 - Add security audit logging

## Sub-issue description
### Objective
Emit structured, low-cardinality security audit events for abuse and policy enforcement outcomes.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `security.audit` events for auth rejection and rate limiting.
2. Added `security.audit` event for prompt-injection refusal path.
3. Added tests asserting emitted security audit fields.
