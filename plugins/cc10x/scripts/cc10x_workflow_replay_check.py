#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
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

REQUIRED_ARTIFACT_KEYS = (
    "workflow_id",
    "workflow_type",
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


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_artifact_shape(fixture: dict[str, Any]) -> None:
    artifact = fixture["starting_artifact"]
    missing = [key for key in REQUIRED_ARTIFACT_KEYS if key not in artifact]
    require(not missing, f"{fixture['id']}: artifact missing keys {missing}")


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
    require(contract["TDD_RED_EXIT"] == 1, f"{fixture_id}: missing RED evidence")
    require(contract["TDD_GREEN_EXIT"] == 0, f"{fixture_id}: missing GREEN evidence")
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


def check_plan_direct(fixture: dict[str, Any]) -> None:
    expected = fixture["expected"]
    require(expected["next_action"] == "build_direct", "plan-direct: wrong next action")
    require(
        fixture["starting_artifact"]["workflow_type"] == "PLAN",
        "plan-direct: wrong workflow type",
    )
    require(expected["pending_gate"] is None, "plan-direct: should not pause")


def check_plan_full(fixture: dict[str, Any]) -> None:
    planner = fixture["agent_outputs"]["planner_contract"]
    require(
        planner["STATUS"] == "PLAN_CREATED", "plan-full: planner should create plan"
    )
    require(planner["PLAN_FILE"], "plan-full: missing plan file")
    require(planner["GATE_PASSED"] is True, "plan-full: gate must pass")
    validate_scenarios("plan-full", planner["SCENARIOS"], require_pass=False)
    require(
        fixture["expected"]["artifact_delta"]["plan_file"] == planner["PLAN_FILE"],
        "plan-full: expected plan_file delta mismatch",
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


CHECKS = {
    "plan-direct.json": check_plan_direct,
    "plan-full.json": check_plan_full,
    "plan-clarification.json": check_plan_clarification,
    "build-happy-path.json": check_build_happy_path,
    "build-scope-gate.json": check_build_scope_gate,
    "build-remediation-loop.json": check_build_remediation_loop,
    "debug-fixed.json": check_debug_fixed,
    "debug-research.json": check_debug_research,
    "review-advisory.json": check_review_advisory,
    "verify-fail-closed.json": check_verify_fail_closed,
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
