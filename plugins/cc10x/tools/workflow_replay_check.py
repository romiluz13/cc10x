#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


if os.environ.get("CC10X_REPO_ROOT") == "":
    raise SystemExit("CC10X_REPO_ROOT is set but empty: unset it or point it at a cc10x repo")
ROOT = Path(os.environ.get("CC10X_REPO_ROOT") or Path(__file__).resolve().parents[3])
if not (ROOT / "plugins" / "cc10x").is_dir():
    raise SystemExit(f"CC10X_REPO_ROOT is not a cc10x repo (no plugins/cc10x): {ROOT}")
PLUGIN_ROOT = ROOT / "plugins" / "cc10x"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
PLANNER_PROMPT = PLUGIN_ROOT / "agents" / "planner.md"
PLAN_REVIEW_GATE = PLUGIN_ROOT / "skills" / "plan-review-gate" / "SKILL.md"

from fixture_registry import REQUIRED_FIXTURES, check_registry_complete

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

CONVERGENCE_STATES = ("pending", "needs_iteration", "converged", "N/A")

MEMORY_TASK_WORKFLOW_TYPES = ("BUILD", "DEBUG", "REVIEW", "PLAN", "QA", "TRIAGE", "CODEBASE-HEALTH")

WORKFLOW_TYPES = ("BUILD", "DEBUG", "PLAN", "REVIEW", "QA", "ORIENT", "TRIAGE", "CODEBASE-HEALTH", "pending")

QA_ROUTE_BLOCKERS = {
    "qa_research": [],
    "qa_plan": ["qa_research"],
    "qa_plan_review": ["qa_plan"],
    "qa_preflight": ["qa_plan_review"],
    "qa_build": ["qa_preflight"],
    "qa_review": ["qa_build"],
    "qa_hunt": ["qa_build"],
    "qa_execute": ["qa_review", "qa_hunt"],
    "memory_finalize": ["qa_execute"],
}
QA_ROUTE_PHASES = (
    "qa-research",
    "qa-plan",
    "qa-plan-review",
    "qa-preflight",
    "qa-build",
    "qa-review",
    "qa-hunt",
    "qa-execute",
    "memory-finalize",
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


def strict_bool(value: Any, expected: bool) -> bool:
    """Strict boolean check: value must be a real bool equal to expected."""
    return isinstance(value, bool) and value == expected


def load_fixture(name: str) -> dict[str, Any]:
    path = FIXTURES_DIR / name
    if not path.exists():
        fail(f"missing fixture: {name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"unreadable fixture {name}: {exc}")
        raise  # unreachable; fail() always raises


def load_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_artifact_keys(label: str, artifact: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_ARTIFACT_KEYS if key not in artifact]
    require(not missing, f"{label}: artifact missing keys {missing}")
    require(
        artifact["workflow_uuid"] == artifact["workflow_id"],
        f"{label}: workflow_uuid and workflow_id must match in v10 fixtures",
    )
    require(
        artifact["state_root"] == ".cc10x",
        f"{label}: state_root must point to the .cc10x namespace",
    )


def validate_artifact_shape(fixture: dict[str, Any]) -> None:
    validate_artifact_keys(fixture["id"], fixture["starting_artifact"])


def count_memory_finalized(label: str, artifact: dict[str, Any]) -> int:
    history = artifact["status_history"]
    require(
        isinstance(history, list)
        and all(isinstance(e, dict) and "event" in e for e in history),
        f"{label}: status_history must be a list of objects with an event",
    )
    return sum(1 for e in history if e["event"] == "memory_finalized")


def validate_end_state(label: str, artifact: dict[str, Any]) -> None:
    """Invariants any workflow artifact must keep, at any point in its life."""
    validate_artifact_keys(label, artifact)
    require(
        artifact["workflow_type"] in WORKFLOW_TYPES,
        f"{label}: unknown workflow_type '{artifact['workflow_type']}'",
    )
    finalized = count_memory_finalized(label, artifact)
    require(finalized <= 1, f"{label}: memory_finalized appears {finalized} times")
    if finalized:
        require(
            artifact["phase_cursor"] == "memory-finalize",
            f"{label}: memory_finalized recorded but phase_cursor is not memory-finalize",
        )


def validate_finalized_once(label: str, artifact: dict[str, Any]) -> None:
    validate_end_state(label, artifact)
    finalized = count_memory_finalized(label, artifact)
    require(finalized == 1, f"{label}: memory_finalized appears {finalized} times")
    require(
        artifact["status_history"][-1]["event"] == "memory_finalized",
        f"{label}: memory_finalized must be the last status_history event",
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
    # SCENARIOS_BLOCKED is optional and additive (ticket #83): absent means 0.
    blocked = contract.get("SCENARIOS_BLOCKED", 0)
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
        total != passed + failed + blocked
        or passed != actual_passed
        or total != len(scenarios)
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
    require(
        strict_bool(contract["PHASE_EXIT_READY"], True),
        f"{fixture_id}: phase exit must pass",
    )
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
    # Enforced builder PASS fields (sub-project 2a): preflight + behavioral RED reason.
    # Mandatory for every builder PASS contract — "enforced" means enforced in fixtures too.
    require(
        "BUILD_PREFLIGHT_EMITTED" in contract,
        f"{fixture_id}: builder PASS contract missing BUILD_PREFLIGHT_EMITTED (enforced gate)",
    )
    require(
        strict_bool(contract["BUILD_PREFLIGHT_EMITTED"], True),
        f"{fixture_id}: BUILD_PREFLIGHT_EMITTED must be true for PASS",
    )
    require(
        "TDD_RED_REASON_KIND" in contract,
        f"{fixture_id}: builder PASS contract missing TDD_RED_REASON_KIND (enforced gate)",
    )
    require(
        contract["TDD_RED_REASON_KIND"] == "behavioral",
        f"{fixture_id}: TDD_RED_REASON_KIND must be behavioral for PASS (false-RED rejected)",
    )
    require(
        bool(contract.get("TDD_RED_REASON")),
        f"{fixture_id}: behavioral RED requires non-empty TDD_RED_REASON",
    )
    # Enforced seam gate (sub-project 2a): TEST_SEAMS + SEAM_GATE_STATUS are contract fields.
    require(
        "SEAM_GATE_STATUS" in contract,
        f"{fixture_id}: builder PASS contract missing SEAM_GATE_STATUS (enforced gate)",
    )
    seam_status = contract.get("SEAM_GATE_STATUS")
    if seam_status is not None:
        require(
            seam_status in {"confirmed", "proposed", "disagreed", "not_applicable"},
            f"{fixture_id}: invalid SEAM_GATE_STATUS '{seam_status}'",
        )
        test_seams = contract.get("TEST_SEAMS", [])
        if seam_status in {"confirmed", "proposed"}:
            require(
                isinstance(test_seams, list) and len(test_seams) > 0,
                f"{fixture_id}: SEAM_GATE_STATUS={seam_status} requires non-empty TEST_SEAMS",
            )
        elif seam_status == "disagreed":
            # disagreed with non-empty TEST_SEAMS = better seam proposed; empty TEST_SEAMS only
            # valid when STATUS=FAIL with the exact ambiguity remediation reason.
            has_seams = isinstance(test_seams, list) and len(test_seams) > 0
            if has_seams:
                pass  # better seam proposed — valid
            else:
                require(
                    contract.get("STATUS") == "FAIL",
                    f"{fixture_id}: disagreed with empty TEST_SEAMS requires STATUS=FAIL (ambiguity block)",
                )
                reason = contract.get("REMEDIATION_REASON", "")
                require(
                    "Ambiguous test surface" in reason,
                    f"{fixture_id}: disagreed+empty+FAIL requires the ambiguity REMEDIATION_REASON",
                )
    validate_scenarios(fixture_id, contract["SCENARIOS"], require_pass=True)


def validate_investigator_contract(
    fixture_id: str, contract: dict[str, Any], *, allow_research: bool = False
) -> None:
    if allow_research:
        require(
            strict_bool(contract["NEEDS_EXTERNAL_RESEARCH"], True),
            f"{fixture_id}: expected research request",
        )
        require(contract["RESEARCH_REASON"], f"{fixture_id}: missing research reason")
        return
    require(contract["STATUS"] == "FIXED", f"{fixture_id}: investigator must be FIXED")
    require(contract["TDD_RED_EXIT"] == 1, f"{fixture_id}: missing regression RED")
    require(contract["TDD_GREEN_EXIT"] == 0, f"{fixture_id}: missing regression GREEN")
    require(
        bool(contract.get("BLAST_RADIUS_SCAN")),
        f"{fixture_id}: blast radius scan is required",
    )
    # Enforced feedback loop + debug close-out (sub-project 2a).
    # Mandatory for every FIXED contract — "enforced" means enforced in fixtures too.
    require(
        "FEEDBACK_LOOP" in contract,
        f"{fixture_id}: FIXED contract missing FEEDBACK_LOOP (enforced gate)",
    )
    require(
        "DEBUG_CLOSEOUT" in contract,
        f"{fixture_id}: FIXED contract missing DEBUG_CLOSEOUT (enforced gate)",
    )
    feedback_loop = contract.get("FEEDBACK_LOOP")
    if feedback_loop is not None:
        require(
            isinstance(feedback_loop, dict),
            f"{fixture_id}: FEEDBACK_LOOP must be an object",
        )
        require(
            feedback_loop.get("rung") != "none",
            f"{fixture_id}: FIXED requires FEEDBACK_LOOP.rung != none (no loop -> BLOCKED)",
        )
        require(
            bool(feedback_loop.get("command")),
            f"{fixture_id}: FIXED requires non-null FEEDBACK_LOOP.command",
        )
    closeout = contract.get("DEBUG_CLOSEOUT")
    if closeout is not None:
        require(
            isinstance(closeout, dict),
            f"{fixture_id}: DEBUG_CLOSEOUT must be an object",
        )
        require(
            strict_bool(closeout.get("instrumentation_removed"), True),
            f"{fixture_id}: FIXED requires DEBUG_CLOSEOUT.instrumentation_removed=true",
        )
        require(
            strict_bool(closeout.get("repro_no_longer_fires"), True),
            f"{fixture_id}: FIXED requires DEBUG_CLOSEOUT.repro_no_longer_fires=true",
        )
    scenarios = contract["SCENARIOS"]
    validate_scenarios(fixture_id, scenarios, require_pass=True)
    scenario_names = [scenario["name"] for scenario in scenarios]
    require(
        any(name.startswith("Regression:") for name in scenario_names),
        f"{fixture_id}: expected a Regression: scenario",
    )
    # Variant coverage is conditional: required unless the bug has no applicable
    # variants, in which case VARIANTS_NOT_APPLICABLE must explain why and
    # VARIANTS_COVERED must be 0 (no fabricated variant).
    if contract.get("VARIANTS_NOT_APPLICABLE"):
        require(
            contract["VARIANTS_COVERED"] == 0,
            f"{fixture_id}: VARIANTS_NOT_APPLICABLE set but VARIANTS_COVERED != 0",
        )
        require(
            not any(name.startswith("Variant:") for name in scenario_names),
            f"{fixture_id}: VARIANTS_NOT_APPLICABLE set but a Variant: scenario was fabricated",
        )
    else:
        require(
            contract["VARIANTS_COVERED"] >= 1,
            f"{fixture_id}: variant coverage must be at least 1",
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
    validate_convergence_states(fixture, fixture["id"])


def validate_convergence_states(node: Any, label: str = "fixture") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "convergence_state":
                require(
                    value in CONVERGENCE_STATES,
                    f"{label}: convergence_state {value!r} is not in CONVERGENCE_STATES {CONVERGENCE_STATES}",
                )
            else:
                validate_convergence_states(value, label)
    elif isinstance(node, list):
        for item in node:
            validate_convergence_states(item, label)


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
    require(strict_bool(planner["GATE_PASSED"], True), "plan-full: gate must pass")
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
    require(strict_bool(planner["BLOCKING"], True), "plan-clarification: must block")
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
        strict_bool(planner["GATE_PASSED"], True),
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
        strict_bool(planner["BLOCKING"], True),
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
        strict_bool(review["REPLAN_NEEDED"], False),
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
        strict_bool(review["REPLAN_NEEDED"], True),
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
        strict_bool(memory_sync["design_reference_persisted"], True),
        "plan-design-handoff: design reference must be persisted during memory finalization",
    )
    require(
        strict_bool(memory_sync["plan_recent_change_persisted"], True),
        "plan-design-handoff: plan save event must be persisted during memory finalization",
    )
    require(
        strict_bool(memory_sync["next_step_persisted"], True),
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
        == "converged",
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
        follow_up == ["re-review", "re-verify"],
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


def check_debug_fixed_no_variant(fixture: dict[str, Any]) -> None:
    # A genuinely no-variant bug must reach FIXED via VARIANTS_NOT_APPLICABLE
    # with VARIANTS_COVERED=0 and no fabricated Variant: scenario.
    contract = fixture["agent_outputs"]["investigator_contract"]
    validate_investigator_contract("debug-fixed-no-variant", contract)
    require(
        bool(contract.get("VARIANTS_NOT_APPLICABLE")),
        "debug-fixed-no-variant: expected VARIANTS_NOT_APPLICABLE to be set",
    )
    require(
        fixture["expected"]["next_action"] == "debug_review",
        "debug-fixed-no-variant: wrong next action",
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
        strict_bool(fixture["expected"]["code_mutation"], False),
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
        strict_bool(expected["collides_with_previous_session"], False),
        "workflow-identity-v10: ids must not collide across sessions",
    )


def check_memory_sync_blocking(fixture: dict[str, Any]) -> None:
    expected = fixture["expected"]
    require(
        expected["next_action"] == "stop_after_memory_sync",
        "memory-sync-blocking: wrong next action",
    )
    require(
        strict_bool(
            expected["artifact_delta"]["memory_sync"]["blocking_exit_persisted"], True
        ),
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


def validate_doc_syncer_contract(fixture_id: str, contract: dict[str, Any]) -> None:
    """Validate a doc-syncer Router Contract against the override rules."""
    valid_status = {"COMPLETE", "SKIPPED", "PARTIAL", "FAIL"}
    require(
        contract["STATUS"] in valid_status,
        f"{fixture_id}: invalid doc-syncer STATUS '{contract['STATUS']}'",
    )
    require("IMPACT_LEVEL" in contract, f"{fixture_id}: missing IMPACT_LEVEL")
    require(
        isinstance(contract.get("DOC_LAYERS_EVALUATED"), list),
        f"{fixture_id}: DOC_LAYERS_EVALUATED must be a list",
    )
    if contract["STATUS"] == "COMPLETE":
        require(
            len(contract.get("DOC_LAYERS_EVALUATED", [])) > 0,
            f"{fixture_id}: COMPLETE requires non-empty DOC_LAYERS_EVALUATED",
        )
        has_update = bool(contract.get("DOC_FILES_UPDATED")) or bool(
            contract.get("AUDIT_DOCS_CREATED")
        )
        require(
            has_update,
            f"{fixture_id}: COMPLETE requires DOC_FILES_UPDATED or AUDIT_DOCS_CREATED",
        )
    elif contract["STATUS"] == "SKIPPED":
        require(
            bool(contract.get("SKIP_REASON")),
            f"{fixture_id}: SKIPPED requires non-empty SKIP_REASON",
        )
    elif contract["STATUS"] == "PARTIAL":
        has_update = bool(contract.get("DOC_FILES_UPDATED")) or bool(
            contract.get("AUDIT_DOCS_CREATED")
        )
        require(
            has_update,
            f"{fixture_id}: PARTIAL requires DOC_FILES_UPDATED or AUDIT_DOCS_CREATED",
        )
        require(
            len(contract.get("DOC_LAYERS_EVALUATED", [])) > 0,
            f"{fixture_id}: PARTIAL requires non-empty DOC_LAYERS_EVALUATED",
        )


def check_build_doc_sync_happy_path(fixture: dict[str, Any]) -> None:
    ds = fixture["agent_outputs"]["doc_syncer_contract"]
    validate_doc_syncer_contract("build-doc-sync-happy-path", ds)
    require(ds["STATUS"] == "COMPLETE", "build-doc-sync-happy-path: expected COMPLETE")
    require(
        ds["IMPACT_LEVEL"] == "medium",
        "build-doc-sync-happy-path: expected medium impact",
    )
    require(
        bool(ds.get("AUDIT_DOCS_CREATED")),
        "build-doc-sync-happy-path: expected an audit doc created",
    )
    require(
        bool(ds.get("DOC_FILES_UPDATED")),
        "build-doc-sync-happy-path: expected DOC_FILES_UPDATED non-empty",
    )


def check_build_doc_sync_skipped(fixture: dict[str, Any]) -> None:
    ds = fixture["agent_outputs"]["doc_syncer_contract"]
    validate_doc_syncer_contract("build-doc-sync-skipped", ds)
    require(ds["STATUS"] == "SKIPPED", "build-doc-sync-skipped: expected SKIPPED")
    require(
        bool(ds.get("SKIP_REASON")),
        "build-doc-sync-skipped: expected non-empty SKIP_REASON",
    )


def validate_triage_contract(fixture_id: str, contract: dict[str, Any]) -> None:
    """Validate a triage-agent Router Contract."""
    valid_status = {"TRIAGED", "NEEDS_INFO", "WONTFIX"}
    require(
        contract["STATUS"] in valid_status,
        f"{fixture_id}: invalid triage STATUS '{contract['STATUS']}'",
    )
    if contract["STATUS"] == "TRIAGED":
        require(
            contract.get("CATEGORY") in {"bug", "enhancement"},
            f"{fixture_id}: TRIAGED requires CATEGORY bug|enhancement",
        )
        require(
            contract.get("STATE")
            in {
                "needs-triage",
                "needs-info",
                "ready-for-agent",
                "ready-for-human",
                "wontfix",
            },
            f"{fixture_id}: invalid STATE",
        )
        if contract.get("STATE") == "ready-for-agent":
            require(
                bool(contract.get("BRIEF_PATH")),
                f"{fixture_id}: ready-for-agent requires BRIEF_PATH",
            )
    require("REDUNDANCY_CHECK" in contract, f"{fixture_id}: missing REDUNDANCY_CHECK")
    require(
        "PRIOR_REJECTION_CHECK" in contract,
        f"{fixture_id}: missing PRIOR_REJECTION_CHECK",
    )


def triage_is_terminal(contract: dict[str, Any]) -> bool:
    return contract["STATUS"] == "WONTFIX" or (contract["STATUS"] == "TRIAGED" and contract.get("NEEDS_GRILLING") is not True)


def triage_pause_gate(contract: dict[str, Any]) -> str:
    return "needs_info" if contract["STATUS"] == "NEEDS_INFO" else "needs_grilling"


def health_is_terminal(contract: dict[str, Any], expected: dict[str, Any]) -> bool:
    return contract["STATUS"] == "NO_CANDIDATES" or expected.get("candidate_choice") in {"declined", "grill_completed"}


def note_strings(node: Any) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, dict):
        return [text for value in node.values() for text in note_strings(value)]
    if isinstance(node, list):
        return [text for value in node for text in note_strings(value)]
    return []


def validate_advisory_memory_task(
    label: str, fixture: dict[str, Any], agent_phase: str, terminal: bool, contract: dict[str, Any], paused_gate: str
) -> None:
    """Memory Update exists, blocked on the agent task, only at the terminal state; a paused workflow has none."""
    tasks = fixture["relevant_tasks"]
    artifact = fixture["starting_artifact"]
    require(
        artifact["quality"]["convergence_state"] == "N/A",
        f"{label}: an advisory workflow must carry convergence_state N/A, got {artifact['quality']['convergence_state']!r}",
    )
    require(
        not artifact["remediation_history"],
        f"{label}: an advisory workflow must carry no remediation_history entries, got {len(artifact['remediation_history'])}",
    )
    agents = [key for key, task in tasks.items() if task["phase"] == agent_phase]
    memory = [key for key, task in tasks.items() if task["phase"] == "memory-finalize"]
    require(len(agents) == 1, f"{label}: expected one {agent_phase} task, got {agents}")
    if terminal:
        require(len(memory) == 1, f"{label}: expected one memory-finalize task, got {memory}")
        require(
            tasks[memory[0]]["blockedBy"] == agents,
            f"{label}: Memory Update must be blocked by the {agent_phase} task, got {tasks[memory[0]]['blockedBy']}",
        )
        require(
            not artifact.get("pending_gate"),
            f"{label}: a terminal advisory workflow must not carry a pending_gate, got {artifact.get('pending_gate')!r}",
        )
        return
    require(not memory, f"{label}: Memory Update must not exist before the terminal state, got {memory}")
    require(
        count_memory_finalized(label, artifact) == 0 and artifact["phase_cursor"] != "memory-finalize",
        f"{label}: memory_finalized recorded before the terminal state",
    )
    require(bool(artifact.get("pending_gate")), f"{label}: a paused advisory workflow must carry a pending_gate")
    require(
        artifact["pending_gate"] == paused_gate,
        f"{label}: pending_gate must be '{paused_gate}' for this pause, got {artifact['pending_gate']!r}",
    )
    sink = set(note_strings(artifact.get("memory_notes", [])))
    missing = [note for note in note_strings(contract.get("MEMORY_NOTES", {})) if note not in sink]
    require(not missing, f"{label}: paused artifact memory_notes is missing the captured notes {missing}")


def check_triage_happy_path(fixture: dict[str, Any]) -> None:
    ta = fixture["agent_outputs"]["triage_agent_contract"]
    validate_advisory_memory_task("triage-happy-path", fixture, "triage", triage_is_terminal(ta), ta, triage_pause_gate(ta))
    validate_triage_contract("triage-happy-path", ta)
    require(ta["STATUS"] == "TRIAGED", "triage-happy-path: expected TRIAGED")
    require(ta["CATEGORY"] == "bug", "triage-happy-path: expected bug")
    require(
        ta["STATE"] == "ready-for-agent",
        "triage-happy-path: expected ready-for-agent",
    )
    require(
        bool(ta.get("BRIEF_PATH")),
        "triage-happy-path: expected non-empty BRIEF_PATH",
    )


def validate_architecture_scanner_contract(
    fixture_id: str, contract: dict[str, Any]
) -> None:
    """Validate an architecture-scanner Router Contract."""
    valid_status = {"CANDIDATES_FOUND", "NO_CANDIDATES"}
    require(
        contract["STATUS"] in valid_status,
        f"{fixture_id}: invalid scanner STATUS '{contract['STATUS']}'",
    )
    if contract["STATUS"] == "CANDIDATES_FOUND":
        candidates = contract.get("CANDIDATES", [])
        require(
            isinstance(candidates, list) and len(candidates) > 0,
            f"{fixture_id}: CANDIDATES_FOUND requires non-empty CANDIDATES array",
        )
        require(
            bool(contract.get("REPORT_PATH")),
            f"{fixture_id}: CANDIDATES_FOUND requires REPORT_PATH",
        )


def check_codebase_health_happy_path(fixture: dict[str, Any]) -> None:
    asc = fixture["agent_outputs"]["architecture_scanner_contract"]
    validate_advisory_memory_task(
        "codebase-health-happy-path", fixture, "codebase-health", health_is_terminal(asc, fixture["expected"]), asc, "candidate_choice"
    )
    validate_architecture_scanner_contract("codebase-health-happy-path", asc)
    require(
        asc["STATUS"] == "CANDIDATES_FOUND",
        "codebase-health-happy-path: expected CANDIDATES_FOUND",
    )
    require(
        len(asc.get("CANDIDATES", [])) >= 2,
        "codebase-health-happy-path: expected >=2 candidates",
    )
    require(
        bool(asc.get("REPORT_PATH")),
        "codebase-health-happy-path: expected non-empty REPORT_PATH",
    )


def check_triage_needs_info_pause(fixture: dict[str, Any]) -> None:
    ta = fixture["agent_outputs"]["triage_agent_contract"]
    validate_triage_contract("triage-needs-info-pause", ta)
    require(ta["STATUS"] == "NEEDS_INFO", "triage-needs-info-pause: expected NEEDS_INFO")
    validate_advisory_memory_task("triage-needs-info-pause", fixture, "triage", triage_is_terminal(ta), ta, triage_pause_gate(ta))


def check_codebase_health_candidate_pause(fixture: dict[str, Any]) -> None:
    asc = fixture["agent_outputs"]["architecture_scanner_contract"]
    validate_architecture_scanner_contract("codebase-health-candidate-pause", asc)
    require(
        asc["STATUS"] == "CANDIDATES_FOUND",
        "codebase-health-candidate-pause: expected CANDIDATES_FOUND",
    )
    validate_advisory_memory_task(
        "codebase-health-candidate-pause", fixture, "codebase-health", health_is_terminal(asc, fixture["expected"]), asc, "candidate_choice"
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


def check_qa_route_happy_path(fixture: dict[str, Any]) -> None:
    label = "qa-route-happy-path"
    artifact = fixture["starting_artifact"]
    tasks = fixture["relevant_tasks"]
    require(artifact["workflow_type"] == "QA", f"{label}: wrong workflow type")
    validate_finalized_once(label, artifact)
    require(artifact["proof_status"] == "passed", f"{label}: finished QA must record proof_status passed")
    phases = [t["phase"] for t in tasks.values()]
    require(
        phases == list(QA_ROUTE_PHASES),
        f"{label}: QA route phases {phases} != {list(QA_ROUTE_PHASES)}",
    )
    for key, task in tasks.items():
        require(
            task["wf"] == artifact["workflow_id"],
            f"{label}: {key} carries wf {task['wf']}, expected {artifact['workflow_id']}",
        )
        require(task["status"] == "completed", f"{label}: {key} must be completed")
        require(
            task["blockedBy"] == QA_ROUTE_BLOCKERS[key],
            f"{label}: {key} blockedBy {task['blockedBy']} != {QA_ROUTE_BLOCKERS[key]}",
        )
    qa = artifact["qa"]
    require(qa["qa_scope"] in {"probe", "standard"}, f"{label}: qa_scope must be probe|standard")
    require(
        strict_bool(qa["isolation"]["plan_phase_readonly"], True),
        f"{label}: qa.isolation.plan_phase_readonly must be true",
    )
    require(
        qa["isolation"]["mutation_allowlist"] == [".cc10x/"],
        f"{label}: qa.isolation.mutation_allowlist must be ['.cc10x/']",
    )


def check_remfix_gate(fixture: dict[str, Any]) -> None:
    label = "remfix-gate"
    artifact = fixture["starting_artifact"]
    remfix = fixture["relevant_tasks"]["completed_remfix"]
    require(remfix["kind"] == "remfix", f"{label}: wrong task kind")
    require(remfix["wf"] == artifact["workflow_id"], f"{label}: remfix task carries a foreign wf")
    require(remfix["status"] == "completed", f"{label}: completed_remfix must be completed, got {remfix['status']!r}")
    report = fixture["agent_outputs"]["remfix_report"]
    for field in ("COVERING_TESTS", "TEST_COMMAND", "TEST_OUTPUT"):
        require(field in report, f"{label}: REM-FIX report missing {field}")
    covering = report["COVERING_TESTS"]
    require(isinstance(covering, list) and bool(covering), f"{label}: REM-FIX report empty COVERING_TESTS (a non-empty list of test file names)")
    require(
        all(isinstance(item, str) and item.strip() for item in covering),
        f"{label}: REM-FIX report has a blank entry in COVERING_TESTS",
    )
    for field in ("TEST_COMMAND", "TEST_OUTPUT"):
        value = report[field]
        require(isinstance(value, str) and bool(value.strip()), f"{label}: REM-FIX report empty {field} (a non-blank string)")
    history = artifact["remediation_history"]
    cycles = [entry.get("cycle_number") for entry in history]
    require(
        cycles == list(range(1, len(history) + 1)) and 1 <= len(history) <= 3,
        f"{label}: remediation_history cycle_number must run 1..n with n <= 3, got {cycles}",
    )
    require(
        fixture["expected"]["follow_up_tasks"] == ["re-review", "re-hunt", "re-verify"],
        f"{label}: gate proof present, so re-review, re-hunt and re-verify must be created",
    )


def check_multi_phase_memory_finalize(fixture: dict[str, Any]) -> None:
    label = "multi-phase-memory-finalize"
    artifact = fixture["starting_artifact"]
    validate_finalized_once(label, artifact)
    phases = artifact["normalized_phases"]
    require(len(phases) >= 2, f"{label}: expected a multi-phase workflow")
    for phase in phases:
        require("phase_id" in phase, f"{label}: normalized_phases entries carry phase_id, got keys {sorted(phase)}")
        require(
            artifact["phase_status"].get(phase["phase_id"]) == "completed",
            f"{label}: phase {phase['phase_id']} must be completed before memory finalizes",
        )
    memory_tasks = [
        key
        for key, task in fixture["relevant_tasks"].items()
        if task["phase"] == "memory-finalize"
    ]
    require(
        len(memory_tasks) == 1,
        f"{label}: exactly one memory-finalize task expected, got {memory_tasks}",
    )
    logged = fixture["expected"]["event_log_events"].count("memory_finalized")
    require(logged == 1, f"{label}: event log memory_finalized appears {logged} times")
    tasks = fixture["relevant_tasks"]
    verifiers = [key for key, task in tasks.items() if task["phase"] == "build-verify"]
    require(len(verifiers) == len(phases), f"{label}: expected one build-verify task per phase, got {verifiers}")
    blocked_by = tasks[memory_tasks[0]]["blockedBy"]
    last_verifier = verifiers[-1]
    doc_syncs = [
        key
        for key in blocked_by
        if tasks.get(key, {}).get("phase") == "build-doc-sync" and last_verifier in tasks[key]["blockedBy"]
    ]
    require(
        last_verifier in blocked_by or bool(doc_syncs),
        f"{label}: memory_finalize must be blocked by the last phase's verifier {last_verifier} or by its doc-sync task, got {blocked_by}",
    )
    implementers = [key for key, task in tasks.items() if task["phase"] == "build-implement"]
    early_doc_syncs = {
        key
        for key, task in tasks.items()
        if task["phase"] == "build-doc-sync" and set(task["blockedBy"]) & set(verifiers[:-1])
    }
    earlier = set(verifiers[:-1]) | set(implementers[:-1]) | early_doc_syncs
    require(
        not earlier & set(blocked_by),
        f"{label}: memory_finalize is blocked by an earlier-phase task {sorted(earlier & set(blocked_by))}",
    )
    for index in range(1, len(phases)):
        prior_verifier = verifiers[index - 1]
        prior_last = [
            key for key, task in tasks.items() if task["phase"] == "build-doc-sync" and prior_verifier in task["blockedBy"]
        ] or [prior_verifier]
        builder_blockers = set(tasks[implementers[index]]["blockedBy"])
        require(
            set(prior_last) <= builder_blockers,
            f"{label}: {implementers[index]} must be blocked on the previous phase's last task {prior_last}, got {sorted(builder_blockers)}",
        )


PAUSE_DECISIONS = {"NEEDS_INFO", "NEEDS_GRILLING"}
TERMINAL_EVENTS = {"memory_finalized", "workflow_completed", "workflow_failed"}


def normalized_phase_id(value: Any) -> Any:
    return "N/A" if value is None else value


def event_phase_id(event: dict[str, Any]) -> Any:
    return normalized_phase_id((event.get("details") or {}).get("phase_id"))


def runnable_steps_from_events(events: list[dict[str, Any]], phase_id: Any, graph: list[dict[str, Any]]) -> list[str]:
    """SKILL.md section 4 rule: a step is complete only if its non-pause result_persisted event for this phase_id is newer than the latest phase_started or remediation_created event for that phase_id (workflow_started when neither exists); null, missing and N/A phase ids are equal."""
    phase_id = normalized_phase_id(phase_id)
    boundary = -1
    for index, event in enumerate(events):
        if event["event"] in {"phase_started", "remediation_created"} and event_phase_id(event) == phase_id:
            boundary = index
    if boundary < 0:
        boundary = max((i for i, e in enumerate(events) if e["event"] == "workflow_started"), default=-1)
    complete = {
        (event["agent"], event["phase"])
        for event in events[boundary + 1 :]
        if event["event"] == "result_persisted"
        and event_phase_id(event) == phase_id
        and event.get("decision") not in PAUSE_DECISIONS
    }
    done_phases = {phase for _, phase in complete}
    return sorted(
        step["phase"]
        for step in graph
        if (step["agent"], step["phase"]) not in complete and set(step["after"]) <= done_phases
    )


def locate_resume(case: dict[str, Any]) -> dict[str, Any]:
    """SKILL.md section 4 step 6(a): drop terminal artifacts, resume on a uuid or request match, else look up non-terminal artifacts with a pending_gate."""
    live = [
        a
        for a in case["artifacts"]
        if not ({h["event"] for h in a["status_history"]} & TERMINAL_EVENTS) and a.get("phase_cursor") != "memory-finalize"
    ]
    matched = [a for a in live if a["workflow_uuid"] == case["named_uuid"] or a["workflow_uuid"] in case["request_matches"]]
    if len(matched) == 1:
        return {"action": "resume", "wf": matched[0]["workflow_uuid"]}
    if len(matched) > 1:
        return {"action": "ask_which"}
    paused = {a["workflow_uuid"]: a for a in live if a.get("pending_gate")}
    if len(paused) == 1:
        return {"action": "answer_gate", "wf": next(iter(paused))}
    if len(paused) > 1:
        return {"action": "ask_which", "gates": sorted(a["pending_gate"] for a in paused.values())}
    return {"action": "new_workflow"}


def check_multi_phase_resume_events(fixture: dict[str, Any]) -> None:
    label = "multi-phase-resume-events"
    results = fixture["starting_artifact"]["results"]
    require(bool(fixture["cases"]), f"{label}: no cases")
    for case in fixture["cases"]:
        for slot in case["stale_slots"]:
            require(
                results.get(slot) is not None,
                f"{label}: stale slot results.{slot} must hold an earlier value, or the case no longer shows the flat-slot trap",
            )
        runnable = runnable_steps_from_events(case["events"], case["phase_id"], case["graph"])
        require(
            runnable == sorted(case["expected_runnable"]),
            f"{label}: runnable steps for '{case['name']}' are {runnable}, expected {sorted(case['expected_runnable'])}",
        )
    require(bool(fixture["locator_cases"]), f"{label}: no locator cases")
    for case in fixture["locator_cases"]:
        located = locate_resume(case)
        require(
            located == case["expected"],
            f"{label}: resume locator for '{case['name']}' is {located}, expected {case['expected']}",
        )


def check_two_workflow_resume(fixture: dict[str, Any]) -> None:
    label = "two-workflow-resume"
    first = fixture["starting_artifact"]
    second = fixture["other_artifact"]
    validate_end_state(label, first)
    validate_end_state(f"{label} other_artifact", second)
    require(
        first["workflow_id"] != second["workflow_id"],
        f"{label}: concurrent workflows need distinct workflow_id",
    )
    expected = fixture["expected"]
    wf = expected["resume_wf"]
    require(wf == first["workflow_id"], f"{label}: resume must be scoped to the conversation's workflow")
    require(
        strict_bool(expected["unscoped_fallback_used"], False),
        f"{label}: unscoped fallback resume is forbidden",
    )
    tasks = fixture["relevant_tasks"]
    for key in expected["resumed_tasks"]:
        require(tasks[key]["wf"] == wf, f"{label}: resumed task {key} carries wf {tasks[key]['wf']}, expected {wf}")
    for key in expected["ignored_tasks"]:
        require(tasks[key]["wf"] != wf, f"{label}: ignored task {key} carries the resumed wf")
    covered = set(expected["resumed_tasks"]) | set(expected["ignored_tasks"])
    require(covered == set(tasks), f"{label}: every task must be either resumed or ignored")


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
    "build-doc-sync-happy-path.json": check_build_doc_sync_happy_path,
    "build-doc-sync-skipped.json": check_build_doc_sync_skipped,
    "triage-happy-path.json": check_triage_happy_path,
    "codebase-health-happy-path.json": check_codebase_health_happy_path,
    "triage-needs-info-pause.json": check_triage_needs_info_pause,
    "codebase-health-candidate-pause.json": check_codebase_health_candidate_pause,
    "debug-fixed.json": check_debug_fixed,
    "debug-fixed-no-variant.json": check_debug_fixed_no_variant,
    "debug-research.json": check_debug_research,
    "skill-precedence.json": check_skill_precedence,
    "workflow-identity-v10.json": check_workflow_identity_v10,
    "memory-sync-blocking.json": check_memory_sync_blocking,
    "review-advisory.json": check_review_advisory,
    "verify-fail-closed.json": check_verify_fail_closed,
    "latency-telemetry.json": check_latency_telemetry,
    "qa-route-happy-path.json": check_qa_route_happy_path,
    "remfix-gate.json": check_remfix_gate,
    "multi-phase-memory-finalize.json": check_multi_phase_memory_finalize,
    "multi-phase-resume-events.json": check_multi_phase_resume_events,
    "two-workflow-resume.json": check_two_workflow_resume,
}


def read_events_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise AssertionError(f"{path.name} line {number} is not JSON: {exc}") from exc
        require(isinstance(event, dict) and "event" in event, f"{path.name} line {number} must be an object with an event")
        events.append(event)
    return events


def validate_artifact_file(path: Path, artifact: Any) -> None:
    """Shape invariants for one real artifact plus its sibling `<stem>.events.jsonl` when present.

    The router records memory finalization in status_history AND the events log, but real runs have
    left it in only one of them, so each source is counted on its own: a source holding more than one
    memory_finalized is a double finalize, while one in each source is the same single finalization.

    The completed-implies-finalized rule covers only the workflow types whose router graph creates a
    Memory Update task (MEMORY_TASK_WORKFLOW_TYPES: every route except ORIENT, which creates no task). TRIAGE
    and CODEBASE-HEALTH joined the set when their graphs gained a Memory Update task (finding B2, plan P4.T1.4);
    a real TRIAGE or CODEBASE-HEALTH artifact written before that change and completed without a finalize now fails.
    """
    require(isinstance(artifact, dict), f"{path.name}: artifact must be a JSON object, got {type(artifact).__name__}")
    validate_end_state(path.name, artifact)
    sibling = path.with_name(path.stem + ".events.jsonl")
    events = read_events_jsonl(sibling) if sibling.is_file() else []
    in_history = count_memory_finalized(path.name, artifact)
    in_events = sum(1 for e in events if e["event"] == "memory_finalized")
    require(in_events <= 1, f"{path.name}: memory_finalized appears {in_events} times in events.jsonl")
    if in_events:
        require(
            artifact["phase_cursor"] == "memory-finalize",
            f"{path.name}: memory_finalized recorded but phase_cursor is not memory-finalize",
        )
    uuid = artifact["workflow_uuid"]
    for event in events:
        require(
            event.get("wf", uuid) == uuid,
            f"{path.name}: events.jsonl event {event['event']} carries a foreign wf {event.get('wf')}",
        )
    completed = any(e["event"] == "workflow_completed" for e in artifact["status_history"] + events)
    if completed and artifact["workflow_type"] in MEMORY_TASK_WORKFLOW_TYPES:
        require(
            in_history + in_events >= 1,
            f"{path.name}: workflow completed but memory_finalized is recorded in neither status_history nor events.jsonl",
        )


def check_artifact_file(path: Path) -> int:
    try:
        validate_artifact_file(path, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, AssertionError, KeyError, TypeError) as exc:
        print(f"FAIL: {path}: {exc}", file=sys.stderr)
        return 1
    print(f"cc10x_workflow_replay_check: artifact OK ({path.name})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay the workflow fixtures, or validate one artifact file.")
    parser.add_argument("--artifact", type=Path, help="validate a real workflow artifact JSON against the shape invariants")
    args = parser.parse_args()
    if args.artifact is not None:
        return check_artifact_file(args.artifact)

    if not FIXTURES_DIR.exists():
        print("FAIL: fixtures directory missing", file=sys.stderr)
        return 1

    errors: list[str] = list(check_registry_complete())
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
