#!/usr/bin/env python3
"""Self-contained test for tools/release_gate.py (the one-command release gate).

No framework: drives the runner through its CLI seam (--list, --only) and, for
the failure path, through an in-process main(argv) with a patched GATE_STEPS.

Run:  python3 test_cc10x_release_gate.py    (exit 0 = pass)
"""

import contextlib
import importlib.util
import io
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


def run_main(rg, *argv: str):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = rg.main(list(argv))
    return rc, buf.getvalue()


def main() -> int:
    FAILURES.clear()
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

    pristine = rg.GATE_STEPS
    py_argv0 = [step[1][0] for step in pristine if step[1] is not None]
    check(
        "every python step runs under sys.executable",
        bool(py_argv0) and all(a == sys.executable for a in py_argv0),
        repr(py_argv0),
    )

    rg.GATE_STEPS = (("always_fails", [sys.executable, "-c", "raise SystemExit(3)"]),)
    check(
        "a failing step makes the runner exit non-zero",
        rg.main(["--only", "always_fails"]) == 1,
    )
    rg.GATE_STEPS = (("always_ok", [sys.executable, "-c", "pass"]),)
    check("a passing step makes the runner exit 0", rg.main(["--only", "always_ok"]) == 0)

    rc, out = run_main(rg, "--only", "always_ok")
    check("partial run banner is qualified", "RELEASE GATE: OK (PARTIAL: 1 of 1 steps)" in out, out)
    rg.GATE_STEPS = (
        ("a_ok", [sys.executable, "-c", "pass"]),
        ("b_ok", [sys.executable, "-c", "pass"]),
    )
    rc, out = run_main(rg)
    check("full run prints the plain OK banner", rc == 0 and out.strip().endswith("RELEASE GATE: OK"), out)
    rc, out = run_main(rg, "--only", "a_ok", "--only", "b_ok")
    check("--only repeats run both steps", rc == 0 and "== a_ok" in out and "== b_ok" in out, out)
    rc, out = run_main(rg, "--only", "a_ok")
    check("--only a single step runs only it", "== b_ok" not in out and "PARTIAL: 1 of 2" in out, out)

    rg.GATE_STEPS = (("missing_exe", ["/nonexistent/definitely-not-here"]), ("after", [sys.executable, "-c", "pass"]))
    rc, out = run_main(rg)
    check(
        "a missing executable is a step FAIL and later steps still run",
        rc == 1 and "== after" in out and "RELEASE GATE: FAIL (missing_exe)" in out,
        f"rc={rc} out={out}",
    )

    rg = load_runner()
    real_find_spec, real_which = rg.importlib.util.find_spec, rg.shutil.which
    rg.importlib.util.find_spec = lambda name, *a, **k: None if name == "pytest" else real_find_spec(name, *a, **k)
    rg.shutil.which = lambda name, *a, **k: None
    try:
        rg.GATE_STEPS = (
            ("a_ok", [sys.executable, "-c", "pass"]),
            ("b_ok", [sys.executable, "-c", "pass"]),
            ("pytest", None),
            ("plugin_validate", None),
        )
        rc, out = run_main(
            rg, "--only", "a_ok", "--only", "pytest", "--only", "plugin_validate", "--allow-no-pytest", "--allow-no-claude"
        )
        check(
            "skipped steps are named in the banner",
            rc == 0 and "RELEASE GATE: OK (SKIPPED: pytest, plugin_validate; PARTIAL: 3 of 4 steps)" in out,
            out,
        )
        rc, out = run_main(rg, "--only", "pytest", "--allow-no-pytest")
        check("a run where every selected step was skipped exits 1 as NOTHING RAN", rc == 1 and "NOTHING RAN (SKIPPED: pytest)" in out, out)
        rc, out = run_main(rg, "--only", "pytest")
        check("skip without the allow flag fails", rc == 1, f"rc={rc}")
        rg.GATE_STEPS = (
            ("a_ok", [sys.executable, "-c", "pass"]),
            ("pytest", None),
        )
        rc, out = run_main(rg, "--allow-no-pytest")
        check(
            "full run with a skip prints SKIPPED and no PARTIAL",
            rc == 0 and out.strip().endswith("RELEASE GATE: OK (SKIPPED: pytest)") and "PARTIAL" not in out,
            out,
        )

        # uv fallback argv: hermetic, run() captured, find_spec/which patched
        rg.shutil.which = lambda name, *a, **k: "/fake/uv" if name == "uv" else None
        captured = []
        rg.run = lambda argv: captured.append(argv) or 0
        rc, out = run_main(rg, "--only", "pytest")
        argv = captured[0] if captured else []
        check(
            "uv fallback pins the invoking interpreter",
            "--python" in argv and argv[argv.index("--python") + 1] == sys.executable,
            repr(argv),
        )
        check(
            "uv resolution line prints the interpreter version",
            f"{sys.version_info.major}.{sys.version_info.minor}" in out and "uv run" in out,
            out,
        )
    finally:
        rg.importlib.util.find_spec, rg.shutil.which = real_find_spec, real_which

    if FAILURES:
        print(f"\nFAILED: {FAILURES}")
        return 1
    print("\nALL PASS")
    return 0


def test_release_gate_runner() -> None:
    assert main() == 0, f"release gate runner checks failed: {FAILURES}"


if __name__ == "__main__":
    sys.exit(main())
