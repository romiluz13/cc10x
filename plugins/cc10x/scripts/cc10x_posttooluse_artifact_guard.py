#!/usr/bin/env python3
"""PostToolUse workflow-artifact integrity guard.

Scope discipline (prevents the stale-artifact footgun):
- When the written file IS a workflow artifact (.cc10x/workflows/*.json,
  not *.events.jsonl), validate THAT file — this is the only case that may
  block (exit 2) in `artifactIntegrity: block` mode.
- For any other Edit/Write, audit the latest workflow artifact for telemetry
  but NEVER block: a malformed or legacy artifact from an old workflow must
  not veto unrelated writes elsewhere in the project.
"""

import sys
from pathlib import Path

from cc10x_hooklib import (
    load_input,
    load_mode,
    log_event,
    now_iso,
    read_latest_workflow_state,
    read_workflow_state,
    workflow_artifact_is_fresh,
    workflow_event_log_append,
    workflow_event_log_exists,
    workflows_dir,
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


def is_workflow_artifact(path: Path) -> bool:
    if path.suffix != ".json" or path.name.endswith(".events.jsonl"):
        return False
    try:
        return path.resolve().parent == workflows_dir().resolve()
    except OSError:
        return False


def main() -> int:
    data = load_input()
    mode = load_mode()
    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    target_is_artifact = is_workflow_artifact(path)

    if target_is_artifact:
        # Validate exactly the artifact that was just written.
        payload, artifact_path, parse_error = read_workflow_state(path.stem)
        if artifact_path is None:
            # File may have been written under a name read_workflow_state cannot
            # resolve; fall back to direct parse via latest-state helper semantics.
            payload, artifact_path, parse_error = read_latest_workflow_state()
            if artifact_path is None or artifact_path.name != path.name:
                return 0
    else:
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

        if target_is_artifact:
            if not payload.get("updated_at"):
                reasons.append("missing-updated-at")
            elif not workflow_artifact_is_fresh(artifact_path):
                reasons.append("stale-artifact-write")

    if not reasons:
        # Fix #2: auto-append event log entry when artifact is mutated.
        # The router instructs the model to append events, but under context
        # pressure the model may skip it. This hook ensures every artifact
        # write gets a matching event log entry.
        if target_is_artifact and payload:
            wf_id = payload.get("workflow_uuid") or payload.get("workflow_id")
            if wf_id:
                workflow_event_log_append(
                    wf_id,
                    {
                        "ts": now_iso(),
                        "wf": wf_id,
                        "event": "artifact_mutated",
                        "phase": payload.get("phase_cursor", "unknown"),
                        "task_id": None,
                        "agent": "hook",
                        "decision": "auto-logged",
                        "reason": "posttool_guard_auto_append",
                    },
                )
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
            "target_is_artifact": target_is_artifact,
            "event": "posttool_artifact_guard",
            "decision": decision if target_is_artifact else "audit",
            "reason": ";".join(reasons),
        },
    )

    # Close the loop in block mode: a corrupt or key-missing artifact (the cases
    # that silently break resume/verifier handoff) must surface to the model, not
    # just the log. Exit code 2 is the PostToolUse blocking signal Claude Code
    # shows back to the model. Blocking applies ONLY when the write target is the
    # artifact itself — never to unrelated files — and only for hard-corruption
    # reasons; the soft reasons (missing-event-log, stale write) stay audit-only.
    blocking_reasons = [
        r for r in reasons if r.startswith(("artifact-json:", "missing-keys:"))
    ]
    if decision == "block" and target_is_artifact and blocking_reasons:
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
