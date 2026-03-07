#!/usr/bin/env python3
from pathlib import Path

from cc10x_hooklib import load_input, load_mode, log_event, pretool_deny, project_dir


PROTECTED_MEMORY_FILES = ("activeContext.md", "patterns.md", "progress.md")


def main() -> int:
    data = load_input()
    mode = load_mode()
    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    root = project_dir().resolve()
    path = Path(file_path).resolve()
    violations = []

    protected_memory = {
        root / ".claude" / "cc10x" / name for name in PROTECTED_MEMORY_FILES
    }

    if path in protected_memory:
        violations.append("memory-write")

    if not violations:
        return 0

    log_event(
        "plugin_pretooluse_guard",
        {
            "tool_name": data.get("tool_name"),
            "path": str(path),
            "violations": violations,
        },
    )

    should_block = "memory-write" in violations and mode.get("memoryWrites") == "block"
    if should_block:
        pretool_deny(
            "CC10X plugin hook blocked a direct memory markdown write. Use the router-owned memory finalization path."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
