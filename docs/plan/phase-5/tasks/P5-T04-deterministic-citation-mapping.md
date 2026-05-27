# P5-T04 - Add deterministic citation mapping

## Sub-issue description
### Objective
Ensure generated answer citations are deterministic, deduplicated, and stably ordered relative to retrieved evidence.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `CitationMapper` service in `src/farmer_helper/services/answering/citation_mapper.py`.
2. Added deterministic deduplication and ranking behavior by score and stable identity fields.
3. Wired citation mapping into `src/farmer_helper/services/answering/generation_service.py`.
4. Added mapper tests in `tests/unit/test_citation_mapper.py` and generation-service citation behavior coverage in `tests/unit/test_answer_generation_service.py`.

## Decisions made
- Citation identity should be stable and content-backed.
- Mapping behavior should be deterministic for regression testing.
