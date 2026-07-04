# Task for scout

DEEP ANALYSIS: addyosmani/agent-skills — Read EVERY skill file and extract what cc10x should steal.

Read EVERY file in /Users/rom.iluz/Dev/addyosmani-agent-skills/skills/ (all 24 skills, every SKILL.md):
- api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills

Also read:
- /Users/rom.iluz/Dev/addyosmani-agent-skills/references/ (ALL 7 reference files)
- /Users/rom.iluz/Dev/addyosmani-agent-skills/CLAUDE.md
- /Users/rom.iluz/Dev/addyosmani-agent-skills/README.md

For each skill, analyze:
1. What does it teach?
2. What patterns does it use (rationalization tables, red flags, checklists, etc.)?
3. What UNIQUE patterns does it have that cc10x doesn't?
4. What could cc10x adopt from it?

Pay special attention to:
- `doubt-driven-development` — this is a unique concept, what is it?
- `context-engineering` — how does Addy think about context management?
- `source-driven-development` — what is this pattern?
- `spec-driven-development` — how does it compare to cc10x's planning?
- `idea-refine` and `interview-me` — are these brainstorming alternatives?
- `code-simplification` — what patterns does it teach?

Output a structured report with every unique pattern found, marked by impact (HIGH/MEDIUM/LOW) and which cc10x file it should go into.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/99888eba/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/99888eba/comparison-11-addyosmani-skills.md
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