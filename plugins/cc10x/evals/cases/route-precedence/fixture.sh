#!/bin/bash
# Scaffold for route-precedence: a repo with three small source files. Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p src
printf 'def total(items):\n    return sum(items)\n' > src/payments.py
printf 'def add(a, b):\n    return a + b\n' > src/calc.py
printf 'def checkout(cart):\n    return cart[0]\n' > src/checkout.py
printf '# Scratch repo\n' > README.md
git add -A
git commit -q -m "chore: initial commit"
