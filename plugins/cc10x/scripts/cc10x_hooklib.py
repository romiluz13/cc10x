#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = "v11"

_input_cwd: str | None = None


def project_dir() -> Path:
    """CLAUDE_PROJECT_DIR, else the checkout root containing the session cwd
    (a subdirectory of a repository is not its own project), else the cwd."""
    value = os.environ.get("CLAUDE_PROJECT_DIR")
    if value:
        return Path(value)
    base = Path(_input_cwd) if _input_cwd else Path.cwd()
    return git_checkout_root(base) or base


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


def _git_common_dir(root: Path) -> Path | None:
    """The shared .git directory of a checkout: its own `.git` directory, or,
    for a linked worktree (`.git` file), the commondir of the gitdir it names."""
    try:
        dot_git = root / ".git"
        if dot_git.is_dir():
            return dot_git.resolve()
        text = dot_git.read_text(encoding="utf-8").strip()
        if not text.startswith("gitdir:"):
            return None
        gitdir = Path(text[len("gitdir:") :].strip())
        if not gitdir.is_absolute():
            gitdir = root / gitdir
        commondir = gitdir / "commondir"
        if commondir.is_file():
            gitdir = gitdir / commondir.read_text(encoding="utf-8").strip()
        return gitdir.resolve()
    except (OSError, ValueError):
        return None


def _is_project_checkout(root: Path, project: Path) -> bool:
    """`root` is the project directory itself or a linked worktree of its repo."""
    try:
        if root.resolve() == project.resolve():
            return True
    except OSError:
        return False
    common = _git_common_dir(root)
    return common is not None and common == _git_common_dir(project)


def state_root() -> Path:
    """The project's .cc10x dir. Never creates it — guards must not litter
    state dirs into repos that never opted into CC10x. Callers that write
    into an opted-in project use ensure_state_root().

    Precedence: the .cc10x of the git checkout containing the hook input `cwd`
    when that checkout is the project directory or one of its linked worktrees
    (CLAUDE_PROJECT_DIR stays on the main checkout while `cwd` follows Claude
    into a worktree), then CLAUDE_PROJECT_DIR/.cc10x, then
    project_dir()/.cc10x. No other walk-up: a nested repository's or a parent
    directory's stray .cc10x is never selected."""
    if _input_cwd:
        root = git_checkout_root(Path(_input_cwd))
        if (
            root is not None
            and (root / ".cc10x").is_dir()
            and _is_project_checkout(root, project_dir())
        ):
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
    if isinstance(data, dict) and isinstance(data.get("cwd"), str) and data["cwd"]:
        _input_cwd = os.path.abspath(data["cwd"])
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


def _mode_source_path(source: str) -> Path | None:
    if source == "shipped":
        return plugin_config_dir() / "hook-mode.json"
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if source == "override" and data_dir:
        return Path(data_dir) / "hook-mode.json"
    return None


def _report_mode_problem(problem: dict[str, str]) -> None:
    """Log one invalid_hook_mode event per distinct problem, project and
    state of the offending file (path, mtime, size). A marker file under
    .cc10x/state/ carries the dedupe across hook processes; when it cannot be
    read or written the event is simply logged every time."""
    marker: Path | None = None
    try:
        source = _mode_source_path(problem.get("source", ""))
        stamp = ""
        if source is not None:
            info = source.stat()
            stamp = f"{source}|{info.st_mtime_ns}|{info.st_size}"
        fingerprint = "|".join([stamp, *(f"{k}={v}" for k, v in sorted(problem.items()))])
        digest = hashlib.sha1(fingerprint.encode("utf-8", "replace")).hexdigest()[:16]
        marker = state_root() / "state" / f"hook-mode-reported-{digest}"
        if marker.exists():
            return
    except OSError:
        pass
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
    if marker is not None:
        try:
            if logs_dir().is_dir():
                marker.parent.mkdir(exist_ok=True)
                marker.touch()
        except OSError:
            pass


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
    except Exception as exc:
        _report_mode_problem(
            {"source": "load", "reason": f"unexpected:{exc.__class__.__name__}"}
        )
        return dict(HOOK_MODE_DEFAULTS)
    for problem in problems:
        _report_mode_problem(problem)
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


def log_unreadable_artifact(path: Path, error: str) -> None:
    log_event(
        "plugin_workflow_artifact_unreadable",
        {
            "wf": path.stem,
            "phase": "unknown",
            "task_id": None,
            "agent": "hook",
            "event": "workflow_artifact_unreadable",
            "decision": "audit",
            "reason": error,
            "path": str(path),
        },
    )


def latest_workflow_payload() -> dict[str, Any]:
    payload, path, parse_error = read_latest_workflow_state()
    if parse_error and path is not None:
        log_unreadable_artifact(path, parse_error)
    return payload


# The router's own vocabulary for a finished workflow (SKILL.md memory-finalize
# step, workflow skeleton status_history).
TERMINAL_EVENTS = {"memory_finalized", "workflow_completed", "workflow_failed"}
EVENTS_TAIL_BYTES = 65_536


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def _events_log_last(artifact_path: Path) -> tuple[bool, datetime | None] | None:
    """(terminal?, timestamp) of the newest router-written record of the events
    log, or None. Hook-appended records (artifact_mutated, compact_occurred)
    are skipped so the hooks' own bookkeeping after finalization does not hide
    it."""
    log = artifact_path.with_name(f"{artifact_path.stem}.events.jsonl")
    try:
        with log.open("rb") as fh:
            size = fh.seek(0, 2)
            fh.seek(max(0, size - EVENTS_TAIL_BYTES))
            tail = fh.read().decode("utf-8", errors="ignore")
    except OSError:
        return None
    for line in reversed(tail.split("\n")):
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if not isinstance(record, dict) or record.get("agent") == "hook":
            continue
        event = record.get("event")
        terminal = isinstance(event, str) and event in TERMINAL_EVENTS
        return terminal, _parse_ts(record.get("ts"))
    return None


def workflow_is_finished(payload: Any, artifact_path: Path | None = None) -> bool:
    """The router's terminal test (SKILL.md, resume algorithm): a terminal last
    `status_history` event, a terminal newest events-log record, or a
    `memory-finalize` cursor whose phase is completed. When the last
    `status_history` entry and the newest events-log record both carry
    timestamps, the later of the two decides between them; without both
    timestamps either terminal signal counts."""
    if not isinstance(payload, dict):
        return False
    status = payload.get("phase_status")
    if (
        payload.get("phase_cursor") == "memory-finalize"
        and isinstance(status, dict)
        and status.get("memory-finalize") == "completed"
    ):
        return True
    history = payload.get("status_history")
    last = history[-1] if isinstance(history, list) and history else None
    history_terminal = (
        isinstance(last, dict)
        and isinstance(last.get("event"), str)
        and last["event"] in TERMINAL_EVENTS
    )
    from_log = _events_log_last(artifact_path) if artifact_path is not None else None
    if from_log is None:
        return history_terminal
    log_terminal, log_ts = from_log
    history_ts = _parse_ts(last.get("ts")) if isinstance(last, dict) else None
    if history_ts is not None and log_ts is not None and history_ts != log_ts:
        return history_terminal if history_ts > log_ts else log_terminal
    return history_terminal or log_terminal


def _artifacts_newest_first() -> list[Path]:
    def mtime_or_none(path: Path) -> float | None:
        try:
            return path.stat().st_mtime
        except OSError:
            return None  # deleted between glob and stat, or dangling symlink

    stamped = [
        (mtime, p)
        for p in workflows_dir().glob("*.json")
        if safe_workflow_id(p.stem) is not None
        and (mtime := mtime_or_none(p)) is not None
    ]
    return [path for _, path in sorted(stamped, reverse=True)]


def latest_workflow_file() -> Path | None:
    """The newest-mtime workflow artifact, finished or not. Guards that hold a
    standing lock (the QA isolation guard) use this: the newest artifact
    decides, so an abandoned older workflow cannot be resurrected by a newer
    one finishing."""
    artifacts = _artifacts_newest_first()
    return artifacts[0] if artifacts else None


def _scan_live() -> tuple[Path | None, list[tuple[Path, str]]]:
    """Newest-mtime artifact that is not finished, for resume and context
    consumers only (a finished workflow must not shadow a live one), and the
    unreadable artifacts met on the way, newest first. A file that is not a
    workflow artifact (its name is not a workflow id) is never considered."""
    unreadable: list[tuple[Path, str]] = []
    for path in _artifacts_newest_first():
        payload, error = _load_artifact(path)
        if error is not None:
            unreadable.append((path, error))
        elif not workflow_is_finished(payload, path):
            return path, unreadable
    return None, unreadable


def _load_artifact(path: Path) -> tuple[dict[str, Any], str | None]:
    """The artifact object, or `{}` plus the error class. JSON that is not an
    object (`[]`, `5`, `null`) is unreadable, never a payload: every consumer
    calls `.get` on what it gets back."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {}, exc.__class__.__name__
    if not isinstance(payload, dict):
        return {}, "NotAnObject"
    return payload, None


def _read_artifact(path: Path | None) -> tuple[dict[str, Any], Path | None, str | None]:
    if path is None:
        return {}, None, None
    payload, error = _load_artifact(path)
    return payload, path, error


def read_latest_workflow_state() -> tuple[dict[str, Any], Path | None, str | None]:
    return _read_artifact(latest_workflow_file())


def read_live_workflow_state() -> tuple[dict[str, Any], Path | None, str | None]:
    """The newest live artifact. Unreadable artifacts newer than it are logged
    here and skipped; when no artifact is live and one is unreadable, that
    artifact is returned with its error so the caller can report it."""
    live, unreadable = _scan_live()
    if live is not None:
        for path, error in unreadable:
            log_unreadable_artifact(path, error)
        return _read_artifact(live)
    if unreadable:
        path, error = unreadable[0]
        return {}, path, error
    return {}, None, None


SAFE_WORKFLOW_ID = re.compile(r"wf-[A-Za-z0-9._-]+")


def safe_workflow_id(value: Any) -> str | None:
    """The id as a file-name stem, or None: ids read from artifact content
    must not carry path separators into an events-log path."""
    if isinstance(value, str) and SAFE_WORKFLOW_ID.fullmatch(value):
        return value
    return None


def workflow_artifact_path(workflow_id: str | None) -> Path | None:
    workflow_id = safe_workflow_id(workflow_id)
    if not workflow_id:
        return None
    path = workflows_dir() / f"{workflow_id}.json"
    if not path.exists():
        return None
    return path


def workflow_event_log_path(workflow_id: str | None) -> Path | None:
    workflow_id = safe_workflow_id(workflow_id)
    if not workflow_id:
        return None
    path = workflows_dir() / f"{workflow_id}.events.jsonl"
    if not path.exists():
        return None
    return path


def read_workflow_state(
    workflow_id: str | None,
) -> tuple[dict[str, Any], Path | None, str | None]:
    return _read_artifact(workflow_artifact_path(workflow_id))


def workflow_event_log_contains(workflow_id: str | None, needle: str) -> bool:
    path = workflow_event_log_path(workflow_id)
    if path is None:
        return False
    try:
        return needle in path.read_text(encoding="utf-8")
    except Exception:
        return False


def log_dropped_workflow_event(source: str, workflow_id: Any, reason: str) -> None:
    """Say that an event for `workflow_id` was not written. An id that fails
    safe_workflow_id is refused on purpose (it came from artifact or task
    content and must not become a path); the refusal is logged, not silent."""
    unsafe = safe_workflow_id(workflow_id) is None
    name = "workflow_id_unsafe" if unsafe else "workflow_event_append_failed"
    log_event(
        f"plugin_{name}",
        {
            "wf": str(workflow_id)[:80],
            "phase": "unknown",
            "task_id": None,
            "agent": "hook",
            "event": name,
            "decision": "audit",
            "reason": reason,
            "source": source,
        },
    )


def workflow_event_log_append(workflow_id: str | None, event: dict[str, Any]) -> bool:
    """Append a single event to the workflow event log.

    Returns True on success, False on failure. Never raises.
    """
    workflow_id = safe_workflow_id(workflow_id)
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
    workflow_uuid = safe_workflow_id(
        payload.get("workflow_uuid") or payload.get("workflow_id")
    )
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
