# cc10x v12.9.1 Remediation: Design

Status: design for the PLAN workflow. Implementation not started.
Baseline: v12.9.1, HEAD 891acf0, Claude Code 2.1.292.
Source: two read-only audits run 2026-10-06. Seven agents audited cc10x internally (router, agents, hooks/tools, docs layer, root surface, skills, in-flight work). Six agents compared cc10x to the official Claude Code docs (plugins, skills, subagents, hooks, settings/memory/tasks, prompting guidance). Reports are not committed; finding IDs below are the stable handles.

## Purpose

Remove every verified inconsistency between cc10x's code, its prompts, its docs, and the Claude Code platform it runs on, so later improvements start from a base where the docs describe the product and the validators can tell when they stop doing so.

## Users

The cc10x maintainer (one writer at a time, solo), and downstream users who install the plugin.

## Success criteria

1. Every finding below is fixed, deliberately deferred with a recorded reason, or rejected with evidence.
2. The release gate passes at the final revision: `harness_audit`, `doc_consistency_check`, `prompt_clause_assertions`, `workflow_replay_check` (all `python3 plugins/cc10x/tools/*.py`), `python3 -m pytest plugins/cc10x/scripts` (where pytest is available), the three script-style suites run explicitly (`test_cc10x_qa_phase_invariants.py`, `test_cc10x_review_package.py`, `test_cc10x_token_usage_report.py`), and `claude plugin validate plugins/cc10x`.
3. New checks make the fixed classes of defect fail loudly: a preloaded skill with `disable-model-invocation`, stale counts in public docs, a hook that cannot start, a doc registry that names a nonexistent path.
4. `agent-common` demonstrably reaches agents (empirical check, not a string check).

## Constraints

- One release (decision 1). Proposed version v12.10.0; all version surfaces bumped together per the gate notes (plugin.json, marketplace.json three spots, README three refs, CHANGELOG, status line in five registries).
- Respect the router's own gates; this plan runs through its PLAN workflow and is fresh-reviewed.
- Prompt, registry and hook changes classified per `docs/prompt-change-checklist.md`.
- Never run `tools/worldclass_benchmark.py` as a gate (it writes gitignored files).
- Deletes of files are performed by the user (auto-mode classifier blocks `rm`); the plan proposes them, it does not execute them.
- No destructive git, no pushes, no commits without the user's explicit go-ahead.

## Out of scope

- New features. This is alignment and cleanup only.
- Executing the router split before the behavioral eval passes (decision 4).
- Backfilling git tags for releases 12.1 through 12.8.2.
- Changing the model-tier policy for any gating agent.

## Decisions (user-made)

1. Ship as one big release.
2. Docs: rewrite the living ones, archive the historical ones with a banner and stop validators requiring them.
3. Router split: build the behavioral eval first; the split phase exists in the plan but executes only after the eval passes on the unsplit router.
4. Python: user asked for "the latest version, perfectly adjusted, and if there is an error ask the agent to update" and asked what I think. Proposed and taken as the working assumption, open to veto at plan review: target latest Python (3.13 tested), keep every hook 3.9-safe with `from __future__ import annotations`, and add a stdlib-only SessionStart health check that tells the agent to tell the user to upgrade Python when a hook cannot start.

## Assumptions recorded (not yet user-approved; flagged for plan review)

- A1. Task tools are optional. This session ran the router in its inline fallback because Sonnet 5.5 has no Task tools by default (`CLAUDE_CODE_ENABLE_TODO_TOOLS=1` opts in). Direction: the workflow artifact is the source of truth, the router tolerates absent Task tools, the env var is documented as recommended, and write agents are not told to depend on `TaskUpdate`.
- A2. The 16 untracked `docs/plans/` files: commit `design-v2` and the Sol review after redacting local paths (a published commit cites design-v2); the remaining reviews and integrity prompts are archived or deleted by the user; flip the v12.1 plan to "done".
- A3. The code-review confidence floor (>=80) is a decision at a phase gate: the current guidance says report everything with a confidence tag and filter downstream. Default: leave as is until the user decides.
- A4. `doc-syncer` stays on `model: haiku` (valid per the docs); add an eval before changing it.
- A5. `worldclass_benchmark.py` is dead tooling: propose deletion (user-run) rather than repairing 7 stale rules.
- A6. Researcher agents: add explicit `mcp__*` entries to their `tools:` lists where the prompts rely on MCP, rather than dropping the MCP lanes.

## Finding catalog

Severity H/M/L. Status V = verified by reading/running; I = inferred; D = from official docs only. IDs are stable handles for the plan.

### A. Agent delivery and contracts

- A1 [H,V] `agent-common` sets `disable-model-invocation: true`, so the 13 agents that preload it never receive it (docs forbid it; debug log shows "not found"; empirically confirmed, and `user-invocable: false` fixes it). Lost: memory-ownership law, SKILL_HINTS rule, contract envelope, single-final-response rule, shell safety, untrusted-input handling. Prompt-clause tests only check the text exists.
- A2 [M,D] `tools:` allowlist excludes MCP tools; `researcher` and `qa-researcher` advertise Bright Data/Octocode/Jira/Confluence use with no `mcp__*` entry.
- A3 [H,V] Task tools unavailable by default on this model; router, TaskCompleted hook and seven agents (`TaskUpdate`) assume them; background subagents also strip them. No doc mentions the opt-in or `CLAUDE_CODE_TASK_LIST_ID`.
- A4 [L,V/D] `color: teal` undocumented; router claims the model cannot be set per dispatch (docs: per-invocation `model` exists); `TaskOutput` deprecated; "subagents cannot spawn" is wrong (they can, three layers deep); router never sets `run_in_background` but interactive sessions run subagents in the background; no agent sets `omitClaudeMd`, so agents load the CLAUDE.md that says to invoke the router.
- A5 [M,V] Contract/path conflicts: planner told to write only under `docs/plans` but QA routes tell it to write under `.cc10x/`; `AMENDED_FILES`, `STALE_SWEEP`, `RECONCILIATION_RERUN` required by the pass-2 gate but absent from any agent contract; code-reviewer zero-finding gate (1 citation, confidence 70) vs router bounce (<3 citations) vs APPROVE needs >=80; doc-syncer told to delete legacy ADRs but has no delete path; triage-agent "read-only" but told to check out PRs and write `.out-of-scope/`, hard-codes `BLOCKING: false`; qa-researcher forbids `mkdir` while Memory First requires it; integration-verifier tamper check uses `git diff HEAD` instead of the recorded BASE; qa-executor and qa-harness-builder hold TaskUpdate but are never told to call it, and qa-executor must fill a report in place without Edit; plan-gap-reviewer says "no YAML block" then emits one; bug-investigator requires `TDD_RED_EXIT=1` while text says any non-zero.
- A6 [M,V] Frontmatter preloads contradict the router's "hints only" law (planner preloads architecture; code-reviewer/triage-agent preload codebase-hygiene; code-reviewer/failure-hunter preload code-review incl. receiving-review mode; researcher preloads mcp-cli).
- A7 [L,V] Boilerplate drift between agents (SKILL_HINTS text, Test Process Discipline in three copies); `agent-common` "Bash read-only" conflicts with test runners/docker/mkdir/open in several agents; `results.git_base_sha` referenced without telling agents to read the artifact.
- A8 [M,I/D] Contract parsing: `CONTRACT {` line-1 envelope is a cc10x convention; with `SubagentHandback` (Claude Code 2.1.271+) the final message is not the report, so the SubagentStop contract check logs false `contract_missing`.

### B. Router consistency

- B1 [H,V] REM-FIX gate (`COVERING_TESTS`, `TEST_COMMAND`, `TEST_OUTPUT`, `FINDING_DISPUTED`/`DISPUTE_UPHELD`) has no producer: no agent, skill or contract table names these fields; no REM-FIX `TaskCreate` template.
- B2 [H/M,V] TRIAGE and CODEBASE-HEALTH workflow references are not pointed to by name from `SKILL.md`; neither graph has a Memory Update task; hydration prefixes omit both.
- B3 [M,V/I] Multi-phase BUILD has no iteration rule (next-phase graph creation; Memory Update once per workflow; memory could finalize after phase 1).
- B4 [M,V] Precedence stated three ways: "lower number wins" vs QA (5) beating REVIEW (3) vs ORIENT (4) preferred over REVIEW (3); `eval-01` teaches the retired first-keyword rule and "priority-7 default" (it is 8).
- B5 [M,V] Entry condition: repo CLAUDE.md says opt out only on exact phrases but also that a trivial one-line edit need not route.
- B6 [M,V] Circuit breaker has four phrasings (before 3rd cycle / at 3rd / after 3rd REM-FIX completes / before 4th); counts created tasks in one place and completed in another; also documented "hook-enforced" while `taskMetadata` ships as audit.
- B7 [M,V] Contract parsing direction inverted vs agents (envelope primary for read-only agents vs STATUS in YAML); required-field tables lack rows for reviewers, verifier, triage-agent, architecture-scanner; list unused `IMPLEMENTATIONS_FOUND`; omit planner's `PLAN_REVISION`/`LAST_REVIEWED_REVISION`.
- B8 [M,V] Schema mismatches: `normalized_phases` field names differ between policy reference and `build-workflow.md`; `plan_trust_gate` defined twice and cites a `plan_trust` anchor that exists nowhere; `DIFF_DRIVEN_DOCS: skip` read from `activeContext.md` by the router but documented in CLAUDE.md by `diff-driven-docs`; `verification_rigor` pre-filled `"standard"` so the "must be explicit" check cannot fire; `scope:` enum violated by DEBUG fan-out; `convergence_state` used with five values and no defined set.
- B9 [M,V] Dangling references: `qa-workflow.md` cites ADR-1/2/4 and "RFC section 6c/6d" (docs/adr has 0001 and 0002 only; 0002 is about TRIAGE); `evals/README.md` names `cc10x_doc_consistency_check.py`; "section 13" should be 12; "section 2a permits pending" should be 6; ORIENT names Octocode tools no agent has.
- B10 [L,V] Dead or unenforced: `[BUILD-START]`/`[PLAN-START]` markers never written or read; REVIEW re-review branch unreachable; "legacy agent-created remediation" dead; spike `SKILL_HINTS` unreachable; six policy event types never emitted and seven emitted ones unlisted; "run inline verification" undefined.
- B11 [M,V] `${CLAUDE_PLUGIN_ROOT}` is used 10 times in `references/*.md` where the docs say substitution applies only to `SKILL.md` body, agent bodies and `allowed-tools`. Needs a runtime test before fixing.
- B12 [M,V] `plan-review-gate` blocks on content the planner is never told to write ("Durable Decisions", phase "enables" statements, a "Differences from agreement" plan section).
- B13 [L,V/D] Router description: imperative, "CRITICAL: Route and execute immediately", generic trigger verbs (add, write, create, update, change) over-trigger risk. `update`/`research`/`cc10x` are listed as router keywords but there is no hand-off to `cc10x-guide` or `update`.
- B14 [M,I] Hooks key on the newest-mtime artifact while the router says to scope by `wf:`; `phase_exit_gate` has no hook enforcement.

### C. Hooks and enforcement

- C1 [M,V] Every hook crashes on Python 3.9 (`Path | None`, no `__future__` import; also `cc10x_git_guard.py:90`, `cc10x_posttooluse_artifact_guard.py:46`); non-0/2 exits fail open; no stated minimum Python.
- C2 [M,D/V] PostToolUse exit 2 cannot undo the write; code, hooks README and policy say "rejects"/"blocks". The malformed artifact stays on disk.
- C3 [L,V] Event logger reads undocumented fields (`instructions_hash`, `instruction_count`, `stop_hook_active` for StopFailure) so log values are always empty; TaskCompleted guard reads undocumented `created_at`; its stderr warnings at exit 0 are never seen by the model; event_logger docstring names a wrong log file; postcompact logger can write `None.events.jsonl`.
- C4 [M,V] `hook-mode.json` ships inside the plugin cache (user edits lost on update); any value other than the literal "block" is audit; a missing/corrupt file silently downgrades `artifactIntegrity` to audit.
- C5 [L,V] Git guard gaps: allows `git clean --force`, `git checkout -f`, `git checkout HEAD -- .`, `git restore -- .`, `git branch --delete --force`, `git stash clear`; false-positives on any text containing the literal push command; approval token is a file the model writes itself.
- C6 [L,D/V] Hook coverage: PostToolUse `Edit|Write` misses artifacts written through Bash; `NotebookRead` is not a documented tool; SessionStart omits `clear` and `fork`; guards match `Bash` only (not PowerShell); hooks resolve `.cc10x` from `CLAUDE_PROJECT_DIR`, which stays put in a worktree while the router uses relative `.cc10x/` (I).
- C7 [M,V] Docs drift on hooks: hooks README says "only two enforcement points" and omits the QA isolation guard; root README has a 4-hook section next to a 10-row table; `cc10x-guide` says memory-write hooks "enforce" while they ship as audit; `harness_audit` only catches the phrase "ships four".
- C8 [L,V] Validator weaknesses: `harness_audit.py:232-248` has an empty-string entry that cannot fail and does not assert the git/QA guards are registered; `yaml_alternatives_parse` passes silently when PyYAML is missing.
- C9 [M,V] Test gaps: no tests for the memory-task completion validator, posttool reasons (missing-event-log, missing-updated-at, stale-artifact-write), the branch-delete token, `phase_brief.py`; QA route has only string invariants (no replay fixtures); `seam_eval.py` is a text-grep not a behavioral test; fixtures use `"N/A"` for `convergence_state` against an undefined enum.
- C10 [M,V] The full release-gate list exists only in the maintainer's memory file; `prompt_clause_assertions.py` and the three script-style suites appear in no repo doc; plain pytest is vacuous for 3 of 4 test files; pytest is not installed in the default python3.
- C11 [L,V] `tools/worldclass_benchmark.py` DeltaRules point at nonexistent `scripts/cc10x_*` paths (2 hard, 7 more stale needles); cosmetic `cc10x_` prefixes remain in tool usage strings.
- C12 [L,V] F-1 from the last release: no QA row or amendment-lane anchors in `prompt_clause_assertions.py`; QA invariants not registered in `router-invariants.md`.

### D. Docs layer and public surface

- D1 [H,V] `prompt-surface-inventory.md`: 16 of 25 entries point at nonexistent files; omits 8 agents and 19 of 22 skills; coupled to `harness_audit.py:505-510` (passes by prefix-matching deleted names).
- D2 [H,V] `agent-contract-registry.md`: phantom agents (web-researcher, github-researcher, silent-failure-hunter), no rows for six real agents, key `bf`/`cr` mismatch, v11 header, dead `~/Dev/cc10x_v5` paths.
- D3 [H,V] `cc10x-orchestration-bible.md` describes 9 agents (three nonexistent), 13 old-name skills, a 4-row routing tree, two loop caps, and claims to be the source of truth. `cc10x-orchestration-logic-analysis.md` claims "SYNCED TO LIVE PROMPTS" but describes 4 workflows and 4 hooks.
- D4 [H,V] `router-invariants.md`: banner says v11.0.0; INV-001/013/017/018/026 stale; no invariants for QA, ORIENT, the seam gate, the git guard. `prompt-invariants.md` lacks PINVs for new agents.
- D5 [M,V] Gate lists in `cc10x-orchestration-safety.md`, `prompt-change-checklist.md`, `EVAL-STANDARD.md` are incomplete and conflict; benchmark-note requirement conflicts with `.gitignore` ignoring new `docs/benchmarks/*`.
- D6 [M,V] Historical docs with no marker: `2026-06-17-HANDOFF.md` (says v11.0.0, "campaign not started"), harmony release plan, latency-reduction note, diff-driven-docs plan (shipped), upstream-steal-list (mostly actioned), five March benchmarks, ADR 0002 (TRIAGE=5; now QA=5), `v12-keep-inventory.md`, v12 loop-engine plan (targets missed: 14 agents vs 7, 22 skills vs <=14, router ~68KB vs <=8K tokens).
- D7 [M,V] README: "The 4 Workflows" and diagrams show 4 of 8; agent list shows 9 of 14; file tree omits failure-hunter, qa agents, `qa-workflow.md`, the QA isolation guard script, `templates/`; lists nonexistent `agents/references/silent-failure-red-flags.md`; "4 hooks"; BUILD diagram shows old "code-generation skill"/"silent-failure" hunter; release-history header says v5.3 to v12.9.1 but table ends at v10.1.20; footer tagline differs from hero; no update instructions; manual install path `~/.claude/plugins/cc10x` undocumented; `/plugins enable` vs `/plugin`; hero phrase "Stop chasing better models" is forbidden by the keynote test's own rule.
- D8 [M,V] `cc10x-guide`: says 11 agents/20 skills (14/21); both "8 workflows" and a "4 workflows" section; implies memory-write hooks block.
- D9 [M,V] Explorer HTMLs and playgrounds linked from README show an old architecture (v6.0.9, six agents, `silent-failure-hunter`, `session-memory`); no QA, triage, doc-syncer, plan-gap-reviewer.
- D10 [M,V] Root `CLAUDE.md` lines 14-40: placeholder "Complementary Skills" gate naming skills that do not exist (`mongodb-agent-skills`, `react-best-practices`, `vercel-agent-skills`); `[CC10x]|entry:` is not a documented directive; the plugin-root CLAUDE.md is not loaded.
- D11 [L,V] `plugin.json` "73% leaner than v11" no longer holds (6,733 agent+SKILL lines vs 4,759 at 12.1.0); marketplace description/keywords differ from plugin.json and omit QA; `version` set in both manifests (docs: do not); auto-update off by default for third-party marketplaces and not stated.
- D12 [M,V] `update` skill: treats `cache/cc10x/cc10x` as the plugin root (it holds version directories), hard-codes `$HOME/.claude`, hand-edits `installed_plugins.json` assuming one entry, bypasses `claude plugin marketplace update` / `claude plugin update cc10x@cc10x` / `/reload-plugins`; following it literally leaves every installPath dangling.
- D13 [M,V/D] Settings template and README: `Write(.cc10x/*)` rules are inert (docs: use `Edit(...)`); `Edit(.cc10x/*)` may not cover nested files (`Edit(.cc10x/**)` is the documented-safe form, untested); `Bash(python3:*)` very broad; no mention of `CLAUDE_CODE_ENABLE_TODO_TOOLS` or `CLAUDE_CODE_TASK_LIST_ID`; hard-coded `~/.claude` paths vs `CLAUDE_CONFIG_DIR`/`CLAUDE_CODE_PLUGIN_CACHE_DIR`.
- D14 [L,V] Housekeeping: `DESIGN.md`/`PRODUCT.md` describe the keynote deck, not the plugin; `keynote copy*.html` are stray gitignored drafts; stray `plugins/cc10x/.cc10x/cc10x-hook-events.log`; `cc10x` never tells users to gitignore `.cc10x/`; relation to Claude Code auto-memory undocumented; the revitalization plan is ignored by `*-PLAN.md` yet cited by CHANGELOG and HANDOFF; 48 generated benchmark files; 07-30 Anthropic-comparison open items live only in a gitignored README.
- D15 [H,V] Root cause of D1-D9 persisting: `harness_audit.py:457-533` checks only that docs exist, contain a title string and the literal current version. Releases append a banner; bodies rot.

### E. Skills

- E1 [M,V] Vocabulary drift: code-reviewer uses MAJOR/MINOR (undefined in `code-review`); `code-review` says "CLEAN" but reviewer verdicts are APPROVE/CHANGES_REQUESTED; "16 named smells" vs "12 named smells" in the same loaded agent; confidence 70 vs >=80; hygiene "Speculative, low confidence" routed through the >=80 contract.
- E2 [M,V] `building/SKILL.md:171` exception fabricates `TDD_RED_EXIT`/`TDD_GREEN_EXIT` with a manual check, contradicting its own "RED is never a bare exit code" and the contract.
- E3 [M,V] `building` reference tells the builder to read `qa-strategy` (router forbids); `qa-strategy` is DRAFT with PLACEHOLDERs and four referenced `references/*.md` files that do not exist; `codebase-design` claims building and planning point to it (they do not) and "seam" is defined differently in `building:63` vs `codebase-design:35`.
- E4 [M,V] `memory-and-handoff` session mode has no loader; five-outcome compounding loop and "consolidate at 3+" not implemented in the router; surface list omits `.cc10x/qa/`, `state/`.
- E5 [L,V] `mcp-cli`: generic description invites auto-fire; instructs an unpinned `git clone` plus `go build` into `~/.local/bin`.
- E6 [L,V] `cc10x-guide` and other skills with `allowed-tools: Read`: per docs it grants permission, does not restrict; "never writes" is prose only.
- E7 [L,V] Dangling/odd: `agent-common/references/silent-failure-red-flags.md` read by nothing (failure-hunter has a newer copy); `research` branches on `[Web phase unavailable]`, which no agent emits; `git bisect run CI=true npm test` fails with exit 127; `templates/coverage-thresholds.json` uses a repo-relative install path; 733 lines of evals ship inside `skills/` loaded by nothing; one duplicated sentence in `architecture/SKILL.md` lines 58 and 143.
- E8 [M,V] Size and shape: router `SKILL.md` 781 lines (docs: <500; after compaction only the first 5,000 tokens of an invoked skill are re-injected); 8 long references lack a table of contents; reference chains are nested more than one level (debug-workflow to qa-workflow to remediation-and-research); a BUILD reads 130-155 KB and QA 180-205 KB.
- E9 [M,V] Skill-only dedupe candidates ~230 lines; agent-restated-skill dedupe ~350 lines (component-builder, integration-verifier, bug-investigator, failure-hunter restate preloaded skills); `qa-strategy` split saves 65-90 lines for executor and plan-gap-reviewer but PP-38/PP-43 and the router's single-file Read pin the text.
- E10 [L,V] Descriptions: six internal skills name the loading agent rather than a trigger (style drift).
- E11 [L,I] Open prompt-quality items from the 07-19 audit: router prose at `SKILL.md` lines 15, 221-242, 373, 763; code-review >=80 floor (A3); no "propose directions" lever in frontend.

### F. In-flight and hygiene

- F1 [M,V] 16 untracked `docs/plans/` files. 15 contain local paths; commits 01b783c and 67a0486 removed such leaks. `design-v2` is cited by a published commit and is currently untracked (dangling reference). The four `*-router-integrity-review.md` files are reviewer prompts, not results. `v12.1-final-improvements.md` is implemented but says "in-progress".
- F2 [L,V] ADR 0001 says pre-seam fixtures are still accepted; the code now requires them. ADR 0002's route priorities are stale.
- F3 [L,I] `architecture-scanner` temp-dir-only Write is a prompt rule, not path-guarded.
- F4 [L,I] Stale local installs: this session loaded cc10x 12.8.2 prompts (a project-scope 12.8.2 pin at the home directory and one for another project); fixing needs `claude plugin update` by the user, not repo changes.

## Approach chosen

One execution plan with ordered phases, risk-first, each with acceptance criteria and a verification command. The ordering principle: (1) fix what silently breaks behavior today, (2) make validators able to see the problem, (3) fix the router and agent contracts the validators now protect, (4) reset docs against those contracts, (5) eval, then (6) the gated split, (7) release. Parallel work is only proposed for disjoint file sets; one writer per file.

Proposed phase outline (the planner refines):

0. Prep: baseline snapshot of the gate at HEAD, record gate list in a repo doc (C10), decide file moves.
1. Silent-breakage fixes: A1, C1 (+health check), A2, A4, C2 wording, D13, D12, B11 test.
2. Make validators see rot: D15, C8, C12, new checks for A1-class and count drift, C10 gate list, C9 test gaps that protect phase 3.
3. Router and contract consistency: B1-B10, B12-B14, A3, A5-A8, E1-E3, E4.
4. Hooks behavior cleanup: C3-C7, C11 decision.
5. Docs reset: D1-D11, D14, F1-F2, plus archive moves (user-run deletes).
6. Behavioral eval (G): BUILD, TRIAGE, REM-FIX, multi-phase memory finalize, two-workflow resume; QA replay fixtures; seam eval upgrade.
7. Gated router/qa-workflow split plus dedupe (E8, E9): executes only if phase 6 passes on the unsplit router.
8. Release: version bump surfaces, CHANGELOG, full gate, `claude plugin validate`, plugin cache refresh guidance for the user.

## Domain glossary

- Gate: the release gate command list in Success criteria.
- Living doc: a doc a validator or a maintainer relies on as current. Historical doc: records past work; banner, no validators.
- Fail-open hook: a hook whose crash exits non-2 so the guarded action proceeds.

## ADR notes (rejected alternatives)

- Splitting the router first: rejected. The three routing-only evals cannot detect regressions from a split; only string-pin tests exist.
- Requiring Python 3.10+ only: rejected. macOS `/usr/bin/python3` is 3.9.6 and the guard would still fail open.
- Deleting historical docs outright: rejected by the user; archive with banner.
- Repairing `worldclass_benchmark.py`: not chosen; it is dev-only tooling with 9 of 20 rules stale (A5 default: propose deletion).

## Error handling

Each phase ends with its gate. A failing gate halts that phase and routes through remediation; no phase starts on a red gate. Prompt-affecting phases classify per the prompt-change checklist. If a runtime test (B11, A1 re-check) contradicts a finding, the finding is downgraded in the plan, not silently dropped.

## Testing strategy

Verification per phase uses the gate plus targeted checks: a 3.9 smoke run of each hook (`/usr/bin/python3`), a debug-log check that `cc10x:agent-common` is preloaded, a count-drift check across README/guide/plugin.json, a new check that no preloaded skill sets `disable-model-invocation`, and the phase-6 behavioral eval before phase 7.

## Questions resolved

Release shape, Python approach (proposed), docs policy, router split timing. Remaining decisions are listed under Assumptions A1-A6 and are surfaced to the user at plan review.
