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
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/187

## What was done
1. Connected the admin dashboard to `GET /admin/dashboard/metrics` through the typed frontend API client.
2. Replaced static metric cards with backend metric cards and formatted numeric values.
3. Added separated loading and error views for admin metrics.
4. Connected the PDF upload panel to `POST /admin/documents/upload` with multipart form data.
5. Added content-version input, file selection, upload progress, success, and error states.
6. Refreshes admin metrics after accepted uploads.
7. Added Vitest coverage for backend metrics hydration and PDF upload submission.

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184
- `frontend/src/components/AdminDashboard.tsx`
- `frontend/src/components/MetricGrid.tsx`
- `frontend/src/components/PdfUploadPanel.tsx`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- Validation: `npm run test` from `frontend/` passes.
- Validation: `npm run build` from `frontend/` passes.
- Validation: `npm run lint` from `frontend/` passes.
- Validation: `ruff check .` passes.