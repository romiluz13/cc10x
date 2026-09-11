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
    # `research_quality` records EXTERNAL research (web/github via the researcher
    # agent). The QA route never writes it — QA's own lanes land in
    # `results.qa_researchers`. Reporting `research_quality=none` on a QA workflow
    # therefore reads as "research never ran" when eight lanes may be on disk, and a
    # resuming agent cannot tell a real gap from a field that does not apply. Report
    # what the route actually populates.
    workflow_type = payload.get("workflow_type")
    if workflow_type == "QA":
        lanes = (payload.get("results") or {}).get("qa_researchers")
        n = len(lanes) if isinstance(lanes, (list, dict)) else (1 if lanes else 0)
        research_field = f"qa_research_lanes={n or 'none'}"
    else:
        overall_quality = (payload.get("research_quality") or {}).get("overall", "none")
        research_field = f"research_quality={overall_quality}"
    workflow_uuid = payload.get("workflow_uuid") or payload.get("workflow_id")
    message = (
        f"CC10X workflow context ({source}): "
        f"wf={workflow_uuid} type={payload.get('workflow_type')} "
        f"plan={payload.get('plan_file') or 'N/A'} design={payload.get('design_file') or 'N/A'} "
        f"phase_cursor={payload.get('phase_cursor') or 'none'} "
        f"{research_field} pending_gate={pending} "
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
