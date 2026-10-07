# cc10x Hooks

This directory serves two different purposes:

1. **Plugin runtime hooks** via `hooks.json`
2. **Optional git pre-commit helper** via `pre-commit`

## Plugin Runtime Hooks

When CC10X is installed as a Claude Code plugin, Claude Code reads `hooks/hooks.json`
from the plugin bundle and runs the referenced scripts from `${CLAUDE_PLUGIN_ROOT}/scripts`.

**Python requirement:** every hook except the preflight is a `python3` script,
so CC10X needs Python 3.9 or newer on `PATH` (3.9 is the minimum, 3.13 is the
version the test suite runs on). If `python3` is missing or older, the guards fail
silently. The POSIX-sh preflight hook below detects this and tells the agent to ask
you to install or upgrade Python; it always exits 0.

### Every registered hook

Each hook in `hooks.json` appears exactly once in this table (a validator in
`harness_audit.py` checks that). "Blocks" means it can deny or signal the model;
"audit" means it only writes log lines.

| Event (matcher) | Hook | What it does | Blocks or audits |
| --- | --- | --- | --- |
| `PreToolUse` (`Edit\|Write`) | `cc10x_pretooluse_guard.py` | Flags direct writes to the memory markdown files under `.cc10x/` | Audit by default; denies when `memoryWrites` is `"block"` |
| `PreToolUse` (`Bash`) | `cc10x_git_guard.py` | Denies push, hard reset, forced clean, forced branch delete, discard-all checkout/restore and stash clear | Blocks always; not controlled by hook-mode config |
| `PreToolUse` (`Read\|Grep\|Glob\|Edit\|Write\|NotebookEdit\|Bash`) | `cc10x_qa_isolation_guard.py` | QA route only: denies reads of quarantined paths and environment mutation during plan phases; disengages once the QA workflow is finished | Blocks always; not controlled by hook-mode config |
| `SessionStart` (`startup\|resume\|clear\|compact\|fork`) | `cc10x_preflight.sh` | Tells the agent when `python3` is missing or older than 3.9 | Context only; always exits 0 |
| `SessionStart` (same matcher) | `cc10x_sessionstart_context.py` | Injects resume context for the newest workflow that is not finished | Context only |
| `PostToolUse` (`Edit\|Write\|Bash`) | `cc10x_posttooluse_artifact_guard.py` | Validates a workflow artifact right after it is written; audits other writes; logs a `bash_workflow_write` event when a Bash command writes into `.cc10x/workflows/` | Exit 2 only for a malformed artifact when `artifactIntegrity` is `"block"` (the shipped default); everything else audits |
| `TaskCompleted` | `cc10x_task_completed_guard.py` | Checks task metadata, memory-finalization evidence and the remediation circuit-breaker backstop | Audit by default; blocks when `taskMetadata` is `"block"` |
| `PostCompact` | `cc10x_event_logger.py postcompact` | Records the compaction in the hook log and the workflow event log | Audit |
| `SubagentStop` | `cc10x_event_logger.py subagent_stop` | Logs whether a `cc10x:*` agent returned a contract; reads the final message, and the SubagentHandback report from the transcript when the final message has none (`report_source` records which) | Audit |
| `PreCompact` | `cc10x_state_persist.py precompact` | Snapshots workflow state before compaction | Persistence only |
| `Stop` | `cc10x_state_persist.py stop` | Snapshots workflow state when the session stops | Persistence only |
| `StopFailure` | `cc10x_event_logger.py stop_failure` | Logs API errors (async) | Audit |
| `InstructionsLoaded` | `cc10x_event_logger.py instructions_loaded` | Logs instruction file loads (async) | Audit |

### Which hooks block, which audit

- **Config-controlled** (`config/hook-mode.json`, values `"block"` or `"audit"`):
  `artifactIntegrity` ships as `"block"`, `memoryWrites` and `taskMetadata` ship as
  `"audit"`.
- **Override location:** put a `hook-mode.json` with the same keys in
  `${CLAUDE_PLUGIN_DATA}` to change a mode without editing the plugin; it survives
  plugin updates. Each key falls back on its own: a missing key, a value other than
  `block` or `audit`, or a corrupt file leaves the shipped value for that key (an
  `invalid_hook_mode` event is logged for invalid input, once per problem and state of
  the file, tracked by a marker under `.cc10x/state/`; if the marker cannot be written
  the event is logged on every call). The resolver never raises
  and always yields all three keys, so a damaged file cannot silently turn
  `artifactIntegrity` off.
- **Unconditional blockers:** the git guard and the QA isolation guard deny
  regardless of the config. Everything else is audit, context or persistence.
- **PostToolUse cannot undo a write.** Exit 2 from the artifact guard feeds its
  message to the model after the file is already on disk; the malformed artifact
  stays until the model repairs it, and the message says to repair it now.
- **Fail-open by design:** a hook that crashes, times out or cannot parse its
  input lets the tool call proceed. The hooks log the decisions they make and
  the failures they notice (an unreadable artifact, an invalid mode file, a
  failed snapshot write, a classifier error, a workflow event dropped because its
  id is unsafe (`workflow_id_unsafe`) or its append failed
  (`workflow_event_append_failed`)), but a hook that dies before it
  logs leaves only a trace in Claude Code's debug output.

### Git guard limits

- It is a **text heuristic**, not a shell parser, and it is built so that it
  denies at least everything the original pattern list denies when run over the
  raw command text. On top of that it reads wrapper prefixes (`env`, `sudo`,
  `xargs`, `nohup`, ...), `git -C`, `git -c alias.x=...`, `bash -c`, `eval`,
  `$(...)`, backticks, chains and newlines. Text that a shell comment (`# ...`
  at a word start) drops is scanned as well, because a `#` is not always a
  comment (`${y/ #/}`), so a command that names a destructive operation in a
  comment is denied. CR is an ordinary character, as in bash.
- **One narrow allowance for quoted data (default deny).** Destructive text is
  allowed only when the whole command is a single pipeline `A | B | C` where `A`
  is `echo`, `printf`, `grep`, `egrep` or `fgrep`, every other member is one of
  `grep`, `egrep`, `fgrep`, `cat`, `head`, `tail`, `wc`, `tr`, `cut` (bare names,
  not `./cat` or `/bin/cat`; not `sort` or `uniq`, which can write files), and
  the destructive text is only inside `A`'s quotes. The command may contain none
  of `#`, backslash, CR, newline, `$`, backtick, `(`, `)`, `{`, `}`, `;`, `&`,
  `<`, `>` outside single or double quotes, none of `exec`, `eval`, `source`,
  `.`, `function`, `for`, `while`, `until`, `if`, `case`, `do`, `done`, `then`,
  `fi` as an unquoted word, and no `$`, backtick or backslash inside double
  quotes. Every other command gets the full pattern list over its entire raw
  text plus the wrapper scan. So a read-only `grep` over notes that quotes a
  destructive command passes, while a redirect (`2>/dev/null` included), a group
  or loop, a pipe into `sh`, `xargs`, `tee`, `sort` or anything else that is not
  a plain text filter is denied. Pipe-fed executors (`xargs`, `sh`, `source`,
  `while read`, `python -c`), a redirect to a file, `<<<`, and process
  substitution are denied.
- Nesting deeper than 8 levels (`$(...)`, backticks, `bash -c`, `eval`, aliases)
  is denied, not skimmed. A quoted argument of `echo`, `printf` or `grep` is
  scanned a second time, so `echo "$(...)"` costs two levels: the real figure
  for that form is four nested levels, the fifth is denied.
- A command longer than 64 KB (65,536 characters) whose text names `git` as a
  word is denied (`command-too-large`) before any pattern runs: the verbatim
  legacy force-push pattern is quadratic in the number of `git push` words, and
  the hook times out and fails open at 5 s. A commit message that large is not
  a use case; a command of that size without the word `git` is not scanned.
- A git command word or subcommand word that a brace expansion, a glob that
  could match `git`, or a `$(...)`/backtick substitution builds (`git {push,}
  origin`, `git pu{sh,} origin`, `{git,} push`, `/usr/bin/gi? push`,
  `$(echo git) push`) is denied without being resolved: as the real operation
  when the command word is built, as `classifier-error` when the subcommand
  word is. A plain variable (`$G push`) is not expanded and is not seen.
- `env -S` / `--split-string` scripts are scanned like `bash -c` text.
- A script written to a file and run later is not seen (the write is not a git
  command). A command whose text hides the git call (variables, `$IFS`, hex
  escapes, `git config` aliases set in an earlier command) is not seen either.
- Destructive text inside other quoted arguments (a commit message, a `gh` body,
  `ssh host '...'`) is still denied; only the allowance above is exempt.
- If the classifier itself crashes, the guard logs `git_guard_classifier_failed`
  and denies any command whose text contains `git`; other commands pass.
- Only remote publish and branch force-delete can be unlocked, by a single-use
  approval token the router writes after the user's explicit finishing choice. The
  token is a plain file under `.cc10x/state/`: **a model that can write files can
  write one itself.** This is a documented limitation, not a defended boundary; the
  guard protects against accidents, not against a model working around it.
- A command that mixes a token-unlockable operation with a non-unlockable one is
  denied as the non-unlockable one.

### SessionStart

The matcher covers every documented source (`startup`, `resume`, `clear`,
`compact`, `fork`). Resume context comes from the newest workflow artifact that is
not finished (the later of the last `status_history` entry and the newest
router-written events-log record decides when both carry a timestamp; otherwise a
terminal `memory_finalized`, `workflow_completed` or `workflow_failed` in either
counts; a completed `memory-finalize` phase also counts); with only finished
workflows nothing is injected. Only files named like a workflow id (`wf-...json`)
are artifacts. JSON that is not an object (`[]`, `5`, `null`) is an unreadable
artifact. An unreadable artifact newer than a live one is logged
(`workflow_artifact_unreadable`) and skipped; when no live workflow can be read,
SessionStart says so in one line naming the unreadable artifact. Without
`CLAUDE_PROJECT_DIR` the project root is the checkout root containing the session
`cwd`, and a relative hook-input `cwd` is made absolute. The QA isolation guard
does not use this selection: the newest artifact decides, so an abandoned older QA
workflow is never revived by a later workflow finishing. The QA guard does not read
the events log.

## Internal Publication Audit

The plugin also ships an internal drift check:

```bash
python3 plugins/cc10x/tools/harness_audit.py
```

It validates the publication-critical contract:
- plugin manifest version matches `README.md` and `CHANGELOG.md`
- marketplace metadata matches the shipped plugin version
- plugin hooks and MCP names referenced by docs/router actually exist
- every hook in `hooks.json` is listed once in this README, and no document claims a fixed count of enforcement points
- workflow replay fixtures and checker are present
- key router headings still exist for invariant coverage
- router-consumed task metadata and agent contract fields are still present

## Optional Git Pre-Commit Hook

This is separate from Claude Code plugin hooks. Install it only if you want
git commits blocked when tests fail:

```bash
cp plugins/cc10x/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

It blocks `git commit` if your test suite fails. No test runner configured?
Hook exits 0 and passes through.
