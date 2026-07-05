# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

BRUTAL REVIEW — comprehensive stale-reference sweep across the ENTIRE cc10x codebase.

The cc10x project has gone through MANY refactoring rounds (v11→v12.1→v12.2→v12.3→v12.4). Each round renamed things. We keep finding stale references. This is a FINAL comprehensive sweep.

Search ALL files in plugins/cc10x/ (every .md, .json, .py file) for references to ANY of these OLD names:

OLD SKILL NAMES (all renamed in v12.1.0):
- verification-before-completion (now: verification)
- planning-patterns (now: planning)
- debugging-patterns (now: debugging)
- architecture-patterns (now: architecture)
- frontend-patterns (now: frontend)
- code-review-patterns (now: code-review)
- session-memory (now: memory-and-handoff)

OLD AGENT NAMES:
- silent-failure-hunter (now: failure-hunter) — check ALL files except references/silent-failure-red-flags.md (that's about the pattern, not the agent)
- web-researcher (merged into researcher)
- github-researcher (merged into researcher)

OLD CONCEPTS:
- Pass 1b (removed — failure-hunter is now a separate parallel agent)
- LEGACY (should no longer appear next to 'hunter' in artifact policy)
- RESIDUAL_FINDINGS (removed — replaced by pointer to deferred_findings)
- residual-review-findings (removed)

For EACH match found, report:
- File path and line number
- The exact stale text
- What it should be (or if it should be deleted)
- Whether it's in executing code (agent prompt, skill text, hook script, router) vs. historical documentation (CHANGELOG entries are OK to keep)

Also check: does the keynote.html contain ANY stale references?

Do NOT edit any files. Read only.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/8d71510e/keynote-review-04-codebase-stale-refs.md
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