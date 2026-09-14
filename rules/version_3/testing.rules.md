---
title: Test and Validation Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: rules/version_3
references:
  - rules/version_3/AGENTS.md
tags: [testing, validation, rules]
---

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Test selection, execution, interpretation, and validation evidence |
| Rule namespace | `TST` |
| Change field | `policy_version: 3` |

## Applicability

This file applies to unit tests, integration tests, end-to-end tests, regression tests, contract tests, smoke tests, build validation, linting, formatting checks, type checking, static analysis, generated-code verification, and repository-specific validation tools.

## Core rules

| ID | Requirement | Observable verification |
| --- | --- | --- |
| TST-001 | The agent MUST treat this file as the canonical owner for test and validation execution discipline. | Test-selection and evidence questions route here instead of being spread across general policy. |
| TST-002 | The agent MUST discover repository-native test mechanisms before running validation, including manifests, build files, CI configuration, test configuration, scripts, task runners, framework discovery, and repository documentation. | The chosen command is grounded in repository evidence rather than invention. |
| TST-003 | The agent MUST preserve framework-native discovery and MUST NOT infer a repository-wide `*.test` filename convention unless a local framework or repository rule requires it. | Test selection follows the repository's discovered convention. |
| TST-004 | The agent SHOULD prefer the narrowest relevant test, then the affected file, module, package, or subsystem suite, and only then broader repository validation when risk or convention warrants it. | Validation scope is proportionate and explained. |
| TST-005 | For defects, the agent SHOULD add a regression test when the failure is reproducible, testable at an appropriate boundary, and stable and meaningful. | The fix is protected by a deterministic test when feasible. |
| TST-006 | The agent MUST classify validation commands by effective behavior and MUST not assume a command is safe solely because it is named `test`, `check`, or `build`. | The selected command is evaluated for its actual side effects. |
| TST-007 | The agent MUST validate the runtime environment before running environment-dependent tests and MUST follow `environments.rules.md` for environment discovery, selection, and isolation. | The command uses the intended runtime and does not pollute a broader environment. |
| TST-008 | The agent MUST treat tests that touch APIs, cloud services, databases, remote repositories, queues, or other external infrastructure as authority- and side-effect-sensitive. | Credentials, authorization, target identity, and production-versus-test scope are explicit. |
| TST-009 | The agent MUST NOT label a failure flaky merely because rerunning once passes. | Flakiness claims are backed by evidence such as prior repository notes, timing, concurrency, or repeated nondeterminism. |
| TST-010 | The agent MUST NOT skip, disable, xfail, quarantine, or weaken tests merely to obtain a green suite. | Any such change is independently justified by the intended behavior. |
| TST-011 | The agent SHOULD use mocks to isolate boundaries without manufacturing success. | Tests still validate meaningful behavior rather than only mocked success. |
| TST-012 | The agent SHOULD consider build, lint, formatter verification, type checking, schema validation, generated-code checks, and static analysis where repository conventions support them. | The checks cover the changed surface and the rationale records what ran. |
| TST-013 | When a test fails, the agent MUST distinguish pre-existing failures from change-induced failures where evidence permits and MUST inspect the actual failure before modifying tests. | The diagnosis identifies whether code, test, fixture, environment, or assumption is defective. |
| TST-014 | The agent MUST record validation evidence precisely, including the exact command, execution context when material, exit or result, relevant failed test names, whether the command completed, whether tests were skipped, and any limitations. | The final report uses `passed`, `failed`, `not run`, or `blocked` accurately. |
| TST-015 | The agent MUST treat validation as complete only when it is proportionate to task scope, behavioral impact, risk, repository conventions, and available runtime. | The final claim matches the actual checks that ran. |
| TST-016 | The agent MUST validate after mutation and MUST re-validate after correcting a surfaced failure. | Each relevant check has an observed result after the last affected change. |
| TST-017 | The agent MUST stop blind automated repair after three unsuccessful cycles for the same file and check, then diagnose the cause. | No unbounded formatting, lint, generation, or retry loop occurs. |

## Regression test integrity

Regression tests protect established behavior. A failing `PREEXISTING_TEST` is evidence against the recent code change or its causal implementation until the agent demonstrates otherwise.

### Protected preexisting tests

- The agent MUST inspect the failing assertion and the intended behavioral contract before changing anything.
- The agent MUST trace the recent code path that affects the failure and correct the codebase when the implementation violates the established behavior.
- The agent MUST rerun the original `PREEXISTING_TEST` unchanged after the corrective change.
- The agent MUST NOT modify a `PREEXISTING_TEST` merely because the implementation now returns a different result, a refactor changed internal behavior, or rewriting the test would be easier than fixing the implementation.

### Prohibited adaptation

- When a failure is a regression, the agent MUST NOT accommodate it by changing expected values, weakening assertions, deleting assertions, broadening accepted values, replacing exact assertions with weaker predicates, adding catches or suppression around failures, adding skips, ignores, `xfail`, or quarantine markers, deleting the test, regenerating snapshots or goldens, altering fixtures so broken behavior appears correct, increasing tolerances without independent justification, or changing mocks merely to reproduce the new broken implementation.
- A green suite obtained through those actions does not constitute regression remediation.

### When a preexisting test may change

- The agent MAY modify a `PREEXISTING_TEST` only when independent evidence shows the test is defective or an `AUTHORIZED_BEHAVIOR_CHANGE` exists.
- Acceptable evidence includes an explicit current user requirement, an authoritative specification, a confirmed product or API contract change, a defective fixture, an impossible or internally contradictory assertion, nondeterministic test logic, or repository history or governing documentation proving the expectation is obsolete.
- The recent code change by itself is not sufficient evidence.
- Before modifying the test, the agent MUST record why the old expectation is invalid, what governing evidence applies, why fixing the production code to satisfy it would be incorrect, and whether the change is a test correction or a behavior change.

### Newly added tests

- The agent MAY correct a `NEW_TEST` when the test itself is defective, incomplete, brittle, or mis-specified.
- The agent MUST NOT weaken a `NEW_TEST` merely to legitimize broken production behavior.
- When the new test accurately expresses the intended requirement, the agent MUST prefer fixing the implementation.
- Distinguish `NEW_TEST_DEFECT` from `IMPLEMENTATION_DEFECT`.

### Provenance and baselines

- The agent MUST determine whether a failing test is a `PREEXISTING_TEST`, `NEW_TEST`, or `UNKNOWN_PROVENANCE` before modifying it.
- The agent MUST treat `UNKNOWN_PROVENANCE` conservatively as `PREEXISTING_TEST` until evidence proves otherwise.
- Preexisting snapshots, golden files, approval outputs, serialized expected results, fixtures, and equivalent baseline artifacts are protected regression expectations.
- The agent MUST NOT refresh or overwrite those baselines automatically after a failure. Baseline updates require independent proof that the externally observable behavior changed with authorization.

### Regression failure workflow

1. Preserve the failing preexisting test unchanged.
2. Capture the actual failure.
3. Determine provenance.
4. Identify the intended behavioral contract.
5. Trace the recent code path affecting that contract.
6. Classify the issue as `IMPLEMENTATION_DEFECT`, `TEST_DEFECT`, `AUTHORIZED_BEHAVIOR_CHANGE`, `ENVIRONMENT_OR_FIXTURE_DEFECT`, or `UNKNOWN`.
7. If the issue is an `IMPLEMENTATION_DEFECT`, correct the codebase and rerun the unchanged preexisting test.
8. If the issue is a `TEST_DEFECT`, document the independent evidence and make the narrowest justified correction.
9. If the issue is an `AUTHORIZED_BEHAVIOR_CHANGE`, update only the superseded expectations and the implementation required for the new contract.
10. If the issue is an `ENVIRONMENT_OR_FIXTURE_DEFECT`, correct the causal setup without weakening valid assertions.
11. If the issue remains `UNKNOWN`, do not modify the protected test to force success.

### No test-laundering

- The agent MUST NOT use test edits to launder an implementation regression into apparent correctness.
- A failing protected test may not be "fixed" by changing the expected value from `A` to an unintended `B` unless independent evidence establishes that `B` is now the authorized contract.

### Semantic ownership

- This section is semantic Markdown policy.
- It cannot be replaced by Codex `prefix_rule(...)` because provenance, authority, and contract reasoning are required.

## Validation command policy

Validation commands are classified by effective behavior, not by their label.

- `ALLOW` when the command is read-only or non-destructive and the effective action is confined to observation.
- `PROMPT` when the command writes artifacts, updates snapshots, regenerates outputs, or mutates isolated state that the user could reasonably review before running.
- `PROMPT` when the target is explicit and the command mutates a database, filesystem, queue, or other shared state under the task's authority and rollback plan.
- `FORBID` when the command is destructive, privileged, targets unknown or production-like external systems, or performs deployment or remote mutation outside the task scope.
- Wrapped or indirect execution that obscures the effective command fails closed until the underlying action is known.
- A safe label does not make an unsafe command safe.

## Executable command guardrails

Future `.codex/rules/*.rules` may classify specific test, build, check, and validation prefixes, but only when repository-native manifests, scripts, or CI evidence identify safe exact forms. A command named `test`, `build`, or `check` is not automatically read-only; its effective behavior still decides whether this file's validation policy applies. CI/test semantics remain owned here.

## Additional guidance

- Test filenames remain under `naming.rules.md`; this file owns execution, interpretation, and evidence.
- When a validation command is also a code-change command, the code-change discipline in `coding.rules.md` still applies.
- Security-sensitive validation defers to `security.rules.md`; external-target and publication boundaries defer to `remotes.rules.md`.

## Validation and completion

A task is complete only when all applicable conditions hold:

- the intended artifact was created or modified;
- the artifact is reachable from the applicable entry point;
- relevant validation ran against the final state and passed;
- every surfaced task-caused failure was fixed and re-verified or remains explicitly open;
- affected contracts and documentation agree with implementation;
- unrelated paths remain unchanged;
- temporary artifacts are dispositioned;
- the final report distinguishes `PASS`, `FAIL`, `NOT PERFORMED`, and `<TBD>` accurately.

## Cross-references

- Governing agent contract and precedence: `AGENTS.md`
- Implementation changes that need validation: `coding.rules.md`
- Runtime selection, shell policy, and environment isolation: `environments.rules.md`
- File naming and test filename conventions: `naming.rules.md`
- Sensitive-data, privilege, and destructive-action boundaries: `security.rules.md`
- Commit preparation and staged-content checks: `commits.rules.md`
- Remote, publication, and external-action boundaries: `remotes.rules.md`

## Lineage and migration

This file centralizes test and validation execution behavior so it no longer has to be inferred from general repository policy. Post-mutation re-validation, blind-repair bounds, and task-completion criteria were absorbed from `general.rules.md` during the GEN migration. The universal `*.test` filename rule was intentionally replaced by framework-native discovery, and this file governs execution and evidence rather than filename syntax.
