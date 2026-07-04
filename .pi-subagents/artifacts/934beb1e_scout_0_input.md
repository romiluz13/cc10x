# Task for scout

VERIFICATION: Router Harmony — Does the router use the full power of the system?

Read the FULL router at /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md (750+ lines) and ALL its reference files:
- references/build-workflow.md
- references/debug-workflow.md
- references/review-workflow.md
- references/plan-workflow.md
- references/remediation-and-research.md
- references/workflow-artifact-and-hook-policy.md
- references/workflow-artifact.skeleton.json

Verify:
1. Does the router reference ALL 17 skills by name? Check which skills are in SKILL_HINTS vs which are orphaned.
2. Does the router dispatch ALL 9 agents? Check the dispatcher table covers every agent.
3. Does the router use the parallel review pattern (code-reviewer || silent-failure-hunter)?
4. Does the router use the DEBUG fan-out pattern?
5. Does the router merge findings from parallel agents?
6. Are ALL workflow types (BUILD, DEBUG, REVIEW, PLAN, ORIENT) fully wired?
7. Does the router reference the new patterns (rationalization tables, red flags, etc.) or are they orphaned in skills?
8. Does the router's verifier handoff include both reviewer AND hunter findings?
9. Are there any broken file references (files that don't exist)?
10. Is the routing table consistent with the dispatcher table?

Output a PASS/FAIL for each check with exact evidence.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/934beb1e/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/934beb1e/verify-01-router-harmony.md
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