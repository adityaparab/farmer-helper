# P18-T04 - Connect user chat and history UI

## Sub-issue description
### Objective
Wire user chat submission and history surfaces to backend answer/session contracts with TanStack AI-ready boundaries.

### Acceptance criteria
- User questions are submitted through a typed backend answer/session client.
- Chat and history state distinguishes pending, answered, refused, and failed responses.
- Each conditionally rendered chat state is a separate component.
- The integration remains ready for TanStack AI streaming without coupling UI components to transport details.
- Vitest coverage exercises submit, history update, and failure states.

## Implementation status
- Status: Not Started
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/188

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184