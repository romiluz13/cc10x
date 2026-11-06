# Blocking Severity

Only CRITICAL and HIGH findings, plus the non-severity gates that already
blocked, stop a BUILD phase. One REM-FIX takes the whole blocking set with
`scope:ALL_ISSUES`, and the router asks no scope question. MEDIUM and LOW
findings in BUILD go to `deferred_findings` and are surfaced at BUILD-DONE
triage step 1a, where the user decides.

## Context

An older router asked `Fix critical only` or `Fix all issues` whenever a
BUILD review raised CRITICAL and HIGH together (rule `1a-SCOPE`), asked again
when the reviewer approved but the hunter reported HIGH (rule 2), and
auto-created a REM-FIX for every non-blocking item (rule 1b). Each answer cost a
round trip, a critical-only fix left the HIGH issues for another cycle, and
MEDIUM findings either blocked a phase through rule 1b or slipped into Memory
Notes `**Deferred:**` and were never fixed. The failure-hunter's findings
carried no per-finding severity, so the router could not tell a MEDIUM from a
coverage note. Once every agent writes MEDIUM and LOW under `### Findings`,
DEBUG's old rule 1b (auto-fix every non-blocking item) would reopen a fix cycle
for a single LOW nit.

## Decision

- **Blocking set (D1).** Every validated CRITICAL and HIGH finding from
  `code-reviewer` and `failure-hunter`, the `integration-verifier`'s
  `### Critical Issues` (after post-verifier finding validation), plus a
  non-PASS `SPEC_COMPLIANCE`, an unresolved `CANNOT_VERIFY_CROSS_PHASE`, a
  verifier `FAIL` and a missing or false TDD RED/GREEN. CRITICAL comes from
  `### Critical Issues`, `Severity: CRITICAL` entries and a non-zero YAML
  `CRITICAL_ISSUES`; HIGH from the
  reviewer's `### Findings` entries with `Severity: HIGH` and from the hunter's
  `HIGH_ISSUES` field and `Severity: HIGH` entries. The verifier rates no
  severity; its `### Findings` are observations. Notes (the hunter's
  `### Coverage`) are not findings. An entry under `### Findings` with a missing
  or unknown severity blocks (fail closed).
- **One wave (D2).** A BUILD REM-FIX always takes the whole blocking set with
  `scope:ALL_ISSUES`. `CRITICAL_ONLY` stays in the `scope:` enum and in
  `REMEDIATION_SCOPE_REQUESTED` only so older tasks still parse; a legacy
  `[SCOPE-DECISION-PENDING]` marker, or a leftover `pending_gate` of
  `scope_decision`, resumes as an `ALL_ISSUES` REM-FIX, or re-runs that
  phase's reviewer and hunter when the artifact stores counts only.
- **Envelope unchanged (D3).** The line-1 envelope `b`/`cr` keep counting
  CRITICAL only; the router computes the blocking set from severities, never
  from `b` or `REMEDIATION_NEEDED`.
- **Deferred entries (D4).** `deferred_findings` entries are
  `{source, phase_id, finding, severity}` with `severity` one of `medium`, `low`
  or `minor`. BUILD writes `medium` or `low`; DEBUG writes `low`; `minor` stays valid for QA and
  older artifacts.
- **DEBUG (D4).** In DEBUG, MEDIUM auto-creates a REM-FIX and LOW is listed under the `[DEBUG-RESET]` summary and in the completion message with no REM-FIX, so a single LOW nit no longer reopens a fix cycle. REVIEW keeps its ask.

## Rejected alternatives

- **Keep the scope question.** Rejected: it paused every mixed review for a
  user answer, and a critical-only answer only moved the HIGH issues to the next
  cycle.
- **Block on every severity.** Rejected: MEDIUM and LOW findings would each cost
  a full remediation cycle inside the phase, the loop the change set out to
  tighten.
- **Defer MEDIUM and LOW without a wave.** Accepted for now: a MEDIUM is fixed
  only if the user picks "fix now" at BUILD-DONE triage. A deferred fix wave is
  a later round.
- **Count HIGH in the envelope.** Rejected: `b`/`cr` are a fast-path signal many
  checks already read as CRITICAL-only; changing them would ripple through every
  agent contract for no gain over reading severities.

## Consequences

- Rules `1a-SCOPE` and the §4 scope prompt are gone; the `Scope-decision resume:`
  label stays for legacy markers.
- The failure-hunter writes a `Severity:` line per finding and moves coverage,
  pattern and step-9 notes to `### Coverage`, so the fail-closed rule never
  blocks a note.
- The agents' Memory Notes `**Deferred:**` line carries non-finding follow-ups
  only, so a MEDIUM in `deferred_findings` is not also written to `patterns.md`.
- A trivial build skips BUILD-DONE finishing, so it lists its
  `deferred_findings` in the completion message instead.
- The verifier handoff passes `**High Issues:**` for both agents, so every HIGH
  in the blocking set is validated.
- CRITICAL is read from `### Critical Issues`, `Severity: CRITICAL` entries and a non-zero YAML `CRITICAL_ISSUES`; a reviewer `CHANGES_REQUESTED` or hunter `ISSUES_FOUND` with an empty extracted blocking set still blocks. The reviewer writes positive assertions and risk checks under `### Verified`, and the trivial-scope verifier writes its folded review under `### Folded Review` with a `Severity:` line per entry.
- A reviewer HIGH now makes the verdict `CHANGES_REQUESTED`, so it also stops the QA harness review before `qa-execute` (`qa-workflow.md` *Harness review*) and makes a REVIEW workflow offer REVIEW-to-BUILD. Both are accepted.
- Replay fixture `build-scope-gate.json` now expects `create_remfix` with
  `ALL_ISSUES` and no pending gate; INV-005 is the whole-blocking-set rule.
