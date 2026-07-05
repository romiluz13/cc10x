# Task for researcher

You are auditing a Claude Code plugin called 'cc10x' for compliance with Anthropic's OFFICIAL Claude Code documentation. This is a documentation/spec compliance audit, not a general research task. Do not write any files.

Step 1: Research and gather authoritative facts from Anthropic's official Claude Code docs (docs.claude.com/en/docs/claude-code or claude.com/product/claude-code documentation, and the Claude Code GitHub repo/changelog if useful) on these specific mechanisms:
- Plugin system: plugin.json / marketplace manifest schema, required/optional fields, plugin directory conventions (agents/, skills/, hooks/, commands/)
- Hooks: the full list of valid hook event names (PreToolUse, PostToolUse, SessionStart, SessionEnd, Stop, SubagentStop, PreCompact, PostCompact, Notification, UserPromptSubmit, PermissionRequest/PermissionDecision or similar, and whether 'TaskCompleted', 'StopFailure', 'InstructionsLoaded' are REAL documented hook events or non-standard/undocumented ones). Exact JSON schema for hooks.json (matcher syntax, hooks[].type, command, timeout, async, statusMessage field — is statusMessage a real supported field?). Exit code semantics: what does exit code 0 vs 1 vs 2 mean for each hook type, and how does stdout get consumed (does the model see it, does it block the tool call, etc.)?
- Subagents: the 'agents/' directory frontmatter schema (name, description, tools, model, color, thinking level fields — what's actually supported today), how subagents get invoked (Task tool), context inheritance behavior, whether a subagent can be told to run with 'no inherited context' / fresh context reliably.
- Skills: SKILL.md frontmatter schema (name, description, allowed-tools or similar), how skill auto-invocation/triggering actually works (description-based matching), directory conventions for references/ and evals/ subfolders (are these an Anthropic convention or purely custom to this plugin?).
- Slash commands / any other plugin surface relevant to orchestration.

Step 2: I'm giving you the ACTUAL current hooks.json content from this plugin to check against what you learn:

```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "python3 ...cc10x_pretooluse_guard.py", "timeout": 10, "statusMessage": "CC10X protected-write guard"}]}, {"matcher": "Bash", "hooks": [{"type": "command", "command": "python3 ...cc10x_git_guard.py", "timeout": 5, "statusMessage": "CC10X git guardrails"}]}],
    "SessionStart": [{"matcher": "startup|resume|compact", "hooks": [{"type": "command", "command": "python3 ...cc10x_sessionstart_context.py", "timeout": 10}]}],
    "PostToolUse": [{"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "python3 ...cc10x_posttooluse_artifact_guard.py", "timeout": 10}]}],
    "TaskCompleted": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_task_completed_guard.py", "timeout": 10}]}],
    "PostCompact": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_event_logger.py postcompact", "timeout": 10}]}],
    "SubagentStop": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_event_logger.py subagent_stop", "timeout": 10}]}],
    "PreCompact": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_state_persist.py precompact", "timeout": 5}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_state_persist.py stop", "timeout": 3}]}],
    "StopFailure": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_event_logger.py stop_failure", "timeout": 3, "async": true}]}],
    "InstructionsLoaded": [{"hooks": [{"type": "command", "command": "python3 ...cc10x_event_logger.py instructions_loaded", "timeout": 5, "async": true}]}]
  }
}
```

Also read these local files directly for their frontmatter (use your `read` tool, absolute paths):
- /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/planner.md (read first ~30 lines for frontmatter)
- /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/plan-gap-reviewer.md (first ~30 lines)
- /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md (first ~50 lines for frontmatter)
- /Users/rom.iluz/Dev/cc10x/plugins/cc10x/.claude-plugin/ (read whatever manifest json is there — try plugin.json or marketplace.json)

Step 3: Produce a compliance report. For EACH hook event name used (TaskCompleted, StopFailure, InstructionsLoaded, PostCompact, PreCompact, SubagentStop especially), explicitly state whether it is a REAL, currently-documented Claude Code hook event, a deprecated/renamed one, or appears to be NON-STANDARD/invented (this matters a lot — if cc10x is shipping hooks.json entries for events Claude Code doesn't actually fire, those hooks silently never run, which would be a CRITICAL finding). Do the same for the 'statusMessage' and 'async' fields in the hook definitions, and for any agent-frontmatter fields you weren't sure are real (e.g. 'effort', 'maxTurns', 'color', a specific 'thinking level' field name). Cite the specific doc URL/section for each claim. End with an overall verdict: is this plugin using real, current Claude Code APIs throughout, or are there compliance risks that could mean parts of it silently don't work?

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```