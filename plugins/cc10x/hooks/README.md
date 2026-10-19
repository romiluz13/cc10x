# cc10x Hooks

This directory serves two different purposes:

1. **Plugin runtime hooks** via `hooks.json`
2. **Optional git pre-commit helper** via `pre-commit`

## Plugin Runtime Hooks

When CC10X is installed as a Claude Code plugin, Claude Code reads `hooks/hooks.json`
from the plugin bundle and runs the referenced scripts from `${CLAUDE_PLUGIN_ROOT}/scripts`.

**Python requirement:** every hook except the preflight is a `python3` script,
so CC10X needs Python 3.9 or newer on `PATH` (3.9 is the minimum, 3.13 is the
version the test suite runs on). If `python3` is missing or older, the hooks fail
silently. The POSIX-sh preflight hook below detects this and tells the agent to ask
you to install or upgrade Python; it always exits 0.

### Every registered hook

Each hook in `hooks.json` appears exactly once in this table (a validator in
`harness_audit.py` checks that). "Blocks" means it can deny or signal the model;
"audit" means it only writes log lines.

| Event (matcher) | Hook | What it does | Blocks or audits |
| --- | --- | --- | --- |
| `SessionStart` (`startup\|resume\|clear\|compact\|fork`) | `cc10x_preflight.sh` | Tells the agent when `python3` is missing or older than 3.9 | Context only; always exits 0 |
| `SessionStart` (same matcher) | `cc10x_sessionstart_context.py` | Injects resume context for the newest workflow that is not finished | Context only |
| `PostToolUse` (`Edit\|Write\|Bash`) | `cc10x_posttooluse_artifact_guard.py` | Validates a workflow artifact right after it is written; audits other writes; logs a `bash_workflow_write` event when a Bash command writes into `.cc10x/workflows/` | Exit 2 only for a malformed artifact when `artifactIntegrity` is `"block"` (the shipped default); everything else audits |
| `PostCompact` | `cc10x_event_logger.py postcompact` | Records the compaction in the hook log and the workflow event log | Audit |
| `SubagentStop` | `cc10x_event_logger.py subagent_stop` | Logs whether a `cc10x:*` agent returned a contract; reads the final message, and the SubagentHandback report from the transcript when the final message has none (`report_source` records which) | Audit |
| `PreCompact` | `cc10x_state_persist.py precompact` | Snapshots workflow state before compaction | Persistence only |
| `Stop` | `cc10x_state_persist.py stop` | Snapshots workflow state when the session stops | Persistence only |
| `StopFailure` | `cc10x_event_logger.py stop_failure` | Logs API errors (async) | Audit |
| `InstructionsLoaded` | `cc10x_event_logger.py instructions_loaded` | Logs instruction file loads (async) | Audit |

### Which hooks block, which audit

- **Config-controlled** (`config/hook-mode.json`, values `"block"` or `"audit"`):
  `artifactIntegrity` is the one key, and it ships as `"block"`.
- **No hook gates git or file operations.** Claude Code's permission settings are
  the gate for git commands and file reads and writes.
- **Override location:** put a `hook-mode.json` with the same key in
  `${CLAUDE_PLUGIN_DATA}` to change a mode without editing the plugin; it survives
  plugin updates. A missing key, a value other than `block` or `audit`, or a corrupt
  file leaves the shipped value (an `invalid_hook_mode` event is logged for invalid
  input, once per problem and state of the file, tracked by a marker under
  `.cc10x/state/`; if the marker cannot be written the event is logged on every call).
  Any key other than `artifactIntegrity`, including the keys earlier versions shipped,
  is ignored and logs no event. The resolver never raises and always yields the one
  key, so a damaged file cannot silently turn `artifactIntegrity` off.
- **PostToolUse cannot undo a write.** Exit 2 from the artifact guard feeds its
  message to the model after the file is already on disk; the malformed artifact
  stays until the model repairs it, and the message says to repair it now.
- **Fail-open by design:** a hook that crashes, times out or cannot parse its
  input lets the tool call proceed. The hooks log the decisions they make and
  the failures they notice (an unreadable artifact, an invalid mode file, a
  failed snapshot write, a workflow event dropped because its
  id is unsafe (`workflow_id_unsafe`) or its append failed
  (`workflow_event_append_failed`)), but a hook that dies before it
  logs leaves only a trace in Claude Code's debug output.

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
`cwd`, and a relative hook-input `cwd` is made absolute.

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
