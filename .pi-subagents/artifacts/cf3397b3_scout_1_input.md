# Task for scout

DEEP COMPARISON: Memory, Context & Handoff Systems

Read EVERY file in:
- cc10x: /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/memory-and-handoff/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/agent-common/SKILL.md, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/scripts/cc10x_state_persist.py, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/scripts/cc10x_postcompact_context.py, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/scripts/cc10x_stop_persist.py, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/scripts/cc10x_sessionstart_context.py, /Users/rom.iluz/Dev/cc10x/plugins/cc10x/hooks/hooks.json
- Superpowers: /Users/rom.iluz/Dev/superpowers/hooks/ (ALL files), /Users/rom.iluz/Dev/superpowers/skills/finishing-a-development-branch/SKILL.md
- Matt Pocock: /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/productivity/handoff/SKILL.md, /Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/skills/in-progress/claude-handoff/SKILL.md

Analyze:
1. How does each project manage memory across sessions?
2. How does each project handle context compaction/recovery?
3. What handoff patterns does each project use? (between agents, between sessions)
4. How does each project persist state? (files, hooks, artifacts)
5. What memory patterns does cc10x have that the others DON'T?
6. What memory patterns do the others have that cc10x SHOULD adopt?
7. Rate each project's memory/handoff system 1-10.

Output a structured comparison + verdict.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/cf3397b3/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/cf3397b3/comparison-07-memory-handoff.md
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