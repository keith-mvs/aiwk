# Implementation and Code-Change Rules

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Implementation, code changes, and code-adjacent edits |
| Rule namespace | `COD` |
| Change field | `policy_version: 3` |

## Applicability

This file applies to new code, bug fixes, refactoring, API changes, configuration-backed code changes, generated-code interaction, dependency-driven edits, and scripts that function as software.

## Core rules

| ID | Requirement | Observable verification |
| --- | --- | --- |
| COD-001 | The agent MUST treat this file as the canonical owner for implementation-level code-change discipline. | The task rationale routes code-change questions here instead of spreading them across general policy. |
| COD-002 | The agent MUST inspect the relevant implementation path before editing, including callers, callees, interfaces, data flow, invariants, configuration, tests, error handling, side effects, and generated ownership where applicable. | The change rationale names the inspected paths and the evidence used to choose the fix. |
| COD-003 | The agent MUST prefer the smallest change that resolves the demonstrated problem and MUST avoid unrelated cleanup, speculative abstraction, opportunistic dependency upgrades, and broad formatting churn. | The final diff is narrow and task-owned. |
| COD-004 | The agent MUST preserve relevant behavioral contracts, including public APIs, internal interfaces, serialization formats, error contracts, persistence formats, command-line interfaces, configuration keys, environment variables, and compatibility expectations. | Any intentional contract break is explicitly identified and justified. |
| COD-005 | For defect remediation, the agent MUST identify the failing invariant or causal mechanism and fix the cause rather than merely suppressing the symptom. | The explanation distinguishes confirmed cause, likely cause, and unknown. |
| COD-006 | The agent MUST handle errors explicitly when failure modes are meaningful, preserve useful causal information, propagate safely, avoid silent swallowing, avoid false-success states, and avoid sensitive-data leakage. | Failure paths remain observable and do not discard diagnostic context. |
| COD-007 | The agent MUST account for state and side effects, including mutation, idempotency, transactions, partial failure, rollback or compensation where relevant, concurrency, retries, duplicate execution, and irreversible side effects. | The change rationale addresses side-effect behavior when it is material. |
| COD-008 | The agent MUST prefer the authoritative source over generated or vendored output and MUST respect generated-file ownership. | Generated outputs trace back to a declared source and generator. |
| COD-009 | The agent MUST require a demonstrated reason before adding, removing, upgrading, downgrading, or replacing dependencies. | Dependency changes cite compatibility, lockfile, transitive, runtime, and security implications when material. |
| COD-010 | The agent MUST respect existing configuration ownership and precedence and MUST not hard-code environment-specific values or silently change material defaults. | Configuration changes follow the owning layer and preserve precedence. |
| COD-011 | The agent MUST defer security-sensitive code decisions to `security.rules.md` and preserve authentication, authorization, secret boundaries, validation, TLS or certificate checks, and safe failure behavior. | Security-sensitive code changes remain bounded by the security policy. |
| COD-012 | The agent SHOULD add comments or documentation only for non-obvious invariants, constraints, compatibility behavior, unusual algorithms, or external contract assumptions. | Comments explain intent or constraints rather than restating code. |
| COD-013 | The agent MAY refactor only when intended behavior remains unchanged unless the behavioral change is explicit, validation is appropriate to the affected area, and the task scope does not expand silently. | The refactor is backed by evidence and scope remains bounded. |
| COD-014 | The agent MUST use repository-native language and framework conventions where they are observable. | The change follows the local convention or a clearly higher-priority repository rule. |
| COD-015 | The agent MUST treat completion as evidence-bound and MUST defer validation details to `testing.rules.md`. | The final report does not claim fixed, working, validated, passing, compatible, or performant without validation evidence. |

## Cross-references

- Broad repository behavior, source-of-truth direction, and completion criteria: `general.rules.md`
- Test selection, execution, interpretation, evidence, and regression-test integrity: `testing.rules.md`
- Placement, generated artifacts, and local versus portable configuration: `configuration.rules.md`
- Naming, file families, and generated-file markers: `naming.rules.md`
- Security-sensitive behavior: `security.rules.md`
- Runtime selection, shell policy, and environment isolation: `environments.rules.md`
- Commit preparation and commit-specific validation: `commits.rules.md`

## Lineage and migration

This file separates implementation discipline from the repository-wide ruleset so code-change ownership is explicit without duplicating general policy. It retains the change-impact intent previously distributed across older engineering guidance while making validation a dependency on `testing.rules.md` instead of a second owner.
