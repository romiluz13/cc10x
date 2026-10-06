#!/bin/bash
# Scaffold for seam-gate: a repo with an approved one-phase plan that names its test seam. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p docs/plans src tests
touch src/__init__.py
cat > docs/plans/slug-plan.md <<'EOF'
# Slug plan (approved)

## Phase 1: slugify
Objective: add `slugify(text)` to src/slug.py returning lowercase text with runs of non-alphanumerics replaced by a single hyphen, and a unittest in tests/test_slug.py.
Files: src/slug.py, tests/test_slug.py
Required checks: `python3 -m unittest discover -s tests` passes.
Exit criteria: slugify("Hello, World") == "hello-world" is covered by a passing test.

### Test Seams
- slugify public function
EOF
printf '# Scratch repo\n' > README.md
git add -A
git commit -q -m "chore: initial commit"
