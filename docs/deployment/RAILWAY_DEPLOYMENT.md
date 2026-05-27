# Railway Deployment

## Deployment artifacts
1. `railway.json` defines startup and healthcheck path.
2. `Procfile` provides compatible web process command.
3. `config/examples/.env.production.example` defines required environment keys.

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

## Health checks
1. Liveness: `/health/live`
2. Readiness: `/health/ready`

## Deployment steps
1. Connect repository to Railway project.
2. Add required environment variables.
3. Deploy `main` branch.
4. Validate `/health/live` and `/health/ready` after migration.

## Notes
Actual secret values must be managed only in Railway variables and never committed.
