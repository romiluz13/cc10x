#!/usr/bin/env python3
from cc10x_hooklib import load_input, load_mode, log_event


def main() -> int:
    data = load_input()
    mode = load_mode()
    agent_type = data.get("agent_type", "") or ""
    agent_id = data.get("agent_id", "") or ""
    agent_transcript_path = data.get("agent_transcript_path", "") or ""
    stop_hook_active = data.get("stop_hook_active", False)
    message = data.get("last_assistant_message", "") or ""
    contract_found = "CONTRACT {" in message

    # Only audit cc10x agents to suppress noise from unrelated subagents
    is_cc10x_agent = (
        agent_type.startswith("cc10x:")
        or "CC10X" in message
        or "Router Contract" in message
    )
    if not is_cc10x_agent:
        return 0

    log_event(
        "plugin_subagent_stop_audit",
        {
            "agent_type": agent_type,
            "agent_id": agent_id,
            "agent_transcript_path": agent_transcript_path,
            "stop_hook_active": stop_hook_active,
            "contract_found": contract_found,
            "message_len": len(message),
            "mode": mode.get("subagentStopAudit", "audit"),
            "task_id": None,
            "agent": agent_type,
            "event": "subagent_stop",
            "decision": "logged",
            "reason": "contract_present" if contract_found else "contract_missing",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
