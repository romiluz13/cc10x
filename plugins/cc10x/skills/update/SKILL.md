---
name: update
description: |
  Safe cc10x upgrade that preserves local modifications.
  Stashes diffs, pulls upstream, rebuilds cache, rebases patches.

  Use this skill when: updating cc10x, upgrading, pulling latest cc10x,
  syncing plugin, refreshing cache, or checking for new versions.

  Triggers: update cc10x, upgrade cc10x, pull cc10x, sync plugin, refresh cc10x,
  check for updates, new version, update plugin, upgrade plugin.
allowed-tools: Read, Bash, AskUserQuestion
---

# cc10x Update

Safe upgrade that preserves your local modifications to cached skill files.

**Workflow:** Discover versions → Stash local diffs → Pull upstream → Rebuild cache → Rebase patches → Verify.

## Paths (Resolve Once)

```bash
REGISTRY="$HOME/.claude/plugins/installed_plugins.json"
KNOWN_MARKETPLACES="$HOME/.claude/plugins/known_marketplaces.json"
CACHE_ROOT="$HOME/.claude/plugins/cache/cc10x/cc10x"
BACKUP_DIR="$HOME/.claude/plugins/cache/cc10x/_backup_$(date +%Y%m%d_%H%M%S)"
```

Read `installed_plugins.json` → extract `cc10x@cc10x` entry. If missing → STOP.
Read `known_marketplaces.json` → extract `cc10x.installLocation` → `MARKETPLACE_ROOT`.
Verify `$MARKETPLACE_ROOT/.git` exists. If missing → STOP.

## Phase 1: Discovery

1. Read installed version from registry entry
2. Read marketplace version from `$MARKETPLACE_ROOT/plugins/cc10x/.claude-plugin/plugin.json`
3. Check upstream: `cd "$MARKETPLACE_ROOT" && git fetch origin && git log HEAD..origin/HEAD --oneline`
4. Display: installed version, marketplace version, commits behind
5. Gate: if no updates → STOP. If updates available → ask user to proceed.

## Phase 2: Stash Local Modifications

1. Enumerate cache files: `find "$CACHE_ROOT" -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) | sort`
2. For each cached file, diff against marketplace source (pristine → locally-modified, so applying the patch later re-adds your changes):

   ```bash
   diff -u "$MARKETPLACE_ROOT/plugins/cc10x/$file" "$CACHE_ROOT/$file"
   ```

3. If diffs found → save to `$BACKUP_DIR/patches/` as `.patch` files. Report which files have local modifications.
4. Also check for user-added files (in cache but not in marketplace): `comm -23 <(cd "$CACHE_ROOT" && find . -type f | sort) <(cd "$MARKETPLACE_ROOT/plugins/cc10x" && find . -type f | sort)`
5. Copy user-added files to `$BACKUP_DIR/user-files/`

**Gate:** If local modifications found, ask user: "Stash and continue? Your changes will be rebased after the pull."

## Phase 3: Pull & Rebuild Cache

1. Git pull: `cd "$MARKETPLACE_ROOT" && git pull origin main`
2. Read new version from updated `plugin.json`
3. Create new cache: `mkdir -p "$CACHE_ROOT.new"` then copy all files from marketplace
4. Swap: `mv "$CACHE_ROOT" "$CACHE_ROOT.old" && mv "$CACHE_ROOT.new" "$CACHE_ROOT"`
5. Update registry only after the swap succeeded: update `cc10x@cc10x` version to new version (a failed swap must not leave the registry claiming the new version)
6. Gate: Ask user before cleaning old cache: "Remove $CACHE_ROOT.old? (your patches are safely in $BACKUP_DIR)"

## Phase 4: Rebase Patches

For each `.patch` file in `$BACKUP_DIR/patches/`:

1. Try: `patch --forward "$CACHE_ROOT/$file" "$BACKUP_DIR/patches/$file.patch"` — the explicit target file makes header paths irrelevant, and `patch` works in `$CACHE_ROOT`, which is NOT a git repository (so `git apply --3way`, which needs a repo index, is unavailable there). Fallback: if `patch` rejects a hunk (`.rej` file), reapply manually — open the `.rej` and the rebuilt file, re-edit, then delete the `.rej`.
2. If conflict: report the conflict, show both versions, ask user to resolve
3. If clean: confirm applied

Restore user-added files from `$BACKUP_DIR/user-files/` to `$CACHE_ROOT/`.

## Phase 5: Verify & Report

1. Verify cache structure: `find "$CACHE_ROOT" -type f | wc -l` matches expected count
2. Verify registry: read `installed_plugins.json` → confirm version updated
3. Run `python3 "$CACHE_ROOT/tools/doc_consistency_check.py"` if available
4. Report: old version → new version, patches rebased (N clean, M conflicts), user files restored (N)
5. Clean up: `rm -rf "$CACHE_ROOT.old"` (only after user confirms)
