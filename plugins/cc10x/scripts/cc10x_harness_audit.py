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
PROMPT_INVARIANTS = ROOT / "docs" / "prompt-invariants.md"
PROMPT_SURFACE_INVENTORY = ROOT / "docs" / "prompt-surface-inventory.md"
PROMPT_CHANGE_CHECKLIST = ROOT / "docs" / "prompt-change-checklist.md"
VERIFIER_LATENCY_MODEL = ROOT / "docs" / "verifier-latency-model.md"
LATENCY_REDUCTION_NOTE = ROOT / "docs" / "latency-reduction-note.md"
REPLAY_CHECK = PLUGIN_ROOT / "scripts" / "cc10x_workflow_replay_check.py"
LATENCY_AUDIT = PLUGIN_ROOT / "scripts" / "cc10x_latency_audit.py"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
FIRST_PLACE_STRATEGY = (
    ROOT / "docs" / "benchmarks" / "2026-03-12-first-place-strategy.md"
)
PROMPT_STEAL_NOTE = (
    ROOT / "docs" / "benchmarks" / "2026-03-14-prompt-steal-hardening.md"
)
PLANNING_RECOVERY_NOTE = (
    ROOT / "docs" / "benchmarks" / "2026-03-16-planning-recovery.md"
)
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
    "build-happy-path.json",
    "build-checkpoint-decision.json",
    "build-phase-blocked.json",
    "build-scope-gate.json",
    "build-remediation-loop.json",
    "debug-fixed.json",
    "debug-research.json",
    "skill-precedence.json",
    "workflow-identity-v10.json",
    "memory-sync-blocking.json",
    "review-advisory.json",
    "verify-fail-closed.json",
    "latency-telemetry.json",
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
    prompt_invariants = read(PROMPT_INVARIANTS)
    prompt_surface_inventory = read(PROMPT_SURFACE_INVENTORY)
    prompt_change_checklist = read(PROMPT_CHANGE_CHECKLIST)
    verifier_latency_model = read(VERIFIER_LATENCY_MODEL)
    latency_reduction_note = read(LATENCY_REDUCTION_NOTE)

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
    if not FIRST_PLACE_STRATEGY.exists():
        errors.append("missing first-place strategy document")
    if not PROMPT_INVARIANTS.exists():
        errors.append("missing prompt invariant registry")
    if not PROMPT_SURFACE_INVENTORY.exists():
        errors.append("missing prompt surface inventory")
    if not PROMPT_CHANGE_CHECKLIST.exists():
        errors.append("missing prompt change checklist")
    if not PROMPT_STEAL_NOTE.exists():
        errors.append("missing latest prompt benchmark note")
    if not PLANNING_RECOVERY_NOTE.exists():
        errors.append("missing planning recovery benchmark note")
    if not VERIFIER_LATENCY_MODEL.exists():
        errors.append("missing verifier latency model")
    if not LATENCY_REDUCTION_NOTE.exists():
        errors.append("missing latency reduction note")
    if not LATENCY_AUDIT.exists():
        errors.append("missing latency audit script")

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
        ".claude/cc10x/v10/workflows",
        "workflow_uuid",
        "phase_cursor",
        "plan_mode",
        "verification_rigor",
        "proof_status",
        "traceability",
        "telemetry",
        "planning_review_runs",
        "planning_review_findings",
        "planning_review_status",
        "task_metrics_available",
        "phase_exit_proof_runs",
        "extended_audit_runs",
        "plan_trust_gate",
        "phase_exit_gate",
        "skill_precedence_gate",
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
    if "Prompt Behavioral Invariant Registry" not in prompt_invariants:
        errors.append("prompt-invariants.md appears malformed")
    if "Prompt Surface Inventory" not in prompt_surface_inventory:
        errors.append("prompt-surface-inventory.md appears malformed")
    if "Prompt Change Checklist" not in prompt_change_checklist:
        errors.append("prompt-change-checklist.md appears malformed")
    if "Verifier Latency Model" not in verifier_latency_model:
        errors.append("verifier-latency-model.md appears malformed")
    if "Latency Reduction Note" not in latency_reduction_note:
        errors.append("latency-reduction-note.md appears malformed")

    expected_router_fields = {
        "component-builder": [
            "PHASE_ID:",
            "PHASE_STATUS:",
            "PHASE_EXIT_READY:",
            "CHECKPOINT_TYPE:",
            "PROOF_STATUS:",
            "INPUTS:",
            "EXPECTED_ARTIFACTS:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "BLOCKED_ITEMS:",
            "SKIPPED_ITEMS:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "bug-investigator": [
            "VERIFICATION_RIGOR:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "BLAST_RADIUS_SCAN:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "planner": [
            "PLAN_MODE:",
            "VERIFICATION_RIGOR:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "OPEN_DECISIONS:",
            "DIFFERENCES_FROM_AGREEMENT:",
            "PLANNING_REVIEW_STATUS:",
            "PLANNING_REVIEW_RUNS:",
            "ALTERNATIVES:",
            "DRAWBACKS:",
            "PROVABLE_PROPERTIES:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "plan-gap-reviewer": [
            'CONTRACT {"s":"PASS","b":false,"bf":0}',
            "## Planning Review: Pass",
            "PLANNING_REVIEW_STATUS:",
            "BLOCKING_FINDINGS_COUNT:",
            "FINDING_BUCKETS:",
            "REPLAN_NEEDED:",
            "REPLAN_REASON:",
        ],
        "integration-verifier": [
            "Proof Status:",
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

    prompt_phrase_guards = {
        "planner": [
            "The first draft must be decisive, but not by inventing facts",
            "Do not finalize a non-trivial plan before comparing it against the current codebase",
            "Codebase Reality Check",
            "Plan-vs-Code Gaps",
            "Assumption Ledger",
            "Phase Dependency Map",
            "Open decisions belong in the plan, not in hidden assumptions",
            "recommended defaults stay unapproved",
            "Differences From Agreement",
        ],
        "component-builder": [
            "Task completion is not goal achievement",
            "Treat the approved phase as the contract",
            "Do not improvise outside it",
        ],
        "integration-verifier": [
            "Task completion is not goal achievement",
            "Do NOT trust prior summaries, status text, or builder confidence claims",
            "**Truths:** what must be TRUE",
            "**Artifacts:** what must EXIST",
            "**Wiring:** what must be WIRED",
            "## Verification Scope Classification (MANDATORY)",
            "### Timing & Workload",
        ],
        "plan-review-gate": [
            'No leniency. "Close enough" is FAIL.',
            'There is no "APPROVED WITH COMMENTS"',
            "A structurally neat but repo-wrong plan is FAIL.",
            "invented or unverified file/module assumptions",
            "missing touched surfaces or integration points",
            "This gate is an auditor, not a collaborator",
        ],
        "plan-gap-reviewer": [
            "Freshness rule:",
            "Do NOT load `.claude/cc10x/v10/*.md`.",
            "Return structured findings only.",
            "You do not own orchestration, plan approval, or plan edits.",
        ],
    }
    for stem, phrases in prompt_phrase_guards.items():
        path = (
            PLUGIN_ROOT / "agents" / f"{stem}.md"
            if (PLUGIN_ROOT / "agents" / f"{stem}.md").exists()
            else PLUGIN_ROOT / "skills" / stem / "SKILL.md"
        )
        text = read(path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{path.name} missing prompt safety phrase '{phrase}'")

    verification_skill = read(
        PLUGIN_ROOT / "skills" / "verification-before-completion" / "SKILL.md"
    )
    for phrase in (
        "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE",
        "Skip any step = lying, not verifying",
        "**Truths:** What must be TRUE?",
        "**Artifacts:** What must EXIST?",
        "**Wiring:** What must be WIRED?",
        "## Phase-Exit Proof vs Extended Audit",
    ):
        if phrase not in verification_skill:
            errors.append(
                "verification-before-completion missing prompt safety phrase "
                f"'{phrase}'"
            )

    description_hygiene = {
        PLUGIN_ROOT
        / "skills"
        / "frontend-patterns"
        / "SKILL.md": (
            'description: "Use when',
            "workflow",
        ),
        PLUGIN_ROOT
        / "skills"
        / "debugging-patterns"
        / "SKILL.md": (
            'description: "Use when',
            "workflow",
        ),
        PLUGIN_ROOT
        / "skills"
        / "verification-before-completion"
        / "SKILL.md": (
            'description: "Use when',
            "workflow",
        ),
        PLUGIN_ROOT
        / "skills"
        / "plan-review-gate"
        / "SKILL.md": (
            'description: "Use after',
            "workflow",
        ),
    }
    for path, (required_prefix, banned_word) in description_hygiene.items():
        text = read(path)
        if required_prefix not in text:
            errors.append(
                f"{path.name} description no longer matches trigger-style format"
            )
        first_lines = "\n".join(text.splitlines()[:6]).lower()
        if banned_word in first_lines:
            errors.append(f"{path.name} description appears to summarize workflow")

    if errors:
        return fail(errors)

    print("cc10x_harness_audit: OK")
    print(f"version={version}")
    print("mcp_servers=user-configured:brightdata,octocode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
