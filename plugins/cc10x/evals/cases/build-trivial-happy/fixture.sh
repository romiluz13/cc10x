#!/bin/bash
# Scaffold for build-trivial-happy: a tiny git repo with one tracked file. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
printf '# Scratch repo\n\nA one-file project used to exercise a trivial BUILD.\n' > README.md
git add README.md
git commit -q -m "chore: initial commit"
