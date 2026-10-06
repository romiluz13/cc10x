#!/usr/bin/env python3
"""Self-contained test for tools/release_gate.py (the one-command release gate).

No framework: drives the runner through its CLI seam (--list, --only) and, for
the failure path, through an in-process main(argv) with a patched GATE_STEPS.

Run:  python3 test_cc10x_release_gate.py    (exit 0 = pass)
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "tools" / "release_gate.py"
EXPECTED_IDS = [
    "harness_audit",
    "doc_consistency_check",
    "prompt_clause_assertions",
    "workflow_replay_check",
    "pytest",
    "suite_qa_phase_invariants",
    "suite_review_package",
    "suite_token_usage_report",
    "plugin_validate",
]

FAILURES = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)


def cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args], capture_output=True, text=True
    )


def load_runner():
    spec = importlib.util.spec_from_file_location("release_gate_under_test", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    r = cli("--list")
    check("--list exits 0", r.returncode == 0, f"rc={r.returncode} err={r.stderr.strip()}")
    check(
        "--list prints exactly the nine step ids in order",
        r.stdout.split() == EXPECTED_IDS,
        repr(r.stdout),
    )

    r = cli("--only", "bogus")
    check("--only bogus exits 2", r.returncode == 2, f"rc={r.returncode}")

    r = cli("--only", "harness_audit")
    check("--only harness_audit exits 0", r.returncode == 0, f"rc={r.returncode} out={r.stdout[-300:]}")

    rg = load_runner()
    check(
        "GATE_STEPS ids match the durable list",
        [s[0] for s in rg.GATE_STEPS] == EXPECTED_IDS,
    )
    check(
        "SCRIPT_STYLE_SUITES names the three script-style suites",
        sorted(rg.SCRIPT_STYLE_SUITES)
        == sorted(
            [
                "test_cc10x_qa_phase_invariants.py",
                "test_cc10x_review_package.py",
                "test_cc10x_token_usage_report.py",
            ]
        ),
    )

    rg.GATE_STEPS = (("always_fails", [sys.executable, "-c", "raise SystemExit(3)"]),)
    check(
        "a failing step makes the runner exit non-zero",
        rg.main(["--only", "always_fails"]) != 0,
    )
    rg.GATE_STEPS = (("always_ok", [sys.executable, "-c", "pass"]),)
    check("a passing step makes the runner exit 0", rg.main(["--only", "always_ok"]) == 0)

    if FAILURES:
        print(f"\nFAILED: {FAILURES}")
        return 1
    print("\nALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
