#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def project_dir() -> Path:
    value = os.environ.get("CLAUDE_PROJECT_DIR")
    if value:
        return Path(value)
    return Path.cwd()


def plugin_root() -> Path:
    value = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if value:
        return Path(value)
    return Path(__file__).resolve().parents[1]


def plugin_config_dir() -> Path:
    return plugin_root() / "config"


def workflows_dir() -> Path:
    path = project_dir() / ".claude" / "cc10x" / "workflows"
    path.mkdir(parents=True, exist_ok=True)
    return path


def logs_dir() -> Path:
    path = project_dir() / ".claude" / "cc10x"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_input() -> Dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def load_mode() -> Dict[str, str]:
    path = plugin_config_dir() / "hook-mode.json"
    if not path.exists():
        return {
            "protectedWrites": "audit",
            "memoryWrites": "audit",
            "taskMetadata": "audit",
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "protectedWrites": "audit",
            "memoryWrites": "audit",
            "taskMetadata": "audit",
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(name: str, payload: Dict[str, Any]) -> None:
    path = logs_dir() / "cc10x-hook-events.log"
    event = {"ts": now_iso(), "event": name, **payload}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=True) + "\n")


def latest_workflow_payload() -> Dict[str, Any]:
    files = sorted(
        workflows_dir().glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if not files:
        return {}
    try:
        return json.loads(files[0].read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_metadata(description: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for line in description.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"wf", "kind", "origin", "phase", "plan", "scope", "reason"}:
            values[key] = value.strip()
    return values


def json_print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=True))


def pretool_deny(reason: str) -> None:
    json_print(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


def session_context(message: str) -> None:
    json_print(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": message,
            }
        }
    )
