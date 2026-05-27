# P14-T02 - Standardize error contracts

## Sub-issue description
### Objective
Use consistent machine-readable error payloads across API routes for future accessible and automated clients.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Applied structured error payload contract to retrieval errors.
2. Applied structured error payload contract to health readiness failures.
3. Applied structured error payload contract to embedding async queue and lookup errors.
4. Updated route tests to assert error contract shape and codes.
