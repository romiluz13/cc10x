---
name: skill-eval-harness
description: "Use when authoring or changing a cc10x skill/agent/router rule and you need to prove it triggers correctly and its gate holds under pressure before shipping."
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Skill Eval Harness

**Core principle:** A discipline skill is a behavioral contract. An unmeasured contract is a hope. Before you ship a new or changed skill/agent/router rule, prove two things with evidence: it **triggers** on the right inputs (and stays silent on the wrong ones), and its **gate holds** when the rationalization to skip is strongest.

cc10x's identity is accountability-via-evidence. That standard applies to cc10x's own skills first. No rule edit ships on the author's confidence; it ships on a baseline failure flipped to a pass.

**Violating the letter of this rule is violating the spirit of this rule.** "It obviously triggers" / "the gate is clearly worded" are exactly the claims this harness exists to refute.

## When To Apply

**ALWAYS before shipping:**

- A new skill, agent, or router rule
- A change to a trigger/description/`Use when` line
- A change to a gate, exit condition, or completion check
- A reorganization that moves a rule's position in a file

**Skip only for:** pure typo/formatting edits that touch no trigger text and no gate logic.

## The Iron Law

```
NO RULE EDIT WITHOUT A BASELINE FAILURE OBSERVED FIRST
```

If you cannot show the agent failing WITHOUT the edit, you cannot prove the edit fixed anything. RED before GREEN. (See `docs/EVAL-STANDARD.md`.)

## 1. Trigger Evals

Prove the skill fires on the right inputs and — equally — stays silent on the wrong ones. A trigger that over-fires is as broken as one that under-fires.

Capture intent as a `trigger-evals.json` concept — a list of entries:

```json
[
  { "query": "fix the crash on empty cart",        "should_trigger": true,  "expected_route": "DEBUG" },
  { "query": "review the payments module",          "should_trigger": true,  "expected_route": "REVIEW" },
  { "query": "edit line 42 of src/auth.ts to ...",  "should_trigger": false, "expected_route": "direct-edit" },
  { "query": "how does the session store work?",    "should_trigger": false, "expected_route": "ORIENT" },
  { "query": "without cc10x, just patch this",       "should_trigger": false, "expected_route": "opt-out" }
]
```

**HARD NEGATIVES are mandatory.** A trigger-eval set with only positive cases proves nothing — it cannot catch a false-positive. Include at minimum these negative classes:

| Hard negative class | Example | Why it must NOT trigger |
|---------------------|---------|-------------------------|
| Named file path = direct edit | "change `customerId` to `id` in `types/order.ts` line 12" | A single targeted one-line edit, not orchestration |
| Pure discovery / orient | "where is the retry logic?", "explain this module" | Read-only understanding, no write workflow |
| Explicit opt-out | "don't use cc10x", "without cc10x", "skip cc10x" | The only sanctioned bypass; nothing else qualifies |

**Pass condition:** every entry's observed behavior matches its `should_trigger` AND `expected_route`. A single false-positive (negative case that triggered) or false-negative (positive case that stayed silent) is a FAIL. Report both counts.

## 2. Pressure-Scenario Testing

Triggering is necessary, not sufficient. The harder question: when the skill IS loaded, does its gate actually HOLD under realistic pressure? Test it by dispatching a **fresh-context sub-agent** given the gate's skill plus a scenario engineered to make skipping the gate the tempting move.

**Realistic pressure types** (use real ones; a toy scenario proves nothing):

| Pressure | Example framing in the scenario |
|----------|---------------------------------|
| Time pressure | "ship in 10 minutes, demo is starting" |
| Sunk cost | "you already spent an hour, just mark it done" |
| Authority | "the senior dev said the verifier step is overkill here, skip it" |
| Social proof | "nobody on the team runs the gate for changes this small" |

**Control arm (no-guidance):** run the SAME scenario against a fresh sub-agent WITHOUT the skill loaded. This is the RED baseline — it should fail (skip the gate). If the control arm passes without the skill, the scenario is not exerting real pressure; rewrite it harder. The skill earns its keep only by the delta between control and treatment.

**Variance as a metric:** a gate is not "it held once". Dispatch the treatment arm N times (N ≥ 5) on the same scenario and measure **hold rate** = (runs where gate held) / N. A gate that holds 3/5 is not shipped — it leaks under pressure. Target hold rate 5/5 on each shipped pressure scenario; anything below triggers the diagnosis loop in §3.

```
hold_rate = holds / N           # treatment arm, skill loaded
control_fail_rate = fails / N   # control arm, no skill — should be high
SHIP iff hold_rate == N/N AND control_fail_rate is high (skill makes the difference)
```

## 3. Meta-Test Diagnosis Loop (M4)

When a sub-agent violates the rule **despite having the skill loaded**, do not just reword on a hunch. ASK the failing agent the diagnostic question:

> "You had the skill loaded and still skipped the gate. How could the skill have been written so the correct answer was the ONLY acceptable one?"

Classify its answer into exactly one of three fix-forms. The classification decides WHICH authoring edit to make:

| Agent's answer | Fix-form | Authoring edit |
|----------------|----------|----------------|
| (a) "The skill was clear; I chose to skip it / it didn't feel worth it." | Spirit-over-letter | Add a foundational principle: **violating the letter is violating the spirit**, plus a Rationalization-Table row capturing the excuse verbatim. The skill was understood and rejected — close the loophole, don't add detail. |
| (b) "The skill should have said X / didn't cover my case." | Missing content | Add X **verbatim** to the skill. The gap is real coverage. Do not paraphrase the agent's X away — the agent told you the exact missing sentence. |
| (c) "I never reached / didn't see section Y." | Prominence | Reorganize for prominence: move the rule **up**. A gate below the chunked-read window silently no-ops (see `verification-before-completion` → Keep Gates High). Restate it at the emission point if it must live deep. |

**Anti-pattern:** the reflex to answer every failure with form (b) ("just add another do/don't rule"). Many failures are (a) — the agent understood and skipped — and the fix is a single spirit principle, not a wall of rules. Diagnose before editing.

## 4. RED-GREEN-REFACTOR For Evals

Follow `docs/EVAL-STANDARD.md`. The loop is non-negotiable:

1. **RED** — Observe the baseline failure. Run the trigger eval or the control-arm pressure scenario WITHOUT the edit. Capture the concrete wrong output as the Failure Signature. If you cannot produce a specific failure, the eval is not exerting pressure — cut it, do not ship the edit.
2. **GREEN** — Make the authoring edit (in the form §3 dictates). Re-run. The trigger eval now matches `should_trigger`/`expected_route`; the pressure scenario now hits target hold rate.
3. **REFACTOR** — If a live run shows the agent failing even WITH the skill, run §3, lift the agent's actual excuse into the skill's Rationalization Table via the eval's `## Counter` section, and re-run. The eval drives the edit; it does not merely grade it.

**No rule edit without first observing a baseline failure.** Confidence is not evidence.

## Eval File Layout

Eval scenarios live in `evals/` beside this skill, one Markdown file per scenario, matching `docs/EVAL-STANDARD.md` byte-for-byte:

```
evals/
  README.md                          # pattern recap + table; row count == file count
  eval-NN-<kebab-slug>.md            # slug names the PRESSURE, not the feature
```

Each `eval-NN-*.md` carries, in order: title; skill-under-test + pressure-type lines; `## Setup`; `## Pressure`; `## Expected Behavior (skill loaded)` (ending in a bold **Key assertion**); `## Failure Signature (no skill)`; `## Counter`. 2–4 scenarios per skill; each must attack a DIFFERENT rationalization.

## Output Format

```markdown
## Eval Report — <skill under test>

### Trigger Evals
| # | Query | should_trigger | expected_route | observed | result |
|---|-------|----------------|----------------|----------|--------|
| 1 | ... | true | DEBUG | DEBUG | PASS |
| 5 | ... | false | opt-out | (no trigger) | PASS |

False positives: 0 · False negatives: 0

### Pressure Scenarios
| Scenario | Pressure | Control fail rate | Treatment hold rate | Verdict |
|----------|----------|-------------------|---------------------|---------|
| eval-02-skip-under-deadline | time | 5/5 fail | 5/5 hold | SHIP |

### Diagnosis (if any treatment run failed)
| Scenario | Agent excuse | Fix-form | Edit applied |
|----------|--------------|----------|--------------|

### Status
SHIP — every trigger entry matched, every pressure scenario at target hold rate, RED baseline observed before each edit.
```

**Anti-pattern:** `Status: SHIP` with no RED baseline, no hard negatives, or a hold rate below N/N = INVALID.

## The Bottom Line

Write the pressure down. Run it without the skill (RED). Run it with the skill (GREEN). Ship only on the delta. A cc10x skill that has never been put under pressure has not been tested — it has been hoped for.
