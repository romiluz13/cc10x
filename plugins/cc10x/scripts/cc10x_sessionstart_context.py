#!/usr/bin/env python3
import json

from cc10x_hooklib import load_input, session_context, workflows_dir


def main() -> int:
    data = load_input()
    source = data.get("source", "startup")
    workflow_files = sorted(
        workflows_dir().glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if not workflow_files:
        return 0

    try:
        payload = json.loads(workflow_files[0].read_text(encoding="utf-8"))
    except Exception:
        return 0

    pending = payload.get("pending_gate") or "none"
    phase_status = payload.get("phase_status") or {}
    incomplete = [
        name
        for name, status in phase_status.items()
        if status not in {"completed", "skipped"}
    ]
    overall_quality = (payload.get("research_quality") or {}).get("overall", "none")
    message = (
        f"CC10X plugin workflow context ({source}): "
        f"wf={payload.get('workflow_id')} type={payload.get('workflow_type')} "
        f"plan={payload.get('plan_file') or 'N/A'} design={payload.get('design_file') or 'N/A'} "
        f"research_quality={overall_quality} pending_gate={pending} "
        f"incomplete_phases={', '.join(incomplete) if incomplete else 'none'}."
    )
    session_context(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
