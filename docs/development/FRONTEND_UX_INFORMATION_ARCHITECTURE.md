# Frontend UX Information Architecture

## Scope
This document defines the first web interface structure for Farmer Helper. The IA is role-based, operational, and aligned to the current React component boundaries in `frontend/src`.

## Primary Views

### Public Landing and Auth
- Entry component path: `App` -> `RoleView` -> `GuestExperience`.
- User goal: understand the application purpose, authenticate, and enter the correct role view without extra navigation.
- Primary regions:
  - `LandingHero`: concise product framing and core capability signals.
  - `AuthPanel`: username/password entry and continuation action.
- Auth outcome:
  - `admin` username routes to the admin dashboard shell.
  - Any non-admin username routes to the user workspace shell.

### User Workspace
- Entry component path: `App` -> `RoleView` -> `UserWorkspace`.
- User goal: ask grounded agricultural questions and review recent question history in one work surface.
- Primary regions:
  - `ChatComposer`: current question input and submit action.
  - `QuestionHistory`: recent questions and answers.
- Future backend integration should connect this view to TanStack AI streaming, authenticated user identity, and persisted session history while keeping composer/history as separate components.

### Admin Dashboard
- Entry component path: `App` -> `RoleView` -> `AdminDashboard`.
- Admin goal: inspect operational state and upload source PDFs for ingestion.
- Primary regions:
  - `MetricGrid`: dashboard metrics and health counters.
  - `PdfUploadPanel`: PDF selection/upload workflow.
- Future backend integration should hydrate metrics from `GET /admin/dashboard/metrics` and upload PDFs through `POST /admin/documents/upload`.

## Responsive Behavior
- Mobile: stack all regions vertically with the most active workflow first after header/auth context.
- Tablet: preserve stacked reading order, increase spacing, and allow metric tiles to form compact grids.
- Desktop: use two-column operational layouts where comparison improves efficiency:
  - landing/auth: product framing beside auth panel
  - user workspace: composer beside history
  - admin dashboard: metrics before upload controls, with cards laid out for scanning
- All views keep the header stable at the top, avoid nested page cards, and keep action labels short.

## Navigation Model
- The first release uses role-gated conditional rendering rather than deep routes.
- `RoleView` owns conditional view selection; each rendered branch is a separate component.
- `AppHeader` owns sign-out and role context.
- Future TanStack Router adoption should preserve these route boundaries:
  - `/` public landing/auth
  - `/admin` admin dashboard
  - `/user/chat` chat workspace
  - `/user/history` history-focused view or split panel state

## Design Principles
- Keep the interface quiet, professional, and operational rather than promotional.
- Prefer dense but readable dashboard information for repeated admin use.
- Keep user chat focused on the current question, with history available without navigation friction.
- Keep admin upload controls close to ingestion metrics so source updates and system state are reviewed together.
- Preserve single-responsibility components so conditional surfaces remain testable with Vitest and React Testing Library.