# Router Harmony Verification — Does the router use the full power of the system?

**Scope:** `cc10x-router/SKILL.md` (752 lines) + 7 reference files + cross-check against all 17 skills and 9 agents.

---

## Check 1: Does the router reference ALL 17 skills by name?

### VERDICT: PARTIAL PASS (8/17 referenced, 9 intentionally not — but 2 are genuinely orphaned)

**Inventory of 17 skills** (from `plugins/cc10x/skills/`):

| # | Skill | Referenced in router? | Evidence |
| --- | ------- | ---------------------- | ---------- |
| 1 | `agent-common` | NO | `disable-model-invocation: true` — shared preamble auto-loaded by agents, never user-facing |
| 2 | `architecture` | YES | §7 deterministic skill hints: "Include `cc10x:architecture` only for multi-component, API, schema, auth, or integration-heavy work." |
| 3 | `building` | NO | This is the BUILD workflow skill loaded by `component-builder` agent, not by the router. The router has its own `build-workflow.md` reference. |
| 4 | `cc10x-router` | NO (self) | The router is itself — no self-reference needed. |
| 5 | `code-review` | YES | §7: "Include `cc10x:code-review` only when a human/external reviewer's feedback must be acted on" |
| 6 | `codebase-hygiene` | YES | §7: "Include `cc10x:codebase-hygiene` only when (a) the code-reviewer is asked for a reuse/consolidation audit..." |
| 7 | `debugging` | NO | This is the DEBUG workflow skill loaded by `bug-investigator` agent. Router has its own `debug-workflow.md`. |
| 8 | `diff-driven-docs` | NO | Loaded by `doc-syncer` agent. Router dispatches doc-syncer but doesn't name the skill. |
| 9 | `exploration` | YES | §7 + `plan-workflow.md` step 2: "ALWAYS run `Skill(skill='cc10x:exploration')` in the main context before planner" |
| 10 | `frontend` | YES | §7: "Include `cc10x:frontend` only when the request, changed files, plan, or design targets UI/frontend work" |
| 11 | `mcp-cli` | YES | §7: "Include `cc10x:mcp-cli` only when a researcher needs a one-off MCP capability" |
| 12 | `memory-and-handoff` | YES | §7: "Include `cc10x:memory-and-handoff` only when work is being handed to a coworker" |
| 13 | `plan-review-gate` | NO | Loaded by `planner` agent (planner.md references `cc10x:plan-review-gate`). Router dispatches planner but doesn't name the skill. |
| 14 | `planning` | NO | Loaded by `planner` agent. Router has its own `plan-workflow.md`. |
| 15 | `research` | YES | §7: "Include `cc10x:research` only when planner or investigator receives `## Research Files`" |
| 16 | `update` | NO | This is the cc10x self-upgrade skill. The router is an orchestration entry point — `update` is a meta/operational skill outside the build/debug/review/plan domain. **Genuinely orphaned from the router** — the router's trigger keywords include "update" but route it to BUILD, not to `cc10x:update`. |
| 17 | `verification` | NO | Loaded by `integration-verifier` and other agents. Router has verification logic inline. |

**Analysis:**

- 8 skills are explicitly referenced by the router in `## SKILL_HINTS` or `Skill()` calls: architecture, code-review, codebase-hygiene, exploration, frontend, mcp-cli, memory-and-handoff, research.
- 7 skills are agent-internal (loaded by dispatched agents, not the router): agent-common, building, debugging, diff-driven-docs, plan-review-gate, planning, verification. This is by design — the router dispatches agents, and agents load their own skills.
- 1 skill is self-referential: cc10x-router.
- 1 skill is genuinely orphaned: **`update`** — the router's trigger keywords include "update" but route it to BUILD (DEFAULT). The `cc10x:update` skill (self-upgrade) is never referenced or dispatched by the router. A user saying "update cc10x" would be routed to BUILD, not to the update skill. This is a **gap** but may be intentional (the update skill has its own trigger keywords in its frontmatter).

**Orphaned skills (in SKILL_HINTS context):** `update` is the only truly orphaned skill. The other 8 unreferenced skills are agent-internal by design.

---

## Check 2: Does the router dispatch ALL 9 agents?

### VERDICT: PASS

**9 agents** (from `plugins/cc10x/agents/`):

| # | Agent | Dispatcher entry | Evidence |
| --- | ------- | ----------------- | ---------- |
| 1 | `component-builder` | `build-implement` | §7 dispatcher table: "`build-implement` → `cc10x:component-builder`" |
| 2 | `bug-investigator` | `debug-investigate` | §7: "`debug-investigate` → `cc10x:bug-investigator`" + remfix origin rule |
| 3 | `code-reviewer` | `build-review`, `debug-review`, `review-audit`, `re-review` | §7: all four phases → `cc10x:code-reviewer` |
| 4 | `silent-failure-hunter` | `build-hunt`, `re-hunt` | §7: "`build-hunt`, `re-hunt` → `cc10x:silent-failure-hunter`" |
| 5 | `integration-verifier` | `build-verify`, `debug-verify`, `re-verify` | §7: all three → `cc10x:integration-verifier`" |
| 6 | `planner` | `plan-create`, `re-plan` | §7: "`plan-create`, `re-plan` → `cc10x:planner`" |
| 7 | `plan-gap-reviewer` | `plan-review-gap-1`, `plan-review-gap-2` | §7: both → `cc10x:plan-gap-reviewer`" |
| 8 | `researcher` | `research-web`, `research-github` | §7: both → `cc10x:researcher`" |
| 9 | `doc-syncer` | `build-doc-sync` | §7: "`build-doc-sync` → `cc10x:doc-syncer`" |

All 9 agents are covered in the dispatcher table (§7). No agent is orphaned.

---

## Check 3: Does the router use the parallel review pattern (code-reviewer || silent-failure-hunter)?

### VERDICT: PASS

**Evidence (3 locations):**

1. **§1 routing table** (line ~37): `BUILD: component-builder → [code-reviewer ‖ silent-failure-hunter] → integration-verifier` — the `‖` symbol explicitly denotes parallel execution.

2. **§1 BUILD rules** (line ~55): "The reviewer and hunter run in parallel (two read-only agents in the same message) and the router merges their findings before verifier handoff."

3. **§12 step 5** (line ~601): "If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD: mark both in_progress first, invoke them in the same message. They are read-only and safe to parallelize." — Also includes fallback: "If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter)."

4. **build-workflow.md** full task graph: `reviewer_task_id` and `hunter_task_id` are both blocked by `builder_task_id` only, and `verifier_task_id` is blocked by `[reviewer_task_id, hunter_task_id]` — confirming parallel readiness.

---

## Check 4: Does the router use the DEBUG fan-out pattern?

### VERDICT: PASS

**Evidence:** `references/debug-workflow.md` contains a complete "DEBUG independence-test gate (opt-in fan-out)" section:

1. **Gate conditions**: Both halves of the INDEPENDENCE TEST must PASS:
   - Separable understanding — each problem fixable without reading the others
   - Disjoint files — no file appears in two groups

2. **Fan-out pattern**: "When BOTH halves PASS, fan out one scoped `bug-investigator` per domain — each scoped to its own non-overlapping file set."

3. **Task creation**: Scoped `bug-investigator` per domain with `scope:{files this investigator owns}` in the task description.

4. **Fan-in conflict-check**: "On return from a fan-out, BEFORE running the unified verifier, run a fan-in CONFLICT-CHECK":
   - Collect actual edited files per investigator
   - Intersect pairwise — if overlap, reconcile with single agent
   - Only proceed when all edited-file sets are pairwise disjoint

5. **Single unified verifier**: "proceed to the single unified verifier... never one verifier per domain"

The pattern is fully wired with independence test, scoped fan-out, conflict-check fan-in, and unified verification.

---

## Check 5: Does the router merge findings from parallel agents?

### VERDICT: PASS

**Evidence (2 locations):**

1. **§12 step 6** (line ~612): "if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff"

2. **§7 "Previous Agent Findings handoff"** (line ~409): The router builds a merged `## Previous Agent Findings` section for the verifier containing both:

   ```
   ### Code Reviewer
   **Verdict:** {Approve|Changes Requested}
   **Critical Issues:** {reviewer critical issues or "None"}

   ### Silent Failure Hunter
   **Critical Issues:** {hunter critical issues or "None / not in this workflow"}
   ```

3. **§12 "Verifier findings handoff"** (line ~640): "Read `results.reviewer` and `results.hunter` from the workflow artifact. Build `## Previous Agent Findings` exactly in the format verifier expects."

The merge is router-owned, written into the workflow artifact, and passed as a combined section to the verifier.

---

## Check 6: Are ALL workflow types (BUILD, DEBUG, REVIEW, PLAN, ORIENT) fully wired?

### VERDICT: PASS

| Workflow | Routing (§1) | Preparation (§5) | Task Graph (§6) | Reference file | Fully wired? |
| ---------- | ------------- | ----------------- | ----------------- | ---------------- | ------------- |
| BUILD | Priority 5 (DEFAULT) | §5 BUILD prep → `references/build-workflow.md` | §6 → build-workflow.md `### BUILD task graph` | ✅ exists | YES — full + reduced graph, complexity gradient, escalation |
| DEBUG | Priority 1 (ERROR) | §5 DEBUG prep → `references/debug-workflow.md` | §6 → debug-workflow.md `### DEBUG task graph` | ✅ exists | YES — includes fan-out/fan-in |
| REVIEW | Priority 3 | §5 REVIEW prep → `references/review-workflow.md` | §6 → review-workflow.md `### REVIEW task graph` | ✅ exists | YES — advisory only |
| PLAN | Priority 2 | §5 PLAN prep → `references/plan-workflow.md` | §6 → plan-workflow.md `### PLAN task graph` | ✅ exists | YES — bounded fresh-review DAG (2 passes max) |
| ORIENT | Priority 4 | §1 ORIENT move procedure (inline) | No task graph (no agents) | N/A | YES — read-only inline, no agents, no artifact |

All 5 workflow types are fully wired with preparation, task graph, and reference files (where applicable).

---

## Check 7: Does the router reference the new patterns (rationalization tables, red flags, etc.) or are they orphaned in skills?

### VERDICT: PARTIAL PASS — patterns are referenced but indirectly

**Rationalization anti-pattern:**

- **Router references it:** §14 hard rules: "Maintain professional objectivity in all routing decisions. Do not rationalize a failing workflow as 'close enough' or downgrade critical findings to avoid remediation."
- **Remediation reference:** `remediation-and-research.md` §verify-before-implement: "[EASY TO MISS: this is evidence-gated and must NOT become a rationalization escape hatch.]"
- **Router evals:** `evals/README.md` mentions "The rationalization tempting a wrong route"
- **NOT orphaned** — the router enforces anti-rationalization at both the hard-rules level and the remediation level.

**Self-check blocklist (dispatch bias prevention):**

- **Referenced in:** `workflow-artifact-and-hook-policy.md` §Dispatch-Prompt Construction Rules: "SELF-CHECK BLOCKLIST — before dispatch, the router greps its own drafted prompt for these literal phrases" (7 phrases listed).
- **NOT orphaned** — the router is instructed to self-grep before every read-only dispatch.

**Red flags (silent failure hunter):**

- **Agent-side:** `agents/references/silent-failure-red-flags.md` contains a full red-flags table (core patterns, language-specific, severity classification).
- **Agent-side:** `agents/integration-verifier.md` line 69: "### False-GREEN red flags"
- **Router-side:** The router does NOT directly reference the red-flags file or the "False-GREEN red flags" section by name. It dispatches the `silent-failure-hunter` and `integration-verifier` agents, which carry these patterns internally.
- **Assessment:** This is **by design** — the router dispatches agents that own their own patterns. The red-flags content lives in agent reference files, not router reference files. Not orphaned — it's agent-internal knowledge that the router doesn't need to duplicate.

**Summary:** No patterns are truly orphaned. Rationalization and self-check blocklist are explicitly router-referenced. Red flags are agent-internal by architecture.

---

## Check 8: Does the router's verifier handoff include both reviewer AND hunter findings?

### VERDICT: PASS

**Evidence (2 explicit locations):**

1. **§7 "Previous Agent Findings handoff"** (line ~409):

   ```
   ## Previous Agent Findings
   ### Code Reviewer
   **Verdict:** {Approve|Changes Requested}
   **Critical Issues:** {reviewer critical issues or "None"}
   ### Silent Failure Hunter
   **Critical Issues:** {hunter critical issues or "None / not in this workflow"}
   ```

   Note: "DEBUG skips the hunter." — correctly conditional.

2. **§12 "Verifier findings handoff"** (line ~640): "Read `results.reviewer` and `results.hunter` from the workflow artifact." + "Never invoke verifier without that section when review/hunt already ran."

Both reviewer and hunter findings are merged into the verifier's `## Previous Agent Findings` section. The handoff is conditional (hunter skipped in DEBUG) and mandatory when both ran.

---

## Check 9: Are there any broken file references (files that don't exist)?

### VERDICT: PASS — No broken references

**All referenced files verified to exist:**

| Referenced path | Exists? |
| ---------------- | --------- |
| `references/build-workflow.md` | ✅ |
| `references/debug-workflow.md` | ✅ |
| `references/review-workflow.md` | ✅ |
| `references/plan-workflow.md` | ✅ |
| `references/remediation-and-research.md` | ✅ |
| `references/workflow-artifact-and-hook-policy.md` | ✅ |
| `references/workflow-artifact.skeleton.json` | ✅ |
| `${CLAUDE_PLUGIN_ROOT}/tools/review_package.py` | ✅ (`plugins/cc10x/tools/review_package.py`) |
| `${CLAUDE_PLUGIN_ROOT}/tools/phase_brief.py` | ✅ (`plugins/cc10x/tools/phase_brief.py`) |

All 9 referenced files exist. No broken references.

---

## Check 10: Is the routing table consistent with the dispatcher table?

### VERDICT: PASS (with minor note)

**Routing table (§1) chains:**

| Workflow | Chain in §1 | Agents used |
| ---------- | ------------ | ------------- |
| DEBUG | `bug-investigator -> code-reviewer -> integration-verifier` | 3 agents |
| PLAN | `exploration -> planner -> bounded fresh review loop` | planner + plan-gap-reviewer |
| REVIEW | `code-reviewer` | 1 agent |
| ORIENT | `advisory orientation (no agents)` | 0 agents |
| BUILD | `component-builder → [code-reviewer ‖ silent-failure-hunter] → integration-verifier` | 4 agents |

**Dispatcher table (§7) covers:**

- `bug-investigator` ✓ (debug-investigate)
- `code-reviewer` ✓ (build-review, debug-review, review-audit, re-review)
- `integration-verifier` ✓ (build-verify, debug-verify, re-verify)
- `planner` ✓ (plan-create, re-plan)
- `plan-gap-reviewer` ✓ (plan-review-gap-1, plan-review-gap-2)
- `component-builder` ✓ (build-implement)
- `silent-failure-hunter` ✓ (build-hunt, re-hunt)
- `researcher` ✓ (research-web, research-github) — not in routing table chains but triggered by remediation/research rules
- `doc-syncer` ✓ (build-doc-sync) — not in routing table chain but in BUILD task graph

**Consistency check:**

- Every agent in the routing chains has a matching dispatcher entry ✓
- Every dispatcher entry maps to an agent used in a workflow task graph ✓
- The routing table's BUILD chain omits `doc-syncer` and Memory Update — this is a **summary simplification**, not an inconsistency. The full BUILD task graph in `build-workflow.md` includes doc-syncer → Memory Update, and the dispatcher table covers `build-doc-sync → cc10x:doc-syncer`. The routing table shows the "core" chain; the task graph shows the full chain.
- `researcher` is not in any routing-table chain but is dispatched via research orchestration rules (§10). This is correct — research is triggered mid-workflow, not at routing time.

**Minor note:** The routing table BUILD chain could be more complete by showing `→ doc-syncer → Memory` but this is a documentation simplification, not a functional inconsistency. The dispatcher and task graphs are consistent.

---

## Summary Table

| Check | Description | Verdict |
| ------- | ------------- | --------- |
| 1 | Router references ALL 17 skills by name | **PARTIAL PASS** — 8/17 referenced in SKILL_HINTS; 7 are agent-internal by design; 1 (`update`) is genuinely orphaned from router routing |
| 2 | Router dispatches ALL 9 agents | **PASS** — all 9 agents in dispatcher table |
| 3 | Parallel review pattern (reviewer ‖ hunter) | **PASS** — 4 explicit references with fallback |
| 4 | DEBUG fan-out pattern | **PASS** — full independence-test gate, scoped fan-out, conflict-check fan-in |
| 5 | Merges findings from parallel agents | **PASS** — router-owned merged summary + structured verifier handoff |
| 6 | All 5 workflow types fully wired | **PASS** — BUILD, DEBUG, REVIEW, PLAN, ORIENT all have prep + task graph + references |
| 7 | New patterns (rationalization, red flags) referenced | **PARTIAL PASS** — rationalization + self-check blocklist are router-referenced; red flags are agent-internal by design |
| 8 | Verifier handoff includes reviewer AND hunter findings | **PASS** — 2 explicit locations, conditional on workflow type |
| 9 | No broken file references | **PASS** — all 9 referenced files exist |
| 10 | Routing table consistent with dispatcher table | **PASS** — minor summary simplification in BUILD chain, no functional inconsistency |

---

## Overall Assessment

**8 PASS, 2 PARTIAL PASS, 0 FAIL**

The router is well-integrated with the system. The two PARTIAL PASS items are:

1. **Skill `update` orphaned from router** — The router's trigger keywords include "update" but route to BUILD. The `cc10x:update` skill (self-upgrade) is never referenced or dispatched. This may be intentional (the skill has its own trigger keywords in its frontmatter and may be invoked directly by the user), but from the router's perspective, a user saying "update cc10x" in a cc10x-routed session would be misrouted to BUILD.

2. **Red flags patterns are agent-internal** — The router doesn't reference `silent-failure-red-flags.md` or the verifier's "False-GREEN red flags" by name, but this is by architecture: the router dispatches agents that own their patterns. Not a true orphaning.

No FAIL items. No broken references. All 9 agents dispatched. All 5 workflows wired. Parallel review, DEBUG fan-out, findings merge, and verifier handoff all fully implemented.