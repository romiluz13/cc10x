#!/usr/bin/env python3
"""Save workflow state snapshot when Claude stops."""
import json

from cc10x_hooklib import (
    load_input,
    log_event,
    now_iso,
    read_latest_workflow_state,
    state_root,
)


def main() -> int:
    try:
        data = load_input()
    except Exception:
        return 0

    # Defensive: never do anything special on continuation stops
    if data.get("stop_hook_active"):
        return 0

    payload, _, parse_error = read_latest_workflow_state()
    if not payload or parse_error:
        return 0

    wf = payload.get("workflow_uuid") or payload.get("workflow_id")
    if not wf:
        return 0

    snapshot = {
        "ts": now_iso(),
        "workflow_uuid": wf,
        "workflow_type": payload.get("workflow_type"),
        "phase_cursor": payload.get("phase_cursor"),
        "phase_status": payload.get("phase_status") or {},
        "plan_file": payload.get("plan_file"),
        "source": "stop",
    }
    try:
        out = state_root() / "precompact-state.json"
        out.write_text(json.dumps(snapshot, ensure_ascii=True), encoding="utf-8")
    except Exception:
        pass  # never fail the hook

    log_event(
        "plugin_stop_persist",
        {
            "wf": wf,
            "phase": payload.get("phase_cursor") or "none",
            "task_id": None,
            "agent": "hook",
            "event": "stop_state_saved",
            "decision": "saved",
            "reason": "session_stop",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
