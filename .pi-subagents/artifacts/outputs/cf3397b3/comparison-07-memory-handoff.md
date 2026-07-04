# Deep Comparison: Memory, Context & Handoff Systems

## Projects Analyzed

| Project | Scope of Analysis |
| --------- | ------------------- |
| **cc10x** | `memory-and-handoff/SKILL.md` + 4 reference files, `agent-common/SKILL.md`, `cc10x_state_persist.py`, `cc10x_sessionstart_context.py`, `cc10x_hooklib.py`, `hooks.json` |
| **Superpowers** | `hooks/` (hooks.json, hooks-cursor.json, run-hook.cmd, session-start), `finishing-a-development-branch/SKILL.md`, plus contextual reads: `using-superpowers`, `dispatching-parallel-agents`, `subagent-driven-development`, `writing-plans` |
| **Matt Pocock** | `productivity/handoff/SKILL.md`, `in-progress/claude-handoff/SKILL.md` |

> **Note:** `cc10x_postcompact_context.py` and `cc10x_stop_persist.py` do not exist as separate files. They have been unified into `cc10x_state_persist.py` (which accepts `precompact` or `stop` as `argv[1]`). The `PostCompact` hook calls `cc10x_event_logger.py postcompact` for event logging. This consolidation is itself a finding.

---

## 1. Memory Management Across Sessions

### cc10x

**Architecture: Multi-surface durable memory with ownership separation.**

cc10x maintains three markdown memory files under `.cc10x/`:

- `activeContext.md` — current focus, decisions, learnings, blockers, references (9 required sections with stable anchors)
- `patterns.md` — durable gotchas, user standards, project skill hints (4 required sections)
- `progress.md` — current workflow, task snapshot, completed items, verification evidence (5 required sections)

Plus machine-owned orchestration state:

- `.cc10x/workflows/{wf}.json` — canonical workflow state (phase cursor, phase status, plan/design files)
- `.cc10x/workflows/{wf}.events.jsonl` — append-only event trail

**Key design principles:**

- **Memory is an index, not a transcript.** Distill decisions, learnings, references — not logs.
- **Ownership separation:** Router owns all writes to `.cc10x/*.md`. WRITE agents emit structured `MEMORY_NOTES` in their Router Contract. READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`. Agents never edit memory directly.
- **Promotion ladder:** one-off observation → activeContext; repeated lesson → patterns; detailed analysis → docs/plans or docs/research; hard proof → progress.md verification.
- **Auto-heal:** If a canonical section is missing, the router inserts it just above `## Last Updated` before proceeding.
- **Mandatory load:** All agents must read all three memory files at workflow start, and re-read before key decision types (architectural, implementation, debugging, planning, completion claims).

**Session continuity:**

- `cc10x_sessionstart_context.py` fires on `startup|resume|compact` events, reads the latest workflow JSON, and injects a context string with workflow UUID, type, plan/design files, phase cursor, research quality, pending gate, and incomplete phases.
- `cc10x_state_persist.py` fires on `PreCompact` and `Stop` events, writing a snapshot (timestamp, workflow UUID, type, phase cursor, phase status, plan file, source) to `precompact-state.json` or `stop-state.json`.

### Superpowers

**Architecture: No persistent memory system. Skill-discovery injection only.**

Superpowers has a single SessionStart hook (`session-start` bash script) that:

1. Reads `skills/using-superpowers/SKILL.md` content at session start
2. Escapes it for JSON
3. Injects it as `additionalContext` (Claude Code) or `additional_context` (Cursor) or `additionalContext` (Copilot)

This is **skill discovery injection**, not memory persistence. It tells the agent "you have superpowers" and how to find skills, but does NOT persist any state across sessions.

The closest thing to memory is the **progress ledger** in subagent-driven-development:

- `.superpowers/sdd/progress.md` — a one-line-per-task ledger file
- Checked at skill start: tasks listed as complete are DONE, don't re-dispatch
- After compaction: "trust the ledger and `git log` over your own recollection"
- But this is skill-scoped, not project-wide, and git-ignored (scratch)

**Session continuity:** None. No state is persisted on Stop or PreCompact. No workflow artifacts. No event logs. Each session starts fresh with only skill-discovery context.

### Matt Pocock

**Architecture: No persistent memory system. Handoff-only.**

Matt Pocock's two skills are purely handoff-oriented:

- `handoff` — writes a handoff document to OS temp dir for a fresh agent
- `claude-handoff` — launches a background agent seeded with a handoff summary

There is no concept of durable project memory, no `.something/` directory, no session-start loading, no compaction handling. Memory lives entirely in the conversation transcript and is exported only when the user explicitly requests a handoff.

---

## 2. Context Compaction / Recovery

### cc10x

**Multi-layered compaction defense:**

1. **PreCompact hook** → `cc10x_state_persist.py precompact` → writes `precompact-state.json` with workflow snapshot (phase cursor, phase status, plan file). This fires BEFORE compaction, capturing the orchestration state that would otherwise be lost.

2. **PostCompact hook** → `cc10x_event_logger.py postcompact` → logs the compaction event for audit trail.

3. **SessionStart on compact** → `cc10x_sessionstart_context.py` → injects workflow context (UUID, phase, incomplete phases, pending gate) as additional context after compaction.

4. **Memory files survive compaction** — they're on disk, not in the conversation. After compaction, the agent re-reads `.cc10x/activeContext.md`, `patterns.md`, `progress.md` to restore context.

5. **Compaction KEEP/SUMMARIZE/DROP rubric** — explicit three-tier guidance:
   - KEEP (verbatim): user constraints, exact next step, open failures
   - SUMMARIZE: resolved decisions, concluded attempts, discovered boundaries
   - DROP: decorative prose, diaries, superseded speculation

6. **Context budget monitoring** — degradation tiers (clear → warming → degrading → fragile) with specific signals and checkpoint triggers. Early warning signs enumerated.

7. **Stop hook** → `cc10x_state_persist.py stop` → writes `stop-state.json` (unless `stop_hook_active` flag is set for continuation stops).

### Superpowers

**Minimal compaction recovery: progress ledger only.**

The subagent-driven-development skill explicitly calls out compaction as a real problem:
> "Conversation memory does not survive compaction. In real sessions, controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed."

Their solution: `.superpowers/sdd/progress.md` ledger file. After compaction, trust the ledger and `git log`.

**No hooks for compaction.** No PreCompact or PostCompact hooks. No state snapshot. No context injection after compaction. The SessionStart hook fires on `startup|clear|compact` but only injects skill-discovery text, not any project state.

### Matt Pocock

**No compaction handling at all.** No hooks, no state persistence, no recovery mechanism. If the conversation gets compacted, the handoff document (if previously written) is the only recovery path, and it's in `/tmp` — ephemeral.

---

## 3. Handoff Patterns

### cc10x

**Two distinct handoff modes:**

1. **Internal resume (structural):** cc10x's own resume is structural — `.cc10x/` workflow artifacts + router rehydrates. No handoff document needed. The router reads workflow JSON, event logs, and memory files to reconstruct state.

2. **Outward handoff package:** A portable, human-readable markdown export for when the next reader is NOT a cc10x session:
   - Written to OS temp dir, never in the repo
   - 7 required sections: Goal, Current state, What's done, What's next, Open blockers/failures, Suggested skills/tools, Artifacts by path
   - Secrets/PII redacted with `<redacted:secret>` / `<redacted:pii>`
   - References artifacts by path/URL, never pastes contents
   - "Suggested skills/tools" is load-bearing: tells next agent how to continue

3. **Inter-agent handoff (within session):** Router Contract system:
   - WRITE agents emit `CONTRACT {json}` + structured `MEMORY_NOTES` (learnings, patterns, verification, deferred)
   - READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`
   - Router collects these and persists during memory-finalize task
   - SubagentStop hook audits subagent contracts

### Superpowers

**Inter-agent handoff via subagent dispatch:**

1. **Subagent-Driven Development:** Fresh subagent per task. Controller dispatches with:
   - Task brief file (extracted via `scripts/task-brief`)
   - Report file path (implementer writes report, returns short summary)
   - Reviewer gets: brief file + report file + review package (diff file)
   - **File-based handoffs:** "Everything you paste into a dispatch prompt stays resident in your context. Hand artifacts over as files."
   - Model selection per task (cheap/standard/capable based on complexity)

2. **Parallel agent dispatch:** One agent per independent problem domain. Each gets focused scope, clear goal, constraints, expected output.

3. **Plan-to-execution handoff:** `writing-plans` creates a plan document with exact file paths, code, test commands. `subagent-driven-development` or `executing-plans` picks it up. Plan header explicitly says which sub-skill to use.

4. **Branch completion handoff:** `finishing-a-development-branch` presents 4 structured options (merge, PR, keep, discard) with worktree cleanup logic.

**No cross-session handoff.** No handoff document generation. No outward-facing export for a different tool or coworker.

### Matt Pocock

**Two handoff modes, both outward-facing:**

1. **`handoff` skill:** Writes a handoff document to OS temp dir. Includes "suggested skills" section. Redacts secrets. References artifacts by path/URL, doesn't duplicate. Tailors to next session's purpose if argument provided.

2. **`claude-handoff` skill:** Launches a background agent (`claude --bg --name "..." "<summary>"`) seeded with the handoff summary as its prompt. Returns immediately. User manages via `claude agents`. Same redaction and skill-suggestion rules.

**Simple, focused, effective.** No inter-agent protocol, no structural resume, no memory persistence. Pure "export current state for the next agent" approach.

---

## 4. State Persistence

### cc10x

| Mechanism | Trigger | What's Persisted | Where |
| ----------- | --------- | ------------------ | ------- |
| Memory files | Router memory-finalize task | Decisions, learnings, patterns, progress, verification | `.cc10x/*.md` |
| Workflow artifact | Router during workflow | Phase cursor, phase status, plan/design files, workflow UUID | `.cc10x/workflows/{wf}.json` |
| Event log | Router/hook events | Append-only event trail (dispatches, decisions, completions) | `.cc10x/workflows/{wf}.events.jsonl` |
| PreCompact snapshot | PreCompact hook | Workflow UUID, type, phase cursor, phase status, plan file | `.cc10x/precompact-state.json` |
| Stop snapshot | Stop hook | Same as precompact | `.cc10x/stop-state.json` |
| Hook event log | All hook scripts | Timestamped JSON events | `.cc10x/cc10x-hook-events.log` |
| SessionStart context | startup/resume/compact | Injected context string (not persisted, injected) | N/A (injected into session) |

**Implementation:** Python scripts via `cc10x_hooklib.py` shared library. Defensively coded — all hooks return 0 on error, never fail the session. State version tracked (`v11`).

### Superpowers

| Mechanism | Trigger | What's Persisted | Where |
| ----------- | --------- | ------------------ | ------- |
| SessionStart injection | startup/clear/compact | Skill-discovery text (using-superpowers SKILL.md) | N/A (injected into session) |
| Progress ledger | Manual (during SDD) | One-line-per-task completion records | `.superpowers/sdd/progress.md` (git-ignored) |
| Plan documents | Manual (writing-plans) | Implementation plan with tasks, code, tests | `docs/superpowers/plans/*.md` |

**Implementation:** Bash scripts. Cross-platform polyglot wrapper (`run-hook.cmd`). No Python. No shared library. No defensive error handling pattern (uses `set -euo pipefail`).

### Matt Pocock

| Mechanism | Trigger | What's Persisted | Where |
|-----------|---------|------------------|-------|
| Handoff document | User invokes `/handoff` | Summary of conversation, suggested skills | `${TMPDIR:-/tmp}/handoff-*.md` |
| Background agent | User invokes `/claude-handoff` | Handoff summary as agent prompt | N/A (passed as CLI arg) |

**Implementation:** Pure skill instructions (no scripts, no hooks, no code). The model itself writes the handoff document or launches the background agent.

---

## 5. cc10x Patterns the Others DON'T Have

| Pattern | Description | Value |
| --------- | ------------- | ------- |
| **Multi-surface memory with ownership separation** | Three distinct memory files with specific purposes, stable anchors, and write ownership (router-only). Agents emit notes, router persists. | Prevents memory corruption, enforces consistency, enables auto-heal |
| **Structured MEMORY_NOTES protocol** | Agents emit YAML-formatted `MEMORY_NOTES` with `learnings`, `patterns`, `verification`, `deferred` fields. Router parses and routes to correct memory file. | Machine-parseable, prevents free-form memory pollution |
| **Compaction KEEP/SUMMARIZE/DROP rubric** | Explicit three-tier taxonomy for what survives compaction. | Reproducible compaction behavior, not ad-hoc |
| **Context budget degradation tiers** | clear → warming → degrading → fragile with specific signals and checkpoint triggers. | Proactive context management, not reactive |
| **PreCompact + Stop state snapshots** | Hooks that fire before compaction and on stop, writing workflow state to JSON. | Structural recovery — state survives even if conversation doesn't |
| **Workflow artifacts + event logs** | Machine-owned JSON workflow state + append-only JSONL event trail. | Full orchestration replayability, dedupe keys |
| **Auto-heal memory contracts** | If canonical sections are missing, router inserts them before proceeding. | Self-repairing memory system, no manual intervention |
| **Promotion ladder** | Explicit rules for what goes where (one-off → activeContext, repeated → patterns, detailed → docs/research, proof → progress). | Prevents memory file bloat and misplacement |
| **Secret redaction protocol** | Systematic redaction of tokens/keys/PII in outward artifacts with `<redacted:secret>` placeholder. | Security by design, not ad-hoc |
| **Router Contract envelope** | `CONTRACT {json}` as first line of agent response, machine-readable status/blocking/critical-issues. | Router can make routing decisions without parsing prose |
| **Hook event log** | All hook events logged to `.cc10x/cc10x-hook-events.log` as timestamped JSON. | Full audit trail of hook activity |
| **Defensive hook design** | All hooks return 0 on error, never fail the session. State version tracked. | Production-grade reliability |

## 6. Patterns the Others Have That cc10x SHOULD Adopt

| Pattern | Source | Description | Why cc10x Should Adopt |
| --------- | -------- | ------------- | ---------------------- |
| **File-based subagent handoffs** | Superpowers (SDD) | Artifacts move as files (task briefs, report files, review packages), not pasted text. Reduces controller context pollution. | cc10x's MEMORY_NOTES are emitted in-conversation. For large workflows, file-based handoff artifacts would reduce context load on the router. |
| **Progress ledger as recovery map** | Superpowers (SDD) | One-line-per-task ledger with commit ranges. "Trust the ledger and git log over your own recollection." | cc10x has `progress.md ## Tasks` but it's more verbose. A compact one-line ledger with commit SHAs would be faster to scan after compaction. |
| **Model selection per task** | Superpowers (SDD) | Explicit model tier per subagent (cheap/standard/capable) based on task complexity. "Always specify the model explicitly." | cc10x's router dispatches agents but the skill docs don't mention model tier selection. Cost optimization opportunity. |
| **Background agent launch** | Matt Pocock (`claude-handoff`) | Launch a fresh background agent seeded with handoff summary. Returns immediately, user manages via `claude agents`. | cc10x's outward handoff writes a file that a human must manually feed to a new session. Auto-launching a background agent would be more seamless. |
| **Plan-to-execution handoff header** | Superpowers (`writing-plans`) | Plan documents start with "For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development" | cc10x plans in `docs/plans/*` lack an explicit execution-mode header. Adding one would help the router (or a human) pick the right execution strategy. |
| **Cross-platform hook wrapper** | Superpowers (`run-hook.cmd`) | Polyglot bash/cmd script that works on Windows (Git Bash) and Unix. | cc10x hooks are Python-only with `${CLAUDE_PLUGIN_ROOT}` interpolation. While Python is more portable than bash, the explicit Windows path detection pattern is worth noting. |
| **Worktree provenance check** | Superpowers (`finishing-a-development-branch`) | Only clean up worktrees under `.worktrees/` or `worktrees/` — don't touch harness-owned workspaces. | cc10x doesn't appear to have worktree lifecycle management. If cc10x ever uses worktrees, this provenance check pattern is essential. |
| **Pre-flight plan review** | Superpowers (SDD) | Scan plan for inter-task conflicts before starting execution. Present findings as one batched question. | cc10x's router could benefit from a plan conflict scan before dispatching the first agent, rather than discovering conflicts mid-workflow. |
| **Tight, single-purpose handoff skills** | Matt Pocock | Two skills, each ~10 lines, each does exactly one thing (write handoff / launch agent). | cc10x's handoff mode is a section within a larger SKILL.md. While the content is richer, Matt Pocock's composability (user invokes `/handoff` when needed) is simpler for the end user. |

---

## 7. Ratings

### cc10x: **8.5/10**

**Strengths:**

- Most sophisticated memory system of the three by a wide margin
- Multi-surface memory with ownership separation prevents corruption
- Compaction defense is multi-layered (PreCompact snapshot, memory files, SessionStart injection, rubric)
- Workflow artifacts + event logs provide full orchestration replayability
- Auto-heal contracts make the system self-repairing
- Defensive hook design (never fail the session)
- Structured MEMORY_NOTES protocol is machine-parseable
- Secret redaction is systematic, not ad-hoc
- Context budget monitoring with degradation tiers is unique and valuable

**Weaknesses:**

- No model-selection-per-task guidance (cost optimization gap)
- MEMORY_NOTES emitted in-conversation rather than as files (context pollution risk for large workflows)
- No background agent launch capability (handoff requires human to manually start new session)
- No explicit plan conflict pre-flight scan
- No worktree lifecycle management
- Complexity is high — 4 reference files + SKILL.md + agent-common + multiple scripts. The system is powerful but has a steep learning curve.
- The `cc10x_postcompact_context.py` and `cc10x_stop_persist.py` files referenced in the task don't exist (consolidated into `cc10x_state_persist.py`), suggesting documentation may lag implementation.

### Superpowers: **5/10**

**Strengths:**

- Excellent subagent-driven-development pattern with file-based handoffs
- Progress ledger is a pragmatic compaction recovery mechanism
- Model selection per task is a real cost optimization
- Plan-to-execution handoff is clean and explicit
- Cross-platform hook wrapper is well-engineered
- Worktree provenance check is a smart safety pattern
- Pre-flight plan review catches conflicts early
- Skills are well-written with clear decision trees and red flags

**Weaknesses:**

- No persistent project memory system at all
- No compaction hooks (PreCompact/PostCompact/Stop)
- SessionStart hook only injects skill-discovery text, not project state
- Progress ledger is skill-scoped (only during SDD), not project-wide
- Progress ledger is git-ignored scratch — `git clean -fdx` destroys it
- No event log or audit trail
- No structured inter-agent memory protocol
- No outward handoff document generation
- No secret redaction protocol
- The system relies entirely on git + plan docs for durability, which is insufficient for complex multi-session workflows

### Matt Pocock: **3/10**

**Strengths:**

- Dead simple: two skills, each ~10 lines, each does exactly one thing
- Background agent launch is a nice UX touch
- Secret redaction and artifact-by-reference are good practices
- "Suggested skills" section in handoff is load-bearing and practical
- Tailoring handoff to next session's purpose (via argument) is thoughtful

**Weaknesses:**

- No persistent memory whatsoever
- No compaction handling at all
- No hooks, no scripts, no automation
- No inter-agent protocol
- No state persistence
- No event log
- No workflow artifacts
- Handoff document is ephemeral (in `/tmp`)
- Entirely manual — user must explicitly invoke handoff
- No recovery mechanism if conversation is lost without a prior handoff

---

## Verdict

**cc10x has the most complete memory/handoff system by a significant margin.** Its multi-surface memory with ownership separation, multi-layered compaction defense, and workflow artifact + event log architecture are production-grade and unique among the three projects. The auto-heal contracts and structured MEMORY_NOTES protocol demonstrate mature systems thinking.

**Superpowers excels at inter-agent orchestration patterns** (file-based handoffs, model selection, progress ledger, pre-flight plan review) but has virtually no persistent memory or compaction recovery infrastructure. It treats git as its memory system, which works for simple workflows but breaks down for complex multi-session orchestration.

**Matt Pocock is intentionally minimal** — a handoff-only approach with no memory infrastructure. It's the right tool for a solo developer who occasionally needs to pass work to a fresh agent, but it's not a memory system at all.

### Key Recommendations for cc10x

1. **Adopt file-based subagent handoffs** from Superpowers — move large MEMORY_NOTES to files instead of in-conversation emission for workflows with many agents.
2. **Add model-selection-per-task guidance** to the router dispatch protocol.
3. **Add a compact progress ledger** (one-line-per-task with commit SHAs) alongside the verbose `progress.md` for fast post-compaction scanning.
4. **Consider background agent launch** as an alternative to writing handoff files to `/tmp`.
5. **Add a pre-flight plan conflict scan** before dispatching the first agent.
6. **Document the file consolidation** — update references to `cc10x_postcompact_context.py` and `cc10x_stop_persist.py` to reflect the unified `cc10x_state_persist.py`.

### Key Recommendations for Superpowers

1. **Adopt cc10x's multi-surface memory** — persistent project memory files that survive compaction.
2. **Add PreCompact/PostCompact hooks** — at minimum, snapshot the progress ledger.
3. **Make the progress ledger project-wide**, not skill-scoped.
4. **Add a SessionStart context injection** that includes project state, not just skill discovery.

### Key Recommendations for Matt Pocock

1. **Adopt any form of persistent memory** — even a single `.context.md` file would be a massive improvement.
2. **Add compaction hooks** — at minimum, auto-write a handoff document on PreCompact.
3. **Add an inter-agent protocol** — even a simple structured notes format.

---

## Summary Matrix

| Capability | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| Persistent project memory | ✅ 3 files + workflow artifacts | ❌ (ledger only, skill-scoped) | ❌ |
| Memory ownership separation | ✅ Router/WRITE/READ-ONLY | ❌ | ❌ |
| Compaction hooks | ✅ PreCompact + PostCompact + Stop | ❌ | ❌ |
| Compaction rubric | ✅ KEEP/SUMMARIZE/DROP | ❌ | ❌ |
| Context budget monitoring | ✅ Degradation tiers | ❌ | ❌ |
| SessionStart context injection | ✅ Workflow state | ✅ Skill discovery only | ❌ |
| Workflow artifacts (JSON) | ✅ | ❌ | ❌ |
| Event log (JSONL) | ✅ | ❌ | ❌ |
| Auto-heal memory | ✅ | ❌ | ❌ |
| Structured inter-agent notes | ✅ MEMORY_NOTES | ❌ | ❌ |
| Outward handoff document | ✅ | ❌ | ✅ |
| Background agent launch | ❌ | ❌ | ✅ |
| File-based subagent handoffs | ❌ | ✅ | ❌ |
| Model selection per task | ❌ | ✅ | ❌ |
| Progress ledger with commits | ❌ (verbose progress.md) | ✅ | ❌ |
| Secret redaction protocol | ✅ | ❌ | ✅ (ad-hoc) |
| Plan-to-execution handoff | ❌ (implicit) | ✅ (explicit header) | ❌ |
| Pre-flight plan conflict scan | ❌ | ✅ | ❌ |
| Worktree lifecycle | ❌ | ✅ | ❌ |
| Cross-platform hooks | Python-only | ✅ (polyglot) | N/A |
| Hook event audit log | ✅ | ❌ | ❌ |
| Defensive hook design | ✅ | ❌ (set -euo pipefail) | N/A |
| **Rating** | **8.5/10** | **5/10** | **3/10** |
