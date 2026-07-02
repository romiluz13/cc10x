# Task for delegate

DEEP ANALYSIS — BENCHMARK/AUDIT/REPLAY ENGINE (large scripts)

You are analyzing the cc10x Claude Code plugin's heavy engine scripts. IGNORE all documentation, README files, audit-explanation MDs. Focus ONLY on functional code.

Read and deeply analyze these files (read every single one FULLY — they are large):

- plugins/cc10x/scripts/cc10x_worldclass_benchmark.py (1389 lines — the biggest script)
- plugins/cc10x/scripts/cc10x_workflow_replay_check.py (1025 lines)
- plugins/cc10x/scripts/cc10x_harness_audit.py (907 lines)
- plugins/cc10x/scripts/cc10x_reference_benchmark.py (338 lines)
- plugins/cc10x/scripts/cc10x_live_harness_runner.py (302 lines)

For EACH script, report:
1. What it does mechanically — entry point, CLI args, main flow
2. What it measures/validates/audits — the actual checks and thresholds
3. Data sources: what files/dirs it reads (workflow artifacts, .cc10x/, docs/benchmarks/, fixtures)
4. Data outputs: what it writes and where
5. The data model — what JSON structures/schemas it uses (workflow artifacts, benchmark results, audit reports)
6. Dependencies: imports, external tools, hooklib usage, other scripts
7. How it's invoked — is it called by hooks? By skills? Manually? By tests?
8. Complexity analysis: what % of the code is actually doing useful work vs boilerplate/ceremony
9. Is this script ever actually run in a live Claude Code session, or is it offline-only tooling?
10. Bloat assessment: what could be cut, simplified, or replaced by modern Claude Code native features

Also analyze the test fixtures to understand the data model:
- plugins/cc10x/tests/fixtures/ (read 3-4 representative fixture JSON files like build-happy-path.json, plan-full.json, debug-research.json)
- plugins/cc10x/tests/live/manifests/cc10x-bootstrap.json

Return a structured report with: (A) per-script deep analysis, (B) shared data model/schema, (C) invocation graph (who calls what), (D) live-vs-offline classification, (E) bloat/ceremony findings with specific line ranges, (F) what modern Claude Code could replace.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/ba839dff/file-only
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