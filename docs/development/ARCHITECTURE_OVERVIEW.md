# Architecture Overview

## Layering
1. API layer: `src/farmer_helper/api/`
2. Service layer: `src/farmer_helper/services/`
3. Repository layer: `src/farmer_helper/repositories/`
4. Schema layer: `src/farmer_helper/schemas/`
5. Core/config/logging: `src/farmer_helper/core/`
6. Persistence models: `src/farmer_helper/db/models/`

## Current capabilities
1. FastAPI app shell with app factory.
2. Health endpoints (`/health/live`, `/health/ready`).
3. Structured JSON logging with request ID propagation.
4. Foundational schema and migration path via Alembic.
5. Deterministic ingestion pipeline with status persistence and trace logging.
6. Embedding pipeline foundation with provider abstraction, batching, retries, orchestration, and API/CLI triggers.

## Operational references
1. Ingestion flow guide: `docs/development/INGESTION_PIPELINE.md`
2. Embedding provider guide: `docs/development/EMBEDDING_PROVIDERS.md`

## Next phases
1. Hybrid retrieval and reranking pipeline.
2. Grounded answer generation with citations.
3. Session memory and multi-turn handling.
