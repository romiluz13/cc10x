# Shared Enforcement - All Workflows

**CRITICAL**: This file contains MANDATORY enforcement rules that apply to ALL workflows. Every workflow MUST reference this file and follow these rules.

## 🚨 EXECUTION MODE - THIS IS NOT DOCUMENTATION 🚨

**CRITICAL**: Workflow files contain EXECUTABLE INSTRUCTIONS, not reference documentation.

**YOU MUST EXECUTE WORKFLOWS STEP-BY-STEP:**

1. **This is an executable script** - NOT a reference guide
   - Each phase is a mandatory step to execute
   - Each checklist item must be checked literally
   - Each bash command must be run and output captured

2. **CRITICAL markers are hard stops** - NOT suggestions
   - "CRITICAL: Run this command" → YOU MUST RUN IT NOW
   - "DO NOT proceed until" → YOU MUST STOP AND VALIDATE
   - "MANDATORY" = MUST DO = HARD STOP IF SKIPPED

3. **Validation gates are mandatory checks** - NOT optional
   - Before Phase 3: Skills Inventory Check → YOU MUST RUN IT
   - Before Phase 4: Subagents Inventory Check → YOU MUST RUN IT
   - Each checklist item → YOU MUST VERIFY IT

4. **Subagent invocation is required** - NOT optional
   - "You MUST invoke [subagent]" → USE Task TOOL
   - Do NOT write code directly → INVOKE SUBAGENTS

**IF YOU READ THIS AS DOCUMENTATION:**

- ❌ You will summarize instead of executing
- ❌ You will skip mandatory bash commands
- ❌ You will skip validation gates
- ❌ You will write code directly instead of invoking subagents
- ❌ Workflow will fail validation

**CORRECT APPROACH:**

1. Orchestrator activates workflow → Execute Phase 0 FIRST
2. Execute each phase → Run all commands, capture output
3. Load skills → Verify each loaded
4. Invoke subagents → Use Task tool
5. Validate outputs → Check all evidence
6. Generate report → Include all evidence

**CRITICAL**: All workflows MUST be activated through cc10x-orchestrator. Do NOT execute workflows directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

## 🚨 CRITICAL ENFORCEMENT - DO NOT WRITE CODE DIRECTLY 🚨

**MANDATORY RULES** (Violation = Workflow Failure):

1. **DO NOT write code directly** - You MUST invoke subagents in sequence:
   - BUILD workflow: component-builder → code-reviewer → integration-verifier
   - REVIEW workflow: analysis subagents → code-reviewer (if changes) → integration-verifier (if integration)
   - PLAN workflow: planner
   - DEBUG workflow: bug-investigator → code-reviewer → integration-verifier
   - VALIDATE workflow: Direct analysis (no subagents)
   - Read subagent's SUBAGENT.md before invoking
   - Verify subagent exists before invoking
   - Check skip conditions before invoking

2. **DO NOT skip TDD cycle** - For BUILD workflow, component-builder MUST follow RED → GREEN → REFACTOR:
   - RED: Write failing test FIRST, run test, capture failing output with exit code
   - GREEN: Write minimal code to pass test, run test, capture passing output with exit code
   - REFACTOR: Clean up while keeping tests green, verify exit code still 0
   - Do NOT mark component complete without seeing test fail then pass

3. **DO NOT skip Actions Taken tracking** - Update Actions Taken IMMEDIATELY after:
   - Each skill loaded (mark as "loaded successfully" or "failed to load")
   - Each subagent invoked (mark as "invoked successfully" or "skipped" with reason)
   - Each phase completed (mark phase as complete)
   - Never proceed to next phase without updating Actions Taken

4. **DO NOT skip inventory checks** - You MUST perform:
   - Skills Inventory Check before Phase 3 (verify ALL required skills loaded)
   - Subagents Inventory Check before Phase 4 (verify ALL required subagents invoked)
   - If ANY missing, STOP workflow, fix immediately, re-validate

5. **DO NOT skip memory integration** - You MUST:
   - Query patterns before complexity scoring (load patterns.json ONCE, cache for workflow duration)
   - Store patterns after workflow completion (validate first, update accuracy)

6. **DO NOT skip web fetch integration** - You MUST:
   - When external APIs/libraries/frameworks mentioned, fetch documentation
   - Use question-based prompts (not raw content requests)
   - Check cache first, use cache if valid, fetch if needed

**If you violate ANY of these rules, Phase 4 validation will FAIL and you will be forced to correct before proceeding.**

## TL;DR Quick Checklist

**CRITICAL**: Complete ALL items below. Skipping any item will cause workflow validation to FAIL.

- [ ] **LOAD ORCHESTRATOR FIRST** - Orchestrator skill MUST be loaded before workflow execution
- [ ] Execute Phase 0: Functionality Analysis FIRST (understand user/admin/system flows, verify functionality works)
- [ ] Load required skills in parallel (if independent) or sequentially (if dependencies exist)
- [ ] **UPDATE Actions Taken** - Document skills loaded IMMEDIATELY after loading
- [ ] **PERFORM Skills Inventory Check** - Verify ALL required skills loaded before Phase 3
- [ ] **DO NOT write code directly** - Invoke subagents instead (workflow-specific sequence)
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
- [ ] Pre-Final-Report Validation passed (see orchestrator VALIDATION.md)

**If validation fails**: STOP final report generation, complete missing items, re-run all validations, then proceed.

**See orchestrator VALIDATION.md for detailed validation checklists and final report format.**
