# P2-T01 - Validate input files before ingestion

## Sub-issue description
### Objective
Validate candidate input files before ingestion to prevent non-deterministic processing failures and to return actionable validation errors.

### Deliverables
1. Deterministic file validation service.
2. Stable validation error codes.
3. Unit tests covering success and failure paths.

### Acceptance criteria
- Missing, invalid-type, unsupported-extension, empty, and oversize files are rejected with explicit codes.
- Validation success returns normalized metadata required by downstream ingestion stages.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `src/farmer_helper/services/ingestion/file_validator.py`.
2. Added ingestion file schema `src/farmer_helper/schemas/ingestion.py`.
3. Added tests in `tests/unit/test_file_validator.py`.

## Decisions made
- Use explicit error codes rather than free-form messages for deterministic handling.
- Limit accepted extensions to configurable allowlist (default PDF only).
