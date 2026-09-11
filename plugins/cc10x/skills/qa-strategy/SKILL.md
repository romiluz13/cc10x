---
name: qa-strategy
description: |
  Test-system design discipline for the QA route: choosing the right tier, designing
  scenario matrices with pipeline-wide observation points, test-environment topology
  and isolation, fixture lifecycle, and flake sources. Loaded by qa-researcher,
  qa-harness-builder, and qa-executor.
allowed-tools: Read Grep Glob Bash LSP
user-invocable: false
---

# QA Strategy

**Status: DRAFT.** This skill fills the two paths `skills/building/references/integration-and-live-proof.md` already points at but that do not exist (`live-verification-strategy.md`, `live-production-testing.md`). Sections marked PLACEHOLDER need a deep dive.

**Core:** A test suite's value is not how many tests it has. It is how much you would believe a green run.

## Tier selection

The three-layer model in `cc10x:building` still governs — unit proves local behavior, integration proves boundary wiring, E2E proves system truth. QA owns the outer two, plus UI.

| Tier | Proves | Use when |
| ------ | -------- | ---------- |
| `integration` | one boundary really works | route→service, service→DB, producer→consumer, cache/side effects |
| `e2e_backend` | a flow across services really works | the value is produced by services cooperating |
| `ui` | a human can actually do the thing | the deliverable is something a person operates |

**Choose the cheapest tier that can still fail for the right reason.** An E2E test that would also fail for ten unrelated reasons is a bad detector: it fires often and tells you little. Push a check down a tier whenever the lower tier can catch the same defect.

**But do not push everything down.** The defects that survive good unit coverage are exactly the ones that live *between* components — serialization mismatches, transaction boundaries, retry storms, partial failures. Those only appear at the tier where the components are real.

## The scenario matrix

Every feature gets scenarios in three classes. A plan with only the first is not a test plan, it is a demo.

| Class | Question it answers |
| ------- | --------------------- |
| `happy-path` | Does the thing work when everything cooperates? |
| `error-handling` | When a dependency fails, does the system fail *correctly* — right status, right message, right rollback, right log? |
| `edge-case` | What about empty, one, many, max, concurrent, duplicate, out-of-order, expired, and unauthorized? |

### Error-handling scenarios are where the bugs are

For each boundary the flow crosses, ask: what happens when it is slow, down, returns garbage, returns a partial result, or succeeds after the caller gave up? Each answer that matters is a scenario.

The most valuable single question: **when this fails halfway, what state is left behind?** Partial-failure state is where data corruption lives, and it is almost never covered by accident.

## Input-space coverage — enumerate exhaustively, then reduce deliberately

The goal is to cover **as many user actions and chains of actions as possible**: every option in a dropdown, every date class, every filter, every combination that a real user could produce.

### Step 1 — enumerate the full input space (do this exhaustively)

For every interactive surface in the flow, list every option a user can actually pick:

- every dropdown / select — **every** option, not "a representative one"
- every filter, toggle, checkbox, radio
- every date field — today, past, future, boundary of range, invalid, empty
- every free-text field — its equivalence classes
- every navigation path that reaches the same screen
- every chain — the ordered sequences of actions a user strings together

**Discover, do not assume.** Options are usually data-driven; reading the component tells you a `<select>` exists, not what is in it at runtime. Drive the real UI to enumerate actual values (see *UI tier tooling* below). An enumeration built from the code alone will miss the options that only appear for certain roles, tenants, or feature flags.

Record the full enumeration in the test plan even when you will not execute all of it. **The enumeration is the coverage claim.** What you skip must be visible.

### Step 2 — reduce with a technique, not by taste

Full combinatorial coverage is not achievable and pretending otherwise produces an unbuildable plan: 5 filters × 4 options each is 1,024 combinations; add a date and a sort and you are past 10,000. Nobody runs that suite, so in practice it never gets written, and you end up with *less* coverage than an honest reduction would have given.

Reduce with a named technique, and **record which one you used and what it leaves uncovered**:

| Technique | Use for | What it costs |
| ----------- | --------- | --------------- |
| **Every-option-once** | dropdowns, radio groups | Each option exercised at least once. Misses interactions between options. |
| **Pairwise (all-pairs)** | combinations of 3+ independent controls | Every *pair* of values co-occurs in some case. Collapses 1,024 → ~25. Misses 3-way interactions, which are rare. |
| **Equivalence classes** | free text, numbers, dates | One representative per class of behavior. Misses defects inside a class. |
| **Boundary values** | anything with a range | 0, 1, max, max+1, empty, null. Where most defects actually live. |
| **Full combinatorial** | 2 controls with few values, or a genuinely safety-critical path | Complete. Only affordable when the space is tiny. |

**Default recipe:** every-option-once for single controls, pairwise across combinations, boundary values on every range, plus full combinatorial on any combination that is known to be risky (billing, permissions, anything where two settings interact by design).

**Pairwise is the highest-leverage tool here.** Most combination defects come from two settings interacting, not five. All-pairs buys the large majority of that value for a small fraction of the runs.

### Step 3 — chains, not just single actions

A user action rarely stands alone. Cover the sequences too:

- **the primary chain** — the full path a real user walks, end to end
- **back / re-entry** — leave mid-flow and return; is state preserved or correctly discarded?
- **re-application** — apply a filter, change it, clear it, apply another
- **order variation** — does filter-then-search behave like search-then-filter?
- **repetition** — the same action twice; the same submit double-clicked

Chains are where state bugs live, and they are almost never found by testing actions in isolation.

### Feature flags are a coverage dimension, not a setup detail

A feature shipped behind a flag has **two live code paths in production**, and only one of them is new. Both need coverage:

| State | What it proves | Why it gets skipped |
| ------- | ---------------- | --------------------- |
| Flag ON | The feature works | Nobody skips this one |
| Flag OFF | The old path still works, or the feature is cleanly absent | Feels redundant — it is not |
| Toggled mid-session | State written under one path is readable under the other | Rarely considered at all |

**The OFF path is where the expensive incidents live.** A flag gets rolled back precisely when something is already going wrong, and that is the worst possible moment to discover the rollback does not restore a working system. If a flag is genuinely one-way, that is a finding to surface, not a row to skip.

Where **entitlements** or plan tiers exist alongside flags, they are independent gates. `flag-on + entitlement-off` must degrade correctly rather than 500 — a combination almost no plan covers, because each gate is usually tested alone.

**Confirm a flag applied, do not confirm it was set.** Asserting that the config call returned 200 proves the call returned 200. Caches, restart requirements, and per-pod config all break the leap from "set" to "in effect", and they break it silently.

### Edge cases worth a default look

- boundaries: 0, 1, max, max+1
- concurrency: two of the same request at once; the same idempotency key twice
- ordering: out-of-order and duplicate messages
- time: expiry, timezone, clock skew, retry after timeout
- identity: unauthorized, wrong tenant, expired token
- data: unicode, very long strings, null vs. absent

## Observation points — the pipeline-wide assertion

A scenario that asserts only the final response tests the response. It does not test the pipeline.

For each scenario, name what should be observable at every stage:

| Point | Asserts |
| ------- | --------- |
| UI | what a person sees |
| API | status, response shape, headers |
| DB | rows/documents actually written, in the right state |
| Queue | messages actually published, with the right payload |
| **Logs** | each pipeline stage actually ran, and said so properly |

### Why logs are a first-class assertion

Logs are the only cheap way to prove that a *middle* stage executed. A 200 at the edge is consistent with a worker that never ran, a retry that silently swallowed, or a branch that fell through.

Asserting logs also makes the suite an enforcement point for the project's logging standard: if a scenario asserts a structured log line with named fields and the line is missing, unstructured, or logged at the wrong level, that is a real finding about observability — found by a test, before an incident needs it.

Assert on **level + message + structured fields**, not on a substring of a formatted line. Substring assertions on log text are among the most brittle tests it is possible to write.

**PLACEHOLDER — log access strategy.** How the harness reads logs differs sharply by environment (local stdout, container logs, a log platform). Needs a deep dive, likely with `ox-datadog-toolset` as one backend.

## Test environment

### Isolation model

Ranked by strength:

1. **Ephemeral everything** — fresh DB, fresh services per run. Strongest; slowest.
2. **Fresh data, shared services** — services stay up, schema/data reset between runs. Usually the right trade.
3. **Namespaced in a shared environment** — every run scopes itself by a unique prefix/tenant. Only when 1 and 2 are impossible; leaks are hard to detect and the failure mode is cross-run interference that looks like flake.

**Never test against an environment someone else is using.** A suite that intermittently fails because a colleague was clicking around teaches the team to ignore red.

### Readiness, not sleeping

`sleep 30` is a race condition with a comment. Gate on a real signal — health endpoint 200, port accepting, migration complete, topic created — with a bounded timeout and a loud failure.

An under-gated environment produces failures that *look like product bugs*. That is precisely how a team learns to distrust its own suite.

### Teardown

Teardown must verify itself. "Ran `docker compose down`" is not evidence; "`docker ps` shows nothing from this run" is. A suite that leaks will eventually make its own machine unable to run it.

### Determining the topology — ask, then detect, then confirm on screen

Never silently infer how to run the system. The order is fixed:

1. **Ask the user first.** They know whether there is a compose file that works, a staging environment, or a cloud-only deploy. One question here saves an hour of wrong inference.
2. **Then detect**, using whatever the machine actually offers — compose/Tilt/Skaffold files, testcontainers in the manifest, `kind`/`k3d`, available MCP servers, project skills, plugins, and agents that already know how to run this system.
3. **Then present the findings on screen and get explicit confirmation** before building anything. Show the proposed topology in the conversation — not only written to a file. A plan the user never actually looked at is not an approved plan, and the environment is the single most expensive thing to get wrong.

Write the confirmed topology to `env-plan.md` *after* the user confirms it, not before.

### Settle contradictions with a probe, not with a preference

When the feature map records a contradiction about something the plan depends on — which tenant a record lands under, which queue is consumed, which identity is resolved, which of two documented shapes the wire actually carries — **the environment can usually answer it, and a document cannot.**

Write the first scenario as a probe: drive the smallest real path that exposes the disputed value, read it back, bind it to a plan variable, and enumerate one branch per outcome *including* a branch where neither expected answer appears and the run stops. Then place the probe in the bring-up sequence as a **gate**, before anything that consumes what it binds.

Picking the likelier answer instead is what makes contradictions expensive. The plan does not fail at the contradiction — it fails ten scenarios later as a mount fault, an empty queue, or a broker error, and the run gets spent debugging the harness instead of the product.

### A stub inside the process under test can be the bug

Some controls can only be applied by injecting something into the process you are measuring — a clock shim, a module preload, a patched global, a stubbed transport. That is sometimes the only lever available, and it is legitimate. It is also a stub *inside* the thing under test, which means a failure it causes is indistinguishable from a product failure until someone looks.

When you must do it: name it as a risk in the plan, keep the patch as narrow as the assertion requires, and prefer patching a value over patching a mechanism. Patching `Date.now` moves thresholds. Patching the timer wheel moves the event loop into orderings the product never produces — the first is an observation aid, the second is a source of fiction.

And prove it applied. A shim that silently failed to load produces a scenario that passes for the wrong reason.

## UI tier tooling

Two different tools for two different jobs. Use both, for what each is good at.

| Tool | Use it for | Do not use it for |
| ------ | ------------ | ------------------- |
| **Agentic browser** (`claude-in-chrome`) | **Discovery** — driving the real UI to enumerate what is actually there: every dropdown option, every filter value, what a role can see, what a page really renders | The deliverable. A browsing session is not an artifact; it cannot re-run next month without an agent and a live browser |
| **Playwright** (`ox-playwright`) | **The deliverable** — durable spec files that run headless, in CI, unattended, repeatably | Exploring an unfamiliar UI from scratch; it is slow going without knowing what is on the page |

**The pipeline is: explore agentically → enumerate → codify as Playwright specs.** Discovery feeds the input-space enumeration above; the specs are what `qa-execute` runs as a standalone regression suite forever after.

**Selector durability matters more than it seems.** Specs pinned to CSS classes or DOM position break on the next refactor and get deleted rather than fixed. Prefer roles, labels, and test ids — what a user perceives, not how it is currently marked up.

## Fixtures and determinism

- **Deterministic by construction:** fixed seeds, injected clock, controlled id generation. If a test can pass or fail depending on the wall clock, it will eventually do both.
- **Build data through the system's own front door** where practical — a fixture written directly into the DB can encode a state the application can never actually produce, and then you are testing fiction.
- **Fixtures are code.** They get reviewed. A fixture that drifts from the real schema produces tests that pass against a shape production never sends — the schema-incomplete-mock failure `integration-verifier` already watches for.
- **Where a fixture LIVES can change what the product does to it.** Many systems exclude paths by convention — anything under `test/`, `fixtures/`, `samples/`, `examples/`, `node_modules/`, a `.dockerignore` entry, a gitignore-derived skip list. A fixture scanned, indexed, or uploaded from such a path is silently skipped, and the scenario under-reports with no error and no log line. Stage fixtures at a path with none of those components, and prove the product actually consumed the fixture rather than inferring it from a green result.

## Flake sources, ranked

1. **Time** — sleeps, timeouts tuned to one machine, timezone, clock skew
2. **Order dependence** — a test that only passes after another test ran
3. **Shared state** — leftover rows, caches, singletons, ports
4. **Real network** — an external call in a test is a scheduled outage
5. **Under-gated readiness** — asserting before the system is up

**A flaky test is a broken test.** Re-run once to classify it, never repeatedly to reach green. Quarantine and fix; a suite people re-run until it passes is a suite that proves nothing.

## Proving the suite can fail

Before believing any harness: break the thing under test on purpose and confirm the test goes red. At minimum once per tier.

An assertion that has never been observed failing is unproven, and unproven assertions are how a suite drifts into decoration. This is the single highest-value check in the whole discipline, and it takes minutes.

**The inverse failure — asserting a state the code cannot produce.** Sometimes a scenario is unfalsifiable in the other direction: the state it checks for is unreachable, so the assertion can never fire at all. A status value the code never writes, an error branch with no caller, a field only a mock ever populates.

When you find one, assert the **absence** instead — "no row is written" is a real, checkable property, and it is usually the behaviour that actually matters. Reaching the unreachable state by writing a fixture past the application's own validators is testing fiction: it may still earn a place (the UI's handling of a shape it might one day receive is worth knowing), but label it as fiction in the plan so nobody reads its PASS as evidence about the product.

The tell is a scenario whose setup has to bypass the system's front door to exist.

## Anti-patterns

| Anti-pattern | Why it is wrong |
| -------------- | ----------------- |
| Asserting only the final response | Proves the edge, not the pipeline |
| `expect(x).toBeTruthy()` | Passes for almost everything |
| `sleep` as readiness | Race condition with a comment |
| Catch-and-continue in setup/teardown | Turns a broken environment into a green run |
| Skipped tests reporting as passed | A lie with good manners |
| Re-running until green | Converts a real defect into a statistic |
| Fixtures written straight into the DB | Can encode states the app cannot produce |
| Testing against a shared live environment | Interference reads as flake; team learns to ignore red |
| Editing the test to make the run pass | Destroys the only thing QA produces |

## Artifact templates

Every QA artifact has a shipped skeleton. **Copy it and fill in place** — do not improvise document structure, and do not delete a section that does not apply (mark it `N/A` with a reason).

| Artifact | Template |
| ---------- | ---------- |
| `test-plan.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-test-plan.template.md` |
| `env-plan.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-env-plan.template.md` |
| `feature-map.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-feature-map.template.md` (router-owned, inline consolidation) |
| `setup.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-setup.template.md` — **environment-scoped, not per-run.** Lives at `.cc10x/qa/env/{env_key}/setup.md`, append-only, and records only MEASURED facts. It is the counterpart to `env-plan.md`: the plan predicts the environment from source, this records what the machine actually said |
| `report.md` | skeleton in `agents/qa-executor.md` |
| harness manifest | `${CLAUDE_PLUGIN_ROOT}/templates/live-harness.template.json` |

**Why deletion is forbidden.** The sections most often dropped are the ones that record what the plan does *not* do — the coverage-reduction table, known gaps, teardown verification, re-runnability. Those are precisely the sections an optimistic plan omits. A missing section reads as "nothing to report"; an `N/A` with a reason reads as a claim someone can challenge.

## Reference files

**PLACEHOLDER** — to be split out as this skill grows past a single file, matching the pattern in `cc10x:building` and `cc10x:frontend`:

- `references/environment-topologies.md` — compose / testcontainers / cloud ephemeral, with worked setups
- `references/observability-assertions.md` — log, metric, and trace assertions per backend
- `references/ui-qa-automation.md` — Playwright vs. agentic browser driving, selector durability
- `references/harness-manifest.md` — the schema `tools/live_harness_runner.py` consumes
