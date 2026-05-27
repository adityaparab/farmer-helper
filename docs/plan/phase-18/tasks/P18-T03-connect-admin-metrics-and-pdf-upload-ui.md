# P18-T03 - Connect admin metrics and PDF upload UI

## Sub-issue description
### Objective
Hydrate admin dashboard metrics from backend APIs and post admin PDF uploads through the multipart API.

### Acceptance criteria
- Admin metrics use `GET /admin/dashboard/metrics`.
- PDF upload uses `POST /admin/documents/upload` with multipart form data.
- Loading, success, duplicate, validation-error, and authorization-error states are represented by separate components.
- UI remains responsive and concise on mobile, tablet, and desktop.
- Vitest coverage exercises metrics rendering and upload outcomes.

## Implementation status
- Status: Not Started
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/187

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184