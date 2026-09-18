---
title: Repository Agent Bridge
generated_at: 2026-09-18
policy_version: 3
status: active
scope: repository
rules_root: rules/version_3
tracking: tracked
references:
  - rules/version_3/AGENTS.md
  - .codex/rules/
tags: [agents, routing, rules]
---

Repository entry point for coding agents. The canonical agent contract, precedence model, rule index, and fail-closed semantics live in `rules/version_3/AGENTS.md`; the normative policy modules are the `rules/version_3/*.rules.md` files it indexes. This bridge carries routing only and defines no additional policy.

- Follow `rules/version_3/AGENTS.md` as the governing contract for repository work.
- Read the sibling `rules/version_3/AGENTS.local.md` when present for machine-local facts and authorized specialization.
- Executable command policy lives in `.codex/rules/*.rules`; it classifies command prefixes only and grants no semantic authority.
- When this file and a deeper `AGENTS.md` conflict, the precedence rules in `rules/version_3/AGENTS.md` decide.
