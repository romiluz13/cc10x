#!/usr/bin/env python3
"""Self-contained test for tools/release_gate.py (the one-command release gate).

No framework: drives the runner through its CLI seam (--list, --only) and, for
the failure path, through an in-process main(argv) with a patched GATE_STEPS.

Run:  python3 test_cc10x_release_gate.py    (exit 0 = pass)
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import signal
import subprocess
import sys
import tempfile
import time
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
    "plugin_test",
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
        "--list prints exactly the ten step ids in order",
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
            ("plugin_test", None),
        )
        rc, out = run_main(
            rg, "--only", "a_ok", "--only", "pytest", "--only", "plugin_validate", "--only", "plugin_test",
            "--allow-no-pytest", "--allow-no-claude",
        )
        check(
            "skipped steps are named in the banner",
            rc == 0 and "RELEASE GATE: OK (SKIPPED: pytest, plugin_validate, plugin_test; PARTIAL: 4 of 5 steps)" in out
            and "SKIPPED plugin_test: claude not on PATH (--allow-no-claude)" in out,
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

        # PyYAML resolution for prompt_clause_assertions: hermetic, run() captured
        rg = load_runner()
        rg.GATE_STEPS = (("prompt_clause_assertions", None),)
        have = {"yaml": True}
        rg.importlib.util.find_spec = lambda name, *a, **k: object() if name == "yaml" and have["yaml"] else (
            None if name == "yaml" else real_find_spec(name, *a, **k)
        )
        captured = []
        rg.run = lambda argv: captured.append(argv) or 0
        script = "plugins/cc10x/tools/prompt_clause_assertions.py"
        rc, out = run_main(rg)
        check(
            "yaml importable: the step runs plainly under sys.executable",
            rc == 0 and captured == [[sys.executable, script]] and "yaml resolution: python3" in out,
            f"{captured} {out}",
        )
        have["yaml"] = False
        rg.shutil.which = lambda name, *a, **k: "/fake/uv" if name == "uv" else None
        captured.clear()
        rc, out = run_main(rg)
        argv = captured[0] if captured else []
        check(
            "yaml missing with uv: runs through uv with pyyaml pinned to the invoking interpreter",
            argv[:3] == ["uv", "run", "--no-project"]
            and "--with" in argv
            and argv[argv.index("--with") + 1] == "pyyaml"
            and argv[argv.index("--python") + 1] == sys.executable
            and argv[-2:] == ["python", script]
            and "yaml resolution: uv run" in out
            and "--allow-no-yaml" not in argv,
            f"{argv} {out}",
        )
        rg.shutil.which = lambda name, *a, **k: None
        captured.clear()
        rc, out = run_main(rg)
        check(
            "yaml missing and no uv: the step FAILS and names the flag",
            rc == 1 and not captured and "FAIL prompt_clause_assertions" in out and "--allow-no-yaml" in out,
            f"rc={rc} {captured} {out}",
        )

        # plugin_test: hermetic, which() and run() patched
        rg.GATE_STEPS = (("plugin_test", None),)
        captured.clear()
        rc, out = run_main(rg, "--only", "plugin_test")
        check(
            "claude absent without --allow-no-claude: plugin_test FAILS, not skipped",
            rc == 1 and not captured
            and "FAIL plugin_test: claude not on PATH" in out
            and "RELEASE GATE: FAIL (plugin_test)" in out,
            f"rc={rc} {captured} {out}",
        )
        rg.shutil.which = lambda name, *a, **k: "/fake/claude" if name == "claude" else None
        rc, out = run_main(rg, "--only", "plugin_test")
        check(
            "claude present: plugin_test runs exactly `claude plugin test plugins/cc10x`",
            rc == 0 and captured == [["claude", "plugin", "test", "plugins/cc10x"]],
            f"rc={rc} {captured} {out}",
        )
        rg.shutil.which = lambda name, *a, **k: None
        rg.GATE_STEPS = (("prompt_clause_assertions", None),)
        captured.clear()
        rc, out = run_main(rg, "--allow-no-yaml")
        check(
            "yaml missing, no uv, --allow-no-yaml: flag passes through and the banner says SKIPPED-YAML",
            rc == 0
            and captured == [[sys.executable, script, "--allow-no-yaml"]]
            and out.strip().endswith("RELEASE GATE: OK (SKIPPED-YAML)"),
            f"rc={rc} {captured} {out}",
        )
    finally:
        rg.importlib.util.find_spec, rg.shutil.which = real_find_spec, real_which

    with tempfile.TemporaryDirectory() as tmp:
        process_group_checks(Path(tmp))

    if FAILURES:
        print(f"\nFAILED: {FAILURES}")
        return 1
    print("\nALL PASS")
    return 0


def pid_gone(pid: int, polls: int = 20) -> bool:
    for _ in range(polls):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        time.sleep(0.1)
    os.kill(pid, 9)  # clean up the leaked process this test started
    return False


def process_group_checks(tmp: Path) -> None:
    # step timeout: a hung step is a named FAIL, its child is killed, and later steps still run
    rg = load_runner()
    pid_file = tmp / "pid"
    sleeper = f"import os, time; open({str(pid_file)!r}, 'w').write(str(os.getpid())); time.sleep(30)"
    rg.STEP_TIMEOUT_S = 1
    rg.GATE_STEPS = (("sleeper", [sys.executable, "-c", sleeper]), ("after", [sys.executable, "-c", "pass"]))
    started = time.monotonic()
    rc, out = run_main(rg)
    elapsed = time.monotonic() - started
    check(
        "a step past the timeout FAILS by name and the gate moves on",
        rc == 1 and elapsed < 15
        and "FAIL sleeper: timed out after 1 s" in out
        and "== after" in out
        and "RELEASE GATE: FAIL (sleeper)" in out,
        f"rc={rc} elapsed={elapsed:.1f} {out}",
    )
    child_gone = False
    if pid_file.exists():
        try:
            os.kill(int(pid_file.read_text()), 0)
        except ProcessLookupError:
            child_gone = True
    check("the timed-out child is killed", child_gone, f"pid_file={pid_file.exists()}")

    # a wrapper step (like `uv run` or `claude plugin test`) whose real work is a grandchild: the whole group dies
    gc_pid_file = tmp / "grandchild_pid"
    grandchild = f"import os, time; open({str(gc_pid_file)!r}, 'w').write(str(os.getpid())); time.sleep(30)"
    wrapper = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {grandchild!r}]); time.sleep(30)"
    rg.GATE_STEPS = (("wrapper", [sys.executable, "-c", wrapper]),)
    rc, out = run_main(rg)
    gc_pid = int(gc_pid_file.read_text()) if gc_pid_file.exists() else None
    gc_gone = False
    if gc_pid is not None:
        for _ in range(20):
            try:
                os.kill(gc_pid, 0)
            except ProcessLookupError:
                gc_gone = True
                break
            time.sleep(0.1)
        if not gc_gone:
            os.kill(gc_pid, 9)  # clean up the leaked grandchild this test started
    check(
        "a timed-out step's grandchild is killed with its process group",
        rc == 1 and "FAIL wrapper: timed out after 1 s" in out and gc_gone,
        f"rc={rc} gc_pid={gc_pid} gone={gc_gone} {out}",
    )
    check("the real step timeout is generous (>= 600 s)", getattr(load_runner(), "STEP_TIMEOUT_S", 0) >= 600)

    # SIGTERM to the gate (terminal close, `kill`) takes the running step's group down; the gate exits 143
    term_pid_file = tmp / "term_grandchild_pid"
    term_grandchild = f"import os, time; open({str(term_pid_file)!r}, 'w').write(str(os.getpid())); time.sleep(30)"
    term_wrapper = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {term_grandchild!r}]); time.sleep(30)"
    driver = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('rg', {str(RUNNER)!r})\n"
        "rg = importlib.util.module_from_spec(spec); spec.loader.exec_module(rg)\n"
        f"rg.GATE_STEPS = (('wrapper', [sys.executable, '-c', {term_wrapper!r}]),)\n"
        "sys.exit(rg.main([]))\n"
    )
    gate = subprocess.Popen([sys.executable, "-c", driver], stdout=subprocess.DEVNULL)
    for _ in range(100):
        if term_pid_file.exists() and term_pid_file.read_text():
            break
        time.sleep(0.1)
    gate.send_signal(signal.SIGTERM)
    try:
        gate_rc = gate.wait(timeout=10)
    except subprocess.TimeoutExpired:
        gate.kill()
        gate_rc = gate.wait()
    term_gc_pid = int(term_pid_file.read_text()) if term_pid_file.exists() else None
    term_gc_gone = term_gc_pid is not None and pid_gone(term_gc_pid)
    check(
        "SIGTERM to the gate exits 143 and kills the running step's grandchild",
        gate_rc == 143 and term_gc_gone,
        f"rc={gate_rc} gc_pid={term_gc_pid} gone={term_gc_gone}",
    )
    rg = load_runner()
    before = signal.getsignal(signal.SIGTERM), signal.getsignal(signal.SIGHUP)
    rg.GATE_STEPS = (("noop", [sys.executable, "-c", "pass"]),)
    run_main(rg)
    check(
        "an in-process main() restores the previous SIGTERM and SIGHUP handlers",
        (signal.getsignal(signal.SIGTERM), signal.getsignal(signal.SIGHUP)) == before,
    )

    # a step that exits normally leaves no background member of its group running
    bg_pid_file = tmp / "bg_pid"
    rg.GATE_STEPS = (("bg", ["sh", "-c", f"sleep 30 & echo $! > {bg_pid_file}; exit 0"]),)
    rc, out = run_main(rg)
    bg_pid = int(bg_pid_file.read_text()) if bg_pid_file.exists() else None
    bg_gone = bg_pid is not None and pid_gone(bg_pid)
    check(
        "a passing step's background grandchild is killed after it exits",
        rc == 0 and bg_gone,
        f"rc={rc} bg_pid={bg_pid} gone={bg_gone} {out}",
    )

    # kill_group on a group whose only member is an unreaped zombie (EPERM on macOS) does not raise
    zombie = subprocess.Popen([sys.executable, "-c", "pass"], start_new_session=True)
    time.sleep(0.5)  # let it exit without reaping it
    try:
        rg.kill_group(zombie)
        zombie_ok, zombie_err = True, ""
    except Exception as exc:  # noqa: BLE001 - the check reports any escape
        zombie_ok, zombie_err = False, repr(exc)
        zombie.wait()
    check("kill_group on a zombie-only group does not raise", zombie_ok, zombie_err)


def test_release_gate_runner() -> None:
    assert main() == 0, f"release gate runner checks failed: {FAILURES}"


if __name__ == "__main__":
    sys.exit(main())
