# Task for scout

VERIFICATION: New Patterns Integration — Are the 18 newly adopted patterns actually referenced and used by the system?

Read these files and verify each new pattern is properly integrated:

1. agent-common/SKILL.md — verify Spirit-vs-Letter and Untrusted Input Handling sections exist and are well-formed
2. building/SKILL.md — verify Rationalization Table, Red Flags, Safety-Check Guard, Tautological Test Anti-Pattern sections exist
3. building/references/test-data-and-mocks.md — verify SDK-Style Interfaces section exists
4. debugging/SKILL.md — verify Rationalization Table, Red Flags, Repro Minimisation, Causal Chain Gate sections exist
5. debugging/evals/ — verify 3 pressure test files exist and are well-formed
6. verification/SKILL.md — verify Rationalization Table and Red Flags sections exist
7. architecture/SKILL.md — verify Deep-Module Vocabulary, Deletion Test, Two-Adapter Rule sections exist
8. code-review/SKILL.md — verify Fowler Code Smells, AI-Generated Anti-Patterns, Metric Honesty, Residual Review Findings sections exist
9. exploration/SKILL.md — verify Doubt-Driven Development section exists
10. memory-and-handoff/SKILL.md — verify Knowledge Compounding Loop section exists
11. bug-investigator.md — verify Causal Chain Gate, Repro Minimisation, Assumption Audit, Ranked Hypotheses steps exist
12. scripts/cc10x_git_guard.py — verify git restore . pattern is blocked

For each, output PASS/FAIL with the exact section heading found.

Also verify: Does the router reference any of these new patterns? Or are they completely invisible to the router (only loaded when agents load skills)?

Finally: Check if the 3 pressure test eval files are properly structured (Setup, Expected Behavior, Failure Signature, Rationalization Counter).

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/fcf3b73a/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/fcf3b73a/verify-05-new-patterns-integration.md
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