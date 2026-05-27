# P14-T01 - Define concise and detailed response schemas

## Sub-issue description
### Objective
Add response-mode aware contracts that allow clients to request concise or detailed payloads while preserving backward compatibility.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `response_mode` hooks to answer and retrieval request schemas.
2. Added `response_mode` fields to answer and retrieval response schemas.
3. Added route-level propagation so response payloads include the selected mode.
