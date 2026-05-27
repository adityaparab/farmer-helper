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

Active implementation tracking for Phase 3 lives in:
- `docs/plan/phase-3/EPIC.md`
- `docs/plan/phase-3/tasks/`

Active implementation tracking for Phase 4 lives in:
- `docs/plan/phase-4/EPIC.md`
- `docs/plan/phase-4/tasks/`

Active implementation tracking for Phase 5 lives in:
- `docs/plan/phase-5/EPIC.md`
- `docs/plan/phase-5/tasks/`

Active implementation tracking for Phase 6 lives in:
- `docs/plan/phase-6/EPIC.md`
- `docs/plan/phase-6/tasks/`

Active implementation tracking for Phase 7 lives in:
- `docs/plan/phase-7/EPIC.md`
- `docs/plan/phase-7/tasks/`

Active implementation tracking for Phase 8 lives in:
- `docs/plan/phase-8/EPIC.md`
- `docs/plan/phase-8/tasks/`

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

## Phase 3 embedding progress
Provider contracts, batching, and retries:
- `src/farmer_helper/schemas/embedding.py`
- `src/farmer_helper/services/embedding/provider.py`
- `src/farmer_helper/services/embedding/batch_service.py`
- `src/farmer_helper/services/embedding/retrying_provider.py`
- `tests/unit/test_embedding_provider_abstraction.py`
- `tests/unit/test_embedding_batch_service.py`
- `tests/unit/test_retrying_embedding_provider.py`

Persistence and orchestration:
- `src/farmer_helper/db/models/foundation.py`
- `src/farmer_helper/repositories/chunk_embedding_repository.py`
- `src/farmer_helper/services/embedding/orchestration_service.py`
- `tests/unit/test_chunk_embedding_repository.py`
- `tests/unit/test_embedding_orchestration_service.py`

Trigger surfaces and end-to-end tests:
- `src/farmer_helper/api/routes/embeddings.py`
- `scripts/trigger-embeddings.py`
- `tests/unit/test_embedding_trigger_route.py`
- `tests/integration/test_embedding_trigger_integration.py`
- `tests/smoke/test_embedding_trigger.py`

Provider versioning and extension documentation:
- `docs/development/EMBEDDING_PROVIDERS.md`

## Phase 4 retrieval progress
Retrieval services and contracts:
- `src/farmer_helper/schemas/retrieval.py`
- `src/farmer_helper/services/retrieval/vector_retrieval_service.py`
- `src/farmer_helper/services/retrieval/keyword_retrieval_service.py`
- `src/farmer_helper/services/retrieval/fusion_service.py`
- `src/farmer_helper/services/retrieval/reranker.py`
- `src/farmer_helper/services/retrieval/query_service.py`

Retrieval API and tests:
- `src/farmer_helper/api/routes/retrieval.py`
- `tests/unit/test_vector_retrieval_service.py`
- `tests/unit/test_keyword_retrieval_service.py`
- `tests/unit/test_retrieval_fusion_service.py`
- `tests/unit/test_reranker.py`
- `tests/unit/test_retrieval_query_service.py`
- `tests/unit/test_retrieval_route.py`
- `tests/integration/test_retrieval_query_integration.py`
- `tests/smoke/test_retrieval_query.py`

Retrieval behavior documentation:
- `docs/development/RETRIEVAL_PIPELINE.md`

## Phase 5 answer-generation progress
Prompting foundation:
- `src/farmer_helper/schemas/answering.py`
- `src/farmer_helper/services/answering/prompt_builder.py`
- `src/farmer_helper/services/answering/provider.py`
- `src/farmer_helper/services/answering/generation_service.py`
- `src/farmer_helper/services/answering/mock_provider.py`
- `src/farmer_helper/services/answering/citation_mapper.py`
- `src/farmer_helper/services/answering/diagnostics_logger.py`
- `src/farmer_helper/api/routes/answers.py`
- `tests/unit/test_prompt_builder.py`
- `tests/unit/test_llm_provider_abstraction.py`
- `tests/unit/test_answer_generation_service.py`
- `tests/integration/test_multi_turn_session_flow.py`
- `tests/unit/test_answer_generation_route.py`
- `tests/unit/test_citation_mapper.py`
- `tests/integration/test_answer_generation_regression.py`
- `tests/unit/test_answer_diagnostics_logging.py`

Answer-generation documentation:
- `docs/development/ANSWERING_PIPELINE.md`

## Phase 6 session-memory progress
Session and message foundations:
- `src/farmer_helper/schemas/session.py`
- `src/farmer_helper/repositories/chat_session_repository.py`
- `src/farmer_helper/services/session/context_resolver.py`
- `src/farmer_helper/services/session/summarizer.py`
- `src/farmer_helper/services/session/lifecycle_service.py`
- `src/farmer_helper/services/session/transcript_service.py`
- `src/farmer_helper/api/routes/retrieval.py`
- `src/farmer_helper/api/routes/answers.py`
- `src/farmer_helper/db/models/foundation.py`
- `alembic/versions/20260527_0004_session_memory_schema.py`
- `tests/unit/test_session_schemas.py`
- `tests/unit/test_chat_session_repository.py`
- `tests/unit/test_follow_up_context_resolver.py`
- `tests/unit/test_session_summarizer.py`
- `tests/unit/test_session_lifecycle_service.py`
- `tests/unit/test_session_transcript_service.py`
- `tests/unit/test_retrieval_route.py`
- `tests/unit/test_answer_generation_service.py`

Session behavior documentation:
- `docs/development/SESSION_BEHAVIOR.md`

## Phase 7 reliability progress
Timeout and retry policy foundations:
- `src/farmer_helper/core/config.py`
- `src/farmer_helper/services/embedding/retrying_provider.py`
- `src/farmer_helper/services/embedding/timeout_provider.py`
- `src/farmer_helper/services/embedding/circuit_breaker_provider.py`
- `src/farmer_helper/services/answering/retrying_provider.py`
- `src/farmer_helper/services/answering/timeout_provider.py`
- `src/farmer_helper/services/answering/circuit_breaker_provider.py`
- `src/farmer_helper/services/reliability/idempotency.py`
- `src/farmer_helper/services/reliability/response_contracts.py`
- `src/farmer_helper/api/routes/embeddings.py`
- `src/farmer_helper/api/routes/answers.py`
- `tests/unit/test_retrying_embedding_provider.py`
- `tests/unit/test_timeout_embedding_provider.py`
- `tests/unit/test_circuit_breaker_embedding_provider.py`
- `tests/unit/test_retrying_llm_provider.py`
- `tests/unit/test_timeout_llm_provider.py`
- `tests/unit/test_circuit_breaker_llm_provider.py`
- `tests/unit/test_idempotency_store.py`
- `tests/unit/test_embedding_trigger_route.py`
- `tests/unit/test_answer_generation_route.py`

Reliability documentation:
- `docs/development/RELIABILITY_RUNBOOK.md`

## Phase 8 evaluation progress
Eval dataset foundation:
- `src/farmer_helper/schemas/evaluation.py`
- `src/farmer_helper/services/evaluation/dataset_loader.py`
- `src/farmer_helper/services/evaluation/runner.py`
- `src/farmer_helper/services/evaluation/reporting.py`
- `src/farmer_helper/services/evaluation/ci_gate.py`
- `scripts/run-evals.py`
- `docs/evaluation/EVAL_DATASET_SEED.jsonl`
- `tests/unit/test_eval_dataset_loader.py`
- `tests/unit/test_eval_runner.py`
- `tests/unit/test_eval_reporting.py`
- `tests/unit/test_eval_ci_gate.py`
