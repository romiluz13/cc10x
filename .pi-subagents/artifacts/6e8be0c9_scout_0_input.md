# Task for scout

DEEP ANALYSIS: addyosmani/agent-skills — Read the MOST IMPORTANT skills and extract what cc10x should steal.

Read these skill files from /Users/rom.iluz/Dev/addyosmani-agent-skills/skills/:
1. doubt-driven-development/SKILL.md — THIS IS UNIQUE, read every word
2. context-engineering/SKILL.md — how does Addy think about context?
3. source-driven-development/SKILL.md — what is this pattern?
4. spec-driven-development/SKILL.md — how does it compare to cc10x planning?
5. idea-refine/SKILL.md and interview-me/SKILL.md — brainstorming alternatives?
6. code-simplification/SKILL.md — what patterns?
7. incremental-implementation/SKILL.md — how does it approach building?
8. planning-and-task-breakdown/SKILL.md — compare to cc10x planning
9. debugging-and-error-recovery/SKILL.md — compare to cc10x debugging
10. code-review-and-quality/SKILL.md — compare to cc10x review
11. test-driven-development/SKILL.md — compare to cc10x TDD
12. using-agent-skills/SKILL.md — how does it bootstrap?

Also read ALL 7 reference files in /Users/rom.iluz/Dev/addyosmani-agent-skills/references/:
- accessibility-checklist.md, definition-of-done.md, observability-checklist.md, orchestration-patterns.md, performance-checklist.md, security-checklist.md, testing-patterns.md

And read /Users/rom.iluz/Dev/addyosmani-agent-skills/CLAUDE.md

For each skill, extract: What UNIQUE patterns does it have that cc10x doesn't? What could cc10x adopt? Mark by impact (HIGH/MEDIUM/LOW) and target cc10x file.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/6e8be0c9/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/6e8be0c9/comparison-11-addyosmani-skills.md
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