# Project Patterns
<!-- CC10X MEMORY CONTRACT: Do not rename headings. Used as Edit anchors. -->

## Architecture Patterns
- CC10x uses single entry point (cc10x-router) for all development tasks
- Skills are composable and loaded contextually based on detected patterns
- Agents run in chains with dependency management via Tasks
- Always-on AGENTS.md + CLAUDE.md symlink enforces router-first behavior

## Code Conventions
- Skill files use SKILL.md with YAML frontmatter
- Memory files in .claude/cc10x/ are updated via Edit (permission-free for existing files)
- Research files in docs/research/ with YYYY-MM-DD-topic-research.md naming

## File Structure
- Skills: plugins/cc10x/skills/<skill-name>/SKILL.md
- Research: docs/research/YYYY-MM-DD-topic-research.md
- Plans: docs/plans/YYYY-MM-DD-feature-plan.md
- Memory: .claude/cc10x/{activeContext,patterns,progress}.md

## Common Gotchas
- **[OBS-1 empty-answer critical gate]** AskUserQuestion returns empty 6x/session due to platform rendering issue. Router auto-defaulting on CRITICAL gates (REM-FIX creation, revert branch, task deletion) causes silent destructive actions. Fix: single "Empty Answer Guard" block in Router Contract Validation section + ⚠️ marker on 19 critical AskUserQuestion calls. Non-critical gates (Plan-First, PLAN-to-BUILD, research prompts) left unmarked — auto-default acceptable. Pattern: mark dangerous gates with ⚠️ → guard re-asks once then STOPs.
- **[OBS-15 code-reviewer output truncation]** Agent runs 20+ tool calls consuming 64-77K tokens but produces 0 chars of text output. NOT caused by parallel phase — happens in sequential mode too. Root cause: output token budget exhausted. Fix: OUTPUT_TRUNCATED pre-check in router (< 500 chars AND >= 10 tool calls → AskUserQuestion). Do NOT create REM-EVIDENCE — same truncation will recur.
- **[OBS-16 REM-EVIDENCE kill phrase]** "Your work is already saved to memory" causes LLM to immediately conclude its job is done and call TaskUpdate without doing any work (31K tokens, 30 chars, 1 tool call). Fix: remove that phrase; add "Re-read files you analyzed / Output ONLY YAML block / Do NOT call TaskUpdate until AFTER YAML". Applies to BOTH the REM-EVIDENCE TaskCreate description AND the chain execution re-invoke prompt.
- **[integration-verifier minimal output on PASS]** When all scenarios pass, agent emits only "Task N: COMPLETED" (same pattern as hunter CC10X-057/058). Fix: unconditional NO EXCEPTIONS rule in Task Completion: "PASS still requires full Router Contract YAML block." Pattern: every READ-ONLY agent needs this unconditional rule.
- **[hunter silent output — zero grep results CC10X-057/058]** Zero grep results on code patterns (try/catch/throw) in Markdown-only projects → LLM concludes "analysis complete, nothing found" → escape hatch "one sentence" interpreted as the completion line → 21-char output, no Router Contract. Fix: explicit Zero-results path in Process step 1 + unconditional NO EXCEPTIONS minimum output rule. Prevention: whenever adding grep-for-code-patterns steps to agents used on Markdown projects, add explicit zero-results fallback requiring full output format.
- **[escape hatch anti-pattern in LLM instructions]** "If X is complete but output is short: emit Y" creates ambiguous exception path. LLM interprets minimum Y ("one sentence") as sufficient, skipping Router Contract YAML. Pattern to avoid: conditional output-reduction clauses with a minimum lower than the full output format. Pattern to use: "NO EXCEPTIONS" unconditional clauses.
- **[parallel-phase IMPORTANT block ambiguity]** When an agent HAS Edit AND is in parallel phase, it hits bullet 4 ("prefer no memory edits") but bullet 5's "MUST include Memory Notes" only applies to agents WITHOUT Edit. If bullet 4's Memory Notes requirement is soft/embedded, the LLM interprets "parallel phase" as "minimize everything" → 21-char output. Fix: explicitly state "no memory edits = skip Edit() calls on memory files; analysis scope + output quality (≥200 chars) + Router Contract + Memory Notes are REQUIRED regardless."
- **[Tier 2 findings 2026-03-02]** M7 (VBC vs verifier overlap) is intentional defense-in-depth; M8 (Promotion Ladder) is aspirational guidance, not automated; M9 (gate retry counter) is in-context only — resets on compaction; M16 (confidence score) factors are self-assessed, not mechanically validated.
- Binary-verdict gates (PASS/FAIL) need explicit fallback: always add "treat output without PASS/FAIL as FAIL" rule
- Router CONTRACT RULE table must include ALL fields mentioned in agent CONTRACT RULE — missing fields are silently unenforced
- {placeholder} in Task() prompts: use explicit assignment syntax immediately before code block, not prose 'set X = ...' instruction
- Version bump checklist: (1) source `.claude-plugin/plugin.json` (2) cache `plugin.json` (3) `~/.claude/plugins/marketplaces/cc10x/.claude-plugin/marketplace.json` (metadata.version + plugins[0].version + description string) — all 3 must be updated
- [v6.0.38 smoke gotcha] grep -c zero-match pipe failure: use direct assignment COUNT=$(grep -c ... || echo "0") for absence checks
- [v6.0.38 cache gotcha] plugin.json: source at .claude-plugin/plugin.json; cache at root plugin.json — structural difference, not a sync error
- [Closed v7.0.0]: 4 v6.0.38-M deferreds resolved — router pre-skip delegated to gate, self-reflect Write() fallback, brainstorming explicit design_path assignment, escalation verbatim feedback
- [Deferred v6.0.33-M]: Research Loop Cap cross-session false trigger: rule 0c Research Loop Cap counts ALL docs/research/ entries in activeContext.md ## References — prior session entries accumulate and can trigger cap early. Same class as Cycle Cap/INVESTIGATING cross-session issues. Fix: scope count to current workflow only (e.g., only count entries added after current workflow start).
- [Deferred v6.0.32-M]: C-3 Cycle Cap cross-workflow false trigger: router SKILL.md:613 counts all-time completed REM-FIX; may false-trigger in new workflow if prior tasks persist in TaskList. Same class as Deferred #15. Fix: add workflow-scope filter (created_after workflow start) or delete completed REM-FIX tasks at workflow end.
- [Deferred v6.0.32-L]: H-2 residual at router SKILL.md:439 — explanatory note in Agent Invocation section still mentions "github-research" as SKILL_HINTS example, contradicting line 647 fix. Fix: remove github-research from the inline note at line 439.
- [Deferred #14]: Rule 2f (research re-invocation / BLOCKED state) has no loop cap — infinite re-invocation possible if BLOCKED status keeps returning; add count check like INVESTIGATING loop cap
- [Closed v6.0.37]: INVESTIGATING loop cap (Deferred #15) — confirmed removed in v6.0.30-6.0.33. Bug-investigator now self-terminates via STATUS: BLOCKED after research + still stuck. Loop cap not needed.
- [Deferred #31]: C-3 Pre-answers check uses 'cover all gaps' wording which is subjective — agents may interpret differently; line 266 in router; consider making criteria explicit
- [Deferred #32]: Rule 1b AskUserQuestion passes REMEDIATION_REASON directly without null guard — if REMEDIATION_REASON is null, user sees literal "null" in prompt; add ?? 'see agent output' guard
- [Deferred #33]: ROOT_CAUSE field used in rules 2c/2f (lines 558/568/572) without null guard — if ROOT_CAUSE is null, AskUserQuestion message shows "null"; add ?? 'unknown root cause' guard
- **`cp` alias trap**: macOS zsh aliases `cp` to `cp -i` (interactive) which blocks `-f`. Use `command cp -f` to bypass alias for cache sync.
- **Skills load via frontmatter, not conditional triggers**: All skills except github-research are in agent frontmatter `skills:` field. Don't add conditional Skill() calls for already-loaded skills.
- **Only github-research is conditional**: It's the only skill that requires external API and shouldn't always load. Other skills are cheap and always useful.
- **Sub-agents don't reliably execute bookkeeping**: Router must update task status after Task() returns - sub-agents may not call TaskUpdate
- **Task() return is the handoff point**: When Task() returns, router has control - this is deterministic, unlike sub-agent internal behavior
- **Pseudocode executes better than prose**: Complex logic (like remediation loops) should use pseudocode, not paragraphs
- Use Edit tool for memory updates (Write asks permission on existing files)
- Use Read tool not Bash(cat) for reading files
- Never use compound Bash commands (mkdir && cat) - asks permission
- Research without saving to docs/research/ is lost after context compaction
- **READ-ONLY agents (reviewer, hunter, verifier) cannot use mkdir or Edit** - they output Memory Notes for router to persist
- **WRITE agents (builder, investigator, planner) CAN use mkdir** - they have Edit tool
- **All READ-ONLY agents should read all 3 memory files** - activeContext, patterns, progress (for consistency)
- **Severity classification needs explicit rubric** - without it, same issue gets different severity in different sessions
- Tasks calls must match the Tasks tool contract exactly (schema + call-shape)
- Assume Tasks are schema-strict: do not rely on undocumented fields like `metadata`
- Tasks can be long-lived; CC10x must namespace/scope tasks (`CC10X ...` prefix)
- After any Edit to memory, always Read-back verify the intended change exists
- **Docs drift**: Always validate docs against actual source files (plugins/cc10x/skills, agents)
- **Agent consistency**: All agents should use `model: inherit` unless explicitly documented otherwise
- **Memory section names**: Use exact header names (`## Decisions` not "Active Decisions (table)")
- **External AI reviews hallucinate**: Always verify claims against actual source code before acting
- **Update flow**: Fix SOURCE (plugins/cc10x) first → then update DOCS (Bible) to match reality
- **Router/template sync**: When templates change, check if router's detection logic matches new format
- **Agents do NOT create CC10X TODO: tasks** — deferred findings go to Memory Notes under `**Deferred:**` key; router/Memory Update writes them to patterns.md and deletes any legacy TODO tasks
- **Butterfly effect check**: Before adding task prefix, trace the full execution path (dispatch, blockedBy, routing)
- **Grep ALL files after pattern change**: When changing a pattern (anchor, prefix), grep entire plugins/cc10x/ to find ALL occurrences
- **Template vs consumer sync**: When memory template changes (session-memory), check all skills/agents that EDIT those files
- **Documentation drift in guidance sections**: When template section names change, grep entire SKILL.md for old names in guidance text (not just Edit anchors)
- **READ-ONLY agents don't load session-memory**: code-reviewer, silent-failure-hunter, integration-verifier receive memory summary in prompt only — instructions added to session-memory won't reach them; fix must be in their own files
- **Double-trigger anti-pattern**: If instruction A says "execute X directly" and instruction B says "pass X as SKILL_HINTS hint", they contradict. Always check for this when adding SKILL_HINTS.
- **Router context bloat**: Router is the most-executed file — every addition is expensive. Prefer delegating to agent files or session-memory. Default: keep router lean, distribute logic.
- **[v6.0.33] addBlockedBy on completed tasks is a no-op**: when re-verification is needed, always create a NEW task — never try to reactivate a completed task by adding blockedBy.
- **[v6.0.33] Explicit dispatch rule for new CC10X task subjects**: every new subject pattern like "CC10X integration-verifier: Re-verify —" needs an explicit dispatch entry in chain loop step 2. LLM inference from subject text is fragile.
- **[v6.0.33] Self-referential fallback paradox**: when a conditional block fires on "X is absent," inner sub-conditions that check "if X exists" are unreachable dead code. Restructure: outer handles "found," inner handles "partially corrupt found," fallback handles "absent."
- **[v6.0.33] Loop caps via file-read count are more reliable than TaskList description filters**: TaskList description field = creation-time value only, NOT invocation PROMPT content. Use Read(activeContext.md) counts for loop caps when the counted artifact is written to memory each cycle.
- **[v6.0.33] Implicit template substitution comment pattern**: `# Replace {placeholder} with {variable_name}` comment immediately before pseudocode string literals containing template variables with non-obvious source.
- **Multi-condition boolean rule audit**: Each exclusion in a multi-part AND condition must have a named handler elsewhere (not just excluded from one rule). Trace the full execution path before adding/removing conditions.
- **REVIEW Memory Update omits Recent Changes REPLACE by design**: REVIEW produces no code changes — clobbering Recent Changes would erase legitimate history. BUILD and DEBUG correctly include it. This asymmetry is intentional.
- **[Cross-session task count class] TaskList() by status only**: Counts all-time tasks — no workflow scope. Both Cycle Cap (completed) and INVESTIGATING loop cap (in_progress/completed) have this issue. Fix pattern: filter by created_after workflow start OR delete completed tasks at workflow end.
- **[SKILL_HINTS prose grep] After removing from Sources table**: grep entire file for inline explanatory notes referencing the removed skill — they'll silently contradict the table fix.
- **4-parallel-agent investigations work well**: Different perspective prompts (Memory Architect, Chain Tracer, Failure Mode Investigator, Simplicity Auditor) surface different failure modes

- **[v7.8.0 build] OBS-15 conditional frontend skill: trigger list .tsx,.jsx,.vue,.css,.scss,.html — intentionally excludes .ts** (backend TypeScript should not trigger frontend skill load; .ts exclusion is more correct than plan specified)
- **[v7.8.0 build] OBS-9 pkill logging gap** — Chain Execution Loop step 3 adds TEST_PROCESSES_CLEANED pkill but does NOT include the log output required by Gate 9 definition ("log result: 'Killed: [names]' or 'None found'"). Non-blocking cosmetic gap — log consistency deferred.
- **[Deferred v7.8.0-M1] OBS-9 pkill log consistency** — Add `|| echo 'No test processes found'` to pkill line in Chain Execution Loop step 3 for log consistency with Gate 9 definition
- **[Deferred v7.8.0-M3] Output skeleton placeholder** — Replace `[list from prompt context]` in code-reviewer step 0 skeleton with deterministic text: `Starting code review. Checking: security, patterns, TDD compliance, architecture.` (remove dynamic file list placeholder that may produce literal text)
- **[Deferred v7.8.0-M4] Conditional frontend skill git-repo guard** — Add git-repo guard: `git rev-parse --is-inside-work-tree 2>/dev/null && git diff HEAD --name-only || git diff --name-only` (currently silently skips if not in git repo)
- **[Deferred v7.8.0-L] Router line count 844 vs ≤840 soft target** — 4 lines over; trim 2 blank lines in step 4a code block if hard constraint ever required
- **[v7.8.0 plan] Planner agent may pass plan-review-gate (GATE_PASS) without writing plan file to disk** — 51 tool calls, 109K tokens, gate passed, but no file on disk. Cause unknown (likely token budget or Write() call at end of long agent run failed silently). Fix: router should verify plan file exists on disk after planner completes (Glob check before proceeding to PLAN-to-BUILD gate). Workaround used: write plan directly in router context.
- **[v7.8.0 plan] Stale "see agent file" notes in router** — When a section moves from agent to router, grep ALL router references to that agent/feature to find stale notes. Pattern: `grep -c "writes its own.*FEATURE" router` should be 0 after move.
- **[v7.8.0 plan] DEBUG-RESET move: router now writes marker** — As of v7.8.0 plan, router writes `[DEBUG-RESET: wf:{workflow_task_id}]` in DEBUG step 4a. Bug-investigator section removed. Pattern mirrors BUILD-START and PLAN-START (both router-written).

## Memory Patterns
- Every skill that produces artifacts must save AND update memory
- activeContext.md is the index, docs/research/ and docs/plans/ are the artifacts
- Research References table links topic → file → key insight
- Memory files are contracts: do not rename headings; always Edit then Read-back verify
- Agents without Edit/Write access should surface memory-worthy notes in output so the main assistant can persist them
- Avoid concurrent memory edits during parallel phases (prefer updating memory after the parallel phase completes)

## Project SKILL_HINTS
<!-- auto-populated: cc10x is the project being developed; no external domain skills needed -->

## Dependencies
- Octocode MCP: External code research
- Context7 MCP: Library documentation (fallback)
- Tasks system: Workflow orchestration with dependencies
