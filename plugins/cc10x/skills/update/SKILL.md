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

---

## Paths (Resolve Once)

Resolve these paths at the start and reuse throughout. All paths are deterministic from the plugin registry.

```bash
REGISTRY="$HOME/.claude/plugins/installed_plugins.json"
KNOWN_MARKETPLACES="$HOME/.claude/plugins/known_marketplaces.json"
CACHE_ROOT="$HOME/.claude/plugins/cache/cc10x/cc10x"
BACKUP_DIR="$HOME/.claude/plugins/cache/cc10x/_backup_$(date +%Y%m%d_%H%M%S)"
```

**Pre-flight check:**

```
Read(file_path="~/.claude/plugins/installed_plugins.json")
```

Extract the `cc10x@cc10x` entry. If missing → STOP: "cc10x is not installed. Install it first with `/install cc10x`."

Then resolve the marketplace repo location:

```
Read(file_path="~/.claude/plugins/known_marketplaces.json")
```

Extract `cc10x.installLocation` → this is `MARKETPLACE_ROOT` (the local git clone of the cc10x repo).
The plugin source lives at `MARKETPLACE_ROOT/plugins/cc10x/`.

Verify the marketplace repo exists:

```
Bash(command="test -d \"$MARKETPLACE_ROOT/.git\" && echo 'OK' || echo 'MISSING'")
```

If MISSING → STOP: "Marketplace repo not found at $MARKETPLACE_ROOT. Re-add it with `claude plugins add-marketplace`."

---

## Phase 1: Discovery

### 1.1 Read installed version

From `installed_plugins.json`, extract for the `cc10x@cc10x` entry:
- `INSTALLED_VERSION` → `.version`
- `CURRENT_CACHE_PATH` → `.installPath`
- `INSTALLED_SHA` → `.gitCommitSha` (may be absent)
- `INSTALL_SCOPE` → `.scope` (user or local)

### 1.2 Read marketplace version

```
Read(file_path="$MARKETPLACE_ROOT/.claude-plugin/marketplace.json")
```

Extract `MARKETPLACE_VERSION` → `.metadata.version`

### 1.3 Check upstream for new commits

```bash
cd "$MARKETPLACE_ROOT" && git fetch origin main --quiet 2>&1
```

```bash
LOCAL_SHA=$(cd "$MARKETPLACE_ROOT" && git rev-parse HEAD)
REMOTE_SHA=$(cd "$MARKETPLACE_ROOT" && git rev-parse origin/main)
```

### 1.4 Display status

Output a status table:

```
## cc10x Update Status

| Field              | Value                    |
|--------------------|--------------------------|
| Installed version  | $INSTALLED_VERSION       |
| Marketplace version| $MARKETPLACE_VERSION     |
| Local SHA          | ${LOCAL_SHA:0:10}        |
| Remote SHA         | ${REMOTE_SHA:0:10}       |
| Cache path         | $CURRENT_CACHE_PATH      |
| Status             | Up-to-date / Update available / Registry drift |
```

If `LOCAL_SHA == REMOTE_SHA` AND the cache path exists AND matches marketplace version:
→ Report "Already up-to-date" and offer a **re-sync** option (skip to Phase 3 to rebuild cache from current marketplace source).

If `LOCAL_SHA != REMOTE_SHA`:
→ Show changelog preview (top 10 new commits):

```bash
cd "$MARKETPLACE_ROOT" && git log --oneline HEAD..origin/main | head -10
```

### 1.5 Gate: Proceed?

```
AskUserQuestion(questions=[{
  "question": "Proceed with cc10x update?",
  "header": "Update",
  "options": [
    {"label": "Yes, update", "description": "Stash local changes, pull upstream, rebuild cache"},
    {"label": "Re-sync only", "description": "Rebuild cache from current marketplace source (no git pull)"},
    {"label": "Cancel", "description": "Do nothing"}
  ],
  "multiSelect": false
}])
```

- **Cancel** → STOP with "Update cancelled."
- **Re-sync only** → Skip Phase 3.1 (git pull), go directly to 3.2.
- **Yes, update** → Continue to Phase 2.

---

## Phase 2: Stash Local Modifications

**Critical timing:** Diff cache against the *current* (un-pulled) marketplace source. This isolates user changes from upstream changes.

### 2.1 Enumerate cache files

```bash
find "$CURRENT_CACHE_PATH" -type f | sort
```

### 2.2 Diff each file against marketplace source

For each file in the cache, compute its relative path and diff against the marketplace counterpart:

```bash
MARKETPLACE_SOURCE="$MARKETPLACE_ROOT/plugins/cc10x"

for CACHE_FILE in $(find "$CURRENT_CACHE_PATH" -type f | sort); do
  REL_PATH="${CACHE_FILE#$CURRENT_CACHE_PATH/}"
  MARKET_FILE="$MARKETPLACE_SOURCE/$REL_PATH"

  if [ -f "$MARKET_FILE" ]; then
    DIFF=$(diff -u "$MARKET_FILE" "$CACHE_FILE" 2>/dev/null)
    if [ -n "$DIFF" ]; then
      # File was locally modified
      mkdir -p "$BACKUP_DIR/patches/$(dirname "$REL_PATH")"
      mkdir -p "$BACKUP_DIR/originals/$(dirname "$REL_PATH")"
      echo "$DIFF" > "$BACKUP_DIR/patches/$REL_PATH.patch"
      cp "$CACHE_FILE" "$BACKUP_DIR/originals/$REL_PATH"
    fi
  else
    # User-added file (no marketplace counterpart)
    mkdir -p "$BACKUP_DIR/new_files/$(dirname "$REL_PATH")"
    cp "$CACHE_FILE" "$BACKUP_DIR/new_files/$REL_PATH"
  fi
done
```

### 2.3 Report modifications

Count and list modified files:

```bash
PATCH_COUNT=$(find "$BACKUP_DIR/patches" -name "*.patch" 2>/dev/null | wc -l | tr -d ' ')
NEW_COUNT=$(find "$BACKUP_DIR/new_files" -type f 2>/dev/null | wc -l | tr -d ' ')
```

Output:
```
## Local Modifications Found

- **$PATCH_COUNT** files with local changes (patches saved)
- **$NEW_COUNT** user-added files (backed up)
- Backup location: `$BACKUP_DIR`
```

If `PATCH_COUNT == 0` and `NEW_COUNT == 0`:
→ "No local modifications detected. Clean update."

List modified files with short summary of each patch (lines added/removed).

---

## Phase 3: Pull & Rebuild Cache

### 3.1 Git pull (skip if re-sync)

```bash
cd "$MARKETPLACE_ROOT" && git pull origin main --ff-only 2>&1
```

If fast-forward fails (diverged history):
→ STOP: "Marketplace repo has diverged from upstream. Resolve manually with `cd $MARKETPLACE_ROOT && git status`."

### 3.2 Read new version

```
Read(file_path="$MARKETPLACE_ROOT/.claude-plugin/marketplace.json")
```

Extract `NEW_VERSION` from `.metadata.version`.

### 3.3 Copy to new cache directory

```bash
NEW_CACHE_PATH="$CACHE_ROOT/$NEW_VERSION"
mkdir -p "$NEW_CACHE_PATH"
cp -r "$MARKETPLACE_SOURCE/"* "$NEW_CACHE_PATH/"
```

Verify the copy:

```bash
echo "Skills: $(ls "$NEW_CACHE_PATH/skills/" 2>/dev/null | wc -l | tr -d ' ')"
echo "Agents: $(ls "$NEW_CACHE_PATH/agents/" 2>/dev/null | wc -l | tr -d ' ')"
echo "Hooks:  $(ls "$NEW_CACHE_PATH/hooks/" 2>/dev/null | wc -l | tr -d ' ')"
```

### 3.4 Update registry

Use Python3 to safely update `installed_plugins.json`:

```bash
python3 -c "
import json, sys
from datetime import datetime, timezone

registry_path = sys.argv[1]
new_version = sys.argv[2]
new_cache_path = sys.argv[3]
new_sha = sys.argv[4]

with open(registry_path) as f:
    reg = json.load(f)

entry = reg['plugins']['cc10x@cc10x'][0]
entry['version'] = new_version
entry['installPath'] = new_cache_path
entry['lastUpdated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
if new_sha:
    entry['gitCommitSha'] = new_sha

with open(registry_path, 'w') as f:
    json.dump(reg, f, indent=2)
    f.write('\n')

print(f'Registry updated: version={new_version}, path={new_cache_path}')
" "$REGISTRY" "$NEW_VERSION" "$NEW_CACHE_PATH" "$NEW_SHA"
```

Where `NEW_SHA` is obtained from:

```bash
NEW_SHA=$(cd "$MARKETPLACE_ROOT" && git rev-parse HEAD)
```

### 3.5 Gate: Old cache cleanup

If `CURRENT_CACHE_PATH != NEW_CACHE_PATH` and the old cache directory still exists:

```
AskUserQuestion(questions=[{
  "question": "Remove old cache version ($INSTALLED_VERSION)?",
  "header": "Cleanup",
  "options": [
    {"label": "Move to backup", "description": "Move old cache to $BACKUP_DIR/old_cache/ (safe, can restore later)"},
    {"label": "Keep it", "description": "Leave old version in place alongside new version"},
    {"label": "Delete", "description": "Permanently remove old cache directory"}
  ],
  "multiSelect": false
}])
```

- **Move to backup** → `mv "$CURRENT_CACHE_PATH" "$BACKUP_DIR/old_cache/"`
- **Keep it** → No action. Mark with `.orphaned_at` timestamp: `date -u > "$CURRENT_CACHE_PATH/.orphaned_at"`
- **Delete** → `rm -rf "$CURRENT_CACHE_PATH"`

---

## Phase 4: Rebase Patches

Skip this phase entirely if no patches were saved in Phase 2.

### 4.1 Apply each patch

For each `.patch` file in `$BACKUP_DIR/patches/`:

```bash
REL_PATH="${PATCH_FILE#$BACKUP_DIR/patches/}"    # e.g., skills/cc10x-router/SKILL.md.patch
TARGET_REL="${REL_PATH%.patch}"                    # e.g., skills/cc10x-router/SKILL.md
TARGET_FILE="$NEW_CACHE_PATH/$TARGET_REL"
```

**Step 1: Dry run**

```bash
patch --dry-run "$TARGET_FILE" < "$PATCH_FILE" 2>&1
```

**Step 2: Apply or handle conflict**

If dry run succeeds (exit code 0):
→ Apply for real: `patch "$TARGET_FILE" < "$PATCH_FILE"`
→ Log: "Patch applied cleanly: $TARGET_REL"

If dry run fails (exit code != 0):
→ Save reject file: `patch "$TARGET_FILE" < "$PATCH_FILE"` (will create `.rej`)
→ Show the conflict context to the user
→ Gate per conflict:

```
AskUserQuestion(questions=[{
  "question": "Patch conflict on $TARGET_REL. How to resolve?",
  "header": "Conflict",
  "options": [
    {"label": "Show diff", "description": "Display the patch content so I can decide"},
    {"label": "Skip patch", "description": "Use upstream version (discard local change)"},
    {"label": "Use backup", "description": "Replace with full backup copy of your modified file"}
  ],
  "multiSelect": false
}])
```

- **Show diff** → Read and display the patch file content, then re-ask with Skip/Use backup options.
- **Skip patch** → No action on this file. Log: "Skipped: $TARGET_REL"
- **Use backup** → `cp "$BACKUP_DIR/originals/$TARGET_REL" "$TARGET_FILE"`

### 4.2 Restore user-added files

If user-added files were saved in Phase 2:

For each file in `$BACKUP_DIR/new_files/`:

```bash
REL_PATH="${NEW_FILE#$BACKUP_DIR/new_files/}"
TARGET="$NEW_CACHE_PATH/$REL_PATH"

if [ ! -f "$TARGET" ]; then
  mkdir -p "$(dirname "$TARGET")"
  cp "$NEW_FILE" "$TARGET"
  echo "Restored user file: $REL_PATH"
else
  echo "Conflict: upstream now has $REL_PATH (your version backed up)"
fi
```

---

## Phase 5: Verify & Report

### 5.1 Verify cache structure

```bash
for DIR in skills agents hooks; do
  if [ -d "$NEW_CACHE_PATH/$DIR" ]; then
    echo "$DIR/ — $(ls "$NEW_CACHE_PATH/$DIR" | wc -l | tr -d ' ') items"
  else
    echo "$DIR/ — MISSING (warning)"
  fi
done
```

### 5.2 Verify registry

```bash
python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    reg = json.load(f)
entry = reg['plugins']['cc10x@cc10x'][0]
print(f\"Registry version:  {entry['version']}\")
print(f\"Registry path:     {entry['installPath']}\")
print(f\"Registry SHA:      {entry.get('gitCommitSha', 'N/A')}\")
print(f\"Last updated:      {entry['lastUpdated']}\")
" "$REGISTRY"
```

### 5.3 Final summary

Output a summary table:

```
## Update Complete

| Field                 | Before               | After                |
|-----------------------|----------------------|----------------------|
| Version               | $INSTALLED_VERSION   | $NEW_VERSION         |
| Cache path            | $CURRENT_CACHE_PATH  | $NEW_CACHE_PATH      |
| Commit SHA            | ${INSTALLED_SHA:0:10}| ${NEW_SHA:0:10}      |
| Patches applied       | N/A                  | $APPLIED_COUNT       |
| Patches conflicted    | N/A                  | $CONFLICT_COUNT      |
| Patches skipped       | N/A                  | $SKIPPED_COUNT       |
| User files restored   | N/A                  | $RESTORED_COUNT      |
| Backup location       | N/A                  | $BACKUP_DIR          |
```

### 5.4 Changelog highlights

```bash
cd "$MARKETPLACE_ROOT" && git log --oneline -10
```

### 5.5 Next steps

Output:
```
**Restart Claude Code** to pick up the new version.

If something went wrong, your backup is at:
  $BACKUP_DIR

To restore from backup:
  cp -r $BACKUP_DIR/originals/* $NEW_CACHE_PATH/
```

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Marketplace repo missing | STOP with instructions to re-add marketplace |
| `git fetch` fails (network) | STOP with error message, suggest retry |
| `git pull --ff-only` fails | STOP — diverged history needs manual resolution |
| Registry missing `cc10x@cc10x` | STOP — cc10x not installed |
| Cache path in registry doesn't exist | Warn, proceed with rebuild (registry drift) |
| No local modifications | Skip Phase 2 stash + Phase 4 rebase entirely |
| User-added file conflicts with new upstream file | Warn, keep upstream, backup available |
| `python3` not available | Extremely unlikely (Claude Code requires it), but STOP with error |
| Same version but different SHA | Offer re-sync (content changed without version bump) |
| Multiple entries in `cc10x@cc10x` array | Use the first entry (primary installation) |

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `rm -rf` any directory | `mv` to timestamped backup |
| Diff after `git pull` | Diff before pull (Phase 2 before Phase 3) |
| Use `jq` for JSON | Use `python3 -c 'import json; ...'` (portable) |
| Hardcode paths | Resolve from registry + known_marketplaces |
| Skip dry-run for patches | Always `patch --dry-run` first |
| Auto-resolve conflicts | Ask user per conflict via `AskUserQuestion` |
| Modify marketplace repo files | Only modify cache and registry |
| Use `git stash` on cache | Cache isn't a git repo — use `diff`/`patch` |
