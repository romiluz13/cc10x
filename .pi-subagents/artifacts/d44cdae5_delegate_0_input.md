# Task for delegate

DEEP ANALYSIS — SUB-AGENTS LAYER (all agent definitions)

You are analyzing the cc10x Claude Code plugin's sub-agent definitions. These are FUNCTIONAL — they define agent personas, system prompts, and behavioral contracts that Claude Code loads when spawning sub-agents. Read every file FULLY.

IGNORE: all docs, README, audit explanations. Focus ONLY on the agent .md files.

Agents to analyze (read ALL fully):
1. plugins/cc10x/agents/planner.md
2. plugins/cc10x/agents/component-builder.md
3. plugins/cc10x/agents/bug-investigator.md
4. plugins/cc10x/agents/code-reviewer.md
5. plugins/cc10x/agents/integration-verifier.md
6. plugins/cc10x/agents/plan-gap-reviewer.md
7. plugins/cc10x/agents/silent-failure-hunter.md
8. plugins/cc10x/agents/doc-syncer.md
9. plugins/cc10x/agents/github-researcher.md
10. plugins/cc10x/agents/web-researcher.md

For EACH agent, report:
1. Agent name + role
2. Full system prompt content summary — what persona, constraints, rules does it enforce?
3. What model is it configured for? Any model-specific tuning?
4. What tools/permissions does it have or claim to need?
5. What does it produce? (artifacts, reports, code, analysis)
6. How is it invoked? (by the router skill? by other skills? manually?)
7. What workflow phase does it participate in?
8. Does it read/write workflow artifacts? How?
9. Contract: what does it guarantee to return? What does it refuse to do?
10. Overlap with other agents — is there redundancy?
11. Is the prompt over-engineered for modern models? Could it be 70% shorter?
12. Does it reference hooks, scripts, or other skills? How?

Also map:
- The agent interaction graph: which agents feed into which? (e.g., planner → component-builder → code-reviewer)
- Which agents are essential vs which could be merged or eliminated
- Whether the agent prompts contain ceremony/boilerplate that modern Claude doesn't need

Return a structured report with: (A) per-agent deep analysis, (B) agent interaction/delegation graph, (C) essential-vs-redundant classification, (D) prompt bloat assessment with specific examples, (E) modernization recommendations (merge/cut/simplify).

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/d44cdae5/file-only
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