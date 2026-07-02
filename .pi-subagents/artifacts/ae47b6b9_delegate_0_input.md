# Task for delegate

DEEP ANALYSIS — SKILLS LAYER (all SKILL.md + references)

You are analyzing the cc10x Claude Code plugin's skills layer. These are FUNCTIONAL instruction files that get loaded into Claude's context — they ARE the system, not documentation. Read every SKILL.md fully. For references/ subdirectories, read them too as they are functional reference material loaded on demand.

IGNORE: any file under docs/, README.md, CHANGELOG.md, CLAUDE.md, or evals/ directories (evals are test-only). Focus on SKILL.md files and references/ files ONLY.

Skills to analyze (read ALL SKILL.md files fully):
1. plugins/cc10x/skills/cc10x-router/SKILL.md — THIS IS THE ORCHESTRATION BRAIN, read it most carefully and most completely
2. plugins/cc10x/skills/planning-patterns/SKILL.md
3. plugins/cc10x/skills/code-generation/SKILL.md
4. plugins/cc10x/skills/debugging-patterns/SKILL.md
5. plugins/cc10x/skills/code-review-patterns/SKILL.md
6. plugins/cc10x/skills/verification-before-completion/SKILL.md
7. plugins/cc10x/skills/test-driven-development/SKILL.md
8. plugins/cc10x/skills/architecture-patterns/SKILL.md
9. plugins/cc10x/skills/brainstorming/SKILL.md
10. plugins/cc10x/skills/session-memory/SKILL.md
11. plugins/cc10x/skills/handoff-package/SKILL.md
12. plugins/cc10x/skills/plan-review-gate/SKILL.md
13. plugins/cc10x/skills/research/SKILL.md
14. plugins/cc10x/skills/receiving-code-review/SKILL.md
15. plugins/cc10x/skills/codebase-deepening/SKILL.md
16. plugins/cc10x/skills/finding-duplicate-functions/SKILL.md
17. plugins/cc10x/skills/frontend-patterns/SKILL.md
18. plugins/cc10x/skills/frontend-design-critique/SKILL.md
19. plugins/cc10x/skills/diff-driven-docs/SKILL.md
20. plugins/cc10x/skills/prototyping/SKILL.md
21. plugins/cc10x/skills/mcp-cli/SKILL.md
22. plugins/cc10x/skills/update/SKILL.md
23. plugins/cc10x/skills/authoring-cc10x-guidance/SKILL.md
24. plugins/cc10x/skills/skill-eval-harness/SKILL.md

Also read key references (ALL of these):
- plugins/cc10x/skills/cc10x-router/references/build-workflow.md
- plugins/cc10x/skills/cc10x-router/references/debug-workflow.md
- plugins/cc10x/skills/cc10x-router/references/plan-workflow.md
- plugins/cc10x/skills/cc10x-router/references/review-workflow.md
- plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md
- plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md
- plugins/cc10x/skills/cc10x-router/references/workflow-artifact.skeleton.json
- plugins/cc10x/skills/debugging-patterns/references/investigation-hygiene.md
- plugins/cc10x/skills/debugging-patterns/references/root-cause-playbooks.md
- plugins/cc10x/skills/code-review-patterns/references/code-review-heuristics.md
- plugins/cc10x/skills/code-review-patterns/references/review-order-and-checkpoints.md
- plugins/cc10x/skills/code-review-patterns/references/security-review-checklist.md
- plugins/cc10x/skills/planning-patterns/references/live-verification-strategy.md
- plugins/cc10x/skills/test-driven-development/references/integration-and-live-proof.md
- plugins/cc10x/skills/test-driven-development/references/test-data-and-mocks.md
- plugins/cc10x/skills/test-driven-development/references/testing-patterns.md
- plugins/cc10x/skills/session-memory/references/context-budget-and-checkpointing.md
- plugins/cc10x/skills/session-memory/references/memory-file-contracts.md
- plugins/cc10x/skills/session-memory/references/memory-model-and-ownership.md
- plugins/cc10x/skills/session-memory/references/memory-operations.md
- plugins/cc10x/skills/verification-before-completion/references/live-production-testing.md
- plugins/cc10x/skills/frontend-patterns/references/accessibility-and-forms.md
- plugins/cc10x/skills/frontend-patterns/references/design-md-authoring.md
- plugins/cc10x/skills/frontend-patterns/references/design-md-inspiration-index.md
- plugins/cc10x/skills/frontend-patterns/references/performance-and-layout.md
- plugins/cc10x/skills/frontend-patterns/references/ui-state-and-feedback.md

For EACH skill, report:
1. Name + trigger conditions (when does Claude load/activate this skill?)
2. What behavior it enforces or guides
3. What workflow phases it participates in (plan/build/debug/review)
4. Does it produce artifacts? What and where?
5. Does it interact with hooks or scripts? How?
6. Token/context cost — how verbose is it? Could it be 50% shorter without losing function?
7. Overlap with other skills — is there redundancy?
8. Is it still relevant for modern Claude (Sonnet 4.5/Opus 4.1 era) or is it over-prompting a model that doesn't need it?

For cc10x-router specifically (THE BRAIN):
- Map the complete routing logic: how does it decide which workflow (plan/build/debug/review)?
- What is the workflow artifact system? How are artifacts created, updated, validated?
- What are the phase transitions and gates?
- How does it coordinate with hooks and agents?
- What is the "router-kernel" concept?

Return a structured report with: (A) per-skill analysis, (B) router deep-dive, (C) skill dependency/interaction graph, (D) workflow artifact schema, (E) redundancy/overlap map, (F) token-cost bloat assessment, (G) modernization opportunities (what to cut/merge/simplify for current models).

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/ae47b6b9/file-only
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