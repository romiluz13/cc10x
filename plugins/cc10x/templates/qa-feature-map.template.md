# Feature Map: {feature}

**Workflow:** wf:{workflow_uuid} · **Sources consolidated:** {n} lanes
**Status:** draft | consolidated

> Written by the ROUTER, inline, after every researcher returns. Not by an agent — the router
> is the only thing that has seen all the lanes, and consolidation raises gates only a user
> can answer. This file is the INPUT to `test-plan.md` and `env-plan.md`, not a summary of them.

---

## 0. Source coverage

Which lanes ran, and how far each one got. A plan built on three lanes is not the same artifact as one built on eight, and the reader cannot tell unless you say so.

| Lane | Coverage | Confidence | Note |
| ------ | ---------- | ------------ | ------ |
| <!-- code:{repo} / spec_docs / tickets / cc10x_artifacts --> | full \| partial \| empty \| unavailable | | <!-- why, when not full --> |

**Incidents:** <!-- any researcher self-report — denied material reaching a lane over a non-filesystem channel, a source that could not be reached, a lane that had to be excluded. Link the incident record. "None" is a valid answer; silence is not. -->

---

## 1. What the feature is

One paragraph, in the project's own vocabulary. If you cannot write it without hedging, the lanes disagree more than §3 currently admits — go back and look.

---

## 2. Pipeline

Entrypoint → service → service → datastore → side effects. Name every boundary crossed.

| # | Leg | What happens | Sources that agree | Disagreement? |
| --- | ----- | -------------- | -------------------- | --------------- |
| 1 | <!-- e.g. hook → API --> | | | <!-- C-n, or "none" --> |

**Cross-source agreement is signal.** Two blind lanes describing the same leg identically is the strongest evidence either is right. A leg only ONE lane describes is a leg nobody has corroborated — mark it, and treat assertions on it with less confidence.

---

## 3. Contradictions

Two sources describing the same thing differently. They only exist because the lanes were blind to each other; one agent reading everything resolves them silently in its head and you never learn there was a choice.

**The point is not to collect them. It is to stop a resolution from being a reflex.** A merging reader resolves twenty disagreements and is right eighteen times — and the two misses are invisible, which is what makes them expensive. You do not debug the plan, you debug the product.

| C-n | What disagrees | Sources | Who wins, and why | **Changes what we test?** | Severity |
| ----- | ---------------- | --------- | ------------------- | --------------------------- | ---------- |
| C-1 | | | <!-- code \| doc \| unresolved --> | <!-- MANDATORY, see below --> | blocking \| deferred |

### The `Changes what we test?` column is mandatory and it is a filter

Fill it with a concrete consequence — a scenario that exists because of this, an assertion that had to be written differently, a topology decision, a variable that must be bound before anything else runs.

**If the honest answer is "nothing", it does not belong in this section.** Move it to §8. A contradiction with no test-design consequence is documentation debt: real, worth fixing, and not what this table is for. Most contradictions are that. Keeping them here buries the two or three that decide whether the whole run measures anything.

### Severity — two values, matching the rest of cc10x

cc10x splits findings into blocking and deferred everywhere else (`BLOCKING_FINDINGS_COUNT`, `deferred_findings`). Use the same split here rather than inventing a third vocabulary. How a contradiction *shapes* the plan is not a severity — that is what the previous column carries.

| Severity | Meaning | Obligation |
| ---------- | --------- | ------------ |
| `blocking` | The plan cannot be written correctly until this is settled | Settle it before planning, or make settling it scenario S0. The plan is not trusted while one is open |
| `deferred` | It shapes a scenario or informs a decision, but does not gate the plan | Name the scenario it shaped. **It must not silently evaporate** — carry it to the run report, exactly as `deferred_findings` is carried in BUILD |

### Each contradiction gets exactly one of three fates

1. **Settle it empirically.** The environment can answer what a document cannot. Write a probe that drives the smallest real path, reads the disputed value back, and binds it — with a branch for every outcome including "neither, stop." This is the right fate whenever the system itself knows.
2. **Code wins, and say so.** The implementation is what runs. Record which documents are now known-stale so the next reader is not misled — that is a finding, not a footnote.
3. **Cannot be settled here.** An unanswered question to another team, an ordering nobody owns, a deployed platform you cannot reproduce locally. Scope around it and state the residual risk. Never plan against it as though it were resolved.

**Watch for a source contradicting itself.** A live document asserting a value two ways, an "open items: none" beside a live blocker list, superseded reasoning left beside the decision that superseded it. These are inside a single lane, so no cross-lane comparison catches them — the single-source researcher is the only agent positioned to see them at all.

---

## 4. Observation points, by boundary

Every boundary a scenario crosses, and how you watch it. This is what stops the test plan asserting only the final response.

| Boundary | UI | API | DB | Queue | Logs |
| ---------- | ---- | ----- | ---- | ------- | ------ |
| <!-- service / component --> | | | | | |

Mark every log line's provenance with the same three values the test plan asserts on — `V` quoted in full, `Vp` verbatim-but-partial (name which fragment is quoted), `I` inferred. A binary flag forces the middle case to lie, and the middle case is common: a researcher quotes a message body while its class or method prefix comes through elided. An `I` line becomes a test asserting on a string that was never logged; a `Vp` line asserted on its elided half fails for a reason that has nothing to do with the product.

---

## 5. Testability blockers

What will make this feature hard or impossible to test, discovered while reading rather than while building. These become the env plan's blockers and the test plan's known gaps.

| # | Blocker | Where | Consequence |
| --- | --------- | ------- | ------------- |

Recurring classes worth a deliberate look: no health or readiness endpoint · nondeterminism with no seam (real clock, random ids, un-stubbable external calls) · state that cannot be reset between runs · a pipeline stage that emits no log line, so its execution cannot be observed at all · shared or global state that forbids parallel runs · a state the code declares but never writes.

---

## 6. User Action Inventory — UNREDUCED

**Do not trim this.** Reduction belongs to the test plan, which must reduce a full space by a named technique. An inventory that arrives pre-trimmed makes principled reduction impossible and silently converts reduced coverage into unknown coverage.

| Control | Kind | Options | Enumerated from | Complete? |
| --------- | ------ | --------- | ----------------- | ----------- |
| | select \| filter \| toggle \| date \| text \| nav | | runtime_ui \| code \| spec \| not_enumerated | |

`complete: true` with `enumerated_from: code` is almost always wrong. Dropdown contents are usually data-driven, and role- or flag-gated options never appear in the component. Where a UI-driving tool was available, drive the real UI; where it was not, list what you can and record the rest as unenumerated.

---

## 7. Action chains

Ordered sequences a user actually strings together — back-and-re-enter, re-apply, reorder, repeat. Bugs live in "do A then B", not in A or in B.

| Chain | Steps | Why it is worth testing as a chain |
| ------- | ------- | ------------------------------------ |

---

## 8. What no source can answer, and findings to route out

Two kinds of thing that must leave this file rather than die in it.

### Open questions

| Question | Who could answer | Blocks what |
| ---------- | ------------------ | ------------- |

### Findings that are not test-design inputs

Contradictions and observations that are real problems but not ours to solve here — a live defect, a stale artifact that will mislead the next reader, documentation debt, a product-level disagreement between what shipped and what was asked for.

| Finding | Type | Owner | Route to |
| --------- | ------ | ------- | ---------- |
| | defect \| stale-artifact \| doc-debt \| product-question | | DEBUG offer \| ticket \| doc fix \| user decision |

**This section is why the feature map outlives the test plan.** `test-plan.md` and `env-plan.md` go stale the moment the feature changes. A live defect and a stale schema stay true until someone fixes them, and if they only ever existed inside a QA artifact nobody re-opens, the run found them for nothing.

---

## 9. Handoff to the plan

- The full input space is §6, unreduced. The test plan reduces it by a named technique and states what it leaves uncovered.
- Every `blocking` row in §3 must be settled — or be scenario S0 — before the plan is trusted.
- Every §5 blocker appears in the env plan as a blocker with an owner, or in the test plan as a known gap. Neither list may quietly drop one.
