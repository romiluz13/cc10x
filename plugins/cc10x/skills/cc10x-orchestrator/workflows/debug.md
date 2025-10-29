# DEBUG Workflow - Root Cause First

**Triggered by:** User requests help investigating bugs, errors, or unexpected behaviour.

## Phase 0 - Intake
1. Gather reproduction steps, error messages, logs, and recent changes.
2. Confirm scope (single bug per run unless explicitly broadened).
3. If scope spans multiple independent failures, queue them and tackle serially unless the user approves separate runs.
4. If resuming after compaction or context is unclear, read the latest snapshot and working plan:
   - Read `.claude/memory/snapshots/` most recent `snapshot-*.md`
   - Read `.claude/memory/WORKING_PLAN.md`

## Phase 1 - Shared Skills
Load the following skills:
- `systematic-debugging`
- `log-analysis-patterns`
- `root-cause-analysis`
- `test-driven-development`
- `verification-before-completion`

## Phase 2 - Bug Investigation Loop
For each identified bug:
1. Invoke `bug-investigator` with all context. Require:
   - Reproduction of the failure.
   - Collection of relevant logs/metrics (LOG FIRST).
   - Written hypothesis before implementing fixes.
   - Failing regression test proving the bug.
2. Once the fix is proposed, re-run the regression test to verify GREEN and document commands run.
3. Send the changes to `code-reviewer` for validation (quality, security, performance).
4. Use `integration-verifier` to confirm there are no regressions in the broader flow.

File size sanity check: As fixes accumulate, if any modified file exceeds ~500 lines, propose a focused refactor/split plan (after green tests).

Invocation pattern (per bug):
- Read the subagent's SKILL.md to load its process and output format.
- Provide the repro steps, logs, and scope.
- Require the specified outputs with file:line evidence and command outputs.
- On failure or missing repro, stop and request direction.

## Phase 3 - Consolidation
- Summarise root cause, fix, and verification evidence for each bug.
- List any follow-up work (monitoring, additional tests) recommended by the skills used.

## Phase 4 - Verification Summary
Document:
```
# Verification Summary
Bugs fixed: <list>
Commands: <tests/log scripts run with exit codes>
Residual risk: <items to monitor>
```

Example:
Commands:
- npm test test/cart.spec.ts -> exit 1 (RED)
- Apply null check in src/cart.ts:85
- npm test test/cart.spec.ts -> exit 0 (GREEN)
Residual risk: add e2e test for empty cart state

## Phase 5 - Report
- Provide a detailed breakdown per bug (root cause, fix, verification evidence).
- Highlight any remaining issues or uncertainties.
- Offer optional next steps (e.g., "Want a code review of the patch?") without assuming consent.

## Failure Handling
- If a reproduction cannot be established, pause and request more information.
- If a fix fails review/integration, report the blocker and wait for direction.
- Never mark bugs as fixed without captured test or log evidence.

## References
- Debugging discipline: `plugins/cc10x/skills/systematic-debugging/SKILL.md`
- Official guidance: `docs/reference/03-SUBAGENTS.md`, `docs/reference/04-SKILLS.md`
