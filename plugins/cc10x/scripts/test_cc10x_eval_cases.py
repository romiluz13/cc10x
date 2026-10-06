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

# The eight ids in the plan's Durable Decisions (Eval layout), each with the finding it guards,
# whether it is expected red at baseline (the defect exists at HEAD), and its required graders.
CASES = {
    "build-multiphase-memory-finalize": ("B3", True, {"phase1-created", "phase2-created", "memory-finalized-once"}),
    "build-trivial-happy": ("trivial-build", False, {"greeting-content", "greeting-created", "outcome-passed", "router-fired"}),
    "qa-seed-template-path": ("B11", True, {"plan-seeded", "no-empty-prefix-copy"}),
    "remfix-gate-producer": ("B1", True, {"remfix-created", "covering-proof", "run-command"}),
    "route-precedence": ("B4", False, {"route-review", "route-orient", "route-qa", "route-debug"}),
    "seam-gate": ("C9", False, {"spec-file-created", "seam-gate-status", "seams-named"}),
    "triage-loads-reference": ("B2", True, {"reference-read", "router-fired", "workflow-type"}),
    "two-workflow-resume": ("B14", True, {"resumed-the-right-workflow", "other-workflow-untouched"}),
}
EXPECTED_CASE_IDS = sorted(CASES)
BASELINE = PLUGIN_ROOT / "evals" / "BASELINE.md"
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


def case_tags(case: Path) -> list[str]:
    match = re.search(r"^tags:\s*\[(.*)\]\s*$", (case / "case.yaml").read_text(encoding="utf-8"), re.M)
    assert match, f"{case.name}/case.yaml needs an inline tags list"
    return [t.strip() for t in match.group(1).split(",") if t.strip()]


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


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_case_declares_guarded_finding_and_expected_red_flag(case):
    finding, red, _ = CASES[case.name]
    tags = case_tags(case)
    assert [t for t in tags if t.startswith("guards-")] == [f"guards-{finding}"]
    assert [t for t in tags if t in {"expected-red", "regression"}] == (["expected-red"] if red else ["regression"])
    description = re.search(r"^description:\s*(.+)$", (case / "case.yaml").read_text(encoding="utf-8"), re.M)
    assert description and finding in description.group(1)
    assert ("EXPECTED RED" if red else "REGRESSION GUARD") in description.group(1)


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_case_has_its_required_graders(case):
    have = {g.stem for g in (case / "graders").glob("*.md")}
    assert CASES[case.name][2] <= have, sorted(CASES[case.name][2] - have)


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_fixture_scaffolds_a_git_repo_in_an_empty_directory(case, tmp_path):
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(tmp_path), "TMPDIR": str(tmp_path), "TERM": "dumb"}
    result = subprocess.run(["bash", str(case / "fixture.sh")], cwd=tmp_path, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".git").exists()
    head = subprocess.run(["git", "log", "--oneline"], cwd=tmp_path, env=env, capture_output=True, text=True)
    assert head.returncode == 0 and head.stdout.strip()



def test_baseline_lists_every_case_and_every_red_case_names_its_p4_task():
    text = BASELINE.read_text(encoding="utf-8")
    rows = {line.split("|")[1].strip().strip("`"): line for line in text.splitlines() if line.startswith("| `")}
    assert sorted(rows) == EXPECTED_CASE_IDS
    for case_id, (finding, red, _) in CASES.items():
        assert finding in rows[case_id]
        if red:
            assert re.search(r"P4\.T\d", rows[case_id]), case_id
    assert "L2 baseline: NOT RUN" in text
