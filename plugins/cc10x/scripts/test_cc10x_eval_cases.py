"""Structural checks for the L2 eval cases under plugins/cc10x/evals/cases.

Cases are never run here (a run spends money); this only proves each case directory
has the files `claude plugin eval` requires: a prompt, a case.yaml naming an existing
scaffold script, and at least one grader with a known type.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = PLUGIN_ROOT / "evals" / "cases"

# Subset of the eight ids in the plan's Durable Decisions (Eval layout) that exist so far.
EXPECTED_CASE_IDS = ["build-trivial-happy"]
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}


def case_dirs():
    if not CASES_DIR.is_dir():
        return []
    return sorted(p for p in CASES_DIR.iterdir() if p.is_dir())


def frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"{path} has no frontmatter"
    end = lines.index("---", 1)
    out = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if match:
            out[match.group(1)] = match.group(2).strip()
    return out


def test_case_ids_are_exactly_the_planned_ones_that_exist():
    assert [p.name for p in case_dirs()] == EXPECTED_CASE_IDS


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_case_has_the_files_the_eval_schema_requires(case):
    assert (case / "prompt.md").is_file()
    case_yaml = (case / "case.yaml").read_text(encoding="utf-8")
    assert re.search(r'^schema_version:\s*"1\.1"\s*$', case_yaml, re.M)
    assert re.search(rf"^name:\s*{re.escape(case.name)}\s*$", case_yaml, re.M)
    prompt = frontmatter(case / "prompt.md")
    assert int(prompt["max_turns"]) >= 10
    assert int(prompt["timeout_seconds"]) >= 300
    graders = sorted((case / "graders").glob("*.md"))
    assert graders, "a case without a grader fails to load"
    for grader in graders:
        assert frontmatter(grader)["type"] in GRADER_TYPES, grader.name


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_scaffold_script_exists_and_parses(case):
    case_yaml = (case / "case.yaml").read_text(encoding="utf-8")
    match = re.search(r"^\s+scaffold_script:\s*(\S+)\s*$", case_yaml, re.M)
    assert match, "case.yaml must name its scaffold_script"
    script = case / match.group(1)
    assert script.is_file()
    for shell in ("sh", "bash"):
        result = subprocess.run([shell, "-n", str(script)], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_file_graders_point_at_files_the_prompt_asks_for(case):
    prompt = (case / "prompt.md").read_text(encoding="utf-8")
    for grader in sorted((case / "graders").glob("*.md")):
        text = grader.read_text(encoding="utf-8")
        for path in re.findall(r"^\s*path:\s*(\S+)\s*$", text, re.M):
            assert path in prompt, f"{grader.name} grades {path}, which the prompt never asks for"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_no_grader_uses_plugin_root_variable(case):
    for path in case.rglob("*"):
        if path.is_file():
            assert "CLAUDE_PLUGIN_ROOT" not in path.read_text(encoding="utf-8"), path.name
