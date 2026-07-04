# Task for scout

DEEP ANALYSIS: EveryInc/compound-engineering-plugin — Read the MOST IMPORTANT skills and extract what cc10x should steal.

Read these skill files from /Users/rom.iluz/Dev/everyinc-compound-engineering/skills/ (read SKILL.md in each):
1. ce-compound/SKILL.md — THIS IS THE CORE CONCEPT, read every word
2. ce-compound-refresh/SKILL.md — what is refresh?
3. ce-work/SKILL.md — how does it manage work?
4. ce-worktree/SKILL.md — worktree management
5. ce-proof/SKILL.md — how does it verify?
6. ce-dogfood/SKILL.md — what is this?
7. ce-sweep/SKILL.md — what does this do?
8. ce-pov/SKILL.md — what is this?
9. ce-strategy/SKILL.md — what is this?
10. ce-product-pulse/SKILL.md — what is this?
11. ce-brainstorm/SKILL.md — compare to cc10x exploration
12. ce-plan/SKILL.md — compare to cc10x planning
13. ce-code-review/SKILL.md — compare to cc10x review
14. ce-debug/SKILL.md — compare to cc10x debugging
15. lfg/SKILL.md — what is this?

Also read:
- /Users/rom.iluz/Dev/everyinc-compound-engineering/CONCEPTS.md — what concepts does it define?
- /Users/rom.iluz/Dev/everyinc-compound-engineering/CLAUDE.md
- /Users/rom.iluz/Dev/everyinc-compound-engineering/README.md (first 100 lines)

For each skill, extract: What UNIQUE patterns does it have that cc10x doesn't? What could cc10x adopt? Mark by impact (HIGH/MEDIUM/LOW) and target cc10x file.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/6e8be0c9/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/6e8be0c9/comparison-13-everyinc-skills.md
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