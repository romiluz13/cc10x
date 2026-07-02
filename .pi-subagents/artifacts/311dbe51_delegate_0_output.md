# DEEP REVIEW: Agents + Hooks + Scripts — Router Consistency Verification

## (A) Per-File Analysis

### AGENTS (8 files)

#### 1. code-reviewer.md — ✓ PASS
- **Pass 1b integrated:** Step 4 ("Pass 1b: Silent Failure Scan") is in the reviewer's own process. Explicitly states: "This pass replaces the former standalone silent-failure-hunter agent."
- **No separate hunter expected:** Router SKILL.md line 577 confirms: "BUILD dispatches exactly ONE `code-reviewer` per review point — its single review covers correctness AND the Pass 1b silent-failure scan; never create a second reviewer task for the same phase."
- **Verdict-first incoherence FIXED:** Step 0 says "Decide the verdict BEFORE writing the final response — then state it first." Explicitly prohibits the old pattern: "Never write a provisional verdict intending to 'revise it later in the same response' — line 1 cannot be revised after it is emitted." The word "preliminary" on line 69 is in the Scope Guard (an analysis-phase heuristic for when >10 files read with no findings), NOT in the final response — this is acceptable.
- **Contract envelope:** `CONTRACT {"s":"APPROVE|CHANGES_REQUESTED","b":true|false,"cr":N}` — uses `s`, `b`, `cr` keys, consistent with router's §8 post-agent validation (SKILL.md line 450).
- **Skills referenced:** cc10x:agent-common, cc10x:code-review, cc10x:verification, cc10x:codebase-hygiene — all exist.
- **References:** `references/silent-failure-red-flags.md` — exists at `plugins/cc10x/agents/references/silent-failure-red-flags.md`.
- **Tool paths:** References `tools/review_package.py` in prose (not as a tool call); integration-verifier uses `${CLAUDE_PLUGIN_ROOT}` for tool invocations.

#### 2. component-builder.md — ✓ PASS
- **BUILD_PREFLIGHT:** Present in contract as `BUILD_PREFLIGHT_EMITTED: [true if token emitted before first mutation]`. Token format documented: `BUILD_PREFLIGHT: context=pass patterns=pass uncertainty=pass mutation=open`.
- **TDD_RED_REASON_KIND:** Present in contract as `TDD_RED_REASON_KIND: "behavioral" | "error" | null`. Router's contract-override (workflow-artifact-and-hook-policy.md line 276) rejects false-RED (`error`) same as missing RED — agent contract rules section explicitly states this.
- **Contract fields:** All fields in agent's YAML contract match the router's required-fields table (workflow-artifact-and-hook-policy.md line 264).
- **Skills referenced:** cc10x:agent-common, cc10x:building, cc10x:verification — all exist.

#### 3. plan-gap-reviewer.md — ✓ PASS
- **Envelope uses "cr" not "bf":** `CONTRACT {"s":"PASS","b":false,"cr":0}`. Grep for "bf" returned zero matches. The `cr` key is explicitly documented: "cr is the blocking finding count (same envelope key every cc10x agent uses; must equal BLOCKING_FINDINGS_COUNT)."
- **Anti-anchoring (no activeContext.md):** Stronger than required — "Do NOT load `.cc10x/*.md`" (all memory files, not just activeContext.md). Also: "Do NOT infer authority from prior planner confidence, history, or planner-authored repo summaries."
- **Contract fields:** `PLANNING_REVIEW_STATUS`, `BLOCKING_FINDINGS_COUNT`, `FINDING_BUCKETS`, `REPLAN_NEEDED`, `REPLAN_REASON` — match router's structured intent fields (SKILL.md lines 457-461).
- **No skills referenced** (tools only: Read, Grep, Glob, LSP) — correct for a read-only adversarial reviewer.

#### 4. integration-verifier.md — ✓ PASS
- **Reads results.reviewer (not results.hunter):** Does not directly reference `results.reviewer` or `results.hunter` in the agent file. Instead, it receives findings via prompt: "Your prompt includes findings from code-reviewer (including Pass 1b silent failure scan) under `## Previous Agent Findings`." The router (SKILL.md line 638) reads `results.reviewer` from the workflow artifact and passes it as `## Previous Agent Findings`. This is the correct handoff pattern — the agent doesn't read the artifact directly; the router mediates.
- **Grep confirmed:** Zero matches for `results.hunter` or `results\.hunter` across all agent files.
- **Tool paths:** Uses `${CLAUDE_PLUGIN_ROOT}/tools/live_harness_runner.py` — correct.
- **Contract envelope:** `CONTRACT {"s":"PASS","b":false,"cr":0}` — consistent.

#### 5. bug-investigator.md — ✓ PASS
- **Contract fields:** All match router's required-fields table (workflow-artifact-and-hook-policy.md line 265): STATUS, VERIFICATION_RIGOR, CONFIDENCE, ROOT_CAUSE, TDD_RED_EXIT, TDD_GREEN_EXIT, VARIANTS_COVERED, BLAST_RADIUS_SCAN, SCENARIOS, ASSUMPTIONS, DECISIONS, BLOCKING, NEXT_ACTION, REMEDIATION_NEEDED, REQUIRES_REMEDIATION, REMEDIATION_REASON, NEEDS_EXTERNAL_RESEARCH, RESEARCH_REASON, MEMORY_NOTES.
- **Skills referenced:** cc10x:agent-common, cc10x:debugging, cc10x:building, cc10x:verification — all exist.

#### 6. planner.md — ✓ PASS
- **Contract fields:** All match router's required-fields table (workflow-artifact-and-hook-policy.md line 266).
- **Skill invocation:** References `cc10x:plan-review-gate` — skill directory exists at `plugins/cc10x/skills/plan-review-gate/`.
- **Skills referenced:** cc10x:agent-common, cc10x:planning, cc10x:architecture — all exist.

#### 7. doc-syncer.md — ✓ PASS
- **model: haiku** — Confirmed in frontmatter. Router SKILL.md line 334 documents this as the mechanism: "cc10x therefore ships `model: haiku` on `doc-syncer` (safely mechanical) and `model: inherit` everywhere else."
- **Contract fields:** All 9 fields match router's required-fields table: STATUS, IMPACT_LEVEL, DOC_LAYERS_EVALUATED, DOC_FILES_UPDATED, DOC_FILES_SKIPPED, SKIP_REASON, AUDIT_DOCS_CREATED, AUDIT_DOCS_UPDATED, MEMORY_NOTES.
- **Skills referenced:** cc10x:agent-common, cc10x:diff-driven-docs, cc10x:verification — all exist.

#### 8. researcher.md — ✓ PASS
- **Contract fields:** STATUS, FILE_PATH, BACKEND_MODE, SOURCES_ATTEMPTED, SOURCES_USED, QUALITY_LEVEL, KEY_FINDINGS_COUNT, WHAT_CHANGED_RECOMMENDATION, MEMORY_NOTES — match router's required-fields table.
- **Skills referenced:** cc10x:agent-common, cc10x:mcp-cli — all exist.

---

### HOOKS + SCRIPTS (9 files)

#### 9. hooks.json — ✓ PASS
- **All script paths valid:** All 7 referenced scripts exist in `plugins/cc10x/scripts/`.
- **All use `${CLAUDE_PLUGIN_ROOT}`:** Every command uses `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/..."` — no repo-relative paths.
- **10 hook events registered:**
  - PreToolUse: Edit|Write → pretooluse_guard.py (timeout 10s)
  - PreToolUse: Bash → git_guard.py (timeout 5s)
  - SessionStart: startup|resume|compact → sessionstart_context.py (timeout 10s)
  - PostToolUse: Edit|Write → posttooluse_artifact_guard.py (timeout 10s)
  - TaskCompleted → task_completed_guard.py (timeout 10s)
  - PostCompact → event_logger.py postcompact (timeout 10s)
  - SubagentStop → event_logger.py subagent_stop (timeout 10s)
  - PreCompact → state_persist.py precompact (timeout 5s)
  - Stop → state_persist.py stop (timeout 3s)
  - StopFailure → event_logger.py stop_failure (timeout 3s, async)
  - InstructionsLoaded → event_logger.py instructions_loaded (timeout 5s, async)
- **No new hooks added beyond what the router policy documents** (workflow-artifact-and-hook-policy.md lists exactly these hook categories).

#### 10. cc10x_git_guard.py — ✓ PASS (CRITICAL)
- **Approval token logic:**
  - Token file: `.cc10x/state/git-approval.json`
  - Token format: `{"wf": "...", "operations": ["push"|"branch-delete"], "expires_at": "<UTC ISO>"}`
  - `consume_approval(operation)`: reads token, checks `expires_at` (ISO format, timezone-aware), checks mtime backstop (MAX_TOKEN_AGE_SECONDS=600=10min), checks if `operation` is in `operations` list, **deletes token regardless of match** (single-use).
  - Returns `token["wf"]` if matched, `None` otherwise.
- **Token-approvable operations:** `push` (git push) and `branch-delete` (git branch -D) — and ONLY those two.
- **Unconditionally blocked (no token path):** force-push (`--force`/`-f`/`--force-with-lease`), `reset --hard`, `clean -f`, `checkout .`, `checkout -- .`, `checkout *`.
- **Output format:** Uses `pretool_deny()` from hooklib, which emits modernized `hookSpecificOutput` JSON with `hookEventName: "PreToolUse"`, `permissionDecision: "deny"`, `permissionDecisionReason`.
- **Consistency with router:** Router's build-workflow.md line 231 documents the exact same token format (`{"wf", "operations": ["push"] or ["branch-delete"], "expires_at": "now+10min"}`), same 10-minute expiry, same single-use consumption, same unconditionally-blocked operations. The guard's `MAX_TOKEN_AGE_SECONDS=600` matches the router's `now+10min`.

#### 11. cc10x_posttooluse_artifact_guard.py — ✓ PASS (CRITICAL)
- **mtime-latest footgun FIXED:** The `workflow_artifact_is_fresh()` check is scoped to artifact-only writes:
  - `target_is_artifact = is_workflow_artifact(path)` — determines if the written file is a workflow artifact.
  - Freshness check (`workflow_artifact_is_fresh(artifact_path)`) only runs inside `if target_is_artifact:` block (line 89).
  - `stale-artifact-write` reason only appended when `target_is_artifact` (line 93).
- **Blocking scoped to artifact writes only:**
  - `blocking_reasons` filtered to hard-corruption only (`artifact-json:`, `missing-keys:`) — soft reasons (`missing-event-log`, `stale-artifact-write`) stay audit-only.
  - Exit 2 (block) only when `decision == "block" and target_is_artifact and blocking_reasons` (line 128).
  - Non-artifact writes: decision is always `"audit"`, never blocks (line 114).
- **Docstring explicitly documents the fix:** "For any other Edit/Write, audit the latest workflow artifact for telemetry but NEVER block: a malformed or legacy artifact from an old workflow must not veto unrelated writes elsewhere in the project."

#### 12. cc10x_hooklib.py — ✓ PASS
- **Modernized output format:** `pretool_deny()` emits `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}`.
- **`session_context()`** emits `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}}`.
- **Helper functions:** `state_root()`, `workflows_dir()`, `latest_workflow_file()`, `read_latest_workflow_state()`, `read_workflow_state()`, `workflow_artifact_is_fresh()`, `parse_metadata()` — all correct.
- **STATE_VERSION = "v11"** — consistent with plugin.json version 11.1.0.

#### 13. cc10x_event_logger.py — ✓ PASS
- Handles 4 event types: postcompact, subagent_stop, instructions_loaded, stop_failure.
- All audit/telemetry only — never blocks (always returns 0).
- PostCompact writes `compact_occurred` event to workflow event log.

#### 14. cc10x_state_persist.py — ✓ PASS
- Handles precompact and stop events.
- Writes state snapshot to `.cc10x/precompact-state.json` or `.cc10x/stop-state.json`.
- Persistence only — never blocks.
- Defensive: skips continuation stops (`stop_hook_active`).

#### 15. cc10x_pretooluse_guard.py — ✓ PASS
- Guards protected memory files: activeContext.md, patterns.md, progress.md.
- Only blocks when `mode.get("memoryWrites") == "block"`.
- Uses `pretool_deny()` (modernized output).

#### 16. cc10x_sessionstart_context.py — ✓ PASS
- Injects workflow context on session start/resume/compact.
- Uses `session_context()` (modernized `hookSpecificOutput` format).
- Graceful no-op when no workflow payload exists.

#### 17. cc10x_task_completed_guard.py — ✓ PASS
- Validates task metadata (required metadata lines: wf, kind, origin, phase, plan, scope, reason).
- Validates memory task completion (origin=router, router-only marker, subject prefix, workflow artifact match, memory_finalized event).
- Only blocks when `mode.get("taskMetadata") == "block"`.

---

## (B) Agent-Router Consistency (Contract Fields Match)

| Agent | Envelope Keys | Required Fields Match | Contract Override Match | Verdict |
|-------|--------------|---------------------|----------------------|---------|
| code-reviewer | s, b, cr | N/A (read-only, no YAML) | APPROVE+critical→CHANGES_REQUESTED; rubber-stamp fallback; Pass 1b scope check | ✓ MATCH |
| component-builder | N/A (YAML) | All 23 fields present | TDD_RED_REASON_KIND=behavioral; BUILD_PREFLIGHT_EMITTED=true | ✓ MATCH |
| plan-gap-reviewer | s, b, cr | N/A (read-only) | PASS requires BLOCKING_FINDINGS_COUNT=0, REPLAN_NEEDED=false | ✓ MATCH |
| integration-verifier | s, b, cr | N/A (read-only) | PASS+critical→FAIL; scenario reconciliation | ✓ MATCH |
| bug-investigator | N/A (YAML) | All 18 fields present | STATUS=FIXED requires TDD evidence, BLAST_RADIUS_SCAN, loop | ✓ MATCH |
| planner | N/A (YAML) | All 22 fields present | PLAN_CREATED requires GATE_PASSED, CONFIDENCE≥50, etc. | ✓ MATCH |
| doc-syncer | N/A (YAML) | All 9 fields present | COMPLETE/SKIPPED/PARTIAL/FAIL gates | ✓ MATCH |
| researcher | N/A (YAML) | All 8 fields present | N/A (no override in router) | ✓ MATCH |

**All agent contracts are consistent with the modified router.**

---

## (C) Hook Integrity (All Scripts Exist, Paths Valid)

| Hook Event | Script | Exists | Path Format | Timeout |
|-----------|--------|--------|-------------|---------|
| PreToolUse (Edit\|Write) | cc10x_pretooluse_guard.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| PreToolUse (Bash) | cc10x_git_guard.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 5s |
| SessionStart | cc10x_sessionstart_context.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| PostToolUse (Edit\|Write) | cc10x_posttooluse_artifact_guard.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| TaskCompleted | cc10x_task_completed_guard.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| PostCompact | cc10x_event_logger.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| SubagentStop | cc10x_event_logger.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 10s |
| PreCompact | cc10x_state_persist.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 5s |
| Stop | cc10x_state_persist.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 3s |
| StopFailure | cc10x_event_logger.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 3s (async) |
| InstructionsLoaded | cc10x_event_logger.py | ✓ | ${CLAUDE_PLUGIN_ROOT} | 5s (async) |

**All 7 scripts exist. All 11 hook registrations use ${CLAUDE_PLUGIN_ROOT}. No new hooks added.**

---

## (D) Git Guard Verification (Token Logic, Output Format)

### Token Logic — ✓ CORRECT
1. **Token location:** `.cc10x/state/git-approval.json`
2. **Token schema:** `{"wf": "...", "operations": ["push"|"branch-delete"], "expires_at": "<UTC ISO>"}`
3. **Freshness check:** `expires_at` parsed as ISO 8601 with timezone; compared to `datetime.now(timezone.utc)`.
4. **Mtime backstop:** `MAX_TOKEN_AGE_SECONDS = 600` (10 minutes) — even if `expires_at` is missing/garbled, a token older than 10 minutes by file mtime is stale.
5. **Operation matching:** `operation in token["operations"]` (list membership check).
6. **Single-use consumption:** Token file is `unlink()`-ed regardless of match result — a stale or mismatched token is consumed, preventing lingering approval.
7. **Approvable operations:** `push` and `branch-delete` only.
8. **Unconditionally blocked:** force-push, reset --hard, clean -f, checkout ., checkout -- ., checkout * — these have `operation=None` (no token path).

### Output Format — ✓ MODERNIZED
- Uses `pretool_deny()` from `cc10x_hooklib.py`, which emits:
```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}
```
- This is the modern Claude Code hook output format (not legacy stdout/stderr).

### Router Consistency — ✓ MATCH
- Router's `build-workflow.md` line 231 documents the exact same token format, 10-minute expiry, single-use consumption, and unconditionally-blocked operations.
- Router writes the token ONLY after user's explicit BUILD-DONE menu choice — the guard enforces this by blocking without a token.

---

## (E) Artifact Guard Verification (mtime Fix)

### The Footgun — ✓ FIXED
**Problem (pre-fix):** The `workflow_artifact_is_fresh()` check would run on EVERY Edit/Write, checking the mtime of the LATEST workflow artifact. If an old workflow's artifact was stale (which it always would be for any completed workflow), any unrelated file write would be blocked or flagged as "stale-artifact-write."

**Fix (current code):**
1. `is_workflow_artifact(path)` determines if the written file itself is a workflow artifact (`.cc10x/workflows/*.json`, excluding `.events.jsonl`).
2. The freshness check (`workflow_artifact_is_fresh()`) ONLY runs when `target_is_artifact=True` (line 89-93).
3. The `stale-artifact-write` reason is ONLY appended when `target_is_artifact=True`.
4. Blocking (exit 2) ONLY occurs when `decision == "block" and target_is_artifact and blocking_reasons` (line 128).
5. For non-artifact writes: `decision` is always `"audit"` (line 114), `blocking_reasons` is never checked, exit code is always 0.
6. `blocking_reasons` is filtered to hard-corruption only (`artifact-json:`, `missing-keys:`) — soft reasons (`missing-event-log`, `stale-artifact-write`) stay audit-only even for artifact writes.

**Result:** A stale artifact from an old workflow can no longer veto unrelated writes. Only a direct write to a corrupt/malformed workflow artifact triggers blocking.

---

## (F) Any NEW Issues or Regressions

**No new issues or regressions found.**

Detailed checks performed:
- `grep -rn "results.hunter" plugins/cc10x/agents/` → **0 matches** (confirmed eliminated)
- `grep -rn "bf" plugins/cc10x/agents/plan-gap-reviewer.md` → **0 matches** (confirmed "cr" used)
- `grep -rn "CLAUDE_PLUGIN_ROOT" plugins/cc10x/agents/` → **1 match** (integration-verifier.md, for live_harness_runner.py — correct)
- `grep -rn "plugins/cc10x/tools" plugins/cc10x/agents/` → **0 matches** (no repo-relative tool paths)
- All 11 referenced skills exist as directories.
- All 2 referenced tools exist as files.
- All 7 hook scripts exist.
- All agent contract fields match router's required-fields and contract-override tables.
- No stale `hunter` agent file exists in `plugins/cc10x/agents/`.
- `doc-syncer` `model: haiku` confirmed and consistent with router's advisory model-tier policy.
- Git-guard `MAX_TOKEN_AGE_SECONDS=600` matches router's `now+10min` token expiry.
- Artifact guard mtime check scoped to artifact-only writes.

---

## (G) VERDICT

**✅ PASS — Agents and hooks are intact and fully consistent with the modified router.**

All 8 agent files, 9 hook/script files, and hooks.json have been verified against the modified router (SKILL.md + references). Specifically:

1. **Consolidated reviewer/hunter:** code-reviewer.md integrates Pass 1b (silent failure scan) as step 4, explicitly replacing the standalone hunter. No `results.hunter` references remain in any agent. Router dispatches exactly ONE code-reviewer per review point.

2. **Model-tier advisory:** doc-syncer.md ships `model: haiku` (the only agent with a non-inherit model). Router SKILL.md line 334 documents this as the mechanism realization and explicitly states the tier table is advisory. All other agents use `model: inherit`.

3. **Git-guard approval token:** Token logic in `cc10x_git_guard.py` is fully consistent with router's `build-workflow.md` §BUILD-DONE finishing. Single-use, 10-minute expiry, mtime backstop, only `push` and `branch-delete` are token-approvable. Output uses modernized `hookSpecificOutput` format.

4. **Artifact-access rule (mtime fix):** `cc10x_posttooluse_artifact_guard.py` correctly scopes the freshness check and blocking to artifact-only writes. Non-artifact writes are audit-only. The stale-artifact footgun is eliminated.

5. **Verdict-first incoherence:** code-reviewer.md step 0 explicitly requires the verdict to be settled BEFORE the final response, and prohibits provisional/revisionable verdicts on line 1.

6. **Plan-gap-reviewer envelope:** Uses `cr` (not `bf`), with anti-anchoring that goes beyond activeContext.md (blocks all `.cc10x/*.md` files).

All contract fields, envelope keys, skill references, tool paths, and hook registrations are consistent. No regressions detected.