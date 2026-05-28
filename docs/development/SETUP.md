# Developer Setup

## Prerequisites
1. Python 3.12+
2. Git
3. Optional: PostgreSQL 16+ for parity with production

## Install dependencies
1. Create virtual environment.
2. Install package in editable mode with dev dependencies.

Example:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run the API
```powershell
uvicorn farmer_helper.main:app --reload --host 127.0.0.1 --port 8000
```

Alternative one-command local start:
```powershell
./scripts/run-local.ps1
```

## Run migrations
```powershell
alembic upgrade head
```

## Verify local run
```powershell
Invoke-WebRequest http://127.0.0.1:8000/health/live -UseBasicParsing | Select-Object -ExpandProperty StatusCode
Invoke-WebRequest http://127.0.0.1:8000/health/ready -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

## Run with Docker
```powershell
docker compose up --build
```

Optional migration command in containerized flow:
```powershell
docker compose run --rm api alembic upgrade head
```

## Run quality checks
```powershell
ruff check src tests
black --check src tests
mypy src
pytest -q
```

## Pre-commit hooks
```powershell
pre-commit install --hook-type pre-commit --hook-type commit-msg
pre-commit run --all-files
```

The pre-commit chain runs lint-fix, Black, Ruff, the full backend test suite, frontend lint-fix, frontend lint, frontend tests, frontend build, and commit-message validation.

Commit messages should follow conventional commit style, for example `feat: add retry policy` or `fix(api): validate input`.
