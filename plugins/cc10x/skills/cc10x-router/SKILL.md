---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X - AUTO-LOAD AND EXECUTE for ANY development task.

  Triggers: build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy, memory, session, context, save, load, test, tdd, frontend, ui, backend, api, pattern, refactor, optimize, improve, enhance, update, modify, change, help, assist, work, start, begin, continue, research, cc10x, c10x.

  CRITICAL: Execute workflow. Never just describe capabilities.
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

**∥ = PARALLEL** - code-reviewer and silent-failure-hunter run simultaneously (both read-only)

## Memory (PERMISSION-FREE)

**LOAD FIRST (Before routing):**
```
Bash(command="mkdir -p .claude/cc10x")
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")
```

**UPDATE LAST (After workflow):** Use Edit tool on activeContext.md (permission-free).

## Check Active Workflow Tasks

**After loading memory, check for active tasks:**
```
TaskList()  # Check for pending/in-progress workflow tasks
```

**If active CC10x workflow task exists (subject starts with BUILD/DEBUG/REVIEW/PLAN):**
- Resume from task state (read task description for context)
- Skip workflow selection - continue execution from where it stopped
- Check blockedBy to determine which agent to run next

**If no active tasks:**
- Proceed with workflow selection below

## Task-Based Orchestration

**At workflow start, create task hierarchy using TaskCreate/TaskUpdate:**

### BUILD Workflow Tasks
```
# 0. Check if following a plan (from activeContext.md)
# If activeContext contains "Plan Reference:" or "Execute:" with plan path:
#   → Extract plan_file path (e.g., docs/plans/2024-01-27-auth-plan.md)
#   → Include in task metadata for context preservation

# 1. Parent workflow task
TaskCreate({
  subject: "BUILD: {feature_summary}",
  description: "User request: {request}\n\nWorkflow: BUILD\nChain: component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier\n\n**Plan:** {plan_file or 'N/A'}",
  activeForm: "Building {feature}",
  metadata: {
    workflow: "BUILD",
    feature: "{feature}",
    planFile: "{plan_file or null}"  # Links task to plan for context recovery
  }
})
# Returns workflow_task_id

# 2. Agent tasks with dependencies
TaskCreate({
  subject: "component-builder: Implement {feature}",
  description: "Build the feature per user request\n\n**Plan:** {plan_file or 'N/A'}",
  activeForm: "Building components",
  metadata: { agent: "component-builder", planFile: "{plan_file or null}" }
})
# Returns builder_task_id

TaskCreate({ subject: "code-reviewer: Review implementation", description: "Review code quality, patterns, security", activeForm: "Reviewing code" })
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({ subject: "silent-failure-hunter: Hunt edge cases", description: "Find silent failures and edge cases", activeForm: "Hunting failures" })
TaskUpdate({ taskId: hunter_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({ subject: "integration-verifier: Verify integration", description: "Run tests, verify E2E functionality", activeForm: "Verifying integration" })
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id, hunter_task_id] })
```

### DEBUG Workflow Tasks
```
TaskCreate({ subject: "DEBUG: {error_summary}", description: "User request: {request}\n\nWorkflow: DEBUG\nChain: bug-investigator → code-reviewer → integration-verifier", activeForm: "Debugging {error}" })

TaskCreate({ subject: "bug-investigator: Investigate {error}", description: "Find root cause and fix", activeForm: "Investigating bug" })
TaskCreate({ subject: "code-reviewer: Review fix", description: "Review the fix quality", activeForm: "Reviewing fix" })
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [investigator_task_id] })
TaskCreate({ subject: "integration-verifier: Verify fix", description: "Verify fix works E2E", activeForm: "Verifying fix" })
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id] })
```

### REVIEW Workflow Tasks
```
TaskCreate({ subject: "REVIEW: {target_summary}", description: "User request: {request}\n\nWorkflow: REVIEW\nChain: code-reviewer (single agent)", activeForm: "Reviewing {target}" })

TaskCreate({ subject: "code-reviewer: Review {target}", description: "Comprehensive code review", activeForm: "Reviewing code" })
```

### PLAN Workflow Tasks
```
TaskCreate({ subject: "PLAN: {feature_summary}", description: "User request: {request}\n\nWorkflow: PLAN\nChain: planner (single agent)", activeForm: "Planning {feature}" })

TaskCreate({ subject: "planner: Create plan for {feature}", description: "Create comprehensive implementation plan", activeForm: "Creating plan" })
```

## Workflow Execution

### BUILD
1. Load memory → Check if already done in progress.md
2. **Clarify requirements** (DO NOT SKIP) → Use AskUserQuestion
3. **Create task hierarchy** (see Task-Based Orchestration above)
4. **Start chain execution** (see Chain Execution Loop below)
5. Update memory when all tasks completed

### DEBUG
1. Load memory → Check patterns.md Common Gotchas
2. Clarify: What error? Expected vs actual? When started?
3. **If github-research detected (external service error OR explicit request):**
   - Execute research FIRST using octocode tools directly
   - Search for error patterns, PRs with similar issues
   - **PERSIST research** → Save to `docs/research/YYYY-MM-DD-<error-topic>-research.md`
   - **Update memory** → Add to activeContext.md Research References table
4. **Create task hierarchy** (see Task-Based Orchestration above)
5. **Start chain execution** (pass research file path if step 3 was executed)
6. Update memory → Add to Common Gotchas when all tasks completed

### REVIEW
1. Load memory
2. **Create task hierarchy** (see Task-Based Orchestration above)
3. **Start chain execution** (see Chain Execution Loop below)
4. Update memory when task completed

### PLAN
1. Load memory
2. **If github-research detected (external tech OR explicit request):**
   - Execute research FIRST using octocode tools directly (NOT as hint)
   - Use: `mcp__octocode__packageSearch`, `mcp__octocode__githubSearchCode`, etc.
   - **PERSIST research** → Save to `docs/research/YYYY-MM-DD-<topic>-research.md`
   - **Update memory** → Add to activeContext.md Research References table
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
      Edit(file_path=".claude/cc10x/activeContext.md", ...)  # Add to Research References
  → PHASE 3: Task(cc10x:planner, prompt="...Research findings: {results}...\nResearch saved to: docs/research/YYYY-MM-DD-<topic>-research.md")
```
Research is a PREREQUISITE, not a hint. Planner cannot skip it.
**Research without persistence is LOST after context compaction.**

## Agent Invocation

**Pass task ID and context to each agent (see Chain Execution Loop for full pattern):**
```
Task(subagent_type="cc10x:component-builder", prompt="
Your task ID: {taskId}
User request: {request}
Requirements: {from AskUserQuestion}
Memory: {from activeContext.md}
Patterns: {from patterns.md}
SKILL_HINTS: {detected skills from table below - agent MUST load these}
")
```

**TASK ID is REQUIRED.** Agent MUST call `TaskUpdate(taskId, status="completed")` when done.
**SKILL_HINTS are MANDATORY.** Agent MUST call `Skill(skill="...")` for each hint immediately after loading memory.

**Skill triggers for agents (DETECT AND PASS AS SKILL_HINTS):**

| Detected Pattern | Skill | Agents |
|------------------|-------|--------|
| Frontend: components/, ui/, pages/, .tsx, .jsx, CSS, styling, "button", "form", "modal" | cc10x:frontend-patterns | planner, component-builder, code-reviewer, integration-verifier |
| API/Backend: api/, routes/, services/, "endpoint", "REST", "GraphQL" | cc10x:architecture-patterns | planner, bug-investigator, code-reviewer |
| Vague: "not sure", "maybe", "options", "ideas", unclear requirements | cc10x:brainstorming | planner |
| External: new tech (post-2024), unfamiliar library, complex integration (auth, payments) | cc10x:github-research | planner, bug-investigator |
| Debug exhausted: 3+ local attempts failed, external service error | cc10x:github-research | bug-investigator |
| User explicitly requests: "research", "github", "octocode", "find on github", "how do others", "best practices" | cc10x:github-research | planner, bug-investigator |

**Detection runs BEFORE agent invocation. Pass detected skills in SKILL_HINTS.**

## Gates (Must Pass)

1. **MEMORY_LOADED** - Before routing
2. **TASKS_CHECKED** - Check TaskList() for active workflow
3. **RESEARCH_EXECUTED** - Before planner (if github-research detected)
4. **RESEARCH_PERSISTED** - Save to docs/research/ + update activeContext.md (if research was executed)
5. **REQUIREMENTS_CLARIFIED** - Before invoking agent (BUILD only)
6. **TASKS_CREATED** - Workflow task hierarchy created
7. **ALL_TASKS_COMPLETED** - All agent tasks status="completed"
8. **MEMORY_UPDATED** - Before marking done

## Chain Execution Loop (Task-Based)

**NEVER stop after one agent.** The workflow is NOT complete until ALL tasks are completed.

### Execution Loop

```
1. Find runnable tasks:
   TaskList() → Find tasks where:
   - status = "pending"
   - blockedBy is empty OR all blockedBy tasks are "completed"

2. Start agent(s):
   - TaskUpdate(taskId, status="in_progress")
   - If multiple tasks ready (e.g., code-reviewer + silent-failure-hunter):
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
   - Agent will have called TaskUpdate(taskId, status="completed")
   - Router calls TaskList() to check state

4. Determine next:
   - Find tasks where ALL blockedBy tasks are "completed"
   - If multiple ready → Invoke ALL in parallel (same message)
   - If one ready → Invoke sequentially
   - If none ready AND uncompleted tasks exist → Wait (error state)
   - If ALL tasks completed → Workflow complete

5. Repeat until:
   - All tasks have status="completed"
   - OR critical error detected (create error task, halt)
```

### Parallel Execution

When multiple tasks become unblocked simultaneously (e.g., code-reviewer AND silent-failure-hunter after component-builder completes):

```
# Both ready after builder completes
TaskUpdate(taskId=reviewer_id, status="in_progress")
TaskUpdate(taskId=hunter_id, status="in_progress")

# Invoke BOTH in same message = parallel execution
Task(subagent_type="cc10x:code-reviewer", prompt="Your task ID: {reviewer_id}...")
Task(subagent_type="cc10x:silent-failure-hunter", prompt="Your task ID: {hunter_id}...")
```

**CRITICAL:** Both Task calls in same message = both complete before you continue.

### Chain Completion Criteria

The workflow is complete ONLY when:
- `TaskList()` shows ALL agent tasks with status="completed"
- OR a critical error prevents continuation

**DO NOT update memory until ALL tasks are completed.**
