# Task for scout

DEEP COMPARISON: Debugging & Root Cause Analysis

Read EVERY file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/debugging/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/references/debug-workflow.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/bug-investigator.md
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/systematic-debugging/ (ALL files: SKILL.md, CREATION-LOG.md, condition-based-waiting.md, defense-in-depth.md, root-cause-tracing.md, test-academic.md, test-pressure-1.md, test-pressure-2.md, test-pressure-3.md)
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/diagnosing-bugs/SKILL.md

Analyze:
1. How does each project approach debugging? (systematic vs ad-hoc)
2. What root cause analysis techniques does each project use?
3. How does each project handle pressure/debugging under time constraints?
4. Defense-in-depth patterns — what does each project recommend?
5. How does each project handle debugging multi-file issues?
6. What debugging patterns does cc10x have that the others DON'T?
7. What debugging patterns do the others have that cc10x SHOULD adopt?
8. Rate each project's debugging methodology 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/94c57dfa/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/94c57dfa/comparison-04-debugging.md
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