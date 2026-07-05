# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

READ-ONLY AUDIT. Do NOT write, edit, or create any files anywhere. Return all findings as your final message text only.

cwd: /Users/rom.iluz/Dev/cc10x

SCOPE: Architecture, Frontend, MCP-CLI, Research, agent-common skills + the researcher agent.
Files to read in full:
- plugins/cc10x/skills/architecture/SKILL.md
- plugins/cc10x/skills/frontend/SKILL.md + references/accessibility-and-forms.md, design-md-authoring.md, design-md-inspiration-index.md, performance-and-layout.md, ui-state-and-feedback.md
- plugins/cc10x/skills/mcp-cli/SKILL.md
- plugins/cc10x/skills/research/SKILL.md
- plugins/cc10x/skills/agent-common/SKILL.md
- plugins/cc10x/agents/researcher.md

BASELINE COMPARISON: `git show v11.1.0:<path>` / `git diff v11.1.0..HEAD -- <path>` against:
- plugins/cc10x/skills/architecture-patterns/SKILL.md
- plugins/cc10x/skills/frontend-patterns/SKILL.md + plugins/cc10x/skills/frontend-design-critique/SKILL.md (both merged into frontend/SKILL.md — v11 combined length vs current 157 lines is a huge cut, verify what survived)
- plugins/cc10x/skills/mcp-cli/SKILL.md (v11)
- plugins/cc10x/skills/research/SKILL.md (v11 — small diff per stat, should be near-identical, confirm)
- plugins/cc10x/skills/authoring-cc10x-guidance/SKILL.md (does this exist in v11? if it was dropped entirely, was ANYTHING load-bearing in it, or was it pure meta-documentation about how to write cc10x skills? check if any of it should have migrated somewhere)
- plugins/cc10x/skills/skill-eval-harness/SKILL.md + evals/* (dropped entirely — check tools/*.py in current repo, e.g. worldclass_benchmark.py, harness_audit.py, workflow_replay_check.py — do any of them depend on skill-eval-harness concepts/files that no longer exist? is this a dangling reference?)
- plugins/cc10x/agents/github-researcher.md + plugins/cc10x/agents/web-researcher.md (merged into researcher.md — verify both source types of research capability actually survived in the merged agent, not just one)

OUTPUT FORMAT: For each area (architecture, frontend, mcp-cli, research, agent-common, researcher-agent-merge), state INTACT / WEAKENED / LOST / IMPROVED with file:line evidence, paying special attention to the frontend merge (biggest cut %) and the skill-eval-harness removal (check for dangling tool dependencies). List all issues found, severity-tagged CRITICAL/HIGH/MEDIUM/LOW with file:line citations. End with a one-paragraph verdict on whether this area is publish-ready.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

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