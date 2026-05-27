# Epic: Phase 18 - Frontend backend integration and authenticated workflows

## Summary
Connect the React/Vite frontend to FastAPI auth, admin, upload, answer, and session APIs with typed client boundaries, role-aware runtime state, and test coverage.

## Scope
This phase turns the Phase 16 frontend scaffold into an authenticated application shell that talks to the backend contracts delivered across Phases 5, 6, 16, and 17.

## Epic status
- Status: In Progress
- Started on: 2026-05-27
- Remote GitHub Epic: https://github.com/adityaparab/farmer-helper/issues/184
- Local/remote sync: Synced on 2026-05-27

## Sub-issues
| ID | Title | Status | Remote issue | Last updated | Notes |
|---|---|---|---|---|---|
| P18-T01 | Implement frontend API client foundation | Completed | https://github.com/adityaparab/farmer-helper/issues/185 | 2026-05-27 | Typed request helpers, API errors, token plumbing delivered |
| P18-T02 | Connect auth session and role routing | Completed | https://github.com/adityaparab/farmer-helper/issues/186 | 2026-05-27 | Backend login/me/logout now drives frontend role state |
| P18-T03 | Connect admin metrics and PDF upload UI | Not Started | https://github.com/adityaparab/farmer-helper/issues/187 | 2026-05-27 | Metrics query and multipart upload integration |
| P18-T04 | Connect user chat and history UI | Not Started | https://github.com/adityaparab/farmer-helper/issues/188 | 2026-05-27 | Answer/session API integration with TanStack AI-ready boundaries |
| P18-T05 | Validate frontend integration workflows | Not Started | https://github.com/adityaparab/farmer-helper/issues/192 | 2026-05-27 | Vitest/build and backend compatibility validation |

## Exit criteria
- Frontend role state comes from backend auth, not mock username branching.
- Admin dashboard fetches backend metrics and uploads PDFs through backend RBAC endpoints.
- User chat flow calls backend answer/session contracts behind typed client helpers.
- Frontend tests cover authenticated role behavior, admin integration, user workflow, and failure states.
- Backend and frontend validation pass before phase completion.