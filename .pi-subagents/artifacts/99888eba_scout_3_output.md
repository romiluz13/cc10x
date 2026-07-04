# Comparison 14 — EveryInc/compound-engineering-plugin Infrastructure, src, tests, ecosystem

Source repo: `/Users/rom.iluz/Dev/everyinc-compound-engineering` (v3.17.1, package name `compound-engineering`, private ESM, Bun + citty + js-yaml, `semantic-release`/`release-please` dev deps).
Target repo: `/Users/rom.iluz/Dev/cc10x` (Python hook scripts under `plugins/cc10x/scripts/`, hooks declared via `plugins/cc10x/hooks/hooks.json`, no `src/` TypeScript, no cross-target converters, no release-automation module).

This report is the deep-structural readout requested by the task. It is organized by the seven analysis questions, followed by a "What cc10x should steal" inventory and an acceptance contract.

---

## 1. What the `src/` TypeScript code is and what the plugin actually DOES programmatically

The repo is a **cross-target plugin transpiler + installer + cleanup tool**, not a runtime plugin in the usual sense. The plugin's "skills" content (markdown in `skills/<name>/SKILL.md`) is consumed directly by Claude Code, but the TypeScript under `src/` is a CLI that turns a Claude Code plugin into the layout other AI coding tools expect and writes it to disk in the right place.

### Entry point — `src/index.ts`

```ts
import { defineCommand, runMain } from "citty"
import convert  from "./commands/convert"
import cleanup  from "./commands/cleanup"
import install  from "./commands/install"
import list     from "./commands/list"
import pluginPath from "./commands/plugin-path"

const main = defineCommand({
  meta: { name: "compound-plugin", version: packageJson.version,
          description: "Convert Claude Code plugins into other agent formats" },
  subCommands: {
    cleanup: () => cleanup,
    convert: () => convert,
    install: () => install,
    list: () => list,
    "plugin-path": () => pluginPath,
  },
})
runMain(main)
```

Five subcommands, all defined with `citty`'s `defineCommand`:

- **`convert <source> --to <target>`** — pure conversion: load a Claude plugin from disk, produce the target's bundle in-memory, write it. No git, no network.
- **`install <plugin-name-or-path> --to <target>`** — same as `convert`, but resolves the plugin from a name (`compound-engineering`, `~/…`, `/abs/path`, `./rel/path`, or a GitHub repo via `git clone --depth 1`) and falls back to bundled / GitHub clone when the input is a bare name. Cleans up the temp clone in a `finally` block.
- **`list`** — enumerate plugin roots under `./plugins/<name>/.claude-plugin/plugin.json` and the root `.claude-plugin/plugin.json`. Used to discover bundled plugins.
- **`cleanup [--target codex|opencode|pi|kiro|copilot|droid|qwen|windsurf|all]`** — back up stale artifacts left by previous CE installs. This is the largest single command and the most subtle: it owns a historical name allow-list, ownership fingerprinting, manifest-driven migration, and "don't touch user-authored files that merely collide by name" safety.
- **`plugin-path <plugin-name> --branch <branch>`** — checkout a plugin branch into `~/.cache/compound-engineering/branches/<plugin>-<sanitized-branch>` and print the path on stdout. Designed for `claude --plugin-dir $(bun run src/index.ts plugin-path compound-engineering feat/foo)`. Includes a reversible `/` → `~` then percent-encoding sanitizer for branch names.

### Internal flow

```
loadClaudePlugin(path)            parsers/claude.ts
  → resolves root by walking up to find .claude-plugin/plugin.json
  → reads manifest, agents/ (markdown + frontmatter),
            commands/ (markdown + frontmatter),
            skills/ (one SKILL.md per dir),
            hooks/ (hooks.json or inline manifest.hooks),
            mcpServers (manifest.mcpServers or .mcp.json)
  → ClaudePlugin { root, manifest, agents, commands, skills, hooks, mcpServers }

targets[targetName].convert(plugin, options)    converters/*
  → target-specific bundle (OpenCodeBundle | CodexBundle | PiBundle | KiroBundle | CopilotBundle | DroidBundle | AntigravityBundle)

targets[targetName].write(outputRoot, bundle, scope)   targets/*
  → writes files to disk; records install-manifest.json under
    <root>/<plugin>/install-manifest.json for cleanup migration
```

`targets/index.ts` exports a `targets: Record<string, TargetHandler>` registry with a uniform `{ name, implemented, defaultScope?, supportedScopes?, convert, write }` shape, so adding a new target is a single object literal — no command wiring changes.

### What it actually does programmatically (one-liner)

> It is a TypeScript CLI (Bun + citty) that parses Claude Code plugin manifests and emits equivalent agent/skill/command/MCP/hook files for OpenCode, Codex, Pi, Antigravity, Kiro (plus cleanup-only for Copilot, Droid, Qwen, Windsurf), with first-class support for installing from a local path, a bundled plugin, or a GitHub clone, and for retiring legacy installs safely.

cc10x has nothing equivalent. cc10x ships Python hook scripts that run *inside* a Claude Code session; this repo ships a TypeScript CLI that runs *outside* a session to publish the plugin into many harnesses.

---

## 2. Converters and parsers

### Parser — `src/parsers/claude.ts`

The only parser. It is the canonical "Claude plugin loader" and it is hardening-rich:

- Resolves the plugin root by walking up for `.claude-plugin/plugin.json` (or treating a path that *ends* in `plugin.json` as a manifest).
- Loads agents, commands, and skills as markdown with YAML frontmatter (`parseFrontmatter` in `utils/frontmatter.ts`, which wraps `js-yaml.load` with a source-path-bearing error message and a "quote values containing colons" hint).
- `loadSkills` only collects entries named `SKILL.md`, preserving the skill directory as `sourceDir` and surfacing `ce_platforms` for per-target filtering via `filterSkillsByPlatform(skills, "codex")` in `types/claude.ts`.
- `loadHooks` merges multiple `hooks.json` files and inline `manifest.hooks` objects into a single `ClaudeHooks` map. `loadMcpServers` accepts `manifest.mcpServers` as inline object, a path string, or an array of paths; falls back to `.mcp.json` at the plugin root.
- `resolveWithinRoot(root, entry, label)` is a guard that throws if a manifest-declared path escapes the plugin root — important because manifests are user-controlled input.

### Converters — `src/converters/claude-to-*.ts`

Seven converters, all symmetric: take `ClaudePlugin + ClaudeToOpenCodeOptions`, return a target bundle. They differ mostly in content transformation and target file shape.

| Converter | Target | What it produces | Notable transforms |
| --- | --- | --- | --- |
| `claude-to-opencode.ts` | OpenCode | `OpenCodeBundle{config, agents[], commandFiles[], plugins[], skillDirs[]}` | Infer temperature from agent name/description; rewrite `.claude/` → `.opencode/`; flatten 3-segment FQ agent refs (`plugin:cat:agent` → `agent`); synthesize slash-command stubs per user-invocable skill; map `allowedTools` → OpenCode permission map; convert hooks into a TS plugin file (`@opencode-ai/plugin`) with a `HOOK_EVENT_MAP` and `try/catch` wrapping for `tool.execute.before` (issue #85). |
| `claude-to-codex.ts` | Codex | `CodexBundle{prompts, skillDirs, generatedSkills, agents, invocationTargets, mcpServers, hooks, externallyManagedSkillNames?}` | Agents-only by default (skills come from native `codex plugin install`); `codexIncludeSkills` opt-in for legacy installs. Maps Claude tool names to Codex equivalents via `utils/codex-content.ts#transformContentForCodex`: `Task agent(args)` → `Spawn the custom agent \`<name>\``,`@agent` → `$skill skill`, slash commands →`/prompts:<name>` or skill name, `.claude/` → `.codex/`. Builds an`agentTargets` map keyed by normalized name, 2-segment cat refs, and bare names so cross-references resolve. |
| `claude-to-pi.ts` | Pi | `PiBundle{prompts, skillDirs, generatedSkills, agents, extensions, mcporterConfig}` | Maps Task calls to `Run subagent with agent="…" and task="…"`. Replaces `TaskCreate/Update/…` and `TodoWrite/TodoRead` with "the platform's task-tracking primitive". Produces a `mcporter` config for Pi's MCP bridge. |
| `claude-to-copilot.ts` | Copilot | `CopilotBundle{agents, generatedSkills, skillDirs, mcpConfig}` | `user-invocable: true` frontmatter on agents. Flattens colon-namespaced slash refs. 30k char body limit warning. Prefixes MCP env vars with `COPILOT_MCP_`. Does **not** support hooks (warns). |
| `claude-to-droid.ts` | Factory Droid | `DroidBundle{commands, droids, skillDirs}` | Tool-name map (`bash`→`Execute`, `read`→`Read`, `multiedit`→`Edit`, `ls`→`LS`, `webfetch`→`FetchUrl`, `question`→`AskUser`). Infers `tools:` list from agent body mentions and validates against `VALID_DROID_TOOLS`. Strips namespace prefix from slash commands (`workflows:plan` → `plan`). |
| `claude-to-kiro.ts` | Kiro | `KiroBundle{agents, generatedSkills, skillDirs, steeringFiles, mcpServers}` | Builds `KiroAgentConfig` with `prompt: file://./prompts/<name>.md`, `tools: ["*"]`, `resources: [file://.kiro/steering/**, skill://.kiro/skills/**]`, `includeMcpJson: true`, `welcomeMessage`. Builds steering files from `AGENTS.md` (preferred) or `CLAUDE.md`. Enforces skill-name pattern `^[a-z][a-z0-9-]*$` and 64-char max, truncating at the last hyphen boundary. Warns on hooks (Kiro uses a different format). |
| `claude-to-antigravity.ts` | Antigravity (Google) | `AntigravityBundle{agents, commands, skillDirs, mcpServers, hooks, generatedSkills, version}` | TOML `commands/` output via a hand-rolled `toToml` (multi-line basic strings). Remote MCP servers use `serverUrl` (not `url`). Task calls → `Use the @<name> subagent to: <args>`. Hooks passed through structurally only (unverified format). |

**Common patterns to steal:**

1. Each converter is a pure function `(plugin, options) => Bundle`. No I/O. The `targets/<name>.ts` writer does all disk work.
2. `ClaudeToOpenCodeOptions` is the shared options type (`agentMode`, `inferTemperature`, `permissions: "none"|"broad"|"from-commands"`, `codexIncludeSkills?`). Codex-only fields live on the shared type with a docstring explaining they are ignored elsewhere.
3. Every converter includes `transformContentForX(body)` with a **Task-call rewrite**, a **slash-command rewrite**, a **path rewrite** (`.claude/` → target dir), and an **@agent-reference rewrite**. These four regex passes are the lingua franca of cross-target plugin conversion and are independently testable.
4. `filterSkillsByPlatform(skills, platform)` is called inside every converter, so a skill's `ce_platforms:` frontmatter field opts it in/out per target without converter branches.
5. `sanitizeDescription(value, maxLength)` with an ellipsis truncator is duplicated across converters — a candidate for a shared helper (cc10x should extract, not copy).

---

## 3. The `release/` directory

`src/release/` is a **release-please companion library** that automates cross-manifest version parity and PR-shape validation. It has four files.

### `types.ts`

Type vocabulary: `ReleaseComponent = "compound-engineering" | "marketplace" | "cursor-marketplace"`, `BumpLevel = "patch"|"minor"|"major"`, `BumpOverride = BumpLevel | "auto"`, `ParsedReleaseIntent` (raw, type, scope, description, breaking), `ComponentDecision`, `ReleasePreview`.

### `config.ts` — `validateReleasePleaseConfig(config, manifest)`

Reads `.github/release-please-config.json` packages and:

1. Rejects a `release-as` pin that is not **strictly ahead** of the released version on the **base branch** (not the working tree, which on a release-please PR is already bumped). Comment explicitly cites issue #674 where a stale pin silently re-pinned every subsequent release.
2. Rejects upward-relative `changelog-path` values containing `..`.

`compareReleaseVersions(a,b)` ignores pre-release suffixes and parses `x.y.z`. `manifest` defaults to `{}` so an unknown base version allows the pin rather than risk blocking a legitimate release.

### `components.ts` — conventional-commit → version bump logic

- `parseReleaseIntent(rawTitle)` regex-parses `<type>(<scope>)!: description`.
- `inferBumpFromIntent`: `breaking`→major, `feat`→minor, `fix|perf|revert`→patch, `docs|chore|test|ci|build|style`→null.
- `detectComponentsFromFiles(files)` maps each changed file to a `ReleaseComponent` via `FILE_COMPONENT_MAP` prefixes (e.g. `skills/`, `.claude-plugin/plugin.json`, `.codex-plugin/`, `.kimi-plugin/plugin.json`, `.opencode/`, `.pi/`, `src/`, `tests/` → `compound-engineering`; `.claude-plugin/marketplace.json` → `marketplace`; `.cursor-plugin/marketplace.json` → `cursor-marketplace`).
- `resolveComponentWarnings` flags scope/file mismatch (e.g. PR claims `marketplace` scope but no marketplace file changed).
- `bumpVersion(version, bump)` does plain `x.y.z` arithmetic.
- `loadCurrentVersions(cwd)` reads `package.json`, `.claude-plugin/plugin.json`, `plugin.json` (Antigravity), `.kimi-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json` and throws if `package.json.version !== ce.version !== antigravity.version !== kimi.version`. This is the **multi-manifest version parity invariant**.
- `buildReleasePreview({title, files, overrides, cwd})` composes everything into a `ReleasePreview` used by `scripts/release/preview.ts` and CI.

### `metadata.ts` — `syncReleaseMetadata({root, write, componentVersions})`

This is the big one. It enforces **detect-only** version parity across Codex/Kimi (release-please owns the actual bump via `extra-files`), **write-enabled** description sync across Claude/Cursor/Codex/Kimi/Antigravity manifests and both marketplaces, and **structural parity checks**:

- Codex plugin.json must exist when Claude plugin.json exists ("Codex manifest parity required"), must declare a `skills` path pointing at a real directory, and its `name` must equal `compound-engineering`.
- Codex marketplace plugin list must mirror Claude marketplace's plugin names exactly; rejects `source.path: "./"` (Codex doesn't enumerate self-referential entries).
- Kimi marketplace must have `version: "2"`, plugin ids must match Claude marketplace names, and every entry must have a non-empty `source` (rejects `./` and `.` — Kimi needs a real URL for a published catalog).
- `getCompoundEngineeringCounts(root)` counts agents (markdown under `agents/`), skills (directories with `SKILL.md`), and MCP servers (entries in `.mcp.json`). Used in CI output and as a smoke metric.

### Scripts — `scripts/release/{preview,validate,sync-metadata}.ts`

- `preview.ts` — CLI front-end for `buildReleasePreview`. Args: `--title`, `--file`, `--override component=level`, `--json`.
- `validate.ts` — runs in CI. Reads `.github/release-please-config.json` + `.release-please-manifest.json`, calls `validateReleasePleaseConfig(config, readReleasedManifest())` where `readReleasedManifest()` does `git show origin/main:.github/.release-please-manifest.json` (with a `try/catch` returning `{}` when origin/main is unreachable — defensive for shallow checkouts). Calls `syncReleaseMetadata({write:false})` to detect drift. Exits non-zero on any config error, structural error, or drifted file.
- `sync-metadata.ts` — `--write` mode applies the description-sync updates. `--version:component=x.y.z` args let release-please hand in the freshly-bumped version.

### GitHub workflow integration

- `.github/workflows/ci.yml` runs: PR title validation (semantic-pull-request action with allowed types), `bun install`, `bun run release:validate`, `npm install -g @anthropic-ai/claude-code@2.1.175 && bun run plugin:validate` (pinned to a known validator version), `bun test`. `fetch-depth: 0` so release:validate can read origin/main's manifest.
- `.github/workflows/release-pr.yml` and `release-preview.yml` drive release-please.
- `.github/release-please-config.json` declares the root package with `skip-changelog: true` (CHANGELOG.md is hand-curated per the file we read), `changelog-sections` including `refactor` as a visible section, `exclude-paths` listing docs/scripts/.github plus all marketplace.json files, and `extra-files` listing every manifest that needs version sync (`package.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.kimi-plugin/plugin.json`, `plugin.json` for Antigravity, etc.).

### What cc10x should steal from `release/`

cc10x has no release-automation module. If cc10x ever publishes a versioned plugin manifest, the single most valuable pattern is:

1. **Detect-only vs write-enabled field split** — version fields stay detect-only (release-please owns them via `extra-files`), description/marketing fields are write-enabled by the sync script. Mixing these causes double-authority drift.
2. **Multi-manifest parity invariant** — `loadCurrentVersions` throws if `package.json.version !== plugin.json.version !== …`. One source of truth, multiple read sites.
3. **Stale `release-as` pin detection** — comparing the pin against the *base-branch* released version, not the working tree, prevents the #674 silent-re-pin bug.
4. **Component-from-file-prefix map** — declarative routing of changed files to release components. Adding a new component is one array entry.
5. **`getCompoundEngineeringCounts`** as a CI smoke metric — "currently has N agents, M skills, K MCP servers". Cheap, catches accidental deletions.

---

## 4. Tests: what exists and how comprehensive

### Scale

- `tests/*.test.ts`: **44 files** at the root.
- `tests/skills/*.test.ts`: **20 files** for skill-behavior contracts.
- `tests/fixtures/`: 8 fixture groups (`sample-plugin/`, `ce-doc-review/`, `custom-paths/`, `invalid-command-path/`, `invalid-hooks-path/`, `invalid-mcp-path/`, `mcp-file/`, `session-history/`).
- Test runner: `bun test` (Bun's built-in). No Jest, no Vitest config.

### Coverage by category

| Category | Files | What they test |
| --- | --- | --- |
| CLI end-to-end | `cli.test.ts` (~2k lines) | Spawns `bun run src/index.ts <cmd>` as a subprocess against tempdirs and fixture plugins. Asserts on stdout, exit codes, and on-disk file existence. Covers install-to-opencode/codex/pi, GitHub-clone install via `COMPOUND_PLUGIN_GITHUB_SOURCE` override, bundled-plugin resolution, `list` against root and `plugins/<name>` layouts, and **cleanup** for codex/opencode/pi/copilot/droid/qwen/windsurf/kiro with explicit regression coverage for "user-authored files at colliding names must be preserved." |
| Converters | `converter.test.ts` (OpenCode, the reference converter), `codex-converter.test.ts`, `codex-writer.test.ts`, `copilot-converter.test.ts`, `droid-converter.test.ts`, `kiro-converter.test.ts`, `kiro-writer.test.ts`, `opencode-writer.test.ts`, `pi-converter.test.ts`, `pi-writer.test.ts`, `antigravity-converter.test.ts`, `antigravity-writer.test.ts` | Pure-function tests on each `convertClaudeToX` plus writer I/O tests against tempdirs. Heavy use of synthetic `ClaudePlugin` literals so tests don't depend on the real plugin layout. |
| Parser/frontmatter | `claude-parser.test.ts`, `frontmatter.test.ts`, `frontmatter-validator.test.ts` | YAML frontmatter parsing/formatting, plugin root resolution, MCP/hooks loading, `resolveWithinRoot` escape guard. |
| Release | `release-config.test.ts`, `release-components.test.ts`, `release-metadata.test.ts`, `release-preview.test.ts` | `validateReleasePleaseConfig` (stale pin, upward-relative changelog), `buildReleasePreview` (component detection from file lists, bump inference), `syncReleaseMetadata` (cross-manifest parity, missing-manifest errors, marketplace plugin-list parity). One test reads the real `.github/release-please-config.json` and asserts `skip-changelog: true` and `refactor` section visibility — guards against accidental config regressions. |
| Legacy cleanup | `legacy-cleanup.test.ts`, `legacy-registry-invariants.test.ts`, `plugin-legacy-artifacts.test.ts`, `plugin-path.test.ts`, `manifest-path-safety.test.ts`, `path-sanitization.test.ts`, `skill-shell-safety.test.ts`, `skill-agent-ce-prefix.test.ts` | The legacy-cleanup subsystem is the most heavily tested. `legacy-registry-invariants.test.ts` asserts `STALE_SKILL_DIRS ∩ currentSkillDirs == ∅` — a structural invariant that prevents a re-added skill from being deleted on every install. |
| Path/safety | `path-sanitization.test.ts`, `manifest-path-safety.test.ts`, `plugin-path.test.ts`, `resolve-output.test.ts` | `isSafeManagedPath`, `sanitizePathName`, `commandNameToRelativePath`, `expandHome`, `resolveTargetOutputRoot`, `resolveOpenCodeWriteScope`. |
| Contracts | `commit-push-pr-contract.test.ts`, `pipeline-review-contract.test.ts`, `review-skill-contract.test.ts`, `skill-conventions.test.ts`, `skill-shell-safety.test.ts`, `ce-sweep-analyzer-parity.test.ts`, `repo-profile-cache-parity.test.ts`, `repo-profile-cache.test.ts`, `sweep-state.test.ts`, `resolve-pr-feedback-pagination.test.ts`, `session-history-scripts.test.ts`, `real-plugin-conversion.test.ts`, `detect-tools.test.ts`, `model-utils.test.ts` | Cross-skill contract tests (e.g. `ce-sweep-analyzer-parity` ensures the byte-duplicated analyzer in `ce-sweep` matches the canonical one in `ce-riffrec-feedback-analysis`), tool detection, model alias normalization. |
| Skill behavior | `tests/skills/*.test.ts` (20 files) | Section ordering, output-mode (markdown vs HTML), routing/handoff, dev-server/port resolution, package-manager detection, project-type detection, resolve-pr-feedback pagination, session-historian no-skill-tool guard, setup health check, worktree, html-output invariants, unified-plan artifact contract. These test **skill prose contracts** by reading the SKILL.md files and asserting structural properties — a poor-person's behavioral eval that catches drift between skills and between skills and their docs. |

### Quality observations

- Tests use real subprocesses for CLI tests and pure functions for converters — the split is principled and keeps the converter tests fast.
- Tempdirs are created with `fs.mkdtemp(path.join(os.tmpdir(), "…-"))` per test; no shared mutable state.
- Regression tests cite issue/PR numbers in comments (e.g. "Regression coverage for PR #609", "fix for #85", "#477"). This is a strong signal of a mature test suite — each regression test is a documented incident.
- `HISTORICAL_AGENT_DESCRIPTIONS` and `HISTORICAL_SKILL_DESCRIPTIONS` in `cli.test.ts` are **fingerprint material** — the exact frontmatter description strings from past releases. They are the ownership signal for legacy cleanup. The test file doubles as a registry of "what we've shipped."
- No snapshot tests. Assertions are structural (file exists, content contains substring, frontmatter field equals value). This avoids the snapshot-drift problem where snapshots get rubber-stamped.
- `real-plugin-conversion.test.ts` loads the actual compound-engineering plugin from the repo root and runs all converters against it — an end-to-end smoke test that the plugin can install itself.

### What cc10x should steal

cc10x has `plugins/cc10x/tests/{fixtures,live}/` and a `test_cc10x_review_package.py` next to the hook scripts. The patterns to adopt:

1. **Fixture-plugin pattern** — a minimal `sample-plugin/` with `.claude-plugin/plugin.json`, one agent, one command, one skill, an MCP server, and a hooks.json. Every converter/CLI test loads the same fixture so test failures localize.
2. **Subprocess CLI tests with tempdir isolation** — `cli.test.ts`'s shape is directly portable to any plugin with a CLI.
3. **Skill-prose contract tests** — `tests/skills/*.test.ts` reads SKILL.md files and asserts section ordering, output-mode flags, routing keys. This is the cheapest way to catch skill/doc drift without an LLM-in-the-loop eval.
4. **Registry invariant tests** — `legacy-registry-invariants.test.ts` is a one-test guard that prevents a whole class of bugs (re-added skill deleted on install). cc10x's `agent-contract-registry.md` and `router-invariants.md` are the analog and deserve executable invariant tests.
5. **Regression tests that cite issue numbers** — turns the test suite into a documented incident history.

---

## 5. Documentation patterns in `docs/`

### Directory map

| Dir | Files | Purpose |
| --- | --- | --- |
| `docs/brainstorms/` | 28 | Pre-plan requirements documents. Filename: `YYYY-MM-DD-<topic>-requirements.md`. Frontmatter: `title`, `date`, `topic`. Each is a Product Contract — problem frame, decisions, skill disposition tables (Delete/Keep/Beta), open questions. |
| `docs/plans/` | ~60 | Implementation plans. Filename: `YYYY-MM-DD-NNN-feat | fix | refactor-<topic>-plan.md`. Frontmatter includes`artifact_contract: ce-unified-plan/v1`,`artifact_readiness: implementation-ready`,`product_contract_source: ce-brainstorm`,`execution: code`. Each plan has a **Goal Capsule** (objective, product authority, authority hierarchy, execution profile, stop conditions, tail ownership, open blockers), **Product Contract**, **Planning Contract**, and Implementation Units with U-IDs. |
| `docs/specs/` | 8 | Per-target platform specs: `antigravity.md`, `claude-code.md`, `codex.md`, `copilot.md`, `cursor.md`, `kimi.md`, `kiro.md`, `opencode.md`. Each has a "Last verified" date, primary-source URLs, and sections for config location, prompts, skills, subagents, MCP, hooks — with `citeturnNviewN` citations from research sessions. These are the **empirical ground truth** the converters are built against. |
| `docs/solutions/` | ~40 | Compounded learnings, organized by `skill-design/`, `integrations/`, `workflow/`, `conventions/`, `best-practices/`, `developer-experience/`. Each is a self-contained finding — e.g. `agent-friendly-cli-principles.md` (7-principle rubric), `confidence-anchored-scoring.md`, `colon-namespaced-names-break-windows-paths.md`, `native-plugin-install-strategy.md`, `release-please-version-drift-recovery.md`. This is the **`/ce-compound` output directory** — the closed loop. |
| `docs/skills/` | 28 | End-user-facing skill documentation. One `README.md` index plus one page per skill. The README draws the **core loop** diagram (`/ce-ideate → /ce-brainstorm → /ce-plan → /ce-work → /ce-compound`) and groups skills into Core Loop / Around the Loop / On-Demand / Research & Context / Git Workflow / Autonomous Pipeline / Frontend Design / Collaboration / Workflow Utilities. Each skill page covers purpose, novel mechanics, use cases, and chain position. |
| `docs/ideation/` | 1 | HTML ideation doc (`2026-06-28-ce-pov-skill-proposal.html`). |
| `docs/residual-review-findings/` | 1 | See §6. |

### Patterns to steal

1. **Brainstorm → Plan → Solutions lifecycle** — `docs/brainstorms/` feeds `docs/plans/`, plans reference brainstorms via `product_contract_source: ce-brainstorm`, and completed work writes learnings into `docs/solutions/`. The next iteration's brainstorm/plan reads `docs/solutions/` as grounding. This is the **compound** in "compound engineering" — a documented, file-system-resident learning loop. cc10x's `docs/plans/` and `docs/research/` exist but there is no `docs/solutions/` and no contract linking them.
2. **Per-target platform spec docs with citations and "Last verified" dates** — `docs/specs/codex.md` etc. are empirical ground truth with `citeturnNviewN` citations from research sessions and a dated verification stamp. cc10x's `docs/research/` could adopt this format for any external API it depends on.
3. **Goal Capsule in every plan** — objective, product authority, authority hierarchy, execution profile, stop conditions, tail ownership, open blockers. This is a portable plan-header contract. cc10x's `docs/plans/` files are unstructured by comparison.
4. **Skill README as a navigable catalog** — the `docs/skills/README.md` groups skills by loop position with a one-line description and a link per skill. cc10x has `prompt-surface-inventory.md` but it is not a navigable catalog.
5. **`artifact_contract: ce-unified-plan/v1` and `artifact_readiness: implementation-ready`** — plan documents carry a versioned artifact contract so downstream consumers (`/lfg`, `ce-plan`) can parse them programmatically. This is the document-as-API pattern.

---

## 6. The `residual-review-findings` concept

`docs/residual-review-findings/` is a **durable record of review findings that were not applied in the PR that produced them**. The single example file (`feat-ce-explain-skill.md`) is short enough to quote in full:

```markdown
# Residual Review Findings

Source: ce-code-review run `20260702-211155-42168d78` on branch `feat/ce-explain-skill`
(pre-PR; review verdict "Ready with fixes", 4 actionable findings, 3 applied in `fix(review)` commit).

## Residual Review Findings

- **P2** — `skills/ce-explain/SKILL.md:70` — Predict-then-reveal protocol duplicated
  with only substring guard — filed:
  https://github.com/EveryInc/compound-engineering-plugin/issues/1057
  (resolution is keep-both-plus-parity-guard per AGENTS.md inline-the-trigger doctrine;
  the reviewer's trim-to-pointer fix was rejected by validation)
```

### The concept

- A `ce-code-review` run produces N actionable findings. Some are applied in a `fix(review)` commit; the remainder are **residual**.
- Each residual finding is persisted as a markdown file under `docs/residual-review-findings/<branch-or-feature>.md` with: the review run id, the branch, the verdict, the count of findings, the count applied, and one bullet per residual finding with severity (P2 here), file:line, description, filed-issue URL, and a **resolution note** explaining why it was not applied (here: "keep-both-plus-parity-guard per AGENTS.md inline-the-trigger doctrine; the reviewer's trim-to-pointer fix was rejected by validation").
- The finding is also filed as a GitHub issue (issue #1057 in the example) so it has a tracker identity.

### Why it exists

- It closes the audit gap between "review found X" and "PR shipped" without forcing the PR to fix everything. The residual is visible, dated, and linked to an issue.
- It prevents residual findings from becoming invisible: the file is in the repo, the issue is in the tracker, and the next review run can read the file to see what was previously deferred.
- The "resolution is keep-both-plus-parity-guard" note is the key — it records **why** the finding was not applied, so a future reviewer doesn't re-flag it and re-derive the same resolution.

### What cc10x should steal

cc10x has `docs/known-flaws.md` and `docs/prompt-change-checklist.md` but no per-PR residual-findings artifact. The pattern to adopt:

1. After each `cc10x` review pass, write `docs/residual-review-findings/<branch>.md` with the review run id, verdict, applied count, and one bullet per residual finding with severity, file:line, filed-issue URL, and resolution note.
2. The file is the durable handshake between the review skill and the issue tracker.
3. The resolution note is mandatory — a residual finding without a "why not applied" note is a TODO, not a residual.

---

## 7. What cc10x should steal — structured inventory

### Tier 1 — directly portable patterns

| Pattern | Source | cc10x application |
| --- | --- | --- |
| **Fixture-plugin for CLI/converter tests** | `tests/fixtures/sample-plugin/` | Add a minimal `plugins/cc10x/tests/fixtures/sample-plugin/` with one agent, one command, one skill, one hook, one MCP server. Every hook-script test loads the same fixture. |
| **Subprocess CLI tests with tempdir isolation** | `tests/cli.test.ts` | cc10x's hook scripts are invoked as subprocesses by Claude Code; test them the same way — spawn `python3 scripts/cc10x_pretooluse_guard.py` with a tempdir CWD and assert on stdout/exit code. |
| **Skill-prose contract tests** | `tests/skills/*.test.ts` | Read each `plugins/cc10x/skills/*/SKILL.md` and assert section ordering, routing-key presence, output-mode flags. Cheapest drift detector. |
| **Registry invariant test** | `tests/legacy-registry-invariants.test.ts` | One test that asserts `cc10x agent-contract-registry.md` entries match `plugins/cc10x/agents/*.md` filenames — prevents the "re-added agent deleted on install" class of bug. |
| **Regression tests that cite issue numbers** | throughout `tests/` | Each new regression test gets a comment citing the issue/PR that motivated it. Turns the test suite into incident history. |
| **Residual review findings** | `docs/residual-review-findings/` | After each cc10x review pass, write `docs/residual-review-findings/<branch>.md` with run id, verdict, applied count, and one bullet per residual finding with severity, file:line, filed-issue URL, and resolution note. |
| **Per-target platform spec with citations + "Last verified"** | `docs/specs/codex.md` etc. | For any external API cc10x depends on (Claude Code hook events, plugin manifest schema), write `docs/specs/<platform>.md` with primary-source URLs, `citeturnNviewN` citations, and a dated verification stamp. |
| **Goal Capsule in every plan** | `docs/plans/*.md` | Adopt the plan-header contract: objective, product authority, authority hierarchy, execution profile, stop conditions, tail ownership, open blockers. |
| **`docs/solutions/` as the compounded-learnings loop** | `docs/solutions/` | Close the loop. cc10x has `docs/research/` and `docs/plans/` but no `docs/solutions/`. Add it and have cc10x's review/retrospective hooks write into it. |

### Tier 2 — patterns that require adaptation

| Pattern | Source | cc10x adaptation |
| --- | --- | --- |
| **Cross-target converter architecture** | `src/converters/*`, `src/targets/*` | cc10x is Claude-Code-only today, so the full converter matrix is not needed. But the **pure-function converter + writer split** and the **`targets` registry shape** (`{name, implemented, defaultScope?, supportedScopes?, convert, write}`) are a clean template if cc10x ever emits a Codex or OpenCode variant. |
| **`filterSkillsByPlatform(skills, platform)`** | `src/types/claude.ts` | If cc10x skills ever need per-harness variants, a `cc10x_platforms:` frontmatter field plus a one-line filter is the minimal viable opt-in/opt-out. |
| **`transformContentForX(body)` four-pass pattern** | every converter | Task-call rewrite, slash-command rewrite, path rewrite, @agent-reference rewrite. If cc10x ever cross-publishes, these four regex passes are the lingua franca. |
| **Release-please companion library** | `src/release/{config,components,metadata,types}.ts` | cc10x has no versioned manifest today. If it ever publishes one, the **detect-only vs write-enabled field split**, **multi-manifest parity invariant**, and **stale `release-as` pin detection** are the three patterns to lift verbatim. |
| **`getCompoundEngineeringCounts(root)` as a CI smoke metric** | `src/release/metadata.ts` | Count agents/skills/MCP servers and print in CI. Catches accidental deletions. |
| **Legacy cleanup with historical allow-list + ownership fingerprinting** | `src/data/plugin-legacy-artifacts.ts`, `src/utils/legacy-cleanup.ts` | The full subsystem is over-engineered for cc10x today, but the **core safety principle** — "legacy detection must be driven by an explicit historical allow-list, not by the current bundle, so user-authored files at colliding names are never swept" — is a portable design rule for any cc10x cleanup path. |
| **`isSafeManagedPath` + `sanitizePathName` defense-in-depth** | `src/utils/files.ts`, `src/targets/managed-artifacts.ts` | Any cc10x script that joins user-controlled relative paths into filesystem operations should re-check `isSafeManagedPath` at the boundary. The managed-artifacts module re-checks every manifest entry at read time and again at every rm site. |
| **Install manifest for cleanup migration** | `src/targets/managed-artifacts.ts` | `install-manifest.json` under `<root>/<plugin>/` records what was installed; cleanup reads it to migrate artifacts whose type or emission format changed between versions. If cc10x ever writes files outside its own plugin dir, this is the pattern. |

### Tier 3 — patterns that are informational only

| Pattern | Source | Notes |
| --- | --- | --- |
| `citty` for CLI subcommands | `src/index.ts` | Clean, but cc10x's CLI surface is Python-based via hook scripts; not directly applicable. |
| `js-yaml` for frontmatter | `src/utils/frontmatter.ts` | cc10x hooks read JSON, not YAML frontmatter. |
| `semantic-release` as a dev dependency | `package.json` | The repo uses release-please, not semantic-release, for actual releases; the devDep appears to be vestigial. |
| `AGENTS.md` + `CLAUDE.md` + `GEMINI.md` + `CONCEPTS.md` coexistence | repo root | The repo ships context files for multiple harnesses. `CONCEPTS.md` is a shared vocabulary substrate introduced in v3.10.0. cc10x has `CLAUDE.md` only. |
| `ce_platforms:` frontmatter field | `src/types/claude.ts` | The `ce_` prefix is a namespace choice; the pattern (per-skill platform opt-in) is the reusable idea. |
| `inferTemperature(agent)` from name/description | `claude-to-opencode.ts` | Heuristic mapping (review→0.1, plan→0.2, doc→0.3, brainstorm→0.6, default→0.3). Portable if cc10x ever emits OpenCode agents. |

### Infrastructure gaps cc10x should close

1. **No `src/` TypeScript** — cc10x's logic lives in Python hook scripts. This is fine for in-session behavior but means cc10x has no out-of-session tooling (no install, no convert, no cleanup, no release validation). If cc10x ever needs out-of-session tooling, the citty + Bun + pure-function-converter shape here is a proven template.
2. **No release-automation module** — `src/release/` is the single most valuable infrastructure module in this repo. cc10x has no equivalent and no versioned manifest to validate, but the **detect-only vs write-enabled** and **multi-manifest parity** patterns are worth remembering for when cc10x ships a versioned plugin.
3. **No `docs/solutions/`** — the compounded-learnings loop is the conceptual core of "compound engineering." cc10x has `docs/research/` and `docs/plans/` but the loop is not closed.
4. **No `docs/residual-review-findings/`** — review findings that are not applied become invisible. cc10x's review hooks should write residual findings as durable artifacts.
5. **No per-target platform spec docs** — cc10x depends on Claude Code hook events but has no `docs/specs/claude-code.md` with citations and a "Last verified" date. The hook event surface is not versioned in any documented way.
6. **No skill-prose contract tests** — `tests/skills/*.test.ts` is the cheapest drift detector in this repo. cc10x's `prompt-invariants.md` and `prompt-surface-inventory.md` are the analog but are not executable.
7. **No fixture-plugin for tests** — cc10x's `tests/fixtures/` exists but is not a minimal plugin used by every test.

---

## Summary table — everyinc/compound-engineering vs cc10x infrastructure

| Dimension | everyinc/compound-engineering | cc10x |
| --- | --- | --- |
| Out-of-session CLI | TypeScript (Bun + citty), 5 subcommands | None (Python hook scripts only) |
| Cross-target converters | 7 (OpenCode, Codex, Pi, Antigravity, Kiro, + Copilot/Droid/Qwen/Windsurf cleanup-only) | None (Claude Code only) |
| Parser | `parsers/claude.ts` (manifest + agents/commands/skills/hooks/mcp) | None |
| Release automation | `src/release/` (config validation, component detection, metadata sync) + release-please | None |
| Test suite | 64 test files (44 root + 20 skill), subprocess CLI tests, fixture-plugin, registry invariants, skill-prose contracts | `tests/{fixtures,live}/` + `test_cc10x_review_package.py` |
| Docs lifecycle | brainstorms → plans → solutions (closed loop) | plans + research (open loop, no solutions) |
| Platform specs | `docs/specs/<platform>.md` with citations + "Last verified" | None |
| Residual review findings | `docs/residual-review-findings/<branch>.md` | None |
| Legacy cleanup | Historical allow-list + ownership fingerprinting + install manifest | None |
| Hook scripts | N/A (the repo is a plugin, not a hook host) | Python (`cc10x_*.py`) with `hooks.json` |
| CI | `bun test` + `release:validate` + `claude plugin validate` (pinned) + semantic PR titles | Not inspected in this task |

---

## Acceptance report

This was a read-only analysis task. No files were changed in either repository except the required output and progress artifacts under `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/`.