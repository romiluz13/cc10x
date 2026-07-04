# Task for scout

DEEP COMPARISON: Code Review & Quality Enforcement

Read EVERY file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/code-reviewer.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/silent-failure-hunter.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/references/silent-failure-red-flags.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/code-review/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/references/review-workflow.md
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/receiving-code-review/SKILL.md, /Users/rom.iluz/Dev/superpowers/skills/requesting-code-review/ (ALL files including code-reviewer.md)
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/code-review/SKILL.md

Analyze:
1. How does each project structure code review? (passes, dimensions, severity)
2. How does each project handle review feedback (receiving, acting on, resolving)?
3. What review dimensions does each project cover? (security, perf, quality, etc.)
4. How does each project enforce review gates (blocking vs advisory)?
5. Parallel review patterns — who has them and how sophisticated?
6. What review patterns does cc10x have that the others DON'T?
7. What review patterns do the others have that cc10x SHOULD adopt?
8. Rate each project's code review methodology 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/94c57dfa/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/94c57dfa/comparison-05-code-review.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: reviewed
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope
- criterion-2: Return evidence sufficient for an independent acceptance review

Required evidence: changed-files, tests-added, commands-run, validation-output, residual-risks, no-staged-files

Review gate: required by reviewer.

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