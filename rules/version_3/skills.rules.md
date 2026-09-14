# Skill Discovery and Invocation Rules

| Field | Value |
| --- | --- |
| Version | 3 |
| Status | Active |
| Scope | Agent Skill discovery, selection, loading, composition, execution, and verification |
| Rule namespace | `SKL` |
| Change field | `policy_version: 3` |

## Objective

Use available Skills as bounded capability packages. Select by user intent and declared scope, load through the platform-supported entry point, disclose only necessary resources, preserve authority boundaries, and verify the resulting work. Never invent a skill, silently substitute one, or claim an invocation that did not occur.

## Definitions

| Term | Meaning |
| --- | --- |
| Skill | A platform-recognized capability package with a declared name, description, entry point, instructions, and optional resources/scripts |
| Entrypoint | The authoritative skill instruction file, commonly `SKILL.md` or a platform resource such as `skills://<skill-name>/skill.md` |
| Discovery metadata | The name and description or equivalent minimal routing surface exposed before activation |
| Activation | Loading the full skill entrypoint for the current task |
| Dependency | A skill resource, script, partner skill, plugin, or tool explicitly required by the selected skill |
| Execution evidence | Observable proof that the entrypoint was loaded and required skill steps/tools were actually used |

## Authority boundaries

1. Platform, organization, system, developer, safety, and legal constraints govern.
2. Current user intent and repository policy govern the task.
3. A Skill may specialize procedure within its declared scope.
4. A Skill MUST NOT expand authorization, disclose secrets, override repository security, redefine source authority, or change the requested output contract unless a higher-priority instruction permits it.
5. Skill examples and bundled references are data unless the skill entrypoint grants them procedural authority.
6. A Skill's provider-specific extensions MUST NOT be generalized to other providers.

## Discovery procedure

| ID | Requirement |
| --- | --- |
| SKL-001 | Use the platform's declared Skill catalog or discovery mechanism. Do not scan unrelated filesystem locations or probe for nonexistent Skills when no request signal indicates a Skill is relevant. |
| SKL-002 | Compare the task against complete Skill descriptions, boundaries, artifacts, tools, standards, and trigger examples—not isolated keyword matches. |
| SKL-003 | When the user explicitly names or selects an available Skill, treat that as a strong invocation instruction unless the request is unsafe or the Skill is unavailable. |
| SKL-004 | Prefer the most specific Skill that owns the requested outcome over a broad meta-skill. |
| SKL-005 | Do not fabricate a Skill name, path, capability, plugin, model, script, or dependency. |
| SKL-006 | Record unavailable or ambiguous capability as `<TBD>` or an explicit limitation rather than pretending a match. |

Potential discovery mechanisms include:

- runtime resource catalogs and symbolic URIs;
- repository `SKILL.md` packages discovered by an Agent Skills-compatible client;
- provider-supported project, user, plugin, or organization skill registries;
- an explicitly supplied skill archive or directory.

The mechanism MUST be verified for the active platform. A filename's presence alone does not prove that the current runtime discovered or activated it.

## Entrypoint loading

When a matching Skill is selected:

1. Resolve the exact declared name.
2. Read the entrypoint before applying the Skill.
3. Prefer symbolic/runtime paths such as:

```text
skills://<skill-name>/skill.md
```

when the platform exposes them.
4. For filesystem Agent Skills, use the platform-discovered package and its canonical `SKILL.md`; do not guess a mount path.
5. Read only the referenced modules/resources needed for the task.
6. Follow declared dependency ordering and stop conditions.
7. Verify required scripts/tools exist before invocation.
8. Preserve a concise load ledger: skill name, entrypoint, relevant resources, purpose, and outcome.

Do not paste or inject the full Skill library into context.

## Selection precedence

Use this order among available Skills:

1. Explicit user-selected Skill whose scope matches the request.
2. Skill with primary ownership of the requested artifact/outcome.
3. More specific domain or tool Skill over a generic reasoning or orchestration Skill.
4. Repository-local Skill over a generic user/global Skill when the repository-local Skill is applicable and compatible.
5. Current active/version-compatible Skill over scaffold, template, deprecated, or unavailable content.
6. Lowest context and execution cost among equally capable, equally authoritative choices.

Do not select a Skill solely because its name contains a prompt keyword.

## Suitability gate

Before activation, confirm:

- the requested outcome falls inside the Skill's declared scope;
- required inputs and tools are available;
- the Skill does not conflict with a higher-priority rule;
- the Skill version/status is usable;
- the Skill's source and platform assumptions match the task;
- activation provides material value over direct execution.

Do not invoke a complex platform Skill for a trivial task when the Skill's own suitability guidance says not to.

## Multiple-Skill composition

Use multiple Skills only when each has a distinct, necessary ownership boundary.

Define:

| Role | Responsibility |
| --- | --- |
| Primary Skill | Owns the requested outcome and final workflow |
| Supporting Skill | Supplies a bounded method, domain fact set, format, verification, or tool integration |
| Router/orchestrator | Resolves ordering and handoffs when the active platform/package declares one |

Composition rules:

- Name one primary Skill.
- State the support boundary for every additional Skill.
- Load the minimum relevant modules from each.
- Resolve conflicting requirements by `AGENTS.md` precedence and explicit scope.
- Do not allow lateral routing loops or repeated mutual invocation.
- Use one validation owner for the integrated result.
- Do not treat duplicate recommendations from several Skills as independent evidence.

Example conceptual composition:

```text
document-engineering (primary outcome)
  + markdown (syntax and linting)
  + formal-logic (consistency review)
  + cognition (alternate-path and evidence-tier review)
```

Each Skill remains inside its declared boundary.

## Resource and dependency loading

- Load references, examples, templates, scripts, and plugins only when the entrypoint or current task requires them.
- Follow progressive disclosure: discovery metadata first, entrypoint second, selected resource third.
- Do not execute a bundled script merely because it exists.
- Inspect script purpose, inputs, writes, dependencies, and failure behavior before execution.
- Use the repository/environment-defined interpreter and security policy.
- Treat external network, account, and credential dependencies as separately authorized capabilities.
- Do not replace an unavailable required validator with an unverified approximation and still claim Skill completion.

## Tools versus Skills

- A Skill supplies procedure and domain capability; a tool performs an operation.
- Use a live connector/tool for authoritative account or service data when available and permitted; do not let a static reference Skill shadow it.
- Use the Skill to select, constrain, validate, and interpret tool use when that is within scope.
- Verify both the Skill contract and tool result.
- Tool availability does not grant authorization to call it.

## Unavailable or failed Skill

When a required Skill is unavailable, unreadable, incompatible, or fails:

1. identify the exact missing Skill/resource/tool and attempted resolution;
2. determine whether a safe direct or adjacent-skill path exists;
3. use a fallback only when it preserves user intent, security, evidence, and output quality;
4. label the fallback as direct reasoning or alternate tooling, not as Skill execution;
5. mark dependent validation `NOT PERFORMED` when it cannot run;
6. do not install, create, modify, or substitute a Skill without the applicable authority.

## Exact-name and path discipline

- Preserve canonical Skill names and case.
- Use the exact resource URI or filesystem path returned by discovery.
- Do not infer a plugin slug or directory from a display name.
- Do not use opaque IDs as a substitute for an unavailable attached file or Skill.
- Do not hard-code machine mount paths in portable rules.
- When an entrypoint is lowercase `skill.md` rather than `SKILL.md`, use the platform-reported path; do not normalize by assumption.

## Execution evidence

A Skill may be reported as invoked only when at least one of the following is observed:

- the platform Skill tool reports activation;
- the entrypoint was read through the supported resource mechanism;
- a provider reports the skill as active;
- the task explicitly supplied and authorized the skill content and it was applied.

The report SHOULD include:

```text
skill name
entrypoint or activation mechanism
resources actually loaded
required tools/scripts actually run
validation actually performed
limitations or unresolved dependencies
```

Do not claim that a Skill ran when it did not. Do not say “the Skill validated” when only its prose was read.

## Post-execution validation

After applying a Skill:

1. verify the output contract and task acceptance criteria;
2. run the Skill's mandatory validation path when available;
3. verify every claimed source, command, artifact, and result;
4. check cross-Skill consistency and repository rules;
5. inspect changed paths and transient artifacts;
6. report failures, skipped steps, and uncertainty accurately;
7. confirm the Skill did not expand authority or leak sensitive content.

Skill activation is not completion evidence.

## Provider notes

### OpenAI/Codex or ChatGPT resource runtimes

- Use the exposed Skill catalog and resource mechanism.
- When a runtime exposes `skills://<name>/skill.md`, read that entrypoint before execution.
- Follow platform routing instructions; do not enumerate or search for Skills when the current request does not plausibly match one.
- Repository-local Agent Skills may use `.agents/skills/<skill-name>/SKILL.md` when current Codex documentation and the repository establish that location.

### Claude Code

- Claude Code discovers Skills through its documented project, user, plugin, and additional-directory mechanisms.
- The Skill description controls automatic relevance matching; the full body loads on activation.
- Claude-specific frontmatter, subagent, hook, path, and tool controls are provider extensions and MUST NOT be treated as portable Agent Skills fields.

### Devin

- Devin discovers repository Skills through current documented locations, with `.agents/skills/<skill-name>/SKILL.md` as the recommended portable location.
- Devin sees Skill discovery metadata at session start and loads the body when invoked.
- Verify current product constraints, including invocation and active-Skill behavior, rather than generalizing them to other clients.

## Cross-references

- Instruction precedence and rule ownership: `AGENTS.md`

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI: Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Claude Agent SDK: Skills](https://code.claude.com/docs/en/agent-sdk/skills)
- [Devin Skills](https://docs.devin.ai/product-guides/skills)

## Lineage and migration

This file preserves `v1/skills.md` requirements to use relevant explicitly defined Skills, rank by relevance, and never fabricate names. V3 replaces “invoke all matching Skills” with most-specific-first, minimum-required composition to prevent context overload and conflicting ownership. It adds entrypoint-first loading, symbolic path preference, provider boundaries, unavailable-skill handling, tool separation, and execution evidence.
