# Task for scout

VERIFICATION: System Prompt Consistency — Is every system prompt from our installation stolen exactly where it should be?

Read ALL 9 agent files in /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/:
planner.md, bug-investigator.md, component-builder.md, code-reviewer.md, silent-failure-hunter.md, integration-verifier.md, doc-syncer.md, plan-gap-reviewer.md, researcher.md

Also read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/agent-common/SKILL.md (the shared preamble)

For EACH agent, verify:
1. Does it load `cc10x:agent-common` in its `skills:` frontmatter? (ALL agents should)
2. Does it have the correct `effort` field?
3. Does it have the correct `color` field? (planner=cyan, bug-investigator=red, component-builder=green, code-reviewer=blue, silent-failure-hunter=red, integration-verifier=yellow, doc-syncer=cyan, plan-gap-reviewer=purple, researcher=orange)
4. Does it have the correct `tools` list? (READ-ONLY agents should NOT have Edit/Write)
5. Does it have the CONTRACT envelope format?
6. Does it have the SINGLE FINAL RESPONSE RULE?
7. Does it have the Memory First protocol (or the anti-anchoring variant for reviewers)?
8. Does it reference the correct skills in its `skills:` list?
9. Are there any broken references to files that don't exist?
10. Does it have the Memory Notes format?

Also check: Are there any references to Pass 1b that should have been removed? Are there any references to the hunter as LEGACY? Are there any stale references to old skill names?

Output PASS/FAIL for each agent with evidence.

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/934beb1e/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/934beb1e/verify-04-system-prompt-consistency.md
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