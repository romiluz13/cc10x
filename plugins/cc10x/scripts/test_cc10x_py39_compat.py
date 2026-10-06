#!/usr/bin/env python3
"""Python 3.9 safety matrix for the hook scripts and runtime-invoked tools.

Hooks run under whatever `python3` the user has (macOS ships 3.9.6). A single
unquoted `X | None` annotation raises TypeError at import time on 3.9, and a
hook that crashes silently disables its guard. This suite:

1. runs every script registered in hooks.json plus the runtime-invoked tools as
   a subprocess under /usr/bin/python3 (skipped unless it is 3.9) and under
   the current interpreter, asserting no Traceback and exit code in {0, 2};
2. asserts via AST that every scripts/*.py and tools/*.py file starts with
   `from __future__ import annotations` right after the docstring.
"""

from __future__ import annotations

import ast
import json
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent
TOOLS_DIR = PLUGIN_ROOT / "tools"
SYSTEM_PYTHON = "/usr/bin/python3"

PAYLOADS = [
    {},
    {"tool_name": "Bash", "tool_input": {"command": "ls"}},
    {"tool_name": "Write", "tool_input": {"file_path": "src.txt", "content": "x"}},
    {"hook_event_name": "SessionStart", "source": "startup"},
]

RUNTIME_TOOLS = ["phase_brief.py", "review_package.py", "live_harness_runner.py"]


def hook_commands() -> list[list[str]]:
    """Script path plus argv for every python command registered in hooks.json."""
    data = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text())
    commands = []
    for entries in data["hooks"].values():
        for entry in entries:
            for hook in entry["hooks"]:
                cmd = hook["command"].replace("${CLAUDE_PLUGIN_ROOT}", str(PLUGIN_ROOT))
                parts = shlex.split(cmd)
                if parts[0] == "python3":
                    commands.append(parts[1:])
    return commands


def interpreters() -> list[str]:
    found = [sys.executable]
    if Path(SYSTEM_PYTHON).exists():
        probe = subprocess.run(
            [SYSTEM_PYTHON, "-c", "import sys;print(sys.version_info[:2])"],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip() == "(3, 9)":
            found.append(SYSTEM_PYTHON)
    return found


def run(interp: str, argv: list[str], stdin: str, project: Path):
    env = {
        "CLAUDE_PROJECT_DIR": str(project),
        "CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT),
        "PATH": "/usr/bin:/bin",
    }
    return subprocess.run(
        [interp, *argv],
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
        cwd=project,
        timeout=30,
    )


def test_system_python39_present_or_skipped():
    if SYSTEM_PYTHON not in interpreters():
        pytest.skip(f"{SYSTEM_PYTHON} is absent or not Python 3.9")


@pytest.mark.parametrize("interp", interpreters())
def test_hook_scripts_do_not_crash(interp, tmp_path):
    commands = hook_commands()
    assert len(commands) >= 9
    for argv in commands:
        for payload in PAYLOADS:
            r = run(interp, argv, json.dumps(payload), tmp_path)
            label = f"{interp} {Path(argv[0]).name} {argv[1:]} {payload}"
            assert "Traceback" not in r.stderr, f"{label}\n{r.stderr}"
            assert r.returncode in (0, 2), f"{label} rc={r.returncode}\n{r.stderr}"


@pytest.mark.parametrize("interp", interpreters())
def test_runtime_tools_import_and_show_help(interp, tmp_path):
    for name in RUNTIME_TOOLS:
        r = run(interp, [str(TOOLS_DIR / name), "--help"], "", tmp_path)
        assert "Traceback" not in r.stderr, f"{interp} {name}\n{r.stderr}"
        assert r.returncode in (0, 2), f"{interp} {name} rc={r.returncode}\n{r.stderr}"


def first_statement_after_docstring(tree: ast.Module):
    body = tree.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return body[0] if body else None


def test_every_script_and_tool_has_future_annotations():
    missing = []
    files = sorted(SCRIPTS_DIR.glob("*.py")) + sorted(TOOLS_DIR.glob("*.py"))
    assert files
    for path in files:
        stmt = first_statement_after_docstring(ast.parse(path.read_text()))
        ok = (
            isinstance(stmt, ast.ImportFrom)
            and stmt.module == "__future__"
            and any(alias.name == "annotations" for alias in stmt.names)
        )
        if not ok:
            missing.append(path.relative_to(PLUGIN_ROOT).as_posix())
    assert not missing, f"missing `from __future__ import annotations`: {missing}"
