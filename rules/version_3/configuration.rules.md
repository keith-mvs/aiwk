---
title: Configuration and File-Placement Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: rules/version_3
references:
  - rules/version_3/AGENTS.md
tags: [configuration, placement, rules]
---

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Repository configuration, hierarchy, and artifact placement |
| Rule namespace | `CFG` |
| Change field | `policy_version: 3` |

## Governing principle

Use the existing repository hierarchy and ecosystem conventions as the primary placement authority. Create a new top-level directory or configuration surface only when no existing owner fits and the new boundary is load-bearing, documented, and validated.

## Repository-root discovery and path portability

Resolve the repository root dynamically:

```sh
git rev-parse --show-toplevel
```

When Git is unavailable, locate the nearest directory containing the authoritative project manifest and state that fallback. Refer to paths as `${REPO_ROOT}/<relative-path>` in documentation and use repository-relative paths in tracked configuration.

- Do not commit machine-specific absolute paths, usernames, drive letters, home-directory expansions, or temporary mount paths.
- Use `${REPO_ROOT}`, `${HOME}`, `${TMPDIR}`, `${XDG_CONFIG_HOME}`, `${XDG_CACHE_HOME}`, `${XDG_STATE_HOME}`, `%USERPROFILE%`, `%TEMP%`, and ecosystem-native discovery only where applicable.
- Do not assume an environment variable is populated; define a deterministic platform-native fallback.
- Normalize paths only at input/output boundaries. Preserve repository-native separators and case semantics.

## Canonical placement hierarchy

Existing, documented repository locations override the defaults below.

| Artifact class | Preferred owner/location | Tracking default | Placement rule |
| --- | --- | --- | --- |
| Product source | Existing language/package source root such as `src/`, `app/`, or package-local source | Tracked | Place with the component that owns runtime behavior |
| Tests | Existing framework test root or tests adjacent to owned source | Tracked | Follow framework discovery and repository convention |
| Documentation | `docs/`, package-local docs, or required root sentinels | Tracked | Keep durable user/operator documentation near its owner |
| Repository configuration | Ecosystem-standard root files or existing `config/` owner | Tracked | Prefer one authoritative config over overlapping copies |
| Scripts | Existing `scripts/` or component-local scripts | Tracked when durable | One bounded operational purpose; no miscellaneous script dump |
| Developer tools | Existing `tools/` or tool package | Tracked when durable | Separate reusable tooling from one-off scratch work |
| Fixtures | Framework-standard fixture path, commonly under tests | Tracked | Keep deterministic, minimal, provenance-aware fixtures |
| Generated source/content | Repository-defined generated path | Conditional | Mark generated; preserve generator/source ownership |
| Build output | Ecosystem output such as `build/`, `dist/`, `out/`, `target/` | Ignored unless release policy requires it | Never treat output as authoritative source |
| Cache | Tool-native cache location | Ignored | Do not relocate into tracked source for convenience |
| Temporary files | Platform temp; ignored repository-local temp only when required | Ignored | Delete at task end unless explicitly retained for diagnosis |
| Reports | Existing reports/evidence location when durable; otherwise temp | Conditional | Track only reviewable, required evidence—not raw tool dumps |
| Logs | Platform local-state/log location | Ignored | Redact, bound retention, and avoid secret-bearing payloads |
| Local-only configuration | Standard local override names, `AGENTS.local.md`, `.env.local`, or existing equivalent | Ignored | Never make local values the portable source of truth |
| User-specific files | Platform user config/state location | Untracked | Do not add to repository unless a sanitized template is required |
| External/reference material | Existing `references/`, `vendor/`, or `third_party/` owner | Conditional | Record origin, version, license, integrity, and update policy |
| Archive input/output | Temporary staging or repository-defined release location | Conditional | Validate members; do not extract uncontrolled content into source |

## File creation decision

Before creating a file:

1. Identify its purpose, owner, lifecycle, authority, consumers, update mechanism, and deletion condition.
2. Search for an existing artifact that already owns the same concern.
3. Prefer extending the authoritative artifact over creating an overlapping one.
4. Use ecosystem-standard filenames and locations where tools require them.
5. Apply `naming.rules.md` only after ownership and ecosystem constraints are established.
6. Determine whether the file is source, generated, local-only, cache, temp, report, or release output.
7. Add or adjust ignore rules before producing recurring local artifacts.
8. Verify that the new file is referenced or discovered by a live entry point.

A file without a distinct owner, consumer, or lifecycle is presumptive clutter and SHOULD NOT be created. Non-project files MUST remain outside the repository or in a documented ignored staging area; do not use the repository as a general download, export, backup, or scratch location.

## Configuration ownership and precedence

- Prefer the ecosystem's canonical configuration file: for example, `pyproject.toml`, `package.json`, `.editorconfig`, or tool-specific standard files when the repository uses that ecosystem.
- Do not duplicate the same setting across files unless a documented compatibility layer requires it.
- When duplication is unavoidable, designate one source of truth and generate or validate mirrors.
- Repository-wide settings belong at the narrowest common owner. Component-specific settings belong with that component.
- Local overrides MUST be ignored and MUST NOT become prerequisites for CI or other users unless a sanitized template and deterministic setup procedure exist.
- Generated configuration MUST identify its source and generator. Source configuration MUST remain human-reviewable.
- Do not migrate configuration formats, merge tools, or add framework scaffolding merely to make policy look uniform.

## Tracked versus ignored configuration

| Configuration class | Policy |
| --- | --- |
| Portable defaults | Track |
| Schemas, templates, and examples without secrets | Track |
| Lockfiles required by the ecosystem | Track according to repository policy |
| Machine paths, account names, local ports, personal preferences | Ignore or externalize |
| Secret references such as `pass://...` | May be tracked only when the reference itself is non-sensitive and repository policy permits it |
| Secret values, access tokens, private keys, recovery data | Never track |
| Generated effective configuration containing plaintext secrets | Never track; use process-scoped injection or ephemeral restricted files |
| CI/deployment configuration | Track only after authority and security review |

## `.gitignore` requirements

- Ignore local virtual environments, caches, build output, local logs, temp files, crash dumps, secret-bearing `.env` files, `AGENTS.local.md`, and tool-specific state when applicable.
- Keep sanitized examples such as `.env.example` tracked when they contain no secret values.
- Use narrow patterns. Do not hide source or broad directories to silence a dirty worktree.
- Review negation rules and nested ignore files before adding a pattern.
- Do not rely on `.gitignore` as a secret-control boundary; previously tracked files and explicit staging can bypass it.

## Machine-specific overrides

Use this order:

1. Portable tracked defaults.
2. Tracked environment-neutral schema or template.
3. Platform- or environment-specific tracked overlay when it is shared and non-secret.
4. Untracked local override.
5. Process-scoped environment variables or Proton Pass secret injection.

Do not encode a user's home path or workstation identifier in portable configuration. Put non-secret local facts in `AGENTS.local.md` and sensitive values in Proton Pass.

## XDG and platform-native locations

For user-scoped tool state outside a repository:

- On XDG-aware systems, prefer `${XDG_CONFIG_HOME:-${HOME}/.config}`, `${XDG_CACHE_HOME:-${HOME}/.cache}`, and `${XDG_STATE_HOME:-${HOME}/.local/state}`.
- On Windows, use application-supported locations under `%APPDATA%`, `%LOCALAPPDATA%`, and `%TEMP%` rather than hard-coded user paths.
- Follow the tool's documented location when it conflicts with the generic convention.
- Do not relocate credentials or security-sensitive state without explicit tool support.

## Temporary and generated artifact policy

| Artifact class | Default location | Tracking policy | End-of-task disposition |
| --- | --- | --- | --- |
| Ephemeral OS/runtime temporary data | Platform temp location | Never track | Delete through normal lifecycle; do not rely on persistence |
| Repository-local working temporary data | Ignored repository-local temp directory only when required by a tool | Never track | Delete unless a current task explicitly retains it for diagnosis |
| Cache | Tool- or platform-native cache location | Never track unless the repository explicitly vendors a cache artifact | Leave only when safe and reusable; otherwise remove |
| Log | Local state/log location | Do not track by default | Redact, summarize relevant evidence, then remove or expire |
| Diagnostic or crash dump | Restricted local diagnostic location | Never track without explicit review and redaction | Retain only as long as required for authorized diagnosis |
| Extracted archive | Dedicated temporary staging directory with validated member paths | Never track by default | Delete after use or promote reviewed members individually |
| Generated but useful artifact | Repository-defined generated/output location | Track only when repository policy requires it | Verify provenance and reproducibility; label as generated |
| Durable project artifact | Canonical repository location | Track as source | Validate, document ownership, and include in review |
| Provider/tool transient output | Local task state or temporary storage | Never track by default | Extract required evidence, then remove |

The agent MUST leave the workspace reviewable and hygienic: task-created transient files are removed, ignored, or promoted to justified durable artifacts.

## Repository-local temporary files

- Prefer the OS or tool-native temporary location.
- Use repository-local temporary storage only when the tool requires repository-relative paths, atomic rename within the repository filesystem, or reproducible local staging.
- Name and ignore the directory according to `naming.rules.md` and the ignore rules in this file.
- Do not place temporary files beside durable source when a dedicated temporary location is available.
- Do not use `README.md`, placeholder files, empty directories, or arbitrary suffixes to preserve unused scaffolding.

## Generated content

- Generated content MUST have a reproducible source and command when deterministic generation is expected.
- Do not hand-edit generated files.
- Do not generate placeholder artifacts, empty directories, sample branding, or unused scaffolding.
- Keep build caches and intermediate outputs out of durable generated directories.
- Compare generated output after regeneration and reject unrelated churn.

## Text encoding, line endings, and whitespace

### Encoding

All agent-generated or agent-modified text artifacts MUST use UTF-8 unless a higher-authority protocol, external interface, file format, or compatibility requirement explicitly requires another encoding. Do not infer a legacy encoding from platform defaults. When an existing file uses a non-UTF-8 encoding required by an authoritative interface, preserve that encoding and record the exception rather than silently converting it.

For Python text I/O, specify UTF-8 explicitly with strict error handling (`encoding="utf-8"`, `errors="strict"`) wherever supported, including file open/read/write, `pathlib` text helpers, subprocess text decoding, and equivalent I/O boundaries. Do not rely on locale-derived default encodings, operating-system defaults, implicit fallback decoding, or lossy handlers such as `ignore` or `replace` for repository-controlled text. Invalid UTF-8 MUST fail visibly rather than being silently altered. When reading bytes whose encoding is externally defined and not UTF-8, use the explicitly required encoding at that boundary and normalize to Unicode internally where appropriate; do not relabel arbitrary bytes as UTF-8.

For other tools and runtimes, explicitly request UTF-8 whenever the API or tool exposes an encoding option; the equivalent contract is UTF-8 with strict decode and encode errors. Repository automation MUST NOT depend on environment-specific ANSI, OEM, locale, shell, terminal, or platform-default encodings when a deterministic UTF-8 mode is available. Binary artifacts are excluded from text-encoding normalization.

### Line endings

`LF` (`0A`) and `CRLF` (`0D 0A`) are distinct byte representations and MUST NOT be treated as equivalent when byte identity, hashing, signatures, patches, generated fixtures, protocol payloads, or exact-format validation is material.

- For repository-controlled text, use the repository's canonical newline convention; when no governing convention exists, default to `LF`.
- Do not introduce mixed newline styles within a file.
- Preserve `CRLF` only when required by an existing authoritative repository convention, a platform or external protocol contract, generated-file ownership, or a verified consumer requirement.
- Do not perform whole-file LF/CRLF normalization as an incidental side effect of an unrelated edit unless the active task authorizes that normalization.

Python text writes MUST avoid accidental platform-dependent newline conversion when exact repository newline behavior is material. Determine the required convention before rewriting an existing file; emit `LF` for newly generated repository text with no contrary rule. When exact preservation is required, use an I/O method that provides deterministic newline handling and validate the resulting bytes. Do not claim newline preservation from source-level inspection alone when a write operation may transform line endings.

### Whitespace

Whitespace changes MUST be intentional, scoped, and semantically safe:

- remove trailing spaces and tabs and do not introduce trailing whitespace, unless a governing format requires otherwise;
- use blank lines according to the owning format or repository convention;
- do not replace meaningful tabs with spaces or meaningful spaces with tabs;
- do not normalize whitespace inside literals, code samples, generated fixtures, protocol payloads, hashes, signatures, snapshots, or other byte-sensitive content;
- do not perform unrelated whole-file whitespace cleanup during a bounded change;
- avoid repeated blank lines in ordinary text files unless required for readability or syntax.

The Markdown frontmatter block structure (opening `---`, metadata, closing `---`, exactly one blank line, body) is owned by `metadata.rules.md`.

### Existing files

Before writing an existing text file, determine where material: current encoding, BOM presence or absence, newline convention, mixed-line-ending state, format-specific whitespace requirements, and generated-file ownership. Preserve established valid characteristics unless the governing repository rule explicitly requires normalization. Do not add or remove a UTF-8 BOM unless repository or consumer requirements establish the expected form. If encoding or newline state cannot be determined safely, mark it `UNKNOWN` and avoid destructive rewriting.

### Generated files

New repository-controlled text artifacts default to UTF-8 with strict errors, `LF` newlines, no mixed newline styles, and no trailing whitespace. Exceptions require an explicit authoritative dependency or format requirement.

### Enforcement

Agents touching text artifacts MUST:

1. identify the authoritative encoding/newline rule;
2. avoid implicit platform defaults;
3. use UTF-8 strict for Python-controlled text I/O unless an explicit boundary requires otherwise;
4. use UTF-8 explicitly in other applicable text I/O;
5. preserve required `LF` or `CRLF` semantics;
6. prevent mixed newline styles;
7. avoid unrelated whitespace churn;
8. validate the final representation when encoding, newline, or byte identity is material.

A file touch does not authorize repository-wide encoding, newline, or whitespace normalization.

### Validation

Final-state validation MUST check, where applicable:

- `encoding`: `utf-8` expected, `strict` errors, exceptions explicit or absent;
- `newlines`: repository-canonical-or-`LF` expected, no mixed styles;
- `whitespace`: no trailing whitespace, semantic whitespace preserved;
- `python_io`: explicit encoding and strict errors.

Validation of exact encoding or newline representation requires inspection of the resulting artifact or bytes. Do not report `VERIFIED` from intent or configuration alone.

### Failure handling

Fail closed when decoding fails under a required strict encoding, conversion would destroy undecodable data, required newline semantics conflict with an authoritative consumer, byte-sensitive content cannot be preserved, or ownership of an incompatible generated artifact is unresolved. Report the file, observed condition, unmet requirement, and minimum corrective action.

### Protocol preservation

Encoding, line-ending, and whitespace normalization MUST NOT change protocol semantics, structured-data meaning, executable behavior, requirement strength, signatures or hashes, parser-significant whitespace, generated-artifact ownership, or external interoperability requirements. When textual normalization and protocol preservation conflict, protocol preservation wins.

## Versioning

- Follow repository version policy and `naming.rules.md`.
- Keep semantic version, schema version, data/catalog version, and release identifier distinct when they represent different contracts.
- Avoid embedding timestamps or run IDs in stable configuration unless time is part of the artifact identity.
- Update version and changelog together when repository policy requires both.

## Cross-references

- Local machine facts and paths: `AGENTS.local.md`
- Environment and virtual environments: `environments.rules.md`
- Naming and versioned filenames: `naming.rules.md`
- Secret handling: `security.rules.md`
- Metadata and frontmatter contract: `metadata.rules.md`

## Lineage and migration

This file expands `v1/configuration-management.md` and `v2/repo.md`. It preserves template-aware placement, clear ownership, portability, de-duplication, and repository hygiene. Hard-coded repository paths and a universal directory layout were rejected in favor of evidence-driven ownership and ecosystem-standard locations. The text encoding, line-ending, and whitespace protocol was added from the `repo.io-encoding-line-endings` policy prompt as a byte-level counterpart to artifact placement and generated-content rules. The temporary and generated artifact policy, repository-local temporary file rules, and workspace-hygiene requirement were absorbed from `general.rules.md` during the GEN migration; the reference to `configuration.rules.md` in those rules was resolved to this file.
