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

**Workflow:** Discover installs → Refresh marketplace → (optional) Capture local patches → Update each scope → Re-apply patches → Restart or reload.

## Phase 1: Discovery

```bash
claude plugin list --json
```

The output is a JSON array. Keep only entries whose `id` is `cc10x@cc10x`. Each entry has `version`, `scope` (`user`, `project`, `local`, or `managed`), `enabled`, `installPath`, and, for `project` and `local` scopes, `projectPath`.

The same plugin can appear several times: once per scope, and once per project for `project` and `local` scopes. Different entries may point at different versions and different `installPath` values. Show the user one row per entry (scope, `projectPath` if present, version, `installPath`).

If no `cc10x@cc10x` entry exists → STOP and tell the user cc10x is not installed (install it with `claude plugin install cc10x@cc10x`).

## Phase 2: Refresh The Marketplace

```bash
claude plugin marketplace update cc10x
```

Installed versions only change in Phase 4. To learn the available version, read `.claude-plugin/plugin.json` under the marketplace plugin directory (locate it as in Phase 3, step 1). If every entry already matches that version → report "already up to date" and STOP.

**Gate:** show installed versus available versions and ask the user which scopes to update.

## Phase 3: Capture Local Patches (Optional)

Skip this phase if the user has not modified cached files.

1. Locate the marketplace source: `claude plugin marketplace list --json`, take the entry named `cc10x`, and use its `installLocation`. The plugin source is `<installLocation>/plugins/cc10x`. If that directory is missing, skip patch carry-over and say so.
2. For each entry being updated, list the differing files between the marketplace source and its old `installPath`: `diff -rq "<installLocation>/plugins/cc10x" "<old installPath>"`. Entries that share an `installPath` share one result; capture it once. Ignore differences that exist only because the old version is older than the marketplace version; local patches are the files the user edited, so compare against the marketplace source at the old version when the versions differ (`git -C "<installLocation>" log` can locate it) or ask the user which files they changed.
3. For each locally modified file, save a per-file patch (pristine to locally modified, so applying it later re-adds the user's changes):

   ```bash
   diff -u "<pristine file>" "<old installPath>/<file>" > "<backup dir>/<file with / replaced by __>.patch"
   ```

   Use a backup directory the user approves (for example a `cc10x-update-backup-<date>` directory under the system temp directory). Report which files were modified, and list files present only in the old `installPath`.

**Gate:** if local modifications exist, ask: "Save these patches and carry them over after the update?"

## Phase 4: Update Each Scope

For each selected entry:

```bash
claude plugin update cc10x@cc10x --scope <scope>
```

For `project` and `local` entries, run the command from the entry's `projectPath` so the CLI resolves the right project. Do not run it for `managed` scope; tell the user managed installs are updated by whoever administers them.

If a command fails, report its output and continue with the remaining scopes; do not retry with other flags.

## Phase 5: Re-apply Patches

Run `claude plugin list --json` again and read the new `installPath` for each updated entry. For each saved patch, apply it to the same file under the new `installPath` (the explicit target file makes header paths irrelevant):

```bash
patch --forward "<new installPath>/<file>" "<patch file>"
```

If a hunk is rejected (a `.rej` file), show both versions and ask the user how to resolve it. Copy files that existed only in the old `installPath` into the new one. Report patches applied clean, conflicts, and files restored.

## Phase 6: Restart Or Reload

Updates apply only to a fresh session. Tell the user to restart Claude Code or run `/reload-plugins`. Report old version → new version for each scope updated.

You cannot restart or reload the session yourself, and you cannot verify the new version is active until the user does.
