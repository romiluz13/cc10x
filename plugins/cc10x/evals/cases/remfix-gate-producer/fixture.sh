#!/bin/bash
# Scaffold for remfix-gate-producer: a tiny python module with an unguarded mean(). Runs in the empty run workspace.
set -eu
git init -q -b main
git config user.email "eval@example.invalid"
git config user.name "Eval Fixture"
mkdir -p src tests
touch src/__init__.py
cat > src/stats.py <<'EOF'
def mean(values):
    return sum(values) / len(values)
EOF
cat > tests/test_stats.py <<'EOF'
import unittest

from src.stats import mean


class MeanTest(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3]), 2)


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -q -m "chore: initial commit"
