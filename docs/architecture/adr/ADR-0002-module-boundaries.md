# ADR-0002: Module boundaries and dependency direction

- Status: Accepted
- Date: 2026-05-26
- Owners: Platform/Backend

## Context
The roadmap requires expert-grade modularity, single responsibility, and testability. Without explicit module boundaries, ingestion, retrieval, and generation logic can become coupled and difficult to validate independently.

## Decision
Adopt strict layered boundaries and dependency direction:
- API layer: transport concerns only (request/response, auth, rate limits, contracts).
- Service layer: orchestration and business rules.
- Repository layer: persistence logic and query composition.
- Schema/domain layer: typed entities, DTOs, validation contracts.
- Infrastructure adapters: provider clients (LLM, embeddings, storage, observability).

Dependency rule:
- Inward dependencies only: API -> Service -> Repository -> Infrastructure/DB models.
- No repository calls from API handlers.
- No provider SDK calls outside adapter modules.
- Shared utilities must be pure and side-effect constrained.

## Consequences
### Positive
- Enables focused unit and integration testing.
- Reduces hidden coupling and improves maintainability.
- Makes fallback and resilience policies easier to enforce.

### Trade-offs
- Additional upfront structure increases initial implementation overhead.
- Requires discipline in review to prevent boundary leakage.

### Follow-up constraints
- Static analysis and architecture checks should be added in CI (Phase 1/3).
- Folder/package conventions must mirror these boundaries (Phase 0 Task 7).