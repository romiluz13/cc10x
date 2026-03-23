#!/usr/bin/env python3
import json
from datetime import datetime, timezone

from cc10x_hooklib import (
    latest_workflow_payload,
    load_input,
    load_mode,
    log_event,
    workflows_dir,
)


def main() -> int:
    data = load_input()
    trigger = data.get("trigger", "auto")
    summary = data.get("compact_summary", "") or ""
    mode = load_mode()

    payload = latest_workflow_payload()
    if not payload:
        return 0

    wf = payload.get("workflow_uuid") or payload.get("workflow_id")
    events_path = workflows_dir() / f"{wf}.events.jsonl"

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "wf": wf,
        "event": "compact_occurred",
        "phase": "unknown",
        "task_id": None,
        "agent": "hook",
        "decision": "logged",
        "reason": trigger,
        "details": summary[:200] if summary else None,
    }
    try:
        with events_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=True) + "\n")
    except Exception:
        pass  # never fail the hook

    log_event(
        "plugin_postcompact_context",
        {
            "wf": wf,
            "trigger": trigger,
            "summary_len": len(summary),
            "mode": mode.get("postcompactAudit", "audit"),
            "task_id": None,
            "agent": "hook",
            "event": "compact_occurred",
            "decision": "logged",
            "reason": trigger,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
