#!/usr/bin/env python3
"""Single source of truth for the workflow replay fixtures.

Both the publication audit (harness_audit.py) and the replay checker
(workflow_replay_check.py) import REQUIRED_FIXTURES from here, so a fixture
added or removed in one place is guarded everywhere. `check_registry_complete`
closes the other direction: a fixture file that exists on disk but is not
registered here is an error, so new fixtures cannot ship unguarded.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("CC10X_REPO_ROOT") or Path(__file__).resolve().parents[3])
if not (ROOT / "plugins" / "cc10x").is_dir():
    raise SystemExit(f"CC10X_REPO_ROOT is not a cc10x repo (no plugins/cc10x): {ROOT}")
PLUGIN_ROOT = ROOT / "plugins" / "cc10x"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"

REQUIRED_FIXTURES = (
    "plan-direct.json",
    "plan-decision-rfc.json",
    "plan-full.json",
    "plan-clarification.json",
    "plan-repo-alignment.json",
    "plan-code-contradiction.json",
    "plan-fresh-review-pass.json",
    "plan-fresh-review-findings.json",
    "plan-fresh-review-exhausted.json",
    "plan-design-handoff.json",
    "build-happy-path.json",
    "build-checkpoint-decision.json",
    "build-phase-blocked.json",
    "build-scope-gate.json",
    "build-remediation-loop.json",
    "build-doc-sync-happy-path.json",
    "build-doc-sync-skipped.json",
    "triage-happy-path.json",
    "codebase-health-happy-path.json",
    "debug-fixed.json",
    "debug-fixed-no-variant.json",
    "debug-research.json",
    "skill-precedence.json",
    "workflow-identity-v10.json",
    "memory-sync-blocking.json",
    "review-advisory.json",
    "verify-fail-closed.json",
    "latency-telemetry.json",
)


def check_registry_complete() -> list[str]:
    """Return error strings for any disk/registry mismatch."""
    errors: list[str] = []
    if not FIXTURES_DIR.exists():
        return ["missing workflow replay fixtures directory"]
    on_disk = {p.name for p in FIXTURES_DIR.glob("*.json")}
    registered = set(REQUIRED_FIXTURES)
    for name in sorted(registered - on_disk):
        errors.append(f"registered fixture missing on disk: {name}")
    for name in sorted(on_disk - registered):
        errors.append(
            f"fixture on disk but not registered in fixture_registry.py: {name}"
        )
    return errors
