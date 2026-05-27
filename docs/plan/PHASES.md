# Farmer Helper Engineering Blueprint

## Purpose
This document provides a Copilot-friendly, phase-wise engineering plan for building Farmer Helper as an expert-grade, production-ready, backend-first AI system.

## Global execution rules
- Every phase must be broken down into logical, measurable, quantifiable, and testable steps.
- Each phase maps to one GitHub Epic.
- Each step within a phase maps to a sub-issue/task under that phase Epic.
- No phase is complete until all sub-issues are complete, tests pass, documentation is updated, and CI quality gates pass.
- Code produced in any implementation phase must be expert professional grade: modular, testable, readable, maintainable, configuration-driven, observable, secure, performant, and built with clear separation of concerns and single responsibility.

## Context-engineering guidance for Copilot
- Work phase-by-phase; do not pull the entire roadmap into active coding context unless necessary.
- Prefer referencing the active phase Epic and its child tasks only.
- Keep prompts focused on one task, one module, or one acceptance criterion at a time.
- Use repository docs as source of truth for standards before generating code.
- When implementing, update tests and docs in the same change.

## Phase index
0. Architecture baseline and engineering standards
1. Backend skeleton and repository setup
2. Document ingestion pipeline
3. Embedding pipeline and pgvector integration
4. Hybrid retrieval and reranking
5. Grounded answer generation and citations
6. Session memory and multi-turn handling
7. Reliability and fault tolerance
8. Evaluation and regression framework
9. Observability and alerting
10. Security, abuse resistance, and AI safety
11. Performance optimization and cost controls
12. Admin operations and maintainability
13. Scalability and concurrency hardening
14. Accessibility-ready API design
15. Final production readiness review
16. Web interface, auth RBAC, and production integration program
17. Auth and RBAC foundation
18. Frontend backend integration and authenticated workflows

---

## Phase 0 — Architecture baseline and engineering standards
**Goal:** Define the structural, operational, and quality standards for all project phases.

### Steps
1. Create ADRs for stack, interfaces, and module boundaries.
2. Document engineering quality charter.
3. Define CI/CD quality gates.
4. Write test and documentation strategy.
5. Define measurable KPIs for retrieval, latency, groundedness, and reliability.
6. Define error taxonomy and fallback matrix.
7. Document folder/package/module conventions.
8. Create development and production example config files.
9. Curate evaluation question set.
10. Create phase sign-off checklist.

### Acceptance criteria
- All artifacts committed and referenced from README/docs.
- CI rules documented.
- KPIs and fallback policies explicit and measurable.

---

## Phase 1 — Backend skeleton and repository setup
**Goal:** Establish the deployable, testable foundation for all later phases.

### Steps
1. Scaffold standardized repo structure.
2. Implement FastAPI app shell with configuration.
3. Set up Railway deployment and env secrets.
4. Add database schema and migrations for foundational tables.
5. Add live and ready health endpoints.
6. Add structured logging, request IDs, and error reporting.
7. Enforce API-service-repository-schema separation.
8. Configure linting, typing, formatting, and pre-commit hooks.
9. Add smoke tests and unit tests.
10. Add onboarding and codebase documentation.

### Acceptance criteria
- Railway deployment works.
- Health endpoints pass.
- CI is green.
- App structure is stable and documented.

---

## Phase 2 — Document ingestion pipeline
**Goal:** Build a reliable, idempotent, and testable ingestion pipeline for source documents.

### Steps
1. Validate input files before ingestion.
2. Extract text from PDFs with deterministic error handling.
3. Normalize and clean extracted text.
4. Chunk text with page-aware, configurable chunking.
5. Attach metadata such as page ranges, headings, version, and content hash.
6. Persist ingestion status and error state.
7. Enforce idempotent re-ingestion behavior.
8. Add unit, integration, and failure-path tests.
9. Add ingestion logs and processing traces.
10. Document ingestion flow and operational guidance.

### Acceptance criteria
- Re-ingestion does not duplicate chunks.
- Chunk quality and metadata are manually spot-checked.
- Failure paths are observable and recoverable.

---

## Phase 3 — Embedding pipeline and pgvector integration
**Goal:** Provide cloud-API embeddings for all chunks and store vectors in pgvector.

### Steps
1. Create embedding provider abstraction.
2. Add batch embedding logic.
3. Extend schema for vector persistence/upsert.
4. Add retry and error handling for embedding jobs.
5. Add async-safe job orchestration.
6. Add API/CLI trigger for embeddings.
7. Add integration and smoke tests with coverage target.
8. Document provider versioning and extension path.

### Acceptance criteria
- Embeddings are stored and queryable.
- Provider failures do not corrupt pipeline state.
- Embedding path passes coverage threshold.

---

## Phase 4 — Hybrid retrieval and reranking
**Goal:** Retrieve top-K relevant chunks via vector + keyword search with optional reranking.

### Steps
1. Implement vector retrieval.
2. Implement keyword retrieval.
3. Merge and deduplicate results with explicit fusion logic.
4. Add pluggable reranker interface.
5. Add retrieval API endpoint with score and citation metadata.
6. Add end-to-end retrieval tests and metrics.
7. Log retrieval diagnostics and timings.
8. Document fusion and reranking behavior.

### Acceptance criteria
- Retrieval quality is measurable on eval set.
- Reranker is optional and config-driven.
- API returns typed, structured retrieval results.

---

## Phase 5 — Grounded answer generation and citations
**Goal:** Generate grounded, citation-rich answers via LLM APIs using retrieved chunks only.

### Steps
1. Build prompt builder with refusal and clarification policy.
2. Add LLM provider abstraction.
3. Build end-to-end answer generation API.
4. Add deterministic citation mapping.
5. Add refusal and ambiguity handling.
6. Add grounded-response regression tests.
7. Add usage, latency, and confidence logging.
8. Document prompting and provider switching.

### Acceptance criteria
- Answers are grounded and cited.
- Unsupported questions are declined cleanly.
- Regression tests cover accuracy and citation correctness.

---

## Phase 6 — Session memory and multi-turn handling
**Goal:** Support bounded, traceable conversation memory and follow-up questions.

### Steps
1. Add session and message schemas.
2. Add follow-up context resolution.
3. Add optional summarization for long sessions.
4. Pass bounded context through retrieval and answering.
5. Add expiry or archival rules.
6. Add multi-turn integration tests.
7. Add transcript export/import.
8. Document session behavior and extension points.

### Acceptance criteria
- Follow-ups work correctly.
- Context remains bounded and explainable.
- Session lifecycle is testable and documented.

---

## Phase 7 — Reliability and fault tolerance
**Goal:** Make failure handling explicit, safe, and observable.

### Steps
1. Add timeout and retry policies to external calls.
2. Add circuit breaker and fallback strategy.
3. Add idempotency protections.
4. Implement graceful degradation paths.
5. Normalize internal-to-user error responses.
6. Add failure injection tests.
7. Add failure observability fields.
8. Document resilience and runbook guidance.

### Acceptance criteria
- Common provider and infra failures are simulated in tests.
- Fallback paths are deterministic.
- No silent failure modes remain.

---

## Phase 8 — Evaluation and regression framework
**Goal:** Continuously measure retrieval and answer quality with automated evals.

### Steps
1. Build eval dataset loader.
2. Build eval runner.
3. Build offline eval reporting.
4. Integrate evals into CI.
5. Log online feedback signals.
6. Expand eval set incrementally.
7. Document eval maintenance and interpretation.

### Acceptance criteria
- CI fails on material regression.
- Quality metrics are tracked over time.
- Eval workflow is reproducible.

---

## Phase 9 — Observability and alerting
**Goal:** Ensure every critical flow is diagnosable through logs, traces, and metrics.

### Steps
1. Add structured logging across modules.
2. Propagate request IDs through all layers.
3. Add stage-level timing metrics.
4. Integrate with Railway/Sentry.
5. Enforce log redaction/privacy.
6. Document operational debugging workflows.

### Acceptance criteria
- A single request can be traced end-to-end.
- Sensitive data is redacted.
- Alerts and errors are actionable.

---

## Phase 10 — Security, abuse resistance, and AI safety
**Goal:** Secure the API and AI workflow against abuse, leakage, and prompt attacks.

### Steps
1. Add auth and rate limiting.
2. Enforce strict input validation.
3. Protect secrets and environment configuration.
4. Add prompt injection defenses and tests.
5. Add security audit logging.
6. Add regression tests for exploit scenarios.
7. Document security model and runbook.

### Acceptance criteria
- Abuse cases are rejected and logged.
- Secrets are never exposed in logs.
- Security checks are part of CI and review.

---

## Phase 11 — Performance optimization and cost controls
**Goal:** Improve runtime efficiency and control third-party usage costs.

### Steps
1. Add caching for retrieval and answers where appropriate.
2. Add model tiering/routing.
3. Add context trimming and deduplication.
4. Move heavy work off request path asynchronously.
5. Add performance and cost regression tests.
6. Document tuning and cost-control levers.

### Acceptance criteria
- Latency and cost are benchmarked.
- Cache and async behavior are tested.
- Tuning remains configuration-driven.

---

## Phase 12 — Admin operations and maintainability
**Goal:** Provide safe operational workflows for ingestion, versioning, QA review, and rollback.

### Steps
1. Add admin API for ingestion and reindex workflows.
2. Add versioned content/model/pipeline tracking.
3. Add gold-answer/editor workflow.
4. Add QA/corpus review queue.
5. Add access audit logs.
6. Document admin and rollback playbooks.

### Acceptance criteria
- Reindex and rollback flows are safe and documented.
- Admin actions are traceable.
- Versioning is explicit.

---

## Phase 13 — Scalability and concurrency hardening
**Goal:** Validate the system under concurrency and prepare it to scale cleanly.

### Steps
1. Configure and test connection pooling.
2. Move background jobs to worker execution.
3. Add concurrent load test scenarios.
4. Document scale limits and bottleneck strategy.
5. Verify ingestion and query paths can coexist under load.

### Acceptance criteria
- Concurrent load tests pass defined thresholds.
- Critical shared-state risks are addressed.
- Scaling path is documented.

---

## Phase 14 — Accessibility-ready API design
**Goal:** Keep the backend ready for future accessible clients and multiple response modes.

### Steps
1. Define concise and detailed response schemas.
2. Standardize error contracts.
3. Add language selection hooks.
4. Prototype streaming responses if needed.
5. Document response compatibility guidance.

### Acceptance criteria
- API responses are machine-readable and future-proof.
- Structured outputs support future accessibility work.
- Backward compatibility expectations are documented.

---

## Phase 15 — Final production readiness review
**Goal:** Execute the final launch gate across functionality, quality, security, and operability.

### Steps
1. Review all phase completion criteria.
2. Run staging dry run with realistic data and failure scenarios.
3. Prepare release, rollback, and incident runbooks.
4. Verify docs, badges, CI, coverage, and monitoring links.
5. Perform final sign-off.

### Acceptance criteria
- All prior phase criteria satisfied.
- Staging results are acceptable.
- Release artifacts and runbooks exist.

---

## Copilot execution pattern
When implementing a phase:
1. Read the active phase section only.
2. Read the linked Epic and child tasks.
3. Implement one child task at a time.
4. Update code, tests, docs, and config together.
5. Run local quality gates before opening a PR.
6. Keep changes atomic and traceable to a single issue.
