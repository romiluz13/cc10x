# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

READ-ONLY AUDIT. Do NOT write, edit, or create any files anywhere. Return all findings as your final message text only.

cwd: /Users/rom.iluz/Dev/cc10x

SCOPE: Review + Verification workflows — the trust/quality core of cc10x.
Files to read in full:
- plugins/cc10x/skills/code-review/SKILL.md + references/code-review-heuristics.md, review-order-and-checkpoints.md, security-review-checklist.md
- plugins/cc10x/skills/verification/SKILL.md + references/live-production-testing.md + evals/*.md
- plugins/cc10x/agents/code-reviewer.md
- plugins/cc10x/agents/failure-hunter.md
- plugins/cc10x/agents/integration-verifier.md
- plugins/cc10x/agents/plan-gap-reviewer.md

BASELINE COMPARISON: `git show v11.1.0:<path>` / `git diff v11.1.0..HEAD -- <path>` against:
- plugins/cc10x/skills/code-review-patterns/SKILL.md
- plugins/cc10x/skills/receiving-code-review/SKILL.md
- plugins/cc10x/skills/verification-before-completion/SKILL.md + references/live-production-testing.md (420 lines -> merged/cut heavily, verify what happened)
- plugins/cc10x/agents/code-reviewer.md (v11)
- plugins/cc10x/agents/silent-failure-hunter.md (renamed to failure-hunter.md — verify the rename preserved ALL logic, check every reference to the old name 'silent-failure-hunter'/'Silent Failure Hunter' elsewhere in the repo was actually updated, not just some)
- plugins/cc10x/agents/integration-verifier.md (v11)
- plugins/cc10x/agents/plan-gap-reviewer.md (v11)

VERIFY THESE SPECIFIC CLAIMED INNOVATIONS survive functionally (this is the highest-stakes area — this is what makes cc10x trustworthy vs a normal agent):
20. Anti-anchoring plan review — plan-gap-reviewer gets FRESH context, explicitly does NOT load .cc10x/*.md, no inherited bias from the planner's own reasoning
21. Two Isolated Assessments — reviewer + hunter run in PARALLEL (not sequential), WEAVE protocol combines independent findings without one anchoring the other
22. Code-reviewer Pass 5 (Plan Validity) — catches 'built the wrong thing well'
23. Code-reviewer Pass 6 (Spec Compliance) — reviews against original spec, not just code quality
24. Test Honesty Gates — false-green detection: mock assertions, schema-incomplete mocks, DB-bypass, test-tampering, condition-based-waiting. This is described as UNIQUE to cc10x — verify the actual detection logic/prompting for each of these 5 sub-patterns still exists with real teeth (not just named in a heading).

Also check plugins/cc10x/agents/references/silent-failure-red-flags.md — is this reference still wired/referenced correctly from failure-hunter.md, or orphaned/stale-named?

OUTPUT FORMAT: For each of the 5 items, state INTACT / WEAKENED / LOST / IMPROVED with file:line evidence. List all issues found, severity-tagged CRITICAL/HIGH/MEDIUM/LOW with file:line citations. This is the most important area of the audit — be maximally skeptical and adversarial. End with a one-paragraph verdict on whether Review+Verification is publish-ready.

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