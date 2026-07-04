# Parallel Review Restoration Plan

## Executive Summary

The v12.1 refactoring merged `silent-failure-hunter` into `code-reviewer` as "Pass 1b" to reduce agent count from 10 to 8. This was a mistake: it lost genuine parallelism, context isolation, the router's merge orchestration pattern, and introduced anchoring bias. This plan restores the standalone hunter agent and all parallel dispatch infrastructure while preserving every v12.1 improvement (effort frontmatter, agent-common skill, stress test fixes, model-tier honesty, etc.).

**Agent count after restoration: 8 → 9**

---

## Phase 1: Create the Restored Hunter Agent

### Step 1.1 — Create `plugins/cc10x/agents/silent-failure-hunter.md`

**Action:** Create a new file with the following content. This is the v11 hunter restored with v12 conventions.

**Frontmatter (v12 conventions):**

```yaml
---
name: silent-failure-hunter
description: "Internal agent. Use cc10x-router for all development tasks."
model: inherit
color: red
effort: high
tools: Read, Bash, Grep, Glob, Skill, LSP, WebFetch
skills:
  - cc10x:agent-common
  - cc10x:code-review
---
```

**Key differences from v11 frontmatter:**

- Added `effort: high` (v12 convention)
- Changed `skills` from `cc10x:code-review-patterns` to `cc10x:agent-common` + `cc10x:code-review` (v12 skill names)
- Removed `cc10x:verification-before-completion` (the hunter doesn't do verification — it detects)

**Agent body — restore from v11 with these adaptations:**

1. **Core/Posture** — verbatim from v11:
   - "Core: Zero tolerance for silent failures. Find empty catches, log-only handlers, generic errors."
   - "Posture: Assume errors are present until evidence proves otherwise. A neutral scan produces neutral results. Your job is to find problems, not to confirm cleanliness."

2. **Memory First** — same as code-reviewer's pattern (read patterns.md + progress.md, do NOT read activeContext.md for anti-anchoring)

3. **Mode: READ-ONLY** — no Edit tool, no self-healing, no TaskUpdate

4. **No self-healing (by design)** — verbatim from v11:
   - "Unlike code-reviewer, this agent does NOT create its own REM-FIX tasks. It reports only. The router handles all remediation."
   - "Do NOT call TaskUpdate(status: completed) — this agent does not have that tool."

5. **Process (single pass, 9 steps)** — verbatim from v11:
   - Step 0: Output contract envelope + verdict heading FIRST
   - Step 1: Find — Search for try, catch, except, .catch(, throw, error
   - Step 2: Audit each — Is error logged? Does user get feedback? Is catch specific?
   - Step 3: Rate severity — CRITICAL/HIGH/MEDIUM/LOW
   - Step 4: Report CRITICAL immediately
   - Step 5: Document HIGH and MEDIUM
   - Step 6: Prevention recommendations
   - Step 7: Output Memory Notes
   - Step 8: Coverage truthfulness — Never claim CLEAN unless scanned scope is stated
   - Step 9: Zero-Results Suspicion Gate — Verify ≥3 concrete sites inspected or flag advisory

6. **Output contract:**

   ```
   CONTRACT {"s":"CLEAN","b":false,"cr":0}
   ## Error Handling Audit: [CLEAN/ISSUES_FOUND]
   ```

   The `s` field is `CLEAN` or `ISSUES_FOUND` — distinct from the code-reviewer's `APPROVE`/`CHANGES_REQUESTED`.

7. **Scoping heuristic** — verbatim from v11 (scope to changed files in the current phase, same diff range as code-reviewer)

8. **Red-flags reference:** `references/silent-failure-red-flags.md` — already exists, no changes needed

9. **SINGLE FINAL RESPONSE RULE** — same as code-reviewer (router only sees the last response turn)

**File path:** `plugins/cc10x/agents/silent-failure-hunter.md` (NEW)

---

## Phase 2: Remove Pass 1b from Code Reviewer

### Step 2.1 — Edit `plugins/cc10x/agents/code-reviewer.md`

**Change 1:** Remove "including silent-failure hunting" from Core description (line 17)

**OLD:**

```
**Core:** Adversarial multi-dimensional review including silent-failure hunting. Only report issues with confidence ≥80.
```

**NEW:**

```
**Core:** Adversarial multi-dimensional review. Only report issues with confidence ≥80.
```

**Change 2:** Remove Pass 1b step entirely (step 4, the "Pass 1b: Silent Failure Scan" block)

**OLD (step 4):**

```
4. **Pass 1b: Silent Failure Scan** — Zero tolerance for silent failures. Search for: try, catch, except, .catch(, throw, error. Check for empty catches, log-only handlers, generic error messages, discarded errors, silent short-circuits. Apply the red-flags table from `references/silent-failure-red-flags.md`. Classify severity: CRITICAL (data loss/security/silent data corruption), HIGH (wrong behavior user notices), MEDIUM (suboptimal but functional), LOW (code smell). This pass replaces the former standalone silent-failure-hunter agent.
```

**NEW:** Remove entirely. Renumber steps 5–10 to 4–9.

**Change 3:** Restore the `REMEDIATION_SCOPE_REQUESTED: N/A` instruction to explicitly reference the parallel merge (in the "Router-Owned Remediation" section)

**OLD:**

```
- BUILD review: request `REMEDIATION_SCOPE_REQUESTED: N/A` so the router can decide `CRITICAL_ONLY` vs `ALL_ISSUES` after combining parallel findings.
```

**NEW:**

```
- BUILD review: request `REMEDIATION_SCOPE_REQUESTED: N/A` so the router can decide `CRITICAL_ONLY` vs `ALL_ISSUES` after combining your findings with the silent-failure-hunter's parallel findings.
```

**Change 4:** Remove `cc10x:codebase-hygiene` from skills if it was added for Pass 1b — check if it's still needed for other passes. (It likely is — keep it.)

**File path:** `plugins/cc10x/agents/code-reviewer.md`

---

## Phase 3: Restore Router Parallel Dispatch

### Step 3.1 — Routing table (§1, line 27)

**OLD:**

```
| 5 | DEFAULT | Everything else | BUILD | component-builder -> code-reviewer -> integration-verifier |
```

**NEW:**

```
| 5 | DEFAULT | Everything else | BUILD | component-builder -> [code-reviewer || silent-failure-hunter] -> integration-verifier |
```

### Step 3.2 — Intent routing rules (line ~37)

**OLD:**

```
- BUILD uses a complexity gradient (see `references/build-workflow.md`): trivial scope (1-2 files, single change, one testable outcome, no cross-module wiring) runs a reduced builder → verifier → memory graph; everything else, and all planned work, runs the full builder → reviewer (correctness + Pass 1b silent-failure scan in ONE review) → verifier → doc-sync → memory chain.
```

**NEW:**

```
- BUILD uses a complexity gradient (see `references/build-workflow.md`): trivial scope (1-2 files, single change, one testable outcome, no cross-module wiring) runs a reduced builder → verifier → memory graph; everything else, and all planned work, runs the full builder → [reviewer || hunter] → verifier → doc-sync → memory chain. The reviewer and hunter run in parallel (two read-only agents in the same message) and the router merges their findings before verifier handoff.
```

### Step 3.3 — Metadata contract (§2, line 114)

**OLD:**

```
phase:{build|build-implement|build-review|build-verify|build-doc-sync|build-finish|debug|debug-investigate|debug-review|debug-verify|review|review-audit|plan|plan-create|plan-review-gap-1|plan-review-gap-2|memory-finalize|re-review|re-verify|re-plan|research-web|research-github}
```

**NEW:** Add `build-hunt` and `re-hunt`:

```
phase:{build|build-implement|build-review|build-hunt|build-verify|build-doc-sync|build-finish|debug|debug-investigate|debug-review|debug-verify|review|review-audit|plan|plan-create|plan-review-gap-1|plan-review-gap-2|memory-finalize|re-review|re-hunt|re-verify|re-plan|research-web|research-github}
```

### Step 3.4 — Dispatcher table (§7, line 309)

**OLD:**

```
| `build-review`, `debug-review`, `review-audit`, `re-review` | `cc10x:code-reviewer` (one review covers correctness AND the Pass 1b silent-failure scan) |
```

**NEW:**

```
| `build-review`, `debug-review`, `review-audit`, `re-review` | `cc10x:code-reviewer` |
| `build-hunt`, `re-hunt` | `cc10x:silent-failure-hunter` |
```

### Step 3.5 — Chain Execution Loop §12 step 5 (line 577)

**OLD:**

```
5. Mark each task in_progress before invoking its agent. BUILD dispatches exactly ONE `code-reviewer` per review point — its single review covers correctness AND the Pass 1b silent-failure scan; never create a second reviewer task for the same phase.
   - If parallel invocation of multiple agents is needed but unavailable: fall back to sequential execution. Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
```

**NEW:**

```
5. Mark each task in_progress before invoking its agent. If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD: mark both in_progress first, invoke them in the same message. They are read-only and safe to parallelize.
   - If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter). Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
```

### Step 3.6 — Chain Execution Loop §12 step 6 (line 579) — Restore merge logic

**OLD:**

```
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - apply workflow rules
```

**NEW:**

```
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff
   - apply workflow rules
```

### Step 3.7 — Hard Rules §14 — Restore parallel-safety example (line ~718)

**OLD:**

```
- Only parallelize agents whose file-write surfaces do not overlap. Read-only agents are safe to parallelize with each other. Two write agents on overlapping files must be serialized. [EASY TO MISS: Each parallel agent must have a distinct phase value and unique task description. Identical prompts cause agents to duplicate work or silently clobber each other's output.]
```

**NEW:**

```
- Only parallelize agents whose file-write surfaces do not overlap. Reviewer and hunter are read-only and safe to parallelize. Two write agents on overlapping files must be serialized. [EASY TO MISS: Each parallel agent must have a distinct phase value and unique task description. Identical prompts cause agents to duplicate work or silently clobber each other's output.]
```

### Step 3.8 — Verifier findings handoff (line ~650)

**OLD:**

```
### Verifier findings handoff

Before invoking `integration-verifier` in BUILD:

- Read `results.reviewer` from the workflow artifact (it includes the Pass 1b silent-failure findings).
- Build `## Previous Agent Findings` exactly in the format verifier expects.
- Never invoke verifier without that section when a review already ran.
```

**NEW:**

```
### Verifier findings handoff

Before invoking `integration-verifier` in BUILD:

- Read `results.reviewer` and `results.hunter` from the workflow artifact.
- Build `## Previous Agent Findings` exactly in the format verifier expects:
  ```

## Previous Agent Findings

### Code Reviewer

  **Verdict:** {Approve|Changes Requested}
  **Critical Issues:**
  {reviewer critical issues or "None"}

### Silent Failure Hunter

  **Critical Issues:**
  {hunter critical issues or "None / not in this workflow"}

  ```
- Never invoke verifier without that section when review/hunt already ran.
```

**File path:** `plugins/cc10x/skills/cc10x-router/SKILL.md`

---

## Phase 4: Restore Build Workflow Task DAG

### Step 4.1 — Edit `plugins/cc10x/skills/cc10x-router/references/build-workflow.md`

**Change 1:** Full task graph — add the hunter task and change verifier to be blocked by both

**OLD (full task graph section):**

```text
TaskCreate({
  subject: "CC10X code-reviewer: Review implementation",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-review\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Review current phase quality\n\nReview only the files and scope of the current phase. Your single review covers correctness, security, silent failures (Pass 1b), and edge cases adjacent to the phase.",
  activeForm: "Reviewing code"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X integration-verifier: Verify integration",
  ...
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id] })
```

**NEW:**

```text
TaskCreate({
  subject: "CC10X code-reviewer: Review implementation",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-review\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Review current phase quality\n\nReview only the files and scope of the current phase.",
  activeForm: "Reviewing code"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X silent-failure-hunter: Hunt edge cases",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-hunt\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Audit current phase blast radius\n\nFind silent failures and edge cases adjacent to the current phase.",
  activeForm: "Hunting failures"
}) -> hunter_task_id
TaskUpdate({ taskId: hunter_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X integration-verifier: Verify integration",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-verify\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Phase exit verification\n\nRun required checks for the current phase and report whether truths, artifacts, wiring, and phase exit criteria are all satisfied.",
  activeForm: "Verifying integration"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id, hunter_task_id] })
```

**Change 2:** Escalation rule — add hunter to the trivial→full escalation

**OLD:**

```
If the builder triggers the escalation rule, convert this into the full graph before running the verifier: add the code-reviewer task (blocked by builder), add doc-syncer (blocked by verifier), re-block verifier on `[reviewer_task_id]`, and re-block Memory Update on `doc_sync_task_id`.
```

**NEW:**

```
If the builder triggers the escalation rule, convert this into the full graph before running the verifier: add the code-reviewer task (blocked by builder), add the silent-failure-hunter task (blocked by builder), add doc-syncer (blocked by verifier), re-block verifier on `[reviewer_task_id, hunter_task_id]`, and re-block Memory Update on `doc_sync_task_id`.
```

**Change 3:** Trivial graph description — add "NO `silent-failure-hunter` task"

**OLD:**

```
- `build_scope=trivial` → use the **reduced task graph** below: `component-builder` → `integration-verifier` → `Memory Update`. NO separate `code-reviewer` task, NO standalone `doc-syncer` task.
```

**NEW:**

```
- `build_scope=trivial` → use the **reduced task graph** below: `component-builder` → `integration-verifier` → `Memory Update`. NO separate `code-reviewer` task, NO `silent-failure-hunter` task, NO standalone `doc-syncer` task.
```

**Change 4:** Deferred findings roll-up — add hunter as a source

**OLD:**

```
- When `code-reviewer` raises a Minor finding that does NOT block the current `phase_exit_gate`, the router appends it to `deferred_findings` (each entry: `source` agent, `phase_id`, terse `finding`, and `severity:minor`) rather than dropping it.
```

**NEW:**

```
- When `code-reviewer` or `silent-failure-hunter` raises a Minor finding that does NOT block the current `phase_exit_gate`, the router appends it to `deferred_findings` (each entry: `source` agent, `phase_id`, terse `finding`, and `severity:minor`) rather than dropping it. Blocking findings still gate the phase as before — this array is only for the non-blocking remainder.
```

**File path:** `plugins/cc10x/skills/cc10x-router/references/build-workflow.md`

---

## Phase 5: Restore Re-Hunt in Remediation

### Step 5.1 — Edit `plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md`

**Change 1:** Re-review loop (§11) — restore the separate re-hunt task

**OLD (step 2):**

```text
2. Create a re-review task (one task — the reviewer's single pass covers both the fix re-review and the silent-failure re-scan):

TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-review\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-review the changes made by the completed remediation task, including a silent-failure re-scan (Pass 1b) of the remediated surface.\nIf scope=ALL_ISSUES: perform a FULL re-audit of CRITICAL and HIGH issue categories after remediation.\nIf scope=CRITICAL_ONLY: verify the CRITICAL issue was resolved and treat HIGH issues as deferred unless newly escalated.",
  activeForm: "Re-reviewing fix"
}) -> rereview_task_id
```

**NEW:**

```text
2. Create a re-review task:

TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-review\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-review the changes made by the completed remediation task.\nIf scope=ALL_ISSUES: perform a FULL re-audit of CRITICAL and HIGH issue categories after remediation.\nIf scope=CRITICAL_ONLY: verify the CRITICAL issue was resolved and treat HIGH issues as deferred unless newly escalated.",
  activeForm: "Re-reviewing fix"
}) -> rereview_task_id

3. Create a re-hunt task (BUILD only — the hunter re-scans for silent failures after remediation):

TaskCreate({
  subject: "CC10X silent-failure-hunter: Re-hunt after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-hunt\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-scan for silent failures after remediation. Focus on the remediated surface and its immediate call sites.",
  activeForm: "Re-hunting failures"
}) -> rehunt_task_id
```

**Change 2:** Step 3 (was "Reuse the pending verifier") — update to block on both

**OLD:**

```
3. Reuse the pending verifier in the same `wf:` if one exists; otherwise create:
```

**NEW:**

```
4. Reuse the pending verifier in the same `wf:` if one exists; otherwise create:
```

**Change 3:** Step 4 (block verifier) — block on both re-review AND re-hunt

**OLD:**

```
4. Block the verifier on the re-review task.
```

**NEW:**

```
5. Block the verifier on both the re-review and re-hunt tasks.
```

**Change 4:** Step 5 (re-block memory) — update step number

**OLD:**

```
5. Re-block the memory task on the verifier for BUILD/DEBUG or on the re-reviewer for REVIEW.
```

**NEW:**

```
6. Re-block the memory task on the verifier for BUILD/DEBUG or on the re-reviewer for REVIEW.
```

**Change 5:** Telemetry counters — restore re_hunt

**OLD:**

```
   - `telemetry.loop_counts.re_review += 1`
   - `telemetry.loop_counts.re_verify += 1`
```

**NEW:**

```
   - `telemetry.loop_counts.re_review += 1`
   - `telemetry.loop_counts.re_hunt += 1` (BUILD only)
   - `telemetry.loop_counts.re_verify += 1`
```

**Change 6:** Rule matrix Rule 2 — update to reference separate hunter

**OLD:**

```
| 2 | Reviewer verdict is Approve overall but its Pass 1b silent-failure scan reports HIGH issues | Ask whether to remediate or proceed. (CRITICAL Pass 1b issues never reach this row — the contract override already converts them to `CHANGES_REQUESTED`.) |
```

**NEW:**

```
| 2 | Reviewer verdict is Approve but silent-failure-hunter reports HIGH issues | Ask whether to remediate or proceed. (CRITICAL hunter issues never reach this row — the contract override already converts them to blocking.) |
```

**Change 7:** Rule 1a-SCOPE — update to reference hunter

**OLD:**

```
  - at least one HIGH issue in the reviewer narrative (including Pass 1b silent-failure findings)
```

**NEW:**

```
  - at least one HIGH issue in the reviewer or hunter narrative
```

**File path:** `plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md`

---

## Phase 6: Fix Stale References

### Step 6.1 — Fix `plugins/cc10x/skills/code-review/SKILL.md` — "Two Isolated Assessments + WEAVE" section

**OLD (lines 56–62):**

```markdown
### Two Isolated Assessments + WEAVE

When reviewer + Pass 1b (silent failure scan) run in parallel:

- **Assessment A** (reviewer): correctness, performance, spec compliance. Forms opinion WITHOUT seeing B's scan.
- **Assessment B** (Pass 1b): silent failure scan using red-flags table. Does NOT see A's findings.
- **WEAVE reconciliation:** after both commit. Where both agree → high confidence. Where B caught what A missed → keep. Where B is false positive → drop with reason.
```

**NEW:**

```markdown
### Parallel Review + Router Merge

When `code-reviewer` and `silent-failure-hunter` run in parallel (BUILD workflow):

- **code-reviewer** (Assessment A): correctness, performance, spec compliance. Forms opinion WITHOUT seeing the hunter's scan.
- **silent-failure-hunter** (Assessment B): silent failure scan using red-flags table. Does NOT see the reviewer's findings.
- **Router-owned merge:** after both complete, the router writes a merged findings summary into the workflow artifact before verifier handoff. Where both agree → high confidence. Where the hunter caught what the reviewer missed → keep. Where the hunter finding is a false positive → drop with reason. Contradictory verdicts: stricter verdict wins, logged in `status_history`.
```

### Step 6.2 — Update `plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md`

**Change 1:** evidence.hunter — remove LEGACY tag

**OLD:**

```
  - `hunter` (LEGACY — the standalone hunter is retired into the reviewer's Pass 1b; key kept for pre-consolidation artifacts, stays empty in new workflows)
```

**NEW:**

```
  - `hunter` (ACTIVE — the standalone silent-failure-hunter agent's evidence)
```

**Change 2:** telemetry.agent_wall_clock_seconds.hunter — remove LEGACY tag

**OLD:**

```
  - `hunter` (LEGACY — stays 0 in new workflows)
```

**NEW:**

```
  - `hunter`
```

**Change 3:** telemetry.loop_counts.re_hunt — remove LEGACY tag

**OLD:**

```
  - `re_hunt` (LEGACY — stays 0 in new workflows; silent-failure re-scan is part of `re_review`)
```

**NEW:**

```
  - `re_hunt`
```

**Change 4:** Contract overrides — update the Pass 1b override to reference the hunter

**OLD:**

```
| code-reviewer | An `APPROVE` whose Pass 1b silent-failure scan states zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification. A clean silent-failure verdict requires stated scan scope. |
```

**NEW:**

```
| code-reviewer | An `APPROVE` with zero findings across ALL dimensions AND fewer than 3 file:line evidence citations → trigger fallback inline verification. Rubber-stamp approvals without substantive analysis are invalid. |
| silent-failure-hunter | A `CLEAN` verdict that states zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification. A clean silent-failure verdict requires stated scan scope. |
```

**File path:** `plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md`

### Step 6.3 — Skeleton JSON — no changes needed

The `workflow-artifact.skeleton.json` already has the `hunter` keys (`results.hunter: null`, `evidence.hunter: []`, `telemetry.agent_wall_clock_seconds.hunter: 0`, `telemetry.loop_counts.re_hunt: 0`). They were kept as LEGACY placeholders. They now become ACTIVE again. **No file changes needed.**

### Step 6.4 — Update `plugins/cc10x/agents/integration-verifier.md`

**OLD (line 37):**

```
Your prompt includes findings from code-reviewer (including Pass 1b silent failure scan) under `## Previous Agent Findings`. Review before starting.
```

**NEW:**

```
Your prompt includes findings from code-reviewer and silent-failure-hunter under `## Previous Agent Findings`. Review before starting.
```

**File path:** `plugins/cc10x/agents/integration-verifier.md`

---

## Phase 7: Update Agent Count References

### Step 7.1 — README.md (line 12)

**OLD:**

```
<strong>1 router</strong> &nbsp;·&nbsp; <strong>8 specialist agents</strong> &nbsp;·&nbsp; <strong>16 skills</strong> &nbsp;·&nbsp; <strong>4 workflows</strong>
```

**NEW:**

```
<strong>1 router</strong> &nbsp;·&nbsp; <strong>9 specialist agents</strong> &nbsp;·&nbsp; <strong>16 skills</strong> &nbsp;·&nbsp; <strong>4 workflows</strong>
```

### Step 7.2 — CHANGELOG.md — Add v12.2.0 entry

Add a new entry at the top documenting the restoration:

```markdown
## [12.2.0] - 2026-07-02

### Restored: Parallel Review (silent-failure-hunter)

Restored the standalone `silent-failure-hunter` agent and all parallel dispatch infrastructure that was incorrectly merged into `code-reviewer` as "Pass 1b" in v12.1.0.

**Agents: 8 → 9** (restored silent-failure-hunter)

#### What was restored:
- `silent-failure-hunter` agent (separate context, zero-tolerance posture, no confidence threshold, no self-healing)
- Parallel dispatch: `code-reviewer` + `silent-failure-hunter` invoked in the same message in BUILD
- Router-owned merged findings summary before verifier handoff
- Contradiction resolution (stricter verdict wins, logged in status_history)
- `phase:build-hunt` and `phase:re-hunt` in metadata contract
- `build-hunt` and `re-hunt` in dispatcher table
- Parallel task DAG: verifier blocked by `[reviewer_task_id, hunter_task_id]`
- Re-hunt task after remediation (BUILD only)
- `telemetry.loop_counts.re_hunt` counter (ACTIVE, no longer LEGACY)
- Verifier handoff format: separate "Silent Failure Hunter" section
- Routing table: `[code-reviewer || silent-failure-hunter]` notation

#### What was removed:
- Pass 1b step from `code-reviewer.md`
- "This pass replaces the former standalone silent-failure-hunter agent" line
- LEGACY tags from hunter keys in artifact policy and skeleton
- Stale "Two Isolated Assessments + WEAVE" section in code-review skill (replaced with "Parallel Review + Router Merge")

#### Why:
The merge sacrificed genuine parallelism, context isolation, and the router's merge orchestration pattern for ~80 lines of savings. Two agents running in parallel cannot bias each other — the reviewer doesn't know what the hunter will find, and vice versa. One agent doing sequential passes introduces anchoring bias. The hunter's zero-tolerance posture and suspicion gate get diluted when competing with 6 other passes in one context.
```

### Step 7.3 — plugin.json version bump

**OLD:**

```json
"version": "12.1.0"
```

**NEW:**

```json
"version": "12.2.0"
```

**File paths:** `README.md`, `CHANGELOG.md`, `plugins/cc10x/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

---

## Phase 8: Version Bump

### Step 8.1 — Bump version in all locations

- `plugins/cc10x/.claude-plugin/plugin.json`: `12.1.0` → `12.2.0`
- `.claude-plugin/marketplace.json`: `12.1.0` → `12.2.0`
- `README.md`: version badge if present
- `CHANGELOG.md`: new entry (see Step 7.2)

---

## Execution Order

The changes must be applied in this order to avoid intermediate broken states:

1. **Step 1.1** — Create `silent-failure-hunter.md` (agent exists before router references it)
2. **Step 2.1** — Remove Pass 1b from `code-reviewer.md` (reviewer no longer does silent-failure scanning)
3. **Step 3.1–3.8** — Update router `SKILL.md` (restore parallel dispatch, merge logic, routing table, dispatcher table, metadata contract, verifier handoff, hard rules)
4. **Step 4.1** — Update `build-workflow.md` (restore parallel task DAG)
5. **Step 5.1** — Update `remediation-and-research.md` (restore re-hunt)
6. **Step 6.1** — Fix `code-review/SKILL.md` (stale WEAVE section)
7. **Step 6.2** — Update `workflow-artifact-and-hook-policy.md` (un-LEGACY hunter keys)
8. **Step 6.4** — Update `integration-verifier.md` (verifier handoff)
9. **Step 7.1–7.3** — Update README, CHANGELOG, plugin.json, marketplace.json (agent count + version)
10. **Step 8.1** — Version bump

---

## Verification Steps

After all changes are applied:

1. **Agent count check:** `ls plugins/cc10x/agents/*.md | wc -l` should return 9
2. **No Pass 1b references:** `grep -r "Pass 1b" plugins/cc10x/` should return zero results (or only CHANGELOG historical entries)
3. **No LEGACY hunter tags:** `grep -r "LEGACY.*hunter" plugins/cc10x/` should return zero results
4. **Parallel dispatch present:** `grep "invoke them in the same message" plugins/cc10x/skills/cc10x-router/SKILL.md` should return 1 match
5. **Build-hunt phase present:** `grep "build-hunt" plugins/cc10x/skills/cc10x-router/SKILL.md` should return ≥2 matches (metadata contract + dispatcher table)
6. **Re-hunt phase present:** `grep "re-hunt" plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md` should return ≥3 matches
7. **Hunter task in build workflow:** `grep "silent-failure-hunter" plugins/cc10x/skills/cc10x-router/references/build-workflow.md` should return ≥2 matches
8. **Verifier blocked by both:** `grep "reviewer_task_id, hunter_task_id" plugins/cc10x/skills/cc10x-router/references/build-workflow.md` should return 1 match
9. **Router merge logic:** `grep "merged findings summary" plugins/cc10x/skills/cc10x-router/SKILL.md` should return 1 match
10. **Contradiction resolution:** `grep "stricter verdict" plugins/cc10x/skills/cc10x-router/SKILL.md` should return 1 match
11. **Routing table parallel notation:** `grep "code-reviewer || silent-failure-hunter" plugins/cc10x/skills/cc10x-router/SKILL.md` should return 1 match
12. **Python scripts pass:** `python3 -c "import ast; ast.parse(open('plugins/cc10x/scripts/cc10x_task_completed_guard.py').read())"` and same for all other scripts
13. **Orchestration validation:** run the 12-check validation suite
14. **Doc consistency:** verify 9 agents, 16 skills

---

## Constraints Checklist

- [x] v12.1 effort frontmatter preserved on all agents (hunter gets `effort: high`)
- [x] v12.1 agent-common skill included in hunter's `skills:` frontmatter
- [x] v12.1 model-tier honesty preserved (hunter gets `model: inherit`)
- [x] Red-flags reference file stays at `agents/references/silent-failure-red-flags.md`
- [x] Stress test fixes preserved (read-back gate, event log append, artifact freshness check — these are in router §12 steps 5–7 and the hook scripts, not affected by this restoration)
- [x] Anti-anchoring design preserved (hunter does NOT read activeContext.md, same as reviewer)
- [x] Router's read-back gate and event log append instructions survive (they're in §12 "After every agent completion" steps 5–7, which are additive to the merge logic restoration)

---

## Residual Risks

1. **Claude Code parallel dispatch support** — The router instructs the model to "invoke them in the same message." Whether the model actually dispatches two `Agent()` calls in one turn depends on the model's behavior. If it dispatches sequentially, the fallback covers this. This is the same risk v11 had.

2. **Token cost** — Two agents instead of one means roughly 2× the token cost for the review phase. This is the deliberate trade-off: parallel execution + context isolation + no anchoring bias in exchange for higher cost.

3. **Doc consistency check** — The doc consistency test counts agents and skills. It needs to be updated to expect 9 agents instead of 8. Check if there's a hardcoded count in the test script.

4. **Research dual-dispatch** — The research parallel pattern is partially preserved but weaker. This plan does NOT strengthen it (the user asked specifically about parallel review). The research pattern should be evaluated separately.

5. **Trivial build gap** — Trivial builds (`build_scope=trivial`) still get no hunter (and no reviewer). This is the same as v11. The escalation path now adds both reviewer AND hunter when trivial→full is triggered.