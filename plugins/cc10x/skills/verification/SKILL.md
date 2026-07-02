---
name: verification
description: |
  Verification discipline: task completion is not goal achievement. Covers the gate
  function, self-critique gate, validation levels, evidence array protocol, and
  goal-backward lens. Loaded by integration-verifier, component-builder, and bug-investigator.
allowed-tools: Read Bash Grep Glob
user-invocable: false
---

# Verification

**Task completion is not goal achievement.** Verify that the phase achieved its goal, not that prior agents said it did.

## Reference Files

- `references/live-production-testing.md` — live/production verification strategy

## The Gate Function

```
COMPLETION → TRUTH → PROOF
```

1. **Completion:** Did the agent finish its task? (contract says PASS)
2. **Truth:** Is the work actually correct? (independent verification)
3. **Proof:** Can you prove it with evidence? (exit codes, test output, screenshots)

A PASS without proof is a claim. A claim is not verification.

**Authoring Rule: Keep Gates High.** Every gate in this skill exists because a specific failure mode was observed. Removing a gate without understanding what it prevents reintroduces the failure. Gates are scar notes — they encode hard-won lessons.

## Self-Critique Gate (BEFORE Verification Commands)

Before running any test, audit your own work:

**Code Quality:**

- [ ] No TODO/FIXME/stubs in changed files
- [ ] No commented-out code
- [ ] No debug logging left in
- [ ] Error handling covers the failure modes the change introduces
- [ ] Types are correct (not `as any` or `as unknown`)

**Implementation Completeness:**

- [ ] Every acceptance criterion from the plan has corresponding code
- [ ] Every named scenario has a test
- [ ] Every error path in the plan has handling
- [ ] No silent failures (empty catches, discarded errors)
- [ ] Build succeeds, type-check passes

**Self-Critique Verdict:** If any check fails, fix it BEFORE running verification. Don't run tests you know will fail on code quality issues.

## Validation Levels

| Level | What | Exit Code | When |
| ------- | ------ | ----------- | ------ |
| **Deterministic** | Automated test | 0/1 | Always — the default |
| **Probabilistic** | Test with known flake rate | 0/1 (retry policy) | When deterministic impossible (timing, network) |
| **Manual** | Human verifies with checklist | n/a | When automation not worth the cost |
| **Live** | Production-like environment | 0/1 | When plan requires live proof |

Every verification must state its validation level. If manual, state the checklist. If deterministic, state the command + exit code. If live, state the harness command.

## Production-Like Live Proof

When the plan includes `### Live Verification Strategy` or a harness manifest:

- Run `python3 plugins/cc10x/tools/live_harness_runner.py --manifest <path> --mode proof`
- If stress required: also run `--mode stress`
- Do NOT silently substitute replay fixtures or unit tests for required live proof

**Flaky test handling:** re-run once. Pass on re-run → mark PASS with `flaky: true`. Fail both → FAIL. Never convert flaky pass into unconditional confidence.

## Evidence Array Protocol (MANDATORY for PASS)

```
EVIDENCE:
  scenarios:
    - "[name] | Given [state] | When [action] | [command] → exit [code] | expected=[expected] | actual=[actual]"
  regressions:
    - "[test] → exit [code]: [result]"
  edge_cases:
    - "[case]: [command] → exit [code]: [result]"
```

Every scenario needs non-empty Expected and Actual. Every scenario maps to exactly one EVIDENCE entry. SCENARIOS_PASSED must equal EVIDENCE.scenarios with exit 0 + Result=PASS.

## Goal-Backward Lens

Walk backward from the goal to verify it was achieved:

1. **What was the goal?** (re-read the plan's exit criteria)
2. **What would prove it?** (name the specific evidence)
3. **Do I have that evidence?** (run the verification)
4. **Does the evidence actually prove the goal?** (not "tests pass" but "the tests test the right thing")

**Forbidden language before proof:** "should pass", "looks good", "seems fine", "builder reported success", "the tests cover this" (without showing which test), "no regressions detected" (without listing what was tested).

## Common Failures

| Failure | What happens | Fix |
| --------- | ------------- | ----- |
| **False green** | Test passes without exercising the real code path | Test Honesty Gates (see integration-verifier) |
| **Scope skip** | "All tests pass" but untested scenarios exist | Goal-backward lens: name every scenario, verify each |
| **Stale evidence** | "Tests pass" but you didn't run them this session | Re-run. Evidence must be from THIS session. |
| **Claim without proof** | "It works" with no command/exit code | Evidence array is mandatory for PASS |
| **Environment escape** | Test fails with env signal (command not found, ECONNREFUSED) | Classify as ENVIRONMENT not code. Mark BLOCKED. |

## Auditor Posture

You are an independent auditor. A reviewer approval, green unit test, or builder claim is never sufficient by itself for PASS. If you cannot independently reproduce a claimed success, return FAIL.
