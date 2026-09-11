# Test Environment Plan: {feature}

**Workflow:** wf:{workflow_uuid} · **Test plan:** `.cc10x/qa/{workflow_uuid}/test-plan.md`
**Mode:** local | compose | testcontainers | cloud_ephemeral | manual_instructions
**Confirmed with user:** yes / no — <!-- MUST be yes before the harness is built -->
**Differences from agreement:** <!-- how the built environment departs from what was confirmed on screen; "none" is a valid answer, absence is not -->

> This plan is written only AFTER the topology was proposed on screen and the user confirmed it.
> The environment is the most expensive thing in a QA workflow to get wrong: a bad topology
> produces failures that look like product bugs, and that is precisely how a team learns to
> distrust its own test suite.

**Maps 1:1 onto the harness manifest** (`templates/live-harness.template.json`). Section → key:
§4→`setup[]` · §5→`reset[]`/`seed[]` · §4 readiness→`healthcheck` · §7→`required_env`/`environment` · §9→`cleanup[]`.
<!-- Corrected: every mapping except `cleanup[]` was stale by the insertion of §2 (feature flags) and
     §3 (prerequisites). The section NUMBERS are not renumbered — renumbering would invalidate every
     env-plan.md already on disk. Only the references are corrected. -->
Write these sections so `qa-harness-builder` can translate them mechanically, not creatively.

---

## 1. Topology

**How the system runs for testing:** <!-- one paragraph a newcomer could act on -->

| Service | Real or stubbed | Started by | Reachable at | Why stubbed (if stubbed) |
| --------- | ----------------- | ------------ | -------------- | -------------------------- |

**Every stub needs a justification.** A stub can *be* the bug — if a scenario fails, the harness must be able to rule out the stub before blaming product code.

### Wiring

How services find each other: <!-- network, ports, service discovery, DNS, env vars -->
Port allocation: <!-- fixed or dynamic; how collisions are avoided on a shared machine -->

---

## 2. Feature flags, settings, and entitlements

**The single most common cause of "works on my machine, not in the test env".** A feature behind a flag that nobody flipped does not fail loudly — it is simply absent, and the scenario fails in a way that looks like a product bug.

| Flag / setting | Where it is set | Default | Required value | Scope | Who can change it |
| ---------------- | ----------------- | --------- | ---------------- | ------- | ------------------- |
| <!-- e.g. enableX --> | <!-- env var, config file, LaunchDarkly, DB row, admin UI --> | off | on | global / org / user | |

**Cover each category that applies:**

- **Feature flags** — service-side and client-side; they are often set in different places
- **Runtime config / env vars** that change behavior (not secrets — those are §7)
- **Entitlements / licensing / plan tier** — a feature can be flag-on and still entitlement-off
- **Permissions and roles** — which role the test actor needs
- **Org / tenant settings** — admin-configurable toggles
- **Kill switches and rollout percentages** — a 10% rollout is nondeterministic unless pinned

### Flags that must be OFF

| Flag | Why it must be off |
| ------ | -------------------- |

Easy to miss and expensive: an unrelated flag left on can mask the behavior under test, or route the request down a path the plan never accounted for.

### Verification

How the harness **confirms** each flag actually took effect — not that it was set, that it applied:

| Flag | Verification |
| ------ | -------------- |

Setting a flag and asserting the API call succeeded proves the call succeeded. It does not prove the running process observed the new value — caches, restart requirements, and per-pod config all break that assumption silently.

> Flag state is also a **scenario dimension**, not only setup. A feature behind a flag needs coverage with it ON *and* OFF — see test plan §3.

---

## 3. Prerequisites

| Requirement | Owner | Cost tier | Check command | How to acquire | If missing |
| ------------- | ------- | ----------- | --------------- | ---------------- | ------------ |
| | human \| harness \| external \| harness decision | T1 \| T2 \| T3 \| T4 | | | |

A missing prerequisite is **BLOCKED**, never FAIL. Environment problems must never be converted into a verdict about product code.

**`Owner: human` with an empty `How to acquire` fails this plan's own completeness bar.** That single
rule is the difference between a run that stops at a missing credential and a run that stops at a
missing credential *with a one-line fix*. If the recipe is genuinely unknown, write what was tried
and who would know — an honest dead end is still actionable; a blank cell is not.

**`Cost tier` orders preflight, and the ordering is the point.** Nothing in a higher tier runs until
every lower tier is green, so a T1 credential check can never be discovered after a T4 build:

| Tier | What belongs here | Typical cost |
| ------ | ------------------- | -------------- |
| `T1` | static existence — nothing is executed against a service (`command -v`, a file exists, an env var is set, a regex on a resolved path) | ms |
| `T2` | local probes — nothing is *started* (port bind-probe, `docker info`, `node -v`, `--help`) | seconds |
| `T3` | reachability of things already running that we did not start (an external service answers, a shared DB accepts a connection) | seconds |
| `T4` | cheap builds and gates (`npx tsc --noEmit`, grep the installed build for a this-build-only symbol) | 10s–1min |

There is no T5. **Booting a service is not preflight** — it belongs to `qa-build` / `qa-execute`.

---

## 4. Bring-up → manifest `setup[]` + `healthcheck`

| # | Step | Command | Readiness signal | Timeout |
| --- | ------ | --------- | ------------------ | --------- |

**`sleep N` is not a readiness signal — it is a race condition with a comment.**

Gate on something real: a health endpoint returning 200, a port accepting connections, a migration completing, a topic being created. Bound the wait, and fail loudly when the bound is hit. A harness that proceeds against a half-started environment produces exactly the failures that get misread as product bugs.

---

## 5. Data → manifest `reset[]` + `seed[]`

**Isolation model:** ephemeral-everything | fresh-data-shared-services | namespaced-shared

| Model | Strength | Cost |
| ------- | ---------- | ------ |
| Ephemeral everything | Strongest | Slowest |
| Fresh data, shared services | Usually the right trade | Requires a reliable reset |
| Namespaced in a shared env | Weakest — leaks read as flake | Only when the others are impossible |

**Never test against an environment someone else is using.** A suite that intermittently fails because a colleague was clicking around teaches the team to ignore red.

**Schema / migrations:** <!-- how the store reaches the expected shape -->
**Seed set:** <!-- what data exists before scenarios run -->
**Reset between runs:** <!-- exact mechanism -->

---

## 6. Determinism

| Source of nondeterminism | Control | Seam |
| -------------------------- | --------- | ------ |
| Time / clock | | |
| Random / ID generation | | |
| External network calls | | |
| Concurrency / ordering | | |
| Rollout percentage / sampling | | |

If a test can pass or fail depending on the wall clock, it will eventually do both.

---

## 7. Secrets and config → manifest `required_env` + `environment`

| Variable | Source | Notes |
| ---------- | -------- | ------- |

**No real credentials, ever.** List what must be a test-only value, and where it comes from. If a real secret is genuinely required, that is a `human_action` checkpoint — not something the harness provisions for itself.

---

## 8. Observability access

How the harness reads each service's logs, so log observation points are actually assertable:

| Service | Log source | Access method | Structured? |
| --------- | ------------ | --------------- | ------------- |

A scenario cannot assert a log line the harness has no way to read. If a service's logs are unreachable, say so here — that turns a silently-skipped assertion into a visible gap.

---

## 9. Teardown → manifest `cleanup[]`

| # | Step | Command | Verification |
| --- | ------ | --------- | -------------- |

**Teardown must verify itself.** "Ran `docker compose down`" is not evidence; "`docker ps` shows nothing from this run" is.

A run that leaves orphaned containers, databases, or cloud resources is a passing run **plus a leak** — and a suite that leaks will eventually make its own machine unable to run it.

**Leak check:** <!-- the exact command that proves nothing survived -->
**Flag restoration:** <!-- any flag or setting flipped in §2 must be restored, especially global-scope ones -->

---

## 10. Re-runnability

**Proven by running twice back-to-back with no manual cleanup between runs.**

| Check | Result |
| ------- | -------- |
| Second run passes | |
| No port collisions | |
| No leftover fixtures | |
| Flags still in required state | |

State collisions and stale state hide behind a single run. One run proves nothing about the second.

---

## 11. Blockers and open decisions

| # | Item | Owner | Blocks | Resolved? |
| --- | ------ | ------- | -------- | ----------- |

Anything preventing the environment from being built, including work owned by another team. **An unresolved blocking item stops the harness build** — do not build against an unresolved contradiction.

### Owner is a classification, and it decides who waits

| Owner | Meaning | Who unblocks it |
| ------- | --------- | ----------------- |
| `human` | Only a person can supply it — a credential, an account, an approval, a provisioned tenant | The user, and the harness build waits |
| `harness` | Mechanical: an install, a version-manager pin, a checkout fast-forward **(only on an answered currency gate — see `qa-harness-builder`'s no-unasked-pull rule, which binds in either mode)**, a preflight check | The harness build itself, at build time |
| `external` | Owned by another team or a deployed system; not resolvable locally at all | Nobody here — record it, scope around it |
| `harness decision` | A choice the harness must make and then state, because no source answers it | The builder, who must name which behaviour it implemented |

**Audit this column before finalising, and downgrade what you can.** The instinct is to mark everything `human` because it is unresolved right now, and that instinct is expensive: it hands the user a list of five prerequisites when two of them were a `nvm install` and a file that already existed on disk. **Every `human`-owned blocker carries a `How to acquire` recipe**, exactly as §3 requires — the two lists describe the same items at different stages and must not disagree. A `human` blocker with no recipe is an unfinished blocker. Measure before you claim. A blocker that turns out to be present, installable, or checkable is not a blocker — it is a build step.

Close the section by naming which items are **genuinely un-closable by the harness**. That number is the real ask.

### Degradation — what the suite still proves when a blocker stays open

| Unresolved blocker | What still runs | What is lost | Must the run report say so? |
| -------------------- | ----------------- | -------------- | ----------------------------- |
| <!-- B-n --> | <!-- scenarios / tiers that survive --> | <!-- scenarios BLOCKED, and roughly what share of the plan --> | yes |

**Every loss is stated in the run report, never absorbed.** A suite that quietly drops 60% of its scenarios and reports PASS is worse than one that fails, because it manufactures confidence. Where a degraded path changes what an assertion *means* — an identity the harness supplies rather than one the pipeline resolved, a stub standing in for a service — say that too: the scenario may still run, but it is no longer measuring the same thing.

If nothing can be provisioned at all, set `ENV_MODE: manual_instructions`, document what a human must supply, and stop at a `human_action` checkpoint — do not pretend to self-provision. An environment that half-came-up produces failures that look like product bugs, and that is exactly how a team learns to distrust its own suite.

---

## 12. Real time cost

**State what a full run actually costs in wall-clock, before anyone builds it.**

| Item | Cost | Reducible? |
| ------ | ------ | ------------ |
| Full bring-up | | |
| Slowest scenario family, and why | | |
| Full-suite wall clock | | |

**A clock shim moves thresholds; it does not move ticks.** Patching `Date.now` / the `Date` constructor makes age comparisons cross their thresholds instantly — and leaves `setInterval` and `setTimeout` exactly where they were. Advancing virtual time does not cause a tick; only real elapsed time does. So for every timer on the path, record separately whether its *rate* is controllable (an env var, a config floor) or fixed. A fixed 15-minute sweep interval costs 15 real minutes per scenario that waits on it, clock shim or not.

Patching the timer wheel as well is usually the wrong trade: it decouples virtual time from the event loop and makes bounded re-checks and watchdogs fire in orderings the product never produces — which turns the shim from an observation aid into a source of fiction.

Say the cost here rather than letting the harness build discover it.
