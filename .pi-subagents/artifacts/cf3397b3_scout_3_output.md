# Deep Comparison 09: Agent Architecture & Dispatch Patterns

## Projects Compared

| Project | Agent Count | Architecture Style | Dispatch Model |
| --------- | ------------- | ------------------- | ---------------- |
| **cc10x** | 9 agents (planner, bug-investigator, component-builder, code-reviewer, silent-failure-hunter, integration-verifier, doc-syncer, plan-gap-reviewer, researcher) | Plugin-native agents with frontmatter + machine-readable router contracts | Router-owned dispatch via `TaskCreate`/`TaskUpdate`; agents are peers, not subagents |
| **Superpowers** | 3 agent roles (implementer, task-reviewer, code-reviewer) — all general-purpose subagents dispatched from a controller skill | Skill-driven prompt templates; no native agent definitions | Inline `Subagent()` dispatch from a controller session (the SKILL.md orchestrates) |
| **Matt Pocock (triage)** | 0 persistent agent definitions; 1 skill that plays 5 state-machine roles inline | Skill-as-agent; state-machine roles with human-in-the-loop gates | Human-invoked `/triage` command; no subagent dispatch at all |

---

## 1. How Does Each Project Define Agents?

### cc10x — Frontmatter + System Prompt + Skills + Router Contract

Each agent is a `.md` file in `plugins/cc10x/agents/` with:

- **YAML frontmatter:** `name`, `description`, `model` (inherit or haiku), `color`, `effort`, `tools` (explicit allowlist), `skills` (cc10x skill dependencies)
- **System prompt body:** Markdown sections defining core posture, mode (READ-ONLY / mutation), process steps, decision checkpoints, loop caps, anti-anchoring rules
- **Router Contract:** Machine-readable YAML block at the end — `STATUS`, `CONFIDENCE`, `SCENARIOS`, `BLOCKING`, `NEXT_ACTION`, `MEMORY_NOTES`, etc. This is the agent's output contract, not just a prompt — the router parses it programmatically.
- **Contract Rules:** Explicit boolean conditions that gate each STATUS value (e.g., `STATUS=PASS` requires `TDD_RED_EXIT=1`, `BUILD_PREFLIGHT_EMITTED=true`, etc.)

**Key design property:** Tools are scoped per agent. READ-ONLY agents (code-reviewer, silent-failure-hunter, integration-verifier, plan-gap-reviewer) deliberately omit `Edit`/`Write` from their tool list. Mutation agents (component-builder, bug-investigator, doc-syncer) include them. The `researcher` agent has `WebFetch`/`WebSearch` but no `Grep`/`Glob` — it's a web research specialist, not a codebase explorer.

### Superpowers — Prompt Templates (No Native Agent Definitions)

Superpowers defines **no agent files**. Agents are created at dispatch time via prompt templates:

- **implementer-prompt.md:** A template the controller fills with `[BRIEF_FILE]`, `[REPORT_FILE]`, context, and model selection. The dispatched agent is `general-purpose` — it has no specialized identity until the prompt gives it one.
- **task-reviewer-prompt.md:** Same pattern — a general-purpose subagent given a reviewer identity via prompt content. Includes spec compliance + code quality dual verdict.
- **code-reviewer.md:** A broader review template for the final whole-branch review. Also general-purpose.

**Key design property:** There are no `.agents/` files with frontmatter or tool restrictions. The `.agents/plugins/marketplace.json` is a plugin manifest, not agent definitions. All agent specialization lives in the prompt text, not in declarative configuration.

### Matt Pocock — Skill-as-Agent with State-Machine Roles

The triage skill has:

- **SKILL.md frontmatter:** `name`, `description`, `disable-model-invocation: true` — meaning the skill can't be self-invoked by the model; it requires explicit `/triage` command.
- **Roles, not agents:** Two category roles (`bug`, `enhancement`) and five state roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). These are states in a state machine, not separate agent definitions.
- **AGENT-BRIEF.md:** A reference document (not an agent definition) describing how to write durable briefs for AFK agents. It's a spec for the *output* of triage, not the triage agent itself.
- **OUT-OF-SCOPE.md:** A reference for the `.out-of-scope/` knowledge base — institutional memory for rejected features.

**Key design property:** There is exactly one "agent" — the triage skill itself, played by the current session. There are no subagents. The AFK agents that consume the briefs are out-of-scope of this skill.

---

## 2. How Does Each Project Dispatch Agents?

### cc10x — Router-Owned Dispatch via TaskCreate/TaskUpdate

cc10x uses a central **router** (not directly visible in the agent files, but referenced throughout) that:

- Creates tasks via `TaskCreate` and assigns them to specific named agents
- Tracks `git_base_sha` per phase for diff scoping
- Dispatches agents in parallel (e.g., code-reviewer + silent-failure-hunter run concurrently)
- Reads agent output contracts and makes routing decisions (REM-FIX, re-plan, advance phase)
- Handles all task completion — some agents call `TaskUpdate` directly, others rely on router fallback
- Passes context to agents via structured prompt sections (`## Pre-Answered Requirements`, `## Intent Contract`, `## Previous Agent Findings`, `## Task Context`)

**Dispatch evidence from agent files:**

- code-reviewer: "Router reads envelope first; falls back to heading scan if malformed"
- bug-investigator: "Router spawns `cc10x:researcher` in parallel and re-invokes you with research file paths"
- integration-verifier: "Your prompt includes findings from code-reviewer and silent-failure-hunter under `## Previous Agent Findings`"
- plan-gap-reviewer: "Router owns all workflow decisions. Do not create tasks or call TaskUpdate."

### Superpowers — Inline Subagent() Dispatch from Controller Session

The SKILL.md orchestrates dispatch:

- Controller reads the plan once, creates todos for all tasks
- Per task: dispatches an implementer subagent via `Subagent(general-purpose)` with the filled template
- After implementer reports DONE: runs `scripts/review-package BASE HEAD`, dispatches task-reviewer subagent
- If reviewer finds issues: dispatches a fix subagent, re-reviews
- After all tasks: dispatches final code-reviewer subagent for whole-branch review
- Uses `scripts/task-brief PLAN_FILE N` to extract task text into a file (keeps it out of context)
- Uses `scripts/review-package BASE HEAD` to create diff packages for reviewers

**Key dispatch properties:**

- Model selection is explicit per dispatch (cheap model for mechanical tasks, capable model for judgment)
- Everything moves as files, not pasted text (brief files, report files, diff packages)
- The controller is the orchestrator — it constructs exactly what each subagent needs
- No parallel dispatch of implementers (they conflict); reviewers are sequential

### Matt Pocock — No Dispatch (Human-Invoked Command)

- The maintainer runs `/triage` with a natural language description
- The triage skill itself performs all roles — it doesn't dispatch subagents
- State transitions happen inline: gather context → recommend → verify → grill → apply outcome
- The "agent" that eventually consumes the brief is external to this skill — the brief is written *for* an AFK agent, but the triage skill doesn't dispatch it
- Human gates: "Wait for direction" after recommending, "ask the maintainer before proceeding" on unusual transitions

---

## 3. What Agent Specialization Patterns Does Each Project Use?

### cc10x — Deep Role Specialization with Enforced Boundaries

| Agent | Specialization Pattern | Boundary Enforcement |
| ------- | ---------------------- | --------------------- |
| planner | Agreement-first planning, 3 plan modes (direct/execution_plan/decision_rfc), verification rigor levels | READ-ONLY for code; writes only to `docs/plans/`; never calls `EnterPlanMode` |
| bug-investigator | Evidence-first debugging with mandatory feedback loop gate, boundary instrumentation matrix, variant scan, anti-hardcode gate | TDD-enforced; loop cap at 3 hypotheses; must return BLOCKED if can't build repro |
| component-builder | TDD execution (RED→GREEN→REFACTOR) with BUILD_PREFLIGHT gate, phase contract enforcement | Phase-scoped only; deviation discipline stops out-of-scope work; loop caps |
| code-reviewer | Adversarial multi-pass review (security→performance→quality→friction→plan validity→spec compliance) with HARD/SOFT signal scoring | READ-ONLY; confidence ≥80 threshold; zero-finding gate; anti-anchoring (no activeContext.md) |
| silent-failure-hunter | Zero-tolerance error-handling audit with language-specific red flags, severity rubric | READ-ONLY; no self-healing; output-only; coverage truthfulness gate |
| integration-verifier | E2E validation with proof reconciliation (truths+artifacts+wiring), test honesty gates, claim extraction from prior agents | READ-ONLY; independent auditor posture; environment escape hatch |
| doc-syncer | Diff-driven documentation sync across 3 layers (business/technical/audit) with impact classification | Mutation but scoped to docs; shell safety rules; self-review before contract |
| plan-gap-reviewer | Fresh anti-anchoring plan review against codebase reality | READ-ONLY; no memory files loaded; no task creation; findings-only |
| researcher | Web/GitHub research with capability ladder (Bright Data → Octocode → WebSearch → WebFetch) | Writes only to `docs/research/`; quality-level classification; source tracking |

**Specialization mechanisms:**

1. **Tool allowlists** — READ-ONLY agents literally cannot mutate code
2. **Skills dependencies** — each agent declares which cc10x skills it needs (e.g., `cc10x:code-review`, `cc10x:debugging`)
3. **Process ordering** — agents have numbered steps with "never skip, never reorder"
4. **Loop caps** — hard limits on retries before forced escalation
5. **Decision checkpoints** — explicit triggers that force return-to-router (e.g., "Changing >3 files not in plan → FAIL")
6. **Contract rules** — boolean conditions that gate STATUS values, enforced by the router

### Superpowers — Context-Scoped Generalists with Dual Verdicts

Superpowers uses **one general-purpose agent type** with three specializations applied via prompt:

1. **Implementer:** Focused on one task from a brief. Self-review before reporting. Status contract (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT). Escalation is encouraged ("It is always OK to stop and say 'this is too hard for me'").
2. **Task reviewer:** Dual verdict — spec compliance (✅/❌/⚠️) + code quality (Critical/Important/Minor). "Do not trust the report" posture. Diff-file-based review (not raw git commands).
3. **Final code reviewer:** Broader scope — plan alignment, architecture, production readiness, backward compatibility.

**Specialization mechanisms:**

1. **Prompt content** — the entire identity comes from the template
2. **Model selection** — cheap/standard/capable tiers per task complexity
3. **File handoffs** — brief files, report files, diff packages keep context controlled
4. **Controller curation** — "you construct exactly what they need"
5. **Status contract** — four statuses with explicit handling rules

### Matt Pocock — State-Machine Role Switching

The triage skill plays multiple roles in sequence:

1. **Categorizer:** bug vs enhancement
2. **Investigator:** redundancy check (already implemented?), prior rejection check (`.out-of-scope/`)
3. **Verifier:** reproduce bugs, confirm PR diffs
4. **Griller:** `/grilling` + `/domain-modeling` to flesh out vague requests
5. **Brief writer:** produce agent-ready briefs following AGENT-BRIEF.md format
6. **State manager:** apply labels, post comments, close issues

**Specialization mechanisms:**

1. **State machine** — explicit state transitions with role labels
2. **Reference docs** — AGENT-BRIEF.md and OUT-OF-SCOPE.md as companion specs
3. **Human gates** — "wait for direction" after recommendation
4. **Durability principles** — briefs describe interfaces not file paths, behavior not procedure

---

## 4. How Does Each Project Handle Agent Completion?

### cc10x — Machine-Readable Router Contracts + Memory Persistence

**Completion mechanism:** Every agent emits a YAML "Router Contract" block that the router parses programmatically. Key fields:

- `STATUS` — the primary verdict (PASS/FAIL, FIXED/INVESTIGATING/BLOCKED, PLAN_CREATED/NEEDS_CLARIFICATION, etc.)
- `BLOCKING` — boolean, whether this blocks workflow advance
- `NEXT_ACTION` — what the router should do next (review/remediation/clarify/abort)
- `CONFIDENCE` — 0-100 numeric confidence
- `SCENARIOS` — structured Given/When/Then with command/expected/actual/exit_code
- `MEMORY_NOTES` — learnings, patterns, verification, deferred items
- `REMEDIATION_NEEDED` / `REQUIRES_REMEDIATION` / `REMEDIATION_REASON`
- `GATE_PASSED` — whether internal review gate passed

**Contract rules** enforce that the STATUS is backed by evidence:

- `STATUS=PASS` requires `TDD_RED_EXIT=1`, `BUILD_PREFLIGHT_EMITTED=true`, ≥1 passing scenario
- `STATUS=FIXED` requires `FEEDBACK_LOOP.rung != "none"`, `DEBUG_CLOSEOUT.instrumentation_removed=true`
- `STATUS=NEEDS_CLARIFICATION` requires `BLOCKING=true` and `REMEDIATION_REASON` populated

**Memory persistence:** Three memory files (`.cc10x/activeContext.md`, `.cc10x/patterns.md`, `.cc10x/progress.md`) are the institutional memory. Agents read specific files based on their role. The router persists memory at workflow-final, not per-agent.

**Task completion:** Some agents call `TaskUpdate` directly (planner, bug-investigator, component-builder, doc-syncer, researcher). Others (code-reviewer, silent-failure-hunter, integration-verifier, plan-gap-reviewer) rely on the router's fallback completion — "the router handles task completion automatically."

### Superpowers — Status Contract + Report Files + Progress Ledger

**Completion mechanism:** The implementer reports one of four statuses (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT) with a short summary. The full report goes to a file.

**Reviewer completion:** The task reviewer returns two verdicts:

- Spec compliance: ✅ / ❌ / ⚠️ (cannot verify from diff)
- Task quality: Approved / Needs fixes

**Progress tracking:** A durable ledger file at `.superpowers/sdd/progress.md`:

```markdown
Task N: complete (commits <base7>..<head7>, review clean)
```

This survives context compaction — the controller checks it before dispatching any task to avoid re-dispatching completed work.

**File-based handoffs:** Reports go to files, not into the controller's context. The controller reads only the status line and commits, not the full report.

### Matt Pocock — Human-Gated State Transitions + Brief Artifacts

**Completion mechanism:** The triage skill doesn't have a programmatic completion contract. Instead:

1. The skill recommends a state → human confirms
2. The skill applies the outcome (post brief, post triage notes, close issue)
3. The outcome IS the completion — a posted brief, a posted needs-info comment, or a closed issue

**Brief as completion artifact:** The AGENT-BRIEF.md template defines the output contract:

- Category, Summary, Current behavior, Desired behavior, Key interfaces, Acceptance criteria, Out of scope
- Acceptance criteria are checkboxes — independently verifiable
- Durability principles ensure the brief stays valid as the codebase changes

**No programmatic parsing:** There's no machine-readable contract. The maintainer reads the output and makes decisions. The brief is written for a future AFK agent, not for a router.

---

## 5. Anti-Anchoring Patterns — How Does Each Project Prevent Agent Bias?

### cc10x — Multi-Layered Anti-Anchoring

cc10x has the most deliberate anti-anchoring architecture:

1. **Explicitly forbidden memory files:** code-reviewer and silent-failure-hunter are told to NOT read `.cc10x/activeContext.md` — "It contains the implementer's own narrative... reading the author's self-assessment before an adversarial review anchors the verdict."
2. **Plan-gap-reviewer freshness rule:** "Stay context-clean and anti-anchored. Do NOT load `.cc10x/*.md`. Do NOT infer authority from prior planner confidence."
3. **Integration-verifier claim extraction:** "before running any test, list every factual claim from prior agents. Mark each UNVERIFIED. During verification, update to VERIFIED, CONTRADICTED, or UNVERIFIABLE."
4. **Code-reviewer self-grading prohibition:** "A stated design rationale from the implementer... is the implementer grading their own work. It is NOT external evidence and MUST NOT downgrade a finding's severity."
5. **Code-reviewer verdict-before-prose rule:** "Decide the verdict BEFORE writing the final response — then state it first." Prevents reverse-engineering a verdict from prose.
6. **Code-reviewer zero-finding gate:** If zero findings, must verify with positive assertions and cap confidence at 70 — prevents rubber-stamp approvals.
7. **Independent auditor posture:** Integration-verifier: "A reviewer approval, green unit test, or builder claim is never sufficient by itself for PASS."
8. **Forbidden language:** code-reviewer bans "looks fine", "LGTM", "ship it", "no major issues" — verdict-softeners that bypass the confidence system.
9. **Bug-investigator hypothesis gate:** "A hypothesis without a repro loop is a guess." Must build evidence before forming hypotheses.

### Superpowers — Controller-as-Buffer + "Do Not Trust the Report"

1. **Fresh subagent per task:** "They should never inherit your session's context or history — you construct exactly what they need." The controller is a context firewall.
2. **"Do not trust the report" directive:** The task reviewer template explicitly says: "Treat the implementer's report as unverified claims... It may be incomplete, inaccurate, or optimistic."
3. **Design rationale as claim:** "Design rationales in the report are claims too: 'left it per YAGNI'... Judge the code on its merits — a stated rationale never downgrades a finding's severity."
4. **Controller pre-judging prohibition:** "Do not pre-judge findings for the reviewer — never instruct a reviewer to ignore or not flag a specific issue."
5. **Diff-file-based review:** Reviewers read a pre-built diff package, not raw git output — the controller controls what the reviewer sees.
6. **No accumulated history in dispatches:** "Do not paste accumulated prior-task summaries into later dispatches."
7. **Self-review before external review:** Implementers self-review first, but self-review explicitly does NOT replace external review: "Let implementer self-review replace actual review" is a red flag.

### Matt Pocock — Codebase-First Anti-Anchoring

1. **Redundancy check:** Before triaging, search the codebase for existing implementations — "search for an existing implementation of the requested behavior by domain concept (not just the request's wording)."
2. **Prior rejection check:** Read `.out-of-scope/*.md` to surface prior rejections — prevents re-litigating settled decisions.
3. **Verify the claim:** "Before any grilling, check that the claim holds up. For a bug, reproduce it from the reporter's steps."
4. **Durability over precision:** Briefs describe interfaces not file paths, behavior not procedure — prevents anchoring to a specific code structure that may change.
5. **Parse prior triage notes:** "Read them, check whether the reporter has answered any outstanding questions" — prevents re-asking resolved questions (a form of anchoring to stale state).

---

## 6. What Agent Patterns Does cc10x Have That the Others DON'T?

| Pattern | cc10x | Superpowers | Matt Pocock |
| --------- | ------- | ------------- | ------------- |
| **Machine-readable router contracts** (YAML output blocks parsed by router) | ✅ Every agent | ❌ Status strings only | ❌ Human-readable only |
| **Contract rules** (boolean conditions gating STATUS values) | ✅ Explicit per agent | ❌ | ❌ |
| **Parallel agent dispatch** (code-reviewer + silent-failure-hunter simultaneously) | ✅ Router-managed | ❌ Sequential only | ❌ No dispatch |
| **Tool allowlists per agent** (READ-ONLY enforced by tool omission) | ✅ Frontmatter `tools` | ❌ General-purpose has all tools | ❌ N/A |
| **Skills dependencies** (each agent declares required skills) | ✅ Frontmatter `skills` | ❌ | ❌ |
| **Feedback loop gate** (bug-investigator's 10-rung repro ladder) | ✅ Unique to bug-investigator | ❌ | ❌ |
| **Boundary instrumentation matrix** (multi-component debugging) | ✅ Unique to bug-investigator | ❌ | ❌ |
| **Test honesty gates** (integration-verifier's false-green detection) | ✅ 7 grep-based gates | ❌ | ❌ |
| **Proof reconciliation** (truths + artifacts + wiring) | ✅ integration-verifier | ❌ | ❌ |
| **Plan-vs-code spec compliance** (MISSING/EXTRA/MISUNDERSTOOD buckets) | ✅ code-reviewer Pass 6 | ✅ task-reviewer Part 1 | ❌ |
| **PLAN_DEFECT routing** (plan is wrong → route to planner, not code fix) | ✅ code-reviewer | ❌ | ❌ |
| **CANNOT_VERIFY_CROSS_PHASE reconciliation** | ✅ code-reviewer + router | ✅ ⚠️ items in task-reviewer | ❌ |
| **Multi-signal scoring** (HARD/SOFT dimension scores, min(HARD) capped by avg(SOFT)) | ✅ code-reviewer | ❌ | ❌ |
| **Zero-finding gate** (must produce positive assertions if zero findings) | ✅ code-reviewer | ❌ | ❌ |
| **Debug attempt tracking** (activeContext.md with [DEBUG-N] entries, loop cap) | ✅ bug-investigator | ❌ | ❌ |
| **BUILD_PREFLIGHT token** (hook-greped token before first mutation) | ✅ component-builder | ❌ | ❌ |
| **Self-review gate** (planner scans for cross-phase contract drift) | ✅ Step 11b | ❌ | ❌ |
| **Plan review gate** (automated skill invocation for plan validation) | ✅ planner Step 15 | ❌ | ❌ |
| **Defense-in-depth** (bug-investigator makes bug class structurally impossible) | ✅ Step 11b | ❌ | ❌ |
| **Regression seam discipline** (no shallow tests) | ✅ bug-investigator | ❌ | ❌ |
| **Coverage gate** (coverage-thresholds.json check) | ✅ component-builder | ❌ | ❌ |
| **Doc-driven impact classification** (none/low/medium/high across 3 layers) | ✅ doc-syncer | ❌ | ❌ |
| **Research capability ladder** (Bright Data → Octocode → WebSearch → WebFetch) | ✅ researcher | ❌ | ❌ |
| **Effort levels in frontmatter** (high/medium per agent) | ✅ | ❌ | ❌ |
| **Color coding** (visual distinction in UI) | ✅ | ❌ | ❌ |
| **Forbidden language list** (banned verdict-softeners) | ✅ code-reviewer | ❌ | ❌ |
| **Loop caps with forced escalation** (3 strikes → BLOCKED) | ✅ Multiple agents | ❌ | ❌ |
| **Variant scan** (locale/i18n, config, roles, platform, etc.) | ✅ bug-investigator | ❌ | ❌ |

---

## 7. What Agent Patterns Do the Others Have That cc10x SHOULD Adopt?

### From Superpowers

| Pattern | Description | Why cc10x Should Adopt |
| --------- | ------------- | ---------------------- |
| **Model selection per dispatch** | Explicit cheap/standard/capable tier selection based on task complexity signals | cc10x agents use `model: inherit` or `model: haiku` — no per-dispatch model selection. The router could save cost by matching model capability to task complexity. |
| **Turn-count cost analysis** | "Turn count beats token price. Wall-clock and context cost scale with how many turns a subagent takes" | cc10x doesn't account for turn economics. A cheaper model that takes 3× turns costs more overall. This is a real cost optimization insight. |
| **File-based context handoffs** | Brief files, report files, diff packages — everything moves as files, not pasted text | cc10x agents communicate via structured prompt sections and router contracts, but there's no evidence of file-based handoff artifacts. Superpowers' approach keeps the controller's context clean. |
| **Durable progress ledger** | `.superpowers/sdd/progress.md` survives context compaction; lists completed tasks with commit SHAs | cc10x has `.cc10x/progress.md` but it's written by the router at workflow-final, not as a real-time recovery map. Superpowers' ledger is checked before every dispatch to prevent re-dispatching completed work — a real failure mode. |
| **Pre-flight plan review** | Scan plan once for conflicts before execution starts; batch all findings to user | cc10x's plan-gap-reviewer does a fresh review, but it's a separate agent dispatched after plan creation. Superpowers does this as a quick controller-side scan before dispatching Task 1 — lighter weight. |
| **"Never dispatch without a diff file"** | Reviewers always get a pre-built diff package, never raw git commands | cc10x's code-reviewer runs git commands itself. Superpowers' approach is cleaner — the controller builds the package once, the reviewer just reads it. |
| **Anti-pre-judging in dispatch prompts** | Explicit prohibition: "never instruct a reviewer to ignore or not flag a specific issue" | cc10x doesn't have this as a dispatch-level discipline. The router could inadvertently bias reviewers by how it frames their task. |
| **ONE fix subagent for all findings** | "Dispatch ONE fix subagent with the complete findings list — not one fixer per finding" | cc10x creates REM-FIX tasks but it's unclear whether it batches. Per-finding fixers each rebuild context — expensive. |
| **"While you work" escalation** | Implementers can pause mid-work to ask questions, not just before starting | cc10x agents have decision checkpoints but they return to the router, not to the user. Superpowers allows real-time clarification. |
| **Continuous execution mandate** | "Do not pause to check in with your human partner between tasks" | cc10x has HITL checkpoints per phase, which may be more conservative than needed for low-risk phases. |

### From Matt Pocock

| Pattern | Description | Why cc10x Should Adopt |
| --------- | ------------- | ---------------------- |
| **Durability over precision in specs** | Briefs describe interfaces/types/behavior, not file paths or line numbers | cc10x's planner does write file paths in phases, which can go stale. The Matt Pocock principle of "interfaces not paths" would make plans more resilient to codebase changes between planning and execution. |
| **`.out-of-scope/` knowledge base** | Persistent records of rejected features with dedup checking | cc10x has `.cc10x/patterns.md` for gotchas, but no structured mechanism for recording *rejected approaches*. An "out-of-scope" or "rejected-approaches" directory would prevent re-litigating settled architectural decisions. |
| **Redundancy check before triage** | "Search for an existing implementation of the requested behavior by domain concept" | cc10x's planner does a "Codebase Reality Check" but doesn't explicitly search for existing implementations of the *requested behavior* before planning. This could catch "already built" cases earlier. |
| **State machine for issue/workflow states** | Explicit states with transitions, roles, and human gates | cc10x has workflow phases but they're linear. Matt Pocock's state machine (with needs-info → needs-triage cycling) handles non-linear flows like clarification loops more naturally. |
| **Acceptance criteria as checkboxes** | Independently verifiable, testable criteria in the brief | cc10x has "exit criteria" per phase but they're prose. Checkboxes with specific testable criteria would make verification more concrete. |
| **Domain glossary respect** | "Explore the codebase using the project's domain glossary, respecting ADRs" | cc10x's planner reads ADRs as constraints, but doesn't explicitly reference a domain glossary. A shared domain vocabulary would improve cross-agent communication. |

---

## 8. Rate Each Project's Agent Architecture 1-10

### cc10x: 8.5/10

**Strengths:**

- Most sophisticated agent architecture of the three — 9 specialized agents with enforced boundaries, machine-readable contracts, and boolean contract rules
- Tool-level enforcement of READ-ONLY vs mutation agents
- Deep anti-anchoring patterns (forbidden memory files, verdict-before-prose, claim extraction)
- Parallel agent dispatch (code-reviewer + silent-failure-hunter)
- Multi-signal scoring with HARD/SOFT dimensions
- Comprehensive verification gates (test honesty, proof reconciliation, zero-finding gate)
- Feedback loop gate and boundary instrumentation for debugging
- Skills dependencies create a clean dependency graph

**Weaknesses:**

- No per-dispatch model selection (all `model: inherit` or `model: haiku`) — misses cost optimization
- No file-based context handoffs — context grows linearly with agent count
- No durable real-time progress ledger (memory written at workflow-final, not per-task)
- Contract complexity is high — the YAML blocks are verbose and may be hard to maintain
- No "out-of-scope" knowledge base for rejected approaches
- No redundancy check (is this already built?) before planning
- Plans reference specific file paths that can go stale

### Superpowers: 7.0/10

**Strengths:**

- Elegant simplicity — 3 prompt templates, no agent files, no router contracts
- Excellent context management — file-based handoffs keep controller context clean
- Per-dispatch model selection with explicit cost/turn analysis
- Durable progress ledger that survives compaction
- "Do not trust the report" anti-anchoring is effective and simple
- Controller-as-firewall pattern (fresh subagent, curated context)
- Pre-flight plan review catches conflicts early
- Clear status contract (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT)
- Anti-pre-judging discipline in dispatch prompts

**Weaknesses:**

- No machine-readable contracts — the controller must parse prose
- No tool-level enforcement (general-purpose agents have all tools)
- No parallel agent dispatch (sequential only)
- No specialized agents — every subagent is general-purpose with a prompt
- No multi-signal scoring or confidence system
- No test honesty gates or proof reconciliation
- No feedback loop gate for debugging
- No skills dependency graph
- No contract rules gating status values

### Matt Pocock: 5.5/10

**Strengths:**

- State machine is a clean mental model for issue triage
- Durability over precision is an excellent spec-writing principle
- `.out-of-scope/` knowledge base is a unique institutional memory pattern
- Redundancy check prevents wasted work on already-built features
- Human gates prevent autonomous mistakes
- Acceptance criteria as checkboxes are concrete and verifiable
- AGENT-BRIEF.md is an excellent spec template for AFK agents

**Weaknesses:**

- No agent architecture at all — it's a skill, not an agent system
- No subagent dispatch — everything happens in one session
- No machine-readable contracts
- No tool restrictions
- No anti-anchoring for code review (it's not a code review tool)
- No parallel execution
- No verification gates or test honesty checks
- No model selection
- No progress tracking beyond GitHub issue labels
- Limited to triage — not a general-purpose agent architecture

---

## Verdict

**cc10x has the most production-grade agent architecture**, with enforcement at every layer: tools, contracts, anti-anchoring, verification, and memory. It's the only system that can run multiple specialized agents in parallel with machine-readable output contracts that a router can programmatically act on.

**Superpowers has the best orchestration ergonomics** — its file-based handoffs, per-dispatch model selection, and durable progress ledger solve real operational problems that cc10x hasn't addressed. cc10x should adopt these patterns.

**Matt Pocock contributes two unique ideas**: the `.out-of-scope/` institutional memory pattern and the durability-over-precision spec-writing principle. Both are lightweight additions that would improve cc10x's planning quality.

### Top 5 Recommendations for cc10x

1. **Add per-dispatch model selection** — match model capability to task complexity (from Superpowers)
2. **Add file-based context handoffs** — brief files, report files, diff packages keep router context clean (from Superpowers)
3. **Add a durable real-time progress ledger** — checked before every dispatch to prevent re-dispatching completed work (from Superpowers)
4. **Add an "out-of-scope" / "rejected-approaches" knowledge base** — prevent re-litigating settled architectural decisions (from Matt Pocock)
5. **Shift plan file references from paths to interfaces** — make plans resilient to codebase changes between planning and execution (from Matt Pocock)