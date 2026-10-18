# Configurable git guard (`gitGuard` hook mode) — design

Status: design approved in conversation; amended at revision 4 to match the built feature (the user-approved changes made during the build are listed under "Questions resolved"). The plan, `docs/plans/2026-10-15-configurable-git-guard-plan.md`, carries the execution history.

## Purpose

The git guard (`scripts/cc10x_git_guard.py`) was one of two blocking hooks a user could not configure (the other, the QA isolation guard, stays unconditional). It denies `git push` and `git branch -D` unless the router wrote a single-use token at the BUILD-DONE finishing menu. That token path doesn't fit how many people work. The user says "push it" in chat, outside a finished BUILD, and the guard refuses. The model is also told not to write the token itself, so the user ends up typing `git push` by hand. Destructive operations (`reset --hard`, `clean -f`, force-push) have no unlock path at all. Before this change the user could only run them by hand or patch the plugin cache, and an update overwrites the patch.

This design lets a user loosen the guard through the existing `hook-mode.json` layering. Nothing changes for anyone who doesn't opt in.

## Users

cc10x users who want Claude Code's own permission system (allow rules, auto mode, a prompt) to decide on routine git publishing, while still getting a human check on everything else the guard catches (superseded 2026-10-18: see Amendment; `audit` keeps no human check).

## Success criteria

1. With no config change, or with `{"gitGuard": "block"}`, every git guard verdict is byte-for-byte the 12.10.0 one: deny envelopes, token path and messages. The classifier is the 12.10.0 classifier, unchanged.
2. With `{"gitGuard": "ask"}` in `${CLAUDE_PLUGIN_DATA}/hook-mode.json`:
   - A command that is only one plain `git push` produces no output and exits 0, so Claude Code's own permission flow decides.
   - Every other verdict returns `permissionDecision: "ask"` with the guard's reason. That covers `branch-delete`, the other nine non-approvable keys, and a `push` verdict in any command that is not a single plain push.
   - The guard logs one decision event per verdict (in a cc10x project, where `.cc10x/` exists).
3. Invalid input stays fail-safe. `gitGuard: "audit"`, a typo, or a non-string falls back to `block` and logs `invalid_hook_mode`, as the other keys do (superseded 2026-10-18: see Amendment). `ask` on any other key is invalid and falls back for that key.
4. The docs no longer say the git guard is "not controlled by hook-mode config". They name the new key, its two values (superseded 2026-10-18: see Amendment), the plain-push rule and the trust trade-off. `plugins/cc10x/hooks/README.md` (Git guard limits) is the single place with the full rule; the other docs point there.

## Constraints

- Reuse the `hook-mode.json` layering in `cc10x_hooklib.py` (`HOOK_MODE_DEFAULTS`, `resolve_hook_mode`, `load_mode`). No new config file or env var.
- Allowed values are per key: `artifactIntegrity`, `memoryWrites` and `taskMetadata` keep `block|audit`; `gitGuard` takes `block|ask` (superseded 2026-10-18: see Amendment).
- `classify_git_command` and everything it calls stay exactly as in 12.10.0. The mode changes only what `main()` does with a verdict.
- Python 3.9 floor (`from __future__ import annotations` is already present).
- Fail open on a hook crash, as today. A mode-read failure takes the `block` path.

## Out of scope

- An `off` value that lets destructive operations through without a human check. Rejected by the user; `ask` is the loosest mode (superseded 2026-10-18: see Amendment).
- Per-operation configuration (for example "ask for push, block for reset"). YAGNI.
- An `audit` alias for `gitGuard`: on the other keys `audit` means log-only, never block, so it would carry a second meaning here. An `audit` value falls back to `block` and logs `invalid_hook_mode`, which is visible and safe (superseded 2026-10-18: see Amendment).
- Changing the approval-token mechanism or the QA isolation guard.
- Any change to the classifier's deny set.

## Approach chosen

Add `"gitGuard": "block"` to `HOOK_MODE_DEFAULTS` and to the shipped `config/hook-mode.json`. Replace the single `HOOK_MODE_VALUES` tuple with a per-key allowed-values map, and validate each layer's value against its key's set. Add `pretool_ask(reason)` beside `pretool_deny` in the hooklib.

In `cc10x_git_guard.main()`, once the unchanged classifier returns a verdict, read `load_mode()["gitGuard"]` (superseded 2026-10-18: see Amendment; `audit` is a third branch):

- `block`: the 12.10.0 code path, unchanged (token check, then deny).
- `ask`: defer only when the verdict key is `push` and `_lone_plain_push(command)` is true. Otherwise return `ask`. A `push` verdict that isn't a lone plain push asks with a reason saying so (`MSG_NOT_LONE_PUSH`).

`_lone_plain_push` is an allow-list over the whole command text, not over one segment of it:
- one line, lexed with no fallback, no comment tail, no quoted token, no operator (`;`, `&&`, `||`, `|`, `&`, parentheses, braces) and no substitution.
- the literal word `git`, optional literal `-C <path>` pairs, then `push`. No `-c`, `--config-env`, alias, env-assignment prefix or wrapper.
- only the safe flags in `PLAIN_PUSH_FLAGS`.
- one remote name, never a URL or path: no `:`, `@` or `/`, and no leading `.`.
- literal `src[:dst]` refs, both sides non-empty.
- optional trailing output-only redirects (`2>&1`, `>/dev/null`, `2>/dev/null`, `&>/dev/null`, `1>/dev/null`).
- every path, remote and ref side matches `PLAIN_WORD` (`^[A-Za-z0-9._/@-]+$`: no `$`, backtick, brace, glob, backslash, quote, `+`, `^` or `~`) and doesn't start with `-`.
- any exception means "not plain", so the push asks.

Alternatives rejected (ADR notes):
- **Reuse `audit` as the value name.** On every other key `audit` means "log, never block". Here it would mean "defer or prompt", so the same word would carry two meanings in one file. The user picked `ask`.
- **Emit `ask` for every push.** It prompts on every push, including pushes the user already allowed through Claude Code rules or in chat. Deferring a plain push lets the user's own permission config decide.
- **A separate `git-guard.json` or an env var.** A second config surface. The layering already survives plugin updates and has fail-safe per-key fallback.
- **Defer per verdict key (`push` and `branch-delete`)**, the approved design before the build. Rejected during the build: the shipped settings template allows `Bash(git branch:*)`, so a deferred `branch -D` would run with no prompt. The user chose to prompt for `branch -D`.
- **Deny-list the dangerous push forms and defer the rest.** Tried in build rounds 4-5: defer only when every git operation found in the command was a push, plus a `push-rewrite` verdict key for remote-rewriting forms. It kept leaking. Remote-rewriting pushes (`--mirror`, `--delete`, `:ref`, `--prune`), shell-built arguments, config overrides (`-c`, `--config-env`, `GIT_CONFIG_*`) and sibling commands each needed one more entry, and each review found another one. The user chose an allow-list.
- **Allow-list each push segment.** Tried in round 6. Unsound, because the rest of the command changes what a plain-looking segment does: a sibling statement (a `git()` function, an alias line, `git config`, `export GIT_CONFIG_*`, `cd`) runs in the same shell, and when the lexer fell back, the segments weren't the shell's. The user chose "single command only": the whole command must be one plain push.
- **Change the classifier.** Rejected in round 7. The classifier was restored verbatim to 12.10.0, so `block` mode can't drift. The ask decision lives in `main()` and `_lone_plain_push`, and it only reads the verdict and the command text.

## Domain glossary

- **hook mode**: the per-key value resolved from shipped `config/hook-mode.json`, overridden by `${CLAUDE_PLUGIN_DATA}/hook-mode.json`.
- **approvable operation**: a git guard verdict key in `APPROVABLE` (`push`, `branch-delete`). In `block` mode the router's token can unlock it. In `ask` mode the token is not read.
- **lone plain push**: a command whose whole text is one `git push` that `_lone_plain_push` accepts. It is the only thing `ask` mode defers.
- **defer**: the hook emits no decision and exits 0, so Claude Code's permission flow (rules, mode, prompt) decides.

## Architecture / components

- `scripts/cc10x_hooklib.py`: `HOOK_MODE_DEFAULTS` gains `gitGuard`. `HOOK_MODE_VALUES` becomes a per-key map, and `resolve_hook_mode` checks against it. `pretool_ask` is new.
- `config/hook-mode.json`: gains `"gitGuard": "block"`.
- `scripts/cc10x_git_guard.py`:
  - new module constants `PLAIN_PUSH_FLAGS`, `PLAIN_REDIRECTS`, `PLAIN_REDIRECT_OPS`, `PLAIN_WORD`, `ASK_MODE_DEFERRED = frozenset({"push"})` and `MSG_NOT_LONE_PUSH`.
  - new `_lone_plain_push`.
  - `_log_classifier_failure` now takes its decision from `main()`.
  - the mode branch in `main()` and the module docstring.
  - the classifier itself is unchanged.
- `scripts/test_cc10x_guards.py`: per-key value tests, `ask`-mode tests (defer vs ask, every key, every pair of keys, plain and non-plain push tables, fault paths, token untouched), `block`-mode identity tests, and a hooks README pin for the ask-mode event names and wording.
- `scripts/test_cc10x_qa_phase_invariants.py`: the PP-39 census comments now record the git guard as mode-aware.
- Docs: `hooks/README.md` (table row, "Which hooks block" bullets, override description, Git guard limits), `skills/cc10x-guide/SKILL.md`, `skills/cc10x-router/references/workflow-artifact-and-hook-policy.md`, `skills/cc10x-router/references/build-workflow.md`, root `README.md`, `docs/router-invariants.md` (INV-013, INV-033), and `CHANGELOG.md` (`## [Unreleased]`).

## Data flow

Bash PreToolUse → `cc10x_git_guard.main()` → `classify_git_command(command)`. If there's no verdict, exit 0 and don't read the mode. If there is one, `load_mode()["gitGuard"]` decides (superseded 2026-10-18: see Amendment):
- `block` runs the 12.10.0 token check, then deny.
- `ask` defers a lone plain push and returns `ask` for everything else.

In `ask` mode each verdict logs exactly one decision event through `log_event`, `git_guard_deferred` or `git_guard_ask`. After a classifier crash, `git_guard_classifier_failed` comes first, with no decision key. `block` mode keeps the 12.10.0 events: the verdict ends in `git_guard_token_consumed` or `git_guard_blocked`. Other events can come before it, such as `git_guard_classifier_failed` (decision `deny`) after a classifier crash, or `git_guard_token_invalid` for an unreadable token.

## Error handling (as built)

- **Mode read.** The `try` covers only `load_mode()["gitGuard"] == "ask"` (superseded 2026-10-18: see Amendment). `load_mode()` itself already falls back to `block` on a missing, corrupt or unreadable file, and logs `invalid_hook_mode` for invalid input. If it raises anyway, the guard logs `git_guard_mode_read_failed` (the error class, no decision key) and takes the `block` path. That path logs `git_guard_blocked`, or `git_guard_token_consumed` when a token covers the operation.
- **Classifier crash.** On text that names `git`, the verdict becomes `classifier-error`. `main()` logs `git_guard_classifier_failed` after the mode read, with decision `deny` in `block` mode. In `ask` mode it has no decision key and is followed by `git_guard_ask` (superseded 2026-10-18: see Amendment; `audit` also has no decision key), which stays the verdict's one decision event. On text without `git`, the event says `allow` and the mode is not read.
- **Plain-push check.** Any exception inside `_lone_plain_push` returns false, so the push asks.
- There is no fallback around the `ask` actions, so the hook can never print two JSON objects.

## Testing strategy

Subprocess tests through `run_guard` (with `extra_env={"CLAUDE_PLUGIN_DATA": ...}`) and in-process tests through `run_git_guard_in_process`, which pins its environment and takes `patches` for fault injection. They cover:
- `block` unchanged: the 12.10.0 classifier assertions, explicit `block` equal to no config, push chains.
- `ask` defer, for every entry in the plain-push table.
- `ask` prompt: every non-plain push form, the ten other keys, every pair of keys in one chain.
- the fault paths.
- the invalid-value fallback.

The full `scripts/test_*.py` suite and the doc validators run through `python3 plugins/cc10x/tools/release_gate.py`.

## Trust trade-off and honest limits (documented in the hooks README)

- `ask` moves a lone plain push to Claude Code's permission mode. Under `bypassPermissions`, or a broad `Bash(git push:*)` allow rule, it runs with no prompt.
- Everything else returns `ask`. Whether that prompt reaches a human depends on the Claude Code mode, and in bypass mode it may not. `branch -D` prompts even with the template's `Bash(git branch:*)` rule, because the guard asks (ask mode; under audit it does not, see Amendment).
- The hook-mode file is a plain file the model could write itself. That's the same documented limitation as the approval token. The guard protects against accidents, not against a model working around it.
- No text guard can see state outside the command text, so a plain push still defers when such state changes what it does:
  - remote config (`remote.<x>.push +...`, `remote.<x>.mirror`), an exported `GIT_*` variable, or a function or alias set by an earlier command.
  - pre-push hooks. `--no-verify` is on the safe-flag list and skips them.
  - the config of the repository that `-C <path>` selects.
  - a remote name that isn't configured, which git reads as a path.
- Decision events are logged only in a cc10x project (`.cc10x/` exists).
- The allow-list errs toward prompting. A quoted ref, an absolute git path, a wrapper such as `bash -c`, or any flag outside the safe set prompts even when harmless.
- `block` mode now reads the mode once per verdict. Its stdout is unchanged, but it may log `invalid_hook_mode` for an unrelated bad key.

## Live evidence

- **12.10.0 reference patch, 2026-10-15.** A live Claude Code session ran on the 12.10.0 install with an equivalent local patch (value spelled `audit` there, deferring by verdict key):
  - A real `git push` to a local bare remote ran with no cc10x deny.
  - A `git reset --hard` produced a Claude Code approval prompt; the user saw it and approved.
  - This confirms that Claude Code exports `CLAUDE_PLUGIN_DATA` to PreToolUse hooks, a point the 12.10.0 CHANGELOG lists as unverified.
  - It also proves Claude Code's handling of "no output, exit 0" and of `permissionDecision: "ask"`.
- **This branch, final integration verification.**
  - The verifier ran the built hook live in `ask` mode against a real local bare remote. A plain push deferred and updated the remote. 22 non-plain push forms returned `ask`.
  - In `block` mode, 952 commands gave identical results through the 12.10.0 hook and this branch's hook (0 differences).
  - 14/14 verification scenarios passed. `test_cc10x_guards.py` passed 232 of 232 (236 after the 2026-10-18 amendment), and `RELEASE GATE: OK`.
  - The Claude Code side of defer and `ask` rests on the reference-patch session above.

## Questions resolved

- Value name: `ask` (user, 2026-10-15).
- Plan first: yes (user, 2026-10-15).
- No `off` value, no per-op config, no `audit` alias (design, YAGNI) (superseded 2026-10-18 for `audit`: see Amendment).
- Build-time decisions (user, 2026-10-15):
  - "Prompt for branch -D (Recommended)": `branch -D` asks in `ask` mode, and only push can defer.
  - "Fix in code + docs (Recommended)": remote-rewriting push forms prompt (later absorbed into the allow-list).
  - "Allow-list defer (Recommended)": defer only a provably plain push.
  - "Allow output redirects (Recommended)": output-only redirects keep a push plain, and a pipe makes it non-plain.
  - "Single-command only (Recommended)": the whole command must be one plain push. The classifier is reverted to 12.10.0, and the decision is made in `main()`.
  - "Yes, small fix (Recommended)": drop `^` and `~` from `PLAIN_WORD`.
- Plan and design docs ship in the PR, scrubbed ("Ship, scrubbed (Recommended)").

## Amendment, 2026-10-18: `audit` value

- `gitGuard` gains a third value, `audit`: log-only, matching what `audit` means on the other three hook-mode keys. The classifier still runs; each verdict (`classifier-error` included) logs one `git_guard_audit` event with its key, the hook returns no decision, and the token is never read.
- Why: `ask` still prompted too often on routine cleanup, for example a forced `worktree remove` of a throwaway worktree the agent had just created.
- Trade-off: Claude Code's own permission flow is the only gate, so `audit` is no stronger than the permission mode; under `bypassPermissions` destructive git runs unprompted, and even in the default permission mode the template's `Bash(git branch:*)` allow rule (like any broad allow rule) runs `git branch -D` with no prompt. `block` stays the default and is unchanged; `ask` is unchanged.
- `audit` is now the loosest mode. There is still no `off` value.
- Data flow: `mode = load_mode()["gitGuard"]` is read once as a value. `audit` logs `git_guard_audit` and returns, before the ask and token branches.
- Error handling: the classifier-failure decision key is `None if mode in ("ask", "audit") else "deny"`. A classifier crash in `audit` mode logs `git_guard_classifier_failed` (no decision key), then `git_guard_audit` with key `classifier-error`. A mode-read failure still sets the mode to `block`, so it takes the block path.
- Events, as in `ask` mode, are logged only in a cc10x project (`.cc10x/` exists). Elsewhere `audit` gates nothing and records nothing.
- Tests: `test_git_guard_mode_accepts_ask_and_audit_and_rejects_others` replaces `test_git_guard_mode_accepts_ask_and_rejects_audit`; the `audit` mode tests are `test_git_guard_audit_mode_logs_every_verdict_and_keeps_the_token`, `test_git_guard_audit_mode_ignores_non_git_commands` and `test_git_guard_audit_mode_classifier_crash_logs_once`.
