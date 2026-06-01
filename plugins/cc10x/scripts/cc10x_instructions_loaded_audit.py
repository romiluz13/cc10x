#!/usr/bin/env python3
"""Audit log for instruction file loads."""
from cc10x_hooklib import load_input, log_event


def main() -> int:
    try:
        data = load_input()
    except Exception:
        return 0
    file_path = data.get("file_path", "unknown")
    memory_type = data.get("memory_type", "unknown")
    load_reason = data.get("load_reason", "unknown")

    log_event(
        "plugin_instructions_loaded",
        {
            "wf": None,
            "phase": None,
            "task_id": None,
            "agent": "hook",
            "event": "instructions_loaded",
            "decision": "logged",
            "reason": load_reason,
            "file_path": file_path,
            "memory_type": memory_type,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
