# Known Flaws & Recovery Patterns

Documented behaviors where CC10x orchestration encounters platform limitations and the recovery mechanisms in place.

---

## FLAW-001: Context Compaction Loses Sub-Agent Output

**Discovered:** 2026-03-01 during v7.2.0 REVIEW workflow

### What Happened

1. Router spawned `code-reviewer` sub-agent (Task #16) to review 13 changes across 6 files
2. Sub-agent completed successfully: 90,915 tokens, 42 tool uses, ~192 seconds
3. Sub-agent returned its output (Router Contract + findings) to the parent conversation
4. **Before the router could process the output**, Claude Code's context compaction triggered
5. The entire sub-agent output was lost — the conversation summary noted it existed but didn't preserve the content
6. Task #16 was marked "completed" (by the sub-agent itself) but the router had no findings, no Router Contract, no Memory Notes

### Why It Happens

Claude Code compacts conversation history when approaching context limits. Long sessions with multiple sub-agent invocations accumulate tokens. The compaction algorithm summarizes prior messages but cannot preserve structured data (Router Contracts, Memory Notes) that hasn't been extracted yet.

**The gap:** Sub-agent output arrives as a tool_result → router needs to parse it → but compaction can fire between arrival and parsing.

### How We Recovered

1. **Transcript mining (failed):** Attempted to extract the output from the JSONL transcript file. The sub-agent's `content` array was empty in the transcript — the output text wasn't persisted at the transcript level.

2. **Agent resume (succeeded):** Used the `resume` parameter with the sub-agent's `agentId`:
   ```
   Agent(subagent_type="cc10x:code-reviewer", resume="a08d9699f39bc5822",
     prompt="Your previous review output was lost during context compaction.
     Please re-output ONLY your final review findings and Router Contract YAML block.
     Do NOT redo the review from scratch.")
   ```
   The resumed agent retained its full context and re-emitted the Router Contract + findings without redoing any work. Cost: ~74K tokens (re-emission only) vs ~91K tokens (original full review).

### Mitigation Now In Place

The live router now captures memory payload **before** validation or task-state mutation after an agent returns:
> "Capture memory payload first, before validation or task-state mutation."

That closes the exact window that previously allowed compaction to land between agent return and Memory Notes extraction.

### Recommendations

1. **Keep memory capture first** — future router edits must preserve payload capture before validation or task-state mutation.
2. **Resume remains the recovery path:** When sub-agent output is lost, `resume` with `agentId` is reliable. The sub-agent retains full context and can re-emit without rework.
3. **Compact receipt patterns remain optional:** The current mitigation is sufficient without adding a second result protocol.

### Impact

- **Severity:** MEDIUM — recoverable with agent resume
- **Frequency:** Rare — requires long session + large sub-agent output + compaction timing
- **Data loss:** None — sub-agent's actual work (file reads, analysis) was done. Only the report was lost.
- **Cost:** ~74K extra tokens for re-emission (acceptable)

---

## FLAW-002: No complexity gradient — trivial work paid the full chain

**Discovered:** 2026-06-17 (v11 revitalization audit) · **Fixed:** v11.0.0

Retiring the QUICK path conflated "everything routes through the router" (kept) with "everything pays the full 6-task / 4-subagent chain" (the defect). A one-line edit triggered builder → reviewer + hunter → verifier → doc-sync → memory. The "Trivial" classifier only suppressed a clarifying question, never the task graph.

**Fix:** BUILD task graph branches on `build_scope` (`references/build-workflow.md`). Trivial scope runs a reduced builder → verifier → memory graph and escalates to the full chain on any `SCOPE_INCREASES`/`BLOCKED_ITEMS`. Router remains the sole entry point. DEBUG's Variant scenario became conditional (`VARIANTS_NOT_APPLICABLE`) to stop fabrication pressure on no-variant bugs.

## FLAW-003: Durable artifact was hand-typed escaped JSON

**Discovered:** 2026-06-17 · **Fixed:** v11.0.0

The router hand-emitted a 2,341-char escaped-JSON artifact — exactly the task LLMs fail at — and the PostToolUse guard that detected corruption only logged it (audit mode), so the model never saw the failure.

**Fix:** ship `references/workflow-artifact.skeleton.json`; router copies it and edits only the live fields, then reads it back before any child task. The artifact guard now blocks (exit 2) on parse-error/missing-keys with `artifactIntegrity: block`.

## FLAW-004: doc-syncer read the legacy memory path + lacked TaskUpdate

**Discovered:** 2026-06-17 · **Fixed:** v11.0.0

doc-syncer read `.claude/cc10x/v10/` (a path nothing else wrote to) and was told to call `TaskUpdate` without the tool granted — risking a hung BUILD finalization.

**Fix:** path corrected to `.cc10x/` (and de-versioned project-wide in v11); `TaskUpdate` added to its frontmatter.

## v11.0.0 — state de-versioned to `.cc10x/`

The on-disk state namespace dropped its version segment (`.cc10x/v10/` → `.cc10x/`); the version lives only in `plugin.json`/GitHub. Fresh-start, no migration. The `cc10x_context_migration.py` script was removed. A `cc10x_doc_consistency_check.py` self-test now fails CI if README counts/versions drift from disk.

---

*Add new flaws below as they are discovered.*
