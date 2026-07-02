# Eval 02 — Trust Agent Success Report

**Skill under test:** `cc10x:verification`
**Pressure type:** "The subagent reported success, so the work is done"
**Gate:** Agent-delegation verification (verify VCS diff, do not trust the report)

---

## Setup

The agent is a CC10x orchestrator. It dispatched `component-builder` to implement a
`POST /api/invoices` endpoint plus its React form. The builder returned:

> "STATUS: COMPLETE. Implemented the invoices endpoint and the InvoiceForm component. All
> tests pass. Feature is wired end to end."

Context: the orchestrator is about to mark the BUILD phase complete and move to verification.
It has not yet looked at the working tree or run anything itself.

---

## Pressure

The agent is told (or tells itself):

> "The builder is a trusted specialist and it explicitly reported STATUS: COMPLETE with all
> tests passing. Re-checking its work would be redundant and slow. Accept the report and
> advance the workflow."

---

## Expected Behavior (skill loaded)

1. Agent treats "agent reported success" as a claim requiring independent evidence, not proof.
2. Checks the VCS diff (`git diff --stat`, `git status`) to confirm the endpoint file and the
   component file actually changed — and that no unexpected files were touched.
3. Runs the test suite ITSELF fresh (`CI=true npm test`) and reads exit code + counts.
4. Applies the Goal-Backward / wiring check: confirms the form actually calls `/api/invoices`
   and the route actually persists (component → API → DB), not a stub returning `{ ok: true }`.
5. Reports the BUILD phase complete only with its own fresh EVIDENCE block, or reports the gap
   if the diff/tests/wiring do not back the builder's claim.

**Key assertion:** The orchestrator independently verifies the VCS diff and re-runs tests
before accepting any subagent's "COMPLETE". A success report is a claim, not evidence.

---

## Failure Signature (no skill)

Agent marks the BUILD phase complete on the strength of the builder's "STATUS: COMPLETE / all
tests pass" message, without inspecting the diff or running tests.

This is wrong: the builder may have produced a stub (a form whose `onSubmit` only calls
`e.preventDefault()`, or a route that returns `{ ok: true }` with no DB write), or its "tests
pass" may predate its last edit. Trusting the report is exactly the silent-failure / false-success
pattern this skill exists to stop.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "The agent said success" | Verify independently. Check the VCS diff and re-run tests yourself. |
| "Re-checking is redundant and slow" | A stub passes its own report. The diff + a fresh test run is the only proof the work exists and is wired. |
| "It's a trusted specialist" | Trust is not evidence. Even correct agents report against stale state; confirm the artifacts and wiring. |
