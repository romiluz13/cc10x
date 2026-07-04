# Task for scout

VERIFICATION: Orphaned Skills Check — Are ALL skills used by the system?

Read ALL 17 skill SKILL.md files in /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/:
agent-common, architecture, building, cc10x-router, code-review, codebase-hygiene, debugging, diff-driven-docs, exploration, frontend, mcp-cli, memory-and-handoff, plan-review-gate, planning, research, update, verification

For EACH skill, verify:
1. Is it referenced by at least one agent's `skills:` frontmatter? Check ALL 9 agent files in /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/
2. Is it referenced by the router's SKILL_HINTS or dispatcher?
3. Is it referenced by another skill?
4. Does it have `user-invocable: false` (internal only) or is it user-facing?
5. If it's internal, is it actually loaded by the router or an agent?

Mark each skill as:
- ACTIVE (loaded by at least one agent or the router)
- ORPHANED (not referenced by any agent or the router)
- USER-FACING (user-invocable, doesn't need agent loading)

For any orphaned skills, explain what they do and whether they should be loaded somewhere.

Output a table with all 17 skills and their status.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/934beb1e/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/934beb1e/verify-02-orphaned-skills.md
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