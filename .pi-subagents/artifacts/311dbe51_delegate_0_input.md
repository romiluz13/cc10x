# Task for delegate

DEEP REVIEW — Agents + Hooks + Scripts (unchanged by other agent, but verify consistency with router changes)

The #1 rule: if the orchestration layer is broken, the entire system is broken.

The router was modified by another agent (consolidated reviewer/hunter, model-tier advisory, git-guard token, artifact-access rule). Your job is to verify the AGENTS and HOOKS are still consistent with the modified router.

READ THESE FILES FULLY:

AGENTS (read all 8):
1. plugins/cc10x/agents/code-reviewer.md — CRITICAL: verify it no longer expects a separate hunter, Pass 1b is integrated, verdict-first wording fixed
2. plugins/cc10x/agents/component-builder.md — verify BUILD_PREFLIGHT and TDD_RED_REASON_KIND are in the contract
3. plugins/cc10x/agents/plan-gap-reviewer.md — verify envelope uses "cr" not "bf", anti-anchoring (no activeContext.md)
4. plugins/cc10x/agents/integration-verifier.md — verify it reads results.reviewer not results.hunter
5. plugins/cc10x/agents/bug-investigator.md
6. plugins/cc10x/agents/planner.md
7. plugins/cc10x/agents/doc-syncer.md — verify model: haiku
8. plugins/cc10x/agents/researcher.md

HOOKS + SCRIPTS (read all):
9. plugins/cc10x/hooks/hooks.json
10. plugins/cc10x/scripts/cc10x_git_guard.py — CRITICAL: verify approval token logic, modernized output format
11. plugins/cc10x/scripts/cc10x_posttooluse_artifact_guard.py — CRITICAL: verify mtime-latest rescoped to artifact-only writes
12. plugins/cc10x/scripts/cc10x_hooklib.py
13. plugins/cc10x/scripts/cc10x_event_logger.py
14. plugins/cc10x/scripts/cc10x_state_persist.py
15. plugins/cc10x/scripts/cc10x_pretooluse_guard.py
16. plugins/cc10x/scripts/cc10x_sessionstart_context.py
17. plugins/cc10x/scripts/cc10x_task_completed_guard.py

For EACH file check:
1. Does it reference any agent/skill/tool path that doesn't exist?
2. Are tool paths using ${CLAUDE_PLUGIN_ROOT} (not repo-relative)?
3. For agents: does the contract match what the router expects? (envelope keys, required fields)
4. For code-reviewer: is Pass 1b integrated? Is the verdict-first "preliminary/revise" incoherence fixed?
5. For plan-gap-reviewer: does it use "cr" not "bf" in the envelope?
6. For integration-verifier: does it read results.reviewer (not results.hunter)?
7. For git_guard.py: does the approval token work? Is the output format modernized (hookSpecificOutput)?
8. For artifact_guard.py: is the mtime-latest footgun fixed (scoped to artifact writes only)?
9. For hooks.json: are all script paths valid? Any new hooks added?

Also run:
- grep -rn "results.hunter\|results\.hunter" plugins/cc10x/agents/ — should be gone
- grep -rn "bf" plugins/cc10x/agents/plan-gap-reviewer.md — should be "cr" now
- grep -rn "CLAUDE_PLUGIN_ROOT" plugins/cc10x/agents/ — agents should use this for tool paths
- grep -rn "plugins/cc10x/tools" plugins/cc10x/agents/ — should use ${CLAUDE_PLUGIN_ROOT}/tools/ not repo-relative

Return a structured report with:
(A) Per-file analysis
(B) Agent-router consistency (contract fields match)
(C) Hook integrity (all scripts exist, paths valid)
(D) Git guard verification (token logic, output format)
(E) Artifact guard verification (mtime fix)
(F) Any NEW issues or regressions
(G) VERDICT: are agents and hooks intact and consistent with the modified router?

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/311dbe51/file-only
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```