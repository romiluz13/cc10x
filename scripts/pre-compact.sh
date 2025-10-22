#!/bin/bash

# cc10x Pre-Compact Hook
# Creates snapshot before context compaction (auto-healing at 75% tokens)

set -e

SNAPSHOT_DIR=".claude/memory/snapshots"
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
SNAPSHOT_FILE="$SNAPSHOT_DIR/snapshot-$TIMESTAMP.md"

mkdir -p "$SNAPSHOT_DIR"

echo "📸 Creating context snapshot before compaction..."
echo ""

# Create snapshot with current state
cat > "$SNAPSHOT_FILE" << 'EOF'
# Context Snapshot

**Created**: $(date)
**Reason**: Auto-healing context compaction (75% token threshold reached)

## Current Task Status

[Automatically captured before compaction]

### Active Work
- Current feature/bug: [To be filled by Claude]
- Phase: [To be filled by Claude]
- Progress: [To be filled by Claude]

### Key Decisions Made
[Important architecture decisions to preserve]

### Pending Work
[Tasks remaining after compaction]

### Important Discoveries
[Codebase patterns, gotchas, important context]

---

## Recovery Instructions

When resuming after compaction:
1. Load this snapshot
2. Continue from where you left off
3. Reference previous decisions in "Key Decisions Made"
4. User sees seamless continuation

---

**This snapshot allows cc10x to preserve critical context across compactions.**
EOF

echo "✅ Snapshot created: $SNAPSHOT_FILE"
echo ""
echo "🔄 Context will be compacted now. Snapshot preserved for recovery."
echo ""

# Keep only last 10 snapshots
echo "🧹 Cleaning old snapshots (keeping last 10)..."
cd "$SNAPSHOT_DIR"
ls -t snapshot-*.md | tail -n +11 | xargs -r rm --
cd - > /dev/null

echo "✅ Pre-compact snapshot complete"
