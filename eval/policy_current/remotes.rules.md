---
title: Remote Repository Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
references:
  - AGENTS.md
tags: [remotes, git, rules]
---

## Remote inventory and current evidence

Remote inventory and account facts are machine- and worktree-specific. Populate the following in `AGENTS.local.md` from the active worktree:

| Field | Required discovery | Current value |
| --- | --- | --- |
| Remote names | `git remote` | `<TBD: inspect target repository>` |
| Fetch URLs | `git remote get-url --all <name>` | `<TBD: inspect and redact credentials>` |
| Push URLs | `git remote get-url --push --all <name>` | `<TBD: inspect and redact credentials>` |
| Protocol | Parse verified URL as SSH, HTTPS, file, or other | `<TBD>` |
| Current branch | `git branch --show-current` | `<TBD>` |
| Upstream branch | `git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'` | `<TBD>` |
| GitHub CLI version | `gh --version` | `<TBD>` |
| Active GitHub account | `gh auth status --active` | `<TBD>` |
| Credential helper | `git config --get credential.helper` | `<TBD>` |

Do not infer the active account from a repository owner, commit author, remote URL, or prior session.

## Safe discovery

```sh
git rev-parse --show-toplevel
git status --short --branch
git remote
git remote -v
git branch --show-current
git config --get-regexp '^remote\..*\.(url|pushurl)$'
git config --get credential.helper
gh --version
gh auth status --active
```

- Never use `gh auth status --show-token`.
- Redact URL user-info, access tokens, embedded passwords, signed query parameters, and credentials before recording output.
- If a remote URL contains embedded credentials, treat it as a security finding and do not repeat the value.
- Discovery does not authorize mutation or network publication.

## Executable command guardrails

Repository-local `.codex/rules/*.rules` may mirror narrow command-prefix classification for safe inspection and approval-gated remote mutations. Those executable rules do not establish host, account, owner, or push authorization, and they do not replace the requirements in this file. A command allowed by `.rules` is still subject to the remote identity and publication checks below.

## Remote naming conventions

| Name | Intended meaning |
| --- | --- |
| `origin` | The primary remote associated with the local clone, commonly the user's writable fork or the authoritative repository |
| `upstream` | The authoritative source repository when `origin` is a fork |
| Other name | A documented, distinct purpose such as mirror, deployment, or vendor source |

- Do not assume `origin` is writable or authoritative; inspect fetch/push URLs and repository workflow.
- Do not create `upstream` when the repository is not a fork or no authoritative source has been established.
- Use one stable name per remote purpose. Avoid aliases that point to the same URL without a documented need.
- A remote name is local configuration, not proof of ownership or authorization.

## Ambiguous account handling and credential boundaries

| ID | Requirement |
| --- | --- |
| REM-001 | The agent MUST identify the active host/account before an account-dependent operation. |
| REM-002 | When several accounts or hosts are configured and the target is ambiguous, the agent MUST fail closed and request or retrieve authoritative account selection. |
| REM-003 | The agent MUST NOT switch accounts, run a new login flow, add a token, alter a credential helper, or broaden credential scope without explicit authorization. |
| REM-004 | The agent MUST NOT expose tokens, passwords, private keys, cookies, or authentication headers. |
| REM-005 | Repository access does not imply authority to push, create repositories, change settings, publish releases, or open pull requests. |

Use Proton Pass CLI or the approved credential/SSH agent according to `environments.rules.md` and `security.rules.md`.

## Protocol policy

- Preserve the repository's verified SSH or HTTPS protocol unless a concrete problem or current instruction requires a change.
- Do not switch protocol solely for preference.
- HTTPS authentication MUST use a supported token/credential helper; password authentication is not a valid GitHub fallback.
- SSH authentication SHOULD use the approved agent and verified host keys. Do not disable host-key checking.
- Separate fetch and push URLs only when the workflow requires it and the distinction is documented.
- Do not use local `file://`, anonymous, or alternate-protocol remotes as a silent substitute for the intended host.

## Operation authorization matrix

| Operation | Default authority | Required safeguards |
| --- | --- | --- |
| Inspect remotes/configuration | Allowed unless the user restricts inspection | Redact credentials |
| `git fetch` | Allowed only when current task requires current remote state and network access is permitted | Confirm target remote; do not alter credentials; report fetched refs |
| `git remote update` | Same as fetch, but broader; avoid unless all configured remotes are intended | Review remote set first |
| `git pull` | Not automatic; it mutates local refs and usually the worktree | Clean/understood worktree, explicit merge/rebase policy, rollback plan |
| Add remote | Explicit authorization required | Verify name, URL, owner, protocol, fetch/push intent |
| Rename remote | Explicit authorization required | Update scripts/docs/config that reference the old name |
| Change fetch or push URL | Explicit authorization required | Verify target identity and credentials; re-inspect result |
| Remove remote | Explicit authorization required | Record old configuration and confirm no workflow depends on it |
| Set branch upstream | Explicit authorization or clearly established repository workflow required | Verify remote branch and current branch |
| Push new commits | Explicit authorization required | Final diff/tests/commit review; confirm account, remote, branch, upstream |
| Push tags | Explicit authorization required | Verify tag content, signing, version, and release policy |
| Delete remote branch/tag | Explicit authorization required for the exact ref | Confirm target and recovery/retention implications |
| Force push | Prohibited by default | Exact explicit authorization, private/owned scope, lease protection, reviewed rewrite range |
| Create repository (`gh repo create`) | Explicit authorization required | Confirm owner, visibility, name, description, initialization, and remote side effects |
| Open PR or publish release | Explicit authorization required | Confirm base/head, account, content, checks, and disclosure scope |

## Fetch and pull

### Fetch

- Fetch only the remote and refs needed for the task.
- Do not prune remote-tracking refs unless the task or repository policy authorizes it.
- Do not use fetch as evidence that local branches are integrated or current without comparing refs.
- Record network failures, authentication failures, and missing refs accurately.

### Pull

Before pull:

1. inspect worktree and index;
2. identify current branch and configured upstream;
3. inspect `pull.rebase`, `pull.ff`, branch-specific configuration, and repository policy;
4. preserve unrelated changes;
5. confirm whether merge, rebase, or fast-forward-only behavior is intended;
6. avoid autostash unless explicitly selected and recovery is understood.

Do not resolve conflicts by discarding user work or choosing one side mechanically.

## Push

Before push:

1. confirm explicit authority;
2. identify active account/host;
3. identify exact remote, destination branch/tag, and upstream relationship;
4. inspect outgoing commits with `git log <remote-ref>..HEAD` or the appropriate range;
5. verify commits, signatures, tests, generated artifacts, sensitive data, and publication content;
6. use `--dry-run` when supported and useful;
7. push only the intended refs;
8. inspect and report the observed result.

Do not treat a local commit request as push authorization.

## Force push and rewritten history

- Force push is prohibited unless the user explicitly authorizes the exact remote and branch after the rewrite is understood.
- Use `--force-with-lease`, not unconditional `--force`, when authorized and supported.
- Refresh the remote ref immediately before the operation so the lease reflects current state.
- Do not force-push a protected, shared, release, or default branch.
- Preserve a recovery reference or record the pre-rewrite object ID when safe and authorized.
- Report any lease rejection rather than bypassing it.

## Remote mutation procedure

For add, rename, URL change, or removal:

1. record the existing remote configuration with credentials redacted;
2. verify task authority and intended owner/repository;
3. perform one bounded mutation;
4. re-run `git remote -v` and exact `get-url` checks;
5. verify dependent branch/upstream configuration;
6. do not contact or push to the new target unless separately authorized;
7. document rollback using the recorded prior configuration.

## GitHub CLI

- Use `gh auth status --active` or safe JSON filtering to identify the active account; never request token display.
- Set `--repo`, `--hostname`, owner, visibility, base, and head explicitly for high-impact operations.
- Do not rely on ambient account selection when multiple accounts or hosts exist.
- `gh repo create`, `gh pr create`, `gh release create`, repository settings changes, secret changes, and workflow dispatches are externally visible actions and require explicit authorization.
- Do not pass secrets as CLI arguments when a supported environment or credential mechanism exists.

## Verification after remote actions

- Re-inspect remotes and upstreams after local configuration changes.
- For fetch/pull, verify resulting refs, worktree state, and conflicts.
- For push, verify the exact remote response and compare the destination ref when possible.
- For PR/release/repository creation, verify visibility, owner, target branches, and published content.
- Report remote failures and partial effects; do not imply rollback occurred unless verified.

## Cross-references

- Credential provider and SSH agent policy: `environments.rules.md`
- Secret handling and security boundaries: `security.rules.md`
- Machine- and worktree-specific remote facts: `AGENTS.local.md`
- Executable command classification: `.codex/rules/*.rules`

## References

- [GitHub Docs: Managing remote repositories](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories)
- [GitHub Docs: About remote repositories](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)
- [GitHub Docs: Pushing commits to a remote repository](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- [GitHub CLI: `gh auth status`](https://cli.github.com/manual/gh_auth_status)
- [GitHub CLI manual](https://cli.github.com/manual/)

## Lineage and migration

`v1/remotes.txt` was empty, so no remote behavior could be preserved from it. This v3 file establishes evidence-first remote discovery, account ambiguity handling, explicit external-action authorization, SSH/HTTPS preservation, and safe force-push boundaries. It incorporates the authorization intent from `v2/testing.md` without retaining that file's unsupported executable rule syntax.
