#!/usr/bin/env python3
"""Log API failure events to workflow event log."""
import json

from cc10x_hooklib import (
    load_input,
    log_event,
    now_iso,
    read_latest_workflow_state,
    workflows_dir,
)


def main() -> int:
    try:
        data = load_input()
    except Exception:
        return 0
    error_type = data.get("error", "unknown")
    error_details = data.get("error_details", "") or ""

    payload, _, _ = read_latest_workflow_state()
    if not payload:
        # No workflow — still log to global hook log
        log_event(
            "plugin_stop_failure",
            {
                "wf": None,
                "phase": None,
                "task_id": None,
                "agent": "hook",
                "event": "stop_failure",
                "decision": "logged",
                "reason": error_type,
            },
        )
        return 0

    wf = payload.get("workflow_uuid") or payload.get("workflow_id")
    events_path = workflows_dir() / f"{wf}.events.jsonl"

    event = {
        "ts": now_iso(),
        "wf": wf,
        "event": "stop_failure",
        "phase": payload.get("phase_cursor") or "unknown",
        "task_id": None,
        "agent": "hook",
        "decision": "logged",
        "reason": error_type,
        "details": error_details[:200] if error_details else None,
    }
    try:
        with events_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=True) + "\n")
    except Exception:
        pass  # fire-and-forget

    log_event(
        "plugin_stop_failure",
        {
            "wf": wf,
            "phase": payload.get("phase_cursor") or "unknown",
            "task_id": None,
            "agent": "hook",
            "event": "stop_failure",
            "decision": "logged",
            "reason": error_type,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
