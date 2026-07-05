# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

READ-ONLY AUDIT. Do NOT write, edit, or create any files anywhere. Return all findings as your final message text only.

cwd: /Users/rom.iluz/Dev/cc10x

SCOPE: The cc10x Router Kernel — the orchestration brain of the plugin.
Files to read in full:
- plugins/cc10x/skills/cc10x-router/SKILL.md
- plugins/cc10x/skills/cc10x-router/references/*.md and workflow-artifact.skeleton.json
- plugins/cc10x/skills/cc10x-router/evals/*.md
- plugins/cc10x/hooks/hooks.json and hooks/README.md
- plugins/cc10x/scripts/cc10x_pretooluse_guard.py, cc10x_posttooluse_artifact_guard.py, cc10x_task_completed_guard.py, cc10x_sessionstart_context.py, cc10x_state_persist.py, cc10x_event_logger.py, cc10x_git_guard.py, cc10x_hooklib.py
- plugins/cc10x/config/hook-mode.json
- docs/known-flaws.md (already summarized here, but re-read for full detail)

BASELINE COMPARISON: use `git show v11.1.0:<path>` and `git diff v11.1.0..HEAD -- <path>` to compare current files against the pre-refactor v11.1.0 tag. v11.1.0 equivalents include plugins/cc10x/skills/cc10x-router/**, plugins/cc10x/scripts/cc10x_instructions_loaded_audit.py, cc10x_postcompact_context.py, cc10x_precompact_state.py, cc10x_reference_benchmark.py, cc10x_stop_failure_log.py, cc10x_stop_persist.py, cc10x_subagent_stop_audit.py (all of which were removed/renamed in the refactor — figure out where each one's FUNCTION went, if anywhere).

VERIFY THESE SPECIFIC CLAIMED INNOVATIONS (from docs/plans/v12-keep-inventory.md) ARE STILL FUNCTIONALLY INTACT, not just mentioned in prose:
1. Workflow artifacts (.cc10x/workflows/{uuid}.json) durable state
2. Intent routing table (ERROR > PLAN > REVIEW > ORIENT > BUILD priority order)
3. Complexity gradient (trivial vs standard) with escalation on SCOPE_INCREASES/BLOCKED_ITEMS
4. Per-role model-tier policy
5. Inline-fallback mode when Agent primitive unavailable
6. Dispatcher table (phase -> agent mapping)
7. Dispatch-by-reference (paths not pasted content)
8. CONTRACT envelope + validation (structured, parseable, not prose)
9. Change-something-before-re-dispatch rule
10. Circuit breaker (max 3 remediation cycles), cycle-cap gate
11. Re-review precondition gate (REM-FIX needs COVERING_TESTS+TEST_COMMAND+TEST_OUTPUT before re-review)
12. Task metadata format (wf:kind:origin:phase:plan:scope:reason)
13. Memory finalization (router-owned single-writer, KEEP/SUMMARIZE/DROP rubric)

Also verify the 4 mitigations in docs/known-flaws.md (FLAW-001 memory-capture-before-validation ordering, FLAW-002 complexity gradient, FLAW-003 workflow-artifact.skeleton.json + hook-enforced block on corruption, FLAW-004 doc-syncer path + TaskUpdate) are still true of the CURRENT code, not just the v11.0.0 code they were fixed in.

Also sanity-check hooks.json against real Claude Code plugin hook semantics you know: are hook event names valid (PreToolUse, PostToolUse, SessionStart, TaskCompleted, PostCompact, SubagentStop, PreCompact, Stop, StopFailure, InstructionsLoaded)? Do matchers make sense? Any exit-code / blocking semantics claims in the scripts that don't match how Claude Code actually consumes hook stdout/exit codes?

OUTPUT FORMAT: For each of the 13 items + 4 flaws, state INTACT / WEAKENED / LOST / IMPROVED with file:line evidence. Then list all issues found, severity-tagged CRITICAL/HIGH/MEDIUM/LOW, with file:line citations. End with a one-paragraph verdict on whether the router kernel is publish-ready.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

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