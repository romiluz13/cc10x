---
name: plan-review-gate
description: "Inline adversarial plan review — 3 sequential checks (Feasibility, Completeness, Scope & Alignment) performed by the calling LLM in its own context. No subagents spawned. Call after saving a plan. Returns GATE_PASS or GATE_FAIL with blocking issues."
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion
---

# Plan Review Gate

**Core principle:** No plan reaches the user without surviving 3 adversarial checks.

**How it works:** This skill runs inline in the calling agent's context (no subagents). The calling LLM reads the plan and checks it against 3 criteria using its Read/Grep/Glob tools. Same LLM, same context — the value is structured adversarial framing, not agent independence.

## When to Skip

**Skip when plan is trivial:** Single-file fix, copy edit, or config tweak with <3 changes → return GATE_PASS immediately.

## The 3 Checks (Run in Sequence)

### Check 1: Feasibility — Can this be executed against the real codebase?

Run these verifications using Read/Grep/Glob:

| Criterion | How to verify | Blocking if |
|-----------|--------------|-------------|
| File paths exist | `Glob(pattern="{path}")` for every referenced file | Any path returns 0 matches and doesn't exist |
| Dependency ordering | Read plan phases — do later phases depend on earlier ones only? | Circular or forward-reference dependencies |
| Technical approach matches codebase | Read 1-2 existing files in the affected area | Proposed patterns/libs differ from what codebase actually uses |
| No unstated infra assumptions | Read plan for external services, env vars, DBs | Plan silently assumes infra that doesn't exist |

### Check 2: Completeness — Does it cover the full request?

Read the user's original request and compare against the plan:

| Criterion | Blocking if |
|-----------|-------------|
| All requirements mapped | Any user requirement has no corresponding plan item |
| Verification steps defined | Any change has no way to verify it worked |
| Edge cases addressed | Obvious error paths, empty states, or boundary conditions missing |
| Cross-file integration | Files that import from changed files not accounted for |

### Check 3: Scope & Alignment — Is it right-sized?

| Criterion | Blocking if |
|-----------|-------------|
| Matches user request | Plan solves different problem or adds unrequested features |
| No scope creep | Extra abstractions, refactoring, or features beyond the request |
| No under-scoping | Obvious implications of the request are omitted |
| Complexity proportional | Solution is over-engineered for the problem |

## Workflow

```text
1. Check if trivial → skip if yes (return GATE_PASS)
2. Run Check 1: Feasibility (use Read/Grep/Glob to verify file paths)
3. Run Check 2: Completeness (read request vs plan)
4. Run Check 3: Scope & Alignment (read request vs plan)
5. Collect findings:
   - Zero BLOCKING issues across all 3 checks → GATE_PASS
   - Any BLOCKING issue → GATE_FAIL with specifics
6. IF GATE_FAIL and iteration < 3:
   a. Present blocking issues clearly
   b. Revise the plan to address them
   c. Re-run checks (increment iteration counter)
7. IF GATE_FAIL after 3 iterations → ESCALATION: AskUserQuestion
```

## Output Format

### GATE_PASS

```
## Plan Review Gate — GATE_PASS (iteration N of 3)

| Check | Result | Key Finding |
|-------|--------|-------------|
| Feasibility | PASS | [evidence: file paths verified / patterns match] |
| Completeness | PASS | [evidence: all N requirements mapped] |
| Scope & Alignment | PASS | [evidence: plan matches request, no creep] |
```

### GATE_FAIL

```
## Plan Review Gate — GATE_FAIL (iteration N of 3)

| Check | Result | Blocking Issues |
|-------|--------|-----------------|
| Feasibility | PASS | — |
| Completeness | FAIL | [N] blocking issues |
| Scope & Alignment | FAIL | [N] blocking issues |

### Blocking Issues (MUST ADDRESS before returning PLAN_CREATED)
- [Check]: [specific issue with evidence]
```

### Escalation (3/3 iterations, still failing)

```
## Plan Review Gate — ESCALATION REQUIRED (3/3 iterations exhausted)

### Remaining Blocking Issues
[List by check with evidence]
```

→ Use `AskUserQuestion` with options: "Override (proceed with known risks)" | "Revise manually" | "Simplify scope" | "Cancel"

## Anti-Patterns

| Anti-Pattern | Why Wrong |
|--------------|-----------|
| Skipping file path verification | Fabricated paths are the #1 plan failure mode |
| Treating GATE_FAIL as advisory | GATE_FAIL must block PLAN_CREATED |
| Skipping for "simple" plans | Read the skip criteria — only truly trivial plans qualify |
| Accepting GATE_PASS without evidence | Each check needs a cited finding, not just "looks fine" |
