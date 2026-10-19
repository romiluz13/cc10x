# Design proposal: project-declared advisory tasks in cc10x task graphs

Status: **proposal, not decided.** Issue: [#90](https://github.com/romiluz13/cc10x/issues/90). Baseline: `main` after PRs #94 and #95 (cc10x 12.10.0 + Unreleased).

Nothing here is implemented. This document lays out the options and recommends one, so the maintainer can decide and the work can then be ticketed.

## Problem

A project cannot add a task to a cc10x task graph. Three things hold the graphs closed:

1. The router applies each route's `### … task graph` block **verbatim** (`skills/cc10x-router/SKILL.md` §6, for BUILD, DEBUG, REVIEW, PLAN and QA).
2. The §7 dispatcher maps every `phase:` label to a `cc10x:*` agent, and the §3 `phase:` enum is closed. There is no row for a project agent.
3. The one project-side seam the router reads, `.cc10x/patterns.md ## Project SKILL_HINTS`, can only add a **skill** to an agent that already runs. It cannot add a **task**.

So a project that wants one more read-only reviewer has to patch the installed plugin. The patch is unrecorded, lost on update, and fails the plugin's own byte-anchored self-checks (`tools/prompt_clause_assertions.py`).

The issue's example is a concrete, reasonable one: an over-engineering reviewer (`ponytail-review`) placed beside `code-reviewer` and `failure-hunter` at `build-review`, beside `plan-gap-reviewer` at `plan-review-gap-1`, and beside `review-audit`.

## Constraints any design must keep

These come from the router's current contract and are not up for negotiation in v1:

- **Append only.** An extension never removes, reorders or re-blocks a cc10x task. The verbatim graph blocks and their assertions stay byte-identical; the extension step runs *after* the verbatim block is applied.
- **Never gates.** An extension's result never decides `phase_exit_gate`, plan approval, a verdict, or a `kind:remfix` task. Its findings can only reach `deferred_findings`, which BUILD-DONE already surfaces before the finishing menu (`references/build-workflow.md`, step 1a). A task that cannot block cannot deadlock a workflow.
- **Degrades quietly.** A missing agent, a missing skill, a malformed file or a failed dispatch logs one event and the workflow continues as if the extension were absent.
- **No runtime enforcement exists.** Since PR #94, cc10x ships no PreToolUse guard. Any "read-only" promise about an extension agent is a prompt rule plus a static check of its frontmatter, not a mechanism.

## Options

### A. A committed JSON file the router only reads — recommended

```json
{
  "version": 1,
  "advisory_tasks": [
    {
      "id": "ponytail",
      "agent": "ponytail-reviewer",
      "attach_to": ["build-review", "plan-review-gap-1", "review-audit"],
      "skills": ["ponytail:ponytail-review"]
    }
  ]
}
```

- **Location: `.claude/cc10x-extensions.json`.** The file sits next to `.claude/agents/`, where the extension agent itself lives, and projects already commit `.claude/`. `.cc10x/` is the wrong home: it is local orchestration state that most projects gitignore, which is exactly what the issue reports. cc10x never writes this file, so it does not reintroduce the sensitive-file prompts that moved state out of `.claude/` (#24).
- **JSON, not YAML.** cc10x's validators are stdlib Python. JSON lets `tools/` validate the file and lets a replay fixture exercise it without adding a dependency.
- **No `blocking` field.** v1 has no blocking mode, so the schema has no key that suggests one. Adding `blocking` later is a schema version bump with its own design.
- **`attach_to`, not `phases`.** The word "phase" already means two things in cc10x (the `phase:` task label and a plan phase tracked by `phase_cursor`), as the issue points out. `attach_to` names the `phase:` label of an existing read-only task.

### B. A `## Project Advisory Tasks` section in `patterns.md` (the issue's smaller alternative)

Smallest change, since the router already reads the file. Rejected as the primary design for two reasons: cc10x writes to `patterns.md` at memory finalization, so configuration and memory share one file; and `.cc10x/` is usually gitignored, so the configuration would not be shared with the team. It stays a fallback if the maintainer wants no new file.

### C. Do nothing; document patching

Keeps the contract closed. It leaves users with the unrecorded per-machine patch the issue describes, and they cannot verify that patch with the plugin's own tools.

## Mechanics of option A

1. **Load.** During §5 shared preparation, the router reads `.claude/cc10x-extensions.json` if it exists, validates it against the v1 schema, and records the accepted entries in the workflow artifact (`extensions.accepted`, `extensions.skipped` with reasons). The file is read once per workflow; resume uses the recorded copy, not a re-read.
2. **Attach points (v1).** Only the existing read-only review points: `build-review` (BUILD full graph only, never the trivial reduced graph), `plan-review-gap-1` (PLAN), `review-audit` (REVIEW). DEBUG and QA are out of scope for v1, because their read-only points carry route-specific contracts.
3. **Task shape.** One new label, `phase:ext-advisory`, with `kind:agent`, `origin:router`, `scope:{attach_to label}` and `reason:ext:{id}`. That is one enum addition to §3, not one per extension.
4. **Wiring.** Each extension task gets the **same blockers** as the task at its attach point, and nothing waits on it except the Memory Update task. That one edge is what keeps its findings from evaporating: BUILD-DONE finishing runs only once Memory Update is otherwise ready (`references/build-workflow.md`, BUILD-DONE finishing), so the findings are in `deferred_findings` before step 1a reads them.
5. **Dispatch.** A new §7 row: `ext-advisory` → the agent named in the entry, by bare name (project `.claude/agents/`) or `plugin:agent`. It is dispatched in the same message as `code-reviewer` and `failure-hunter`, and the existing sequential fallback applies.
6. **Result handling.** Extension agents are not cc10x agents and will not emit the line-1 `CONTRACT` envelope, so the router does **not** parse a `STATUS` from them. It appends each finding to `deferred_findings` as `{source: "ext:{id}", phase_id, finding, severity: "minor"}` and lists them in the merged findings summary under their own heading, outside cross-reviewer agreement promotion.
7. **Read-only check.** Before the first dispatch, the router reads the agent's frontmatter `tools:`. If it grants `Edit`, `Write` or `NotebookEdit`, the router skips the extension and logs why. That is cheap, and it closes the foot-gun the issue names: a write-capable agent changing the tree after review, outside any gate.
8. **Events.** `extension_loaded`, `extension_skipped` (with reason), `extension_dispatched`, `extension_failed`. None of them changes a workflow status.

## What would change in the repo

- Router `SKILL.md`: §3 enum (+`ext-advisory`), §5 load step, §6 one line after each verbatim graph ("then append extension tasks per `references/extensions.md`"), §7 one dispatcher row. Each touches router line budgets that are pinned, so `prompt_clause_assertions.py` gains clauses rather than losing anchors.
- New `references/extensions.md`: the full contract above, in one place.
- `references/workflow-artifact.skeleton.json` and the hook-policy reference: an `extensions` block.
- `tools/`: a stdlib validator for the file, run in `release_gate.py`; a `workflow_replay_check.py` fixture with one advisory task at `build-review`, including a missing-agent skip.
- README and `cc10x-guide`: a short "Extending the task graphs" section, including the `.gitignore` note the issue asks for. With option A that note is moot, since the file is not under `.cc10x/`.

## Decisions for the maintainer

1. **Option A, B or C?** Recommendation: A.
2. **File location.** Recommendation: `.claude/cc10x-extensions.json`. The alternative is `.cc10x/extensions.json` with a documented `.gitignore` exception.
3. **Do extension tasks block Memory Update?** Recommendation: yes, and nothing else. Without the edge, a slow extension's findings can arrive after BUILD-DONE has already triaged `deferred_findings`.
4. **Reject write-capable extension agents, or only warn?** Recommendation: reject (skip and log). The issue argues for not policing; the counterargument is that cc10x no longer has a runtime guard to catch the post-gate write.
5. **v1 attach points.** Recommendation: `build-review`, `plan-review-gap-1`, `review-audit`. DEBUG and QA later, on demand.

## Suggested slices once decided

1. Schema, validator and `references/extensions.md`, with no router wiring. The gate validates a sample file.
2. BUILD `build-review` attach point end to end: load, task, dispatch, `deferred_findings`, events, replay fixture.
3. PLAN and REVIEW attach points.
4. Docs: README, `cc10x-guide`, CHANGELOG.

The issue's author offered a PR. Once decisions 1–5 are settled, slices 1–2 are a good scope to hand them.
