#!/usr/bin/env python3
from cc10x_hooklib import (
    latest_workflow_payload,
    load_input,
    log_event,
    session_context,
)


def main() -> int:
    data = load_input()
    source = data.get("source", "startup")
    payload = latest_workflow_payload()
    if not payload:
        return 0

    pending = payload.get("pending_gate") or "none"
    phase_status = payload.get("phase_status") or {}
    incomplete = [
        name
        for name, status in phase_status.items()
        if status not in {"completed", "skipped"}
    ]
    overall_quality = (payload.get("research_quality") or {}).get("overall", "none")
    workflow_uuid = payload.get("workflow_uuid") or payload.get("workflow_id")
    message = (
        f"CC10X v10 workflow context ({source}): "
        f"wf={workflow_uuid} type={payload.get('workflow_type')} "
        f"plan={payload.get('plan_file') or 'N/A'} design={payload.get('design_file') or 'N/A'} "
        f"phase_cursor={payload.get('phase_cursor') or 'none'} "
        f"research_quality={overall_quality} pending_gate={pending} "
        f"incomplete_phases={', '.join(incomplete) if incomplete else 'none'}."
    )
    log_event(
        "plugin_sessionstart_context",
        {
            "wf": workflow_uuid,
            "phase": ",".join(incomplete) if incomplete else "none",
            "task_id": None,
            "agent": "router",
            "event": "session_context",
            "decision": "inject",
            "reason": source,
        },
    )
    session_context(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
