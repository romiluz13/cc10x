from __future__ import annotations

import argparse
import importlib.util
import shutil
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

# argv None means the step has a dedicated resolver (pytest, plugin_validate).
GATE_STEPS = (
    ("harness_audit", ["python3", f"{TOOLS}/harness_audit.py"]),
    ("doc_consistency_check", ["python3", f"{TOOLS}/doc_consistency_check.py"]),
    ("prompt_clause_assertions", ["python3", f"{TOOLS}/prompt_clause_assertions.py"]),
    ("workflow_replay_check", ["python3", f"{TOOLS}/workflow_replay_check.py"]),
    ("pytest", None),
    ("suite_qa_phase_invariants", ["python3", f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[0]}"]),
    ("suite_review_package", ["python3", f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[1]}"]),
    ("suite_token_usage_report", ["python3", f"{SCRIPTS}/{SCRIPT_STYLE_SUITES[2]}"]),
    ("plugin_validate", None),
)


def run(argv: list[str]) -> int:
    print("$ " + " ".join(argv), flush=True)
    return subprocess.run(argv, cwd=ROOT).returncode


def run_pytest(allow_missing: bool) -> int:
    if importlib.util.find_spec("pytest") is not None:
        print("pytest resolution: python3 -m pytest", flush=True)
        return run([sys.executable, "-m", "pytest", f"{SCRIPTS}", "-q"])
    if shutil.which("uv"):
        print("pytest resolution: uv run --no-project --with pytest", flush=True)
        return run(
            ["uv", "run", "--no-project", "--with", "pytest", "python", "-m", "pytest", f"{SCRIPTS}", "-q"]
        )
    if allow_missing:
        print("SKIPPED pytest: no importable pytest and no uv on PATH (--allow-no-pytest)", flush=True)
        return 0
    print("FAIL pytest: no importable pytest and no uv on PATH (use --allow-no-pytest to skip)", flush=True)
    return 1


def run_plugin_validate(allow_missing: bool) -> int:
    if shutil.which("claude"):
        return run(["claude", "plugin", "validate", "plugins/cc10x"])
    if allow_missing:
        print("SKIPPED plugin_validate: claude not on PATH (--allow-no-claude)", flush=True)
        return 0
    print("FAIL plugin_validate: claude not on PATH (use --allow-no-claude to skip)", flush=True)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc10x release gate runner")
    parser.add_argument("--list", action="store_true", help="print step ids and exit")
    parser.add_argument("--only", action="append", default=[], metavar="STEP", help="run only this step id (repeatable)")
    parser.add_argument("--strict", action="store_true", help="pass --strict to harness_audit")
    parser.add_argument("--allow-no-pytest", action="store_true")
    parser.add_argument("--allow-no-claude", action="store_true")
    args = parser.parse_args(argv)

    ids = [step_id for step_id, _ in GATE_STEPS]
    if args.list:
        print("\n".join(ids))
        return 0
    unknown = [s for s in args.only if s not in ids]
    if unknown:
        print(f"unknown step id(s): {', '.join(unknown)}; valid: {', '.join(ids)}", file=sys.stderr)
        return 2

    failed = []
    for step_id, cmd in GATE_STEPS:
        if args.only and step_id not in args.only:
            continue
        print(f"== {step_id}", flush=True)
        if step_id == "pytest":
            rc = run_pytest(args.allow_no_pytest)
        elif step_id == "plugin_validate":
            rc = run_plugin_validate(args.allow_no_claude)
        else:
            rc = run(cmd + (["--strict"] if args.strict and step_id == "harness_audit" else []))
        if rc != 0:
            failed.append(step_id)

    if failed:
        print(f"RELEASE GATE: FAIL ({', '.join(failed)})")
        return 1
    print("RELEASE GATE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
