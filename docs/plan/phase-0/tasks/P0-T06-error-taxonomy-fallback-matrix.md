# P0-T06 - Define error taxonomy and fallback matrix

## Sub-issue description
### Objective
Define a stable error taxonomy and deterministic fallback matrix that standardizes internal handling and user-facing behavior.

### Deliverables
1. Error taxonomy by category and error codes.
2. User-facing error contract.
3. Fallback matrix for critical workflow failure points.

### Acceptance criteria
- Error categories and codes are explicit.
- Fallback behavior is deterministic and observable.
- User-facing error contract is standardized.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `docs/standards/ERROR_TAXONOMY_AND_FALLBACK_MATRIX.md`.
2. Defined error categories A-D and code examples.
3. Added fallback matrix with response and observability expectations.

## Decisions made
- No silent fallbacks are allowed.
- Retry/fallback behavior is keyed by error code and operation type.

## Evidence
- Deliverable file present at `docs/standards/ERROR_TAXONOMY_AND_FALLBACK_MATRIX.md`.
- Epic tracker updated at `docs/plan/phase-0/EPIC.md`.