# Epic: Phase 0 - Architecture baseline and engineering standards

## Summary
Define and lock baseline engineering standards, architecture boundaries, quality controls, and measurable outcomes before backend implementation begins.

## Scope
This Epic maps to Phase 0 in `docs/plan/PHASES.md` and is the source of truth for sub-issue status.

## Epic status
- Status: Completed
- Completed on: 2026-05-26
- Local/remote sync: Verified (local markdown and GitHub issues aligned)

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P0-T01 | Create ADRs for stack, interfaces, and module boundaries | Completed | 2026-05-26 | ADRs 0001-0003 authored and linked |
| P0-T02 | Document engineering quality charter | Completed | 2026-05-26 | Charter created in standards docs |
| P0-T03 | Define CI/CD quality gates | Completed | 2026-05-26 | Gate policy documented with required checks |
| P0-T04 | Write test and documentation strategy | Completed | 2026-05-26 | Strategy doc added with lifecycle and ownership |
| P0-T05 | Define measurable KPIs | Completed | 2026-05-26 | KPI spec added with formulas and thresholds |
| P0-T06 | Define error taxonomy and fallback matrix | Completed | 2026-05-26 | Error classes, mappings, and fallback actions documented |
| P0-T07 | Document folder/package/module conventions | Completed | 2026-05-26 | Repository conventions documented for layering and ownership |
| P0-T08 | Create development and production example config files | Completed | 2026-05-26 | Dev/prod config examples added under config/examples |
| P0-T09 | Curate evaluation question set | Completed | 2026-05-26 | Seed evaluation set with scoring rubric published |
| P0-T10 | Create phase sign-off checklist | Completed | 2026-05-26 | Final checklist and evidence requirements documented |

## Decision log
- 2026-05-26: Use ADR format based on Context/Decision/Consequences for consistent, audit-friendly architecture records.
- 2026-05-26: Keep issue tracking in-repo while bootstrap phase is in progress to ensure planning and implementation remain coupled.
- 2026-05-26: Promote engineering quality charter to a first-class standards document consumed by all later phases.
- 2026-05-26: Define CI/CD gates as policy first, then map to concrete CI implementation in Phase 1 repository setup.
- 2026-05-26: Define testing and docs maintenance lifecycle early to avoid drift once implementation phases accelerate.
- 2026-05-26: Separate KPI definitions into offline quality metrics and online reliability/latency SLOs.
- 2026-05-26: Use explicit error taxonomy with deterministic fallback mapping to avoid silent failures.
- 2026-05-26: Phase 0 completion requires both in-repo artifacts and synced GitHub issue updates.

## Exit criteria for Epic completion
- All P0 sub-issues marked Completed.
- Artifacts linked from README/docs.
- CI quality gates defined and enforceable.
- KPIs and fallback policies explicit and measurable.

## Completion confirmation
Phase 0 deliverables are complete, linked, and sign-off artifacts are present.
Remote GitHub Step issues (#2-#11) are closed and Epic issue status has been updated.