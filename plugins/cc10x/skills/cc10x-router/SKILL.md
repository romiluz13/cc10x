---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X. This skill MUST be activated for ANY development task - never skip.

  Use this skill when: building, implementing, debugging, fixing, reviewing, planning, refactoring, testing, or ANY coding request. If user asks to write code, fix bugs, review code, or plan features - USE THIS SKILL.

  Triggers: build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy, memory, session, context, save, load, test, tdd, frontend, ui, backend, api, pattern, refactor, optimize, improve, enhance, update, modify, change, help, assist, work, start, begin, continue, research, cc10x, c10x.

  CRITICAL: Execute workflow immediately. Never just describe capabilities.
---

# cc10x Router

**EXECUTION ENGINE.** When loaded: Detect intent → Load memory → Execute workflow → Update memory.

**NEVER** list capabilities. **ALWAYS** execute.

## Decision Tree (FOLLOW IN ORDER)

| Priority | Signal | Keywords | Workflow |
|----------|--------|----------|----------|
| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue, problem, doesn't work | **DEBUG** |
| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, "before we build", "how should we" | **PLAN** |
| 3 | REVIEW | review, audit, check, analyze, assess, "what do you think", "is this good" | **REVIEW** |
| 4 | DEFAULT | Everything else | **BUILD** |

**Conflict Resolution:** ERROR signals always win. "fix the build" = DEBUG (not BUILD).

## Agent Chains

| Workflow | Agents |
|----------|--------|
| BUILD | component-builder → **[code-reviewer ∥ silent-failure-hunter]** → integration-verifier |
| DEBUG | bug-investigator → code-reviewer → integration-verifier |
| REVIEW | code-reviewer |
| PLAN | planner |

**∥ = PARALLEL** - code-reviewer and silent-failure-hunter - run simultaneously

## Memory (PERMISSION-FREE)

**LOAD FIRST (Before routing):**

**Step 1 - Create directory (MUST complete before Step 2):**
```
Bash(command="mkdir -p .claude/cc10x")
```

**Step 2 - Load memory files (AFTER Step 1 completes):**
```
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")
```

**IMPORTANT:** Do NOT run Step 1 and Step 2 in parallel. Wait for mkdir to complete before reading files.

If any memory file is missing:
- Create it with `Write(...)` using the templates from `cc10x:session-memory` (include the contract comment + required headings).
- Then `Read(...)` it before continuing.

**TEMPLATE VALIDATION GATE (Auto-Heal):**

After loading memory files, ensure ALL required sections exist.

### activeContext.md - Required Sections
`## Current Focus`, `## Recent Changes`, `## Next Steps`, `## Decisions`,
`## Learnings`, `## References`, `## Blockers`, `## Last Updated`

### progress.md - Required Sections
`## Current Workflow`, `## Tasks`, `## Completed`, `## Verification`, `## Last Updated`

### patterns.md - Required Sections
`## Common Gotchas` (minimum)

**Auto-heal pattern:**
```
# If any section missing in activeContext.md, insert before ## Last Updated:
# Example: "## References" is missing
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Last Updated",
     new_string="## References\n- Plan: N/A\n- Design: N/A\n- Research: N/A\n\n## Last Updated")

# Example: progress.md missing "## Verification"
Edit(file_path=".claude/cc10x/progress.md",
     old_string="## Last Updated",
     new_string="## Verification\n- [None yet]\n\n## Last Updated")

# VERIFY after each heal
Read(file_path=".claude/cc10x/activeContext.md")
```

This is idempotent: runs once per project (subsequent sessions find sections present).
**Why:** Old projects may lack these sections, causing Edit failures.

**UPDATE (Checkpoint + Final):**
- Avoid memory edits during parallel phases.
- Do a **workflow-final** memory update/check after the chain completes.
- Use Edit tool on memory files (permission-free), then Read-back verify.

Memory update rules (do not improvise):
1. Use `Edit(...)` (not `Write`) to update existing `.claude/cc10x/*.md`.
2. Immediately `Read(...)` the edited file and confirm the expected text exists.
3. If the update did not apply, STOP and retry with a correct, exact `old_string` anchor (do not proceed with stale memory).

## Check Active Workflow Tasks

**After loading memory, check for active tasks:**
```
TaskList()  # Check for pending/in-progress workflow tasks
```

**Orphan check:** If any CC10X task has status="in_progress" → Ask user: Resume (reset to pending) / Complete (skip) / Delete.

**If active CC10x workflow task exists (preferred: subject starts with `CC10X `):**
- Resume from task state (use `TaskGet({ taskId })` for the task you plan to resume)
- Skip workflow selection - continue execution from where it stopped
- Check `blockedBy` to determine which agent to run next

**Safety rule (avoid cross-project collisions):**
- If you find tasks that do NOT clearly belong to CC10x, do not resume them.
- If unsure, ask the user whether to resume or create a fresh task hierarchy.

**Legacy compatibility:** Older CC10x versions may have created tasks with subjects starting `BUILD:` / `DEBUG:` / `REVIEW:` / `PLAN:` (without the `CC10X` prefix).
- If such tasks exist, ask the user whether to resume the legacy tasks or start a fresh CC10X-namespaced workflow.

Task lists can be shared across sessions via `CLAUDE_CODE_TASK_LIST_ID`. Treat TaskLists as potentially long-lived; always scope before resuming.

**If no active tasks:**
- Proceed with workflow selection below

## Task Dependency Safety

**All `addBlockedBy` calls MUST follow these rules:**
1. Dependencies flow FORWARD only (downstream blocked by upstream)
2. NEVER block an upstream task by a downstream task
3. If unsure, list current dependencies before adding new ones

**If you suspect a cycle:**
1. Run `TaskList()` to see all task dependencies
2. Trace the dependency chain
3. If cycle detected → Skip the dependency, log warning, continue

**Current design guarantees no cycles:** All workflows are DAGs with forward-only dependencies.

---

## Task-Based Orchestration

**At workflow start, create task hierarchy using TaskCreate/TaskUpdate:**

### BUILD Workflow Tasks
```
# 0. Check if following a plan (from activeContext.md)
# Look in "## References" section for "- Plan:" entry (not "N/A"):
#   → Extract plan_file path from the line (e.g., `docs/plans/2024-01-27-auth-plan.md`)
#   → Include in task description for context preservation
# Example match: "- Plan: `docs/plans/auth-flow-plan.md`" → plan_file = "docs/plans/auth-flow-plan.md"

# 1. Parent workflow task
TaskCreate({
  subject: "CC10X BUILD: {feature_summary}",
  description: "User request: {request}\n\nWorkflow: BUILD\nChain: component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier\n\nPlan: {plan_file or 'N/A'}",
  activeForm: "Building {feature}"
})
# Returns workflow_task_id

# 2. Agent tasks with dependencies
TaskCreate({
  subject: "CC10X component-builder: Implement {feature}",
  description: "Build the feature per user request\n\nPlan: {plan_file or 'N/A'}",
  activeForm: "Building components"
})
# Returns builder_task_id

TaskCreate({ subject: "CC10X code-reviewer: Review implementation", description: "Review code quality, patterns, security", activeForm: "Reviewing code" })
# Returns reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({ subject: "CC10X silent-failure-hunter: Hunt edge cases", description: "Find silent failures and edge cases", activeForm: "Hunting failures" })
# Returns hunter_task_id
TaskUpdate({ taskId: hunter_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({ subject: "CC10X integration-verifier: Verify integration", description: "Run tests, verify E2E functionality", activeForm: "Verifying integration" })
# Returns verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id, hunter_task_id] })

# 3. Memory Update task (blocked by final agent - TASK-ENFORCED)
TaskCreate({
  subject: "CC10X Memory Update: Persist workflow learnings",
  description: "REQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\n**Instructions:**\n1. Find all '### Memory Notes' sections from completed agents\n2. Persist learnings to .claude/cc10x/activeContext.md ## Learnings\n3. Persist patterns to .claude/cc10x/patterns.md ## Common Gotchas\n4. Persist verification to .claude/cc10x/progress.md ## Verification\n\n**Pattern:**\nRead(file_path=\".claude/cc10x/activeContext.md\")\nEdit(old_string=\"## Learnings\", new_string=\"## Learnings\\n- [from agent]: {insight}\")\nRead(file_path=\".claude/cc10x/activeContext.md\")  # Verify\n\nRepeat for patterns.md and progress.md.",
  activeForm: "Persisting workflow learnings"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

### DEBUG Workflow Tasks
```
TaskCreate({ subject: "CC10X DEBUG: {error_summary}", description: "User request: {request}\n\nWorkflow: DEBUG\nChain: bug-investigator → code-reviewer → integration-verifier", activeForm: "Debugging {error}" })

TaskCreate({ subject: "CC10X bug-investigator: Investigate {error}", description: "Find root cause and fix", activeForm: "Investigating bug" })
# Returns investigator_task_id
TaskCreate({ subject: "CC10X code-reviewer: Review fix", description: "Review the fix quality", activeForm: "Reviewing fix" })
# Returns reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [investigator_task_id] })
TaskCreate({ subject: "CC10X integration-verifier: Verify fix", description: "Verify fix works E2E", activeForm: "Verifying fix" })
# Returns verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id] })

# Memory Update task (blocked by final agent - TASK-ENFORCED)
TaskCreate({
  subject: "CC10X Memory Update: Persist debug learnings",
  description: "REQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\nFocus on:\n- Root cause for patterns.md ## Common Gotchas\n- Debug attempt history for activeContext.md\n- Verification evidence for progress.md\n\n**Use Read-Edit-Read pattern for each file.**",
  activeForm: "Persisting debug learnings"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

### REVIEW Workflow Tasks
```
TaskCreate({ subject: "CC10X REVIEW: {target_summary}", description: "User request: {request}\n\nWorkflow: REVIEW\nChain: code-reviewer (single agent)", activeForm: "Reviewing {target}" })

TaskCreate({ subject: "CC10X code-reviewer: Review {target}", description: "Comprehensive code review", activeForm: "Reviewing code" })
# Returns reviewer_task_id

# Memory Update task (blocked by final agent - TASK-ENFORCED)
TaskCreate({
  subject: "CC10X Memory Update: Persist review learnings",
  description: "REQUIRED: Collect Memory Notes from code-reviewer output and persist to memory files.\n\nFocus on:\n- Patterns discovered for patterns.md\n- Review verdict for progress.md\n\n**Use Read-Edit-Read pattern for each file.**",
  activeForm: "Persisting review learnings"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [reviewer_task_id] })
```

### PLAN Workflow Tasks
```
TaskCreate({ subject: "CC10X PLAN: {feature_summary}", description: "User request: {request}\n\nWorkflow: PLAN\nChain: planner (single agent)", activeForm: "Planning {feature}" })

TaskCreate({ subject: "CC10X planner: Create plan for {feature}", description: "Create comprehensive implementation plan", activeForm: "Creating plan" })
# Returns planner_task_id

# Memory Update task (blocked by final agent - TASK-ENFORCED)
TaskCreate({
  subject: "CC10X Memory Update: Index plan in memory",
  description: "REQUIRED: Update memory files with plan reference.\n\nFocus on:\n- Add plan file to activeContext.md ## References\n- Update progress.md with plan status\n\n**Use Read-Edit-Read pattern for each file.**",
  activeForm: "Indexing plan in memory"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [planner_task_id] })
```

## Workflow Execution

### BUILD
1. Load memory → Check if already done in progress.md
2. **Plan-First Gate** (STATE-BASED, not phrase-based):
   - Skip ONLY if: (plan in `## References` ≠ "N/A") AND (active `CC10X` task exists)
   - Otherwise → AskUserQuestion: "Plan first (Recommended) / Build directly"
3. **Clarify requirements** (DO NOT SKIP) → Use AskUserQuestion
4. **Create task hierarchy** (see Task-Based Orchestration above)
5. **Start chain execution** (see Chain Execution Loop below)
6. Update memory when all tasks completed

### DEBUG
1. Load memory → Check patterns.md Common Gotchas
2. **CLARIFY (REQUIRED)**: Use AskUserQuestion if ANY ambiguity:
   - What error message/behavior?
   - Expected vs actual?
   - When did it start?
   - Which component/file affected?
3. **Check for research trigger:**
   - User explicitly requested research ("research", "github", "octocode"), OR
   - External service error (API timeout, auth failure, third-party), OR
   - **3+ local debugging attempts failed**

   **Debug Attempt Counting:**
   - Format in activeContext.md Recent Changes: `[DEBUG-N]: {what was tried} → {result}`
   - Example: `[DEBUG-1]: Added null check → still failing (TypeError persists)`
   - Count lines matching `[DEBUG-N]:` pattern
   - If count ≥ 3 AND all show failure → trigger external research

   **What counts as an attempt:**
   - A hypothesis tested with code change or command
   - NOT: reading files, thinking, planning
   - Each attempt must have a concrete action + observed result

   **If ANY trigger met:**
   - Execute research FIRST using octocode tools directly
   - Search for error patterns, PRs with similar issues
   - **PERSIST research** → Save to `docs/research/YYYY-MM-DD-<error-topic>-research.md`
   - **Update memory** → Add to activeContext.md References section
4. **Create task hierarchy** (see Task-Based Orchestration above)
5. **Start chain execution** (pass research file path if step 3 was executed)
6. Update memory → Add to Common Gotchas when all tasks completed

### REVIEW
1. Load memory
2. **CLARIFY (REQUIRED)**: Use AskUserQuestion to confirm scope:
   - Review entire codebase OR specific files?
   - Focus area: security/performance/quality/all?
   - Blocking issues only OR all findings?
3. **Create task hierarchy** (see Task-Based Orchestration above)
4. **Start chain execution** (see Chain Execution Loop below)
5. Update memory when task completed

### PLAN
1. Load memory
2. **If github-research detected (external tech OR explicit request):**
   - Execute research FIRST using octocode tools directly (NOT as hint)
   - Use: `mcp__octocode__packageSearch`, `mcp__octocode__githubSearchCode`, etc.
   - **PERSIST research** → Save to `docs/research/YYYY-MM-DD-<topic>-research.md`
   - **Update memory** → Add to activeContext.md References section
   - Summarize findings before invoking planner
3. **Create task hierarchy** (see Task-Based Orchestration above)
4. **Start chain execution** (pass research results + file path in prompt if step 2 was executed)
5. Update memory → Reference saved plan when task completed

**THREE-PHASE for External Research (MANDATORY):**
```
If SKILL_HINTS includes github-research:
  → PHASE 1: Execute research using octocode tools
  → PHASE 2: PERSIST research (prevents context loss):
      Bash(command="mkdir -p docs/research")
      Write(file_path="docs/research/YYYY-MM-DD-<topic>-research.md", content="[research summary]")
      Edit(file_path=".claude/cc10x/activeContext.md", ...)  # Add to References section
  → PHASE 3: Task(cc10x:planner, prompt="...Research findings: {results}...\nResearch saved to: docs/research/YYYY-MM-DD-<topic>-research.md")
```
Research is a PREREQUISITE, not a hint. Planner cannot skip it.
**Research without persistence is LOST after context compaction.**

## Agent Invocation

**Pass task ID, plan file, and context to each agent:**
```
Task(subagent_type="cc10x:component-builder", prompt="
## Task Context
- **Task ID:** {taskId}
- **Plan File:** {planFile or 'None'}

## User Request
{request}

## Requirements
{from AskUserQuestion or 'See plan file'}

## Memory Summary
{brief summary from activeContext.md}

## Project Patterns
{key patterns from patterns.md}

## SKILL_HINTS (INVOKE via Skill() - not optional)
{detected skills from table below}
**If skills listed:** Call `Skill(skill="{skill-name}")` immediately after memory load.

---
IMPORTANT:
- If your tools include `Edit` **and you are not running in a parallel phase**, update `.claude/cc10x/{activeContext,patterns,progress}.md` at the end per `cc10x:session-memory` and `Read(...)` back to verify.
- If you are running in a parallel phase (e.g., BUILD’s review/hunt phase), prefer **no memory edits**; include a clearly labeled **Memory Notes** section so the main assistant can persist safely after parallel completion.
- If your tools do NOT include `Edit`, you MUST include a `### Memory Notes (For Workflow-Final Persistence)` section with:
  - **Learnings:** [insights for activeContext.md]
  - **Patterns:** [gotchas for patterns.md]
  - **Verification:** [results for progress.md]

Execute the task and include 'Task {TASK_ID}: COMPLETED' in your output when done.
")
```

**TASK ID is REQUIRED in prompt.** Router updates task status after agent returns (agents do NOT call TaskUpdate for their own task).
**SKILL_HINTS:** If router passes skills in SKILL_HINTS, agent MUST call `Skill(skill="{skill-name}")` after loading memory. This includes both cc10x skills (github-research) and complementary skills (react-best-practices, mongodb-agent-skills, etc.).

**Post-Agent Validation (After agent completes):**

When agent returns, verify output quality before proceeding.

### Required Output by Agent

| Agent | Mode | Required Sections | Required Evidence |
|-------|------|-------------------|-------------------|
| component-builder | WRITE | TDD Evidence (RED + GREEN) | Exit codes: 1 (RED), 0 (GREEN) |
| code-reviewer | READ-ONLY | Critical Issues, Verdict, **Memory Notes** | Confidence scores (≥80) |
| silent-failure-hunter | READ-ONLY | Critical (blocks ship), Router Handoff, **Memory Notes** | Count of issues found |
| integration-verifier | READ-ONLY | Scenarios table, Verdict, **Memory Notes** | PASS/FAIL per scenario |
| bug-investigator | WRITE | Root cause, TDD Evidence (RED + GREEN), Variant Coverage, Fix applied | Exit codes: 1 (RED), 0 (GREEN) |
| planner | WRITE | Plan saved path, Phases | Confidence score |

**Memory Notes schema (READ-ONLY agents):**
- **Learnings:** [insights for activeContext.md]
- **Patterns:** [gotchas for patterns.md]
- **Verification:** [results for progress.md]

### Validation Logic

```
After agent completes:

1. Check for required sections in output
2. Check for skill loading evidence (SKILL_HINTS loaded?)

3. If REQUIRED sections are missing:
   → Create remediation task (evidence-only; no code changes intended):
     TaskCreate({
       subject: "CC10X REM-EVIDENCE: {agent} missing {sections}",
       description: "Agent output incomplete. Missing: {sections}\n\nRequired: re-run the relevant command(s) and report the missing evidence in the required format (exit codes, verdicts, etc).",
       activeForm: "Collecting missing evidence"
     })

   → Task-enforced gate (do not rely on self-discipline):
     - Find downstream workflow tasks via TaskList() (subjects prefixed with `CC10X `)
     - For every downstream task that is not completed:
       TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })

   → STOP. Do not invoke the next agent.
     Only proceed after remediation completes OR user explicitly approves bypass (and record it in memory).

**Circuit breaker:** Before creating `CC10X REM-FIX:` task, if count ≥ 3 → AskUserQuestion:
- **Research best practices (Recommended)** → `Skill(skill="cc10x:github-research")`, persist to `docs/research/`, retry with insights
- **Fix locally** → Create another REM-FIX task
- **Skip** → Proceed despite errors (not recommended)
- **Abort** → Stop workflow, manual fix

4. If silent-failure-hunter reports CRITICAL issues (count > 0):
   → Treat as WORKFLOW BLOCKER until fixed.
   → Create a remediation task for component-builder (code changes intended):
     TaskCreate({
       subject: "CC10X REM-FIX: Fix CRITICAL silent failures",
       description: "Fix the CRITICAL issues reported by silent-failure-hunter.\n\nAfter fixing: include TDD Evidence (RED+GREEN) and list files changed.",
       activeForm: "Fixing silent failures"
     })
   → Task-enforced gate:
     - Block all downstream CC10x tasks until remediation completes:
       TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })
   → STOP. Do not proceed to integration-verifier until remediation is completed (or user explicitly accepts shipping with known issues and records it in memory).

4b. If code-reviewer verdict is "Changes Requested" OR Critical Issues exist:
   → Treat as WORKFLOW BLOCKER until fixed.
   → Create a remediation task (code changes intended):
     TaskCreate({
       subject: "CC10X REM-FIX: Address code-reviewer critical issues",
       description: "Fix the Critical Issues reported by code-reviewer.\n\nAfter fixing: include TDD Evidence (RED+GREEN) and list files changed.",
       activeForm: "Fixing review issues"
     })
   → Task-enforced gate:
     - Block all downstream CC10x tasks until remediation completes:
       TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })
   → STOP. Do not proceed until remediation is completed (or user explicitly accepts shipping with known issues and records it in memory).

5. If bug-investigator is missing TDD Evidence (RED+GREEN) or Variant Coverage:
   → Treat as WORKFLOW BLOCKER until evidence is provided.
   → Create remediation task (may involve code/test changes):
     TaskCreate({
       subject: "CC10X REM-FIX: bug-investigator missing TDD/variants",
       description: "Add regression test (RED), then fix (GREEN) and report exit codes.\nAlso document Variant Coverage and confirm no hardcoding.",
       activeForm: "Adding regression coverage"
     })
   → Task-enforced gate:
     - Block all downstream CC10x tasks until remediation completes:
       TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })
   → STOP. Do not proceed to code-reviewer/integration-verifier until remediation is completed (or user explicitly accepts bypassing TDD and records it in memory).

6. If NON-CRITICAL missing (skill evidence):
   → Note for improvement, continue workflow

7. If validation PASSES:
   → Proceed to next agent in chain
```

**Validation Evidence Format (include in your response):**
```
### Agent Validation: {agent_name}
- Required Sections: [Present/Missing]
- Evidence: [Present/Missing]
- Proceeding: [Yes/No + reason]
```

## Remediation Re-Review Loop (Pseudocode)

```
WHEN any CC10X REM-FIX task COMPLETES:
  │
  ├─→ 1. TaskCreate({ subject: "CC10X code-reviewer: Re-review after remediation" })
  │      → Returns re_reviewer_id
  │
  ├─→ 2. TaskCreate({ subject: "CC10X silent-failure-hunter: Re-hunt after remediation" })
  │      → Returns re_hunter_id
  │
  ├─→ 3. Find verifier task:
  │      TaskList() → Find task where subject contains "integration-verifier"
  │      → verifier_task_id
  │
  ├─→ 4. Block verifier on re-reviews:
  │      TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [re_reviewer_id, re_hunter_id] })
  │
  └─→ 5. Resume chain execution (re-reviews run before verifier)
```

**Why:** Code changes must be re-reviewed before shipping (orchestration integrity).

**How it works:** Task() is synchronous - router waits for agent to complete and receives its output before proceeding to next agent.

**Skill triggers for agents (DETECT AND PASS AS SKILL_HINTS):**

| Detected Pattern | Skill | Agents |
|------------------|-------|--------|
| External: new tech (post-2024), unfamiliar library, complex integration (auth, payments) | cc10x:github-research | planner, bug-investigator |
| Debug exhausted: 3+ local attempts failed, external service error | cc10x:github-research | bug-investigator |
| User explicitly requests: "research", "github", "octocode", "find on github", "how do others", "best practices" | cc10x:github-research | planner, bug-investigator |

**Detection runs BEFORE agent invocation. Pass detected skills in SKILL_HINTS.**

## Skill Loading Hierarchy (DEFINITIVE)

**Two mechanisms exist:**

### 1. Agent Frontmatter `skills:` (PRELOAD - Automatic)
```yaml
skills: cc10x:session-memory, cc10x:code-generation, cc10x:frontend-patterns
```
- Load AUTOMATICALLY when agent starts
- Full skill content injected into agent context
- Agent does NOT need to call `Skill()` for these
- **This is the PRIMARY mechanism for ALL skills except github-research**

### 2. Router's SKILL_HINTS (github-research ONLY)
- Router detects external research triggers and passes hint in prompt
- Agent calls `Skill(skill="cc10x:github-research")` when hint is present
- Only used for github-research (requires external API, not always needed)

## Gates (Must Pass)

1. **MEMORY_LOADED** - Before routing
2. **TASKS_CHECKED** - Check TaskList() for active workflow
3. **INTENT_CLARIFIED** - User intent is unambiguous (all workflows)
4. **RESEARCH_EXECUTED** - Before planner (if github-research detected)
5. **RESEARCH_PERSISTED** - Save to docs/research/ + update activeContext.md (if research was executed)
6. **REQUIREMENTS_CLARIFIED** - Before invoking agent (BUILD only)
7. **TASKS_CREATED** - Workflow task hierarchy created
8. **ALL_TASKS_COMPLETED** - All workflow tasks (including Memory Update) status="completed"
9. **MEMORY_UPDATED** - Before marking done

## Chain Execution Loop (Task-Based)

**NEVER stop after one agent.** The workflow is NOT complete until ALL tasks are completed.

### Execution Loop

```
1. Find runnable tasks:
   TaskList() → Find tasks where:
   - status = "pending"
   - blockedBy is empty OR all blockedBy tasks are "completed"

2. Start agent(s):
   - TaskUpdate({ taskId: runnable_task_id, status: "in_progress" })
   - Otherwise, if multiple agent tasks are ready (e.g., code-reviewer + silent-failure-hunter):
     → Invoke BOTH in same message (parallel execution)
   - Pass task ID in prompt:
     Task(subagent_type="cc10x:{agent}", prompt="
       Your task ID: {taskId}
       User request: {request}
       Requirements: {requirements}
       Memory: {activeContext}
       SKILL_HINTS: {detected skills}
     ")

3. After agent completes:
   - Router updates task: TaskUpdate({ taskId: runnable_task_id, status: "completed" })
   - Router validates output (see Post-Agent Validation)
   - Router calls TaskList() to find next available tasks

4. Determine next:
   - Find tasks where ALL blockedBy tasks are "completed"
   - If multiple ready → Invoke ALL in parallel (same message)
   - If one ready → Invoke sequentially
   - If none ready AND uncompleted tasks exist → Wait (error state)
   - If ALL tasks completed → Workflow complete

5. Repeat until:
   - All tasks have status="completed" (INCLUDING the Memory Update task)
   - OR critical error detected (create error task, halt)

**CRITICAL:** The workflow is NOT complete until the "CC10X Memory Update" task is completed.
This ensures Memory Notes from READ-ONLY agents are persisted even if context compacted.
```

### Parallel Execution

When multiple tasks become unblocked simultaneously (e.g., code-reviewer AND silent-failure-hunter after component-builder completes):

```
# Both ready after builder completes
TaskUpdate({ taskId: reviewer_id, status: "in_progress" })
TaskUpdate({ taskId: hunter_id, status: "in_progress" })

# Invoke BOTH in same message = parallel execution
Task(subagent_type="cc10x:code-reviewer", prompt="Your task ID: {reviewer_id}...")
Task(subagent_type="cc10x:silent-failure-hunter", prompt="Your task ID: {hunter_id}...")
```

**CRITICAL:** Both Task calls in same message = both complete before you continue.

### Workflow-Final Memory Persistence (Task-Enforced)

Memory persistence is enforced via the "CC10X Memory Update" task in the task hierarchy.

**When you see this task become available:**
1. Review agent outputs for `### Memory Notes` sections
2. Follow the task description to persist learnings
3. Use Read-Edit-Read pattern for each memory file
4. Mark task completed

**Why task-enforced:**
- Tasks survive context compaction
- Tasks are visible in TaskList() - can't be forgotten
- Task description contains explicit instructions
- Workflow isn't complete until Memory Update task is done

**Why this design:**
- READ-ONLY agents (code-reviewer, silent-failure-hunter, integration-verifier) cannot persist memory themselves
- You (main assistant) collect their Memory Notes and persist at workflow-final
- This avoids parallel edit conflicts and ensures nothing is lost

### TODO Task Handling (After Workflow Completes)

After all workflow tasks complete, check for `CC10X TODO:` tasks created by agents:

```
1. TaskList() → Find tasks with subject starting "CC10X TODO:"

2. If TODO tasks exist:
   → List them: "Agents identified these items for follow-up:"
     - [task subject] - [first line of description]
   → Ask user: "Address now (start new workflow) / Keep for later / Delete"

3. User chooses:
   - "Address now" → Start new BUILD/DEBUG workflow for the TODO
   - "Keep" → Leave tasks pending (will appear next session)
   - "Delete" → TaskUpdate({ taskId, status: "deleted" }) for each

4. Continue to MEMORY_UPDATED gate
```

**Why TODO tasks are separate:** They are non-blocking discoveries made during agent work. They don't auto-execute because they lack proper context/dependencies. User decides priority.

## Results Collection (Parallel Agents)

**Task system handles coordination. The main assistant (running this router) handles results.**

When parallel agents complete (code-reviewer + silent-failure-hunter), their outputs must be passed to the next agent.

### Pattern: Collect and Pass Findings

```
# After both parallel agents complete:
1. TaskList()  # Verify both show "completed"

2. Collect outputs from this response:
   REVIEWER_FINDINGS = {code-reviewer's Critical Issues + Verdict}
   HUNTER_FINDINGS = {silent-failure-hunter's Router Handoff section (preferred), else Critical section}

3. Pass to integration-verifier:
   Task(subagent_type="cc10x:integration-verifier", prompt="
   ## Task Context
   - **Task ID:** {verifier_task_id}

   ## Previous Agent Findings (REVIEW BEFORE VERIFYING)

   ### Code Reviewer
   **Verdict:** {Approve/Changes Requested}
   **Critical Issues:**
   {REVIEWER_FINDINGS}

   ### Silent Failure Hunter
   **Critical Issues:**
   {HUNTER_FINDINGS}

   ---
   Verify the implementation. Consider ALL findings above.
   Any CRITICAL issues should block PASS verdict.
   ")
```

### Why Both Task System AND Results Passing

| Aspect | Tasks Handle | Router Handles |
|--------|--------------|----------------|
| Completion status | Automatic | - |
| Dependency unblocking | Automatic | - |
| Agent findings/output | NOT shared | Pass in prompt |
| Conflict resolution | - | Include both findings |
