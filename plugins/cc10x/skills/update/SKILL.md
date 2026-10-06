---
name: update
description: |
  Safe cc10x upgrade through the Claude Code plugin CLI.
  Lists every installed scope, refreshes the marketplace, updates each scope,
  and optionally carries local patches over to the new install.

  Use this skill when: updating cc10x, upgrading, pulling latest cc10x,
  syncing plugin, refreshing cache, or checking for new versions.

  Triggers: update cc10x, upgrade cc10x, pull cc10x, sync plugin, refresh cc10x,
  check for updates, new version, update plugin, upgrade plugin.
allowed-tools: Read, Bash, AskUserQuestion
---

# cc10x Update

Upgrade cc10x with the `claude plugin` CLI. The CLI owns the plugin registry and the install cache; this skill never edits either one directly and never assumes where they live.

**Workflow:** Discover installs → Locate the marketplace → (optional) Capture local patches → Refresh marketplace → Update each scope → Re-apply patches → Restart or reload.

Capture comes before the refresh on purpose: `marketplace update` moves the marketplace checkout to the new version, and the pristine baseline is read from that checkout. The marketplace checkout is often a shallow clone, so the baseline for an installed version is resolvable only when that version's commit is within the checkout depth; for an older install it usually is not. Carry-over is best-effort, and the skill says so plainly when it cannot run.

## Phase 1: Discovery

```bash
claude plugin list --json
```

The output is a JSON array. Keep only entries whose `id` is `cc10x@cc10x`. Each entry has `version`, `scope` (`user`, `project`, `local`, or `managed`), `enabled`, `installPath`, and, for `project` and `local` scopes, `projectPath`.

The same plugin can appear several times: once per scope, and once per project for `project` and `local` scopes. Different entries may point at different versions and different `installPath` values.

If no `cc10x@cc10x` entry exists → STOP and tell the user cc10x is not installed (install it with `claude plugin install cc10x@cc10x`).

Show the user one row per entry (scope, `projectPath` if present, version, `installPath`). For a `project` or `local` entry whose `projectPath` no longer exists on disk, mark it "skipped: project directory no longer exists"; it cannot be updated from there.

## Phase 2: Locate The Marketplace

```bash
claude plugin marketplace list --json
```

Take the entry named `cc10x` and set `LOC` to its `installLocation`. The plugin source is `$LOC/plugins/cc10x`. If the entry or that directory is missing → STOP and tell the user the marketplace is not registered (`claude plugin marketplace add romiluz13/cc10x`).

## Phase 3: Capture Local Patches (Optional)

Ask the user whether they have modified cached cc10x files. Skip this phase only if they say no. Run it before Phase 4.

The scope gate comes later (Phase 4), so capture covers every discovered entry, not only those chosen afterwards. For each distinct old `version` among them, pin the pristine baseline: the commit that set that version in the marketplace checkout.

```bash
SHA=$(git -C "$LOC" log --format=%H -S"\"version\": \"<old>\"" -- plugins/cc10x/.claude-plugin/plugin.json | tail -1)
git -C "$LOC" show "$SHA:plugins/cc10x/.claude-plugin/plugin.json"
```

`tail -1` takes the oldest match, the commit that introduced the version string. The `show` output must contain `"version": "<old>"`. The baseline is resolvable only if `SHA` is non-empty and the `show` output contains the old version string. If not (checkout depth is the usual cause: a one-commit shallow clone only resolves the version it currently holds) → ABORT carry-over: say plainly that carry-over is unavailable for that version because local modifications cannot be separated from upstream content, then offer the two safe choices: continue the update without carry-over, or stop so the user can save their edits by hand first. Do not guess a baseline from the new marketplace version.

With a pinned `SHA`, for each file in `git -C "$LOC" ls-tree -r --name-only "$SHA" -- plugins/cc10x`, save a per-file patch (pristine to locally modified, so applying it later re-adds the user's changes). A file that differs exits 1 from `diff`; a file missing from the install, or any exit 2, is reported rather than patched:

```bash
git -C "$LOC" show "$SHA:plugins/cc10x/<file>" | diff -u - "<old installPath>/<file>" > "<backup dir>/<file with / replaced by __>.patch"
```

Entries that share an `installPath` share one result; capture it once. Use a backup directory the user approves (for example a `cc10x-update-backup-<date>` directory under the system temp directory). Report the modified files, files missing from the install, and files present only in the old `installPath`.

**Gate:** if local modifications exist, ask: "Save these patches and carry them over after the update?"

## Phase 4: Refresh The Marketplace

```bash
claude plugin marketplace update cc10x
```

If it exits non-zero, show its output and STOP: the available version is unknown, so do not claim success or continue to Phase 5. Saved patches stay in the backup directory.

Installed versions only change in Phase 5. To learn the available version, read `.claude-plugin/plugin.json` under `$LOC/plugins/cc10x`. If every entry already matches that version → report "already up to date" and STOP.

**Gate:** show installed versus available versions and ask the user which scopes to update.

## Phase 5: Update Each Scope

For each selected entry:

```bash
claude plugin update cc10x@cc10x --scope <scope>
```

For `project` and `local` entries, run the command from the entry's `projectPath` so the CLI resolves the right project; if that directory no longer exists, skip the entry and say so. Do not run it for `managed` scope; tell the user managed installs are updated by whoever administers them.

If a command fails, report its output and continue with the remaining scopes; do not retry with other flags.

## Phase 6: Re-apply Patches

Run `claude plugin list --json` again and read the new `installPath` for each updated entry. For each saved patch, apply it to the same file under the new `installPath` (the explicit target file makes header paths irrelevant):

```bash
patch --forward "<new installPath>/<file>" "<patch file>"
```

If a hunk is rejected (a `.rej` file), show both versions and ask the user how to resolve it. Copy files that existed only in the old `installPath` into the new one. Report patches applied clean, conflicts, and files restored.

## Phase 7: Restart Or Reload

Updates apply only to a fresh session. Tell the user to restart Claude Code or run `/reload-plugins`. Report old version → new version for each scope updated.

You cannot restart or reload the session yourself, and you cannot verify the new version is active until the user does.
