# Epic: Phase 16 - Web interface, auth RBAC, and production integration program

## Summary
Deliver a production-ready web experience for Farmer Helper using React + TypeScript + Vite + Tailwind + TanStack AI, with backend-enforced RBAC, admin operations UI, user chat/history UX, and FastAPI static asset serving.

## Scope
This Epic extends the roadmap after Phase 15 and establishes the execution baseline for frontend and auth/RBAC delivery.

## Epic status
- Status: In Progress
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P16-T01 | Save implementation plan and bootstrap tracking | Completed | 2026-05-27 | Program plan documented and phase structure created |
| P16-T02 | Scaffold modular frontend with React TS Vite Tailwind TanStack and Vitest | Completed | 2026-05-27 | Responsive, professional, componentized frontend foundation with Vitest coverage delivered |
| P16-T03 | Serve SPA index and assets from backend startup path | In Progress | 2026-05-27 | Backend entrypoint integration in progress |
| P16-T04 | Define auth and RBAC schema changes and migration plan | Not Started | 2026-05-27 | Pending migration authoring |
| P16-T05 | Define admin dashboard metrics contracts | Not Started | 2026-05-27 | Based on existing DB entities |
| P16-T06 | Define admin PDF upload architecture and controls | Not Started | 2026-05-27 | Validation, audit, ingestion integration |
| P16-T07 | Define UX information architecture for landing/admin/user views | Not Started | 2026-05-27 | Professional UI quality criteria |
| P16-T08 | Define local and remote Epic/issue synchronization workflow | Not Started | 2026-05-27 | gh CLI + status comment template |

## Frontend implementation standards
- The web application must be fully responsive across mobile, tablet, and desktop viewports.
- The UI must be elegant, professional, beautiful, clear, and concise while remaining domain-appropriate for an operational AI tool.
- Frontend code must be modular, fully testable, easy to read, easy to maintain, and easy to update.
- Each conditionally rendered node or view must be represented by a separate component.
- Components must follow single responsibility, separation of concerns, typed props, and clear ownership boundaries.
- Unit tests must be written with Vitest and React Testing Library for interactive and role-based behavior.
