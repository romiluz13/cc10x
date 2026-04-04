#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TIMEOUT_SECONDS = 900
BLOCKED_PATTERNS = (
    "command not found",
    "no such file or directory",
    "econnrefused",
    "connection refused",
    "enospc",
    "engine",
    "module not found",
    "cannot find module",
)


def fail(message: str, *, exit_code: int = 3) -> int:
    print(json.dumps({"status": "INVALID", "error": message}, indent=2), file=sys.stderr)
    return exit_code


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"manifest is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("manifest root must be a JSON object")
    return payload


def ensure_mapping(name: str, value: Any) -> dict[str, str]:
    if value in (None, {}):
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    normalized: dict[str, str] = {}
    for key, raw in value.items():
        normalized[str(key)] = str(raw)
    return normalized


def ensure_steps(
    name: str, value: Any, *, require_scenario_fields: bool = False
) -> list[dict[str, Any]]:
    if value in (None, []):
        return []
    raw_items = value if isinstance(value, list) else [value]
    if not isinstance(raw_items, list):
        raise ValueError(f"{name} must be an object or array")

    steps: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_items, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"{name}[{index}] must be an object")
        required = ["name", "command", "expected"]
        if require_scenario_fields:
            required.extend(["given", "when", "then"])
        missing = [field for field in required if not raw.get(field)]
        if missing:
            raise ValueError(f"{name}[{index}] missing required fields: {missing}")
        step = dict(raw)
        step["timeout_seconds"] = int(raw.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        step["env"] = ensure_mapping(f"{name}[{index}].env", raw.get("env"))
        steps.append(step)
    return steps


def manifest_workdir(manifest_path: Path, payload: dict[str, Any]) -> Path:
    workdir = payload.get("workdir") or "."
    resolved = Path(workdir)
    if not resolved.is_absolute():
        resolved = (ROOT / resolved).resolve()
    return resolved


def merge_env(base_env: dict[str, str], step_env: dict[str, str]) -> dict[str, str]:
    merged = os.environ.copy()
    merged.update(base_env)
    merged.update(step_env)
    return merged


def detect_blocked(output: str) -> bool:
    lower = output.lower()
    return any(pattern in lower for pattern in BLOCKED_PATTERNS)


def summarize_output(stdout: str, stderr: str, exit_code: int) -> str:
    text = stdout.strip() or stderr.strip()
    if not text:
        return f"exit {exit_code} with no output"
    flattened = " | ".join(line.strip() for line in text.splitlines() if line.strip())
    return flattened[:300]


def run_step(
    step: dict[str, Any],
    *,
    category: str,
    workdir: Path,
    base_env: dict[str, str],
) -> dict[str, Any]:
    env = merge_env(base_env, step.get("env", {}))
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["/bin/zsh", "-lc", step["command"]],
            cwd=workdir,
            env=env,
            text=True,
            capture_output=True,
            timeout=step["timeout_seconds"],
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + "\ncommand timed out"

    duration_seconds = round(time.monotonic() - started, 3)
    combined_output = "\n".join(part for part in (stdout, stderr) if part)
    actual = summarize_output(stdout, stderr, exit_code)
    blocked = detect_blocked(combined_output)
    if exit_code == 0:
        status = "PASS"
    elif blocked or category in {"setup", "reset", "seed", "healthcheck"}:
        status = "BLOCKED"
    else:
        status = "FAIL"

    return {
        "name": step["name"],
        "given": step.get("given", f"{category} prerequisites are satisfied"),
        "when": step.get("when", f"The harness runs `{step['command']}`"),
        "then": step.get("then", step["expected"]),
        "command": step["command"],
        "expected": step["expected"],
        "actual": actual,
        "exit_code": exit_code,
        "status": status,
        "category": category,
        "duration_seconds": duration_seconds,
    }


def required_env_status(
    manifest: dict[str, Any], manifest_path: Path
) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    required = manifest.get("required_env") or []
    if required and not isinstance(required, list):
        raise ValueError("required_env must be an array of environment variable names")
    for key in required:
        if not os.environ.get(str(key)):
            missing.append(str(key))
    details: list[str] = []
    if missing:
        details.append(
            f"manifest {manifest_path} requires environment variables: {', '.join(missing)}"
        )
    return missing, details


def filter_scenarios(scenarios: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for scenario in scenarios:
        scenario_mode = str(scenario.get("mode", "proof"))
        if scenario_mode in {mode, "all"}:
            selected.append(scenario)
    return selected


def overall_status(rows: list[dict[str, Any]], missing_env: list[str]) -> str:
    if missing_env:
        return "BLOCKED"
    statuses = {row["status"] for row in rows}
    if "FAIL" in statuses:
        return "FAIL"
    if "BLOCKED" in statuses:
        return "BLOCKED"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CC10X live harness scenarios.")
    parser.add_argument("--manifest", required=True, help="Path to the harness manifest JSON")
    parser.add_argument(
        "--mode",
        choices=("proof", "stress"),
        default="proof",
        help="Scenario mode to execute",
    )
    parser.add_argument(
        "--json-indent",
        type=int,
        default=2,
        help="Indentation level for JSON output",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (ROOT / manifest_path).resolve()

    try:
        manifest = load_manifest(manifest_path)
        workdir = manifest_workdir(manifest_path, manifest)
        manifest_env = ensure_mapping("environment", manifest.get("environment"))
        setup_steps = ensure_steps("setup", manifest.get("setup"))
        reset_steps = ensure_steps("reset", manifest.get("reset"))
        seed_steps = ensure_steps("seed", manifest.get("seed"))
        cleanup_steps = ensure_steps("cleanup", manifest.get("cleanup"))
        scenarios = ensure_steps(
            "scenarios", manifest.get("scenarios"), require_scenario_fields=True
        )
        healthcheck = ensure_steps("healthcheck", manifest.get("healthcheck"))
    except ValueError as exc:
        return fail(str(exc))

    missing_env, errors = required_env_status(manifest, manifest_path)
    selected_scenarios = filter_scenarios(scenarios, args.mode)
    if not selected_scenarios:
        errors.append(f"manifest {manifest_path} has no scenarios for mode={args.mode}")

    rows: list[dict[str, Any]] = []
    skipped: list[str] = []
    preflight_failed = bool(errors)
    sequence: list[tuple[str, list[dict[str, Any]]]] = [
        ("setup", setup_steps),
        ("reset", reset_steps),
        ("seed", seed_steps),
        ("healthcheck", healthcheck),
    ]

    for category, steps in sequence:
        if preflight_failed:
            break
        for step in steps:
            row = run_step(step, category=category, workdir=workdir, base_env=manifest_env)
            rows.append(row)
            if row["status"] != "PASS":
                preflight_failed = True
                break

    if preflight_failed:
        skipped = [scenario["name"] for scenario in selected_scenarios]
    else:
        for scenario in selected_scenarios:
            rows.append(
                run_step(
                    scenario,
                    category=args.mode,
                    workdir=workdir,
                    base_env=manifest_env,
                )
            )

    for step in cleanup_steps:
        rows.append(run_step(step, category="cleanup", workdir=workdir, base_env=manifest_env))

    status = overall_status(rows, missing_env)
    summary = {
        "manifest": str(manifest_path),
        "mode": args.mode,
        "status": status,
        "workdir": str(workdir),
        "errors": errors,
        "missing_env": missing_env,
        "skipped_scenarios": skipped,
        "summary": {
            "total": len(rows),
            "passed": sum(1 for row in rows if row["status"] == "PASS"),
            "failed": sum(1 for row in rows if row["status"] == "FAIL"),
            "blocked": sum(1 for row in rows if row["status"] == "BLOCKED"),
        },
        "scenarios": rows,
    }
    print(json.dumps(summary, indent=args.json_indent))
    if status == "PASS":
        return 0
    if status == "BLOCKED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
