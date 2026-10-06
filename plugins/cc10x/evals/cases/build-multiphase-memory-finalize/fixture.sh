#!/bin/bash
# Scaffold for build-multiphase-memory-finalize: a repo holding an approved two-phase plan. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p docs/plans
cat > docs/plans/two-phase-plan.md <<'EOF'
# Two-phase plan (approved)

## Phase 1: first file
Objective: create phase-one.txt in the repo root containing exactly the line `one`.
Files: phase-one.txt
Required checks: the file exists with that content.
Exit criteria: phase-one.txt exists and contains `one`.
test_seams: file-content check

## Phase 2: second file
Depends on: Phase 1.
Objective: create phase-two.txt in the repo root containing exactly the line `two`.
Files: phase-two.txt
Required checks: the file exists with that content.
Exit criteria: phase-two.txt exists and contains `two`.
test_seams: file-content check
EOF
printf '# Scratch repo\n' > README.md
git add -A
git commit -q -m "chore: initial commit"
