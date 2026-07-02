# cc10x v12.0 — "The Loop Engine" Refactoring Plan (Validated against Claude Code v2.1.198)

> **For Claude:** This plan was validated against the live Claude Code documentation (v2.1.198, June 2026). Every assumption has been checked against the actual hooks reference, skills docs, sub-agent docs, and plugins reference. The plan is harmonized with Claude Code's native capabilities — it uses native frontmatter fields, native hook types, native skill features, and aligns with bundled skills.

**Goal:** Transform cc10x from a bloated legacy harness into the world's leanest, most powerful Claude Code harness — built for Claude Code only, leveraging every native capability the platform offers.

**Architecture:** Keep the 4-layer design (router → skills → agents → hooks). Compress every layer. Move declarative fields from prose to frontmatter. Replace Python scripts with native hook types where possible. Align with bundled skills. Trust modern Claude.

**Tech Stack:** Claude Code native hooks (command + http + agent + prompt types), Markdown/YAML (skills + agents), JSON (workflow artifacts + config). Minimal Python — only for logic that can't be expressed declaratively.

**Prerequisites:** Current cc10x v11.1.0 installed and functional. Git branch `v12-refactor` created from `main`. Claude Code v2.1.198+.

**Durable Decisions:**

- **Zero regression principle:** Every cut must be verified against current behavior. If a skill teaches Claude something it wouldn't know without the skill, it stays. If a skill teaches Claude something it already knows, it goes.
- **Fable 5 alignment:** "Skills developed for prior models are often too prescriptive and can degrade output quality." Modern Claude needs constraints, not procedures. Brevity instructions replace enumerated patterns. Fresh-context verifier subagents replace self-critique.
- **Keynote thesis:** The harness is a *loop engine* — plan → build → verify → learn, with durable state, fresh-context verification, and memory that persists. Claude Code now has native /goal, /loop, and dynamic workflows — the plan aligns with these.
- **Token budget (CORRECTED):** Skills are LAZY-LOADED — "a skill's body loads only when it's used, so long reference material costs almost nothing until you need it." The real always-loaded cost is just the router. Optimization priority: (1) router (always loaded, target ~8K from ~30K), (2) frequently-invoked skills (moderate compression), (3) reference files (low priority — on-demand), (4) agent prompts (only when spawned).
- **Claude Code native:** Use native frontmatter (effort, maxTurns, memory, background, skills, isolation). Use native hook types (agent-based for fresh-context verification, http for logging). Use dynamic context injection (!`command`) in skills. Align with bundled /debug, /code-review, /loop, /run, /verify.
- **Plugin agent constraints:** Plugin agents CANNOT have hooks, mcpServers, or permissionMode in frontmatter. Supported fields: name, description, model, effort, maxTurns, tools, disallowedTools, skills, memory, background, isolation. Plan accordingly.

---

## Claude Code v2.1.198 Capability Map (Validation Reference)

### Hook events available (31 events)

cc10x v11 uses 10. New events to consider: **UserPromptSubmit**, **SubagentStart**, **PostToolBatch**, **PostToolUseFailure**, **FileChanged**, **TaskCreated**, **SessionEnd**, **Setup**.

### Hook types available (5 types)

cc10x v11 uses only `command`. New types:

- **http:** POST event JSON to URL — no Python process startup for logging
- **mcp_tool:** Call MCP server tool — use Bright Data, MongoDB, etc. in hooks
- **prompt:** Evaluate prompt with LLM — lightweight semantic checks
- **agent:** Run agentic verifier with tools — **THIS IS FRESH-CONTEXT VERIFICATION** (Fable 5 recommends this over self-critique)

### Skill features available

- **Dynamic context injection:** `!`command`` — Claude Code runs command and injects output before Claude sees skill content
- **Lazy loading:** Skill body loads only when used — reference files are free until needed
- **Subagent execution:** Skills can run in their own subagent context
- **Frontmatter:** description, disable-model-invocation, name, etc.
- **Arguments:** $ARGUMENTS placeholder
- **Pre-approve tools:** Tools can be pre-approved per-skill

### Agent frontmatter available (plugin agents)

name, description, model, effort, maxTurns, tools, disallowedTools, skills, memory, background, isolation
**NOT supported:** hooks, mcpServers, permissionMode

### Bundled skills (overlap with cc10x)

/debug, /code-review, /loop, /run, /verify, /claude-api, /batch

### New platform features (Week 13-26, 2026)

- **/goal:** Work across turns until completion condition holds
- **/loop:** Self-paced loop (bundled skill)
- **Dynamic workflows:** Orchestrate dozens to hundreds of subagents from a script Claude writes
- **Agent teams:** Multiple Claude Code instances with shared tasks + inter-agent messaging (experimental)
- **/ultrareview:** Fleet of bug-hunting agents in cloud
- **Nested subagents:** Subagents can spawn own subagents (5 levels deep)
- **Computer use in CLI:** Verify GUI changes from terminal
- **Effort levels:** Hooks see effort.level and $CLAUDE_EFFORT
- **Auto mode:** Classifier handles permission prompts (user has this enabled)

---

## Phase 0: Safety Net & Baseline

> **Exit Criteria:** A test suite exists that verifies current cc10x behavior on 5 representative workflows. All tests pass on `main` before any changes.

### Task 1: Create behavioral baseline fixtures

**Files:**

- Create: `tests/v12-baseline/trivial-build.json`
- Create: `tests/v12-baseline/standard-build.json`
- Create: `tests/v12-baseline/debug-workflow.json`
- Create: `tests/v12-baseline/plan-workflow.json`
- Create: `tests/v12-baseline/review-workflow.json`

**Step 1:** For each of the 5 workflows, capture: router intent classification, workflow artifact structure, agent dispatch order, hook events fired, final memory state.

**Step 2:** Write a baseline runner script that replays these fixtures and asserts key invariants.

**Step 3:** Run baseline, verify all 5 pass. Commit: `test: add v12 behavioral baseline fixtures`

### Task 2: Document the "what stays" inventory

**Files:** Create: `docs/plans/v12-keep-inventory.md`

**Step 1:** List every functional element that MUST survive:

- Workflow artifact system (`.cc10x/workflows/`)
- Intent routing table (ERROR > PLAN > REVIEW > ORIENT > BUILD)
- Complexity gradient (trivial vs standard)
- Per-role model-tier policy → **now maps to native `effort` frontmatter**
- Agent dispatch protocol with contract validation
- Anti-anchoring plan review (fresh context for plan-gap-reviewer)
- Test Honesty Gates (false-green detection)
- Blast radius scan after debug fixes
- Memory finalization → **now maps to native `memory` frontmatter**
- Dispatch-by-reference (pass paths, not pasted content)
- Inline-fallback mode (graceful degradation)

**Step 2:** For each item, write one sentence on WHY it stays. Commit: `docs: v12 keep-inventory`

---

## Phase 1: Dead Weight Removal & Bug Fixes

> **Exit Criteria:** All dead code, dead config keys, and known bugs removed/fixed. Baseline tests pass. Zero functional change.

### Task 1: Delete dead script and dead functions

**Files:**

- Delete: `plugins/cc10x/scripts/cc10x_reference_benchmark.py` (338 lines, zero callers)
- Modify: `plugins/cc10x/scripts/cc10x_hooklib.py` — remove 3 dead functions (`parse_markdown_sections`, `extract_bullets`, `normalize_bullet`)

**Steps:** Grep to confirm zero references → delete → run baseline → commit: `refactor: remove dead reference_benchmark.py and 3 dead hooklib functions`

### Task 2: Remove dead hook-mode.json config keys

**Files:** Modify: `plugins/cc10x/config/hook-mode.json`

**Steps:** Remove 7 dead keys. Keep only `artifactIntegrity` (the one that blocks). Run baseline → commit: `refactor: remove 7 dead hook-mode.json config keys`

### Task 3: Fix the stop_persist/precompact_state clobber bug

**Files:** Modify: `plugins/cc10x/scripts/cc10x_stop_persist.py`

**Steps:** `stop_persist.py` writes to `.cc10x/precompact-state.json`, clobbering `precompact_state.py`. Fix: write to `.cc10x/stop-state.json`. Run baseline → commit: `fix: stop_persist no longer clobbers precompact_state output`

### Task 4: Fix doc-syncer skills/tools mismatch

**Files:** Modify: `plugins/cc10x/agents/doc-syncer.md`

**Steps:** Frontmatter lists skills but `tools` lacks `Skill`. Add `Skill` to tools. Run baseline → commit: `fix: doc-syncer can now invoke its declared skills`

---

## Phase 2: Hook Layer Modernization

> **Exit Criteria:** Hook scripts reduced from 20 to ~8. Log-only hooks replaced with HTTP or consolidated command hook. Agent-based hook used for fresh-context verification. New events wired (UserPromptSubmit, SubagentStart, PostToolBatch). Baseline tests pass.

### Task 1: Replace log-only hooks with HTTP or single consolidated command hook

**VALIDATION:** Claude Code v2.1.198 supports `http` hook type (POST event JSON to URL) and `agent` hook type (agentic verifier). For log-only hooks, an HTTP endpoint or a single consolidated command script is better than 6 separate Python scripts.

**Files:**

- Create: `plugins/cc10x/scripts/cc10x_event_logger.py` (~60 lines)
- Delete: 6 log-only scripts (subagent_stop_audit, postcompact_context, instructions_loaded_audit, latency_audit, doc_consistency_check, stop_failure_log)
- Modify: `plugins/cc10x/hooks/hooks.json`

**Steps:**

1. Write `cc10x_event_logger.py` — takes event type as argv[1], reads stdin JSON, appends to `.cc10x/events.jsonl`. ~60 lines using hooklib.
2. Update `hooks.json` to route 6 log-only events to the new script with different argv. Use `if` conditions in hook config to filter before spawning (native v2.1 feature).
3. Delete 6 old scripts. Run baseline → commit: `refactor: merge 6 log-only hooks into 1 event logger with if-condition filtering`

### Task 2: Merge precompact_state + stop_persist into 1 parameterized script

**Files:**

- Create: `plugins/cc10x/scripts/cc10x_state_persist.py` (~80 lines)
- Delete: `plugins/cc10x/scripts/cc10x_precompact_state.py`
- Delete: `plugins/cc10x/scripts/cc10x_stop_persist.py`
- Modify: `plugins/cc10x/hooks/hooks.json`

**Steps:** Write 1 parameterized script. Route PreCompact and Stop to it with different argv. Delete 2 old scripts. Run baseline → commit: `refactor: merge precompact_state + stop_persist into 1 parameterized script`

### Task 3: Move 4 utility scripts to tools/ subdir

**Files:**

- Move: `cc10x_phase_brief.py` → `tools/phase_brief.py`
- Move: `cc10x_review_package.py` → `tools/review_package.py`
- Move: `cc10x_harness_audit.py` → `tools/harness_audit.py` (rewrite in Phase 6)
- Move: `cc10x_worldclass_benchmark.py` → `tools/worldclass_benchmark.py` (delete in Phase 6)

**Steps:** Move files. Update references. Run baseline → commit: `refactor: move 4 utility scripts to tools/`

### Task 4: Wire new hook events (VALIDATED against v2.1.198)

**Files:** Modify: `plugins/cc10x/hooks/hooks.json`

**Steps:**

1. **UserPromptSubmit:** Wire to inject workflow state context. Currently the SessionStart hook does this — but UserPromptSubmit is better (injects before each prompt, not just at session start). Use `command` type with a small script that reads `.cc10x/workflows/current.json` and outputs it as additional context.

2. **SubagentStart:** Wire to log agent dispatch (replaces part of subagent_stop_audit). Use the event logger.

3. **PostToolBatch:** Wire to validate batch artifacts after a full batch of parallel tool calls (better than individual PostToolUse). Use `command` type pointing to the artifact guard script.

4. **PostToolUseFailure:** Wire to log tool failures (cc10x v11 doesn't handle this). Use the event logger.

5. **FileChanged:** Wire to trigger re-verification on watched file changes. Matcher: `*.py,*.ts,*.js,*.json`. Use `command` type that writes to `.cc10x/file-changes.jsonl`.

6. Run baseline → commit: `feat: wire UserPromptSubmit, SubagentStart, PostToolBatch, PostToolUseFailure, FileChanged hooks`

### Task 5: Evaluate agent-based hook for fresh-context verification

**VALIDATION:** Claude Code v2.1.198 supports `agent` hook type — "run an agentic verifier with tools for complex verification tasks." This is EXACTLY what the Fable 5 guide recommends: "Separate, fresh-context verifier subagents tend to outperform self-critique."

**Files:** Modify: `plugins/cc10x/hooks/hooks.json`

**Steps:**

1. Evaluate: should the PostToolUse artifact guard (currently `command` type, exit 2 to block) become an `agent` hook? The agent hook can run a fresh-context verifier that checks artifact integrity with full Claude reasoning, not just Python regex checks.

2. If yes: configure an agent-based PostToolUse hook that dispatches a fresh-context verifier to check workflow artifact integrity. This replaces the Python script's hardcoded checks with Claude-powered semantic validation.

3. If the agent hook type is too slow for PostToolUse (fires on every Edit/Write), keep the command hook for fast blocking checks and add an agent-based Stop hook for comprehensive end-of-turn verification.

4. Run baseline → commit: `feat: add agent-based fresh-context verification hook (Fable 5 aligned)`

---

## Phase 3: Agent Layer Modernization

> **Exit Criteria:** Agent count reduced from 10 to 7. Shared boilerplate moved to native frontmatter. Total agent lines reduced ~50%. All contracts still validate. Baseline tests pass.

### Task 1: Merge web-researcher + github-researcher → researcher

**Files:**

- Create: `plugins/cc10x/agents/researcher.md`
- Delete: `plugins/cc10x/agents/web-researcher.md`, `plugins/cc10x/agents/github-researcher.md`

**Steps:** Merge 90% common structure. Mode flag: `github` vs `web` set by router. Target: ~100 lines (from 302). Update router references. Run baseline → commit: `refactor: merge web-researcher + github-researcher → researcher`

### Task 2: Merge silent-failure-hunter → code-reviewer (Pass 1b)

**Files:**

- Modify: `plugins/cc10x/agents/code-reviewer.md`
- Delete: `plugins/cc10x/agents/silent-failure-hunter.md`
- Create: `plugins/cc10x/agents/references/silent-failure-red-flags.md`

**Steps:** Extract red-flags table to reference file. Add "Pass 1b: Silent failure scan" to code-reviewer (3-4 lines referencing the table). Update router. Run baseline → commit: `refactor: merge silent-failure-hunter into code-reviewer as Pass 1b`

### Task 3: Move declarative fields from prose to native frontmatter

**VALIDATION:** Plugin agents support: `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`. Currently cc10x encodes these in prose. Move them to frontmatter.

**Files:** Modify: all 7 remaining agent .md files

**Steps:** For each agent, move:

| Current prose | New frontmatter |
| -------------- | ---------------- |
| "Memory First" (mkdir + 3 Read calls) | `memory: true` |
| Model tier prose ("use Haiku for...", "use Opus for...") | `model: haiku` or `model: sonnet` or `model: opus` |
| Effort level prose | `effort: medium` / `effort: high` / `effort: xhigh` |
| Turn limit prose ("max 15 turns") | `maxTurns: 15` |
| Background dispatch prose | `background: true` (where applicable) |
| "Preload these skills..." prose | `skills: [cc10x:planning, cc10x:verification]` |
| Worktree isolation prose | `isolation: "worktree"` (where applicable) |
| Tool restrictions prose | `tools: [Read, Bash, Grep]` or `disallowedTools: [Write, Edit]` |

**IMPORTANT:** Do NOT add `hooks` to frontmatter — plugin agents don't support it. Keep hooks in hooks.json.

Run baseline → commit: `refactor: move declarative agent fields to native frontmatter`

### Task 4: Extract shared agent preamble (non-declarative boilerplate only)

**VALIDATION:** After Task 3, most shared boilerplate moves to frontmatter. What remains is non-declarative procedural text.

**Files:**

- Create: `plugins/cc10x/agents/_shared/preamble.md`
- Modify: all 7 agent .md files

**Steps:** After frontmatter migration, remaining shared blocks:

- MEMORY_NOTES ownership ("don't edit .cc10x/*.md; emit MEMORY_NOTES")
- SINGLE FINAL RESPONSE RULE
- CONTRACT envelope format
- Shell Safety

Write `preamble.md` (~20 lines). Each agent's frontmatter gets `skills: [_shared/preamble]` or reference it via a preloaded skill. Run baseline → commit: `refactor: extract shared agent preamble (post-frontmatter migration)`

### Task 5: Compress each agent to target size

**Files:** Modify: all 7 agent .md files

**Steps:** Apply Fable 5 principle: "a short brevity instruction is as effective as listing each pattern." Cut:

- Procedural step-by-step hand-holding
- "BAD: ... GOOD: ..." examples
- Repeated explanations of TDD, false-RED, vertical slicing (in skills, not agent prompts)
- Decision Checkpoints tables → 1-line "checkpoint before irreversible actions"
- Confidence factor tables → "state confidence if uncertain"
- Debug Close-Out → "report root cause + fix + blast radius"

Target sizes: bug-investigator 460→~150, planner 414→~150, component-builder 354→~130, integration-verifier 336→~150, code-reviewer 257→~150, doc-syncer 150→~120, researcher ~100, plan-gap-reviewer 126→~126 (already lean).

Run baseline after each agent → commit: `refactor: compress {agent-name} — {old}→{new} lines`

---

## Phase 4: Skills Layer Modernization

> **Exit Criteria:** Skills reduced from 24 to ~14. Aligned with bundled /debug, /code-review, /loop, /verify. Training-data-level explanations removed. Dynamic context injection used in router. Baseline tests pass.

### Task 1: Evaluate bundled skill overlap

**VALIDATION:** Claude Code v2.1.198 bundles /debug, /code-review, /loop, /run, /verify. cc10x has custom equivalents. Must evaluate overlap.

**Files:** Create: `docs/plans/v12-bundled-skill-evaluation.md`

**Steps:**

1. **/debug (bundled) vs cc10x debugging-patterns:** Read the bundled /debug skill (it's prompt-based, ships with Claude Code). Compare with cc10x's debugging-patterns (493 lines + 2 references).
   - If bundled /debug covers the basics: strip cc10x debugging to ONLY unique concepts (10-rung repro ladder, variant scan dimensions, blast radius scan).
   - Target: 493 → ~80 lines (just the unique cc10x methodology).

2. **/code-review (bundled) vs cc10x code-review-patterns:** Bundled /code-review now "reports correctness bugs." Compare with cc10x's code-review-patterns (395 lines + 3 references).
   - If bundled covers the basics: strip cc10x to ONLY unique concepts (review heuristics, security checklist, review order).
   - Target: 395 → ~80 lines (just unique heuristics).

3. **/verify (bundled) vs cc10x verification-before-completion:** Bundled /verify "builds and runs your app to confirm a code change does what it should." Compare with cc10x's verification-before-completion (420 lines).
   - If bundled covers launch + verify: strip cc10x to ONLY unique concepts (Test Honesty Gates, false-RED guard).
   - Target: 420 → ~60 lines (just Test Honesty Gates).

4. **/loop (bundled) vs cc10x loop concept:** Bundled /loop is a self-paced loop skill. cc10x's "loop engine" is the router's workflow loop. These serve different purposes — /loop is a user-facing command, cc10x's loop is the architectural backbone. Keep both, but document the relationship.

5. Commit: `docs: v12 bundled skill evaluation — align with /debug, /code-review, /verify`

### Task 2: Merge overlapping skills

**Files:** (same as v1 plan, but with corrected targets based on Task 1 evaluation)

- Merge: `code-generation` + `test-driven-development` → `building`
- Merge: `frontend-patterns` + `frontend-design-critique` → `frontend`
- Merge: `code-review-patterns` + `receiving-code-review` → `code-review` (aligned with bundled /code-review)
- Merge: `brainstorming` + `prototyping` → `exploration`
- Merge: `codebase-deepening` + `finding-duplicate-functions` → `codebase-hygiene`
- Merge: `session-memory` + `handoff-package` → `memory-and-handoff`
- Delete: `authoring-cc10x-guidance` (meta-skill, no longer needed)
- Delete: `skill-eval-harness` (eval tooling → tests/)

**Steps:** For each merge, keep ONLY unique content (verified against bundled skills in Task 1). Run baseline after each → commit: `refactor: merge {skill-a} + {skill-b} → {new-skill}`

### Task 3: Compress all remaining skills (the Fable 5 cut)

**Files:** Modify: all remaining SKILL.md files and references

**Steps:** Apply to EVERY skill:

**CUT (modern Claude already knows):**

- "BAD: ... GOOD: ..." examples
- Step-by-step procedural hand-holding
- Training-data-level explanations (what TDD is, how to write a test, what accessibility means)
- Repeated boilerplate (now in frontmatter or preamble)
- Rationalization prevention tables
- Red flags / "STOP and revise" sections → 1-line constraint
- Functionality Flow Mapping, Validation Levels tables, Risk Assessment tables, Requirements Checklists

**KEEP (unique cc10x value):**

- Workflow artifact schema and lifecycle
- Router routing table and dispatch protocol
- Test Honesty Gates (false-green detection — unique concept)
- Anti-anchoring plan review
- Blast radius scan dimensions
- Memory file contracts
- Dispatch-by-reference rule
- Complexity gradient
- 10-rung repro ladder (IF Task 1 test shows modern Claude needs it)
- Variant scan dimensions

**TEST BEFORE CUTTING:** Run a task with the skill and without it. If quality drops, keep it.

Run baseline after each skill → commit: `refactor: compress {skill-name} — {old}→{new} lines`

### Task 4: Use dynamic context injection in router

**VALIDATION:** Claude Code skills support `!`command`` syntax — "Claude Code runs the command and replaces the line with its output before Claude sees the skill content." This can replace SessionStart hook context injection.

**Files:** Modify: `plugins/cc10x/skills/cc10x-router/SKILL.md`

**Steps:**

1. Add dynamic context injection lines to the router SKILL.md:

   ```
   ## Current Workflow State
   !`cat .cc10x/workflows/current.json 2>/dev/null || echo '{"status":"none"}'`
   
   ## Memory
   !`cat .cc10x/memory.md 2>/dev/null || echo 'No memory yet.'`
   ```

2. This injects live workflow state and memory every time the router skill is invoked — no hook needed for context injection.
3. Evaluate: can this replace the SessionStart hook entirely? If yes, remove the SessionStart hook's context injection logic.
4. Run baseline → commit: `feat: use dynamic context injection in router — live workflow state without hooks`

### Task 5: Audit for reasoning-extraction triggers (Fable 5 safety)

**Files:** Modify: any skill/agent that instructs Claude to "explain your reasoning"

**Steps:** Grep for "explain", "narrate", "show your", "reasoning", "thought process", "reflect on". Remove or rephrase (Fable 5 triggers refusal on reasoning extraction). Run baseline → commit: `refactor: remove reasoning-extraction triggers (Fable 5 safety)`

---

## Phase 5: Router Modernization

> **Exit Criteria:** Router SKILL.md compressed from 677 to ~250 lines. References compressed from 1,106 to ~500 lines. Dynamic context injection replaces hook-based state injection. Fable 5 constraints added. CONTRACT envelope simplified. Baseline tests pass.

### Task 1: Compress router SKILL.md

**Files:** Modify: `plugins/cc10x/skills/cc10x-router/SKILL.md`

**Steps:**

1. **CUT:**
   - §14 Hard Rules — keep only rules not encoded elsewhere
   - §12 Chain Execution Loop — replace with simple state machine description
   - SELF-CHECK BLOCKLIST — modern Claude doesn't bias prompts this way
   - Dispatch Context Hygiene detailed rules → "dispatch by path, not by pasted content"
   - Optional prompt scaffold sections → "include relevant context for the agent's task"
   - Repeated examples and edge cases

2. **KEEP:**
   - Intent routing table (ERROR > PLAN > REVIEW > ORIENT > BUILD)
   - Workflow artifact lifecycle (create → update → finalize)
   - Agent dispatch protocol (contract validation, dispatch-by-reference)
   - Complexity gradient (trivial vs standard)
   - Per-role model-tier policy → now maps to native `effort` frontmatter
   - Inline-fallback mode
   - Memory finalization rule

3. **ADD (Fable 5-aligned constraints):**
   - "When you have enough information to act, act." (anti-overplanning)
   - "Pause for the user only when the work genuinely requires them." (checkpoint discipline)
   - "Before reporting progress, audit each claim against a tool result." (progress grounding)
   - "Delegate independent subtasks to subagents and keep working while they run." (parallelism)

4. **ADD (dynamic context injection):**
   - `!`cat .cc10x/workflows/current.json`` — live workflow state
   - `!`cat .cc10x/memory.md`` — live memory

Run baseline → commit: `refactor: compress router SKILL.md — 677→250 lines, add Fable 5 constraints + dynamic context`

### Task 2: Compress router references

**Files:** Modify all 6 reference files + verify skeleton JSON

**Steps:** Apply same cut rules. Targets: build-workflow 236→~100, debug-workflow 66→~40, plan-workflow 72→~40, review-workflow 22→keep, remediation-and-research 321→~100, workflow-artifact-and-hook-policy 267→~100. Run baseline → commit: `refactor: compress router references — 1106→500 lines`

### Task 3: Simplify CONTRACT envelope

**Files:** Modify router SKILL.md, all agent files, preamble

**Steps:**

1. The current CONTRACT envelope (`CONTRACT {"s":"...","b":...}` on line 1) is fragile JSON-in-prose. Evaluate Claude Code's native sub-agent return mechanism.
2. If native structured output is available, switch to it. If not, simplify to a YAML block at the END of the agent's response (less fragile than line 1).
3. Update all agents and router validation logic. Run baseline → commit: `refactor: simplify CONTRACT envelope — JSON-in-prose → YAML block`

### Task 4: Align with native /goal and /loop

**VALIDATION:** Claude Code v2.1.198 has native /goal (work across turns until completion condition) and /loop (self-paced loop). The router's workflow loop is the architectural backbone — but it should be compatible with these user-facing commands.

**Files:** Modify: `plugins/cc10x/skills/cc10x-router/SKILL.md`

**Steps:**

1. Document: how does the router's workflow loop relate to /goal and /loop?
   - /goal: user sets a completion condition → router workflow runs until condition holds
   - /loop: user invokes self-paced loop → router workflow is the loop body
2. Add a section to the router: "When /goal or /loop is active, the workflow loop continues until the user's completion condition is met. Do not stop and ask for permission mid-loop."
3. Add the Fable 5 autonomous-mode instruction: "You are operating autonomously. The user is not watching in real time. For reversible actions that follow from the original request, proceed without asking."
4. Run baseline → commit: `feat: align router with native /goal and /loop — autonomous mode support`

---

## Phase 6: Engine Script Cleanup

> **Exit Criteria:** Engine scripts reduced from 5 (~3,961 lines) to 3 (~800 lines). Data-driven design. Baseline tests pass.

### Task 1: Rewrite harness_audit.py as data-driven validator

**Files:** Create: `plugins/cc10x/tools/harness_audit.py` (~200 lines), `plugins/cc10x/tools/harness_audit_checks.yaml`

**Steps:** Extract 24+ check patterns into YAML. Rewrite as ~200-line generic validator. Run baseline → commit: `refactor: rewrite harness_audit as data-driven — 907→200 lines`

### Task 2: Rewrite workflow_replay_check.py as table-driven validator

**Files:** Create: `plugins/cc10x/tools/workflow_replay_check.py` (~300 lines), `plugins/cc10x/tools/replay_checks.yaml`

**Steps:** Extract 24 repetitive check functions into YAML. Rewrite as ~300-line validator. Run baseline → commit: `refactor: rewrite workflow_replay_check — 1025→300 lines`

### Task 3: Delete degenerate worldclass_benchmark.py

**Steps:** Script references 17 repos, only 1 exists. Delete. Remove references. Run baseline → commit: `refactor: remove degenerate worldclass_benchmark.py`

### Task 4: Slim live_harness_runner.py

**Files:** Modify: `plugins/cc10x/tools/live_harness_runner.py` (302→~200 lines)

**Steps:** Fix hardcoded `/bin/zsh` → `os.environ.get('SHELL', '/bin/sh')`. Cut 40% ceremony. Run baseline → commit: `refactor: slim live_harness_runner — 302→200, fix portability`

---

## Phase 7: Keynote-Ready Polish

> **Exit Criteria:** cc10x v12.0 is the leanest, most powerful Claude Code harness. All baseline tests pass. Fable 5 aligned. Keynote-ready.

### Task 1: Write the "Loop Engine" architecture document

**Files:** Create: `docs/plans/v12-loop-engine-architecture.md`

**Steps:** Write the keynote's technical backbone:

- The Loop: plan → build → verify → learn (with durable state at each step)
- The Harness: router (routing kernel) → agents (delegation) → hooks (enforcement) → skills (instruction)
- The Principles: trust the model, constrain not prescribe, fresh-context verification, memory that persists
- The Platform: aligned with Claude Code native /goal, /loop, /debug, /code-review, /verify, dynamic workflows, agent-based hooks
- The Numbers: router 30K→8K, agents 39K→15K, skills lazy-loaded, scripts 20→8, dead code 7→0

Commit: `docs: v12 loop engine architecture document`

### Task 2: Fable 5 alignment checklist

**Files:** Create: `docs/plans/v12-fable5-alignment-checklist.md`

**Steps:** Verify:

- [ ] Skills not too prescriptive (reviewed and trimmed)
- [ ] Brevity instructions replace enumerated patterns
- [ ] Fresh-context verifier subagents (agent-based hooks or verifier agents)
- [ ] No reasoning-extraction triggers
- [ ] Progress claims grounded in tool results
- [ ] Boundaries stated
- [ ] Parallel subagents with async communication
- [ ] Memory system (one lesson per file, corrections + confirmations)
- [ ] Checkpoint discipline (pause only when genuinely needed)
- [ ] Effort levels mapped to native frontmatter
- [ ] Autonomous mode instruction for /goal and /loop
- [ ] Dynamic context injection (no hook needed for state injection)

Commit: `docs: v12 Fable 5 alignment checklist`

### Task 3: Final token cost audit (CORRECTED)

**Files:** Create: `docs/plans/v12-token-audit.md`

**Steps:** Measure actual token cost. **Key correction:** skills are lazy-loaded, so measure:

1. **Always-loaded cost:** Router SKILL.md (target ~8K from ~30K) + CLAUDE.md
2. **Per-invocation cost:** Each skill's SKILL.md (target: most <150 lines, mega-skills <200)
3. **On-demand cost:** Reference files (target: each <100 lines)
4. **Per-spawn cost:** Agent prompts (target: most <150 lines)
5. **Runtime cost:** Hook scripts (not in context, but complexity matters)

Commit: `docs: v12 token audit — corrected for lazy loading`

### Task 4: Full regression test

**Steps:** Run all 5 baseline tests on fully refactored system. Verify: routing decisions, workflow artifacts, agent dispatch, hooks, memory. Fix any failures. Commit: `test: v12 full regression — all 5 baseline workflows pass`

### Task 5: Version bump

**Files:** Modify: `plugins/cc10x/.claude-plugin/plugin.json` (version: 12.0.0)

Commit: `release: cc10x v12.0.0 — The Loop Engine`

---

## Risks

| Risk | P | I | Score | Mitigation |
| ------ | --- | --- | ------- | ------------ |
| Cutting a skill that provides unique value | 3 | 5 | 15 | Test each cut: run task with and without skill |
| Router compression breaks routing | 2 | 5 | 10 | Baseline tests after each router change |
| Agent merge loses specialized behavior | 3 | 4 | 12 | Keep unique content in reference files |
| Agent-based hook too slow for PostToolUse | 3 | 3 | 9 | Keep command hook for fast checks, agent hook for Stop |
| Bundled skill overlap assessment wrong | 2 | 4 | 8 | Read bundled skill content before cutting |
| Plugin agent frontmatter restrictions missed | 1 | 5 | 5 | Validated: no hooks/mcpServers/permissionMode in plugin agents |
| Dynamic context injection fails on empty state | 2 | 2 | 4 | Use `2>/dev/null | | echo 'none'` fallback |
| Token reduction over-target | 3 | 3 | 9 | Phase 7 token audit with corrected lazy-loading model |

---

## Success Criteria

- [ ] All 5 baseline workflow tests pass on v12.0.0
- [ ] Router context cost ≤ 8K tokens (from ~30K — this is the always-loaded cost)
- [ ] Agent prompts ≤ 150 lines each (from 126-460)
- [ ] Skill prompts ≤ 200 lines each (from 139-677)
- [ ] Hook scripts ≤ 8 (from 20)
- [ ] Agent count = 7 (from 10)
- [ ] Skill count ≤ 14 (from 24)
- [ ] Zero dead code, zero dead config keys, zero known bugs
- [ ] Fable 5 alignment checklist complete
- [ ] Native frontmatter used (effort, maxTurns, memory, skills, background)
- [ ] Dynamic context injection used in router
- [ ] Agent-based hook evaluated for fresh-context verification
- [ ] Aligned with bundled /debug, /code-review, /verify
- [ ] Aligned with native /goal and /loop
- [ ] Version 12.0.0 released

---

## The Keynote Narrative

**"Harness and Loop Engineering for Claude Code"**

This talk teaches developers and companies how to work with Claude Code like professionals — not just prompting it, but engineering their work. The discipline is harness and loop engineering. cc10x v12 is the artifact that embodies the discipline — the proof that the principles work, the demo that runs live on stage.

### The Teaching Arc

**1. The Gap:** Most developers prompt Claude Code like a chatbot — type a request, get code, paste it, move on. This is prompt-and-pray. It doesn't scale to real engineering work: multi-file refactors, bug investigations across a codebase, features that touch 20 files. The gap between "Claude wrote me a function" and "Claude engineered a feature end-to-end" is not about prompting harder. It's about engineering the work.

**2. The Discipline — Harness Engineering:** A harness is the scaffolding around the model that makes it reliable for real work. It's not a chat — it's a system. The four components:

- **Routing:** Classify intent — is this a bug, a plan, a review, a build? Different work needs different workflows, different agents, different verification.
- **State:** Durable workflow artifacts — the model doesn't have to hold everything in context. The harness remembers what phase you're in, what's been done, what's left.
- **Delegation:** Dispatch sub-agents with fresh context for independent work. The orchestrator doesn't build and review in the same context — it delegates and verifies.
- **Enforcement:** Hooks that block bad states, log events, and run fresh-context verification. The harness catches what the model misses — not by trusting it less, but by verifying independently.

**3. The Discipline — Loop Engineering:** Real work is a loop, not a prompt. plan → build → verify → learn. Each iteration is a cycle:

- **Plan:** Understand the problem, decompose into tasks, define done.
- **Build:** Execute tasks, delegate to sub-agents, manage parallelism.
- **Verify:** Fresh-context verification — a separate agent checks the work against the spec. Not self-critique. Not "does it look right." Does it actually work?
- **Learn:** Record what worked and what didn't. Memory that persists across sessions. One lesson per file. Corrections and confirmations alike.
   The loop runs until the completion condition holds. Claude Code's native /goal and /loop commands are the user-facing interface to this discipline.

**4. The Principles (what to teach):**

- **Trust the model, constrain the harness.** Modern Claude knows how to write tests, review code, debug. Don't teach it what it already knows. Constrain what it must not do.
- **Constrain, don't prescribe.** A one-line brevity instruction beats a 50-line enumerated checklist. The model is smart — give it the boundary, not the map.
- **Fresh-context verification.** Self-critique degrades in long sessions. A separate agent with no baggage checks the work against the spec. This is the single biggest quality lever.
- **Memory that learns.** One lesson per file. Record corrections and confirmed approaches. Delete what's wrong. The harness gets better with use.
- **Dispatch, don't paste.** Pass paths, not pasted content. Agents read what they need from the filesystem. The orchestrator stays lean.
- **Native over custom.** Use the platform's features — native hooks, native frontmatter, native skills, bundled /debug and /verify. Don't reinvent what Claude Code already does.

**5. The Demo (cc10x v12 as the proof):**

- Show the loop running live: a real task goes through plan → build → verify → learn
- Show the router classifying intent and dispatching agents
- Show fresh-context verification catching a bug that self-critique missed
- Show memory persisting a lesson from a previous session
- The numbers prove the discipline: router 30K→8K (trust the model), agents 50% shorter (constrain not prescribe), scripts 20→8 (native over custom), zero regression (fresh-context verification works)

**6. The Takeaway:** The harness shrinks as models grow. The loop persists. The discipline is knowing what to cut — and what to keep. When you engineer the work, not just the prompt, Claude Code becomes a teammate, not a chatbot.

### How cc10x v12 Supports the Talk

cc10x v12 is not the subject of the keynote — it's the evidence. Every principle taught on stage is embodied in the harness:

| Principle (taught) | cc10x v12 (proof) |
| --- | --- |
| Trust the model | Router compressed 70% — no training-data-level instruction |
| Constrain, don't prescribe | Skills stripped to unique concepts, brevity instructions replace enumerated tables |
| Fresh-context verification | Agent-based hooks, plan-gap-reviewer with no prior context |
| Memory that learns | `.cc10x/memory.md` — one lesson per file, corrections + confirmations |
| Dispatch, don't paste | Agents receive paths, not pasted content; dynamic context injection |
| Native over custom | Frontmatter (effort, maxTurns, memory), agent hooks, /goal and /loop alignment |
| The loop | plan → build → verify → learn with durable workflow artifacts |
