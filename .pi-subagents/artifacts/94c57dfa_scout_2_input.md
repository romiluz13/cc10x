# Task for scout

DEEP COMPARISON: TDD & Testing Methodology

Read EVERY file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/verification/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/building/SKILL.md
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/test-driven-development/ (ALL files including testing-anti-patterns.md), /Users/rom.iluz/Dev/superpowers/skills/verification-before-completion/SKILL.md
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/engineering/tdd/ (ALL files including mocking.md, tests.md)

Also search cc10x for any TDD-related content:
- grep -r 'TDD\|test.driven\|RED.*GREEN\|test.first' /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/

Analyze:
1. How does each project teach TDD? (RED-GREEN-REFACTOR cycle, test-first, etc.)
2. What testing anti-patterns does each project warn about?
3. How does each project handle test verification (Test Honesty Gates, etc.)?
4. How does each project handle mocking?
5. What TDD patterns does cc10x have that the others DON'T?
6. What TDD patterns do the others have that cc10x SHOULD adopt?
7. Rate each project's TDD methodology 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/94c57dfa/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/94c57dfa/comparison-03-tdd-testing.md
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