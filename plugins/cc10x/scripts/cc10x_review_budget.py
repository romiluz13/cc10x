#!/usr/bin/env python3
"""Local, conservative review accounting. The CLI never writes workflows."""
from __future__ import annotations

import argparse
import copy
import hashlib
import math
import json
import os
import re
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Literal, Optional, TypedDict, Union

from cc10x_hooklib import state_root

DEFAULT_POLICY = dict(base_units=32, extension_units=8, fresh_limit=2,
                      remediation_limit=3, amendment_attempt_limit=3,
                      code_review_limit=4, spec_gate_limit=3)
EMPTY_COUNTS = dict(attempts=0, fresh_valid=0, amendment_valid=0,
                    code_review_valid=0, remediation_attempts=0)
LIMITS = dict(fresh="fresh_limit", amendment="amendment_attempt_limit",
              code_review="code_review_limit", remediation="remediation_limit")


class EventHeader(TypedDict):
    event_id: str
    seq: int
    workflow_uuid: str
    subject_id: str
    recorded_at: str


class Reserved(EventHeader):
    kind: Literal["attempt_reserved"]
    attempt_id: str
    node_id: str
    node_descriptor: dict
    dependency_node_ids: List[str]
    lane: str
    phase_id: str
    scope_digest: str
    parent_attempt_id: Optional[str]
    retry_of: Optional[str]
    input_digest: str
    input_refs: List[dict]
    reserved_units: int
    funding: List[dict]
    lane_funding: Optional[dict]
    authorization_checks: List[dict]
    finding_ids: List[str]
    checkpoint_id: Optional[str]


class Finished(EventHeader):
    kind: Literal["attempt_finished"]
    attempt_id: str
    outcome: Literal["valid", "invalid", "cancelled", "lost"]
    contract_ref: Optional[str]
    contract_digest: Optional[str]
    verdict: Optional[str]
    review_mode: Optional[str]
    reviewed_revision: Optional[int]
    reviewed_input_digest: Optional[str]
    spec_gate_iterations: int
    evidence_refs: List[dict]
    measurement: dict


class ContentRef(TypedDict):
    ref: str
    digest: str


class ContractCorrection(TypedDict):
    invalid_attempt_id: str
    instruction: ContentRef


class CorrectionFields(TypedDict, total=False):
    contract_correction: ContractCorrection


class Checkpoint(EventHeader, CorrectionFields):
    kind: Literal["checkpoint"]
    checkpoint_id: str
    action: str
    observed_revision: int
    scope_digest: str
    input_digest: str
    finding_ids: List[str]
    proof_refs: List[dict]
    changed_input_refs: List[dict]
    progress: str
    reopened_ids: List[str]
    scope_change: str
    rationale: str
    remaining_units: int


class Extension(EventHeader):
    kind: Literal["extension_granted"]
    grant_id: str
    authorization_id: str
    authorization_kind: Literal["single_use", "standing"]
    authorization_ref: str
    authorization_scope: dict
    checkpoint_id: str
    additional_units: int
    lane_increments: dict


class Finding(EventHeader):
    kind: Literal["finding_recorded"]
    finding_id: str
    source_attempt_id: str
    invariant: str
    surface: str
    summary: str
    state: str
    proof_refs: List[dict]
    alias_of: Optional[str]


BudgetEvent = Union[Reserved, Finished, Checkpoint, Extension, Finding]


class BudgetError(Exception):
    def __init__(self, reason: str, status: str = "invalid") -> None:
        self.reason = reason
        self.status = status


def _id(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise BudgetError("invalid_id")
    return value


def _read(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    if not isinstance(data, dict):
        raise BudgetError("invalid_object")
    return data


def _workflow_evidence(path: Path) -> dict:
    """Use the same artifact and companion evidence at every CLI boundary."""
    artifact = _read(path)
    log = path.with_suffix(".events.jsonl")
    events = []
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise BudgetError("invalid_event_evidence")
                events.append(event)
    artifact["_budget_events"] = events
    return artifact


def _has_evidence(value: object) -> bool:
    if isinstance(value, dict):
        return any(_has_evidence(child) for child in value.values())
    if isinstance(value, list):
        return any(_has_evidence(child) for child in value)
    return bool(value)


def _history_floor(artifact: dict) -> tuple[dict[str, int], int, list[str]]:
    """Corroborated lower bounds, not a claim that legacy history is complete."""
    events = artifact.get("_budget_events", [])
    history = artifact.get("remediation_history", [])
    if not isinstance(history, list):
        raise BudgetError("invalid_history")
    attempt_cycles: dict[str, int] = {}
    cycle_attempts: dict[int, str] = {}
    sources: list[set[tuple]] = []

    def collect_rounds(rows: list) -> None:
        identities = set()
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise BudgetError("invalid_history")
            attempt = _id(row["attempt_id"]) if row.get("attempt_id") is not None else None
            cycle = _integer(row["cycle_number"], 1) if row.get("cycle_number") is not None else None
            if attempt is not None and cycle is not None:
                if (attempt_cycles.get(attempt, cycle) != cycle or
                        cycle_attempts.get(cycle, attempt) != attempt):
                    raise BudgetError("contradictory_round_links", "blocked")
                attempt_cycles[attempt], cycle_attempts[cycle] = cycle, attempt
            if attempt is not None:
                identity = ("attempt", attempt)
            elif cycle is not None:
                identity = ("cycle", cycle)
            else:
                identity = ("unmapped", index)
            identities.add(identity)
        sources.append(identities)

    collect_rounds(history)
    for source in (events, artifact.get("status_history", [])):
        if not isinstance(source, list) or any(not isinstance(event, dict) for event in source):
            raise BudgetError("invalid_history")
        remediation_events = [event.get("details", event) for event in source
                              if event.get("event", event.get("kind")) == "remediation_created"]
        collect_rounds(remediation_events)
    # Resolve links only after all sources have contributed aliases. Anonymous
    # rows establish a per-source floor; identified disjoint rounds are unioned.
    observed_rounds: set[tuple] = set()
    repairs = 0
    for identities in sources:
        resolved = {("attempt", cycle_attempts[value]) if kind == "cycle" and value in cycle_attempts
                    else (kind, value) for kind, value in identities}
        repairs = max(repairs, len(resolved))
        observed_rounds.update(identity for identity in resolved if identity[0] != "unmapped")
    repairs = max(repairs, len(observed_rounds))
    attempts = {}

    def collect(value: object) -> None:
        if isinstance(value, dict):
            if value.get("attempt_id") is not None:
                attempt = _id(value["attempt_id"])
                descriptor = value.get("node_descriptor") or {}
                role = descriptor.get("role", value.get("role"))
                attempts[attempt] = max(attempts.get(attempt, 0), 4 if role == "planner" else 1)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    for key in ("results", "evidence", "remediation_history", "status_history", "_budget_events"):
        collect(artifact.get(key))
    fresh = _integer(artifact.get("planning_review_runs", 0))
    counts = dict(fresh_valid=fresh, remediation_attempts=repairs,
                  attempts=max(len(attempts), fresh + repairs))
    return counts, max(sum(attempts.values()), fresh + repairs), sorted(attempts)


def _reconcile_opening(artifact: dict, opening: dict, subject: str, policy: dict) -> dict:
    opening = copy.deepcopy(opening)
    if not opening["source_refs"]:
        raise BudgetError("missing_migration_evidence", "blocked")
    floor, units, attempt_ids = _history_floor(artifact)
    counts = opening["counts"].setdefault(subject, {})
    if opening["coverage"] == "unknown":
        opening["charged_units"] = max(policy["base_units"], units, _integer(opening["charged_units"]))
        for key, value in floor.items():
            counts[key] = max(_integer(counts.get(key, 0)), value)
    elif (_integer(opening["charged_units"]) < units or
          any(_integer(counts.get(key, 0)) < value for key, value in floor.items())):
        raise BudgetError("accounting_conflict", "blocked")
    # Keep the imported identity set immutable so old receipts remain readable,
    # while a later, unledgered receipt still causes a conflict.
    opening["evidence_attempt_ids"] = attempt_ids
    return opening


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def _integer(value: object, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise BudgetError("invalid_counter")
    return value


def _text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BudgetError("invalid_text")
    return value


def _sha(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
        raise BudgetError("invalid_digest")
    return value


def _refs(refs: list) -> None:
    if not isinstance(refs, list):
        raise BudgetError("invalid_refs")
    for ref in refs:
        _text(ref["ref"])
        _sha(ref["digest"])
        if "input_digest" in ref:
            _sha(ref["input_digest"])


def _event_shape(event: BudgetEvent) -> None:
    shape = {"attempt_reserved": Reserved, "attempt_finished": Finished, "checkpoint": Checkpoint,
             "extension_granted": Extension, "finding_recorded": Finding}[event["kind"]]
    expected = set(shape.__annotations__) - {"seq"}
    if event["kind"] == "attempt_reserved":
        expected -= {"reserved_units", "funding", "lane_funding"}
    if event["kind"] == "checkpoint":
        expected -= {"contract_correction"}
    if not expected.issubset(event):
        raise BudgetError("missing_event_fields")
    for key in ("event_id", "workflow_uuid", "subject_id"):
        _id(event[key])
    datetime.fromisoformat(_text(event["recorded_at"]).replace("Z", "+00:00"))
    for key in ("scope_digest", "input_digest"):
        if key in event:
            _sha(event[key])
    for key in ("input_refs", "changed_input_refs", "proof_refs", "evidence_refs"):
        if key in event:
            _refs(event[key])
    for key in ("finding_ids", "reopened_ids", "dependency_node_ids"):
        if key in event:
            values = event[key]
            if not isinstance(values, list) or len(set(values)) != len(values):
                raise BudgetError("duplicate_ids")
            for value in values:
                (_sha if key == "dependency_node_ids" else _id)(value)


def _events(ledger: dict, kind: str) -> list:
    return [event for event in ledger["events"] if event["kind"] == kind]


def _projection(ledger: dict, subject: str, path: str = "") -> dict:
    counts = EMPTY_COUNTS.copy()
    counts.update({k: v for k, v in ledger["opening"]["counts"].get(subject, {}).items() if k in counts})
    reserved = _events(ledger, "attempt_reserved")
    counts["attempts"] = sum(c.get("attempts", 0) for c in ledger["opening"]["counts"].values()) + len(reserved)
    counts["remediation_attempts"] += sum(e["subject_id"] == subject and e["lane"] == "remediation" for e in reserved)
    by_id = {event["attempt_id"]: event for event in reserved}
    for finished in _events(ledger, "attempt_finished"):
        reservation = by_id[finished["attempt_id"]]
        if finished["outcome"] == "valid" and reservation["subject_id"] == subject:
            key = reservation["lane"] + "_valid"
            if key in counts:
                counts[key] += 1
    charged = ledger["opening"]["charged_units"] + sum(e["reserved_units"] for e in reserved)
    remaining = sum(_balances(ledger).values())
    return dict(version=1, lineage_id=ledger["lineage_id"], ledger_path=path, subject_id=subject,
                ledger_revision=ledger["revision"], counts=counts, charged_units=charged,
                remaining_units=remaining)


def _balances(ledger: dict) -> dict:
    balances = {None: max(ledger["policy"]["base_units"] - ledger["opening"]["charged_units"], 0)}
    balances.update({e["grant_id"]: e["additional_units"] for e in _events(ledger, "extension_granted")})
    for event in _events(ledger, "attempt_reserved"):
        for debit in event["funding"]:
            balances[debit["grant_id"]] -= debit["units"]
    return balances


def _eligible(ledger: dict, event: dict) -> list:
    checks = {item["grant_id"]: item for item in event["authorization_checks"]}
    eligible = []
    for grant in _events(ledger, "extension_granted"):
        scope = grant["authorization_scope"]
        check = checks.get(grant["grant_id"], {})
        if (scope["subject_id"] == event["subject_id"] and scope["scope_digest"] == event["scope_digest"]
                and event["lane"] in scope["lanes"] and check.get("applicable") is True
                and check.get("evidence_ref") and check.get("evidence_digest")):
            eligible.append(grant)
    return eligible


def _fund(ledger: dict, event: dict, units: int) -> None:
    eligible = _eligible(ledger, event)
    balances = _balances(ledger)
    sources = [None] + [g["grant_id"] for g in eligible]
    if sum(balances[source] for source in sources) < units:
        raise BudgetError("insufficient_eligible_units", "blocked")
    funding = []
    remaining = units
    for source in sources:
        amount = min(remaining, balances[source])
        if amount:
            funding.append(dict(source="base" if source is None else "grant", grant_id=source, units=amount))
            remaining -= amount
    event["reserved_units"], event["funding"] = units, funding
    event["lane_funding"] = None
    lane = event["lane"]
    if lane == "work":
        return
    finished = {e["attempt_id"]: e["outcome"] for e in _events(ledger, "attempt_finished")}
    usage = {source: 0 for source in sources}
    opening_key = dict(fresh="fresh_valid", code_review="code_review_valid",
                       amendment="amendment_attempts", remediation="remediation_attempts")[lane]
    limit = ledger["policy"][LIMITS[lane]]
    usage[None] = min(limit, ledger["opening"]["counts"].get(event["subject_id"], {}).get(opening_key, 0))
    for prior in _events(ledger, "attempt_reserved"):
        if prior["lane"] != lane or prior["subject_id"] != event["subject_id"]:
            continue
        if lane in ("fresh", "code_review") and finished.get(prior["attempt_id"]) in ("invalid", "cancelled", "lost"):
            continue
        source = prior["lane_funding"]["grant_id"]
        if source in usage:
            usage[source] += 1
    capacities = {None: limit}
    capacities.update({g["grant_id"]: g["lane_increments"].get(lane, 0) for g in eligible})
    for source in sources:
        if usage[source] < capacities[source]:
            event["lane_funding"] = dict(source="base" if source is None else "grant", grant_id=source)
            return
    raise BudgetError("lane_limit", "blocked")


def _validate_ledger(ledger: dict) -> None:
    if type(ledger["version"]) is not int or ledger["version"] != 1:
        raise BudgetError("unsupported_version")
    _id(ledger["lineage_id"])
    _integer(ledger["revision"], 1)
    if _integer(ledger["event_count"]) != len(ledger["events"]):
        raise BudgetError("accounting_conflict")
    if ledger["revision"] != ledger["event_count"] + len(ledger["members"]):
        raise BudgetError("accounting_conflict")
    if set(ledger["policy"]) != set(DEFAULT_POLICY):
        raise BudgetError("invalid_policy")
    for value in ledger["policy"].values():
        _integer(value, 1)
    for key in ("fresh_limit", "remediation_limit", "amendment_attempt_limit", "spec_gate_limit"):
        if ledger["policy"][key] != DEFAULT_POLICY[key]:
            raise BudgetError("invalid_policy")
    _integer(ledger["opening"]["charged_units"])
    imported_ids = ledger["opening"].get("evidence_attempt_ids", [])
    if not isinstance(imported_ids, list) or len(set(imported_ids)) != len(imported_ids):
        raise BudgetError("invalid_opening_evidence")
    for attempt_id in imported_ids:
        _id(attempt_id)
    for subject, counts in ledger["opening"]["counts"].items():
        _id(subject)
        for key, value in counts.items():
            if key not in (*EMPTY_COUNTS, "amendment_attempts"):
                raise BudgetError("invalid_opening_count")
            _integer(value)
    if ledger["opening"]["coverage"] not in ("complete", "unknown"):
        raise BudgetError("invalid_opening")
    members = set()
    for member in ledger["members"]:
        key = _id(member["workflow_uuid"])
        _id(member["subject_id"])
        if key in members:
            raise BudgetError("membership_mismatch")
        members.add(key)
    ids = set()
    prefix = copy.deepcopy(ledger)
    prefix["events"] = []
    prefix["revision"] = 1
    for index, event in enumerate(ledger["events"], 1):
        _event_shape(event)
        if _integer(event["seq"], 1) != index or event["event_id"] in ids:
            raise BudgetError("accounting_conflict")
        ids.add(_id(event["event_id"]))
        candidate = copy.deepcopy(event)
        if event["workflow_uuid"] not in members:
            raise BudgetError("membership_mismatch")
        kind = event["kind"]
        if kind == "checkpoint":
            observed = _integer(event["observed_revision"], index)
            if observed > index + len(members) - 1:
                raise BudgetError("accounting_conflict")
            prefix["revision"] = observed
        handler = {"attempt_reserved": _reserve, "attempt_finished": _finish,
                   "checkpoint": _checkpoint, "extension_granted": _extend, "finding_recorded": _finding}.get(kind)
        if handler is None:
            raise BudgetError("invalid_event_kind")
        try:
            handler(prefix, candidate)
        except BudgetError:
            raise BudgetError("accounting_conflict")
        if candidate != event:
            raise BudgetError("accounting_conflict")
        prefix["events"].append(event)
        prefix["revision"] += 1


def validate_budget_projection(artifact: dict, ledger: dict) -> list[str]:
    """Diagnose a v1 mirror without mutating it; absent legacy fields are readable."""
    try:
        mirror = artifact.get("review_budget")
        if mirror is None:
            return []
        _validate_ledger(ledger)
        if mirror["version"] != 1:
            return ["unsupported_version"]
        path = Path(mirror["ledger_path"])
        if not path.is_absolute() or str(path.resolve()) != str(path):
            return ["invalid_ledger_path"]
        if not any(m["workflow_uuid"] == artifact["workflow_uuid"] and
                   m["subject_id"] == mirror["subject_id"] for m in ledger["members"]):
            return ["membership_mismatch"]
        expected = _projection(ledger, mirror["subject_id"], str(path))
        known_attempts = {e["attempt_id"] for e in _events(ledger, "attempt_reserved")}
        known_attempts.update(ledger["opening"].get("evidence_attempt_ids", []))
        def check_attempts(value: object) -> None:
            if isinstance(value, dict):
                if "attempt_id" in value and value["attempt_id"] not in known_attempts:
                    raise BudgetError("accounting_conflict")
                for child in value.values():
                    check_attempts(child)
            elif isinstance(value, list):
                for child in value:
                    check_attempts(child)
        for key in ("results", "evidence", "remediation_history", "status_history", "_budget_events"):
            check_attempts(artifact.get(key))
        floor, units, _ = _history_floor(artifact)
        if units > expected["charged_units"] or any(value > expected["counts"][key] for key, value in floor.items()):
            return ["accounting_conflict"]
        if (_integer(mirror["charged_units"]) > expected["charged_units"] or
                any(_integer(n) > expected["counts"][key] for key, n in mirror["counts"].items()) or
                _integer(artifact.get("planning_review_runs", 0)) > expected["counts"]["fresh_valid"]):
            return ["accounting_conflict"]
        if mirror != expected:
            return ["accounting_conflict" if mirror["ledger_revision"] > ledger["revision"]
                    else "projection_stale"]
        if artifact.get("planning_review_status") == "passed":
            reserved = {e["attempt_id"]: e for e in _events(ledger, "attempt_reserved")}
            if not any(e["outcome"] == "valid" and e["verdict"] == "PASS" and
                       e["review_mode"] == "fresh" and e["reviewed_revision"] == artifact.get("plan_revision") and
                       e["reviewed_input_digest"] == artifact.get("plan_input_digest") and
                       reserved[e["attempt_id"]]["subject_id"] == mirror["subject_id"]
                       for e in _events(ledger, "attempt_finished")):
                return ["fresh_pass_required"]
        return []
    except BudgetError as exc:
        return [exc.reason]
    except (KeyError, TypeError, ValueError, OSError, AttributeError):
        return ["invalid_budget_schema"]


def _reserve(ledger: dict, event: dict) -> None:
    _id(event["attempt_id"])
    if not event["input_refs"]:
        raise BudgetError("missing_input_refs")
    checks = event["authorization_checks"]
    if not isinstance(checks, list) or len({c["grant_id"] for c in checks}) != len(checks):
        raise BudgetError("invalid_authorization_checks")
    for check in checks:
        _id(check["grant_id"])
        if type(check["applicable"]) is not bool:
            raise BudgetError("invalid_authorization_checks")
        _text(check["evidence_ref"])
        _sha(check["evidence_digest"])
    descriptor = event["node_descriptor"]
    canonical_input = dict(scope_digest=event["scope_digest"], role=descriptor["role"],
                           input_refs=sorted(event["input_refs"], key=lambda ref: (ref["ref"], ref["digest"])))
    if event["input_digest"] != _digest(canonical_input):
        raise BudgetError("input_digest_mismatch")
    if set(descriptor) != {"lineage_id", "subject_id", "step_key", "phase_id", "role", "source_id", "repository_id"}:
        raise BudgetError("invalid_node")
    if event["node_id"] != _digest(descriptor) or descriptor["lineage_id"] != ledger["lineage_id"]:
        raise BudgetError("invalid_node")
    if any(descriptor[key] != event[key] for key in ("subject_id", "phase_id")):
        raise BudgetError("invalid_node")
    for key, value in descriptor.items():
        if key not in ("source_id", "repository_id") or value is not None:
            _id(value)
    reserved = _events(ledger, "attempt_reserved")
    if any(e["attempt_id"] == event["attempt_id"] for e in reserved):
        raise BudgetError("conflicting_attempt")
    history = [e for e in reserved if e["node_id"] == event["node_id"]]
    if history:
        prior = history[-1]
        if not any(e["attempt_id"] == prior["attempt_id"] for e in _events(ledger, "attempt_finished")):
            raise BudgetError("node_unresolved", "blocked")
        if event["input_digest"] == prior["input_digest"]:
            raise BudgetError("unchanged_input", "blocked")
        if event["retry_of"] != prior["attempt_id"]:
            raise BudgetError("invalid_retry")
    correction = next((e for e in _events(ledger, "checkpoint")
                       if e["checkpoint_id"] == event["checkpoint_id"] and "contract_correction" in e), None)
    if correction is not None:
        prior = _correction_prior(ledger, correction)
        if ledger["revision"] != correction["observed_revision"] + 1:
            raise BudgetError("stale_checkpoint", "blocked")
        if any(event[key] != prior[key] for key in
               ("node_descriptor", "node_id", "subject_id", "lane", "scope_digest", "dependency_node_ids")):
            raise BudgetError("contract_correction_identity", "blocked")
        instruction = correction["contract_correction"]["instruction"]
        expected_refs = sorted(prior["input_refs"] + [instruction], key=lambda ref: (ref["ref"], ref["digest"]))
        if sorted(event["input_refs"], key=lambda ref: (ref["ref"], ref["digest"])) != expected_refs:
            raise BudgetError("contract_correction_input", "blocked")
    if history:
        prior = history[-1]
        checkpoints = [e for e in _events(ledger, "checkpoint") if e["checkpoint_id"] == event["checkpoint_id"]]
        if not checkpoints:
            raise BudgetError("retry_checkpoint_required", "blocked")
        checkpoint = checkpoints[0]
        if (checkpoint["action"] != "continue" or checkpoint["subject_id"] != event["subject_id"] or
                checkpoint["scope_digest"] != event["scope_digest"] or checkpoint["input_digest"] != event["input_digest"]):
            raise BudgetError("retry_checkpoint_mismatch", "blocked")
        for proof in checkpoint["proof_refs"]:
            _proof(ledger, proof, [prior["node_id"]] + event["dependency_node_ids"])
        if event["lane"] in ("fresh", "amendment", "code_review") and not checkpoint["proof_refs"] and correction is None:
            raise BudgetError("covering_proof_required", "blocked")
    elif event["retry_of"] is not None:
        raise BudgetError("invalid_retry")
    if event["parent_attempt_id"] is not None and not any(e["attempt_id"] == event["parent_attempt_id"] for e in reserved):
        raise BudgetError("invalid_parent")
    units = 4 if descriptor["role"] == "planner" else 1
    role, lane = descriptor["role"], event["lane"]
    allowed = ({"fresh", "amendment"} if role == "plan-gap-reviewer" else
               {"code_review"} if role == "code-reviewer" else
               {"work", "remediation"} if role in ("component-builder", "bug-investigator", "qa-harness-builder") else {"work"})
    if lane not in allowed:
        raise BudgetError("role_lane_mismatch")
    _fund(ledger, event, units)


def _finish(ledger: dict, event: dict) -> None:
    _id(event["attempt_id"])
    measurement = event["measurement"]
    if measurement["availability"] not in ("known", "partial", "unknown"):
        raise BudgetError("invalid_measurement")
    tokens, seconds = measurement["tokens"], measurement["agent_seconds"]
    if tokens is not None:
        _integer(tokens)
    if seconds is not None and (type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0):
        raise BudgetError("invalid_measurement")
    if measurement["availability"] == "unknown" and (tokens is not None or seconds is not None):
        raise BudgetError("invalid_measurement")
    if measurement["availability"] == "known" and (tokens is None or seconds is None):
        raise BudgetError("partial_measurement")
    if tokens is not None or seconds is not None:
        _text(measurement["source"])
    matches = [e for e in _events(ledger, "attempt_reserved") if e["attempt_id"] == event["attempt_id"]]
    if not matches or any(e["attempt_id"] == event["attempt_id"] for e in _events(ledger, "attempt_finished")):
        raise BudgetError("invalid_finish")
    if event["outcome"] not in ("valid", "invalid", "cancelled", "lost"):
        raise BudgetError("invalid_outcome")
    if event["subject_id"] != matches[0]["subject_id"]:
        raise BudgetError("invalid_finish")
    if _integer(event["spec_gate_iterations"]) > 3:
        raise BudgetError("spec_gate_limit")
    if matches[0]["node_descriptor"]["role"] != "planner" and event["spec_gate_iterations"]:
        raise BudgetError("invalid_inline_iterations")
    if event["outcome"] == "valid" and not (event["contract_ref"] and event["contract_digest"]):
        raise BudgetError("missing_contract")
    if event["outcome"] == "valid":
        _text(event["contract_ref"])
        _sha(event["contract_digest"])
    lane = matches[0]["lane"]
    if event["outcome"] == "valid" and lane in ("fresh", "amendment", "code_review"):
        if lane == "code_review" and event["review_mode"] is not None:
            raise BudgetError("review_mode_mismatch")
        if event["reviewed_input_digest"] != matches[0]["input_digest"]:
            raise BudgetError("review_input_mismatch")
        verdicts = ("APPROVE", "CHANGES_REQUESTED") if lane == "code_review" else ("PASS", "FINDINGS")
        if event["verdict"] not in verdicts:
            raise BudgetError("invalid_verdict")
        if lane in ("fresh", "amendment"):
            if event["review_mode"] != lane:
                raise BudgetError("review_mode_mismatch")
            _integer(event["reviewed_revision"], 1)


def _checkpoint(ledger: dict, event: dict) -> None:
    _id(event["checkpoint_id"])
    if event["observed_revision"] != ledger["revision"]:
        raise BudgetError("stale_checkpoint", "blocked")
    if event["remaining_units"] != _projection(ledger, event["subject_id"])["remaining_units"]:
        raise BudgetError("accounting_conflict")
    if event["action"] not in ("continue", "stop", "needs_authorization"):
        raise BudgetError("invalid_checkpoint")
    if event["progress"] not in ("new_counterexample", "verified_reduction", "finite_fix", "none"):
        raise BudgetError("invalid_progress")
    if event["scope_change"] not in ("none", "implementation", "test_allocation", "architecture", "product", "security"):
        raise BudgetError("invalid_scope_change")
    _text(event["rationale"])
    if event["action"] != "stop" and (event["progress"] == "none" or
            event["scope_change"] in ("architecture", "product", "security") or
            not (event["changed_input_refs"] or event["proof_refs"])):
        raise BudgetError("progress_stop", "blocked")
    if any(e["checkpoint_id"] == event["checkpoint_id"] for e in _events(ledger, "checkpoint")):
        raise BudgetError("duplicate_checkpoint")
    for proof in event["proof_refs"]:
        _proof(ledger, proof)
    if "contract_correction" in event:
        _correction_prior(ledger, event)


def _correction_prior(ledger: dict, checkpoint: dict) -> dict:
    """Bind the single instruction correction to a terminal receipt and its proof ancestry."""
    correction = checkpoint["contract_correction"]
    if not isinstance(correction, dict) or set(correction) != {"invalid_attempt_id", "instruction"}:
        raise BudgetError("invalid_contract_correction")
    _id(correction["invalid_attempt_id"])
    instruction = correction["instruction"]
    if not isinstance(instruction, dict) or set(instruction) != {"ref", "digest"}:
        raise BudgetError("invalid_contract_correction")
    _refs([instruction])
    reserved = {e["attempt_id"]: e for e in _events(ledger, "attempt_reserved")}
    prior = reserved.get(correction["invalid_attempt_id"])
    if prior is None:
        raise BudgetError("contract_correction_attempt", "blocked")
    latest = [e for e in reserved.values() if e["node_id"] == prior["node_id"]][-1]
    if latest != prior:
        raise BudgetError("contract_correction_attempt", "blocked")
    finish = next((e for e in _events(ledger, "attempt_finished") if e["attempt_id"] == prior["attempt_id"]), None)
    if finish is None or finish["outcome"] != "invalid":
        raise BudgetError("contract_correction_outcome", "blocked")
    receipt = dict(ref=_text(finish["contract_ref"]), digest=_sha(finish["contract_digest"]))
    if (receipt not in checkpoint["changed_input_refs"] or instruction not in checkpoint["changed_input_refs"] or
            instruction == receipt or
            any(all(ref[key] == instruction[key] for key in ("ref", "digest")) for ref in prior["input_refs"])):
        raise BudgetError("contract_correction_evidence", "blocked")
    if (checkpoint["action"] != "continue" or checkpoint["subject_id"] != prior["subject_id"] or
            checkpoint["scope_digest"] != prior["scope_digest"]):
        raise BudgetError("contract_correction_identity", "blocked")
    checkpoints = {e["checkpoint_id"]: e for e in _events(ledger, "checkpoint")}
    ancestor = prior
    while ancestor is not None:
        previous = checkpoints.get(ancestor["checkpoint_id"])
        if previous is not None and "contract_correction" in previous:
            raise BudgetError("contract_correction_used", "blocked")
        ancestor = reserved.get(ancestor["retry_of"])
    previous = checkpoints.get(prior["checkpoint_id"])
    inherited = previous["proof_refs"] if previous is not None else []
    if any(proof not in checkpoint["proof_refs"] for proof in inherited):
        raise BudgetError("covering_proof_required", "blocked")
    for proof in checkpoint["proof_refs"]:
        _proof(ledger, proof, [prior["node_id"]] + prior["dependency_node_ids"])
    return prior


def _proof(ledger: dict, proof: dict, nodes: Optional[list] = None) -> None:
    reservations = [e for e in _events(ledger, "attempt_reserved") if e["attempt_id"] == proof["producer_attempt_id"]]
    if not reservations:
        raise BudgetError("unknown_proof_producer", "blocked")
    producer = reservations[0]
    if producer["node_id"] != proof["producer_node_id"] or producer["subject_id"] != proof["subject_id"]:
        raise BudgetError("proof_producer_mismatch", "blocked")
    if nodes is not None and producer["node_id"] not in nodes:
        raise BudgetError("undeclared_proof_dependency", "blocked")
    evidence = {key: proof[key] for key in ("ref", "digest", "input_digest")}
    if not any(e["attempt_id"] == producer["attempt_id"] and e["outcome"] == "valid" and evidence in e["evidence_refs"]
               for e in _events(ledger, "attempt_finished")):
        raise BudgetError("stale_or_invalid_proof", "blocked")


def _finding(ledger: dict, event: dict) -> None:
    _id(event["finding_id"])
    if not any(e["attempt_id"] == event["source_attempt_id"] for e in _events(ledger, "attempt_reserved")):
        raise BudgetError("unknown_finding_source")
    if event["state"] not in ("open", "fixed", "disputed", "upheld", "rejected", "reopened"):
        raise BudgetError("invalid_finding_state")
    findings = _events(ledger, "finding_recorded")
    history = [e for e in findings if e["finding_id"] == event["finding_id"]]
    if event["alias_of"] is not None:
        matches = [e for e in findings if e["finding_id"] == event["alias_of"]]
        if not matches or matches[0]["alias_of"] is not None or event["alias_of"] == event["finding_id"]:
            raise BudgetError("invalid_alias")
        if any(matches[0][key] != event[key] for key in ("invariant", "surface")):
            raise BudgetError("conflicting_alias")
    if history and any(history[-1][key] != event[key] for key in ("invariant", "alias_of")):
        raise BudgetError("finding_identity_conflict")
    if history and event["state"] == "reopened" and (not event["proof_refs"] or event["proof_refs"] == history[-1]["proof_refs"]):
        raise BudgetError("reopening_requires_evidence", "blocked")
    for proof in event["proof_refs"]:
        _proof(ledger, proof)


def _extend(ledger: dict, event: dict) -> None:
    for key in ("grant_id", "authorization_id", "checkpoint_id"):
        _id(event[key])
    grants = _events(ledger, "extension_granted")
    if any(g["checkpoint_id"] == event["checkpoint_id"] for g in grants):
        raise BudgetError("checkpoint_consumed", "blocked")
    checkpoints = [e for e in _events(ledger, "checkpoint") if e["checkpoint_id"] == event["checkpoint_id"]]
    if not checkpoints or ledger["revision"] != checkpoints[0]["observed_revision"] + 1:
        raise BudgetError("stale_checkpoint", "blocked")
    checkpoint = checkpoints[0]
    scope = event["authorization_scope"]
    if (checkpoint["action"] != "needs_authorization" or checkpoint["progress"] == "none" or
            checkpoint["scope_change"] not in ("none", "implementation", "test_allocation") or
            scope["subject_id"] != event["subject_id"] or checkpoint["subject_id"] != event["subject_id"] or
            scope["scope_digest"] != checkpoint["scope_digest"] or not event["authorization_ref"]):
        raise BudgetError("ineligible_authorization", "blocked")
    if event["authorization_kind"] not in ("single_use", "standing"):
        raise BudgetError("invalid_authorization")
    for prior in grants:
        if prior["authorization_id"] == event["authorization_id"] and (prior["authorization_kind"] != "standing" or event["authorization_kind"] != "standing"):
            raise BudgetError("authorization_consumed", "blocked")
    units = _integer(event["additional_units"])
    increments = event["lane_increments"]
    if not scope["lanes"] or len(set(scope["lanes"])) != len(scope["lanes"]) or any(l not in (*LIMITS, "work") for l in scope["lanes"]):
        raise BudgetError("invalid_lanes")
    if units > ledger["policy"]["extension_units"] or any(l not in LIMITS or l not in scope["lanes"] or _integer(n) > 1 for l, n in increments.items()):
        raise BudgetError("invalid_extension")
    if units + sum(increments.values()) == 0:
        raise BudgetError("empty_extension")


def evaluate_budget(ledger: dict, request: dict) -> dict:
    """Pure event reducer. Returns a proposed ledger; never mutates its inputs."""
    result = dict(status="invalid", reasons=[], ledger=ledger, projection=None, dispatch=None, eligible_units=None)
    try:
        _validate_ledger(ledger)
        event = copy.deepcopy(request)
        op = event.pop("op")
        kinds = dict(reserve="attempt_reserved", finish="attempt_finished", checkpoint="checkpoint", extend="extension_granted", finding="finding_recorded")
        if op not in kinds:
            raise BudgetError("unsupported_operation")
        event["kind"] = kinds[op]
        _event_shape(event)
        for key in ("event_id", "workflow_uuid", "subject_id"):
            _id(event[key])
        if not any(m["workflow_uuid"] == event["workflow_uuid"] and m["subject_id"] == event["subject_id"] for m in ledger["members"]):
            raise BudgetError("membership_mismatch")
        result["projection"] = _projection(ledger, event["subject_id"])
        for old in ledger["events"]:
            if old["event_id"] == event["event_id"]:
                comparable = {k: v for k, v in old.items() if k not in ("seq", "reserved_units", "funding", "lane_funding")}
                if comparable != event:
                    raise BudgetError("conflicting_event")
        if op == "reserve":
            balances = _balances(ledger)
            result["eligible_units"] = balances[None] + sum(balances[g["grant_id"]] for g in _eligible(ledger, event))
            for old in _events(ledger, "attempt_reserved"):
                if old["attempt_id"] == event["attempt_id"]:
                    ignored = ("seq", "event_id", "recorded_at", "workflow_uuid", "reserved_units", "funding", "lane_funding")
                    if {k: v for k, v in old.items() if k not in ignored} != {k: v for k, v in event.items() if k not in ignored}:
                        raise BudgetError("conflicting_attempt")
                    result.update(status="allowed", dispatch="resume", reservation=old)
                    return result
        if op == "extend":
            for old in _events(ledger, "extension_granted"):
                if old["grant_id"] == event["grant_id"]:
                    ignored = ("seq", "event_id", "recorded_at")
                    if {k: v for k, v in old.items() if k not in ignored} != {k: v for k, v in event.items() if k not in ignored}:
                        raise BudgetError("conflicting_grant")
                    result.update(status="allowed")
                    return result
        for old in ledger["events"]:
            if old["event_id"] == event["event_id"]:
                comparable = {k: v for k, v in old.items() if k not in ("seq", "reserved_units", "funding", "lane_funding")}
                if comparable != event:
                    raise BudgetError("conflicting_event")
                result.update(status="allowed")
                return result
        proposed = copy.deepcopy(ledger)
        dict(reserve=_reserve, finish=_finish, checkpoint=_checkpoint, extend=_extend, finding=_finding)[op](proposed, event)
        event["seq"] = len(proposed["events"]) + 1
        proposed["events"].append(event)
        proposed["event_count"] += 1
        proposed["revision"] += 1
        result.update(status="allowed", ledger=proposed, projection=_projection(proposed, event["subject_id"]))
        if op == "reserve":
            result.update(dispatch="new", reservation=event)
    except BudgetError as exc:
        result.update(status=exc.status, reasons=[exc.reason])
    except (KeyError, ValueError, TypeError, AttributeError):
        result.update(reasons=["invalid_budget_schema"])
    return result


@contextmanager
def _lock(path: Path) -> Iterator[None]:
    try:
        import fcntl
    except ImportError:
        raise BudgetError("unsupported_locking")
    with path.open("a") as handle:
        deadline = time.monotonic() + 5
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise BudgetError("lock_contention", "blocked")
                time.sleep(0.025)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _write(path: Path, data: dict) -> None:
    descriptor, name = tempfile.mkstemp(dir=str(path.parent), prefix=".budget-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(data, handle, sort_keys=True, allow_nan=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _projection_result(artifact: dict, ledger: dict, subject: str, path: Path) -> dict:
    """Return recoverable accounting without claiming unsupported closure."""
    projection = _projection(ledger, subject, str(path))
    reasons = validate_budget_projection(dict(artifact, review_budget=projection), ledger)
    if reasons and not (reasons == ["fresh_pass_required"] and ledger["opening"]["source_refs"]):
        raise BudgetError(reasons[0], "blocked")
    return dict(status="blocked" if reasons else "allowed", reasons=reasons,
                projection=projection, ledger_revision=ledger["revision"])


def _fresh_proof_operation(ledger: dict, request: dict) -> bool:
    """Admission only: the evaluator still checks identity, proof and funding."""
    if not ledger["opening"]["source_refs"]:
        return False
    op = request.get("op")
    if op == "checkpoint":
        return True  # No dispatch or spending; existing checkpoint gates apply.
    if op == "extend":
        return (request.get("authorization_scope", {}).get("lanes") == ["fresh"] and
                set(request.get("lane_increments", {})) <= {"fresh"})
    if op == "reserve":
        return request.get("lane") == "fresh"
    if op == "finish":
        return any(event["attempt_id"] == request.get("attempt_id") and event["lane"] == "fresh"
                   for event in _events(ledger, "attempt_reserved"))
    return False


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", type=Path, default=None)
    parser.add_argument("--workflow", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args(argv)
    result = dict(status="invalid", reasons=[], projection=None, ledger_revision=None)
    try:
        root = (args.state_root or state_root()).resolve()
        workflow = args.workflow.resolve()
        if workflow.parent != root / "workflows":
            raise BudgetError("workflow_outside_state_root")
        artifact, request = _read(workflow), _read(args.request)
        workflow_uuid = _id(artifact.get("workflow_uuid"))
        if request.get("op") == "join":
            source_path = Path(request["source_workflow"]).resolve()
            source = _read(source_path)
            source_mirror = source.get("review_budget")
            if not isinstance(source_mirror, dict):
                raise BudgetError("missing_source", "blocked")
            path = Path(source_mirror["ledger_path"])
            if not path.is_absolute() or path != path.resolve():
                raise BudgetError("invalid_ledger_path")
            with _lock(path.with_suffix(".lock")):
                source = _workflow_evidence(source_path)
                if source["review_budget"]["ledger_path"] != str(path):
                    raise BudgetError("accounting_conflict", "blocked")
                ledger = _read(path)
                _validate_ledger(ledger)
                reasons = validate_budget_projection(source, ledger)
                if reasons == ["projection_stale"]:
                    current = _projection(ledger, source["review_budget"]["subject_id"], str(path))
                    reasons = validate_budget_projection(dict(source, review_budget=current), ledger)
                if reasons:
                    raise BudgetError("invalid_source", "blocked")
                subject = _id(request.get("subject_id", source_mirror["subject_id"]))
                if subject != source_mirror["subject_id"]:
                    _refs([request["subject_rationale"]])
                member = dict(workflow_uuid=workflow_uuid, subject_id=subject,
                              source_workflow_uuid=source["workflow_uuid"])
                existing = [m for m in ledger["members"] if m["workflow_uuid"] == workflow_uuid]
                if existing and existing != [member]:
                    raise BudgetError("membership_mismatch")
                destination = _workflow_evidence(workflow)
                if destination["workflow_uuid"] != workflow_uuid:
                    raise BudgetError("membership_mismatch")
                proposed = copy.deepcopy(ledger)
                if not existing:
                    if destination.get("review_budget") is not None:
                        raise BudgetError("membership_mismatch")
                    proposed["members"].append(member)
                    proposed["revision"] += 1
                if destination.get("review_budget") is None:
                    _, _, ids = _history_floor(destination)
                    if _has_evidence(destination.get("results")) and not ids:
                        raise BudgetError("migration_required", "blocked")
                    destination["review_budget"] = _projection(proposed, subject, str(path))
                if destination["review_budget"].get("ledger_path") != str(path):
                    raise BudgetError("membership_mismatch")
                reasons = validate_budget_projection(destination, proposed)
                if reasons == ["projection_stale"]:
                    current = _projection(proposed, destination["review_budget"]["subject_id"], str(path))
                    reasons = validate_budget_projection(dict(destination, review_budget=current), proposed)
                if reasons:
                    raise BudgetError("accounting_conflict", "blocked")
                ledger = proposed
                if not existing:
                    _write(path, ledger)
                result.update(status="allowed", projection=_projection(ledger, member["subject_id"], str(path)),
                              ledger_revision=ledger["revision"])
            print(json.dumps(result, allow_nan=False))
            return 0
        if request.get("op") != "init":
            mirror = artifact.get("review_budget")
            if not isinstance(mirror, dict):
                raise BudgetError("migration_required", "blocked")
            path = Path(mirror["ledger_path"])
            if not path.is_absolute() or str(path.resolve()) != str(path):
                raise BudgetError("invalid_ledger_path")
            with _lock(path.with_suffix(".lock")):
                ledger = _read(path)
                _validate_ledger(ledger)
                artifact = _workflow_evidence(workflow)
                if artifact.get("workflow_uuid") != workflow_uuid or artifact.get("review_budget", {}).get("ledger_path") != str(path):
                    raise BudgetError("membership_mismatch")
                reasons = validate_budget_projection(artifact, ledger)
                result.update(projection=_projection(ledger, mirror["subject_id"], str(path)),
                              ledger_revision=ledger["revision"])
                if reasons and not (
                        request["op"] == "reconcile" and reasons == ["projection_stale"] or
                        reasons == ["fresh_pass_required"] and _fresh_proof_operation(ledger, request)):
                    raise BudgetError(reasons[0], "blocked")
                if request["op"] in ("inspect", "reconcile"):
                    result.update(_projection_result(artifact, ledger, mirror["subject_id"], path))
                else:
                    if request.get("workflow_uuid") != workflow_uuid:
                        raise BudgetError("membership_mismatch")
                    evaluated = evaluate_budget(ledger, request)
                    if evaluated["status"] == "allowed":
                        ledger = evaluated["ledger"]
                        _write(path, ledger)
                        result.update(projection=_projection(ledger, mirror["subject_id"], str(path)),
                                      ledger_revision=ledger["revision"])
                    result.update(status=evaluated["status"], reasons=evaluated["reasons"])
                    for key in ("eligible_units", "dispatch", "reservation"):
                        if key in evaluated:
                            result[key] = evaluated[key]
            print(json.dumps(result, allow_nan=False))
            return {"allowed": 0, "blocked": 2, "invalid": 3}[result["status"]]
        lineage, subject = _id(request.get("lineage_id")), _id(request.get("subject_id"))
        path = root / "budgets" / (lineage + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        with _lock(path.with_suffix(".lock")):
            artifact = _workflow_evidence(workflow)
            if artifact["workflow_uuid"] != workflow_uuid:
                raise BudgetError("membership_mismatch")
            if artifact.get("review_budget") is not None:
                raise BudgetError("already_initialized", "blocked")
            if path.exists():
                ledger = _read(path)
                _validate_ledger(ledger)
                if ledger["lineage_id"] != lineage or not any(
                        member["workflow_uuid"] == workflow_uuid and member["subject_id"] == subject
                        for member in ledger["members"]):
                    raise BudgetError("membership_mismatch", "blocked")
                _, _, ids = _history_floor(artifact)
                if (_has_evidence(artifact.get("results")) and not ids and
                        not ledger["opening"]["source_refs"]):
                    raise BudgetError("migration_required", "blocked")
                # Retry only returns the committed state. Policy/migration in
                # the request cannot rewrite an existing ledger or its funding.
                result.update(_projection_result(artifact, ledger, subject, path))
                print(json.dumps(result, allow_nan=False))
                return 0 if result["status"] == "allowed" else 2
            policy = DEFAULT_POLICY.copy()
            policy.update(request.get("policy", {}))
            opening = dict(charged_units=0, counts={}, coverage="complete", source_refs=[])
            floor, units, _ = _history_floor(artifact)
            historical = bool(units or any(floor.values()) or _has_evidence(artifact.get("results")))
            migration = request.get("migration")
            if historical and migration is None:
                raise BudgetError("migration_required", "blocked")
            if migration is not None:
                opening = _reconcile_opening(artifact, migration, subject, policy)
            ledger = dict(version=1, lineage_id=lineage, revision=1, event_count=0,
                          policy=policy, events=[],
                          members=[dict(workflow_uuid=workflow_uuid, subject_id=subject,
                                        source_workflow_uuid=None)],
                          opening=opening)
            _validate_ledger(ledger)
            initialized = _projection_result(artifact, ledger, subject, path)
            _write(path, ledger)
            result.update(initialized)
    except BudgetError as exc:
        result.update(status=exc.status, reasons=[exc.reason])
        result.pop("dispatch", None)
        result.pop("reservation", None)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = dict(status="invalid", reasons=["invalid_io_or_json:" + type(exc).__name__],
                      projection=None, ledger_revision=None)
    print(json.dumps(result, allow_nan=False))
    return {"allowed": 0, "blocked": 2, "invalid": 3}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
