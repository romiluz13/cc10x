# Research: cc10x Plugin Compliance Audit vs. Anthropic's Claude Code Docs

## Important caveat on methodology (read first)

My assigned toolset for this task contained **no `web_search`/`fetch` tool** — only `read`, `write`, `intercom`, `contact_supervisor`. I flagged this to the supervisor (via `contact_supervisor`, `need_decision`) and got no reply within the wait window, so per my stated fallback I proceeded with:
1. **Direct, verified reads** of the actual local plugin files (manifest, hooks.json, agent/skill frontmatter) — this evidence is 100% verified against the real repo.
2. **Best-effort recall** of Anthropic's Claude Code hooks/plugin/subagent/skill documentation, from training knowledge that predates the current date (2026-07-05) by a meaningful margin. I could not fetch live doc pages to confirm exact current wording, newly added events, or renamed fields.

**Every doc-derived claim below is marked `[TRAINING-KNOWLEDGE, UNVERIFIED-LIVE]`** rather than cited to a freshly-fetched URL. Given Claude Code's hooks/plugins system has been actively evolving, treat every "non-standard" verdict as a strong, actionable hypothesis that **must be re-checked against the live docs at docs.claude.com/en/docs/claude-code/hooks and .../plugins before shipping or removing anything** — not as a final ruling. This is the single biggest gap in this audit and I want it to be impossible to miss.

## Summary

Based on the local file evidence, cc10x v12.4.0 ships a `hooks.json` with **9 hook event names**, at least **4 of which (`TaskCompleted`, `PostCompact`, `StopFailure`, `InstructionsLoaded`) do not match any hook event name I have reliable trained knowledge of as documented by Anthropic** — the canonical, long-documented set I recall is `PreToolUse`, `PostToolUse`, `Notification`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `SessionStart`, and (added later) `SessionEnd`. If my recollection is still accurate as of 2026-07-05, hooks registered under undocumented event names are silently never invoked by Claude Code — a CRITICAL, high-value finding for this audit. The `statusMessage` field applied to every hook entry and the `async: true` field on two hook entries are also **not part of the hook schema I have knowledge of**, and agent frontmatter fields `effort` and `color` are similarly outside the documented agent-frontmatter schema I recall — though `model`, `tools`, `name`, `description` are solid. **All of this must be confirmed against live docs before treating it as fact.**

## Findings

### A. Verified local evidence (100% confirmed by direct file reads, not docs)

1. **Plugin manifest** (`/Users/rom.iluz/Dev/cc10x/plugins/cc10x/.claude-plugin/plugin.json`) has `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords` — matches the general shape of plugin manifests I've seen documented, no unusual fields.
2. **Marketplace manifest** (`/Users/rom.iluz/Dev/cc10x/.claude-plugin/marketplace.json`) has `name`, `owner`, `metadata{description,version}`, `plugins[]` with `name/description/version/author/homepage/repository/license/keywords/category/source`. Shape is consistent with Anthropic's documented marketplace.json convention (a repo-level manifest listing one or more `source`-pointed plugin dirs).
3. **hooks.json actual content** (verified read of `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/hooks/hooks.json`) registers hook arrays for: `PreToolUse`, `SessionStart`, `PostToolUse`, `TaskCompleted`, `PostCompact`, `SubagentStop`, `PreCompact`, `Stop`, `StopFailure`, `InstructionsLoaded`. Every single hook entry (all 9 events, all 10 hook objects) carries a `statusMessage` string field, and 2 entries (`StopFailure`, `InstructionsLoaded`) additionally carry `"async": true`.
4. **planner.md agent frontmatter**: `name, description, model: inherit, color: cyan, effort: high, tools: [Read, Edit, Write, Bash, Grep, Glob, Skill, LSP, WebFetch, TaskUpdate], skills: [...]`.
5. **plan-gap-reviewer.md agent frontmatter**: `name, description, model: inherit, color: purple, effort: high, tools: [Read, Grep, Glob, LSP]` — no `skills:` key, and the body explicitly documents an intentional "no inherited skills/context, anti-anchoring" design pattern implemented purely via prompt instructions (not a schema-level "fresh context" flag).
6. **cc10x-router SKILL.md frontmatter**: only `name` and `description` (a long multi-line string used for auto-trigger matching via keywords embedded in the description) — no `allowed-tools` or other fields present in this file.

### B. Hook event names — documented vs. suspect (TRAINING-KNOWLEDGE, UNVERIFIED-LIVE)

1. **`PreToolUse`, `PostToolUse`** — REAL, long-documented core hook events (fire before/after tool calls; support `matcher` regex against tool name, and JSON stdout with `decision`/`permissionDecision`/`reason` fields to allow/deny/ask). High confidence this is still correct. [TRAINING-KNOWLEDGE]
2. **`SessionStart`** — REAL, documented event firing on session start/resume/compact, with a `matcher` field supporting values like `startup`, `resume`, `compact` (matches what cc10x uses). High confidence. [TRAINING-KNOWLEDGE]
3. **`Stop`** — REAL, documented event firing when the main agent loop is about to stop; hook output can force continuation via `decision: "block"` + `reason`. High confidence. [TRAINING-KNOWLEDGE]
4. **`SubagentStop`** — REAL, documented event, analogous to `Stop` but scoped to a subagent (Task tool) run finishing. High confidence. [TRAINING-KNOWLEDGE]
5. **`PreCompact`** — REAL, documented event firing immediately before context compaction, used for pre-compaction snapshotting (exactly the use cc10x makes of it). High confidence. [TRAINING-KNOWLEDGE]
6. **`TaskCompleted`** — **NOT part of the documented hook event vocabulary I have knowledge of.** The closest real, documented events touching subagent/task completion are `SubagentStop` (subagent finished) and `Stop` (main loop finished) — there is no separate "task completed" lifecycle event in the schema I know of. **Verdict: likely NON-STANDARD/invented.** If true, `cc10x_task_completed_guard.py` never runs. **This must be re-verified live — it is the single highest-value thing to check first**, since cc10x's entire "task metadata guard" enforcement depends on it firing.
7. **`PostCompact`** — I only have knowledge of `PreCompact` being documented; I do not recall a documented `PostCompact` counterpart. **Verdict: likely NON-STANDARD/invented** (possibly the plugin author assumed a Pre/Post symmetry that doesn't exist in the real API, the way it exists for `PreToolUse`/`PostToolUse`). If true, `cc10x_event_logger.py postcompact` never fires.
8. **`StopFailure`** — I have no knowledge of a documented `StopFailure` event; `Stop` is documented, but a distinct "stop due to failure" variant is not something I recall existing. **Verdict: likely NON-STANDARD/invented.**
9. **`InstructionsLoaded`** — I have no knowledge of a documented `InstructionsLoaded` event at all — nothing resembling "instructions/system-prompt loaded" appears anywhere in the hook event vocabulary I know of. **Verdict: likely NON-STANDARD/invented.**
10. **`Notification`, `UserPromptSubmit`, `SessionEnd`** — these are events I recall as documented but that cc10x does **not** use at all; not a compliance problem, just noting cc10x's hook surface doesn't touch them.

**Net read on hook events:** of the 9 event names cc10x registers, 5 (`PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStop`, `PreCompact` — six, not five) look solid, and 4 (`TaskCompleted`, `PostCompact`, `StopFailure`, `InstructionsLoaded`) are suspect enough that I'd bet real money they are silently dead hook registrations under the real Claude Code runtime — **but this is trained-knowledge inference, not a live-verified fact, and is exactly the kind of claim that needs a 5-minute live doc check before you trust it enough to delete code.**

### C. Hook-entry fields — `statusMessage` and `async`

11. **`statusMessage`** — I do not recall this as a documented field on hook command objects. The field I associate with user-facing hook status text is closer to a `systemMessage` field returned in a hook's JSON **stdout output** (not a static field in the hooks.json *registration* itself). cc10x applies `statusMessage` as a static config-time field on every single hook entry in hooks.json, which doesn't match the pattern I recall (where user-facing messaging is a per-invocation JSON output field, not a manifest-time string). **Verdict: likely a non-standard/invented field that Claude Code ignores at hook-registration time** — probably harmless (unknown JSON keys are typically ignored rather than causing a parse failure) but almost certainly a no-op, meaning the "friendly labels" cc10x intends to surface to users likely never appear. Needs live verification.
12. **`async: true`** — I do not recall an `async` field on hook command objects in the documented schema. My recollection of the hook execution model is that each hook command runs synchronously up to its `timeout`, and the framework does not expose a fire-and-forget "async" mode as manifest config. **Verdict: likely non-standard/ignored field** — if so, `StopFailure`/`InstructionsLoaded` hooks (which are moot anyway per finding B.8/B.9) would run synchronously (blocking up to their timeout) rather than async, contrary to the plugin author's intent, on top of likely never firing at all.

### D. Exit code semantics (general schema knowledge, for context)

13. My trained understanding of exit-code semantics for hooks (**verify live**): exit code `0` = success, stdout may be shown to the user in transcript/verbose mode but is not otherwise consumed specially; exit code `2` = blocking error — for `PreToolUse` this **blocks the tool call** and feeds stderr back to Claude as the reason; for `PostToolUse`/`Stop`/`SubagentStop` a blocking exit surfaces the error to Claude to react to; any other non-zero exit code = non-blocking error shown to the user only, tool call proceeds. This is a general schema note, not something I can confirm cc10x's own hook scripts implement correctly without reading `cc10x_pretooluse_guard.py` et al. (out of scope for this pass — I only read hooks.json, not the referenced Python scripts).

### E. Subagent (`agents/*.md`) frontmatter fields

14. **`name`, `description`, `model`, `tools`** — REAL, documented core fields for the `agents/` directory subagent frontmatter schema (Task-tool-invoked agents). High confidence. [TRAINING-KNOWLEDGE]
15. **`color`** — I recall `color` as a real, supported cosmetic field (affects how the subagent is rendered/labeled in the transcript UI) — plausible but lower confidence than the core fields above; should be double-checked live since it's a UI-cosmetic field that could have been added/removed across versions.
16. **`effort: high`** — I do **not** have confident recollection of an `effort` field being part of the documented subagent frontmatter schema. This may be a cc10x-invented convention layered on top of the real schema (likely intended as an instruction to the agent prompt itself rather than a schema field Claude Code's runtime interprets) rather than an API Claude Code enforces. **Needs live verification**; if unsupported, it's presumably inert (extra YAML keys generally get ignored) rather than breaking, but it would not do anything the plugin author might believe it does (e.g., mapping to an actual "thinking budget"/reasoning-effort API parameter).
17. **`skills:`** (a list under agent frontmatter, e.g. `planner.md`'s `skills: [cc10x:agent-common, cc10x:planning, cc10x:architecture]`) — I have some recollection of subagents being able to declare skill dependencies to auto-load, but I'm not fully confident this specific `skills:` frontmatter key (as opposed to referencing skills in the prompt body) is the documented mechanism vs. a plugin-author convention. Needs live verification.
18. **No `maxTurns` or explicit "thinking level" field** (e.g., no `thinking:` key) appears in either agent file read — so I can't assess those against docs; not present, not a finding either way.
19. **"Fresh/no-inherited-context" behavior** (plan-gap-reviewer.md): The file's approach to anti-anchoring is implemented entirely via **prose instructions in the markdown body** ("do NOT load `.cc10x/*.md`", "do NOT infer authority from prior planner confidence") rather than any schema-level "no context inheritance" flag. This matches my recollection that Claude Code subagents invoked via the Task tool **do get a fresh context window by default** (they don't inherit the parent conversation's full history automatically) but any additional isolation (e.g., not reading specific repo files) has to be enforced by agent prompt instructions, not a config flag — so cc10x's approach here is consistent with what I understand of the real mechanism, though this should be double-checked for whether newer Claude Code versions expose an explicit context-isolation flag that would be a stronger guarantee than prose.

### F. Skills (`SKILL.md`) frontmatter and directory conventions

20. **`name`, `description`** — REAL, core documented SKILL.md frontmatter fields; `description` is what drives auto-invocation/triggering via semantic + keyword matching against the user's request. cc10x-router's SKILL.md leans heavily on this by cramming an explicit trigger-keyword list into the description string — consistent with the documented "description drives auto-trigger" mechanism, just an aggressive/dense implementation of it.
21. **`allowed-tools` (or similar tool-restriction field)** — not present in the one SKILL.md file read; I recall this as a real, documented optional field for skills, but cc10x-router doesn't use it (not a compliance defect, just an unused optional feature).
22. **`references/` and `evals/` subfolders** — I could not verify from the single file read whether these exist in cc10x's skill directories (not read in this pass), and I do not have confident recollection that `references/`/`evals/` are an official Anthropic-documented convention for the Skills directory structure (as opposed to a general "skills can bundle supporting files" allowance, where the subfolder naming itself is left to the author). **My best guess: these are very likely a cc10x-specific convention layered on top of a more general "skills may include supporting files/folders" allowance, not an Anthropic-mandated folder name** — but I did not confirm this by reading the actual skill folders, so treat this specific item as a low-confidence guess pending both a live-doc check and a local directory listing.

## Sources

- Kept: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/.claude-plugin/plugin.json` (direct read) — ground truth for plugin manifest fields.
- Kept: `/Users/rom.iluz/Dev/cc10x/.claude-plugin/marketplace.json` (direct read) — ground truth for marketplace manifest fields.
- Kept: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/hooks/hooks.json` (direct read) — ground truth for the exact hooks currently shipped, confirms the task's provided excerpt and reveals `statusMessage` is applied to literally every hook entry (not just some).
- Kept: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/planner.md`, `plan-gap-reviewer.md` frontmatter (direct reads) — ground truth for actual agent frontmatter fields in use.
- Kept: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md` frontmatter (direct read) — ground truth for actual skill frontmatter fields in use.
- **Not used / unavailable**: `docs.claude.com/en/docs/claude-code/hooks`, `.../sub-agents`, `.../skills`, `.../plugins`, and the Claude Code GitHub changelog — I had no `web_search`/`fetch` tool in this session to retrieve these live. All doc-derived claims above are trained-knowledge recollections only, explicitly flagged as such.
- Dropped: none (no low-quality sources encountered — the only sourcing problem is the missing live-fetch capability, not source quality).

## Gaps

1. **The entire live-doc-verification layer is missing.** This is the most important open item: every "likely non-standard" verdict in section B and C (`TaskCompleted`, `PostCompact`, `StopFailure`, `InstructionsLoaded`, `statusMessage`, `async`) needs a 10-minute check against `docs.claude.com/en/docs/claude-code/hooks` (and the GitHub changelog for any recently-added events) before cc10x's maintainer acts on it. If any of these turn out to be real (e.g., Anthropic may have shipped new hook events like `PostCompact`/`TaskCompleted` after my training cutoff, given how actively this surface has evolved), the "critical finding" framing would need to be walked back for that specific event.
2. **Agent-frontmatter `effort` and `color` fields** — not verified live; recommend checking the current subagent frontmatter schema doc page directly.
3. **`references/`/`evals/` skill subfolder convention** — not verified against docs, and I did not even list the actual skill directory contents locally (only read one SKILL.md file), so this claim is the weakest in the report; recommend both a local `ls` of `plugins/cc10x/skills/*/` and a doc check.
4. **Hook Python scripts themselves were not read** (`cc10x_pretooluse_guard.py`, `cc10x_task_completed_guard.py`, etc.) — exit-code behavior and stdout/JSON output contracts implemented by cc10x's own scripts vs. what Claude Code expects were not audited; only the hooks.json registration layer was reviewed.
5. **Suggested next step for whoever owns this repo**: run a live fetch of the hooks doc page, diff the confirmed current event list against cc10x's 9 registered events, and if `TaskCompleted`/`PostCompact`/`StopFailure`/`InstructionsLoaded` are indeed non-existent, either (a) remove those hook registrations as dead weight, or (b) if the intended behavior maps to a real event (e.g., `TaskCompleted` intent might really need `SubagentStop`, `PostCompact` intent might really need to be handled inside `PreCompact` since there's no post-hook), rewire them to the real event names so the guards actually execute.

## Overall Verdict

**Based on trained knowledge only (not live-verified — see caveat above), cc10x has real compliance risk, and it is exactly the kind of risk this audit was designed to catch.** The core hook surface (`PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStop`, `PreCompact`) and core plugin/agent/skill manifest fields (`name`, `description`, `model`, `tools`, plugin.json/marketplace.json shape) appear to align with genuine, long-standing Claude Code APIs. But **4 of the plugin's 9 hook.json event registrations (`TaskCompleted`, `PostCompact`, `StopFailure`, `InstructionsLoaded`) do not match any documented hook event name in my knowledge, and 2 hook-entry fields (`statusMessage` on every single hook, `async` on two) do not match the documented hook schema** — meaning it is plausible that roughly 40% of cc10x's enforcement/logging hook surface (its "task metadata guard," "failure event logging," "instruction audit," and "compaction event capture" features) silently never executes under the real Claude Code runtime, and that its "friendly status label" and "async execution" intentions are no-ops even where the parent event is real. **This verdict is not final — it must be confirmed with a live doc fetch before cc10x's maintainer treats it as ground truth**, but given the pattern (4 suspicious events out of 9, all clustered around exactly the newer/more speculative lifecycle concepts — task completion, post-compaction, stop-failure, instruction-loading — rather than the well-established ones), the prior probability that this is genuine drift/invention rather than a documentation gap on my end is high enough to warrant immediate live verification before the next release.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Delivered the requested documentation/spec compliance research brief in the exact structure requested (Steps 1-3): gathered/recalled authoritative Claude Code hook/plugin/subagent/skill facts, directly read all specified local files (plugin.json, marketplace.json, hooks.json, planner.md, plan-gap-reviewer.md, cc10x-router SKILL.md frontmatter), and produced a per-hook-event compliance verdict (TaskCompleted, StopFailure, InstructionsLoaded, PostCompact flagged as likely non-standard; PreToolUse/PostToolUse/SessionStart/Stop/SubagentStop/PreCompact confirmed as real) plus a verdict on statusMessage/async fields and agent-frontmatter fields (effort, color), ending with an overall verdict. No scope was added beyond the requested audit; no files were written, matching the read-only research task type despite the generic write-task acceptance template."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/.claude-plugin/plugin.json",
      "result": "passed",
      "summary": "Confirmed plugin manifest fields: name, version, description, author, homepage, repository, license, keywords"
    },
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/.claude-plugin/marketplace.json",
      "result": "passed",
      "summary": "Confirmed marketplace manifest shape with plugins[] array and source pointer"
    },
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/hooks/hooks.json",
      "result": "passed",
      "summary": "Confirmed exact hook registrations: 9 events, statusMessage on all entries, async on 2 entries"
    },
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/planner.md (first 30 lines)",
      "result": "passed",
      "summary": "Confirmed frontmatter fields: name, description, model, color, effort, tools, skills"
    },
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/plan-gap-reviewer.md (first 30 lines)",
      "result": "passed",
      "summary": "Confirmed frontmatter fields and anti-anchoring prose-based (not schema-based) context isolation design"
    },
    {
      "command": "read /Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md (first 50 lines)",
      "result": "passed",
      "summary": "Confirmed minimal frontmatter (name, description only) with dense keyword-loaded description for auto-trigger"
    },
    {
      "command": "contact_supervisor(need_decision) re: missing web_search tool",
      "result": "no reply within 10 min",
      "summary": "Proceeded per stated fallback plan using caveated trained-knowledge doc claims"
    }
  ],
  "validationOutput": [
    "All local file reads succeeded and match the hooks.json excerpt provided in the task verbatim (plus revealed statusMessage present on every entry, not just some, and async on 2 entries).",
    "No live web verification was possible in this session (no web_search/fetch tool available) — all doc-derived claims are explicitly marked TRAINING-KNOWLEDGE/UNVERIFIED-LIVE in the brief and flagged as the top residual risk."
  ],
  "residualRisks": [
    "HIGH: Doc claims about which hook events are real (TaskCompleted, PostCompact, StopFailure, InstructionsLoaded flagged as likely non-standard) are based on trained knowledge only, not a live fetch of docs.claude.com — must be verified before acting (e.g., removing hooks).",
    "MEDIUM: statusMessage and async hook-entry field verdicts are similarly unverified live.",
    "MEDIUM: effort and color agent-frontmatter field verdicts are similarly unverified live.",
    "LOW-MED: references/evals skill subfolder convention claim is a low-confidence guess; actual skill directory contents were not listed/read in this pass.",
    "LOW: Hook Python scripts (cc10x_pretooluse_guard.py etc.) were not read, so exit-code/stdout contract compliance of the scripts themselves was not audited, only the hooks.json registration layer."
  ],
  "noStagedFiles": true,
  "diffSummary": "No files changed; read-only research/audit task. No repository modifications made.",
  "reviewFindings": [
    "no blockers — this is a research deliverable, not a code change"
  ],
  "manualNotes": "Tooling gap: this subagent session had no web_search/fetch tool despite the task requiring live doc verification. Escalated via contact_supervisor(need_decision) and received no reply within the wait window, so proceeded per the stated fallback (local file audit fully verified; doc claims caveated as trained-knowledge/unverified-live). Recommend the parent orchestrator re-run the doc-verification portion with a session that has live web access before treating the 'likely non-standard hook event' findings as final, since that determination is the single highest-value, highest-risk claim in this report and directly actionable (could mean deleting/rewiring ~40% of cc10x's hook surface)."
}
```