# Setup Record: {env_key}

**Environment key:** `{env_key}` · **Mode:** local | compose | testcontainers | cloud_ephemeral | manual_instructions
**Target repo:** `{repo_path}` · **First created:** {iso_ts} · **Last updated:** {iso_ts} (wf:{workflow_uuid})

> **This file records only what was MEASURED. If preflight did not observe it, it does not go in.**
>
> That is the whole discipline, and it is what makes this file different from `env-plan.md`.
> The env plan is a *prediction* written by reading source code — necessary, and systematically
> wrong about environments, because environment facts are not in the code. This file is the
> other half: what the machine actually said when someone asked it.
>
> A prediction that leaks in here turns a record you can trust into a second env-plan, and then
> there are two places for the same fact to go stale. **No section of this file may be filled in
> before a run.** If a heading could be answered from a document, it does not belong here.

**Append-only.** Nothing is ever overwritten or deleted. A fact that stops being true is marked
`superseded` and the new observation is appended beneath it. A record that cannot rewrite its own
history cannot lie about it — and the history is often the interesting part, because a fact that
changed is a fact about the environment drifting under you.

**Scope: the environment, not the feature.** Two features tested against the same topology share
nearly every fact here. One feature tested on a laptop and in CI shares none of them. This file is
keyed by `{env_key}`, lives at `.cc10x/qa/env/{env_key}/setup.md`, is machine-local, and is
deliberately gitignored — it holds this machine's versions, this machine's ports, and this user's
credential paths.

---

## 1. Identity

| Field | Value |
| ------- | ------- |
| `env_key` | <!-- {basename(repo)}-{env_mode} --> |
| Environment mode | |
| Target repo + branch | |
| Host OS / arch | <!-- measured, e.g. `uname -sm` output --> |
| First created | <!-- ISO ts + the workflow that created it --> |
| Last updated | <!-- ISO ts + the most recent workflow to confirm a row --> |
| Workflows that have written here | <!-- append one id per run --> |

---

## 2. Measured facts

One row per fact. **A row missing `How observed` or `Observed output` is invalid and must be
deleted rather than guessed at** — that rule is the only thing standing between this file and a
second env-plan.

| Fact | Volatility | How observed | Observed output | First observed | Last confirmed | Fingerprint | State |
| ------ | ------------ | -------------- | ----------------- | ---------------- | ---------------- | ------------- | ------- |
| <!-- e.g. opengrep on PATH --> | stable \| volatile \| derived | <!-- the exact command --> | <!-- verbatim, trimmed --> | wf:… | wf:… @ ts | <!-- derived rows only --> | current \| superseded \| unverified |
| branch currency — <!-- repo name --> | volatile | `git rev-parse --abbrev-ref HEAD; git rev-parse --short HEAD; git rev-list --count HEAD..{default_branch}; git status --porcelain` | <!-- branch, sha, commits_behind, dirty --> | wf:… | wf:… @ ts | — | current \| superseded \| unverified |

**One `branch currency` row per repo in the topology, and it is `volatile` — not `stable`.**
`commits_behind` is true only for an instant, because the remote moves. By this table's own rule a
`volatile` row is **always re-checked, never trusted from this file**, which is exactly the property
this fact needs: a run that trusts a recorded `commits_behind` is measuring one side of a cross-repo
contract at a revision nobody confirmed. Recording it `stable` would re-create that defect one run
later.

### What each volatility class means, and what preflight does with it

| Class | Meaning | Preflight behaviour on run 2+ |
| ------- | --------- | ------------------------------- |
| `stable` | changes only when a human changes the machine — a binary on `$PATH`, a credential file existing, an installed version | re-run the **cheap existence probe only**, and compare against `Observed output` |
| `volatile` | true only for an instant — a port being free, a service answering, a container running | **always re-checked, never trusted from this file** |
| `derived` | a fact learned the hard way about the product or topology — "the analyzer image has no sshd", "wipe the mount before the DB" | **never re-checked mechanically**; carried forward as a constraint the plan and harness must honour, guarded by `Fingerprint` |

### State transitions

| From | Trigger | To | Consequence |
| ------ | --------- | ---- | ------------- |
| `current` (`stable`) | the cheap re-probe disagrees with `Observed output` | `superseded` | append the new observation as a new row; preflight reports `SETUP_RECORD_STALE: true` |
| `current` (`derived`) | `Fingerprint` no longer matches (image digest, lockfile hash, compose-file hash) | `unverified` | **not** `superseded` — we know we cannot vouch for it, not that it is false. The harness must treat that fact as a *prediction* again rather than a measurement |
| `unverified` | re-observed | `current` | new row appended with a fresh fingerprint |

`unverified` and `superseded` are different claims and must not be collapsed. "This was true and is
now false" and "this may still be true and nobody has checked" lead to different decisions.

---

## 3. Human prerequisites, measured

Only items preflight **confirmed missing or present**. Not the env plan's predicted blocker list —
that list is written from source and reliably over-reports. Measuring first is what turns a list of
twelve into the one or two things a human actually has to do.

| Item | Why it is needed | How to acquire | Supplied? | Where it lives | Class |
| ------ | ------------------ | ---------------- | ----------- | ---------------- | ------- |
| | <!-- what breaks without it --> | <!-- the actual recipe: the command, the secret id, the region, the page --> | yes \| no | <!-- path or store, never the value itself --> | `missing-input` |

**`Class` is fixed at `missing-input` for every row in this section**, because that is what this
section structurally *is*: a thing the environment needs and does not have. A row that wants a
different `FAILURE_CLASS` is not a stricter row — it is a row in the wrong section. `wrong-guess`
belongs in section 4; `defect` is a product finding and belongs in the report, never here. The column
exists so that misfiling is greppable and countable instead of invisible.

**`How to acquire` is mandatory for every row.** A prerequisite recorded without a recipe reproduces
the exact failure this file exists to prevent: a run that stops at a missing credential and cannot
say how to get one. If the recipe is genuinely unknown, write what was tried and who would know.

**Never record a secret's value here.** Record where it lives. This file is machine-local, not
encrypted, and a path is enough for the next run.

---

## 4. Corrections to `env-plan.md`

Where the prediction and the measurement disagree. Each row is a finding for the env plan, not just
a note to self — these are what make the next plan better than this one.

| What `env-plan.md` predicted | What was measured | Which env-plan section now disagrees | Routed? | Class |
| ------------------------------ | ------------------- | -------------------------------------- | --------- | ------- |

**`Class` is fixed at `wrong-guess` for every row in this section.** A prediction that the
measurement contradicted is the definition of `wrong-guess`. A row that wants `missing-input` is
describing an absent prerequisite and belongs in section 3; a row that wants `defect` is describing
the product, not the env plan, and belongs in the report. Same rule, same reason: a misfiled row
should be visible, not merely wrong.

---

## 5. Superseded rows

The append-only history. Moved here verbatim when a row's `State` becomes `superseded`, with the
observation that replaced it.

| Fact | Was | Became | When | Detected by |
| ------ | ----- | -------- | ------ | ------------- |

---

## 6. What this record does NOT contain

Stated so a reader does not mistake absence for a clean bill of health.

- Anything preflight did not run. Preflight stops at **T4** and never boots a service, so no fact
  here was learned from a running topology.
- Anything about the feature under test. That is `feature-map.md`.
- Any recommendation, plan, or intended state. That is `env-plan.md`.
