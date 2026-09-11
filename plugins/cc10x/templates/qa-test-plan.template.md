# Test Plan: {feature}

**Workflow:** wf:{workflow_uuid} · **Feature map:** `.cc10x/qa/{workflow_uuid}/feature-map.md`
**Environment:** `.cc10x/qa/{workflow_uuid}/env-plan.md`
**Status:** draft | reviewed@r{n} | approved@r{n}
<!-- A bare `reviewed` is the unqualified claim the wording law forbids; name the revision it
     applies to. `{n}` here is the QA amendment-sweep marker (`r2`/`r3`) written by `qa-re-plan`
     into the three QA plan artifacts — NOT the PLAN route's `plan_revision`, which is an integer
     in the workflow artifact owned by the router. Binding this to `plan_revision` would import a
     PLAN-route key into a QA artifact and re-open the ownership question §3 Q2 settles. -->

**verification_rigor:** standard | critical_path
**Differences from agreement:** <!-- how this plan departs from what was requested/confirmed; "none" is a valid answer, absence is not -->

> The last two fields exist because cc10x's `plan_trust_gate` reads them. `Differences from
> agreement` must be present even when empty — a silent departure from what the user agreed to
> is the failure it is there to catch.

---

## 0. Constraints that shape every assertion

**Mandatory.** These are measured facts from the feature map and the researcher reports — not wishes to be engineered away. Every scenario below is written *inside* them.

The purpose of this section is to stop a plan from asserting things the system cannot express. A plan written without it produces assertions that look rigorous and are unfalsifiable: a "service is up" check against a service with no health endpoint, a latency bound against a product with no SLO, a "failed" state the code can never write.

| Constraint | Consequence for assertions |
| ------------ | ---------------------------- |
| <!-- e.g. no health/readiness endpoint exists on any service --> | <!-- e.g. readiness is a log line plus a functional probe; no scenario may assert "up" via HTTP --> |
| <!-- e.g. the mutation returns 200/false on every downstream failure --> | <!-- e.g. no scenario's ONLY assertion may be that boolean --> |
| <!-- e.g. no latency SLO is stated anywhere --> | <!-- e.g. every time bound is a harness liveness bound, not a product SLO --> |
| <!-- e.g. state X is unreachable in code --> | <!-- e.g. assert the ABSENCE of the row; a fixture-forced X is testing fiction and is labelled as such --> |

Three rules follow from this section and bind the whole plan:

1. **A time bound is a harness liveness bound, never a product SLO** — unless a source states an SLO. Blowing an unsourced bound is `BLOCKED`/`TIMEOUT`, never a product `FAIL`. Round the other way and the suite manufactures bugs.
2. **`BLOCKED` is a distinct outcome from `FAIL` and from `PASS`.** A scenario that could not run has not passed. It never rounds up.
3. **When a state is unreachable in code, assert its absence** — not its appearance. If reaching it needs a fixture written past the application's own validators, that scenario is testing fiction: keep it only if it earns its place, and label it plainly so no one reads its PASS as product evidence.

---

## 1. Scope

**Under test:** <!-- the flow, named concretely enough to write scenarios against -->
**Not under test:** <!-- explicitly out of scope, so a reader knows this is a boundary, not an oversight -->
**Services involved:** <!-- every service the flow crosses -->

### Preconditions carried from the environment

| Requirement | Value | Source |
| ------------- | ------- | -------- |
| Feature flags ON | | env-plan §2 |
| Feature flags OFF | | env-plan §2 |
| Entitlement / plan tier | | env-plan §2 |
| Actor role / permissions | | env-plan §2 |
| Org / tenant settings | | env-plan §2 |
| <!-- any precondition preflight MEASURED --> | | `setup.md` §2 |

**`Source` may be `env-plan §N` or `setup.md §N`, and the difference matters.** An `env-plan`
source is a *prediction* written from source code; a `setup.md` source is a fact preflight
*observed* on the machine. When the two disagree, the measurement wins and the disagreement is
itself a finding — record it in `setup.md` §4 rather than quietly preferring one.

Restate them here rather than cross-referencing. A scenario that silently assumed a flag was on is indistinguishable from a product bug when it fails, and the reader of a scenario should never have to open a second document to know what state it needs.

---

## 2. Coverage plan

The User Action Inventory in the feature map is the full input space. This table is how much of it this plan actually executes, and by what rule.

**Reduction is deliberate, never silent.** Full combinatorial coverage is unachievable on any real UI — 5 filters × 4 options is 1,024 cases — and a plan that claims it never gets built, which yields less coverage than an honest reduction. State the technique and state the residual risk.

| Control group | Space size | Technique | Cases | Uncovered — and why that is acceptable |
| --------------- | ------------ | ----------- | ------- | ---------------------------------------- |
| <!-- e.g. status filter --> | | every-option-once | | |
| <!-- e.g. filter × sort × date --> | | pairwise | | 3-way interactions |
| <!-- e.g. page size --> | | boundary values | | mid-range values |
| <!-- e.g. billing × permission --> | | full combinatorial | | none |

**Techniques:** `every-option-once` · `pairwise` (all-pairs) · `equivalence-classes` · `boundary-values` · `full-combinatorial` · `risk-ranked` (name this one explicitly wherever the reduction is by expected defect density rather than by structure — it is the only technique whose justification is a judgement call, so it must be visible as one)

**Every number in the `Cases` column must be traceable to the scenario rows that deliver it.** Write the counts as `N (S3, S7, U2)`, not as a bare `N`. A claimed case count with no delivering scenario is the most common way a plan overstates its own coverage, and it survives review because the arithmetic looks right. Before finalising, walk each row backwards from the count to the bodies; when the count and the bodies disagree, the count is wrong, and the surplus moves to the `Uncovered` column.

### Every rollup in this section must reconcile

**Before finalising, count.** The scenario ids listed across `Coverage by class` must equal the ids across `Coverage by tier`, must equal the ids across §3's waves, and must equal the total scenario count in §4. State the total explicitly and show the arithmetic (`S0–S25 = 26 · H1–H15 = 15 · U1–U16 = 16 → 57`).

This is not bookkeeping. cc10x already refuses a *run* whose evidence count does not reconcile with its scenario accounting — `integration-verifier` counts `EVIDENCE = SCENARIOS_TOTAL`, and `qa-executor`'s contract calls a mismatch invalid output. The same gate belongs one phase earlier: a plan that claims coverage it does not deliver produces a run that cannot be reconciled, and the mismatch is discovered after the harness is built rather than before.

An off-by-one here is not cosmetic. The scenario most likely to fall out of a rollup is the one added last or the one that does not fit the usual shape — which is disproportionately the blocking probe or the one deliberate expected-failure, i.e. the highest-value row in the plan.

### Coverage by class

Every feature needs all three. A plan with only happy-path is a demo, not a test plan.

| Class | Scenarios | Notes |
| ------- | ----------- | ------- |
| happy-path | | |
| error-handling | | <!-- per boundary: slow, down, garbage, partial, late-success --> |
| edge-case | | <!-- boundaries, concurrency, ordering, time, identity, data shape --> |

### Coverage by tier

| Tier | Scenarios | Why this tier |
| ------ | ----------- | --------------- |
| integration | | |
| e2e_backend | | |
| ui | | |

### Coverage by flag state

**A flag is a scenario dimension, not just setup.** A feature shipped behind a flag has two live code paths in production, and only one of them is the new one. Cover both.

| Flag | ON — feature behaves correctly | OFF — old path still works / feature absent cleanly | Toggled mid-session |
| ------ | -------------------------------- | ----------------------------------------------------- | --------------------- |

The OFF column is the one that gets skipped, and it is where the expensive incidents come from: a flag rolled back after an incident must return the system to a working state, and nobody finds out whether it does until that moment. If a flag is genuinely one-way (no rollback path), say so here — that is a finding worth surfacing, not a reason to skip the row.

**Entitlement × flag.** Where both exist they are independent gates: flag-on + entitlement-off must degrade correctly, not 500.

---

## 2c. Provable properties

**Required when `verification_rigor: critical_path`. Optional otherwise.** This mirrors the rule PLAN
already enforces on itself — a `critical_path` plan must carry non-empty provable properties — and it
exists so the harness builder's mutation floor has a unit finer than "a tier".

A scenario is a thing you run. A **provable property** is a thing the run is supposed to
*discriminate*: a claim that would be false in some reachable world, and that a green suite is
asserting is not. Naming them here is what lets the harness builder prove each one can go false,
instead of proving that one assertion somewhere in a tier can go false and calling the tier honest.

| PP-id | Property — what a green run is claiming is true | Scenario ids that would break it | At risk of appearing proven |
| ------- | ------------------------------------------------- | ---------------------------------- | ----------------------------- |
| PP-1 | <!-- a claim that could be false --> | <!-- S3, S7 — or `—` --> | yes \| no |
| PP-2 | | | |

**The fourth column is a self-flag, and the cost points toward honesty.** `yes` means: this property
is one a suite could plausibly appear to prove while proving nothing — the assertion is loose, the
observation point is downstream of the thing that would break, or the scenario would still pass with
the feature removed. Above **8** properties the mutation floor applies only to the rows flagged `yes`.
Declining to flag any row does not buy a cheaper run: a plan with no `yes` rows falls back to the
per-tier-**and**-per-wave floor, which is strictly more mutation work in most shapes than flagging
honestly would have been.

### The three mapping cases, and the floor in each

The third column will not map one-to-one onto §4, and it is not supposed to. All three shapes are
legal; each has a different floor, and the harness builder reads this table to know which applies.

| Case | Shape | Floor |
| ------ | ------- | ------- |
| One property → many scenarios | `PP-4 \| … \| S3, S7, S11 \| yes` | **One** falsified assertion anywhere in `{S3, S7, S11}` satisfies PP-4. The *property* is what must be shown discriminating; which scenario shows it is the harness builder's choice. |
| Many properties → one scenario | `PP-2 \| … \| S9` and `PP-5 \| … \| S9` | **Two separate mutations of S9**, one per property, each naming a different failing assertion. A scenario that asserts two things needs two sabotages to show both assertions can independently go false. Collapsing them into one is the conflation this section exists to end. |
| Property → no scenario | `PP-8 \| … \| —` | **Cannot be floored.** It falls back to its tier's floor, and the harness builder MUST list it in `TESTABILITY_BLOCKERS` with the reason. An unmapped property is a plan defect with an honest exit — it escalates to a BUILD for the missing seam, never to a silent pass. |

**Reconciliation.** Every `PP-id` names at least one scenario id that actually exists in §4, or names
`—` and is carried into the harness builder's `TESTABILITY_BLOCKERS`. A row naming a scenario id that
§4 does not contain, and a row with an empty third column, are both plan-review findings of the same
class as a rollup that does not add up — the fresh review pass already reconciles rollups against the
scenario set, and this table is one more rollup for it to reconcile.

---

## 3. Build order

**Mandatory.** A flat list of scenarios is not a buildable plan. Nobody builds fifty scenarios in one sitting, and a plan that does not say where to start stalls at the starting line — or gets built in discovery order, which puts the cheapest scenarios first and the load-bearing ones last.

This mirrors what every other cc10x plan already does: `planner` normalizes work into ordered phases with `dependencies` and an `objective`, and BUILD walks them one at a time through `phase_exit_gate`. A test plan is a plan. Give it phases.

| Wave | Scenarios | Objective — what this wave proves | Depends on | Stop-if |
| ------ | ----------- | ----------------------------------- | ------------ | --------- |
| 1 | <!-- the smallest set that proves the pipeline is wired end to end --> | | — | <!-- what makes it pointless to continue --> |
| 2 | | | wave 1 | |
| 3 | | | | |

Rules that make the waves real:

- **Wave 1 is the thinnest slice that proves the system is wired**, including any probe that binds a variable later waves consume. If wave 1 cannot pass, later waves cannot be interpreted — their failures will be environment artifacts, not product findings.
- **Every wave carries a `Stop-if`.** A wave whose premise is broken must halt the build rather than hand the next wave a false baseline.
- **Order by what a failure teaches you**, not by tier and not by scenario id. A cheap scenario that discriminates between two failure causes is worth more early than an expensive one that only confirms the happy path.
- **A scenario appears in exactly one wave.** Every scenario in §4 appears in exactly one row here; the union of the waves is the full scenario set. Reconcile it (§2's reconciliation rule applies to this table too).

---

## 4. Scenarios

<!-- Repeat this block per scenario. Observation points are the point: a scenario
     that asserts only the final response tests the response, not the pipeline. -->

### S0 — environment-truth probe (include whenever the feature map records a contradiction the environment can settle)

When two sources disagree about something the rest of the plan depends on — which tenant a record lands under, which queue is consumed, which identity is resolved — **do not pick the likelier answer and write the plan on top of it.** Make the first scenario a probe that settles it empirically, and make it blocking.

**Shape:** drive the smallest real path that exposes the disputed value → read the value back → bind it to a plan variable → enumerate one branch per possible outcome, including a `STOP` branch when neither answer appears.

This matters more than it looks. A plan built on the wrong branch of a contradiction does not fail cleanly at the contradiction; it fails ten scenarios downstream as a mount fault, an empty queue, or a broker error, and the run gets spent debugging the harness. A probe converts a documentation contradiction into a bound variable in one step, and its `STOP` branch is what stops a mis-wired environment from being reported as a wall of product bugs.

The probe belongs in the env-plan's bring-up sequence as a **gate**, not a smoke test — it must run before anything that consumes the value it binds.

---

### S{n} — {name}

**Tier:** integration | e2e_backend | ui
**Class:** happy-path | error-handling | edge-case
**Covers:** <!-- which inventory rows / which reduction case -->

**Preconditions:** <!-- flags/settings this scenario needs, only where they DIFFER from §1 defaults; "as §1" otherwise -->
**Given:** <!-- starting state, including seeded data and the variant in play (role, tenant, locale) -->
**When:** <!-- the action: API call, UI interaction, message published -->

**Then observe:**

| Point | Expected |
| ------- | ---------- |
| UI | <!-- what the user should see --> |
| API | <!-- status, response shape --> |
| DB | <!-- store, and the expected row/document state --> |
| Queue | <!-- topic, and the expected message --> |
| Logs | <!-- {service} emits {level} "{message}" with fields {a, b, c} --> |

<!-- These five are a FLOOR, not the set. Add a row for every datastore this pipeline
     actually writes to — a shared filesystem or mount, a cache, an object store, an
     external system of record. Where most of the interesting state lives nowhere but a
     mount, a five-row table silently omits the only observation point that matters.

     Omit a row only when that point genuinely does not exist in this flow.
     Never omit it because it is inconvenient to assert.
     Log assertions are the only cheap way to prove a MIDDLE stage ran — a 200 at the
     edge is consistent with a worker that never fired. Assert level + message + fields,
     never a substring of formatted log text. -->

**Cleanup:** <!-- what must be undone for the next scenario to start clean -->

---

## 5. Observability assertions

| Service | Stage | Level | Message | Required fields | Provenance |
| --------- | ------- | ------- | --------- | ----------------- | ------------ |

**Provenance has three values, not two.** A binary verbatim/inferred flag forces the middle case to lie in one direction or the other, and the middle case is common:

| Value | Meaning | What may be asserted |
| ------- | --------- | ---------------------- |
| `V` | Quoted from source in full | The whole string |
| `Vp` | **Verbatim-but-partial** — part of the line is quoted and part was elided (a truncated prefix, an `…`, a placeholder for a class or method name) | **Only the quoted fragment.** Name which fragment |
| `I` | Inferred — nobody quoted this; it is what the line probably says, or it is a function name mistaken for a message | Nothing, until confirmed against the code |

`Vp` is the value that earns this table. An assertion built on the elided half of a partially-quoted line fails for a reason that has nothing to do with the product — and where two log lines share a quoted body but differ in the elided part, asserting on the wrong half can silently *invert* a scenario's verdict. Where that risk exists, say so in the row.

This mirrors `code-reviewer`'s `CANNOT_VERIFY_FROM_DIFF`: cc10x already treats "I could not fully confirm this" as a first-class value rather than rounding it to yes or no.

---

## 6. Test data

| Fixture | Built via | Deterministic? | Notes |
| --------- | ----------- | ---------------- | ------- |

Prefer building data through the system's own front door. A fixture written straight into the datastore can encode a state the application is incapable of producing — and then the suite tests fiction.

---

## 7. Known gaps

| Gap | Reason | What a PASS does NOT prove | Severity |
| ----- | -------- | ---------------------------- | ---------- |
| | | <!-- MANDATORY --> | blocking \| deferred |

**Mandatory, even when empty.** A plan that lists only what it covers reads as complete coverage. Naming the gap is how a reader calibrates what a PASS is worth.

**Ranked, not listed in discovery order.** Fifty gaps in the order they were found gives a whole-tier blind spot the same visual weight as a missing mid-range value, and the reader calibrates on neither. Two values only — matching how cc10x already splits findings everywhere else:

| Severity | Meaning | Obligation |
| ---------- | --------- | ------------ |
| `blocking` | The suite cannot be believed about something it appears to cover | Resolve, or state it in §8 as an open decision, before the harness is built |
| `deferred` | Real, non-blocking, and **must not silently evaporate** | Carried into the run report and surfaced to the user at the end — the same contract `deferred_findings` carries in BUILD |

**A cross-service stub always earns a row here, tagged `unproven by stub`.** A stub written from the calling side encodes that side's belief about the wire, so it cannot disagree with the caller and the scenario passes whether or not the real service reads the field. Keep the scenario in the §4 waves and the §2 rollups so the counts reconcile; take it out of the coverage `Cases` column and carry the difference in *Uncovered — and why that is acceptable*.

**The `What a PASS does NOT prove` column is the point of the row.** "This is untested" is not calibration; "a green run here is consistent with the analyzer never having executed" is. If the column cannot be filled with a concrete false-confidence statement, the row is probably a scope note and belongs in §1's *Not under test*.

---

## 8. Open decisions

| # | Decision | Blocking? |
| --- | ---------- | ----------- |

Any unresolved blocking decision stops the harness build. Do not build against an unresolved contradiction.
