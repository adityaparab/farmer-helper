# P0-T09 - Curate evaluation question set

## Sub-issue description
### Objective
Curate an initial evaluation question set to bootstrap measurable retrieval and grounded-answer quality checks.

### Deliverables
1. Seed evaluation question set with metadata.
2. Initial scoring rubric.
3. Dataset maintenance and growth rules.

### Acceptance criteria
- Question set is representative and diverse.
- Scoring rubric is explicit.
- Maintenance guidance exists.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added `docs/evaluation/EVAL_QUESTION_SET.md`.
2. Curated 10 seed questions across easy/medium/hard difficulty.
3. Added rubric and maintenance rules.

## Decisions made
- Include refusal/uncertainty scenarios in the seed set.
- Keep schema simple to support future automation.

## Evidence
- Deliverable file present at `docs/evaluation/EVAL_QUESTION_SET.md`.
- Epic tracker updated at `docs/plan/phase-0/EPIC.md`.