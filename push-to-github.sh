#!/bin/bash
# Push version 3.1.0 changes to GitHub

set -e

echo "🚀 Pushing version 3.1.0 to GitHub..."

# Navigate to worktree
cd /Users/rom.iluz/.cursor/worktrees/cc10x/OZn9l

echo "📦 Checking git status..."
git status --short

echo "➕ Staging all changes..."
git add -A

echo "💾 Committing changes..."
git commit -m "fix: Version 3.1.0, hook fixes, and contributor attribution

- Fix session-start.sh to create memory directory before logging
- Bump version to 3.1.0 across all files (marketplace.json, plugin.json, README.md, hooks)
- Add explicit hooks reference in plugin.json (best practice)
- Add .mailmap file to attribute all contributions to Rom Iluz
- Add comprehensive marketplace audit documentation" || echo "No changes to commit (may already be committed)"

echo "📤 Pushing to feature branch..."
git push origin 2025-10-29-lnzt-OZn9l

echo "🔄 Merging to main..."
cd /Users/rom.iluz/Dev/cc10x_v3/cc10x
git fetch origin
git merge origin/2025-10-29-lnzt-OZn9l --no-edit

echo "📤 Pushing to main..."
git push origin main

echo "✅ Done! Version 3.1.0 is now on GitHub!"
echo ""
echo "📋 Latest commits:"
git log --oneline -3

