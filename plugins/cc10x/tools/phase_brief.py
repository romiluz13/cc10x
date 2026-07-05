#!/usr/bin/env python3
"""Slice ONE approved phase out of a plan file into a brief the implementer
reads in one call, so the phase text never has to be pasted through the
router's context. cc10x's analog of superpowers' task-brief, at PHASE
granularity (cc10x's build unit is the phase).

Usage: cc10x_phase_brief.py PLAN_FILE PHASE
  PLAN_FILE  path to the implementation plan markdown
  PHASE      phase number or id (matched against '## Phase <PHASE>' headings)

Writes <state_root>/phase-<PHASE>-brief.md (state_root = .cc10x, resolved like
the hooklib: CLAUDE_PROJECT_DIR env, else git toplevel, else cwd) and prints
'wrote <path>: <n> lines'. Exit 3 if the phase heading is not found.

Fence-aware: '## Phase N' lines inside ``` code fences are ignored. The brief
runs from the matched phase heading to the next sibling phase heading (a
heading at the same '#' depth).
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def project_dir() -> Path:
    value = os.environ.get("CLAUDE_PROJECT_DIR")
    if value:
        return Path(value)
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if top:
            return Path(top)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return Path.cwd()


def state_root() -> Path:
    path = project_dir() / ".cc10x"
    path.mkdir(parents=True, exist_ok=True)
    return path


def slice_phase(text: str, phase: str) -> str | None:
    """Return the matched phase heading + body, or None if not found."""
    # ## Phase <phase> followed by a non-alphanumeric boundary or end of token,
    # so 'Phase 1' does not match 'Phase 10'. Heading prefix is 1+ '#'.
    heading = re.compile(
        r"^(#+)[ \t]+Phase[ \t]+" + re.escape(phase) + r"(?![0-9A-Za-z]).*$"
    )
    sibling = re.compile(r"^(#+)[ \t]+Phase[ \t]+", re.IGNORECASE)

    in_fence = False
    collecting = False
    depth = 0
    out: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if collecting:
                out.append(line)
            continue
        if not in_fence:
            if not collecting:
                m = heading.match(line)
                if m:
                    collecting = True
                    depth = len(m.group(1))
                    out.append(line)
                    continue
            else:
                m = sibling.match(line)
                if m and len(m.group(1)) <= depth:
                    break
                out.append(line)
                continue
        elif collecting:
            out.append(line)
    if not collecting:
        return None
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cc10x_phase_brief.py",
        description="Slice one phase out of a plan file into a .cc10x brief.",
    )
    parser.add_argument("plan_file", help="path to the implementation plan markdown")
    parser.add_argument("phase", help="phase number or id")
    args = parser.parse_args()

    plan = Path(args.plan_file)
    if not plan.is_file():
        print(f"no such plan file: {plan}", file=sys.stderr)
        return 2

    try:
        text = plan.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read plan file {plan}: {exc}", file=sys.stderr)
        return 2

    brief = slice_phase(text, args.phase)
    if brief is None:
        print(
            f"phase {args.phase} not found in {plan} "
            f"(no heading matching '## Phase {args.phase}')",
            file=sys.stderr,
        )
        return 3

    out = state_root() / f"phase-{args.phase}-brief.md"
    try:
        out.write_text(brief, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write brief {out}: {exc}", file=sys.stderr)
        return 2

    n_lines = brief.count("\n")
    print(f"wrote {out}: {n_lines} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
