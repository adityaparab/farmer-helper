# Engineering Quality Charter

## Purpose
This charter defines mandatory engineering standards for Farmer Helper. It applies to all phases, modules, and pull requests.

## Quality principles
1. Correctness before speed: behavior must be deterministic, testable, and reviewable.
2. Groundedness and safety by design: AI flows must be constrained, observable, and abuse-aware.
3. Operational excellence: logs, metrics, traces, and runbooks are required engineering outputs.
4. Separation of concerns: each module has one responsibility and explicit interface contracts.
5. Change traceability: every implementation change maps to a tracked issue/task with acceptance criteria.

## Definition of done baseline
A task is done only when all items below are satisfied:
1. Functional requirements implemented and peer-reviewable.
2. Unit tests and relevant integration tests added/updated and passing.
3. Failure paths and edge cases explicitly handled.
4. Docs and configuration examples updated in the same change.
5. Observability fields (request IDs, timings, errors) included where applicable.
6. Security and privacy considerations reviewed and documented.
7. CI quality checks pass without bypass.

## Code quality standards
1. Strong typing for public/internal service interfaces.
2. Configuration-driven behavior; avoid hardcoded environment assumptions.
3. Layered architecture compliance (API -> Service -> Repository -> Adapters).
4. Explicit error taxonomy and normalized user-facing errors.
5. Avoid hidden side effects and tightly coupled utility helpers.

## Testing standards
1. Unit tests cover normal paths, boundary conditions, and failure modes.
2. Integration tests cover cross-layer contracts and provider interactions.
3. Regression tests protect groundedness, citation correctness, and retrieval quality.
4. Tests must be deterministic and avoid flaky timing dependencies.

## Security and safety standards
1. Validate and sanitize all inputs at boundaries.
2. Enforce secret hygiene and avoid sensitive logging.
3. Apply least privilege for data access and operational endpoints.
4. Include prompt injection and abuse-path testing for AI workflows.

## Observability standards
1. Structured logs with correlation/request IDs.
2. Timing metrics for critical pipeline stages.
3. Actionable error events with stable codes and remediation hints.
4. Redaction policy for sensitive fields.

## Documentation standards
1. Architecture-impacting changes must update ADRs and/or architecture docs.
2. Operationally relevant changes must update runbooks/playbooks.
3. Public contracts must update API docs and examples.

## Review and governance
1. PR reviews must verify adherence to this charter.
2. Exceptions require documented rationale and explicit follow-up issue.
3. Charter changes require dedicated review and changelog entry.