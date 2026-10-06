#!/usr/bin/env python3
"""Characterization tests for tools/phase_brief.py (P2.T4).

Pins what the tool does TODAY: it slices one phase out of a plan markdown
file into <state_root>/phase-<PHASE>-brief.md. Each test runs the tool as a
subprocess against a tmp project dir (CLAUDE_PROJECT_DIR), asserting only on
exit code, output and the files written.

Runs as a dependency-free script (`python3 test_cc10x_phase_brief.py`) and
unchanged under pytest.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent
TOOL = PLUGIN_ROOT / "tools" / "phase_brief.py"

PLAN = """\
# Plan

## Phase 1: Alpha
alpha body
```
## Phase 9: inside a fence, not a heading
```
### Task 1.1
detail

## Phase 10: Ten
ten body

## Phase 2: Beta
beta body
### Phase 2.1 sub-phase
sub body

## Phase 3: Gamma
gamma body
"""


def run_tool(
    project_dir: Path,
    plan: Path,
    phase: str,
    *,
    cwd: Path | None = None,
    with_project_dir: bool = True,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    env = {"PATH": "/usr/bin:/bin", **(extra_env or {})}
    if with_project_dir:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    return subprocess.run(
        [sys.executable, str(TOOL), str(plan), phase],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd or project_dir,
        timeout=30,
    )


def write_plan(project_dir: Path, text: str = PLAN) -> Path:
    plan = project_dir / "plan.md"
    plan.write_text(text, encoding="utf-8")
    return plan


def brief(project_dir: Path, phase: str) -> Path:
    return project_dir / ".cc10x" / f"phase-{phase}-brief.md"


def test_slices_phase_up_to_next_sibling_heading(tmp_path):
    plan = write_plan(tmp_path)
    r = run_tool(tmp_path, plan, "1")
    assert r.returncode == 0
    text = brief(tmp_path, "1").read_text()
    assert text.startswith("## Phase 1: Alpha\n")
    assert "alpha body" in text
    assert "### Task 1.1\ndetail" in text
    assert "Phase 10" not in text
    assert text.endswith("detail\n")  # trailing blank line trimmed to one newline
    assert r.stdout == f"wrote {brief(tmp_path, '1')}: 7 lines\n"


def test_phase_id_matches_on_a_token_boundary(tmp_path):
    plan = write_plan(tmp_path)
    assert run_tool(tmp_path, plan, "10").returncode == 0
    text = brief(tmp_path, "10").read_text()
    assert text.startswith("## Phase 10: Ten\n")
    assert "ten body" in text and "alpha body" not in text


def test_fenced_phase_lines_are_not_headings(tmp_path):
    plan = write_plan(tmp_path)
    r = run_tool(tmp_path, plan, "9")
    assert r.returncode == 3
    assert not brief(tmp_path, "9").exists()


def test_fenced_phase_lines_do_not_end_the_slice(tmp_path):
    plan = write_plan(tmp_path)
    run_tool(tmp_path, plan, "1")
    text = brief(tmp_path, "1").read_text()
    assert "## Phase 9: inside a fence, not a heading" in text


def test_deeper_phase_heading_stays_inside_the_slice(tmp_path):
    plan = write_plan(tmp_path)
    run_tool(tmp_path, plan, "2")
    text = brief(tmp_path, "2").read_text()
    assert "### Phase 2.1 sub-phase\nsub body" in text
    assert "Gamma" not in text


def test_last_phase_runs_to_end_of_file(tmp_path):
    plan = write_plan(tmp_path)
    run_tool(tmp_path, plan, "3")
    assert brief(tmp_path, "3").read_text() == "## Phase 3: Gamma\ngamma body\n"


def test_missing_phase_exits_3_and_writes_nothing(tmp_path):
    plan = write_plan(tmp_path)
    r = run_tool(tmp_path, plan, "99")
    assert r.returncode == 3
    assert "phase 99 not found" in r.stderr
    assert not (tmp_path / ".cc10x").exists()


def test_missing_plan_file_exits_2(tmp_path):
    r = run_tool(tmp_path, tmp_path / "nope.md", "1")
    assert r.returncode == 2
    assert "no such plan file" in r.stderr


def test_state_root_is_created_on_demand(tmp_path):
    # Differs from cc10x_hooklib.state_root(), which never creates .cc10x.
    plan = write_plan(tmp_path)
    assert not (tmp_path / ".cc10x").exists()
    assert run_tool(tmp_path, plan, "1").returncode == 0
    assert (tmp_path / ".cc10x").is_dir()


def hooklib_project_dir(cwd: Path) -> str:
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "import cc10x_hooklib as h; print(h.project_dir())"
    )
    r = subprocess.run(
        [sys.executable, "-c", code, str(SCRIPTS_DIR)],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
        cwd=cwd,
        timeout=30,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def test_state_root_resolution_differs_from_the_docstring_claim(tmp_path):
    # P5.T1 changes this: state_root() gains the git-checkout precedence.
    # KNOWN DOC DEFECT, pinned as current behavior (the tool is not changed
    # here): the module docstring says the state root is "resolved like the
    # hooklib: CLAUDE_PROJECT_DIR env, else git toplevel, else cwd". The
    # hooklib has no git-toplevel step (CLAUDE_PROJECT_DIR, else cwd), so with
    # no env var and a cwd below a repo root the two disagree.
    repo = tmp_path / "repo"
    sub = repo / "pkg" / "inner"
    sub.mkdir(parents=True)
    git = subprocess.run(
        ["git", "init", "-q", str(repo)],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
    )
    assert git.returncode == 0, git.stderr
    plan = write_plan(tmp_path)
    r = run_tool(tmp_path, plan, "1", cwd=sub, with_project_dir=False)
    assert r.returncode == 0, r.stderr
    assert (repo / ".cc10x" / "phase-1-brief.md").is_file()  # git toplevel
    assert not (sub / ".cc10x").exists()
    assert os.path.realpath(hooklib_project_dir(sub)) == os.path.realpath(sub)


def test_state_root_falls_back_to_cwd_outside_a_repo(tmp_path):
    # P5.T1 changes this: state_root() gains the git-checkout precedence.
    work = tmp_path / "plain"
    work.mkdir()
    plan = write_plan(work)
    # The ceiling keeps git from finding a checkout above tmp_path when TMPDIR sits inside one.
    r = run_tool(
        work, plan, "1", cwd=work, with_project_dir=False,
        extra_env={"GIT_CEILING_DIRECTORIES": str(tmp_path)},
    )
    assert r.returncode == 0, r.stderr
    assert (work / ".cc10x" / "phase-1-brief.md").is_file()
    assert not (tmp_path / ".cc10x").exists()


def run_tool_file(name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PLUGIN_ROOT / "tools" / name), *args],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
        timeout=30,
    )


def source_head(path: Path, lines: int = 25) -> str:
    return "\n".join(path.read_text(encoding="utf-8").splitlines()[:lines])


# P2.T5: usage strings name the real tool files, not the retired cc10x_ names.


def test_phase_brief_usage_names_the_real_tool(tmp_path):
    r = run_tool_file("phase_brief.py", "--help")
    assert r.returncode == 0
    assert "usage: phase_brief.py" in r.stdout
    assert "cc10x_phase_brief" not in r.stdout
    head = source_head(TOOL)
    assert "Usage: phase_brief.py PLAN_FILE PHASE" in head


def test_review_package_usage_names_the_real_tool(tmp_path):
    r = run_tool_file("review_package.py", "--help")
    assert r.returncode == 0
    assert "usage: review_package.py" in r.stdout
    assert "cc10x_review_package" not in r.stdout
    head = source_head(PLUGIN_ROOT / "tools" / "review_package.py")
    assert "Usage: review_package.py BASE [HEAD]" in head


def test_latency_audit_banner_names_the_real_tool(tmp_path):
    r = run_tool_file("latency_audit.py", "--fixtures")
    assert r.returncode == 0
    assert r.stdout.splitlines()[0] == "latency_audit"


def test_event_logger_docstring_names_the_real_log_file(tmp_path):
    head = source_head(SCRIPTS_DIR / "cc10x_event_logger.py", 8)
    assert ".cc10x/events.jsonl" not in head
    assert "cc10x-hook-events.log" in head


def main() -> int:
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    failures = 0
    for name, fn in tests:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                fn(Path(tmp).resolve())
                print(f"PASS {name}")
            except Exception:
                failures += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    print(f"{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
