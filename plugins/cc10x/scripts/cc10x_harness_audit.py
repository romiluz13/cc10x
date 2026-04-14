#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ROUTER = PLUGIN_ROOT / "skills" / "cc10x-router" / "SKILL.md"
ROUTER_REFERENCES_DIR = PLUGIN_ROOT / "skills" / "cc10x-router" / "references"
ROUTER_ARTIFACT_POLICY_REFERENCE = (
    ROUTER_REFERENCES_DIR / "workflow-artifact-and-hook-policy.md"
)
ROUTER_BUILD_REFERENCE = ROUTER_REFERENCES_DIR / "build-workflow.md"
ROUTER_DEBUG_REFERENCE = ROUTER_REFERENCES_DIR / "debug-workflow.md"
ROUTER_REVIEW_REFERENCE = ROUTER_REFERENCES_DIR / "review-workflow.md"
ROUTER_PLAN_REFERENCE = ROUTER_REFERENCES_DIR / "plan-workflow.md"
ROUTER_REMEDIATION_REFERENCE = ROUTER_REFERENCES_DIR / "remediation-and-research.md"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
TASK_COMPLETED_GUARD = PLUGIN_ROOT / "scripts" / "cc10x_task_completed_guard.py"
INVARIANTS = ROOT / "docs" / "router-invariants.md"
PROMPT_INVARIANTS = ROOT / "docs" / "prompt-invariants.md"
PROMPT_SURFACE_INVENTORY = ROOT / "docs" / "prompt-surface-inventory.md"
PROMPT_CHANGE_CHECKLIST = ROOT / "docs" / "prompt-change-checklist.md"
ORCHESTRATION_BIBLE = ROOT / "docs" / "cc10x-orchestration-bible.md"
ORCHESTRATION_LOGIC = ROOT / "docs" / "cc10x-orchestration-logic-analysis.md"
ORCHESTRATION_SAFETY = ROOT / "docs" / "cc10x-orchestration-safety.md"
AGENT_CONTRACT_REGISTRY = ROOT / "docs" / "agent-contract-registry.md"
VERIFIER_LATENCY_MODEL = ROOT / "docs" / "verifier-latency-model.md"
LATENCY_REDUCTION_NOTE = ROOT / "docs" / "latency-reduction-note.md"
REPLAY_CHECK = PLUGIN_ROOT / "scripts" / "cc10x_workflow_replay_check.py"
LATENCY_AUDIT = PLUGIN_ROOT / "scripts" / "cc10x_latency_audit.py"
LIVE_HARNESS_RUNNER = PLUGIN_ROOT / "scripts" / "cc10x_live_harness_runner.py"
SESSION_MEMORY_SKILL = PLUGIN_ROOT / "skills" / "session-memory" / "SKILL.md"
PLANNER_AGENT = PLUGIN_ROOT / "agents" / "planner.md"
PLANNING_PATTERNS_SKILL = PLUGIN_ROOT / "skills" / "planning-patterns" / "SKILL.md"
BRAINSTORMING_SKILL = PLUGIN_ROOT / "skills" / "brainstorming" / "SKILL.md"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
LIVE_MANIFEST_TEMPLATE = PLUGIN_ROOT / "templates" / "live-harness.template.json"
PLANNING_LIVE_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "planning-patterns"
    / "references"
    / "live-verification-strategy.md"
)
VERIFY_LIVE_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "verification-before-completion"
    / "references"
    / "live-production-testing.md"
)
LIVE_MANIFEST_BOOTSTRAP = (
    PLUGIN_ROOT / "tests" / "live" / "manifests" / "cc10x-bootstrap.json"
)
DEBUGGING_PLAYBOOKS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "debugging-patterns"
    / "references"
    / "root-cause-playbooks.md"
)
DEBUGGING_HYGIENE_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "debugging-patterns"
    / "references"
    / "investigation-hygiene.md"
)
REVIEW_ORDER_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "code-review-patterns"
    / "references"
    / "review-order-and-checkpoints.md"
)
REVIEW_SECURITY_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "code-review-patterns"
    / "references"
    / "security-review-checklist.md"
)
REVIEW_HEURISTICS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "code-review-patterns"
    / "references"
    / "code-review-heuristics.md"
)
FRONTEND_STATE_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend-patterns"
    / "references"
    / "ui-state-and-feedback.md"
)
FRONTEND_A11Y_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend-patterns"
    / "references"
    / "accessibility-and-forms.md"
)
FRONTEND_LAYOUT_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend-patterns"
    / "references"
    / "performance-and-layout.md"
)
FRONTEND_DESIGN_MD_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend-patterns"
    / "references"
    / "design-md-authoring.md"
)
FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend-patterns"
    / "references"
    / "design-md-inspiration-index.md"
)
TDD_PATTERNS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "test-driven-development"
    / "references"
    / "testing-patterns.md"
)
TDD_MOCKS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "test-driven-development"
    / "references"
    / "test-data-and-mocks.md"
)
TDD_LIVE_PROOF_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "test-driven-development"
    / "references"
    / "integration-and-live-proof.md"
)
SESSION_MEMORY_MODEL_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "session-memory"
    / "references"
    / "memory-model-and-ownership.md"
)
SESSION_MEMORY_OPERATIONS_REFERENCE = (
    PLUGIN_ROOT / "skills" / "session-memory" / "references" / "memory-operations.md"
)
SESSION_MEMORY_FILE_CONTRACTS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "session-memory"
    / "references"
    / "memory-file-contracts.md"
)
SESSION_MEMORY_CONTEXT_BUDGET_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "session-memory"
    / "references"
    / "context-budget-and-checkpointing.md"
)
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
    "plan-design-handoff.json",
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
    router_artifact_policy_reference = read(ROUTER_ARTIFACT_POLICY_REFERENCE)
    router_build_reference = read(ROUTER_BUILD_REFERENCE)
    router_debug_reference = read(ROUTER_DEBUG_REFERENCE)
    router_review_reference = read(ROUTER_REVIEW_REFERENCE)
    router_plan_reference = read(ROUTER_PLAN_REFERENCE)
    router_remediation_reference = read(ROUTER_REMEDIATION_REFERENCE)
    router_surface = "\n\n".join(
        [
            router,
            router_artifact_policy_reference,
            router_build_reference,
            router_debug_reference,
            router_review_reference,
            router_plan_reference,
            router_remediation_reference,
        ]
    )
    task_completed_guard = read(TASK_COMPLETED_GUARD)
    readme = read(README)
    changelog = read(CHANGELOG)
    invariants = read(INVARIANTS)
    prompt_invariants = read(PROMPT_INVARIANTS)
    prompt_surface_inventory = read(PROMPT_SURFACE_INVENTORY)
    prompt_change_checklist = read(PROMPT_CHANGE_CHECKLIST)
    orchestration_bible = read(ORCHESTRATION_BIBLE)
    orchestration_logic = read(ORCHESTRATION_LOGIC)
    orchestration_safety = read(ORCHESTRATION_SAFETY)
    session_memory = read(SESSION_MEMORY_SKILL)
    planner_agent = read(PLANNER_AGENT)
    planning_patterns = read(PLANNING_PATTERNS_SKILL)
    brainstorming = read(BRAINSTORMING_SKILL)
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
        "cc10x_postcompact_context.py",
        "cc10x_subagent_stop_audit.py",
        "cc10x_precompact_state.py",
        "cc10x_stop_persist.py",
        "cc10x_stop_failure_log.py",
        "cc10x_instructions_loaded_audit.py",
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
    if not ORCHESTRATION_BIBLE.exists():
        errors.append("missing orchestration bible")
    if not ORCHESTRATION_LOGIC.exists():
        errors.append("missing orchestration logic analysis")
    if not ORCHESTRATION_SAFETY.exists():
        errors.append("missing orchestration safety doc")
    if not AGENT_CONTRACT_REGISTRY.exists():
        errors.append("missing agent contract registry")
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
    if not LIVE_HARNESS_RUNNER.exists():
        errors.append("missing live harness runner script")
    if not LIVE_MANIFEST_TEMPLATE.exists():
        errors.append("missing live harness template manifest")
    if not PLANNING_LIVE_REFERENCE.exists():
        errors.append("missing planning live verification reference")
    if not VERIFY_LIVE_REFERENCE.exists():
        errors.append("missing verification live testing reference")
    if not LIVE_MANIFEST_BOOTSTRAP.exists():
        errors.append("missing live harness bootstrap manifest")
    if not DEBUGGING_PLAYBOOKS_REFERENCE.exists():
        errors.append("missing debugging root-cause playbooks reference")
    if not DEBUGGING_HYGIENE_REFERENCE.exists():
        errors.append("missing debugging investigation hygiene reference")
    if not REVIEW_ORDER_REFERENCE.exists():
        errors.append("missing code review order/checkpoints reference")
    if not REVIEW_SECURITY_REFERENCE.exists():
        errors.append("missing code review security checklist reference")
    if not REVIEW_HEURISTICS_REFERENCE.exists():
        errors.append("missing code review heuristics reference")
    if not FRONTEND_STATE_REFERENCE.exists():
        errors.append("missing frontend UI state reference")
    if not FRONTEND_A11Y_REFERENCE.exists():
        errors.append("missing frontend accessibility/forms reference")
    if not FRONTEND_LAYOUT_REFERENCE.exists():
        errors.append("missing frontend performance/layout reference")
    if not FRONTEND_DESIGN_MD_REFERENCE.exists():
        errors.append("missing frontend DESIGN.md authoring reference")
    if not FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE.exists():
        errors.append("missing frontend DESIGN.md inspiration reference")
    if not TDD_PATTERNS_REFERENCE.exists():
        errors.append("missing TDD testing patterns reference")
    if not TDD_MOCKS_REFERENCE.exists():
        errors.append("missing TDD test-data-and-mocks reference")
    if not TDD_LIVE_PROOF_REFERENCE.exists():
        errors.append("missing TDD integration/live-proof reference")
    if not SESSION_MEMORY_MODEL_REFERENCE.exists():
        errors.append("missing session-memory model/ownership reference")
    if not SESSION_MEMORY_OPERATIONS_REFERENCE.exists():
        errors.append("missing session-memory operations reference")
    if not SESSION_MEMORY_FILE_CONTRACTS_REFERENCE.exists():
        errors.append("missing session-memory file-contract reference")
    if not SESSION_MEMORY_CONTEXT_BUDGET_REFERENCE.exists():
        errors.append("missing session-memory context-budget reference")

    for required in ("brightdata", "octocode"):
        if required not in router:
            errors.append(f"router no longer mentions MCP server '{required}'")
        if required not in readme:
            errors.append(
                f"README no longer documents optional MCP server '{required}'"
            )

    if ".claude/cc10x/v10/" not in readme:
        errors.append("README does not document the live v10 memory namespace")
    for stale in (
        "live in `.claude/cc10x/`",
        "MEMORY (.claude/cc10x/)",
        "WORKFLOW STATE (.claude/cc10x/workflows/)",
        ".claude/cc10x/\n├── activeContext.md",
    ):
        if stale in readme:
            errors.append(
                f"README still contains stale root-level memory text: {stale}"
            )

    required_router_inline = [
        "## 2a. Workflow Artifact And Hook Policy",
        "references/workflow-artifact-and-hook-policy.md",
        "references/build-workflow.md",
        "references/debug-workflow.md",
        "references/review-workflow.md",
        "references/plan-workflow.md",
        "references/remediation-and-research.md",
        "## 12. Chain Execution Loop",
        "## 13. Memory Finalization",
        "## 14. Hard Rules",
    ]
    for heading in required_router_inline:
        if heading not in router:
            errors.append(f"router missing required inline reference/text: {heading}")

    required_router_surface_text = [
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
    for heading in required_router_surface_text:
        if heading not in router_surface:
            errors.append(f"router surface missing required heading/text: {heading}")

    reference_expectations = {
        ROUTER_ARTIFACT_POLICY_REFERENCE: (
            "## 2a. Workflow Artifact And Hook Policy",
            "Artifact schema must include:",
            "Hook policy:",
        ),
        ROUTER_BUILD_REFERENCE: (
            "### BUILD preparation",
            "### BUILD task graph",
            "plan_trust_gate",
        ),
        ROUTER_DEBUG_REFERENCE: (
            "### DEBUG preparation",
            "### DEBUG task graph",
            "[DEBUG-RESET:",
        ),
        ROUTER_REVIEW_REFERENCE: (
            "### REVIEW preparation",
            "### REVIEW task graph",
            "CHANGES_REQUESTED",
        ),
        ROUTER_PLAN_REFERENCE: (
            "### PLAN preparation",
            "### PLAN task graph",
            "decision_rfc",
        ),
        ROUTER_REMEDIATION_REFERENCE: (
            "## 9. Remediation And Workflow Rules",
            "## 10. Research Orchestration",
            "## 11. Re-Review Loop",
        ),
    }
    for path, expected_phrases in reference_expectations.items():
        text = read(path)
        for phrase in expected_phrases:
            if phrase not in text:
                errors.append(f"{path.name} missing required reference text: {phrase}")

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
        if field not in router_surface:
            errors.append(
                f"router surface missing task metadata contract field {field}"
            )

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
    if "CC10X Orchestration Bible" not in orchestration_bible:
        errors.append("cc10x-orchestration-bible.md appears malformed")
    if "CC10x Orchestration Logic Analysis" not in orchestration_logic:
        errors.append("cc10x-orchestration-logic-analysis.md appears malformed")
    if "CC10x Orchestration Safety" not in orchestration_safety:
        errors.append("cc10x-orchestration-safety.md appears malformed")
    if "CC10X Agent Contract Registry" not in read(AGENT_CONTRACT_REGISTRY):
        errors.append("agent-contract-registry.md appears malformed")
    if "Verifier Latency Model" not in verifier_latency_model:
        errors.append("verifier-latency-model.md appears malformed")
    if "Latency Reduction Note" not in latency_reduction_note:
        errors.append("latency-reduction-note.md appears malformed")
    if "MEMORY_FINAL_EVENT" not in task_completed_guard:
        errors.append("task_completed_guard missing memory finalize event guard")
    for phrase in (
        'metadata.get("kind") != "memory"',
        "workflow_event_log_contains(workflow_id, MEMORY_FINAL_EVENT)",
        "missing-memory-finalized-event",
        "CC10X Memory Update:",
    ):
        if phrase not in task_completed_guard:
            errors.append(
                f"task_completed_guard missing memory finalize phrase '{phrase}'"
            )

    for required in (
        "memory-model-and-ownership.md",
        "memory-operations.md",
        "memory-file-contracts.md",
        "context-budget-and-checkpointing.md",
        "MEMORY_NOTES",
    ):
        if required not in session_memory:
            errors.append(
                f"session-memory skill missing required reference/text: {required}"
            )

    if ".claude/cc10x/v10/*" not in planner_agent:
        errors.append("planner agent no longer documents the live v10 memory namespace")

    if "### session-memory" not in prompt_surface_inventory:
        errors.append("prompt surface inventory missing session-memory entry")
    for required_surface in ("### planning-patterns", "### brainstorming"):
        if required_surface not in prompt_surface_inventory:
            errors.append(
                f"prompt surface inventory missing required entry {required_surface}"
            )
    if "PINV-012" not in prompt_invariants:
        errors.append("prompt invariants missing session-memory invariant")

    version_tag = f"v{version}"
    for name, body in (
        ("router invariants", invariants),
        ("prompt invariants", prompt_invariants),
        ("orchestration bible", orchestration_bible),
        ("orchestration logic analysis", orchestration_logic),
        ("agent contract registry", read(AGENT_CONTRACT_REGISTRY)),
    ):
        if version_tag not in body:
            errors.append(f"{name} is not synced to current version tag {version_tag}")

    for name, body in (
        ("orchestration bible", orchestration_bible),
        ("orchestration logic analysis", orchestration_logic),
        ("orchestration safety", orchestration_safety),
    ):
        if ".claude/cc10x/v10/workflows" not in body:
            errors.append(f"{name} does not reference the v10 workflow namespace")

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

    prompt_phrase_guards: dict[str, list[str]] = {
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
    for stem, guard_phrases in prompt_phrase_guards.items():
        path = (
            PLUGIN_ROOT / "agents" / f"{stem}.md"
            if (PLUGIN_ROOT / "agents" / f"{stem}.md").exists()
            else PLUGIN_ROOT / "skills" / stem / "SKILL.md"
        )
        text = read(path)
        for phrase in guard_phrases:
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
        "live-production-testing.md",
    ):
        if phrase not in verification_skill:
            errors.append(
                "verification-before-completion missing prompt safety phrase "
                f"'{phrase}'"
            )

    if "live-verification-strategy.md" not in planning_patterns:
        errors.append("planning-patterns missing live verification reference link")

    forbidden_direct_memory_writes = (
        'Edit(file_path=".claude/cc10x/v10/activeContext.md"',
        'Edit(file_path=".claude/cc10x/v10/progress.md"',
        'Edit(file_path=".claude/cc10x/v10/patterns.md"',
    )
    for forbidden in forbidden_direct_memory_writes:
        if forbidden in planning_patterns:
            errors.append(
                "planning-patterns still contains direct v10 memory writes instead of router-owned MEMORY_NOTES"
            )
        if forbidden in brainstorming:
            errors.append(
                "brainstorming still contains direct v10 memory writes instead of router-owned handoff"
            )

    for phrase in (
        "One direct save is required - the plan file. Memory indexing is router-owned.",
        "Emit Router-Owned Memory Intent",
        "MEMORY_NOTES",
    ):
        if phrase not in planning_patterns:
            errors.append(f"planning-patterns missing harmony phrase '{phrase}'")

    for phrase in (
        "router handoff are required",
        "### Brainstorming Handoff (MACHINE-READABLE)",
        "DESIGN_FILE:",
        "Router will carry the design reference forward and manage any research or planning transitions automatically.",
    ):
        if phrase not in brainstorming:
            errors.append(f"brainstorming missing harmony phrase '{phrase}'")

    for phrase in (
        "parse `### Brainstorming Handoff (MACHINE-READABLE)`",
        "persist it into the workflow artifact `design_file` field",
        "fall back to the pre-existing memory design reference",
    ):
        if phrase not in router_plan_reference:
            errors.append(f"plan-workflow missing design handoff phrase '{phrase}'")

    for phrase in (
        "### Inline brainstorming handoff",
        "persist it into workflow artifact `design_file`",
        "- Ensure `- Design: {design_file}` remains correct",
    ):
        if phrase not in router:
            errors.append(f"router missing design-handoff phrase '{phrase}'")

    if "Explore project first, then invoke the router." in readme:
        errors.append(
            "README still contains the stale explore-before-router instruction"
        )
    if "The plugin ships four Claude Code-native hooks:" in readme:
        errors.append("README still contains the stale four-hooks inventory")
    if "query-optimize," in planner_agent or " query-optimize " in planner_agent:
        errors.append("planner still contains stale MongoDB example 'query-optimize'")

    frontend_skill = read(PLUGIN_ROOT / "skills" / "frontend-patterns" / "SKILL.md")
    frontend_design_md = read(FRONTEND_DESIGN_MD_REFERENCE)
    frontend_design_md_inspiration = read(FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE)
    for phrase in (
        "DESIGN.md authoring from screenshots",
        "references/design-md-authoring.md",
        "references/design-md-inspiration-index.md",
        "Treat inspiration as input to the project's own design contract",
    ):
        if phrase not in frontend_skill:
            errors.append(
                f"frontend-patterns missing DESIGN.md trigger/reference phrase '{phrase}'"
            )
    for phrase in (
        "`DESIGN.md` is a project-local visual contract.",
        "Do not copy a screenshot or a brand.",
        "## Stable Structure",
        "## Screenshot-Specific Rules",
        "Use inspiration references to choose a direction, not to clone",
    ):
        if phrase not in frontend_design_md:
            errors.append(
                f"design-md-authoring reference missing required phrase '{phrase}'"
            )
    for phrase in (
        "inspect only the requested company/style entry.",
        "Choose at most one primary reference and one secondary accent.",
        "Never paste a company `DESIGN.md` into project memory.",
    ):
        if phrase not in frontend_design_md_inspiration:
            errors.append(
                f"design-md-inspiration-index reference missing required phrase '{phrase}'"
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
