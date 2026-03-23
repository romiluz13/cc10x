#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

STATE_VERSION = "v10"


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


def state_root() -> Path:
    path = project_dir() / ".claude" / "cc10x" / STATE_VERSION
    path.mkdir(parents=True, exist_ok=True)
    return path


def workflows_dir() -> Path:
    path = state_root() / "workflows"
    path.mkdir(parents=True, exist_ok=True)
    return path


def logs_dir() -> Path:
    path = state_root()
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
    try:
        path = logs_dir() / "cc10x-hook-events.log"
        event = {
            "ts": now_iso(),
            "event": name,
            "state_version": STATE_VERSION,
            **payload,
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=True) + "\n")
    except Exception:
        pass  # never fail the hook


def latest_workflow_payload() -> Dict[str, Any]:
    payload, _, _ = read_latest_workflow_state()
    return payload


def latest_workflow_file() -> Path | None:
    files = sorted(
        workflows_dir().glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if not files:
        return None
    return files[0]


def read_latest_workflow_state() -> Tuple[Dict[str, Any], Path | None, str | None]:
    latest = latest_workflow_file()
    if latest is None:
        return {}, None, None
    try:
        return json.loads(latest.read_text(encoding="utf-8")), latest, None
    except Exception as exc:
        return {}, latest, exc.__class__.__name__


def workflow_event_log_exists(payload: Dict[str, Any], artifact_path: Path) -> bool:
    workflow_uuid = payload.get("workflow_uuid") or payload.get("workflow_id")
    if not workflow_uuid:
        workflow_uuid = artifact_path.stem
    event_log = workflows_dir() / f"{workflow_uuid}.events.jsonl"
    return event_log.exists()


def workflow_artifact_is_fresh(path: Path, max_age_seconds: int = 60) -> bool:
    try:
        age = datetime.now(timezone.utc).timestamp() - path.stat().st_mtime
    except FileNotFoundError:
        return False
    return age <= max_age_seconds


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
