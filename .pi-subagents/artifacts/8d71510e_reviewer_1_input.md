# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

BRUTAL REVIEW of keynote.html — visual harmony and slide structure.

Read the ENTIRE keynote at /Users/rom.iluz/Dev/cc10x/keynote.html.

Check for visual/structural problems:

1. Do all 21 slides have the same CSS classes available? Check that new slides (2c, 9b, 10a-10d) use the same class names as existing slides (card, card-grid, chain, chain-node, etc.).

2. Are the new workflow slides (10a-10d) visually consistent with each other? Same layout structure (chain at top, 3 cards below)?

3. Does the slide counter in the JavaScript at the bottom correctly count 21 slides? The script uses `document.querySelectorAll('.slide')` — will it pick up all 21?

4. Check for any broken HTML — unclosed divs, mismatched tags, missing closing <!-- --> comment markers.

5. Do the new slides have data-section attributes? (The section label in the UI reads from this.) What sections do the workflow slides (10a-10d) belong to?

6. Is the 'chain' layout in the workflow slides going to overflow on a 1920x1080 projector? Count the nodes in each chain — are there too many to fit?

7. Check the color coding: are agent colors in the slides consistent with the actual agent frontmatter colors? (planner=cyan, bug-investigator=red, component-builder=green, code-reviewer=blue, failure-hunter=red, integration-verifier=yellow, doc-syncer=cyan, plan-gap-reviewer=purple, researcher=orange)

8. Are there any slides that are too text-heavy (would be unreadable from the back of a 10,000-person hall)? Flag any slide with more than ~150 words of body text.

For each check, output PASS or FAIL with evidence. Do NOT edit any files. Read only.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/8d71510e/keynote-review-02-visual-harmony.md
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