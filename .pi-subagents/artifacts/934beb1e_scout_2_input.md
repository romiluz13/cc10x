# Task for scout

VERIFICATION: Autonomous Invocation — Does every workflow activate without manual intervention?

Read the FULL router at /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md and verify that EVERY workflow can be autonomously invoked:

1. BUILD workflow: Can the router detect a BUILD request, create the workflow artifact, dispatch the builder, and run the full chain (builder → [reviewer || hunter] → verifier → doc-syncer → memory) without user intervention?
2. DEBUG workflow: Can the router detect an error, create the workflow, dispatch the bug-investigator, and run the full chain (investigator → reviewer → verifier → memory) autonomously?
3. REVIEW workflow: Can the router detect a review request and dispatch the code-reviewer autonomously?
4. PLAN workflow: Can the router detect a planning request, dispatch the planner, and run the fresh-review DAG (plan → gap-review-1 → re-plan → gap-review-2 → memory) autonomously?
5. ORIENT workflow: Can the router detect an orientation request and run read-only without spawning agents?

For each workflow, trace the EXACT path from user request → router detection → workflow creation → agent dispatch → completion. Identify any gaps where manual intervention would be needed.

Also verify:
6. Does the SessionStart hook inject workflow context for resume?
7. Does the router's resume logic work for interrupted workflows?
8. Does the memory-finalize task run automatically at workflow end?
9. Does the event log get appended automatically (via the PostToolUse guard)?
10. Does the artifact freshness check run after every task completion?

Output PASS/FAIL for each with evidence.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/934beb1e/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/934beb1e/verify-03-autonomous-invocation.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

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