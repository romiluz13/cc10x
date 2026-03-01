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
# If any section missing, insert before ## Last Updated. Example:
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Last Updated",
     new_string="## References\n- Plan: N/A\n- Design: N/A\n- Research: N/A\n\n## Last Updated")
# VERIFY after each heal
Read(file_path=".claude/cc10x/activeContext.md")
```

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
- **Reconstruct memory_task_id (exact taskId preferred over subject search):**
  1. Read(file_path=".claude/cc10x/activeContext.md") → look for `[cc10x-internal] memory_task_id:` line in ## References
  2. If found:
     a. If taskId is a valid non-empty value: use it directly (collision-safe, even in shared TaskLists)
     b. If taskId is missing or invalid (partial compaction — e.g., line reads "[cc10x-internal] memory_task_id: wf:43"): extract `wf:{parent_task_id}` and use scoped fallback:
        `TaskList()` → filter subject starts with "CC10X Memory Update:" AND description contains `wf:{parent_task_id}` AND status IN [pending, in_progress] → use first match (workflow-scoped)
  3. If NOT found at all: `TaskList()` → filter subject starts with "CC10X Memory Update:" AND status IN [pending, in_progress] → use first match (unscoped fallback — single-session assumption)
  4. Assign to `memory_task_id` before invoking any agent (step 3a requires this)

**Safety rule (avoid cross-project collisions):**
- If you find tasks that do NOT clearly belong to CC10x, do not resume them.
- If unsure, ask the user whether to resume or create a fresh task hierarchy.

**Legacy compatibility:** Older CC10x versions may have created tasks with subjects starting `BUILD:` / `DEBUG:` / `REVIEW:` / `PLAN:` (without the `CC10X` prefix).
- If such tasks exist, ask the user whether to resume the legacy tasks or start a fresh CC10X-namespaced workflow.

Task lists can be shared across sessions via `CLAUDE_CODE_TASK_LIST_ID`. Treat TaskLists as potentially long-lived; always scope before resuming.

**If no active tasks:**
- Proceed with workflow selection below

## Task Dependency Safety

All `addBlockedBy` calls are forward-only: downstream tasks blocked by upstream, never reverse. All workflows are DAGs — no cycles possible.

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
# Replace {parent_task_id} below with workflow_task_id (returned by the parent BUILD task created in step 1)
TaskCreate({
  subject: "CC10X Memory Update: Persist workflow learnings",
  description: "REQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\n**Instructions:**\n1. Read Memory Notes from THIS task's description — they were captured between '---' separator lines by the router immediately after each agent completed (compaction-safe). Do NOT search conversation history.\n2. Persist learnings to .claude/cc10x/activeContext.md ## Learnings\n3. Persist patterns to .claude/cc10x/patterns.md ## Common Gotchas\n4. For **Deferred:** entries in agent Memory Notes: Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n5. Persist verification to .claude/cc10x/progress.md ## Verification\n\n**Pattern:**\nRead(file_path=\".claude/cc10x/activeContext.md\")\nEdit(old_string=\"## Learnings\", new_string=\"## Learnings\\n- [from agent]: {insight}\")\nRead(file_path=\".claude/cc10x/activeContext.md\")  # Verify\n\nRepeat for patterns.md and progress.md.\n\n**Freshness (prevent bloat):**\n- activeContext.md ## Recent Changes: Find `[BUILD-START: wf:{parent_task_id}]` in ## Recent Changes (extract parent_task_id from `[workflow-scope: wf:{parent_task_id}]` at end of this description). Replace FROM that marker onward with this workflow's final summary. Preserve all entries BEFORE that marker.\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- Collect Memory Notes from READ-ONLY agents only (code-reviewer, silent-failure-hunter, integration-verifier) — WRITE agents (component-builder, bug-investigator, planner) already wrote memory directly; skip their Memory Notes to avoid duplicates.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
# Replace {parent_task_id} below with workflow_task_id (returned by the parent DEBUG task created above)
TaskCreate({
  subject: "CC10X Memory Update: Persist debug learnings",
  description: "REQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\nFocus on:\n- Root cause for patterns.md ## Common Gotchas\n- Debug attempt history for activeContext.md\n- Verification evidence for progress.md\n- **Deferred:** entries from Memory Notes → Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- activeContext.md ## Recent Changes: Find `[DEBUG-RESET: wf:{parent_task_id}]` in ## Recent Changes (extract parent_task_id from `[workflow-scope: wf:{parent_task_id}]` at end of this description). Replace FROM that marker onward with this workflow's final summary. Preserve all entries BEFORE that marker.\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- Collect Memory Notes from READ-ONLY agents only (code-reviewer, integration-verifier) — WRITE agents (bug-investigator) already wrote memory directly; skip their Memory Notes to avoid duplicates.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
# Replace {parent_task_id} below with workflow_task_id (returned by the parent REVIEW task created above)
TaskCreate({
  subject: "CC10X Memory Update: Persist review learnings",
  description: "REQUIRED: Collect Memory Notes from code-reviewer output and persist to memory files.\n\nFocus on:\n- Patterns discovered for patterns.md\n- Review verdict for progress.md\n- **Deferred:** entries from Memory Notes → Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
# Replace {parent_task_id} below with workflow_task_id (returned by the parent PLAN task created above)
TaskCreate({
  subject: "CC10X Memory Update: Index plan in memory",
  description: "REQUIRED: Update memory files with plan reference.\n\nFocus on:\n- Add plan file to activeContext.md ## References\n- Update progress.md with plan status\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
  activeForm: "Indexing plan in memory"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [planner_task_id] })
```

## Workflow Execution

### BUILD
> **NEVER call `EnterPlanMode`.** Use `AskUserQuestion` for user decisions.

1. Load memory → Check if already done in progress.md
2. **Plan-First Gate** (STATE-BASED, not phrase-based):
   - Skip ONLY if: (plan in `## References` ≠ "N/A") AND (active `CC10X` task exists)
   - **Trivial request heuristic** (auto-select "Build directly" — skip AskUserQuestion): If request is under 20 words AND contains none of: API, database, db, schema, migration, component, multiple files, refactor, auth, security, crypto, payment, password — select "Build directly" automatically and log: "Plan-First Gate: trivial request detected, skipping plan prompt."
   - Otherwise → AskUserQuestion: "Plan first (Recommended) / Build directly"
3. **Clarify requirements** (DO NOT SKIP):
   - **Pre-answers (always run first):** Read activeContext.md `## Decisions` — look for entries starting with `"Planner clarification ["`. If found, treat those Q→A pairs as pre-answered (do NOT re-ask them).
   - **Ambiguity check:** If the request explicitly states (a) the file/component to change, (b) the function/behavior to change, (c) what the change is, AND (d) acceptance criteria or expected outcome — AND pre-answers cover all gaps — skip the AskUserQuestion below. If ANY element is missing, vague, or contradictory → continue to AskUserQuestion.
   - **Then:** Use AskUserQuestion for any remaining unanswered requirements.
   - Pass all answers (pre-populated + new) to component-builder in prompt under `## Pre-Answered Requirements`.
   - **Persist answers (compaction-safe):** For each NEW Q&A gathered from AskUserQuestion in this step (skip pre-populated answers already in Decisions from Planner clarification): Edit activeContext.md ## Decisions appending `- Build clarification [{current_date}]: {question} → {answer}`. Read-back verify after each append.
4. **Create task hierarchy** (see Task-Based Orchestration above)
4a. **Write BUILD-START marker** (immediately after task hierarchy created — before any agent runs):
    ```
    Edit(file_path=".claude/cc10x/activeContext.md",
         old_string="## Recent Changes",
         new_string="## Recent Changes\n[BUILD-START: wf:{workflow_task_id}]")
    Read(file_path=".claude/cc10x/activeContext.md")  # VERIFY marker written
    # If marker NOT found in Read output: STOP — retry Edit before proceeding to step 5
    ```
5. **Start chain execution** (see Chain Execution Loop below)
6. Update memory when all tasks completed

### Execution Depth Selector (BUILD only)

**Pre-check (runs FIRST — before evaluating any condition):**
`Bash(command="git diff --name-only HEAD 2>/dev/null || echo NO_GIT")`
→ If output is `NO_GIT`: **use FULL depth immediately. Stop here. Do NOT evaluate conditions 1-5.** Cannot verify security scope without git history.

**Default: FULL.** Use QUICK only if ALL 5 conditions are met:
1. Single-unit change (one file, one function)
2. No security implications — verified by BOTH:
   (a) Request text doesn't contain: auth, crypto, security, payment, password, secret, token, permission, role, jwt, oauth, session
   (b) `git diff --name-only HEAD` output doesn't match paths: auth/, security/, crypto/, payment/, token/, permission/, secrets/, passwords/, roles/
   (Note: NO_GIT case already handled by the pre-check above — if we reach condition 2, we are in a git repo)
3. No cross-layer dependencies (e.g., API + DB + UI)
4. No open `CC10X REM-FIX` tasks in current workflow
5. Requirements are explicit and unambiguous

| Depth | Chain | When |
|-------|-------|------|
| **FULL** | component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier | Default for all BUILD |
| **QUICK** | component-builder → integration-verifier | ALL 5 conditions above met |

**QUICK still requires:** Router Contract validation + verifier + memory update.
**Blocking signal during QUICK** (verifier FAIL, test failure, lint error):
→ AskUserQuestion: "Quick verification failed ({reason}). Escalating to full review adds code-reviewer + silent-failure-hunter before final verification. Continue?"
  Options: "Run full review chain (Recommended)" | "Abort — I'll investigate manually"
→ If "Run full review chain": Invoke code-reviewer + silent-failure-hunter in parallel (same as standard BUILD), then re-invoke integration-verifier
→ If "Abort": Record in activeContext.md ## Decisions: "QUICK escalation declined by user", stop workflow

### DEBUG
1. Load memory → Check patterns.md Common Gotchas
2. **CLARIFY (REQUIRED)**: Use AskUserQuestion if ANY ambiguity:
   - What error message/behavior?
   - Expected vs actual?
   - When did it start?
   - Which component/file affected?
3. **Check for research trigger (Pre-investigation):**
   - User explicitly requested research ("research", "github", "octocode"), OR
   - External service error (API timeout, auth failure, third-party)

   **If ANY trigger met:**
   → AskUserQuestion: "Before debugging, should we research similar issues on GitHub? This makes external API calls and saves findings to docs/research/."
     Options: "Research GitHub (Recommended)" | "Skip research" | "Abort workflow"
   → If "Research GitHub": Execute THREE-PHASE research (octocode tools → persist → pass to agent)
   → If "Abort": Record in activeContext.md ## Decisions: "Research declined", stop workflow

   **Debug Workflow Scoping:**
   - Note: bug-investigator writes its own `[DEBUG-RESET: wf:{task_id}]` marker at startup — see agent file.
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
> **NEVER call `EnterPlanMode`.** Invoke the planner agent — it writes plan files directly.

1. Load memory
2. **Clarification (if request is vague or ambiguous):**
   → `Skill(skill="cc10x:brainstorming")` — runs in main context, `AskUserQuestion` available here
   → Collect answers, pass clarified requirements to planner in step 4
3. **If github-research detected (external tech OR explicit request):**
   - Execute research FIRST using octocode tools directly (NOT as hint)
   - Use: `mcp__octocode__packageSearch`, `mcp__octocode__githubSearchCode`, etc.
   - **PERSIST research** → Save to `docs/research/YYYY-MM-DD-<topic>-research.md`
   - **Update memory** → Add to activeContext.md References section
   - Summarize findings before invoking planner
4. **Create task hierarchy** (see Task-Based Orchestration above)
5. **Start chain execution** (pass clarified requirements + research results + file path in prompt if step 3 was executed)
5a. **After planner task completes — collect user input if needed:**
    → Check planner output for "**Your Input Needed:**" section
    → If section exists and has bullet points:
      → AskUserQuestion: "Before BUILD starts, planner flagged these assumptions that need your input:\n{extracted bullet points}\nProvide answers (or confirm the defaults)."
      → Collect answers → Persist to activeContext.md ## Decisions with Edit: "- Planner clarification [{date}]: {Q} → {A}"
      → Include answers summary in BUILD context: When invoking component-builder, add "## Planner Clarifications\n{Q+A pairs}" to prompt
    → If section empty or absent: Proceed directly to step 6 (Memory Update)
6. Update memory → Reference saved plan when task completed

**THREE-PHASE for External Research (MANDATORY):**
```
If router detected github-research signal (external tech, explicit request, or 3+ failed debug attempts):
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
- **NEVER call `EnterPlanMode`.** This is an execution agent that writes files directly. Plan mode would block Write/Edit tools and prevent saving outputs.
- If your tools include `Edit` **and you are not running in a parallel phase**, update `.claude/cc10x/{activeContext,patterns,progress}.md` at the end per `cc10x:session-memory` and `Read(...)` back to verify.
- If you are running in a parallel phase (e.g., BUILD’s review/hunt phase), prefer **no memory edits**; include a clearly labeled **Memory Notes** section so the main assistant can persist safely after parallel completion.
- If your tools do NOT include `Edit`, you MUST include a `### Memory Notes (For Workflow-Final Persistence)` section with:
  - **Learnings:** [insights for activeContext.md]
  - **Patterns:** [gotchas for patterns.md]
  - **Verification:** [results for progress.md]

Execute the task and include ‘Task {TASK_ID}: COMPLETED’ in your output when done.
")
```

**TASK ID is REQUIRED in prompt.** Agents call TaskUpdate(completed) for their own task after final output. Router verifies via TaskList().
**SKILL_HINTS:** If router passes skills in SKILL_HINTS, agent MUST call `Skill(skill="{skill-name}")` after loading memory. This includes complementary skills (react-best-practices, mongodb-agent-skills, etc.) — not github-research (router-executed directly via THREE-PHASE).

**Post-Agent Validation (After agent completes):**

When agent returns, verify output quality before proceeding.

---

### Router Contract Validation (PRIMARY - Use This First)

**Step 1: Check for Router Contract**
```
Look for "### Router Contract (MACHINE-READABLE)" section in agent output.
If found → Use contract-based validation below.
If NOT found → Agent output is non-compliant.
  **REM-EVIDENCE Loop Cap (before creating task):**
    # Substitute {agent} with the actual agent name from the failed output (e.g., "code-reviewer", "silent-failure-hunter", "integration-verifier")
    Count: TaskList() → filter subject contains "CC10X REM-EVIDENCE:" AND subject contains "{agent}" AND status IN [pending, in_progress, completed]
    If count >= 1: AskUserQuestion: "Agent {agent} has already been re-invoked once via REM-EVIDENCE and still has not produced a Router Contract. How to proceed?"
      Options: "Retry once more" | "Skip agent, proceed without its review" | "Abort workflow"
      → Handle chosen option, then STOP. Do NOT create another REM-EVIDENCE task.
    If count < 1: Create REM-EVIDENCE task:
  TaskCreate({
    subject: "CC10X REM-EVIDENCE: [router-internal] {agent} missing Router Contract",
    description: "Agent output lacks '### Router Contract (MACHINE-READABLE)' section. Re-invoke the same agent once with a modified prompt: append the following note to the original prompt: 'NOTE: Your previous output succeeded but lacked the ### Router Contract (MACHINE-READABLE) section. Your work is already saved to memory. Please re-output ONLY the Router Contract YAML block — do NOT redo investigation/build/review from scratch.' If Router Contract still missing after retry, AskUserQuestion to decide next action.",
    activeForm: "Collecting agent contract"
  })
  Block downstream tasks and STOP.
```

**Step 2: Parse and Validate Contract**
```
Parse the YAML block inside Router Contract section.

CONTRACT FIELDS:
- STATUS: Agent's self-reported status (PASS/FAIL/APPROVE/etc)
- BLOCKING: true/false - whether workflow should stop
- REQUIRES_REMEDIATION: true/false - whether REM-FIX task needed
- REMEDIATION_REASON: Exact text for remediation task description
- CRITICAL_ISSUES: Count of blocking issues (if applicable)
- MEMORY_NOTES: Structured notes for workflow-final persistence

VALIDATION RULES:

**0. CONTRACT RULE Enforcement (RUNS FIRST — auto-override STATUS if violated):**

Before applying rules 1a/1b/2, validate each agent's self-reported STATUS against its CONTRACT RULE:

| Agent | CONTRACT RULE violation → Override |
|-------|-------------------------------------|
| component-builder | STATUS=PASS but TDD_RED_EXIT≠1 OR TDD_GREEN_EXIT≠0 → STATUS=FAIL, BLOCKING=true, REMEDIATION_REASON="CONTRACT RULE violated: TDD evidence missing" |
| bug-investigator | STATUS=FIXED but (TDD_RED_EXIT≠1 OR TDD_GREEN_EXIT≠0 OR VARIANTS_COVERED<1) AND contract.NEEDS_EXTERNAL_RESEARCH != true → STATUS=FAIL, BLOCKING=true, REQUIRES_REMEDIATION=true, REMEDIATION_REASON="CONTRACT RULE violated: TDD evidence missing — add regression test (RED→GREEN) + variant coverage" |
| code-reviewer | STATUS=APPROVE but CRITICAL_ISSUES>0 OR CONFIDENCE<80 → STATUS=CHANGES_REQUESTED, REQUIRES_REMEDIATION=true; BLOCKING=true only if CRITICAL_ISSUES>0 |
| integration-verifier | STATUS=PASS but SCENARIOS_PASSED≠SCENARIOS_TOTAL → STATUS=FAIL, BLOCKING=true |
| planner | STATUS=PLAN_CREATED but PLAN_FILE is null/empty OR CONFIDENCE<50 → STATUS=NEEDS_CLARIFICATION |

**If override applied:** Log in output: "⚠️ CONTRACT RULE override: {agent} self-reported {original} but rule violated (TDD_RED_EXIT={X}/TDD_GREEN_EXIT={Y}/etc.). Overriding STATUS to {new_status}."

Proceed with rules 1a/1b/2 using the OVERRIDDEN values.

**Circuit Breaker (BEFORE creating any REM-FIX):**
Before creating a new REM-FIX task, count ACTIVE REM-FIX tasks: `TaskList()` → filter by (subject contains "CC10X REM-FIX:") AND (status IN [pending, in_progress]). Do NOT count completed REM-FIX tasks — they are resolved and irrelevant.
If count ≥ 3 → AskUserQuestion: "Too many active fix attempts are stacking up ({N} active CC10X REM-FIX tasks). This may indicate a deeper systemic issue. How to proceed?"
- **Research best practices (Recommended)** → Skill(skill="cc10x:github-research"), persist, retry
- **Fix locally** → Create another REM-FIX task
- **Skip** → Proceed despite errors (not recommended)
- **Abort** → Stop workflow, manual fix

# (rule 2e was moved here as rule 0c — runs BEFORE rule 1a, not after rule 2)
0c. If contract.NEEDS_EXTERNAL_RESEARCH == true (bug-investigator only):
    **Runs BEFORE rule 1a — do NOT evaluate rules 1a/1b/2 when this fires.**
    → Execute THREE-PHASE research immediately using contract.RESEARCH_REASON as query:
      PHASE 1: Search using octocode tools (mcp__octocode__githubSearchCode, etc.)
      PHASE 2: PERSIST → Bash(command="mkdir -p docs/research")
               Write(file_path="docs/research/YYYY-MM-DD-{topic}-research.md", content="[findings]")
               Edit(activeContext.md ## References, add "- Research: docs/research/...")
      **Research Loop Cap (BEFORE PHASE 3):**
        Count external research iterations: Read(.claude/cc10x/activeContext.md) → count entries in ## References that match `docs/research/` (each represents one completed research cycle for this workflow)
        If count >= 2: AskUserQuestion: "External research has been provided to bug-investigator {count} time(s) and it still reports NEEDS_EXTERNAL_RESEARCH. How to proceed?"
          Options: "Try research once more" | "Create manual fix task (skip re-invoke)" | "Abort workflow" | "Research best practices (cc10x:github-research)"
          → Do NOT proceed to PHASE 3. Handle chosen option, then STOP.
        If count < 2: Proceed to PHASE 3 below.
      PHASE 3: Re-invoke cc10x:bug-investigator with same prompt + "## External Research Findings\nSaved to: {research_file}\n{key_findings}"
    → Do NOT create REM-FIX task — research IS the response
    → STOP after PHASE 3 — do not evaluate rules 1a/1b/2 for this contract

0b. If contract.STATUS == "SELF_REMEDIATED":
    → The agent has autonomously created a REM-FIX task and blocked itself (or downstream tasks).
    → Acknowledge the self-healing action: log "Agent {agent} has self-remediated via TaskCreate."
    → Do NOT create a duplicate REM-FIX task.
    → DO NOT force the agent's task to "completed" in the fallback check. Wait for the fix task to execute natively.
    → STOP evaluating rules 1a/1b/2 for this agent's contract.

1a. If contract.BLOCKING == true AND contract.STATUS NOT IN ["NEEDS_CLARIFICATION", "INVESTIGATING", "BLOCKED", "SELF_REMEDIATED", "REVERT_RECOMMENDED", "LIMITATION_ACCEPTED"] AND contract.NEEDS_EXTERNAL_RESEARCH != true:
    **Parallel blocking merge (pre-check — BUILD only, runs before TaskCreate):**
    → If currently processing parallel review phase (code-reviewer ∥ silent-failure-hunter outputs in same response):
      → Check sibling agent's Router Contract in this same response — does sibling ALSO have BLOCKING=true?
      → If YES (both agents blocking):
          merged_subject = "CC10X REM-FIX: code-reviewer + silent-failure-hunter — multiple blocking issues"
          merged_description = "**code-reviewer issues:**\n" + reviewer_contract.REMEDIATION_REASON + "\n\n**silent-failure-hunter issues:**\n" + hunter_contract.REMEDIATION_REASON
      → If NO (only this agent blocking): use this agent's data alone (existing behavior)
    → If NOT parallel phase: use this agent's data alone (existing behavior)
    → TaskCreate({
        subject: merged_subject ?? "CC10X REM-FIX: {agent_name} — {first 60 chars of (contract.REMEDIATION_REASON ?? 'see agent output')}",
        description: merged_description ?? (contract.REMEDIATION_REASON ?? "REMEDIATION_REASON null — re-check agent Router Contract output."),
        activeForm: "Fixing {agent_name} issues"
      })
    → Task-enforced gate:
      - Find downstream workflow tasks via TaskList() (subjects prefixed with `CC10X `)
      - For every downstream task not completed:
        TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })
    → STOP. Do not invoke next agent until remediation completes.

1b. If contract.REQUIRES_REMEDIATION == true AND contract.BLOCKING == false:
    **ALWAYS AskUserQuestion — unconditionally, whether serial or parallel phase.**
    → Gather context first:
      - If parallel phase AND sibling agent also has REQUIRES_REMEDIATION=true: merge both REMEDIATION_REASONs into one combined message
      - Otherwise (serial phase or sibling has no issues): use this agent's REMEDIATION_REASON alone
    → AskUserQuestion: "{merged or single REMEDIATION_REASON} — fix before continuing?"
      Options: "Fix now (Recommended)" | "Proceed anyway"
    → "Fix now" → Circuit Breaker check, then apply rule 1a for each affected agent
    → "Proceed" → Edit activeContext.md ## Decisions: "{agent(s)}: HIGH issues skipped by user", continue
               → Edit patterns.md ## Common Gotchas: append "[Skipped HIGH — {agent}]: {first 80 chars of (REMEDIATION_REASON ?? 'see agent output')}"

2. **Only applies when:** code-reviewer STATUS=APPROVE AND silent-failure-hunter found issues (parallel phase, Cases A and B only). All other reviewer+hunter combinations are handled by rules 1a/1b before reaching rule 2.
   → **Conflict check** — compare reviewer and hunter verdicts:
   **Case A:** code-reviewer STATUS=APPROVE AND silent-failure-hunter CRITICAL_ISSUES > 0:
     AskUserQuestion: "Reviewer approved, but Hunter found {N} critical silent failures. Investigate or skip?"
     - "Investigate" → Create REM-FIX for hunter CRITICAL issues (apply rule 1a)
     - "Skip" → Record decision in memory, proceed to verifier
   **Case B:** code-reviewer STATUS=APPROVE AND silent-failure-hunter HIGH_ISSUES > 0 (CRITICAL=0):
     AskUserQuestion: "Reviewer approved, but Hunter found {N} high-severity error handling gaps. Fix before continuing?"
     - "Fix" → Apply rule 1a for hunter HIGH issues (non-blocking REM-FIX)
     - "Proceed anyway" → Record in memory: "Hunter HIGH issues skipped by user", proceed

# (rule 2a not needed — single-agent non-blocking cases are handled by rule 1b above)

2b. If contract.STATUS == "NEEDS_CLARIFICATION" (planner agent):
    → Extract "**Your Input Needed:**" bullet points from planner output
    → AskUserQuestion: "Planner needs clarification before the plan can be completed:\n{extracted items}\nPlease answer to unblock planning."
    → Collect user answers → Persist to activeContext.md ## Decisions: "Plan clarification: {Q} → {A}"
    → Re-invoke planner with prompt: "{original prompt}\n\n## User Clarifications\n{answers}"
    → Do NOT proceed to BUILD until planner returns STATUS=PLAN_CREATED

2c. If contract.STATUS == "INVESTIGATING" (bug-investigator):
    → Treat as BLOCKING=true (investigation incomplete — no fix applied yet)
    → Announce to user: "Bug investigator is still investigating (no fix applied yet). Continuing investigation..."
    → TaskCreate({ subject: "CC10X bug-investigator: Continue investigation", description: "Previous attempt: STATUS=INVESTIGATING. ROOT_CAUSE hint: {contract.ROOT_CAUSE}. Continue from this hypothesis." })
    → Block downstream tasks on this new investigation task
    → Re-invoke bug-investigator with previous context included in prompt

2f. If contract.STATUS == "BLOCKED" (bug-investigator terminal stuck state):
    → Investigation is permanently stuck — cannot proceed without external help or user decision
    → AskUserQuestion: "Bug investigation is completely stuck (BLOCKED). ROOT_CAUSE hint: {contract.ROOT_CAUSE}. How to proceed?"
      Options: "Research externally (Recommended)" | "Create manual fix task" | "Abort workflow"
    → "Research externally": Execute THREE-PHASE research (same as rule 0c), re-invoke bug-investigator
    → "Create manual fix task": Proceed as rule 1a (create REM-FIX task)
    → "Abort": Record in activeContext.md ## Decisions: "Investigation aborted (BLOCKED): {ROOT_CAUSE}", stop workflow

2d. If integration-verifier STATUS=REVERT_RECOMMENDED: Log decision, suggest git revert steps, stop workflow (record in memory). Note: user already confirmed revert in-agent.
2d. If integration-verifier STATUS=LIMITATION_ACCEPTED: Record acceptance in activeContext.md ## Decisions, proceed to Memory Update. Note: user already accepted in-agent.
2d. If integration-verifier STATUS=FAIL AND contract.CHOSEN_OPTION=="A" (or not set): Create REM-FIX task (existing behavior). Note: B/C decisions are handled inline by the verifier — see agent file.

3. Collect contract.MEMORY_NOTES for workflow-final persistence

4. If none of above triggered → Proceed to next agent
```

**Step 3: Output Validation Evidence**
```
### Agent Validation: {agent_name}
- Router Contract: Found
- STATUS: {contract.STATUS}
- BLOCKING: {contract.BLOCKING}
- CRITICAL_ISSUES: {contract.CRITICAL_ISSUES}
- HIGH_ISSUES: {contract.HIGH_ISSUES}
- REQUIRES_REMEDIATION: {contract.REQUIRES_REMEDIATION}
- Proceeding: [Yes/No + reason]
```

---

## Remediation Re-Review Loop (Pseudocode)

```
WHEN any CC10X REM-FIX task COMPLETES:
  │
  ├─→ 0. **Cycle Cap Check (RUNS FIRST):**
  │      Count completed "CC10X REM-FIX:" tasks in this workflow: TaskList() → filter subject contains "CC10X REM-FIX:" AND status = "completed"
  │      If count ≥ 2:
  │        → AskUserQuestion: "This workflow has already completed {count} fix cycles. The same issues keep recurring. How to proceed?"
  │          - "Create another fix task" → Continue with steps 1-5 below
  │          - "Research patterns (Recommended)" → Execute cc10x:github-research THREE-PHASE, pass findings to REM-FIX task
  │          - "Accept known issues" → Record in activeContext.md ## Decisions, proceed directly to verifier/memory-update
  │          - "Abort workflow" → Stop; user resolves manually
  │      If count < 2: Continue to step 1 below
  │
  ├─→ 1. Extract the completed REM-FIX task subject (the task that just completed):
  │      → completed_remfix_title = first 50 chars of completed task subject after "CC10X REM-FIX: "
  │      TaskCreate({ subject: "CC10X code-reviewer: Re-review — {completed_remfix_title}" })
  │      → Returns re_reviewer_id
  │
  ├─→ 2. **Skip in DEBUG workflows:** If the parent workflow task subject contains "CC10X DEBUG:" → SKIP step 2 entirely (no hunter in DEBUG chain).
  │      Otherwise: TaskCreate({ subject: "CC10X silent-failure-hunter: Re-hunt — {completed_remfix_title}" })
  │      → Returns re_hunter_id (or null if DEBUG)
  │
  ├─→ 3. Spawn new re-verifier task (do NOT reactivate the already-completed verifier):
  │      If DEBUG (re_hunter_id is null):
  │        TaskCreate({ subject: "CC10X integration-verifier: Re-verify — {completed_remfix_title}", description: "Re-verify after REM-FIX fix. Re-reviewer findings will be in context.", activeForm: "Re-verifying after fix" })
  │        → Returns re_verifier_id
  │        TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id] })
  │      Otherwise:
  │        TaskCreate({ subject: "CC10X integration-verifier: Re-verify — {completed_remfix_title}", description: "Re-verify after REM-FIX fix. Re-reviewer and re-hunter findings will be in context.", activeForm: "Re-verifying after fix" })
  │        → Returns re_verifier_id
  │        TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id, re_hunter_id] })
  │
  ├─→ 4. Block Memory Update on new re-verifier (so memory persists after re-verification completes):
  │      TaskUpdate({ taskId: memory_task_id, addBlockedBy: [re_verifier_id] })
  │      Note: memory_task_id must be defined (from step 3a compaction-safe store or reconstruction).
  │
  └─→ 5. Resume chain execution (re-reviews → re-verifier run before Memory Update)
         Note: If re-reviews produce a new REM-FIX-N, rule 1a automatically blocks all downstream tasks — no additional blocking needed here.
```

**Why:** Code changes must be re-reviewed before shipping (orchestration integrity).

**How it works:** Task() is synchronous - router waits for agent to complete and receives its output before proceeding to next agent.

**Note: cc10x:github-research is router-executed directly (THREE-PHASE process in PLAN/DEBUG) — never passed as SKILL_HINTS.**

**Detection runs BEFORE agent invocation. Pass detected skills in SKILL_HINTS.**
**Also check CLAUDE.md Complementary Skills table and include matching skills in SKILL_HINTS.**

## Skill Loading

**1. Frontmatter `skills:` (PRELOAD):** Loaded automatically at agent start. Agent does NOT call `Skill()` for these.

**2. SKILL_HINTS (Conditional):** Router passes domain skills from CLAUDE.md Complementary Skills table (e.g., `mongodb-agent-skills:*`, `react-best-practices`). Agent calls `Skill(skill="{name}")` after memory load. If not installed, agent notes in Memory Notes and continues.

**Note:** `cc10x:github-research` is router-executed directly (THREE-PHASE) — never passed as SKILL_HINTS.

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
10. **TEST_PROCESSES_CLEANED** - Before running: announce "Cleaning up orphaned test processes..." then run: `pkill -f "vitest|jest|mocha" 2>/dev/null || true` and log result: "Killed: [process names found]" or "None found"

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
   - Announce in 1 sentence what this agent will do and why it matters now.
   - For tasks with subject "CC10X REM-FIX:": invoke cc10x:component-builder (BUILD/REVIEW) or cc10x:bug-investigator (DEBUG).
   - For tasks with subject "CC10X REM-EVIDENCE:": re-invoke the original agent (extract agent name from the subject suffix — e.g., "CC10X REM-EVIDENCE: code-reviewer missing Router Contract" → invoke cc10x:code-reviewer). When re-invoking, append to the original prompt: "NOTE: Your previous output succeeded but lacked the '### Router Contract (MACHINE-READABLE)' section. Your work is already saved to memory. Please re-output ONLY the Router Contract YAML block — do NOT redo investigation/build/review from scratch."
   - For tasks with subject starting "CC10X integration-verifier:": invoke cc10x:integration-verifier (covers both original verify tasks and Re-verify tasks from Re-Review Loop).
   - Otherwise, if multiple agent tasks are ready (e.g., code-reviewer + silent-failure-hunter):
     → Call TaskUpdate({ status: "in_progress" }) for EACH ready task before any Task() call
     → Invoke BOTH in same message (parallel execution)
   - Pass task ID in prompt:
     Task(subagent_type="cc10x:{agent}", prompt="
       Your task ID: {taskId}
       Parent Workflow ID: {parent_task_id}   (the CC10X DEBUG: parent task, not your own task ID)
       User request: {request}
       Requirements: {requirements}
       Memory: {activeContext}
       SKILL_HINTS (INVOKE via Skill() - not optional): {detected skills}
     ")

3. After agent completes:
   - Agent self-reports: TaskUpdate({ taskId, status: "completed" }) — already done by agent
   - Router validates output (see Post-Agent Validation)
   - Router calls TaskList() to verify task is completed; if still in_progress, call TaskGet({ taskId: runnable_task_id }) and check blockedBy — if blockedBy is non-empty the agent intentionally blocked itself (self-healing), do NOT force to completed; if blockedBy is empty, router calls TaskUpdate({ taskId: runnable_task_id, status: "completed" }) as fallback
   - If completed task subject starts with "CC10X REM-FIX:", execute Remediation Re-Review Loop (see below) BEFORE finding next runnable tasks.
   - Router finds next available tasks from TaskList()

3a. **Immediately preserve Memory Notes (prevents compaction loss):**
    After any READ-ONLY agent completes (code-reviewer, silent-failure-hunter, integration-verifier):
    → Locate "### Memory Notes (For Workflow-Final Persistence)" section in agent's output (this message)
    → If found, extract the full section content
    → TaskGet({ taskId: memory_task_id })  # Retrieve Memory Update task's current description
    → TaskUpdate({
        taskId: memory_task_id,
        description: current_description + "\n\n---\n### Captured from {agent_name} ({timestamp}):\n" + extracted_memory_notes
      })
    → This stores Memory Notes in the task filesystem (survives context compaction)
    → Memory Update task executes by reading its OWN description — not conversation history
    → **Persist memory_task_id subject for reconstruction:**
      At this point, ensure memory_task_id is defined:
      If `memory_task_id` is undefined (compaction recovery): `TaskList()` → find task where subject starts with "CC10X Memory Update:" AND status IN [pending, in_progress] → assign its taskId to `memory_task_id`
    → **Store taskId durably (survives compaction):**
      `Edit(file_path=".claude/cc10x/activeContext.md", old_string="## References", new_string="## References\n- [cc10x-internal] memory_task_id: {memory_task_id} wf:{parent_task_id}")`

4. Determine next:
   - Find tasks where ALL blockedBy tasks are "completed"
   - If multiple ready → Invoke ALL in parallel (same message)
   - If one ready → Invoke sequentially
   - If none ready AND uncompleted tasks exist → Wait (error state)
   - If ALL tasks completed → Workflow complete

5. Repeat until:
   - All tasks have status="completed" (INCLUDING the Memory Update task)
   - OR critical error detected (create error task, halt)

```

**Parallel execution:** When multiple tasks are ready simultaneously, invoke ALL Task() calls in the same message — both complete before you continue.

### Workflow-Final Memory Persistence (Task-Enforced)

Memory persistence is enforced via the "CC10X Memory Update" task in the task hierarchy.

**When you see this task become available:**
1. Read Memory Notes from this task's own description — step 3a captured them here after each agent completed (compaction-safe). Do NOT scan conversation history.
2. Follow the task description to persist learnings
3. Use Read-Edit-Read pattern for each memory file
4. Mark task completed

**Note:** In DEBUG workflows, silent-failure-hunter is not in the chain — its Memory Notes will not exist. Skip it when collecting notes.

### Deferred Findings Cleanup (After Workflow Completes)

**Tasks are execution artifacts, not parking lots.** Deferred findings go to patterns.md, not tasks.

**Step 1:** Collect `**Deferred:**` entries from Memory Notes (already captured in Memory Update task description).

**Step 2:** If any `CC10X TODO:` tasks exist in TaskList (legacy or from rule 1b):
   → For each: Write description to `patterns.md ## Common Gotchas` as:
     `Edit(old_string="## Common Gotchas", new_string="## Common Gotchas\n- [Deferred v{version}]: {task description}")`
   → Then: `TaskUpdate({ taskId, status: "deleted" })`
   → No user prompt. Findings are preserved in memory. Tasks are cleaned up.

**Step 3:** Continue to MEMORY_UPDATED gate.

**Note:** The Memory Update task handles `**Deferred:**` entries from agent Memory Notes automatically. This cleanup only handles any legacy `CC10X TODO:` tasks that still exist.

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
