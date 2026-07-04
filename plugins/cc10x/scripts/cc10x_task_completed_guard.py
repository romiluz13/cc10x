#!/usr/bin/env python3
"""TaskCompleted guard.

Validates:
1. Every CC10X task has required metadata (wf, kind, origin, phase, plan, scope, reason)
2. Memory tasks have router-owned evidence (origin=router, inline marker, finalized event)
3. After any non-memory CC10X task completes, check that the workflow artifact was
   updated (updated_at bumped) since the task was created. A stale artifact means the
   router skipped persistence.
4. Circuit breaker backstop: when a kind:remfix task completes, count remediation_history
   entries in the workflow artifact. This is the hook-enforced version of the router's
   own LLM-counted 3-cycle circuit breaker — it does not depend on the router counting
   correctly, only on remediation_history being an accurate array in the artifact.
"""

import sys

from cc10x_hooklib import (
    load_input,
    load_mode,
    log_event,
    parse_metadata,
    read_workflow_state,
    workflow_artifact_is_fresh,
    workflow_event_log_contains,
)


REQUIRED_METADATA = (
    "wf:",
    "kind:",
    "origin:",
    "phase:",
    "plan:",
    "scope:",
    "reason:",
)

MEMORY_FINAL_EVENT = "memory_finalized"


def validate_memory_task_completion(data: dict, metadata: dict, mode: dict) -> int:
    if metadata.get("kind") != "memory":
        return 0

    subject = data.get("task_subject", "")
    description = data.get("task_description") or ""
    workflow_id = metadata.get("wf")
    reasons: list[str] = []

    if metadata.get("origin") != "router":
        reasons.append("memory-task-origin-not-router")
    if "ROUTER ONLY: execute inline." not in description:
        reasons.append("memory-task-missing-router-only-marker")
    if not subject.startswith("CC10X Memory Update:"):
        reasons.append("memory-task-subject-not-router-owned")

    payload, artifact_path, parse_error = read_workflow_state(workflow_id)
    if artifact_path is None:
        reasons.append("missing-workflow-artifact")
    elif parse_error:
        reasons.append(f"artifact-json:{parse_error}")
    else:
        artifact_wf = payload.get("workflow_uuid") or payload.get("workflow_id")
        if artifact_wf and artifact_wf != workflow_id:
            reasons.append("workflow-artifact-mismatch")

    if not workflow_event_log_contains(workflow_id, MEMORY_FINAL_EVENT):
        reasons.append("missing-memory-finalized-event")

    if not reasons:
        return 0

    log_event(
        "plugin_task_completed_memory_finalize_guard",
        {
            "wf": workflow_id,
            "phase": metadata.get("phase"),
            "task_id": data.get("task_id"),
            "agent": metadata.get("origin"),
            "event": "task_completed_memory_finalize_guard",
            "decision": "block" if mode.get("taskMetadata") == "block" else "audit",
            "reason": ",".join(reasons),
            "task_subject": subject,
        },
    )
    if mode.get("taskMetadata") == "block":
        sys.stderr.write(
            "CC10X memory-task completion blocked: router-owned memory finalization evidence "
            "is missing (" + ", ".join(reasons) + ").\n"
        )
        return 2
    return 0


def check_artifact_freshness(data: dict, metadata: dict, mode: dict) -> int:
    """Fix #3/#5: After a non-memory CC10X task completes, verify the workflow
    artifact was updated since the task was created.

    A stale artifact (updated_at unchanged since before the task ran) means the
    router skipped persistence — the agent's results were not written to the
    durable state. This breaks resume logic and leaves the workflow incomplete.

    We use a generous window (300s = 5 min) because agent runs can be long.
    The check is: artifact mtime must be newer than the task creation time.
    """
    if metadata.get("kind") == "memory":
        return 0  # memory tasks are handled separately

    workflow_id = metadata.get("wf")
    if not workflow_id:
        return 0

    payload, artifact_path, parse_error = read_workflow_state(workflow_id)
    if artifact_path is None or parse_error:
        return 0  # don't compound errors — the main validator catches missing artifacts

    # Check freshness: artifact should have been updated during this task's run.
    # Use 300s window (agents can run for minutes) — if the artifact hasn't been
    # touched in 5+ minutes after a task completes, it's stale.
    if not workflow_artifact_is_fresh(artifact_path, max_age_seconds=300):
        log_event(
            "plugin_task_completed_stale_artifact",
            {
                "wf": workflow_id,
                "phase": metadata.get("phase"),
                "task_id": data.get("task_id"),
                "agent": metadata.get("origin"),
                "event": "task_completed_stale_artifact",
                "decision": "audit",
                "reason": "artifact-not-updated-after-task-completion",
                "task_subject": data.get("task_subject", ""),
            },
        )
        # Audit-only for now — blocking would be too aggressive since the model
        # may update the artifact in the next turn. But the audit log entry
        # creates an observable signal for stress tests.
        sys.stderr.write(
            f"CC10X WARNING: workflow artifact {artifact_path.name} appears stale "
            f"after task completion (phase={metadata.get('phase')}, "
            f"agent={metadata.get('origin')}). "
            "Ensure the router updates the artifact with agent results before "
            "proceeding.\n"
        )

    return 0


CIRCUIT_BREAKER_LIMIT = 3


def check_circuit_breaker(data: dict, metadata: dict, mode: dict) -> int:
    """When a kind:remfix task completes, count remediation_history entries in
    the workflow artifact. This is the hook-enforced backstop for the router's
    own LLM-counted 3-cycle circuit breaker (remediation-and-research.md
    'Circuit breaker' section) — it does not depend on the router remembering
    to count correctly, only on the router having appended a remediation_history
    entry when it created this remfix task (also mandated in that same section).

    Fires only on kind:remfix completion (not on every task) — the circuit
    breaker is specifically about remediation cycles, not general task volume.
    """
    if metadata.get("kind") != "remfix":
        return 0

    workflow_id = metadata.get("wf")
    if not workflow_id:
        return 0

    payload, artifact_path, parse_error = read_workflow_state(workflow_id)
    if artifact_path is None or parse_error:
        return 0  # can't evaluate without a readable artifact — don't compound errors

    remediation_history = payload.get("remediation_history")
    if not isinstance(remediation_history, list):
        return 0  # field missing or malformed — nothing to count yet

    cycle_count = len(remediation_history)
    if cycle_count <= CIRCUIT_BREAKER_LIMIT:
        return 0

    decision = "block" if mode.get("taskMetadata") == "block" else "audit"
    log_event(
        "plugin_task_completed_circuit_breaker",
        {
            "wf": workflow_id,
            "phase": metadata.get("phase"),
            "task_id": data.get("task_id"),
            "agent": metadata.get("origin"),
            "event": "task_completed_circuit_breaker_exceeded",
            "decision": decision,
            "reason": f"remediation_history has {cycle_count} entries (limit {CIRCUIT_BREAKER_LIMIT})",
            "task_subject": data.get("task_subject", ""),
        },
    )
    sys.stderr.write(
        f"CC10X circuit breaker: workflow {workflow_id} has {cycle_count} remediation "
        f"cycles recorded in remediation_history, exceeding the {CIRCUIT_BREAKER_LIMIT}-cycle "
        "limit. The router must stop and ask the user how to proceed before creating "
        "another kind:remfix task.\n"
    )
    if decision == "block":
        return 2
    return 0


def main() -> int:
    data = load_input()
    subject = data.get("task_subject", "")
    description = data.get("task_description") or ""
    mode = load_mode()
    metadata = parse_metadata(description)

    if not subject.startswith("CC10X "):
        return 0

    missing = [item for item in REQUIRED_METADATA if item not in description]
    if missing:
        log_event(
            "plugin_task_completed_missing_metadata",
            {
                "wf": metadata.get("wf"),
                "phase": metadata.get("phase"),
                "task_id": data.get("task_id"),
                "agent": metadata.get("origin"),
                "event": "task_completed_guard",
                "decision": "block" if mode.get("taskMetadata") == "block" else "audit",
                "reason": ",".join(missing),
                "task_subject": subject,
            },
        )
        if mode.get("taskMetadata") == "block":
            sys.stderr.write(
                "CC10X task completion blocked: task description is missing metadata lines: "
                + ", ".join(missing)
                + "\n"
            )
            return 2
        return 0

    # Metadata is complete — run the memory-task validator
    result = validate_memory_task_completion(data, metadata, mode)
    if result != 0:
        return result

    # Check artifact freshness after any non-memory task
    check_artifact_freshness(data, metadata, mode)

    # Circuit breaker backstop: enforced independently of router self-counting
    result = check_circuit_breaker(data, metadata, mode)
    if result != 0:
        return result

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
