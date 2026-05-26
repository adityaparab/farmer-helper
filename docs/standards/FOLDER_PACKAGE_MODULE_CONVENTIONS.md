# Folder, Package, and Module Conventions

## Purpose
Define repository structure and naming conventions that enforce architectural boundaries and ownership clarity.

## Top-level conventions
1. `docs/`: Planning, standards, architecture, and operational documentation.
2. `scripts/`: Automation scripts for developer and operational workflows.
3. `config/`: Environment and runtime config templates/examples.
4. `src/` (Phase 1+): Application code organized by architectural layer.
5. `tests/` (Phase 1+): Test suites organized by test type.

## Application structure conventions (Phase 1+)
1. `src/api/`
- HTTP routes, request/response schemas, transport-only concerns.

2. `src/services/`
- Business orchestration, policy enforcement, workflow coordination.

3. `src/repositories/`
- Data access/query logic only.

4. `src/domain/`
- Core entities, value objects, typed contracts.

5. `src/adapters/`
- External system integrations (LLM, embeddings, telemetry, storage).

6. `src/core/`
- Shared configuration, error definitions, and cross-cutting utilities.

## Naming rules
1. Files and modules: `snake_case`.
2. Classes: `PascalCase`.
3. Functions/variables: `snake_case`.
4. Constants and environment keys: `UPPER_SNAKE_CASE`.

## Dependency direction rules
1. API may depend on services and schemas only.
2. Services may depend on repositories, domain, and adapters via interfaces.
3. Repositories may depend on persistence models and DB abstractions only.
4. Adapters may not call API handlers.
5. Domain must remain framework-light and side-effect minimal.

## Test folder conventions (Phase 1+)
1. `tests/unit/`
2. `tests/integration/`
3. `tests/contract/`
4. `tests/regression/`

Test file names should mirror module names with `_test` suffix conventions according to selected test framework.

## Documentation conventions
1. Each phase deliverable must have a stable path under `docs/`.
2. Architecture-impacting decisions require ADR updates.
3. Operational behavior changes require runbook/playbook updates.

## Ownership and review
1. Code owners enforce boundary compliance during review.
2. New folders/modules require documented rationale in PR description.