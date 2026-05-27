# P16-T07 - Define UX information architecture for landing admin user views

## Sub-issue description
### Objective
Define clear, responsive, professional information architecture for public, admin, and user-facing application views.

### Acceptance criteria
- Landing, auth, user chat/history, and admin dashboard flows are specified.
- Responsive behavior is defined for mobile, tablet, and desktop.
- UI remains concise, operational, and domain-appropriate.

## Implementation status
- Status: Completed
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/176

## IA summary
- Public flow: landing/auth enters role-specific workspace from the first screen.
- Admin flow: dashboard metrics and PDF upload controls are grouped as the first admin work surface.
- User flow: chat composer and history are visible in one responsive workspace.
- Conditional rendering remains centralized in `RoleView`, and each conditional branch renders a separate component.
- Responsive behavior is mobile-first stacked layout, tablet grid refinement, and desktop two-column operational layouts where useful.

## Evidence
- Tracked remotely under Phase 16 Epic: https://github.com/adityaparab/farmer-helper/issues/168
- UX IA documented in `docs/development/FRONTEND_UX_INFORMATION_ARCHITECTURE.md`.
- Current component mapping verified against `frontend/src/App.tsx`, `frontend/src/components/RoleView.tsx`, `frontend/src/components/GuestExperience.tsx`, `frontend/src/components/UserWorkspace.tsx`, and `frontend/src/components/AdminDashboard.tsx`.
- Existing Vitest coverage validates guest, admin, and user view selection in `frontend/src/App.test.tsx`.
