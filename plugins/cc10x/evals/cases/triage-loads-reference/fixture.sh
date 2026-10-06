#!/bin/bash
# Scaffold for triage-loads-reference: a repo with one incoming issue file. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p issues
cat > issues/ISSUE-1.md <<'EOF'
# ISSUE-1: Export button does nothing

Reporter says clicking Export on the reports page has no effect since last week's release. No error shown. Not yet reproduced.
EOF
printf '# Scratch repo\n' > README.md
git add -A
git commit -q -m "chore: initial commit"
