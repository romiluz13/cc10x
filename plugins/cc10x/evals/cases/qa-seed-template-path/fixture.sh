#!/bin/bash
# Scaffold for qa-seed-template-path: a repo with a tiny app to QA. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
cat > calc.py <<'EOF'
def add(a, b):
    return a + b
EOF
printf '# Scratch repo\n' > README.md
git add -A
git commit -q -m "chore: initial commit"
