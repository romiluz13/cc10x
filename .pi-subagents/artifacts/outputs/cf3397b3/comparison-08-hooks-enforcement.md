# Deep Comparison: Hooks, Guards & Enforcement Mechanisms

## Projects Analyzed

| Project | Type | Hook System |
| --------- | ------ | ------------- |
| **cc10x** | Claude Code plugin (workflow orchestration) | 9 hook event types, 8 Python scripts, configurable audit/block modes |
| **Superpowers** | Claude Code plugin (skills library) | 1 hook event (SessionStart), 1 bash script |
| **Matt Pocock** | Skills (git guardrails + pre-commit) | 1 PreToolUse hook (bash), 1 pre-commit setup skill |

---

## 1. Hook Events Used

### cc10x — 9 Event Types

| Event | Matcher | Script | Purpose |
| ------- | --------- | -------- | --------- |
| **PreToolUse** | `Edit\|Write` | `cc10x_pretooluse_guard.py` | Blocks direct writes to protected memory files |
| **PreToolUse** | `Bash` | `cc10x_git_guard.py` | Blocks dangerous git commands with approval-token system |
| **SessionStart** | `startup\|resume\|compact` | `cc10x_sessionstart_context.py` | Injects workflow resume context (phase, quality, pending gate) |
| **PostToolUse** | `Edit\|Write` | `cc10x_posttooluse_artifact_guard.py` | Validates workflow artifact integrity after writes |
| **TaskCompleted** | (all) | `cc10x_task_completed_guard.py` | Validates task metadata + memory finalization + artifact freshness |
| **PostCompact** | (all) | `cc10x_event_logger.py postcompact` | Logs compaction events to workflow event log |
| **SubagentStop** | (all) | `cc10x_event_logger.py subagent_stop` | Audits subagent transcripts for contract compliance |
| **PreCompact** | (all) | `cc10x_state_persist.py precompact` | Snapshots workflow state before compaction |
| **Stop** | (all) | `cc10x_state_persist.py stop` | Persists session state on stop |
| **StopFailure** | (all) | `cc10x_event_logger.py stop_failure` | Logs stop-hook failures (async) |
| **InstructionsLoaded** | (all) | `cc10x_event_logger.py instructions_loaded` | Audits loaded instructions hash/count (async) |

### Superpowers — 1 Event Type

| Event | Matcher | Script | Purpose |
|-------|---------|--------|---------|
| **SessionStart** | `startup\|clear\|compact` | `session-start` (bash) | Injects "using-superpowers" skill content as context |

### Matt Pocock — 1 Event Type (per skill)

| Event | Matcher | Script | Purpose |
|-------|---------|--------|---------|
| **PreToolUse** | `Bash` | `block-dangerous-git.sh` | Blocks dangerous git commands |
| *(setup-pre-commit)* | N/A | Husky pre-commit hook | Runs lint-staged + typecheck + tests at commit time |

---

## 2. Enforcement Mechanisms

### cc10x — Multi-Layer Configurable Enforcement

**Configurable modes** (`hook-mode.json`):

```json
{
  "artifactIntegrity": "block",   // PostToolUse: blocks corrupt artifacts
  "protectedWrites": "audit",     // PreToolUse: audits protected writes
  "memoryWrites": "audit",        // PreToolUse: audits memory writes
  "taskMetadata": "audit"         // TaskCompleted: audits task metadata
}
```

**Enforcement layers:**

1. **PreToolUse blocking** (exit code 2 + JSON deny):
   - Git guard: blocks 7 dangerous git patterns; 2 patterns have approval-token escape hatch
   - Memory guard: blocks direct writes to `activeContext.md`, `patterns.md`, `progress.md` when `memoryWrites: block`

2. **PostToolUse blocking** (exit code 2):
   - Artifact guard: blocks writes that produce corrupt/missing-key workflow artifacts when `artifactIntegrity: block`
   - Scope discipline: only blocks when the write target IS the artifact; unrelated writes get audit-only

3. **TaskCompleted blocking** (exit code 2):
   - Validates 7 required metadata fields (`wf:`, `kind:`, `origin:`, `phase:`, `plan:`, `scope:`, `reason:`)
   - Memory task validation: checks router-owned evidence (origin, inline marker, finalized event)
   - Artifact freshness check (audit-only): warns if artifact wasn't updated after task completion

4. **Audit-only logging** (structured JSONL):
   - PostCompact, SubagentStop, StopFailure, InstructionsLoaded events
   - All enforcement decisions logged to `cc10x-hook-events.log`

5. **State persistence**:
   - PreCompact: snapshots workflow state before context compaction
   - Stop: persists session state on session end

6. **Auto-remediation**:
   - PostToolUse artifact guard auto-appends event log entries when artifacts are mutated (compensates for model skipping the step)

### Superpowers — Context Injection Only

- **No enforcement mechanisms at all**
- SessionStart hook injects skill instructions into context
- No blocking, no auditing, no validation
- Cross-platform output format detection (Cursor, Claude Code, Copilot CLI)

### Matt Pocock — Single-Purpose Blocking

**Git guardrails skill:**

- PreToolUse hook blocks 9 dangerous git patterns
- Exit code 2 + stderr message → Claude sees block
- **No approval token system** — all blocks are unconditional
- **No audit logging** — blocks are fire-and-forget
- Bash-based (simple, portable, but less sophisticated than Python regex)

**Pre-commit skill:**

- Sets up Husky + lint-staged + Prettier + typecheck + tests
- This is a **project-level** enforcement (git hooks, not Claude Code hooks)
- Runs at commit time, not at agent action time
- No Claude Code hook integration

---

## 3. Git Operation Protection

### cc10x Git Guard (`cc10x_git_guard.py`)

| Pattern | Blocked | Approvable | Token Path |
| --------- | --------- | ------------ | ------------ |
| `git push --force` | ✅ | ❌ Never | None |
| `git push` | ✅ | ✅ | `push` token |
| `git reset --hard` | ✅ | ❌ Never | None |
| `git clean -f` | ✅ | ❌ Never | None |
| `git branch -D` | ✅ | ✅ | `branch-delete` token |
| `git checkout .` | ✅ | ❌ Never | None |
| `git checkout -- .` | ✅ | ❌ Never | None |
| `git checkout *` | ✅ | ❌ Never | None |

**Approval token system:**

- Single-use JSON token at `.cc10x/state/git-approval.json`
- Written by router after explicit user menu choice
- Has `expires_at` timestamp + 600s backstop max age
- Token is consumed (deleted) on first match regardless of success
- Force-push and destructive operations have NO token path — unconditionally blocked
- Full audit logging of both approved and blocked decisions

### Matt Pocock Git Guard (`block-dangerous-git.sh`)

| Pattern | Blocked |
| --------- | --------- |
| `git push` | ✅ Unconditional |
| `git reset --hard` | ✅ Unconditional |
| `git clean -fd` | ✅ Unconditional |
| `git clean -f` | ✅ Unconditional |
| `git branch -D` | ✅ Unconditional |
| `git checkout .` | ✅ Unconditional |
| `git restore .` | ✅ Unconditional |
| `push --force` | ✅ Unconditional |
| `reset --hard` | ✅ Unconditional |

**No approval mechanism** — all blocks are permanent. No token, no escape hatch. If a workflow legitimately needs `git push`, it must be done manually by the user.

### Superpowers Git Protection

**None.** Superpowers has no git guardrails whatsoever.

### Comparison Summary

| Feature | cc10x | Matt Pocock | Superpowers |
| --------- | ------- | ------------- | ------------- |
| Dangerous git blocks | 8 patterns | 9 patterns | None |
| Approval token system | ✅ Yes | ❌ No | N/A |
| Force-push specifically blocked | ✅ | ✅ (via `push --force`) | N/A |
| `git restore .` blocked | ❌ No | ✅ Yes | N/A |
| `git checkout *` blocked | ✅ Yes | ❌ No | N/A |
| Audit logging of decisions | ✅ Yes | ❌ No | N/A |
| Token expiry/backstop | ✅ 600s | N/A | N/A |
| Language | Python (regex) | Bash (grep) | N/A |

**Gap: cc10x should add `git restore .` to its blocked patterns** — Matt Pocock catches this but cc10x doesn't.

---

## 4. Artifact/State Validation

### cc10x — Comprehensive Artifact Validation

**PostToolUse artifact guard:**

- Validates 12 required workflow keys (`workflow_uuid`, `workflow_id`, `workflow_type`, `state_root`, `phase_cursor`, `task_ids`, `results`, `intent`, `evidence`, `quality`, `status_history`, `remediation_history`)
- Checks event log file existence
- Checks artifact freshness (staleness detection)
- Checks `updated_at` timestamp presence
- **Scope discipline**: only blocks when the write target IS the artifact; unrelated writes get audit-only
- **Auto-remediation**: auto-appends event log entries on artifact mutation
- Blocking for hard corruption (bad JSON, missing keys); audit-only for soft issues (stale, missing event log)

**TaskCompleted guard:**

- Validates 7 required metadata fields in task descriptions
- Memory task validation: checks `origin=router`, inline marker, subject prefix, event log finalization
- Artifact freshness check: warns if artifact wasn't updated within 300s after task completion
- Cross-checks workflow artifact UUID matches task metadata

**State persistence:**

- PreCompact: snapshots workflow UUID, type, phase cursor, phase status, plan file
- Stop: persists same snapshot on session end
- These snapshots enable resume logic after compaction or session restart

**SessionStart context injection:**

- Injects workflow context: UUID, type, plan file, design file, phase cursor, research quality, pending gate, incomplete phases

### Superpowers — No Artifact Validation

No artifact or state validation of any kind. Pure context injection.

### Matt Pocock — No Artifact Validation

No artifact or state validation. The pre-commit skill validates code quality (lint, types, tests) but only at commit time via Husky, not at agent action time.

---

## 5. Enforcement Patterns cc10x Has That Others DON'T

| Pattern | Description | Value |
| --------- | ------------- | ------- |
| **Configurable audit/block modes** | `hook-mode.json` allows toggling between audit-only and blocking per enforcement type | Lets teams gradually adopt enforcement without breaking workflows |
| **Approval token system** | Single-use, time-limited JSON tokens for sanctioned git operations | Enables workflow-sanctioned push/branch-delete without unblocking everything |
| **PostToolUse artifact integrity validation** | Validates workflow JSON artifacts have all 12 required keys after writes | Catches corrupt state that would break resume/verifier handoff |
| **TaskCompleted metadata validation** | Validates 7 required metadata fields in task descriptions | Ensures all tasks have traceable workflow context |
| **Memory task finalization validation** | Validates router-owned evidence for memory tasks | Prevents unauthorized memory mutations |
| **Artifact freshness detection** | Detects when artifacts haven't been updated after task completion | Catches the #1 stress-test failure: skipped persistence |
| **Auto-remediation (event log auto-append)** | Auto-appends event log entries when artifacts are mutated | Compensates for model skipping steps under context pressure |
| **SubagentStop contract audit** | Checks subagent transcripts for CONTRACT marker presence | Verifies subagents followed output contracts |
| **PreCompact state snapshot** | Snapshots workflow state before context compaction | Enables reliable resume after compaction |
| **Stop state persistence** | Persists session state on session end | Enables cross-session workflow resume |
| **InstructionsLoaded audit** | Logs instruction hash and count | Detects instruction drift or missing context |
| **Structured event logging** | All enforcement decisions logged as JSONL with wf, phase, task_id, agent, decision, reason | Full observability for debugging and stress testing |
| **Scope discipline in PostToolUse** | Only blocks when write target IS the artifact; unrelated writes get audit-only | Prevents false positives from stale legacy artifacts |
| **SessionStart workflow context injection** | Injects current workflow state (phase, quality, pending gate, incomplete phases) | Enables seamless workflow resume after session restart/compaction |
| **StopFailure logging** | Logs when stop hooks themselves fail | Catches hook infrastructure failures |
| **Shared hooklib module** | Centralized utilities (state reading, event logging, mode loading, metadata parsing) | DRY enforcement logic, consistent behavior |

---

## 6. Enforcement Patterns Others Have That cc10x SHOULD Adopt

| Pattern | Source | Description | Why cc10x Should Adopt |
| --------- | -------- | ------------- | ---------------------- |
| **`git restore .` blocking** | Matt Pocock | Blocks `git restore .` which discards all working tree changes | cc10x blocks `git checkout .` but misses `git restore .` — same destructive effect |
| **Pre-commit hooks (Husky + lint-staged)** | Matt Pocock | Runs Prettier, typecheck, tests at commit time | cc10x has no commit-time enforcement; adding pre-commit would catch issues that slip past agent-time hooks |
| **Cross-platform hook wrapper** | Superpowers | `run-hook.cmd` polyglot batch/bash wrapper for Windows + Unix | cc10x's Python scripts assume Python3 is available; a polyglot wrapper would improve Windows compatibility |
| **Multi-platform output format** | Superpowers | Detects Cursor vs Claude Code vs Copilot CLI and emits correct JSON format | cc10x is Claude Code-specific; multi-platform support would broaden applicability |
| **Self-contained simplicity** | Matt Pocock | Single bash script, no dependencies, easy to audit | cc10x's 8 Python scripts + shared library is harder to audit; some guards could be simpler |

---

## 7. Enforcement Sophistication Ratings

### cc10x: **9/10**

**Strengths:**

- 9 hook event types covering the entire agent lifecycle
- Configurable audit/block modes per enforcement category
- Approval token system with expiry and single-use consumption
- Multi-layer artifact validation (12 keys, event logs, freshness, scope discipline)
- Auto-remediation for missed event log entries
- Comprehensive structured logging for observability
- State persistence for compaction/session resume
- Shared hooklib for DRY enforcement logic

**Weaknesses:**

- Missing `git restore .` pattern (Matt Pocock catches this)
- No commit-time enforcement (pre-commit hooks)
- Python3 dependency (no polyglot wrapper for Windows)
- No SubagentStop blocking (audit-only — can't prevent contract-violating subagents from stopping)
- `cc10x_subagent_stop_audit.py` referenced in task but doesn't exist as separate file (functionality is in event_logger)

### Superpowers: **2/10**

**Strengths:**

- Clean cross-platform SessionStart context injection
- Multi-platform output format detection
- Polyglot wrapper for Windows compatibility

**Weaknesses:**

- Only 1 hook event (SessionStart)
- Zero enforcement mechanisms
- No blocking, no auditing, no validation
- No git guardrails
- No artifact validation
- No state persistence
- It's a skills library, not an enforcement framework — rating reflects enforcement capabilities specifically

### Matt Pocock: **4/10**

**Strengths:**

- Clean, effective git guardrails (9 patterns)
- Pre-commit skill (Husky + lint-staged + typecheck + tests) adds commit-time enforcement
- Simple, auditable bash implementation
- Catches `git restore .` (which cc10x misses)
- Good skill documentation with step-by-step setup

**Weaknesses:**

- Only 1 Claude Code hook event (PreToolUse for Bash)
- No approval token system — all blocks unconditional
- No audit logging of decisions
- No artifact/state validation
- No PostToolUse, TaskCompleted, or session lifecycle hooks
- No configurable modes (can't toggle audit vs block)
- Git guardrails and pre-commit are separate skills, not integrated
- Bash grep matching is less precise than Python regex

---

## Verdict

**cc10x is in a different league entirely.** While Superpowers and Matt Pocock each address a single enforcement concern (context injection and git safety respectively), cc10x implements a comprehensive, multi-layer enforcement framework that covers the entire agent lifecycle — from session start through tool use, task completion, compaction, and session stop.

**cc10x's enforcement architecture is production-grade:**

- Configurable modes allow gradual adoption
- Approval tokens enable workflow-sanctioned operations without unconditional blocking
- Structured logging provides full observability
- State persistence enables reliable workflow resume
- Auto-remediation compensates for model unreliability

**Key gaps to close:**

1. **Add `git restore .` to blocked patterns** — same risk as `git checkout .`, currently missed
2. **Consider pre-commit hooks** — commit-time enforcement would add a safety net below agent-time hooks
3. **Consider SubagentStop blocking** — currently audit-only, can't prevent contract-violating subagents from stopping
4. **Consider polyglot wrapper** — improve Windows compatibility for Python-dependent hooks

**The approval token system is cc10x's standout innovation** — no other project has a mechanism for unblocking specific git operations through workflow-sanctioned tokens with expiry and single-use consumption. This is the kind of nuanced enforcement that real-world agent orchestration requires.
