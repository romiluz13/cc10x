#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cc10x – Lightweight Scope Warning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your request has a LOW complexity score (≤ 2):
  • Single function or single-file trivially scoped changes
  • Minimal risk, no external dependencies, no test changes expected

cc10x is optimized for higher‑risk, multi‑step workflows
(review → plan → build → debug → validate) where orchestration adds value.

You have two options:
  1) Proceed anyway with cc10x workflows (may be overkill)
  2) Handle directly with a simple edit or a focused prompt

Please confirm how you want to proceed: yes/no

Tip: If you choose "yes", cc10x will continue with gates,
delegation to subagents as needed, and evidence‑first verification.
EOF

exit 0

