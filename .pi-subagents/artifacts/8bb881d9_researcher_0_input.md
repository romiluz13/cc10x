# Task for researcher

You are auditing a Claude Code plugin called 'cc10x' for compliance with Anthropic's OFFICIAL Claude Code documentation. This is a documentation/spec compliance audit. Do NOT write any files. Do NOT use intercom, contact_supervisor, or ask any clarifying questions — proceed autonomously using your best judgment on any ambiguity, and note assumptions in your final report. Just research and answer directly as your final message.

Research Anthropic's official Claude Code docs (docs.claude.com/en/docs/claude-code, or the Claude Code GitHub repo/CHANGELOG) on these specific mechanisms, then answer the compliance questions below:

1. Plugin system: plugin.json / marketplace manifest schema — required/optional fields, plugin directory conventions (agents/, skills/, hooks/, commands/).
2. Hooks: the full list of VALID, currently-documented hook event names. Specifically: are "TaskCompleted", "StopFailure", and "InstructionsLoaded" REAL documented Claude Code hook events, or are they non-standard/invented names that Claude Code will never actually fire? (The real documented set as of recent Claude Code versions includes things like PreToolUse, PostToolUse, Notification, UserPromptSubmit, Stop, SubagentStop, PreCompact, SessionStart, SessionEnd — confirm the exact current list and flag any name in cc10x's hooks.json that doesn't match.) Also confirm: is "PostCompact" a real event, or is the real name different (e.g. does compaction only have PreCompact, with post-compaction context restoration handled via SessionStart with a \"compact\" matcher/source instead)? What is the exact JSON schema for hooks.json (matcher syntax, hooks[].type values, command, timeout, and is \"statusMessage\" a real supported field, is \"async\" a real supported field on a hook entry)? What do hook exit codes 0/1/2 mean, and how is stdout consumed by Claude Code for each hook type (does it block the action, get shown to the user, get fed to the model)?\n3. Subagents: the agents/ directory frontmatter schema — which fields are real and supported today (name, description, tools, model, color, and is there a real \"thinking level\"/\"effort\" field)? How are subagents invoked (Task tool)? Can a subagent be configured to run with NO inherited context reliably via frontmatter (e.g. omitting a \"skills\" field), or is this purely a prompting convention with no real isolation guarantee?\n4. Skills: SKILL.md frontmatter schema (name, description, allowed-tools/tools field) and how skill auto-invocation actually works (description-based matching by the model, not a deterministic mechanism) — confirm this is genuinely how it works, since this matters for whether cc10x's router-driven dispatch model is even reliable.\n\nThe ACTUAL current hooks.json in this plugin registers hooks for these event names: PreToolUse (matcher Edit|Write, and matcher Bash), SessionStart (matcher startup|resume|compact), PostToolUse (matcher Edit|Write), TaskCompleted (no matcher), PostCompact (no matcher), SubagentStop (no matcher), PreCompact (no matcher), Stop (no matcher), StopFailure (no matcher, async:true), InstructionsLoaded (no matcher, async:true). Hook commands use \"timeout\" and some use \"statusMessage\" and \"async\" fields.

Produce a compliance report. For EACH of the 10 hook event names listed above, state explicitly: REAL/CURRENT, DEPRECATED/RENAMED (give the correct current name), or NON-STANDARD/INVENTED (cite doc evidence). Do the same for the \"statusMessage\" and \"async\" hook-entry fields, and for agent-frontmatter fields (name, description, tools, model, color, any thinking/effort field). Cite specific doc sections/URLs for each claim you make. End with an overall verdict: is this plugin using real, current Claude Code APIs throughout, or are there hooks/fields that will silently never fire / never take effect?

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