---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X - AUTO-LOAD AND EXECUTE for ANY development task.

  Triggers: build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy, memory, session, context, save, load, test, tdd, frontend, ui, backend, api, pattern, refactor, optimize, improve, enhance, update, modify, change, help, assist, work, start, begin, continue.

  CRITICAL: Execute workflow. Never just describe capabilities.
---

# cc10x Router - Workflow Execution Engine

**THIS IS AN EXECUTION ENGINE, NOT DOCUMENTATION.**

When this skill loads, you MUST:
1. Detect intent from user request
2. Execute the matching workflow
3. Invoke agents via Task tool
4. Update memory with results

## CRITICAL: What NOT To Do

**NEVER respond with:**
- "cc10x has these capabilities..."
- "Here are the skills available..."
- "I can use cc10x to..."
- "Let me list what cc10x can do..."

**ALWAYS respond with:**
- Detecting intent → Executing [WORKFLOW] workflow
- Loading memory...
- Clarifying requirements: [questions]
- Invoking [agent]...

## Execution Examples

<example>
user: "I want to build a task tracker app"
assistant: "Detected **BUILD** intent. Executing BUILD workflow.

**Loading memory...**
[Runs memory load command]

**Clarifying requirements (CRITICAL: DO NOT SKIP):**
1. What framework/language should I use? (Node.js, Python, etc.)
2. Should tasks have priorities, due dates, or categories?
3. CLI app or web app?
4. Any specific features beyond basic CRUD?

Please answer these questions so I can proceed with the right approach."
</example>

<example>
user: "help me create a simple API"
assistant: "Detected **BUILD** intent. Executing BUILD workflow.

**Loading memory...**
[Runs memory load command]

**Clarifying requirements (CRITICAL: DO NOT SKIP):**
1. What should this API do? (e.g., user management, data storage)
2. REST or GraphQL?
3. What language/framework? (Express, FastAPI, etc.)
4. Authentication needed?

Waiting for your answers before invoking component-builder."
</example>

<example>
user: "there's a bug in my login function"
assistant: "Detected **DEBUG** intent. Executing DEBUG workflow.

**Loading memory...**
[Runs memory load command - checking Common Gotchas]

**Understanding the issue:**
1. What error message are you seeing?
2. What's the expected behavior vs actual behavior?
3. When did it start happening?

Waiting for details before invoking bug-investigator with LOG FIRST approach."
</example>

## MANDATORY: Memory Operations (PERMISSION-FREE)

**ALL memory operations are PERMISSION-FREE using the correct tools.**

**EVERY workflow MUST:**

### 1. LOAD Memory FIRST (Before ANY routing)

**Use separate tool calls (PERMISSION-FREE):**

```
# Step 1: Create directory (single Bash command)
Bash(command="mkdir -p .claude/cc10x")

# Step 2: Load ALL 3 memory files using Read tool
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")
```

**NEVER use compound commands (they ask permission):**
```bash
# WRONG - asks permission
mkdir -p .claude/cc10x && cat .claude/cc10x/activeContext.md
```

**If memory exists:** Resume from context, avoid repeating work.
**If file doesn't exist:** Read returns error - means starting fresh.

### 2. UPDATE Memory LAST (After workflow completes)

**Use Edit tool (NO permission prompt):**
```
# First read existing content
Read(file_path=".claude/cc10x/activeContext.md")

# Then use Edit to replace (matches first line, replaces entire content)
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context

## Current Focus
[What was accomplished]

## Recent Changes
[Changes made]

## Next Steps
[What to do next]

## Active Decisions
| Decision | Choice | Why |
|----------|--------|-----|
[Decisions made]

## Learnings This Session
[What was learned]

## Last Updated
[current date/time]")
```

**WHY Edit not Write?** Write asks "Do you want to overwrite?" for existing files. Edit is always permission-free.

**Failure to update memory = incomplete workflow.**

## WORKFLOW SELECTION - Decision Tree (FOLLOW IN ORDER)

**DO NOT use intuition. Follow this decision tree EXACTLY.**

### Step 1: Check for ERROR signals (HIGHEST PRIORITY)
**Keywords:** error, bug, fix, broken, crash, fail, exception, debug, troubleshoot, issue, problem, wrong, doesn't work, not working, stopped working

**If ANY of these appear → DEBUG workflow**

### Step 2: Check for PLAN signals (Priority 2)
**Keywords:** plan, design, architect, roadmap, strategy, structure, blueprint, spec, specification

**User phrases:** "before we build", "let's think about", "how should we", "what's the best approach"

**If ANY of these appear (and NO error signals) → PLAN workflow**

### Step 3: Check for REVIEW signals (Priority 3)
**Keywords:** review, audit, check, analyze, assess, look at, examine, inspect

**User phrases:** "what do you think of", "is this good", "check my code", "any issues with"

**If ANY of these appear (and NO error/plan signals) → REVIEW workflow**

### Step 4: Default to BUILD (Priority 4)
**Everything else → BUILD workflow**

---

## CONFLICT RESOLUTION TABLE

When multiple keywords appear, use this table:

| User Says | Contains | Workflow | Why |
|-----------|----------|----------|-----|
| "fix the build script" | fix + build | **DEBUG** | "fix" = error signal (priority 1) |
| "plan how to fix the bug" | plan + fix + bug | **DEBUG** | "fix/bug" = error signal (priority 1) |
| "review and fix this" | review + fix | **DEBUG** | "fix" = error signal (priority 1) |
| "build a new feature" | build | **BUILD** | No error signal, default |
| "plan the new feature" | plan + feature | **PLAN** | Plan signal (priority 2) |
| "design the API" | design + API | **PLAN** | Design = plan signal |
| "review my changes" | review | **REVIEW** | Review signal (priority 3) |
| "check this code" | check | **REVIEW** | Check = review signal |
| "help me with this" | help | **BUILD** | No specific signal, default |
| "there's an issue with login" | issue | **DEBUG** | Issue = error signal |

---

## Intent Summary Table

| Workflow | Agent Chain | When |
|----------|-------------|------|
| DEBUG | bug-investigator → code-reviewer → integration-verifier | Error/bug/fix signals detected |
| PLAN | planner | Plan/design signals (no errors) |
| REVIEW | code-reviewer (or silent-failure-hunter for error audits) | Review signals (no errors/plan) |
| BUILD | component-builder → code-reviewer → silent-failure-hunter → integration-verifier | Default (no other signals) |

---

## HARD GATES (MUST PASS TO PROCEED)

**Gates are BLOCKING. Cannot proceed to next step without passing.**

### GATE 1: MEMORY_LOADED (Before ANY routing)

```
[GATE: MEMORY_LOADED]
- [ ] Ran: Bash(command="mkdir -p .claude/cc10x")
- [ ] Ran: Read(file_path=".claude/cc10x/activeContext.md")
- [ ] Ran: Read(file_path=".claude/cc10x/patterns.md")
- [ ] Ran: Read(file_path=".claude/cc10x/progress.md")

STATUS: [PASS/FAIL]
```

**If FAIL → STOP. Load memory before proceeding.**

### GATE 2: REQUIREMENTS_CLARIFIED (Before invoking any agent)

```
[GATE: REQUIREMENTS_CLARIFIED]
- [ ] Asked clarifying questions via AskUserQuestion
- [ ] Received user answers (not empty)
- [ ] If user said "whatever you think" → stated recommendation AND got confirmation

STATUS: [PASS/FAIL]
```

**If FAIL → STOP. Clarify requirements before invoking agent.**

### GATE 3: AGENT_COMPLETED (Before next agent in chain)

```
[GATE: AGENT_COMPLETED]
- [ ] Previous agent returned (not error)
- [ ] Captured: files modified
- [ ] Captured: key outputs for handoff

STATUS: [PASS/FAIL]
```

**If FAIL → STOP. Previous agent must complete before next.**

### GATE 4: WORKFLOW_COMPLETE (Before marking done)

```
[GATE: WORKFLOW_COMPLETE]
- [ ] All agents in chain invoked
- [ ] Each agent completed successfully
- [ ] Verification evidence captured (exit codes)
- [ ] Memory updated with Edit tool (permission-free)

STATUS: [PASS/FAIL]
```

**If FAIL → STOP. Cannot mark workflow complete.**

---

## Workflow Execution

### BUILD Workflow

When user wants to build/implement/create something:

0. **LOAD MEMORY** - Load ALL 3 files:
   - activeContext.md → prior decisions, current focus
   - patterns.md → project conventions to follow
   - progress.md → check if already done!

1. **CLARIFY REQUIREMENTS** - DO NOT SKIP
   - Use `AskUserQuestion` tool for structured questions with options
   - What exactly needs to be built?
   - What are the acceptance criteria?
   - What edge cases should be handled?
   - **WAIT for user answers before proceeding**
   - If user says "whatever you think", state your recommendation and get confirmation
   - **CHECK**: activeContext.md Active Decisions before choosing approach

2. **Invoke component-builder** - Uses TDD cycle (RED → GREEN → REFACTOR)
   - **CHECK**: patterns.md for code conventions during build

3. **Invoke code-reviewer** - Reviews the built code

4. **Invoke silent-failure-hunter** - (if error handling code) Audits error handling

5. **Invoke integration-verifier** - Verifies end-to-end functionality

6. **UPDATE MEMORY** - Save learnings, decisions, and progress

### REVIEW Workflow

When user wants to review/audit code:

0. **LOAD MEMORY** - Load ALL 3 files:
   - activeContext.md → what we're reviewing and why
   - patterns.md → project conventions to enforce
   - progress.md → related review findings
1. **Understand what to review** - Identify files/PR/changes
2. **Invoke code-reviewer** - Reviews for security, quality, performance
   - **CHECK**: patterns.md to apply project-specific standards
3. **UPDATE MEMORY** - Save review findings and patterns learned

### DEBUG Workflow

When user encounters errors/bugs:

0. **LOAD MEMORY** - Load ALL 3 files:
   - activeContext.md → may have clues from prior work
   - patterns.md → check Common Gotchas section!
   - progress.md → when did it last work?
1. **Understand what's broken** - Clarify the error/symptom
   - **CHECK**: patterns.md Common Gotchas before investigating
2. **Invoke bug-investigator** - Uses LOG FIRST approach to diagnose and fix
3. **Invoke code-reviewer** - Reviews the fix
4. **Invoke integration-verifier** - Verifies fix works end-to-end
5. **UPDATE MEMORY** - Save root cause, fix, and lessons learned (add to Common Gotchas!)

### PLAN Workflow

When user wants to plan/design:

0. **LOAD MEMORY** - Load ALL 3 files:
   - activeContext.md → prior decisions to align with
   - patterns.md → existing architecture to extend
   - progress.md → what's already done
1. **Understand what to plan** - Clarify scope and goals
   - **CHECK**: activeContext.md Active Decisions before proposing approach
2. **Invoke planner** - Creates architecture, identifies risks, builds roadmap
   - **CHECK**: patterns.md to align with existing patterns
3. **UPDATE MEMORY** - Save architectural decisions and rationale

## Agent Invocation - EXPLICIT HANDOFF TEMPLATES

**DO NOT use vague prompts. Use these exact templates with filled values.**

### BUILD Chain Templates

**Step 1: BUILDER**
```
Task(subagent_type="cc10x:component-builder", prompt="
CONTEXT FROM ROUTER:
- User request: {exact user request}
- Requirements: {answers from AskUserQuestion}
- Memory context: {relevant info from activeContext.md}
- Patterns to follow: {from patterns.md}
- Files to modify: {identified files}

SKILL TRIGGERS:
- If files in /components/, /ui/, /pages/ OR .tsx/.jsx → Load frontend-patterns
- If files in /api/, /routes/, /services/ → Load architecture-patterns

YOUR TASK: Build using TDD (RED → GREEN → REFACTOR)

HANDOFF OUTPUT (REQUIRED):
- Files created: [list]
- Files modified: [list]
- Tests added: [list]
- Exit codes: [test results]
")
```

**Step 2: REVIEWER (after builder)**
```
Task(subagent_type="cc10x:code-reviewer", prompt="
CONTEXT FROM BUILDER:
- Files modified: {from builder output}
- Tests added: {from builder output}
- Feature built: {description}

SKILL TRIGGERS:
- If .tsx/.jsx/.vue files → Load frontend-patterns
- If /api/, /routes/ files → Load architecture-patterns

YOUR TASK: Review for security, quality, performance (confidence >= 80 only)

HANDOFF OUTPUT (REQUIRED):
- Findings: [list with file:line]
- Fixes needed: [yes/no]
")
```

**Step 3: ERROR HUNTER (if error handling code)**
**TRIGGER:** If builder output contains: try, catch, except, .catch(, throw, error
```
Task(subagent_type="cc10x:silent-failure-hunter", prompt="
CONTEXT FROM REVIEWER:
- Files with error handling: {from grep}
- Review findings: {from reviewer}

YOUR TASK: Audit all error handling for silent failures

HANDOFF OUTPUT (REQUIRED):
- Critical issues: [list]
- Silent failures found: [yes/no]
")
```

**Step 4: VERIFIER (final)**
```
Task(subagent_type="cc10x:integration-verifier", prompt="
CONTEXT FROM CHAIN:
- Feature: {description}
- Files: {list}
- Tests: {list}

YOUR TASK: Verify end-to-end

HANDOFF OUTPUT (REQUIRED):
- Status: PASS/FAIL
- Evidence: [exit codes]
")
```

### DEBUG Chain Templates

**Step 1: INVESTIGATOR**
```
Task(subagent_type="cc10x:bug-investigator", prompt="
CONTEXT FROM ROUTER:
- Error reported: {user's error description}
- Expected behavior: {what should happen}
- Actual behavior: {what happens}
- Common Gotchas: {from patterns.md}

SKILL TRIGGERS:
- If error in /components/, /ui/ → Load frontend-patterns
- If error in /api/, /services/ → Load architecture-patterns

YOUR TASK: LOG FIRST, then diagnose and fix

HANDOFF OUTPUT (REQUIRED):
- Root cause: [description]
- Fix applied: [file:line]
- Regression test: [test file]
")
```

### PLAN Chain Template

```
Task(subagent_type="cc10x:planner", prompt="
CONTEXT FROM ROUTER:
- User request: {what to plan}
- Existing architecture: {from patterns.md}
- Prior decisions: {from activeContext.md}

SKILL TRIGGERS:
- If planning UI → Load frontend-patterns
- If requirements vague → Load brainstorming

YOUR TASK: Create architecture, risks, roadmap

OUTPUT (REQUIRED):
- Plan saved to: docs/plans/{date}-{feature}-plan.md
- Key decisions: [list]
")
```

### REVIEW Chain Template

```
Task(subagent_type="cc10x:code-reviewer", prompt="
CONTEXT FROM ROUTER:
- Files to review: {file list or PR}
- Project patterns: {from patterns.md}

SKILL TRIGGERS:
- If reviewing UI code → Load frontend-patterns
- If reviewing API code → Load architecture-patterns

YOUR TASK: Review with confidence scoring (report >= 80 only)

OUTPUT (REQUIRED):
- Status: Approve/Changes requested
- Findings: [list with confidence scores]
")
```

## Sequential vs Parallel

- **BUILD workflow**: Sequential (component-builder → code-reviewer → silent-failure-hunter → integration-verifier)
- **DEBUG workflow**: Sequential (bug-investigator → code-reviewer → integration-verifier)
- **REVIEW workflow**: Single agent (code-reviewer) or silent-failure-hunter (for error handling focus)
- **PLAN workflow**: Single agent (planner)

Always run agents sequentially when outputs depend on previous steps.

## Output Format

Provide brief progress updates after each significant tool use. After workflow completion, provide:

```markdown
## Workflow Summary

- **Intent**: [BUILD/REVIEW/DEBUG/PLAN]
- **Agents Used**: [list]
- **Result**: [success/issues found]
- **Memory Updated**: Yes/No

## Key Outcomes

[Summary of what was accomplished]

## Learnings & Decisions

[What was learned, decisions made and why]

## Next Steps

[If any follow-up needed]
```

## Memory Checklist

### READ Verification (Start + During)
- [ ] ALL 3 memory files loaded at workflow start
- [ ] Active Decisions checked before choosing approach
- [ ] patterns.md checked before making implementation choices
- [ ] progress.md checked to avoid repeating done work
- [ ] Common Gotchas checked when debugging

### WRITE Verification (End)
- [ ] activeContext.md updated with current state
- [ ] Learnings/decisions documented with reasoning
- [ ] patterns.md updated (if new patterns discovered)
- [ ] progress.md updated (if tasks completed)
- [ ] Common Gotchas updated (if bug was found/fixed)

**Workflow is NOT complete until BOTH checklists pass.**
