#!/usr/bin/env python3
import sys
from pathlib import Path

from cc10x_hooklib import (
    load_input,
    load_mode,
    log_event,
    read_latest_workflow_state,
    workflow_artifact_is_fresh,
    workflow_event_log_exists,
)


REQUIRED_WORKFLOW_KEYS = (
    "workflow_uuid",
    "workflow_id",
    "workflow_type",
    "state_root",
    "phase_cursor",
    "task_ids",
    "results",
    "intent",
    "evidence",
    "quality",
    "status_history",
    "remediation_history",
)


def main() -> int:
    data = load_input()
    mode = load_mode()
    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    payload, artifact_path, parse_error = read_latest_workflow_state()
    if artifact_path is None:
        return 0

    reasons: list[str] = []
    if parse_error:
        reasons.append(f"artifact-json:{parse_error}")
    else:
        missing = [key for key in REQUIRED_WORKFLOW_KEYS if key not in payload]
        if missing:
            reasons.append("missing-keys:" + ",".join(missing))

        if not workflow_event_log_exists(payload, artifact_path):
            reasons.append("missing-event-log")

        if path.suffix == ".json" and path.name == artifact_path.name:
            if not payload.get("updated_at"):
                reasons.append("missing-updated-at")
            elif not workflow_artifact_is_fresh(artifact_path):
                reasons.append("stale-artifact-write")

    if not reasons:
        return 0

    decision = mode.get("artifactIntegrity", "audit")
    log_event(
        "plugin_posttooluse_artifact_guard",
        {
            "wf": (
                (payload.get("workflow_uuid") or payload.get("workflow_id"))
                if payload
                else None
            ),
            "phase": (payload or {}).get("pending_gate") or "unknown",
            "task_id": None,
            "agent": "router",
            "tool_name": data.get("tool_name"),
            "path": str(path),
            "event": "posttool_artifact_guard",
            "decision": decision,
            "reason": ";".join(reasons),
        },
    )

    # Close the loop in block mode: a corrupt or key-missing artifact (the cases
    # that silently break resume/verifier handoff) must surface to the model, not
    # just the log. Exit code 2 is the PostToolUse blocking signal Claude Code
    # shows back to the model. Only hard-corruption reasons block; the soft
    # reasons (missing-event-log, stale write) stay audit-only to avoid false stops.
    blocking_reasons = [
        r for r in reasons if r.startswith("artifact-json:") or r.startswith("missing-keys:")
    ]
    if decision == "block" and blocking_reasons:
        print(
            "CC10X artifact integrity guard: the workflow artifact "
            f"{artifact_path.name} is invalid ({';'.join(blocking_reasons)}). "
            "Rewrite it from references/workflow-artifact.skeleton.json before "
            "creating child tasks.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
