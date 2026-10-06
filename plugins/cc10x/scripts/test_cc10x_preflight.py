#!/usr/bin/env python3
"""Behavioral tests for scripts/cc10x_preflight.sh (SessionStart Python check).

The script is driven exactly as hooks.json runs it (`sh <script>`) with a
controlled PATH: no python3, a stub python3 that fails the version probe, and a
real python3. It must always exit 0 and print the SessionStart
additionalContext JSON only when python3 is missing or older than 3.9.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "cc10x_preflight.sh"


def run_preflight(path_dirs: list[Path]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["/bin/sh", str(SCRIPT)],
        capture_output=True,
        text=True,
        env={"PATH": ":".join(str(d) for d in path_dirs)},
        timeout=30,
    )


def assert_python_guidance(r: subprocess.CompletedProcess) -> None:
    assert r.returncode == 0
    out = json.loads(r.stdout)
    hso = out["hookSpecificOutput"]
    assert hso["hookEventName"] == "SessionStart"
    ctx = hso["additionalContext"]
    assert "python3" in ctx.lower() or "python" in ctx.lower()
    assert "3.13" in ctx and "3.9" in ctx
    assert "tell the user" in ctx.lower()


def test_missing_python3_prints_install_guidance(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert_python_guidance(run_preflight([empty]))


def test_failing_version_probe_prints_upgrade_guidance(tmp_path):
    stub_dir = tmp_path / "stub"
    stub_dir.mkdir()
    stub = stub_dir / "python3"
    stub.write_text("#!/bin/sh\nexit 1\n")
    stub.chmod(0o755)
    assert_python_guidance(run_preflight([stub_dir]))


def test_real_python3_is_silent(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    (real / "python3").symlink_to(sys.executable)
    r = run_preflight([real])
    assert r.returncode == 0
    assert r.stdout == ""
    assert r.stderr == ""
