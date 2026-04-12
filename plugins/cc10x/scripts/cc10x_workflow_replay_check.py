#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
PLANNER_PROMPT = PLUGIN_ROOT / "agents" / "planner.md"
PLAN_REVIEW_GATE = PLUGIN_ROOT / "skills" / "plan-review-gate" / "SKILL.md"

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

REQUIRED_ARTIFACT_KEYS = (
    "workflow_uuid",
    "workflow_id",
    "workflow_type",
    "state_root",
    "plan_mode",
    "verification_rigor",
    "proof_status",
    "traceability",
    "phase_cursor",
    "task_ids",
    "results",
    "intent",
    "evidence",
    "quality",
    "status_history",
    "remediation_history",
)

REQUIRED_SCENARIO_KEYS = (
    "name",
    "given",
    "when",
    "then",
    "command",
    "expected",
    "actual",
    "exit_code",
    "status",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def load_fixture(name: str) -> dict[str, Any]:
    path = FIXTURES_DIR / name
    if not path.exists():
        fail(f"missing fixture: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_artifact_shape(fixture: dict[str, Any]) -> None:
    artifact = fixture["starting_artifact"]
    missing = [key for key in REQUIRED_ARTIFACT_KEYS if key not in artifact]
    require(not missing, f"{fixture['id']}: artifact missing keys {missing}")
    require(
        artifact["workflow_uuid"] == artifact["workflow_id"],
        f"{fixture['id']}: workflow_uuid and workflow_id must match in v10 fixtures",
    )
    require(
        artifact["state_root"] == ".claude/cc10x/v10",
        f"{fixture['id']}: state_root must point to v10 namespace",
    )


def validate_scenarios(
    fixture_id: str, scenarios: list[dict[str, Any]], *, require_pass: bool = False
) -> None:
    require(bool(scenarios), f"{fixture_id}: expected at least one scenario")
    for idx, scenario in enumerate(scenarios, start=1):
        missing = [key for key in REQUIRED_SCENARIO_KEYS if key not in scenario]
        require(not missing, f"{fixture_id}: scenario {idx} missing keys {missing}")
        for key in REQUIRED_SCENARIO_KEYS:
            value = scenario[key]
            require(
                value not in ("", None), f"{fixture_id}: scenario {idx} empty {key}"
            )
    if require_pass:
        require(
            any(s["status"] == "PASS" and s["exit_code"] == 0 for s in scenarios),
            f"{fixture_id}: expected at least one passing scenario",
        )


def validate_verifier_contract(
    fixture_id: str, contract: dict[str, Any], *, allow_invalid: bool = False
) -> None:
    total = contract["SCENARIOS_TOTAL"]
    passed = contract["SCENARIOS_PASSED"]
    failed = contract["SCENARIOS_FAILED"]
    scenarios = contract["SCENARIO_ROWS"]
    if allow_invalid:
        require(
            bool(scenarios), f"{fixture_id}: expected at least one verifier scenario"
        )
    else:
        validate_scenarios(fixture_id, scenarios)
    evidence_rows = contract["EVIDENCE"]["scenarios"]
    actual_passed = sum(
        1 for row in scenarios if row["status"] == "PASS" and row["exit_code"] == 0
    )
    mismatch = (
        total != passed + failed or passed != actual_passed or total != len(scenarios)
    )
    has_blank_expected_actual = any(
        (not row["expected"]) or (not row["actual"]) for row in scenarios
    )
    if allow_invalid:
        require(
            mismatch or has_blank_expected_actual,
            f"{fixture_id}: expected invalid verifier evidence mismatch",
        )
    else:
        require(
            not mismatch, f"{fixture_id}: verifier scenario totals do not reconcile"
        )
        require(
            not has_blank_expected_actual,
            f"{fixture_id}: verifier scenario rows missing expected/actual",
        )
        require(
            len(evidence_rows) == total,
            f"{fixture_id}: verifier evidence rows do not match total scenarios",
        )


def validate_builder_contract(fixture_id: str, contract: dict[str, Any]) -> None:
    require(contract["STATUS"] == "PASS", f"{fixture_id}: builder must pass")
    require(
        contract["PHASE_STATUS"] == "completed", f"{fixture_id}: phase must complete"
    )
    require(contract["PHASE_EXIT_READY"] is True, f"{fixture_id}: phase exit must pass")
    require(
        contract["CHECKPOINT_TYPE"] == "none",
        f"{fixture_id}: checkpoint type must be none",
    )
    require(
        contract["PROOF_STATUS"] == "passed", f"{fixture_id}: proof status must pass"
    )
    require(contract["TDD_RED_EXIT"] == 1, f"{fixture_id}: missing RED evidence")
    require(contract["TDD_GREEN_EXIT"] == 0, f"{fixture_id}: missing GREEN evidence")
    require(
        not contract.get("BLOCKED_ITEMS"), f"{fixture_id}: blocked items must be empty"
    )
    validate_scenarios(fixture_id, contract["SCENARIOS"], require_pass=True)


def validate_investigator_contract(
    fixture_id: str, contract: dict[str, Any], *, allow_research: bool = False
) -> None:
    if allow_research:
        require(
            contract["NEEDS_EXTERNAL_RESEARCH"] is True,
            f"{fixture_id}: expected research request",
        )
        require(contract["RESEARCH_REASON"], f"{fixture_id}: missing research reason")
        return
    require(contract["STATUS"] == "FIXED", f"{fixture_id}: investigator must be FIXED")
    require(contract["TDD_RED_EXIT"] == 1, f"{fixture_id}: missing regression RED")
    require(contract["TDD_GREEN_EXIT"] == 0, f"{fixture_id}: missing regression GREEN")
    require(
        contract["VARIANTS_COVERED"] >= 1,
        f"{fixture_id}: variant coverage must be at least 1",
    )
    require(
        bool(contract.get("BLAST_RADIUS_SCAN")),
        f"{fixture_id}: blast radius scan is required",
    )
    scenarios = contract["SCENARIOS"]
    validate_scenarios(fixture_id, scenarios, require_pass=True)
    scenario_names = [scenario["name"] for scenario in scenarios]
    require(
        any(name.startswith("Regression:") for name in scenario_names),
        f"{fixture_id}: expected a Regression: scenario",
    )
    require(
        any(name.startswith("Variant:") for name in scenario_names),
        f"{fixture_id}: expected a Variant: scenario",
    )


def validate_fixture_common(fixture: dict[str, Any]) -> None:
    for key in (
        "id",
        "workflow_type",
        "starting_artifact",
        "relevant_tasks",
        "agent_outputs",
        "expected",
    ):
        require(key in fixture, f"{fixture.get('id', '<unknown>')}: missing {key}")
    validate_artifact_shape(fixture)


def validate_latency_telemetry(
    fixture_id: str, telemetry: dict[str, Any], *, require_verifier_detail: bool = False
) -> None:
    require(
        "agent_wall_clock_seconds" in telemetry,
        f"{fixture_id}: missing agent_wall_clock_seconds",
    )
    require("loop_counts" in telemetry, f"{fixture_id}: missing loop_counts")
    require("verifier" in telemetry, f"{fixture_id}: missing verifier telemetry")
    agent_wall = telemetry["agent_wall_clock_seconds"]
    for key in ("builder", "reviewer", "hunter", "verifier"):
        require(key in agent_wall, f"{fixture_id}: missing agent timing for {key}")
    loop_counts = telemetry["loop_counts"]
    for key in ("re_review", "re_hunt", "re_verify"):
        require(key in loop_counts, f"{fixture_id}: missing loop counter {key}")
    verifier = telemetry["verifier"]
    for key in ("phase_exit_proof_runs", "extended_audit_runs", "workload_seconds"):
        require(key in verifier, f"{fixture_id}: missing verifier telemetry {key}")
    workload = verifier["workload_seconds"]
    for key in ("tests", "build", "scan", "reconcile", "reasoning"):
        require(key in workload, f"{fixture_id}: missing verifier workload {key}")
    if require_verifier_detail:
        require(
            verifier["phase_exit_proof_runs"] >= 1,
            f"{fixture_id}: phase_exit_proof_runs must be recorded",
        )


def validate_plan_dag(
    fixture_id: str,
    relevant_tasks: dict[str, Any],
    *,
    planner_status: str,
    pass1_status: str,
    replan_status: str,
    pass2_status: str,
    memory_status: str,
) -> None:
    expected_keys = (
        "planner_create",
        "planning_review_pass1",
        "planner_replan",
        "planning_review_pass2",
        "memory_finalize",
    )
    missing = [key for key in expected_keys if key not in relevant_tasks]
    require(not missing, f"{fixture_id}: missing PLAN DAG tasks {missing}")

    planner = relevant_tasks["planner_create"]
    pass1 = relevant_tasks["planning_review_pass1"]
    replan = relevant_tasks["planner_replan"]
    pass2 = relevant_tasks["planning_review_pass2"]
    memory = relevant_tasks["memory_finalize"]

    require(
        planner["phase"] == "plan-create",
        f"{fixture_id}: planner_create must use phase plan-create",
    )
    require(
        pass1["phase"] == "plan-review-gap-1",
        f"{fixture_id}: planning_review_pass1 must use phase plan-review-gap-1",
    )
    require(
        replan["phase"] == "re-plan",
        f"{fixture_id}: planner_replan must use phase re-plan",
    )
    require(
        pass2["phase"] == "plan-review-gap-2",
        f"{fixture_id}: planning_review_pass2 must use phase plan-review-gap-2",
    )
    require(
        memory["phase"] == "memory-finalize",
        f"{fixture_id}: memory_finalize must use phase memory-finalize",
    )

    require(
        planner["status"] == planner_status,
        f"{fixture_id}: planner_create wrong status",
    )
    require(
        pass1["status"] == pass1_status,
        f"{fixture_id}: planning_review_pass1 wrong status",
    )
    require(
        replan["status"] == replan_status,
        f"{fixture_id}: planner_replan wrong status",
    )
    require(
        pass2["status"] == pass2_status,
        f"{fixture_id}: planning_review_pass2 wrong status",
    )
    require(
        memory["status"] == memory_status,
        f"{fixture_id}: memory_finalize wrong status",
    )

    require(
        pass1["blockedBy"] == ["planner_create"],
        f"{fixture_id}: pass1 must be blocked by planner_create",
    )
    require(
        replan["blockedBy"] == ["planning_review_pass1"],
        f"{fixture_id}: planner_replan must be blocked by pass1",
    )
    require(
        pass2["blockedBy"] == ["planner_replan"],
        f"{fixture_id}: pass2 must be blocked by planner_replan",
    )
    require(
        memory["blockedBy"]
        == [
            "planner_create",
            "planning_review_pass1",
            "planner_replan",
            "planning_review_pass2",
        ],
        f"{fixture_id}: memory_finalize must be blocked by the full PLAN chain",
    )


def check_plan_direct(fixture: dict[str, Any]) -> None:
    expected = fixture["expected"]
    require(
        expected["next_action"] == "run_plan_review_pass1",
        "plan-direct: wrong next action",
    )
    require(
        fixture["starting_artifact"]["workflow_type"] == "PLAN",
        "plan-direct: wrong workflow type",
    )
    require(expected["pending_gate"] is None, "plan-direct: should not pause")
    require(
        fixture["starting_artifact"]["plan_mode"] == "direct",
        "plan-direct: artifact should record direct mode",
    )
    require(
        expected["artifact_delta"]["planning_review_status"] == "pending_review",
        "plan-direct: fresh review should be pending",
    )
    require(
        expected["artifact_delta"]["planning_review_runs"] == 0,
        "plan-direct: review count should not increment before reviewer output",
    )
    validate_plan_dag(
        "plan-direct",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="pending",
        replan_status="pending",
        pass2_status="pending",
        memory_status="pending",
    )


def check_plan_decision_rfc(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "DECISION_RFC_CREATED",
        "plan-decision-rfc: planner should create decision RFC",
    )
    require(
        planner["PLAN_MODE"] == "decision_rfc",
        "plan-decision-rfc: plan mode must be decision_rfc",
    )
    require(
        planner["VERIFICATION_RIGOR"] == "critical_path",
        "plan-decision-rfc: verification rigor must be critical_path",
    )
    require(
        len(planner["ALTERNATIVES"]) >= 2,
        "plan-decision-rfc: expected at least two alternatives",
    )
    require(
        bool(planner["DRAWBACKS"]),
        "plan-decision-rfc: expected explicit drawbacks",
    )
    require(
        bool(planner["PROVABLE_PROPERTIES"]),
        "plan-decision-rfc: expected provable properties",
    )
    validate_scenarios("plan-decision-rfc", planner["SCENARIOS"], require_pass=False)
    require(
        fixture["expected"]["next_action"] == "run_plan_review_pass1",
        "plan-decision-rfc: should queue fresh review before final handoff",
    )
    require(
        fixture["expected"]["artifact_delta"]["planning_review_status"]
        == "pending_review",
        "plan-decision-rfc: fresh review should be pending",
    )
    require(
        fixture["expected"]["artifact_delta"]["planning_review_runs"] == 0,
        "plan-decision-rfc: review count should not increment before reviewer output",
    )
    validate_plan_dag(
        "plan-decision-rfc",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="pending",
        replan_status="pending",
        pass2_status="pending",
        memory_status="pending",
    )


def check_plan_full(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "PLAN_CREATED", "plan-full: planner should create plan"
    )
    require(planner["PLAN_FILE"], "plan-full: missing plan file")
    require(
        planner["PLAN_MODE"] == "execution_plan",
        "plan-full: planner should use execution_plan mode",
    )
    require(
        planner["VERIFICATION_RIGOR"] == "standard",
        "plan-full: planner should use standard rigor",
    )
    require(planner["GATE_PASSED"] is True, "plan-full: gate must pass")
    require(planner["OPEN_DECISIONS"] == [], "plan-full: open decisions must be empty")
    require(
        "DIFFERENCES_FROM_AGREEMENT" in planner,
        "plan-full: differences from agreement must be explicit",
    )
    validate_scenarios("plan-full", planner["SCENARIOS"], require_pass=False)
    require(
        fixture["expected"]["next_action"] == "run_plan_review_pass1",
        "plan-full: should queue fresh review before final handoff",
    )
    require(
        fixture["expected"]["artifact_delta"]["plan_file"] == planner["PLAN_FILE"],
        "plan-full: expected plan_file delta mismatch",
    )
    require(
        fixture["expected"]["artifact_delta"]["planning_review_status"]
        == "pending_review",
        "plan-full: fresh review should be pending",
    )
    require(
        fixture["expected"]["artifact_delta"]["planning_review_runs"] == 0,
        "plan-full: review count should not increment before reviewer output",
    )
    validate_plan_dag(
        "plan-full",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="pending",
        replan_status="pending",
        pass2_status="pending",
        memory_status="pending",
    )


def check_plan_clarification(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "NEEDS_CLARIFICATION",
        "plan-clarification: wrong planner status",
    )
    require(planner["BLOCKING"] is True, "plan-clarification: must block")
    require(
        fixture["expected"]["next_action"] == "ask_user",
        "plan-clarification: wrong next action",
    )
    require(
        fixture["expected"]["pending_gate"] == "clarification",
        "plan-clarification: wrong pending gate",
    )
    validate_plan_dag(
        "plan-clarification",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="deleted",
        replan_status="deleted",
        pass2_status="deleted",
        memory_status="pending",
    )


def check_plan_repo_alignment(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "PLAN_CREATED",
        "plan-repo-alignment: planner should create plan",
    )
    require(
        planner["PLAN_MODE"] == "execution_plan",
        "plan-repo-alignment: plan mode must be execution_plan",
    )
    require(
        planner["GATE_PASSED"] is True,
        "plan-repo-alignment: gate must pass",
    )
    require(
        bool(planner["ASSUMPTIONS"]),
        "plan-repo-alignment: assumptions must be explicit",
    )
    planner_text = load_text(PLANNER_PROMPT)
    gate_text = load_text(PLAN_REVIEW_GATE)
    for marker in fixture["expected"]["planner_markers"]:
        require(
            marker in planner_text,
            f"plan-repo-alignment: planner marker missing '{marker}'",
        )
    for marker in fixture["expected"]["gate_markers"]:
        require(
            marker in gate_text,
            f"plan-repo-alignment: gate marker missing '{marker}'",
        )


def check_plan_code_contradiction(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "NEEDS_CLARIFICATION",
        "plan-code-contradiction: planner must block on contradiction",
    )
    require(
        planner["BLOCKING"] is True,
        "plan-code-contradiction: contradiction must block",
    )
    require(
        bool(planner["REMEDIATION_REASON"]),
        "plan-code-contradiction: missing remediation reason",
    )
    require(
        fixture["expected"]["next_action"] == "ask_user",
        "plan-code-contradiction: wrong next action",
    )
    require(
        fixture["expected"]["pending_gate"] == "clarification",
        "plan-code-contradiction: wrong pending gate",
    )
    planner_text = load_text(PLANNER_PROMPT)
    gate_text = load_text(PLAN_REVIEW_GATE)
    for marker in fixture["expected"]["planner_markers"]:
        require(
            marker in planner_text,
            f"plan-code-contradiction: planner marker missing '{marker}'",
        )
    for marker in fixture["expected"]["gate_markers"]:
        require(
            marker in gate_text,
            f"plan-code-contradiction: gate marker missing '{marker}'",
        )


def check_plan_fresh_review_pass(fixture: dict[str, Any]) -> None:
    review = fixture["agent_outputs"]["plan_gap_review_contract"]
    require(
        review["STATUS"] == "PASS",
        "plan-fresh-review-pass: reviewer should pass",
    )
    require(
        review["BLOCKING_FINDINGS_COUNT"] == 0,
        "plan-fresh-review-pass: blocking findings must be zero",
    )
    require(
        review["REPLAN_NEEDED"] is False,
        "plan-fresh-review-pass: pass should not require replan",
    )
    require(
        fixture["expected"]["next_action"] == "memory_finalize",
        "plan-fresh-review-pass: wrong next action",
    )
    artifact_delta = fixture["expected"]["artifact_delta"]
    require(
        artifact_delta["planning_review_status"] == "passed",
        "plan-fresh-review-pass: wrong planning review status",
    )
    require(
        artifact_delta["planning_review_runs"] == 1,
        "plan-fresh-review-pass: wrong review run count",
    )
    validate_plan_dag(
        "plan-fresh-review-pass",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="completed",
        replan_status="deleted",
        pass2_status="deleted",
        memory_status="pending",
    )


def check_plan_fresh_review_findings(fixture: dict[str, Any]) -> None:
    review = fixture["agent_outputs"]["plan_gap_review_contract"]
    require(
        review["STATUS"] == "FINDINGS",
        "plan-fresh-review-findings: reviewer should return findings",
    )
    require(
        review["BLOCKING_FINDINGS_COUNT"] >= 1,
        "plan-fresh-review-findings: expected blocking findings",
    )
    require(
        review["REPLAN_NEEDED"] is True,
        "plan-fresh-review-findings: findings should request replan",
    )
    require(
        fixture["expected"]["next_action"] == "run_planner_replan",
        "plan-fresh-review-findings: wrong next action",
    )
    artifact_delta = fixture["expected"]["artifact_delta"]
    require(
        artifact_delta["planning_review_status"] == "findings_received",
        "plan-fresh-review-findings: wrong planning review status",
    )
    require(
        artifact_delta["planning_review_runs"] == 1,
        "plan-fresh-review-findings: wrong review run count",
    )
    validate_plan_dag(
        "plan-fresh-review-findings",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="completed",
        replan_status="pending",
        pass2_status="pending",
        memory_status="pending",
    )


def check_plan_fresh_review_exhausted(fixture: dict[str, Any]) -> None:
    review = fixture["agent_outputs"]["plan_gap_review_contract"]
    require(
        review["STATUS"] == "FINDINGS",
        "plan-fresh-review-exhausted: reviewer should still find issues",
    )
    require(
        review["BLOCKING_FINDINGS_COUNT"] >= 1,
        "plan-fresh-review-exhausted: expected blocking findings",
    )
    require(
        fixture["expected"]["next_action"] == "ask_user",
        "plan-fresh-review-exhausted: wrong next action",
    )
    require(
        fixture["expected"]["pending_gate"] == "clarification",
        "plan-fresh-review-exhausted: wrong pending gate",
    )
    artifact_delta = fixture["expected"]["artifact_delta"]
    require(
        artifact_delta["planning_review_status"] == "needs_clarification",
        "plan-fresh-review-exhausted: wrong planning review status",
    )
    require(
        artifact_delta["planning_review_runs"] == 2,
        "plan-fresh-review-exhausted: wrong review run count",
    )
    validate_plan_dag(
        "plan-fresh-review-exhausted",
        fixture["relevant_tasks"],
        planner_status="completed",
        pass1_status="completed",
        replan_status="completed",
        pass2_status="completed",
        memory_status="pending",
    )


def check_plan_design_handoff(fixture: dict[str, Any]) -> None:
    handoff = fixture["agent_outputs"]["brainstorming_handoff"]
    require(
        handoff["DESIGN_FILE"] == fixture["expected"]["artifact_delta"]["design_file"],
        "plan-design-handoff: router must persist the brainstorming design_file into the artifact",
    )
    require(
        bool(handoff["DESIGN_SUMMARY"]),
        "plan-design-handoff: brainstorming handoff must include a design summary",
    )
    require(
        fixture["expected"]["planner_inputs"]["design_file"] == handoff["DESIGN_FILE"],
        "plan-design-handoff: planner must receive the handoff design file",
    )
    planner_text = load_text(PLANNER_PROMPT)
    gate_text = load_text(PLAN_REVIEW_GATE)
    for marker in fixture["expected"]["planner_markers"]:
        require(
            marker in planner_text,
            f"plan-design-handoff: planner marker missing '{marker}'",
        )
    for marker in fixture["expected"]["gate_markers"]:
        require(
            marker in gate_text or marker == "memory_router_owned",
            f"plan-design-handoff: missing required marker '{marker}'",
        )
    require(
        fixture["expected"]["next_action"] == "run_planner_with_design_file",
        "plan-design-handoff: wrong next action",
    )
    memory_sync = fixture["expected"]["artifact_delta"]["memory_sync"]
    require(
        memory_sync["design_reference_persisted"] is True,
        "plan-design-handoff: design reference must be persisted during memory finalization",
    )
    require(
        memory_sync["plan_recent_change_persisted"] is True,
        "plan-design-handoff: plan save event must be persisted during memory finalization",
    )
    require(
        memory_sync["next_step_persisted"] is True,
        "plan-design-handoff: next step must be persisted during memory finalization",
    )


def check_build_happy_path(fixture: dict[str, Any]) -> None:
    validate_builder_contract(
        "build-happy-path", fixture["agent_outputs"]["builder_contract"]
    )
    verifier = fixture["agent_outputs"]["verifier_contract"]
    validate_verifier_contract("build-happy-path", verifier)
    require(
        fixture["expected"]["next_action"] == "memory_finalize",
        "build-happy-path: wrong next action",
    )
    require(
        fixture["expected"]["artifact_delta"]["quality"]["convergence_state"]
        == "stable",
        "build-happy-path: wrong convergence state",
    )
    require(
        fixture["expected"]["artifact_delta"]["phase_cursor"] == "phase-2",
        "build-happy-path: phase cursor should advance after successful phase exit",
    )


def check_build_checkpoint_decision(fixture: dict[str, Any]) -> None:
    builder = fixture["agent_outputs"]["builder_contract"]
    require(
        builder["CHECKPOINT_TYPE"] == "decision",
        "build-checkpoint-decision: expected decision checkpoint",
    )
    require(
        builder["PROOF_STATUS"] == "human_needed",
        "build-checkpoint-decision: proof should require human decision",
    )
    require(
        builder["STATUS"] == "FAIL",
        "build-checkpoint-decision: builder must fail closed",
    )
    require(
        fixture["expected"]["pending_gate"] == "checkpoint_decision",
        "build-checkpoint-decision: pending gate should be checkpoint_decision",
    )


def check_build_phase_blocked(fixture: dict[str, Any]) -> None:
    builder = fixture["agent_outputs"]["builder_contract"]
    require(
        builder["STATUS"] == "FAIL", "build-phase-blocked: builder must fail closed"
    )
    require(
        builder["PHASE_STATUS"] == "blocked", "build-phase-blocked: phase must block"
    )
    require(
        fixture["expected"]["next_action"] == "stop_for_blocked_phase",
        "build-phase-blocked: wrong next action",
    )
    require(
        fixture["expected"]["artifact_delta"]["pending_gate"] == "phase_blocked",
        "build-phase-blocked: pending gate must record blocked phase",
    )


def check_build_scope_gate(fixture: dict[str, Any]) -> None:
    findings = fixture["agent_outputs"]["parallel_findings"]
    require(
        findings["critical_issues"] > 0, "build-scope-gate: expected critical issues"
    )
    require(findings["high_issues"] > 0, "build-scope-gate: expected high issues")
    require(
        fixture["expected"]["next_action"] == "pause_for_scope_decision",
        "build-scope-gate: wrong next action",
    )
    require(
        fixture["expected"]["pending_gate"] == "scope_decision",
        "build-scope-gate: wrong pending gate",
    )


def check_build_remediation_loop(fixture: dict[str, Any]) -> None:
    remfix = fixture["relevant_tasks"]["completed_remfix"]
    require(remfix["kind"] == "remfix", "build-remediation-loop: wrong task kind")
    require(remfix["scope"] == "ALL_ISSUES", "build-remediation-loop: wrong scope")
    follow_up = fixture["expected"]["follow_up_tasks"]
    require(
        follow_up == ["re-review", "re-hunt", "re-verify"],
        "build-remediation-loop: wrong follow-up tasks",
    )


def check_debug_fixed(fixture: dict[str, Any]) -> None:
    validate_investigator_contract(
        "debug-fixed", fixture["agent_outputs"]["investigator_contract"]
    )
    require(
        fixture["expected"]["next_action"] == "debug_review",
        "debug-fixed: wrong next action",
    )


def check_debug_research(fixture: dict[str, Any]) -> None:
    validate_investigator_contract(
        "debug-research",
        fixture["agent_outputs"]["investigator_contract"],
        allow_research=True,
    )
    research = fixture["agent_outputs"]["research_results"]
    require(
        research["overall_quality"] in {"low", "medium"},
        "debug-research: research quality must be degraded or partial",
    )
    require(
        fixture["expected"]["next_action"] == "reinvoke_investigator",
        "debug-research: wrong next action",
    )


def check_review_advisory(fixture: dict[str, Any]) -> None:
    review = fixture["agent_outputs"]["reviewer_contract"]
    require(
        review["heading"] == "## Review: Changes Requested",
        "review-advisory: wrong review heading",
    )
    require(
        fixture["expected"]["code_mutation"] is False,
        "review-advisory: review must stay advisory",
    )
    require(
        fixture["expected"]["next_action"] == "offer_build_transition",
        "review-advisory: wrong next action",
    )


def check_skill_precedence(fixture: dict[str, Any]) -> None:
    expected = fixture["expected"]
    require(
        expected["next_action"] == "respect_user_standard",
        "skill-precedence: wrong next action",
    )
    require(
        expected["winner"] == "project_claude_md",
        "skill-precedence: project standards must win",
    )


def check_workflow_identity_v10(fixture: dict[str, Any]) -> None:
    artifact = fixture["starting_artifact"]
    expected = fixture["expected"]
    require(
        artifact["workflow_uuid"].startswith("wf-20260312T"),
        "workflow-identity-v10: expected time-ordered workflow uuid",
    )
    require(
        expected["collides_with_previous_session"] is False,
        "workflow-identity-v10: ids must not collide across sessions",
    )


def check_memory_sync_blocking(fixture: dict[str, Any]) -> None:
    expected = fixture["expected"]
    require(
        expected["next_action"] == "stop_after_memory_sync",
        "memory-sync-blocking: wrong next action",
    )
    require(
        expected["artifact_delta"]["memory_sync"]["blocking_exit_persisted"] is True,
        "memory-sync-blocking: blocking exit must persist memory sync",
    )


def check_verify_fail_closed(fixture: dict[str, Any]) -> None:
    validate_verifier_contract(
        "verify-fail-closed",
        fixture["agent_outputs"]["verifier_contract"],
        allow_invalid=True,
    )
    require(
        fixture["expected"]["next_action"] == "stop_invalid_output",
        "verify-fail-closed: wrong next action",
    )
    require(
        fixture["expected"]["artifact_delta"]["quality"]["convergence_state"]
        == "needs_iteration",
        "verify-fail-closed: wrong convergence state",
    )


def check_latency_telemetry(fixture: dict[str, Any]) -> None:
    telemetry = fixture["starting_artifact"]["telemetry"]
    validate_latency_telemetry(
        "latency-telemetry", telemetry, require_verifier_detail=True
    )
    expected = fixture["expected"]["artifact_delta"]["telemetry"]
    require(
        expected["loop_counts"]["re_verify"] == 1,
        "latency-telemetry: expected one re-verify loop",
    )
    require(
        expected["verifier"]["workload_seconds"]["tests"] == 600,
        "latency-telemetry: expected tests workload seconds",
    )


CHECKS = {
    "plan-direct.json": check_plan_direct,
    "plan-decision-rfc.json": check_plan_decision_rfc,
    "plan-full.json": check_plan_full,
    "plan-clarification.json": check_plan_clarification,
    "plan-repo-alignment.json": check_plan_repo_alignment,
    "plan-code-contradiction.json": check_plan_code_contradiction,
    "plan-fresh-review-pass.json": check_plan_fresh_review_pass,
    "plan-fresh-review-findings.json": check_plan_fresh_review_findings,
    "plan-fresh-review-exhausted.json": check_plan_fresh_review_exhausted,
    "plan-design-handoff.json": check_plan_design_handoff,
    "build-happy-path.json": check_build_happy_path,
    "build-checkpoint-decision.json": check_build_checkpoint_decision,
    "build-phase-blocked.json": check_build_phase_blocked,
    "build-scope-gate.json": check_build_scope_gate,
    "build-remediation-loop.json": check_build_remediation_loop,
    "debug-fixed.json": check_debug_fixed,
    "debug-research.json": check_debug_research,
    "skill-precedence.json": check_skill_precedence,
    "workflow-identity-v10.json": check_workflow_identity_v10,
    "memory-sync-blocking.json": check_memory_sync_blocking,
    "review-advisory.json": check_review_advisory,
    "verify-fail-closed.json": check_verify_fail_closed,
    "latency-telemetry.json": check_latency_telemetry,
}


def main() -> int:
    if not FIXTURES_DIR.exists():
        print("FAIL: fixtures directory missing", file=sys.stderr)
        return 1

    errors: list[str] = []
    for name in REQUIRED_FIXTURES:
        try:
            fixture = load_fixture(name)
            validate_fixture_common(fixture)
            CHECKS[name](fixture)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("cc10x_workflow_replay_check: OK")
    print(f"fixtures={len(REQUIRED_FIXTURES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
