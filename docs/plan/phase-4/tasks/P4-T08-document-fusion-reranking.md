# P4-T08 - Document fusion and reranking behavior

## Sub-issue description
### Objective
Document retrieval fusion, reranking options, deterministic ordering, and API output semantics for maintainers and integrators.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `docs/development/RETRIEVAL_PIPELINE.md` covering retrieval stages and endpoint behavior.
2. Documented fusion formula, deduplication key, and deterministic tie-break ordering.
3. Documented reranker options and unsupported reranker behavior.
4. Documented retrieval response citation metadata and metrics fields.
5. Added retrieval documentation references in `README.md` and `docs/development/ARCHITECTURE_OVERVIEW.md`.

## Decisions made
- Documentation should be implementation-accurate and test-aligned.
- Include deterministic ordering guarantees and observability fields explicitly.
