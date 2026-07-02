#!/usr/bin/env python3
"""Unified event logger — replaces 4 separate log-only hook scripts.

Takes the event name as argv[1], reads stdin JSON, appends a structured
log line to .cc10x/events.jsonl and the hook-events log.
"""
import sys

from cc10x_hooklib import load_input, log_event


def main() -> int:
    event_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    data = load_input()

    if event_name == "postcompact":
        from cc10x_hooklib import workflows_dir, latest_workflow_payload
        import json
        from datetime import datetime, timezone

        trigger = data.get("trigger", "auto")
        summary = data.get("compact_summary", "") or ""
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
            pass
        log_event("plugin_postcompact_context", {
            "wf": wf, "trigger": trigger, "summary_len": len(summary),
            "task_id": None, "agent": "hook", "event": "compact_occurred",
            "decision": "logged", "reason": trigger,
        })
        return 0

    if event_name == "subagent_stop":
        agent_type = data.get("agent_type", "") or ""
        agent_id = data.get("agent_id", "") or ""
        agent_transcript_path = data.get("agent_transcript_path", "") or ""
        stop_hook_active = data.get("stop_hook_active", False)
        message = data.get("last_assistant_message", "") or ""
        contract_found = "CONTRACT {" in message
        is_cc10x_agent = (
            agent_type.startswith("cc10x:")
            or "CC10X" in message
            or "Router Contract" in message
        )
        if not is_cc10x_agent:
            return 0
        log_event("plugin_subagent_stop_audit", {
            "agent_type": agent_type, "agent_id": agent_id,
            "agent_transcript_path": agent_transcript_path,
            "stop_hook_active": stop_hook_active,
            "contract_found": contract_found,
            "message_len": len(message),
            "task_id": None, "agent": agent_type, "event": "subagent_stop",
            "decision": "logged",
            "reason": "contract_present" if contract_found else "contract_missing",
        })
        return 0

    if event_name == "instructions_loaded":
        instructions_hash = data.get("instructions_hash", "")
        instruction_count = data.get("instruction_count", 0)
        log_event("plugin_instructions_loaded_audit", {
            "instructions_hash": instructions_hash,
            "instruction_count": instruction_count,
            "task_id": None, "agent": "hook", "event": "instructions_loaded",
            "decision": "logged", "reason": "audit",
        })
        return 0

    if event_name == "stop_failure":
        stop_hook_active = data.get("stop_hook_active", False)
        log_event("plugin_stop_failure_log", {
            "stop_hook_active": stop_hook_active,
            "task_id": None, "agent": "hook", "event": "stop_failure",
            "decision": "logged", "reason": "stop_hook_failure",
        })
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
