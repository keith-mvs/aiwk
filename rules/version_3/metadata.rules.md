---
title: Metadata and Frontmatter Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: rules/version_3
references:
  - rules/version_3/AGENTS.md
tags: [metadata, frontmatter, rules]
---

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Metadata and frontmatter policy for durable repository artifacts |
| Rule namespace | `MET` |
| Change field | `policy_version: 3` |

Metadata policy for generated and agent-touched durable artifacts. Require lean, machine-readable metadata on every newly generated durable artifact and on every existing durable file an agent touches when that file lacks required metadata. Do not alter underlying protocols, behavioral semantics, requirement strength, precedence, state transitions, defaults, interfaces, or execution behavior merely to add or normalize metadata.

## Required metadata

Markdown durable artifacts carry YAML frontmatter as the first content in the file unless a higher-authority format, parser, executable requirement, or repository convention prohibits it.

Minimum required fields:

| Field | Requirement |
| --- | --- |
| `title` | Concise, stable artifact title |
| `generated_at` | ISO-8601 timestamp or repository-approved deterministic equivalent |
| `references` | YAML array of authoritative repository-relative references; `[]` when none |

Additional fields are permitted only when they provide concrete machine-consumable value. Prefer established repository vocabulary and schemas over introducing new fields. Do not add decorative, narrative, redundant, inferable, speculative, or unused metadata.

## Formatting

- The frontmatter block is `---`, fields, `---`, exactly one blank line, then document content.
- Use lowercase `snake_case` keys unless a governing schema requires otherwise.
- Keep stable key names and deterministic ordering.
- Use ISO-8601 timestamps when timestamps are required.
- Use repository-relative references when possible.
- Use YAML arrays for zero-to-many values and explicit `[]` rather than prose such as `none`.
- Prefer concise scalar values over descriptive paragraphs.
- Do not duplicate metadata values in the body unless the body requires them for human comprehension or protocol semantics.

## Non-Markdown artifacts

Do not inject YAML frontmatter into formats where it would invalidate syntax, execution, parsing, schemas, signatures, generated ownership, or protocol behavior.

For a touched non-Markdown file without an established metadata mechanism:

1. Discover whether the format or repository defines a native metadata/header mechanism.
2. Use that mechanism only when semantically safe and repository-compatible.
3. If no safe mechanism exists, do not modify the file solely to force metadata.
4. Record the exception through the repository's metadata manifest or index mechanism when one exists.
5. When metadata enforcement is mandatory but no safe representation exists, mark the artifact `UNKNOWN` and fail closed.

## Agent enforcement

Before creating or modifying any durable artifact:

| ID | Requirement |
| --- | --- |
| MET-001 | Discover governing `AGENTS.md`, rules, schemas, generators, templates, and artifact-specific metadata conventions within scope. |
| MET-002 | Determine whether the artifact already contains valid metadata and preserve valid existing metadata unless normalization is required by a governing rule. |
| MET-003 | Add the minimum required metadata when the artifact is being touched and lacks it; preserve artifact semantics while inserting. |
| MET-004 | Update `references` only from verified repository relationships. |
| MET-005 | Validate metadata syntax, required fields, and unchanged protocol or executable semantics after modification. |

A file touch does not authorize unrelated cleanup or metadata expansion.

## Generated artifacts

- Agents generating durable artifacts MUST emit compliant metadata at creation time rather than relying on later remediation.
- Templates and generators SHOULD encode the minimum metadata contract directly when compatible with their owning format and generation pipeline.
- Generated-file ownership takes precedence: modify the authoritative generator or template rather than repeatedly editing generated outputs when repository evidence identifies an owning source.

## Existing files

- When an agent performs an otherwise-authorized modification to a durable file lacking metadata, metadata incorporation is part of that same bounded mutation.
- Do not perform repository-wide metadata backfills merely because this rule is discovered unless the active task explicitly authorizes that scope.
- Do not rewrite otherwise untouched files solely to satisfy this policy without explicit authorization.

## References usage

`references` exposes machine-traversable relationships. Include only verified, materially relevant references: governing rules, canonical specifications, owning schemas, source-of-truth artifacts, generators or templates, and directly required dependencies.

- Prefer canonical repository-relative paths.
- Do not use `references` as a bibliography, exhaustive dependency graph, backlink collection, or speculative relationship list.
- Deduplicate references and keep ordering deterministic.

## Value-added test

A metadata field is justified only when a concrete consumer or repository operation can use it for discoverability, archiving, indexing, manifesting, grep/search, provenance, ownership, dependency traversal, lifecycle management, validation, or deterministic automation. If no concrete value exists, omit the field.

Minimize field count, repeated text, verbose descriptions, duplicated path information, natural-language metadata, and values derivable cheaply from canonical repository state. Do not minimize so aggressively that required provenance, references, validation, or discovery information is lost.

## Protocol-preservation invariant

Metadata work MUST NOT change:

- normative requirements or MUST/SHOULD/MAY strength;
- authority or precedence;
- protocol states or transitions;
- trigger conditions;
- inputs, outputs, interfaces, or schemas;
- defaults or failure behavior;
- security boundaries;
- validation obligations;
- compatibility semantics.

When metadata insertion conflicts with any of these, preserve the original artifact and report the conflict. Deduplication is permitted only when semantic equivalence and canonical ownership are established from repository evidence.

## Validation

Validate each affected artifact where applicable:

| Check | Requirement |
| --- | --- |
| `metadata_present` | Required metadata exists |
| `metadata_parseable` | Metadata parses under the governing format |
| `required_fields` | `title`, `generated_at`, and `references` are present |
| `format_boundary` | Closing `---` is followed by exactly one blank line |
| `references_valid` | Listed references resolve or are explicitly marked `UNKNOWN` |
| `schema_compatible` | Governing metadata schema is satisfied when one exists |
| `artifact_valid` | Original artifact format remains parseable and usable |
| `protocol_preserved` | No underlying protocol semantics were intentionally changed |
| `generator_consistent` | Generated artifacts remain aligned with their authoritative generator or template |

Do not report a validation as passed without returned inspection or deterministic validation evidence.

## Evidence states

Use only `OBSERVED`, `VERIFIED`, `DERIVED`, `INFERRED`, `UNKNOWN`, and `NOT PERFORMED`. Inference is not evidence.

## Cross-references

- Contract and routing index: `AGENTS.md`
- Artifact placement, ownership, and portability: `configuration.rules.md`
- File and directory naming: `naming.rules.md`
- Temporary and durable artifact policy: `configuration.rules.md`

## Lineage and migration

New in v3. Establishes a single metadata and frontmatter contract for generated and agent-touched durable artifacts, aligned with the frontmatter already carried by `AGENTS.md` and `AGENTS.local.md`.
