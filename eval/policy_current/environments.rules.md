---
title: Development Environment Rules
generated_at: 2026-09-14
policy_version: 3
status: active
scope: repository
rules_root: .
tracking: tracked
references:
  - AGENTS.md
tags: [environments, runtimes, rules]
---

## Evidence model

Portable policy belongs here. Machine-specific values belong in `AGENTS.local.md` and MUST be established by inspection.

Do not substitute the artifact-generation sandbox's versions for the user's workstation values.

## Environment discovery

Inspect only what is relevant and do not print secrets.

### PowerShell

```powershell
$RepoRoot = git rev-parse --show-toplevel
$PSVersionTable
[System.Environment]::OSVersion.Version
$env:PROCESSOR_ARCHITECTURE

git --version
git config --list --show-origin
gh --version
gh auth status --active
ssh -V
py -0p
python --version
uv --version
conda --version
poetry --version
node --version
npm --version
dotnet --info
go version
rustc --version
cargo --version
pass-cli --version
pass-cli info
wsl --list --verbose
```

Filter `git config --list --show-origin` before recording output. Do not preserve credential values, authorization headers, tokens, passwords, private keys, or secret-bearing URLs.

### POSIX shell or WSL

```sh
REPO_ROOT="$(git rev-parse --show-toplevel)"
uname -a
cat /etc/os-release
git --version
ssh -V
python3 --version
uv --version
conda --version
node --version
pass-cli --version
pass-cli info
```

## Environment selection precedence

Use this order:

1. Repository-declared toolchain and version files.
2. Repository lockfiles and checked-in environment configuration.
3. Documented project bootstrap commands.
4. Existing local environment that exactly satisfies the repository contract.
5. Portable fallback defined below.

Do not select a globally installed interpreter, package manager, or dependency version merely because it is available first on `PATH`.

## Executable command guardrails

Repository-local `.codex/rules/*.rules` may allow version and discovery commands and prompt on environment or package mutations such as virtualenv creation or dependency installation. Those executable rules do not decide which interpreter, package manager, or environment is correct; that remains governed by the evidence and selection precedence in this file. An executable allow still has to target the correct environment.

## Python policy

### Project isolation

- Every Python project MUST use a project-specific environment or an explicitly isolated tool environment.
- Do not install project dependencies into the system Python, user site-packages, or an unrelated environment.
- On Windows, use the repository's declared environment; otherwise default to a repository-root `.venv/`.
- In WSL, use Conda only when the repository declares Conda, an `environment.yml`/lock exists, or native dependency requirements justify it. Do not assume WSL implies Conda.
- Do not share one mutable environment across unrelated repositories.

### Tool selection

When no dominant tool is configured, use this preference order:

1. Existing repository manager and lockfile.
2. `uv` with repository-managed `pyproject.toml` and lockfile, when `uv` is installed and the repository permits it.
3. Standard-library `venv` in `.venv/` with a pinned, hash-capable dependency input appropriate to the project.
4. Conda only for an established Conda workflow or native/scientific dependency need.
5. Poetry, PDM, Hatch, or another manager only when the repository already declares it or the user authorizes adoption.

Do not introduce a new manager solely for stylistic preference.

### Interpreter selection

1. Read `requires-python`, `.python-version`, `runtime.txt`, CI matrices, container images, and existing environment files.
2. Resolve an installed interpreter satisfying the complete supported range.
3. Record the exact interpreter used for validation.
4. Refuse to claim compatibility with untested interpreters.
5. In multi-version projects, run the repository's supported matrix or report untested versions as `NOT PERFORMED`.

### Creation and activation

Use repository commands when present. Portable fallbacks:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Do not upgrade `pip`, build tools, or dependencies when the repository pins them differently.

### Dependency installation and locking

- Install from the authoritative manifest and lockfile.
- Preserve hashes and integrity metadata where the ecosystem supports them.
- Keep direct and transitive dependency changes reviewable.
- Regenerate lockfiles only with the owning tool and configured version.
- Do not hand-edit lockfiles.
- Do not loosen version constraints to obtain a passing install without compatibility evidence.
- Record network access and registry sources when dependency resolution occurs.

### Recreation

A Python environment is reproducible only when a clean environment can be created from tracked configuration and supported external prerequisites. Validate recreation for material environment changes; do not infer reproducibility from an existing environment.

### Caches and build artifacts

- Keep `.venv/`, `__pycache__/`, `.pytest_cache/`, type-checker caches, wheel caches, `build/`, `dist/`, and `*.egg-info/` ignored unless repository policy explicitly requires a distribution artifact.
- Use tool-native cache locations.
- Clean caches only when diagnosis, reproducibility, storage, or security requires it; do not destroy caches reflexively.
- Build wheels and source distributions through the repository's supported build command and inspect artifact contents.

### Temporary environments

Use a temporary environment for compatibility probes, one-off migrations, or dependency conflict isolation. Create it outside tracked paths or under an ignored task directory, record its interpreter and dependency inputs, and delete it when the task ends.

## Shell and command policy

- Use the shell declared by the repository or current environment.
- Do not silently translate commands between PowerShell, Bash, CMD, and POSIX `sh` when semantics differ.
- Quote paths and arguments according to the active shell.
- Prefer argument arrays or native command APIs over concatenated shell strings in code.
- Do not bypass execution policy, signature checks, or shell security controls without explicit authorization.
- Treat command examples as platform-specific unless both forms are verified.

## Critical application versions

Record only tools relevant to the repository and current task. Typical sources include:

- language/compiler version files;
- CI images and action versions;
- package-manager lockfiles;
- container base image digests;
- database/server compatibility declarations;
- formatter/linter/type-checker configuration;
- Git, GitHub CLI, SSH, and Proton Pass CLI versions when they affect the workflow.

Do not copy a transient full software inventory into stable policy. Put resolved values in `AGENTS.local.md` or task evidence.

## Temporary and state locations

| Class | Windows | POSIX/WSL | Policy |
| --- | --- | --- | --- |
| OS temp | `$env:TEMP` | `${TMPDIR:-/tmp}` | Use for ephemeral work; do not commit |
| User config | `%APPDATA%` or tool-documented location | `${XDG_CONFIG_HOME:-${HOME}/.config}` | Non-secret user configuration |
| User cache | `%LOCALAPPDATA%` or tool-documented location | `${XDG_CACHE_HOME:-${HOME}/.cache}` | Rebuildable cache only |
| User state/logs | `%LOCALAPPDATA%` or tool-documented location | `${XDG_STATE_HOME:-${HOME}/.local/state}` | Restricted, redacted local state |
| Repository environment | Repository-defined; otherwise `.venv/` | Repository-defined; otherwise `.venv/` | Ignored and reproducible |

A tool's documented secure location overrides the generic fallback.

## API keys and credentials

- Store sensitive credentials in Proton Pass, not in Markdown, source, shell profiles, task prompts, tickets, or repository history.
- Resolve a credential only when a specific authorized operation requires it.
- Prefer child-process or process-scoped injection.
- Do not echo, print, inspect, transform, or retain the value unnecessarily.
- Clear manually exported secret variables immediately after use.
- Do not write secret-bearing command output to logs, diagnostics, generated artifacts, or context summaries.
- Preserve a stable secret reference or logical name rather than the secret value.

## Proton Pass CLI policy

Use the official `pass-cli` interface when installed and authorized.

### Secret references

Use URI references in this form:

```text
pass://<vault>/<item>/<field>
```

Prefer stable IDs over ambiguous names when duplicate names exist, but do not place sensitive vault/item identifiers in portable policy.

### Process-scoped execution

Prefer:

```sh
export SERVICE_TOKEN='pass://<vault>/<item>/<field>'
pass-cli run -- command --arguments
```

or a local ignored environment-reference file:

```text
SERVICE_TOKEN=pass://<vault>/<item>/<field>
```

```sh
pass-cli run --env-file .env.local -- command --arguments
```

`pass-cli run` resolves references for the child process and masks matching secret values in stdout/stderr by default. Do not use `--no-masking` unless the current task explicitly requires it and output controls are established.

### File injection

Use `pass-cli inject` only when an application cannot consume process-scoped variables:

- write to a restricted ephemeral file;
- keep the template separate from the resolved output;
- use restrictive permissions;
- prevent the output from entering version control, logs, backups, or context;
- delete the plaintext output immediately after use;
- do not overwrite a durable configuration file without explicit authorization and rollback.

### Authentication

- Prefer interactive/web login for human use or a scoped access token for approved automation.
- Never place a Proton account password, TOTP, extra password, personal access token, or session material in a command argument, source file, task prompt, or committed environment file.
- Use `pass-cli info` only to verify session state; do not copy account metadata into durable logs.
- Use `pass-cli logout` when the authorized workflow requires session termination.
- Do not create or broaden vault access without explicit authorization.

## SSH keys and agent policy

- Prefer an approved SSH agent rather than plaintext private-key files.
- When Proton Pass SSH agent is configured and verified, use it for Git authentication and signing according to its generated setup instructions.
- Do not copy a private key from Proton Pass into the repository or a persistent plaintext file.
- Store only public keys and non-secret fingerprints where needed.
- Verify host keys through the approved `known_hosts` policy; do not disable host-key checking as a workaround.
- Do not alter SSH config, agent sockets, key selection, or forwarding without task authority.
- Agent forwarding SHOULD be disabled unless a specific trusted workflow requires it.

## Environment validation

Before reporting an environment-dependent result:

1. Record the OS, architecture, shell, interpreter/tool versions, and active environment relevant to the command.
2. Confirm the repository root and configuration loaded.
3. Confirm the command used the intended executable, not an accidental global one.
4. Record the exact command and exit status.
5. Distinguish local success from cross-platform or CI compatibility.
6. Remove temporary credentials, files, environments, and diagnostic output.

## Cross-references

- Machine-local facts and authorized exceptions: `AGENTS.local.md`
- Secret classification and handling boundaries: `security.rules.md`
- Executable command classification: `.codex/rules/*.rules`

## References

- [Python virtual environments](https://docs.python.org/3/library/venv.html)
- [Python packaging user guide](https://packaging.python.org/)
- [Proton Pass CLI overview](https://protonpass.github.io/pass-cli/)
- [Proton Pass CLI secret references](https://protonpass.github.io/pass-cli/commands/contents/secret-references/)
- [Proton Pass CLI run command](https://protonpass.github.io/pass-cli/commands/contents/run/)
- [Proton Pass CLI inject command](https://protonpass.github.io/pass-cli/commands/contents/inject/)
- [Proton Pass SSH agent](https://proton.me/support/ssh-agent)

## Lineage and migration

This file preserves project-specific isolation and cleanup from `v1/environments.md` and `v1/engineering.md`. The Windows-venv and WSL-Conda statements were converted into evidence-driven precedence: `.venv` is the portable fallback, while Conda is selected only when the repository or native dependency contract requires it. Proton Pass CLI process-scoped injection and SSH-agent controls were added from current official documentation.
