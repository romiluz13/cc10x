# Task for scout

VERIFICATION: End-to-End Trace — Trace a complete BUILD workflow from user request to completion, verifying every component fires.

Read the router SKILL.md and all reference files, then trace this scenario step by step:

**Scenario:** User says 'build a user authentication system with JWT tokens'

Trace EVERY step:
1. How does the router detect this as BUILD? (what keywords match?)
2. What memory files are loaded?
3. How is the workflow artifact created? (skeleton copy, placeholder fill, read-back gate)
4. What event log entry is written?
5. What task graph is created? (list all tasks with their phases and blockedBy)
6. How is the builder dispatched? (what prompt scaffold? what SKILL_HINTS?)
7. After builder completes, what does the router do? (validate output, persist results, read-back gate, event log append)
8. How are reviewer + hunter dispatched in parallel? (same message? what prompts?)
9. After both complete, how does the router merge findings?
10. How is the verifier dispatched with the merged findings?
11. After verifier passes, how is doc-syncer dispatched?
12. After doc-syncer, how does memory-finalize work?
13. What hooks fire during this entire process? (SessionStart, PreToolUse, PostToolUse, TaskCompleted, PreCompact, Stop)
14. What happens if the builder reports SCOPE_INCREASES?
15. What happens if the reviewer returns CHANGES_REQUESTED?

For each step, cite the EXACT line/section in the router or reference files that defines the behavior. Output PASS/FAIL for each step.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/fcf3b73a/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/fcf3b73a/verify-06-end-to-end-trace.md
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