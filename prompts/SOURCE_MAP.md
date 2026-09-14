# Source Map and Completeness Record

## Scope

The source was read in place and was not modified. Generated outputs are confined to `prompts/**`. This map distinguishes direct source evidence from normalization and corpus design decisions.

## Completeness Gate

| Source file | Bytes | Lines | SHA-256 | Type | Read result | Disposition |
| --- | ---: | ---: | --- | --- | --- | --- |
| `prompt_corpus.json` | 13,269,850 | 98,814 | `A69034D7F9A2DAC826F64C64EF7260084168941C0BE225A75E64BA573CC76612` | JSON run corpus | Fully parsed and recursively traversed | Primary task-intent evidence |
| `prompt_library_analysis.json` | 77,806 | 3,050 | `1C7710074A79E14C378713230E8F3B57240BD55DE466AF1828322D603EC25352` | JSON analysis | Fully parsed and recursively traversed | Secondary analysis and cross-check |
| `prompt_library_analysis.md` | 31,498 | 631 | `BC155A73F89DE911518A2E0D19B8AD8891EBF3C872F5723D3A3CBFEF5F454C20` | Markdown report | Fully read top to bottom | Secondary narrative and template evidence |
| `prompt_library_query_strategy.md` | 2,107 | 55 | `DE8E2A527CEBB5A77630F3CB1DAC2DB324720967DE4C0ECC6A91AABD4293CCE9` | Markdown/SQL reference | Fully read top to bottom | `REFERENCE_ONLY`; duplicated in the analysis report |
| `prompt_template_library.yaml` | 20,183 | 677 | `2CDFD606FD9F7887BF18AD22A1D6D1CA4B75B0877DCFF1C6A4A97A140F64371E` | YAML template library | Fully read top to bottom | Template and composition evidence |

- Files discovered: 5.
- Files fully read: 5.
- Files excluded from reading: 0.
- Inaccessible, corrupt, binary, or unsafe files: 0.
- Unexamined source material: 0.
- NUL bytes: 0 in every source file.

## Inventory Annotations

All paths below are relative to the authoritative source root.

| Relative path | Extension | High-level semantic purpose | Likely reusable category | Repository-specific content | Duplication/overlap candidates |
| --- | --- | --- | --- | --- | --- |
| `prompt_corpus.json` | `.json` | Run-level raw requests, compiled/substituted prompts, criteria, section bodies, execution metadata, and KPI data | All normalized task domains; primary evidence | High: repository names, local paths, product APIs, request IDs, and task instances | Exact/near-duplicate requests; repeated canonical scaffolds; renderer and repository-name variants |
| `prompt_library_analysis.json` | `.json` | Structured aggregate analysis, reusable component inventory, template library, and retrieval strategy | Prompt engineering and corpus maintenance | Medium: original control-plane schema and source module names | Structured counterpart of the Markdown analysis and YAML templates |
| `prompt_library_analysis.md` | `.md` | Human-readable coverage, patterns, trends, templates, and query strategy | Prompt engineering and corpus maintenance | Medium: original database/table/module names | Narrative rendering of the analysis JSON; embeds the standalone query strategy and YAML template content |
| `prompt_library_query_strategy.md` | `.md` | SQL retrieval/update guidance for the original run database | Reference-only retrieval maintenance | High: original database tables and JSON paths | Duplicate of section 5 in `prompt_library_analysis.md` |
| `prompt_template_library.yaml` | `.yaml` | Canonical/concise/technical prompt scaffolds, system layers, renderers, and composition rules | Prompt compilation and execution contracts | Medium: original module and control-plane identities | Overlaps template sections in both analysis files; style variants are near-duplicates |

## Full-Corpus Traversal

`EXPLICIT_SOURCE_EVIDENCE`:

- Corpus records: 1,247.
- Nested corpus objects: 7,482; arrays: 12,654; string leaves: 34,832; string characters: 11,112,684.
- Analysis JSON objects: 113; arrays: 571; string leaves: 972; string characters: 34,035.
- Non-empty raw requests: 1,246; exact unique raw requests: 1,062; normalized unique raw requests: 1,051.
- Non-empty compiled prompts: 1,243; exact unique compiled prompts: 1,203; normalized unique compiled prompts: 1,202.
- One failed record has no raw request. Its compiled backlog-remediation task was read and classified from compiled content.

These counts come from complete JSON parses and recursive value traversal. Filenames, source summaries, and retrieval rankings were not used as substitutes for reading the corpus.

## Semantic Census

The following counts are multi-label because a single request may combine discovery, mutation, validation, and reporting.

| Reusable intent | Matching records | Unique raw requests | Normalized prompt coverage |
| --- | ---: | ---: | --- |
| Prompt engineering | 766 | 700 | `prompt.compile-task`, `prompt.maintain-corpus` |
| Implementation/build | 533 | 497 | `repo.implement-change`, `repo.execute-work-item` |
| Repository discovery | 498 | 455 | `repo.discover-context`, `repo.audit-structure` |
| Codebase analysis/review | 334 | 310 | `repo.analyze-codebase`, `repo.review-code-change` |
| Documentation | 265 | 255 | `repo.update-documentation`, `repo.maintain-changelog` |
| Architecture/design | 219 | 202 | `repo.assess-architecture` |
| Testing/validation | 196 | 179 | `repo.add-regression-coverage`, `repo.validate-change` |
| Rules/policy | 144 | 141 | `repo.engineer-policy` |
| Root-cause/debugging | 141 | 136 | `repo.diagnose-root-cause`, `repo.remediate-defect` |
| Skills engineering | 141 | 135 | `repo.engineer-agent-skill` |
| Dependency management | 134 | 128 | `repo.manage-dependency` |
| Corrective action | 130 | 123 | `repo.remediate-defect` |
| Refactoring/migration | 121 | 111 | `repo.refactor-code`, `repo.migrate-artifacts` |
| Code review | 118 | 100 | `repo.review-code-change` |
| Performance | 114 | 111 | `repo.investigate-performance` |
| Git/worktree | 114 | 104 | `repo.manage-worktree`, `repo.create-commit`, `repo.publish-remote-changes` |
| Cleanup/maintenance | 82 | 79 | `repo.clean-repository` |
| Configuration/environment | 74 | 71 | `repo.change-configuration` |
| Release/publication | 58 | 55 | `repo.assess-release-readiness`, `repo.publish-release` |
| Security review | 36 | 35 | `repo.review-security` |

## Evidence and Reusability Classification

| Source behavior | Classification | Evidence class | Corpus treatment |
| --- | --- | --- | --- |
| Repeated canonical execution scaffold | `GENERIC_REUSABLE` | `EXPLICIT_SOURCE_EVIDENCE` | Condensed into explicit input, authority, workflow, evidence, completion, and output contracts in every prompt. |
| Requests naming a repository, path, tool, schema, or work item | `GENERIC_WITH_PARAMETERS` or `REPOSITORY_SPECIFIC_BUT_GENERALIZABLE` | `DERIVED_NORMALIZATION` | Replace names and paths with declared inputs; retain workflow semantics. |
| Exact repeated raw requests and compiled scaffolds | `DUPLICATE` | `EXPLICIT_SOURCE_EVIDENCE` | One semantic workflow retained; occurrence counts recorded above. |
| Case, spelling, format, output-renderer, and repository-name variations | `VARIANT` | `DERIVED_NORMALIZATION` | Merge when authority, deliverable, and workflow are equivalent. |
| Earlier incomplete section layouts and redundant fallback styles | `SUPERSEDED` | `BOUNDED_INFERENCE` | Do not preserve as separate prompts; retain only useful contracts confirmed by later templates and repeated runs. |
| Product-specific control-plane API calls, tunnel probes, UUID lookups, and local absolute paths | `REPOSITORY_SPECIFIC_NOT_PORTABLE` | `EXPLICIT_SOURCE_EVIDENCE` | Excluded from executable prompts; no endpoint, account, repository name, or machine path retained. |
| Image/music fallback templates, greetings, arithmetic, thermodynamics, marketing, career, and other non-software examples | `REFERENCE_ONLY` | `EXPLICIT_SOURCE_EVIDENCE` | Used only to confirm general formatting behavior; omitted from this software-engineering corpus. |
| Taxonomy, stage vocabulary, authority levels, prompt IDs, and routing tie-breaks | Not a source requirement | `CORPUS_DESIGN` | Added to make the normalized corpus deterministic and discoverable. |

## Conflict Resolution

- Source variants alternate between deliverable-only output and reporting execution evidence. The normalized prompts require the requested artifact plus a concise evidence report when repository actions occur. This is `CORPUS_DESIGN` informed by repeated source acceptance language.
- Source executor text sometimes assumes text-only execution while many tasks require file and command access. Normalized prompts require capability honesty: act only when tools and authority exist, otherwise mark the action `NOT PERFORMED` or blocked.
- Source requests sometimes instruct destructive or remote actions directly. Normalized prompts separate those actions behind explicit authority levels and preflight gates.
- Source templates use `<TBD>` as an uncertainty sentinel. Normalized prompts retain `<TBD: reason>` only for material unknowns that cannot be safely discovered; they do not use it to conceal incomplete execution.

## Deduplication Decisions

- Repository audit, codebase audit, and broad review variants were split only where the deliverable differs: structure, implementation behavior, architecture, code change, or security.
- Fix, repair, remediation, and regression-remediation variants share one causal defect workflow, with regression coverage and validation as composable prompts.
- Implementation and work-item execution remain distinct: one owns a code change; the other owns lifecycle progression and work-record reconciliation.
- Commit, remote push, and release publication remain distinct because each grants materially different authority.
- Documentation updates and changelog maintenance remain distinct because changelogs have versioning and user-visible classification contracts.
- Generic prompt compilation and whole-corpus maintenance remain distinct because the latter requires inventory, source mapping, deduplication, and routing validation.

## Portability Check

Generated `.prompt` files contain no source repository names, source hostnames, user names, drive letters, UNC paths, request UUIDs, or product-specific APIs. Repository locations are discovered at runtime and all external or remote actions require explicit target identity and authority.
