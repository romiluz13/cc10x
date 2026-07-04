# v11 Parallel Review Pattern — Deep Architecture Analysis

> **Source state:** `584049d~1` (the commit immediately before `584049d refactor: Phase 3 — merge agents, update all references`)
> **Refactoring commit:** `584049d` merged `silent-failure-hunter` into `code-reviewer` as "Pass 1b" and reduced agent count from 10 to ~7-8.
> **Analysis date:** Extracted from git history via `git show 584049d~1:<path>`

---

## 1. The v11 `silent-failure-hunter` Agent

**File:** `584049d~1:plugins/cc10x/agents/silent-failure-hunter.md` (190 lines, deleted in `584049d`)

### Identity & Frontmatter

```yaml
---
name: silent-failure-hunter
description: "Internal agent. Use cc10x-router for all development tasks."
model: inherit
color: red
tools: Read, Bash, Grep, Glob, Skill, LSP, WebFetch
skills:
  - cc10x:code-review-patterns
---
```

### Core Purpose

> **Core:** Zero tolerance for silent failures. Find empty catches, log-only handlers, generic errors.
>
> **Posture:** Assume errors are present until evidence proves otherwise. A neutral scan produces neutral results. Your job is to find problems, not to confirm cleanliness.

This was a **READ-ONLY, detection-only** agent with a single adversarial focus: silent failures in error handling. Its entire scope was:

| Pattern | Problem |
| --------- | --------- |
| `catch (e) {}` | Swallows errors |
| Log-only catch | User never knows |
| "Something went wrong" | Not actionable |
| `\|\| defaultValue` | Masks errors |
| `?.` chains without logging | Silent short-circuit |
| Retry without notification | User unaware of degradation |

It also included **language-specific red flags** for Python, Go, Java, Rust, and Shell.

### Key Design Difference from `code-reviewer`: No Self-Healing

> **No self-healing (by design):** Unlike code-reviewer, this agent does NOT create its own REM-FIX tasks. It reports only. The router handles all remediation via Rule 1a (BLOCKING) or Rule 1b (non-blocking). This is intentional — the hunter's job is detection, not correction.

The hunter **never called `TaskUpdate(status: completed)`** — the router owned completion via fallback:

> Do NOT call TaskUpdate(status: completed) — this agent does not have that tool.

### Pass Structure

The hunter had a **single pass** — an error-handling audit — structured as a 9-step process:

```
0. Output contract envelope + verdict heading FIRST
1. Find — Search for: try, catch, except, .catch(, throw, error
2. Audit each — Is error logged? Does user get feedback? Is catch specific?
3. Rate severity — CRITICAL (silent), HIGH (generic), MEDIUM (could improve)
4. Report CRITICAL immediately — Provide exact file:line, recommended fix
5. Document others — HIGH and MEDIUM go in report only
6. Prevention recommendations — For each CRITICAL
7. Output Memory Notes — Document patterns found
8. Coverage truthfulness — Never claim CLEAN unless scanned scope is stated
9. Zero-Results Suspicion Gate — Verify ≥3 concrete sites inspected or flag advisory
```

### Severity Rubric

| Severity | Definition | Blocks Ship? |
| ---------- | ----------- | ------------- |
| CRITICAL | Data loss, security hole, crash, silent data corruption | YES |
| HIGH | Wrong behavior user will notice, degraded UX | Should fix |
| MEDIUM | Suboptimal but functional | Track as TODO |
| LOW | Code smell, style issue | Optional |

### Output Contract

```
CONTRACT {"s":"CLEAN","b":false,"cr":0}
## Error Handling Audit: [CLEAN/ISSUES_FOUND]
```

The envelope's `s` field was `CLEAN` or `ISSUES_FOUND`, distinct from the code-reviewer's `APPROVE`/`CHANGES_REQUESTED`.

### Scoping Heuristic (important for understanding the parallel split)

> **Scoping heuristic:** Start with files changed in the current workflow — use the router-provided changed-file list, or `git diff --name-only BASE..HEAD` (BASE = `results.git_base_sha`, the recorded sha before the phase's builder ran). Audit those first. Expand to their direct importers only if critical patterns are found. Do not scan the entire repo unless the prompt explicitly requests a full audit.

The hunter scoped to the **changed files** in the current phase, same as the code-reviewer — both operated on the same diff range but from different angles.

---

## 2. The v11 `code-reviewer` Agent

**File:** `584049d~1:plugins/cc10x/agents/code-reviewer.md` (full file, ~300 lines)

### Identity & Frontmatter

```yaml
---
name: code-reviewer
description: "Internal agent. Use cc10x-router for all development tasks."
model: inherit
color: blue
tools: Read, Bash, Grep, Glob, Skill, LSP, WebFetch
skills:
  - cc10x:code-review-patterns
  - cc10x:verification-before-completion
---
```

### Core Purpose

> **Core:** Adversarial multi-dimensional review. Only report issues with confidence ≥80. Every reported issue must state category, impact, and why it matters.
>
> **Posture:** Be opinionated. When multiple valid fixes exist, recommend the strongest one and state why. Present a recommendation, not a menu. Alternatives are context, not cover.

### Pass Structure — 6 Passes (Multi-Dimensional)

The code-reviewer had **six distinct review passes**, making it a broad-spectrum reviewer:

| Pass | Name | Focus |
| ------ | ------ | ------- |
| 1 | Security | Auth, input validation, secrets, injection, OWASP |
| 2 | Performance | N+1 queries, hot loops, memory leaks, cache opportunities |
| 3 | Quality | Complexity, naming, error handling, duplication, types |
| 4 | Friction Scan | Architectural friction: fragmentation, shallow modules, coupling risk |
| 5 | Plan Validity | Code-vs-plan compliance; flags WRONG plans as `PLAN_DEFECT` |
| 6 | Spec Compliance | Silent divergence from approved plan: MISSING / EXTRA / MISUNDERSTOOD |

### How Its Scope Differed from the Hunter

The **code-reviewer was a broad-spectrum reviewer** covering security, performance, quality, architecture friction, and plan/spec compliance. It had a confidence threshold (≥80 to report), multi-signal scoring (HARD/SOFT scores per dimension), and the ability to self-heal (create REM-FIX tasks in BUILD workflows).

The **silent-failure-hunter was a narrow-spectrum specialist** focused exclusively on error-handling anti-patterns (silent failures, swallowed exceptions, generic error messages). It had no confidence threshold, no multi-signal scoring, and no self-healing — it reported findings only, and the router owned remediation.

**The key architectural insight:** The code-reviewer's Pass 3 (Quality) did include "error handling" as one of its checks:

> Missing or generic error handling | HIGH

But this was a single line item in a broad pass. The hunter existed because the code-reviewer's error-handling check was shallow — a line item among many, easily deprioritized. The hunter was purpose-built with language-specific red flag tables, a zero-tolerance posture, and a dedicated suspicion gate that forced thorough inspection.

### Self-Healing Behavior

Unlike the hunter, the code-reviewer could create remediation tasks — but only in non-REVIEW workflows:

> **REVIEW WORKFLOW GUARD:** First, check your parent workflow:
> → If the task phase is `review-audit` for a REVIEW workflow:
>
> - Do NOT create a REM-FIX task. Do NOT block yourself.

In BUILD workflows:

> **Router-Owned Remediation (BUILD/DEBUG workflows only):**
>
> - BUILD review: request `REMEDIATION_SCOPE_REQUESTED: N/A` so the router can decide `CRITICAL_ONLY` vs `ALL_ISSUES` after combining parallel findings.

The critical detail: the code-reviewer **requested `N/A` scope in BUILD** specifically because it knew the router would combine its findings with the hunter's before deciding remediation scope. This is direct evidence of the parallel merge logic being anticipated by the agent's own instructions.

### Output Contract

```
CONTRACT {"s":"APPROVE","b":false,"cr":0}
## Review: [Approve/Changes Requested]
```

### Multi-Signal Scoring (absent from hunter)

```
SIGNAL_SCORES:
  security: [HARD] 100
  correctness: [HARD] 85
  performance: [SOFT] 70
  maintainability: [SOFT] 90
CONFIDENCE: 85  (min HARD=85, avg SOFT=80)
```

> **CONFIDENCE calculation:** `min(HARD scores)` capped by `avg(SOFT scores) - 10`.
> A single HARD:0 = CONFIDENCE:0 regardless of other dimensions.

---

## 3. The v11 Router's Parallel Dispatch Logic

**File:** `584049d~1:plugins/cc10x/skills/cc10x-router/SKILL.md`

### Routing Table — The `||` Notation

The routing table itself used the `||` (parallel) notation to declare the parallel relationship:

```
| 5 | DEFAULT | Everything else | BUILD | component-builder -> [code-reviewer || silent-failure-hunter] -> integration-verifier |
```

And the complexity gradient description:

> everything else, and all planned work, runs the full builder → [reviewer || hunter] → verifier → doc-sync → memory chain.

### The EXACT Parallel Dispatch Instructions (§12, Chain Execution Loop, Step 5)

Verbatim from the router SKILL.md:

```text
5. If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD:
   - mark both in_progress first
   - invoke them in the same message
   - If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter). Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
```

**Key observations:**

1. The condition was "both ready in BUILD" — meaning both tasks had their blockers (the builder) completed and were simultaneously runnable.
2. The instruction was "invoke them in the same message" — literally dispatching both `Agent()` calls in one response turn.
3. The fallback was **sequential, reviewer-first** — not hunter-first. The reviewer was the primary agent; the hunter was the supplement.
4. The fallback was never a hard failure: "Never block a workflow because parallelism is unavailable."

### Hard Rule on Parallelization Safety (§14)

Verbatim:

> Only parallelize agents whose file-write surfaces do not overlap. Reviewer and hunter are read-only and safe to parallelize. Two write agents on overlapping files must be serialized. [EASY TO MISS: Each parallel agent must have a distinct phase value and unique task description. Identical prompts cause agents to duplicate work or silently clobber each other's output.]

This confirms: the parallel dispatch was safe **because both agents were read-only**. They had no file-write surfaces that could conflict. The distinct phase values were `build-review` (code-reviewer) and `build-hunt` (silent-failure-hunter).

---

## 4. The v11 Build Workflow — Task DAG

**File:** `584049d~1:plugins/cc10x/skills/cc10x-router/references/build-workflow.md`

### Full Task Graph (`build_scope=standard`)

The task DAG had this structure:

```
component-builder (phase: build-implement)
    ├── code-reviewer (phase: build-review)       ── blockedBy: [builder]
    ├── silent-failure-hunter (phase: build-hunt)  ── blockedBy: [builder]
    │       (both reviewer and hunter run in PARALLEL after builder completes)
    └── integration-verifier (phase: build-verify) ── blockedBy: [reviewer, hunter]
            └── doc-syncer (phase: build-doc-sync) ── blockedBy: [verifier]
                    └── Memory Update (phase: memory-finalize) ── blockedBy: [doc_syncer]
```

### Exact Task Creation Code (verbatim from build-workflow.md)

**Code-reviewer task:**

```text
TaskCreate({
  subject: "CC10X code-reviewer: Review implementation",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-review\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Review current phase quality\n\nReview only the files and scope of the current phase.",
  activeForm: "Reviewing code"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })
```

**Silent-failure-hunter task:**

```text
TaskCreate({
  subject: "CC10X silent-failure-hunter: Hunt edge cases",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-hunt\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Audit current phase blast radius\n\nFind silent failures and edge cases adjacent to the current phase.",
  activeForm: "Hunting failures"
}) -> hunter_task_id
TaskUpdate({ taskId: hunter_task_id, addBlockedBy: [builder_task_id] })
```

**Integration-verifier task (blocked by BOTH):**

```text
TaskCreate({
  subject: "CC10X integration-verifier: Verify integration",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-verify\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Phase exit verification\n\nRun required checks for the current phase and report whether truths, artifacts, wiring, and phase exit criteria are all satisfied.",
  activeForm: "Verifying integration"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id, hunter_task_id] })
```

### Dependencies Summary

| Task | Phase | Blocked By |
| ------ | ------- | ------------ |
| component-builder | build-implement | (none) |
| code-reviewer | build-review | builder_task_id |
| silent-failure-hunter | build-hunt | builder_task_id |
| integration-verifier | build-verify | reviewer_task_id, hunter_task_id |
| doc-syncer | build-doc-sync | verifier_task_id |
| Memory Update | memory-finalize | doc_sync_task_id |

The verifier was blocked by **both** reviewer and hunter — it could not run until both parallel agents completed. This is the fan-in point of the parallel pattern.

### Trivial Scope Exclusion

The reduced task graph (`build_scope=trivial`) explicitly excluded both the reviewer and hunter:

> `build_scope=trivial` → use the **reduced task graph**: `component-builder` → `integration-verifier` → `Memory Update`. NO separate `code-reviewer` task, NO `silent-failure-hunter` task, NO standalone `doc-syncer` task.

### Escalation Rule (trivial → full)

> after the builder returns, if its Router Contract reports non-empty `SCOPE_INCREASES` or non-empty `BLOCKED_ITEMS`, the work was not actually trivial. Before advancing, promote the workflow to the full graph: create the `code-reviewer` and `silent-failure-hunter` tasks (blocked by the builder) and the `doc-syncer` task (blocked by the verifier), and re-block Memory Update on `doc_sync_task_id`.

---

## 5. The v11 Router's Merge/Combine Logic

### 5a. Merged Findings Summary (§12, Step 6)

Verbatim from the router SKILL.md:

```text
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff
```

The merge was **router-owned** — not delegated to either agent. The router wrote a single merged findings summary into the workflow artifact's `results` section after both agents completed. This merged summary was the input to the verifier handoff.

### 5b. Verifier Findings Handoff Format

The router constructed a `## Previous Agent Findings` section for the integration-verifier from both agents' results:

```text
## Previous Agent Findings

### Code Reviewer
**Verdict:** {Approve|Changes Requested}
**Critical Issues:**
{reviewer critical issues or "None"}

### Silent Failure Hunter
**Critical Issues:**
{hunter critical issues or "None / not in this workflow"}
```

The handoff instruction was explicit:

> Before invoking `integration-verifier` in BUILD:
>
> - Read `results.reviewer` and `results.hunter` from the workflow artifact.
> - Build `## Previous Agent Findings` exactly in the format verifier expects.
> - Never invoke verifier without that section when review/hunt already ran.

### 5c. Contradiction Resolution Rule

Verbatim from §12, Step 6:

```text
   - if two agents in the same phase return contradictory verdicts (e.g., reviewer approves but verifier fails on the same evidence), treat the stricter verdict as authoritative and do not average or reconcile the signals. Log the contradiction in `status_history`.
```

**The rule was: stricter verdict wins.** No averaging, no reconciliation, no "split the difference." If the reviewer said APPROVE but the hunter found CRITICAL issues, the hunter's CRITICAL findings would gate the phase. The contradiction was logged in `status_history` for auditability.

Note: the example given was "reviewer approves but verifier fails" — but the rule applied to **any two agents in the same phase**, which included the reviewer/hunter pair. Since the hunter used `ISSUES_FOUND` (not `CHANGES_REQUESTED`) and the reviewer used `CHANGES_REQUESTED` (not `ISSUES_FOUND`), a contradiction looked like: reviewer returns `APPROVE` while hunter returns `ISSUES_FOUND` with `b:true`. Under the stricter-verdict rule, the hunter's blocking finding would override the reviewer's approval.

### 5d. Remediation Scope Decision (Combining Both Agents' Findings)

The code-reviewer's own instructions reveal how the combined findings affected remediation:

> BUILD review: request `REMEDIATION_SCOPE_REQUESTED: N/A` so the router can decide `CRITICAL_ONLY` vs `ALL_ISSUES` after combining parallel findings.

The code-reviewer deliberately requested `N/A` scope because it knew the router would **combine** its findings with the hunter's before deciding the remediation scope. This is the "merge before deciding" pattern: the router collected both agents' structured intent fields, merged their critical issue counts, and then decided whether the REM-FIX task should fix only critical issues or all issues.

### 5e. Convergence Rule (§8)

> If evidence is incomplete, contradictory, or missing for a required pass path, do not advance the workflow. Set the workflow artifact `quality.convergence_state` to `needs_iteration` and stop on the appropriate remediation or clarification gate instead of treating the task as good enough.

This was a backstop: even if the stricter-verdict rule resolved a contradiction, the convergence rule could still halt the workflow if the combined evidence was incomplete.

### 5f. Deferred Minor Findings Roll-Up

Non-blocking findings from both agents were accumulated, not dropped:

> When `code-reviewer` or `silent-failure-hunter` raise a Minor finding that does NOT block the current `phase_exit_gate`, the router appends it to `deferred_findings` (each entry: `source` agent, `phase_id`, terse `finding`, and `severity:minor`) rather than dropping it.

The `deferred_findings` array accumulated across phases and was surfaced once at BUILD-DONE for user triage.

---

## 6. Architecture Summary — The Complete Parallel Pattern

### Data Flow

```
                    ┌─────────────────┐
                    │ component-builder│
                    │  (build-implement)│
                    └────────┬────────┘
                             │ (builder completes)
                    ┌────────┴────────┐
                    │                 │
          ┌─────────▼──────┐ ┌───────▼──────────┐
          │  code-reviewer  │ │ silent-failure   │
          │  (build-review) │ │ hunter           │
          │                 │ │ (build-hunt)     │
          │  6 passes:      │ │ 1 pass:          │
          │  security, perf,│ │ error handling   │
          │  quality,       │ │ anti-patterns    │
          │  friction,      │ │                  │
          │  plan validity, │ │ No self-healing  │
          │  spec compliance│ │ Reports only     │
          └─────────┬───────┘ └───────┬──────────┘
                    │                 │
                    │  PARALLEL       │
                    │  (same message) │
                    │                 │
                    └────────┬────────┘
                             │ (both complete)
                    ┌────────▼────────┐
                    │     ROUTER       │
                    │  (merge logic)   │
                    │                  │
                    │ 1. Capture memory│
                    │ 2. Validate output│
                    │ 3. Write merged  │
                    │    findings      │
                    │ 4. Resolve       │
                    │    contradictions│
                    │    (stricter wins)│
                    │ 5. Decide REM    │
                    │    scope         │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ integration-     │
                    │ verifier         │
                    │ (build-verify)   │
                    │                  │
                    │ Receives:        │
                    │ ## Previous Agent│
                    │ Findings         │
                    │ (both reviewer + │
                    │  hunter results) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  doc-syncer      │
                    │  (build-doc-sync)│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Memory Update   │
                    │  (inline)        │
                    └─────────────────┘
```

### Why Two Agents Instead of One?

1. **Different adversarial postures:** The code-reviewer had a confidence threshold (≥80) and multi-signal scoring — it would suppress low-confidence findings. The hunter had zero tolerance and no confidence threshold — it reported everything matching its red flag table.

2. **Different scopes:** The code-reviewer was broad-spectrum (6 passes). The hunter was narrow-spectrum (1 pass, error handling only). Running them in parallel meant the error-handling audit got a dedicated agent's full attention rather than being a line item in Pass 3.

3. **Different self-healing behavior:** The code-reviewer could create REM-FIX tasks. The hunter could not. This separation prevented the hunter from self-remediating in ways that might mask the broader review's findings.

4. **Different output contracts:** `APPROVE`/`CHANGES_REQUESTED` vs `CLEAN`/`ISSUES_FOUND` — two distinct machine-readable signals that the router merged.

### Why the Refactoring Merged Them

Commit `584049d` merged the hunter into the code-reviewer as "Pass 1b" and moved the red-flags table to `agents/references/silent-failure-red-flags.md`. The refactoring commit message explains:

> silent-failure-hunter → code-reviewer Pass 1b (red-flags table → reference file)

The trade-off: the merged agent lost the dedicated adversarial posture (zero tolerance, no confidence threshold, suspicion gate) that the standalone hunter had. The red-flags table survived as a reference file, but the hunter's "assume errors are present until evidence proves otherwise" posture and its zero-results suspicion gate were absorbed into a broader reviewer that has competing priorities across 6+ passes.

---

## 7. Exact Verbatim Quotes — Quick Reference

### Parallel dispatch condition and method
>
> "If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD: mark both in_progress first, invoke them in the same message"

### Parallel fallback
>
> "If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter). Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log."

### Merge logic
>
> "if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff"

### Contradiction resolution
>
> "if two agents in the same phase return contradictory verdicts (e.g., reviewer approves but verifier fails on the same evidence), treat the stricter verdict as authoritative and do not average or reconcile the signals. Log the contradiction in `status_history`."

### Parallelization safety
>
> "Only parallelize agents whose file-write surfaces do not overlap. Reviewer and hunter are read-only and safe to parallelize. Two write agents on overlapping files must be serialized. [EASY TO MISS: Each parallel agent must have a distinct phase value and unique task description.]"

### Verifier handoff
>
> "Read `results.reviewer` and `results.hunter` from the workflow artifact. Build `## Previous Agent Findings` exactly in the format verifier expects. Never invoke verifier without that section when review/hunt already ran."

### Remediation scope combination
>
> "BUILD review: request `REMEDIATION_SCOPE_REQUESTED: N/A` so the router can decide `CRITICAL_ONLY` vs `ALL_ISSUES` after combining parallel findings."