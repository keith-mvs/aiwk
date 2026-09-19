---
title: Repository Agent Contract
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
references:
  - AGENTS.local.md
  - .codex/rules/
  - coding.rules.md
  - commits.rules.md
  - configuration.rules.md
  - context.rules.md
  - environments.rules.md
  - metadata.rules.md
  - naming.rules.md
  - remotes.rules.md
  - security.rules.md
  - skills.rules.md
  - testing.rules.md
tags: [agents, routing, rules]
---

Stable entry point for coding agents in this repository. Canonical protocols live in the `*.rules.md` modules co-located with this contract; this file carries discovery, scope, precedence, and routing only. `*.rules.md` files are ordinary Markdown policy modules made applicable by this contract; do not claim a platform executes them natively.

## Scope

- As an `AGENTS.md` document, this file's own instructions apply from its directory downward; a deeper `AGENTS.md` may specialize its subtree.
- The `*.rules.md` policy modules indexed below apply repository-wide whenever an agent engages this contract, including through a parent-directory or repository-root `AGENTS.md` that routes here.
- A narrower rule may narrow behavior but MUST NOT weaken security, authorization, evidence, or user-intent boundaries.
- Platform, organization, system, and legal constraints are non-overridable.

## Precedence

Within the repository-configurable layer, resolve conflicts in this order:

1. Explicit current user instruction.
2. A repository instruction of narrower scope (a deeper `AGENTS.md` or a directory-scoped equivalent) over a broader one.
3. An authorized `AGENTS.local.md` specialization of the applicable `AGENTS.md` in the same directory.
4. The nearest applicable `AGENTS.md`.
5. The top-level `AGENTS.md`.
6. Specialized `*.rules.md`.
7. Detected repository conventions.
8. Current official provider guidance.
9. Ecosystem convention.
10. Reversible, low-risk default.

Same-level conflicts: prefer narrower scope, then the newer explicit version, then the more specific condition. Preserve a material unresolved conflict as `<TBD>`. Lower-priority instructions MUST NOT weaken security or authority boundaries.

## Policy layers

- Semantic policy: the `*.rules.md` modules co-located with this contract (routing index below).
- Executable command policy: `.codex/rules/*.rules` classifies command prefixes as `allow`, `prompt`, or `forbidden` only; it does not grant semantic authority.
- Sandbox and approval boundaries are configured outside repository policy.
- More restrictive applicable control prevails. Read the owning rule before mutating repository state.

## Rule index

| tag | ns | rule |
| --- | --- | --- |
| coding | COD | `coding.rules.md` |
| commits | COM | `commits.rules.md` |
| configuration | CFG | `configuration.rules.md` |
| context | CTX | `context.rules.md` |
| environments | ENV | `environments.rules.md` |
| metadata | MET | `metadata.rules.md` |
| naming | NAM | `naming.rules.md` |
| remotes | REM | `remotes.rules.md` |
| security | SEC | `security.rules.md` |
| skills | SKL | `skills.rules.md` |
| testing | TST | `testing.rules.md` |

Read order: this contract, then the specialized rules applicable to the task; `coding` for implementation edits, `testing` for validation and evidence.

Rule identifiers use each module's `ns` prefix where present (for example, `COD-003`); modules without numbered identifiers are addressed as `<file>#<section>` and `ns` reserves the namespace for future identifiers.

## Local

Read the sibling `AGENTS.local.md` when present: machine-local facts and authorized specialization. It is not a universally native discovery filename; this contract requires the read.

## Fail closed

A missing required rule file, unresolved canonical owner, or unresolved precedence conflict stops the task: report `<TBD>`; do not invent protocol.
