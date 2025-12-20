---
name: planning-patterns
description: Use when you have a spec or requirements for a multi-step task, before touching code
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

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Prerequisites:** [What must exist before starting]

---
```

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

## Requirements Checklist

Before writing a plan:

- [ ] Problem statement clear
- [ ] Users identified
- [ ] Functional requirements listed
- [ ] Non-functional requirements listed (performance, security, scale)
- [ ] Constraints documented
- [ ] Success criteria defined
- [ ] Existing code patterns understood

## Risk Assessment Table

For each identified risk:

| Risk | Probability (1-5) | Impact (1-5) | Score | Mitigation |
|------|-------------------|--------------|-------|------------|
| API timeout | 3 | 4 | 12 | Retry with backoff |
| Invalid input | 4 | 2 | 8 | Validation layer |
| Auth bypass | 2 | 5 | 10 | Security review |

Score = Probability × Impact. Address risks with score > 8 first.

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

## Phase 1: Foundation

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

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete. Two execution options:**

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
