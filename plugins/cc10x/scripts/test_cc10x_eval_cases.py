"""Structural checks for the L2 eval cases under plugins/cc10x/evals/cases.

Cases are never run here (a run spends money); this only proves each case directory
has the files `claude plugin eval` requires: a prompt, a case.yaml naming an existing
scaffold script, and at least one well-formed grader with a known type and only known keys.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = PLUGIN_ROOT / "evals" / "cases"

# The eight ids in the plan's Durable Decisions (Eval layout), each with the finding it guards,
# whether it is expected red at baseline (the defect exists at HEAD), and its required graders.
CASES = {
    "build-multiphase-memory-finalize": (
        "B3", True,
        {"phase1-created", "phase2-created", "memory-finalized-once", "memory-finalized-not-twice", "router-fired"},
    ),
    "build-trivial-happy": ("trivial-build", False, {"greeting-content", "greeting-created", "outcome-passed", "router-fired"}),
    "qa-seed-template-path": ("B11", True, {"plan-seeded", "no-empty-prefix-copy", "router-fired"}),
    "remfix-gate-producer": (
        "B1", True, {"remfix-created", "covering-proof", "run-command", "output-proof", "router-fired"},
    ),
    "route-precedence": ("B4", False, {"route-review", "route-orient", "route-qa", "route-debug", "router-fired"}),
    "seam-gate": ("C9", False, {"spec-file-created", "seam-gate-status", "seams-named", "router-fired"}),
    "triage-loads-reference": ("B2", True, {"reference-read", "router-fired", "workflow-type"}),
    "two-workflow-resume": (
        "scoped-resume", False, {"resumed-the-right-workflow", "other-workflow-untouched", "router-fired"},
    ),
}
EXPECTED_CASE_IDS = sorted(CASES)
BASELINE = PLUGIN_ROOT / "evals" / "BASELINE.md"
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
# Allow-lists from the recorded `claude plugin eval` schema: an unknown key is an error at load time.
PROMPT_KEYS = {
    "schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome", "model",
    "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env",
}
GRADER_KEYS = {
    "type", "weight", "arm", "pattern", "flags", "match", "target", "tool", "input_match", "min", "max",
    "before", "after", "path", "exists", "criteria", "focus", "baseline_file",
}
CASE_YAML_KEYS = {
    None: {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome", "execution", "context"},
    "execution": {"model", "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env"},
    "context": {"scaffold_script", "history_file", "add_dirs"},
}
GRADER_REQUIRED_KEYS = {"regex": {"pattern"}, "tool_used": {"tool"}, "file_exists": {"path"}, "tool_order": {"before", "after"}}
DISPATCH_TOOLS = {"Agent", "TaskCreate", "TaskGet", "TaskList", "TaskUpdate"}
NO_DISPATCH_CASES = {"route-precedence"}
KEY_LINE = re.compile(r"^([A-Za-z_]+):(?:\s+(.*))?$")
REGEX_FLAGS = {"i": re.I, "m": re.M, "s": re.S}


def case_dirs():
    if not CASES_DIR.is_dir():
        return []
    return sorted(p for p in CASES_DIR.iterdir() if p.is_dir())


def strict_keys(lines: list[str], source: str) -> list[tuple[str | None, str, str]]:
    """Return (parent_key, key, value) for each `key: value` line; fail on any other non-blank line shape."""
    found = []
    parent = None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            match = KEY_LINE.match(line)
            assert match, f"{source}: malformed line {line!r} (expected `key: value`)"
            parent = match.group(1)
            found.append((None, parent, (match.group(2) or "").strip()))
            continue
        nested = KEY_LINE.match(line.strip())
        if nested and not line.strip().startswith("- "):
            found.append((parent, nested.group(1), (nested.group(2) or "").strip()))
    return found


def frontmatter_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"{path} has no frontmatter"
    return lines[1 : lines.index("---", 1)]


def frontmatter(path: Path) -> dict:
    return {key: value for parent, key, value in strict_keys(frontmatter_lines(path), str(path)) if parent is None}


def prompt_body(case: Path) -> str:
    lines = (case / "prompt.md").read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[lines.index("---", 1) + 1 :])


def yaml_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def scaffold_script_name(case: Path) -> str:
    match = re.search(r"^\s+scaffold_script:\s*(\S+)\s*$", (case / "case.yaml").read_text(encoding="utf-8"), re.M)
    assert match, f"{case.name}/case.yaml must name its scaffold_script"
    return match.group(1)


def run_scaffold(case: Path, workdir: Path) -> subprocess.CompletedProcess:
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(workdir), "TMPDIR": str(workdir), "TERM": "dumb"}
    return subprocess.run(["bash", str(case / scaffold_script_name(case))], cwd=workdir, env=env, capture_output=True, text=True)


def graders_of(case: Path):
    return sorted((case / "graders").glob("*.md"))


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
    script = case / scaffold_script_name(case)
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
    result = run_scaffold(case, tmp_path)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".git").exists()
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(tmp_path), "TMPDIR": str(tmp_path), "TERM": "dumb"}
    head = subprocess.run(["git", "log", "--oneline"], cwd=tmp_path, env=env, capture_output=True, text=True)
    assert head.returncode == 0 and head.stdout.strip()


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_files_the_prompt_reads_exist_after_the_scaffold(case, tmp_path):
    created = set(re.findall(r"^\s*path:\s*(\S+)\s*$", "".join(g.read_text(encoding="utf-8") for g in graders_of(case)), re.M))
    assert run_scaffold(case, tmp_path).returncode == 0
    mentioned = set(re.findall(r"(?<![\w./<>*-])[\w./-]+\.(?:md|py|txt|json)\b", prompt_body(case)))
    for name in sorted(mentioned - created):
        assert (tmp_path / name).exists(), f"prompt reads {name}, which the scaffold does not create"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_scaffolded_workflow_artifacts_pass_the_repo_validator(case, tmp_path):
    assert run_scaffold(case, tmp_path).returncode == 0
    tool = PLUGIN_ROOT / "tools" / "workflow_replay_check.py"
    for artifact in sorted((tmp_path / ".cc10x" / "workflows").glob("*.json")):
        result = subprocess.run([sys.executable, str(tool), "--artifact", str(artifact)], capture_output=True, text=True)
        assert result.returncode == 0, f"{artifact.name}: {result.stderr}"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_prompt_and_case_yaml_use_only_known_well_formed_keys(case):
    for parent, key, _ in strict_keys(frontmatter_lines(case / "prompt.md"), "prompt.md"):
        assert parent is None or key in {"source", "path"}
        if parent is None:
            assert key in PROMPT_KEYS, f"{case.name}/prompt.md has unknown key {key!r}"
    text = (case / "case.yaml").read_text(encoding="utf-8").splitlines()
    for parent, key, _ in strict_keys(text, "case.yaml"):
        assert parent in CASE_YAML_KEYS, f"{case.name}/case.yaml has unknown block {parent!r}"
        assert key in CASE_YAML_KEYS[parent], f"{case.name}/case.yaml has unknown key {key!r}"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_graders_use_only_known_keys_and_carry_their_required_ones(case):
    for grader in graders_of(case):
        entries = strict_keys(frontmatter_lines(grader), grader.name)
        top = {key for parent, key, _ in entries if parent is None}
        assert top <= GRADER_KEYS, f"{grader.name} has unknown keys {sorted(top - GRADER_KEYS)}"
        kind = frontmatter(grader)["type"]
        filled = {key for parent, key, value in entries if parent is None and value}
        needed = GRADER_REQUIRED_KEYS.get(kind, set())
        assert needed <= filled, f"{grader.name} ({kind}) lacks a value for {sorted(needed - filled)}"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_every_grader_regex_compiles(case):
    for grader in graders_of(case):
        fm = frontmatter(grader)
        for key in ("pattern", "input_match"):
            if key in fm:
                flags = 0
                for flag in yaml_scalar(fm.get("flags", "")):
                    flags |= REGEX_FLAGS[flag]
                try:
                    re.compile(yaml_scalar(fm[key]), flags)
                except (re.error, KeyError) as exc:
                    pytest.fail(f"{grader.name} {key} is not a valid regex: {exc}")


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_outcome_key_graders_read_only_keys_the_prompt_requests(case):
    lines = prompt_body(case).splitlines()
    for grader in graders_of(case):
        pattern = yaml_scalar(frontmatter(grader).get("pattern", ""))
        match = re.match(r"\^([A-Z][A-Z0-9_]*)(=?)", pattern)
        if not match:
            continue
        wanted = match.group(1) + match.group(2)
        assert any(line.startswith(wanted) for line in lines), f"{grader.name} reads {wanted!r}, which the prompt never asks for"


LEAK = re.compile(r"expected[- ]red|baseline|regression|guards-|\bB\d+\b|\bC\d+\b", re.I)


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_prompt_does_not_leak_the_expected_outcome_or_the_finding(case):
    body = prompt_body(case)
    assert not LEAK.search(body), f"{case.name}/prompt.md leaks {LEAK.search(body).group(0)!r}"
    for other in EXPECTED_CASE_IDS:
        assert other not in body, f"{case.name}/prompt.md names case id {other}"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_dispatch_dependent_cases_grant_the_agent_and_task_tools(case):
    match = re.search(r"\[(.*)\]", frontmatter(case / "prompt.md")["allowed_tools"])
    tools = {t.strip() for t in match.group(1).split(",")}
    if case.name in NO_DISPATCH_CASES:
        assert not tools & DISPATCH_TOOLS
    else:
        assert DISPATCH_TOOLS <= tools, f"{case.name} cannot dispatch: missing {sorted(DISPATCH_TOOLS - tools)}"


@pytest.mark.parametrize("case", case_dirs(), ids=lambda p: p.name)
def test_case_proves_the_router_ran_not_only_the_self_written_outcome(case):
    ran = False
    for grader in graders_of(case):
        fm = frontmatter(grader)
        if fm["type"] == "tool_used" and fm["tool"] in {"Skill", "Read"}:
            ran = True
    assert ran, f"{case.name} grades only what the run wrote about itself"


def test_baseline_lists_every_case_and_every_red_case_names_its_p4_task():
    text = BASELINE.read_text(encoding="utf-8")
    rows = {line.split("|")[1].strip().strip("`"): line for line in text.splitlines() if line.startswith("| `")}
    assert sorted(rows) == EXPECTED_CASE_IDS
    for case_id, (finding, red, _) in CASES.items():
        assert finding in rows[case_id]
        if red:
            assert re.search(r"P4\.T\d", rows[case_id]), case_id
    assert "L2 baseline: NOT RUN" in text


def test_seam_eval_docstring_calls_itself_a_text_check_and_points_at_the_behavioral_case():
    source = (PLUGIN_ROOT / "tests" / "live" / "seam_eval.py").read_text(encoding="utf-8")
    docstring = source.split('"""')[1]
    assert "TEXT check" in docstring
    assert "seam-gate" in docstring


def test_baseline_measure_command_carries_the_flags_the_plan_requires():
    command = next(line for line in BASELINE.read_text(encoding="utf-8").splitlines() if "claude plugin eval" in line)
    for flag in ("--allow-tools Bash Write Edit", "--ablation none", "--no-publish", "--scaffold", "--runs 3", "--max-cost-usd"):
        assert flag in command, f"BASELINE.md measure command lacks {flag}"


def test_baseline_cites_no_local_only_notes():
    assert ".cc10x/anchors" not in BASELINE.read_text(encoding="utf-8")
