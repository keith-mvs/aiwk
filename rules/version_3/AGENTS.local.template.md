---
title: Local Agent Configuration
generated_at: 2026-09-14
policy_version: 3
status: active
scope: machine-worktree
rules_root: .
tracking: untracked
references:
  - environments.rules.md
  - commits.rules.md
  - configuration.rules.md
  - remotes.rules.md
  - security.rules.md
tags: [agents, local, environment]
---

Machine/worktree-local facts and authorized exceptions for `AGENTS.md`. Populate by inspection; re-resolve on tool update, machine, or worktree change; an unresolved value stays `<TBD: reason>`. Untracked and non-secret only; secret references resolve at execution per `environments` and `security`.

## Host facts

| field | value | evidence |
| --- | --- | --- |
| host_os | `Windows_NT 10.0.26200` | observed 2026-09-14 |
| host_arch | `AMD64` (x86_64) | observed 2026-09-14 |
| primary_shell | `PowerShell 7.6.5` | observed (`pwsh --version`) |
| repo_root | `C:/Users/kjfle/Projects/aiwk` | observed (`git rev-parse --show-toplevel`) |
| git | `2.55.0.windows.3` | observed (`git --version`) |
| git_identity | `Keith Fleming` / `248089218+keith-mvs@users.noreply.github.com` | observed (`git config`) |
| git_signing | `gpg.format=ssh`, `commit.gpgsign=true`, key `C:/Users/kjfle/.ssh/id_ed25519_signing.pub` | observed (`git config`) |
| git_defaults | `init.defaultBranch=master`, `pull.rebase=false`, `pull.ff=true`, `credential.helper=manager` | observed (`git config`) |
| git_remote | `origin` -> `git@github.com:keith-mvs/aiwk.git` (ssh) | observed (`git remote -v`) |
| gh | `2.97.0`; active account `keith-mvs` on github.com | observed (`gh auth status --active`, token withheld) |
| ssh | `OpenSSH_10.3p1` | observed (`ssh -V`) |
| python | `3.14.5` on PATH; `py -0p`: 3.15 (default), 3.14, 3.11 | observed |
| env_manager | `uv 0.9.13`; conda absent | observed |
| node | `v24.19.0` | observed (`node --version`) |
| pass_cli | `2.2.3` | observed (`pass-cli --version`) |
| pass_session | `<TBD: local non-secret reference only>` | unresolved |
| ssh_agent | `<TBD: verify Proton Pass SSH agent or other configured agent>` | unresolved |
| wsl | `Ubuntu-24.04` (default), `NVIDIA-Workbench`, `Debian`; all WSL2 | observed (`wsl --list --verbose`) |

Re-resolution commands: environment discovery in `environments`, commit config evidence in `commits`, remote account evidence in `remotes`.

## Local exceptions

| id | scope | rule | authorization | expiry |
| --- | --- | --- | --- | --- |
| `<TBD: none recorded>` | - | - | - | - |

Exceptions MUST be explicit, narrow, reversible, and non-secret; they MUST NOT authorize remote publication, destructive history rewriting, credential disclosure, or weakened validation unless the current user instruction independently grants it.
