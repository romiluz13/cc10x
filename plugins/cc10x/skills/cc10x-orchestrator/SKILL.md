---
name: cc10x-orchestrator
description: Primary orchestrator for cc10x with functionality-first approach. Interprets user intent and coordinates review, planning, build, and debug workflows. ALWAYS starts with functionality analysis (user flows, admin flows, system flows) before applying specialized checks. Honors focus requests, enforces evidence-first rules, and never invokes non-existent agents. Use for complex multi-step engineering tasks that need structured coordination.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# cc10x Orchestrator Skill - Functionality First

## TL;DR Quick Checklist

- [ ] Detect user intent (review/plan/build/debug/validate) using keyword matching
- [ ] Execute Phase 0: Functionality Analysis FIRST (understand user/admin/system flows, verify functionality works)
- [ ] Load required skills in parallel (if independent) or sequentially (if dependencies exist)
- [ ] Load conditional skills based on detection logic (UI detected → load ui-design, etc.)
- [ ] Invoke subagents based on conditions and dependencies (check skip conditions, analyze dependencies)
- [ ] Validate outputs before proceeding (check format, evidence, file:line citations)
- [ ] Generate verification summary with evidence (commands run, exit codes, artifacts)
- [ ] Use Error Recovery Protocol if any component fails (context → problem → options → impact → default)

## Guardrails

**CRITICAL**: These guardrails MUST be followed in all workflows. Violations lead to incomplete or incorrect results.

- **Functionality First**: Always understand functionality (user flows, admin flows, system flows) BEFORE applying specialized checks (security, quality, performance, UX, accessibility, architecture). Verify functionality works BEFORE checking other concerns.

- **Evidence Required**: Every claim must include file:line citations or command outputs. No assertions without proof. Use `file:line` format for code references, include exit codes for commands.

- **No Placeholders**: Never use "TODO", "TBD", "FIXME" in critical sections (functionality analysis, findings, recommendations, verification summaries). Complete all required sections before proceeding.

- **Validation Mandatory**: Validate all outputs before proceeding to next phase. Check format, evidence, file:line citations, exit codes. Do NOT proceed until validation passes.

- **Scope Awareness**: Keep changes tightly scoped to requested outcome. Don't expand beyond user's request unless explicitly asked. Focus on what was requested, not what "could be improved."

- **Phase 0 Enforcement**: Phase 0: Functionality Analysis MUST be completed before any skill loading or subagent dispatching. This is non-negotiable.

- **Error Recovery**: Always use Error Recovery Protocol when failures occur. Provide context, problem, options, impact, and default action. Wait for user decision before proceeding.

## Functionality First Mandate

**CRITICAL**: Every workflow MUST start with functionality analysis before applying specialized checks (security, quality, performance, UX, accessibility, architecture, etc.).

**Core Principle**: Understand what the code/feature is supposed to do (user flows, admin flows, system flows) and verify it works BEFORE checking other concerns.

**Mandatory First Step**: Before loading any skills or dispatching any subagents:

1. **Understand Functionality**: What does the user need? What are the user flows? Admin flows? System flows?
2. **Verify Functionality**: Does it work? Test if possible, verify with evidence.
3. **THEN Apply Specialized Checks**: Only after functionality is understood and verified, apply security, quality, performance, UX, accessibility, architecture checks.

**Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for standard format.

## Purpose

Coordinate the four cc10x workflows using the official Anthropic model-invoked skills pattern. The orchestrator:

- Identifies the requested outcome (review, plan, build, debug).
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

## Operation

1. **Functionality Analysis (MANDATORY FIRST STEP)**
   - **Before any workflow execution**: Complete functionality analysis using the functionality analysis template
   - **Load Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - **Analyze User Request**: Understand what functionality is needed (user flows, admin flows, system flows)
   - **Document Flows**: Document user flows, admin flows (if applicable), system flows, integration flows (if applicable)
   - **Verify Functionality**: If possible, verify functionality works (test, check logs, manual verification)
   - **Gate Check**: Do NOT proceed to workflow execution until functionality analysis is complete
   - **If Functionality Unclear**: Ask user: "Functionality unclear. Please clarify: What functionality is needed? What are the user flows?"
2. **Intent and Context Check**
   - **Intent Detection Decision Tree**: Match user request to workflow using visual decision tree:

     ```
     User request?
     ├─ Contains "review"/"audit"/"analyze"/"assess"/"evaluate"/"inspect"/"examine"?
     │   └─ YES → Review workflow
     │   └─ NO → Continue
     ├─ Contains "plan"/"design"/"architect"/"roadmap"/"strategy"/"architecture"/"system design"?
     │   └─ YES → Plan workflow
     │   └─ NO → Continue
     ├─ Contains "build"/"implement"/"create"/"write"/"code"/"develop"/"make"/"add feature"?
     │   └─ YES → Build workflow
     │   └─ NO → Continue
     ├─ Contains "debug"/"fix"/"error"/"bug"/"investigate"/"failure"/"broken"/"issue"/"problem"/"troubleshoot"/"diagnose"?
     │   └─ YES → Debug workflow
     │   └─ NO → Continue
     ├─ Contains "validate"/"verify"/"check"/"confirm implementation"/"alignment check"/"consistency check"?
     │   └─ YES → Validate workflow
     │   └─ NO → Continue
     ├─ Multiple keywords matched?
     │   └─ YES → Intent Disambiguation required
     │   └─ NO → Continue
     └─ No keywords matched?
         └─ YES → Ask user: "Which workflow should I run? (review/plan/build/debug/validate)"
     ```

     **Matching Logic**:
     1. Scan user request for intent keywords (case-insensitive)
     2. Count matches per workflow (one keyword can match multiple workflows)
     3. If single workflow has >0 matches → select that workflow
     4. If multiple workflows have matches → Intent Disambiguation required
     5. If no matches → ask user: "Which workflow should I run? (review/plan/build/debug/validate)"

     **Examples**:
     - "Review my code" → Review workflow (single match)
     - "Review and plan the feature" → Intent Disambiguation (multiple matches)
     - "Fix the bug" → Debug workflow (single match)
     - "Make it better" → Ask user (no matches)

   - **Intent Disambiguation**: If user request contains multiple workflow keywords (e.g., "review and plan"), list detected workflows: [review, plan, build, debug, validate]. Ask user: "I detected multiple intents. Which should I execute? (or 'both' for sequential)". Wait for explicit selection before proceeding.
   - Validate inputs (files, directories, questions). Ask for clarifications when context is missing.

   **Memory Integration** (filesystem-based, optimized):
   - **Efficient Query**: Load `.claude/memory/patterns.json` ONCE, cache for workflow duration
   - **Semantic Match**: Use `jq` to filter by task signature (file_count, type, deps) - not exact text
   - **Top Matches Only**: Return top 3 highest-confidence patterns
   - **Check User Preferences**: Load `.claude/memory/preferences.json` if exists
   - **Validation**: Only use patterns with confidence="high" or accuracy > 70%

   **External Resource Check** (smart caching):
   - **Check Cache First**: Lookup URL in `.claude/memory/web_cache/cache_index.json`
   - **Use Cache if Valid**: If cached and TTL valid → use cache (skip fetch)
   - **Re-fetch if Expired**: If cached but expired → re-fetch
   - **Deduplication**: Track URLs fetched in this workflow, avoid duplicates
   - **Batch Detection**: If multiple URLs needed, batch-fetch when possible
   - Ask user: "Detected external dependencies: {list}. Check cache or fetch documentation? (yes/no)"
   - Score complexity on a 1-5 scale using the expanded Complexity Rubric below. When the score is <=2 for plan/build, run Bash: `${CLAUDE_PLUGIN_ROOT}/scripts/lightweight-warning.sh` and wait for the user's explicit yes/no decision before proceeding.

## Skill Loading Optimization

**Skill Loading Decision Tree**:

```
Workflow requires skills?
├─ Identify required skills (from workflow Phase 2)
│   └─ Required skills exist?
│       ├─ YES → Continue
│       └─ NO → Report error, ask user: "Required skill '{name}' not found. Continue without it? (yes/no)"
├─ Identify conditional skills (from workflow detection logic)
│   └─ Detection logic check
│       ├─ UI components detected? → Load ui-design
│       ├─ Design patterns mentioned? → Load design-patterns
│       ├─ Feature planning needed? → Load feature-planning
│       └─ None detected → Skip conditional skills
├─ Check skill dependencies
│   └─ Skills have dependencies?
│       ├─ YES → Build dependency graph
│       │   └─ Load in topological order (sequential)
│       └─ NO → No dependencies
├─ Determine loading strategy
│   └─ All skills independent?
│       ├─ YES → Load all in parallel (faster)
│       └─ NO → Load sequentially (respect dependencies)
└─ Verify loading success
    └─ All skills loaded?
        ├─ YES → Continue to subagent invocation
        └─ NO → Error Recovery Protocol
```

**Unified Parallel Loading Strategy**:

1. **Identify Skill Dependencies**:
   - Map skill dependencies: skill A → skill B (B requires A)
   - Check if skills are independent (no dependencies)

2. **Load Strategy**:

   **PARALLEL Loading**:
   - ✅ Independent skills (no dependencies) → Load simultaneously
   - ✅ Faster initialization (all skills ready together)

   **SEQUENTIAL Loading**:
   - ❌ Skills with dependencies → Load in topological order
   - ❌ Dependent skill waits for prerequisite

3. **Implementation**:

   ```
   Example: Review workflow requires 8 skills

   Dependency Analysis:
   - risk-analysis: no deps → Parallel group 1
   - security-patterns: no deps → Parallel group 1
   - performance-patterns: no deps → Parallel group 1
   - code-quality-patterns: no deps → Parallel group 1
   - ux-patterns: no deps → Parallel group 1
   - accessibility-patterns: no deps → Parallel group 1
   - memory-tool-integration: no deps → Parallel group 1
   - web-fetch-integration: no deps → Parallel group 1

   Load all 8 skills in parallel (no dependencies)
   ```

**Update all workflow Phase 1 sections** to use "Load all independent skills in parallel" instead of mixed strategies.

2. **Workflow Existence Verification**
   - Before loading any workflow skill, verify it exists: Read first 100 chars of `plugins/cc10x/skills/{workflow-name}/SKILL.md`.
   - If workflow doesn't exist, report: "Workflow '{name}' not found. Available workflows: [review, plan, build, debug, validate]".
   - Ask user: "Choose an available workflow or specify custom instructions?"

3. **Policy Enforcement**
   - Do not auto-chain workflows. Offer optional follow-ups only after delivering the requested result.
   - Require explicit consent before continuing past a gate or rerunning an analysis.
   - When a workflow needs evidence (tests, lint, build), invoke `verification-before-completion` so the agent executes the command, captures output, and cites results before claiming success.

4. **Workflow Execution**
   - Load the workflow skill with `Read` (progressive disclosure Level 2).
   - **CRITICAL**: Ensure workflow executes Phase 0: Functionality Analysis FIRST before any skill loading or subagent dispatching
   - **Verify Phase 0**: Check that workflow includes Phase 0: Functionality Analysis (MANDATORY)
   - **Coordination Verification** (before proceeding):
     - [ ] Intent detected correctly (verify keyword matching)
     - [ ] Workflow exists (verify workflow file exists)
     - [ ] Phase 0 executed (verify functionality analysis complete)
     - [ ] Gate checks passed (verify all gate checks passed)
   - **Skill Loading Verification**: After loading each skill referenced by the workflow, verify success:
     - Read first 100 chars of SKILL.md to confirm content loaded
     - If loading fails, report immediately: "Skill '{name}' failed to load: {error details}"
     - Present options: "Continue without {skill} (functionality reduced)? Abort workflow? Retry loading?"
     - Wait for user decision before proceeding
   - **Skill Loading Coordination**:
     - Identify required skills (from workflow Phase 2)
     - Identify conditional skills (from workflow detection logic)
     - Check detection logic for conditional skills BEFORE loading
     - Load all independent skills in parallel (faster initialization)
     - Verify each skill loaded successfully
   - Follow workflow instructions exactly. Workflows now reference only real subagents and skills.
   - Record which domain skills are invoked so results can point to specific guidance files.

   **Subagent Invocation Rules** (CRITICAL):

   **Subagent Invocation Decision Tree**:

   ```
   Workflow requires subagents?
   ├─ Verify subagent exists (check plugins/cc10x/subagents/)
   │   └─ Subagent exists?
   │       ├─ YES → Continue
   │       └─ NO → Report error, ask user: "Subagent '{name}' not found. Skip it? (yes/no)"
   ├─ Check skip conditions (from workflow definition)
   │   └─ Skip condition met?
   │       ├─ YES → Skip subagent, ask user: "Skipping {name} due to {reason}. Proceed? (yes/no)"
   │       └─ NO → Continue
   ├─ Analyze dependencies
   │   └─ Build dependency graph
   │       ├─ Subagent A → Subagent B (B needs A's output)?
   │       │   └─ YES → Sequential execution required
   │       │   └─ NO → Check conflicts
   │       └─ Subagents modify same files?
   │           └─ YES → Sequential execution required
   │           └─ NO → Check execution mode
   ├─ Determine execution mode
   │   └─ All conditions met for parallel?
   │       ├─ YES (no dependencies, read-only, isolated contexts, independent data) → Parallel execution
   │       └─ NO → Sequential execution
   ├─ Prepare context
   │   └─ All context provided?
   │       ├─ YES → Invoke subagent
   │       └─ NO → Gather missing context, then invoke
   └─ Validate output
       └─ Output valid?
           ├─ YES → Continue to next subagent or workflow phase
           └─ NO → Error Recovery Protocol
   ```

   - **Verify existence FIRST**: Before invoking any subagent, verify it exists in `plugins/cc10x/subagents/`
   - **Check skip conditions**: Each workflow defines "when NOT to invoke" - check these BEFORE invocation
   - **Dependency Analysis**: Build dependency graph BEFORE invocation:
     - Map dependencies: subagent A → subagent B (B requires A's output)
     - Check conflicts: subagents modifying same files
     - Determine execution mode: parallel (safe) vs sequential (required)
   - **Coordination Verification** (before subagent invocation):
     - [ ] Subagent exists (verify subagent file exists)
     - [ ] Skip conditions checked (verify "when NOT to invoke" checked)
     - [ ] Dependencies analyzed (verify dependency graph built)
     - [ ] Execution mode determined (verify parallel vs sequential)
     - [ ] Context prepared (verify all context provided)
   - **Respect user overrides**: If user explicitly skips a subagent, document and skip it
   - **Sequential only**: Never invoke multiple subagents in parallel UNLESS all conditions met:
     - ✅ No output dependencies (operation B doesn't need operation A's output)
     - ✅ Read-only operations (no state mutations)
     - ✅ Isolated contexts (separate subagent contexts)
     - ✅ Independent data (different files/components/bugs)
     - ✅ Validation after each (prevents error propagation)
   - **Context isolation**: Each subagent starts fresh - provide all needed context explicitly
   - **Confirmation on skip**: If skipping subagent, ask user: "Skipping {subagent-name} due to {reason}. Proceed? (yes/no)"
   - **Output Validation** (after subagent completes):
     - [ ] Output format matches expected template (check required sections present)
     - [ ] All required fields present (findings, file:line citations, commands, exit codes)
     - [ ] File references include path:line where applicable
     - [ ] Commands included with exit codes (if applicable)
     - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
     - [ ] Output is actionable (not just descriptions)
   - **Error Recovery**: If subagent fails, use Error Recovery Protocol

### Tool Access Precedence

- When multiple skills are active, the orchestrator/workflow tool set governs delegation and verification. Domain skills may restrict themselves (e.g., Read/Grep/Glob), but they do not prevent the orchestrator/workflow from using `Task` or `Bash` to delegate/verify.

## Ask Questions Tool Usage

**Purpose**: Clarify requirements and gather missing information before proceeding

**When to Use**:

- Phase 0: Functionality Analysis (when functionality unclear)
- Plan Workflow: Requirements gathering
- Build Workflow: UI requirements for UI components
- Debug Workflow: Bug clarification

**Usage Pattern**:

```
Use the askquestion tool to clarify requirements:
- [Specific questions about functionality/requirements]
```

**Example**:

```
Use the askquestion tool to clarify requirements:
- What are the specific user flows?
- What are the acceptance criteria?
- What are the constraints?
```

## Task Tool Usage

**Purpose**: Track workflow progress and manage task queues

**When to Use**:

- Phase tracking (all workflows)
- Component build queue (Build workflow)
- Review findings tracking (Review workflow)
- Planning checklist (Plan workflow)

**Usage Pattern**:

```
Task: Create tasks for [purpose]
- Task 1: [description] (status)
- Task 2: [description] (status)

Task: Update [task] status to [new_status]
```

**Example**:

```
Task: Create tasks for workflow phases
- Phase 0: Functionality Analysis (in_progress)
- Phase 1: Input Validation (pending)
- Phase 2: Load Skills (pending)
```

## Tool Selection Guide

| Task                    | Tool          | When to Use                                                            | Example                                    |
| ----------------------- | ------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| Clarify requirements    | Ask Questions | Functionality unclear, missing requirements, need user input           | "What are the specific user flows?"        |
| Track workflow progress | Task          | Phase tracking, component queue, findings tracking, planning checklist | "Task: Create tasks for workflow phases"   |
| Find files by pattern   | Glob          | Need to find files matching pattern (e.g., `*.ts`, `**/test/**`)       | `Glob("**/*.test.ts")`                     |
| Search file content     | Grep          | Need to find text/patterns in files                                    | `Grep("function.*test")`                   |
| Read file contents      | Read          | Need to read specific file or section                                  | `Read("path/to/file.ts")`                  |
| Execute shell commands  | Bash          | Need to run commands, check exit codes, verify functionality           | `Bash("npm test")`                         |
| Fetch external docs     | WebFetch      | Need external API docs, library docs, reference materials              | `WebFetch("https://api.example.com/docs")` |

**Tool Selection Logic**:

- **Finding files**: Use `Glob` for pattern matching, `Grep` for content search
- **Reading files**: Use `Read` for specific files, `Grep` for searching across files
- **User interaction**: Use `Ask Questions` for clarification, `Task` for progress tracking
- **Verification**: Use `Bash` to run tests/commands, check exit codes
- **External resources**: Use `WebFetch` for documentation, cache results

## Search Guidance

**CRITICAL**: Choose the right tool for the search task. Using the wrong tool wastes tokens and time.

**When to Use Glob** (file discovery):

- Finding files by name pattern: `Glob("**/*.test.ts")`
- Finding files in specific directories: `Glob("src/components/**/*.tsx")`
- Discovering project structure: `Glob("**/*.json")` to find config files
- **Example**: "Find all test files" → `Glob("**/*.test.{ts,tsx,js,jsx}")`

**When to Use Grep** (content search):

- Searching for function/class names: `Grep("function.*authenticate")`
- Finding imports/exports: `Grep("import.*from.*api")`
- Searching for patterns across files: `Grep("TODO|FIXME|HACK")`
- Finding specific code patterns: `Grep("useState|useEffect")`
- **Example**: "Find all uses of authentication function" → `Grep("authenticate")`

**When to Use Read** (specific file access):

- Reading a known file: `Read("src/api/auth.ts")`
- Reading configuration files: `Read("package.json")`
- Reading workflow/skill files: `Read("plugins/cc10x/skills/review-workflow/SKILL.md")`
- Reading specific sections: `Read("file.ts", offset=100, limit=50)`
- **Example**: "Read the orchestrator skill" → `Read("plugins/cc10x/skills/cc10x-orchestrator/SKILL.md")`

**Search Strategy** (combine tools efficiently):

1. **Discovery Phase**: Use `Glob` to find relevant files
2. **Content Phase**: Use `Grep` to search within discovered files
3. **Detail Phase**: Use `Read` to read specific files/sections
4. **Example**:
   - Step 1: `Glob("**/*auth*.ts")` → Find auth-related files
   - Step 2: `Grep("function.*login", path="src/auth/")` → Find login functions
   - Step 3: `Read("src/auth/login.ts")` → Read specific implementation

**Anti-Patterns** (what NOT to do):

- ❌ Using `Grep` to find files by name (use `Glob` instead)
- ❌ Using `Read` to search for patterns (use `Grep` instead)
- ❌ Reading entire large files when you only need a section (use `Read` with offset/limit)
- ❌ Using `Glob` to search file contents (use `Grep` instead)

## Validation Checklist

**CRITICAL**: Before proceeding to the next phase, ALL items below MUST be checked. In Strict Mode, workflow aborts if any validation fails.

**Mandatory Validation Steps** (before proceeding):

- [ ] Phase 0 complete and verified (functionality analysis complete, all gate checks passed)
- [ ] Skills loaded successfully (all required skills loaded, conditional skills loaded if detected)
- [ ] Subagents invoked correctly (existence verified, skip conditions checked, dependencies analyzed, execution mode determined)
- [ ] Outputs validated (format matches expected template, all required fields present, file:line citations provided)
- [ ] Evidence provided for all claims (file:line citations for code references, exit codes for commands, logs/artifacts for verification)

**Strict Mode** (optional, recommended for production):

When Strict Mode is enabled:

- Workflow aborts immediately if any validation step fails
- No partial results are accepted
- All evidence must be provided before proceeding
- Error Recovery Protocol is triggered on any validation failure

**Usage**: Enable Strict Mode by adding "strict mode" to user request or by default for production workflows.

5. **Result Compilation**
   - Summarise findings with severity or priority (high/medium/low) based on evidence.
   - Link each recommendation to the skill or subagent that produced it.
   - Surface open questions and next-step offers without assuming consent.

   **Memory Integration** (filesystem-based, optimized):
   - **Validate Patterns First**: Compare predicted complexity → actual complexity
   - **Update Accuracy**: Calculate accuracy = (matches / total_uses) \* 100
   - **Update Confidence**: high (>80%), medium (60-80%), low (<60%)
   - **Store Only Validated**: Only save patterns with accuracy > 50% after 3+ uses
   - **Efficient Storage**: Use `Bash` + `jq` to update JSON files atomically
   - **Run Cleanup**: Execute memory cleanup script after storing
   - **Update Only**: Don't create new patterns without validation

   **Memory Cleanup** (after workflow):
   - Delete complexity patterns with accuracy < 50% (after 3+ uses)
   - Delete unused patterns > 60 days old
   - Keep top 20 most accurate patterns per project
   - Delete failure modes unused > 30 days
   - Delete failure modes with success rate < 60%

6. **Failure Handling**
   - If a workflow or subagent fails, use the standardized Error Recovery Protocol:

   ## Error Recovery Protocol

   **Error Recovery Decision Tree**:

   ```
   Error occurred?
   ├─ Skill loading failed?
   │   ├─ File missing?
   │   │   └─ YES → Report error, offer: Retry / Continue without / Abort
   │   │   └─ NO → Continue
   │   ├─ Parse error?
   │   │   └─ YES → Report error, offer: Retry / Continue without / Abort
   │   │   └─ NO → Continue
   │   └─ Unknown error?
   │       └─ YES → Report error, offer: Retry / Continue without / Abort
   │       └─ NO → Continue
   ├─ Subagent invocation failed?
   │   ├─ Subagent missing?
   │   │   └─ YES → Report error, offer: Skip / Abort
   │   │   └─ NO → Continue
   │   ├─ Output invalid?
   │   │   └─ YES → Report error, offer: Retry / Request correction / Continue
   │   │   └─ NO → Continue
   │   └─ Execution error?
   │       └─ YES → Report error, offer: Retry / Skip / Abort
   │       └─ NO → Continue
   └─ Workflow execution failed?
       ├─ Phase 0 incomplete?
       │   └─ YES → Complete Phase 0, then retry
       │   └─ NO → Continue
       ├─ Validation failed?
       │   └─ YES → Fix issues, then retry
       │   └─ NO → Continue
       └─ Unknown error?
           └─ YES → Report error, offer: Retry / Abort
           └─ NO → Continue
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

   **Error Recovery Checklists** (step-by-step recovery paths):

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

   Example Error Recovery Message:

   ```
   ## Error Recovery Required

   **Context**: Attempted to load workflow skill 'review-workflow'
   - Read: plugins/cc10x/skills/review-workflow/SKILL.md
   - Error: File not found

   **Problem**: Review workflow skill file missing or inaccessible

   **Options**:
   1. **Retry**: Check alternative path or permissions
   2. **Continue without review workflow**: Use manual review process
   3. **Abort workflow**: Stop and verify cc10x plugin installation

   **Impact**:
   - Retry: May resolve if path/permission issue
   - Continue: Review functionality reduced
   - Abort: Ensures clean state but loses progress

   **Recommended**: Abort workflow (ensures clean state)

   **Please respond**: [Retry / Continue / Abort] or [Custom instruction]
   ```

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

## Parallel Execution Strategy

**Dependency Analysis Protocol**:

1. **Build Dependency Graph**: For each workflow phase:
   - Identify all operations (subagents, skills, components, bugs)
   - Map dependencies: operation A → operation B (B requires A's output)
   - Map conflicts: operation A ⚠️ operation B (shared state, same files)
2. **Execution Mode Selection**:

   **PARALLEL (Safe)**:
   - ✅ No output dependencies (operation B doesn't need operation A's output)
   - ✅ Read-only operations (no state mutations)
   - ✅ Isolated contexts (separate subagent contexts)
   - ✅ Independent data (different files/components/bugs)
   - ✅ Validation after each (prevents error propagation)

   **SEQUENTIAL (Required)**:
   - ❌ Output → Input dependency (A's output feeds B's input)
   - ❌ State mutation → Read dependency (A mutates, B reads)
   - ❌ Validation gates (must wait for validation)
   - ❌ Feedback loops (B can trigger return to A)
   - ❌ Shared state (both modify same data)

3. **Workflow-Specific Parallel Execution Rules**:
   - **Review Workflow**: Analysis subagents (analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility) CAN run in parallel IF comprehensive review (read-only, independent, isolated contexts)
   - **Plan Workflow**: Planning subagents MUST run sequentially (planning-architecture-risk → planning-design-deployment, architecture informs design)
   - **Build Workflow**: Component subagents MUST run sequentially per component (component-builder → code-reviewer → integration-verifier), but components can run in parallel IF independent
   - **Debug Workflow**: Bug subagents MUST run sequentially per bug (bug-investigator → code-reviewer → integration-verifier), but bugs can run in parallel IF independent
   - **Validate Workflow**: No subagents (direct comparisons)

4. **Conflict Prevention Rules**:
   - Read-only subagents analyzing SAME code → PARALLEL (safe)
   - Subagents mutating DIFFERENT files → PARALLEL (safe)
   - Subagents with output dependencies → SEQUENTIAL (required)
   - Subagents in same workflow phase → Check dependencies first

5. **Fallback Strategy**:
   - If parallel execution fails → Automatically fallback to sequential
   - Log fallback reason for debugging
   - Continue with remaining operations

## Parallel Execution Safety Validation

**Conflict Detection Checklist** (before parallel execution):

- [ ] No output dependencies (operation B doesn't need A's output)
- [ ] No shared state mutations (operations don't modify same data)
- [ ] Read-only operations (no write conflicts)
- [ ] Isolated contexts (separate subagent contexts)
- [ ] Validation gates (validation occurs after all complete)
- [ ] Error isolation (failure of one doesn't corrupt others)

**Fallback Triggers**:

- Any conflict detected → Automatically fallback to sequential
- Parallel execution fails → Retry sequentially
- User preference for sequential → Honor user choice
- Complexity threshold exceeded → Sequential for safety

## Complexity Gate (Plan/Build)

If the complexity score is 2 or lower, warn that cc10x is optimized for higher-risk work and ask whether to proceed (yes/no). Pause until the user answers. Abort if the answer is "no" or no answer is provided.

## Complexity Rubric (1-5) - Functionality First

**Note**: Complexity scoring should consider functional complexity (user flows, system flows, integration flows) in addition to technical complexity.

### Base Scoring

- **1** - Single function (<50 LOC), no external dependencies, no test changes, no config changes, single user flow
- **2** - Single file (<200 LOC), trivial change, low risk, minimal test updates, simple user flow
- **3** - 2-5 files, moderate change, adds/updates tests, low/medium risk, some refactoring, multiple user flows or admin flow
- **4** - Multi-module change or new integration, notable risk/uncertainty, cross-file coordination needed, complex user/admin/system flows
- **5** - Cross-cutting or architectural impact, migrations/rollout considerations, breaking changes, complex multi-flow functionality

### Edge Case Handling

**Mixed Complexity**: If changes include both trivial and complex parts:

- Use the **highest score** (assume maximum risk)
- Document: "Mixed complexity detected: {trivial parts} and {complex parts}. Scoring: {highest score}"

**Unclear Architectural Impact**: If impact is uncertain:

- Default to **score 4** (assume risk exists)
- Ask user: "I cannot determine architectural impact. Is this change cross-cutting or isolated? (isolated=3, cross-cutting=4-5)"

**Refactor-Only Changes**: If no functional changes, only code structure:

- Score based on **file count** and **scope of refactor**
- Refactor within 1-2 files = score 2
- Refactor across 3-5 files = score 3
- Refactor across modules = score 4
- Large-scale architectural refactor = score 5

**Dependency Complexity**: Consider dependency changes:

- No new dependencies = no adjustment
- New dependency with clear migration path = +0.5 to score
- New dependency requiring significant integration = +1 to score
- Breaking dependency updates = +1.5 to score

**Calculation Method**: Start with base score, apply adjustments above, round to nearest integer (1-5).

### Examples

Example 1: "Add user registration form"

- 1 new component file, 1 API endpoint, tests = 3 files
- New database migration = moderate change
- **Score: 3**

Example 2: "Replace payment processor"

- Multiple files affected (payment service, config, tests)
- External API integration change = high risk
- **Score: 4**

Example 3: "Fix typo in comment"

- Single file, single line
- **Score: 1**

Example 4: "Refactor authentication across all modules"

- Multiple modules affected, architectural change
- **Score: 5**

## Quick Reference

**Workflow Indicators** (intent keywords):

- **Review**: review, audit, check, analyze, security, quality, performance, UX, accessibility
- **Plan**: plan, design, architect, structure, feature planning
- **Build**: build, implement, create, code, develop, feature
- **Debug**: debug, fix, error, bug, investigate, troubleshoot
- **Validate**: validate, verify, check alignment, compare

**File Purposes**:

- **Orchestrator Skill** (`plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`): Main coordination logic, intent detection, workflow routing
- **Workflow Files** (`plugins/cc10x/skills/cc10x-orchestrator/workflows/*.md`): Workflow-specific instructions, phases, skill/subagent coordination
- **Skill Files** (`plugins/cc10x/skills/*/SKILL.md`): Domain-specific expertise, patterns, best practices
- **Subagent Files** (`plugins/cc10x/subagents/*/SUBAGENT.md`): Specialized AI personalities for specific tasks
- **Templates** (`plugins/cc10x/skills/cc10x-orchestrator/templates/*.md`): Reusable templates for functionality analysis

**Essentials** (must-know):

1. **Functionality First**: Always understand functionality (user/admin/system flows) BEFORE applying specialized checks
2. **Phase 0 Mandatory**: All workflows MUST execute Phase 0: Functionality Analysis FIRST
3. **Evidence Required**: All findings must include file:line citations or command exit codes
4. **Parallel Loading**: Load all independent skills in parallel for faster initialization
5. **Validation Gates**: Validate outputs between phases before proceeding
6. **Error Recovery**: Use Error Recovery Protocol with clear options and impacts

## Evidence-First Expectations

- Reviews must cite file paths and line numbers.
- Planning, build, and debug workflows must run the relevant verification commands before claiming completion.
- For every success statement, include a short "Verification Summary" that lists commands run, exit codes, and artefacts.

## Final Report - Output Format (REQUIRED)

**MANDATORY TEMPLATE** - All workflows must use this exact structure:

```markdown
# [Workflow Name] Report

## Executive Summary

[2-3 sentences summarizing outcome, key findings, and overall status]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
  [Bullet list of key steps, tools used, subagents invoked, skills loaded]

## Functionality Analysis

[Include complete functionality analysis from Phase 0 - user flows, admin flows, system flows, functional verification]

## Findings / Decisions

[Workflow-specific sections with file:line citations where applicable]

## Verification Summary

Scope: <files/modules>
Criteria: <list of what was verified - functionality FIRST, then other checks>
Commands:

- <command> -> exit <code>
- <command> -> exit <code>
  Evidence:
- <log/report snippet>
- <test output snippet>
  Risks / Follow-ups: <items still pending or needing attention>

## Recommendations / Next Steps

[Prioritized list of actionable next steps - functionality issues FIRST, then other concerns]

## Open Questions / Assumptions

[If any - list questions requiring user input or assumptions made]
```

**Validation**: Before presenting final report, verify:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes functionality verification FIRST, then other checks
- [ ] File:line citations provided for all findings
- [ ] Recommendations are prioritized (functionality issues first)
- [ ] All subagents/skills used are documented in Actions Taken

## Memory Integration

**Purpose**: Use filesystem-based memory (`.claude/memory/`) to persist workflow state, patterns, and preferences across conversations.

**NOTE**: Anthropic's Memory Tool (API beta) is **NOT available in Claude Code**. This integration uses filesystem-based memory.

**Memory Usage**:

- **Before Complexity Scoring**: Query `.claude/memory/patterns.json` for similar tasks and use learned complexity scores as reference
- **After Workflow Completion**: Store workflow outcomes, learned patterns, and user preferences in JSON files
- **Pattern Learning**: Store complexity patterns, failure modes, and successful approaches in `.claude/memory/`

**What to Store**:

- Complexity patterns: `.claude/memory/patterns.json` → Task types → complexity scores → accuracy
- Failure modes: `.claude/memory/failure_modes.json` → Common errors → root causes → fixes
- User preferences: `.claude/memory/preferences.json` → Review depth, build approach, test coverage targets
- Workflow checkpoints: `.claude/memory/snapshots/` → Phase progress, component state, pending tasks

**Implementation**: See `plugins/cc10x/skills/memory-tool-integration/SKILL.md` for detailed guidance on filesystem-based memory usage patterns, including query patterns, storage procedures, and cleanup scripts.

## Web Fetch Integration

**Purpose**: Use Web Fetch Tool to load external documentation, API specifications, and reference materials when needed.

**When to Use**:

- External APIs mentioned: Fetch API documentation before planning
- Libraries/frameworks: Load documentation before building
- External services: Fetch service docs for integration
- Reference materials: Load guides, standards, best practices

**Integration Points**:

- **Planning Workflow**: Fetch API specs, framework docs, integration guides
- **Build Workflow**: Load library docs, SDK examples, framework guides
- **Review Workflow**: Fetch security standards, coding guidelines, best practices
- **Debug Workflow**: Load error docs, troubleshooting guides, stack trace resources

**Best Practices**:

- Cache frequently accessed docs
- Validate URLs before fetching
- Extract only relevant sections
- Cite sources in workflow output

**Integration**: Load `web-fetch-integration` skill for detailed guidance on web fetch usage.

## Context Editing (Sep 2025)

**Available Strategies**:

- Clear older tool results when approaching limits
- Clear thinking blocks automatically (`clear_thinking_20251015`)
- Automatic context cleanup for long conversations

**For Long Workflows**:

- Explicit checkpointing at major phases
- Summarizing intermediate results
- Document state between phases

## References

- Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`
- Verification guardrails: `plugins/cc10x/skills/verification-before-completion/SKILL.md`
- Orchestration Coordination Matrix: `audit/orchestration-coordination-matrix.md` (complete skill/subagent activation matrix)
- Anthropic Context Editing: https://docs.claude.com/en/docs/build-with-claude/context-editing
- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool

Keep this skill concise (<500 lines) and ASCII-only so it stays compliant with Anthropic marketplace requirements.
