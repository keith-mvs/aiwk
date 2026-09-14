# Configuration and File-Placement Rules

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

## Generated content

- Generated content MUST have a reproducible source and command when deterministic generation is expected.
- Do not hand-edit generated files.
- Do not generate placeholder artifacts, empty directories, sample branding, or unused scaffolding.
- Keep build caches and intermediate outputs out of durable generated directories.
- Compare generated output after regeneration and reject unrelated churn.

## Versioning

- Follow repository version policy and `naming.rules.md`.
- Keep semantic version, schema version, data/catalog version, and release identifier distinct when they represent different contracts.
- Avoid embedding timestamps or run IDs in stable configuration unless time is part of the artifact identity.
- Update version and changelog together when repository policy requires both.

## Cross-references

- General hygiene and temp disposition: `general.rules.md`
- Local machine facts and paths: `AGENTS.local.md`
- Environment and virtual environments: `environments.rules.md`
- Naming and versioned filenames: `naming.rules.md`
- Secret handling: `security.rules.md`

## Lineage and migration

This file expands `v1/configuration-management.md` and `v2/repo.md`. It preserves template-aware placement, clear ownership, portability, de-duplication, and repository hygiene. Hard-coded repository paths and a universal directory layout were rejected in favor of evidence-driven ownership and ecosystem-standard locations.
