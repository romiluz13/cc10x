# Task for scout

DEEP COMPARISON: Orchestration & Routing Architecture

Read EVERY file in these directories:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/ (SKILL.md + all references/*.md + skeleton JSON)
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/subagent-driven-development/ (ALL files), /Users/rom.iluz/Dev/superpowers/skills/dispatching-parallel-agents/SKILL.md, /Users/rom.iluz/Dev/superpowers/skills/executing-plans/SKILL.md
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/triage/ (ALL files), /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/to-issues/SKILL.md, /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/to-prd/SKILL.md

Analyze:
1. How does each project route work? (router kernel vs skill-driven vs manual)
2. How does each project decide what agent to dispatch?
3. How does each project manage task dependencies (DAGs, blockedBy)?
4. How does each project handle parallel vs sequential execution?
5. How does each project handle fallbacks when things go wrong?
6. What orchestration patterns does cc10x have that the others DON'T?
7. What orchestration patterns do the others have that cc10x DOESN'T?
8. Rate each project's orchestration sophistication 1-10 and explain why.

Output a structured comparison table + verdict on who wins orchestration and why.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/94c57dfa/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/94c57dfa/comparison-01-orchestration.md
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