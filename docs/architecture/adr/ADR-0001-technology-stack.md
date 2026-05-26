# ADR-0001: Core technology stack

- Status: Accepted
- Date: 2026-05-26
- Owners: Platform/Backend

## Context
Farmer Helper requires a backend-first architecture optimized for reliability, explainability, and rapid iteration across ingestion, retrieval, and grounded answer generation. The system must support API-first integration, observability, and strict quality gates from early phases.

## Decision
Adopt the following baseline stack:
- Language/runtime: Python 3.12+
- API framework: FastAPI
- Data validation and settings: Pydantic v2
- Database: PostgreSQL 16+
- Vector storage: pgvector extension
- Migrations: Alembic
- Packaging/dependency management: pip-tools or Poetry (finalized in implementation phase)
- Testing: pytest, pytest-asyncio, coverage.py
- Lint/format/type checks: Ruff, Black (optional if Ruff formatter enabled), mypy
- Observability: structured JSON logging and OpenTelemetry-compatible tracing hooks
- Deployment target: Railway (primary), local Docker for development parity

## Consequences
### Positive
- Strong ecosystem maturity and hiring familiarity.
- Fast API iteration with type-driven schema generation.
- Unified relational and vector storage reduces operational overhead.
- Migrations and typing support predictable, testable change management.

### Trade-offs
- Python concurrency and CPU-bound workloads may require worker strategy tuning.
- pgvector performance must be validated under realistic corpus size and query load.
- Tooling decisions (Poetry vs pip-tools) still need final standardization.

### Follow-up constraints
- All external model providers must be abstracted behind provider interfaces.
- Any new dependency requires security/license review and rationale.