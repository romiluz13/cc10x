# Task for scout

DEEP ANALYSIS: EveryInc/compound-engineering-plugin — Read EVERY skill and extract what cc10x should steal.

This is a large repo with 28+ skills. Read EVERY SKILL.md in /Users/rom.iluz/Dev/everyinc-compound-engineering/skills/:
- ce-brainstorm, ce-code-review, ce-commit, ce-commit-push-pr, ce-compound, ce-compound-refresh, ce-debug, ce-doc-review, ce-dogfood, ce-explain, ce-ideate, ce-optimize, ce-plan, ce-polish, ce-pov, ce-product-pulse, ce-promote, ce-proof, ce-resolve-pr-feedback, ce-riffrec-feedback-analysis, ce-setup, ce-simplify-code, ce-strategy, ce-sweep, ce-test-browser, ce-test-xcode, ce-work, ce-worktree, lfg

Also read:
- /Users/rom.iluz/Dev/everyinc-compound-engineering/CLAUDE.md
- /Users/rom.iluz/Dev/everyinc-compound-engineering/AGENTS.md
- /Users/rom.iluz/Dev/everyinc-compound-engineering/CONCEPTS.md
- /Users/rom.iluz/Dev/everyinc-compound-engineering/README.md
- /Users/rom.iluz/Dev/everyinc-compound-engineering/plugin.json

For each skill, analyze:
1. What does it teach?
2. What patterns does it use?
3. What UNIQUE patterns does it have that cc10x doesn't?
4. What could cc10x adopt?

Pay special attention to:
- `ce-compound` and `ce-compound-refresh` — what is the 'compound' concept?
- `ce-work` and `ce-worktree` — how do they manage work?
- `ce-proof` — how does it verify?
- `ce-dogfood` — what is this pattern?
- `ce-sweep` — what does this do?
- `ce-pov` and `ce-strategy` — are these unique?
- `ce-product-pulse` — what is this?
- `ce-riffrec-feedback-analysis` — what is this?
- `lfg` — what is this skill?
- `CONCEPTS.md` — what concepts does this project define?

Output a structured report with every unique pattern found, marked by impact (HIGH/MEDIUM/LOW) and which cc10x file it should go into.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/99888eba/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/99888eba/comparison-13-everyinc-skills.md
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