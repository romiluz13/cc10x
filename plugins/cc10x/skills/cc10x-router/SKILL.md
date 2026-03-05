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

| Priority | Signal | Keywords | Workflow | Agent Chain |
|----------|--------|----------|----------|-------------|
| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue, problem, doesn't work | **DEBUG** | bug-investigator → code-reviewer → integration-verifier |
| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, brainstorm, brainstorming, explore, "before we build", "how should we" | **PLAN** | planner |
| 3 | REVIEW | review, audit, check, analyze, assess, "what do you think", "is this good" | **REVIEW** | code-reviewer |
| 4 | DEFAULT | Everything else | **BUILD** | component-builder → **[code-reviewer ∥ silent-failure-hunter]** → integration-verifier |

**∥ = PARALLEL.** Conflict Resolution: ERROR signals always win. "fix the build" = DEBUG (not BUILD).

**Announce routing:** Before executing any workflow, output one line: `→ {WORKFLOW} workflow (signals: {matched keywords})`

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

**Orphan check:** If any CC10X task has status="in_progress": check `blockedBy` list — if non-empty: "Task blocked by REM-FIX (self-healing in progress). Options: Resume REM-FIX / Abandon self-heal / Delete." If blockedBy empty: ⚠️ AskUserQuestion: Resume (reset to pending) / Complete (skip) / Delete.

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
#
# Plan file validation (if plan_file != "N/A"):
#   Read(file_path=plan_file)  # Verify plan exists
#   If file not found:
#     AskUserQuestion: "Plan file {plan_file} not found. It may have been moved or deleted."
#     Options: "Build without plan" | "Re-plan first (Recommended)"
#     → "Build without plan": set plan_file = "N/A", proceed
#     → "Re-plan first": switch to PLAN workflow

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
  description: "**ROUTER: Execute inline — NEVER spawn Task() for this task.**\n\nREQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\n**Instructions:**\n1. Read Memory Notes from THIS task's description — they were captured between '---' separator lines by the router immediately after each agent completed (compaction-safe). Do NOT search conversation history.\n2. Persist learnings to .claude/cc10x/activeContext.md ## Learnings\n3. Persist patterns to .claude/cc10x/patterns.md ## Common Gotchas\n4. For **Deferred:** entries in agent Memory Notes: Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n5. Persist verification to .claude/cc10x/progress.md ## Verification\n\n**Pattern:**\nRead(file_path=\".claude/cc10x/activeContext.md\")\nEdit(old_string=\"## Learnings\", new_string=\"## Learnings\\n- [from agent]: {insight}\")\nRead(file_path=\".claude/cc10x/activeContext.md\")  # Verify\n\nRepeat for patterns.md and progress.md.\n\n**Freshness (prevent bloat):**\n- activeContext.md ## Recent Changes: Find `[BUILD-START: wf:{parent_task_id}]` in ## Recent Changes (extract parent_task_id from `[workflow-scope: wf:{parent_task_id}]` at end of this description). Replace FROM that marker onward with this workflow's final summary. Preserve all entries BEFORE that marker.\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- Collect Memory Notes from READ-ONLY agents only (code-reviewer, silent-failure-hunter, integration-verifier) — WRITE agents (component-builder, bug-investigator, planner) already wrote memory directly; skip their Memory Notes to avoid duplicates. Exception: check WRITE agent output for **Deferred:** entries — these are NOT written by the agent and must be collected here.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
  activeForm: "Persisting workflow learnings"
})
# Returns memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
# Early store (M1 compaction safety): immediately after this, write [cc10x-internal] memory_task_id to activeContext.md ## References. Step 3a overwrites with same value — no harm if redundant.
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
  description: "**ROUTER: Execute inline — NEVER spawn Task() for this task.**\n\nREQUIRED: Collect Memory Notes from agent outputs and persist to memory files.\n\nFocus on:\n- Root cause for patterns.md ## Common Gotchas\n- Debug attempt history for activeContext.md\n- Verification evidence for progress.md\n- **Deferred:** entries from Memory Notes → Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- activeContext.md ## Recent Changes: Find `[DEBUG-RESET: wf:{parent_task_id}]` in ## Recent Changes (extract parent_task_id from `[workflow-scope: wf:{parent_task_id}]` at end of this description). Replace FROM that marker onward with this workflow's final summary. Preserve all entries BEFORE that marker. (Fallback: if not found, preserve all ## Recent Changes — do not trim.)\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- Collect Memory Notes from READ-ONLY agents only (code-reviewer, integration-verifier) — WRITE agents (bug-investigator) already wrote memory directly; skip their Memory Notes to avoid duplicates. Exception: check WRITE agent output for **Deferred:** entries — these are NOT written by the agent and must be collected here.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
  description: "**ROUTER: Execute inline — NEVER spawn Task() for this task.**\n\nREQUIRED: Collect Memory Notes from code-reviewer output and persist to memory files.\n\nFocus on:\n- Patterns discovered for patterns.md\n- Review verdict for progress.md\n- **Deferred:** entries from Memory Notes → Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
  description: "**ROUTER: Execute inline — NEVER spawn Task() for this task.**\n\nREQUIRED: Update memory files with plan reference and planner learnings.\n\nFocus on:\n- Add plan file to activeContext.md ## References\n- Persist planner Learnings to activeContext.md ## Learnings\n- Persist planner Patterns to patterns.md ## Common Gotchas\n- **Deferred:** entries from planner Memory Notes → Write each to patterns.md ## Common Gotchas as \"[Deferred]: {entry}\"\n- Update progress.md with plan status\n\n**Use Read-Edit-Read pattern for each file.**\n\n**Freshness (prevent bloat):**\n- activeContext.md ## Recent Changes: Find `[PLAN-START: wf:{parent_task_id}]` in ## Recent Changes (extract parent_task_id from `[workflow-scope: wf:{parent_task_id}]` at end of this description). Replace FROM that marker onward with this workflow's final summary. Preserve all entries BEFORE that marker. (Fallback: if not found, preserve all ## Recent Changes — do not trim.)\n- progress.md ## Tasks: REPLACE existing entries with only this workflow's task items.\n- patterns.md: Before adding to ## Common Gotchas, scan for an existing entry about the same file or error. If found, update it in-place instead of adding a duplicate.\n- activeContext.md ## Learnings: before appending, check for same topic/file; update in-place if found; if count > 20, promote oldest entries to patterns.md ## Common Gotchas.\n- progress.md ## Completed: keep only the 10 most recent entries.\n[workflow-scope: wf:{parent_task_id}] — used by compaction-recovery scoped search",
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
   - Skip ONLY if: plan in `## References` ≠ "N/A"
   - AskUserQuestion: "Plan first (Recommended) / Build directly"
3. **Clarify requirements** (DO NOT SKIP):
   - **Pre-answers (always run first):** Read activeContext.md `## Decisions` — look for entries starting with `"Planner clarification ["` OR `"Build clarification ["`. If found, treat those Q→A pairs as pre-answered (do NOT re-ask them).
   - Use AskUserQuestion for any unanswered requirements.
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
3. No cross-layer dependencies (e.g., API + DB + UI)
4. No open `CC10X REM-FIX` tasks in current workflow
5. Requirements are explicit and unambiguous

| Depth | Chain | When |
|-------|-------|------|
| **FULL** | component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier | Default for all BUILD |
| **QUICK** | component-builder → integration-verifier | ALL 5 conditions above met |

**QUICK still requires:** Text-based verdict extraction + verifier + memory update.
**Blocking signal during QUICK** (verifier FAIL, test failure, lint error):
→ ⚠️ AskUserQuestion: "Quick verification failed ({reason}). Escalating to full review adds code-reviewer + silent-failure-hunter before final verification. Continue?"
  Options: "Run full review chain (Recommended)" | "Abort — I'll investigate manually"
→ If "Run full review chain":
    1. Create missing tasks:
       TaskCreate({ subject: "CC10X code-reviewer: Review implementation (escalated from QUICK)", description: "QUICK escalation — verifier failed, full review chain activated.", activeForm: "Reviewing code" }) → esc_reviewer_id
       TaskCreate({ subject: "CC10X silent-failure-hunter: Hunt edge cases (escalated from QUICK)", description: "QUICK escalation — verifier failed, full review chain activated.", activeForm: "Hunting failures" }) → esc_hunter_id
    2. Mark both in_progress (before any Task() call — per Chain Execution Loop step 2):
       TaskUpdate({ taskId: esc_reviewer_id, status: "in_progress" })
       TaskUpdate({ taskId: esc_hunter_id, status: "in_progress" })
    3. Block verifier on both new tasks:
       TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [esc_reviewer_id, esc_hunter_id] })
    4. Invoke code-reviewer + silent-failure-hunter in parallel (same as standard BUILD), then re-invoke integration-verifier
→ If "Abort": Record in activeContext.md ## Decisions: "QUICK escalation declined by user", stop workflow

### DEBUG
1. Load memory → Check patterns.md Common Gotchas
2. **CLARIFY (REQUIRED)**: AskUserQuestion if ANY ambiguity (error message, expected vs actual, when it started, affected component/file)
3. **Check for research trigger (Pre-investigation):**
   - User explicitly requested research ("research", "github", "octocode"), OR
   - External service error (API timeout, auth failure, third-party)

   **If ANY trigger met:**
   → AskUserQuestion: "Before debugging, should we research similar issues on the web and GitHub? This makes external API calls and saves findings to docs/research/."
     Options: "Research web + GitHub (Recommended)" | "Skip research" | "Abort workflow"
   → If "Skip research": proceed without research
   → If "Abort": Record in activeContext.md ## Decisions: "Research declined", stop workflow
   → If "Research web + GitHub":
     - `TaskCreate({ subject: "CC10X web-researcher: Research {error topic}", description: "Topic: {error topic}\nReason: Debug — external error\nFile: docs/research/{date}-{topic}-web.md", activeForm: "Researching web" })` → web_task_id
     - `TaskCreate({ subject: "CC10X github-researcher: Research {error topic}", description: "Topic: {error topic}\nReason: Debug — external error\nFile: docs/research/{date}-{topic}-github.md", activeForm: "Researching GitHub" })` → github_task_id
     - Mark both in_progress. Spawn BOTH in same message (parallel):
       `Task(subagent_type="cc10x:web-researcher", ...)` ∥ `Task(subagent_type="cc10x:github-researcher", ...)`
     - **Timeout fallback:** If either agent returns no FILE_PATH or fails, use only the successful agent's file (or skip research and proceed with empty context if both fail).
     - Collect: `web_file = web_contract.FILE_PATH`, `github_file = github_contract.FILE_PATH`
     - **Persist research (compaction-safe):** Edit(activeContext.md ## References, "- Research (web): {web_file}\n- Research (github): {github_file}") → Read(activeContext.md) to verify
     - Pass both to bug-investigator: `## Research Files\nWeb: {web_file}\nGitHub: {github_file}`
     - Add SKILL_HINTS: `cc10x:research` (synthesis guidance)

4. **Create task hierarchy** (see Task-Based Orchestration above)
4a. **Write DEBUG-RESET marker** (immediately after task hierarchy created — before bug-investigator runs):
    ```
    Edit(file_path=".claude/cc10x/activeContext.md",
         old_string="## Recent Changes",
         new_string="## Recent Changes\n[DEBUG-RESET: wf:{workflow_task_id}]")
    Read(file_path=".claude/cc10x/activeContext.md")  # VERIFY marker written
    # If marker NOT found in Read output: STOP — retry Edit before invoking bug-investigator
    ```
5. **Start chain execution** (pass research file path if step 3 was executed)
6. Update memory → Add to Common Gotchas when all tasks completed

### REVIEW
1. Load memory
2. **CLARIFY (REQUIRED)**: Use AskUserQuestion to confirm scope:
   - Review entire codebase OR specific files?
   - Focus area: security/performance/quality/all?
   - Blocking issues only OR all findings?
   **Persist scope (compaction-safe):** Edit(activeContext.md ## Decisions, "- Review clarification [{date}]: {scope_question} → {scope_answer}")
2b. **Scope extraction:** From answers, extract `review_scope = "files: {list}" | "focus: {topic}" | "all"`. Pass in reviewer prompt under `## Review Scope` to prevent whole-repo audit.
3. **Create task hierarchy** (see Task-Based Orchestration above)
4. **Start chain execution** (see Chain Execution Loop below) — pass scope from ## Decisions to code-reviewer prompt
5. Update memory when task completed
6. **REVIEW-to-BUILD Transition Gate** (if STATUS=CHANGES_REQUESTED): AskUserQuestion: "Reviewer found changes needed. Start BUILD to fix (Recommended) | Review findings first | Done for now" → "Start BUILD": execute BUILD workflow with reviewer findings as context. Otherwise: record "REVIEW complete, BUILD deferred [{date}]" in activeContext.md ## Decisions, stop.

### PLAN
> **NEVER call `EnterPlanMode`.** Invoke the planner agent — it writes plan files directly.

1. Load memory
2. **Design file extraction (ALWAYS — regardless of request clarity):**
   → `Read(.claude/cc10x/activeContext.md)` → find `- Design:` in `## References` → store as `design_file` (or null if not found / "N/A")
   → **Design relevance:** If `design_file` is not null/N/A: `Glob(pattern="{design_file}")` → if 0 matches: AskUserQuestion: "Design file not found at {design_file}. Re-run brainstorming | Provide path manually | Proceed without design" → If found: pass to planner; planner assesses relevance based on filename (feature-name mismatch → planner notes it and proceeds without design constraint).
3. **Brainstorming (ALWAYS — explore idea before planning):**
   → `Skill(skill="cc10x:brainstorming")` — runs in main context, `AskUserQuestion` available here
   → Collect clarified requirements, pass to planner in step 6
   → **AFTER brainstorming returns: continue to step 4. Design file ≠ plan file. Do NOT jump to BUILD — planner (step 6) has not run yet.**
4. **If research detected (external tech OR explicit request):**
   - AskUserQuestion: "Research web + GitHub before planning? Improves plan quality for external tech."
     Options: "Yes, research (Recommended)" | "No, skip" | "Abort workflow"
   - If "No, skip": proceed to step 5
   - If "Abort workflow": Record in activeContext.md ## Decisions: "Research declined, workflow aborted [{date}]", stop workflow
   - If "Yes":
     - `TaskCreate({ subject: "CC10X web-researcher: Research {topic}", description: "Topic: {topic}\nReason: {reason}\nFile: docs/research/{date}-{topic}-web.md", activeForm: "Researching web" })` → web_task_id
     - `TaskCreate({ subject: "CC10X github-researcher: Research {topic}", description: "Topic: {topic}\nReason: {reason}\nFile: docs/research/{date}-{topic}-github.md", activeForm: "Researching GitHub" })` → github_task_id
     - Mark both in_progress. Spawn BOTH in same message (parallel):
       `Task(subagent_type="cc10x:web-researcher", prompt="Topic: {topic}\nReason: {reason}\nFile: docs/research/{date}-{topic}-web.md\nTask ID: {web_task_id}")`
       `Task(subagent_type="cc10x:github-researcher", prompt="Topic: {topic}\nReason: {reason}\nFile: docs/research/{date}-{topic}-github.md\nTask ID: {github_task_id}")`
     - Collect: `web_file = web_contract.FILE_PATH`, `github_file = github_contract.FILE_PATH`
     - **Timeout fallback:** If either agent returns no FILE_PATH or fails, use only the successful agent's file (or skip research and proceed with empty context if both fail). Do NOT pass null/empty paths to planner.
     - **Persist research (compaction-safe):** Edit(activeContext.md ## References, "- Research (web): {web_file}\n- Research (github): {github_file}") → Read(activeContext.md) to verify
5. **Create task hierarchy** (see Task-Based Orchestration above)
5b. **Write PLAN-START marker** (immediately after task hierarchy created — before any agent runs):
    ```
    Edit(file_path=".claude/cc10x/activeContext.md",
         old_string="## Recent Changes",
         new_string="## Recent Changes\n[PLAN-START: wf:{workflow_task_id}]")
    Read(file_path=".claude/cc10x/activeContext.md")  # VERIFY marker written
    ```
6. **Start chain execution** (pass clarified requirements + research files + design file in prompt)
   → Re-read `.claude/cc10x/activeContext.md` → find `- Design:` in `## References` → update design_file with fresh value (post-brainstorming). If null/N/A: proceed without design context.
   If research ran (step 4): Add to planner prompt: `## Research Files\nWeb: {web_file}\nGitHub: {github_file}`
   If research ran (step 4): Add SKILL_HINTS: `cc10x:research` (synthesis guidance for reading the files)
   If design_file found (step 2 or refreshed above): Add to planner prompt: `## Design File\n{design_file}`
6a. **After planner task completes — Your Input Needed gate (MANDATORY if items exist):**
    → Scan planner output text for "**Your Input Needed:**" section header
    → Also check planner Router Contract for `USER_INPUT_NEEDED:` field (compaction-safe fallback)
    → If EITHER source has content (non-empty bullet points or non-empty USER_INPUT_NEEDED list):
      → AskUserQuestion is MANDATORY: "Before BUILD starts, planner flagged these assumptions that need your input:\n{extracted bullet points}\nProvide answers (or confirm the defaults)."
      → Collect answers → Persist to activeContext.md ## Decisions with Edit: "- Planner clarification [{date}]: {Q} → {A}"
      → Include answers summary in BUILD context: When invoking component-builder, add "## Planner Clarifications\n{Q+A pairs}" to prompt
    → If both sources empty or absent: Proceed directly to step 7
7. Update memory → Reference saved plan when task completed
7b. **Plan file existence check (after CONTRACT RULE passes):**
    If STATUS == PLAN_CREATED:
      Glob(pattern="{contract.PLAN_FILE}")
      If 0 matches:
        → Override STATUS to NEEDS_CLARIFICATION
        → AskUserQuestion: "Planner reported PLAN_CREATED but the plan file was not found on disk at {contract.PLAN_FILE}. The Write() call may have failed silently. How to proceed?"
          Options: "Re-run planner (Recommended)" | "Write plan content manually" | "Abort workflow"
8. **Announce completion:** Output "Plan saved to `{plan_file}`. Start BUILD when you're ready." and stop. Memory already has the plan reference — Plan-First Gate will auto-skip on next BUILD.

**Research prerequisite:** Each agent handles its own file persistence. Router collects both `FILE_PATH` values from agent output and passes them to the planner prompt.

## Agent Invocation

**Pass task ID, plan file, and context to each agent:**
```
Task(subagent_type="cc10x:component-builder", prompt="
## Task Context
- **Task ID:** {taskId}
- **Parent Workflow ID:** {parent_task_id}
- **Plan File:** {planFile or 'None'}

## User Request
{request}

## Requirements
{from AskUserQuestion or 'See plan file'}

## Memory Summary
{brief summary from activeContext.md}

## Project Patterns
{key patterns from patterns.md — include ## Common Gotchas and ## User Standards only; if combined length > 2000 chars, include ## User Standards only}

## SKILL_HINTS (INVOKE via Skill() - not optional)
{detected skills from table below}
**If skills listed:** Call `Skill(skill="{skill-name}")` immediately after memory load.

---
IMPORTANT:
- **NEVER call `EnterPlanMode`.** This is an execution agent that writes files directly. Plan mode would block Write/Edit tools and prevent saving outputs.
- **WRITE agents (builder, investigator, planner):** call `TaskUpdate(status: completed)` AFTER outputting full analysis. Do NOT call TaskUpdate as your only or last tool call — substantive output must precede it.
- **READ-ONLY agents (reviewer, hunter, verifier):** do NOT call `TaskUpdate(status: completed)`. Just stop after your report. The router handles task completion via fallback.
- If your tools include `Edit` **and you are not running in a parallel phase**, update `.claude/cc10x/{activeContext,patterns,progress}.md` at the end per `cc10x:session-memory` and `Read(...)` back to verify.
- If you are running in a parallel phase (e.g., BUILD’s review/hunt phase), prefer **no memory edits** (skip Edit() calls on `.claude/cc10x/*.md`); your analysis scope, output quality (≥200 chars), and `### Memory Notes` section are REQUIRED regardless — "no memory edits" means no file writes, NOT reduced output.
- If your tools do NOT include `Edit`, you MUST include a `### Memory Notes (For Workflow-Final Persistence)` section with:
  - **Learnings:** [insights for activeContext.md]
  - **Patterns:** [gotchas for patterns.md]
  - **Verification:** [results for progress.md]

Execute the task and include ‘Task {TASK_ID}: COMPLETED’ in your output when done.
")
```

**TASK ID is REQUIRED in prompt.** Agents call TaskUpdate(completed) for their own task after final output. Router verifies via TaskList().
**SKILL_HINTS:** If router passes skills in SKILL_HINTS, agent MUST call `Skill(skill="{skill-name}")` after loading memory. This includes complementary skills (react-best-practices, mongodb-agent-skills, etc.) and `cc10x:research` (when research files were passed in prompt).

**Post-Agent Validation (After agent completes):**

When agent returns, verify output quality before proceeding.

---

### Verdict Extraction (envelope-first, text fallback)

**Pre-AskUserQuestion output rule (ALL ⚠️ gates):**
Before invoking any ⚠️ AskUserQuestion, output one sentence summarizing the finding. Examples: "Review found critical issues that need fixing." / "Verdict conflict: reviewer approved but hunter found critical failures." / "Investigation stuck — external research needed." This ensures UI renders context before the question appears.

**Empty Answer Guard:**
If AskUserQuestion returns empty:
→ For ⚠️ REVERT gates only: Output "⚠️ Revert decision requires your input. Please answer the question above." Re-ask once. If still empty: STOP workflow.
→ For ALL other gates: Auto-default to the recommended option and log: "Empty answer — auto-proceeding with recommended default."
→ This allows batch/automated workflows to proceed without deadlock.

**JUST_GO Session Mode (check once, at memory load):**
After loading memory: Read `## Session Settings` from activeContext.md.
If line `AUTO_PROCEED: true` exists: Set session flag `JUST_GO=true`.
While `JUST_GO=true`: All AskUserQuestion gates auto-default to recommended option without prompting (except ⚠️ REVERT gates). Log: "JUST_GO: auto-proceeding with [{option}] for {gate}."

**Step 0: Try contract envelope (line 1 — primary fast path)**

Check if the first line of agent output matches `CONTRACT {`:
- If YES: parse JSON fields — `s`→STATUS, `b`→BLOCKING, `cr`→CRITICAL_ISSUES
  - Map `s` values: `"APPROVE"`→APPROVE, `"CHANGES_REQUESTED"`→CHANGES_REQUESTED, `"CLEAN"`→CLEAN, `"ISSUES_FOUND"`→ISSUES_FOUND, `"PASS"`→PASS, `"FAIL"`→FAIL
  - If all fields parsed and `s` is recognized: set STATUS/BLOCKING/CRITICAL_ISSUES from envelope, **skip Step 1**. Continue at Step 2 (still scan `### Critical Issues` for REMEDIATION_REASON and CONTRACT RULE validation).
  - If envelope malformed or `s` unrecognized: fall through to Step 1.
- If NO envelope on line 1: fall through to Step 1.

**Step 1: Extract STATUS from agent output heading (first 5 lines of output)**

After agent completes, scan first 5 lines for these heading patterns:

| Agent | Heading → STATUS | BLOCKING default |
|-------|-----------------|-----------------|
| code-reviewer | `## Review: Approve` → APPROVE | false |
| code-reviewer | `## Review: Changes Requested` → CHANGES_REQUESTED | false (upgraded if Critical Issues found) |
| silent-failure-hunter | `## Error Handling Audit: CLEAN` or `## Error Handling Audit: Clean` → CLEAN | false |
| silent-failure-hunter | `## Error Handling Audit: ISSUES_FOUND` or `## Error Handling Audit: Issues Found` → ISSUES_FOUND | false (upgraded if Critical Issues found) |
| integration-verifier | `## Verification: PASS` or `## Verification: Pass` → PASS | false |
| integration-verifier | `## Verification: FAIL` or `## Verification: Fail` → FAIL | true |

**Step 2: Extract BLOCKING/CRITICAL from `### Critical Issues` section**

Scan agent output for `### Critical Issues` section:
- If section found AND has at least one non-empty bullet (`- ` prefix): CRITICAL_ISSUES = count of bullet items
- If CRITICAL_ISSUES > 0: BLOCKING=true, REQUIRES_REMEDIATION=true
- Extract first bullet text → REMEDIATION_REASON (first 100 chars)
- If STATUS=CHANGES_REQUESTED and CRITICAL_ISSUES=0: REQUIRES_REMEDIATION=true, BLOCKING=false (HIGH issues present)
- If STATUS=ISSUES_FOUND and CRITICAL_ISSUES=0: REQUIRES_REMEDIATION=true, BLOCKING=false (HIGH issues present)

**Step 3: Fallback if heading not found**

If no heading pattern matched:
- If output >= 500 chars:
  1. First: scan for anchored line `^STATUS:\s*(PASS|FAIL|FIXED|INVESTIGATING|BLOCKED|PLAN_CREATED|NEEDS_CLARIFICATION)` — use this if found (YAML write-agent contract; anchored parse prevents false keyword match in prose)
  2. If not found: scan full output for keywords: "APPROVE" | "CHANGES_REQUESTED" | "CLEAN" | "ISSUES_FOUND" | "PASS" | "FAIL" — use first match as STATUS
- If output < 200 chars: **INLINE VERIFICATION REQUIRED** — do NOT blindly default to APPROVE/CLEAN/PASS:
  → Log: "Agent {agent} returned minimal output ({N} chars). Running inline verification..."
  → For **integration-verifier**: Run tests inline:
    `Bash(command="npx vitest run --reporter=verbose 2>&1 | tail -30")` (fallback: `npm test 2>&1 | tail -20`). If exit=0 AND output contains passing tests → STATUS=PASS (log: "Inline test run: PASS"). If exit≠0 → STATUS=FAIL, BLOCKING=true, REMEDIATION_REASON="Inline test run failed — see output."
  → For **code-reviewer** or **silent-failure-hunter**: Run inline scan on changed files:
    `Bash(command="git diff HEAD --name-only 2>/dev/null | head -20")` → get changed files.
    `Grep(pattern="catch\\s*[({][^)]*[)}]\\s*\\{\\s*\\}", files)` → empty catch scan.
    `Grep(pattern="console\\.log|TODO|FIXME|debugger", files)` → noise scan (LOW only, not blocking).
    If empty catch found → STATUS=ISSUES_FOUND/CHANGES_REQUESTED, CRITICAL_ISSUES=1, BLOCKING=true.
    If only noise patterns → STATUS=APPROVE/CLEAN, log: "Inline scan: no blocking issues."
    If no changes found (`git diff` empty = NO_GIT) → STATUS=APPROVE/CLEAN (cannot scan, safe default).
  → Set BLOCKING per normal STATUS rules. Output inline findings under "### Inline Verification".
- If output 200–499 chars and no heading: Apply same two-step parse as >= 500 chars (anchored `^STATUS:` first, then keyword scan).

**Step 4: Detect SELF_REMEDIATED (task-state-based)**

After Steps 1-3: Call `TaskList()` → check if agent's task still has status="in_progress".
If still in_progress: Call `TaskGet({ taskId: agent_task_id })` → if blockedBy is non-empty:
  → STATUS=SELF_REMEDIATED → apply rule 0b
  (Task state is the definitive signal — agent created REM-FIX and blocked itself)

**Step 5: Output Validation Evidence**
```
### Agent Validation: {agent_name}
- Status extracted from: heading | fallback scan | minimal output default
- STATUS: {extracted_STATUS}
- BLOCKING: {computed_BLOCKING}
- CRITICAL_ISSUES: {computed_CRITICAL_ISSUES}
- REQUIRES_REMEDIATION: {computed_REQUIRES_REMEDIATION}
- Proceeding: [Yes/No + reason]
```

**Step 6: Apply validation rules using extracted values**
```
VALIDATION RULES:

---
**PRE-PROCESSING (ALWAYS RUNS FIRST — does NOT short-circuit. Apply to every agent output before the routing matrix below):**

**Rule 0: CONTRACT RULE Enforcement:**
Before applying any conditional rules, validate each agent's extracted STATUS:

| Agent | CONTRACT RULE violation → Override |
|-------|-------------------------------------|
| component-builder | STATUS=PASS but TDD_RED_EXIT≠1 OR TDD_GREEN_EXIT≠0 → STATUS=FAIL, BLOCKING=true, REMEDIATION_REASON="CONTRACT RULE violated: TDD evidence missing" |
| bug-investigator | STATUS=FIXED but (TDD_RED_EXIT≠1 OR TDD_GREEN_EXIT≠0 OR VARIANTS_COVERED<1) AND contract.NEEDS_EXTERNAL_RESEARCH != true → STATUS=FAIL, BLOCKING=true, REQUIRES_REMEDIATION=true, REMEDIATION_REASON="CONTRACT RULE violated: TDD evidence missing — add regression test (RED→GREEN) + variant coverage" |
| code-reviewer | STATUS=APPROVE but CRITICAL_ISSUES>0 (from text extraction) → STATUS=CHANGES_REQUESTED, BLOCKING=true, REQUIRES_REMEDIATION=true |
| silent-failure-hunter | STATUS=CLEAN but CRITICAL_ISSUES>0 (from text extraction) → STATUS=ISSUES_FOUND, BLOCKING=true, REQUIRES_REMEDIATION=true |
| integration-verifier | STATUS=PASS but CRITICAL_ISSUES>0 (from text extraction — mapped from blockers section) → STATUS=FAIL, BLOCKING=true |
| planner | STATUS=PLAN_CREATED but PLAN_FILE is null/empty OR CONFIDENCE<50 OR GATE_PASSED!=true → STATUS=NEEDS_CLARIFICATION, BLOCKING=true, REQUIRES_REMEDIATION=true, REMEDIATION_REASON="CONTRACT RULE violated: {missing field}" |

**If override applied:** Log: "⚠️ CONTRACT RULE override: {agent} self-reported {original} but rule violated (CRITICAL_ISSUES={N} found in heading/output). Overriding STATUS to {new_status}."
Proceed with conditional routing below using the OVERRIDDEN values.

**Circuit Breaker (BEFORE creating any REM-FIX):**
Before creating a new REM-FIX task, count ALL REM-FIX tasks in this workflow: `TaskList()` → filter by (subject contains "CC10X REM-FIX:") AND (description contains "wf:{parent_task_id}"). Count ALL statuses — cumulative count across the workflow lifecycle matters, not just currently active tasks.
If count ≥ 3 → ⚠️ AskUserQuestion: "This workflow has already created {N} fix attempts. This may indicate a deeper systemic issue. How to proceed?"
- **Research best practices (Recommended)** → Spawn parallel researchers (Topic: {issue pattern}, Reason: Circuit Breaker — 3+ REM-FIX tasks):
  TaskCreate({ subject: "CC10X web-researcher: Research {issue pattern}", description: "Topic: {issue pattern}\nReason: Circuit Breaker — 3+ REM-FIX tasks\nFile: docs/research/{date}-{topic}-web.md", activeForm: "Researching web" }) → cb_web_task_id
  TaskCreate({ subject: "CC10X github-researcher: Research {issue pattern}", description: "Topic: {issue pattern}\nReason: Circuit Breaker — 3+ REM-FIX tasks\nFile: docs/research/{date}-{topic}-github.md", activeForm: "Researching GitHub" }) → cb_github_task_id
  Mark both in_progress. `Task(cc10x:web-researcher, prompt="Topic: {issue pattern}\nReason: Circuit Breaker\nFile: docs/research/{date}-{topic}-web.md\nTask ID: {cb_web_task_id}")` ∥ `Task(cc10x:github-researcher, prompt="Topic: {issue pattern}\nReason: Circuit Breaker\nFile: docs/research/{date}-{topic}-github.md\nTask ID: {cb_github_task_id}")` → collect both FILE_PATHs → pass both file paths to next REM-FIX task description + SKILL_HINTS: cc10x:research
- **Fix locally** → Create another REM-FIX task
- **Skip** → Proceed despite errors (not recommended)
- **Abort** → Stop workflow, manual fix

---
**Conditional Routing Matrix (evaluate top-to-bottom — FIRST MATCH WINS; applies to rules 0b through 2f):**
Note: Rules 3 and 4 always run after the triggered rule completes (they are collectors, not gates).

| Priority | Condition | Action | Next State |
|----------|-----------|--------|------------|
| **0b** | STATUS == SELF_REMEDIATED | Log "Agent {agent} has self-remediated via TaskCreate." Do NOT create duplicate REM-FIX. Do NOT force-complete task (re-review loop handles it). | STOP |
| **0c** | NEEDS_EXTERNAL_RESEARCH == true (bug-investigator only) | **[Research Loop Cap first — see Detailed Logic: Rule 0c]** Spawn parallel web+github researchers. Re-invoke bug-investigator with research files + SKILL_HINTS: cc10x:research. Do NOT create REM-FIX. | STOP |
| **1a** | BLOCKING == true AND STATUS ∉ [NEEDS_CLARIFICATION, INVESTIGATING, BLOCKED, SELF_REMEDIATED, REVERT_RECOMMENDED, LIMITATION_ACCEPTED] AND NEEDS_EXTERNAL_RESEARCH ≠ true | **If REVIEW workflow** (parent task subject starts with "CC10X REVIEW:"): AskUserQuestion "Reviewer found critical issues. Start BUILD to fix (Recommended) \| Done for now". If "Start BUILD": execute BUILD workflow with reviewer findings as context. If "Done for now": record in activeContext.md ## Decisions, STOP. **Otherwise (BUILD/DEBUG):** **[Circuit Breaker first — see above]** **[Parallel blocking merge if BUILD parallel phase — see Detailed Logic: Rule 1a]** TaskCreate REM-FIX. Block all incomplete downstream CC10X tasks via TaskUpdate addBlockedBy. | STOP |
| **1b** | REQUIRES_REMEDIATION == true AND BLOCKING == false | Log "Rule 1b: non-blocking issues found." If REVIEW workflow: AskUserQuestion "Start BUILD / Done for now." Otherwise: **[Circuit Breaker first — see above]** TaskCreate REM-FIX. Block downstream tasks. | STOP |
| **2** | code-reviewer STATUS=APPROVE AND silent-failure-hunter found issues (parallel phase only) | **[Conflict check — Cases A/B in Detailed Logic: Rule 2]** AskUserQuestion: investigate or skip/proceed. | STOP |
| **2b** | STATUS == NEEDS_CLARIFICATION (planner) | **[NEEDS_CLARIFICATION Loop Cap first — see Detailed Logic: Rule 2b]** AskUserQuestion with extracted "Your Input Needed" items. Collect answers → persist to ## Decisions. TaskCreate Re-plan. Block downstream. Re-invoke planner. | STOP |
| **2c** | STATUS == INVESTIGATING (bug-investigator) | **[Investigation Loop Cap first — see Detailed Logic: Rule 2c]** TaskCreate Continue Investigation. Block downstream. Re-invoke bug-investigator with ROOT_CAUSE hint. | STOP |
| **2f** | STATUS == BLOCKED (bug-investigator terminal stuck) | AskUserQuestion: "Research externally (Recommended) / Create manual fix task / Abort." Handle choice per Detailed Logic: Rule 2f. | STOP |
| **2d** | integration-verifier STATUS == FAIL | **[DEBUG serial loop check if DEBUG workflow — see Detailed Logic: Rule 2d]** **[REVERT gate first — see Detailed Logic: Rule 2d]** Otherwise: TaskCreate REM-FIX. Block downstream tasks. | STOP |
| **3** | (Always — runs after triggered rule completes) | Collect Memory Notes from agent output (### Memory Notes section) for workflow-final persistence. | Continue |
| **4** | None of above triggered | Proceed to next agent. | Continue |

---
**Detailed Logic (required reading for rows marked [see Detailed Logic: Rule X]):**

### Rule 0b — SELF_REMEDIATED
→ The agent has autonomously created a REM-FIX task and blocked itself (or downstream tasks).
→ Acknowledge the self-healing action: log "Agent {agent} has self-remediated via TaskCreate."
→ Do NOT create a duplicate REM-FIX task.
→ Do NOT mark the original task as completed — the REM-FIX task it created has blocked it.
  The Remediation Re-Review Loop (step 1) will create a fresh re_reviewer task to re-invoke this agent after the fix. Forcing completed here would cancel the re-review.
→ STOP evaluating rules 1a/1b/2 for this agent's contract.

### Rule 0c — NEEDS_EXTERNAL_RESEARCH (bug-investigator only)
Runs BEFORE rule 1a — do NOT evaluate rules 1a/1b/2 when this fires.
**Research Loop Cap (BEFORE spawning agents):**
  Count external research iterations: Read(.claude/cc10x/activeContext.md) → find the `[DEBUG-RESET: wf:{parent_task_id}]` marker in ## Recent Changes → count entries in ## References that match `docs/research/` AND were added after that marker (scoped to current workflow). If no marker found: count = 0 (fresh workflow, never triggered).
  If count >= 2: ⚠️ AskUserQuestion: "External research has been provided to bug-investigator {count} time(s) and it still reports NEEDS_EXTERNAL_RESEARCH. How to proceed?"
    Options: "Try research once more" | "Create manual fix task (skip re-invoke)" | "Abort workflow"
    → Do NOT proceed. Handle chosen option, then STOP.
  If count < 2: Proceed below.
→ TaskCreate web-researcher + github-researcher tasks (with topic = contract.RESEARCH_REASON)
→ Mark both in_progress. Spawn BOTH in same message (parallel):
  `Task(subagent_type="cc10x:web-researcher", prompt="Topic: {contract.RESEARCH_REASON}\nReason: Bug investigation stuck — NEEDS_EXTERNAL_RESEARCH\nFile: docs/research/{date}-{topic}-web.md\nTask ID: {web_task_id}")`
  `Task(subagent_type="cc10x:github-researcher", prompt="Topic: {contract.RESEARCH_REASON}\nReason: Bug investigation stuck — NEEDS_EXTERNAL_RESEARCH\nFile: docs/research/{date}-{topic}-github.md\nTask ID: {github_task_id}")`
→ Collect: web_file = web_contract.FILE_PATH, github_file = github_contract.FILE_PATH
→ **Persist research (compaction-safe):** Edit(activeContext.md ## References, "- Research (web): {web_file}\n- Research (github): {github_file}") → Read(activeContext.md) to verify
→ Re-invoke cc10x:bug-investigator with same prompt + "## Research Files\nWeb: {web_file}\nGitHub: {github_file}"
→ Add SKILL_HINTS: cc10x:research (synthesis guidance)
→ Do NOT create REM-FIX task — research IS the response
→ STOP after re-invoke — do not evaluate rules 1a/1b/2 for this contract

### Rule 1a — BLOCKING: Parallel Blocking Merge (BUILD only, pre-check before TaskCreate)
→ If currently processing parallel review phase (code-reviewer ∥ silent-failure-hunter outputs in same response):
  → Check sibling agent's extracted verdict in this same response — does sibling ALSO have BLOCKING=true?
  → If YES (both agents blocking):
      merged_subject = "CC10X REM-FIX: code-reviewer + silent-failure-hunter — multiple blocking issues"
      merged_description = "**code-reviewer issues:**\n" + reviewer_REMEDIATION_REASON + "\n\n**silent-failure-hunter issues:**\n" + hunter_REMEDIATION_REASON
  → If NO (only this agent blocking): use this agent's data alone (existing behavior)
  → If NOT parallel phase: use this agent's data alone (existing behavior)
→ TaskCreate({
    subject: merged_subject ?? "CC10X REM-FIX: {agent_name} — {first 60 chars of (REMEDIATION_REASON ?? 'see agent output')}",
    description: merged_description ?? (REMEDIATION_REASON ?? "Issues found — see agent Critical Issues section."),
    activeForm: "Fixing {agent_name} issues"
  })
→ Task-enforced gate:
  - Find downstream workflow tasks via TaskList() (subjects prefixed with `CC10X `)
  - For every downstream task not completed:
    TaskUpdate({ taskId: downstream_task_id, addBlockedBy: [remediation_task_id] })
→ STOP. Do not invoke next agent until remediation completes.

### Rule 1b — NON-BLOCKING REMEDIATION
→ Auto-default to "Fix now" (no AskUserQuestion needed — JUST_GO compatible).
→ Log: "Rule 1b: non-blocking issues found — auto-proceeding with fix."
→ Gather context:
  - If parallel phase AND sibling agent also has REQUIRES_REMEDIATION=true: merge both REMEDIATION_REASONs into one combined description
  - Otherwise: use this agent's REMEDIATION_REASON alone
→ **REVIEW workflow check:** If parent workflow task subject starts with "CC10X REVIEW:":
    → Do NOT create REM-FIX. Instead: AskUserQuestion: "Start a BUILD workflow to apply fixes? Options: 'Start BUILD' | 'Done for now'"
    → If "Start BUILD": Execute BUILD workflow with reviewer findings as context. STOP.
    → If "Done for now": Record in activeContext.md ## Decisions: "REVIEW complete, fixes deferred [{date}]". STOP.
→ Otherwise (BUILD/DEBUG): Circuit Breaker check, then create REM-FIX task: TaskCreate({subject: "CC10X REM-FIX: {agent} — {REMEDIATION_REASON[:60]}", description: REMEDIATION_REASON ?? "HIGH issues found — see agent output"}) → block downstream tasks → STOP

### Rule 2 — Conflict Check (parallel phase: reviewer APPROVE + hunter found issues)
Only applies when: code-reviewer STATUS=APPROVE AND silent-failure-hunter found issues (parallel phase, Cases A and B only). All other reviewer+hunter combinations are handled by rules 1a/1b before reaching rule 2.
**Case A:** code-reviewer STATUS=APPROVE AND silent-failure-hunter CRITICAL_ISSUES > 0:
  ⚠️ AskUserQuestion: "Reviewer approved, but Hunter found {N} critical silent failures. Investigate or skip?"
  - "Investigate" → Create REM-FIX: TaskCreate({subject: "CC10X REM-FIX: silent-failure-hunter — {REMEDIATION_REASON[:60]}", description: REMEDIATION_REASON}) → block downstream tasks → STOP
  - "Skip" → Record decision in memory, proceed to verifier
**Case B:** code-reviewer STATUS=APPROVE AND silent-failure-hunter STATUS=ISSUES_FOUND AND CRITICAL_ISSUES=0 (high issues only):
  ⚠️ AskUserQuestion: "Reviewer approved, but Hunter found high-severity error handling gaps. Fix before continuing?"
  - "Fix" → Create REM-FIX: TaskCreate({subject: "CC10X REM-FIX: silent-failure-hunter — {REMEDIATION_REASON[:60]}", description: REMEDIATION_REASON ?? "HIGH silent failure issues found — see hunter output"}) → block downstream tasks → STOP
  - "Proceed anyway" → Record in memory: "Hunter HIGH issues skipped by user", proceed

### Rule 2b — NEEDS_CLARIFICATION (planner)
**NEEDS_CLARIFICATION Loop Cap (BEFORE re-invoking):**
  Count: TaskList() → filter (subject contains "CC10X planner: Create plan" OR subject contains "CC10X planner: Re-plan after clarification") AND status = "completed"
  If count >= 3: ⚠️ AskUserQuestion: "Planner has been re-invoked {count} times and still returns NEEDS_CLARIFICATION. How to proceed?"
    Options: "Try once more" | "Proceed with best available plan" | "Abort workflow"
    → Handle chosen option, then STOP.
  If count < 3: Continue below.
→ Extract "**Your Input Needed:**" bullet points from planner output
→ ⚠️ AskUserQuestion: "Planner needs clarification before the plan can be completed:\n{extracted items}\nPlease answer to unblock planning."
→ Collect user answers → Persist to activeContext.md ## Decisions: "Plan clarification: {Q} → {A}"
→ TaskCreate({ subject: "CC10X planner: Re-plan after clarification (attempt {count+1})", description: "Re-planning after NEEDS_CLARIFICATION. User answers: {answers}", activeForm: "Re-planning" }) → planner_retry_id
→ Block downstream tasks on planner_retry_id
→ Task(subagent_type="cc10x:planner", prompt: "Parent Workflow ID: {parent_task_id}\nTask ID: {planner_retry_id}\n{original prompt}\n\n## User Clarifications\n{answers}")
→ Do NOT proceed to BUILD until planner returns STATUS=PLAN_CREATED

### Rule 2c — INVESTIGATING (bug-investigator)
Treat as BLOCKING=true (investigation incomplete — no fix applied yet)
**Investigation Loop Cap (BEFORE re-invoke):**
  Count: TaskList() → filter subject contains "CC10X bug-investigator: Continue investigation" AND status = "completed"
  If count >= 2: ⚠️ AskUserQuestion: "Bug investigator has completed {count} investigation cycles without resolving. How to proceed?"
    Options: "Try once more" | "Force BLOCKED status" | "Abort workflow"
    → "Try once more": Continue below (one more re-invoke only)
    → "Force BLOCKED": Set contract.STATUS = "BLOCKED", evaluate rule 2f instead. STOP.
    → "Abort": Record in activeContext.md ## Decisions: "Investigation aborted after {count} cycles", stop workflow
  If count < 2: Continue below.
→ Announce to user: "Bug investigator is still investigating (no fix applied yet). Continuing investigation..."
→ TaskCreate({ subject: "CC10X bug-investigator: Continue investigation", description: "Previous attempt: STATUS=INVESTIGATING. ROOT_CAUSE hint: {contract.ROOT_CAUSE}. Continue from this hypothesis." })
→ Block downstream tasks on this new investigation task
→ Re-invoke bug-investigator with prompt: "Parent Workflow ID: {parent_task_id}\nTask ID: {new_task_id}\nPrevious STATUS=INVESTIGATING — ROOT_CAUSE hint: {contract.ROOT_CAUSE}\n{original_prompt}"

### Rule 2f — BLOCKED (bug-investigator terminal stuck state)
→ Investigation is permanently stuck — cannot proceed without external help or user decision
→ ⚠️ AskUserQuestion: "Bug investigation is completely stuck (BLOCKED). ROOT_CAUSE hint: {contract.ROOT_CAUSE}. How to proceed?"
  Options: "Research externally (Recommended)" | "Create manual fix task" | "Abort workflow"
→ "Research externally": Spawn parallel researchers (Topic: {contract.ROOT_CAUSE}, Reason: Bug BLOCKED — terminal stuck):
  `Task(cc10x:web-researcher) ∥ Task(cc10x:github-researcher)` → collect both FILE_PATHs → re-invoke bug-investigator with `## Research Files\nWeb: {web_file}\nGitHub: {github_file}` + SKILL_HINTS: cc10x:research
→ "Create manual fix task": Proceed as rule 1a (create REM-FIX task)
→ "Abort": Record in activeContext.md ## Decisions: "Investigation aborted (BLOCKED): {ROOT_CAUSE}", stop workflow

### Rule 2d — integration-verifier FAIL
**DEBUG Serial Loop Check (pre-condition, DEBUG only):** If parent workflow subject contains "CC10X DEBUG:": count completed "CC10X integration-verifier: Re-verify" tasks. If count >= 2: ⚠️ AskUserQuestion "Re-verify ran {count}x — deeper issue? Continue / Escalate / Abort" → handle, STOP.
→ Create REM-FIX task (self-heal by default). Note: verifier asked user inline via AskUserQuestion before emitting FAIL — if user chose "Accept limitation" the verifier emits PASS instead; if user chose "Revert", verifier emits FAIL and router creates REM-FIX (user can abandon it and revert manually after recording the decision in memory).
→ ⚠️ REVERT gate: If verifier output contains text "REVERT" or "revert branch":
    ⚠️ AskUserQuestion: "Verifier output suggests reverting the branch. How to proceed?"
    Options: "Revert branch (Recommended)" | "Create fix task instead"
    - "Revert": Suggest git revert steps, stop workflow (record in memory)
    - "Create fix task": Create REM-FIX task normally
→ Otherwise: Create REM-FIX task: TaskCreate({subject: "CC10X REM-FIX: integration-verifier — {REMEDIATION_REASON[:60]}", description: REMEDIATION_REASON ?? "Verification failed — see verifier output"}) → block downstream tasks → STOP
```

---

## Remediation Re-Review Loop (Pseudocode)

```
WHEN any CC10X REM-FIX task COMPLETES:
  │
  ├─→ PRE-CHECK: **Original Reviewer Guard (runs before everything else):**
  │      TaskList() → find task where (subject starts with "CC10X code-reviewer:") AND (status IN ["pending", "in_progress"])
  │      If found (original code-reviewer is still active — pending or self-healed in_progress):
  │        → SKIP the entire Re-Review Loop (steps 0-5). Do nothing.
  │        → Log: "Re-Review Loop skipped — original code-reviewer is still active ({status}). Execution loop will re-invoke it directly when blockers clear."
  │        → The execution loop (Step 1) picks up in_progress tasks with cleared blockers and re-invokes them.
  │      If NOT found (original code-reviewer IS completed): Continue to Step 0 below.
  │
  ├─→ 0. **Cycle Cap Check (RUNS FIRST):**
  │      Count completed "CC10X REM-FIX:" tasks in this workflow: TaskList() → filter subject contains "CC10X REM-FIX:" AND status = "completed"
  │      Note: count ≥ 2 is a coarse heuristic — cross-issue false triggers possible. Per-issue accuracy: filter subject also contains the same agent/issue token.
  │      If count ≥ 2:
  │        → ⚠️ AskUserQuestion: "This workflow has completed {count} fix cycles. How to proceed?"
  │          - "Create another fix task" → Continue with steps 1-5 below
  │          - "Research patterns (Recommended)" → Spawn parallel researchers (Topic: {current issue pattern}, Reason: Multiple REM-FIX cycles failing):
            TaskCreate({ subject: "CC10X web-researcher: Research {current issue pattern}", description: "Topic: {current issue pattern}\nReason: Multiple REM-FIX cycles failing\nFile: docs/research/{date}-{topic}-web.md", activeForm: "Researching web" }) → rrr_web_task_id
            TaskCreate({ subject: "CC10X github-researcher: Research {current issue pattern}", description: "Topic: {current issue pattern}\nReason: Multiple REM-FIX cycles failing\nFile: docs/research/{date}-{topic}-github.md", activeForm: "Researching GitHub" }) → rrr_github_task_id
            Mark both in_progress. `Task(cc10x:web-researcher, prompt="Topic: {current issue pattern}\nReason: Multiple REM-FIX cycles\nFile: docs/research/{date}-{topic}-web.md\nTask ID: {rrr_web_task_id}")` ∥ `Task(cc10x:github-researcher, prompt="Topic: {current issue pattern}\nReason: Multiple REM-FIX cycles\nFile: docs/research/{date}-{topic}-github.md\nTask ID: {rrr_github_task_id}")` → collect both FILE_PATHs → pass both file paths to next REM-FIX task description + SKILL_HINTS: cc10x:research
  │          - "Accept known issues" → Record in activeContext.md ## Decisions, proceed directly to verifier/memory-update
  │          - "Abort workflow" → Stop; user resolves manually
  │      If count < 2: Continue to step 1 below
  │
  ├─→ 1. Extract the completed REM-FIX task subject (the task that just completed):
  │      → completed_remfix_title = first 50 chars of completed task subject after "CC10X REM-FIX: "
  │      TaskCreate({ subject: "CC10X code-reviewer: Re-review — {completed_remfix_title}" })
  │      → Returns re_reviewer_id
  │
  ├─→ 2. **Skip in DEBUG or REVIEW workflows:** If the parent workflow task subject contains "CC10X DEBUG:" or "CC10X REVIEW:" → SKIP step 2 entirely (no hunter in these chains).
  │      Otherwise: TaskCreate({ subject: "CC10X silent-failure-hunter: Re-hunt — {completed_remfix_title}", description: "Re-hunt for silent failures after REM-FIX. Full output required even if no issues found (emit heading: Error Handling Audit: CLEAN)." })
  │      → Returns re_hunter_id (or null if DEBUG/REVIEW)
  │
  ├─→ 3. **Skip in REVIEW workflows:** If the parent workflow task subject contains "CC10X REVIEW:" → SKIP step 3 entirely (no verifier in REVIEW chain). Proceed directly to step 4 with re_verifier_id = null.
  │      Otherwise, find or create re-verifier task:
  │      **Pending verifier check (run FIRST):** TaskList() → find task where (subject starts with "CC10X integration-verifier:") AND (status = "pending")
  │      If found (original verifier is pending — unblocked by REM-FIX completion):
  │        → re_verifier_id = original_verifier_id (reuse it — do NOT create duplicate)
  │        → If DEBUG or re_hunter_id is null:
  │            TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id] })
  │          Otherwise:
  │            TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id, re_hunter_id] })
  │        → Log: "Re-verifier reused — original integration-verifier {re_verifier_id} is pending. Adding re-reviewer as blocker."
  │      If NOT found (no pending verifier — original already completed or never existed):
  │        If DEBUG or re_hunter_id is null:
  │          TaskCreate({ subject: "CC10X integration-verifier: Re-verify — {completed_remfix_title}", description: "Re-verify after REM-FIX fix. Re-reviewer findings will be in context.", activeForm: "Re-verifying after fix" })
  │          → Returns re_verifier_id
  │          TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id] })
  │        Otherwise:
  │          TaskCreate({ subject: "CC10X integration-verifier: Re-verify — {completed_remfix_title}", description: "Re-verify after REM-FIX fix. Re-reviewer and re-hunter findings will be in context.", activeForm: "Re-verifying after fix" })
  │          → Returns re_verifier_id
  │          TaskUpdate({ taskId: re_verifier_id, addBlockedBy: [re_reviewer_id, re_hunter_id] })
  │
  ├─→ 4. Block Memory Update:
  │      If re_verifier_id is not null:
  │        TaskUpdate({ taskId: memory_task_id, addBlockedBy: [re_verifier_id] })
  │      If re_verifier_id is null (REVIEW workflow):
  │        TaskUpdate({ taskId: memory_task_id, addBlockedBy: [re_reviewer_id] })
  │      Note: memory_task_id must be defined (from step 3a compaction-safe store or reconstruction).
  │
  └─→ 5. Resume chain execution (re-reviews → re-verifier run before Memory Update)
         Note: If re-reviews produce a new REM-FIX-N, rule 1a automatically blocks all downstream tasks — no additional blocking needed here.
         Note: For REVIEW workflows, chain completes after re-reviewer → Memory Update (no hunter or verifier).
```

## Gates (Must Pass)

1. **MEMORY_LOADED** - Before routing
2. **TASKS_CHECKED** - Check TaskList() for active workflow
3. **INTENT_CLARIFIED** - User intent is unambiguous (all workflows)
4. **RESEARCH_COMPLETE** - Before planner/bug-investigator (if research detected) — both parallel agents return FILE_PATH in their output; router collects both
5. **REQUIREMENTS_CLARIFIED** - Before invoking agent (BUILD only)
6. **TASKS_CREATED** - Workflow task hierarchy created
7. **ALL_TASKS_COMPLETED** - All workflow tasks (including Memory Update) status="completed"
8. **MEMORY_UPDATED** - Before marking done
9. **TEST_PROCESSES_CLEANED** - Before running: announce "Cleaning up orphaned test processes..." then run: `pids=$(pgrep -f 'vitest|jest|mocha' 2>/dev/null); if [ -n "$pids" ]; then pkill -f 'vitest|jest|mocha' 2>/dev/null; echo "Killed: $(ps -p $pids -o comm= 2>/dev/null | tr '\n' ',' | sed 's/,$//')"; else echo 'None found'; fi` and log result: "Killed: [names]" or "None found"

## Chain Execution Loop (Task-Based)

### Execution Loop

```
1. Find runnable tasks:
   TaskList() → Find tasks where:
   - status IN ["pending", "in_progress"]
   - blockedBy is empty OR all blockedBy tasks are "completed"
   Note: in_progress tasks with cleared blockers are self-healed agents waiting to be re-invoked (e.g., code-reviewer that blocked itself pending a REM-FIX). Re-invoking them directly avoids creating zombie tasks.

2. Start agent(s):
   - TaskUpdate({ taskId: runnable_task_id, status: "in_progress" })
   - Announce in 1 sentence what this agent will do and why it matters now.
   - **Memory Update guard:** If task subject starts with "CC10X Memory Update:":
     → Execute INLINE (Read + Edit calls in main context). NEVER spawn Task() — sub-agents read stale memory.
     → Follow task description instructions directly (Read Memory Notes from description, persist to .claude/cc10x/*.md).
     → Mark task completed inline: TaskUpdate({ taskId, status: "completed" }).
     → Mark parent workflow task completed: extract parent_task_id from `[workflow-scope: wf:{N}]` at end of task description. If found: TaskUpdate({ taskId: parent_task_id, status: "completed" }).
     → Continue to next runnable task. Do NOT proceed to agent routing logic below.
   - For tasks with subject "CC10X REM-FIX:": Route by originating agent, not workflow:
     - If REM-FIX originated from bug-investigator contract → invoke cc10x:bug-investigator
     - If REM-FIX originated from code-reviewer, silent-failure-hunter, or integration-verifier contract → invoke cc10x:component-builder (all workflows)
   - For tasks with subject starting "CC10X integration-verifier:": invoke cc10x:integration-verifier (covers both original verify tasks and Re-verify tasks from Re-Review Loop).
   - Otherwise, if multiple agent tasks are ready (e.g., code-reviewer + silent-failure-hunter):
     → Call TaskUpdate({ status: "in_progress" }) for EACH ready task before any Task() call
     → Invoke BOTH in same message (parallel execution)
   - Pass task ID in prompt — use the canonical Agent Invocation template above.
     All fields required: Task ID, Parent Workflow ID, Plan File, User Request, Memory Summary, Project Patterns, SKILL_HINTS.

3. After agent completes:
   - WRITE agents self-report: TaskUpdate({ taskId, status: "completed" }) — already done by agent. READ-ONLY agents (reviewer, hunter, verifier) do NOT call this — router fallback handles it.
   - Router validates output (see Post-Agent Validation)
   - Router calls TaskList() to verify task is completed; if still in_progress, call TaskGet({ taskId: runnable_task_id }) and check blockedBy — if blockedBy is non-empty the agent intentionally blocked itself (self-healing), do NOT force to completed; if blockedBy is empty, router calls TaskUpdate({ taskId: runnable_task_id, status: "completed" }) as fallback
   - **TEST_PROCESSES_CLEANED (after component-builder only):** If completed task subject contains "CC10X component-builder:":
     Announce: "Cleaning up orphaned test processes..."
     `Bash(command="pids=$(pgrep -f 'vitest|jest|mocha' 2>/dev/null); if [ -n \"$pids\" ]; then pkill -f 'vitest|jest|mocha' 2>/dev/null; echo \"Killed: $(ps -p $pids -o comm= 2>/dev/null | tr '\n' ',' | sed 's/,$//')\"; else echo 'None found'; fi")`
     Log result to output.
   - **Restore workflow marker (WRITE agents overwrite ## Recent Changes — v8.0.1):**
     If completed task subject contains "CC10X component-builder:":
       → Re-write BUILD-START marker: `Edit(file_path=".claude/cc10x/activeContext.md", old_string="## Recent Changes", new_string="## Recent Changes\n[BUILD-START: wf:{workflow_task_id}]")` → `Read(".claude/cc10x/activeContext.md")` to verify. If `[BUILD-START: wf:{workflow_task_id}]` not present in output: retry Edit once.
     If completed task subject contains "CC10X bug-investigator:":
       → Re-write DEBUG-RESET marker: `Edit(file_path=".claude/cc10x/activeContext.md", old_string="## Recent Changes", new_string="## Recent Changes\n[DEBUG-RESET: wf:{workflow_task_id}]")` → `Read(".claude/cc10x/activeContext.md")` to verify. If `[DEBUG-RESET: wf:{workflow_task_id}]` not present in output: retry Edit once.
     If completed task subject contains "CC10X planner:":
       → Re-write PLAN-START marker: `Edit(file_path=".claude/cc10x/activeContext.md", old_string="## Recent Changes", new_string="## Recent Changes\n[PLAN-START: wf:{workflow_task_id}]")` → `Read(".claude/cc10x/activeContext.md")` to verify. If `[PLAN-START: wf:{workflow_task_id}]` not present in output: retry Edit once.
   - If completed task subject starts with "CC10X REM-FIX:", execute Remediation Re-Review Loop (see below) BEFORE finding next runnable tasks.
   - Router finds next available tasks from TaskList()

3a. **Immediately preserve Memory Notes (prevents compaction loss):**
    After ANY agent completes:
    → Locate "### Memory Notes (For Workflow-Final Persistence)" section in agent's output (this message)
    → If found, extract the full section content
    → TaskGet({ taskId: memory_task_id })  # Retrieve Memory Update task's current description
    → TaskUpdate({
        taskId: memory_task_id,
        description: current_description + "\n\n---\n### Captured from {agent_name} ({timestamp}):\n" + extracted_memory_notes
      })
    → **Persist memory_task_id subject for reconstruction:**
      At this point, ensure memory_task_id is defined:
      If `memory_task_id` is undefined (compaction recovery): `TaskList()` → find task where subject starts with "CC10X Memory Update:" AND status IN [pending, in_progress] → assign its taskId to `memory_task_id`
    → **Store taskId durably (idempotent — skip if already present):**
      Read(activeContext.md) → if "[cc10x-internal] memory_task_id:" NOT found in ## References:
        `Edit(file_path=".claude/cc10x/activeContext.md", old_string="## References", new_string="## References\n- [cc10x-internal] memory_task_id: {memory_task_id} wf:{parent_task_id}")`
      # (If already present, skip — value is the same)

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
# Memory Update task: execute inline (READ + EDIT calls in main context — see task description for full instructions including Deferred cleanup).

## Results Collection (Parallel Agents)

# After both parallel agents complete: TaskList() → verify both "completed"
# Collect REVIEWER_FINDINGS from code-reviewer output: extract heading verdict + Critical Issues section
# Collect HUNTER_FINDINGS from silent-failure-hunter output: extract heading verdict + Critical Issues section
# Pass both under "## Previous Agent Findings" in integration-verifier prompt (see integration-verifier.md ## Context from Previous Agents for template)

## Release Checklist

**When bumping version — update ALL THREE files:**

| File | Location | Fields to update |
|------|----------|-----------------|
| Source plugin.json | `plugins/cc10x/.claude-plugin/plugin.json` | `version` |
| Cache plugin.json | `~/.claude/plugins/cache/cc10x/cc10x/{folder}/plugin.json` | `version` (note: cache folder name stays at old version; only the field changes) |
| Marketplace | `~/.claude/plugins/marketplaces/cc10x/.claude-plugin/marketplace.json` | `metadata.version`, `plugins[0].version`, `metadata.description` (inline version string) |

**Also update:** `README.md` (version in prose), `CHANGELOG.md` (new section header).
