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

## Next phases
1. Document ingestion pipeline.
2. Embedding and retrieval pipelines.
3. Grounded answer generation with citations.
