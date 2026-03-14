name: plan-review-gate
description: "Use after saving a non-trivial plan or decision RFC when a fail-closed feasibility, completeness, and alignment review must block execution."
allowed-tools: Read, Bash, Grep, Glob
---

# Spec Review Gate

**Core principle:** No execution plan or decision RFC reaches the user without surviving adversarial scrutiny. No leniency. "Close enough" is FAIL.

**How it works:** This skill runs inline in the calling agent's context (no subagents). The calling LLM acts as an independent auditor, reads the saved artifact, and checks it against 3 criteria using Read/Grep/Glob. The value is fail-closed blocking and adversarial framing, not fake reviewer independence.

**Important limit:** This gate is stronger wording plus hard blocking, not true reviewer isolation. Keep the auditor posture, but do not pretend fresh runtime separation exists when it does not.

## When to Skip

**Skip when artifact is truly trivial:** Single-file fix, copy edit, or config tweak with <3 changes and no architecture choice → return `SPEC_GATE_PASS` immediately.

## The 3 Checks (Run in Sequence)

### Check 1: Feasibility — Can this be executed against the real codebase?

Run these verifications using Read/Grep/Glob:

| Criterion | How to verify | Blocking if |
|-----------|--------------|-------------|
| Artifact file exists on disk | `Glob(pattern="{plan_file_path}")` where plan_file_path is the path from the calling agent's context | Returns 0 matches |
| File paths exist | `Glob(pattern="{path}")` for every referenced file | Any path returns 0 matches and doesn't exist |
| Dependency ordering | Read plan phases — do later phases depend on earlier ones only? | Circular or forward-reference dependencies |
| Technical approach matches codebase | Read 1-2 existing files in the affected area | Proposed patterns/libs differ from what codebase actually uses |
| No unstated infra assumptions | Read plan for external services, env vars, DBs | Plan silently assumes infra that doesn't exist |
| Plan mode fits the task | Read request + artifact: `direct`, `execution_plan`, or `decision_rfc` | Mode is too weak for the request |
| Verification rigor fits risk | Check `verification_rigor` against the requested work | Critical-path work is missing `critical_path` rigor or claims proof it never defined |

### Check 2: Completeness — Does it cover the full request?

Read the user's original request and compare against the plan:

| Criterion | Blocking if |
|-----------|-------------|
| All requirements mapped | Any user requirement has no corresponding plan item |
| Verification steps defined | Any change has no way to verify it worked |
| Edge cases addressed | Obvious error paths, empty states, or boundary conditions missing |
| Cross-file integration | Files that import from changed files not accounted for |
| Decision-grade content present when needed | A `decision_rfc` is missing alternatives, drawbacks, or references |
| Critical-path spec present when needed | A `critical_path` artifact is missing behavior contract, edge-case catalog, provable properties, purity boundary, or verification strategy |

### Check 3: Scope & Alignment — Is it right-sized and faithful?

| Criterion | Blocking if |
|-----------|-------------|
| Matches user request | Plan solves different problem or adds unrequested features |
| No scope creep | Extra abstractions, refactoring, or features beyond the request |
| No under-scoping | Obvious implications of the request are omitted |
| Complexity proportional | Solution is over-engineered for the problem |
| Defaults are framed honestly | A recommended default is treated as approved instead of still-open |
| Agreement fidelity holds | `Differences from agreement` is missing, hidden, or contradicted by the body |

## Workflow

```text
1. Check if trivial → skip if yes (return SPEC_GATE_PASS)
2. Run Check 1: Feasibility (use Read/Grep/Glob to verify file paths)
3. Run Check 2: Completeness (read request vs plan)
4. Run Check 3: Scope & Alignment (read request vs plan)
5. Collect findings:
   - Zero BLOCKING issues across all 3 checks → SPEC_GATE_PASS
   - Any BLOCKING issue → SPEC_GATE_FAIL with specifics
   - There is no "APPROVED WITH COMMENTS"
6. IF SPEC_GATE_FAIL and iteration < 3:
   a. Present blocking issues clearly
   b. Revise the plan to address them
   c. Re-run checks (increment iteration counter)
   <!-- CC10X-M9: iteration counter is in-context only — not persisted to memory. If compaction occurs mid-retry, counter resets to 0 and gate may retry more than 3 times. Acceptable for now (gate still converges). -->
7. IF SPEC_GATE_FAIL after 3 iterations → ESCALATION: emit a blocking review result and stop
```

## Output Format

### SPEC_GATE_PASS

```
## Spec Gate — SPEC_GATE_PASS (iteration N of 3)

| Check | Result | Key Finding |
|-------|--------|-------------|
| Feasibility | PASS | [evidence: file paths verified / patterns match] |
| Completeness | PASS | [evidence: all N requirements mapped / required decision or proof sections present] |
| Alignment | PASS | [evidence: artifact matches request, no hidden defaults or scope creep] |
```

### SPEC_GATE_FAIL

```
## Spec Gate — SPEC_GATE_FAIL (iteration N of 3)

| Check | Result | Blocking Issues |
|-------|--------|-----------------|
| Feasibility | PASS | — |
| Completeness | FAIL | [N] blocking issues |
| Alignment | FAIL | [N] blocking issues |

### Blocking Issues (MUST ADDRESS before returning PLAN_CREATED or DECISION_RFC_CREATED)
- [Check]: [specific issue with evidence]
```

### Escalation (3/3 iterations, still failing)

```
## Spec Gate — ESCALATION REQUIRED (3/3 iterations exhausted)

### Remaining Blocking Issues
[List by check with evidence]
```

→ Do NOT question the user from this skill. Return blocking issues only. No suggestions, no softening, no collaborative rewrite advice. The planner decides how to revise or escalate.

## Anti-Patterns

| Anti-Pattern | Why Wrong |
|--------------|-----------|
| Skipping file path verification | Fabricated paths are the #1 plan failure mode |
| Treating SPEC_GATE_FAIL as advisory | The gate must block PLAN_CREATED / DECISION_RFC_CREATED |
| Skipping for "simple" plans | Read the skip criteria — only truly trivial plans qualify |
| Accepting SPEC_GATE_PASS without evidence | Each check needs cited proof, not "looks fine" or "seems reasonable" |
| Reporting suggestions instead of verdicts | This gate is an auditor, not a collaborator |
