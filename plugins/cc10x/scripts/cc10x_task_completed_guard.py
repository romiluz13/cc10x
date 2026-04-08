#!/usr/bin/env python3
import sys

from cc10x_hooklib import (
    load_input,
    load_mode,
    log_event,
    parse_metadata,
    read_workflow_state,
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


def main() -> int:
    data = load_input()
    subject = data.get("task_subject", "")
    description = data.get("task_description") or ""
    mode = load_mode()
    metadata = parse_metadata(description)

    if not subject.startswith("CC10X "):
        return 0

    missing = [item for item in REQUIRED_METADATA if item not in description]
    if not missing:
        return validate_memory_task_completion(data, metadata, mode)

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


if __name__ == "__main__":
    raise SystemExit(main())
