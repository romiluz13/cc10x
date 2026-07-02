---
name: debugging
description: |
  Debugging discipline: feedback loop FIRST, root cause before fix, blast radius after
  fix. Covers the 10-rung construction ladder, LSP-powered tracing, hypothesis quality
  criteria, and four-phase investigation. Loaded by bug-investigator.
allowed-tools: Read Edit Bash Grep Glob LSP
user-invocable: false
---

# Debugging

**Feedback Loop FIRST:** No hypothesis without a repro loop. No fix without root cause. No fix without blast radius scan.

## Reference Files

- `references/investigation-hygiene.md` — investigation discipline, evidence handling
- `references/root-cause-playbooks.md` — scenario-specific debugging playbooks

## Feedback Loop FIRST (Before Any Hypothesis)

A hypothesis without a repro loop is a guess. Before H1, build a fast, deterministic, agent-runnable signal that turns red on the bug.

### Construction Ladder (try in rank order, stop at first that works)

1. Failing automated test (unit/integration) — best: lives at a seam, reusable as RED
2. `curl`/HTTP request with asserted response
3. CLI snapshot diff (run command, diff stdout/stderr/exit)
4. Headless browser script (real DOM/runtime crash)
5. Trace replay (recorded request/log/event re-run)
6. Throwaway harness (tiny script calling the suspect function)
7. Property/fuzz check (when failing input is unknown)
8. `git bisect run` (regression with existing test)
9. Differential old-vs-new (last-good vs HEAD behavior diff)
10. Human-in-the-loop (LAST resort: scripted manual steps)

**Sharpen the loop:** sub-second beats sub-minute. Assert the exact failing fact, not a noisy superset. Same input → same red, no drift.

**Flaky bugs:** run in a tight loop (`for i in $(seq 1 N); do ...; done`), record hit rate (e.g. `3/50`), treat raising that rate as loop iteration.

### When You Genuinely Cannot Build a Loop

STOP. Do NOT advance to hypothesis. Return BLOCKED with:

- **What was tried:** each rung attempted and why it failed
- **Concrete ask:** the one thing that would unblock (env/credential access, captured artifact, permission for temporary instrumentation)

## LSP-Powered Root Cause Tracing

Use LSP to trace root causes through the codebase:

- **Go to Definition** — follow the call chain to where the value is actually set
- **Find References** — find all callers of a suspect function (blast radius)
- **Go to Type Definition** — check if the type allows the failing value
- **Hover** — check types and signatures at the failure site

Don't guess where a value comes from — trace it with LSP. Don't grep for a function name — use Find References to get every caller with type info.

## The Four Phases

### Phase 1: Root Cause Investigation

1. **Understand** — expected vs actual, when did it start?
2. **Git History** — `git log --oneline -20 -- <files>`, `git blame`, `git diff BASE..HEAD`
3. **LOG FIRST** — collect error logs, stack traces, run failing commands
4. **Feedback Loop** — build repro signal (construction ladder above). No loop → fail closed.
5. **Variant Scan** — identify which variant dimensions must keep working (locale, config, env, platform, data shape, concurrency)

### Phase 2: Pattern Analysis

1. **Read the code around the failure** — not just the failing line, the surrounding logic
2. **Check for recent changes** — `git diff` the files involved
3. **Look for similar patterns** — grep for the same anti-pattern elsewhere
4. **Identify the mechanism** — not "what's wrong" but "how does the wrong thing happen"

### Phase 3: Hypothesis and Testing

Form H1/H2/H3 with 0-100 confidence. Proceed to fix only when one reaches 80+.

**Hypothesis Quality Criteria:**

- States a specific mechanism ("X returns null because Y is not set when Z")
- Predicts a specific test outcome ("if I set Y, X returns the correct value")
- Is falsifiable ("if Y is already set, this hypothesis is wrong")
- Explains ALL observed symptoms, not just the primary one

**Hypothesis Confidence Scoring:**

| Score | Meaning |
| ------- | --------- |
| 90-100 | Verified: traced with LSP, reproduces the bug, fix resolves it |
| 80-89 | Strong: consistent with all evidence, mechanism is clear |
| 60-79 | Plausible: fits some evidence but gaps remain — investigate more |
| <60 | Speculative: do not act — gather more evidence |

**When to Restart Investigation:** If 3 hypotheses fail, you're pattern-matching, not investigating. Re-read the loop output. Re-trace with LSP. Consider you're looking at the wrong layer.

### Phase 4: Implementation

1. **RED** — failing regression test reproducing the bug (must fail before fix)
2. **GREEN** — minimal fix (smallest diff, no hardcoding)
3. **Blast Radius Scan** — search same file for identical anti-patterns, adjacent files for same signature
4. **Verify** — regression test passes + relevant suite passes
5. **Prevention** — recommend lint rule, test, type guard, or monitoring

## Scenario Playbooks

Read `references/root-cause-playbooks.md` for scenario-specific guidance:

- State machine bugs (dead states, missing transitions)
- Race conditions (timing-dependent failures)
- Data corruption (cascading from wrong input)
- Performance degradation (regression after change)
- Integration failures (contract mismatch between services)

## Debug Attempt Tracking

Track failed hypotheses: `[DEBUG-N]: {what was tried} → {result}`. After 3 failed hypotheses, set `NEEDS_EXTERNAL_RESEARCH: true`. After research files provided and still stuck, return BLOCKED.
