# Task for scout

DEEP COMPARISON: Planning & Architecture Methodology

Read EVERY file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/planning/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/architecture/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/exploration/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/references/plan-workflow.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/planner.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/plan-gap-reviewer.md (if exists), /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/plan-review-gate/SKILL.md
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/writing-plans/ (ALL files), /Users/rom.iluz/Dev/superpowers/skills/brainstorming/ (ALL files), /Users/rom.iluz/Dev/superpowers/skills/executing-plans/SKILL.md
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/codebase-design/ (ALL files), /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/domain-modeling/ (ALL files), /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/improve-codebase-architecture/ (ALL files), /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/prototype/ (ALL files)

Analyze:
1. How does each project approach planning? (plans, RFCs, design docs)
2. How does each project handle architecture decisions?
3. What planning gates does each project enforce? (review, gap analysis)
4. How does each project handle brainstorming/ideation?
5. What planning patterns does cc10x have that the others DON'T?
6. What planning patterns do the others have that cc10x SHOULD adopt?
7. Rate each project's planning methodology 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/cf3397b3/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/cf3397b3/comparison-06-planning-architecture.md
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