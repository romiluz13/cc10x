#!/usr/bin/env python3
"""Self-contained test for tools/token_usage_report.py.

No framework: builds a throwaway Claude-config tree with two synthetic
project directories and four session transcripts, runs the report via
subprocess in --json mode, and asserts the aggregation:

  - usage summed per session and in totals
  - duplicate message.id records (Claude Code emits one record per streamed
    content block) counted exactly once; id-less records counted as-is
  - cc10x detection via the raw-line markers
  - malformed lines skipped, never fatal
  - sessions with no assistant turns and no cc10x marker are excluded
  - JSON output carries no local filesystem paths
  - default projects dir honors $CLAUDE_CONFIG_DIR
  - text mode exits 0 and carries the INV-025 footer

Lives in scripts/ because the repo's .gitignore tracks .py only under scripts/.
Run:  python3 test_cc10x_token_usage_report.py    (exit 0 = pass)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "token_usage_report.py"


def assistant_record(
    ts: str, inp: int, out: int, cread: int, ccreate: int, msg_id: str | None = None
) -> str:
    message = {
        "usage": {
            "input_tokens": inp,
            "output_tokens": out,
            "cache_read_input_tokens": cread,
            "cache_creation_input_tokens": ccreate,
        }
    }
    if msg_id is not None:
        message["id"] = msg_id
    return json.dumps(
        {"type": "assistant", "timestamp": ts, "message": message}
    )


def make_tree(root: Path) -> None:
    projects = root / "projects"
    cc10x_dir = projects / "-Users-x-dev-cc10x"
    plain_dir = projects / "-Users-x-dev-plain"
    cc10x_dir.mkdir(parents=True)
    plain_dir.mkdir(parents=True)

    # Session A: cc10x-active, 3 counted assistant messages, one malformed line,
    # one user line, and a duplicate-id pair that must count once.
    (cc10x_dir / "session-a.jsonl").write_text(
        "\n".join(
            [
                # same message.id streamed as two content blocks -> counted once
                assistant_record("2026-09-30T10:00:00Z", 10, 100, 5000, 200, "msg-1"),
                assistant_record("2026-09-30T10:00:00Z", 10, 100, 5000, 200, "msg-1"),
                json.dumps({"type": "user", "timestamp": "2026-09-30T10:01:00Z"}),
                "{not valid json",
                assistant_record("2026-09-30T10:02:00Z", 20, 200, 6000, 300, "msg-2"),
                json.dumps(
                    {
                        "type": "assistant",
                        "timestamp": "2026-09-30T10:03:00Z",
                        "message": {"text": "dispatching cc10x-router"},
                    }
                ),
                # no message.id -> counted as-is
                assistant_record("2026-09-30T10:04:00Z", 30, 300, 7000, 400),
            ]
        )
        + "\n"
    )

    # Session B: plain project, 1 assistant turn, no cc10x marker.
    (plain_dir / "session-b.jsonl").write_text(
        assistant_record("2026-09-30T11:00:00Z", 5, 50, 1000, 100, "msg-b1") + "\n"
    )

    # Session C: user chatter only — no assistant usage, no marker. Must be excluded.
    (plain_dir / "session-c.jsonl").write_text(
        json.dumps({"type": "user", "timestamp": "2026-09-30T12:00:00Z"}) + "\n"
    )

    # Session D: cc10x marker but zero usage records — kept (cc10x_active), turns 0.
    (cc10x_dir / "session-d.jsonl").write_text(
        json.dumps({"type": "system", "text": ".cc10x/workflows probe"}) + "\n"
    )


def check(label: str, cond: bool) -> None:
    if not cond:
        print(f"FAIL: {label}")
        sys.exit(1)
    print(f"  ok: {label}")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        make_tree(root)

        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--projects-dir",
                str(root / "projects"),
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        check("json mode exits 0", proc.returncode == 0)
        data = json.loads(proc.stdout)
        by_session = {s["session"]: s for s in data["sessions"]}

        check("session A present", "session-a" in by_session)
        a = by_session["session-a"]
        check(
            "A turns=3 (duplicate-id pair counted once; id-less record kept)",
            a["assistant_turns"] == 3,
        )
        check("A input=60 (no double count)", a["input_tokens"] == 60)
        check("A output=600", a["output_tokens"] == 600)
        check("A cache_read=18000", a["cache_read_input_tokens"] == 18000)
        check("A cache_creation=900", a["cache_creation_input_tokens"] == 900)
        check("A cc10x detected via raw-line marker", a["cc10x_active"] is True)
        check("A timestamps spanned", a["first_timestamp"] == "2026-09-30T10:00:00Z"
              and a["last_timestamp"] == "2026-09-30T10:04:00Z")
        check("A JSON carries no local path", "file" not in a)

        check("session B present", "session-b" in by_session)
        b = by_session["session-b"]
        check("B not cc10x", b["cc10x_active"] is False)
        check("B turns=1", b["assistant_turns"] == 1)

        check("session C excluded (no turns, no marker)", "session-c" not in by_session)

        check("session D kept (marker, zero turns)", "session-d" in by_session)
        check("D turns=0", by_session["session-d"]["assistant_turns"] == 0)

        t = data["totals"]
        check("totals turns=4", t["assistant_turns"] == 4)
        check("totals cache_read=19000", t["cache_read_input_tokens"] == 19000)
        check("cc10x_sessions=2", data["cc10x_sessions"] == 2)

        # --project filter
        proc_f = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--projects-dir",
                str(root / "projects"),
                "--project",
                "cc10x",
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        names = {s["session"] for s in json.loads(proc_f.stdout)["sessions"]}
        check("--project filters to cc10x dir only", names == {"session-a", "session-d"})

        # text mode + footer
        proc_t = subprocess.run(
            [sys.executable, str(SCRIPT), "--projects-dir", str(root / "projects")],
            capture_output=True,
            text=True,
        )
        check("text mode exits 0", proc_t.returncode == 0)
        check(
            "INV-025 footer present",
            "Informational only (INV-025)" in proc_t.stdout,
        )

        # missing directory
        proc_m = subprocess.run(
            [sys.executable, str(SCRIPT), "--projects-dir", str(root / "nope")],
            capture_output=True,
            text=True,
        )
        check("missing projects dir exits 1", proc_m.returncode == 1)

        # default path honors $CLAUDE_CONFIG_DIR
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(root))
        proc_e = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            capture_output=True,
            text=True,
            env=env,
        )
        check("CLAUDE_CONFIG_DIR default exits 0", proc_e.returncode == 0)
        names_e = {s["session"] for s in json.loads(proc_e.stdout)["sessions"]}
        check(
            "CLAUDE_CONFIG_DIR default reads its projects dir",
            names_e == {"session-a", "session-b", "session-d"},
        )

    print("token_usage_report test: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
