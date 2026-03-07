#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ROUTER = PLUGIN_ROOT / "skills" / "cc10x-router" / "SKILL.md"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
INVARIANTS = ROOT / "docs" / "router-invariants.md"
REPLAY_CHECK = PLUGIN_ROOT / "scripts" / "cc10x_workflow_replay_check.py"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
REQUIRED_FIXTURES = (
    "plan-direct.json",
    "plan-full.json",
    "plan-clarification.json",
    "build-happy-path.json",
    "build-scope-gate.json",
    "build-remediation-loop.json",
    "debug-fixed.json",
    "debug-research.json",
    "review-advisory.json",
    "verify-fail-closed.json",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    return 1


def main() -> int:
    errors: list[str] = []

    plugin = json.loads(read(PLUGIN_JSON))
    hooks = json.loads(read(HOOKS_JSON))
    marketplace = (
        json.loads(read(MARKETPLACE_JSON)) if MARKETPLACE_JSON.exists() else {}
    )
    router = read(ROUTER)
    readme = read(README)
    changelog = read(CHANGELOG)
    invariants = read(INVARIANTS)

    version = plugin.get("version")
    if f"**Current version:** {version}" not in readme:
        errors.append(
            f"README.md current version does not match plugin.json ({version})"
        )
    if f"## [{version}]" not in changelog:
        errors.append(f"CHANGELOG.md missing release section for {version}")
    if MARKETPLACE_JSON.exists():
        marketplace_version = ((marketplace.get("metadata") or {}).get("version")) or ""
        if marketplace_version != version:
            errors.append(
                f"marketplace.json metadata.version ({marketplace_version}) does not match plugin.json ({version})"
            )
        plugins = marketplace.get("plugins") or []
        if not plugins:
            errors.append("marketplace.json has no plugins entries")
        else:
            plugin_entry = plugins[0]
            if plugin_entry.get("version") != version:
                errors.append(
                    f"marketplace.json plugin entry version ({plugin_entry.get('version')}) does not match plugin.json ({version})"
                )
            if plugin_entry.get("source") != "./plugins/cc10x":
                errors.append(
                    f"marketplace.json plugin source changed unexpectedly ({plugin_entry.get('source')})"
                )

    hook_commands = json.dumps(hooks)
    for script in (
        "cc10x_pretooluse_guard.py",
        "cc10x_posttooluse_artifact_guard.py",
        "cc10x_sessionstart_context.py",
        "cc10x_task_completed_guard.py",
    ):
        if script not in hook_commands:
            errors.append(f"hooks.json does not reference {script}")
        if not (PLUGIN_ROOT / "scripts" / script).exists():
            errors.append(f"missing plugin hook script {script}")

    if not REPLAY_CHECK.exists():
        errors.append("missing workflow replay checker script")
    if not FIXTURES_DIR.exists():
        errors.append("missing workflow replay fixtures directory")
    else:
        for fixture in REQUIRED_FIXTURES:
            if not (FIXTURES_DIR / fixture).exists():
                errors.append(f"missing replay fixture {fixture}")

    for required in ("brightdata", "octocode"):
        if required not in router:
            errors.append(f"router no longer mentions MCP server '{required}'")
        if required not in readme:
            errors.append(
                f"README no longer documents optional MCP server '{required}'"
            )

    required_router_headings = [
        "## 1. Intent Routing",
        "## 2a. Workflow Artifact And Hook Policy",
        "## 3. Task Metadata Contract",
        "Scope-decision resume:",
        "## 8. Post-Agent Validation",
        "## 10. Research Orchestration",
        "## 12. Chain Execution Loop",
        "## 13. Memory Finalization",
        ".events.jsonl",
        "Convergence rule:",
    ]
    for heading in required_router_headings:
        if heading not in router:
            errors.append(f"router missing required heading/text: {heading}")

    required_task_metadata = (
        "wf:",
        "kind:",
        "origin:",
        "phase:",
        "plan:",
        "scope:",
        "reason:",
    )
    for field in required_task_metadata:
        if field not in router:
            errors.append(f"router missing task metadata contract field {field}")

    if "Task Metadata Contract" not in invariants and "Status note:" not in invariants:
        errors.append(
            "router-invariants.md appears malformed or missing the current audit banner"
        )

    expected_router_fields = {
        "component-builder": [
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "bug-investigator": [
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "planner": [
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "integration-verifier": [
            "SCENARIOS_TOTAL",
            "SCENARIOS_PASSED",
            "SCENARIOS_FAILED",
            "REMEDIATION_NEEDED:",
            "REVERT_RECOMMENDED:",
        ],
        "code-reviewer": [
            "REMEDIATION_NEEDED:",
            "REMEDIATION_REASON:",
            "REMEDIATION_SCOPE_REQUESTED:",
            "REVERT_RECOMMENDED:",
        ],
    }

    for agent_name, fields in expected_router_fields.items():
        agent_path = PLUGIN_ROOT / "agents" / f"{agent_name}.md"
        text = read(agent_path)
        for field in fields:
            if field not in text:
                errors.append(
                    f"{agent_name}.md missing expected contract field '{field}'"
                )

    if errors:
        return fail(errors)

    print("cc10x_harness_audit: OK")
    print(f"version={version}")
    print("mcp_servers=user-configured:brightdata,octocode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
