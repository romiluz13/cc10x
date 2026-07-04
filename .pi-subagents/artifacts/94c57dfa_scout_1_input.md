# Task for scout

DEEP COMPARISON: Skill Design & Format Methodology

Read EVERY skill file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/ (ALL 17 skills, every SKILL.md)
- Superpowers: /Users/rom.iluz/Dev/superpowers/skills/writing-skills/ (ALL files including examples/), /Users/rom.iluz/Dev/superpowers/skills/using-superpowers/SKILL.md
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/productivity/writing-great-skills/ (ALL files), /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/productivity/teach/ (ALL files)

Also read 3 representative skills from each project to compare format:
- cc10x: verification/SKILL.md, planning/SKILL.md, debugging/SKILL.md
- Superpowers: test-driven-development/SKILL.md, systematic-debugging/SKILL.md, verification-before-completion/SKILL.md
- Matt Pocock: engineering/tdd/SKILL.md, engineering/diagnosing-bugs/SKILL.md, engineering/implement/SKILL.md

Analyze:
1. Skill frontmatter format comparison (what fields each uses)
2. Skill body structure (sections, formatting, length)
3. How each project teaches skill writing (writing-great-skills vs writing-skills vs implicit)
4. Leading words / activation patterns — how does each project make skills discoverable?
5. Reference files — how does each project use supporting docs within skills?
6. What skill design patterns does cc10x have that the others DON'T?
7. What skill design patterns do the others have that cc10x SHOULD adopt?
8. Which project's skills are most effective at steering agent behavior? Rate 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/94c57dfa/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/94c57dfa/comparison-02-skills-format.md
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