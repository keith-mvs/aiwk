---
title: Repository Agent Contract
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: rules/version_3
references:
  - rules/version_3/
  - .codex/rules/
tags: [agents, routing, rules]
---

Stable entry point for coding agents in this repository. Canonical protocols live in `rules/version_3/*.rules.md`; this file carries discovery, scope, precedence, and routing only. `*.rules.md` files are ordinary Markdown policy modules made applicable by this contract; do not claim a platform executes them natively.

## Scope

- Applies from this file's directory downward; a deeper `AGENTS.md` may specialize its subtree.
- A narrower rule may narrow behavior but MUST NOT weaken security, authorization, evidence, or user-intent boundaries.
- Platform, organization, system, and legal constraints are non-overridable.

## Precedence

Within the repository-configurable layer, resolve conflicts in this order:

1. Explicit current user instruction.
2. Repository-local instruction with narrower scope.
3. Nearest applicable `AGENTS.md`.
4. Authorized `AGENTS.local.md` specialization.
5. Top-level `AGENTS.md`.
6. Specialized `*.rules.md`.
7. Detected repository conventions.
8. Current official provider guidance.
9. Ecosystem convention.
10. Reversible, low-risk default.

Same-level conflicts: prefer narrower scope, then the newer explicit version, then the more specific condition. Preserve a material unresolved conflict as `<TBD>`. Lower-priority instructions MUST NOT weaken security or authority boundaries.

## Policy layers

- Semantic policy: `rules/version_3/*.rules.md` (routing index below).
- Executable command policy: `.codex/rules/*.rules` classifies command prefixes as `allow`, `prompt`, or `forbidden` only; it does not grant semantic authority.
- Sandbox and approval boundaries are configured outside repository policy.
- More restrictive applicable control prevails. Read the owning rule before mutating repository state.

## Rule index

| tag | ns | rule |
| --- | --- | --- |
| coding | COD | `rules/version_3/coding.rules.md` |
| commits | COM | `rules/version_3/commits.rules.md` |
| configuration | CFG | `rules/version_3/configuration.rules.md` |
| context | CTX | `rules/version_3/context.rules.md` |
| environments | ENV | `rules/version_3/environments.rules.md` |
| metadata | MET | `rules/version_3/metadata.rules.md` |
| naming | NAM | `rules/version_3/naming.rules.md` |
| remotes | REM | `rules/version_3/remotes.rules.md` |
| security | SEC | `rules/version_3/security.rules.md` |
| skills | SKL | `rules/version_3/skills.rules.md` |
| testing | TST | `rules/version_3/testing.rules.md` |

Read order: this contract, then the specialized rules applicable to the task; `coding` for implementation edits, `testing` for validation and evidence.

## Local

Read `rules/version_3/AGENTS.local.md` when present: machine-local facts and authorized specialization. It is not a universally native discovery filename; this contract requires the read.

## Fail closed

A missing required rule file, unresolved canonical owner, or unresolved precedence conflict stops the task: report `<TBD>`; do not invent protocol.
