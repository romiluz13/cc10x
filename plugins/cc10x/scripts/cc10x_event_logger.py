#!/usr/bin/env python3
"""Unified event logger — replaces 4 separate log-only hook scripts.

Takes the event name as argv[1], reads stdin JSON, appends a structured
log line to the hook-events log (.cc10x/cc10x-hook-events.log); the
postcompact event also appends to the workflow's <wf>.events.jsonl.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from cc10x_hooklib import load_input, log_event

TRANSCRIPT_TAIL_BYTES = 1_048_576


def read_handback_report(transcript_path: str) -> str | None:
    """The report a subagent delivered through SubagentHandback, read from the
    tail of its own transcript. With that tool `last_assistant_message` holds
    only the closing text, not the report (hooks reference, SubagentStop)."""
    if not transcript_path:
        return None
    try:
        path = Path(transcript_path)
        with path.open("rb") as fh:
            fh.seek(max(0, path.stat().st_size - TRANSCRIPT_TAIL_BYTES))
            tail = fh.read().decode("utf-8", errors="ignore")
    except OSError:
        return None
    for line in reversed(tail.splitlines()):
        try:
            content = json.loads(line)["message"]["content"]
        except (ValueError, KeyError, TypeError):
            continue
        if not isinstance(content, list):
            continue
        for block in reversed(content):
            if (
                isinstance(block, dict)
                and block.get("type") == "tool_use"
                and block.get("name") == "SubagentHandback"
            ):
                message = (block.get("input") or {}).get("message")
                if isinstance(message, str):
                    return message
    return None


def main() -> int:
    event_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    data = load_input()

    if event_name == "postcompact":
        from cc10x_hooklib import latest_workflow_payload, workflow_event_log_append
        from datetime import datetime, timezone

        trigger = data.get("trigger", "auto")
        summary = data.get("compact_summary", "") or ""
        payload = latest_workflow_payload()
        if not payload:
            return 0
        wf = payload.get("workflow_uuid") or payload.get("workflow_id")
        if not wf:
            return 0
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
        workflow_event_log_append(wf, event)
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

    if event_name == "subagent_stop":
        agent_type = data.get("agent_type", "") or ""
        agent_id = data.get("agent_id", "") or ""
        agent_transcript_path = data.get("agent_transcript_path", "") or ""
        stop_hook_active = data.get("stop_hook_active", False)
        message = data.get("last_assistant_message", "") or ""
        if not agent_type.startswith("cc10x:"):
            log_event(
                "plugin_subagent_stop_audit",
                {
                    "agent_type": agent_type,
                    "agent_id": agent_id,
                    "task_id": None,
                    "agent": agent_type,
                    "event": "subagent_stop",
                    "decision": "logged",
                    "reason": "non_cc10x_agent",
                },
            )
            return 0
        report = message
        report_source = "last_assistant_message"
        if "CONTRACT {" not in report:
            handback = read_handback_report(agent_transcript_path)
            if handback is not None:
                report = handback
                report_source = "handback_report"
            elif not message:
                report_source = "none"
        contract_found = "CONTRACT {" in report
        log_event(
            "plugin_subagent_stop_audit",
            {
                "agent_type": agent_type,
                "agent_id": agent_id,
                "agent_transcript_path": agent_transcript_path,
                "stop_hook_active": stop_hook_active,
                "contract_found": contract_found,
                "report_source": report_source,
                "message_len": len(message),
                "task_id": None,
                "agent": agent_type,
                "event": "subagent_stop",
                "decision": "logged",
                "reason": "contract_present" if contract_found else "contract_missing",
            },
        )
        return 0

    if event_name == "instructions_loaded":
        log_event(
            "plugin_instructions_loaded_audit",
            {
                "file_path": data.get("file_path", ""),
                "memory_type": data.get("memory_type", ""),
                "load_reason": data.get("load_reason", ""),
                "task_id": None,
                "agent": "hook",
                "event": "instructions_loaded",
                "decision": "logged",
                "reason": "audit",
            },
        )
        return 0

    if event_name == "stop_failure":
        log_event(
            "plugin_stop_failure_log",
            {
                "error": data.get("error", ""),
                "error_details": data.get("error_details", ""),
                "task_id": None,
                "agent": "hook",
                "event": "stop_failure",
                "decision": "logged",
                "reason": "stop_hook_failure",
            },
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
