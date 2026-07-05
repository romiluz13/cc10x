# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

BRUTAL REVIEW of keynote.html — content consistency check.

Read the ENTIRE keynote at /Users/rom.iluz/Dev/cc10x/keynote.html (21 slides, ~2000 lines).

Cross-check EVERY factual claim against the ACTUAL cc10x codebase:

1. Slide 4 shows a chain with 'code-reviewer' and 'failure-hunter' as parallel agents. Verify: does the actual router (plugins/cc10x/skills/cc10x-router/SKILL.md) dispatch these two in parallel? Check §12 step 5 and the routing table.

2. Slide 10a (BUILD workflow) claims specific skills are loaded by each agent. Verify by reading the actual agent frontmatter in plugins/cc10x/agents/*.md — do the skills: lists match what the slide claims?

3. Slide 10a claims 'max 3 cycles' for the remediation loop. Verify this is what the router actually says in plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md.

4. Slide 10b (PLAN workflow) claims the plan-gap-reviewer loads ZERO skills and ZERO memory. Verify by reading plugins/cc10x/agents/plan-gap-reviewer.md frontmatter — does it have a skills: field?

5. Slide 10b claims 'max 2 review passes' for the plan review loop. Verify in plugins/cc10x/skills/cc10x-router/references/plan-workflow.md.

6. Slide 10c (DEBUG workflow) claims '10-rung feedback loop' and '3-5 ranked hypotheses'. Verify in plugins/cc10x/agents/bug-investigator.md and plugins/cc10x/skills/debugging/SKILL.md.

7. Slide 10d (REVIEW) claims '6 passes' and 'confidence ≥80'. Verify in plugins/cc10x/agents/code-reviewer.md.

8. Slide 11 says '9 agents · 17 skills · 4 workflows'. Verify: count actual agent files in plugins/cc10x/agents/*.md, count actual skill directories in plugins/cc10x/skills/, and count workflows (BUILD, DEBUG, REVIEW, PLAN — is ORIENT a 5th workflow or just a routing mode?).

9. Slide 14 says '9' for agents. Verify consistency with slide 11.

10. Check for ANY stale references to 'Pass 1b', 'silent-failure-hunter' (old name), '8 agents', or any other pre-v12.4.0 content that shouldn't be there.

For each check, output PASS or FAIL with exact evidence (file:line from the codebase vs. what the slide says). Do NOT edit any files. Read only.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/8d71510e/keynote-review-01-content-consistency.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

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