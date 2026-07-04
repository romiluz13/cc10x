# Parallel Patterns Audit: v11 → v12 Refactoring

**Commit analyzed:** `584049d` — "refactor: Phase 3 — merge agents, update all references"
**v11 reference:** `584049d~1` (pre-refactoring)
**v12 current:** `HEAD` (post-refactoring)

---

## Summary

| # | Pattern | v11 Status | v12 Status | Verdict |
|---|---------|------------|------------|---------|
| 1 | BUILD: code-reviewer + silent-failure-hunter parallel dispatch | Explicit parallel ("same message") | Merged into single code-reviewer (Pass 1b) | **LOST** |
| 2 | BUILD: re-review + re-hunt parallel dispatch | Two separate tasks, both blocked verifier | Merged into single re-review task (Pass 1b) | **LOST** |
| 3 | BUILD: router-owned merged findings summary | Explicit merge step after both complete | Removed (only one agent, nothing to merge) | **LOST** |
| 4 | Research: web-researcher + github-researcher parallel dispatch | Two separate agents, "in parallel with sibling" | Merged into single `cc10x:researcher` with mode flag; "Wait for both" language preserved | **PARTIALLY PRESERVED** |
| 5 | DEBUG: bug-investigator fan-out (opt-in, independence-gated) | Explicit fan-out with conflict-check | Unchanged — identical text | **PRESERVED** |

---

## Pattern 1: BUILD Parallel Review (code-reviewer + silent-failure-hunter)

### Status: LOST

### v11 Evidence (SKILL.md, §12 Chain Execution Loop, step 5)

```text
5. If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD:
   - mark both in_progress first
   - invoke them in the same message
   - If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter). Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
```

v11 also had two separate tasks in build-workflow.md:
- `phase:build-review` → `cc10x:code-reviewer`
- `phase:build-hunt` → `cc10x:silent-failure-hunter`

Both blocked by `builder_task_id`; verifier blocked by `[reviewer_task_id, hunter_task_id]`.

### v12 Evidence (SKILL.md, §12 Chain Execution Loop, step 5)

```text
5. Mark each task in_progress before invoking its agent. BUILD dispatches exactly ONE `code-reviewer` per review point — its single review covers correctness AND the Pass 1b silent-failure scan; never create a second reviewer task for the same phase.
   - If parallel invocation of multiple agents is needed but unavailable: fall back to sequential execution. Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
```

v12 build-workflow.md: only `phase:build-review` → `cc10x:code-reviewer` exists. No `build-hunt` phase. The verifier is blocked by `[reviewer_task_id]` only. The `build-hunt` phase value was removed from the metadata contract line.

### What was lost

- Genuine parallel execution of two independent read-only agents (reviewer + hunter) in the same message
- The `phase:build-hunt` task and its dispatch to `cc10x:silent-failure-hunter`
- The fallback-to-sequential logic was downgraded to a generic statement with no specific agents named
- The `silent-failure-hunter` agent was deleted (confirmed in git log)

### Impact

The code-reviewer now does a "Pass 1b: Silent Failure Scan" as an additional pass within its single review. This is sequential by construction — no parallelism is possible when one agent does both passes. The scan quality may also be lower since the reviewer's primary focus is correctness, not adversarial failure-hunting.

---

## Pattern 2: BUILD Re-Review + Re-Hunt Parallel Dispatch

### Status: LOST

### v11 Evidence (remediation-and-research.md, §11 Re-Review Loop)

v11 created TWO separate tasks after remediation:

Step 2 — re-review:
```text
TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  ...
  phase:re-review
  ...
  "Re-review the changes made by the completed remediation task."
}) -> rereview_task_id
```

Step 3 — re-hunt (BUILD only):
```text
TaskCreate({
  subject: "CC10X silent-failure-hunter: Re-hunt after REM-FIX",
  ...
  phase:re-hunt
  ...
  "Re-scan for silent failures after remediation."
}) -> rehunt_task_id
```

Step 5: `Block verifier on re-review and re-hunt as applicable.`
Step 7: `telemetry.loop_counts.re_hunt += 1 in BUILD`

The `phase:re-hunt` value existed in the metadata contract and dispatcher table (`re-hunt` → `cc10x:silent-failure-hunter`).

### v12 Evidence (remediation-and-research.md, §11 Re-Review Loop)

v12 creates ONE task:

Step 2 — re-review (merged):
```text
Create a re-review task (one task — the reviewer's single pass covers both the fix re-review and the silent-failure re-scan):

TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  ...
  phase:re-review
  ...
  "Re-review the changes made by the completed remediation task, including a silent-failure re-scan (Pass 1b) of the remediated surface."
}) -> rereview_task_id
```

- No re-hunt task creation
- Step 3 (was re-hunt) is now: `Reuse the pending verifier...`
- `telemetry.loop_counts.re_hunt` removed from telemetry counters
- `phase:re-hunt` removed from metadata contract and dispatcher table

### What was lost

- Parallel re-review + re-hunt after remediation (both could run simultaneously, both blocked the verifier)
- The `phase:re-hunt` task and its dispatch
- The `re_hunt` telemetry counter

---

## Pattern 3: Router-Owned Merged Findings Summary

### Status: LOST

### v11 Evidence (SKILL.md, §12 Chain Execution Loop, step 6)

```text
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff
   - apply workflow rules
```

### v12 Evidence (SKILL.md, §12 Chain Execution Loop, step 6)

```text
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - apply workflow rules
```

The "merged findings summary" line was removed entirely. This is a direct consequence of Pattern 1 being lost — with only one reviewer agent, there's nothing to merge.

### What was lost

- The router's explicit step to synthesize findings from two independent agents into a unified summary before verifier handoff
- This was a quality gate: the router owned the merge, preventing the verifier from having to reconcile two separate agent outputs

---

## Pattern 4: Research Dual-Dispatch (web-researcher + github-researcher)

### Status: PARTIALLY PRESERVED (intent preserved, mechanism degraded)

### v11 Evidence

**Agent files (deleted in v12):**

`plugins/cc10x/agents/web-researcher.md`:
```text
**Invoked by:** Router directly (in parallel with its sibling agent). Never invoked standalone.
```

`plugins/cc10x/agents/github-researcher.md`:
```text
**Invoked by:** Router directly (in parallel with its sibling agent). Never invoked standalone.
```

**Dispatcher table (v11 SKILL.md):**
```text
| `research-web` | `cc10x:web-researcher` |
| `research-github` | `cc10x:github-researcher` |
```

**Model-tier policy (v11 SKILL.md):**
```text
| `web-researcher`, `github-researcher` | standard | Retrieval + synthesis. |
```

**Research persistence (v11 remediation-and-research.md):**
```text
1. Wait for both research tasks in the round to finish.
```

Two SEPARATE agents, each with distinct tool sets (web-researcher had Bright Data; github-researcher had Octocode). Designed to be invoked "in parallel with its sibling."

### v12 Evidence

**Agent file (new, merged):**

`plugins/cc10x/agents/researcher.md`:
```text
**Invoked by:** Router directly, in parallel with its sibling if both modes are dispatched. Never invoked standalone.
**Mode:** Set by the router dispatch context — `web` or `github`. The mode determines which MCP accelerators are preferred.
```

**Dispatcher table (v12 SKILL.md):**
```text
| `research-web` | `cc10x:researcher` |
| `research-github` | `cc10x:researcher` |
```

Both phase kinds now dispatch to the SAME agent (`cc10x:researcher`).

**Research persistence (v12 remediation-and-research.md):**
```text
1. Wait for both research tasks in the round to finish.
```
(Identical to v11 — the "both" language was preserved.)

### What was preserved

- The `research-web` and `research-github` phase kinds still exist in the metadata contract
- The "Wait for both research tasks in the round to finish" language is still present
- The `results.research.web` and `results.research.github` artifact fields are still separate
- The researcher.md agent file still claims "in parallel with its sibling if both modes are dispatched"

### What was lost/degraded

- Two distinct agent definitions (different tools, different MCP accelerators, different system prompts) became one agent with a mode flag
- The web-researcher and github-researcher agent files were deleted
- Whether genuine parallelism still occurs depends on whether the router dispatches two `Agent()` calls in the same message — the dispatcher table now maps both to the same agent name, so the router must create two separate tasks with different `phase:` values (`research-web` vs `research-github`) and dispatch them in the same message
- The chain execution loop's step 5 in v12 no longer has explicit parallel dispatch language for research (it only mentions the generic "If parallel invocation of multiple agents is needed but unavailable")

### Assessment

This is **partially preserved**: the data model and phase kinds support parallel dispatch, and the merged researcher.md agent file still claims parallel sibling dispatch. However, the v12 chain execution loop lost the v11's explicit "invoke them in the same message" instruction (that was specific to code-reviewer + silent-failure-hunter). The research parallel pattern was never explicitly codified in the chain execution loop in either version — it was implicit in the "Wait for both" language and the agent file's "in parallel with sibling" declaration. Since both of those survive in v12, the research parallel pattern is **structurally intact but has weaker enforcement** than before.

---

## Pattern 5: DEBUG Fan-Out (bug-investigator independence-gated parallel dispatch)

### Status: PRESERVED

### v11 Evidence (debug-workflow.md)

```text
### DEBUG independence-test gate (opt-in fan-out)

Default to a SINGLE investigator. Fan-out is an opt-in optimization, gated on provable independence — when in doubt, serialize.

Only consider fanning out when the user reports many tests red across files AND the failures look like distinct root causes. Before fanning out, both halves of the INDEPENDENCE TEST must PASS:

1. **Separable understanding** — each problem is understandable and fixable without reading the others.
2. **Disjoint files** — group the failures by domain and list the files each group must touch.

When BOTH halves PASS, fan out one scoped `bug-investigator` per domain — each scoped to its own non-overlapping file set.

### DEBUG fan-in conflict-check

On return from a fan-out, BEFORE running the unified verifier, run a fan-in CONFLICT-CHECK — two WRITE agents that strayed past their scope will silently clobber each other:
```

### v12 Evidence (debug-workflow.md)

**Identical text.** No changes were made to the DEBUG fan-out pattern. The entire `### DEBUG independence-test gate (opt-in fan-out)` and `### DEBUG fan-in conflict-check` sections are byte-for-byte identical between v11 and v12.

### What was preserved

- The opt-in fan-out pattern (multiple bug-investigators dispatched in parallel for independent failures)
- The independence test gate (separable understanding + disjoint files)
- The fan-in conflict-check (pairwise file intersection before verifier)
- The single unified verifier over the full test suite

---

## Deleted Agents (git log)

```
584049d refactor: Phase 3 — merge agents, update all references
plugins/cc10x/agents/github-researcher.md          ← DELETED
plugins/cc10x/agents/silent-failure-hunter.md       ← DELETED
plugins/cc10x/agents/web-researcher.md              ← DELETED
```

Three agents were deleted in the v12 refactoring:
1. **`silent-failure-hunter.md`** — merged into `code-reviewer.md` as "Pass 1b: Silent Failure Scan"
2. **`web-researcher.md`** — merged into `researcher.md` as "web mode"
3. **`github-researcher.md`** — merged into `researcher.md` as "github mode"

One agent was created:
- **`researcher.md`** — new merged agent with `web`/`github` mode flag

---

## Other Parallel-Related Changes

### Previous Agent Findings Handoff (verifier scaffold)

**v11:**
```text
### Code Reviewer
**Verdict:** {Approve|Changes Requested}
**Critical Issues:**
{reviewer critical issues or "None"}

### Silent Failure Hunter
**Critical Issues:**
{hunter critical issues or "None / not in this workflow"}
```

**v12:**
```text
### Code Reviewer
**Verdict:** {Approve|Changes Requested}
**Critical Issues:**
{reviewer critical issues or "None"}

### Code Reviewer (Pass 1b: Silent Failure Scan)
**Critical Issues:**
{silent failure findings or "None / not in this workflow"}
```

The verifier scaffold was updated to reflect that the same agent now produces both findings. The "Silent Failure Hunter" section header became "Code Reviewer (Pass 1b: Silent Failure Scan)."

### Rule 2 (remediation table)

**v11:** `| 2 | Reviewer approved but hunter found issues | Ask whether to remediate or proceed. |`
**v12:** `| 2 | Reviewer verdict is Approve overall but its Pass 1b silent-failure scan reports HIGH issues | Ask whether to remediate or proceed. |`

### 1a-SCOPE description

**v11:** `BUILD parallel phase has CRITICAL + HIGH issues`
**v12:** `BUILD parallel phase has CRITICAL + HIGH issues` (unchanged in the table, but the detail text changed from "the parallel review phase shows both" to "the review phase shows both")

### General parallel-safety rule (hard rules section)

**v11:**
```text
Only parallelize agents whose file-write surfaces do not overlap. Reviewer and hunter are read-only and safe to parallelize. Two write agents on overlapping files must be serialized.
```

**v12:**
```text
Only parallelize agents whose file-write surfaces do not overlap. Read-only agents are safe to parallelize with each other. Two write agents on overlapping files must be serialized.
```

The specific "Reviewer and hunter are read-only and safe to parallelize" was generalized to "Read-only agents are safe to parallelize with each other." The parallel-safety rule itself is preserved but the specific example of reviewer+hunter was removed.

---

## Conclusion

Three parallel patterns were **LOST** in the v12 refactoring, all related to the silent-failure-hunter merger:

1. **BUILD review+hunt parallel dispatch** — the explicit "invoke them in the same message" instruction for code-reviewer + silent-failure-hunter
2. **BUILD re-review+re-hunt parallel dispatch** — the separate re-hunt task after remediation
3. **Router-owned merged findings summary** — the explicit merge step before verifier handoff

One pattern was **PARTIALLY PRESERVED**:

4. **Research dual-dispatch** — the data model and "wait for both" language survive, and the merged researcher.md still claims parallel sibling dispatch, but the enforcement is weaker (no explicit "same message" instruction for research in the chain execution loop in either version)

One pattern was **PRESERVED** unchanged:

5. **DEBUG fan-out** — the opt-in independence-gated parallel bug-investigator pattern with conflict-check is byte-for-byte identical