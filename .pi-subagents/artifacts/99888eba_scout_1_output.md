# Deep Analysis: addyosmani/agent-skills — Agents, Hooks, Commands, and Infrastructure vs cc10x

## Executive Summary

addyosmani/agent-skills is a **markdown-first plugin** for Claude Code that provides 4 personas (agents), 4 hook scripts (with 2 test scripts), and 8 slash commands. It is philosophically different from cc10x: it is a **human-facing workflow guide** (skills + commands tell the agent *how to work*), whereas cc10x is a **machine-enforced workflow engine** (agents emit structured contracts, hooks guard artifacts, a router orchestrates phases). The two complement each other — addyosmani brings domain expertise and UX patterns; cc10x brings enforcement and telemetry.

---

## 1. Agent Comparison: addyosmani (4) vs cc10x (9)

### addyosmani Agents

| Agent | Role | Key Pattern |
| ------- | ------ | ------------- |
| code-reviewer | Five-axis code review (correctness, readability, architecture, security, performance) | Markdown output template, Critical/Important/Suggestion severity, "What's Done Well" section |
| security-auditor | Vulnerability detection, threat modeling, OWASP + LLM Top 10 | Severity table (Critical→Info), PoC for Critical/High, STRIDE-from-trust-boundaries |
| test-engineer | Test strategy, coverage analysis, Prove-It pattern for bugs | Test pyramid (unit→integration→E2E), scenario coverage table, priority-ranked recommendations |
| web-performance-auditor | Core Web Vitals, loading/rendering/network optimization | Quick mode (source-only) vs Deep mode (Lighthouse/PSI/CrUX/DevTools), metric-honesty rule, scorecard with source labels |

### cc10x Agents

| Agent | Role | Key Pattern |
| ------- | ------ | ------------- |
| code-reviewer | Adversarial multi-dimensional review with confidence scoring | CONTRACT envelope, SIGNAL_SCORES (HARD/SOFT), spec compliance pass, plan-defect detection, anti-anchoring (skips activeContext.md) |
| bug-investigator | Evidence-first debugging with TDD | Feedback loop gate (10-rung ladder), boundary matrix, anti-hardcode gate, debug close-out, variant coverage |
| component-builder | TDD execution of approved phases | BUILD_PREFLIGHT token, phase contract, false-RED guard, loop caps, deviation discipline |
| doc-syncer | Diff-driven documentation sync | Impact classifier (business/technical/audit layers), audit doc structure, skip detection |
| integration-verifier | E2E verification auditor | Proof reconciliation (truths/artifacts/wiring), test honesty gates, claim extraction from prior agents |
| plan-gap-reviewer | Fresh read-only plan challenge | Finding buckets (repo_mismatches, missing_surfaces, etc.), anti-anchored freshness rule |
| planner | Agreement-first planning artifacts | Plan mode selection (direct/execution_plan/decision_rfc), cross-phase contract drift check, verification rigor |
| researcher | Web/GitHub research with backend ladder | Bright Data/Octocode/WebSearch fallback, source quality signals, quality levels |
| silent-failure-hunter | Zero-tolerance silent failure detection | Language-specific red flags, severity rubric, zero-results suspicion gate |

### Key Differences

| Dimension | addyosmani | cc10x |
| ----------- | ----------- | ------- |
| **Agent count** | 4 | 9 |
| **Output format** | Markdown templates (human-readable) | Machine-readable YAML contracts + markdown (dual audience) |
| **Orchestration** | Personas never call each other; slash commands orchestrate | Router orchestrates; agents emit contracts the router parses |
| **Confidence/scoring** | None — qualitative severity only | Numeric confidence scoring (0-100), HARD/SOFT signal separation, gating thresholds |
| **Memory** | No persistent memory system | `.cc10x/` memory files (activeContext, patterns, progress), anti-anchoring protocols |
| **TDD enforcement** | Test-engineer *advises* on tests | component-builder *enforces* TDD with exit-code proof, false-RED detection |
| **Spec compliance** | Not a concept | First-class verdict (MISSING/EXTRA/MISUNDERSTOOD buckets, separate from code quality) |
| **Debugging** | Not covered by a dedicated agent | bug-investigator with 10-rung feedback loop ladder, variant coverage, debug close-out |
| **Performance** | Dedicated web-performance-auditor with CWV scorecard | Covered as one pass in code-reviewer's performance axis |
| **Security** | Dedicated security-auditor with OWASP + LLM Top 10 | Covered as one pass in code-reviewer's security axis + silent-failure-hunter |
| **Planning** | Not an agent — planning is a skill + `/planning` command | Dedicated planner agent with plan modes, cross-phase contract drift, plan-review-gate |
| **Documentation** | Not covered | Dedicated doc-syncer agent with impact classification |
| **Research** | Not covered | Dedicated researcher agent with backend ladder |
| **Composition rules** | Explicit "personas do not invoke other personas" in each agent's footer | Router-owned orchestration; agents emit remediation intent for router to act on |

### What addyosmani Agents Do Better

1. **Dedicated domain specialists**: security-auditor and web-performance-auditor go much deeper than cc10x's single-pass treatment. The security-auditor has a 6-section review scope including AI/LLM-specific threats. The web-performance-auditor has a metric-honesty rule, Quick vs Deep modes, and explicit framework detection before giving advice.

2. **AI-generated anti-patterns**: Both security-auditor and web-performance-auditor include "AI-generated patterns" sections — recognizing that LLM-generated code has specific failure modes (over-eager `useMemo`, state duplication, sequential `await`s when `Promise.all` would work). cc10x doesn't have this.

3. **Positive reinforcement**: Every addyosmani agent includes a "What's Done Well" / "Positive Observations" section. cc10x's agents are purely adversarial — they never acknowledge good practices. This is a UX gap.

4. **Framework-awareness**: web-performance-auditor explicitly says "Identify the framework and rendering model before applying framework-specific checks. Do not recommend `<Image>` from `next/image` to a Vue app." cc10x has no such guardrail.

5. **Metric honesty rule**: web-performance-auditor has an explicit rule: "Never fabricate metrics. An LLM reading static source code cannot measure real-world LCP, INP, or CLS." This is a guardrail against LLM hallucination that cc10x lacks.

6. **OWASP LLM Top 10**: security-auditor includes AI/LLM-specific security checks (prompt injection, excessive agency, unbounded consumption). cc10x has no LLM-specific security review.

7. **Prove-It pattern**: test-engineer has an explicit "write a test that demonstrates the bug (must FAIL), confirm it fails, report ready for fix" pattern. cc10x's bug-investigator has a more sophisticated version (feedback loop gate, variant coverage), but the Prove-It pattern is simpler and more teachable.

8. **Composition documentation**: Each addyosmani agent has a "Composition" section explaining when to invoke it directly vs via a slash command, and explicitly stating "Do not invoke from another persona." This makes orchestration boundaries explicit. cc10x agents don't document their composition rules in-agent.

### What cc10x Agents Do Better

1. **Machine-readable contracts**: Every cc10x agent emits a YAML contract with STATUS, CONFIDENCE, BLOCKING, NEXT_ACTION, REMEDIATION_NEEDED. The router can parse these and make automated decisions. addyosmani agents produce human-readable markdown only.

2. **Confidence scoring**: cc10x's 0-100 confidence with HARD/SOFT signal separation and `min(HARD) capped by avg(SOFT)-10` formula provides a principled gating mechanism. addyosmani has qualitative severity only.

3. **Anti-anchoring**: cc10x's code-reviewer and silent-failure-hunter explicitly skip `activeContext.md` to avoid being anchored by the implementer's self-assessment. addyosmani has no such concept.

4. **Spec compliance as first-class verdict**: cc10x separates "code quality" from "did you build the right thing?" with MISSING/EXTRA/MISUNDERSTOOD buckets. addyosmani's code-reviewer checks "does it match the spec?" but doesn't formalize divergence.

5. **Plan-defect detection**: cc10x's code-reviewer can flag a PLAN_DEFECT (the code faithfully implements a flawed plan) and route it to the planner, not the implementer. addyosmani has no concept of this.

6. **Test honesty gates**: cc10x's integration-verifier has explicit grep patterns for false-green tests (asserting mocks, schema-incomplete mocks, DB-bypass verification, arbitrary sleeps). addyosmani's test-engineer has no such automated detection.

7. **Proof reconciliation**: cc10x's integration-verifier requires truths/artifacts/wiring to all reconcile before PASS. addyosmani has no reconciliation concept.

8. **Loop caps**: cc10x agents have explicit failure caps (TDD failure cap: 3 consecutive GREEN fails → FAIL; debug attempt tracking: 3 hypotheses → BLOCKED). addyosmani has no caps.

9. **Scope discipline**: cc10x agents have explicit "only absorb work directly caused by the current phase" rules with decision checkpoints for >3 files, API changes, new dependencies. addyosmani agents don't bound scope.

10. **Memory persistence**: cc10x agents write learnings/patterns/verification/deferred to `.cc10x/` memory files. addyosmani agents have no memory concept.

---

## 2. Unique Agent Patterns in addyosmani

### Pattern A: Composition Footer (Explicit Orchestration Boundary)

Every addyosmani agent ends with a "Composition" section:

```markdown
## Composition
- **Invoke directly when:** [scenario]
- **Invoke via:** [slash command names]
- **Do not invoke from another persona.** [explanation]
```

This is a self-documenting pattern that makes the orchestration boundary explicit in the agent itself, not just in external docs.

### Pattern B: Operating Modes (Quick vs Deep)

web-performance-auditor has two explicit operating modes triggered by tool availability:

- Quick mode: source-only analysis, all findings tagged "potential impact"
- Deep mode: triggered by Lighthouse JSON / PSI JSON / CrUX / DevTools trace / live MCP

This pattern of "degrade gracefully when tools are absent" is more nuanced than cc10x's all-or-nothing agent design.

### Pattern C: Metric Honesty Rule

An explicit guardrail against LLM hallucination:

```markdown
**Never fabricate metrics.** An LLM reading static source code cannot measure real-world LCP, INP, or CLS.
```

With a clear protocol: if no data → return source-level findings, mark scorecard "not measured", label findings "potential impact."

### Pattern D: AI-Generated Anti-Patterns

Both security-auditor and web-performance-auditor include dedicated sections for patterns commonly produced by AI code generation:

- State duplication instead of lifting state
- `React.memo`/`useMemo`/`useCallback` wrapping everything
- Over-eager `useEffect` dependencies
- Sequential `await`s when `Promise.all` would work
- Over-fetching data "just in case"

### Pattern E: Five-Axis Review Framework

code-reviewer evaluates every change across exactly five dimensions (correctness, readability, architecture, security, performance) with specific sub-questions per dimension. This is simpler and more memorable than cc10x's 6-pass review with confidence scoring.

### Pattern F: Prove-It Pattern (Simplified TDD for Bugs)

test-engineer has a 3-step Prove-It pattern:

1. Write a test that demonstrates the bug (must FAIL)
2. Confirm the test fails
3. Report the test is ready for the fix implementation

This is deliberately simpler than cc10x's bug-investigator (which has a 10-rung feedback loop ladder, variant coverage, boundary matrix, etc.) — it's designed for cases where the bug is understood and you just need a failing test.

### Pattern G: Severity Classification Tables

Every addyosmani agent includes a severity table with Criteria + Action columns:

```
| Critical | Exploitable remotely, leads to data breach | Fix immediately, block release |
| High     | Exploitable with some conditions           | Fix before release             |
```

cc10x uses confidence scores (0-100) which are more precise but less immediately readable.

### Pattern H: Framework Detection Before Advice

web-performance-auditor: "Identify the framework and rendering model before applying framework-specific checks. Do not recommend `<Image>` from `next/image` to a Vue app, or `React.memo` to a Svelte app."

### Pattern I: OWASP LLM Top 10

security-auditor has a dedicated "AI / LLM Features" section covering:

- Model output treated as untrusted
- System prompt as security boundary (prompt injection)
- Secrets/cross-tenant data in context window
- Tool/agent permissions scoped with confirmation for destructive actions
- Token, rate, and recursion limits

---

## 3. Hook Comparison: addyosmani (4 hooks) vs cc10x (9 hooks)

### addyosmani Hooks

| Hook | Event(s) | Purpose |
| ------ | ---------- | --------- |
| session-start.sh | SessionStart | Injects `using-agent-skills` meta-skill content as additional context |
| sdd-cache-pre.sh | PreToolUse (WebFetch) | HTTP cache for documentation fetches — revalidates with origin via ETag/Last-Modified, serves cached content on 304 |
| sdd-cache-post.sh | PostToolUse (WebFetch) | Stores WebFetch results + captures ETag/Last-Modified via HEAD request |
| simplify-ignore.sh | PreToolUse (Read), PostToolUse (Edit\|Write), Stop | Block-level code protection — replaces `simplify-ignore-start/end` annotated blocks with placeholders before the model sees them, restores on edit/stop |

### cc10x Hooks

| Hook | Event(s) | Purpose |
| ------ | ---------- | --------- |
| cc10x_pretooluse_guard.py | PreToolUse (Edit\|Write) | Blocks direct writes to `.cc10x/` memory files (router-owned) |
| cc10x_git_guard.py | PreToolUse (Bash) | Blocks dangerous git commands (push, reset --hard, clean -f, branch -D, checkout .) with single-use approval tokens |
| cc10x_sessionstart_context.py | SessionStart | Injects workflow context (phase cursor, pending gate, incomplete phases, research quality) |
| cc10x_posttooluse_artifact_guard.py | PostToolUse (Edit\|Write) | Validates workflow artifact integrity (required keys, event log, freshness) |
| cc10x_task_completed_guard.py | TaskCompleted | Validates task metadata, memory finalization evidence, artifact freshness after task completion |
| cc10x_state_persist.py | PreCompact, Stop | Snapshots workflow state before compaction/session end |
| cc10x_event_logger.py | PostCompact, SubagentStop, StopFailure, InstructionsLoaded | Structured event logging for compaction, subagent contract audit, failure events, instruction audit |
| cc10x_hooklib.py | (shared library) | Common utilities (state root, workflow I/O, event logging, mode loading) |

### Key Differences

| Dimension | addyosmani | cc10x |
| ----------- | ----------- | ------- |
| **Language** | Bash (with jq) | Python 3 |
| **Hook count** | 4 scripts (1 SessionStart, 2 PreToolUse, 1 PostToolUse, 1 Stop) | 9 scripts across 10 hook events |
| **Architecture** | Standalone scripts, no shared library | Shared `cc10x_hooklib.py` library |
| **State management** | File-system cache (`.claude/sdd-cache/`, `.claude/.simplify-ignore-cache/`) | Workflow artifacts (`.cc10x/workflows/*.json`), event logs (`.events.jsonl`), state snapshots |
| **Guardrails** | Code protection (simplify-ignore), doc cache (sdd-cache) | Git safety, memory protection, artifact integrity, task metadata validation |
| **Telemetry** | Debug logging (sentinel file or env var) | Structured event logging to `cc10x-hook-events.log` + per-workflow event logs |
| **Mode system** | None (hooks always run) | `hook-mode.json` with audit/block modes per hook type |
| **Testing** | 2 test scripts (session-start-test.sh, simplify-ignore-test.sh) | 1 test script (test_cc10x_review_package.py) |
| **Events covered** | SessionStart, PreToolUse, PostToolUse, Stop | SessionStart, PreToolUse, PostToolUse, TaskCompleted, PreCompact, PostCompact, SubagentStop, Stop, StopFailure, InstructionsLoaded |

### What addyosmani Hooks Do That cc10x Doesn't

1. **SDD-CACHE (HTTP documentation cache with origin revalidation)**: This is the most innovative hook in either plugin. It caches WebFetch results keyed by URL, revalidates with the origin server via `If-None-Match`/`If-Modified-Since` on every reuse, and serves cached content only on `304 Not Modified`. This saves redundant doc fetches across sessions while maintaining freshness guarantees. cc10x has no caching layer.

2. **SIMPLIFY-IGNORE (Block-level code protection)**: This hook hides annotated code blocks from the model by replacing them with `BLOCK_<hash>` placeholders before Read, then expanding them back after Edit/Write, and restoring originals on Stop. This prevents the model from simplifying code that was deliberately complex (perf-critical loops, manually unrolled code, etc.). The round-trip is content-hashed for unambiguous restoration. cc10x has no code-protection mechanism.

3. **Meta-skill injection on session start**: session-start.sh injects the full `using-agent-skills` meta-skill content as additional context. cc10x's session-start hook injects workflow state context (phase cursor, pending gate), which is different in purpose — it's about workflow resume, not skill discovery.

4. **Graceful degradation**: addyosmani hooks check for dependencies (jq, curl, shasum) and exit 0 (no-op) if missing, rather than failing. cc10x hooks also degrade gracefully but through Python exception handling, not explicit dependency checks.

5. **Debug mode via sentinel file**: SDD-CACHE supports `touch .claude/sdd-cache/.debug` or `SDD_CACHE_DEBUG=1` to enable timestamped debug logging. This is a lightweight observability pattern.

6. **Test scripts for hooks**: addyosmani has dedicated test scripts that exercise hook logic (simplify-ignore-test.sh runs 10 tests, session-start-test.sh validates JSON payload with and without jq). cc10x has test_cc10x_review_package.py but it tests the review package tool, not the hooks directly.

### What cc10x Hooks Do That addyosmani Doesn't

1. **Git guardrails with approval tokens**: cc10x blocks `git push`, `git reset --hard`, `git clean -f`, `git branch -D`, `git checkout .` with single-use approval tokens for router-sanctioned operations. addyosmani has no git safety.

2. **Artifact integrity validation**: cc10x validates workflow artifacts have required keys, event logs exist, and artifacts aren't stale. addyosmani has no artifact concept.

3. **Task metadata validation**: cc10x validates every task has required metadata (wf, kind, origin, phase, plan, scope, reason) and that memory tasks have router-owned evidence. addyosmani has no task system.

4. **Compaction state preservation**: cc10x snapshots workflow state before compaction (PreCompact) and on session end (Stop), ensuring workflow continuity across context window resets. addyosmani has no compaction handling.

5. **SubagentStop contract audit**: cc10x logs whether subagents emitted CONTRACT envelopes. addyosmani has no contract concept.

6. **InstructionsLoaded audit**: cc10x logs instruction hashes and counts. addyosmani has no instruction auditing.

7. **Mode system (audit vs block)**: cc10x's `hook-mode.json` allows toggling between audit (log only) and block (enforce) modes per hook type. addyosmani hooks always enforce.

8. **Shared library**: cc10x's `cc10x_hooklib.py` provides reusable utilities (state root, workflow I/O, event logging, mode loading) that all hooks share. addyosmani hooks are standalone.

---

## 4. TOML Commands: What They Are and How They Work

### addyosmani Command System

addyosmani has 8 `.toml` files in `commands/`:

| Command | Description | What It Does |
| --------- | ------------- | -------------- |
| `/build` | Incremental implementation with TDD | Single-task mode (default) or autonomous mode (`/build auto`). RED→GREEN→regression→build→commit→mark complete. Autonomous mode requires spec, clean baseline, single approval, then runs all tasks. |
| `/code-simplify` | Code simplification | Identifies simplification opportunities (deep nesting, long functions, nested ternaries, generic names, duplicated logic, dead code), applies incrementally with test verification. |
| `/planning` | Task breakdown | Reads spec, enters plan mode, identifies dependency graph, slices work vertically, writes tasks/plan.md + tasks/todo.md. |
| `/review` | Five-axis code review | Reviews staged/recent changes across correctness, readability, architecture, security, performance. Categorizes as Critical/Important/Suggestion. |
| `/ship` | Pre-launch fan-out orchestrator | Spawns 3 subagents in parallel (code-reviewer, security-auditor, test-engineer), merges reports into GO/NO-GO decision with rollback plan. Skip fan-out only if ≤2 files, <50 lines, no auth/payments/data/config. |
| `/spec` | Spec-driven development | Asks clarifying questions, generates structured spec (objective, commands, project structure, code style, testing, boundaries), saves as SPEC.md. |
| `/test` | TDD workflow | Write failing tests → implement → refactor. For bugs: Prove-It pattern (write failing test, confirm fail, fix, confirm pass, regression check). |
| `/webperf` | Web performance audit | Quick mode (source analysis) or Deep mode (with Lighthouse/PSI/CrUX/DevTools). Spawns web-performance-auditor subagent. Single-persona command, no merge step. |

### TOML Format

Each `.toml` file has:

```toml
description = "Short description"
prompt = """
[Full prompt text that becomes the agent's instruction when the command is invoked]
"""
```

The `prompt` field contains the complete instruction set — it's essentially a macro that expands into the agent's context when the slash command is invoked. Some commands invoke skills (`Invoke the [skill-name] skill`), some spawn subagents (`Spawn the [agent-name] subagent`), and some do both.

### Does cc10x Have an Equivalent?

**No.** cc10x has no `.toml` command files and no `commands/` directory. cc10x's orchestration is entirely router-driven — the router dispatches agents based on workflow phase, not user-issued slash commands. cc10x agents are invoked by the router, not by the user typing `/review` or `/ship`.

This is a fundamental architectural difference:

- **addyosmani**: User → slash command → skill invocation + agent spawning
- **cc10x**: User → router → phase-based agent dispatch with contracts

### Key Command Patterns

1. **`/ship` parallel fan-out**: The most sophisticated command. It spawns 3 subagents concurrently in a single assistant turn, then merges their reports in Phase B (main context), and produces a GO/NO-GO decision with a mandatory rollback plan in Phase C. The skip-fan-out heuristic (≤2 files, <50 lines, no sensitive areas) is a smart scope guard.

2. **`/build auto` autonomous mode**: Implements an entire plan autonomously after a single approval checkpoint. Has explicit stop conditions (test can't pass, spec ambiguous, high-risk/irreversible task). Stages only files the task touched (never `git add -A`). Each task gets its own commit for clean rollback.

3. **`/spec` → `/planning` → `/build` → `/review` → `/ship` lifecycle**: The commands form a complete development lifecycle, each producing an artifact the next command consumes (SPEC.md → tasks/plan.md → code → review → ship decision).

4. **`/webperf` mode detection**: Automatically determines Quick vs Deep mode based on available tool artifacts, and passes mode expectations to the subagent.

5. **Skill invocation pattern**: Commands like `/build`, `/review`, `/test`, `/spec`, `/planning`, `/code-simplify` all start with `Invoke the [skill-name] skill.` This delegates the workflow to the skill system, keeping the command as a thin entry point.

---

## 5. SDD-CACHE and SIMPLIFY-IGNORE: Deep Dive

### SDD-CACHE (Source-Driven Development Cache)

**Purpose**: Cross-session HTTP cache for documentation fetches. Eliminates redundant `WebFetch` calls while maintaining the "verify against current docs" guarantee.

**Architecture**:

- **PreToolUse (WebFetch)**: Checks if a cache entry exists for the URL (keyed by `sha256(url)`). If yes, sends a `HEAD` request with `If-None-Match`/`If-Modified-Since` headers. On `304 Not Modified`, blocks the fetch (exit code 2) and serves cached content to the agent via stderr. Otherwise, allows the fetch.
- **PostToolUse (WebFetch)**: Captures the WebFetch response, issues a `HEAD` request to record current `ETag`/`Last-Modified`, and stores `{url, prompt, etag, last_modified, content, fetched_at}` as JSON.

**Key design decisions**:

1. **No TTL**: Freshness is delegated entirely to the origin server via HTTP validators. If validators don't catch a change, nothing will.
2. **URL-only key**: The same URL with a different prompt hits the same entry. The original prompt is surfaced as metadata so the next agent can decide if the earlier reading still applies.
3. **No validator = no cache**: Entries without `ETag` or `Last-Modified` are never cached — can't revalidate without a validator.
4. **Prompt-shaped body**: The cached content is WebFetch's post-processed result (model's reading of the page), not raw HTML. This is a deliberate trade-off: the cache stores one agent's interpretation, not the raw page.
5. **Exit code 2 as cache-hit signal**: Claude Code delivers hook stderr to the agent as a tool error — this is the intended signal for a cache hit, not a failure.
6. **Debug mode**: `SDD_CACHE_DEBUG=1` env var or `touch .claude/sdd-cache/.debug` sentinel file enables timestamped debug logging.

**Known limitations**:

- Every cache write costs an extra HEAD request (Claude Code doesn't expose response headers from WebFetch)
- Servers without ETag/Last-Modified are never cached
- Cache is local and per-project (no team-wide shared cache)
- Body is prompt-shaped (one agent's reading, not the raw page)

### SIMPLIFY-IGNORE (Block-Level Code Protection)

**Purpose**: Mark code blocks that should never be simplified by `/code-simplify`. The model sees placeholders instead of the protected implementation.

**Architecture**: One script, three hook events:

- **PreToolUse (Read)**: Backs up the original file, replaces `simplify-ignore-start`/`simplify-ignore-end` annotated blocks with `BLOCK_<hash>` placeholders in-place. The file on disk always has placeholders while the session is active.
- **PostToolUse (Edit|Write)**: Expands placeholders back to real code, saves the model's changes, then re-filters so the file stays with placeholders. Uses progressive fallback matching (full placeholder → prefix+hash+suffix → hash-only) if the model altered placeholder formatting.
- **Stop**: Restores all files from backup when the session ends.

**Key design decisions**:

1. **Content-hashed blocks**: Each block is hashed (8 hex chars via `shasum`/`sha1sum`) so round-trip restoration is unambiguous even if the model duplicates or reorders placeholders.
2. **Comment-syntax aware**: Detects comment prefix/suffix to preserve language-appropriate syntax (`# BLOCK_xxx` for Python, `<!-- BLOCK_xxx -->` for HTML, `// BLOCK_xxx` for JS).
3. **Reason strings**: `/* simplify-ignore-start: perf-critical */` includes a reason that appears in the placeholder, so the model knows *why* the block is protected.
4. **Atomic locking**: Uses `mkdir` for atomic lock acquisition (fails if another session races). Stale locks (>60s old, no backup) are reclaimed.
5. **Crash recovery**: If Claude Code crashes without triggering Stop, files may have placeholders. Manual recovery: `echo '{}' | bash hooks/simplify-ignore.sh`. Also, deleted/moved files get `.recovered` backups.
6. **Progressive fallback expansion**: If the model alters a placeholder's formatting, the hook tries progressively simpler matches. Hash-only fallback may leave cosmetic debris but preserves the code.

**Known limitations**:

- Single-line blocks hide the entire line
- Comment suffix detection covers `*/` and `-->` only
- File renaming leaves placeholders (original saved as `.recovered`)
- Fallback expansion is progressive, not exact

---

## 6. What cc10x Should Steal

### HIGH PRIORITY — Adopt These

#### 6.1 SDD-CACHE Pattern (HTTP Documentation Cache)

**What**: An HTTP-validated cache for WebFetch results, keyed by URL, revalidating with origin via ETag/Last-Modified.
**Why cc10x needs it**: cc10x's researcher agent does WebSearch + WebFetch. Repeated research on the same topics across sessions re-fetches the same pages. The SDD-CACHE pattern eliminates this without sacrificing freshness.
**How to adapt**: Port to Python (cc10x's hook language). Integrate with the researcher agent's workflow. Cache to `.cc10x/research-cache/`. The revalidation-with-origin design is the key insight — no TTL, just HTTP validators.

#### 6.2 Slash Command System (`.toml` commands)

**What**: User-facing slash commands that invoke skills and spawn agents.
**Why cc10x needs it**: cc10x is entirely router-driven. Users have no direct entry points — they can't type `/review` or `/ship` to trigger specific workflows. This limits user agency and makes ad-hoc reviews impossible without the full workflow machinery.
**How to adapt**: Add a `commands/` directory with `.toml` files. Key commands to port: `/review` (five-axis review), `/ship` (parallel fan-out with GO/NO-GO), `/test` (TDD workflow). Each command would dispatch cc10x agents with appropriate contracts.

#### 6.3 Parallel Fan-Out Orchestration (`/ship` pattern)

**What**: Spawn multiple specialist agents in a single assistant turn, then merge their reports in main context.
**Why cc10x needs it**: cc10x's router dispatches agents sequentially (plan → build → review → verify). The `/ship` pattern runs code-reviewer, security-auditor, and test-engineer *concurrently*, which is faster and provides independent perspectives.
**How to adapt**: cc10x already has the agents (code-reviewer, silent-failure-hunter, integration-verifier). Add a `/ship`-equivalent that spawns them in parallel before phase exit, merges their contracts, and produces a combined GO/NO-GO with rollback plan. The skip-fan-out heuristic (≤2 files, <50 lines, no sensitive areas) is worth adopting directly.

#### 6.4 Positive Reinforcement in Agent Output

**What**: Every addyosmani agent includes a "What's Done Well" / "Positive Observations" section.
**Why cc10x needs it**: cc10x agents are purely adversarial — they never acknowledge good practices. This creates a negative feedback loop where developers only hear about problems. Positive reinforcement is a well-established motivator for good engineering practices.
**How to adapt**: Add a `### Verified Good` section to cc10x agent output (silent-failure-hunter already has this — extend to code-reviewer and integration-verifier). Require at least one positive observation with file:line evidence.

#### 6.5 AI-Generated Anti-Patterns Section

**What**: Dedicated sections in security-auditor and web-performance-auditor for patterns commonly produced by AI code generation.
**Why cc10x needs it**: cc10x is an AI coding agent plugin — the code it produces and reviews is LLM-generated. Having explicit awareness of AI-generated anti-patterns (over-eager `useMemo`, state duplication, sequential `await`s, over-fetching) would make cc10x's code-reviewer more effective at catching its own blind spots.
**How to adapt**: Add an "AI-Generated Anti-Patterns" checklist to cc10x's code-reviewer Pass 3 (Quality) or as a new pass. Include framework-specific patterns (React, Vue, Angular, Svelte).

#### 6.6 Framework Detection Before Advice

**What**: web-performance-auditor explicitly identifies the framework before recommending framework-specific patterns.
**Why cc10x needs it**: cc10x's code-reviewer gives generic advice without knowing the stack. This leads to irrelevant recommendations (suggesting `React.memo` in a Vue project, or `next/image` in a Vite project).
**How to adapt**: Add a framework/stack detection step to cc10x's code-reviewer and component-builder. Check `package.json` dependencies, import statements, and config files. Store detected stack in memory for downstream agents.

### MEDIUM PRIORITY — Consider These

#### 6.7 Block-Level Code Protection (SIMPLIFY-IGNORE pattern)

**What**: Annotated code blocks are hidden from the model as `BLOCK_<hash>` placeholders, restored after edits.
**Why cc10x needs it**: cc10x's component-builder and bug-investigator sometimes touch code that shouldn't be simplified or refactored (perf-critical loops, manually optimized code, security-sensitive blocks). A protection mechanism would prevent well-intentioned but harmful changes.
**How to adapt**: Port to Python. Integrate with cc10x's pretool/posttool hooks. Use `.cc10x/.protect-cache/` for backups. Add `cc10x-protect-start`/`cc10x-protect-end` annotation syntax. The content-hashing and progressive fallback matching are the key technical innovations.

#### 6.8 OWASP LLM Top 10 in Security Review

**What**: security-auditor has a dedicated "AI / LLM Features" section covering prompt injection, excessive agency, unbounded consumption, secrets in context window.
**Why cc10x needs it**: cc10x agents themselves use LLM features (tool use, subagents, context windows). Security review of cc10x's own code should include LLM-specific threats. Also, cc10x reviews AI-generated code that may include LLM features.
**How to adapt**: Add an "LLM Security" pass to cc10x's code-reviewer (or create a dedicated security-auditor agent). Check for: model output used in eval/SQL/shell, system prompt as security boundary, secrets in context window, unscoped tool permissions, missing recursion/rate limits.

#### 6.9 Metric Honesty Rule

**What**: "Never fabricate metrics. An LLM reading static source code cannot measure real-world LCP, INP, or CLS."
**Why cc10x needs it**: cc10x's integration-verifier requires proof with exit codes and expected/actual values, but cc10x's code-reviewer can make performance claims without evidence. A metric-honesty rule would prevent the reviewer from asserting performance characteristics without measurement.
**How to adapt**: Add to code-reviewer's performance pass: "If no measurement data is available, tag all performance findings as 'potential impact', not as measurements. Never claim a specific performance characteristic without evidence."

#### 6.10 Composition Footer in Agent Definitions

**What**: Every addyosmani agent has a "Composition" section documenting when to invoke directly, via which commands, and explicitly stating "Do not invoke from another persona."
**Why cc10x needs it**: cc10x agents are dispatched by the router, but the dispatch rules live in the router's prompt, not in the agent definitions. Adding composition footers would make each agent self-documenting its orchestration boundaries.
**How to adapt**: Add a "## Composition" section to each cc10x agent describing: when the router dispatches this agent, what phase it runs in, what it cannot do (e.g., "Do not self-activate internal CC10X skills"), and what the router does with its output.

#### 6.11 Hook Test Scripts

**What**: addyosmani has dedicated test scripts for hooks (simplify-ignore-test.sh runs 10 tests, session-start-test.sh validates JSON payload).
**Why cc10x needs it**: cc10x's hooks are complex (artifact validation, git guardrails, task metadata) but only has one test file (test_cc10x_review_package.py) that tests the review package tool, not the hooks. Hook regressions could silently break workflow enforcement.
**How to adapt**: Add `test_cc10x_pretooluse_guard.py`, `test_cc10x_git_guard.py`, `test_cc10x_artifact_guard.py`, `test_cc10x_task_completed_guard.py` that exercise each hook with synthetic inputs. Run in CI.

### LOWER PRIORITY — Nice to Have

#### 6.12 Operating Modes (Quick vs Deep)

**What**: web-performance-auditor has Quick mode (source-only) and Deep mode (with tool artifacts), triggered by availability.
**Why cc10x might want it**: cc10x agents are all-or-nothing — they run the same process regardless of available data. A Quick/Deep mode pattern could let agents provide faster, lighter-weight reviews when no measurement data is available.
**How to adapt**: Add a `MODE: quick | deep` field to agent contracts. In quick mode, agents skip measurement-dependent passes and tag findings as "potential." In deep mode, they require evidence for all claims.

#### 6.13 Debug Mode via Sentinel File

**What**: `touch .claude/sdd-cache/.debug` enables debug logging without env vars.
**Why cc10x might want it**: cc10x has structured event logging but no easy way to enable verbose debug output for a specific hook. A sentinel file is simpler than env vars for per-project debugging.
**How to adapt**: Add `.cc10x/.debug` sentinel file support to cc10x_hooklib.py's `log_event` function. When present, log additional detail (full input, decision reasoning, timing).

#### 6.14 Five-Axis Review Framework (Simpler Alternative)

**What**: code-reviewer evaluates across exactly 5 dimensions with specific sub-questions per dimension.
**Why cc10x might want it**: cc10x's code-reviewer has 6 passes with confidence scoring, signal separation, spec compliance, and plan-defect detection. It's powerful but complex. The five-axis framework (correctness, readability, architecture, security, performance) is simpler and more memorable.
**How to adapt**: This is a simplification, not an addition. Could be offered as a "lite" review mode for smaller changes, with cc10x's full review for critical-path work.

#### 6.15 Prove-It Pattern (Simplified Bug TDD)

**What**: 3-step pattern: write failing test → confirm fail → report ready for fix.
**Why cc10x might want it**: cc10x's bug-investigator is comprehensive (10-rung feedback loop, variant coverage, boundary matrix, debug close-out) but heavy. For simple bugs where the root cause is understood, a lighter-weight Prove-It pattern would be faster.
**How to adapt**: Add a `SIMPLE_BUG` mode to bug-investigator that skips the feedback loop ladder and variant coverage when the bug is well-understood. Use the Prove-It pattern as the simplified workflow.

---

## 7. Architecture Comparison Summary

| Aspect | addyosmani | cc10x |
| -------- | ----------- | ------- |
| **Philosophy** | Human-facing workflow guide | Machine-enforced workflow engine |
| **Agent output** | Markdown templates | YAML contracts + markdown |
| **Orchestration** | Slash commands (user-driven) | Router (phase-driven) |
| **Memory** | None | `.cc10x/` files with anti-anchoring |
| **Hooks** | Bash, standalone, 4 scripts | Python, shared lib, 9 scripts |
| **Commands** | 8 `.toml` slash commands | None (router-only) |
| **Enforcement** | Advisory (agents recommend) | Enforced (contracts gate, hooks block) |
| **Telemetry** | Debug logging | Structured event logging + audit trail |
| **Testing** | 2 hook test scripts | 1 review package test |
| **Scope** | Skills + personas + commands | Agents + hooks + router |

### The Fundamental Complement

addyosmani is a **knowledge layer** — it encodes domain expertise (security threats, performance anti-patterns, test strategies, review frameworks) into agent personas and user-facing commands. It tells agents *what to look for* and *how to report it*.

cc10x is an **enforcement layer** — it encodes workflow discipline (TDD proof, spec compliance, phase gates, artifact integrity, git safety) into agent contracts and hooks. It ensures agents *follow the process* and *produce verifiable evidence*.

The ideal system combines both: cc10x's enforcement machinery with addyosmani's domain expertise. The highest-value thefts are the SDD-CACHE pattern (infrastructure), the slash command system (user agency), and the parallel fan-out orchestration (efficiency). The domain expertise (AI anti-patterns, OWASP LLM Top 10, framework detection, metric honesty) should be folded into cc10x's existing agents as new passes or checklist items.