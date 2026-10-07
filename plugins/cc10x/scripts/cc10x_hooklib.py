#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = "v11"

_input_cwd: str | None = None


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


def git_checkout_root(start: Path) -> Path | None:
    """Nearest ancestor of `start` (itself included) holding a `.git` entry,
    file (worktree) or directory."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def state_root() -> Path:
    """The project's .cc10x dir. Never creates it — guards must not litter
    state dirs into repos that never opted into CC10x. Callers that write
    into an opted-in project use ensure_state_root().

    Precedence: the .cc10x of the git checkout or worktree containing the hook
    input `cwd` (CLAUDE_PROJECT_DIR stays on the main checkout while `cwd`
    follows Claude into a worktree), then CLAUDE_PROJECT_DIR/.cc10x, then
    project_dir()/.cc10x. No other walk-up: a stray nested .cc10x is never
    selected."""
    if _input_cwd:
        root = git_checkout_root(Path(_input_cwd))
        if root is not None and (root / ".cc10x").is_dir():
            return root / ".cc10x"
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir and (Path(env_dir) / ".cc10x").is_dir():
        return Path(env_dir) / ".cc10x"
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
    global _input_cwd
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return {}
    if isinstance(data, dict) and isinstance(data.get("cwd"), str):
        _input_cwd = data["cwd"]
    return data


HOOK_MODE_DEFAULTS = {
    "artifactIntegrity": "block",
    "memoryWrites": "audit",
    "taskMetadata": "audit",
}
HOOK_MODE_VALUES = ("block", "audit")
_MODE_MISSING = object()
_MODE_CORRUPT = object()


def resolve_hook_mode(
    layers: list[tuple[str, Any]],
) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Merge parsed hook-mode layers (lowest precedence first) over
    HOOK_MODE_DEFAULTS. Always returns exactly the default keys, each `block`
    or `audit`; an invalid layer or value is skipped, so that key keeps the
    value from the layer below, and is reported as a problem."""
    modes = dict(HOOK_MODE_DEFAULTS)
    problems: list[dict[str, str]] = []
    for source, layer in layers:
        if layer is _MODE_MISSING:
            continue
        if layer is _MODE_CORRUPT or not isinstance(layer, dict):
            problems.append({"source": source, "reason": "not-a-json-object"})
            continue
        for key, value in layer.items():
            if key not in HOOK_MODE_DEFAULTS:
                continue
            if isinstance(value, str) and value in HOOK_MODE_VALUES:
                modes[key] = value
            else:
                problems.append(
                    {"source": source, "key": key, "reason": "invalid-value"}
                )
    return modes, problems


def _read_mode_layer(path: Path) -> Any:
    if not path.exists():
        return _MODE_MISSING
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _MODE_CORRUPT


def load_mode() -> dict[str, str]:
    """Shipped config/hook-mode.json, then the user override at
    ${CLAUDE_PLUGIN_DATA}/hook-mode.json (survives plugin updates). Never
    raises; invalid input falls back per key and logs invalid_hook_mode."""
    try:
        layers = [("shipped", _read_mode_layer(plugin_config_dir() / "hook-mode.json"))]
        data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
        if data_dir:
            layers.append(("override", _read_mode_layer(Path(data_dir) / "hook-mode.json")))
        modes, problems = resolve_hook_mode(layers)
    except Exception:
        return dict(HOOK_MODE_DEFAULTS)
    for problem in problems:
        log_event(
            "invalid_hook_mode",
            {
                **problem,
                "task_id": None,
                "agent": "hook",
                "event": "invalid_hook_mode",
                "decision": "fallback",
            },
        )
    return modes


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
