---
name: cc10x-router
description: |
  AUTO-LOAD AND EXECUTE when user says: build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy.

  MANDATORY: Execute the workflow - DO NOT just list capabilities or describe what cc10x can do.

  When triggered: (1) Detect intent, (2) Load memory, (3) Clarify requirements, (4) Execute agent chain, (5) Update memory.
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

## MANDATORY: Memory Operations

**EVERY workflow MUST:**

### 1. LOAD Memory FIRST (Before ANY routing)

```bash
echo "=== LOADING MEMORY ===" && mkdir -p .claude/cc10x
cat .claude/cc10x/activeContext.md 2>/dev/null || echo "No active context - starting fresh"
cat .claude/cc10x/patterns.md 2>/dev/null || echo "No patterns saved"
cat .claude/cc10x/progress.md 2>/dev/null || echo "No progress tracked"
echo "=== MEMORY LOADED ==="
```

**If memory exists:** Resume from context, avoid repeating work.
**If memory empty:** Start fresh, but WILL save at end.

### 2. UPDATE Memory LAST (After workflow completes)

Update `.claude/cc10x/activeContext.md` with:
- What was accomplished
- Decisions made and why
- Learnings discovered
- Next steps

**Failure to update memory = incomplete workflow.**

## Intent Detection

Detect intent from user request and route to the appropriate workflow:

| Intent Keywords | Workflow | Agent Chain |
|-----------------|----------|-------------|
| build, implement, create, write, add, make | BUILD | component-builder → code-reviewer → silent-failure-hunter (if error handling) → integration-verifier |
| review, audit, check, analyze, assess | REVIEW | code-reviewer |
| error handling, audit errors, catch blocks, silent failures | REVIEW (error focus) | silent-failure-hunter |
| debug, fix, error, bug, troubleshoot, broken | DEBUG | bug-investigator → code-reviewer → integration-verifier |
| plan, design, architect, roadmap, strategy | PLAN | planner |

## Workflow Execution

### BUILD Workflow

When user wants to build/implement/create something:

0. **LOAD MEMORY** - Load ALL 3 files:
   - activeContext.md → prior decisions, current focus
   - patterns.md → project conventions to follow
   - progress.md → check if already done!

1. **CLARIFY REQUIREMENTS** - **CRITICAL: DO NOT SKIP**
   - What exactly needs to be built?
   - What are the acceptance criteria?
   - What edge cases should be handled?
   - **Present questions to user in a clear list**
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

## Agent Invocation

Use Task tool to invoke agents:

```
Task(subagent_type="cc10x:component-builder", prompt="Build [component description]")
Task(subagent_type="cc10x:code-reviewer", prompt="Review [code/PR description]")
Task(subagent_type="cc10x:bug-investigator", prompt="Debug [error description]")
Task(subagent_type="cc10x:integration-verifier", prompt="Verify [integration description]")
Task(subagent_type="cc10x:planner", prompt="Plan [feature description]")
Task(subagent_type="cc10x:silent-failure-hunter", prompt="Audit error handling in [description]")
```

## Sequential vs Parallel

- **BUILD workflow**: Sequential (component-builder → code-reviewer → silent-failure-hunter → integration-verifier)
- **DEBUG workflow**: Sequential (bug-investigator → code-reviewer → integration-verifier)
- **REVIEW workflow**: Single agent (code-reviewer) or silent-failure-hunter (for error handling focus)
- **PLAN workflow**: Single agent (planner)

Always run agents sequentially when outputs depend on previous steps.

## Output Format

After workflow completion, provide:

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
