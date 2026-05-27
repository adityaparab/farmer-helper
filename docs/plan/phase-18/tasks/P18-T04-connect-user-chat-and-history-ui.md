# P18-T04 - Connect user chat and history UI

## Sub-issue description
### Objective
Wire user chat submission and history surfaces to backend answer/session contracts with TanStack AI-ready boundaries.

### Acceptance criteria
- User questions are submitted through a typed backend answer/session client.
- Chat and history state distinguishes pending, answered, refused, and failed responses.
- Each conditionally rendered chat state is a separate component.
- The integration remains ready for TanStack AI streaming without coupling UI components to transport details.
- Vitest coverage exercises submit, history update, and failure states.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/188

## What was done
1. Connected user question submission to `POST /answers/generate` through the typed frontend API client.
2. Added authenticated answer requests with session-key context derived from the current user.
3. Mapped answer, clarification, and refusal decisions into displayable history entries.
4. Added pending and failure states to the chat composer with separate conditional components.
5. Kept question history as the user-facing transcript surface for successful backend responses.
6. Added Vitest coverage for successful answer generation and answer-service failure behavior.

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184
- `frontend/src/App.tsx`
- `frontend/src/components/ChatComposer.tsx`
- `frontend/src/components/UserWorkspace.tsx`
- `frontend/src/components/RoleView.tsx`
- `frontend/src/App.test.tsx`
- Validation: `npm run test` from `frontend/` passes.
- Validation: `npm run build` from `frontend/` passes.
- Validation: `npm run lint` from `frontend/` passes.
- Validation: `ruff check .` passes.