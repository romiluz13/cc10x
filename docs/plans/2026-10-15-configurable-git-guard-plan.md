# Configurable git guard (`gitGuard` hook mode) Plan

## Metadata
- Created: 2026-10-15
- Status: P1-P3 complete, P4 (pre-PR handoff) in progress. Revision 4 (fresh-reviewed@r1; amended after review at r2, r3 and r4).
- PLAN_REVISION: 4
- LAST_REVIEWED_REVISION: 1
- PLANNING_REVIEW_STATUS: revised_after_review
- Verification Rigor: critical_path
- Plan Mode: execution_plan

**Revision 4 — not read whole by a fresh review.** One fresh plan review ran, and it read revision 1. Revision 3 rewrote the plan to describe the built feature, and an amendment check read it. Revision 4 applies that check's findings. The code itself was reviewed separately, through 8 remediation rounds and a final verifier pass.

- Design file: `docs/plans/2026-10-15-configurable-git-guard-design.md` (authoritative for intent; amended to revision 4 alongside this plan).
- Baseline: v12.10.0, HEAD f346ebe. `python3 plugins/cc10x/tools/release_gate.py` ended `RELEASE GATE: OK` (810 pytest passed), and `test_cc10x_guards.py` had 204 tests.

Mode reason: `execution_plan`. The design chose the approach; the plan sequenced it. The deferral rule changed during the build, by user decision, and the ADR below records why.

Rigor reason: `critical_path`. The change edits the only hook that stops destructive git operations. A wrong rule would loosen it silently.

## Human Layer

### What and why
The git guard denies `git push` and `git branch -D` unless the router wrote a single-use token at the BUILD-DONE menu. It denies `reset --hard`, `clean -f`, force-push and the discard forms with no unlock path at all. Users who govern git through Claude Code's permission system had no way to opt out short of patching the plugin cache. This change adds one opt-in key, `gitGuard`, to the existing `hook-mode.json` layering:

- `block` (shipped default): the 12.10.0 behavior, byte for byte. The classifier is unchanged.
- `ask`: a command that is only one plain `git push` produces no hook decision, so Claude Code's permission flow decides. Every other verdict returns `permissionDecision: "ask"`: `branch -D`, the destructive set, and a push in any other command. The guard logs one decision event per verdict.

Nothing changes for anyone who doesn't opt in.

### Agreement Snapshot
- **Goal:** let a user change the git guard from `block` to `ask` through `${CLAUDE_PLUGIN_DATA}/hook-mode.json`, with docs and CHANGELOG updated, ready for an upstream PR to romiluz13/cc10x.
- **Constraints:**
  - Reuse `HOOK_MODE_DEFAULTS` / `resolve_hook_mode` / `load_mode`. No new config file or env var.
  - Allowed values per key: `artifactIntegrity`, `memoryWrites`, `taskMetadata` take `block|audit`; `gitGuard` takes `block|ask`.
  - `classify_git_command` and everything it calls stay exactly as in v12.10.0.
  - Python 3.9 floor. Fail open on a hook crash, as today. A mode-read failure takes the `block` path.
  - Every phase ends with `python3 plugins/cc10x/tools/release_gate.py` green (run with Claude validation, without `--allow-no-claude`).
  - Destructive git test strings live in test files, built with the `git(...)` helper, and never inline in a Bash command, because the live guard scans Bash text.
  - No commit, push or PR without the user's explicit approval.
- **In Scope:**
  - `cc10x_hooklib.py`, `config/hook-mode.json`, `cc10x_git_guard.py` (new constants, `_lone_plain_push`, `_log_classifier_failure`, `main()`, the docstring).
  - `test_cc10x_guards.py`, the PP-39 census comments in `test_cc10x_qa_phase_invariants.py`.
  - The doc surfaces D1-D18 below, and a `CHANGELOG.md` `## [Unreleased]` entry.
- **Out of Scope:** an `off` value; per-operation config; an `audit` alias for `gitGuard`; any change to the classifier's deny set; the token mechanism and the router's token-writing step; the QA isolation guard; a version bump; `docs/history/**` and CHANGELOG entries for 12.10.0 and older.
- **Open Decisions:** none.
- **Decisions answered by the user (2026-10-15), verbatim choice labels:**
  - Value name `ask` over `audit`; plan first.
  - Push remote: "Fork (Recommended)". At P4 the branch goes to the user's fork, and the PR targets `romiluz13/cc10x`. Each step needs its own approval.
  - Plan docs: "Ship, scrubbed (Recommended)".
  - "Prompt for branch -D (Recommended)": only push can defer.
  - "Yes, fix it (Recommended)" (remediation round 4, past the circuit breaker), then "Fix in code + docs (Recommended)" (round 5).
  - "Allow-list defer (Recommended)" (round 6), and "Allow output redirects (Recommended)".
  - "Single-command only (Recommended)" (round 7).
  - "Yes, small fix (Recommended)" (round 8): drop `^` and `~`, then one verifier pass.

### Durable Decisions
Spell these exactly.
- Config key `gitGuard`, values `"block"` (default) and `"ask"`.
- `HOOK_MODE_DEFAULTS["gitGuard"] == "block"`, and `config/hook-mode.json` carries `"gitGuard": "block"` as its last key.
- `HOOK_MODE_VALUES` is a per-key dict: `{"artifactIntegrity": ("block", "audit"), "memoryWrites": ("block", "audit"), "taskMetadata": ("block", "audit"), "gitGuard": ("block", "ask")}`. `resolve_hook_mode` checks `value in HOOK_MODE_VALUES[key]`.
- `pretool_ask(reason: str) -> None`, the same shape as `pretool_deny` with `"permissionDecision": "ask"`.
- Verdict keys (`PRIORITY`, 11, unchanged): `push-force`, `reset-hard`, `clean-force`, `discard-all`, `checkout-force`, `worktree-force`, `stash-clear`, `classifier-error`, `command-too-large`, `push`, `branch-delete`. `APPROVABLE` (token-unlockable in `block` mode) is `push` and `branch-delete`.
- `ASK_MODE_DEFERRED = frozenset({"push"})`. In `ask` mode a verdict defers if and only if `key in ASK_MODE_DEFERRED and _lone_plain_push(command)`.
- `_lone_plain_push(command: str) -> bool` is an allow-list over the whole command, built from `PLAIN_PUSH_FLAGS`, `PLAIN_REDIRECTS`, `PLAIN_REDIRECT_OPS` and `PLAIN_WORD = re.compile(r"^[A-Za-z0-9._/@-]+$")`. The design doc's "Approach chosen" has the full rule.
- `MSG_NOT_LONE_PUSH` replaces the reason for a `push` verdict that does not defer.
- Ask reason text: `f"cc10x git guardrails: {reason} Approve only if intended."`.
- Events:
  - `git_guard_deferred` (decision `defer`) and `git_guard_ask` (decision `ask`); log names `plugin_git_guard_deferred` and `plugin_git_guard_ask`.
  - `git_guard_mode_read_failed` (error class, no decision key).
  - `git_guard_classifier_failed`, whose decision comes from `main()`: `allow` when there is no verdict, `deny` in `block` mode, and no decision key in `ask` mode.
- No third-party boundary changes. Claude Code's handling of "no output, exit 0" and of `permissionDecision: "ask"` was proven live on 2026-10-15.

### ADR: the `ask`-mode deferral rule
**Context:** `ask` must hand routine publishing to Claude Code without letting anything else the guard catches run unprompted. A text hook sees only the command string.

**Decision:** defer only a command whose whole text is one plain `git push` (`_lone_plain_push`). Ask for everything else. Leave the classifier verbatim at v12.10.0, and make the decision in `main()`.

**Rejected Alternatives:**
- `audit` as the value name. On every other key it means "log, never block".
- `ask` for every push. It prompts on pushes the user already allowed.
- A separate `git-guard.json` or env var. A second config surface.
- Defer per verdict key, `push` and `branch-delete` (revision 2). The shipped template's `Bash(git branch:*)` allow rule would auto-approve a deferred `branch -D`.
- A deny-list per verdict key (rounds 4-5): defer unless known-bad forms are present, plus a `push-rewrite` verdict key and a check that every git operation found was a push. It leaked through remote-rewriting pushes (`--mirror`, `--delete`, `:ref`), shell-built arguments, config overrides (`-c`, `--config-env`, `GIT_CONFIG_*`) and sibling commands. Every review round found one more.
- A per-segment allow-list (round 6). It leaked through sibling statements that change what the plain segment does (a `git()` function, an alias line, `git config`, `export`, `cd`), and through the lexer's fallback, where the segments are not the shell's.

**Consequences:**
- `block` mode can't drift, because the classifier is untouched.
- The allow-list errs toward prompting. Harmless forms outside it prompt.
- State outside the command text is invisible (see Honest limits).

### Codebase Reality Check (as built, against f346ebe)
| Surface | Change |
|---------|--------|
| `cc10x_hooklib.py` | `HOOK_MODE_DEFAULTS` + `gitGuard`; `HOOK_MODE_VALUES` per key; `resolve_hook_mode` lookup and docstring; `pretool_ask` after `pretool_deny` |
| `config/hook-mode.json` | + `"gitGuard": "block"` |
| `cc10x_git_guard.py` | import of `load_mode`, `pretool_ask`; new constants after `APPROVABLE` and among the messages; `_lone_plain_push` after `classify_git_command`; `_log_classifier_failure(exc, decision)`; the mode branch in `main()`; docstring. `classify_git_command`, `_scan`, `_floor`, `PRIORITY`, `APPROVABLE`, the existing messages and `consume_approval` are unchanged (no diff hunk inside them; the classifier, `_scan`, `_floor` and `PRIORITY` are also AST-identical to f346ebe) |
| `test_cc10x_guards.py` | 204 → 232 tests; `run_git_guard_in_process` gains `extra_env` and pins its environment; 4 default-mode literals gain `gitGuard` |
| `test_cc10x_qa_phase_invariants.py` | PP-39 census comments updated to the live census (4 mode-aware / 1 unconditional) |

### Doc surface inventory
Line numbers are at f346ebe.

| # | Surface | Phase |
|---|---------|-------|
| D1, D2 | `skills/cc10x-router/references/workflow-artifact-and-hook-policy.md`: the W8 hook-mode paragraph (`- Default mode is audit-only` anchor kept) and the token bullet | P2 (forced by PP-39(b)) |
| D3 | `cc10x_git_guard.py` module docstring | P2 |
| D4 | `cc10x_hooklib.py` `resolve_hook_mode` docstring | P1 |
| D5-D7, D17 | `plugins/cc10x/hooks/README.md`: table row, "Which hooks block" bullets, Git guard limits (the single source for the full rule, the trade-off and the limits), classifier-crash bullet | P3 |
| D8, D9, D18 | `skills/cc10x-guide/SKILL.md`: overview sentence, Git guard bullet, `git push` troubleshooting row | P3 |
| D10-D12 | `README.md`: the settings-template note, the hooks overview sentence, the Hooks table | P3 |
| D13, D14 | `docs/router-invariants.md`: INV-013 list, INV-033 Covers / Enforces / If removed | P3 |
| D15 | `skills/cc10x-router/references/build-workflow.md`: end of the token bullet | P3 |
| D16 | `CHANGELOG.md` `## [Unreleased]` | P3 |

Every surface except the hooks README states the short rule ("a command that is only a plain `git push` defers to Claude Code's permissions; everything else prompts") and points to `plugins/cc10x/hooks/README.md`.

Validator constraints that held throughout:
- `harness_audit.check_hooks_readme` allows exactly one backticked `cc10x_git_guard.py` in the hooks README, and no "only N blocking hooks" phrasing.
- PP-39(b) needs W8 to name only the hooks that never call `load_mode`, now `cc10x_qa_isolation_guard.py`.

### Context References
- The design doc: intent, rule, trade-off, error handling, evidence.
- `plugins/cc10x/scripts/cc10x_git_guard.py`: `PLAIN_*`, `ASK_MODE_DEFERRED`, `MSG_NOT_LONE_PUSH`, `_lone_plain_push`, `_log_classifier_failure`, `main()`.
- `plugins/cc10x/scripts/cc10x_hooklib.py`: `HOOK_MODE_*`, `resolve_hook_mode`, `load_mode`, `pretool_ask`.
- `plugins/cc10x/hooks/README.md` "Git guard limits": the user-facing rule and limits.
- `docs/prompt-change-checklist.md` §2-§5: the review and record applied in P3.
- ADRs `docs/adr/0001-*` and `0002-*` cover unrelated areas. No conflict.

Durability horizon: P1-P3 are `stable` (a config contract users write files against). P4 is `session-only`.

## Execution Contract Layer (as executed)

### Phase P1: per-key hook-mode values, `gitGuard` default, `pretool_ask` (complete)
- **objective:** `load_mode()` returns `gitGuard`, validated against its own allowed set; `pretool_ask` exists. No hook behavior changes.
- **files/surfaces:** `cc10x_hooklib.py`, `config/hook-mode.json`, `test_cc10x_guards.py`.
- **Depends on:** nothing. **Enables:** P2.
- **allowed scope:** the Durable Decisions for the hooklib and config, D4, and the 4 test literals. **out-of-scope drift:** any guard script, an `audit` alias, changes to invalid-value logging.
- **tests:** `test_git_guard_mode_accepts_ask_and_rejects_audit`, `test_ask_is_invalid_on_the_block_audit_keys`, `test_hook_mode_values_cover_every_key_and_admit_each_default`.
- **required checks / exit:** 207 guard tests passed, `RELEASE GATE: OK`, only the three files changed. Met; verifier 13/13.
- **validation level:** Deterministic. **checkpoint:** none (AFK).
- **test_seams:** unit seam `resolved_mode` → `load_hooklib().load_mode()`; module constants via `load_hooklib()`.
- **Interfaces:**
  - **Consumes:** none.
  - **Produces:**
    - `HOOK_MODE_DEFAULTS["gitGuard"] == "block"`
    - `HOOK_MODE_VALUES: dict[str, tuple[str, ...]]`
    - `load_mode() -> dict[str, str]`
    - `pretool_ask(reason: str) -> None`

### Phase P2: git guard mode branch, plus the policy paragraph PP-39 reads (complete)
- **objective:** `main()` reads the mode once a verdict exists. `ask` defers or asks, and logs one decision event. A mode-read failure takes the `block` path. D1-D3 stop calling the git guard unconditional.
- **files/surfaces:** `cc10x_git_guard.py`, `test_cc10x_guards.py`, `workflow-artifact-and-hook-policy.md` (D1, D2 only).
- **Depends on:** P1 (`load_mode() -> dict[str, str]`, `pretool_ask(reason: str) -> None`). **Enables:** P3.
- **allowed scope:**
  - the mode branch and the import.
  - `run_git_guard_in_process(project_dir, command, patches=(), extra_env=None)`, which pins `CLAUDE_PLUGIN_ROOT` and drops an ambient `CLAUDE_PLUGIN_DATA`.
  - D1-D3.
  - as remediated: `_log_classifier_failure(exc, decision)` and the `git_guard_mode_read_failed` event.
- **out-of-scope drift:** any change inside the classifier, `PRIORITY`, `APPROVABLE`, the messages or `consume_approval`; any change to the `block`-path deny text; reading the mode before a verdict exists; a fallback that could print two JSON objects.
- **exit criterion (narrowed by the router in remediation cycle 1):** no change inside `classify_git_command`, `_scan`, `_floor`, `PRIORITY`, `APPROVABLE`, the existing messages or `consume_approval`. `_log_classifier_failure` and `main()`'s classifier-failure handling are sanctioned. This replaces revision 2's "no hunk between `def _floor` and `def main`", which the later `_lone_plain_push` and new constants would break anyway. Checked by AST comparison against f346ebe.
- **remediation (2 rounds):**
  1. The classifier-failure event's `decision` mislabelled the `ask` outcome. Fixed: `main()` now supplies the decision.
  2. A P1 test failed under the file's own runner, the mode-read fallback was silent, and two crash-combination tests were missing. Fixed: the runner-compatible test, `git_guard_mode_read_failed`, and the two tests.
- **required checks / exit:** guard tests green, `test_cc10x_qa_phase_invariants.py` exits 0 (PP-39 `5 blocking / 4 mode-aware / 1 unconditional`), `RELEASE GATE: OK`. Met; reviewer APPROVE, hunter CLEAN, verifier 14/14.
- **validation level:** Deterministic. **checkpoint:** none (AFK).
- **test_seams:** integration seam `run_guard` (hook subprocess: stdin JSON, stdout, exit code, events log); in-process seam `run_git_guard_in_process` with `patches` for fault injection; unit seam `classify(...)`. No new seam.
- **Interfaces:**
  - **Consumes:** `load_mode() -> dict[str, str]`, `pretool_ask(reason: str) -> None`.
  - **Produces:**
    - events `git_guard_deferred` (decision `defer`), `git_guard_ask` (decision `ask`) and `git_guard_mode_read_failed`
    - ask reason prefix `cc10x git guardrails: `
    - `run_git_guard_in_process(project_dir, command, patches=(), extra_env=None)`
    - policy W8 naming only `cc10x_qa_isolation_guard.py`

### Phase P3: docs, invariants, CHANGELOG, and the deferral rule's remediation rounds (complete)
- **objective:** D5-D18 state the shipped behavior. The review rounds in this phase also produced the final deferral rule.
- **files/surfaces:**
  - docs: `plugins/cc10x/hooks/README.md`, `plugins/cc10x/skills/cc10x-guide/SKILL.md`, `README.md`, `docs/router-invariants.md`, `build-workflow.md` (D15), `CHANGELOG.md`.
  - code and tests, through the remediation rounds: `cc10x_git_guard.py`, `test_cc10x_guards.py`, `test_cc10x_qa_phase_invariants.py` (census comments), and D1-D3.
- **Depends on:** P2 (the `git_guard_deferred` and `git_guard_ask` events and the reason prefix `cc10x git guardrails: `). **Enables:** P4.
- **remediation rounds (P3's six, numbered across the build):**
  - 3. The template's `Bash(git branch:*)` would auto-approve a deferred `branch -D`, so the user chose to prompt for it. Doc fact fixes: a missing key logs nothing; `git_guard_mode_read_failed` is a backstop; events are logged only in a cc10x project. Added a hooks README pin test. Updated the census comments.
  - 4. A push chained with `branch -D` was deferred, because `push` outranks `branch-delete` in `PRIORITY`. Fix: defer only when every git operation found was a push. User-authorized past the circuit breaker.
  - 5. Remote-rewriting push forms deferred. A `push-rewrite` verdict key made them prompt (deny-list).
  - 6. Shell-built arguments and config overrides still deferred. Switched to an allow-list over each push. Output-only redirects allowed.
  - 7. The per-segment proof was unsound against sibling statements and the lexer's fallback. Switched to a whole-command single plain push. The classifier reverted verbatim to v12.10.0, which removed the `push-rewrite` key. URL, scp and path remotes prompt. The full rule now lives only in the hooks README.
  - 8. `^` and `~` in `PLAIN_WORD` let zsh `EXTENDED_GLOB` and tilde expansion inject arguments (`GIT_TRACE` showed an injected flag). Dropped both. Added `NON_PLAIN` cases. Renamed an overclaiming test to `test_git_guard_classifier_keys_and_push_verdicts_are_unchanged`. Noted `--no-verify` beside the pre-push-hook limit.
  - Rounds 4-8 went past the 3-cycle circuit breaker, each with the user's authorization. Every round was re-reviewed and re-hunted, except the last, which the user approved for one verifier pass only.
- **required checks:**
  - a stale-wording sweep over the doc surfaces.
  - `harness_audit.py` exit 0.
  - the §2-§4 semantic review of the three prompt surfaces (D1/D2, D15, D8/D9/D18).
  - the prompt diff review against f346ebe.
  - the CHANGELOG §5 record with classification `wording_only_trust_sensitive`.
  - `RELEASE GATE: OK`.
- **exit:** met. Final verifier 14/14 scenarios; after the P4 polish round 232/232 guard tests, 838 pytest, `RELEASE GATE: OK`.
- **validation level:** Deterministic (sweep, tests, gate) plus Manual (semantic and prompt-diff review). **checkpoint:** none (AFK); the rule changes were user decisions at circuit-breaker gates.
- **test_seams:** as in P2, plus validator seams (`harness_audit.check_hooks_readme`, PP-39, the README pin `test_hooks_readme_git_guard_limits_name_every_ask_mode_event`).
- **Interfaces:**
  - **Consumes:** events `git_guard_deferred` (decision `defer`) and `git_guard_ask` (decision `ask`); ask reason prefix `cc10x git guardrails: `.
  - **Produces:**
    - `_lone_plain_push(command: str) -> bool`
    - `ASK_MODE_DEFERRED = frozenset({"push"})`
    - `## [Unreleased]` CHANGELOG section
    - the hooks README Git guard limits section that the other docs point to

### Phase P4: pre-PR handoff (HITL, in progress)
- **objective:** bring this plan and the design doc in line with the build (this revision), scrub them, show the user the diff and evidence, and take each publishing step only on explicit approval.
- **files/surfaces:** this plan and the design doc (amend + scrub only).
- **Depends on:** P3 (`## [Unreleased]` CHANGELOG section). **Enables:** the upstream PR (outside this plan).
- **allowed scope:** reporting; read-only commands; the doc amendment and scrub. Then, each after its own explicit approval and in this order: the commit, the fork, pushing the branch to the fork, and `gh pr create` against `romiluz13/cc10x`.
- **out-of-scope drift:** code or other doc changes; pushing to `romiluz13/cc10x` directly; any publishing step without approval; committing either doc unscrubbed.
- **required checks:** a grep over both docs for local paths, home directories, user names and scratchpad references returns zero hits. Manual: the user's approval of each publishing step.
- **validation level:** Deterministic (scrub grep) and Manual. A live Claude Code session on the final code is optional. The final verifier already ran the hook live, and the 2026-10-15 session proved the Claude Code side.
- **checkpoint type:** human_verify (`manual-verification` + `external-access`).
- **exit criteria:** the user's recorded decision: approve the PR steps, or stop.
- **test_seams:** E2E (a real Claude Code session), optional and user-run.
- **Interfaces:**
  - **Consumes:** `## [Unreleased]` CHANGELOG section.
  - **Produces:** none.

Self-review: no cross-phase reference drift.
- P2 consumes P1's `load_mode() -> dict[str, str]` and `pretool_ask(reason: str) -> None`.
- P3 consumes P2's two decision events and the reason prefix.
- P4 consumes P3's CHANGELOG section.

## Critical-path sections

### Behavior contract
For a Bash PreToolUse call with command `c`:
- If the unchanged classifier, or its crash fallback, yields no verdict, the hook prints nothing, exits 0, and doesn't read the mode.
- If there is a verdict `(key, reason)`, and the mode read raises or `gitGuard` resolves to `block`, the output is identical to v12.10.0: token check, then `git_guard_token_consumed`, or `git_guard_blocked` and the same deny. A raise also logs `git_guard_mode_read_failed` first.
- If there is a verdict and `gitGuard == "ask"`, one decision event is logged, then:
  - `key == "push"` and `_lone_plain_push(c)`: no stdout, exit 0, `git_guard_deferred`.
  - otherwise: exactly one `pretool_ask` JSON, exit 0, `git_guard_ask`. The reason is `MSG_NOT_LONE_PUSH` for a non-plain push.
- `gitGuard` is `"ask"` only when the highest-precedence valid layer holds exactly the string `"ask"`.

### Edge-case catalog
| Case | Expected | Test |
|------|----------|------|
| No override, or explicit `block` | 12.10.0 output | baseline tests; `test_git_guard_explicit_block_mode_matches_no_config` |
| `audit`, `Ask`, `1`, `null` for `gitGuard` | `block` + `invalid_hook_mode` | `test_git_guard_mode_accepts_ask_and_rejects_audit`, `test_git_guard_audit_value_falls_back_to_block` |
| `ask` on the other three keys | that key keeps its default + event | `test_ask_is_invalid_on_the_block_audit_keys` |
| Lone plain push (flags, `-C`, refspecs, output redirects) | defer | `test_git_guard_ask_mode_defers_every_plain_push` |
| Push with another statement, chain, `&`, alias, function, `git config`, `export`, env prefix, wrapper, `-c`, `--config-env`, URL/scp/path/`~` remote, `^`/`~` glob, quoted or built argument, pipe, file redirect | `ask`, token kept | `test_git_guard_ask_mode_asks_for_every_non_plain_push_and_keeps_the_token`, `test_git_guard_plain_word_admits_no_shell_special_character` |
| `branch -D` | `ask`, token kept | `test_git_guard_ask_mode_asks_for_branch_delete_and_keeps_the_token` |
| Each of the ten non-deferred keys; every pair in one chain | `ask` | `test_git_guard_ask_mode_asks_for_every_non_deferred_key`, `test_git_guard_ask_mode_asks_for_every_pair_of_keys`, `test_git_guard_ask_mode_push_chained_with_branch_delete_asks` |
| The same pushes in `block` mode | the 12.10.0 `push` verdict | `test_git_guard_classifier_keys_and_push_verdicts_are_unchanged`, `test_git_guard_block_mode_rewrite_pushes_match_plain_push`, `test_git_guard_block_mode_push_chained_with_branch_delete_is_unchanged` |
| `_lone_plain_push` raises | `ask` | `test_git_guard_lone_plain_push_check_fails_closed` |
| Classifier crash on git text (with or without a mode failure); crash without `git` | `ask` / `block` path / pass with no mode read | `test_git_guard_ask_mode_classifier_crash_asks`, `test_git_guard_classifier_crash_with_mode_read_failure_blocks`, `test_git_guard_classifier_crash_without_git_word_never_reads_mode`, `test_git_guard_a_crash_while_picking_the_verdict_fails_closed` |
| `load_mode` raises | `block` path | `test_git_guard_mode_read_failure_takes_the_block_path` |
| No verdict in `ask` | silent, no event | `test_git_guard_ask_mode_ignores_commands_without_a_verdict` |
| Ambient `CLAUDE_PLUGIN_DATA` with `ask` in the pytest shell | in-process baseline tests still see `block` | `test_git_guard_in_process_helper_ignores_ambient_plugin_data` |

### Provable properties (as amended)
1. **PP-A (default preserved).** With no override, or with `block`, every git-guard stdout equals v12.10.0's. Held by:
   - the 12.10.0 classifier assertions, restored.
   - the three block-mode tests above and the explicit-block test.
   - AST identity of the classifier functions with f346ebe.
   - the final verifier's 952-command differential run (0 differences).
   - the environment pin on `run_git_guard_in_process`.
2. **PP-B (resolver total).** `load_mode()` returns exactly the `HOOK_MODE_DEFAULTS` keys, each in `HOOK_MODE_VALUES[key]`. Held by `test_hook_mode_values_cover_every_key_and_admit_each_default` and the resolver tests.
3. **PP-C (no silent loosening on bad input).** Any `gitGuard` value other than the string `"ask"` resolves to `"block"`. Held by the two invalid-value tests.
4. **PP-D (ask partition, amended).** In `ask` mode a verdict defers if and only if its key is `push` and `_lone_plain_push(command)` is true. Every other verdict returns `ask`; none yields `deny` or silence. Held by:
   - `test_git_guard_ask_mode_defers_push_only`.
   - the set lock in `test_git_guard_ask_mode_asks_for_every_non_deferred_key`: its cases equal `PRIORITY` minus `ASK_MODE_DEFERRED`.
   - the plain and non-plain push tables, the pair test.
   - `test_git_guard_plain_push_flags_are_exactly_the_contract_set`.
5. **PP-E (fault direction, amended).** A fault never loosens the guard:
   - a mode-read exception takes the `block` path.
   - an exception in `_lone_plain_push` means `ask`.
   - a classifier crash on git text is `classifier-error`, so `deny` in `block` mode and `ask` in `ask` mode.
   - Held by the six fault tests in the catalog.
6. **PP-F (token untouched in ask).** `ask` mode never reads or deletes `.cc10x/state/git-approval.json`. Held by the two "keeps_the_token" tests.
7. **PP-G (audit trail, amended).** In `ask` mode each verdict logs exactly one decision event, `git_guard_deferred` or `git_guard_ask`. `git_guard_classifier_failed` (in `ask` mode) and `git_guard_mode_read_failed` carry no decision key, so the decision event stays unique. Events are written only where `.cc10x/` exists. Held by the defer and ask tests, and the crash tests.
8. **PP-H (docs truthful about modes).** W8 names exactly the hooks that never call `load_mode`. Held by PP-39(b).

### Purity boundary map
- Pure: `classify_git_command` and helpers (unchanged); `_lone_plain_push` (text in, bool out); `resolve_hook_mode(layers)`.
- I/O edge, never raises: `load_mode()`, `log_event` (writes only where `.cc10x/` exists).
- I/O shell: `main()` (stdin, `load_mode`, `consume_approval` on the `block` path only, events log, stdout via `pretool_deny` / `pretool_ask`).

### Verification strategy and live evidence
- Deterministic each phase: `uvx --with pytest pytest -q plugins/cc10x/scripts/test_cc10x_guards.py` and the file's own runner, then the full release gate. The gate includes the Python 3.9 hook run.
- Live, 12.10.0 reference patch (2026-10-15): a real Claude Code session on the 12.10.0 install with an equivalent patch (value `audit`, deferral by verdict key).
  - A real `git push` to a local bare remote ran with no cc10x deny.
  - `git reset --hard` produced a Claude Code prompt that the user approved.
  - It confirmed `CLAUDE_PLUGIN_DATA` reaches PreToolUse hooks.
- Live, this branch (final integration verifier):
  - The built hook ran in `ask` mode against a real local bare remote. The plain push deferred and updated the remote. 22 non-plain push forms returned `ask`.
  - In `block` mode, 952 commands gave identical results through the 12.10.0 hook and this branch's hook.
  - 14/14 scenarios (final verifier and the P4 polish re-verify); 232/232 guard tests after the polish round; `RELEASE GATE: OK`.
  - The Claude Code side of defer and `ask` rests on the reference-patch session.

## Honest limits
- A lone plain push runs whenever Claude Code's rules allow it, with no prompt under `bypassPermissions` or a broad `Bash(git push:*)` rule. Whether an `ask` reaches a human depends on the permission mode.
- No text guard sees state outside the command, so a plain push still defers when such state changes what it does:
  - remote config such as `remote.<x>.push +...` or `remote.<x>.mirror`.
  - an exported `GIT_*` variable, or a function or alias set earlier.
  - pre-push hooks. `--no-verify` is allowed and skips them.
  - the config of the repository `-C <path>` selects.
  - an unconfigured remote name, which git reads as a path.
- `hook-mode.json` and the token are plain files a model could write. The guard protects against accidents, not against a model working around it.
- Decision events are logged only in a cc10x project.
- Harmless forms outside the allow-list prompt: a quoted ref, an absolute git path, `bash -c`, an unlisted flag.
- `block` mode reads the mode once per verdict. Its stdout is unchanged, but it may log `invalid_hook_mode` for an unrelated bad key.
- Pre-existing and unchanged from 12.10.0:
  - a redirect between `git` and `push` (`git >/dev/null push`) gets no verdict in either mode.
  - an unguarded `json_print` failure exits 1 and fails open.

## Risk-Based Testing Matrix
| Risk | Probability | Impact | Test Required |
|------|------------|--------|---------------|
| A config error loosens the guard | med | high | invalid-value tests (deterministic) |
| `ask` defers a push whose effect differs from a plain push | med | high | non-plain push table, `PLAIN_WORD` and flag-set locks, pair test (deterministic) |
| `ask` silently defers a non-push key (`branch -D` included) | low | high | non-deferred set lock, `branch -D` test (deterministic) |
| `block` output drifts | low | high | 12.10.0 assertions, block-mode tests, AST identity, 952-command differential |
| A fault loosens the guard | low | high | the six fault tests |
| PP-39(b) red because W8 still names the git guard | high without the P2 edit | med | `suite_qa_phase_invariants` in the gate |
| A stale doc claim (unconditional, or push and branch-delete both deferring) | med | low | P3 sweep, README pin test, this revision's stale sweep |
| State outside the command text changes a deferred push | med | med | documented limit; no in-repo test possible |
| `ask` under `bypassPermissions` reaches no human | med | med | documented trade-off |
| A local path or user name ships in these docs | med | med | P4 scrub grep |

## Functionality Flow Mapping
Flow: the user opts into `ask`.
1. Writes `{"gitGuard": "ask"}` to `${CLAUDE_PLUGIN_DATA}/hook-mode.json`. Test: `test_git_guard_mode_accepts_ask_and_rejects_audit`.
2. The model runs `git push origin main`. The guard defers. Test: `test_git_guard_ask_mode_defers_every_plain_push`.
3. The model runs `git add . && git commit -m x && git push`. The guard asks. Test: the non-plain push table.
4. The model runs `git branch -D old` or `reset --hard`. The guard asks. Tests: the `branch -D` and non-deferred-key tests.

Error paths:
- invalid value → `block`.
- mode read raises → `block`.
- classifier or plain-push check raises → `ask` (in `ask` mode).
- Tests: as in the catalog.

## Scenarios
- **default-unchanged:** given no override; when the model runs `git reset --hard`; then the guard denies exactly as in v12.10.0.
- **ask-defers-lone-plain-push:** given `{"gitGuard":"ask"}`; when the model runs `git push origin main`; then the hook prints nothing, exits 0 and logs `git_guard_deferred`.
- **ask-prompts-chained-push:** given `ask`; when the model runs a commit chained with a push; then the hook returns `ask` with the not-a-single-plain-push reason.
- **ask-prompts-branch-delete:** given `ask`; when the model runs `git branch -D old`; then the hook returns `ask`, and the token file is untouched.
- **audit-value-rejected:** given `{"gitGuard":"audit"}`; when the model runs `git push`; then the guard denies and logs `invalid_hook_mode`.
- **mode-read-failure:** given `ask` configured and `load_mode` raising; when a verdict exists; then `git_guard_mode_read_failed` is logged and the `block` path runs.

## Assumptions
| Assumption | Class |
|-----------|-------|
| No stdout + exit 0 from PreToolUse means Claude Code's normal permission flow applies | proven_by_code (live session, 2026-10-15) |
| `permissionDecision: "ask"` prompts in a default permission mode | proven_by_code (live session, 2026-10-15) |
| Claude Code exports `CLAUDE_PLUGIN_DATA` to PreToolUse hooks | proven_by_code (live session, 2026-10-15) |
| `HOOK_MODE_VALUES` has no reader besides `resolve_hook_mode` | proven_by_code (grep) |
| The classifier is identical to v12.10.0 | proven_by_code (AST comparison; 952-command differential) |
| The shipped settings template allows `Bash(git branch:*)` | proven_by_code (`README.md` settings template, line 267; the reason `branch -D` asks) |

## Decisions
- Keep the name `HOOK_MODE_VALUES`, retyped to a per-key dict.
- Read the mode only after a verdict exists.
- The `try` covers only the mode read. There is no fallback around the `ask` actions, so the hook can't print two JSON objects.
- The deferral rule is the whole-command allow-list `_lone_plain_push`, used only for `push`. See the ADR.
- The full rule lives in the hooks README. The other docs carry the short rule and a pointer.
- CHANGELOG `## [Unreleased]`; no version bump.
- PR route: the user's fork, then a PR into `romiluz13/cc10x`. Each step is approved separately at P4.

## Differences from agreement
Measured against revision 2 of this plan and the original design.
- **`branch -D` prompts in `ask` mode** ("Prompt for branch -D (Recommended)"). Revision 2 deferred both `push` and `branch-delete`. Only `push` can defer now, because the template's `Bash(git branch:*)` would auto-approve a deferred `branch -D`.
- **The deferral rule is a whole-command allow-list**:
  - "Yes, fix it (Recommended)" and "Fix in code + docs (Recommended)" made it a deny-list.
  - "Allow-list defer (Recommended)" made it a per-push allow-list.
  - "Single-command only (Recommended)" made it the whole command.
  - Revision 2 deferred per verdict key.
- **Output-only redirects keep a push plain** ("Allow output redirects (Recommended)"). Pipes and file redirects do not.
- **`^` and `~` are excluded from `PLAIN_WORD`** ("Yes, small fix (Recommended)").
- **The classifier is restored verbatim to v12.10.0.** The ask decision lives in `main()` and `_lone_plain_push`, with new module constants. An intermediate `push-rewrite` verdict key was added in round 5 and removed in round 7.
- **The P2 exit criterion was narrowed** (router, remediation cycle 1). It used to say no hunk between `def _floor` and `def main`. It now says no change inside `classify_git_command`, `_scan`, `_floor`, `PRIORITY`, `APPROVABLE`, the existing messages or `consume_approval`. `_log_classifier_failure` and `main()`'s classifier-failure handling are sanctioned.
- **Two event changes beyond revision 2:**
  - `git_guard_mode_read_failed`, which has no decision key.
  - `git_guard_classifier_failed`, whose decision is now set by `main()` (`allow` / `deny` / no key in `ask`).
- **Census comments updated.** Revision 2 left the PP-39 "measured at this commit" comments in `test_cc10x_qa_phase_invariants.py` as history. P3 updated them to the live census (4 mode-aware / 1 unconditional), after review.
- **A doc-pin test was added.** Revision 2 said P3 needed no new doc-pin seam. `test_hooks_readme_git_guard_limits_name_every_ask_mode_event` pins the ask-mode event names and the single-source wording, after review.
- **Docs are single-sourced.** Revision 2 gave per-surface target wording for push and branch-delete deferral. The shipped docs carry a short rule plus a pointer to the hooks README, which has the full rule.
- **Test counts:** 232 guard tests, against revision 2's planned 216. 838 pytest in the gate, against 810 at baseline.
- **Carried over from revision 2:**
  - the real `PRIORITY` key names are used (`worktree-force`, `discard-all`, `checkout-force`), where the design said `worktree-remove-force` and the discard forms.
  - D1/D2 moved into P2 for PP-39(b).
  - doc surfaces were added beyond the design's list (D15, D10-D12, INV-013/033, D17, D18).
  - the in-process helper's environment pin.
  - the `try` covers the mode read only.
