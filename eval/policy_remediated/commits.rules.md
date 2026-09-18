---
title: Commit Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
references:
  - AGENTS.md
  - testing.rules.md
  - remotes.rules.md
  - security.rules.md
tags: [commits, git, rules]
---

## Evidence before policy application

Before creating or modifying a commit, inspect the effective configuration without exposing credentials:

```sh
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git config --get user.name
git config --get user.email
git config --get user.signingkey
git config --get gpg.format
git config --get commit.gpgsign
git config --get tag.gpgsign
git config --get init.defaultBranch
git config --get pull.rebase
git config --get pull.ff
git config --get credential.helper
```

Record unresolved values in `AGENTS.local.md`; do not invent identity, signing, branch, or authorization settings.

## Commit authority

| ID | Requirement |
| --- | --- |
| COM-001 | The agent MUST create a commit only when the current task or applicable repository policy authorizes it. |
| COM-002 | The agent MUST NOT amend, rebase, reset, squash, cherry-pick, or otherwise rewrite existing history without authority that covers the exact operation and affected commits. |
| COM-003 | The agent MUST NOT push, force-push, publish a release, create a remote repository, or open a pull request solely because a local commit was authorized. |
| COM-004 | The agent MUST preserve unrelated staged and unstaged user changes and MUST NOT use broad staging commands when they could include unrelated files. |
| COM-005 | The agent MUST NOT create or use a fabricated Git identity, signing key, co-author, issue reference, or attribution. |

## Executable command guardrails

Repository-local `.codex/rules/*.rules` may allow read-only Git inspection and prompt for staging, commit, history-rewrite, branch, tag, and cleanup commands. They may forbid destructive forms such as `git reset --hard`, but they do not waive commit-message format, signing, provenance, staging discipline, or rollback requirements in this file.

## Commit message format

Use:

```text
<type>: <imperative summary>
```

Controlled types:

| Type | Use |
| --- | --- |
| `build` | Add or change product behavior, implementation, or a deliverable artifact |
| `repair` | Correct a defect or regression |
| `maintain` | Refactor, clean, or maintain without intended behavior change |
| `test` | Add or revise tests without a production behavior change |
| `document` | Change documentation or prose-only policy |
| `configure` | Change configuration, tooling, dependency metadata, CI, or environment policy |
| `revert` | Reverse a prior commit |

Rules:

- The subject MUST be concise, specific, and imperative.
- The subject MUST describe one logical change and MUST NOT include a trailing period.
- Use the repository's stricter subject-length rule when one exists; otherwise avoid an arbitrary hard-coded limit.
- A subject-only commit is acceptable when the change and reason are self-evident from the staged diff.
- A body MUST be added when operational rationale is not evident, including breaking changes, migrations, security-sensitive changes, rollback constraints, non-obvious generated artifacts, or material tradeoffs.
- The body SHOULD explain why, risk, compatibility, validation, and rollback—not narrate every changed line.
- Add issue, pull-request, breaking-change, or sign-off footers only when repository convention or explicit instruction requires them.

## Atomicity and staging

| ID | Requirement | Observable verification |
| --- | --- | --- |
| COM-006 | One commit MUST represent one reviewable logical change. | The commit can be reverted without separating unrelated concerns. |
| COM-007 | Production code, its required tests, contract/schema updates, generated derivatives, and documentation MUST remain in the same commit when they jointly define one behavior change. | No intermediate committed state violates the intended contract. |
| COM-008 | Formatting-only, dependency-only, configuration-only, and generated-output-only changes SHOULD be separate when separation improves review and does not break repository invariants. | Each separated commit remains buildable or the dependency is explicitly ordered. |
| COM-009 | Stage explicit paths or hunks. Avoid `git add -A`, `git add .`, and broad glob staging when unrelated work exists. | `git diff --staged --name-status` contains only task-owned paths. |
| COM-010 | Do not stage caches, logs, local overrides, secrets, temp files, crash dumps, or editor state. | Staged-path and secret review passes. |

Recommended review sequence:

```sh
git status --short
git diff --check
git diff --stat
git diff

git add -- <explicit-paths>

git diff --staged --check
git diff --staged --name-status
git diff --staged --stat
git diff --staged
```

## Generated files

- Commit generated files only when the repository treats them as required source, release, lock, catalog, or distribution artifacts.
- Regenerate through the authoritative tool; do not hand-edit the derivative.
- Stage the generator/source change and its required generated outputs together unless repository policy explicitly separates them.
- Record the generator command and validation result in the task evidence or commit body when non-obvious.
- Do not commit transient build output solely because it changed locally.

## Branch-aware behavior

- Inspect the current branch and upstream before committing.
- Do not commit directly to a protected, release, shared, or default branch unless the current authority explicitly permits it.
- Do not create, switch, rename, or delete a branch merely to satisfy a presumed workflow.
- If the repository is in detached `HEAD`, merge, rebase, cherry-pick, or bisect state, stop mutation until the state and intended recovery are established.
- Preserve branch-specific generated metadata and versioning rules.

## Signing

- Preserve the effective repository and user signing configuration.
- When `commit.gpgsign=true` or repository policy requires signing, sign with the configured key and verify the resulting signature.
- When signing is not configured, do not enable it, generate a key, select a key, or disable a repository requirement without explicit authorization.
- Private signing keys MUST remain in the approved key store or agent. Prefer the verified Proton Pass SSH agent when the environment is configured for it.
- A signing failure is a failed commit operation; do not silently retry unsigned.

## Amend, fixup, and history rewriting

| Operation | Default policy |
| --- | --- |
| `git commit --amend` | Prohibited without explicit authority, even when the commit is local |
| Fixup commit without autosquash | MAY be created only when committing is authorized and repository workflow permits it |
| Interactive rebase or autosquash | Prohibited without explicit authority covering the rewrite range |
| Reset of committed history | Prohibited without explicit authority and a recovery plan |
| Force push | Governed by `remotes.rules.md`; prohibited by default |

Prefer a new corrective commit when existing history should remain stable.

## Attribution

- Use the configured human identity; do not substitute an agent identity.
- Do not add `Co-authored-by`, AI-generated markers, vendor signatures, or tool advertising unless required by repository or user policy.
- Do not remove existing required sign-offs or provenance markers.

## Specialized commit cases

### Configuration-only

Use `configure`. State affected scope and validation. Keep local-only values and secrets out of tracked configuration.

### Dependency update

Use `configure` unless repository convention defines another type. Include the manifest and lockfile together, preserve integrity metadata, record compatibility/security rationale when material, and run the repository's dependency and test gates.

### Formatting-only

Use `maintain`. Do not combine with behavior changes unless the formatter necessarily touches the same lines and separation would be misleading. Avoid repository-wide formatting without explicit scope.

### Revert

Use `revert`. Identify the reverted commit and why restoration is required. Do not use a revert to conceal an unresolved defect.

## Pre-commit verification

Before committing:

1. Confirm authority to commit.
2. Confirm branch and repository state.
3. Review unstaged and staged diffs.
4. Run relevant validation defined in `testing.rules.md` against the final staged content where feasible.
5. Scan staged content for credentials, private keys, tokens, sensitive personal data, local absolute paths, and transient artifacts.
6. Verify generated-file provenance.
7. Verify the commit message against this file and repository convention.
8. Create the commit using the configured signing behavior.
9. Inspect `git show --stat --oneline --decorate HEAD` and, when required, verify the signature.
10. Report the commit identifier without implying push or publication.

## Cross-references

- Validation execution and evidence before commit: `testing.rules.md`
- Remote, publication, and force-push authority: `remotes.rules.md`
- Secret and credential boundaries: `security.rules.md`
- Executable command classification: `.codex/rules/*.rules`

## Lineage and migration

This file reconciles `v1/commits.md` and `v2/commit.md`. The later v2 type vocabulary is retained as the local lineage. The absolute “subject only” rule was narrowed: simple commits remain subject-only, while the v3 task's required rationale, migration, security, and rollback cases receive a body. Remote operations and history rewriting are separated from ordinary commit authority.
