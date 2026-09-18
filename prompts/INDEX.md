---
title: Reusable Prompt Corpus Index
generated_at: 2026-09-14
status: active
scope: repository
tracking: tracked
references:
  - manifest.yaml
  - SOURCE_MAP.md
tags: [prompts, index]
---

# Reusable Prompt Corpus

This corpus contains repository-agnostic prompts distilled from the complete source library described in [SOURCE_MAP.md](SOURCE_MAP.md). Select one prompt by task outcome, provide its declared inputs, and preserve its authority boundary. Prompt metadata is indexed in [manifest.yaml](manifest.yaml).

## Routing Rules

1. Choose the narrowest prompt whose purpose matches the requested deliverable.
2. Start with discovery or analysis when the cause, owner, or scope is unknown.
3. Use a mutation prompt only when the task authorizes repository changes.
4. Compose local Git, remote publication, and release prompts only when those actions are separately authorized.
5. Treat unrun validation as `NOT PERFORMED`; never promote a plan or inference to execution evidence.
6. Resolve repository instructions and native tooling before applying any prompt defaults.

## Stage Vocabulary

`discover` -> `inspect` -> `analyze` -> `plan` -> `execute` -> `validate` -> `report` -> `publish`

A prompt lists every stage it spans. Its first listed stage is the dominant routing stage.

## Authority Levels

| Level | Boundary |
| --- | --- |
| `read-only` | Inspect and report; do not mutate repository or remote state. |
| `bounded-mutation` | Change only the task-owned repository paths; no staging, commit, or remote action. |
| `local-git-mutation` | May alter local Git state within the explicit task; no remote action. |
| `remote-mutation` | May change an explicitly identified remote only with current authorization and preflight evidence. |

## Prompt Index

| Domain | Prompt | Primary outcome |
| --- | --- | --- |
| Repository | [Discover Repository Context](repository/discover-context.prompt) | Establish root, policy, structure, state, and validation mechanisms. |
| Repository | [Audit Repository Structure](repository/audit-structure.prompt) | Assess hierarchy, ownership, generated content, and portability. |
| Analysis | [Analyze Codebase](analysis/analyze-codebase.prompt) | Explain a bounded implementation or behavior from traceable evidence. |
| Analysis | [Compare Artifacts](analysis/compare-artifacts.prompt) | Produce a deterministic semantic comparison and reconciliation path. |
| Analysis | [Assess Architecture](analysis/assess-architecture.prompt) | Evaluate boundaries, flows, risks, and fitness for stated qualities. |
| Analysis | [Review Code Change](analysis/review-code-change.prompt) | Find actionable defects and missing validation in a change. |
| Debugging | [Diagnose Root Cause](debugging/diagnose-root-cause.prompt) | Establish the causal mechanism behind an observed failure. |
| Debugging | [Remediate Defect](debugging/remediate-defect.prompt) | Fix a confirmed cause and protect the behavior with validation. |
| Implementation | [Implement Change](implementation/implement-change.prompt) | Implement and integrate a requested behavior with bounded scope. |
| Implementation | [Refactor Code](implementation/refactor-code.prompt) | Improve structure while preserving declared behavior. |
| Implementation | [Migrate Artifacts](implementation/migrate-artifacts.prompt) | Move data, code, or configuration with integrity and rollback controls. |
| Implementation | [Change Configuration](implementation/change-configuration.prompt) | Modify the authoritative configuration layer and verify effective behavior. |
| Dependencies | [Manage Dependency](dependencies/manage-dependency.prompt) | Add, remove, or change a dependency for a demonstrated reason. |
| Testing | [Add Regression Coverage](testing/add-regression-coverage.prompt) | Reproduce and protect a stable behavioral contract. |
| Testing | [Validate Change](testing/validate-change.prompt) | Select and run evidence-based checks from narrow to broad. |
| Git | [Manage Worktree](git/manage-worktree.prompt) | Inspect and safely prepare local worktree state. |
| Git | [Create Commit](git/create-commit.prompt) | Stage only the intended set and create a reviewable local commit. |
| Git | [Publish Remote Changes](git/publish-remote-changes.prompt) | Push an authorized ref after remote and payload preflight. |
| Release | [Assess Release Readiness](release/assess-release-readiness.prompt) | Decide readiness from explicit gates and residual risk. |
| Release | [Publish Release](release/publish-release.prompt) | Publish an authorized release and verify the remote result. |
| Documentation | [Update Documentation](documentation/update-documentation.prompt) | Align durable documentation with verified behavior. |
| Documentation | [Maintain Changelog](documentation/maintain-changelog.prompt) | Record user-visible changes using repository conventions. |
| Governance | [Engineer Repository Policy](governance/engineer-repository-policy.prompt) | Create or revise enforceable, non-duplicative agent policy. |
| Governance | [Maintain Work Items](governance/maintain-work-items.prompt) | Normalize, reconcile, and prioritize backlog or work-contract records. |
| Governance | [Engineer Agent Skill](governance/engineer-agent-skill.prompt) | Build or revise a bounded, discoverable capability package. |
| Prompts | [Compile Task Prompt](prompts/compile-task-prompt.prompt) | Convert a task request into an executable, evidence-bound prompt. |
| Prompts | [Maintain Prompt Corpus](prompts/maintain-prompt-corpus.prompt) | Inventory, deduplicate, stage, index, and validate a prompt library. |
| Security | [Review Security](security/review-security.prompt) | Evaluate threats, controls, exposures, and evidence without silent remediation. |
| Maintenance | [Clean Repository](maintenance/clean-repository.prompt) | Remove confirmed clutter without deleting owned or generated artifacts. |
| Performance | [Investigate Performance](performance/investigate-performance.prompt) | Measure a bottleneck, identify cause, and validate a bounded improvement. |
| Workflow | [Execute Work Item](workflow/execute-work-item.prompt) | Carry an authorized work item from discovery through verified completion. |
| Workflow | [Monitor Agent Session](workflow/monitor-session.prompt) | Observe an active agent session and report evidence-bounded feedback. |
| Research | [Source-Grounded Analysis](research/source-grounded-analysis.prompt) | Answer a bounded question with authoritative, traceable evidence. |

## Common Chains

- Defect: `repo.discover-context` -> `repo.diagnose-root-cause` -> `repo.remediate-defect` -> `repo.validate-change`
- Feature: `repo.discover-context` -> `repo.implement-change` -> `repo.validate-change`
- Refactor: `repo.analyze-codebase` -> `repo.refactor-code` -> `repo.validate-change`
- Delivery: `repo.validate-change` -> `repo.create-commit` -> `repo.publish-remote-changes`
- Release: `repo.assess-release-readiness` -> `repo.publish-release`
- Corpus maintenance: `prompt.maintain-corpus` -> `repo.validate-change` -> `repo.create-commit`
