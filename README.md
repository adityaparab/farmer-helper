# farmer-helper

Backend-first AI system for grounded, citation-rich agricultural question answering based on a curated document set.

## Quickstart
Run locally (native):
1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `pip install -e .[dev]`
4. `alembic upgrade head`
5. `uvicorn farmer_helper.main:app --reload --host 127.0.0.1 --port 8000`

Run locally (Docker):
1. `docker compose up --build`

Health checks:
1. `http://127.0.0.1:8000/health/live`
2. `http://127.0.0.1:8000/health/ready`

## Planning
The engineering roadmap is documented in `docs/plan/PHASES.md`.

Use the roadmap phase-by-phase. Each phase is broken into measurable, testable steps and is intended to map to GitHub Epics and sub-issues for focused implementation.

## Execution tracking
Active implementation tracking for Phase 0 lives in:
- `docs/plan/phase-0/EPIC.md`
- `docs/plan/phase-0/tasks/`

Active implementation tracking for Phase 1 lives in:
- `docs/plan/phase-1/EPIC.md`
- `docs/plan/phase-1/tasks/`

Active implementation tracking for Phase 2 lives in:
- `docs/plan/phase-2/EPIC.md`
- `docs/plan/phase-2/tasks/`

GitHub issue status comment standard:
- `docs/plan/ISSUE_COMMENT_TEMPLATE.md`
- `scripts/post-issue-status-comment.ps1`

Architecture decisions from Phase 0 Task 1:
- `docs/architecture/adr/ADR-0001-technology-stack.md`
- `docs/architecture/adr/ADR-0002-module-boundaries.md`
- `docs/architecture/adr/ADR-0003-service-interfaces.md`

Engineering quality charter from Phase 0 Task 2:
- `docs/standards/ENGINEERING_QUALITY_CHARTER.md`

CI/CD quality gates from Phase 0 Task 3:
- `docs/standards/CI_CD_QUALITY_GATES.md`

Test and documentation strategy from Phase 0 Task 4:
- `docs/standards/TEST_AND_DOCUMENTATION_STRATEGY.md`

KPI specification from Phase 0 Task 5:
- `docs/standards/KPI_SPECIFICATION.md`

Error taxonomy and fallback matrix from Phase 0 Task 6:
- `docs/standards/ERROR_TAXONOMY_AND_FALLBACK_MATRIX.md`

Folder/package/module conventions from Phase 0 Task 7:
- `docs/standards/FOLDER_PACKAGE_MODULE_CONVENTIONS.md`

Config examples from Phase 0 Task 8:
- `config/examples/.env.development.example`
- `config/examples/.env.production.example`

Evaluation question set from Phase 0 Task 9:
- `docs/evaluation/EVAL_QUESTION_SET.md`

Phase sign-off checklist from Phase 0 Task 10:
- `docs/plan/phase-0/PHASE_SIGN_OFF_CHECKLIST.md`

## Phase 1 backend foundation
Core backend implementation:
- `src/farmer_helper/main.py`
- `src/farmer_helper/core/config.py`
- `src/farmer_helper/api/routes/health.py`

Database and migrations:
- `src/farmer_helper/db/models/foundation.py`
- `alembic/`

Quality and automation:
- `.github/workflows/ci.yml`
- `.pre-commit-config.yaml`
- `pyproject.toml`

Developer and deployment docs:
- `docs/development/SETUP.md`
- `docs/development/ARCHITECTURE_OVERVIEW.md`
- `docs/deployment/RAILWAY_DEPLOYMENT.md`

## Phase 2 ingestion progress
Input file validation:
- `src/farmer_helper/services/ingestion/file_validator.py`
- `src/farmer_helper/schemas/ingestion.py`
- `tests/unit/test_file_validator.py`

PDF extraction and normalization:
- `src/farmer_helper/services/ingestion/pdf_extractor.py`
- `src/farmer_helper/services/ingestion/text_normalizer.py`
- `tests/unit/test_pdf_extractor.py`
- `tests/unit/test_text_normalizer.py`

Chunking and metadata:
- `src/farmer_helper/services/ingestion/text_chunker.py`
- `src/farmer_helper/services/ingestion/chunk_metadata_enricher.py`
- `tests/unit/test_text_chunker.py`
- `tests/unit/test_chunk_metadata_enricher.py`

Status, idempotency, and observability:
- `src/farmer_helper/repositories/document_repository.py`
- `src/farmer_helper/services/ingestion/idempotency_service.py`
- `src/farmer_helper/services/ingestion/status_service.py`
- `src/farmer_helper/services/ingestion/trace_logger.py`
- `tests/unit/test_idempotency_service.py`
- `tests/unit/test_ingestion_status_service.py`
- `tests/unit/test_ingestion_trace_logging.py`
- `tests/integration/test_ingestion_pipeline_paths.py`

Operational documentation:
- `docs/development/INGESTION_PIPELINE.md`
