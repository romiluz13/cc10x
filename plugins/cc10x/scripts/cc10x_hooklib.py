#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = "v11"


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
    """The project's .cc10x dir. Never creates it — guards must not litter
    state dirs into repos that never opted into CC10x. Callers that write
    into an opted-in project use ensure_state_root()."""
    return project_dir() / ".cc10x"


def ensure_state_root() -> Path:
    path = state_root()
    path.mkdir(parents=True, exist_ok=True)
    return path


def workflows_dir() -> Path:
    return state_root() / "workflows"


def logs_dir() -> Path:
    return state_root()


def load_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return {}


def load_mode() -> dict[str, str]:
    path = plugin_config_dir() / "hook-mode.json"
    if not path.exists():
        return {
            "memoryWrites": "audit",
            "taskMetadata": "audit",
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "memoryWrites": "audit",
            "taskMetadata": "audit",
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(name: str, payload: dict[str, Any]) -> None:
    try:
        if not logs_dir().is_dir():
            return  # not a CC10x project — never create state dirs to log
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


def latest_workflow_payload() -> dict[str, Any]:
    payload, _, _ = read_latest_workflow_state()
    return payload


def latest_workflow_file() -> Path | None:
    def mtime_or_none(path: Path) -> float | None:
        try:
            return path.stat().st_mtime
        except OSError:
            return None  # deleted between glob and stat, or dangling symlink

    stamped = [
        (mtime, p)
        for p in workflows_dir().glob("*.json")
        if (mtime := mtime_or_none(p)) is not None
    ]
    if not stamped:
        return None
    return max(stamped)[1]


def read_latest_workflow_state() -> tuple[dict[str, Any], Path | None, str | None]:
    latest = latest_workflow_file()
    if latest is None:
        return {}, None, None
    try:
        return json.loads(latest.read_text(encoding="utf-8")), latest, None
    except Exception as exc:
        return {}, latest, exc.__class__.__name__


def workflow_artifact_path(workflow_id: str | None) -> Path | None:
    if not workflow_id:
        return None
    path = workflows_dir() / f"{workflow_id}.json"
    if not path.exists():
        return None
    return path


def workflow_event_log_path(workflow_id: str | None) -> Path | None:
    if not workflow_id:
        return None
    path = workflows_dir() / f"{workflow_id}.events.jsonl"
    if not path.exists():
        return None
    return path


def read_workflow_state(
    workflow_id: str | None,
) -> tuple[dict[str, Any], Path | None, str | None]:
    path = workflow_artifact_path(workflow_id)
    if path is None:
        return {}, None, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), path, None
    except Exception as exc:
        return {}, path, exc.__class__.__name__


def workflow_event_log_contains(workflow_id: str | None, needle: str) -> bool:
    path = workflow_event_log_path(workflow_id)
    if path is None:
        return False
    try:
        return needle in path.read_text(encoding="utf-8")
    except Exception:
        return False


def workflow_event_log_append(workflow_id: str | None, event: dict[str, Any]) -> bool:
    """Append a single event to the workflow event log.

    Returns True on success, False on failure. Never raises.
    """
    if not workflow_id:
        return False
    path = workflows_dir() / f"{workflow_id}.events.jsonl"
    try:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=True) + "\n")
        return True
    except Exception:
        return False


def workflow_event_log_count(workflow_id: str | None) -> int:
    """Count the number of lines in the event log."""
    path = workflow_event_log_path(workflow_id)
    if path is None:
        return 0
    try:
        with path.open("r", encoding="utf-8") as fh:
            return sum(1 for _ in fh)
    except Exception:
        return 0


def workflow_event_log_exists(payload: dict[str, Any], artifact_path: Path) -> bool:
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


def parse_metadata(description: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in description.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"wf", "kind", "origin", "phase", "plan", "scope", "reason"}:
            values[key] = value.strip()
    return values


def json_print(payload: dict[str, Any]) -> None:
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
