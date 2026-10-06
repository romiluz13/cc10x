#!/usr/bin/env python3
"""Live probe: does `cc10x:agent-common` reach a dispatched cc10x agent?

Runs a headless `claude -p` session from a temp cwd outside the repo with the
plugin dir loaded and a debug file, dispatches the named agent, then greps the
debug log. Exit 0 only when the preload line is present and no not-found or
disabled warning for the skill is logged. Calls a model: never part of the gate.

Usage:
  python3 plugins/cc10x/tools/preload_probe.py --agent component-builder
  python3 plugins/cc10x/tools/preload_probe.py --all [--plugin-dir DIR] [--model haiku]
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL = "cc10x:agent-common"
PRELOADED = re.compile(r"Preloaded skill '" + re.escape(SKILL) + r"'")
WARNING = re.compile(
    r"Warning: Skill '" + re.escape(SKILL) + r"'.*(not found|disabled)", re.I
)
MAX_BUDGET_USD = "0.60"
TIMEOUT_S = 300


def agent_names(plugin_dir: Path) -> list[str]:
    names = []
    for path in sorted((plugin_dir / "agents").glob("*.md")):
        head = path.read_text(encoding="utf-8").split("---", 2)
        if len(head) > 2 and SKILL in head[1]:
            names.append(path.stem)
    return names


def judge(log: str) -> tuple[bool, str]:
    warning = WARNING.search(log)
    if warning:
        return False, warning.group(0)
    if not PRELOADED.search(log):
        return False, f"no 'Preloaded skill {SKILL}' line in debug log"
    return True, f"Preloaded skill '{SKILL}'"


def probe(agent: str, plugin_dir: Path, model: str) -> tuple[bool, str]:
    if agent not in {p.stem for p in (plugin_dir / "agents").glob("*.md")}:
        return False, f"unknown agent: {agent}"
    if shutil.which("claude") is None:
        return False, "claude CLI not found on PATH"
    prompt = (
        f"Dispatch the subagent cc10x:{agent} with the single instruction: "
        "'Reply with the word ok and do nothing else.' Then report its reply."
    )
    with tempfile.TemporaryDirectory(prefix="cc10x-preload-probe-") as tmp:
        debug_file = Path(tmp) / "debug.log"
        cmd = [
            "claude",
            "-p",
            "--plugin-dir",
            str(plugin_dir),
            "--model",
            model,
            "--max-budget-usd",
            MAX_BUDGET_USD,
            "--debug-file",
            str(debug_file),
            prompt,
        ]
        try:
            run = subprocess.run(
                cmd, cwd=tmp, capture_output=True, text=True, timeout=TIMEOUT_S
            )
        except subprocess.TimeoutExpired:
            return False, f"claude timed out after {TIMEOUT_S}s"
        if not debug_file.exists():
            return False, f"no debug log written (claude exit {run.returncode})"
        return judge(debug_file.read_text(encoding="utf-8", errors="replace"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--agent")
    target.add_argument("--all", action="store_true")
    parser.add_argument("--plugin-dir", type=Path, default=PLUGIN_ROOT)
    parser.add_argument("--model", default="haiku")
    args = parser.parse_args(argv)

    plugin_dir = args.plugin_dir.resolve()
    agents = agent_names(plugin_dir) if args.all else [args.agent]
    failed = 0
    for agent in agents:
        ok, detail = probe(agent, plugin_dir, args.model)
        print(f"{'PASS' if ok else 'FAIL'} {agent}: {detail}")
        failed += 0 if ok else 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
