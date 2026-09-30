#!/usr/bin/env python3
"""Measured token usage from Claude Code session transcripts.

Read-only. No network, no writes outside stdout. Complements
`claude plugin details cc10x`, which reports *projected* per-component
costs: this tool reports what sessions *actually consumed*, aggregated
from the assistant `message.usage` records in `<config-dir>/projects/*/
*.jsonl` transcripts.

Scope and honesty:
- cc10x-active is a heuristic: a session counts if any of the marker
  strings appears anywhere in the transcript, so a session that merely
  mentions cc10x also counts.
- Covers main-session transcripts; subagent usage is not verified.

INV-025 (informational only): these numbers may inform context-diet and
optimization work; they must not change routing, approval, remediation,
or phase-advance decisions by themselves. The footer says so on every run.

Usage:
  python3 token_usage_report.py                     # all projects, 20 newest sessions
  python3 token_usage_report.py --project cc10x     # only project dirs matching a substring
  python3 token_usage_report.py --limit 50 --json   # machine-readable
"""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_LIMIT = 20

CC10X_MARKERS = ("cc10x-router", "[CC10x]|entry", ".cc10x/")


def default_projects_dir() -> Path:
    """Honor $CLAUDE_CONFIG_DIR (some machines keep Claude data elsewhere)."""
    config_root = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(config_root) / "projects"


def iter_sessions(projects_dir: Path, project_filter: str | None):
    """Yield (project_name, jsonl_path) newest-first, honoring --project."""
    if not projects_dir.is_dir():
        return
    dirs = sorted(d for d in projects_dir.iterdir() if d.is_dir())
    if project_filter:
        dirs = [d for d in dirs if project_filter.lower() in d.name.lower()]
    for d in dirs:
        for f in sorted(
            d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True
        ):
            yield d.name, f


def scan_session(path: Path) -> dict:
    """Aggregate one session transcript. Malformed lines are skipped, never fatal.

    Claude Code writes one transcript record per streamed content block, and
    every record for the same assistant message carries that message's usage.
    Deduplicate by message.id so each assistant message counts exactly once;
    records without an id are counted as-is.
    """
    turns = 0
    input_tokens = 0
    output_tokens = 0
    cache_read = 0
    cache_creation = 0
    cc10x = False
    first_ts = None
    last_ts = None
    seen_ids = set()

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            if not cc10x and any(m in raw for m in CC10X_MARKERS):
                cc10x = True
            try:
                record = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(record, dict):
                continue
            ts = record.get("timestamp")
            if isinstance(ts, str):
                if first_ts is None:
                    first_ts = ts
                last_ts = ts
            message = record.get("message")
            if not (
                isinstance(message, dict)
                and record.get("type") == "assistant"
                and isinstance(message.get("usage"), dict)
            ):
                continue
            message_id = message.get("id")
            if isinstance(message_id, str):
                if message_id in seen_ids:
                    continue
                seen_ids.add(message_id)
            turns += 1
            usage = message["usage"]
            input_tokens += _num(usage.get("input_tokens"))
            output_tokens += _num(usage.get("output_tokens"))
            cache_read += _num(usage.get("cache_read_input_tokens"))
            cache_creation += _num(usage.get("cache_creation_input_tokens"))

    return {
        "session": path.stem,
        "assistant_turns": turns,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
        "cc10x_active": cc10x,
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
        "bytes": path.stat().st_size,
    }


def _num(value) -> int:
    return value if isinstance(value, (int, float)) else 0


def human(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Measured token usage from Claude Code session transcripts "
            "(cc10x-active is a marker heuristic; main-session transcripts only, "
            "subagent usage not verified)."
        )
    )
    parser.add_argument(
        "--projects-dir",
        type=Path,
        default=None,
        help=(
            "Claude Code projects directory "
            "(default: $CLAUDE_CONFIG_DIR/projects, else ~/.claude/projects)"
        ),
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Only project directories whose sanitized name contains this substring",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"How many sessions to report, newest first (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    projects_dir = args.projects_dir or default_projects_dir()
    if not projects_dir.is_dir():
        print(
            f"token_usage_report: no such projects directory: {projects_dir}",
            file=sys.stderr,
        )
        return 1

    sessions = []
    for _project_name, path in iter_sessions(projects_dir, args.project):
        data = scan_session(path)
        if data["assistant_turns"] > 0 or data["cc10x_active"]:
            sessions.append(data)
        if len(sessions) >= args.limit:
            break

    totals = {
        key: sum(s[key] for s in sessions)
        for key in (
            "assistant_turns",
            "input_tokens",
            "output_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
        )
    }
    cc10x_sessions = sum(1 for s in sessions if s["cc10x_active"])

    if args.json:
        print(
            json.dumps(
                {"sessions": sessions, "totals": totals, "cc10x_sessions": cc10x_sessions},
                indent=2,
            )
        )
        return 0

    if not sessions:
        print("token_usage_report: no sessions with assistant usage records found.")
        return 0

    name_w = max(len(s["session"]) for s in sessions)
    name_w = max(name_w, len("session"))
    print(
        f"{'session':<{name_w}}  turns  cc10x  input    output   cache-read  cache-create"
    )
    for s in sessions:
        flag = "yes" if s["cc10x_active"] else "-"
        print(
            f"{s['session'][:name_w]:<{name_w}}  {s['assistant_turns']:>5}  {flag:>5}"
            f"  {human(s['input_tokens']):>7}  {human(s['output_tokens']):>8}"
            f"  {human(s['cache_read_input_tokens']):>10}"
            f"  {human(s['cache_creation_input_tokens']):>12}"
        )
    n = len(sessions)
    print("-" * 72)
    print(
        f"sessions={n} (cc10x-active={cc10x_sessions})  "
        f"turns={totals['assistant_turns']}  "
        f"input={human(totals['input_tokens'])}  "
        f"output={human(totals['output_tokens'])}  "
        f"cache-read={human(totals['cache_read_input_tokens'])}  "
        f"cache-create={human(totals['cache_creation_input_tokens'])}"
    )
    if n:
        print(
            f"mean/session: turns={totals['assistant_turns'] / n:.1f}  "
            f"cache-read={human(totals['cache_read_input_tokens'] // n)}"
        )
    print(
        "Informational only (INV-025): measured usage may inform context-diet work;"
        " it must not change routing, approval, remediation, or phase-advance decisions."
    )
    print(
        "cc10x-active is a marker heuristic; covers main-session transcripts,"
        " subagent usage not verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
