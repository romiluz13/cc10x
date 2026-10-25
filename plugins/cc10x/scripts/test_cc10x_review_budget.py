"""Budget behavior through the production CLI and temporary durable state."""
from __future__ import annotations

import json
import hashlib
import os
import subprocess
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("cc10x_review_budget.py")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class Client:
    def __init__(self, root, artifact=None, initialize=True):
        self.root = root / ".cc10x"
        self.workflow = self.root / "workflows" / "wf-a.json"
        self.workflow.parent.mkdir(parents=True)
        self.workflow.write_text(json.dumps(artifact or {"workflow_uuid": "wf-a"}))
        self.serial = 0
        self.reservations = {}
        if initialize:
            self.call(dict(op="init", lineage_id="lineage-a", subject_id="subject-a"))

    def call(self, request, expected=0, project=True):
        self.serial += 1
        path = self.root / ("request-%s.json" % self.serial)
        path.write_text(json.dumps(request))
        run = subprocess.run([sys.executable, str(SCRIPT), "--state-root", str(self.root),
                              "--workflow", str(self.workflow), "--request", str(path)],
                             capture_output=True, text=True)
        assert run.returncode == expected, run.stdout + run.stderr
        result = json.loads(run.stdout)
        if request["op"] == "reserve" and expected == 0:
            self.reservations[request["attempt_id"]] = request
        if project and result.get("projection") is not None and expected == 0:
            artifact = json.loads(self.workflow.read_text())
            artifact["review_budget"] = result["projection"]
            self.workflow.write_text(json.dumps(artifact))
        return result

    def reserve(self, attempt="a", role="component-builder", source=None, content="input", **changes):
        node = dict(lineage_id="lineage-a", subject_id="subject-a", step_key="build",
                    phase_id="P1", role=role, source_id=source, repository_id=None)
        request = dict(op="reserve", event_id="reserve-" + attempt, attempt_id=attempt,
                       workflow_uuid="wf-a", subject_id="subject-a", recorded_at="2026-01-01T00:00:00Z",
                       node_descriptor=node, node_id=digest(node), dependency_node_ids=[],
                       lane="work", phase_id="P1", scope_digest=digest("scope"),
                       parent_attempt_id=None, retry_of=None, input_digest=digest("input"),
                       input_refs=[dict(ref="graph-row", digest=digest(node)), dict(ref="content", digest=digest(content))],
                       authorization_checks=[], finding_ids=[], checkpoint_id=None)
        request.update(changes)
        if "input_digest" not in changes:
            request["input_digest"] = digest(dict(scope_digest=request["scope_digest"], role=role,
                                                   input_refs=sorted(request["input_refs"], key=lambda r: (r["ref"], r["digest"]))))
        return request

    def finish(self, attempt="a", outcome="invalid", **changes):
        request = dict(op="finish", event_id="finish-" + attempt, workflow_uuid="wf-a",
                       subject_id="subject-a", recorded_at="2026-01-01T00:00:01Z", attempt_id=attempt,
                       outcome=outcome, contract_ref=None, contract_digest=None, verdict=None,
                       review_mode=None, reviewed_revision=None,
                       reviewed_input_digest=getattr(self, "reservations", {}).get(attempt, {}).get("input_digest"),
                       spec_gate_iterations=0, evidence_refs=[],
                       measurement=dict(availability="unknown", tokens=None, agent_seconds=None, source=None))
        request.update(changes)
        return request


@pytest.mark.parametrize("role,phase", [("qa-harness-builder", "re-qa-build"),
                                         ("component-builder", "build-implement"),
                                         ("bug-investigator", "debug-investigate")])
def test_remfix4_remediation_executors_charge_and_retain_slots(tmp_path, role, phase):
    client = Client(tmp_path)

    def reservation(attempt):
        request = client.reserve(attempt, role=role, source=attempt, lane="remediation", phase_id=phase)
        node = dict(request["node_descriptor"], phase_id=phase, step_key=phase)
        refs = [dict(ref="approved-remfix-row", digest=digest(node)), dict(ref="content", digest=digest("repair"))]
        return client.reserve(attempt, role=role, source=attempt, lane="remediation", phase_id=phase,
                              node_descriptor=node, node_id=digest(node), input_refs=refs)

    for index, outcome in enumerate(("invalid", "cancelled", "lost"), 1):
        attempt = "repair-%s" % index
        request = reservation(attempt)
        result = client.call(request)
        assert result["dispatch"] == "new"
        assert result["reservation"]["node_descriptor"]["role"] == role
        assert result["reservation"]["lane"] == "remediation"
        replay = client.call(request)
        assert replay["dispatch"] == "resume" and replay["ledger_revision"] == result["ledger_revision"]
        projection = client.call(client.finish(attempt, outcome))["projection"]
        assert (projection["counts"]["attempts"], projection["counts"]["remediation_attempts"],
                projection["charged_units"], projection["remaining_units"]) == (index, index, index, 32-index)
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    rejected = client.call(reservation("fourth"), 2)
    assert rejected["reasons"] == ["lane_limit"]
    assert path.read_bytes() == before
    # Ordinary work by the same executor still spends units without repair credit.
    ordinary = client.call(client.reserve("ordinary", role=role, source="ordinary"))["projection"]
    assert (ordinary["counts"]["attempts"], ordinary["counts"]["remediation_attempts"],
            ordinary["charged_units"], ordinary["remaining_units"]) == (4, 3, 4, 28)


def test_remfix4_qa_remediation_cannot_bypass_aggregate_funds(tmp_path):
    client = Client(tmp_path)
    for index in range(8):
        client.call(client.reserve("planner-%s" % index, role="planner", source="source-%s" % index))
    projection = client.call(dict(op="inspect"))["projection"]
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    result = client.call(client.reserve("repair", role="qa-harness-builder", lane="remediation"), 2)
    assert result["reasons"] == ["insufficient_eligible_units"]
    assert path.read_bytes() == before
    assert projection["charged_units"] == 32 and projection["counts"]["remediation_attempts"] == 0


@pytest.mark.parametrize("role,lane", [("qa-harness-builder", "fresh"), ("qa-harness-builder", "amendment"),
                                       ("qa-harness-builder", "code_review"), ("qa-executor", "remediation"),
                                       ("qa-researcher", "remediation"), ("planner", "remediation")])
def test_remfix4_specialized_remediation_does_not_expand_other_roles_or_lanes(tmp_path, role, lane):
    client = Client(tmp_path)
    projection = client.call(dict(op="inspect"))["projection"]
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    result = client.call(client.reserve(role=role, lane=lane), 3)
    assert result["reasons"] == ["role_lane_mismatch"]
    assert path.read_bytes() == before


def correction_requests(client, prior, name="corrected", proof_refs=None, pending=False):
    instruction = dict(ref="contract-instruction-" + name, digest=digest("Return required role fields " + name))
    request = dict(prior, event_id="reserve-" + name, attempt_id=name,
                   retry_of=prior["attempt_id"], checkpoint_id="checkpoint-" + name,
                   input_refs=prior["input_refs"] + [instruction])
    request["input_digest"] = digest(dict(scope_digest=request["scope_digest"],
                                         role=request["node_descriptor"]["role"],
                                         input_refs=sorted(request["input_refs"], key=lambda r: (r["ref"], r["digest"]))))
    p = client.call(dict(op="inspect"), 2 if pending else 0)["projection"]
    cp = dict(op="checkpoint", event_id="event-" + name, checkpoint_id=request["checkpoint_id"],
              workflow_uuid="wf-a", subject_id="subject-a", recorded_at="2026-01-01T00:00:02Z",
              action="continue", observed_revision=p["ledger_revision"], scope_digest=prior["scope_digest"],
              input_digest=request["input_digest"], finding_ids=[], proof_refs=proof_refs or [],
              changed_input_refs=[dict(ref="malformed-output", digest=digest("malformed-output")), instruction],
              progress="finite_fix", reopened_ids=[], scope_change="none",
              rationale="Malformed role fields; add only required contract instructions",
              remaining_units=p["remaining_units"],
              contract_correction=dict(invalid_attempt_id=prior["attempt_id"], instruction=instruction))
    return cp, request


def invalid_contract(client, attempt):
    return client.finish(attempt, contract_ref="malformed-output", contract_digest=digest("malformed-output"))


@pytest.mark.parametrize("role,lane,credit,limit", [("plan-gap-reviewer", "fresh", "fresh_valid", 2),
    ("plan-gap-reviewer", "amendment", "amendment_valid", 3),
    ("code-reviewer", "code_review", "code_review_valid", 4)])
def test_contract_correction_cli(tmp_path, role, lane, credit, limit):
    client = Client(tmp_path)
    first = client.reserve(role=role, lane=lane)
    client.call(first)
    client.call(invalid_contract(client, "a"))
    cp, retry = correction_requests(client, first)
    client.call(cp)
    result = client.call(retry)
    assert result["dispatch"] == "new"
    assert (result["projection"]["counts"]["attempts"], result["projection"]["charged_units"],
            result["projection"]["remaining_units"], result["projection"]["counts"][credit]) == (2, 2, 30, 0)
    assert client.call(retry)["dispatch"] == "resume"
    assert client.call(retry)["projection"] == result["projection"]
    unchanged = dict(retry, event_id="reserve-identical", attempt_id="identical", retry_of="corrected")
    assert client.call(unchanged, 2)["reasons"] == ["node_unresolved"]
    client.call(invalid_contract(client, "corrected"))
    assert client.call(unchanged, 2)["reasons"] == ["unchanged_input"]
    second_cp, _ = correction_requests(client, retry, "second-correction")
    assert client.call(second_cp, 2)["reasons"] == ["contract_correction_used"]
    # Failed fresh/code reviews release their slots; amendment attempts consume them.
    available = limit - (2 if lane == "amendment" else 0)
    for n in range(available):
        client.call(client.reserve("slot-%s" % n, role=role, lane=lane, source="slot-%s" % n))
    assert client.call(client.reserve("overflow", role=role, lane=lane, source="overflow"), 2)["reasons"] == ["lane_limit"]


@pytest.mark.parametrize("case,reason,exit_code", [
    ("null", "invalid_contract_correction", 3), ("empty", "invalid_contract_correction", 3),
    ("extra", "invalid_contract_correction", 3), ("instruction-extra", "invalid_contract_correction", 3),
    ("missing-receipt", "invalid_text", 3), ("bad-receipt", "invalid_digest", 3),
    ("wrong-receipt", "contract_correction_evidence", 2),
    ("missing-instruction", "contract_correction_evidence", 2),
    ("unknown-attempt", "contract_correction_attempt", 2),
    ("cancelled", "contract_correction_outcome", 2), ("lost", "contract_correction_outcome", 2),
    ("valid", "contract_correction_outcome", 2), ("unresolved", "contract_correction_outcome", 2),
    ("unsafe", "progress_stop", 2), ("no-progress", "progress_stop", 2),
])
def test_contract_correction_checkpoint_controls(tmp_path, case, reason, exit_code):
    client = Client(tmp_path)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh")
    client.call(first)
    finish = invalid_contract(client, "a")
    if case in ("cancelled", "lost", "valid"):
        finish.update(outcome=case, verdict="FINDINGS", review_mode="fresh", reviewed_revision=1)
    if case == "missing-receipt":
        finish.update(contract_ref=None, contract_digest=None)
    if case == "bad-receipt":
        finish["contract_digest"] = "bad"
    if case != "unresolved":
        client.call(finish)
    cp, _ = correction_requests(client, first)
    if case in ("null", "empty"):
        cp["contract_correction"] = None if case == "null" else {}
    if case == "extra":
        cp["contract_correction"]["extra"] = True
    if case == "instruction-extra":
        cp["contract_correction"]["instruction"]["extra"] = True
    if case == "wrong-receipt":
        cp["changed_input_refs"][0]["digest"] = digest("other")
    if case == "missing-instruction":
        cp["changed_input_refs"] = cp["changed_input_refs"][:1]
    if case == "unknown-attempt":
        cp["contract_correction"]["invalid_attempt_id"] = "unknown"
    if case == "unsafe":
        cp["scope_change"] = "security"
    if case == "no-progress":
        cp["progress"] = "none"
    path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    before = path.read_bytes()
    assert client.call(cp, exit_code)["reasons"] == [reason]
    assert path.read_bytes() == before


@pytest.mark.parametrize("case,reason", [
    ("changed-content", "contract_correction_input"), ("extra-input", "contract_correction_input"),
    ("wrong-instruction", "contract_correction_input"), ("scope", "contract_correction_identity"),
    ("dependencies", "contract_correction_identity"), ("lane", "contract_correction_identity"),
    ("node", "contract_correction_identity"), ("wrong-retry", "invalid_retry"),
    ("stale", "stale_checkpoint"),
])
def test_contract_correction_reservation_controls(tmp_path, case, reason):
    client = Client(tmp_path)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh")
    client.call(first)
    client.call(invalid_contract(client, "a"))
    cp, retry = correction_requests(client, first)
    if case == "changed-content":
        retry["input_refs"] = [dict(ref="content", digest=digest("changed"))] + retry["input_refs"][1:]
    if case == "extra-input":
        retry["input_refs"] += [dict(ref="extra", digest=digest("extra"))]
    if case == "wrong-instruction":
        retry["input_refs"] = first["input_refs"] + [dict(ref="other-instruction", digest=digest("other"))]
    if case == "scope":
        retry["scope_digest"] = cp["scope_digest"] = digest("new-scope")
    if case == "dependencies":
        retry["dependency_node_ids"] = [digest("new-dependency")]
    if case == "lane":
        retry["lane"] = "amendment"
    if case == "node":
        retry["node_descriptor"] = dict(retry["node_descriptor"], step_key="other")
        retry["node_id"] = digest(retry["node_descriptor"])
    if case == "wrong-retry":
        retry["retry_of"] = "other"
    retry["input_digest"] = cp["input_digest"] = digest(dict(scope_digest=retry["scope_digest"],
        role=retry["node_descriptor"]["role"], input_refs=sorted(retry["input_refs"], key=lambda r: (r["ref"], r["digest"]))))
    # Scope admission is checked against the invalid attempt at checkpoint time.
    if case == "scope":
        assert client.call(cp, 2)["reasons"] == [reason]
        return
    client.call(cp)
    if case == "stale":
        client.call(client.reserve("intervening", source="intervening"))
    path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    before = path.read_bytes()
    result = client.call(retry, 3 if case == "wrong-retry" else 2)
    assert result["reasons"] == [reason]
    assert path.read_bytes() == before


@pytest.mark.parametrize("outcome", ["valid", "cancelled", "lost", "invalid"])
def test_contract_correction_absent_retains_ordinary_proof_gate(tmp_path, outcome):
    client = Client(tmp_path)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh")
    client.call(first)
    client.call(client.finish(outcome=outcome, contract_ref="contract", contract_digest=digest("contract"),
                              verdict="FINDINGS", review_mode="fresh", reviewed_revision=1))
    cp, retry = correction_requests(client, first)
    del cp["contract_correction"]
    client.call(cp)
    assert client.call(retry, 2)["reasons"] == ["covering_proof_required"]


@pytest.mark.parametrize("eligible", [False, True])
def test_contract_correction_still_requires_eligible_funds(tmp_path, eligible):
    client = Client(tmp_path)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh")
    client.call(first)
    client.call(invalid_contract(client, "a"))
    for n in range(31):
        client.call(client.reserve("work-%s" % n, source="source-%s" % n))
    cp, retry = correction_requests(client, first)
    client.call(cp)
    assert client.call(retry, 2)["reasons"] == ["insufficient_eligible_units"]
    client.call(checkpoint(client, "funds"))
    client.call(grant("funding", "funds", authorization_scope=dict(subject_id="subject-a",
                     lanes=["fresh"] if eligible else ["remediation"], scope_digest=digest("scope"))))
    # A grant after a correction checkpoint makes that checkpoint stale.
    assert client.call(retry, 2)["reasons"] == ["stale_checkpoint"]
    cp, retry = correction_requests(client, first, "funded-correction")
    retry["authorization_checks"] = [dict(grant_id="funding", applicable=True,
        evidence_ref="decision-a", evidence_digest=digest("authority"))]
    client.call(cp)
    result = client.call(retry, 0 if eligible else 2)
    if eligible:
        assert (result["projection"]["charged_units"], result["projection"]["remaining_units"]) == (33, 7)
    else:
        assert result["reasons"] == ["insufficient_eligible_units"]
        assert result["projection"]["remaining_units"] == 8


@pytest.mark.parametrize("case", ["existing-pair-with-metadata", "raw-receipt-as-instruction"])
def test_contract_correction_instruction_is_new_and_separate(tmp_path, case):
    client = Client(tmp_path)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh")
    if case == "existing-pair-with-metadata":
        refs = first["input_refs"] + [dict(ref="contract-instruction-corrected",
            digest=digest("Return required role fields corrected"), input_digest=digest("context"))]
        first = client.reserve(role="plan-gap-reviewer", lane="fresh", input_refs=refs)
    client.call(first)
    client.call(invalid_contract(client, "a"))
    cp, _ = correction_requests(client, first)
    if case == "raw-receipt-as-instruction":
        cp["contract_correction"]["instruction"] = cp["changed_input_refs"][0]
    assert client.call(cp, 2)["reasons"] == ["contract_correction_evidence"]


def test_contract_correction_findings_never_close(tmp_path):
    client = Client(tmp_path, artifact=dict(workflow_uuid="wf-a", plan_revision=1,
                                          planning_review_status="pending"))
    request = client.reserve(role="plan-gap-reviewer", lane="fresh")
    client.call(request)
    client.call(client.finish(outcome="valid", contract_ref="review", contract_digest=digest("review"),
                              verdict="FINDINGS", review_mode="fresh", reviewed_revision=1))
    artifact = json.loads(client.workflow.read_text())
    artifact.update(plan_input_digest=request["input_digest"], planning_review_status="passed")
    client.workflow.write_text(json.dumps(artifact))
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]


def repair_proof(client, attempt="repair"):
    request = client.reserve(attempt, source=attempt, lane="remediation")
    client.call(request)
    evidence = dict(ref="covering-tests", digest=digest("tested-output"), input_digest=request["input_digest"])
    client.call(client.finish(attempt, "valid", contract_ref="repair-contract", contract_digest=digest("repair"),
                              evidence_refs=[evidence]))
    return dict(**evidence, producer_attempt_id=attempt, producer_node_id=request["node_id"], subject_id="subject-a")


@pytest.mark.parametrize("case", ["retained", "missing", "wrong-producer", "stale-digest"])
def test_contract_correction_preserves_covering_proof(tmp_path, case):
    client = Client(tmp_path)
    proof = repair_proof(client)
    first = client.reserve(role="plan-gap-reviewer", lane="fresh", dependency_node_ids=[proof["producer_node_id"]])
    client.call(first)
    client.call(client.finish(outcome="valid", contract_ref="review", contract_digest=digest("review"),
                              verdict="FINDINGS", review_mode="fresh", reviewed_revision=1))
    second = client.reserve("review-two", role="plan-gap-reviewer", lane="fresh", retry_of="a", content="repaired",
                            dependency_node_ids=first["dependency_node_ids"], checkpoint_id="repair-proof")
    client.call(checkpoint(client, "repair-proof", action="continue", input_digest=second["input_digest"], proof_refs=[proof]))
    client.call(second)
    client.call(invalid_contract(client, "review-two"))
    cp, retry = correction_requests(client, second, proof_refs=[dict(proof)])
    if case == "missing":
        cp["proof_refs"] = []
    if case == "wrong-producer":
        cp["proof_refs"][0]["producer_node_id"] = digest("wrong")
    if case == "stale-digest":
        cp["proof_refs"][0]["digest"] = digest("stale")
    if case != "retained":
        reason = {"missing": "covering_proof_required", "wrong-producer": "proof_producer_mismatch",
                  "stale-digest": "stale_or_invalid_proof"}[case]
        assert client.call(cp, 2)["reasons"] == [reason]
    else:
        client.call(cp)
        p = client.call(retry)["projection"]
        assert (p["charged_units"], p["counts"]["fresh_valid"]) == (4, 1)


def legacy_review_client(tmp_path, passed=True):
    artifact = json.loads((SCRIPT.parent.parent / "skills/cc10x-router/references/workflow-artifact.skeleton.json").read_text())
    artifact.update(workflow_uuid="wf-a", workflow_id="wf-a", workflow_type="BUILD", phase_cursor="build-implement",
                    planning_review_runs=3, plan_revision=3,
                    last_reviewed_revision=3, plan_input_digest=None,
                    planning_review_status="passed" if passed else "pending",
                    remediation_history=[dict(cycle_number=i) for i in range(1, 5)])
    return Client(tmp_path, artifact=artifact, initialize=False)


def legacy_replay(client, expected):
    root = SCRIPT.parents[3]
    run = subprocess.run([sys.executable, str(root / "plugins/cc10x/tools/workflow_replay_check.py"),
                          "--artifact", str(client.workflow)], capture_output=True, text=True,
                         env=dict(os.environ, CC10X_REPO_ROOT=str(root)))
    assert run.returncode == expected, run.stdout + run.stderr
    if expected:
        assert "fresh_pass_required" in run.stderr


def legacy_import_request():
    return dict(op="init", lineage_id="lineage-a", subject_id="subject-a",
                migration=dict(coverage="unknown", charged_units=32, source_refs=["review-history", "repair-history"],
                               counts={"subject-a": dict(attempts=7, fresh_valid=3, remediation_attempts=4)}))


def projected_legacy_review(tmp_path):
    # Real migration without closure, then attach the historical passed claim:
    # equivalent to an already-projected ledger from an older CLI version.
    client = legacy_review_client(tmp_path, passed=False)
    client.call(legacy_import_request())
    artifact = json.loads(client.workflow.read_text())
    artifact["planning_review_status"] = "passed"
    client.workflow.write_text(json.dumps(artifact))
    return client


def legacy_review_checkpoint(client, name="review-checkpoint"):
    p = client.call(dict(op="inspect"), 2)["projection"]
    return dict(op="checkpoint", event_id="event-" + name, checkpoint_id=name,
                workflow_uuid="wf-a", subject_id="subject-a", recorded_at="2026-01-01T00:00:02Z",
                action="needs_authorization", observed_revision=p["ledger_revision"],
                scope_digest=digest("scope"), input_digest=digest("input"), finding_ids=[], proof_refs=[],
                changed_input_refs=[dict(ref="current-plan", digest=digest("current-plan"))],
                progress="finite_fix", reopened_ids=[], scope_change="none",
                rationale="Obtain genuine current fresh review", remaining_units=p["remaining_units"])


def legacy_review_grant():
    return grant(checkpoint_id="review-checkpoint", lane_increments={"fresh": 1},
                 authorization_scope=dict(subject_id="subject-a", lanes=["fresh"], scope_digest=digest("scope")))


def funded_legacy_review(client):
    client.call(legacy_review_checkpoint(client))
    client.call(legacy_review_grant())
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    request = client.reserve("fresh-review", role="plan-gap-reviewer", lane="fresh", authorization_checks=checks)
    artifact = json.loads(client.workflow.read_text())
    artifact["plan_input_digest"] = request["input_digest"]
    client.workflow.write_text(json.dumps(artifact))
    client.call(request)
    return request


@pytest.mark.parametrize("correct_contract", [False, True])
def test_legacy_findings_recovery_cli(tmp_path, correct_contract):
    client = legacy_review_client(tmp_path)
    artifact = json.loads(client.workflow.read_text())
    artifact["status_history"] = [dict(event="historical-approval", planning_review_status="passed", plan_revision=3,
                                       evidence_ref="historical-approval")]
    client.workflow.write_text(json.dumps(artifact))
    historical = artifact["status_history"][:]
    result = client.call(legacy_import_request(), 2)
    artifact["review_budget"] = result["projection"]
    client.workflow.write_text(json.dumps(artifact))
    ledger_path = Path(result["projection"]["ledger_path"])
    opening = json.loads(ledger_path.read_text())["opening"]
    first = funded_legacy_review(client)
    if correct_contract:
        client.call(invalid_contract(client, "fresh-review"))
        cp, retry = correction_requests(client, first, pending=True)
        client.call(cp)
        artifact = json.loads(client.workflow.read_text())
        artifact["plan_input_digest"] = retry["input_digest"]
        client.workflow.write_text(json.dumps(artifact))
        client.call(retry)
        # An old-input PASS cannot be attached to the corrected reservation.
        stale = client.finish("corrected", "valid", contract_ref="review", contract_digest=digest("review"),
                              verdict="PASS", review_mode="fresh", reviewed_revision=3,
                              reviewed_input_digest=first["input_digest"])
        assert client.call(stale, 3)["reasons"] == ["review_input_mismatch"]
        first = retry
    finish = client.finish(first["attempt_id"], "valid", contract_ref="current-findings", contract_digest=digest("findings"),
                           verdict="FINDINGS", review_mode="fresh", reviewed_revision=3)
    p = client.call(finish)["projection"]
    assert client.call(finish)["projection"] == p
    # Crash before parent ingestion: accounting is durable, historical closure still fails.
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]
    legacy_replay(client, 1)
    assert client.call(client.reserve("planner", role="planner", source="planner"), 2)["reasons"] == ["fresh_pass_required"]
    artifact = json.loads(client.workflow.read_text())
    artifact.update(planning_review_status="findings_received", planning_review_runs=p["counts"]["fresh_valid"],
                    last_reviewed_revision=3, planning_review_findings=["Synthetic missing requirement"])
    artifact["results"]["planning_reviewer"] = dict(attempt_id=first["attempt_id"], verdict="FINDINGS",
                                                       reviewed_input_digest=first["input_digest"])
    client.workflow.write_text(json.dumps(artifact))
    client.call(dict(op="inspect"))
    legacy_replay(client, 0)
    # Re-ingestion is idempotent: no new finish, history row, count or charge.
    before = ledger_path.read_bytes()
    client.workflow.write_text(json.dumps(artifact))
    assert client.call(finish)["projection"] == p and ledger_path.read_bytes() == before
    assert artifact["status_history"] == historical
    assert artifact["planning_review_status"] == "findings_received"
    assert json.loads(ledger_path.read_text())["opening"] == opening
    assert (p["counts"]["fresh_valid"], p["counts"]["remediation_attempts"], p["charged_units"]) == (4, 4, 34 if correct_contract else 33)
    # Spare fresh-only grant units cannot pay for a planner or repair.
    assert client.call(client.reserve("planner", role="planner", source="planner"), 2)["reasons"] == ["insufficient_eligible_units"]
    client.call(checkpoint(client, "repair-funds"))
    client.call(grant("repair-grant", "repair-funds", lane_increments={"remediation": 1},
                       authorization_scope=dict(subject_id="subject-a", lanes=["work", "remediation"], scope_digest=digest("scope"))))
    checks = [dict(grant_id="repair-grant", applicable=True, evidence_ref="repair-decision", evidence_digest=digest("authority"))]
    client.call(client.reserve("planner", role="planner", source="planner", authorization_checks=checks))
    client.call(client.finish("planner", "valid", contract_ref="revised-plan", contract_digest=digest("revised-plan")))
    repair = client.reserve("repair", source="repair", lane="remediation", authorization_checks=checks)
    client.call(repair)
    evidence = dict(ref="tests", digest=digest("green-output"), input_digest=repair["input_digest"])
    client.call(client.finish("repair", "valid", contract_ref="repair", contract_digest=digest("repair"), evidence_refs=[evidence]))
    artifact = json.loads(client.workflow.read_text())
    artifact.update(planning_review_status="revised_after_review", plan_revision=4)
    client.workflow.write_text(json.dumps(artifact))
    proof = dict(**evidence, producer_attempt_id="repair", producer_node_id=repair["node_id"], subject_id="subject-a")
    client.call(checkpoint(client, "review-funds"))
    client.call(grant("review-grant", "review-funds", additional_units=0, lane_increments={"fresh": 1},
                       authorization_scope=dict(subject_id="subject-a", lanes=["fresh"], scope_digest=digest("scope"))))
    review_checks = [dict(grant_id=g, applicable=True, evidence_ref="review-decision", evidence_digest=digest("authority"))
                     for g in ("g", "review-grant")]
    review = client.reserve("final-review", role="plan-gap-reviewer", lane="fresh", content="revised-plan",
                            retry_of=first["attempt_id"], checkpoint_id="final-proof", dependency_node_ids=[repair["node_id"]],
                            authorization_checks=review_checks)
    client.call(checkpoint(client, "final-proof", action="continue", input_digest=review["input_digest"], proof_refs=[proof]))
    artifact = json.loads(client.workflow.read_text())
    artifact["plan_input_digest"] = review["input_digest"]
    client.workflow.write_text(json.dumps(artifact))
    client.call(review)
    # FINDINGS/historical approval cannot be relabeled as current approval.
    artifact = json.loads(client.workflow.read_text())
    artifact["planning_review_status"] = "passed"
    client.workflow.write_text(json.dumps(artifact))
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]
    client.call(client.finish("final-review", "valid", contract_ref="final-pass", contract_digest=digest("pass"),
                              verdict="PASS", review_mode="fresh", reviewed_revision=4))
    client.call(dict(op="inspect"))
    legacy_replay(client, 0)
    final = json.loads(client.workflow.read_text())
    assert final["status_history"] == historical
    assert final["review_budget"]["charged_units"] == (40 if correct_contract else 39)
    assert final["review_budget"]["counts"]["remediation_attempts"] == 5


def test_legacy_closure_migration_reports_pending_proof_and_recovers_projection(tmp_path):
    client = legacy_review_client(tmp_path)
    original = client.workflow.read_bytes()
    result = client.call(legacy_import_request(), 2)
    assert result["reasons"] == ["fresh_pass_required"]
    p = result["projection"]
    assert (p["counts"]["fresh_valid"], p["counts"]["remediation_attempts"], p["charged_units"], p["remaining_units"]) == (3, 4, 32, 0)
    path = Path(p["ledger_path"])
    before = path.read_bytes()
    assert json.loads(before)["events"] == [] and client.workflow.read_bytes() == original
    recovered = client.call(dict(op="init", lineage_id="lineage-a", subject_id="subject-a"), 2)
    assert recovered["projection"] == p and path.read_bytes() == before
    artifact = json.loads(original)
    artifact["review_budget"] = p
    client.workflow.write_text(json.dumps(artifact))
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]
    legacy_replay(client, 1)
    assert client.call(client.reserve("work"), 2)["reasons"] == ["fresh_pass_required"]
    assert client.call(client.reserve("review", role="plan-gap-reviewer", lane="fresh"), 2)["reasons"] == ["insufficient_eligible_units"]
    assert path.read_bytes() == before


@pytest.mark.parametrize("prior_digest", [None, "known"])
def test_legacy_closure_genuine_funded_fresh_review_unlocks_without_reset(tmp_path, prior_digest):
    import cc10x_review_budget as budget
    client = projected_legacy_review(tmp_path)
    artifact = json.loads(client.workflow.read_text())
    artifact["plan_input_digest"] = digest(prior_digest) if prior_digest else None
    client.workflow.write_text(json.dumps(artifact))
    history = artifact["remediation_history"]
    legacy_replay(client, 1)
    request = funded_legacy_review(client)
    client.call(client.finish("fresh-review", "valid", contract_ref="fresh-contract", contract_digest=digest("contract"),
                              verdict="PASS", review_mode="fresh", reviewed_revision=3))
    p = client.call(dict(op="inspect"))["projection"]
    assert (p["counts"]["attempts"], p["counts"]["fresh_valid"], p["counts"]["remediation_attempts"], p["charged_units"], p["remaining_units"]) == (8, 4, 4, 33, 7)
    artifact = json.loads(client.workflow.read_text())
    ledger = json.loads(Path(p["ledger_path"]).read_text())
    assert artifact["planning_review_status"] == "passed" and artifact["remediation_history"] == history
    assert ledger["opening"]["charged_units"] == 32 and ledger["opening"]["coverage"] == "unknown"
    assert budget.validate_budget_projection(artifact, ledger) == []
    legacy_replay(client, 0)
    source = client.workflow
    client.workflow = source.with_name("wf-b.json")
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b")))
    assert client.call(dict(op="join", source_workflow=str(source)))["projection"]["charged_units"] == 33
    client.workflow = source
    client.call(dict(op="reconcile"))
    artifact = json.loads(source.read_text())
    artifact["plan_input_digest"] = digest("changed-input")
    source.write_text(json.dumps(artifact))
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]
    legacy_replay(client, 1)
    artifact["plan_input_digest"] = request["input_digest"]
    artifact["plan_revision"] = 4
    source.write_text(json.dumps(artifact))
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["fresh_pass_required"]


def test_legacy_closure_stale_reconcile_retains_pending_proof(tmp_path):
    client = projected_legacy_review(tmp_path)
    client.call(legacy_review_checkpoint(client), project=False)
    result = client.call(dict(op="reconcile"), 2)
    assert result["reasons"] == ["fresh_pass_required"] and result["projection"]["ledger_revision"] == 2


@pytest.mark.parametrize("side", ["source", "destination"])
def test_legacy_closure_stale_join_cannot_hide_missing_fresh_proof(tmp_path, side):
    client = projected_legacy_review(tmp_path) if side == "source" else Client(tmp_path)
    source = client.workflow
    destination = source.with_name("wf-b.json")
    destination.write_text(json.dumps(dict(workflow_uuid="wf-b")))
    if side == "source":
        client.call(legacy_review_checkpoint(client), project=False)
    else:
        client.workflow = destination
        client.call(dict(op="join", source_workflow=str(source)))
        artifact = json.loads(destination.read_text())
        artifact.update(planning_review_status="passed", plan_revision=3, last_reviewed_revision=3)
        destination.write_text(json.dumps(artifact))
        client.workflow = source
        client.call(dict(op="reconcile"))
        client.call(client.reserve())
    path = Path(json.loads(source.read_text())["review_budget"]["ledger_path"])
    before = path.read_bytes()
    client.workflow = destination
    rejected = client.call(dict(op="join", source_workflow=str(source)), 2)
    assert rejected["reasons"] == ["invalid_source" if side == "source" else "accounting_conflict"]
    assert path.read_bytes() == before


@pytest.mark.parametrize("case", ["work", "amendment", "mixed-grant", "foreign-receipt", "foreign-subject"])
def test_legacy_closure_repair_path_rejects_other_work_or_conflicts(tmp_path, case):
    client = projected_legacy_review(tmp_path)
    p = client.call(dict(op="inspect"), 2)["projection"]
    path = Path(p["ledger_path"])
    before = path.read_bytes()
    if case == "mixed-grant":
        request = legacy_review_grant()
        request["authorization_scope"]["lanes"].append("work")
    elif case in ("foreign-receipt", "foreign-subject"):
        request = legacy_review_checkpoint(client)
        if case == "foreign-receipt":
            client.workflow.with_suffix(".events.jsonl").write_text(json.dumps(dict(event="attempt_reserved", attempt_id="unknown")) + "\n")
        else:
            request["subject_id"] = "other-subject"
    else:
        request = client.reserve("wrong", role="plan-gap-reviewer" if case == "amendment" else "component-builder",
                                 lane="amendment" if case == "amendment" else "work")
    result = client.call(request, 3 if case == "foreign-subject" else 2)
    assert result.get("dispatch") != "new" and path.read_bytes() == before


@pytest.mark.parametrize("outcome,verdict,revision", [("invalid", None, None), ("valid", "FINDINGS", 3), ("valid", "PASS", 2)])
def test_legacy_closure_noncurrent_or_failed_fresh_result_never_closes(tmp_path, outcome, verdict, revision):
    client = projected_legacy_review(tmp_path)
    funded_legacy_review(client)
    finish = client.finish("fresh-review", outcome)
    if outcome == "valid":
        finish.update(contract_ref="fresh-contract", contract_digest=digest("contract"), verdict=verdict,
                      review_mode="fresh", reviewed_revision=revision)
    client.call(finish)
    result = client.call(dict(op="inspect"), 2)
    assert result["reasons"] == ["fresh_pass_required"] and result["projection"]["charged_units"] == 33
    source = client.workflow
    client.workflow = source.with_name("wf-b.json")
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b")))
    assert client.call(dict(op="join", source_workflow=str(source)), 2)["reasons"] == ["invalid_source"]


def test_legacy_closure_no_migration_provenance_does_not_enable_repair_gate(tmp_path):
    client = Client(tmp_path)
    artifact = json.loads(client.workflow.read_text())
    artifact.update(planning_review_status="passed", plan_revision=3, last_reviewed_revision=3)
    client.workflow.write_text(json.dumps(artifact))
    assert client.call(legacy_review_checkpoint(client), 2)["reasons"] == ["fresh_pass_required"]


def test_reservations_charge_invalid_work_and_replay_once(tmp_path):
    client = Client(tmp_path)
    first = client.call(client.reserve())
    assert first["projection"]["charged_units"] == 1
    replay = client.call(client.reserve())
    assert replay["ledger_revision"] == first["ledger_revision"]
    client.call(client.finish())
    result = client.call(dict(op="inspect"))
    assert result["projection"]["counts"]["attempts"] == 1
    assert result["projection"]["charged_units"] == 1
    client.call(client.finish("unknown"), 3)
    client.call(client.reserve(input_digest=digest("different")), 3)


def test_crash_requires_projection_reconciliation(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve(), project=False)
    client.call(client.reserve("b", source="source-b"), 2)
    result = client.call(dict(op="reconcile"))
    assert result["projection"]["charged_units"] == 1
    client.call(client.reserve("b", source="source-b"))


def test_siblings_hold_distinct_nodes_but_renamed_retry_is_blocked(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve("a", source="source-a"))
    client.call(client.reserve("b", source="source-b"))
    result = client.call(client.reserve("renamed", source="source-a"), 2)
    assert "node_unresolved" in result["reasons"]
    client.call(client.finish("a"))
    client.call(checkpoint(client, action="continue", input_digest=client.reserve(source="source-a")["input_digest"]))
    result = client.call(client.reserve("renamed", source="source-a", retry_of="a", checkpoint_id="c"), 2)
    assert "unchanged_input" in result["reasons"]


def test_planner_cost_and_default_exhaustion(tmp_path):
    client = Client(tmp_path)
    for index in range(8):
        client.call(client.reserve(str(index), role="planner", source="source-" + str(index)))
    result = client.call(client.reserve("overflow", source="new"), 2)
    assert "insufficient_eligible_units" in result["reasons"]
    assert result["projection"]["charged_units"] == 32
    client.call(client.finish("0", outcome="lost"))
    assert client.call(dict(op="inspect"))["projection"]["remaining_units"] == 0


def checkpoint(client, name="c", **changes):
    revision = client.call(dict(op="inspect"))["ledger_revision"]
    value = dict(op="checkpoint", event_id=name, checkpoint_id=name, workflow_uuid="wf-a",
                 subject_id="subject-a", recorded_at="2026-01-01T00:00:02Z",
                 action="needs_authorization", observed_revision=revision,
                 scope_digest=digest("scope"), input_digest=digest("input"), finding_ids=[],
                 proof_refs=[], changed_input_refs=[dict(ref="diagnostic", digest=digest(name))],
                 progress="finite_fix", reopened_ids=[], scope_change="none", rationale="Finite repair",
                 remaining_units=client.call(dict(op="inspect"))["projection"]["remaining_units"])
    value.update(changes)
    return value


def grant(name="g", checkpoint_id="c", **changes):
    value = dict(op="extend", event_id=name, grant_id=name, workflow_uuid="wf-a", subject_id="subject-a",
                 recorded_at="2026-01-01T00:00:03Z", authorization_id="authority-a",
                 authorization_kind="standing", authorization_ref="decision-a", checkpoint_id=checkpoint_id,
                 authorization_scope=dict(subject_id="subject-a", lanes=["remediation"], scope_digest=digest("scope")),
                 additional_units=8, lane_increments={})
    value.update(changes)
    return value


def test_scoped_grants_preserve_aggregate_but_cannot_fund_other_lanes(tmp_path):
    client = Client(tmp_path)
    for index in range(8):
        client.call(client.reserve(str(index), role="planner", source="source-" + str(index)))
    client.call(checkpoint(client))
    result = client.call(grant())
    assert result["projection"]["remaining_units"] == 8
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    result = client.call(client.reserve("wrong", source="wrong", authorization_checks=checks), 2)
    assert result["projection"]["remaining_units"] == 8
    assert "insufficient_eligible_units" in result["reasons"]
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    result = client.call(client.reserve("repair", source="repair", lane="remediation", authorization_checks=checks))
    assert result["projection"]["charged_units"] == 33
    assert result["projection"]["remaining_units"] == 7
    revision = result["ledger_revision"]
    assert client.call(grant(event_id="transport-replay"))["ledger_revision"] == revision
    client.call(checkpoint(client, "c2"))
    assert client.call(grant("g2", "c2"))["projection"]["remaining_units"] == 15
    client.call(grant("g3", "c2"), 2)


def test_review_slots_release_only_on_invalid_completion(tmp_path):
    client = Client(tmp_path)
    for name in ("a", "b"):
        client.call(client.reserve(name, role="plan-gap-reviewer", source=name, lane="fresh"))
    client.call(client.reserve("c", role="plan-gap-reviewer", source="c", lane="fresh"), 2)
    client.call(client.finish("a"))
    client.call(client.reserve("c", role="plan-gap-reviewer", source="c", lane="fresh"))
    client.call(client.finish("b", "valid", contract_ref="contract-b", contract_digest=digest("contract"),
                              verdict="FINDINGS", review_mode="fresh", reviewed_revision=1))
    result = client.call(dict(op="inspect"))
    assert result["projection"]["counts"]["fresh_valid"] == 1
    assert result["projection"]["charged_units"] == 3
    client.call(client.reserve("d", role="plan-gap-reviewer", source="d", lane="fresh"), 2)


def test_join_cross_root_preserves_ledger_and_event_sequence(tmp_path):
    client = Client(tmp_path / "first")
    client.call(client.reserve())
    source = client.workflow
    original = json.loads(source.read_text())["review_budget"]["ledger_path"]
    client.root = tmp_path / "second" / ".cc10x"
    client.workflow = client.root / "workflows" / "wf-b.json"
    client.workflow.parent.mkdir(parents=True)
    client.workflow.write_text(json.dumps({"workflow_uuid": "wf-b"}))
    result = client.call(dict(op="join", source_workflow=str(source)))
    assert result["ledger_revision"] == 3
    assert result["projection"]["ledger_path"] == original
    result = client.call(dict(op="join", source_workflow=str(source)))
    assert result["ledger_revision"] == 3
    client.call(client.finish(workflow_uuid="wf-b"))
    ledger = json.loads(Path(original).read_text())
    assert (ledger["revision"], ledger["event_count"]) == (4, 2)
    assert [e["seq"] for e in ledger["events"]] == [1, 2]


def test_legacy_unknown_history_does_not_mint_allowance(tmp_path):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps({"workflow_uuid": "wf-legacy", "planning_review_runs": 1}))
    result = client.call(dict(op="init", lineage_id="legacy", subject_id="subject-a"), 2, project=False)
    assert "migration_required" in result["reasons"]
    result = client.call(dict(op="init", lineage_id="legacy", subject_id="subject-a",
                             migration=dict(coverage="unknown", source_refs=["history"], counts={}, charged_units=0)))
    assert result["projection"]["charged_units"] == 32
    assert result["projection"]["remaining_units"] == 0


def test_final_unit_concurrency_cannot_overspend(tmp_path):
    client = Client(tmp_path)
    for index in range(31):
        client.call(client.reserve(str(index), source="s-" + str(index)))
    requests = []
    for index in range(2):
        path = tmp_path / ("race-%s.json" % index)
        path.write_text(json.dumps(client.reserve("race-" + str(index), source="race-" + str(index))))
        requests.append(path)
    def invoke(path):
        return subprocess.run([sys.executable, str(SCRIPT), "--state-root", str(client.root),
                               "--workflow", str(client.workflow), "--request", str(path)],
                              capture_output=True, text=True).returncode
    with ThreadPoolExecutor(2) as pool:
        assert sorted(pool.map(invoke, requests)) == [0, 2]
    result = client.call(dict(op="reconcile"))
    assert result["projection"]["charged_units"] == 32


def test_stored_funding_tamper_is_rejected(tmp_path):
    client = Client(tmp_path)
    result = client.call(client.reserve())
    path = Path(result["projection"]["ledger_path"])
    ledger = json.loads(path.read_text())
    ledger["events"][0]["funding"][0]["units"] = 0
    path.write_text(json.dumps(ledger))
    client.call(dict(op="inspect"), 3)


def test_changed_retry_requires_matching_checkpoint_and_producer(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve("producer", source="producer"))
    producer = client.reserve("producer", source="producer")
    evidence = dict(ref="test-output", digest=digest("passed"), input_digest=digest("input"))
    client.call(client.finish("producer", "valid", contract_ref="contract", contract_digest=digest("contract"), evidence_refs=[evidence]))
    client.call(client.reserve("a", source="consumer"))
    client.call(client.finish("a"))
    proof = dict(**evidence, producer_attempt_id="producer", producer_node_id=producer["node_id"], subject_id="subject-a")
    request = client.reserve("retry", source="consumer", retry_of="a", content="changed",
                             checkpoint_id="c", dependency_node_ids=[producer["node_id"]])
    client.call(checkpoint(client, action="continue", input_digest=request["input_digest"], proof_refs=[proof]))
    result = client.call(request)
    assert result["projection"]["charged_units"] == 3


def test_amendment_pass_cannot_establish_whole_plan_closure(tmp_path):
    import cc10x_review_budget as budget
    client = Client(tmp_path)
    client.call(client.reserve(role="plan-gap-reviewer", lane="amendment"))
    result = client.call(client.finish(outcome="valid", contract_ref="contract", contract_digest=digest("contract"),
                                      verdict="PASS", review_mode="amendment", reviewed_revision=2))
    artifact = json.loads(client.workflow.read_text())
    artifact.update(planning_review_status="passed", plan_revision=2, last_reviewed_revision=2,
                    plan_input_digest=client.reservations["a"]["input_digest"])
    ledger = json.loads(Path(result["projection"]["ledger_path"]).read_text())
    assert "fresh_pass_required" in budget.validate_budget_projection(artifact, ledger)


def test_finding_alias_keeps_identity_and_upheld_requires_new_evidence(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve())
    finding = dict(op="finding", event_id="f1", workflow_uuid="wf-a", subject_id="subject-a",
                   recorded_at="2026-01-01T00:00:04Z", finding_id="finding-a", source_attempt_id="a",
                   invariant="no-refund", surface="ledger", summary="Charges persist", state="open", proof_refs=[], alias_of=None)
    client.call(finding)
    client.call(dict(finding, event_id="f2", finding_id="alias-a", alias_of="finding-a", summary="Retain charge"))
    client.call(dict(finding, event_id="f3", state="upheld"))
    client.call(dict(finding, event_id="f4", state="reopened"), 2)


def test_real_artifact_replay_diagnoses_budget_conflict(tmp_path):
    client = Client(tmp_path)
    root = SCRIPT.parents[3]
    skeleton = root / "plugins/cc10x/skills/cc10x-router/references/workflow-artifact.skeleton.json"
    artifact = json.loads(skeleton.read_text())
    artifact.update(json.loads(client.workflow.read_text()))
    artifact.update(workflow_id="wf-a", workflow_type="BUILD", phase_cursor="build-implement")
    client.workflow.write_text(json.dumps(artifact))
    tool = root / "plugins/cc10x/tools/workflow_replay_check.py"
    run = subprocess.run([sys.executable, str(tool), "--artifact", str(client.workflow)], capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    artifact["review_budget"]["charged_units"] = 99
    client.workflow.write_text(json.dumps(artifact))
    run = subprocess.run([sys.executable, str(tool), "--artifact", str(client.workflow)], capture_output=True, text=True)
    assert run.returncode == 1, "Replay accepted a contradictory budget"
    assert "budget" in run.stderr


def test_guard_audits_budget_conflict_without_new_blocking(tmp_path):
    from test_cc10x_guards import run_guard, write_artifact
    path = write_artifact(tmp_path, review_budget={"version": 1})
    for tool, payload in (("Write", {"file_path": str(path)}),
                          ("Write", {"file_path": str(tmp_path / "unrelated.txt")}),
                          ("Bash", {"command": "touch .cc10x/workflows/wf-test.json"})):
        result = run_guard("cc10x_posttooluse_artifact_guard.py", {"tool_name": tool, "tool_input": payload}, tmp_path)
        assert result.returncode == 0, result.stderr
    log = (tmp_path / ".cc10x/cc10x-hook-events.log").read_text()
    assert "review-budget:" in log


@pytest.mark.parametrize("field,value", [("attempt_id", ""), ("input_digest", "not-a-digest"),
                                        ("input_refs", []), ("recorded_at", ""),
                                        ("authorization_checks", [{"grant_id": "g", "applicable": 1}]),
                                        ("dependency_node_ids", ["bad"]), ("finding_ids", ["same", "same"])])
def test_malformed_reservation_cannot_write_state(tmp_path, field, value):
    client = Client(tmp_path)
    before = client.call(dict(op="inspect"))["ledger_revision"]
    client.call(client.reserve(**{field: value}), 3)
    assert client.call(dict(op="inspect"))["ledger_revision"] == before


def test_invalid_measurements_are_not_zero_cost_observations(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve())
    client.call(client.finish(measurement=dict(availability="known", tokens=True, agent_seconds=-1, source=None)), 3)


def test_router_routes_share_budget_contract_and_persist_inline_iterations():
    plugin = SCRIPT.parent.parent
    router = plugin / "skills/cc10x-router"
    for path in [router / "SKILL.md"] + [router / "references" / (name + "-workflow.md") for name in ("plan", "build", "debug", "review", "qa")]:
        assert "review-budget.md" in path.read_text(), str(path)
    gate = (plugin / "skills/plan-review-gate/SKILL.md").read_text()
    assert "SPEC_GATE_ATTEMPT_ID" in gate
    assert "SPEC_GATE_ITERATIONS_USED" in gate
    assert "counter resets to 0" not in gate
    assert "uncapped" not in (plugin / "agents/plan-gap-reviewer.md").read_text()


def test_transport_replay_of_attempt_keeps_original_funding(tmp_path):
    client = Client(tmp_path)
    first = client.call(client.reserve())
    replay = client.call(client.reserve(event_id="new-transport"))
    assert replay["ledger_revision"] == first["ledger_revision"]
    assert replay["dispatch"] == "resume"


def test_higher_mirror_is_conflict_not_repairable_staleness(tmp_path):
    client = Client(tmp_path)
    artifact = json.loads(client.workflow.read_text())
    artifact["review_budget"]["charged_units"] = 100
    client.workflow.write_text(json.dumps(artifact))
    result = client.call(dict(op="reconcile"), 2)
    assert result["reasons"] == ["accounting_conflict"]


def test_mixed_base_grant_and_lane_only_are_independent(tmp_path):
    client = Client(tmp_path)
    for index in range(31):
        client.call(client.reserve(str(index), source="source-" + str(index)))
    client.call(checkpoint(client))
    client.call(grant())
    result = client.call(client.reserve("planner", role="planner", source="planner"), 2)
    assert result["eligible_units"] == 1
    client.call(client.reserve("last-base", source="last-base"))
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    client.call(client.reserve("repair", lane="remediation", source="repair", authorization_checks=checks))
    client.call(client.reserve("child", source="child", parent_attempt_id="repair", authorization_checks=checks), 2)


def test_fifth_code_review_requires_lane_credit_without_extra_units(tmp_path):
    client = Client(tmp_path)
    for index in range(4):
        name = str(index)
        client.call(client.reserve(name, role="code-reviewer", source=name, lane="code_review"))
        client.call(client.finish(name, "valid", contract_ref="contract", contract_digest=digest("contract"),
                                  verdict="APPROVE"))
    client.call(client.reserve("fifth", role="code-reviewer", source="fifth", lane="code_review"), 2)
    client.call(checkpoint(client))
    scope = dict(subject_id="subject-a", lanes=["code_review"], scope_digest=digest("scope"))
    client.call(grant(additional_units=0, lane_increments={"code_review": 1}, authorization_scope=scope))
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    result = client.call(client.reserve("fifth", role="code-reviewer", source="fifth", lane="code_review", authorization_checks=checks))
    assert result["projection"]["charged_units"] == 5
    assert result["projection"]["remaining_units"] == 27


@pytest.mark.parametrize("needle,replacement,scenario", [
    ('event["reserved_units"], event["funding"] = units, funding',
     'event["reserved_units"], event["funding"] = 0, funding', 'reservations_charge_invalid'),
    ('if event["input_digest"] == prior["input_digest"]:', 'if False:', 'siblings_hold_distinct'),
    ('e["review_mode"] == "fresh"', 'e["review_mode"] in ("fresh", "amendment")', 'amendment_pass_cannot'),
    ('and event["lane"] in scope["lanes"]', 'and True', 'scoped_grants_preserve'),
    ('history = [e for e in reserved if e["node_id"] == event["node_id"]]',
     'history = [e for e in reserved if e["phase_id"] == event["phase_id"]]', 'siblings_hold_distinct'),
    ('if finish is None or finish["outcome"] != "invalid":', 'if finish is None:',
     'contract_correction_checkpoint_controls and valid-contract_correction_outcome'),
    ('if any(proof not in checkpoint["proof_refs"] for proof in inherited):', 'if False:',
     'contract_correction_preserves_covering_proof and missing'),
    ('e["verdict"] == "PASS"', 'e["verdict"] in ("PASS", "FINDINGS")',
     'contract_correction_findings_never_close'),
])
def test_negative_controls_falsify_distinct_budget_claims(tmp_path, needle, replacement, scenario):
    source = SCRIPT.read_text()
    assert source.count(needle) == 1
    (tmp_path / SCRIPT.name).write_text(source.replace(needle, replacement))
    shutil.copy2(SCRIPT.with_name("cc10x_hooklib.py"), tmp_path)
    shutil.copy2(Path(__file__), tmp_path)
    run = subprocess.run([sys.executable, "-m", "pytest", str(tmp_path / Path(__file__).name),
                          "-q", "-k", "(%s) and not negative_controls" % scenario],
                         capture_output=True, text=True, cwd=tmp_path, timeout=60)
    assert run.returncode == 1, run.stdout + run.stderr
    assert "AssertionError" in run.stdout and "ERROR collecting" not in run.stdout, run.stdout


def test_unledgered_attempt_in_event_log_blocks_dispatch(tmp_path):
    client = Client(tmp_path)
    log = client.workflow.with_suffix(".events.jsonl")
    log.write_text(json.dumps(dict(event="attempt_reserved", wf="wf-a", attempt_id="unrecorded")) + "\n")
    result = client.call(client.reserve(), 2)
    assert "accounting_conflict" in result["reasons"]


def test_mixed_eligible_planner_funding_is_base_first(tmp_path):
    client = Client(tmp_path)
    for index in range(31):
        client.call(client.reserve(str(index), source="source-" + str(index)))
    client.call(checkpoint(client))
    scope = dict(subject_id="subject-a", lanes=["work"], scope_digest=digest("scope"))
    client.call(grant(authorization_scope=scope))
    checks = [dict(grant_id="g", applicable=True, evidence_ref="decision-a", evidence_digest=digest("authority"))]
    result = client.call(client.reserve("planner", role="planner", source="planner", authorization_checks=checks))
    assert result["reservation"]["funding"] == [dict(source="base", grant_id=None, units=1), dict(source="grant", grant_id="g", units=3)]
    assert result["projection"]["charged_units"] == 35


def test_proof_wrong_producer_and_undeclared_sibling_fail(tmp_path):
    client = Client(tmp_path)
    producer = client.reserve("producer", source="producer")
    client.call(producer)
    evidence = dict(ref="test", digest=digest("test"), input_digest=digest("input"))
    client.call(client.finish("producer", "valid", contract_ref="contract", contract_digest=digest("contract"), evidence_refs=[evidence]))
    proof = dict(**evidence, producer_attempt_id="producer", producer_node_id=digest("wrong"), subject_id="subject-a")
    client.call(checkpoint(client, action="continue", proof_refs=[proof]), 2)
    proof["producer_node_id"] = producer["node_id"]
    client.call(client.reserve("a", source="consumer"))
    client.call(client.finish())
    request = client.reserve("retry", source="consumer", retry_of="a", content="changed", checkpoint_id="c")
    client.call(checkpoint(client, action="continue", input_digest=request["input_digest"], proof_refs=[proof]))
    result = client.call(request, 2)
    assert "undeclared_proof_dependency" in result["reasons"]


def test_unsubstantiated_input_digest_cannot_authorize_retry(tmp_path):
    client = Client(tmp_path)
    client.call(client.reserve())
    client.call(client.finish())
    client.call(checkpoint(client, action="continue", input_digest=digest("invented")))
    client.call(client.reserve("retry", retry_of="a", checkpoint_id="c", input_digest=digest("invented")), 3)


def test_different_subject_join_cannot_inherit_grant(tmp_path):
    client = Client(tmp_path / "first")
    for index in range(8):
        client.call(client.reserve(str(index), role="planner", source="s-" + str(index)))
    client.call(checkpoint(client))
    client.call(grant())
    source = client.workflow
    client.root = tmp_path / "second" / ".cc10x"
    client.workflow = client.root / "workflows/wf-b.json"
    client.workflow.parent.mkdir(parents=True)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b")))
    result = client.call(dict(op="join", source_workflow=str(source), subject_id="subject-b",
                             subject_rationale=dict(ref="approved-scope", digest=digest("scope-b"))))
    assert result["projection"]["subject_id"] == "subject-b"
    request = client.reserve("b", lane="remediation", workflow_uuid="wf-b", subject_id="subject-b")
    request["node_descriptor"]["subject_id"] = "subject-b"
    request["node_id"] = digest(request["node_descriptor"])
    request["authorization_checks"] = [dict(grant_id="g", applicable=True, evidence_ref="decision", evidence_digest=digest("decision"))]
    result = client.call(request, 2)
    assert result["eligible_units"] == 0
    assert result["projection"]["remaining_units"] == 8


def test_symlink_state_root_retains_canonical_ledger(tmp_path):
    client = Client(tmp_path / "actual")
    original = client.call(dict(op="inspect"))["projection"]["ledger_path"]
    link = tmp_path / "linked-state"
    link.symlink_to(client.root, target_is_directory=True)
    client.root, client.workflow = link, link / "workflows/wf-a.json"
    result = client.call(client.reserve())
    assert result["projection"]["ledger_path"] == original


def test_lock_contention_has_finite_stop(tmp_path):
    import fcntl
    client = Client(tmp_path)
    path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    with path.with_suffix(".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        result = client.call(client.reserve(), 2)
        assert result["reasons"] == ["lock_contention"]


@pytest.mark.parametrize("change", [dict(contract_digest="bad"), dict(review_mode="fresh"), dict(spec_gate_iterations=1)])
def test_code_review_finish_cannot_claim_wrong_contract_or_inline_work(tmp_path, change):
    client = Client(tmp_path)
    client.call(client.reserve(role="code-reviewer", lane="code_review"))
    request = client.finish(outcome="valid", contract_ref="contract", contract_digest=digest("contract"), verdict="APPROVE")
    request.update(change)
    client.call(request, 3)


def test_complete_legacy_migration_preserves_corroborated_counts(tmp_path):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-old", planning_review_runs=1)))
    result = client.call(dict(op="init", lineage_id="old", subject_id="subject-a",
                             migration=dict(coverage="complete", source_refs=["old-results"], charged_units=5,
                                            counts={"subject-a": dict(attempts=2, fresh_valid=1)})))
    assert result["projection"]["remaining_units"] == 27
    assert result["projection"]["counts"]["fresh_valid"] == 1
    client.call(dict(op="inspect"))


@pytest.mark.parametrize("failure", ["mkstemp", "dump", "fsync", "replace", "after_replace"])
def test_remfix_failed_persistence_never_authorizes_dispatch(tmp_path, monkeypatch, capsys, failure):
    import cc10x_review_budget as budget
    client = Client(tmp_path)
    path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    before = path.read_bytes()
    request = tmp_path / "reserve.json"
    request.write_text(json.dumps(client.reserve()))
    owner, name = {"mkstemp": (budget.tempfile, "mkstemp"), "dump": (budget.json, "dump"),
                   "fsync": (budget.os, "fsync"), "replace": (budget.os, "replace"),
                   "after_replace": (budget.os, "replace")}[failure]
    original = getattr(owner, name)
    def fail(*args, **kwargs):
        if failure == "after_replace":
            original(*args, **kwargs)
        if failure == "dump":
            args[1].write('{"partial":')
            raise ValueError("synthetic serialization failure")
        raise OSError("synthetic persistence failure")
    with monkeypatch.context() as patch:
        patch.setattr(owner, name, fail)
        code = budget.main(["--state-root", str(client.root), "--workflow", str(client.workflow), "--request", str(request)])
    result = json.loads(capsys.readouterr().out)
    assert code == 3 and result["status"] == "invalid", result
    assert result.get("dispatch") is None and result.get("reservation") is None
    assert not list(path.parent.glob(".budget-*"))
    if failure == "after_replace":
        recovered = client.call(dict(op="reconcile"))
        assert recovered["projection"]["charged_units"] == 1
        assert client.call(client.reserve())["dispatch"] == "resume"
    else:
        assert path.read_bytes() == before
        assert client.call(client.reserve())["dispatch"] == "new"


def test_remfix_canonical_skeleton_initializes_without_legacy_migration(tmp_path):
    client = Client(tmp_path)
    skeleton = SCRIPT.parent.parent / "skills/cc10x-router/references/workflow-artifact.skeleton.json"
    artifact = json.loads(skeleton.read_text())
    artifact.update(workflow_uuid="wf-a", workflow_id="wf-a")
    client.workflow.write_text(json.dumps(artifact))
    result = client.call(dict(op="init", lineage_id="fresh-skeleton", subject_id="subject-a"))
    assert result["projection"]["remaining_units"] == 32
    artifact = dict(artifact, results={"research": {"web": {"contract_ref": "completed-research"}}})
    client.workflow.write_text(json.dumps(artifact))
    client.call(dict(op="init", lineage_id="real-history", subject_id="subject-a"), 2)


@pytest.mark.parametrize("corrupt", [False, True])
def test_remfix_join_checks_source_event_evidence(tmp_path, corrupt):
    client = Client(tmp_path)
    source = client.workflow
    ledger_path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    before = ledger_path.read_bytes()
    source.with_suffix(".events.jsonl").write_text("{" if corrupt else json.dumps(dict(event="attempt_reserved", attempt_id="unrecorded")) + "\n")
    client.workflow = source.with_name("wf-b.json")
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b")))
    client.call(dict(op="join", source_workflow=str(source)), 3 if corrupt else 2)
    assert ledger_path.read_bytes() == before


@pytest.mark.parametrize("evidence_source", ["history", "events", "status_history", "both"])
def test_remfix_migration_rejects_lower_history_and_deduplicates_rounds(tmp_path, evidence_source):
    client = Client(tmp_path)
    history = [dict(cycle_number=i, phase="build-review", reason="repair") for i in range(1, 4)]
    artifact = dict(workflow_uuid="wf-a")
    if evidence_source == "history":
        artifact["remediation_history"] = history + [history[0]]
    elif evidence_source == "status_history":
        artifact["status_history"] = [dict(event="remediation_created", details=row) for row in history + [history[0]]]
    else:
        client.workflow.with_suffix(".events.jsonl").write_text("\n".join(json.dumps(dict(event="remediation_created", details=row)) for row in history + [history[0]]) + "\n")
        if evidence_source == "both":
            artifact["remediation_history"] = history
    client.workflow.write_text(json.dumps(artifact))
    opening = dict(coverage="complete", charged_units=0, counts={}, source_refs=[evidence_source])
    request = dict(op="init", lineage_id="imported", subject_id="subject-a", migration=opening)
    client.call(request, 2)
    assert not (client.root / "budgets/imported.json").exists()
    opening.update(charged_units=3, counts={"subject-a": {"attempts": 3, "remediation_attempts": 3}})
    result = client.call(request)
    assert result["projection"]["counts"]["remediation_attempts"] == 3
    assert result["projection"]["charged_units"] == 3
    client.call(dict(op="inspect"))


def test_remfix_imported_attempt_evidence_does_not_hide_later_conflicts(tmp_path):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-a")))
    log = client.workflow.with_suffix(".events.jsonl")
    old = dict(event="attempt_reserved", attempt_id="old", role="planner")
    log.write_text(json.dumps(old) + "\n" + json.dumps(old) + "\n")
    request = dict(op="init", lineage_id="imported", subject_id="subject-a",
                   migration=dict(coverage="complete", charged_units=0, counts={}, source_refs=["events"]))
    client.call(request, 2)
    request["migration"].update(charged_units=4, counts={"subject-a": {"attempts": 1}})
    result = client.call(request)
    assert result["projection"]["charged_units"] == 4
    client.call(dict(op="inspect"))
    with log.open("a") as handle:
        handle.write(json.dumps(dict(event="attempt_reserved", attempt_id="new")) + "\n")
    client.call(dict(op="inspect"), 2)


def test_remfix_join_cannot_hide_destination_history(tmp_path):
    client = Client(tmp_path)
    source = client.workflow
    client.workflow = source.with_name("wf-b.json")
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b", remediation_history=[dict(cycle_number=1)])))
    client.call(dict(op="join", source_workflow=str(source)), 2)


@pytest.mark.parametrize("operation", ["init", "join", "finish", "checkpoint", "extend", "finding"])
def test_remfix_other_transactions_do_not_report_failed_writes_as_success(tmp_path, monkeypatch, capsys, operation):
    import cc10x_review_budget as budget
    client = Client(tmp_path)
    ledger_path = Path(client.call(dict(op="inspect"))["projection"]["ledger_path"])
    if operation in ("finish", "finding"):
        client.call(client.reserve())
    if operation == "extend":
        client.call(checkpoint(client))
        request = grant()
    elif operation == "checkpoint":
        request = checkpoint(client)
    elif operation == "finish":
        request = client.finish()
    elif operation == "finding":
        request = dict(op="finding", event_id="f", workflow_uuid="wf-a", subject_id="subject-a",
                       recorded_at="2026-01-01T00:00:00Z", finding_id="finding", source_attempt_id="a",
                       invariant="durability", surface="ledger", summary="Retain charge", state="open", proof_refs=[], alias_of=None)
    else:
        source = client.workflow
        client.workflow = source.with_name("wf-b.json")
        client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-b")))
        request = (dict(op="join", source_workflow=str(source)) if operation == "join" else
                   dict(op="init", lineage_id="new", subject_id="subject-a"))
    before = ledger_path.read_bytes()
    request_path = tmp_path / "request.json"
    request_path.write_text(json.dumps(request))
    def fail(*args):
        raise OSError("synthetic replace failure")
    with monkeypatch.context() as patch:
        patch.setattr(budget.os, "replace", fail)
        code = budget.main(["--state-root", str(client.root), "--workflow", str(client.workflow), "--request", str(request_path)])
    result = json.loads(capsys.readouterr().out)
    assert code == 3 and result["status"] == "invalid", result
    assert result.get("reservation") is None and result.get("dispatch") is None
    assert ledger_path.read_bytes() == before
    assert not (client.root / "budgets/new.json").exists()


def test_remfix_unknown_migration_retains_observed_repair_floor(tmp_path):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-a", remediation_history=[dict(cycle_number=i) for i in range(1, 4)])))
    result = client.call(dict(op="init", lineage_id="unknown", subject_id="subject-a",
                             migration=dict(coverage="unknown", charged_units=0, counts={}, source_refs=["history"])))
    assert result["projection"]["charged_units"] == 32
    assert result["projection"]["counts"]["remediation_attempts"] == 3
    client.call(dict(op="inspect"))


def test_remfix_migration_unions_distinct_rounds_across_evidence_sources(tmp_path):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-a", remediation_history=[dict(cycle_number=1)])))
    client.workflow.with_suffix(".events.jsonl").write_text(json.dumps(dict(event="remediation_created", details=dict(cycle_number=2))) + "\n")
    opening = dict(coverage="complete", charged_units=1, counts={"subject-a": {"attempts": 1, "remediation_attempts": 1}}, source_refs=["history", "events"])
    request = dict(op="init", lineage_id="combined", subject_id="subject-a", migration=opening)
    client.call(request, 2)
    opening.update(charged_units=2, counts={"subject-a": {"attempts": 2, "remediation_attempts": 2}})
    result = client.call(request)
    assert result["projection"]["counts"]["remediation_attempts"] == 2


@pytest.mark.parametrize("link_source", ["history", "events", "status_history"])
@pytest.mark.parametrize("disjoint", [False, True])
def test_remfix2_linked_round_receipts_count_once(tmp_path, link_source, disjoint):
    client = Client(tmp_path)
    rows = {"history": dict(attempt_id="repair"), "events": dict(cycle_number=1),
            "status_history": dict(cycle_number=1)}
    rows[link_source] = dict(attempt_id="repair", cycle_number=1)
    artifact = dict(workflow_uuid="wf-a", remediation_history=[rows["history"]],
                    status_history=[dict(event="remediation_created", details=rows["status_history"])])
    if disjoint:
        artifact["remediation_history"].append(dict(cycle_number=2))
    client.workflow.write_text(json.dumps(artifact))
    client.workflow.with_suffix(".events.jsonl").write_text(json.dumps(dict(event="remediation_created", details=rows["events"])) + "\n")
    count = 2 if disjoint else 1
    request = dict(op="init", lineage_id="linked", subject_id="subject-a",
                   migration=dict(coverage="complete", charged_units=count, source_refs=["receipts"],
                                  counts={"subject-a": dict(attempts=count, remediation_attempts=count)}))
    result = client.call(request)
    assert result["projection"]["counts"]["remediation_attempts"] == count
    assert client.call(dict(op="inspect"))["projection"] == result["projection"]


@pytest.mark.parametrize("contradiction", [dict(attempt_id="repair", cycle_number=2),
                                           dict(attempt_id="other", cycle_number=1)])
def test_remfix2_contradictory_round_links_block_import(tmp_path, contradiction):
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-a", remediation_history=[dict(attempt_id="repair", cycle_number=1)])))
    client.workflow.with_suffix(".events.jsonl").write_text(json.dumps(dict(event="remediation_created", details=contradiction)) + "\n")
    client.call(dict(op="init", lineage_id="conflict", subject_id="subject-a",
                     migration=dict(coverage="complete", charged_units=3, source_refs=["receipts"],
                                    counts={"subject-a": dict(attempts=3, remediation_attempts=3)})), 2)
    assert not (client.root / "budgets/conflict.json").exists()


def test_remfix2_live_receipts_preserve_one_round_and_reject_changed_link(tmp_path):
    client = Client(tmp_path)
    projection = client.call(client.reserve("repair", lane="remediation"))["projection"]
    artifact = json.loads(client.workflow.read_text())
    artifact["remediation_history"] = [dict(attempt_id="repair", cycle_number=1)]
    client.workflow.write_text(json.dumps(artifact))
    log = client.workflow.with_suffix(".events.jsonl")
    log.write_text(json.dumps(dict(event="remediation_created", details=dict(cycle_number=1))) + "\n")
    assert client.call(dict(op="inspect"))["projection"] == projection
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    with log.open("a") as handle:
        handle.write(json.dumps(dict(event="remediation_created", details=dict(attempt_id="repair", cycle_number=2))) + "\n")
    assert client.call(dict(op="inspect"), 2)["reasons"] == ["contradictory_round_links"]
    assert path.read_bytes() == before


def test_remfix2_imported_ledger_recovers_null_mirror_with_known_receipts(tmp_path):
    client = Client(tmp_path)
    artifact = dict(workflow_uuid="wf-a", results=dict(attempt_id="old", role="planner"))
    client.workflow.write_text(json.dumps(artifact))
    request = dict(op="init", lineage_id="imported", subject_id="subject-a",
                   migration=dict(coverage="unknown", charged_units=0, counts={}, source_refs=["history"]))
    projection = client.call(request)["projection"]
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    artifact["review_budget"] = None
    client.workflow.write_text(json.dumps(artifact))
    recovered = client.call(dict(op="init", lineage_id="imported", subject_id="subject-a"))
    assert recovered["projection"] == projection
    assert recovered["projection"]["remaining_units"] == 0
    assert path.read_bytes() == before


@pytest.mark.parametrize("funded", [False, True])
def test_remfix2_missing_mirror_recovers_exact_ledger_without_refunding(tmp_path, funded):
    client = Client(tmp_path)
    if funded:
        client.call(checkpoint(client))
        client.call(grant())
        client.call(client.reserve())
    projection = client.call(dict(op="inspect"))["projection"]
    path = Path(projection["ledger_path"])
    before = path.read_bytes()
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-a")))
    artifact_before = client.workflow.read_bytes()
    request = dict(op="init", lineage_id="lineage-a", subject_id="subject-a", policy=dict(base_units=999),
                   migration=dict(coverage="complete", charged_units=0, counts={}, source_refs=["reset"]))
    for _ in range(2):
        result = client.call(request, project=False)
        assert result["projection"] == projection
        assert result.get("dispatch") is None and result.get("reservation") is None
        assert path.read_bytes() == before
        assert client.workflow.read_bytes() == artifact_before
    client.call(request)
    assert client.call(dict(op="inspect"))["projection"] == projection


def test_remfix2_init_after_replace_failure_recovers(tmp_path, monkeypatch, capsys):
    import cc10x_review_budget as budget
    client = Client(tmp_path)
    client.workflow.write_text(json.dumps(dict(workflow_uuid="wf-new")))
    request = dict(op="init", lineage_id="interrupted", subject_id="subject-a")
    request_path = tmp_path / "init.json"
    request_path.write_text(json.dumps(request))
    original = budget.os.replace
    def fail_after_replace(*args):
        original(*args)
        raise OSError("synthetic interrupted initialization")
    with monkeypatch.context() as patch:
        patch.setattr(budget.os, "replace", fail_after_replace)
        code = budget.main(["--state-root", str(client.root), "--workflow", str(client.workflow), "--request", str(request_path)])
    failed = json.loads(capsys.readouterr().out)
    assert code == 3 and failed["projection"] is None
    path = client.root / "budgets/interrupted.json"
    before = path.read_bytes()
    result = client.call(request)
    assert result["projection"]["ledger_revision"] == 1
    assert result["projection"]["remaining_units"] == 32
    assert path.read_bytes() == before
    client.call(dict(op="inspect"))


@pytest.mark.parametrize("conflict", ["member", "subject", "lineage", "history", "receipt", "results", "log", "closure"])
def test_remfix2_recovery_rejects_identity_or_evidence_conflicts(tmp_path, conflict):
    client = Client(tmp_path)
    path = client.root / "budgets/lineage-a.json"
    artifact = dict(workflow_uuid="wf-a")
    request = dict(op="init", lineage_id="lineage-a", subject_id="subject-a")
    if conflict == "member":
        artifact["workflow_uuid"] = "foreign"
    elif conflict == "subject":
        request["subject_id"] = "foreign"
    elif conflict == "lineage":
        path = path.with_name("foreign.json")
        path.write_bytes((client.root / "budgets/lineage-a.json").read_bytes())
        request["lineage_id"] = "foreign"
    elif conflict == "history":
        artifact["remediation_history"] = [dict(cycle_number=1)]
    elif conflict == "receipt":
        client.workflow.with_suffix(".events.jsonl").write_text(json.dumps(dict(attempt_id="unknown")) + "\n")
    elif conflict == "results":
        artifact["results"] = dict(contract_ref="unmapped-result")
    elif conflict == "log":
        client.workflow.with_suffix(".events.jsonl").write_text("{")
    else:
        artifact["planning_review_status"] = "passed"
    client.workflow.write_text(json.dumps(artifact))
    before = path.read_bytes()
    result = client.call(request, 3 if conflict == "log" else 2)
    assert result["projection"] is None
    assert path.read_bytes() == before


def test_initialization_is_durable_and_does_not_write_workflow(tmp_path):
    assert SCRIPT.is_file(), "Production budget CLI is not available"
    state = tmp_path / ".cc10x"
    workflow = state / "workflows" / "wf-a.json"
    workflow.parent.mkdir(parents=True)
    workflow.write_text(json.dumps({"workflow_uuid": "wf-a"}))
    before = workflow.read_bytes()
    request = tmp_path / "request.json"
    request.write_text(json.dumps({"op": "init", "lineage_id": "lineage-a", "subject_id": "subject-a"}))
    result = subprocess.run([sys.executable, str(SCRIPT), "--state-root", str(state),
                             "--workflow", str(workflow), "--request", str(request)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    projection = json.loads(result.stdout)["projection"]
    assert projection["charged_units"] == 0
    assert projection["remaining_units"] == 32
    assert projection["ledger_path"] == str(state / "budgets" / "lineage-a.json")
    assert workflow.read_bytes() == before
    ledger = json.loads(Path(projection["ledger_path"]).read_text())
    assert (ledger["revision"], ledger["event_count"]) == (1, 0)
