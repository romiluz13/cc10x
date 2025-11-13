# Orchestrator Enforcement Mechanisms

All CRITICAL enforcement rules, validation gates, and compliance checks for the cc10x orchestrator.

## CRITICAL ENFORCEMENT - READ THIS FIRST

**🚨 BYPASS PREVENTION - DO NOT WRITE CODE DIRECTLY 🚨**

**CRITICAL RULES** (Violation = Incomplete Results):

1. **DO NOT write code directly** - You MUST invoke subagents instead:
   - BUILD workflow: component-builder → code-reviewer → integration-verifier
   - REVIEW workflow: analysis subagents → code-reviewer (if changes) → integration-verifier (if integration)
   - PLAN workflow: planning-architecture-risk → planning-design-deployment
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
- [ ] Phase 5.5: Context Preservation complete (session summary created)
- [ ] Actions Taken section complete (ALL phases documented)
- [ ] Skills Inventory Check passed
- [ ] Subagents Inventory Check passed
- [ ] Memory integration used (patterns queried before complexity, stored after completion)
- [ ] Web fetch integration used (if external APIs/libraries mentioned)
- [ ] Pre-Final-Report Validation passed (see VALIDATION.md)

**If validation fails**: STOP final report generation, complete missing items, re-run all validations, then proceed.

### Automatic Validation Execution

**When**: These checks run automatically at each validation point above.

**How**:

1. Read Actions Taken section
2. Verify required items present
3. If ANY item missing → STOP workflow, report missing items, force correction
4. Re-validate after correction
5. Only proceed when ALL items pass

**Enforcement**: Workflow CANNOT proceed past validation point until ALL checks pass.

## Strict Mode Enforcement

**CRITICAL**: Strict Mode is enabled by default. Workflow aborts if any validation fails.

**Enforcement Points**:

1. **Phase 0 Enforcement**:
   - Workflow aborts if Phase 0 not completed FIRST
   - Workflow aborts if functionality analysis incomplete
   - Workflow aborts if gate check fails

2. **Phase 5.5 Enforcement**:
   - Workflow aborts if Phase 5.5 not completed before Phase 6
   - Workflow aborts if session summary file missing
   - Workflow aborts if session summary incomplete (missing required sections)
   - Phase 5.5 Completion Checklist must pass before proceeding

3. **Skills Loading Enforcement**:
   - Workflow aborts if Actions Taken section missing required skills
   - Workflow aborts if any required skill not loaded (unless user explicitly skipped)
   - Workflow aborts if conditional skill should be loaded but missing (detection logic matched)
   - Skills Inventory Check must pass before proceeding

4. **Subagents Invocation Enforcement**:
   - Workflow aborts if Actions Taken section missing required subagents
   - Workflow aborts if any required subagent not invoked (unless skip condition met)
   - Workflow aborts if subagent should be invoked but missing (skip condition NOT met)
   - Subagents Inventory Check must pass before proceeding

5. **Phase Transition Enforcement**:
   - Workflow aborts if any phase skipped without documentation
   - Workflow aborts if phase completion checklist not verified
   - Workflow aborts if gate check fails
   - All phase transitions require explicit checklist completion

6. **Final Report Enforcement**:
   - Workflow aborts if Pre-Final-Report Validation fails
   - Workflow aborts if Actions Taken validation fails
   - Workflow aborts if any required section missing
   - All audits must pass before presenting final report

**Error Recovery**:

- When Strict Mode enforcement triggers:
  - Report: "CRITICAL: Strict Mode enforcement failed. Missing: {list}"
  - Use Error Recovery Protocol
  - Options: Fix missing items / Abort workflow / Disable Strict Mode (user approval required)
  - Wait for user decision before proceeding

**CRITICAL**: Strict Mode cannot be disabled without explicit user approval. Default is enabled.

When Strict Mode is enabled:

- Workflow aborts immediately if any validation step fails
- No partial results are accepted
- All evidence must be provided before proceeding
- Error Recovery Protocol is triggered on any validation failure

## Error Recovery Protocol

**Error Recovery Decision Tree**:

```
Error occurred?
├─ Skill loading failed?
│   ├─ File missing?
│   │   └─ YES → Report error, offer: Retry / Continue without / Abort
│   ├─ Parse error?
│   │   └─ YES → Report error, offer: Retry / Continue without / Abort
│   └─ Unknown error?
│       └─ YES → Report error, offer: Retry / Continue without / Abort
├─ Subagent invocation failed?
│   ├─ Subagent missing?
│   │   └─ YES → Report error, offer: Skip / Abort
│   ├─ Output invalid?
│   │   └─ YES → Report error, offer: Retry / Request correction / Continue
│   └─ Execution error?
│       └─ YES → Report error, offer: Retry / Skip / Abort
└─ Workflow execution failed?
    ├─ Phase 0 incomplete?
    │   └─ YES → Complete Phase 0, then retry
    ├─ Validation failed?
    │   └─ YES → Fix issues, then retry
    └─ Unknown error?
        └─ YES → Report error, offer: Retry / Abort
```

When any component fails, provide:

1. **Context**: What was attempted (with evidence - file paths, commands run, error messages)
2. **Problem**: What failed (specific error, exit code, or failure point)
3. **Options**: Clear choices with implications:
   - **Retry**: Attempt again (if transient error likely)
   - **Continue without {component}**: Proceed with reduced functionality (if optional)
   - **Abort workflow**: Stop and restart (if critical failure)
   - **Custom**: User provides alternative instructions
4. **Impact**: What each choice means:
   - Retry: May succeed, adds time
   - Continue: Workflow proceeds but missing {component} outputs
   - Abort: Loses progress, starts fresh
5. **Default**: Recommended action (usually "Abort" for critical failures, "Retry" for transient)

**Error Recovery Checklists**:

**Checklist 1: Skill Loading Failed**

- [ ] Error detected (skill file missing, parse error, unknown error)
- [ ] Identify error type (file missing / parse error / unknown)
- [ ] Select recovery path (Retry / Continue without / Abort)
- [ ] Execute recovery action
- [ ] Validate recovery success (skill loaded / workflow continues / workflow aborted)
- [ ] Continue workflow or abort

**Checklist 2: Subagent Invocation Failed**

- [ ] Error detected (subagent missing / output invalid / execution error)
- [ ] Identify error type (missing / invalid output / execution error)
- [ ] Select recovery path (Skip / Retry / Request correction / Abort)
- [ ] Execute recovery action
- [ ] Validate recovery success (subagent skipped / retried / corrected / workflow aborted)
- [ ] Continue workflow or abort

**Checklist 3: Workflow Execution Failed**

- [ ] Error detected (Phase 0 incomplete / validation failed / unknown error)
- [ ] Identify error type (Phase 0 incomplete / validation failed / unknown)
- [ ] Select recovery path (Complete Phase 0 / Fix issues / Retry / Abort)
- [ ] Execute recovery action
- [ ] Validate recovery success (Phase 0 completed / issues fixed / workflow retried / workflow aborted)
- [ ] Continue workflow or abort

**Error Recovery Timeout**:

- **Timeout Duration**: 5 minutes waiting for user response
- **Timeout Behavior**:
  - Critical failures (workflow missing, skill loading failed): **Abort workflow** (default)
  - Transient failures (network error, file lock): **Retry once** (default)
  - Optional failures (subagent missing): **Continue without component** (default)
- **Timeout Notification**: "No response after 5 minutes. Taking default action: {action}. Workflow {status}."
- **Timeout Logging**: Log timeout event to `.claude/memory/workflow_history.json` with timestamp and default action taken
- Never fabricate outputs for missing agents or skipped steps.
- Wait for explicit user decision before proceeding (do not assume).
- After timeout, proceed with default action and log the decision.
