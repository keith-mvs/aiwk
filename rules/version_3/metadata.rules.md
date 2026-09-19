---
title: Metadata and Frontmatter Rules
generated_at: "2026-09-19T00:03:11Z"
references:
  - AGENTS.md
  - configuration.rules.md
  - naming.rules.md
  - prompts/manifest.yaml
  - tools/policy_check.py
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
tags: [metadata, frontmatter, rules]
---

Canonical policy for metadata generation, representation, validation, and serialization on durable repository artifacts. This file is the single canonical owner of the metadata contract; `configuration.rules.md` explicitly defers frontmatter block structure to this file, and domain schemas such as `prompts/manifest.yaml` hold only the delegated vocabularies named below. No other file may define metadata policy without an explicit canonical-reference relationship to this file.

The contract is optimized simultaneously for human readability, machine readability, deterministic parsing, field discoverability, semantic disambiguation, stable typing, canonical serialization, validation, interoperability, and reproducibility. Do not introduce multiple fields that encode the same semantic fact.

## Scope and authority

- Applies to every newly generated durable artifact and to every existing durable file an agent touches when that file lacks required metadata.
- Do not alter underlying protocols, behavioral semantics, requirement strength, precedence, state transitions, defaults, interfaces, or execution behavior merely to add or normalize metadata.
- A governing domain schema (for example `prompts/manifest.yaml` for the prompt corpus) MAY narrow a field's vocabulary or required set for its own artifact class; it MUST NOT weaken the naming, typing, timestamp, uniqueness, or failure-behavior rules defined here.

## Metadata location and carrier

- Markdown durable artifacts carry one YAML frontmatter block as the first content in the file unless a higher-authority format, parser, executable requirement, or repository convention prohibits it.
- The block is: opening `---` on the first line, YAML mapping fields, closing `---`, exactly one blank line, then document content. No other delimiter or location carries metadata for these artifacts.
- The serialization format is YAML 1.2 with JSON-schema-compatible typing. Consumers MUST NOT need natural-language inference to determine field boundaries or types.

### Non-Markdown artifacts

Do not inject YAML frontmatter into formats where it would invalidate syntax, execution, parsing, schemas, signatures, generated ownership, or protocol behavior.

For a touched non-Markdown file without an established metadata mechanism:

1. Discover whether the format or repository defines a native metadata/header mechanism.
2. Use that mechanism only when semantically safe and repository-compatible.
3. If no safe mechanism exists, do not modify the file solely to force metadata.
4. Record the exception through the repository's metadata manifest or index mechanism when one exists.
5. When metadata enforcement is mandatory but no safe representation exists, mark the artifact `UNKNOWN` and fail closed.

## Field model

### Field-selection rule

Every metadata field MUST satisfy all of the following:

- it represents one distinct semantic property;
- its meaning is not already represented by another field;
- its value has a stable declared type;
- its presence serves a concrete parsing, routing, provenance, validation, governance, or discovery function;
- its name can be understood without relying on surrounding prose.

Do not add fields merely because they may be useful later.

### Field naming

Field names MUST:

- match `^[a-z][a-z0-9_]*$`: lowercase `snake_case`, ASCII only;
- be semantically precise;
- avoid abbreviations unless standardized by the governing domain;
- use singular names for scalar values and plural names for arrays or collections;
- remain stable once published unless a versioned migration is defined.

Canonical examples: `generated_at`, `authority_level`, `requires_validation`, `references`.

Prohibited examples: `genAt`, `authLvl`, `refs_list`, `misc`, `data`, `info`.

### Type discipline

Each field has exactly one declared value type from: `string`, `integer`, `number`, `boolean`, `null` (only where explicitly permitted), `array`, `object`.

Do not overload a field so the same semantic field alternates between scalar, object, and array representations. Example: `references` is declared `array`; `references: []` and `references: ["source-a", "source-b"]` are valid; `references: "source-a"` is invalid.

## Canonical field order

Metadata fields MUST be emitted in the following total order. Fields not present are skipped; the relative order of present fields is invariant.

1. `id`
2. `title`
3. `generated_at`
4. `references`
5. `category`
6. `purpose`
7. `authority_level`
8. `requires_validation`
9. `mutates_repository`
10. `policy_version`
11. `status`
12. `scope`
13. `rules_root`
14. `tracking`
15. `tags`
16. `stage`
17. `inputs`
18. `outputs`
19. `composes_with`

Positions 1-9 are the base contract; positions 10-19 are repository-defined extensions appended in this documented order. New fields defined in the future are appended after position 19 in the order this file publishes them.

Two conformance levels apply:

- `schema_valid`: the block parses and satisfies every invariant in "Validation invariants". Field order is not a schema-validity condition.
- `canonical`: `schema_valid` plus canonical field order and canonical scalar/array formatting defined in "Serialization rules".

Generators and serializers MUST emit canonical form. A schema-valid but non-canonically ordered block is normalized by re-serialization, not by silent repair during validation; normalizing order inside a touched file is a permitted bounded metadata normalization.

## Field definitions

The following table is the complete closed field vocabulary for defined profiles. Every field resolves to exactly one definition here; referential clarity requires no second definition elsewhere. Cardinality is conveyed by type and required status: a scalar field carries exactly one value when present; an array field carries zero or more elements, with `[]` expressing the intentionally empty collection.

| Field | Type | Required | Allowed values / constraints | Null | Default | Validation rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | prompt profile | Dotted slug `^[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+$` unique within its domain; UUID form only where a domain schema declares it | no | none | Pattern match; uniqueness within domain index; UUID form additionally validated per "Identifiers" |
| `title` | string | always | Non-empty concise declarative artifact title | no | none | Present, non-empty string |
| `generated_at` | string | core profile | ISO 8601 datetime with explicit offset; canonical regex below | no | none | Parses as ISO 8601; offset explicit; date-only and naive forms invalid |
| `references` | array of string | core profile | Resolvable repository references or declared `<TBD>` entries; `[]` for none; no duplicates | no | none | Each element resolves or is a permitted non-path entry |
| `category` | string | prompt profile | Domain-declared closed vocabulary; prompt corpus: the artifact's top-level corpus directory name | no | none | Value in declared vocabulary; prompt corpus: equals containing directory |
| `purpose` | string | prompt profile | One declarative sentence describing artifact function | no | none | Non-empty string |
| `authority_level` | string | prompt profile | Domain-declared closed vocabulary; prompt corpus: `prompts/manifest.yaml` `authority_levels` | no | none | Value in declared vocabulary; consistency invariant with `mutates_repository` |
| `requires_validation` | boolean | prompt profile | `true` or `false` | no | none | Native boolean |
| `mutates_repository` | boolean | prompt profile | `true` or `false`; derived value per "Semantic uniqueness" | no | none | Native boolean; equals `authority_level != "read-only"` when `authority_level` present |
| `policy_version` | integer | optional | Integer `>= 1`; the policy generation the artifact follows | no | none | Integer type; `>= 1` |
| `status` | string | optional | `{active, final, frozen, historical}` | no | none | Value in enumeration |
| `scope` | string | optional | `{repository, machine-worktree, task-data}` | no | none | Value in enumeration |
| `rules_root` | string | optional | Path to governing rules directory relative to the artifact's directory; `.` when co-located | no | none | Non-empty string resolving to the rules directory when verifiable |
| `tracking` | string | optional | `{tracked, untracked}` | no | none | Value in enumeration |
| `tags` | array of string | optional | Lowercase discovery labels; `[]` for none; no duplicates | no | `[]` | Array of strings |
| `stage` | array of string | prompt profile | Elements from `prompts/manifest.yaml` `stage_vocabulary`; ordered; first element is the dominant routing stage; no duplicates | no | none | Non-empty array; each element in vocabulary |
| `inputs` | array of string | prompt profile | `snake_case` contract tokens `^[a-z][a-z0-9_]*$`; `[]` for none | no | none | Array of strings matching pattern |
| `outputs` | array of string | prompt profile | `snake_case` contract tokens `^[a-z][a-z0-9_]*$`; `[]` for none | no | none | Array of strings matching pattern |
| `composes_with` | array of string | optional | `id` values of other indexed prompts; `[]` for none; no duplicates | no | `[]` | Each element resolves to an indexed prompt id |

### Field semantics

- `id`: machine identifier used as the domain's routing and reference key (for example `repo.validate-change`). Where a domain declares UUID form, canonical lowercase UUID textual representation `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` is required; where UUIDv4 is required, validation MUST check both UUID syntax and version `4` (the version nibble at position 15). A UUID-looking string is not validated by length alone.
- `title`: human-facing artifact name. Distinct from `id`: `id` identifies, `title` names.
- `generated_at`: the instant at which the current artifact revision was generated. It is a generation timestamp, not a modification timestamp; metadata-only normalization does not advance it, and modification history belongs to version control, not to metadata.
- `references`: machine-traversable authoritative relationships — governing rules, canonical specifications, owning schemas, source-of-truth artifacts, generators or templates, and directly required dependencies. Element resolution: repository-root-relative, with artifact-directory-relative resolution for sibling names; an element matching both resolves sibling-first and is ambiguous. Non-path entries are limited to `<TBD>` declared-unresolved markers and documented external identifiers required by the domain. Not a bibliography, exhaustive dependency graph, backlink collection, or speculative relationship list. Order is preserved as declared; the governing contract SHOULD be listed first when one exists, and consumers MUST NOT infer further precedence from position.
- `category`: the artifact's primary governed classification. Distinct from `tags`: `category` is one closed-vocabulary value; `tags` are open discovery labels.
- `purpose`: the artifact's function as a single declarative sentence. Distinct from `title`: `title` names the artifact; `purpose` states what it does.
- `authority_level`: the maximum mutation authority boundary the artifact's procedure operates under, using the governing domain's declared vocabulary. For the prompt corpus the vocabulary is `prompts/manifest.yaml` `authority_levels`: `{read-only, bounded-mutation, local-git-mutation, remote-mutation}`.
- `requires_validation`: whether the artifact's procedure requires returned validation evidence before completion may be claimed.
- `mutates_repository`: whether the artifact's execution may alter local repository state (working-tree content or `.git` refs/objects). See "Semantic uniqueness" for its declared derivation.
- `policy_version`: the policy generation the artifact follows (currently `3` for the `rules/version_3/` corpus).
- `status`: artifact lifecycle state — `active` (current, maintained, authoritative), `frozen` (immutable; further change prohibited), `final` (completed terminal record), `historical` (retained for reference; superseded or inactive).
- `scope`: the breadth the artifact's content governs — `repository` (repository-wide), `machine-worktree` (machine- or worktree-local facts), `task-data` (bounded task records, non-governing).
- `rules_root`: locates the governing rules directory from the artifact; `.` means the artifact's own directory is the rules root.
- `tracking`: expected version-control tracking state — `tracked` (committed/distributed) or `untracked` (intentionally local-only).
- `stage`: ordered span of workflow stages the artifact covers; first element is the dominant routing stage.
- `inputs` / `outputs`: declared contract tokens the artifact consumes or produces.
- `composes_with`: peer prompt `id` values forming declared composition chains. Distinct from `references`: `composes_with` links composable prompt peers; `references` links governing or source artifacts.

### Profiles

A metadata block is validated against the profile its artifact class selects:

| Profile | Selected by | Required fields | Optional fields |
| --- | --- | --- | --- |
| `core` | Durable Markdown artifacts (`.md`) not claimed by a narrower profile | `title`, `generated_at`, `references` | Any other defined field whose presence satisfies the field-selection rule |
| `prompt` | `*.prompt` files indexed by `prompts/manifest.yaml` | `id`, `title`, `category`, `stage`, `purpose`, `inputs`, `outputs`, `authority_level`, `requires_validation`, `mutates_repository` | `composes_with` (`[]` permitted), `generated_at`, `references`, `status`, `scope`, `tracking`, `tags` |

The schema is closed per profile: a field outside the defined vocabulary fails validation unless a governing domain schema declares it for that artifact class. Domain schemas declaring additional fields MUST meet every field-selection rule above and register the field here by canonical reference.

## Value domains

### Enumerations

Fields with a closed vocabulary MUST use an explicit enumeration with one canonical spelling and case. Unbounded synonyms are prohibited: `high`, `highest`, `system-level`, and `SYSTEM` are not interchangeable with a canonical `system` value. The closed vocabularies defined by this file are `status`, `scope`, `tracking` (above) and, for the prompt domain, `authority_level`, `category`, and `stage` element values delegated to `prompts/manifest.yaml`. An enumeration is extended only by revising this file or the owning domain schema.

### Booleans

Boolean concepts serialize as native YAML booleans `true` and `false` only. `yes`, `no`, `on`, `off`, `enabled`, `disabled`, `1`, and `0` are prohibited as boolean representations unless an external schema explicitly requires them, and they are prohibited as unquoted scalars generally because YAML 1.1 parsers coerce them.

### Arrays

Arrays MUST contain values of the declared element type, use `[]` for an intentionally empty collection, preserve ordering only where ordering has defined semantics (`stage`, `references`), and avoid duplicate elements unless duplication itself carries meaning. Where order is not semantically meaningful (`tags`, `inputs`, `outputs`, `composes_with`), consumers MUST NOT infer precedence from position and canonical serialization emits lexicographic order.

### Timestamps

`generated_at` is the only canonical generated-timestamp field. `generate_at`, `generated`, `generation_time`, and `created_at` are prohibited as aliases for the same fact unless an external governing schema explicitly requires one under the alias rules below.

`generated_at` MUST contain an ISO 8601 datetime with an explicit UTC offset:

- Canonical form: `YYYY-MM-DDTHH:MM:SS±HH:MM`; UTC MAY serialize as `YYYY-MM-DDTHH:MM:SSZ`.
- Canonical regex: `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$`.
- The value MUST be a real calendar datetime with offset magnitude within `14:00`.
- Date-only values and naive datetimes without an offset are invalid.

### Absent, null, TBD, and empty values

The four states are distinct and MUST NOT be used interchangeably:

| State | Meaning |
| --- | --- |
| Field absent | The property does not apply or is not part of the artifact's profile |
| `null` | Explicitly unknown or unavailable, only where the field definition permits null (no defined field currently permits null) |
| `<TBD>` | Unresolved value requiring later resolution, only where the field definition permits that literal (`references` non-path entries; elsewhere only where a governing schema declares it) |
| `""` | Valid only when empty text has defined meaning (no defined field assigns meaning to the empty string) |

## Semantic uniqueness and derived fields

For any two fields `f1` and `f2`: if both encode the same semantic proposition, they MUST NOT coexist as independently authoritative fields. Formally: `meaning(f1) = meaning(f2)` implies `canonicalize(f1, f2)` yields one canonical field, unless an external compatibility requirement mandates both.

If compatibility aliases are unavoidable:

- designate exactly one canonical field;
- identify aliases explicitly;
- define precedence, deprecation behavior, and migration behavior.

Declared derived fields in this contract:

- `mutates_repository` is a derived projection of `authority_level`: `mutates_repository == (authority_level != "read-only")`. `authority_level` is the canonical authority field; `mutates_repository` exists as the declared binary predicate for safety gating and routing. When both are present, a value violating the derivation is a consistency failure, not a choice between authorities.
- `prompts/manifest.yaml` is a derived index of the prompt corpus: per-prompt `id`, `category`, `stage` (the frontmatter array's first element), and `authority_level` duplicate frontmatter facts. Frontmatter is canonical; on conflict the frontmatter value wins and the manifest MUST be regenerated or corrected, never edited into divergence.

Prohibited duplicate encodings: `created_at`, `updated_at`, `modified_at`, or any second timestamp field overlapping `generated_at` semantics; a free-text `flags`-style field packing multiple declared booleans; parallel relation lists duplicating `references` or `composes_with` semantics.

## Serialization rules

Canonical YAML serialization of a metadata block MUST satisfy:

- YAML 1.2-compatible values; JSON-schema typing (`true`/`false`, `null`, integers, numbers, strings).
- Duplicate keys are prohibited and MUST be rejected at parse time.
- Anchors, aliases, merge keys, tags/directives, and multiple YAML documents are prohibited inside the metadata block.
- Keys match `^[a-z][a-z0-9_]*$`; no tabs anywhere in the block.
- Ambiguous scalars MUST be double-quoted: `generated_at` is emitted as a quoted string (for example `generated_at: "2026-09-19T00:03:11Z"`) so heterogeneous parsers cannot coerce it to a timestamp object; `<TBD>` markers containing a colon-space sequence (for example `<TBD: reason>`) MUST be quoted; strings resembling booleans, nulls, or numbers MUST be quoted when string type is intended.
- Use native arrays and objects rather than delimiter-packed strings; positional tuples, overloaded delimiters, and compressed multi-property strings are prohibited.
- Comments MAY appear for human readers but carry no semantics and are not part of canonical form.
- Array style is not semantically meaningful: the prompt profile emits flow style for `stage`, `inputs`, `outputs`, `composes_with`; `references` emit block style and `tags` flow style, matching established corpus convention.

## Validation invariants

Every accepted metadata block MUST satisfy:

1. Uniqueness — no two canonical fields encode the same semantic property, and declared derivations hold.
2. Type consistency — for every field `f`: `value(f)` is a member of `declared_type(f)`.
3. Enumeration closure — for every enum field `f`: `value(f)` is a member of `allowed_values(f)` per the owning vocabulary.
4. Required-field completeness — for every field `f` required by the artifact's profile: `present(f) = true`.
5. Timestamp validity — `generated_at` parses as ISO 8601 and carries an explicit timezone offset.
6. Referential clarity — every field name resolves to exactly one definition in this file (or a domain schema it delegates to).
7. Deterministic interpretation — conforming parsers derive the same field/value structure from the same serialized block; no inference from prose is required.

## Validation procedure

Before accepting any metadata block:

1. Parse using the declared serialization format; reject duplicate keys, anchors/aliases, tabs, and unterminated blocks.
2. Validate required fields for the artifact's profile.
3. Validate field names against the closed vocabulary or the governing domain schema.
4. Validate declared types.
5. Validate enumerations against their owning vocabularies.
6. Validate cardinality and structural constraints (array element types, uniqueness, string patterns).
7. Validate `generated_at` as ISO 8601 with explicit offset.
8. Validate identifiers against their declared format, including UUID syntax plus version where required.
9. Reject unknown fields under the closed-schema rule; process declared domain extensions only per "Profiles".
10. Verify no two fields encode conflicting values for the same semantic property, including the `mutates_repository` derivation and manifest/frontmatter consistency.
11. Serialize into canonical field order for canonical comparison or emission.
12. Report PASS, or precise validation failures with field, violated rule, and observed value. Distinguish `schema_valid` from `canonical` in reports.

The repository's deterministic subset validator is `tools/policy_check.py` (frontmatter presence, parseability, required fields per profile, format boundary, `references` resolution, manifest coverage). It implements a subset of this contract; checks it does not implement remain obligations of the reviewing agent.

## Failure behavior

Metadata MUST fail closed when:

- a required field is absent;
- a field has the wrong type;
- duplicate keys exist;
- an enum value is outside its declared vocabulary;
- `generated_at` lacks a valid ISO 8601 datetime or an explicit timezone offset;
- conflicting aliases or derived fields supply different values for the same semantic property;
- semantic interpretation is ambiguous.

Do not silently repair a value during validation. The only normalization this file defines is canonical re-serialization (field order, ordering-insensitive array sort, canonical scalar quoting) applied when emitting or normalizing a block — never applied silently to accept an invalid value.

## Examples

Canonical valid prompt-profile block:

```yaml
---
id: repo.validate-change
title: Validate Change
category: testing
purpose: Select and execute proportionate repository-native checks against the final changed state.
authority_level: read-only
requires_validation: true
mutates_repository: false
stage: [validate, discover, inspect, report]
inputs: [acceptance_criteria, change_set]
outputs: [validation_report]
composes_with: [repo.create-commit, repo.implement-change, repo.refactor-code, repo.remediate-defect]
---
```

Canonical valid core-profile block:

```yaml
---
title: Example Durable Report
generated_at: "2026-09-19T00:03:11Z"
references:
  - rules/version_3/metadata.rules.md
policy_version: 3
status: final
scope: task-data
tracking: tracked
tags: [example]
---
```

Invalid blocks and expected failures:

```yaml
generated_at: 2026-09-18
```

- `generated_at_format`: date-only value; explicit time and offset required.

```yaml
generated_at: "2026-09-18T17:52:00"
```

- `generated_at_format`: naive datetime; explicit offset required.

```yaml
authority_level: read_only
```

- `enum_violation`: `read_only` is outside `authority_levels`; canonical spelling is `read-only`.

```yaml
mutates_repository: "yes"
```

- `type_violation`: boolean field carrying a string; also a prohibited YAML 1.1 boolean literal.

```yaml
mutates_repository: true
authority_level: read-only
```

- `derivation_conflict`: `mutates_repository` must equal `authority_level != "read-only"`.

```yaml
references: "AGENTS.md"
```

- `type_violation`: `references` is declared `array`, not scalar.

## Agent enforcement

Before creating or modifying any durable artifact:

| ID | Requirement |
| --- | --- |
| MET-001 | Discover governing `AGENTS.md`, rules, schemas, generators, templates, and artifact-specific metadata conventions within scope. |
| MET-002 | Determine whether the artifact already contains valid metadata and preserve valid existing metadata unless normalization is required by a governing rule. |
| MET-003 | Add the minimum required metadata for the artifact's profile when the artifact is being touched and lacks it; preserve artifact semantics while inserting. |
| MET-004 | Update `references` only from verified repository relationships. |
| MET-005 | Validate metadata syntax, required fields, and unchanged protocol or executable semantics after modification. |
| MET-006 | Emit fields in canonical order with declared types, canonical enum spellings, native booleans, and a quoted offset-aware `generated_at`. |
| MET-007 | Keep absent, `null`, `<TBD>`, and empty-string states distinct; never substitute one for another. |
| MET-008 | On conflicting aliases or duplicate semantic fields, canonicalize per "Semantic uniqueness"; fail closed when the conflict cannot be resolved from governing evidence. |
| MET-009 | Run `tools/policy_check.py` where applicable and treat its findings plus the invariants here as the acceptance floor, not the ceiling. |

A file touch does not authorize unrelated cleanup or metadata expansion.

## Generated artifacts

- Agents generating durable artifacts MUST emit compliant canonical metadata at creation time rather than relying on later remediation.
- Templates and generators SHOULD encode the metadata contract directly when compatible with their owning format and generation pipeline.
- Generated-file ownership takes precedence: modify the authoritative generator or template rather than repeatedly editing generated outputs when repository evidence identifies an owning source.

## Existing files

- When an agent performs an otherwise-authorized modification to a durable file lacking metadata, metadata incorporation is part of that same bounded mutation.
- Do not perform repository-wide metadata backfills merely because this rule is discovered unless the active task explicitly authorizes that scope.
- Do not rewrite otherwise untouched files solely to satisfy this policy without explicit authorization.

## Value-added test

A metadata field is justified only when a concrete consumer or repository operation can use it for discoverability, archiving, indexing, manifesting, grep/search, provenance, ownership, dependency traversal, lifecycle management, validation, or deterministic automation. If no concrete value exists, omit the field.

Minimize field count, repeated text, verbose descriptions, duplicated path information, natural-language metadata, and values derivable cheaply from canonical repository state. Do not minimize so aggressively that required provenance, references, validation, or discovery information is lost. Declared derived fields are exempt from this minimization only to the extent their derivation is defined above.

## Human readability

Metadata MUST remain directly understandable to a human reader. Field names SHOULD make the value's meaning evident without external lookup wherever practical. Text-valued metadata SHOULD be concise and declarative. Prefer `requires_validation: true` over compressed forms such as `flags: "rv1"`. Avoid unexplained codes, positional tuples, overloaded delimiters, and compressed multi-property strings.

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

## Evidence states

Use only `OBSERVED`, `VERIFIED`, `DERIVED`, `INFERRED`, `UNKNOWN`, and `NOT PERFORMED`. Inference is not evidence. Do not report a validation as passed without returned inspection or deterministic validation evidence.

## Cross-references

- Contract and routing index: `AGENTS.md`
- Artifact placement, ownership, text encoding, and portability: `configuration.rules.md`
- File and directory naming: `naming.rules.md`
- Prompt-corpus vocabulary and derived index: `prompts/manifest.yaml`, `prompts/INDEX.md`
- Deterministic subset validator: `tools/policy_check.py`

## Lineage and migration

Established in v3 and remediated on 2026-09-19. The remediation tightens the original contract as follows:

- `generated_at` narrowed from "ISO-8601 timestamp or repository-approved deterministic equivalent" to a required offset-aware ISO 8601 datetime; date-only and naive values are invalid. Existing date-only `generated_at` values are a declared migration backlog: they are `generated_at_format` violations to be normalized within bounded touches, not silently repaired and not backfilled repository-wide without explicit authorization.
- Canonical field order defined for the first time. Existing blocks remain `schema_valid`; ordering conformance applies to emitted and rewritten blocks.
- Enumerations (`status`, `scope`, `tracking`, `stage`, `category`, `authority_level`) made explicit and closed, with the prompt domain delegated to `prompts/manifest.yaml`.
- Semantic-uniqueness rule formalized; `mutates_repository` declared a derived projection of `authority_level`; `prompts/manifest.yaml` declared a derived index subordinate to prompt frontmatter.
- Serialization rules fixed: YAML 1.2 typing, duplicate-key rejection, no anchors/aliases, mandatory quoting for ambiguous scalars, and absent/null/`<TBD>`/empty-string distinction.
- Rule identifiers extended from MET-001..005 to MET-001..009 without renumbering published IDs.
