---
title: Implementation and Code-Change Rules
generated_at: "2026-09-19T00:34:01Z"
references:
  - AGENTS.md
  - testing.rules.md
  - configuration.rules.md
  - naming.rules.md
  - security.rules.md
  - environments.rules.md
  - commits.rules.md
  - context.rules.md
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
tags: [coding, implementation, rules]
---

## Applicability

This file applies to new code, bug fixes, refactoring, API changes, configuration-backed code changes, generated-code interaction, dependency-driven edits, and scripts that function as software. It also carries the portable coding conventions—formatting precedence, whitespace, indentation, file hygiene, layout, naming, comments, imports, control flow, error handling, and tool protocol—that govern how such changes are written.

## Core rules

| ID | Requirement | Observable verification |
| --- | --- | --- |
| COD-001 | The agent MUST treat this file as the canonical owner for implementation-level code-change discipline. | The task rationale routes code-change questions here instead of spreading them across general policy. |
| COD-002 | The agent MUST inspect the relevant implementation path before editing, including callers, callees, interfaces, data flow, invariants, configuration, tests, error handling, side effects, and generated ownership where applicable. | The change rationale names the inspected paths and the evidence used to choose the fix. |
| COD-003 | The agent MUST prefer the smallest change that resolves the demonstrated problem, MUST avoid unrelated cleanup, speculative abstraction, opportunistic dependency upgrades, and broad formatting churn, and MUST preserve unrelated user changes. | The final diff is narrow and task-owned; unrelated user changes are preserved. |
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

`context.rules.md` CTX-001 through CTX-009 own the general sufficient-context requirement for file processing and changes; COD-002 is that rule's implementation-path specialization for code edits and does not restate it.

## Change-impact procedure

For every material change:

1. Identify the user-visible or operator-visible behavior being changed.
2. Trace inward to the owning source, configuration, data model, and dependencies.
3. Trace outward through direct and transitive callers, jobs, queues, caches, storage, interfaces, and consumers where applicable.
4. Identify compatibility, migration, security, performance, rollback, and observability effects.
5. Select validation that observes the changed behavior at the narrowest useful boundary and at least one live or realistic entry point when feasible.
6. Update code, schemas, configuration, tests, documentation, and runbooks only where the behavior or contract requires it.
7. Re-run affected checks after the final change.

Passing unit tests are a signal, not a complete change-impact analysis.

## Formatting and style precedence

Source formatting follows the strongest applicable convention, not a generic house style. Resolve style questions in this order:

1. Language syntax and semantic requirements.
2. The language specification or official style guidance where applicable.
3. Canonical formatter behavior for the ecosystem.
4. Repository-local formatter and linter configuration, including `.editorconfig` or equivalent.
5. The requirements in this file.
6. The established local style of the affected file.

Where two applicable rules conflict, preserve semantics first and follow the higher-authority requirement. Do not override canonical formatter output merely to satisfy generic aesthetic preferences, and do not impose one universal formatting convention where a language, formatter, specification, or established repository convention requires different behavior.

Formatting expectations SHOULD be machine-enforceable where practical: prefer formatter configuration, `.editorconfig`, language-native formatter settings, lint rules, pre-commit validation, or CI checks over prose-only requirements when the repository supports such mechanisms. This file defines expectations; it does not assert that corresponding automation exists or passes. These conventions are repository-portable: they name the repository root, the applicable formatter configuration, and the affected source file semantically rather than by fixed paths.

## Formatter and linter protocol

- Run the narrowest formatter applicable to the modified source; do not format unrelated files.
- Do not manually undo canonical formatter output without a documented reason.
- Formatter success is not proof of semantic correctness; a clean lint result is not proof of correct behavior.
- Address linter findings caused by the change when they are within task scope.
- Do not perform unrelated repository-wide remediation unless requested.
- Do not suppress a finding merely to make validation pass without understanding the underlying condition.

## Whitespace

The byte-level whitespace protocol is owned by `configuration.rules.md`; the conventions below are the source-editing specialization.

### Horizontal whitespace

- Prefer formatter-controlled spacing around operators, delimiters, keywords, declarations, and expressions.
- Do not use whitespace for visual alignment that canonical tooling would remove or destabilize, and do not use repeated spaces to simulate tables or columns in ordinary source.
- In Markdown, do not blindly strip an intentional CommonMark hard break; prefer an unambiguous alternative such as a trailing backslash or an explicit `<br>` where practical.

### Blank lines

- Use blank lines to separate logical units, not as decoration.
- Follow the language-specific formatter for spacing between declarations, types, functions, methods, imports, and major logical blocks.
- Do not insert blank lines that fragment tightly related statements without improving readability, and do not remove required or formatter-generated blank lines.

### Line endings and final newline

The canonical newline convention and final-newline requirement are owned by `configuration.rules.md`. For source editing:

- Do not introduce mixed line endings within a file.
- Preserve a required platform-specific or generated-file convention where repository evidence establishes one.
- Do not normalize line endings across unrelated files inside an otherwise scoped change.

## Indentation and tabs

### Default indentation

Unless a language, file format, formatter, generated artifact, or existing governing repository convention requires otherwise:

- Indent with spaces.
- Use one consistent indentation width per file type, selected by ecosystem or formatter convention; do not mandate one universal width across ecosystems with different canonical conventions.
- Never mix tabs and spaces for indentation within the same syntactic context.
- Never use tabs to align comments, assignments, tables, or arbitrary columns.

### Required tabs

Tabs are permitted or required only when one of the following applies:

1. The language or file format requires them.
2. The canonical formatter emits them.
3. An authoritative project-local configuration requires them.
4. Changing them would alter semantics.
5. The file is generated and must preserve generator output.

Do not convert required tabs into spaces. Known semantic cases include recipe command indentation in traditional Makefiles—required unless the file deliberately changes the recipe prefix—and Go source, which defers to `gofmt` including its indentation behavior.

### Mixed indentation

Mixed indentation that is not language-required or formatter-produced MUST be treated as a formatting defect.

- Correct mixed indentation in the lines or logical region being edited.
- Do not perform repository-wide whitespace rewrites unless the task explicitly calls for normalization.
- Preserve semantic whitespace.

### Display width versus storage

Distinguish the indentation characters stored in the file from the tab display width configured in an editor. Editor display width MUST NOT be treated as evidence that tab characters are permitted in source.

## File hygiene

Portable baseline, suitable for `.editorconfig` or equivalent tooling:

- Indentation style defined per language and file type rather than assumed globally where canonical conventions differ.

The byte-level encoding, line-ending, and whitespace protocol—including `UTF-8`, `LF`, and exactly one final newline—is owned by `configuration.rules.md`; this section states the source-editing baseline only and does not restate that protocol. Do not modify binary, generated, vendored, minified, lock, snapshot, fixture, or other machine-produced artifacts merely to satisfy generic source-formatting rules unless those artifacts are explicitly in scope.

## Generated and third-party content

Generated, vendored, externally mirrored, minified, and machine-maintained files MUST NOT be manually reformatted unless the generating process is also updated appropriately, repository policy explicitly permits the modification, or the task explicitly requires it. Prefer regenerating a generated file from its source over hand-editing the output. Generated-file ownership follows COD-008 and the generated-content rules in `configuration.rules.md`.

## Source layout

- Keep related code together and keep each unit focused on one coherent responsibility.
- Prefer shallow, readable control flow over avoidable nesting; use early returns or guard clauses where they improve clarity and fit language conventions.
- Avoid deeply nested conditional structures where a clearer decomposition exists, and avoid excessively long functions or methods when cohesive extraction improves comprehension.
- Do not apply arbitrary numeric limits on function, method, or file length without a repository-specific requirement, and do not split cohesive logic solely to satisfy a metric.
- Do not convert subjective design preferences into unconditional rules where context determines correctness.

## Naming

- Defer first to language and ecosystem naming standards; `naming.rules.md` governs filenames and repository-controlled identifiers.
- Use names that communicate role or intent; avoid cryptic abbreviations except conventional domain terms or very local, obvious variables.
- Do not encode type information redundantly into names unless an established ecosystem convention requires it.
- Keep terminology consistent with the domain model and public interfaces.
- Preserve externally defined names, serialized fields, API contracts, protocol identifiers, database schema names, and interoperability constraints.
- Do not rename public or externally observable identifiers solely for stylistic consistency.

## Comments and documentation

Write comments for what the code alone does not communicate: rationale, non-obvious constraints, invariants, safety assumptions, compatibility requirements, externally imposed behavior, and intentional deviations from expected patterns.

- Do not write comments that merely restate the code, and do not require comments for every declaration, variable, branch, or obvious operation.
- Update or remove a stale comment when the associated behavior changes.
- Public API documentation SHOULD follow the documentation convention of the language or framework when applicable.

## Imports and dependencies

- Use language-standard import/include ordering or the canonical formatter's behavior; do not maintain manual orderings that conflict with canonical tooling.
- Remove unused imports when safe.
- Avoid wildcard imports except where ecosystem conventions or framework behavior justify them.
- Keep dependency declarations minimal and explicit; do not introduce a dependency solely to perform a trivial operation already supported adequately by the standard library or existing project dependencies without a documented reason, per COD-009.

## Delimiters and expression style

- Do not impose a single cross-language brace or delimiter style; follow canonical language formatting.
- Use explicit grouping where it materially improves correctness or readability.
- Avoid clever compression that obscures control flow, and do not combine unrelated statements solely to reduce line count.
- Do not fight formatter output to enforce a preferred brace placement.

## Line length

No universal hard line-length limit applies unless repository policy defines one.

- Follow language and ecosystem conventions where established; readability is the primary objective.
- Wrap prose, expressions, signatures, and data structures using canonical formatter behavior where available.
- Permit justified exceptions for URLs, generated identifiers, serialized values, regular expressions, commands, tables, or content whose splitting would reduce clarity or alter semantics.
- Preserve an existing repository-specified numeric maximum unless a task explicitly reconsiders it.

## Control flow and expressions

- Prefer readable boolean expressions over unnecessarily clever formulations.
- Avoid assignments or hidden side effects inside conditions unless they are idiomatic and clear in the language.
- Keep error and exceptional paths explicit according to language norms rather than disguising them in conditionals.

## Error handling

- Propagate, handle, transform, or deliberately ignore each error with an explicit rationale; do not swallow failures silently or leave empty catch, except, or error handlers unless the ignored condition is intentional and documented.
- Give error messages useful context without exposing secrets or other sensitive data.
- Keep cleanup reliable on failure paths; pair resource acquisition with release using language-native mechanisms where available.
- Avoid broad exception capture unless the boundary genuinely requires it.
- Do not treat an error-handling pattern as universally safe independent of runtime and language semantics.

## Constants and magic values

- Give meaningful names to repeated or domain-significant constants; preserve literals where they are clearer than indirection.
- Do not replace every literal with a named constant mechanically.
- Include units in names or types where ambiguity would otherwise exist, and prefer typed representations for units, states, and constrained values where the language supports them and the cost is proportionate.

## Dead code and suppressions

- Remove unreachable or obsolete code instead of commenting it out; prior versions remain available from version control.
- Do not leave debug output, temporary instrumentation, placeholder branches, or abandoned feature flags without an explicit reason.
- Keep lint and compiler suppressions narrowly scoped and record a rationale for non-obvious suppressions.
- Do not disable an entire rule category to silence a local problem when a narrower correction exists.

## Change hygiene

- Minimize unrelated formatting churn and preserve surrounding style unless normalization is explicitly requested.
- Keep diffs reviewable; separate mechanical formatting from behavioral changes when practical.
- Avoid opportunistic renaming or restructuring outside task scope.
- Preserve public behavior unless behavioral modification is part of the requested task.

## Security-relevant practices

Baseline expectations consistent with secure coding practice; `security.rules.md` remains the governing security policy:

- Validate untrusted input at the appropriate trust boundary and prefer allow-list or structurally constrained validation where applicable.
- Use safe APIs and parameterized interfaces instead of constructing executable commands or queries through unsafe string concatenation.
- Do not embed credentials, secrets, private keys, access tokens, or environment-specific sensitive values in source.
- Apply least privilege appropriate to the execution context and fail in a controlled manner.
- Do not log secrets or unnecessary sensitive data; use language-appropriate resource management and secure temporary-file and filesystem patterns.
- Preserve output encoding or escaping appropriate to the destination context, and distinguish validation from sanitization and output encoding.
- Do not infer that clean formatting makes code secure; these rules do not establish compliance, certification, or complete security.

## Language-specific overrides

When this document's generic conventions conflict with a language specification, semantic file-format requirement, canonical formatter, or repository-approved language-specific rule, the language-specific requirement takes precedence unless a higher-authority repository requirement explicitly states otherwise.

Representative deferrals:

- Go: defer formatting to `gofmt`, including its tab and indentation behavior.
- Rust: defer formatting to `rustfmt` when the repository adopts it.
- Python: follow the repository-selected formatter and established Python conventions.
- C/C++: follow the repository `clang-format` configuration or documented project style when present.
- C#/.NET: follow `.editorconfig`, compiler and analyzer rules, and the configured formatter.
- JavaScript, TypeScript, CSS, JSON, and YAML: follow the repository-selected formatter and parser-valid syntax.
- Makefiles: preserve recipe-tab semantics.
- Markdown: preserve intentional CommonMark semantics, including hard-break whitespace.

These entries name deferral targets, not installed tools; do not assume a listed tool is available without repository evidence.

## Cross-references

- Governing agent contract and precedence: `AGENTS.md`
- Test selection, execution, interpretation, evidence, and regression-test integrity: `testing.rules.md`
- Placement, generated artifacts, and local versus portable configuration: `configuration.rules.md`
- Naming, file families, and generated-file markers: `naming.rules.md`
- Security-sensitive behavior: `security.rules.md`
- Runtime selection, shell policy, and environment isolation: `environments.rules.md`
- Commit preparation and commit-specific validation: `commits.rules.md`

## Lineage and migration

This file separates implementation discipline from the repository-wide ruleset so code-change ownership is explicit without duplicating general policy. It retains the change-impact intent previously distributed across older engineering guidance while making validation a dependency on `testing.rules.md` instead of a second owner. The change-impact procedure and the repository-wide minimal-change and preserve-unrelated-work requirements were absorbed from `general.rules.md` during the GEN migration. The formatting precedence, whitespace, indentation, file-hygiene, layout, naming, comment, import, control-flow, error-handling, constant, dead-code, change-hygiene, security-baseline, and language-override conventions were added later as portable, language-aware defaults that defer to canonical formatters and ecosystem standards rather than a universal house style.
