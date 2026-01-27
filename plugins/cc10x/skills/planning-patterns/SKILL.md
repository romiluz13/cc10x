---
name: planning-patterns
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** Plans must be executable without asking questions.

## The Iron Law

```
NO VAGUE STEPS - EVERY STEP IS A SPECIFIC ACTION
```

"Add validation" is not a step. "Write test for empty email, run it, implement check, run it, commit" - that's 5 steps.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

**Not a step:**

- "Add authentication" (too vague)
- "Implement the feature" (multiple actions)
- "Test it" (which tests? how?)

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED: Follow this plan task-by-task using TDD.
> **Design:** See `docs/plans/YYYY-MM-DD-<feature>-design.md` for full specification.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Prerequisites:** [What must exist before starting]

---
```

**Note:** If a design document exists, always reference it in the header.

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/test.ts`

**Step 1: Write the failing test**

```typescript
test('specific behavior being tested', () => {
  const result = functionName(input);
  expect(result).toBe(expected);
});
```

**Step 2: Run test to verify it fails**

Run: `npm test tests/path/test.ts -- --grep "specific behavior"`
Expected: FAIL with "functionName is not defined"

**Step 3: Write minimal implementation**

```typescript
function functionName(input: InputType): OutputType {
  return expected;
}
```

**Step 4: Run test to verify it passes**

Run: `npm test tests/path/test.ts -- --grep "specific behavior"`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.ts src/path/file.ts
git commit -m "feat: add specific feature"
```
```

## Context is King (Cole Medin Principle)

**The plan must contain ALL information for a single-pass implementation.**

A developer with zero codebase context should be able to execute the plan WITHOUT asking any questions.

### Context References Section (MUST READ!)

**Every plan MUST include a Context References section:**

```markdown
## Relevant Codebase Files

### Patterns to Follow
- `src/components/Button.tsx` (lines 15-45) - Component structure pattern
- `src/services/api.ts` (lines 23-67) - API service pattern

### Configuration Files
- `tsconfig.json` - TypeScript settings
- `.env.example` - Environment variables needed

### Related Documentation
- `docs/architecture.md#authentication` - Auth flow overview
- `README.md#running-tests` - Test commands
```

**Why:** Claude forgets context. External docs get stale. File:line references are always accurate.

## Validation Levels

**Match validation depth to plan complexity:**

| Level | Name | Commands | When |
|-------|------|----------|------|
| 1 | Syntax & Style | `npm run lint`, `tsc --noEmit` | Every task |
| 2 | Unit Tests | `npm test` | Low-Medium risk |
| 3 | Integration Tests | `npm run test:integration` | Medium-High risk |
| 4 | Manual Validation | User flow walkthrough | High-Critical risk |

**Include specific validation commands in each task step.**

## Requirements Checklist

Before writing a plan:

- [ ] Problem statement clear
- [ ] Users identified
- [ ] Functional requirements listed
- [ ] Non-functional requirements listed (performance, security, scale)
- [ ] Constraints documented
- [ ] Success criteria defined
- [ ] Existing code patterns understood
- [ ] Context References section prepared with file:line references

## Risk Assessment Table

For each identified risk:

| Risk | Probability (1-5) | Impact (1-5) | Score | Mitigation |
|------|-------------------|--------------|-------|------------|
| API timeout | 3 | 4 | 12 | Retry with backoff |
| Invalid input | 4 | 2 | 8 | Validation layer |
| Auth bypass | 2 | 5 | 10 | Security review |

Score = Probability × Impact. Address risks with score > 8 first.

## Risk-Based Testing Matrix

**Match testing depth to task risk:**

| Task Risk | Example | Tests Required |
|-----------|---------|----------------|
| Trivial | Typo fix, docs update | None |
| Low | Single file change, utility function | Unit tests only |
| Medium | Multi-file feature, new component | Unit + Integration tests |
| High | Cross-service, auth, state management | Unit + Integration + E2E tests |
| Critical | Payments, security, data migrations | All tests + Security audit |

**How to assess risk:**
- How many files touched? (1 = low, 3+ = medium, cross-service = high)
- Is it auth/payments/security? (always high or critical)
- Is it user-facing? (medium minimum)
- Can it cause data loss? (high or critical)

**Use this matrix when planning test steps. Don't over-test trivial changes. Don't under-test critical ones.**

## Functionality Flow Mapping

Before planning, document all flows:

**User Flow:**
```
1. User clicks [button]
2. System shows [form]
3. User enters [data]
4. System validates [input]
5. System saves [data]
6. System shows [confirmation]
```

**Admin Flow:**
```
1. Admin opens [dashboard]
2. Admin selects [item]
3. System shows [details]
4. Admin changes [setting]
5. System applies [change]
```

**System Flow:**
```
1. Request arrives at [endpoint]
2. Middleware validates [auth]
3. Controller calls [service]
4. Service queries [database]
5. Response returns [data]
```

## Architecture Decision Records (ADR)

**When comparing approaches, document the decision formally:**

Use this format when a plan involves choosing between multiple valid approaches:

```markdown
## ADR: [Decision Title]

**Context:** What situation or requirement prompted this decision?

**Decision:** What approach did we choose?

**Consequences:**
- **Positive:** [benefits of this choice]
- **Negative:** [tradeoffs we accept]
- **Alternatives Considered:** [what we didn't choose and why]
```

**When to use ADR:**
- Choosing between architectures (monolith vs microservices)
- Selecting libraries/frameworks (React vs Vue)
- Database decisions (SQL vs NoSQL)
- Authentication approaches (JWT vs sessions)

**Save ADRs to:** `docs/decisions/ADR-NNN-title.md`

## Red Flags - STOP and Revise

If you find yourself:

- Writing "add feature" without exact file paths
- Skipping the test step
- Combining multiple actions into one step
- Using "etc." or "similar" instead of explicit steps
- Planning without understanding existing code patterns
- Creating steps that take more than 5 minutes
- Not including expected output for test commands

**STOP. Revise the plan with more specific steps.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "They'll know what I mean" | No they won't. Be explicit. |
| "Too much detail is annoying" | Vague plans cause bugs. |
| "Testing is obvious" | Write the test command. |
| "File paths are discoverable" | Write the exact path. |
| "Commits are implied" | Write when to commit. |
| "They can figure out edge cases" | List every edge case. |

## Output Format

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED: Follow this plan task-by-task using TDD.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Technologies]

**Prerequisites:** [Requirements]

---

## Phase 1: [Demonstrable Milestone]

> **Exit Criteria:** [What must be true when this phase is complete - e.g., "User can log in and receive JWT"]

### Task 1: [First Component]

**Files:**
- Create: `src/path/file.ts`
- Test: `tests/path/file.test.ts`

**Step 1:** Write failing test
[code block with test]

**Step 2:** Run test, verify fails
Run: `[command]`
Expected: FAIL

**Step 3:** Implement
[code block with implementation]

**Step 4:** Run test, verify passes
Run: `[command]`
Expected: PASS

**Step 5:** Commit
```bash
git add [files]
git commit -m "feat: [description]"
```

### Task 2: [Second Component]
...

---

## Risks

| Risk | P | I | Score | Mitigation |
|------|---|---|-------|------------|
| ... | ... | ... | ... | ... |

---

## Success Criteria

- [ ] All tests pass
- [ ] Feature works as specified
- [ ] No regressions
- [ ] Code reviewed
```

## Save the Plan (MANDATORY)

**Two saves are required - plan file AND memory update:**

### Step 1: Save Plan File (Use Write tool - NO PERMISSION NEEDED)

```
# First create directory
Bash(command="mkdir -p docs/plans")

# Then save plan using Write tool (permission-free)
Write(file_path="docs/plans/YYYY-MM-DD-<feature>-plan.md", content="[full plan content from output format above]")

# Then commit (separate commands to avoid permission prompt)
Bash(command="git add docs/plans/*.md")
Bash(command="git commit -m 'docs: add <feature> implementation plan'")
```

### Step 2: Update Memory (CRITICAL - Links Plan to Memory)

**Use Edit tool (NO permission prompt):**

```
# First read existing content
Read(file_path=".claude/cc10x/activeContext.md")

# Then use Edit to replace (matches first line, replaces entire content)
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context

## Current Focus
Plan created for [feature]. Ready for execution.

## Recent Changes
- Plan saved to docs/plans/YYYY-MM-DD-<feature>-plan.md

## Next Steps
1. Execute plan at docs/plans/YYYY-MM-DD-<feature>-plan.md
2. Follow TDD cycle for each task
3. Update progress.md after each task

## Active Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| [Key decisions from plan] | [Choice] | [Reason] |

## Plan Reference
**Execute:** `docs/plans/YYYY-MM-DD-<feature>-plan.md`

## Last Updated
[current date/time]")
```

**Also append to progress.md using Edit:**
```
Read(file_path=".claude/cc10x/progress.md")

Edit(file_path=".claude/cc10x/progress.md",
     old_string="[last section heading]",
     new_string="[last section heading]

## Plan Created
- [x] Plan saved - docs/plans/YYYY-MM-DD-<feature>-plan.md")
```

**WHY BOTH:** Plan files are artifacts. Memory is the index. Without memory update, next session won't know the plan exists.

**This is non-negotiable.** Memory is the single source of truth.

## Task-Based Execution Tracking

After saving plan, create execution tasks for tracking progress:

### Step 1: Create Parent Task
```
TaskCreate({
  subject: "Execute: {feature} Plan",
  description: "Plan file: docs/plans/YYYY-MM-DD-{feature}-plan.md\n\n{brief_plan_summary}",
  activeForm: "Executing {feature} plan",
  metadata: {
    planFile: "docs/plans/YYYY-MM-DD-{feature}-plan.md",
    workflow: "PLAN_EXECUTION",
    feature: "{feature}"
  }
})
# Returns parent_task_id
```

### Step 2: Create Phase Tasks with Dependencies
```
# For each phase in plan:
TaskCreate({
  subject: "Phase 1: {phase_title}",
  description: "**Plan:** docs/plans/YYYY-MM-DD-{feature}-plan.md\n**Section:** Phase 1\n**Exit Criteria:** {demonstrable_milestone}\n\n{phase_details}",
  activeForm: "Working on {phase_title}",
  metadata: {
    planFile: "docs/plans/YYYY-MM-DD-{feature}-plan.md",
    phase: "1",
    phaseTitle: "{phase_title}"
  }
})
# Returns phase_1_id

TaskCreate({
  subject: "Phase 2: {phase_title}",
  description: "**Plan:** docs/plans/YYYY-MM-DD-{feature}-plan.md\n**Section:** Phase 2\n**Exit Criteria:** {demonstrable_milestone}\n\n{phase_details}",
  activeForm: "Working on {phase_title}",
  metadata: {
    planFile: "docs/plans/YYYY-MM-DD-{feature}-plan.md",
    phase: "2",
    phaseTitle: "{phase_title}"
  }
})
TaskUpdate({ taskId: phase_2_id, addBlockedBy: [phase_1_id] })

# Continue for all phases...
```

### Step 3: Store Task IDs in Memory

Update `.claude/cc10x/progress.md` with task IDs:
```
Edit(file_path=".claude/cc10x/progress.md",
     old_string="## Current Workflow",
     new_string="## Current Workflow
PLAN → Execution

## Active Workflow Tasks

| Task ID | Subject | Status | Blocked By |
|---------|---------|--------|------------|
| {parent_id} | Execute: {feature} Plan | pending | - |
| {phase_1_id} | Phase 1: {title} | pending | - |
| {phase_2_id} | Phase 2: {title} | pending | {phase_1_id} |

Last Updated: {timestamp}")
```

**WHY:** Tasks enable resume capability across sessions. If conversation compacts or session ends, TaskList() will show where to continue.

## Plan-Task Linkage (Context Preservation)

**The relationship between Plan Files and Tasks:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  PLAN FILE (Persistent - Source of Truth)                           │
│  Location: docs/plans/YYYY-MM-DD-{feature}-plan.md                 │
│  Contains: Full implementation details, TDD steps, file paths      │
│  Survives: Session close, context compaction, conversation reset   │
└─────────────────────────────────────────────────────────────────────┘
                              ↕ metadata.planFile links them
┌─────────────────────────────────────────────────────────────────────┐
│  TASKS (Session-Scoped - Execution Engine)                          │
│  Storage: In-memory (ephemeral per session)                        │
│  Contains: Status, dependencies, progress tracking                 │
│  Survives: Within session only (unless using TASK_LIST_ID)         │
└─────────────────────────────────────────────────────────────────────┘
```

**metadata.planFile is CRITICAL:** If context compacts mid-execution, the task description contains enough info to:
1. Find the plan file
2. Locate the exact phase/task
3. Continue without asking questions

**Phase Exit Criteria are CRITICAL:** Each phase MUST have a demonstrable milestone (not arbitrary naming):
- ❌ "Phase 1: Foundation" - Vague, when is it done?
- ✅ "Phase 1: User can authenticate" - Demonstrable, testable

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - Fresh subagent per task, review between tasks, fast iteration

**2. Manual Execution** - Follow plan step by step, verify each step

**Which approach?"**

## Remember

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- Each step = one action (2-5 minutes)
- No assumptions about context
