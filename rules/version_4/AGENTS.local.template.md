---
title: Local Agent Configuration Template
generated_at: 2026-09-14
policy_version: 4
status: active
scope: machine-worktree
rules_root: .aiwk/rules
tracking: untracked
references:
  - .aiwk/rules/environments.rules.md
  - .aiwk/rules/commits.rules.md
  - .aiwk/rules/configuration.rules.md
  - .aiwk/rules/remotes.rules.md
  - .aiwk/rules/security.rules.md
tags: [agents, local, environment, template]
---

Sanitized installation template for repository-root `AGENTS.local.md`. The installed copy is optional, untracked, non-secret, and populated by inspection in the target worktree. Do not distribute or preserve source-machine facts in this package. An unresolved value stays `<TBD: reason>`.

## Host facts

| field | value | evidence |
| --- | --- | --- |
| host_os | `<TBD: inspect target host>` | unresolved |
| host_arch | `<TBD: inspect target host>` | unresolved |
| primary_shell | `<TBD: inspect target environment>` | unresolved |
| repo_root | `<TBD: resolve in target worktree>` | unresolved |
| git | `<TBD: inspect when relevant>` | unresolved |
| git_identity | `<TBD: inspect before commit work>` | unresolved; non-secret |
| git_signing | `<TBD: inspect before signed commit work>` | unresolved; do not copy private material |
| git_defaults | `<TBD: inspect when behavior depends on them>` | unresolved |
| git_remote | `<TBD: inspect and redact when remote work is requested>` | unresolved |
| gh | `<TBD: inspect when GitHub account state is relevant>` | unresolved |
| ssh | `<TBD: inspect when SSH behavior is relevant>` | unresolved |
| python | `<TBD: resolve from repository configuration>` | unresolved |
| env_manager | `<TBD: use repository-declared manager>` | unresolved |
| node | `<TBD: inspect when relevant>` | unresolved |
| pass_cli | `<TBD: inspect when secret injection is required>` | unresolved |
| pass_session | `<TBD: local non-secret reference only>` | unresolved |
| ssh_agent | `<TBD: verify configured agent when required>` | unresolved |
| wsl | `<TBD: inspect only when WSL is relevant>` | unresolved |

Re-resolve a fact when the repository, worktree, machine, tool version, account, or task premise on which it depends changes. Do not load or refresh unrelated facts.

## Local exceptions

| id | scope | rule | authorization | expiry |
| --- | --- | --- | --- | --- |
| `<TBD: none recorded>` | - | - | - | - |

Exceptions MUST be explicit, narrow, reversible, time- or condition-bounded, and non-secret. They MUST NOT authorize remote publication, destructive history rewriting, credential disclosure, weakened security, or weakened validation unless a current higher-priority instruction independently grants that exact authority.
