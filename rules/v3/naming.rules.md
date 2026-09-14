# Naming Rules

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Repository-controlled filenames, directories, identifiers, and versioned artifacts |
| Rule namespace | `NAM` |
| Change field | `policy_version: 3` |

## Formal filename model

Use this abstract component model when the ecosystem does not mandate a filename:

```text
[prefix][base][modifier][suffix][extension]
```

Render optional components with the repository's controlled separators; the default rendered grammar is:

```text
[prefix-]base[-modifier...][-suffix][.extension]
```

| Component | Required | Definition |
| --- | --- | --- |
| `prefix` | No | Scope, sequence, or category discriminator needed before the semantic identity |
| `base` | Yes | Stable semantic identity of the artifact |
| `modifier` | No; repeatable | Ordered variant information such as platform, audience, locale, version, or date |
| `suffix` | No | Artifact role or lifecycle state such as `schema`, `template`, `generated`, `backup`, or `tmp` |
| `extension` | As required | Standard media, language, or tool extension |

Do not force every component to appear. The shortest unambiguous name is preferred.

## Deterministic component order

When components are present, order them as follows:

1. Scope or sequence prefix.
2. Stable base identity.
3. Functional modifiers: subsystem, platform/runtime, audience, locale.
4. Compatibility/version modifier: `v3`, semantic version, API version, or schema version when the version must be in the filename.
5. Date modifier in `YYYY-MM-DD` only when the date is part of identity or retention policy.
6. Lifecycle/role suffix: `schema`, `template`, `example`, `generated`, `backup`, `tmp`.
7. Extension.

Examples:

```text
api-client-windows-v3-schema.json
incident-summary-2026-08-27-report.md
service-config-template.yaml
repository-rules-v3.zip
```

Avoid redundant markers such as `final`, `new`, `latest`, `copy`, repeated versions, or status words whose meaning is not controlled.

## General casing and separators

| Artifact | Default |
| --- | --- |
| Generic directories | `lowercase-kebab-case` |
| Generic Markdown and plain text | `lowercase-kebab-case` |
| Generic configuration/data filenames | `lowercase-kebab-case` unless the ecosystem mandates another form |
| Python modules/functions/variables | `snake_case` |
| Python classes/types | `PascalCase` |
| JavaScript/TypeScript variables/functions | `camelCase` |
| JavaScript/TypeScript classes/components/types | Repository/framework convention, commonly `PascalCase` |
| Constants | Language and repository convention |
| CLI commands and subcommands | `lowercase-kebab-case` unless the tool mandates another form |
| Environment variables | `UPPER_SNAKE_CASE` |
| Schema identifiers | Existing standard or `lowercase-kebab-case`; do not rename externally governed IDs |

Use ASCII hyphen-minus (`-`) as the generic filename separator. Do not mix spaces, underscores, hyphens, and dots in one naming family without an ecosystem reason.

## Required sentinel exceptions

Preserve conventional names exactly when tooling or community convention requires them, including:

```text
README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
CODEOWNERS
AGENTS.md
AGENTS.local.md
AGENTS.override.md
CLAUDE.md
```

Also preserve ecosystem-mandated names such as `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Dockerfile`, `.gitignore`, and `.editorconfig`.

## Filenames and directories

| ID | Requirement |
| --- | --- |
| NAM-001 | A name MUST describe the artifact's durable purpose, not the current editing state. |
| NAM-002 | Sibling artifacts in one family MUST use the same component order and separator convention. |
| NAM-003 | A rename MUST preserve or deliberately migrate every reference, import, link, build rule, manifest entry, and external contract. |
| NAM-004 | Do not rename a standardized or externally consumed file solely for stylistic consistency. |
| NAM-005 | Directory names MUST represent ownership or lifecycle boundaries, not vague buckets such as `misc`, `stuff`, or `new`. |
| NAM-006 | Generated names MUST be deterministic from controlled inputs when reproducibility matters. |

## Markdown and rule files

- Use lowercase kebab case for generic Markdown files.
- Preserve the mandatory v3 filenames exactly.
- Use ATX headings and stable heading text to avoid anchor churn.
- Do not encode a transient status or generation timestamp in a stable policy filename.
- Nested repository agent guidance remains `AGENTS.md`; do not invent variants unless the target platform documents them.

## Source code

- Follow the language formatter, compiler, linter, framework, and repository convention before this generic policy.
- Public identifiers SHOULD express domain meaning and remain stable across refactors.
- Avoid abbreviations unless they are standard in the domain.
- Use consistent singular/plural semantics for collections, resources, and commands.
- Do not encode implementation details in a public identifier when the abstraction is intended to outlive them.

## Tests and fixtures

- Follow the test framework's discovery convention; do not impose a universal `*.test` suffix. Test selection, execution, interpretation, and evidence live in `testing.rules.md`.
- Test names SHOULD describe behavior and condition, not implementation sequence.
- Regression tests SHOULD identify the failed behavior without embedding sensitive incident data.
- Fixture names SHOULD identify scenario, variant, and expected class when needed.
- Golden/snapshot files MUST follow framework convention and have an update/verification procedure.

Examples by convention, not universal mandate:

```text
test_router.py
router.test.ts
router.spec.ts
RouterTests.cs
fixtures/invalid-binding.json
```

## Configuration, schemas, and migrations

- Prefer the ecosystem's canonical config filename.
- Use `*.schema.json`, `*.schema.yaml`, or the repository's established schema convention.
- Migration names MUST use the framework's ordering identifier and a stable semantic description.
- Do not renumber or reuse a published migration or stable schema identifier.
- Keep environment modifiers controlled: for example, `app-config-development.yaml`, not `app-config-dev-new.yaml`, unless `dev` is the repository's established vocabulary.

## Generated files

- Mark generated ownership in a header, manifest, or repository-standard metadata when the format permits.
- Use a `generated` suffix only when needed to distinguish the file from its source; prefer a dedicated generated directory or manifest when that is the repository convention.
- Never add a misleading generated marker to hand-authored content.
- Do not hand-edit a generated artifact.

## Reports, logs, temporary files, and backups

| Class | Naming pattern | Tracking |
| --- | --- | --- |
| Durable report | `<topic>[-<date>]-report.<ext>` when date is part of identity | Conditional |
| Local log | `<component>-<YYYY-MM-DD>.log` or tool convention | Ignored |
| Temporary file | `<base>-tmp.<ext>` or tool-generated unique name inside a temp directory | Ignored and removed |
| Diagnostic dump | `<component>-<failure-class>-<date>.<ext>` in restricted local storage | Ignored |
| Backup | `<base>-backup-<YYYY-MM-DD>.<ext>` only when a real retention workflow requires it | Normally outside repository |
| Archive | `<base>[-vN].zip` or repository release convention | Conditional |

Do not create manual backup copies inside source control. Git history is not replaced by `file-old`, `file-copy`, or `file-backup` clutter.

## Archive files

- Use the repository release convention; otherwise use `<base>[-vN].zip`, `<base>[-vN].tar.gz`, or the ecosystem-standard extension.
- Keep the version marker before the archive extension and do not append uncontrolled status markers.
- Validate member paths and exclude caches, secrets, local state, and unrelated artifacts before release.
- Treat an archive as a derivative unless repository policy explicitly makes it authoritative.

## Versioned files

- Prefer internal version metadata and version control when only one active file should exist.
- Use side-by-side filename versions only when consumers require simultaneous versions or the task explicitly preserves lineage.
- For major lineage sets, use `name-v1.ext`, `name-v2.ext`, `name-v3.ext`.
- Use lowercase `v` followed by an integer for document-generation lineage unless the repository uses another controlled format.
- Do not combine version labels with uncontrolled status labels.

Valid:

```text
agent-rules-v1.zip
agent-rules-v2.zip
agent-rules-v3.zip
```

Invalid:

```text
agent-rules-final-final-v2-new.zip
agent_rules-v3-latest-copy.zip
```

## Dates and timestamps

- Use `YYYY-MM-DD` for human-readable date identity.
- Use an ISO 8601 UTC timestamp only where sub-day ordering is required and the target format permits it.
- Do not add timestamps to stable cache-sensitive policy content, generated reproducibility inputs, or filenames that represent a single current artifact.

## Renaming procedure

1. Identify all references, imports, links, manifests, build rules, external consumers, and case-sensitive filesystem effects.
2. Define the new canonical name and compatibility/redirect strategy.
3. Perform a case-safe rename when the filesystem is case-insensitive.
4. Update references atomically with the rename.
5. Run link, import, build, packaging, and relevant behavior checks.
6. Verify the old name is absent except in intentional migration history.

## Lineage and migration

This file retains the naming rules from `v1/naming.md` and `v2/repo.md`, including lowercase kebab case, language idioms, sentinel exceptions, and generated-file ownership. The universal `*.test` rule was replaced with framework-native test discovery. Test execution, interpretation, and evidence live in `testing.rules.md`, with `AGENTS.md` routing to it.
