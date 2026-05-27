# Railway Deployment

## Deployment artifacts
1. `railway.json` selects the Dockerfile builder and defines startup and healthcheck path.
2. `Procfile` provides compatible web process command.
3. `config/examples/.env.production.example` defines required environment keys.
4. `Dockerfile` builds the Vite frontend in a Node stage and copies `frontend/dist` into the FastAPI runtime image.

## Required environment variables
At minimum set:
1. `APP_ENV=production`
2. `APP_LOG_LEVEL=INFO`
3. `DATABASE_URL=<railway-postgres-url>`
4. `SENTRY_DSN=<optional>`
5. `SENTRY_TRACES_SAMPLE_RATE=<optional, default 0.0>`
6. `SENTRY_ENVIRONMENT=<optional, default APP_ENV>`
7. Provider configuration values (`LLM_PROVIDER`, `LLM_MODEL`, `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`)
8. `SECURITY_API_KEY=<recommended in production>`
9. `SECURITY_RATE_LIMIT_REQUESTS=<optional, default 0 (disabled)>`
10. `SECURITY_RATE_LIMIT_WINDOW_SECONDS=<optional, default 60>`
11. `PERFORMANCE_CACHE_MAX_ENTRIES=<optional, default 512>`
12. `RETRIEVAL_CACHE_TTL_SECONDS=<optional, default 0 (disabled)>`
13. `ANSWER_CACHE_TTL_SECONDS=<optional, default 0 (disabled)>`
14. `LLM_MODEL_LOW_COST=<optional>`
15. `LLM_MODEL_HIGH_QUALITY=<optional>`
16. `LLM_MODEL_ROUTER_QUESTION_LENGTH_THRESHOLD=<optional, default 120>`
17. `SESSION_CONTEXT_MAX_CHARS_PER_MESSAGE=<optional, default 300>`
18. `DATABASE_POOL_MIN=<optional, default 2>`
19. `DATABASE_POOL_MAX=<optional, default 10>`
20. `DATABASE_POOL_TIMEOUT_SECONDS=<optional, default 30>`
21. `EMBEDDING_WORKER_COUNT=<optional, default 2>`
22. `EMBEDDING_JOB_QUEUE_MAX_SIZE=<optional, default 100>`
23. `FRONTEND_SERVE_ENABLED=true`
24. `FRONTEND_DIST_DIR=/app/frontend/dist`

## Frontend serving
The Railway Docker image builds the React/Vite app during `docker build` and copies the generated assets to `/app/frontend/dist`. FastAPI serves `/`, `/assets/*`, and SPA fallback routes from that directory when `FRONTEND_SERVE_ENABLED=true`.

Keep `FRONTEND_DIST_DIR=/app/frontend/dist` in Railway unless the Dockerfile layout changes. API routes such as `/auth`, `/admin`, `/answers`, `/retrieval`, `/embeddings`, `/health`, `/docs`, and `/openapi.json` remain backend routes and are excluded from the SPA fallback.

## Health checks
1. Liveness: `/health/live`
2. Readiness: `/health/ready`

## Deployment steps
1. Connect repository to Railway project.
2. Add required environment variables.
3. Deploy `main` branch.
4. Validate `/health/live` and `/health/ready` after migration.
5. Validate `/` returns the frontend `index.html` and `/assets/*` returns built frontend assets.

## Notes
Actual secret values must be managed only in Railway variables and never committed.
