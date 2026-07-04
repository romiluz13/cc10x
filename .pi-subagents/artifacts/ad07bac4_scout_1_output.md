# v12.1 Current Review State — Deep Analysis

## Executive Summary

The silent-failure-hunter has been merged into the code-reviewer agent as **Pass 1b**, an inline sequential scan step. The router dispatches exactly ONE `code-reviewer` per review point — no parallel reviewer+hunter dispatch exists anywhere in the workflow definitions. The reference file `silent-failure-red-flags.md` was preserved and is actively referenced by Pass 1b.

However, **one critical stale reference** remains in `skills/code-review/SKILL.md`, which still describes the old parallel "Two Isolated Assessments + WEAVE" pattern that no longer matches the actual single-reviewer dispatch. Additionally, **legacy `hunter` keys** persist in the workflow artifact skeleton and policy doc (documented as LEGACY but still structurally present).

---

## 1. code-reviewer.md — Current Merged Agent

### Pass Inventory (Process section, numbered steps 0–10)

| Step | Name | Purpose |
| ------ | ------ | --------- |
| 0 | Verdict Pre-Decision | Decide verdict BEFORE writing final response |
| 1 | Git Context | `git log`, `git blame` |
| 2 | Verify Functionality | Run tests if available |
| 3 | **Pass 1: Security** | Auth, input validation, secrets, injection, OWASP |
| 4 | **Pass 1b: Silent Failure Scan** | The merged hunter — see below |
| 5 | **Pass 2: Performance** | N+1, hot loops, memory leaks, caching |
| 6 | **Pass 3: Quality** | Complexity, naming, error handling, duplication, types |
| 7 | **Pass 4: Friction Scan** | Architectural friction, fragmentation, coupling |
| 8 | **Pass 5: Plan Validity** | Flag PLAN_DEFECT (wrong plan, not wrong code) |
| 9 | **Pass 6: Spec Compliance** | MISSING/EXTRA/MISUNDERSTOOD divergence from plan |
| 10 | Output Memory Notes | Learnings for router persistence |

### Pass 1b Location and Content (Step 4, line 96)

> **Pass 1b: Silent Failure Scan** — Zero tolerance for silent failures. Search for: try, catch, except, .catch(, throw, error. Check for empty catches, log-only handlers, generic error messages, discarded errors, silent short-circuits. Apply the red-flags table from `references/silent-failure-red-flags.md`. Classify severity: CRITICAL (data loss/security/silent data corruption), HIGH (wrong behavior user notices), MEDIUM (suboptimal but functional), LOW (code smell). This pass replaces the former standalone silent-failure-hunter agent.

**Key observations:**

- Pass 1b is an **inline instruction within the same agent context** — it runs sequentially after Pass 1 (Security) and before Pass 2 (Performance).
- It explicitly states "This pass replaces the former standalone silent-failure-hunter agent."
- It references `references/silent-failure-red-flags.md` (the preserved reference file).
- The agent's frontmatter `skills:` list includes `cc10x:code-review` (which itself contains the stale parallel section — see §3 below).
- The agent's Core description (line 17) says: "Adversarial multi-dimensional review including silent-failure hunting."

### What Was Lost from v11 (Standalone Hunter)

The standalone silent-failure-hunter agent (now deleted) was a **separate subagent dispatch** with its own fresh context. The merge into an inline Pass 1b sacrificed:

1. **Context isolation**: The hunter ran in a fresh subagent context, uncontaminated by the correctness reviewer's anchoring. In the merged form, the same agent that just reviewed correctness now also scans for silent failures — cognitive anchoring risk (the agent may subconsciously skip error-handling sites it already deemed "correct" in Pass 1/2).

2. **Independent attention budget**: The standalone hunter had 100% of its token budget dedicated to silent-failure patterns. Pass 1b is one of 8+ passes in a single agent — it competes for attention with security, performance, quality, friction, plan validity, and spec compliance. Deep silent-failure hunting requires sustained focus on error paths; a checklist item in a multi-pass flow gets shallower treatment.

3. **WEAVE reconciliation**: The old pattern (still documented in `code-review/SKILL.md`) had Assessment A (correctness) and Assessment B (silent failure) run independently, then a WEAVE step reconciled disagreements. This cross-check is gone — there's no second independent opinion to catch what the first pass missed.

4. **Parallel execution latency benefit**: The old parallel dispatch (if it was actually used) meant the hunter's scan happened concurrently with the reviewer's, reducing wall-clock time. The merged sequential form adds the scan to the reviewer's turn.

5. **Separate contract output**: The hunter had its own contract/verdict. Now silent-failure findings are folded into the reviewer's single output. The router still passes them separately to the verifier (see §3), but they originate from one agent, not two.

**What was preserved:**

- The red-flags reference table (`silent-failure-red-flags.md`)
- Severity classification (CRITICAL/HIGH/MEDIUM/LOW)
- The search patterns (try, catch, except, .catch(, throw, error)
- Contract override: "An APPROVE whose Pass 1b silent-failure scan states zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification" (artifact policy)

---

## 2. silent-failure-red-flags.md — Preserved Reference

**Location:** `plugins/cc10x/agents/references/silent-failure-red-flags.md`

**Content:** Three tables:

1. **Core Red Flags** (6 patterns): empty catch, log-only catch, generic error message, `|| defaultValue` masking, `?.` chains without logging, retry without notification.
2. **Language-Specific Red Flags** (7 languages): Python (bare except, logging.exception without re-raise), Go (discarded error, `return nil` on error), Java (printStackTrace only), Rust (.unwrap in non-test), Shell (missing set -e), plus the 6 core patterns.
3. **Severity Classification** (4-tier decision tree): DATA LOSS/SECURITY → CRITICAL, USER sees broken behavior → HIGH, UX degraded → MEDIUM, style only → LOW.

**Status:** Intact, actively referenced by Pass 1b in code-reviewer.md. No changes needed.

---

## 3. cc10x-router SKILL.md — Router Dispatch

### All Review-Related Mentions

| Line | Context | Content |
| ------ | --------- | --------- |
| 35 | Intent Routing §1 | "everything else, and all planned work, runs the full builder → reviewer (correctness + Pass 1b silent-failure scan in ONE review) → verifier → doc-sync → memory chain" |
| 309 | Dispatcher table §7 | `build-review`, `debug-review`, `review-audit`, `re-review` → `cc10x:code-reviewer` (one review covers correctness AND the Pass 1b silent-failure scan) |
| 424–429 | Previous Agent Findings handoff §7 | Separate sub-section for "Code Reviewer (Pass 1b: Silent Failure Scan)" with `{silent failure findings or "None / not in this workflow"}`. "DEBUG skips Pass 1b findings." |
| 577 | Chain Execution §12 step 5 | "BUILD dispatches exactly ONE `code-reviewer` per review point — its single review covers correctness AND the Pass 1b silent-failure scan; never create a second reviewer task for the same phase." |
| 650 | Verifier findings handoff §12 | "Read `results.reviewer` from the workflow artifact (it includes the Pass 1b silent-failure findings)." |

### How the Router Currently Dispatches Review

**Single-agent, sequential.** The router creates exactly ONE `code-reviewer` task per review point. That one agent runs all passes (1 through 6, including 1b) in sequence within a single subagent context. There is no parallel dispatch of a separate hunter. The router explicitly forbids creating a second reviewer task.

The verifier handoff still structurally separates Pass 1b findings into their own sub-section under `## Previous Agent Findings`, but both the correctness findings and the silent-failure findings come from the same single agent invocation.

### Parallel Dispatch?

**No.** The only mention of parallelism in the router is the general rule (§14): "Only parallelize agents whose file-write surfaces do not overlap. Read-only agents are safe to parallelize with each other." But the BUILD task graph (build-workflow.md) creates the reviewer as a single sequential task blocked by the builder, with the verifier blocked by the reviewer. No parallel reviewer+hunter pair is ever created.

---

## 4. build-workflow.md — Review Wiring

### Full Task Graph (standard scope)

```
component-builder (phase:build-implement)
    ↓ blockedBy
code-reviewer (phase:build-review) — single review covers correctness, security, silent failures (Pass 1b), edge cases
    ↓ blockedBy
integration-verifier (phase:build-verify)
    ↓ blockedBy
doc-syncer (phase:build-doc-sync)
    ↓ blockedBy
Memory Update (phase:memory-finalize)
```

**Trivial scope** (`build_scope=trivial`): builder → verifier → memory. **No code-reviewer at all** — the verifier "folds a brief review/edge-case pass into its report." This means **trivial builds get no Pass 1b silent-failure scan** — a potential gap.

### Parallel Dispatch?

**No.** The graph is strictly sequential: builder → reviewer → verifier → doc-sync → memory. Each task is blocked by the previous one. The reviewer task description explicitly says: "Your single review covers correctness, security, silent failures (Pass 1b), and edge cases adjacent to the phase."

### Escalation

If the builder reports `SCOPE_INCREASES` on a trivial build, the router promotes to the full graph by adding the code-reviewer and doc-syncer tasks. This is the only path from trivial to full.

---

## 5. review-workflow.md — Standalone Review

### Task Graph

```
code-reviewer (phase:review-audit) — "Run a scoped code review."
    ↓ blockedBy
Memory Update (phase:memory-finalize)
```

**Single reviewer, no parallel dispatch.** The REVIEW workflow is advisory-only, never creates REM-FIX or implementation tasks. If the verdict is CHANGES_REQUESTED, the router may offer to start a BUILD workflow.

The reviewer task description is minimal: "Run a scoped code review." It does not explicitly mention Pass 1b, but the code-reviewer agent itself always runs Pass 1b as part of its process.

---

## 6. planner.md — Parallel Review Awareness

**None.** The planner agent file contains zero mentions of "parallel", "review", "hunter", "silent-failure", or "Pass 1b". The planner is focused on creating execution plans and decision RFCs. It does not know or care about how review is dispatched — that's the router's concern.

---

## 7. All Other Agents — Hunter/Silent-Failure/Parallel Mentions

### integration-verifier.md (line 37)

> Your prompt includes findings from code-reviewer (including Pass 1b silent failure scan) under `## Previous Agent Findings`. Review before starting.

**Status:** Correct and consistent. The verifier expects Pass 1b findings in its scaffold. This is the consumption side of the merged pattern.

### bug-investigator.md, component-builder.md, doc-syncer.md, plan-gap-reviewer.md, researcher.md

**Zero mentions** of hunter, silent-failure, parallel review, or Pass 1b. Clean.

---

## 8. Stale / Broken References to the Old Hunter Pattern

### 🔴 CRITICAL: `skills/code-review/SKILL.md` — "Two Isolated Assessments + WEAVE" (lines 56–62)

```markdown
### Two Isolated Assessments + WEAVE

When reviewer + Pass 1b (silent failure scan) run in parallel:

- **Assessment A** (reviewer): correctness, performance, spec compliance. Forms opinion WITHOUT seeing B's scan.
- **Assessment B** (Pass 1b): silent failure scan using red-flags table. Does NOT see A's findings.
- **WEAVE reconciliation:** after both commit. Where both agree → high confidence. Where B caught what A missed → keep. Where B is false positive → drop with reason.
```

**This is completely stale.** It describes a parallel two-agent pattern that no longer exists:

- The router explicitly dispatches ONE code-reviewer, not two agents.
- There is no "Assessment A" and "Assessment B" running in isolation.
- There is no WEAVE reconciliation step.
- The code-reviewer agent's own process (Pass 1b at step 4) runs the silent-failure scan inline, sequentially, in the same context.

**Impact:** The `cc10x:code-review` skill is listed in the code-reviewer agent's frontmatter `skills:` list. When the agent loads this skill, it will read instructions describing a parallel WEAVE pattern that contradicts its own inline Pass 1b process. This is a direct contradiction within the system. An agent following the skill's guidance would attempt to split into two assessments and weave them — but it's a single agent with no second assessment to weave with.

**Fix needed:** Replace the "Two Isolated Assessments + WEAVE" section with guidance for the inline sequential Pass 1b pattern, matching the code-reviewer agent's actual process.

### 🟡 LEGACY (Documented): `workflow-artifact.skeleton.json` — `hunter` keys

Three legacy `hunter` keys remain in the skeleton JSON:

- Line 55: `"hunter": null` (in `results`)
- Line 69: `"hunter": []` (in `evidence`)
- Line 80: `"hunter": 0` (in `telemetry.agent_wall_clock_seconds`)
- Line 86: `"re_hunt": 0` (in `telemetry.loop_counts`)

**Status:** These are documented as LEGACY in the artifact policy doc:

- `evidence.hunter` → "LEGACY — the standalone hunter is retired into the reviewer's Pass 1b; key kept for pre-consolidation artifacts, stays empty in new workflows"
- `telemetry.agent_wall_clock_seconds.hunter` → "LEGACY — stays 0 in new workflows"
- `telemetry.loop_counts.re_hunt` → "LEGACY — stays 0 in new workflows; silent-failure re-scan is part of `re_review`"

**Impact:** Low. These are explicitly marked LEGACY and the policy says they stay empty/0 in new workflows. They exist for backward compatibility with pre-consolidation artifacts. Not broken, but technically dead keys.

### 🟡 LOW: `workflow-artifact-and-hook-policy.md` — `hunter` in contract overrides context

Line 280 mentions Pass 1b in the contract override table, which is correct (not stale). The `hunter` key references in the schema section (lines 87, 109, 114) are the same LEGACY documentation as above.

---

## 9. Summary: What Exists NOW vs What Was Lost

### What Exists Now (v12.1)

| Component | State | Location |
| ----------- | ------- | ---------- |
| Pass 1b (Silent Failure Scan) | ✅ Inline step 4 in code-reviewer | `agents/code-reviewer.md:96` |
| Red-flags reference table | ✅ Preserved and actively referenced | `agents/references/silent-failure-red-flags.md` |
| Router dispatch (single reviewer) | ✅ One code-reviewer per review point | `SKILL.md:309,577` |
| Verifier handoff (Pass 1b findings) | ✅ Separate sub-section in scaffold | `SKILL.md:424–429` |
| Contract override (zero-scan fallback) | ✅ Enforces scan scope evidence | `workflow-artifact-and-hook-policy.md:280` |
| Remediation routing (Pass 1b HIGH issues) | ✅ Row 2 in remediation table | `remediation-and-research.md:44` |
| Re-review with silent-failure re-scan | ✅ Single re-review task covers both | `remediation-and-research.md:288–293` |
| Legacy `hunter` keys in skeleton | 🟡 LEGACY, documented | `workflow-artifact.skeleton.json:55,69,80,86` |

### What Was Lost from v11

| Lost Capability | Impact | Mitigation |
| ----------------- | -------- | ------------ |
| Context isolation (fresh subagent for silent-failure) | HIGH — anchoring risk; reviewer may skip error sites it already judged "correct" | None in current design |
| Independent attention budget (100% tokens on silent failures) | MEDIUM — Pass 1b is 1 of 8+ passes, gets shallower treatment | None |
| WEAVE reconciliation (cross-check between two independent assessments) | MEDIUM — no second opinion to catch misses | None |
| Parallel execution (concurrent scan) | LOW — sequential adds latency but not correctness risk | None |
| Separate contract/verdict for hunter | LOW — findings folded into reviewer output | Router still separates them in verifier handoff |

### Broken/Stale References

| File | Issue | Severity |
|------|-------|----------|
| `skills/code-review/SKILL.md:56–62` | "Two Isolated Assessments + WEAVE" describes parallel pattern that no longer exists — contradicts single-reviewer dispatch | 🔴 CRITICAL — directly contradicts current architecture, loaded by code-reviewer agent |
| `workflow-artifact.skeleton.json` | Legacy `hunter`/`re_hunt` keys | 🟡 LOW — documented as LEGACY, harmless |

---

## 10. Trivial Build Gap

A notable design consequence of the merge: **trivial builds (`build_scope=trivial`) get no code-reviewer and therefore no Pass 1b silent-failure scan.** The reduced task graph is builder → verifier → memory, with the verifier "folding a brief review/edge-case pass." The verifier's own checklist (`skills/verification/SKILL.md:50`) includes "No silent failures (empty catches, discarded errors)" but this is a single checklist item, not a dedicated scan with the red-flags table. If the builder escalates (reports `SCOPE_INCREASES`), the full graph with code-reviewer is added — but if the builder doesn't escalate, the silent-failure scan is skipped entirely.