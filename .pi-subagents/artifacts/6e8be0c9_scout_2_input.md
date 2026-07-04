# Task for scout

DEEP ANALYSIS: multica-ai/andrej-karpathy-skills — Read EVERY file and extract what cc10x should steal.

This is a small repo. Read EVERY file:
- /Users/rom.iluz/Dev/multica-karpathy-skills/README.md
- /Users/rom.iluz/Dev/multica-karpathy-skills/CLAUDE.md (THIS IS THE KEY FILE — the Karpathy guidelines)
- /Users/rom.iluz/Dev/multica-karpathy-skills/CURSOR.md
- /Users/rom.iluz/Dev/multica-karpathy-skills/EXAMPLES.md
- /Users/rom.iluz/Dev/multica-karpathy-skills/README.zh.md (skip if not readable)
- /Users/rom.iluz/Dev/multica-karpathy-skills/skills/karpathy-guidelines/SKILL.md

Also read the original Karpathy quotes in the README — these are the problems the guidelines solve.

Compare against cc10x's agent-common/SKILL.md (the shared preamble) and the router's hard rules.

Analyze:
1. What are the 4 principles? (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)
2. How does each principle address a specific Karpathy observation about LLM failures?
3. What unique patterns does it use to enforce these principles?
4. How does this compare to cc10x's agent-common preamble?
5. What could cc10x adopt from this? Is there anything here that cc10x doesn't already have?
6. Is the 'confusion management' concept unique? Does cc10x have anything like it?
7. Is the 'surgical changes' concept unique? How does it compare to cc10x's scope guard?

Output a structured report of unique patterns cc10x should adopt, if any.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/6e8be0c9/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/6e8be0c9/comparison-15-karpathy-guidelines.md
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