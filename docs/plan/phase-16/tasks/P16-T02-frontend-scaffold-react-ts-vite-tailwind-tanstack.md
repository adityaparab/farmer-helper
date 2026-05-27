# P16-T02 - Scaffold frontend app with React TS Vite Tailwind TanStack

## Sub-issue description
### Objective
Establish the frontend codebase foundation for landing, admin, and user role experiences.

### Deliverables
1. Frontend project scaffold with React + TypeScript + Vite.
2. Tailwind CSS integration and visual theme baseline.
3. TanStack package installation baseline for query/router/AI integration.
4. Initial UX shell for landing, admin, and user views.
5. Modular component architecture with isolated conditionally rendered views.
6. Vitest unit test setup and component coverage for core role flows.

### Acceptance criteria
- Frontend builds successfully in CI-compatible mode.
- Landing, admin, and user shell views are implemented, fully responsive, elegant, professional, clear, and concise.
- Dependencies for TanStack AI integration are present.
- Code follows frontend engineering best practices: single responsibility, separation of concerns, readable component boundaries, reusable typed data contracts, and easy maintenance.
- Each conditionally rendered application view is implemented as a separate component rather than inline JSX blocks.
- Unit tests are written with Vitest and React Testing Library for landing/auth, admin shell, and user chat/history behavior.
- Frontend test, lint, and production build commands pass locally and are ready for CI integration.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Created frontend project scaffold under frontend/.
2. Installed runtime dependencies including TanStack AI and utility packages.
3. Added Tailwind Vite plugin and custom UI theme styles.
4. Replaced default Vite template with role-aware product shell (landing/admin/user).
5. Verified frontend production build succeeds.
6. Refactored the shell into typed, focused components for header, guest, landing, auth, admin dashboard, metrics, PDF upload, user workspace, chat composer, and question history.
7. Added Vitest + React Testing Library setup and behavior tests for guest, admin, user, and chat-history flows.
8. Verified frontend lint, unit tests, and production build pass.

## Additional frontend engineering requirements
- Treat responsive behavior as a first-class acceptance gate across mobile, tablet, and desktop.
- Prefer small, named components and typed props over large application-level JSX blocks.
- Keep presentation components decoupled from state orchestration where practical.
- Keep conditional rendering at the application composition layer and render separate view components for each condition.
- Use Vitest for unit tests and React Testing Library for behavior-focused component tests.
- Keep UI copy concise and functional; avoid in-app implementation descriptions once backend integrations replace placeholders.

## Evidence
- frontend/package.json
- frontend/vite.config.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/src/components/
- frontend/src/data/dashboard.ts
- frontend/src/types.ts
- frontend/src/test/setup.ts
- frontend/src/index.css

## Risks and follow-ups
- User chat currently uses placeholder answer generation and needs backend API binding.
- TanStack AI useChat wiring is pending in the next implementation slice.
