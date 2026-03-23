#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from cc10x_hooklib import latest_workflow_payload, load_input, log_event


def main() -> int:
    data = load_input()
    trigger = data.get("trigger", "auto")
    summary = data.get("compact_summary", "") or ""

    payload = latest_workflow_payload()
    if not payload:
        return 0

    wf = payload.get("workflow_uuid") or payload.get("workflow_id")
    state_root = payload.get("state_root", ".claude/cc10x/v10")
    events_path = (
        Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
        / state_root
        / "workflows"
        / f"{wf}.events.jsonl"
    )

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
