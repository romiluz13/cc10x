#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_WORKFLOWS = ROOT / ".claude" / "cc10x" / "v10" / "workflows"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def discover_artifacts(use_fixtures: bool) -> list[tuple[str, dict[str, Any]]]:
    items: list[tuple[str, dict[str, Any]]] = []
    if use_fixtures:
        for path in sorted(FIXTURES_DIR.glob("*.json")):
            payload = load_json(path)
            artifact = payload.get("starting_artifact")
            if artifact:
                items.append((path.name, artifact))
        return items

    if not RUNTIME_WORKFLOWS.exists():
        return items

    for path in sorted(RUNTIME_WORKFLOWS.glob("*.json")):
        items.append((path.name, load_json(path)))
    return items


def fmt_seconds(value: Any) -> str:
    if value in (None, "", "unknown"):
        return "unknown"
    if isinstance(value, (int, float)):
        return str(value)
    return str(value)


def summarize(name: str, artifact: dict[str, Any]) -> str:
    telemetry = artifact.get("telemetry") or {}
    agent_wall = telemetry.get("agent_wall_clock_seconds") or {}
    loop_counts = telemetry.get("loop_counts") or {}
    verifier = telemetry.get("verifier") or {}
    verifier_seconds = verifier.get("workload_seconds") or {}

    lines = [
        f"- Workflow: {name}",
        f"  Type: {artifact.get('workflow_type', 'unknown')}",
        f"  Workflow Seconds: {fmt_seconds(telemetry.get('workflow_wall_clock_seconds'))}",
        "  Agent Seconds:"
        f" builder={fmt_seconds(agent_wall.get('builder'))},"
        f" reviewer={fmt_seconds(agent_wall.get('reviewer'))},"
        f" hunter={fmt_seconds(agent_wall.get('hunter'))},"
        f" verifier={fmt_seconds(agent_wall.get('verifier'))}",
        "  Loop Counts:"
        f" re-review={loop_counts.get('re_review', 'unknown')},"
        f" re-hunt={loop_counts.get('re_hunt', 'unknown')},"
        f" re-verify={loop_counts.get('re_verify', 'unknown')}",
        "  Verifier Scope:"
        f" phase_exit_proof_runs={verifier.get('phase_exit_proof_runs', 'unknown')},"
        f" extended_audit_runs={verifier.get('extended_audit_runs', 'unknown')}",
        "  Verifier Workload Seconds:"
        f" tests={fmt_seconds(verifier_seconds.get('tests'))},"
        f" build={fmt_seconds(verifier_seconds.get('build'))},"
        f" scan={fmt_seconds(verifier_seconds.get('scan'))},"
        f" reconcile={fmt_seconds(verifier_seconds.get('reconcile'))},"
        f" reasoning={fmt_seconds(verifier_seconds.get('reasoning'))}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize CC10X workflow latency telemetry."
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Read telemetry from replay fixtures instead of runtime workflow artifacts.",
    )
    args = parser.parse_args()

    artifacts = discover_artifacts(use_fixtures=args.fixtures)
    if not artifacts:
        print("cc10x_latency_audit: no workflow artifacts found")
        return 0

    print("cc10x_latency_audit")
    print(f"source={'fixtures' if args.fixtures else 'runtime'}")
    print(f"workflows={len(artifacts)}")
    for name, artifact in artifacts:
        print(summarize(name, artifact))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
