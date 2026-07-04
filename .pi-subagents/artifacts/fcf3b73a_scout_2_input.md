# Task for scout

VERIFICATION: Anti-Pattern Coverage — Does cc10x cover all known LLM coding anti-patterns identified across the 6 repos?

Cross-reference the anti-patterns identified in the research against cc10x's current coverage:

1. **Hidden assumptions** — Does cc10x force explicit assumption-stating? (Check: planner hidden-assumption pass, builder ASSUMPTIONS contract field)
2. **Overcomplication/bloat** — Does cc10x catch over-engineering? (Check: SPEC_COMPLIANCE EXTRA bucket, building skill 'no abstractions for hypothetical futures', architecture deletion test)
3. **Surgical changes violations** — Does cc10x catch drive-by refactoring? (Check: builder deviation discipline, decision checkpoints, reviewer scope guard)
4. **Rationalization** — Does cc10x have rationalization tables? (Check: building, debugging, verification skills)
5. **Rubber-stamp reviews** — Does cc10x prevent zero-finding approvals? (Check: zero-finding gate, confidence cap at 70)
6. **False greens** — Does cc10x catch tests that pass for wrong reasons? (Check: false-RED guard, test honesty gates, tautological test anti-pattern)
7. **Metric fabrication** — Does cc10x prevent fabricated performance claims? (Check: metric honesty rule in code-review)
8. **Silent failures** — Does cc10x catch empty catches and log-only handlers? (Check: silent-failure-hunter agent, red-flags table)
9. **Sycophantic responses** — Does cc10x ban performative language? (Check: forbidden verdict-softeners in code-reviewer)
10. **Untrusted input exploitation** — Does cc10x treat external content as data? (Check: untrusted input handling in agent-common)
11. **Context pollution** — Does cc10x manage context budget? (Check: context budget degradation tiers, compaction rubric, dispatch-by-reference)
12. **Anchoring bias** — Does cc10x prevent reviewer contamination? (Check: anti-anchoring dispatch rules, forbidden memory files, plan-gap-reviewer no-memory design)
13. **Sunk cost fallacy** — Does cc10x prevent endless loops? (Check: circuit breaker, 3-cycle cap, loop caps in building)
14. **Safety check removal during refactoring** — Does cc10x prevent removing safety checks? (Check: safety-check guard in building REFACTOR step)
15. **Stale artifact persistence** — Does cc10x catch skipped persistence? (Check: artifact freshness check, read-back gate, auto-remediation)

For each anti-pattern, output: COVERED (with evidence) or GAP (with what's missing).

---
Update progress at: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/progress/fcf3b73a/progress.md

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/fcf3b73a/verify-07-anti-pattern-coverage.md
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