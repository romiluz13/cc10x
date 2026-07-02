#!/usr/bin/env python3
"""Unified state persistence — handles PreCompact and Stop events.

Replaces cc10x_precompact_state.py and cc10x_stop_persist.py.
Takes event type as argv[1].
"""
import json
import sys

from cc10x_hooklib import (
    load_input,
    log_event,
    now_iso,
    read_latest_workflow_state,
    state_root,
)


def main() -> int:
    event_type = sys.argv[1] if len(sys.argv) > 1 else "stop"

    try:
        data = load_input()
    except Exception:
        return 0

    # Defensive: never do anything special on continuation stops
    if event_type == "stop" and data.get("stop_hook_active"):
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
        "source": event_type,
    }

    output_file = "precompact-state.json" if event_type == "precompact" else "stop-state.json"

    try:
        out = state_root() / output_file
        out.write_text(json.dumps(snapshot, ensure_ascii=True), encoding="utf-8")
    except Exception:
        pass  # never fail the hook

    log_event(
        f"plugin_{event_type}_persist",
        {
            "wf": wf,
            "phase": payload.get("phase_cursor") or "none",
            "task_id": None,
            "agent": "hook",
            "event": f"{event_type}_state_saved",
            "decision": "saved",
            "reason": f"session_{event_type}",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
