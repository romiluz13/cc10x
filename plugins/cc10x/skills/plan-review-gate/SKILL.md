---
name: plan-review-gate
description: "Use after saving a non-trivial plan or decision RFC when a fail-closed feasibility, completeness, and alignment review must block execution."
allowed-tools: Read Bash Grep Glob
user-invocable: false
---

# Spec Review Gate

**Core principle:** No execution plan or decision RFC reaches the user without surviving adversarial scrutiny. No leniency. "Close enough" is FAIL. A structurally neat but repo-wrong plan is FAIL.

**How it works:** This skill runs inline in the calling agent's context (no subagents). The calling LLM acts as an independent auditor, reads the saved artifact, and checks it against 3 criteria using Read/Grep/Glob. The value is fail-closed blocking and adversarial framing, not reviewer isolation — keep the auditor posture, but do not claim independence the gate doesn't have.

## When to Skip

**Skip when artifact is truly trivial:** Single-file fix, copy edit, or config tweak with <3 changes and no architecture choice → return `SPEC_GATE_PASS` immediately.

## The 3 Checks (Run in Sequence)

### Check 1: Feasibility — Can this be executed against the real codebase?

Run these verifications using Read/Grep/Glob:

| Criterion | How to verify | Blocking if |
|-----------|--------------|-------------|
| Artifact file exists on disk | `Glob(pattern="{plan_file_path}")` where plan_file_path is the path from the calling agent's context | Returns 0 matches |
| File paths exist | `Glob(pattern="{path}")` for every referenced file | Any path returns 0 matches and doesn't exist |
| Codebase reality check is present | Read artifact for `Codebase Reality Check` | Non-trivial plan omits repo-grounded verification of existing code |
| Dependency ordering | Read plan phases — do later phases depend on earlier ones only? | Circular or forward-reference dependencies |
| Technical approach matches codebase | Read 1-2 existing files in the affected area | Proposed patterns/libs differ from what codebase actually uses |
| No unstated infra assumptions | Read plan for external services, env vars, DBs | Plan silently assumes infra that doesn't exist |
| No invented or unverified file/module assumptions | Compare claimed touched surfaces to repo reality | Artifact presents guessed files/modules as verified facts |
| Plan mode fits the task | Read request + artifact: `direct`, `execution_plan`, or `decision_rfc` | Request changes ≥3 files or any contract/schema/auth surface while mode is `direct`; or request asks for a decision between alternatives and mode is not `decision_rfc` |
| Verification rigor fits risk | Check `verification_rigor` against the requested work | Critical-path work is missing `critical_path` rigor or claims proof it never defined |

**Critical-path work** = auth, payment, data-destructive operations, migrations, or work the user labeled critical.

### Check 2: Completeness — Does it cover the full request?

Read the user's original request and compare against the plan:

| Criterion | How to verify | Blocking if |
|-----------|--------------|-------------|
| All requirements mapped | List each sentence of the user request; cite the plan item covering it | Any user requirement has no corresponding plan item |
| Verification steps defined | For each plan item, find its named test, command, or checklist | Any change has no way to verify it worked |
| Edge cases addressed | For each input surface the plan touches, find its empty, invalid, and failure case | An input surface's empty, invalid, or failure case is neither named nor covered by an explicit "why none applies" statement |
| Cross-file integration | Trace each touched surface to the callers/importers the plan names | missing touched surfaces or integration points |
| Plan-vs-code gaps surfaced | Read the artifact for the mismatch table; spot-check one claim against the code | A non-trivial plan omits the concrete mismatch table or hides contradictions with current code |
| Assumption ledger is honest | Read each important claim for its classification tag | Important claims are not classified as `proven_by_code`, `inferred`, or `needs_user_confirmation` |
| Phase dependency map is present | Read each phase for its depends-on/enables statements | Non-trivial phases do not say what they depend on or what they enable |
| Durable Decisions present for multi-phase plans | For multi-phase plans, read for a foundational-decisions section | A multi-phase plan omits foundational decisions (routes, schema, models, auth, third-party boundaries) that all phases should reference |
| Decision-grade content present when needed | For `decision_rfc`, read for alternatives, drawbacks, and references sections | A `decision_rfc` is missing alternatives, drawbacks, or references |
| Critical-path spec present when needed | For `critical_path`, read for each of the five required sections | A `critical_path` artifact is missing behavior contract, edge-case catalog, provable properties, purity boundary, or verification strategy |

### Check 3: Scope & Alignment — Is it right-sized and faithful?

| Criterion | How to verify | Blocking if |
|-----------|--------------|-------------|
| Matches user request | Re-read the request; diff its ask against the plan's stated goal | Plan solves different problem or adds unrequested features |
| No scope creep | For each plan item, name the requirement it serves | Extra abstractions, refactoring, or features beyond the request |
| No under-scoping | List the request's direct implications; find each in the plan | Direct implications of the request are omitted |
| Execution order is real | Walk the phases in order; check each prerequisite exists in an earlier phase | wrong execution order or missing prerequisites |
| Complexity proportional | For each new file, abstraction, or dependency, cite the requirement row that needs it | The plan introduces a file, abstraction, or dependency that no requirement row maps to |
| Defaults are framed honestly | Check each recommended default is listed as still-open | A recommended default is treated as approved instead of still-open |
| Agreement fidelity holds | Read `Differences from agreement`; cross-check its claims against the body | `Differences from agreement` is missing, hidden, or contradicted by the body |
| Human layer matches execution contract | Compare each summary claim to the detailed plan body | Top summary or recommendation contradicts the detailed plan body |
| Hidden future work is explicit | Search the plan for "later", "follow-up", "eventually"; check each is explicit scope | Unscoped follow-on work is buried behind vague “later” language |
| Architecture contradictions are surfaced | Compare the plan's patterns to existing ADRs and code patterns | contradictions with existing architecture/patterns are hidden instead of made explicit |

## Workflow

```text
1. Check if trivial → skip if yes (return SPEC_GATE_PASS)
2. Run Check 1: Feasibility (use Read/Grep/Glob to verify file paths)
3. Run Check 2: Completeness (read request vs plan)
4. Run Check 3: Scope & Alignment (read request vs plan)
5. Collect findings:
   - Zero BLOCKING issues across all 3 checks → SPEC_GATE_PASS
   - Any BLOCKING issue → SPEC_GATE_FAIL with specifics
   - There is no "APPROVED WITH COMMENTS" — comments get ignored; FAILs get fixed
6. IF SPEC_GATE_FAIL and iteration < 3:
   a. Present blocking issues clearly
   b. Revise the plan to address them
   c. Re-run checks (increment iteration counter)
   <!-- CC10X-M9: iteration counter is in-context only — not persisted to memory. If compaction occurs mid-retry, counter resets to 0 and gate may retry more than 3 times. Acceptable for now (gate still converges). -->
7. IF SPEC_GATE_FAIL after 3 iterations → ESCALATION: emit a blocking review result and stop — three failed revisions means the premise is wrong, not the wording
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
| Accepting repo-agnostic summaries | A clean summary is worthless if the plan ignores real code constraints |
| Treating SPEC_GATE_FAIL as advisory | The gate must block PLAN_CREATED / DECISION_RFC_CREATED |
| Skipping for "simple" plans | Read the skip criteria — only truly trivial plans qualify |
| Accepting SPEC_GATE_PASS without evidence | Each check needs cited proof, not "looks fine" or "seems reasonable" |
| Ignoring plan-vs-code contradictions | Contradictions must be surfaced, not rewritten as assumptions |
| Reporting suggestions instead of verdicts | This gate is an auditor, not a collaborator |
