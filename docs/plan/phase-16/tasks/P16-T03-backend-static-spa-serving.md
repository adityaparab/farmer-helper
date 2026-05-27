# P16-T03 - Serve SPA index and assets from backend startup path

## Sub-issue description
### Objective
Enable the backend to serve the frontend build output, including SPA fallback, when the server starts.

### Deliverables
1. Configuration for frontend dist directory and feature toggle.
2. Backend static asset mounting and index fallback routing.
3. Smoke test coverage for root, fallback route, and static asset serving.

### Acceptance criteria
- Backend serves index.html at root when dist is available.
- Client-side routes return SPA fallback index.
- Static assets are served from mounted dist assets.
- Health and core API routes remain accessible.

## Implementation status
- Status: In Progress
- Started: 2026-05-27

## What was done
1. Added frontend static serving settings in backend config.
2. Registered startup-time static routes and fallback logic in app creation.
3. Added public-route bypasses for frontend/auth paths in security guard.
4. Added and passed smoke test validating index, fallback, and assets.

## Evidence
- src/farmer_helper/core/config.py
- src/farmer_helper/main.py
- src/farmer_helper/services/security/guard.py
- tests/smoke/test_frontend_static_serving.py

## Risks and follow-ups
- Build/deploy pipeline still needs frontend artifact production and copy strategy.
- API key + JWT model harmonization must be finalized during auth phase.
