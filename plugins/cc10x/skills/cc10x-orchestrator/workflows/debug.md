# DEBUG Workflow - Root Cause First

**CRITICAL**: This workflow MUST be activated through cc10x-orchestrator. Do NOT execute this workflow directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

**🚨 CRITICAL ENFORCEMENT - DO NOT WRITE CODE DIRECTLY 🚨**

**MANDATORY RULES** (Violation = Workflow Failure):

1. **DO NOT write code directly** - You MUST invoke subagents sequentially per bug:
   - bug-investigator → code-reviewer → integration-verifier
   - Read subagent's SUBAGENT.md before invoking
   - Verify subagent exists before invoking
   - Check skip conditions before invoking

2. **DO NOT skip Actions Taken tracking** - Update Actions Taken IMMEDIATELY after:
   - Each skill loaded (mark as "loaded successfully" or "failed to load")
   - Each subagent invoked (mark as "invoked successfully" or "skipped" with reason)
   - Each phase completed (mark phase as complete)
   - Never proceed to next phase without updating Actions Taken

3. **DO NOT skip inventory checks** - You MUST perform:
   - Skills Inventory Check before Phase 3 (verify ALL required skills loaded)
   - Subagents Inventory Check before Phase 4 (verify ALL required subagents invoked)
   - If ANY missing, STOP workflow, fix immediately, re-validate

4. **DO NOT skip memory integration** - You MUST:
   - Query patterns before complexity scoring (load patterns.json ONCE, cache for workflow duration)
   - Store patterns after workflow completion (validate first, update accuracy)

5. **DO NOT skip web fetch integration** - You MUST:
   - When external APIs/libraries/frameworks mentioned, fetch documentation
   - Use question-based prompts (not raw content requests)
   - Check cache first, use cache if valid, fetch if needed

**If you violate ANY of these rules, Phase 4 validation will FAIL and you will be forced to correct before proceeding.**

**Triggered by:** User requests help investigating bugs, errors, or unexpected behaviour.

## WHEN/HOW/WHY - DEBUG Workflow

### WHEN to Use This Workflow

**Keywords that trigger DEBUG workflow:**

- debug, debugging, debugger, debug this
- fix, fixing, fix this, fix the, fix a
- error, errors, error in, error with
- bug, bugs, bug in, bug with
- investigate, investigation, investigating
- failure, failures, failed, failing
- broken, broke, break, breaking
- issue, issues, issue with, problem, problems
- troubleshoot, troubleshooting, diagnose, diagnosis

**Example user requests:**

- "debug this memory leak"
- "fix this error: [error message]"
- "investigate why this is broken"
- "troubleshoot authentication failure"

### HOW Orchestrator Selects This Workflow

**Detection Process:**

1. User says keyword like "debug" → Orchestrator skill loads automatically (via description keywords)
2. Orchestrator scans user request for workflow keywords
3. If "debug", "fix", "error", "bug", "investigate", "failure", "broken", "issue", "problem", "troubleshoot", or "diagnose" detected → DEBUG workflow selected
4. Orchestrator activates this workflow file
5. Workflow executes phases: Functionality Analysis → Intake → Log Analysis → Bug Investigation → Fix → Regression Test → Report

**Decision Tree:**

```
User request contains "debug"/"fix"/"error"/"bug"/"investigate"/"failure"/"broken"/"issue"/"problem"/"troubleshoot"/"diagnose"?
├─ YES → DEBUG workflow
└─ NO → Check other workflow keywords
```

### WHY Use DEBUG Workflow vs Others

**Use DEBUG workflow when:**

- Code is broken or not working as expected
- You need to find root cause of bugs
- You need to fix errors
- You need to investigate failures

**DEBUG vs PLAN:**

- DEBUG: Fix broken code (reactive)
- PLAN: Design solutions (proactive)

**DEBUG vs BUILD:**

- DEBUG: Fix existing code (backward)
- BUILD: Write new code (forward)

**DEBUG vs REVIEW:**

- DEBUG: Fix specific bugs (focused)
- REVIEW: General code analysis (broad)

**DEBUG vs VALIDATE:**

- DEBUG: Fix broken functionality (repair)
- VALIDATE: Verify implementation matches plan (verification)

## TL;DR Quick Checklist

**CRITICAL**: Complete ALL items below. Skipping any item will cause workflow validation to FAIL.

- [ ] Complete Phase 0: Functionality Analysis FIRST (understand expected vs observed functionality, document broken flows)
- [ ] Gather bug details using Ask Questions tool if needed
- [ ] Check logs FIRST before loading skills (LOG FIRST principle)
- [ ] Load required skills in parallel (systematic-debugging, log-analysis-patterns, root-cause-analysis)
- [ ] **UPDATE Actions Taken** - Document ALL skills loaded IMMEDIATELY after loading
- [ ] **PERFORM Skills Inventory Check** - Verify ALL required skills loaded before Phase 3
- [ ] **DO NOT write code directly** - Invoke subagents sequentially per bug: bug-investigator → code-reviewer → integration-verifier
- [ ] **UPDATE Actions Taken** - Document ALL subagents invoked IMMEDIATELY after invocation
- [ ] **PERFORM Subagents Inventory Check** - Verify ALL required subagents invoked before Phase 4
- [ ] Verify fix works and functionality restored before claiming completion
- [ ] Generate debug report with functionality verification FIRST, then root cause analysis

## Guardrails

**CRITICAL**: These guardrails MUST be followed in the Debug workflow. Violations lead to incomplete or incorrect debugging.

- **Functionality First**: Always understand what functionality SHOULD work (expected behavior) and what is actually broken (observed behavior) BEFORE investigating bugs. Map observed to expected flows.

- **Evidence Required**: Every bug finding must include file:line citations, error messages, logs, or reproduction steps. No assertions without proof.

- **LOG FIRST**: Check logs FIRST before loading skills or investigating deeply. Logs often contain the answer.

- **Root Cause Focus**: Find the root cause, not just symptoms. Fix the underlying issue, not just the surface problem.

- **Scope Awareness**: Debug only what was requested. Don't expand beyond the requested scope unless explicitly asked.

## Search Guidance

**CRITICAL**: Use the right tool for each search task in the Debug workflow.

**Phase 0 - Functionality Analysis**:

- **Discovery**: Use `Glob` to find relevant files (`Glob("src/**/*error*.{ts,tsx}")` for error handling)
- **Content Search**: Use `Grep` to find error patterns (`Grep("throw|Error|catch")` for error handling)
- **Detail Reading**: Use `Read` to read specific files (`Read("src/api/auth.ts")` for broken functionality)
- **Example**: Understanding broken authentication flow:
  - Step 1: `Glob("**/*auth*.{ts,tsx}")` → Find auth-related files
  - Step 2: `Grep("function.*login|function.*authenticate")` → Find auth functions
  - Step 3: `Read("src/api/auth.ts")` → Read implementation

**Phase 1 - Intake**:

- **Log Discovery**: Use `Glob` to find log files (`Glob("**/*.log")` or `Glob("logs/**/*")`)
- **Error Patterns**: Use `Grep` to find error messages (`Grep("ERROR|FATAL|Exception")`)

**Phase 2 - Investigation**:

- **Error Locations**: Use `Grep` to find error handling (`Grep("try|catch|throw")`)
- **Function Calls**: Use `Grep` to find function invocations (`Grep("function.*name")`)
- **Dependency Analysis**: Use `Grep` to find imports (`Grep("import.*from")` to map dependencies)

**Anti-Patterns**:

- ❌ Using `Read` to search for patterns (use `Grep` instead)
- ❌ Using `Grep` to find files by name (use `Glob` instead)
- ❌ Reading entire large files when only a section is needed (use `Read` with offset/limit)

## Phase 0 - Functionality Analysis (MANDATORY)

**CRITICAL**: This phase MUST be completed before any intake, skill loading, or subagent dispatching. Understanding what functionality is broken is the foundation for all debugging activities.

**Purpose**: Understand what functionality should work (user flows, admin flows, system flows) and what is actually broken before investigating bugs.

**Task Tool Usage** (phase tracking):

- Create tasks for all workflow phases at start:
  ```
  Task: Create tasks for workflow phases
  - Phase 0: Functionality Analysis (in_progress)
  - Phase 1: Intake (pending)
  - Phase 2: Shared Skills (pending)
  - Phase 3: Bug Investigation Loop (pending)
  - Phase 4: Consolidation (pending)
  - Phase 5: Verification Summary (pending)
  - Phase 6: Report (pending)
  ```
- Update task status as phases complete:
  ```
  Task: Update Phase 0 status to completed
  Task: Update Phase 1 status to in_progress
  ```

**Process**:

1. **Load Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
2. **Analyze Expected Functionality**:
   - Read user bug report and any provided context
   - Understand what functionality SHOULD work (expected behavior)
   - Document expected user flows, admin flows (if applicable), and system flows
   - Identify integration flows if external systems are involved
3. **Analyze Broken Functionality**:
   - Understand what is actually broken (observed behavior)
   - Document where functionality fails (which step in flow)
   - Identify error messages, logs, or symptoms
4. **Output**: Complete functionality analysis using template format:

   ```markdown
   ## Functionality Analysis

   ### What Functionality is Broken?

   [Clear description of broken functionality]

   ### Expected User Flow (What Should Work)

   1. [Step 1: User action]
   2. [Step 2: System response]
   3. [Step 3: User sees result]
      ...

   ### Expected Admin Flow (if applicable)

   [Similar structure]

   ### Expected System Flow (What Should Work)

   1. [Step 1: System receives input]
   2. [Step 2: System processes]
   3. [Step 3: System stores/transforms]
   4. [Step 4: System sends output]
      ...

   ### Observed Broken Behavior

   - [ ] User flow breaks at: [which step]
   - [ ] Admin flow breaks at: [which step, if applicable]
   - [ ] System flow breaks at: [which step]
   - [ ] Error messages: [list]
   - [ ] Logs: [relevant snippets]
   - [ ] Symptoms: [what user sees/experiences]
   ```

**Gate Check**: Before proceeding to Phase 1, ALL items below MUST be checked:

- [ ] Expected functionality documented (user flow, admin flow if applicable, system flow - what SHOULD work)
- [ ] Broken behavior documented (where it fails, which step in flow, error messages, logs, symptoms)
- [ ] Observed vs expected mapped (clear comparison of what should happen vs what actually happens)
- [ ] Reproduction steps identified (if available) OR limitation documented
- [ ] Template format followed (all required sections completed)
- [ ] Functionality clear and understood (no ambiguous requirements)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items above are checked. If any item is incomplete:

- Ask user: "Functionality unclear. Please clarify: What should work? What is broken? What are the expected user flows?"
- Do NOT proceed until functionality is understood and all gate check items are complete

**Display Success Message** (after Phase 0 completion):

```
✅ Phase 0 Complete: Functionality Analysis

Analyzed:
- Broken flows: [X] flows identified
- Expected vs observed: ✅ Documented
- Error symptoms: [Y] symptoms documented

Next: Proceeding to Phase 1 - Intake
```

**Ask Questions Tool Usage** (when functionality unclear):

- Use the askquestion tool to clarify requirements before proceeding
- Ask specific questions about functionality:
  - What are the specific user flows?
  - What are the acceptance criteria?
  - What are the constraints?
  - What are the dependencies?
- Proceed with functionality analysis using answers

**Example**:

```
Use the askquestion tool to clarify requirements:
- What are the specific user flows for this feature?
- What are the acceptance criteria?
- What are the technical constraints?
- What are the business constraints?
```

**Memory Integration** (optimized):

- **Store Failure Patterns**: After workflow completes, save successful failure analysis patterns to `.claude/memory/failure_modes.json` (only if fix validated successful)
- **Query Similar Failures**: Check `.claude/memory/failure_modes.json` for similar failure patterns (use semantic match, top 3 only)

## Phase 1 - Intake

**CRITICAL:** Phase 0 (Functionality Analysis) MUST be complete before proceeding.

**LOG FIRST Principle** (enhanced):

**Quick Log Access** (automatic detection):

**Detection Logic:**

1. **Check package.json for log scripts:**
   - `pnpm app:log`, `pnpm backend:log`, `pnpm typecheck:watch`
   - `npm run dev:log`, `npm run watch:logs`
   - Common patterns: `*:log`, `*:watch`, `*:monitor`

2. **If Log Scripts Found:**
   - Offer: "Would you like me to start log monitoring? (app logs, backend logs, typecheck)"
   - If yes → Run appropriate log command in background
   - Continue with existing LOG FIRST investigation
   - Integrate log output with bug investigation

3. **If No Log Scripts Found:**
   - Continue with existing LOG FIRST investigation (existing flow unchanged)

**Integration:**

- Log monitoring runs in background (non-blocking)
- Log output feeds into bug investigation
- Existing LOG FIRST principle remains unchanged
- LOG FIRST happens AFTER Phase 0 completion

**Memory Integration** (optimized):

- **Load Failure Modes Once**: Read `.claude/memory/failure_modes.json` ONCE, cache for workflow duration
- **Semantic Match**: Use `jq` + `grep` to match error_pattern (regex) against current error message
- **Top Matches Only**: Return top 3 failure modes with highest success_rate (>60%)
- **Fix Patterns**: Check `.claude/memory/patterns.json` for fix_patterns matching error type

**Bug Information Gathering**:

1. Gather reproduction steps, error messages, logs, and recent changes.
2. Confirm scope (single bug per run unless explicitly broadened).

**Ask Questions Tool Usage** (for bug clarification):

- If bug symptoms unclear, use the askquestion tool:
  - What are the exact steps to reproduce?
  - What is the expected behavior?
  - What is the actual behavior?
  - When did this start happening?
  - Are there any error messages?
- Proceed with debugging using answers

**External Resource Check** (smart Q&A caching):

- **Check Cache First**: Lookup {url, prompt} combinations in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - Create hash from `{url}_{prompt}` for each planned question
  - Error docs: 48h TTL
  - If cached and TTL valid → use cached answer (skip fetch)
  - If cached but expired → re-fetch with same prompt
  - If not cached → WebFetch with prompt and cache answer
- Check if debug needs external resources:
  - Error documentation? → Ask: "What does error [error code/message] mean and how do I fix it?"
  - Stack trace analysis? → Ask: "How do I troubleshoot [symptom] in [technology]? What are common causes?"
  - Library-specific issues? → Ask: "What are common errors in [library] and their solutions? How do I debug integration issues?"
- Ask user: "Should I fetch external debugging resources? Will ask {N} targeted questions. Found {M} in cache. Proceed? (yes/no)"

3. **Bug Classification**: Classify bug type before investigation:
   - **Reproducible**: Clear steps, consistent failure
   - **Intermittent**: Fails sometimes, unclear pattern
   - **Non-reproducible**: Cannot reproduce with given steps
   - **External**: Requires environment/data not available
   - **Performance**: Slow response, resource exhaustion
   - **Functional**: Wrong behavior, crash, error

**Action by Bug Type**:

- **Reproducible**: Proceed with standard workflow
- **Intermittent**: Add monitoring/logging, investigate patterns, estimate probability, may require multiple attempts
- **Non-reproducible**: Request more data (logs, environment, steps), pause investigation until data available
- **External**: Investigate external dependency, document limitation
- **Performance**: Focus on profiling, bottlenecks, resource usage (load performance-patterns skill)
- **Functional**: Focus on logic, state, data flow

**Multiple Bugs Handling**:

- If scope spans multiple independent failures, queue them and tackle serially unless the user approves separate runs.
- If bugs are NOT independent (related failures), investigate together as single root cause may affect multiple symptoms.

**Bug Independence Analysis**:

1. **Analyze Bug Relationships**:
   - Check if bugs share:
     - Same files (mutations conflict)
     - Same root cause (investigation overlap)
     - Same test suites (verification conflict)
     - Dependent fixes (fix A enables fix B)
2. **Execution Strategy**:

   **PARALLEL (Safe for Independent Bugs)**:
   - ✅ Different files (no mutation conflicts)
   - ✅ Different root causes (independent investigations)
   - ✅ Different test suites (no verification overlap)
   - ✅ Isolated subagent contexts
   - **Orchestrator dispatches bug-investigator subagents in parallel** (uses `parallel-agent-dispatch` skill)

   **SEQUENTIAL (Required for Related Bugs)**:
   - ❌ Same files (mutation conflicts)
   - ❌ Same root cause (investigation overlap)
   - ❌ Dependent fixes (fix B needs fix A)

3. **Parallel Dispatch Logic** (when bugs are independent):
   - **Load Skill**: Reference `parallel-agent-dispatch` skill for independence detection and coordination patterns
   - **Orchestrator Analysis**: Orchestrator analyzes bugs for independence using parallel-agent-dispatch skill patterns:
     - File overlap check (different files → independent)
     - Resource overlap check (different resources → independent)
     - Dependency check (no dependencies → independent)
     - State check (no shared state → independent)
   - **Parallel Dispatch**: If all checks pass → Orchestrator dispatches bug-investigator subagent for each independent bug concurrently
   - **Coordination**: Orchestrator tracks all subagents, collects results, verifies no conflicts
   - **Sequential Fallback**: If any check fails → Execute sequentially (existing behavior)

4. **Bug Execution Plan**:

   ```
   Bug Independence Graph:
   - Bug 1: file X, cause A → Independent
   - Bug 2: file Y, cause B → Independent (parallel with Bug 1)
   - Bug 3: file X, cause A → Related to Bug 1 (sequential after Bug 1)

   Execution Order:
   Phase 1 (Parallel): Bug 1 + Bug 2 (independent)
   Phase 2 (Sequential): Bug 3 (after Bug 1 completes, same file/root cause)
   ```

**Workflow State Persistence** (Checkpoint System):

- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/debug_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "debug",
    "phase": "Phase_2_Bug_Investigation_Loop",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "bugs": [{name, status, investigation_attempts, root_cause}],
      "investigation_history": [...],
      "fixes_applied": [...],
      "current_bug": "BugName"
    },
    "next_phase": "Phase_3_Consolidation"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/debug_*.json`
  2. Validate checkpoint state (bugs present, investigation valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}, Bug {name}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3 (after each bug), Phase 4, Phase 5 completion

**Context Restoration**:

- **If resuming after compaction or context is unclear**, use checkpoint system:
  - Read most recent checkpoint from `.claude/memory/workflow_state/debug_*.json`
  - If checkpoint exists: Restore state and continue from `next_phase`
  - If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

**Display Success Message** (after Phase 1 completion):

```
✅ Phase 1 Complete: Root Cause Analysis

Identified:
- Root cause: [description]
- Bug type: [type]
- Investigation: ✅ Complete

Next: Proceeding to Phase 2 - Shared Skills
```

## Phase 2 - Shared Skills

**Required Skills**:

- `project-context-understanding` - **MANDATORY** (understand project structure, dependencies, and conventions before debugging)
- `systematic-debugging`
- `log-analysis-patterns`
- `root-cause-analysis`
- `test-driven-development`
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external resources needed)

**Skill Loading Strategy**:

- Core 6 skills are independent (no dependencies between them)
- **Load all core skills in parallel** for faster initialization
- Conditional skills (performance-patterns, security-patterns, integration-patterns) added based on bug type, load in parallel when needed
- If conditional skill needed (web-fetch-integration), load conditionally but still in parallel with others

**Skill Loading Verification Protocol**:
For each skill above:

1. Read first 100 chars of `plugins/cc10x/skills/{skill-name}/SKILL.md` to verify file exists
2. Parse YAML frontmatter to verify valid format
3. Check body content exists (not empty)
4. If any verification fails:
   - Report immediately: "Skill '{name}' failed to load: {error details}"
   - Present options: Continue without {skill} / Abort workflow / Retry loading
   - Wait for user decision before proceeding
5. Document successfully loaded skills in Actions Taken section

**Bug Type Skill Selection**:

- For performance bugs: Also load `performance-patterns`
- For security-related bugs: Also load `security-patterns`
- For integration bugs: Also load `integration-patterns`
- For code quality bugs: Also load `code-quality-patterns` (complexity, maintainability, SOLID violations)
- For multiple independent bugs (3+): Also load `parallel-agent-dispatch` (orchestrator coordinates parallel subagent dispatch)

**Display Success Message** (after Phase 2 completion):

```
✅ Phase 2 Complete: Solution Design

Designed:
- Solutions: [X] solutions designed
- Risks assessed: [Y] risks identified
- Skills loaded: [Z] skills loaded

Next: Proceeding to Phase 3 - Bug Investigation Loop
```

## Phase 3 - Bug Investigation Loop

**Per-Bug Subagent Sequence** (ALWAYS SEQUENTIAL):

- bug-investigator → regression test → code-reviewer → integration-verifier
- Must remain sequential (each needs previous output)
- Parallelization applies BETWEEN bugs, not WITHIN bug investigation

For each identified bug:

**When to Invoke Subagents**:

- **INVOKE** - Bug needs investigation: Always invoke `bug-investigator` (required for systematic debugging)
- **INVOKE** - Fix implemented: After bug-investigator proposes fix, invoke `code-reviewer` (always for quality/security check)
- **INVOKE** - Integration risk: After review passes, invoke `integration-verifier` (always to prevent regressions)

**When NOT to Invoke Subagents**:

- **SKIP** - Investigation timeout exceeded: If 3 attempts to find root cause failed → Skip `bug-investigator` re-invocation, escalate to user with options
- **SKIP** - Bug not reproducible: If bug cannot be reproduced with given steps → Skip `bug-investigator`, request more data from user
- **SKIP** - Trivial fix (typo/comment): If bug is single-line typo or comment fix → Skip `code-reviewer` (no security/code quality risk), skip `integration-verifier` (no integration risk)
- **SKIP** - User explicitly skips review: If user says "skip review" or "just fix it" → Skip `code-reviewer`, proceed to integration check
- **SKIP** - User explicitly skips integration: If user says "skip integration check" → Skip `integration-verifier`, mark bug fixed
- **SKIP** - No code changes: If investigation determines bug is external (environment, dependency) → Skip all subagents, report finding to user

**Conflict Prevention**:

- **One bug per investigation**: Never invoke `bug-investigator` for multiple bugs simultaneously
- **Sequential flow**: Investigation → Fix → Review → Integration (never parallel)
- **Skip if blocked**: If bug-investigator fails, don't invoke code-reviewer or integration-verifier until investigation succeeds

**Default Sequence** (unless conditions above met):

1. Invoke `bug-investigator` with all context. Require:
   - Reproduction of the failure.
   - Collection of relevant logs/metrics (LOG FIRST).
   - Written hypothesis before implementing fixes.
   - Failing regression test proving the bug.
2. Once the fix is proposed, re-run the regression test to verify GREEN and document commands run.
3. Send the changes to `code-reviewer` for validation (quality, security, performance) (unless user skipped or trivial fix).
4. Use `integration-verifier` to confirm there are no regressions in the broader flow (unless user skipped or trivial fix).

File size sanity check: As fixes accumulate, if any modified file exceeds ~500 lines, propose a focused refactor/split plan (after green tests).

**Subagent Invocation Pattern** (per bug):

- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SUBAGENT.md`
- Read the subagent's SUBAGENT.md to load its process and output format.
- Provide the repro steps, logs, and scope from Phase 0.
- Require the specified outputs with file:line evidence and command outputs.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (root cause, evidence, fix, regression test)
    - [ ] File references include path:line where applicable
    - [ ] Commands included with exit codes (RED → GREEN proof)
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (root cause identified, fix provided)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
- **On failure or missing repro**: Use Error Recovery Protocol
  - If bug not reproducible: Request more data, pause investigation
  - If subagent fails: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Investigation Timeout** (CRITICAL):

- **Timeout Threshold**: 3 attempts to find root cause
- **Attempt Tracking**: Count investigation attempts per bug:
  - Attempt 1: Initial investigation (logs, tests, hypothesis)
  - Attempt 2: Deeper investigation (additional logging, more tests, refined hypothesis)
  - Attempt 3: Comprehensive investigation (all available data, multiple hypotheses)
- **Timeout Trigger**: After 3 attempts without root cause identification:
  1. Document all investigation attempts:
     ```
     Investigation Attempts (3/3):
     - Attempt 1: [logs checked, tests run, hypotheses tested]
     - Attempt 2: [additional investigation details]
     - Attempt 3: [comprehensive investigation details]
     ```
  2. Present escalation options:

     ```
     Investigation Timeout (3 attempts):
     Root cause not identified after 3 investigation attempts.

     Options:
     1. Add strategic logging → Capture bug when it occurs naturally
     2. Request more data → User provides environment details, logs, reproduction steps
     3. Skip investigation → Mark as "cannot reproduce, needs manual investigation"
     4. Escalate to user → User provides domain expertise or manual investigation
     ```

  3. **Wait for user decision** (with 5-minute timeout per orchestrator error recovery)
  4. **Document timeout**: Log to Actions Taken: "Investigation timeout after 3 attempts"

**Escalation Paths**:
If bug-investigator cannot determine root cause (before timeout):

1. Document investigation attempts:
   - Logs checked: [list]
   - Tests run: [list with results]
   - Hypotheses tested: [list with outcomes]
2. List remaining possibilities with probability estimates:
   - Hypothesis A: 60% probability - [reason]
   - Hypothesis B: 30% probability - [reason]
   - Hypothesis C: 10% probability - [reason]
3. Recommend next steps:
   - **Additional logging/monitoring**: Add strategic logging to capture bug when it occurs
   - **User-provided reproduction environment**: Request environment details (OS, dependencies, data, config)
   - **External dependency investigation**: Check external services, APIs, databases
   - **Escalation to domain expert**: Requires knowledge not in skills
4. Ask user which path to pursue (if not at timeout)

**External Dependency Handling**:
If bug investigation requires external services unavailable:

1. Check if service available: ping/health check
2. If unavailable:
   - **Option A**: Mock services (document limitation: "Investigation limited - external service unavailable")
   - **Option B**: Skip investigation, verify contract/structure only
   - **Option C**: Request user to provide test environment
3. Document approach chosen and limitations

**Debug Workflow Inventory Validation** (MANDATORY after Phase 3):

- [ ] bug-investigator documented for EACH bug in Actions Taken
- [ ] code-reviewer documented for EACH bug (unless skipped)
- [ ] integration-verifier documented for EACH bug (unless skipped)
- [ ] Sequential execution per bug documented
- [ ] Parallel execution between bugs documented (if independent)
- [ ] All subagent outputs validated
- [ ] No bug missing subagent sequence

**If ANY item missing**: STOP and invoke missing subagent immediately.

## Phase 4 - Consolidation

- Summarise root cause, fix, and verification evidence for each bug.
- List any follow-up work (monitoring, additional tests) recommended by the skills used.

**Display Success Message** (after Phase 4 completion):

```
✅ Phase 4 Complete: Solution Verification

Verified:
- Error resolved: ✅ Yes
- Tests passing: ✅ Yes
- Fix complete: ✅ Yes

Next: Proceeding to Phase 5 - Verification Summary
```

## Phase 5 - Verification Summary

**MANDATORY**: Use exact template:

```
## Verification Summary
Scope: <bugs investigated>
Bugs fixed: <list>
Criteria: <what was verified - reproduction, fix, regression prevention>
Commands:
- <command> -> exit <code>
- <command> -> exit <code>
Evidence:
- <log snippets showing bug>
- <test output showing RED then GREEN>
- <integration test results>
Residual risk: <items to monitor, edge cases not covered>
```

**Example**:

```
## Verification Summary
Scope: Cart null pointer exception
Bugs fixed: Cart crash when items array is null
Criteria: Bug reproduces, fix prevents crash, regression test passes
Commands:
- npm test test/cart.spec.ts -> exit 1 (RED - null pointer)
- Apply null check in src/cart.ts:85
- npm test test/cart.spec.ts -> exit 0 (GREEN)
- npm test test/integration/cart-flow.spec.ts -> exit 0
Evidence:
- Log: "TypeError: Cannot read property 'length' of null at cart.ts:42"
- Test: "should handle null items array" -> passes
Residual risk: Add e2e test for empty cart state
```

**Validation Gate** (before proceeding to Phase 6):

**CRITICAL**: Execute this bash command to verify fix is complete:

```bash
# Verify fix files exist
FIX_FILES=("src/path/to/fix.ts")  # Adjust based on actual fix files
MISSING_FILES=()

for file in "${FIX_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "Error: Missing fix files: ${MISSING_FILES[*]}"
    exit 1
else
    echo "✓ All fix files created"
fi

# Verify error no longer occurs (run original failing command)
ORIGINAL_COMMAND="npm test"  # Adjust based on actual failing command
if eval "$ORIGINAL_COMMAND" 2>&1 | grep -q "error\|Error\|ERROR\|failing\|FAIL"; then
    echo "Error: Original error still occurs after fix"
    exit 1
else
    echo "✓ Original error resolved"
fi
```

**CRITICAL**: Do NOT proceed to Phase 6 until bash command exits with code 0.

**Display Success Message** (after Phase 5 completion):

```
✅ Phase 5 Complete: Debug Complete

Completed:
- Issue fixed: ✅ Yes
- Files modified: [X] files
- Tests passing: ✅ Yes

Next: Debug workflow complete - Issue resolved
```

## Phase 6 - Report

**Before Reporting** (optimized memory):

- **Validate Fix Success**:
  - Did fix actually resolve the bug? (verify with tests/verification)
  - Track success: fixed successfully? (true/false)
- **Store Failure Mode** (only if fix validated successful):
  - Save to `.claude/memory/failure_modes.json` ONLY if fix worked
  - Format: `{error_pattern, root_causes: [{cause, fix, success_rate, occurrences, last_seen}]}`
  - If failure mode exists: update success_rate, increment occurrences, update last_seen
  - If success_rate < 60% after 5+ fixes → mark for deletion
- **Store Fix Pattern** (only validated):
  - Save fix approach ONLY if validated successful
  - Track success_rate across multiple uses
- **Auto-Delete Rules**:
  - Delete failure modes unused > 30 days
  - Delete failure modes with success_rate < 60%
- **Run Cleanup**: Execute memory cleanup script

## Quick Reference

**Phase Summary**:

- **Phase 0**: Functionality Analysis (MANDATORY FIRST) - Understand expected vs observed functionality, document broken flows
- **Phase 1**: Intake - Gather bug details using Ask Questions tool if needed
- **Phase 2**: Investigation - Check logs FIRST, load required skills, investigate bugs sequentially
- **Phase 3**: Root Cause Analysis - Find root cause, not just symptoms
- **Phase 4**: Consolidation - Consolidate findings
- **Phase 5**: Verification Summary - Verify fix works and functionality restored
- **Phase 6**: Report - Generate debug report with functionality verification FIRST

**Key Outputs**:

- Functionality analysis (expected vs observed flows)
- Bug findings with file:line citations
- Root cause analysis with evidence
- Fix verification with test results
- Debug report with evidence

**Validation Requirements**:

- [ ] Phase 0 complete (functionality analysis done, gate checks passed)
- [ ] Logs checked FIRST before deep investigation
- [ ] All required skills loaded successfully
- [ ] Bugs investigated sequentially per bug
- [ ] Root cause identified (not just symptoms)
- [ ] Fix verified and functionality restored
- [ ] Evidence provided for all claims (logs, file:line citations, test results)

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Debug Report

## Executive Summary

[2-3 sentences summarizing root cause, fix status, and overall resolution]

## Actions Taken

- Functionality analysis completed: [expected functionality documented, broken behavior documented]
- Skills loaded: systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development, verification-before-completion
- Subagents invoked: bug-investigator, code-reviewer, integration-verifier
- Bugs investigated: [list]
- Tools used: [Read, Edit, Write, Bash, Grep, Glob]

## Functionality Analysis

[Include complete functionality analysis from Phase 0]

## Findings / Decisions

### Bug {name}

- **Root Cause**: [what failed and why]
- **Evidence**: [log excerpts, stack traces, code paths]
- **Fix**: [what changed, file:line]
- **Regression Test**: [test name, file:line]
- **Verification**: [command outputs showing RED → GREEN]

### Reproduction

- Steps: [detailed reproduction steps]
- Environment: [OS, dependencies, config]
- Error Messages: [full error messages]
- Logs: [relevant log snippets]

### Investigation Timeline

- [Hypothesis 1]: [result]
- [Hypothesis 2]: [result]
- [Root Cause Found]: [explanation]

### Fix & Regression Test

- Changes: [file:line diffs summary]
- Tests Added: [list]
- GREEN Proof: [command outputs]

### Reviews & Integration

- code-reviewer findings: [resolved/open]
- integration-verifier scenarios: [pass/fail with logs]

## Verification Summary

[Use exact template from Phase 4]

## Recommendations / Next Steps

[Prioritized: Monitoring setup, additional tests, prevention measures]

## Open Questions / Assumptions

[If escalation needed, external dependencies unavailable, or assumptions made]
```

**Validation Before Presenting**:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes commands with exit codes
- [ ] Root cause clearly explained with evidence
- [ ] Regression test documented with RED → GREEN proof
- [ ] Reviews and integration status documented
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken

**Offer Optional Next Steps**:

- "Want a code review of the patch?" (without assuming consent)
- "Run review workflow on fixed code?" (without assuming consent)

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

**If Reproduction Cannot Be Established**:

1. **Context**: What was attempted (reproduction steps tried, logs checked)
2. **Problem**: Cannot reproduce bug with provided information
3. **Options**:
   - **Request more data**: User provides additional logs, environment details, or steps
   - **Add logging**: Add strategic logging to capture bug when it occurs
   - **Skip investigation**: Mark as "cannot reproduce" and document limitation
4. **Impact**: Explain what each choice means
5. **Default**: Request more data (ensures proper investigation)

**If Fix Fails Review/Integration**:

1. **Context**: What was attempted (fix applied, tests run)
2. **Problem**: Review rejects fix or integration test fails
3. **Options**:
   - **Return to bug-investigator**: Revise fix based on feedback
   - **Accept review concerns**: Document as risk or limitation
   - **Fix integration**: Update integration code
4. **Impact**: Explain what each choice means
5. **Default**: Return to bug-investigator (ensures quality)

**Critical Rules**:

- Never mark bugs as fixed without captured test or log evidence
- Never proceed without user decision when failure occurs
- Document all failures in Actions Taken section
- If bug cannot be reproduced after multiple attempts, escalate to user with options

## References

- Debugging discipline: `plugins/cc10x/skills/systematic-debugging/SKILL.md`
- Official guidance: `docs/reference/03-SUBAGENTS.md`, `docs/reference/04-SKILLS.md`
