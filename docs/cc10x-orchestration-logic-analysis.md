# cc10x Orchestration Logic Analysis

> **Last synced with agents/skills:** 2026-02-05 | **Status:** IN SYNC

> **Relationship to Bible:** This document explains HOW the system works.
> For the canonical specification (WHAT the system IS), see `cc10x-orchestration-bible.md`.

> **Critical Understanding:** This is NOT code orchestration. This is **English orchestration** - prompt engineering and instructions that guide AI behavior. Every "chain," "gate," and "handoff" is implemented through carefully crafted English text.

---

## System Architecture Overview

### Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                        cc10x-router (ORCHESTRATOR)                   │
│   THE ONLY ENTRY POINT - Detects intent, routes to workflows         │
│   Decision Tree: ERROR → DEBUG | PLAN → PLAN | REVIEW → REVIEW | → BUILD │
└─────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
    ┌─────────┐                ┌─────────┐                ┌─────────┐
    │ AGENTS  │                │ SKILLS  │                │ MEMORY  │
    │ (6)     │                │ (12)    │                │ (3 files)│
    └─────────┘                └─────────┘                └─────────┘
```

### The 6 Agents (Executors)
| Agent | Role | Workflow Usage | Mode | Memory | Model |
|-------|------|----------------|------|--------|-------|
| `component-builder` | Build features using TDD | BUILD | WRITE | Direct Edit | inherit |
| `code-reviewer` | Multi-dimensional code review | BUILD, DEBUG, REVIEW | READ-ONLY | Memory Notes | inherit |
| `silent-failure-hunter` | Find error handling gaps | BUILD | READ-ONLY | Memory Notes | inherit |
| `integration-verifier` | E2E validation | BUILD, DEBUG | READ-ONLY | Memory Notes | inherit |
| `bug-investigator` | Root cause debugging | DEBUG | WRITE | Direct Edit | inherit |
| `planner` | Create implementation plans | PLAN | WRITE | Direct Edit | inherit |

**Mode Clarification:**
- **WRITE agents**: Have Edit tool, update `.claude/cc10x/*.md` memory directly, load session-memory skill
- **READ-ONLY agents**: No Edit tool, output `### Memory Notes` section, persisted via task-enforced Memory Update task
- **Memory Notes pattern**: READ-ONLY agents include learnings/patterns/verification in structured output section

### The 12 Skills (Knowledge/Patterns)
| Skill | Purpose | Used By (via frontmatter) |
|-------|---------|---------------------------|
| `cc10x-router` | THE ENTRY POINT - orchestration engine | Main assistant |
| `session-memory` | Memory persistence rules | WRITE agents (component-builder, bug-investigator, planner) |
| `planning-patterns` | How to write plans | planner |
| `debugging-patterns` | Systematic debugging process | bug-investigator, integration-verifier |
| `code-review-patterns` | Review methodology | code-reviewer, silent-failure-hunter |
| `code-generation` | Code writing guidelines | component-builder |
| `verification-before-completion` | Evidence requirements | ALL agents |
| `architecture-patterns` | System design | ALL agents |
| `brainstorming` | Ideas → designs | planner |
| `frontend-patterns` | UI/UX patterns | ALL agents |
| `github-research` | External research (conditional) | planner, bug-investigator |
| `test-driven-development` | TDD cycle | component-builder, bug-investigator |

### The 3 Memory Files
| File | Purpose | When Updated |
|------|---------|--------------|
| `.claude/cc10x/activeContext.md` | Current focus, decisions, learnings | Every workflow |
| `.claude/cc10x/patterns.md` | Project conventions, gotchas | When patterns learned |
| `.claude/cc10x/progress.md` | What's done, what's remaining | Task completion |

---

## Orchestration Flow (Detailed)

### Phase 0: Router Activation

**Trigger Keywords (from SKILL.md description):**
```
build, implement, create, make, write, add, develop, code, feature,
component, app, application, review, audit, check, analyze, debug,
fix, error, bug, broken, troubleshoot, plan, design, architect,
roadmap, strategy, memory, session, context, save, load, test, tdd,
frontend, ui, backend, api, pattern, refactor, optimize, improve,
enhance, update, modify, change, help, assist, work, start, begin,
continue, research, cc10x, c10x
```

### Phase 1: Memory Loading (GATE: MEMORY_LOADED)

```
Bash(command="mkdir -p .claude/cc10x")
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")
```

**English Trick:** Separating mkdir and Read prevents permission prompts (compound commands ask for permission, separate tools don't).

### Phase 2: Task State Check (GATE: TASKS_CHECKED)

```
TaskList()  # Check for pending/in-progress workflow tasks
```

**Decision Point:**
- If active CC10x workflow task exists → Resume from task state
- If no active tasks → Proceed with workflow selection

### Phase 3: Intent Classification

**Decision Tree (PRIORITY ORDER - ERROR always wins):**

| Priority | Signal | Keywords | Workflow |
|----------|--------|----------|----------|
| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue, problem, doesn't work | **DEBUG** |
| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, "before we build", "how should we" | **PLAN** |
| 3 | REVIEW | review, audit, check, analyze, assess, "what do you think", "is this good" | **REVIEW** |
| 4 | DEFAULT | Everything else | **BUILD** |

**English Trick:** "Conflict Resolution: ERROR signals always win" prevents ambiguity. "fix the build" = DEBUG (not BUILD).

### Phase 4: Skill Loading

**Most skills load automatically via agent frontmatter** - no router detection needed.

**Only github-research uses SKILL_HINTS mechanism:**

| Trigger | Skill | Agents |
|---------|-------|--------|
| External: new tech (post-2024), unfamiliar library, complex integration | `cc10x:github-research` | planner, bug-investigator |
| Debug exhausted: 3+ local attempts failed | `cc10x:github-research` | bug-investigator |
| User explicit: "research", "github", "octocode" | `cc10x:github-research` | planner, bug-investigator |

**Flow:** Router detects trigger → passes `github-research` in SKILL_HINTS → Agent calls `Skill(skill="cc10x:github-research")`

**All other skills** (frontend-patterns, architecture-patterns, brainstorming, etc.) are hardcoded in agent frontmatter and load automatically when the agent starts.

### Phase 5: Workflow-Specific Execution

#### BUILD Workflow

```
Chain: component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier
                              ↑ PARALLEL ↑
```

**Steps:**
1. Load memory → Check progress.md (already done?)
2. **Clarify requirements** → AskUserQuestion (GATE: REQUIREMENTS_CLARIFIED)
3. **Create task hierarchy** (GATE: TASKS_CREATED)
4. **Chain execution loop**
5. Update memory when ALL tasks completed (GATE: MEMORY_UPDATED)

#### DEBUG Workflow

```
Chain: bug-investigator → code-reviewer → integration-verifier
```

**Steps:**
1. Load memory → Check patterns.md Common Gotchas
2. **Clarify** (REQUIRED): What error? Expected vs actual? When started?
3. **Check research triggers:**
   - User explicitly requested research? OR
   - External service error? OR
   - 3+ local debugging attempts failed?
   - **If ANY → Execute research FIRST, persist to docs/research/, update memory**
4. Create task hierarchy
5. Chain execution
6. Update memory → Add to Common Gotchas

**Debug Attempt Tracking Format:**
```
[DEBUG-N]: {what was tried} → {result}
```
Example entries in activeContext.md Recent Changes:
- `[DEBUG-1]: Added null check → still failing (same error)`
- `[DEBUG-2]: Wrapped in try-catch → error is in upstream fetch()`
- `[DEBUG-3]: Fixed fetch() URL encoding → tests pass`

Router counts `[DEBUG-N]:` lines to trigger external research after 3+ failures.

#### REVIEW Workflow

```
Chain: code-reviewer (single agent)
```

**Steps:**
1. Load memory
2. **Clarify** (REQUIRED): Entire codebase OR specific files? Focus area?
3. Create task hierarchy
4. Execute
5. Update memory

#### PLAN Workflow

```
Chain: planner (single agent)
```

**Steps:**
1. Load memory
2. **If github-research detected:**
   - Execute research FIRST using octocode tools (NOT as hint)
   - **PERSIST research** → docs/research/YYYY-MM-DD-<topic>-research.md
   - **Update memory** → activeContext.md Research References table
   - Summarize findings before invoking planner
3. Create task hierarchy
4. Execute (pass research results + file path in prompt)
5. Update memory → Reference saved plan

---

## Chain Execution Loop (THE HEART OF ORCHESTRATION)

**English Pattern for Sequential + Parallel Execution:**

```
LOOP:
1. Find runnable tasks:
   TaskList() → Find tasks where:
   - status = "pending"
   - blockedBy is empty OR all blockedBy tasks are "completed"

2. Start agent(s):
   - TaskUpdate(taskId, status="in_progress")
   - If MULTIPLE tasks ready (e.g., code-reviewer + silent-failure-hunter):
     → Invoke BOTH in SAME MESSAGE (parallel execution)
   - Pass task ID in prompt:
     Task(subagent_type="cc10x:{agent}", prompt="
       Your task ID: {taskId}
       User request: {request}
       Requirements: {requirements}
       Memory: {activeContext}
       SKILL_HINTS: {detected skills}
     ")

3. After agent completes:
   - Router calls TaskUpdate(taskId, status="completed")
   - Router validates agent output
   - Router calls TaskList() to find next tasks

4. Determine next:
   - Find tasks where ALL blockedBy tasks are "completed"
   - If multiple ready → Invoke ALL in parallel (same message)
   - If one ready → Invoke sequentially
   - If none ready AND uncompleted tasks exist → Error state
   - If ALL tasks completed → Workflow complete

5. Repeat until:
   - All tasks have status="completed"
   - OR critical error detected
```

**Critical English Trick:** "Both Task calls in same message = both complete before you continue" - This leverages Claude's tool execution model where parallel tool calls in one message complete before the next response.

---

## Task Hierarchy Structures

### BUILD Workflow Tasks

```
[Parent]      BUILD: {feature_summary}
                   |
[Agent 1]     component-builder: Implement {feature}
                   |
         ┌────────┴────────┐
         ▼                 ▼
[Agent 2a]             [Agent 2b]
code-reviewer    silent-failure-hunter
(blockedBy: 1)   (blockedBy: 1)
         |                 |
         └────────┬────────┘
                  ▼
[Agent 3]  integration-verifier
           (blockedBy: 2a, 2b)
                  |
                  ▼
[Task]     Memory Update           ← TASK-ENFORCED
           (blockedBy: 3)
```

### DEBUG Workflow Tasks

```
[Parent]      DEBUG: {error_summary}
                   |
[Agent 1]     bug-investigator: Investigate {error}
                   |
[Agent 2]     code-reviewer: Review fix (blockedBy: 1)
                   |
[Agent 3]     integration-verifier: Verify fix (blockedBy: 2)
                   |
[Task]        Memory Update (blockedBy: 3)  ← TASK-ENFORCED
```

---

## English Tricks & Patterns Used

### 1. Permission-Free Operations
Using specific tools to avoid permission prompts:
- `mkdir -p` as single command (no compound)
- `Read()` tool instead of `cat` command
- `Edit()` for updates instead of `Write()` for overwrites

### 2. Gate Enforcement Through English
"GATE: X" creates psychological checkpoints:
- MEMORY_LOADED - Before routing
- TASKS_CHECKED - Check TaskList() for active workflow
- INTENT_CLARIFIED - User intent is unambiguous
- RESEARCH_EXECUTED - Before planner (if github-research detected)
- RESEARCH_PERSISTED - Save + update memory
- REQUIREMENTS_CLARIFIED - Before invoking agent (BUILD only)
- TASKS_CREATED - Workflow task hierarchy created
- ALL_TASKS_COMPLETED - All agent tasks completed
- MEMORY_UPDATED - Before marking done

### 3. Confidence Scoring
"Only report issues with confidence ≥80" - Prevents vague feedback.

### 4. Rationalization Prevention Tables
Every skill has a table mapping excuses to reality:
```
| "I'll test later" | Tests passing immediately prove nothing |
```

### 5. Iron Laws
Each skill has a single, memorable rule that cannot be violated:
- session-memory: "LOAD memory at START, UPDATE at END"
- debugging-patterns: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
- code-review-patterns: "NO CODE QUALITY REVIEW BEFORE SPEC COMPLIANCE"
- test-driven-development: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- code-generation: "NO CODE BEFORE UNDERSTANDING FUNCTIONALITY AND PROJECT PATTERNS"
- planning-patterns: "NO VAGUE STEPS - EVERY STEP IS A SPECIFIC ACTION"
- architecture-patterns: "NO ARCHITECTURE DESIGN BEFORE FUNCTIONALITY FLOWS ARE MAPPED"
- frontend-patterns: "NO UI DESIGN BEFORE USER FLOW IS UNDERSTOOD"
- brainstorming: "NO DESIGN WITHOUT UNDERSTANDING PURPOSE AND CONSTRAINTS"
- verification-before-completion: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- github-research: "NO EXTERNAL RESEARCH WITHOUT CLEAR AI KNOWLEDGE GAP OR EXPLICIT USER REQUEST"

### 6. Agent-Specific Gates (Beyond Router Gates)

**component-builder: Plan File Check**
- If `Plan File` in prompt is NOT "None" → MUST read plan file first
- Match task to plan's phases/steps
- Follow plan's specific instructions
- Cannot proceed without reading plan

**bug-investigator: Anti-Hardcode Gate**
- Before writing regression test, identify variant dimensions:
  - Locale/i18n, config/env, roles/permissions, platform, time, data shape, concurrency, network, caching
- Regression test MUST cover at least one non-default variant case
- Prevents patchy/hardcoded fixes

### 6. Output Formats as Templates
Every agent/skill has a specific output format with sections:
- Forces structured thinking
- Ensures nothing is forgotten
- Makes handoffs consistent

---

## Agent → Skill Mapping

### Which Skills Each Agent Uses

All skills are loaded via agent frontmatter (automatic). Only `github-research` has conditional triggers.

| Agent | Mode | Frontmatter Skills | Conditional |
|-------|------|-------------------|-------------|
| component-builder | WRITE | session-memory, test-driven-development, code-generation, verification-before-completion, frontend-patterns, architecture-patterns | — |
| code-reviewer | READ-ONLY | code-review-patterns, verification-before-completion, frontend-patterns, architecture-patterns | — |
| silent-failure-hunter | READ-ONLY | code-review-patterns, verification-before-completion, frontend-patterns, architecture-patterns | — |
| integration-verifier | READ-ONLY | architecture-patterns, debugging-patterns, verification-before-completion, frontend-patterns | — |
| bug-investigator | WRITE | session-memory, debugging-patterns, test-driven-development, verification-before-completion, architecture-patterns, frontend-patterns | github-research (external/exhausted) |
| planner | WRITE | session-memory, planning-patterns, architecture-patterns, brainstorming, frontend-patterns | github-research (external tech) |

**Notes:**
- READ-ONLY agents don't load session-memory. They output `### Memory Notes` section; persisted via task-enforced "CC10X Memory Update" task at workflow-final.
- Only `github-research` uses conditional `Skill()` calls - all other skills load automatically via frontmatter.

### Context Retrieval Pattern (Used by planner, bug-investigator)

**When exploring unfamiliar or large codebases:**

```
Cycle 1: DISPATCH - Broad search (grep patterns, related keywords)
Cycle 2: EVALUATE - Score relevance (0-1), note codebase terminology
Cycle 3: REFINE - Focus on high-relevance (≥0.7), fill gaps
Max 3 cycles, then proceed with best available context
```

**Stop when:** Understand existing patterns, dependencies, and constraints (planner) OR 3+ files with relevance ≥0.7 AND no critical gaps (bug-investigator)

**English Trick:** Bounded exploration prevents infinite context gathering while ensuring adequate understanding.

---

## Memory Flow

### Load → Work → Update Cycle

```
SESSION START
      │
      ▼
┌─────────────────┐
│ LOAD MEMORY     │ Read all 3 files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ CHECK MEMORY    │ Before each decision
│ BEFORE DECISION │ - Did we decide this before?
└────────┬────────┘ - Is there a project pattern?
         │
         ▼
┌─────────────────┐
│ DO WORK         │ Execute workflow
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ UPDATE MEMORY   │ Edit (not Write!) for permission-free
└────────┬────────┘
         │
         ▼
   SESSION END
```

### Memory File Purposes

**activeContext.md** - What's happening NOW
- `## Current Focus` - Active work
- `## Recent Changes` - What changed (includes `[DEBUG-N]:` format for debug tracking)
- `## Next Steps` - What's next
- `## Decisions` - Choices made and why
- `## Learnings` - Insights discovered
- `## References` - Links to Plan, Design, Research files
- `## Blockers` - What's blocking progress
- `## Last Updated` - Timestamp

**patterns.md** - What we've LEARNED
- `## Architecture Patterns` - How this project implements patterns
- `## Code Conventions` - Naming, style, structure
- `## File Structure` - Where things go
- `## Testing Patterns` - How to write tests here
- `## Common Gotchas` - Bugs and solutions (including from research)
- `## API Patterns` - Endpoint conventions
- `## Error Handling` - How project handles errors
- `## Dependencies` - What's used and why

**progress.md** - What's DONE
- `## Current Workflow` - PLAN | BUILD | REVIEW | DEBUG
- `## Tasks` - Active task list with checkboxes
- `## Completed` - Done items with evidence
- `## Verification` - Commands + exit codes
- `## Last Updated` - Timestamp

---

## Research Flow (External)

### Three-Phase Pattern

```
Phase 1: Execute Research
         │
         ▼ (ATOMIC - no agent invocations between phases)
Phase 2: Persist Research
         - Bash("mkdir -p docs/research")
         - Write("docs/research/YYYY-MM-DD-<topic>-research.md")
         - Edit(".claude/cc10x/activeContext.md") → Add to Research References
         │
         ▼
Phase 3: Invoke Agent with Research Context
         - Task(cc10x:planner, prompt="...Research findings: {results}...")
```

**Critical:** "Research without persistence is LOST after context compaction."

---

## Handoff Patterns

### Router → Agent Handoff

```
Task(subagent_type="cc10x:component-builder", prompt="
Your task ID: {taskId}
User request: {request}
Requirements: {from AskUserQuestion}
Memory: {from activeContext.md}
Patterns: {from patterns.md}
SKILL_HINTS: {detected skills from table}
")
```

**Task ID is REQUIRED in prompt.** Router updates task status after agent returns (agents do NOT call TaskUpdate for own task).
**SKILL_HINTS are MANDATORY** - Agent must load each skill immediately.

### Agent → Router Handoff (Completion)

**All agents output two mandatory sections:**

1. **Dev Journal (User Transparency)** - Human-readable narrative:
   - What I Did (actions taken)
   - Key Decisions Made (decisions + WHY)
   - Alternatives Considered (what was rejected + reason)
   - Where Your Input Helps (decision points, assumptions to validate)
   - What's Next (what user should expect from next phase)

2. **Router Contract (Machine-Readable)** - YAML block for validation:
   ```yaml
   STATUS: [PASS|FAIL|APPROVE|CHANGES_REQUESTED|CLEAN|ISSUES_FOUND|FIXED|PLAN_CREATED]
   CONFIDENCE: [0-100]
   CRITICAL_ISSUES: [count]
   BLOCKING: [true|false]
   REQUIRES_REMEDIATION: [true|false]
   REMEDIATION_REASON: [null or exact text for REM-FIX task]
   MEMORY_NOTES:
     learnings: ["..."]
     patterns: ["..."]
     verification: ["..."]
   ```

**Router Contract enables:**
- Machine-readable validation (no fragile string parsing)
- Consistent remediation handling across all agents
- Memory Notes collection for workflow-final persistence

**WRITE agents** (component-builder, bug-investigator, planner):
1. Complete the work
2. Update memory directly using `Edit()` + `Read()` verify
3. Return structured output with Dev Journal + Router Contract

**READ-ONLY agents** (code-reviewer, silent-failure-hunter, integration-verifier):
1. Complete the analysis/verification
2. Include Memory Notes in Router Contract YAML
3. Return structured output with Dev Journal + Router Contract

**Router's responsibility after Task() returns:**
1. Call `TaskUpdate(taskId, status="completed")` (agents do NOT do this)
2. **Validate Router Contract:**
   - Look for `### Router Contract (MACHINE-READABLE)` section
   - Parse YAML block
   - If `BLOCKING=true` or `REQUIRES_REMEDIATION=true` → Create REM-FIX task, block downstream
   - Circuit breaker: If 3+ REM-FIX tasks exist → AskUserQuestion for direction
3. Collect `MEMORY_NOTES` from contract for workflow-final persistence
4. Call `TaskList()` to find next tasks
5. Find next runnable tasks (including "CC10X Memory Update" task)
6. Continue loop or complete workflow
7. **When Memory Update task becomes available:** Persist collected Memory Notes to `.claude/cc10x/*.md` (task-enforced, survives context compaction)

### Plan → Build Handoff

When plan is created:
1. Plan saved to `docs/plans/YYYY-MM-DD-<feature>-plan.md`
2. Memory updated with reference
3. User asked: "Execute now?" or "Manual execution?"

When executing plan:
1. component-builder receives `planFile` in task metadata
2. component-builder reads plan file
3. Follows plan task-by-task

---

## Verification Flow

### Before Any Completion Claim

```
IDENTIFY: What command proves this claim?
    │
    ▼
RUN: Execute the FULL command (fresh, complete)
    │
    ▼
READ: Full output, check exit code, count failures
    │
    ▼
VERIFY: Does output confirm the claim?
    │
    ├──▶ NO: State actual status with evidence
    │
    └──▶ YES: State claim WITH evidence
```

### Goal-Backward Lens (After Standard Verification)

```
GOAL: [What user wants to achieve]

TRUTHS (observable):
- [ ] [User-facing behavior 1]
- [ ] [User-facing behavior 2]

ARTIFACTS (exist):
- [ ] [Required file/endpoint 1]
- [ ] [Required file/endpoint 2]

WIRING (connected):
- [ ] [Component] → [calls] → [API]
- [ ] [API] → [queries] → [Database]

Standard verification: exit code 0 ✓
Goal check: All boxes checked?
```

---

## Task Coordination Mechanics

### The Hydration Pattern (Critical)

CC10x uses BOTH Tasks AND Memory files for different purposes:

```
┌─────────────────────┐     Session Start      ┌──────────────────┐
│  Memory Files       │ ────────────────────►  │  Claude Tasks    │
│  (progress.md)      │      "Hydrate"         │  (session state) │
└─────────────────────┘                        └──────────────────┘
                                                       │
                                                       │ Work
                                                       ▼
┌─────────────────────┐     Session End        ┌──────────────────┐
│  Memory Files       │  ◄──────────────────── │  Task Updates    │
│  (updated)          │      "Sync back"       │  (completed)     │
└─────────────────────┘                        └──────────────────┘
```

**Why this matters:**
- Tasks may be session-scoped (not guaranteed to persist across sessions)
- Memory files ARE persistent (survive sessions, stored in `.claude/cc10x/`)
- CC10x uses BOTH: Tasks for runtime coordination, memory for persistence
- At session start: Create tasks from progress.md state
- At session end: Sync task status back to progress.md

**The key insight:** Tasks are the execution engine; memory is the persistence layer.

### Cross-Session Coordination

The `CLAUDE_CODE_TASK_LIST_ID` environment variable enables shared task lists:

```bash
export CLAUDE_CODE_TASK_LIST_ID="project-name-tasks"
```

**What this enables:**
- Session A (Writer) completes Task #1
- Session B (Reviewer) sees Task #2 is now unblocked
- Both sessions share state in real-time

**CC10x Safety Stance:**
- Some sources say Tasks are session-scoped, others mention shared lists
- CC10x treats Tasks as **potentially long-lived/shared**
- Therefore: namespace with `CC10X ` prefix, keep examples schema-minimal
- Always scope before resuming (check if tasks belong to current project)

### When to Use Tasks (Decision Guide)

**USE Tasks when:**
| Scenario | Why |
|----------|-----|
| Multi-file features | Track progress across files |
| Large-scale refactors | Ensure nothing missed |
| Parallelizable work | Enable concurrent agents |
| Complex dependencies | Automatic unblocking |
| Sub-agent coordination | Shared progress tracking |

**SKIP Tasks when:**
| Scenario | Why |
|----------|-----|
| Single-function fixes | Overhead exceeds benefit |
| Simple bugs | Just fix it directly |
| Trivial edits | No tracking needed |
| < 3 steps | Not worth orchestration |

**The 3-Task Rule:** If you have fewer than 3 related steps, just do them directly.

---

## Summary: The Orchestration is Pure English

Every aspect of this system is English-based:

1. **Intent Detection** = Keyword matching in English
2. **Workflow Selection** = Decision tree described in English
3. **Gate Enforcement** = "GATE:" labels with psychological weight
4. **Chain Execution** = Instructions about task dependencies
5. **Parallel Execution** = "Both Task calls in same message"
6. **Memory Persistence** = Specific tool usage instructions
7. **Agent Behavior** = Templates and rationalization prevention
8. **Verification** = "NO completion claims without evidence"

The "code" is the English. The "compiler" is Claude's instruction following. The "bugs" are ambiguities, gaps, and conflicts in the English instructions.
