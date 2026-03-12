#!/usr/bin/env python3
import sys

from cc10x_hooklib import load_input, load_mode, log_event, parse_metadata


REQUIRED_METADATA = (
    "wf:",
    "kind:",
    "origin:",
    "phase:",
    "plan:",
    "scope:",
    "reason:",
)


def main() -> int:
    data = load_input()
    subject = data.get("task_subject", "")
    description = data.get("task_description") or ""
    mode = load_mode()
    metadata = parse_metadata(description)

    if not subject.startswith("CC10X "):
        return 0

    missing = [item for item in REQUIRED_METADATA if item not in description]
    if not missing:
        return 0

    log_event(
        "plugin_task_completed_missing_metadata",
        {
            "wf": metadata.get("wf"),
            "phase": metadata.get("phase"),
            "task_id": data.get("task_id"),
            "agent": metadata.get("origin"),
            "event": "task_completed_guard",
            "decision": "block" if mode.get("taskMetadata") == "block" else "audit",
            "reason": ",".join(missing),
            "task_subject": subject,
        },
    )
    if mode.get("taskMetadata") == "block":
        sys.stderr.write(
            "CC10X task completion blocked: task description is missing metadata lines: "
            + ", ".join(missing)
            + "\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
