from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = "plugins/cc10x/scripts"
TOOLS = "plugins/cc10x/tools"

SCRIPT_STYLE_SUITES = (
    "test_cc10x_qa_phase_invariants.py",
    "test_cc10x_review_package.py",
    "test_cc10x_token_usage_report.py",
)

# Python steps use sys.executable so the gate exercises the interpreter that invoked it.
# argv None means the step has a dedicated resolver (prompt_clause_assertions, pytest, plugin_validate, plugin_test).
GATE_STEPS = (
    ("harness_audit", [sys.executable, f"{TOOLS}/harness_audit.py"]),
    ("doc_consistency_check", [sys.executable, f"{TOOLS}/doc_consistency_check.py"]),
    ("prompt_clause_assertions", None),
    ("workflow_replay_check", [sys.executable, f"{TOOLS}/workflow_replay_check.py"]),
    ("pytest", None),
    ("suite_qa_phase_invariants", [sys.executable, f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[0]}"]),
    ("suite_review_package", [sys.executable, f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[1]}"]),
    ("suite_token_usage_report", [sys.executable, f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[2]}"]),
    ("plugin_validate", None),
    ("plugin_test", None),
)


# Per-step wall-clock cap: the slowest step (pytest) took about 55 s on 2026-10-20, so a hung mod test cannot stall the gate.
STEP_TIMEOUT_S = 600


def run(argv: list[str]) -> int:
    print("$ " + " ".join(argv), flush=True)
    try:
        # Own session so a timeout kills the whole group: `uv run` and `claude plugin test` do their work in grandchildren.
        p = subprocess.Popen(argv, cwd=ROOT, start_new_session=True)
    except OSError as exc:
        print(f"FAIL: cannot execute {argv[0]}: {exc}", flush=True)
        return 1
    try:
        rc = p.wait(timeout=STEP_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        kill_group(p)
        return TIMED_OUT_RC
    except BaseException:
        # Ctrl-C no longer reaches a child in its own session, so take the group down before re-raising.
        kill_group(p)
        raise
    # A background member left by a passing step would keep running and block a `| cat` reader.
    kill_group(p)
    return rc


def kill_group(p: subprocess.Popen) -> None:
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        # macOS answers EPERM, not ESRCH, when the group holds only unreaped zombies.
        pass
    p.wait()


def raise_exit(signum, frame) -> None:
    # SIGTERM/SIGHUP no longer reach a step in its own session; exiting via SystemExit runs run()'s cleanup.
    raise SystemExit(128 + signum)


SKIPPED_RC = -1000
PASSED_NO_YAML_RC = -1001
TIMED_OUT_RC = -1002
CLAUSE_SCRIPT = f"{TOOLS}/prompt_clause_assertions.py"


def run_prompt_clauses(allow_missing: bool) -> int:
    if importlib.util.find_spec("yaml") is not None:
        print("yaml resolution: python3", flush=True)
        return run([sys.executable, CLAUSE_SCRIPT])
    if shutil.which("uv"):
        version = ".".join(map(str, sys.version_info[:3]))
        print(f"yaml resolution: uv run --no-project --python {sys.executable} (Python {version}) --with pyyaml", flush=True)
        return run(
            ["uv", "run", "--no-project", "--with", "pyyaml", "--python", sys.executable, "python", CLAUSE_SCRIPT]
        )
    if allow_missing:
        print("SKIPPED-YAML prompt_clause_assertions: no importable PyYAML and no uv on PATH (--allow-no-yaml)", flush=True)
        rc = run([sys.executable, CLAUSE_SCRIPT, "--allow-no-yaml"])
        return PASSED_NO_YAML_RC if rc == 0 else rc
    print("FAIL prompt_clause_assertions: no importable PyYAML and no uv on PATH (use --allow-no-yaml to skip the YAML parse check)", flush=True)
    return 1


def run_pytest(allow_missing: bool) -> int:
    if importlib.util.find_spec("pytest") is not None:
        print("pytest resolution: python3 -m pytest", flush=True)
        return run([sys.executable, "-m", "pytest", f"{SCRIPTS}", "-q"])
    if shutil.which("uv"):
        version = ".".join(map(str, sys.version_info[:3]))
        print(f"pytest resolution: uv run --no-project --python {sys.executable} (Python {version}) --with pytest", flush=True)
        return run(
            ["uv", "run", "--no-project", "--python", sys.executable, "--with", "pytest", "python", "-m", "pytest", f"{SCRIPTS}", "-q"]
        )
    if allow_missing:
        print("SKIPPED pytest: no importable pytest and no uv on PATH (--allow-no-pytest)", flush=True)
        return SKIPPED_RC
    print("FAIL pytest: no importable pytest and no uv on PATH (use --allow-no-pytest to skip)", flush=True)
    return 1


def run_plugin_validate(allow_missing: bool) -> int:
    if shutil.which("claude"):
        return run(["claude", "plugin", "validate", "plugins/cc10x"])
    if allow_missing:
        print("SKIPPED plugin_validate: claude not on PATH (--allow-no-claude)", flush=True)
        return SKIPPED_RC
    print("FAIL plugin_validate: claude not on PATH (use --allow-no-claude to skip)", flush=True)
    return 1


def run_plugin_test(allow_missing: bool) -> int:
    # claude plugin test exits 1 on a failing test, a load error, or no modules key, so its exit code is the verdict.
    if shutil.which("claude"):
        return run(["claude", "plugin", "test", "plugins/cc10x"])
    if allow_missing:
        print("SKIPPED plugin_test: claude not on PATH (--allow-no-claude)", flush=True)
        return SKIPPED_RC
    print("FAIL plugin_test: claude not on PATH (use --allow-no-claude to skip)", flush=True)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc10x release gate runner")
    parser.add_argument("--list", action="store_true", help="print step ids and exit")
    parser.add_argument("--only", action="append", default=[], metavar="STEP", help="run only this step id (repeatable)")
    parser.add_argument("--strict", action="store_true", help="pass --strict to harness_audit")
    parser.add_argument("--allow-no-pytest", action="store_true")
    parser.add_argument("--allow-no-yaml", action="store_true")
    parser.add_argument("--allow-no-claude", action="store_true")
    args = parser.parse_args(argv)
    previous = {sig: signal.signal(sig, raise_exit) for sig in (signal.SIGTERM, signal.SIGHUP)}
    try:
        return run_gate(args)
    finally:
        for sig, handler in previous.items():
            if handler is not None:
                signal.signal(sig, handler)


def run_gate(args: argparse.Namespace) -> int:

    ids = [step_id for step_id, _ in GATE_STEPS]
    if args.list:
        print("\n".join(ids))
        return 0
    unknown = [s for s in args.only if s not in ids]
    if unknown:
        print(f"unknown step id(s): {', '.join(unknown)}; valid: {', '.join(ids)}", file=sys.stderr)
        return 2

    failed = []
    skipped = []
    yaml_skipped = False
    ran = 0
    for step_id, cmd in GATE_STEPS:
        if args.only and step_id not in args.only:
            continue
        print(f"== {step_id}", flush=True)
        ran += 1
        if step_id == "prompt_clause_assertions":
            rc = run_prompt_clauses(args.allow_no_yaml)
            if rc == PASSED_NO_YAML_RC:
                yaml_skipped, rc = True, 0
        elif step_id == "pytest":
            rc = run_pytest(args.allow_no_pytest)
        elif step_id == "plugin_validate":
            rc = run_plugin_validate(args.allow_no_claude)
        elif step_id == "plugin_test":
            rc = run_plugin_test(args.allow_no_claude)
        else:
            # harness_audit parses --strict itself: it fails while the docs-rot baseline is non-empty.
            rc = run(cmd + (["--strict"] if args.strict and step_id == "harness_audit" else []))
        if rc == TIMED_OUT_RC:
            print(f"FAIL {step_id}: timed out after {STEP_TIMEOUT_S} s", flush=True)
        if rc == SKIPPED_RC:
            skipped.append(step_id)
        elif rc != 0:
            failed.append(step_id)

    if failed:
        print(f"RELEASE GATE: FAIL ({', '.join(failed)})")
        return 1
    if skipped and len(skipped) == ran:
        print(f"RELEASE GATE: NOTHING RAN (SKIPPED: {', '.join(skipped)})")
        return 1
    qualifiers = []
    if skipped:
        qualifiers.append(f"SKIPPED: {', '.join(skipped)}")
    if yaml_skipped:
        qualifiers.append("SKIPPED-YAML")
    if args.only:
        qualifiers.append(f"PARTIAL: {ran} of {len(ids)} steps")
    print("RELEASE GATE: OK" + (f" ({'; '.join(qualifiers)})" if qualifiers else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
