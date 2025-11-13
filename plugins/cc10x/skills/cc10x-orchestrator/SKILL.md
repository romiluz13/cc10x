---
name: cc10x-orchestrator
description: Use when user request contains workflow keywords (plan/design/architect/roadmap/strategy, build/implement/create/write/code/develop/make, review/audit/analyze/assess/evaluate/inspect/examine, debug/fix/error/bug/investigate/failure/issue/problem/troubleshoot/diagnose, validate/verify/check/confirm). AUTO-LOAD on these keywords. CRITICAL: MANDATORY entry for ALL code tasks. Coordinates subagents - do NOT write directly. Phase 0: Functionality Analysis first. Enforces TDD (RED→GREEN→REFACTOR), Actions Taken tracking, memory/web fetch. DO NOT bypass validation.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# cc10x Orchestrator Skill - Functionality First

## 🚨 EXECUTION MODE - THIS IS NOT DOCUMENTATION 🚨

**CRITICAL**: This skill file contains EXECUTABLE INSTRUCTIONS, not reference documentation.

**YOU MUST:**

1. **Load this skill using Skill tool** - NOT just Read tool
   - Use: `Skill(skill="cc10x:cc10x-orchestrator")` or equivalent
   - Do NOT just read the file - you must ACTIVATE the skill
2. **Execute workflows as step-by-step instructions** - NOT as summaries
   - When workflow says "Run this bash command" → YOU MUST RUN IT
   - When workflow says "DO NOT proceed until" → YOU MUST STOP AND VALIDATE
   - When workflow says "You MUST invoke subagents" → YOU MUST USE Task TOOL
3. **Treat CRITICAL markers as hard stops** - NOT suggestions
   - CRITICAL = MANDATORY = MUST DO = HARD STOP IF SKIPPED
4. **Execute validation gates literally** - NOT conceptually
   - Check each item in checklist
   - Run validation commands
   - Verify evidence exists
   - Do NOT proceed until ALL checks pass

**IF YOU READ THIS AS DOCUMENTATION INSTEAD OF EXECUTING IT:**

- ❌ You will skip mandatory steps
- ❌ You will bypass validation gates
- ❌ You will write code directly instead of invoking subagents
- ❌ Workflow will fail validation

**CORRECT APPROACH:**

1. Load orchestrator skill → Skill activates workflow
2. Execute each phase literally → Follow step-by-step
3. Run all bash commands → Capture output
4. Invoke all subagents → Use Task tool
5. Validate at each gate → Check checklist items

## Quick Start

The orchestrator automatically loads when you detect workflow keywords, then coordinates the appropriate workflow.

**Example:**

1. **User says**: "Build a file upload feature"
2. **Detect keyword**: "build" → Load orchestrator skill
3. **Orchestrator activates**: BUILD workflow
4. **Phase 0**: Complete functionality analysis (user flow, system flow)
5. **Phase 2**: Load required skills (code-generation, test-driven-development)
6. **Phase 3**: Invoke subagents (component-builder → code-reviewer → integration-verifier)

**Result:** Coordinated workflow execution with functionality-first approach.

## 🚨 AUTO-LOAD TRIGGERS - READ THIS FIRST 🚨

**This skill MUST be loaded automatically when user request contains ANY of these keywords:**

**PLAN**: plan, planning, planner, plan a, plan the, plan for, design, designing, designer, design a, design the, architect, architecture, architectural, system design, roadmap, road map, strategy, strategic planning, feature planning, project planning, implementation plan

**BUILD**: build, building, builder, build a, build the, implement, implementation, implementing, create, creating, create a, create the, write code, write a, write the, coding, code, develop, development, developing, developer, make, making, make a, make the, add feature, implement feature, build feature

**REVIEW**: review, reviewing, reviewer, review this, review the, audit, auditing, auditor, audit this, analyze, analysis, analyzing, analyze this, assess, assessment, assessing, assess this, evaluate, evaluation, evaluating, evaluate this, inspect, inspection, inspecting, inspect this, examine, examination, examining, examine this

**DEBUG**: debug, debugging, debugger, debug this, fix, fixing, fix this, fix the, fix a, error, errors, error in, error with, bug, bugs, bug in, bug with, investigate, investigation, investigating, failure, failures, failed, failing, broken, broke, break, breaking, issue, issues, issue with, problem, problems, troubleshoot, troubleshooting, diagnose, diagnosis

**VALIDATE**: validate, validation, validating, validate this, verify, verification, verifying, verify this, check, checking, check this, check the, confirm implementation, alignment check, consistency check

**If user request contains ANY keyword above → LOAD THIS SKILL IMMEDIATELY**

## CRITICAL ENFORCEMENT - READ THIS FIRST

**🚨 BYPASS PREVENTION - DO NOT WRITE CODE DIRECTLY 🚨**

**CRITICAL RULES** (Violation = Incomplete Results):

1. **DO NOT write code directly** - You MUST invoke subagents instead:
   - BUILD workflow: component-builder → code-reviewer → integration-verifier
   - REVIEW workflow: analysis subagents → code-reviewer (if changes) → integration-verifier (if integration)
   - PLAN workflow: planner
   - DEBUG workflow: bug-investigator → code-reviewer → integration-verifier
   - VALIDATE workflow: Direct analysis (no subagents)

2. **DO NOT skip TDD cycle** - For BUILD workflow, you MUST follow RED → GREEN → REFACTOR:
   - RED: Write failing test first, capture output with exit code
   - GREEN: Minimal implementation, run test, capture exit code
   - REFACTOR: Clean up while tests green, verify exit code
   - Do NOT mark component complete without seeing test fail then pass

3. **DO NOT skip Actions Taken tracking** - You MUST maintain Actions Taken section in real-time:
   - Update IMMEDIATELY after each activation (skill loading, subagent invocation, phase completion)
   - Never proceed to next phase without updating Actions Taken
   - Verify Actions Taken updated before each phase transition
   - Before final report, verify ALL phases documented in Actions Taken

4. **DO NOT skip inventory checks** - You MUST perform:
   - Skills Inventory Check before Phase 3 (verify ALL required skills loaded)
   - Subagents Inventory Check before Phase 4 (verify ALL required subagents invoked)
   - If ANY missing, STOP workflow execution, fix immediately, re-validate

5. **DO NOT skip memory integration** - You MUST use:
   - Query patterns before complexity scoring (load patterns.json ONCE, cache for workflow duration)
   - Store patterns after workflow completion (validate first, update accuracy)
   - Store user preferences (explicit only, never inferred)
   - Store workflow checkpoints

6. **DO NOT skip web fetch integration** - You MUST use:
   - When external APIs/libraries/frameworks mentioned, fetch documentation
   - Use question-based prompts (not raw content requests)
   - Check cache first, use cache if valid, fetch if needed
   - Cache results with appropriate TTL

**If you violate ANY of these rules, the workflow will FAIL validation and you will be forced to correct before proceeding.**

**See ENFORCEMENT.md for detailed enforcement mechanisms and validation gates.**

## TL;DR Quick Checklist

**CRITICAL**: Complete ALL items below. Skipping any item will cause workflow validation to FAIL.

- [ ] **LOAD ORCHESTRATOR FIRST** - This skill MUST be loaded before any code tasks
- [ ] Detect user intent (review/plan/build/debug/validate) using keyword matching
- [ ] Execute Phase 0: Functionality Analysis FIRST (understand user/admin/system flows, verify functionality works)
- [ ] Execute Phase 0: Context Preset Detection (automatically detect task type and load appropriate preset)
- [ ] Load required skills in parallel (if independent) or sequentially (if dependencies exist)
  - [ ] Load conditional skills based on detection logic (UI detected → load frontend-patterns, etc.)
- [ ] **UPDATE Actions Taken** - Document skills loaded IMMEDIATELY after loading
- [ ] **PERFORM Skills Inventory Check** - Verify ALL required skills loaded before Phase 3
- [ ] **DO NOT write code directly** - Invoke subagents instead (component-builder → code-reviewer → integration-verifier)
- [ ] **FOR BUILD workflow** - Follow TDD cycle: RED (failing test) → GREEN (minimal code) → REFACTOR (clean up)
- [ ] Invoke subagents based on conditions and dependencies (check skip conditions, analyze dependencies)
- [ ] **UPDATE Actions Taken** - Document subagents invoked IMMEDIATELY after invocation
- [ ] **PERFORM Subagents Inventory Check** - Verify ALL required subagents invoked before Phase 4
- [ ] **USE memory integration** - Query patterns before complexity, store patterns after completion
- [ ] **USE web fetch integration** - Fetch external docs when APIs/libraries mentioned
- [ ] Validate outputs before proceeding (check format, evidence, file:line citations)
- [ ] Generate verification summary with evidence (commands run, exit codes, artifacts)
- [ ] Use Error Recovery Protocol if any component fails (context → problem → options → impact → default)
- [ ] **VALIDATE Actions Taken** - Verify ALL phases documented before final report

## Guardrails

**CRITICAL**: These guardrails MUST be followed in all workflows. Violations lead to incomplete or incorrect results.

- **Functionality First**: Always understand functionality (user flows, admin flows, system flows) BEFORE applying specialized checks (security, quality, performance, UX, accessibility, architecture). Verify functionality works BEFORE checking other concerns.

- **Evidence Required**: Every claim must include file:line citations or command outputs. No assertions without proof. Use `file:line` format for code references, include exit codes for commands.

- **No Placeholders**: Never use "TODO", "TBD", "FIXME" in critical sections (functionality analysis, findings, recommendations, verification summaries). Complete all required sections before proceeding.

- **Validation Mandatory**: Validate all outputs before proceeding to next phase. Check format, evidence, file:line citations, exit codes. Do NOT proceed until validation passes.

- **Scope Awareness**: Keep changes tightly scoped to requested outcome. Don't expand beyond user's request unless explicitly asked. Focus on what was requested, not what "could be improved."

- **Phase 0 Enforcement**: Phase 0: Functionality Analysis MUST be completed before any skill loading or subagent dispatching. This is non-negotiable.

- **Error Recovery**: Always use Error Recovery Protocol when failures occur. Provide context, problem, options, impact, and default action. Wait for user decision before proceeding.

## Runtime Compliance Checks

**CRITICAL**: These validation gates are executed automatically at key checkpoints. If validation fails, workflow STOPS and you MUST fix issues before proceeding.

### Validation Point 1: Before Phase 2 (Skills Loading)

**Checklist** (ALL must pass):

- [ ] Phase 0: Functionality Analysis complete (user flow, admin flow if applicable, system flow documented)
- [ ] Actions Taken section exists and Phase 0 documented
- [ ] Gate checks passed (if applicable)

**If validation fails**: STOP workflow, complete missing items, re-validate, then proceed.

### Validation Point 2: Before Phase 3 (Subagent Invocation)

**Checklist** (ALL must pass):

- [ ] Phase 2: Skills loaded complete
- [ ] Actions Taken section updated with ALL required skills listed
- [ ] Skills Inventory Check passed (ALL required skills loaded, conditional skills loaded IF detected)
- [ ] Each skill marked as "loaded successfully" or "failed to load" in Actions Taken

**If validation fails**: STOP workflow, load missing skills, update Actions Taken, re-run Skills Inventory Check, then proceed.

### Validation Point 3: Before Phase 4 (Synthesis)

**Checklist** (ALL must pass):

- [ ] Phase 3: Subagents invoked complete
- [ ] Actions Taken section updated with ALL required subagents listed
- [ ] Subagents Inventory Check passed (ALL required subagents invoked, execution mode documented)
- [ ] Each subagent marked as "invoked successfully" or "skipped" with reason in Actions Taken
- [ ] For BUILD workflow: TDD cycle evidence present (RED → GREEN → REFACTOR with exit codes)

**If validation fails**: STOP workflow, invoke missing subagents, update Actions Taken, re-run Subagents Inventory Check, then proceed.

### Validation Point 4: Before Final Report

**Checklist** (ALL must pass):

- [ ] ALL workflow phases completed
- [ ] Actions Taken section complete (ALL phases documented)
- [ ] Skills Inventory Check passed
- [ ] Subagents Inventory Check passed
- [ ] Memory integration used (patterns queried before complexity, stored after completion)
- [ ] Web fetch integration used (if external APIs/libraries mentioned)
- [ ] Pre-Final-Report Validation passed (see VALIDATION.md)

**If validation fails**: STOP final report generation, complete missing items, re-run all validations, then proceed.

**See VALIDATION.md for detailed validation checklists and final report format.**

## Purpose

Coordinate the five cc10x workflows using the official Anthropic model-invoked skills pattern. The orchestrator:

- Identifies the requested outcome (review, plan, build, debug, validate).
- Loads only workflow skills that exist in `plugins/cc10x/skills/`.
- Analyzes dependencies and parallelizes subagents where safe (read-only, independent, isolated contexts).
- Falls back to sequential execution for operations with dependencies or shared state.
- Prompts for explicit user approval before continuing past any complexity gates.
- Routes all completion claims through the `verification-before-completion` skill.

## Supported Workflows

- **review** -> `review-workflow`
- **plan** -> `planning-workflow`
- **build** -> `build-workflow`
- **debug** -> `debug-workflow`
- **validate** -> `VALIDATION workflow` (see `workflows/validate.md`)

If a user combines intents (for example "review then plan"), run each workflow in the order requested and confirm between phases. Never promise simultaneous execution or reference agents that are not bundled with the plugin.

## Before Any Task

**Context Checklist** (complete ALL before proceeding):

- [ ] Read user request and understand intent (what does user want to accomplish?)
- [ ] Check existing workflows/skills/subagents (verify what's available in `plugins/cc10x/skills/` and `plugins/cc10x/subagents/`)
- [ ] Load functionality analysis template (`plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`)
- [ ] Identify code type (UI/API/Utility/Integration/Database/Configuration/CLI/Background Job) if applicable
- [ ] Run Phase 0: Functionality Analysis (understand user/admin/system flows, verify functionality works)

**CRITICAL**: Do NOT proceed to workflow execution until ALL items above are checked. If any item is incomplete, complete it before proceeding.

## Detailed Reference Files

For detailed information, see these progressive disclosure files:

- **ENFORCEMENT.md**: All CRITICAL enforcement rules, validation gates, and compliance checks
- **WORKFLOWS.md**: Workflow coordination, skill loading optimization, and subagent invocation rules
- **VALIDATION.md**: Validation checklists, evidence requirements, and final report formatting
- **INTEGRATION.md**: Memory integration, web fetch integration, and context editing strategies
- **COMPLEXITY.md**: Complexity gate and rubric for plan/build workflows
- **PARALLEL.md**: Dependency analysis and parallel execution safety validation
- **REFERENCE.md**: Tool usage guides, search guidance, and reference materials

**CRITICAL**: All detailed instructions in these files are MANDATORY. They are not optional reference material - they contain executable instructions that must be followed.

- Orchestration Coordination Matrix: `audit/orchestration-coordination-matrix.md` (complete skill/subagent activation matrix)
- Anthropic Context Editing: https://docs.claude.com/en/docs/build-with-claude/context-editing
- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool

## Troubleshooting

**Common Issues:**

1. **Orchestrator not loaded when workflow keywords detected**
   - **Symptom**: Workflow keywords present but orchestrator not activated
   - **Cause**: Skill discovery didn't detect keywords or orchestrator not loaded
   - **Fix**: Manually load orchestrator skill, verify keyword detection
   - **Prevention**: Always check orchestrator first in skill-discovery

2. **Phase 0 (Functionality Analysis) skipped**
   - **Symptom**: Workflow proceeds without functionality analysis
   - **Cause**: Bypassed Phase 0 enforcement
   - **Fix**: Complete Phase 0 first, document user/admin/system flows
   - **Prevention**: Never skip Phase 0 - it's mandatory

3. **Subagents not invoked (code written directly)**
   - **Symptom**: Code written directly instead of using subagents
   - **Cause**: Bypassed orchestrator subagent dispatch
   - **Fix**: Use Task tool to invoke subagents, don't write code directly
   - **Prevention**: Always invoke subagents through orchestrator

4. **Actions Taken not updated**
   - **Symptom**: Actions Taken section missing or incomplete
   - **Cause**: Didn't update Actions Taken after each phase
   - **Fix**: Update Actions Taken immediately after each activation
   - **Prevention**: Always update Actions Taken in real-time

**If issues persist:**

- Verify orchestrator was loaded first
- Check that Phase 0 was completed
- Ensure subagents were invoked, not bypassed
- Review ENFORCEMENT.md for validation gates
- Check VALIDATION.md for compliance requirements

## References

- Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`
- Verification guardrails: `plugins/cc10x/skills/verification-before-completion/SKILL.md`
- Orchestration Coordination Matrix: `audit/orchestration-coordination-matrix.md` (complete skill/subagent activation matrix)
- Anthropic Context Editing: https://docs.claude.com/en/docs/build-with-claude/context-editing
- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool
