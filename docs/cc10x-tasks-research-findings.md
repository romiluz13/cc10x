# Claude Code Tasks Research Findings (Jan 2026 Feature)

> **Source:** VentureBeat, Medium articles by Joe Njenga and Rick Hightower, official changelog analysis

---

## Executive Summary

The Tasks feature was released in **Claude Code v2.1.16 (January 23, 2026)** as a replacement for the old "Todos" system. This is a fundamental architectural change that transforms Claude Code from a reactive assistant into a **state-aware project orchestrator**.

---

## Key Distinctions: Todos vs Tasks

| Aspect | Old Todos (Deprecated) | New Tasks (v2.1.16+) |
|--------|------------------------|----------------------|
| **Persistence** | Memory-only, vanish on session end | Filesystem-based (`~/.claude/tasks/`) |
| **Structure** | Linear checklist | **Directed Acyclic Graph (DAG)** |
| **Dependencies** | None | Full `blockedBy`/`blocks` support |
| **Cross-session** | Impossible | Via `CLAUDE_CODE_TASK_LIST_ID` env var |
| **Multi-agent** | No coordination | **Shared state across agents** |
| **Subagent awareness** | None | Full visibility |

---

## The Four Task Tools (Official API)

### 1. TaskCreate
```javascript
TaskCreate({
  subject: "Implement JWT authentication middleware",  // Imperative form
  description: "Add JWT validation to API routes...", // Full requirements
  activeForm: "Implementing JWT authentication",       // Present continuous (spinner)
  metadata: { feature: "auth", phase: "2.1" }         // Arbitrary key-value pairs
})
```

**Parameters:**
- `subject` (required): Brief imperative title
- `description` (required): Detailed requirements and acceptance criteria
- `activeForm` (optional): Present-tense form shown in progress spinner
- `metadata` (optional): Arbitrary key-value pairs for tracking

### 2. TaskUpdate
```javascript
TaskUpdate({
  taskId: "task-123",
  status: "in_progress",          // pending → in_progress → completed
  addBlockedBy: ["task-122"],     // I cannot start until these complete
  addBlocks: ["task-124"],        // These cannot start until I complete
  owner: "code-reviewer"          // Assign to specific agent
})
```

**Key Parameters:**
- `status`: `pending` → `in_progress` → `completed` (or `deleted`)
- `addBlockedBy`: Tasks that must complete before this one starts
- `addBlocks`: Tasks that cannot start until this one completes
- `owner`: Assign to a specific agent

### 3. TaskList
```javascript
TaskList()
// Returns for each task:
// - id: unique identifier
// - subject: task title
// - status: pending | in_progress | completed
// - owner: assigned agent (if any)
// - blockedBy: list of blocking task IDs
```

A task is **"available"** when:
- status = `pending`
- owner is empty (not assigned)
- blockedBy list is empty (all dependencies resolved)

### 4. TaskGet
```javascript
TaskGet({ taskId: "task-123" })
// Returns full task details including:
// - subject, description
// - status, owner
// - blockedBy, blocks
// - metadata
```

---

## Critical Architecture Insight: Session-Scoped by Design

> **"Tasks are session-scoped. They don't persist across sessions. This isn't a bug. It's a design choice."**
> — Rick Hightower, Medium

### What This Means:
1. Tasks stored at `~/.claude/tasks/` contain **only lock files for coordination**
2. When session ends, task data is **gone**
3. To persist across sessions, use the **Hydration Pattern**

### The Hydration Pattern (CRITICAL)

```
┌─────────────────────┐     Session Start      ┌──────────────────┐
│  Persistent Files   │ ────────────────────►  │  Claude Tasks    │
│  (spec, plan, etc)  │      "Hydrate"         │  (session-scoped)│
└─────────────────────┘                        └──────────────────┘
                                                       │
                                                       │ Work
                                                       ▼
┌─────────────────────┐     Session End        ┌──────────────────┐
│  Persistent Files   │  ◄──────────────────── │  Task Updates    │
│  (updated)          │      "Sync back"       │  (completed)     │
└─────────────────────┘                        └──────────────────┘
```

### Hydration in Practice:

**Session Start:**
1. Read spec/plan files (e.g., `.claude/cc10x/progress.md`)
2. Create Claude Tasks for each unchecked/pending item
3. Set up dependencies using `addBlockedBy`

**During Session:**
- Tasks track progress in real-time
- Status updates: pending → in_progress → completed
- Parallel agents coordinate through shared task list

**Session End:**
1. Update spec files with completed status
2. Update progress.md with current state
3. Commit changes to git for audit trail

---

## Cross-Session Coordination

### The `CLAUDE_CODE_TASK_LIST_ID` Environment Variable

By setting this env var, **multiple Claude Code sessions can share the same task list**:

```bash
export CLAUDE_CODE_TASK_LIST_ID="my-project-tasks"
```

**What this enables:**
- Session A (Writer) completes Task #1
- Session B (Reviewer) sees Task #2 is now unblocked
- Both sessions share state in real-time

### Multi-Agent Patterns

From VentureBeat:
> "The most potent technical unlock is the ability to share state across sessions. By setting the CLAUDE_CODE_TASK_LIST_ID environment variable, developers can point multiple instances of Claude at the same task list."

---

## Parallel Agent Coordination (Key for cc10x)

### The Pattern That Works:

```
Main Session (Orchestrator):
├── Creates task hierarchy with dependencies
├── Spawns Agent A → Works on independent feature
├── Spawns Agent B → Works on another feature
└── When both complete, spawns Agent C (was blocked by A & B)
```

### Key Success Factors (from real case study):

1. **Scoped Access Rights**: Each agent limited to specific directories
2. **Independent Branches**: Features with no shared dependencies progress simultaneously
3. **Central Coordination**: Orchestrator maintains shared task list

### Example from code_agent_context_hooks project:
```
Agent A: Rust governance (cch_cli/) - 12 tasks
Agent B: React UI (rulez_ui/) - Milestone 1

Result: Both features completed in single session
        Sequential would have taken 2x longer
```

---

## Implications for cc10x Design

### What cc10x Is Doing RIGHT:

1. ✅ Using router as central orchestrator
2. ✅ Defining task dependencies (blockedBy)
3. ✅ Running parallel agents (code-reviewer ∥ silent-failure-hunter)
4. ✅ Using memory files for persistence

### What cc10x NEEDS TO CHANGE:

1. **Embrace Hydration Pattern Explicitly**
   - Session start: Create tasks from progress.md state
   - Session end: Sync task status back to progress.md

2. **Don't Store Task IDs in Memory Files**
   - Task IDs are session-scoped
   - Store phase names/status, not task IDs
   - On resume: Create FRESH tasks matching state

3. **Leverage Shared Task List for Parallel Agents**
   - All agents see same task list automatically
   - When one completes a task, others see it immediately
   - No need for explicit result merging in many cases

4. **Use `activeForm` Properly**
   - Router should pass `activeForm` to agents
   - Shows progress in spinner during execution

---

## Task Status Flow

```
┌─────────┐       ┌─────────────┐       ┌───────────┐
│ pending │──────►│ in_progress │──────►│ completed │
└─────────┘       └─────────────┘       └───────────┘
     │                   │
     │                   │
     └───────────────────┴──────────► deleted
```

### State Transitions:
- `pending` → `in_progress`: When agent starts work
- `in_progress` → `completed`: When agent finishes
- Any → `deleted`: When task removed

### Blocked Tasks:
- Task with non-empty `blockedBy` cannot become `in_progress`
- When blocking task completes, blocked task automatically becomes available

---

## Decision Matrix: When to Use Tasks

### USE Tasks When:
| Scenario | Why |
|----------|-----|
| Multi-file features | Track progress across files |
| Large-scale refactors | Ensure nothing missed |
| Parallelizable work | Enable concurrent agents |
| Complex dependencies | Automatic unblocking |
| Sub-agent coordination | Shared progress tracking |

### SKIP Tasks When:
| Scenario | Why |
|----------|-----|
| Single-function fixes | Overhead exceeds benefit |
| Simple bugs | Just fix it directly |
| Trivial edits | No tracking needed |
| < 3 steps | Not worth orchestration |

### The 3-Task Rule:
> "If you have fewer than 3 related steps, just do them directly."

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_TASK_LIST_ID` | Share task list across sessions |
| `CLAUDE_CODE_ENABLE_TASKS=false` | Opt-out of new system (migration) |

---

## Changelog Highlights (v2.1.16-v2.1.19)

- **v2.1.16**: Tasks introduced, replacing Todos
- **v2.1.17**: Fixed OOM crashes with heavy subagent usage
- **v2.1.19**: Fixed dangling processes, added opt-out flag

---

## Key Quotes

> "With Opus 4.5 running longer autonomous workflows, Anthropic needed something better than a memory-bound to-do list."
> — Joe Njenga

> "By giving Claude Code a persistent memory, a way to understand dependency, and the stability fixes required for long-running processes, they have moved the tool from a 'copilot' that sits next to you to a 'subagent' that can be trusted to run in the background."
> — VentureBeat

> "The code is cheap; it is the context, the plan, and the reliability that are precious."
> — VentureBeat

---

## References

1. [Claude Code Tasks Are Here - Joe Njenga (Medium)](https://medium.com/@joe.njenga/claude-code-tasks-are-here-new-update-turns-claude-code-todos-to-tasks-a0be00e70847)
2. [Claude Code Todos to Tasks - Rick Hightower (Medium)](https://medium.com/@richardhightower/claude-code-todos-to-tasks-5a1b0e351a1c)
3. [VentureBeat: Claude Code's 'Tasks' update](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)
4. [Claude Code Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
