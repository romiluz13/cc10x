# Task for scout

DEEP ANALYSIS: addyosmani/agent-skills — Agents, hooks, commands, and infrastructure.

Read EVERY file in:
- /Users/rom.iluz/Dev/addyosmani-agent-skills/agents/ (ALL 4 agent files: code-reviewer.md, security-auditor.md, test-engineer.md, web-performance-auditor.md)
- /Users/rom.iluz/Dev/addyosmani-agent-skills/hooks/ (ALL files: hooks.json, SDD-CACHE.md, SIMPLIFY-IGNORE.md, sdd-cache-post.sh, sdd-cache-pre.sh, session-start.sh, simplify-ignore.sh, simplify-ignore-test.sh, session-start-test.sh)
- /Users/rom.iluz/Dev/addyosmani-agent-skills/commands/ (ALL 8 .toml files)
- /Users/rom.iluz/Dev/addyosmani-agent-skills/plugin.json
- /Users/rom.iluz/Dev/addyosmani-agent-skills/AGENTS.md
- /Users/rom.iluz/Dev/addyosmani-agent-skills/CONTRIBUTING.md

Compare against cc10x's agents (9 agents at /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/), hooks (9 scripts at /Users/rom.iluz/Dev/cc10x/plugins/cc10x/scripts/), and hooks.json.

Analyze:
1. How does each agent compare to cc10x's agents? What's different?
2. What unique agent patterns does addyosmani have?
3. What hook patterns does addyosmani have? How do they compare to cc10x's 9 hooks?
4. What are the .toml commands? How do they work? Does cc10x have an equivalent?
5. What is SDD-CACHE and SIMPLIFY-IGNORE? What do these hooks do?
6. What can cc10x steal from the agents, hooks, or commands?

Output a structured report of unique patterns cc10x should adopt.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/99888eba/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/99888eba/comparison-12-addyosmani-agents-hooks.md
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