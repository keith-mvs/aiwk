---
title: Prompt Metadata Provenance Session Notes
generated_at: 2026-09-14
status: historical
scope: task-data
tracking: tracked
references: []
tags: [notes, session-log, non-governing]
---

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• ## Current Architecture

  The inspected repository contains only:

  - prompts/ corpus and management artifacts;
  - rules/;
  - .codex/rules/;
  - policy/configuration files.

  There is no prompt compiler, runtime metadata type, persistence/database layer, API schema, frontend consumer, or test suite implementing task_inputs. No references to task_inputs, composes_path, compose_path, or equivalent composition metadata exist in executable code.

  Therefore:

  - task_inputs has no current runtime meaning in this repository.
  - composes_path has no pre-existing implementation.
  - Prompt composition is represented only conceptually in prompt text and composes_with front matter.

  ## Task Inputs

  No implementation was possible because no metadata producer or consumer exists.

  The existing prompt corpus declares task-level inputs in YAML front matter, but those are prompt contract declarations, not runtime-observed inputs. Converting them into concrete provenance would require inventing a compiler/runtime contract.

  ## Composes Path

  No implementation exists.

  The closest existing concept is composes_with, which lists related prompt IDs for workflow chaining. It is not an execution lineage and does not record actual composition traversal.

  ## Wiring

  No code path exists to wire:

  task/runtime data
  → compiler
  → metadata
  → persistence/API
  → consumer

  Adding fields to manifest.yaml or prompt front matter alone would not implement runtime metadata, persistence, serialization, or UI support.

  ## Validation

  Executed checks:

  - Full repository file inventory, including hidden and ignored paths.
  - Recursive search for all requested metadata and lineage terms.
  - Inspection of prompt manifest, index, and source map.
  - Confirmation that no compiler/runtime/database/API/frontend/test implementation exists.

  No implementation tests could be run because there is no implementation under test.

  ## Open Questions

  The repository does not establish:

  - the canonical metadata type;
  - the compiler/runtime ownership layer;
  - the persistence schema;
  - API serialization format;
  - UI/API consumers;
  - whether composition is linear, graph-based, or transform-based;
  - migration requirements for historical records.

  No files were modified. Implementing this safely requires the repository or package containing the actual prompt compiler/control-plane implementation.


› what is in the intent with the metadata (if there were a producer/consumer)


• The intended metadata is an observability contract between a prompt producer and its consumers.

  task_inputs means “what task data was actually used.”

  A compiler/runtime producer would populate it only from concrete consumed inputs, such as:

  task_inputs:
    - kind: user_text
      identifier: current_request
      role: task_request
      ordering: 1
    - kind: file
      identifier: src/auth/login.ts
      role: requested_source
      content_type: text
      ordering: 2
    - kind: tool_result
      identifier: test-run-42
      role: validation_evidence
      ordering: 3

  Consumers could use this to:

  - show provenance in a control-plane UI;
  - explain which files, attachments, retrievals, or parameters affected execution;
  - audit whether unrelated accessible data was used;
  - reproduce or review a task;
  - distinguish supplied data from system/developer instructions.

  It should not include merely available or considered-but-unused context, secrets, hidden instructions, or inferred facts without a concrete source.

  composes_path means “how the final prompt was assembled.”

  A producer would record the actual activated composition sequence or graph, using stable identifiers rather than hidden prompt text:

  composes_path:
    - id: system
      kind: base_component
      ordering: 1
    - id: scenario:developer_tech
      kind: scenario
      ordering: 2
    - id: method:instruction_prompt
      kind: method
      ordering: 3
    - id: context:tool_use
      kind: context
      ordering: 4
    - id: output:execution_report
      kind: output_contract
      ordering: 5
    - id: compiler:final_assembly
      kind: transform
      ordering: 6

  Consumers could use this to:

  - explain why a prompt had its structure;
  - inspect which rules, methods, templates, and context layers were activated;
  - debug routing or composition errors;
  - compare executions;
  - display lineage without exposing privileged prompt contents.

  The distinction is:

  task_inputs   = task-data provenance
  composes_path = prompt-assembly provenance

  A requested source file may appear in task_inputs but not composes_path. Conversely, a compiler template or system component may appear in composes_path without being task data.

  The producer must record observed execution, not hypothetical routing. The consumer should treat missing fields in historical records as “unknown/not recorded,” not as empty proof that nothing was used.


› the consumer being the prompt compiler? ("C:\Users\kjfle\Projects\aplexon"; "C:\Users\kjfle\Projects\aplexon-e"; )


• I’ll verify the two referenced repositories directly to distinguish the metadata producer from its consumers. The key question is whether the compiler constructs these fields, receives them from an upstream control plane, or both.

• Ran $roots = @('C:\Users\kjfle\Projects\aplexon','C:\Users\kjfle\Projects\aplexon-e'); foreach ($root in $roots) { Write-Output "=== $root ==="; if (Test-Path -LiteralPath $root) { rg -n --hidden -S "task_inputs|composes_path|compose_path|composition_path|prompt compiler|prompt_compiler|metadata" -g '!\.git/**' -g '!node_modules/**' -g '!vendor/**' $root | Select-Object -First 200 } else { Write-Output 'MISSING' } }
  └ (no output)

• Ran Get-Item -LiteralPath 'C:\Users\kjfle\Projects\aplexon','C:\Users\kjfle\Projects\aplexon-e' -ErrorAction SilentlyContinue | Select-Object FullName,Exists; Get-ChildItem -LiteralPath 'C:\Users\kjfle\Projects' -Force | Select-Object Name,FullName
  └
    FullName                                       Exists
    … +26 lines (ctrl + t to view transcript)
    C:\Users\kjfle\Projects\aplexon.code-workspace


• Ran Get-ChildItem -LiteralPath 'C:\Users\kjfle\Projects\aplexon','C:\Users\kjfle\Projects\aplexon-e' -Force | Select-Object FullName,Name,Mode; rg -n --hidden -S "task_inputs|composes_path|compose_path|composition_path" 'C:\Users\kjfle\Projects\aplexon' 'C:\Users\kjfle\Projects\aplexon-e' -g '!node_modules/**' -g '!vendor/**' -g '!\.git/**'
  └
    FullName                                                 Name                     Mode
    … +55 lines (ctrl + t to view transcript)
    C:\Users\kjfle\Projects\aplexon-e\README.md              README.md                -a---


• Ran rg -n --hidden -S "PromptMetadata|prompt metadata|compiled_prompt|compiler|composition|task input|task-input|provenance|lineage" 'C:\Users\kjfle\Projects\aplexon\app' 'C:\Users\kjfle\Projects\aplexon\gpt' 'C:\Users\kjfle\Projects\aplexon\tests' 'C:\Users\kjfle\Projects\aplexon-e\src' 'C:\Users\kjfle\Projects\aplexon-e\tests' -g '!node_modules/**' -g '!\.venv/**' -g '!bin/**' -g '!obj/**' | Select-Object -First 300
  └ C:\Users\kjfle\Projects\aplexon\tests\conftest.py:76:    # NIM call. To exercise compiler behavior over a *specific* body, use the
    C:\Users\kjfle\Projects\aplexon\tests\conftest.py:78:    # (which the compiler now ignores and overwrites).
    … +296 lines (ctrl + t to view transcript)
    C:\Users\kjfle\Projects\aplexon\app\scoring\dimensions\reproducibility.py:181:    The obj-bound ``score`` wrapper derives provenance from the run's actual
    C:\Users\kjfle\Projects\aplexon\app\scoring\dimensions\reproducibility.py:202:    exec_manifest = extract_manifest(provenance or "")

• Ran rg -n --hidden -S "task_inputs|task_input|input_data|compiled_by_gpt|template_version|provenance|composition|lineage" 'C:\Users\kjfle\Projects\aplexon\app\modules' 'C:\Users\kjfle\Projects\aplexon\app\storage' 'C:\Users\kjfle\Projects\aplexon\app\api' 'C:\Users\kjfle\Projects\aplexon\tests' -g '!\.venv/**' | Select-Object -First 300
  └ C:\Users\kjfle\Projects\aplexon\app\storage\repository.py:14:from app.storage import provenance
    C:\Users\kjfle\Projects\aplexon\app\storage\repository.py:78:    ("input_data", "context"),
    … +296 lines (ctrl + t to view transcript)
    C:\Users\kjfle\Projects\aplexon\tests\test_kpi_scorer.py:224:        compiled_by_gpt=cbg,
    C:\Users\kjfle\Projects\aplexon\tests\test_kpi_projection.py:68:        task=Task(raw_input=raw, compiled_by_gpt=CANONICAL_PROMPT),

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Not exactly. In the two repositories, the prompt compiler is primarily the producer of compilation metadata, while it is a consumer of task data.

  The flow is better represented as:

  API/task request
    → task model and input_data
    → compiler
    → compiled prompt + compilation metadata
    → persistence
    → API/dashboard/replay/scoring consumers

  In aplexon:

  - app/modules/compiler.py consumes task.raw_input, task options, obj.input_data, repository context, attachments, and generated template data.
  - It produces the compiled prompt and existing metadata such as template_version, dynamic-input information, compiler provenance, and related fields.
  - app/storage/repository.py and the database persistence layer consume that result and store provenance.
  - API/dashboard/replay/scoring code consumes the persisted metadata.

  So the intended placement would be:

  task_inputs:
    compiler input provenance
    → recorded by compiler
    → persisted and exposed to consumers

  composes_path:
    compiler assembly provenance
    → recorded by compiler as it activates sections/components
    → persisted and exposed to consumers

  The compiler may read an input collection such as obj.input_data, but that is not the same as the metadata field task_inputs.

  For example:

  obj.input_data["repo_context"]

  is compiler/runtime task data.

  A derived metadata entry such as:

  task_inputs:
    - kind: repository_context
      identifier: repo_context
      role: compiler_input

  would be provenance describing what the compiler actually consumed.

  Likewise, composes_path should describe the compiler’s actual assembly path, for example:

  composes_path:
    - compiler:input-normalization
    - compiler:section-generation
    - compiler:dynamic-input-binding
    - compiler:substitution
    - compiler:canonical-validation
    - compiler:final-assembly

  The exact nodes must come from the actual compiler stages. It should not be populated by the consumer, and it should not be inferred from composes_with, which is only a declared prompt-chain relationship.

  For aplexon-e, the same distinction applies:

  - PromptCompiler and related generation/context builders are producer-side components.
  - CompilationResult, persistence/transport layers, diagnostics, dashboards, replay tooling, and tests are consumer-side surfaces.
  - Existing InputArtifact and ProvenanceRecord concepts may provide reusable shapes for task_inputs, but they should not automatically be treated as equivalent to composes_path.

  So: the compiler consumes task inputs and produces metadata about both consumed inputs and composition lineage; persistence/API/UI/replay layers consume that metadata.


› none of the skills are being invoked automatically


• Correct. The current .prompt files only describe skill-routing behavior; they do not cause the host runtime to invoke skills.

  Automatic invocation requires an actual dispatcher integration:

  task request
  → task classifier
  → repository/rule resolver
  → skill catalog matcher
  → skill invocation
  → prompt compiler
  → compiled prompt + metadata

  At present:

  - aiwk/prompts contains declarative prompt files.
  - aiwk/skills has no repository-local skill implementation.
  - The available Codex skills are runtime capabilities exposed by the host, not callable through prompt text alone.
  - aplexon’s compiler can select or record a skill identifier only if an explicit adapter/dispatcher is added; it cannot invoke Codex skills merely because a prompt says “select the most specific skill.”

  Therefore the correct metadata semantics should distinguish:

  skill_routing:
    selected:
      - id: requirements-engineering
        status: requested
    invoked:
      - id: requirements-engineering
        status: confirmed
    unavailable:
      - id: some-skill
        status: not_available

  A prompt must never claim invoked based on selection or filename presence.

  If automatic invocation is required, the implementation belongs in the compiler/control-plane runtime, with:

  - a skill-catalog adapter;
  - deterministic matching and tie-breaking;
  - explicit invocation;
  - unavailable/failure handling;
  - invocation evidence;
  - propagation into compilation metadata;
  - tests for selected, invoked, unavailable, and fallback paths.

  The current prompt corpus can enforce the decision procedure, but it cannot itself provide automatic skill execution.

• Context compacted


› save this verbatim to a markdown in the repo root (aiuwka)


• Clarifying save text and path

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Specify the exact text to save and the filename you want.

  Also confirm the target root: I’m in C:\Users\kjfle\Projects\aiwk, not aiuwka. If aiuwka was a typo, I can save it in the repo root here.

To continue this session, run codex resume 01a04fe4-db40-7062-99c3-bcb045694f9a

⚠ The mnemo-team MCP server is not logged in. Run `codex mcp login mnemo-team`.

⚠ MCP startup incomplete (failed: mnemo-team)


› put this login verbatim in a markdown saved to the repo root


⚠ Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.

• I need the exact text you want saved. I also need a filename.

  If you meant the current repo root, I’m in C:\Users\kjfle\Projects\aiwk and can write the markdown there once you provide the content.
Token usage: total=767,808 input=687,190 (+ 9,506,048 cached) output=80,618 (reasoning 15,542)
To continue this session, run codex resume 01a050c3-377b-7853-b632-0309162bda6b
PS C:\Users\kjfle\Projects\aiwk>
