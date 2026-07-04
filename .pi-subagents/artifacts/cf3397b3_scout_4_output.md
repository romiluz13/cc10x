# Deep Comparison: Developer Experience, Installation & Ecosystem

**Projects compared:** cc10x (v12.2.0) · Superpowers (v6.1.1) · Matt Pocock Skills
**Date:** 2026-07-02
**Scope:** Installation, getting-started DX, multi-platform support, versioning/updates, testing/eval infrastructure, documentation quality, unique DX patterns, cross-project adoption opportunities, overall DX rating.

---

## 1. Installation

| Dimension | cc10x | Superpowers | Matt Pocock Skills |
| ----------- | ------- | ------------- | --------------------- |
| **Primary method** | Claude Code plugin marketplace (`/plugin marketplace add romiluz13/cc10x` → `/plugin install cc10x@romiluz13`) | Multi-harness plugin marketplace (official Claude, self-hosted marketplace, Codex portal, Antigravity, Cursor, Factory Droid, GitHub Copilot CLI, Kimi, OpenCode, Pi) | Manual skill files in a skills repo — no plugin system, no marketplace |
| **Secondary method** | Manual `git clone` into `~/.claude/plugins/cc10x` (documented troubleshooting fallback) | `npm install superpowers@git+...` for OpenCode; `pi install git:...` for Pi; `agy plugin install` for Antigravity; `/add-plugin` for Cursor | Copy skills into `.claude/skills/` or equivalent |
| **Marketplace metadata** | `marketplace.json` at repo root + `plugin.json` inside the plugin directory — both versioned at 12.2.0 | `.claude-plugin/plugin.json` (Claude), `.codex-plugin/plugin.json` (Codex), `.cursor-plugin/plugin.json` (Cursor), `.kimi-plugin/plugin.json` (Kimi), `.opencode/` (OpenCode JS plugin), `.pi/` (Pi extension) — one manifest per harness, all at 6.1.1 | None — no plugin.json, no marketplace.json |
| **Post-install setup** | User says "set up cc10x for me" → 6-step wizard (CLAUDE.md injection, settings.json permissions merge, optional user-standards capture, installed-skill scan, restart prompt) | Session-start hook auto-injects `using-superpowers` bootstrap; no manual setup needed for most harnesses | User runs `setup-matt-pocock-skills` skill once per repo (explores repo, asks 3 questions one at a time, writes `docs/agents/*.md` config files, edits CLAUDE.md/AGENTS.md) |
| **Linux troubleshooting** | Dedicated EXDEV cross-device link fix with `TMPDIR` workaround and manual clone fallback | Windows-specific troubleshooting documented; Linux not specifically called out | N/A |
| **npm support** | None | `package.json` with `pi-package` keywords; OpenCode installs via `npm install superpowers@git+...` | None |

### Verdict: Installation

- **Superpowers** wins on breadth — 10 harnesses with per-harness install instructions and manifests. The README is a one-stop shop for installation no matter which AI tool you use.
- **cc10x** wins on depth — the "set up cc10x for me" wizard is the most guided post-install experience of the three, handling CLAUDE.md merge, permissions, optional standards capture, and installed-skill discovery. But it's Claude Code only.
- **Matt Pocock** is the simplest — no plugin system at all, just skill files. The per-repo setup skill is thoughtful but manual.

---

## 2. Getting Started (Developer Experience)

| Dimension | cc10x | Superpowers | Matt Pocock Skills |
| ----------- | ------- | ------------- | --------------------- |
| **First-run experience** | "set up cc10x for me" wizard: 6 steps, asks about coding standards, scans installed skills, adds complementary-skills table to CLAUDE.md | Zero-touch: session-start hook injects bootstrap, brainstorming skill auto-triggers when you start building something | Run `setup-matt-pocock-skills` per repo: 3 interactive decisions (issue tracker, triage labels, domain docs) with explainers for non-experts |
| **Time to first value** | After restart: say "build a user auth system" → router auto-detects intent, asks clarifying questions, runs BUILD workflow | After install: say "let's make a react todo list" → brainstorming auto-triggers, refines spec, creates plan, dispatches subagents | After setup: invoke any engineering skill (e.g. `/tdd`, `/triage`, `/to-issues`) — but you need to know which skill to invoke |
| **Cognitive load** | Low — one router entry point, everything routes through it; user never needs to remember 12 slash commands | Low — skills auto-trigger; user doesn't need to invoke them manually | Medium — user needs to know which skill to use; `ask-matt` skill acts as a router but it's user-invoked (`disable-model-invocation: true`) |
| **Examples in README** | 3 quick-start examples (Build, Fix, Review) with expected workflow traces | 7-step basic workflow described in prose; "How it works" narrative | Engineering README lists all skills with one-line descriptions |
| **Onboarding doc quality** | README has "Why cc10x" pain table, architecture diagrams, workflow table, expected-behavior comparison (with/without cc10x) | README has "How it works" narrative, philosophy section, visual companion feature | README is a skill index — no onboarding narrative |

### Verdict: Getting Started

- **cc10x** has the most guided onboarding with the setup wizard and "with/without" comparison that sells the value proposition. The pain-to-solution table is excellent marketing-as-documentation.
- **Superpowers** has the lowest friction — zero-touch auto-triggering means the user doesn't even need to think about skills. The "let's make a react todo list" acceptance test is a model of simplicity.
- **Matt Pocock** has the most pedagogical setup (explainers for each decision, one-at-a-time questions), but requires the most user knowledge upfront.

---

## 3. Multi-Platform Support

| Platform | cc10x | Superpowers | Matt Pocock Skills |
| ---------- | ------- | ------------- | --------------------- |
| **Claude Code** | ✅ Primary (plugin marketplace) | ✅ (official marketplace + self-hosted marketplace) | ✅ (manual skill files) |
| **Codex App** | ❌ | ✅ (official Codex plugin marketplace) | ❌ (not documented) |
| **Codex CLI** | ❌ | ✅ (`/plugins` search) | ❌ |
| **Cursor** | ❌ | ✅ (`/add-plugin superpowers`) | ❌ |
| **GitHub Copilot CLI** | ❌ | ✅ (marketplace add + install) | ❌ |
| **Kimi Code** | ❌ | ✅ (plugin marketplace + repo install) | ❌ |
| **OpenCode** | ❌ | ✅ (npm-backed plugin + JS runtime) | ❌ |
| **Pi** | ❌ | ✅ (`pi install git:...`) | ❌ |
| **Antigravity** | ❌ | ✅ (`agy plugin install`) | ❌ |
| **Gemini CLI** | ❌ | ❌ (removed — Google EOL'd it) | ❌ |
| **Total harnesses** | **1** | **9** | **1 (Claude Code only)** |

### Per-harness adaptation approach

- **Superpowers** has a dedicated plugin manifest per harness with harness-specific metadata:
  - `.codex-plugin/plugin.json`: Codex-specific `interface` block with `displayName`, `capabilities`, `defaultPrompt`, `brandColor`, `composerIcon`, `logo`, `screenshots`
  - `.kimi-plugin/plugin.json`: Kimi-specific `skillInstructions` block mapping Superpowers actions to Kimi tools (`AskUserQuestion`, `TodoList`, `Agent` with `subagent_type: "coder"/"explore"/"plan"`)
  - `.cursor-plugin/plugin.json`: Cursor-specific `displayName` + hook config pointer
  - `.opencode/`: Full JS plugin (`superpowers.js`) that injects bootstrap via message transform, caches at module level, auto-registers skills directory
  - Per-harness tool-mapping reference files in `skills/using-superpowers/references/`
- **cc10x** has no multi-harness support — it's deeply coupled to Claude Code's plugin system, hooks, and Task/Agent primitives
- **Matt Pocock** is harness-agnostic in principle (skills are just markdown) but has no per-harness manifests or tool mappings

### Verdict: Multi-Platform

- **Superpowers** is the clear winner with 9 supported harnesses and a documented porting guide (`docs/porting-to-a-new-harness.md`). Each harness gets a tailored manifest and tool mapping.
- **cc10x** is single-platform by design — its deep integration with Claude Code hooks, Tasks, and plugin system is a strength within that platform but a moat against portability.
- **Matt Pocock** is nominally portable (plain markdown skills) but has no manifests, no tool mappings, and no per-harness documentation.

---

## 4. Updates & Versioning

| Dimension | cc10x | Superpowers | Matt Pocock Skills |
| ----------- | ------- | ------------- | --------------------- |
| **Versioning scheme** | Semver, currently 12.2.0 | Semver, currently 6.1.1 | No version number visible in files read |
| **Changelog** | Extensive `CHANGELOG.md` (3385+ lines) with per-release sections, detailed change descriptions, migration notes | `RELEASE-NOTES.md` (1330+ lines) with versioned sections, contributor credits, bug fix details | None found |
| **Update mechanism** | Dedicated `update` SKILL.md — 5-phase safe upgrade: discover versions → stash local diffs → pull & rebuild cache → rebase patches → verify. Preserves user modifications. | "Updates are somewhat coding-agent dependent, but are often automatic." Per-harness reinstall guidance (e.g. `agy plugin install` to update for Antigravity) | Manual — re-pull or re-copy skill files |
| **Local modification preservation** | ✅ The update skill stashes local diffs as `.patch` files, saves user-added files, then rebases patches after pull. Explicit conflict reporting. | ❌ No documented local-modification preservation | ❌ |
| **Version sync validation** | `cc10x_doc_consistency_check.py` asserts README counts/headings and every version string matches disk + plugin.json on every commit | Manual — version appears in multiple plugin manifests, synced by hand | N/A |
| **Marketplace metadata sync** | `marketplace.json` and `plugin.json` both carry version; README banner shows version | 5+ plugin manifests each carry version; `package.json` carries version | N/A |
| **Release frequency** | Very high — 30+ releases from v5.x to v12.2.0, multiple releases per month | Regular — v5.1.0 to v6.1.1 over ~2 months | Unknown |

### Verdict: Updates & Versioning

- **cc10x** has the most sophisticated update story — a dedicated skill that preserves local modifications through patch stashing and rebasing is unique in this comparison. The version-sync validator is a strong CI safeguard.
- **Superpowers** has a good changelog but relies on "often automatic" updates, which is less reassuring for users who customize skills.
- **Matt Pocock** has no versioning or update mechanism documented.

---

## 5. Testing & Evaluation Infrastructure

| Dimension | cc10x | Superpowers | Matt Pocock Skills |
| ----------- | ------- | ------------- | --------------------- |
| **Eval directory** | `plugins/cc10x/skills/cc10x-router/evals/` — 3 routing-decision evals + README | `evals/` (external submodule from `superpowers-evals` repo) + `tests/` (10 test directories) | None found |
| **Eval format** | RED-GREEN-REFACTOR structure (from superpowers' writing-skills): Setup → Pressure → Expected behavior → Failure signature → Counter/rationalization table | "Drill" eval harness: runs real tmux sessions of Claude Code/Codex/Gemini, judges skill compliance with an LLM verifier | N/A |
| **Eval coverage** | 3 evals covering router intent decisions: ERROR-over-BUILD priority, REVIEW-stays-advisory, don't-skip-router-for-multifile | Full skill-behavior testing: code-review catches planted bugs, spec-reviewer catches planted flaws, brainstorming auto-trigger, TDD enforcement, etc. | N/A |
| **Plugin-infrastructure tests** | `cc10x_harness_audit.py`, `cc10x_doc_consistency_check.py`, `cc10x_workflow_replay_check.py`, `cc10x_latency_audit.py` | `tests/` has: `claude-code/` (SDD integration, worktree tests, token analysis), `codex/` (marketplace manifest, package tests), `hooks/` (session-start), `opencode/` (bootstrap caching, plugin loading, priority, tools), `pi/` (extension), `kimi/` (manifest), `antigravity/` (tools), `brainstorm-server/` (auth, branding, lifecycle, WS protocol — 10 test files), `shell-lint/`, `explicit-skill-requests/` (multi-turn tests), `codex-plugin-sync/` | N/A |
| **Test runner** | Python scripts run manually | `run-*.sh` scripts per directory; `npm test` for infrastructure | N/A |
| **Behavioral testing** | Eval files describe expected behavior but are manual dispatch scenarios (no automated runner) | Drill harness runs real agent sessions and LLM-judges compliance — the gold standard | N/A |

### Verdict: Testing & Evaluation

- **Superpowers** has the most comprehensive testing infrastructure — 10 test directories, a dedicated external eval harness (drill) that runs real agent sessions, and per-harness infrastructure tests. The brainstorm-server alone has 10 test files covering auth, branding, lifecycle, and WebSocket protocol.
- **cc10x** has solid infrastructure auditing (harness audit, doc consistency, replay checks, latency audit) and thoughtful eval scenarios with rationalization tables, but only 3 eval files and no automated eval runner — evals are manual dispatch-and-observe.
- **Matt Pocock** has no testing infrastructure visible in the files read.

---

## 6. Documentation Quality

| Dimension | cc10x | Superpowers | Matt Pocock Skills |
| ----------- | ------- | ------------- | --------------------- |
| **README** | ~800 lines: pain table, architecture diagrams (ASCII), workflow table, quick-start examples, expected-behavior comparison, file structure, troubleshooting (3 sections), optional MCP docs, version history table | ~200 lines: quickstart per harness, "How it works" narrative, workflow steps, skills library index, philosophy, contributing, telemetry disclosure, community links | Engineering README is a skill index with one-line descriptions and links |
| **CLAUDE.md / AGENTS.md** | Setup instructions embedded in README (6-step wizard with exact file contents) | Dedicated `CLAUDE.md` (symlinked to `AGENTS.md`) with contributor guidelines for AI agents — 94% PR rejection rate warning, pre-submission checklist, what-we-won't-accept list, new-harness acceptance test, skill-change eval requirements | N/A in files read |
| **Changelog / Release notes** | 3385+ line CHANGELOG.md with per-release sections, migration notes, verification commands | 1330+ line RELEASE-NOTES.md with detailed per-release notes, contributor credits, bug fix details | None |
| **Examples** | 3 quick-start examples with workflow traces; expected-behavior "with vs without" comparison | "How it works" narrative + basic workflow steps | Skill descriptions in README |
| **Architecture docs** | 4 dedicated docs: orchestration bible, logic analysis, safety, router invariants | `docs/porting-to-a-new-harness.md`, `docs/testing.md`, `docs/README.opencode.md`, `docs/README.kimi.md` | Per-skill SKILL.md files with detailed process steps |
| **Troubleshooting** | 3 dedicated sections: permission prompts, project activation, Linux EXDEV error, unknown skill error | Troubleshooting in per-harness install docs (e.g. OpenCode plugin not loading, Windows issues, cache clearing) | N/A |
| **Contributing guide** | Brief: star, report issues, suggest improvements | Comprehensive: PR template, 94% rejection rate warning, what-we-won't-accept list, dev-branch targeting, agent disclosure requirement, eval evidence requirement | N/A |

### Verdict: Documentation Quality

- **cc10x** has the most thorough primary README — the pain table, architecture diagrams, expected-behavior comparison, and troubleshooting sections are exceptional marketing-as-documentation. The embedded setup wizard with exact file contents is immediately actionable.
- **Superpowers** has the best contributor documentation (CLAUDE.md with 94% rejection rate warning is a masterclass in managing AI-generated PRs) and the most complete per-harness documentation.
- **Matt Pocock** has lean but well-structured skill documentation — each SKILL.md is a precise process document.

---

## 7. DX Patterns cc10x Has That Others DON'T

| Pattern | Description | Value |
| --------- | ------------- | ------- |
| **Setup wizard with installed-skill scanning** | The "set up cc10x for me" wizard scans `~/.claude/settings.json`, `installed_plugins.json`, and skills directories, then auto-populates a "Complementary Skills" table in CLAUDE.md | Users don't need to manually wire up skill composition — the wizard discovers and documents it |
| **Safe-update skill with patch rebasing** | The `update` SKILL.md implements a 5-phase upgrade that stashes local modifications as `.patch` files, pulls upstream, then rebases patches with conflict reporting | Users who customize skill files don't lose their changes on update — unique in this comparison |
| **Version-sync validator** | `cc10x_doc_consistency_check.py` asserts README counts/headings and every version string matches disk + plugin.json on every commit | Catches version drift across metadata surfaces before release |
| **Pain-to-solution marketing table** | README opens with a "The pain you know → How cc10x handles it" table | Self-selling documentation that maps known problems to solutions |
| **Workflow-state-on-disk with UUIDs** | `.cc10x/workflows/{wf}.json` + `.events.jsonl` with stable UUIDs, auto-healed by router | Durable truth that survives compaction — the others rely on chat context or git branches |
| **Fail-closed hook enforcement** | 10 Claude Code-native hooks (PreToolUse, SessionStart, PostToolUse, TaskCompleted, PreCompact, Stop, etc.) that block on corruption, validate metadata, and guard protected files | Guardrails that don't rely on the LLM remembering rules |
| **Complexity gradient** | Trivial BUILD work runs a reduced builder→verifier→memory graph instead of the full 4-subagent chain | Avoids "one-line edit pays full ceremony" cost |
| **Router-eval rationalization tables** | Each eval file includes a "Counter" table mapping rationalization excuses to counter-arguments | Evaluates not just behavior but the rationalization patterns that lead to wrong behavior |
| **`.cc10x/` namespace outside `.claude/`** | State lives at `.cc10x/` — outside `.claude/`, so the harness's sensitive-file gate never fires | Eliminates permission prompts on every memory write — a specific DX pain point solved |

---

## 8. DX Patterns Others Have That cc10x SHOULD Adopt

| Pattern | Source | Description | Why cc10x should adopt it |
| --------- | -------- | ------------- | --------------------------- |
| **Multi-harness manifests** | Superpowers | Per-harness plugin.json with harness-specific metadata (Codex `interface` block, Kimi `skillInstructions` tool mapping, Cursor `displayName`) | cc10x is Claude Code only; even a partial port to Codex or Cursor would expand reach |
| **Automated eval runner (drill)** | Superpowers | Drill harness runs real tmux sessions of Claude Code/Codex and judges skill compliance with an LLM verifier | cc10x's 3 evals are manual dispatch-and-observe; an automated runner would catch regressions in CI |
| **Per-harness tool-mapping references** | Superpowers | `skills/using-superpowers/references/` has one file per harness mapping skill actions to native tools | If cc10x ever ports, this pattern decouples skill logic from harness-specific tool names |
| **Contributor guidelines for AI agents** | Superpowers CLAUDE.md | 94% PR rejection rate warning, pre-submission checklist, what-we-won't-accept list, agent disclosure requirement | cc10x's contributing section is 3 lines; a real contributor guide would improve external contribution quality |
| **Telemetry opt-out** | Superpowers | Visual companion telemetry with `SUPERPOWERS_DISABLE_TELEMETRY` env var; honors `DISABLE_TELEMETRY` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | cc10x has no telemetry but if it ever adds any, this is the model |
| **Discord community + release announcements** | Superpowers | Discord server, release announcement mailing list | cc10x has no community infrastructure beyond GitHub issues |
| **Porting guide for new harnesses** | Superpowers | `docs/porting-to-a-new-harness.md` with the "load the bootstrap at session start" rule and acceptance test | If cc10x wants to expand beyond Claude Code, this is the template |
| **Per-repo interactive setup with explainers** | Matt Pocock | `setup-matt-pocock-skills` walks users through 3 decisions one at a time with explainers for non-experts | cc10x's setup wizard is good but asks about coding standards in one shot; Matt Pocock's one-at-a-time-with-explainer approach is more beginner-friendly |
| **Issue tracker integration** | Matt Pocock | Skills that read/write GitHub Issues, GitLab Issues, or local markdown — with `gh`/`glab` CLI conventions | cc10x has no issue-tracker integration; its workflow artifacts are file-based only |
| **Domain modeling (CONTEXT.md + ADRs)** | Matt Pocock | `CONTEXT.md` glossary + `docs/adr/` consumed by multiple skills; multi-context support for monorepos | cc10x's memory (`patterns.md`) is similar but less structured; a domain glossary would improve agent vocabulary consistency |
| **Brainstorming visual companion** | Superpowers | Optional web server showing brainstorming questions visually with per-session auth | Novel UX for design conversations; cc10x's planning is purely text-based |
| **Marketplace packaging script** | Superpowers | `package-codex-plugin.sh` for deterministic Codex portal archive building | cc10x has no packaging script — releases are manual git pushes |

---

## 9. DX Ratings (1-10)

### cc10x — **7.5/10**

**Strengths:**

- Best-in-class setup wizard (6-step guided onboarding with installed-skill scanning)
- Unique safe-update skill with local-modification preservation
- Excellent README as marketing (pain table, architecture diagrams, expected-behavior comparison)
- Durable workflow state that survives compaction
- Fail-closed hooks for guardrails
- Comprehensive changelog with migration notes
- Version-sync validator for release hygiene

**Weaknesses:**

- Single-platform (Claude Code only) — no portability
- No automated eval runner (manual dispatch-and-observe only)
- No community infrastructure (Discord, mailing list)
- Contributing guide is minimal (3 lines)
- No issue-tracker integration
- No npm/package distribution

### Superpowers — **8.5/10**

**Strengths:**

- Broadest platform support (9 harnesses with per-harness manifests and tool mappings)
- Zero-touch auto-triggering (session-start hook, no manual setup for most harnesses)
- Best testing infrastructure (drill eval harness, 10 test directories, per-harness tests)
- Best contributor documentation (94% PR rejection rate warning, comprehensive guidelines)
- Community infrastructure (Discord, release announcements, hiring page)
- Commercial services offering
- Detailed release notes with contributor credits
- Visual companion for brainstorming
- Porting guide for new harnesses

**Weaknesses:**

- No local-modification preservation on update
- No safe-update skill (relies on "often automatic")
- No durable workflow state (relies on chat context + git worktrees)
- No fail-closed hook enforcement beyond session-start bootstrap
- Version sync across 5+ manifests is manual

### Matt Pocock Skills — **5.5/10**

**Strengths:**

- Thoughtful per-repo setup with one-at-a-time explainers for non-experts
- Issue tracker integration (GitHub, GitLab, local markdown)
- Domain modeling with CONTEXT.md + ADRs
- Clean skill-index README
- Triage state machine with label vocabulary
- `ask-matt` router skill for skill discovery

**Weaknesses:**

- No plugin system, no marketplace, no versioning
- No changelog or release notes
- No testing infrastructure
- No multi-harness support (no manifests, no tool mappings)
- No update mechanism
- Manual installation only
- No community infrastructure
- Skills are user-invoked (`disable-model-invocation: true`) for several key skills — higher cognitive load

---

## Summary Verdict

| Category | Winner | Runner-up |
| ---------- | -------- | ----------- |
| **Installation breadth** | Superpowers (9 harnesses) | cc10x (Claude Code, deep) |
| **Installation depth (guided setup)** | cc10x (6-step wizard) | Matt Pocock (interactive per-repo) |
| **Getting started DX** | cc10x (wizard + examples + pain table) | Superpowers (zero-touch auto-trigger) |
| **Multi-platform support** | Superpowers (9 harnesses) | Matt Pocock (portable in principle) |
| **Updates & versioning** | cc10x (safe-update skill + validator) | Superpowers (good changelog) |
| **Testing & evaluation** | Superpowers (drill + 10 test dirs) | cc10x (audit scripts + 3 evals) |
| **Documentation quality** | cc10x (README) / Superpowers (contributor docs) | — |
| **Community & ecosystem** | Superpowers (Discord, hiring, commercial) | cc10x (GitHub only) |
| **Unique DX innovations** | cc10x (patch-rebase updates, complexity gradient, `.cc10x/` namespace) | Superpowers (visual companion, porting guide) |

### Bottom line

**Superpowers** is the most mature ecosystem project — it has the breadth (9 harnesses), the testing infrastructure (drill), the contributor guidelines, and the community. It's the project you'd point a team at if they use multiple AI tools.

**cc10x** is the deepest single-platform experience — the setup wizard, safe-update skill, workflow-state-on-disk, fail-closed hooks, and complexity gradient are genuine DX innovations that Superpowers doesn't have. But it's Claude Code only, has no automated eval runner, and lacks community infrastructure. The highest-leverage improvements for cc10x would be: (1) adopt an automated eval runner, (2) write a real contributing guide, (3) add even one more harness, and (4) build community infrastructure.

**Matt Pocock Skills** is the most pedagogically thoughtful for per-repo setup (one-at-a-time with explainers) and has unique value in issue-tracker integration and domain modeling. But it lacks the infrastructure (versioning, testing, multi-platform, community) to compete on DX breadth.