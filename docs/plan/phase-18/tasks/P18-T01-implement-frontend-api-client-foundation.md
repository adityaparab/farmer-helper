# P18-T01 - Implement frontend API client foundation

## Sub-issue description
### Objective
Create typed frontend API helpers for auth, admin metrics, upload, answers, errors, and token handling.

### Acceptance criteria
- API base URL and request helpers are centralized.
- Backend error responses are normalized for UI consumption.
- Auth token plumbing supports authenticated JSON and multipart requests.
- Response types align with existing backend contracts.
- Unit tests cover success and failure behavior for the client boundary.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/185

## What was done
1. Added a typed frontend API client in `frontend/src/api/client.ts`.
2. Added auth helpers for login, register, me, refresh, and logout.
3. Added admin helpers for dashboard metrics and multipart PDF upload.
4. Added answer generation helper aligned to the backend answer contract.
5. Added normalized `ApiError` handling for backend error payloads.
6. Added support for bearer access tokens and optional API-key headers.
7. Added Vitest coverage for JSON requests, authenticated headers, multipart uploads, and error normalization.

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184
- `frontend/src/api/client.ts`
- `frontend/src/api/client.test.ts`
- Validation: `npm run test` from `frontend/` passes.
- Validation: `npm run build` from `frontend/` passes.
- Validation: `npm run lint` from `frontend/` passes.
- Validation: `ruff check .` passes.