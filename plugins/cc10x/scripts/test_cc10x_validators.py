"""Hermetic tests for the validator tools, driven through their CLI seam against a temp copy of the tree.

CC10X_REPO_ROOT points a validator at the copy, so a mutation never touches the real repo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "plugins" / "cc10x" / "tools"
COPIED = ("plugins", "docs", ".claude-plugin", "README.md", "CHANGELOG.md")
FIVE_FILES = (
    "harness_audit.py",
    "doc_consistency_check.py",
    "prompt_clause_assertions.py",
    "workflow_replay_check.py",
    "fixture_registry.py",
)


def make_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for name in COPIED:
        src = REPO / name
        if src.is_dir():
            shutil.copytree(src, root / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, root / name)
    return root


def run_tool(script: str, root: Path | None = None, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "CC10X_REPO_ROOT"}
    if root is not None:
        env["CC10X_REPO_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(TOOLS / script), *args], capture_output=True, text=True, env=env
    )


def rewrite(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not found in {path.name}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_replay_check_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/tests/fixtures/plan-direct.json").unlink()
    assert run_tool("workflow_replay_check.py").returncode == 0
    bad = run_tool("workflow_replay_check.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "plan-direct.json" in bad.stdout + bad.stderr


def test_clause_assertions_read_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / "plugins/cc10x/skills/building/SKILL.md", "seam, one test", "seam, one xxxx")
    assert run_tool("prompt_clause_assertions.py").returncode == 0
    bad = run_tool("prompt_clause_assertions.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "building: one-seam-one-test cycle" in bad.stdout


def test_harness_audit_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/tests/fixtures/plan-direct.json").unlink()
    assert run_tool("harness_audit.py").returncode == 0
    bad = run_tool("harness_audit.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "missing replay fixture plan-direct.json" in bad.stderr


def test_doc_consistency_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / "README.md", "**Current version:**", "**Current versionx:**")
    assert run_tool("doc_consistency_check.py").returncode == 0
    bad = run_tool("doc_consistency_check.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "README banner version" in bad.stdout


def test_fixture_registry_plugin_root_follows_the_override(tmp_path):
    root = make_tree(tmp_path)
    code = "import fixture_registry as f; print(f.PLUGIN_ROOT)"
    env = {**os.environ, "CC10X_REPO_ROOT": str(root)}
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=str(TOOLS)
    )
    assert out.returncode == 0, out.stderr
    assert Path(out.stdout.strip()) == root / "plugins" / "cc10x"


@pytest.mark.parametrize("script", FIVE_FILES)
def test_non_repo_root_fails_clearly(script, tmp_path):
    result = run_tool(script, tmp_path)
    assert result.returncode != 0
    assert "CC10X_REPO_ROOT" in result.stderr
    assert "Traceback" not in result.stderr
