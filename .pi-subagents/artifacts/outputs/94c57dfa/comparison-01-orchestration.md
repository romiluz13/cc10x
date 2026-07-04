# Deep Comparison: Orchestration & Routing Architecture

**Projects analyzed:**

- **cc10x** — `cc10x-router` skill (SKILL.md + 7 reference files + skeleton JSON + evals)
- **Superpowers** — `subagent-driven-development`, `dispatching-parallel-agents`, `executing-plans`
- **Matt Pocock** — `triage`, `to-issues`, `to-prd`

---

## Executive Summary

| Dimension | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| Routing model | Router kernel with priority-matched intent table | Skill-driven (user picks skill, skill runs) | Manual / maintainer-driven state machine |
| Agent dispatch decision | Deterministic dispatcher table keyed by phase+kind+origin | Controller constructs per-task prompt with model tier | No agent dispatch — writes agent briefs for later pickup |
| Task dependency management | Full DAG via `blockedBy` + workflow artifact `phase_cursor` | Sequential todo list + per-task review gate | `Blocked by` field in published issues |
| Parallel vs sequential | Parallel read-only agents (reviewer ‖ hunter); sequential write agents; optional DEBUG fan-out with independence test | Explicitly serial for implementation; parallel only for independent debugging problems | N/A — no execution orchestration |
| Fallback handling | Circuit breaker (3-cycle cap), change-something-before-re-dispatch, inline fallback mode, model tier escalation, scope escalation (trivial→full) | Status-based handling (DONE, BLOCKED, NEEDS_CONTEXT), model escalation, task splitting | Maintainer override at any point; `needs-info` loop back to reporter |
| Sophistication score | **9/10** | **6/10** | **3/10** |

---

## 1. How Does Each Project Route Work?

### cc10x: Router Kernel with Priority-Matched Intent Table

cc10x is the only project with a dedicated **routing kernel** — the `cc10x-router` SKILL.md is explicitly "THE ONLY ENTRY POINT FOR CC10X." It uses a priority-ordered intent routing table:

| Priority | Signal | Workflow |
| ---------- | -------- | ---------- |
| 1 | ERROR | DEBUG |
| 2 | PLAN | PLAN |
| 3 | REVIEW | REVIEW |
| 4 | ORIENT | ORIENT (read-only, no agents) |
| 5 | DEFAULT | BUILD |

The router applies explicit precedence rules: "ERROR always wins over BUILD, but route on the PRIMARY DELIVERABLE." It emits a routing announcement line (`-> {WORKFLOW} workflow (signals: {matched keywords})`) before execution. The router is a **monolithic orchestration kernel** that owns all state, all dispatch, all validation, and all remediation decisions. Agents are never autonomous — they receive structured scaffolds and return machine-readable contracts.

### Superpowers: Skill-Driven (User/Context Picks the Skill)

Superpowers has no central router. Instead, the user or context determines which skill to activate:

- `subagent-driven-development` — for executing plans with independent tasks in-session
- `dispatching-parallel-agents` — for 2+ independent problems
- `executing-plans` — for executing plans in a separate session

Each skill is self-contained. The decision flow is a decision tree inside each SKILL.md (dot-graph rendered). The `subagent-driven-development` SKILL has a "When to Use" decision tree that routes between itself, `executing-plans`, and manual execution based on three questions: "Have implementation plan?", "Tasks mostly independent?", "Stay in this session?"

There is no unified entry point — the user must already know which skill to invoke.

### Matt Pocock: Manual / Maintainer-Driven State Machine

Matt Pocock's `triage` skill is a **state machine** for issue triage, not a code execution orchestrator. The maintainer invokes `/triage` and describes what they want. The skill routes issues through states: `needs-triage` → `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`.

`to-issues` breaks a plan into vertical-slice issues with `Blocked by` dependencies. `to-prd` synthesizes a conversation into a PRD. None of these skills execute code — they produce **artifacts for later pickup** by AFK agents or humans.

---

## 2. How Does Each Project Decide What Agent to Dispatch?

### cc10x: Deterministic Dispatcher Table

cc10x has an explicit dispatcher table mapping task phase/kind to a named agent:

| Task Phase / Kind | Agent |
| --- | --- |
| `build-implement` | `cc10x:component-builder` |
| `debug-investigate` | `cc10x:bug-investigator` |
| `build-review`, `debug-review`, `review-audit`, `re-review` | `cc10x:code-reviewer` |
| `build-hunt`, `re-hunt` | `cc10x:silent-failure-hunter` |
| `build-verify`, `debug-verify`, `re-verify` | `cc10x:integration-verifier` |
| `plan-create`, `re-plan` | `cc10x:planner` |
| `plan-review-gap-1/2` | `cc10x:plan-gap-reviewer` |
| `research-web/github` | `cc10x:researcher` |
| `build-doc-sync` | `cc10x:doc-syncer` |

The dispatch is keyed by `kind` + `origin` + `phase` metadata lines embedded in every task description. The router also applies a **per-role model-tier policy** (cheap/standard/capable) with a reviewer floor — "never run a verifier or reviewer on the cheapest tier."

The router constructs a **structured prompt scaffold** for every agent, including task context, user request, requirements, memory summary, project patterns, domain context, and skill hints. Anti-anchoring rules omit memory summaries from adversarial read-only agents to prevent bias.

### Superpowers: Controller Constructs Per-Task Prompt

The controller (main session) manually constructs each implementer and reviewer dispatch using template files (`implementer-prompt.md`, `task-reviewer-prompt.md`). Model selection is guided by a table:

| Task Type | Model Tier |
| --- | --- |
| Mechanical (1-2 files, clear spec) | cheap/fast |
| Integration (multi-file) | standard |
| Architecture/design | most capable |
| Review | scaled to diff complexity |

The controller extracts task briefs via `scripts/task-brief` and review packages via `scripts/review-package`, passing file paths rather than pasting content. The dispatch is template-driven but not table-driven — the controller fills in placeholders manually.

### Matt Pocock: No Agent Dispatch

Matt Pocock's skills do not dispatch agents. They produce **agent-ready briefs** (structured comments posted to GitHub issues) that AFK agents pick up later. The `AGENT-BRIEF.md` defines the brief format: category, summary, current behavior, desired behavior, key interfaces, acceptance criteria, out of scope. The brief is "the authoritative specification that an AFK agent will work from."

There is no model selection, no prompt scaffold construction, and no runtime dispatch.

---

## 3. How Does Each Project Manage Task Dependencies (DAGs, blockedBy)?

### cc10x: Full DAG via `blockedBy` + Workflow Artifact

cc10x uses Claude Code's native `TaskCreate` / `TaskUpdate` with `addBlockedBy` to construct explicit dependency graphs. Every task graph is defined as code with explicit `TaskUpdate({ addBlockedBy: [...] })` calls.

**BUILD full graph:**

```
builder → reviewer (blocked by builder)
builder → hunter (blocked by builder)
reviewer + hunter → verifier (blocked by both)
verifier → doc-syncer (blocked by verifier)
doc-syncer → memory (blocked by doc-syncer)
```

**BUILD trivial graph:**

```
builder → verifier → memory
```

**PLAN graph (pre-created DAG):**

```
planner → plan-review-gap-1 → re-plan → plan-review-gap-2 → memory
```

With pruning: if pass 1 succeeds, `re-plan` and `plan-review-gap-2` are pruned (marked deleted/completed).

The workflow artifact (`.cc10x/workflows/{uuid}.json`) tracks `phase_cursor`, `phase_status`, `normalized_phases`, and `task_ids` — a complete durable state machine. Resume logic reconstructs runnable tasks from `TaskList()` + `TaskGet()` using `wf:` + `kind:` + `phase:` metadata.

### Superpowers: Sequential Todo List + Per-Task Review Gate

Superpowers uses a simple sequential model: a todo list (Claude Code's built-in todos) with tasks executed one at a time. Each task goes through: implementer → task reviewer → (fix loop if needed) → mark complete. There is no explicit `blockedBy` — the controller simply doesn't start the next task until the current one passes review.

The **progress ledger** (`.superpowers/sdd/progress.md`) is a flat list: `Task N: complete (commits <base7>..<head7>, review clean)`. It serves as a recovery map after compaction, not a DAG.

Dependencies between tasks are acknowledged in the plan (`to-issues` uses `Blocked by` fields), but `subagent-driven-development` itself executes them sequentially regardless — "Dispatch multiple implementation subagents in parallel (conflicts)" is a red flag / never-rule.

### Matt Pocock: `Blocked by` in Published Issues

`to-issues` publishes issues with a `## Blocked by` section referencing other issue identifiers. Issues are published in dependency order (blockers first) so references are real. This is a **dependency declaration** for downstream consumption, not a runtime DAG — there is no execution engine that respects these dependencies automatically.

---

## 4. How Does Each Project Handle Parallel vs Sequential Execution?

### cc10x: Parallel Read-Only Agents + Sequential Write Agents + Optional DEBUG Fan-Out

cc10x has the most sophisticated parallelism model:

1. **BUILD parallel review+hunt:** `code-reviewer` and `silent-failure-hunter` are both read-only and safe to parallelize. The router marks both `in_progress` and invokes them in the same message. If parallel invocation fails, it falls back to sequential (reviewer first, then hunter) — "Never block a workflow because parallelism is unavailable."

2. **DEBUG fan-out (opt-in):** When multiple independent failures are detected, the router can fan out one `bug-investigator` per domain — but only after passing an **independence test** (separable understanding + disjoint files). A **fan-in conflict-check** runs after all investigators return: if any file was edited by two investigators, it reconciles before proceeding to the unified verifier.

3. **Write agents are always serialized:** "Only parallelize agents whose file-write surfaces do not overlap."

4. **Per-TASK fresh-implementer dispatch (pilot):** For phases with 3+ independent tasks sharing no in-flight state, the router can rotate a fresh builder per task within a phase. This is opt-in and explicitly gated.

### Superpowers: Serial Implementation + Parallel Debugging

- **`subagent-driven-development`:** Strictly serial. "Dispatch multiple implementation subagents in parallel (conflicts)" is a never-rule. One implementer per task, one reviewer per task, sequential.
- **`dispatching-parallel-agents`:** Explicitly for parallel dispatch of independent debugging problems. "Issue all three subagent dispatches in the same response — they run in parallel." The pattern is: identify independent domains, create focused tasks, dispatch in parallel, review and integrate. No independence test or conflict-check mechanism — it relies on the controller's judgment.

### Matt Pocock: N/A

No execution orchestration. Issues are published with dependencies; agents pick them up independently whenever they're ready.

---

## 5. How Does Each Project Handle Fallbacks When Things Go Wrong?

### cc10x: Multi-Layered Fallback System

cc10x has the most comprehensive fallback architecture:

1. **Circuit breaker:** Remediation tasks (`kind:remfix`) are capped at 3 cycles per workflow before requiring a human checkpoint.
2. **Change-something-before-re-dispatch:** Before any re-dispatch, the router MUST change at least one input: provide missing context, escalate model tier, shrink task scope, or escalate to human. "NEVER re-dispatch the same agent with the same model on the same unchanged input."
3. **Inline fallback mode:** When the Task/Agent primitive is unavailable or work is tightly coupled, the router executes phases inline in the main session — keeping all gates but losing subagent isolation.
4. **Model tier escalation:** Bug-investigator can escalate from `standard` to `capable` on a stubborn root cause.
5. **Scope escalation (trivial → full):** If a builder reports `SCOPE_INCREASES` or `BLOCKED_ITEMS` on a trivial build, the router promotes to the full graph (adds reviewer, hunter, doc-syncer).
6. **Verifier REVERT gate:** If the verifier emits `FAIL` with `REVERT`, the router asks the user whether to revert or create a fix task.
7. **FINDING_DISPUTED path:** A fix agent can dispute a reviewer finding only with a concrete `VERIFY_COMMAND` that proves the finding false. The independent verifier adjudicates.
8. **Parallel fallback:** If parallel invocation of reviewer+hunter fails, falls back to sequential.
9. **Research backend fallback:** Accelerated backend (Bright Data/Octocode) → built-in WebSearch/WebFetch → model's own analysis. Never aborts to BLOCKED while a fallback path exists.
10. **Contract override system:** If agent YAML is missing/malformed, treats as invalid output and re-runs inline verification. Rubber-stamp approvals (zero findings + <3 file:line citations) trigger fallback verification.

### Superpowers: Status-Based Handling + Model Escalation

1. **Implementer status handling:** Four statuses — DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED — each with a defined response.
2. **BLOCKED escalation ladder:** (1) provide more context, (2) re-dispatch with more capable model, (3) break into smaller pieces, (4) escalate to human. "Never ignore an escalation or force the same model to retry without changes."
3. **Review fix loop:** Reviewer finds issues → dispatch fix subagent → re-review → repeat until approved.
4. **Durable progress ledger:** After compaction, trust the ledger and `git log` over recollection. Prevents re-dispatching completed tasks.
5. **Reviewer ⚠️ items:** Requirements that can't be verified from the diff alone are flagged for the controller to resolve.

### Matt Pocock: Maintainer Override + Needs-Info Loop

1. **Maintainer override:** "The maintainer can override at any point — flag transitions that look unusual and ask before proceeding."
2. **`needs-info` loop:** Issues go to `needs-info`, wait for reporter response, then return to `needs-triage` for re-evaluation.
3. **Resuming sessions:** Read prior triage notes, check for reporter answers, present updated picture. "Don't re-ask resolved questions."
4. **Out-of-scope dedup:** The `.out-of-scope/` knowledge base prevents re-litigating rejected features.

---

## 6. What Orchestration Patterns Does cc10x Have That the Others DON'T?

| Pattern | Description |
| --------- | ------------- |
| **Router kernel as sole entry point** | A single skill owns all orchestration state, dispatch, validation, and remediation. Agents never self-orchestrate. |
| **Durable workflow artifact (JSON)** | A complete state machine persisted to `.cc10x/workflows/{uuid}.json` with 40+ fields including intent, phases, evidence, telemetry, convergence state, and remediation history. |
| **Event log (JSONL)** | Append-only audit trail at `.cc10x/workflows/{uuid}.events.jsonl` tracking every workflow event. |
| **Workflow UUID system** | Stable UUIDs generated independently of Claude task IDs, used as the canonical identifier everywhere. |
| **Task metadata contract** | Seven mandatory metadata lines (`wf:`, `kind:`, `origin:`, `phase:`, `plan:`, `scope:`, `reason:`) on every task, audited by hooks. |
| **Resume & hydration** | Full resume algorithm: stop-state hints, scope-decision markers, task reconstruction from metadata, stale `memory_task_id` detection. |
| **Memory system (3-file)** | `activeContext.md`, `progress.md`, `patterns.md` with auto-heal rules for missing sections, `JUST_GO` autonomous mode. |
| **Intent Readiness Gate** | Three conditions before PLAN/BUILD: context-bounded, contradiction-free, sufficiently specific. |
| **Plan Trust Gate** | Validates open decisions, plan mode, verification rigor, and constraint consistency before BUILD. |
| **Phase Exit Gate** | Per-phase completion validation before advancing `phase_cursor`. |
| **Complexity gradient** | Trivial (reduced graph: builder → verifier → memory) vs. standard (full graph) with automatic escalation. |
| **Silent failure hunter** | A dedicated agent that hunts edge cases and silent failures in parallel with the code reviewer. Neither Superpowers nor Matt Pocock has this role. |
| **Per-role model-tier policy** | Explicit tier recommendations per role with a reviewer floor — "never run a verifier on the cheapest tier." |
| **Contract override system** | Machine-readable YAML contracts from agents with per-agent override conditions (e.g., APPROVE + critical issues → CHANGES_REQUESTED). |
| **Anti-anchoring dispatch rules** | Read-only agents omit memory summaries to prevent bias. Self-check blocklist for dispatch prompts. |
| **Dispatch-by-reference** | Agents receive file paths, not pasted content. Reduces context bloat. |
| **Doc-syncer agent** | Dedicated agent for documentation synchronization after builds. |
| **Research orchestration** | Multi-backend research with capability model, loop caps, quality assessment, and fallback paths. |
| **Plan fresh-review loop** | Bounded 2-pass review DAG for plans with pruning of unused branches. |
| **BUILD-DONE finishing** | Optional git finishing menu (merge/PR/keep/discard) with merge-then-cleanup ordering invariant and git-guard approval tokens. |
| **Hook policy** | Plugin hooks (PreToolUse, PostToolUse, TaskCompleted, SessionStart, etc.) with block-mode artifact integrity guard. |
| **Circuit breaker + change-before-re-dispatch** | 3-cycle remediation cap + mandatory input change before any re-dispatch. |
| **FINDING_DISPUTED adjudication** | Evidence-gated dispute path with independent verifier adjudication. |
| **Scope resolution gate** | User decides between `critical only` vs `all issues` remediation scope. |
| **Fix-wave consolidation** | One REM-FIX per review pass, not per finding. |
| **Deferred findings roll-up** | Non-blocking minor findings accumulate and are surfaced at BUILD-DONE. |
| **Whole-branch final review** | Optional cross-phase review after all per-phase gates pass. |
| **Telemetry system** | Per-agent wall-clock timing, loop counters, verifier workload classification. |
| **Convergence state tracking** | `quality.convergence_state` transitions from `pending` → `needs_iteration` → `converged`. |
| **Traceability** | Requirement → phase → verification → remediation linkage arrays. |
| **ORIENT mode** | Read-only orientation that spawns no write agents and creates no phase graph. |
| **Re-review precondition gate** | REM-FIX must include covering tests, test command, and test output before re-review is allowed. |

---

## 7. What Orchestration Patterns Do the Others Have That cc10x DOESN'T?

| Pattern | Source | Description |
| --------- | -------- | ------------- |
| **Vertical-slice decomposition (tracer bullets)** | Matt Pocock `to-issues` | Breaking plans into thin end-to-end slices that cut through ALL integration layers, each independently demoable. cc10x has planner phases but not this explicit vertical-slice methodology. |
| **Out-of-scope knowledge base** | Matt Pocock `triage/OUT-OF-SCOPE.md` | Persistent records of rejected feature requests with concept-based dedup matching. cc10x has no equivalent institutional memory for rejected ideas. |
| **Issue-tracker-native workflow** | Matt Pocock (all skills) | Triage, issue creation, and PRD publishing happen on the project issue tracker — designed for human/agent collaboration across time. cc10x is session-native. |
| **Agent brief durability principles** | Matt Pocock `AGENT-BRIEF.md` | Briefs that survive codebase changes: describe interfaces not file paths, behavioral not procedural, durable over precision. cc10x's prompt scaffolds are session-scoped. |
| **AFK agent model** | Matt Pocock | Briefs written for agents that pick up work days/weeks later. cc10x assumes same-session execution. |
| **PRD synthesis from conversation** | Matt Pocock `to-prd` | No interview — just synthesize what's already discussed into a structured PRD. cc10x has no PRD concept. |
| **Seam-first testing strategy** | Matt Pocock `to-prd` | "Sketch the seams at which you'll test the feature. Use the highest seam possible. The fewer seams, the better." cc10x doesn't prescribe testing architecture. |
| **Domain glossary / ADR respect** | Matt Pocock (all skills) | Explicit instruction to use the project's domain glossary vocabulary and respect ADRs. cc10x has `patterns.md` but no domain glossary concept. |
| **Pre-flight plan conflict scan** | Superpowers SDD | Scan the plan once before Task 1 for tasks that contradict each other or global constraints, present as one batched question. cc10x has plan_trust_gate but not this specific pre-execution conflict scan. |
| **Continuous execution mandate** | Superpowers SDD | "Do not pause to check in with your human partner between tasks. Execute all tasks without stopping." cc10x has `JUST_GO` but it's more nuanced (never overrides failure-stop gates). |
| **Controller context preservation** | Superpowers SDD | Explicit design goal: subagents preserve the controller's context for coordination work. cc10x achieves this via dispatch-by-reference but doesn't frame it as a first-principle. |
| **File handoff discipline** | Superpowers SDD | Structured file naming convention: brief `task-N-brief.md` → report `task-N-report.md`, with fix dispatches appending to the same report file. cc10x uses artifact paths but not this paired naming convention. |

---

## 8. Orchestration Sophistication Ratings

### cc10x: 9/10

**Why:** cc10x is a full orchestration kernel with:

- A priority-matched intent routing table with 5 workflow types
- A deterministic agent dispatcher with 10+ named agents
- A durable workflow artifact (40+ field JSON state machine) + event log
- Full DAG-based task dependency management with `blockedBy`
- Parallel read-only agents with sequential write agents + optional DEBUG fan-out with independence test and conflict-check
- A 10-layer fallback system (circuit breaker, change-before-re-dispatch, inline mode, model escalation, scope escalation, REVERT gate, FINDING_DISPUTED, parallel fallback, research backend fallback, contract override)
- Per-role model-tier policy with reviewer floor
- Machine-readable agent contracts with override conditions
- Anti-anchoring dispatch rules with self-check blocklist
- Hook policy with block-mode artifact integrity guard
- Telemetry, convergence tracking, traceability, and deferred findings
- Resume & hydration with stop-state hints and scope-decision markers
- BUILD-DONE finishing with merge-then-cleanup invariant and git-guard tokens

**What keeps it from 10:** The sheer complexity creates a steep learning curve. The SKILL.md alone is 750+ lines with 7 reference files. The system is deeply coupled to Claude Code's Task primitives and `.cc10x/` state namespace. The model-tier policy is explicitly advisory ("mechanism honesty" — the router cannot actually set per-dispatch models). Some patterns (per-TASK fresh-implementer dispatch) are still pilot/opt-in.

### Superpowers: 6/10

**Why:** Superpowers has a solid but simpler orchestration model:

- Skill-driven routing (no central router, user/context picks the skill)
- Template-driven dispatch with model tier selection
- Sequential execution with per-task review gates
- Parallel dispatch for independent debugging problems (but no independence test or conflict-check)
- Status-based fallback handling with escalation ladder
- Durable progress ledger for compaction recovery
- File handoff discipline (task-brief, review-package scripts)
- Pre-flight plan conflict scan
- Continuous execution mandate

**What limits it:** No durable workflow state (just a flat ledger). No DAG — sequential only for implementation. No circuit breaker or remediation loop cap. No machine-readable agent contracts (relies on prose status reports). No anti-anchoring rules for dispatch prompts (though it does warn against pre-judging reviewers). No telemetry or convergence tracking. No resume/hydration system beyond the ledger. Parallel dispatch lacks formal independence verification. The model tier guidance is good but not enforced.

### Matt Pocock: 3/10

**Why:** Matt Pocock's skills are not execution orchestrators — they are **preparation and triage tools**:

- State machine for issue triage with 2 category roles + 5 state roles
- Vertical-slice decomposition for issue creation
- PRD synthesis from conversation
- Agent brief authoring with durability principles
- Out-of-scope knowledge base for institutional memory
- Maintainer-driven with override at any point
- `needs-info` loop for reporter interaction

**What limits it:** No agent dispatch, no runtime execution, no task graph, no parallel execution, no fallback system, no model selection, no contract validation, no telemetry, no resume logic. The orchestration is entirely human-mediated — the skills produce artifacts, they don't execute them. The sophistication is in the **preparation quality** (agent briefs, vertical slices, domain glossary respect), not in execution orchestration.

---

## Verdict: Who Wins Orchestration and Why

### **cc10x wins orchestration, decisively.**

cc10x is the only project that implements a **complete orchestration kernel** — a single entry point that owns routing, dispatch, dependency management, parallel/sequential execution, fallbacks, validation, state persistence, and resumption. It is an order of magnitude more sophisticated than Superpowers and two orders more than Matt Pocock in terms of execution orchestration.

**However, each project wins in its own domain:**

| Domain | Winner | Why |
| -------- | -------- | ----- |
| **Execution orchestration** | cc10x | Router kernel, DAG, parallel agents, 10-layer fallback, durable state |
| **Developer experience & simplicity** | Superpowers | Clear decision trees, template-driven dispatch, readable process, low ceremony |
| **Issue preparation & institutional memory** | Matt Pocock | Vertical-slice decomposition, agent briefs, out-of-scope KB, domain glossary, ADR respect |

**The ideal system** would combine cc10x's execution kernel with Matt Pocock's preparation methodology (vertical slices, durable briefs, out-of-scope KB) and Superpowers' developer-friendly ergonomics (clear decision trees, file handoff conventions, pre-flight conflict scans). cc10x already borrows some patterns from Superpowers (dispatch-by-reference, review-package, model tiers) but lacks Matt Pocock's preparation-layer sophistication.

---

## Detailed Comparison Table

| Feature | cc10x | Superpowers | Matt Pocock |
| --------- | ------- | ------------- | ------------- |
| Central router | ✅ Router kernel | ❌ Skill-driven | ❌ Manual |
| Intent routing table | ✅ 5 priorities | ❌ Decision trees | ❌ State machine |
| Agent dispatcher table | ✅ 10+ agents | ❌ Template-based | ❌ N/A |
| Model tier policy | ✅ Per-role + floor | ✅ Per-task | ❌ N/A |
| Durable workflow state | ✅ JSON artifact (40+ fields) | ⚠️ Flat ledger | ❌ N/A |
| Event log | ✅ JSONL audit trail | ❌ | ❌ N/A |
| Task DAG | ✅ `blockedBy` + artifact | ⚠️ Sequential todos | ⚠️ `Blocked by` in issues |
| Parallel execution | ✅ Read-only agents + DEBUG fan-out | ⚠️ Debugging only | ❌ N/A |
| Independence test | ✅ Separable + disjoint | ❌ | ❌ N/A |
| Conflict check | ✅ Fan-in file intersection | ❌ | ❌ N/A |
| Circuit breaker | ✅ 3-cycle cap | ❌ | ❌ N/A |
| Change-before-re-dispatch | ✅ Mandatory | ⚠️ Implicit | ❌ N/A |
| Inline fallback mode | ✅ 2 triggers | ❌ | ❌ N/A |
| Contract validation | ✅ YAML + override conditions | ⚠️ Prose status | ❌ N/A |
| Anti-anchoring rules | ✅ Self-check blocklist | ⚠️ Warnings only | ❌ N/A |
| Remediation loop | ✅ Re-review + re-hunt + re-verify | ⚠️ Fix loop | ❌ N/A |
| Resume & hydration | ✅ Multi-layer | ⚠️ Ledger recovery | ⚠️ Notes recovery |
| Telemetry | ✅ Per-agent + loop counts | ❌ | ❌ N/A |
| Convergence tracking | ✅ `convergence_state` | ❌ | ❌ N/A |
| Research orchestration | ✅ Multi-backend + fallback | ❌ | ❌ N/A |
| Plan fresh-review loop | ✅ 2-pass bounded DAG | ❌ | ❌ N/A |
| Doc sync | ✅ Dedicated agent | ❌ | ❌ N/A |
| Git finishing | ✅ Menu + merge invariant | ✅ Via finishing skill | ❌ N/A |
| Hook policy | ✅ Block-mode guards | ❌ | ❌ N/A |
| Silent failure hunter | ✅ Dedicated agent | ❌ | ❌ N/A |
| ORIENT mode | ✅ Read-only routing | ❌ | ❌ N/A |
| Vertical-slice decomposition | ❌ | ❌ | ✅ Tracer bullets |
| Agent brief durability | ⚠️ Session-scoped | ⚠️ Session-scoped | ✅ Durable, codebase-proof |
| Out-of-scope KB | ❌ | ❌ | ✅ Institutional memory |
| Issue-tracker integration | ❌ | ❌ | ✅ Native |
| Domain glossary respect | ⚠️ Optional (patterns.md) | ❌ | ✅ Explicit |
| Pre-flight conflict scan | ❌ | ✅ Batched question | ❌ |
| Continuous execution | ✅ `JUST_GO` mode | ✅ Explicit mandate | ❌ N/A |
| File handoff convention | ✅ Artifact paths | ✅ Paired naming | ✅ Briefs |
| **Score** | **9/10** | **6/10** | **3/10** |
