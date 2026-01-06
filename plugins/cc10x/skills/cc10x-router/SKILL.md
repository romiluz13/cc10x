---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X - AUTO-LOAD AND EXECUTE for ANY development task.

  Triggers: build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy, memory, session, context, save, load, test, tdd, frontend, ui, backend, api, pattern, refactor, optimize, improve, enhance, update, modify, change, help, assist, work, start, begin, continue.

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

| Workflow | Agents (Sequential) |
|----------|---------------------|
| BUILD | component-builder → code-reviewer → silent-failure-hunter* → integration-verifier |
| DEBUG | bug-investigator → code-reviewer → integration-verifier |
| REVIEW | code-reviewer |
| PLAN | planner |

*silent-failure-hunter only if error handling code exists (try/catch/except)

## Memory (PERMISSION-FREE)

**LOAD FIRST (Before routing):**
```
Bash(command="mkdir -p .claude/cc10x")
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")
```

**UPDATE LAST (After workflow):** Use Edit tool on activeContext.md (permission-free).

## Workflow Execution

### BUILD
1. Load memory → Check if already done in progress.md
2. **Clarify requirements** (DO NOT SKIP) → Use AskUserQuestion
3. Invoke component-builder (TDD: RED→GREEN→REFACTOR)
4. Invoke code-reviewer (confidence ≥80 only)
5. Invoke silent-failure-hunter (if try/catch exists)
6. Invoke integration-verifier
7. Update memory

### DEBUG
1. Load memory → Check patterns.md Common Gotchas
2. Clarify: What error? Expected vs actual? When started?
3. Invoke bug-investigator (LOG FIRST)
4. Invoke code-reviewer
5. Invoke integration-verifier
6. Update memory → Add to Common Gotchas

### REVIEW
1. Load memory
2. Invoke code-reviewer (check git history, confidence ≥80)
3. Update memory

### PLAN
1. Load memory
2. Invoke planner
3. Update memory → Reference saved plan

## Agent Invocation

Pass context to each agent:
```
Task(subagent_type="cc10x:component-builder", prompt="
User request: {request}
Requirements: {from AskUserQuestion}
Memory: {from activeContext.md}
Patterns: {from patterns.md}
")
```

**Skill triggers for agents:**
- Frontend code (components/, ui/, pages/, .tsx, .jsx) → Load frontend-patterns
- API code (api/, routes/, services/) → Load architecture-patterns

## Gates (Must Pass)

1. **MEMORY_LOADED** - Before routing
2. **REQUIREMENTS_CLARIFIED** - Before invoking agent (BUILD only)
3. **AGENT_COMPLETED** - Before next agent in chain
4. **MEMORY_UPDATED** - Before marking done
