#!/usr/bin/env python3
from cc10x_hooklib import load_input, load_mode, log_event


def main() -> int:
    data = load_input()
    mode = load_mode()
    agent_type = data.get("agent_type", "") or ""
    message = data.get("last_assistant_message", "") or ""
    contract_found = "CONTRACT {" in message

    log_event(
        "plugin_subagent_stop_audit",
        {
            "agent_type": agent_type,
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
