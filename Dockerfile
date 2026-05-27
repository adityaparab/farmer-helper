FROM node:22-slim AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FRONTEND_SERVE_ENABLED=true
ENV FRONTEND_DIST_DIR=/app/frontend/dist

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn farmer_helper.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
