# P0-T08 - Create development and production example config files

## Sub-issue description
### Objective
Provide reference environment configuration files for development and production to reduce misconfiguration risk and improve deployment consistency.

### Deliverables
1. Development example environment file.
2. Production example environment file.
3. Variable set covering app, database, retrieval, model, and observability.

### Acceptance criteria
- Both config examples exist and are readable.
- Variables cover critical functional and operational settings.
- Sensitive values are placeholders only.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `config/examples/.env.development.example`.
2. Added `config/examples/.env.production.example`.
3. Included app/database/provider/retrieval/observability/security-related keys.

## Decisions made
- Use placeholder values for all secret-like fields.
- Keep development defaults practical and production defaults conservative.

## Evidence
- Deliverable files present under `config/examples/`.
- Epic tracker updated at `docs/plan/phase-0/EPIC.md`.