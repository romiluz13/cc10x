# cc10x Hooks

This directory now serves two different purposes:

1. **Plugin runtime hooks** via `hooks.json`
   - `PreToolUse` — protected writes guard
   - `SessionStart` — workflow resume context
   - `PostToolUse` — workflow artifact integrity audit
   - `TaskCompleted` — task metadata validation
   - `PostCompact` — compaction event capture
   - `SubagentStop` — agent contract presence audit
   - `PreCompact` — workflow state snapshot before compaction
   - `Stop` — workflow state snapshot on session stop
   - `StopFailure` — API error logging (async)
   - `InstructionsLoaded` — instruction file load audit (async)
2. **Optional git pre-commit helper** via `pre-commit`

## Plugin Runtime Hooks

When CC10X is installed as a Claude Code plugin, Claude Code reads `hooks/hooks.json`
from the plugin bundle and runs the referenced scripts from `${CLAUDE_PLUGIN_ROOT}/scripts`.

The shipped runtime hooks are intentionally minimal and audit-first. Be
precise about what blocks and what only logs (`config/hook-mode.json`):

**Blocking** (the only two enforcement points):
- workflow-artifact integrity after writes — a malformed or key-missing
  artifact write exits 2 (`artifactIntegrity: "block"`)
- git guardrails — push/reset-hard/clean/branch-D/checkout-dot are denied
  unless a fresh single-use approval token covers the operation

**Audit-only** (log lines, never denials — `"audit"` in hook-mode.json):
- direct memory markdown writes (flip `memoryWrites` to `"block"` to deny)
- CC10X task metadata + memory-finalization evidence on task completion
  and the remediation circuit-breaker backstop (flip `taskMetadata`)

**Context/telemetry** (no enforcement role):
- inject workflow resume context on session start
- snapshot workflow state before compaction and on session stop
- log API failures and instruction file loads for telemetry

## Internal Publication Audit

The plugin also ships an internal drift check:

```bash
python3 plugins/cc10x/tools/harness_audit.py
```

It validates the publication-critical contract:
- plugin manifest version matches `README.md` and `CHANGELOG.md`
- marketplace metadata matches the shipped plugin version
- plugin hooks and MCP names referenced by docs/router actually exist
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
