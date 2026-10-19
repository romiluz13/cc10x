#!/usr/bin/env python3
"""Behavioral tests for the CC10x guard scripts.

Every test invokes a guard exactly the way the Claude Code hook runtime does:
the script runs as a subprocess with hook-event JSON on stdin, and assertions
are made only on exit code, stdout/stderr, and filesystem effects — never on
imported internals. `cc10x_hooklib.py` is exercised through every guard.

Isolation: each test gets a fresh temp project dir via CLAUDE_PROJECT_DIR.
Mode overrides use a synthetic CLAUDE_PLUGIN_ROOT holding only a
config/hook-mode.json, so the shipped config is never touched.

This suite is the GREEN BASELINE for the current tree (ticket T2/#67): it
locks in today's behavior, including audit-mode defaults. Bug-reproduction
tests for the known fail-open paths land with their fixes in T8/#73.
"""

from __future__ import annotations

import atexit
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent

# In-process hooklib tests that do not set CLAUDE_PROJECT_DIR would otherwise
# resolve the checkout running the suite and write events and markers there.
if not os.environ.get("CLAUDE_PROJECT_DIR"):
    _AMBIENT_PROJECT = tempfile.mkdtemp(prefix="cc10x-guards-ambient-")
    os.environ["CLAUDE_PROJECT_DIR"] = _AMBIENT_PROJECT
    atexit.register(shutil.rmtree, _AMBIENT_PROJECT, True)


def run_guard(
    script: str,
    payload: dict | None,
    project_dir: Path,
    *,
    argv: list[str] | None = None,
    plugin_root: Path | None = None,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    env = {
        "CLAUDE_PROJECT_DIR": str(project_dir),
        "CLAUDE_PLUGIN_ROOT": str(plugin_root or PLUGIN_ROOT),
        "PATH": "/usr/bin:/bin",
        **(extra_env or {}),
    }
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script), *(argv or [])],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True,
        text=True,
        env=env,
        cwd=project_dir,
        timeout=30,
    )


def mode_root(tmp_path: Path, modes: dict) -> Path:
    """Synthetic plugin root carrying only a hook-mode.json."""
    root = tmp_path / "plugin-root"
    (root / "config").mkdir(parents=True)
    (root / "config" / "hook-mode.json").write_text(json.dumps(modes))
    return root


REQUIRED_WORKFLOW_KEYS = (
    "workflow_uuid",
    "workflow_id",
    "workflow_type",
    "state_root",
    "phase_cursor",
    "task_ids",
    "results",
    "intent",
    "evidence",
    "quality",
    "status_history",
    "remediation_history",
)


def write_artifact(project_dir: Path, wf: str = "wf-test", **overrides) -> Path:
    workflows = project_dir / ".cc10x" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {key: None for key in REQUIRED_WORKFLOW_KEYS}
    payload.update(
        {
            "workflow_uuid": wf,
            "workflow_id": wf,
            "workflow_type": "BUILD",
            "state_root": ".cc10x",
            "phase_cursor": "phase-1",
            "task_ids": {},
            "results": {},
            "intent": {},
            "evidence": [],
            "quality": {},
            "status_history": [],
            "remediation_history": [],
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
    )
    payload.update(overrides)
    path = workflows / f"{wf}.json"
    path.write_text(json.dumps(payload))
    (workflows / f"{wf}.events.jsonl").write_text("")
    return path


def hook_log_lines(project_dir: Path) -> list[dict]:
    log = project_dir / ".cc10x" / "cc10x-hook-events.log"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text().splitlines() if line.strip()]


# --- cc10x_posttooluse_artifact_guard.py ------------------------------------


def assert_repair_now_message(stderr: str) -> None:
    # Exit 2 feeds stderr to the model but cannot undo the write: the message
    # must say so and tell the model to repair the artifact now.
    assert "already written" in stderr
    assert "still on disk" in stderr
    assert "repair it now" in stderr.lower()
    assert "rejected" not in stderr.lower()


def test_artifact_guard_passes_valid_artifact_and_auto_appends_event(tmp_path):
    path = write_artifact(tmp_path)
    # Freshness window is 60s; rewrite so mtime is now.
    path.write_text(path.read_text())
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode == 0
    events_log = path.parent / "wf-test.events.jsonl"
    lines = [json.loads(line) for line in events_log.read_text().splitlines()]
    assert any(e["event"] == "artifact_mutated" for e in lines)


def test_artifact_guard_blocks_artifact_missing_required_keys(tmp_path):
    # Shipped config: artifactIntegrity=block — hard corruption exits 2.
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(bad)}},
        tmp_path,
    )
    assert r.returncode == 2
    assert "missing-keys" in r.stderr
    assert_repair_now_message(r.stderr)


def test_artifact_guard_blocks_malformed_artifact_json(tmp_path):
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-corrupt.json"
    bad.write_text("{not json")
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(bad)}},
        tmp_path,
    )
    assert r.returncode == 2
    assert "artifact-json" in r.stderr
    assert_repair_now_message(r.stderr)


def test_artifact_guard_never_blocks_unrelated_writes(tmp_path):
    # A corrupt LATEST artifact must not veto writes elsewhere (audit only).
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "wf-old.json").write_text("{not json")
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "src.py")}},
        tmp_path,
    )
    assert r.returncode == 0


# --- cc10x_sessionstart_context.py ------------------------------------------


def test_sessionstart_silent_without_workflow(tmp_path):
    r = run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_sessionstart_injects_context_for_active_workflow(tmp_path):
    write_artifact(tmp_path, phase_status={"phase-1": "in_progress"})
    r = run_guard("cc10x_sessionstart_context.py", {"source": "resume"}, tmp_path)
    assert r.returncode == 0
    out = json.loads(r.stdout)
    context = out["hookSpecificOutput"]["additionalContext"]
    assert "wf=wf-test" in context
    assert "phase-1" in context


def test_sessionstart_tells_the_model_when_the_newest_artifact_is_unreadable(tmp_path):
    # Never-raise contract of read_latest_workflow_state, and no silent skip:
    # the model gets one line saying the newest artifact cannot be read, and
    # the log gets a workflow_artifact_unreadable event.
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "wf-corrupt.json").write_text("{not json")
    r = run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    assert r.returncode == 0
    context = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "wf-corrupt.json" in context and "unreadable" in context
    assert "\n" not in context
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "workflow_artifact_unreadable"]
    assert len(events) == 1
    assert events[0]["reason"] == "JSONDecodeError"
    assert events[0]["path"].endswith("wf-corrupt.json")


# --- cc10x_hooklib.py (mode resolution, exercised through the artifact guard) --


def test_hooklib_corrupt_mode_config_falls_back_to_the_block_default(tmp_path):
    # P5.T3: a corrupt hook-mode.json falls back to HOOK_MODE_DEFAULTS
    # (artifactIntegrity=block) and records an invalid_hook_mode event, so a
    # key-missing artifact write still exits 2 instead of silently auditing.
    root = tmp_path / "plugin-root"
    (root / "config").mkdir(parents=True)
    (root / "config" / "hook-mode.json").write_text("{not json")
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(bad)}},
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2
    assert any(e["event"] == "invalid_hook_mode" for e in hook_log_lines(tmp_path))


# --- cc10x_state_persist.py --------------------------------------------------


def test_state_persist_stop_writes_snapshot(tmp_path):
    write_artifact(tmp_path)
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    assert r.returncode == 0
    snapshot = json.loads((tmp_path / ".cc10x" / "stop-state.json").read_text())
    assert snapshot["workflow_uuid"] == "wf-test"
    assert snapshot["source"] == "stop"


def test_state_persist_precompact_writes_snapshot(tmp_path):
    write_artifact(tmp_path)
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["precompact"])
    assert r.returncode == 0
    assert (tmp_path / ".cc10x" / "precompact-state.json").exists()


def test_state_persist_skips_continuation_stop(tmp_path):
    write_artifact(tmp_path)
    r = run_guard(
        "cc10x_state_persist.py", {"stop_hook_active": True}, tmp_path, argv=["stop"]
    )
    assert r.returncode == 0
    assert not (tmp_path / ".cc10x" / "stop-state.json").exists()


# --- cc10x_event_logger.py ---------------------------------------------------


def test_event_logger_audits_cc10x_subagent_contract(tmp_path):
    # A cc10x subagent implies an active workflow, so .cc10x exists.
    (tmp_path / ".cc10x").mkdir()
    r = run_guard(
        "cc10x_event_logger.py",
        {
            "agent_type": "cc10x:component-builder",
            "agent_id": "a1",
            "last_assistant_message": 'CONTRACT {"status": "PASS"}',
        },
        tmp_path,
        argv=["subagent_stop"],
    )
    assert r.returncode == 0
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "subagent_stop" and e["reason"] == "contract_present"
        for e in events
    )


def test_event_logger_does_not_evaluate_the_contract_for_non_cc10x_subagents(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    # Contract-looking text or "CC10X"/"Router Contract" wording must not make a
    # non-cc10x agent type count as a contract miss (N1).
    for agent_type in ("general-purpose", "worktree-worker", ""):
        r = run_guard(
            "cc10x_event_logger.py",
            {
                "agent_type": agent_type,
                "last_assistant_message": "CC10X Router Contract notes, no envelope",
            },
            tmp_path,
            argv=["subagent_stop"],
        )
        assert r.returncode == 0
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "subagent_stop"]
    assert len(events) == 3
    for e in events:
        assert e["reason"] == "non_cc10x_agent"
        assert "contract_found" not in e


def test_event_logger_postcompact_appends_workflow_event(tmp_path):
    write_artifact(tmp_path)
    r = run_guard(
        "cc10x_event_logger.py",
        {"trigger": "auto", "compact_summary": "summary text"},
        tmp_path,
        argv=["postcompact"],
    )
    assert r.returncode == 0
    events_log = tmp_path / ".cc10x" / "workflows" / "wf-test.events.jsonl"
    lines = [json.loads(line) for line in events_log.read_text().splitlines()]
    assert any(e["event"] == "compact_occurred" for e in lines)


# --- T8 (#73) bug reproductions: each of these failed before the fix -------


def test_hooklib_survives_unstatable_workflow_entry(tmp_path):
    # latest_workflow_file() stat()s during sort; an entry that exists in the
    # glob but cannot be stat()ed (deleted concurrently — reproduced here with
    # a dangling symlink) crashed every caller, failing the guard open.
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "dangling.json").symlink_to(workflows / "gone.json")
    r = run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    assert r.returncode == 0
    assert "Traceback" not in r.stderr


def test_guards_do_not_litter_foreign_repos(tmp_path):
    # Guards ran state_root()/workflows_dir() with mkdir on every event,
    # creating .cc10x/ in every repo the user touched — CC10x or not.
    run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "a.py")}},
        tmp_path,
    )
    run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    assert not (tmp_path / ".cc10x").exists()


# --- P2.T4 characterization tests (pin CURRENT behavior; P5 updates them) ----
#
# These lock what the hooks do today so the P5 hook cleanup changes behavior
# deliberately. Where a test pins something P5 plans to change, the comment
# says which task.


def posttool_reasons(project_dir: Path) -> list[str]:
    events = [
        e for e in hook_log_lines(project_dir) if e["event"] == "posttool_artifact_guard"
    ]
    assert len(events) == 1, events
    return events[0]["reason"].split(";")


def run_posttool(project_dir: Path, path: Path, **kwargs) -> subprocess.CompletedProcess:
    return run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        project_dir,
        **kwargs,
    )


def test_artifact_guard_missing_event_log_is_audit_only_in_block_mode(tmp_path):
    path = write_artifact(tmp_path)
    (path.parent / "wf-test.events.jsonl").unlink()
    r = run_posttool(tmp_path, path)  # shipped artifactIntegrity=block
    assert r.returncode == 0  # soft reason: never blocks
    assert posttool_reasons(tmp_path) == ["missing-event-log"]
    # UNOWNED defect: no P5 task changes this; the log says "block" on a path that exits 0.
    assert hook_log_lines(tmp_path)[0]["decision"] == "block"  # the mode, not an exit
    # A non-empty reason list skips the artifact_mutated auto-append.
    assert not (path.parent / "wf-test.events.jsonl").exists()


def test_artifact_guard_missing_updated_at_is_audit_only_in_block_mode(tmp_path):
    path = write_artifact(tmp_path, updated_at="")
    r = run_posttool(tmp_path, path)
    assert r.returncode == 0
    assert posttool_reasons(tmp_path) == ["missing-updated-at"]


def test_artifact_guard_stale_artifact_write_is_audit_only_in_block_mode(tmp_path):
    import os
    import time

    path = write_artifact(tmp_path)
    old = time.time() - 600  # freshness window is 60s
    os.utime(path, (old, old))
    r = run_posttool(tmp_path, path)
    assert r.returncode == 0
    assert posttool_reasons(tmp_path) == ["stale-artifact-write"]


def test_artifact_guard_updated_at_checks_apply_only_to_the_written_artifact(tmp_path):
    # Writing an unrelated file never evaluates updated_at/staleness of the
    # latest artifact, even when that artifact lacks updated_at.
    write_artifact(tmp_path, updated_at="")
    r = run_posttool(tmp_path, tmp_path / "src.py")
    assert r.returncode == 0
    assert hook_log_lines(tmp_path) == []


def test_artifact_guard_blocks_review_closure_mismatch(tmp_path):
    path = write_artifact(
        tmp_path,
        planning_review_status="passed",
        plan_revision=2,
        last_reviewed_revision=1,
    )
    r = run_posttool(tmp_path, path)
    assert r.returncode == 2
    assert "review-closure:plan_revision=2,last_reviewed_revision=1" in r.stderr
    assert "revised_after_review" in r.stderr


def test_artifact_guard_hard_corruption_is_audit_when_mode_is_audit(tmp_path):
    root = mode_root(tmp_path, {"artifactIntegrity": "audit"})
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text("{not json")
    r = run_posttool(tmp_path, bad, plugin_root=root)
    assert r.returncode == 0
    assert hook_log_lines(tmp_path)[0]["decision"] == "audit"


def test_artifact_guard_mode_file_without_the_key_keeps_the_block_default(tmp_path):
    # P5.T3: a partial hook-mode.json is merged over HOOK_MODE_DEFAULTS, so a
    # file lacking artifactIntegrity can no longer downgrade block to audit.
    root = mode_root(tmp_path, {})
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_posttool(tmp_path, bad, plugin_root=root)
    assert r.returncode == 2
    assert hook_log_lines(tmp_path)[0]["decision"] == "block"


def run_precommit_with_pytest_exit(tmp_path: Path, exit_code: int) -> int:
    """Run hooks/pre-commit in a Python project whose `python -m pytest`
    exits with `exit_code` (hermetic shim — no real pytest dependency)."""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\nversion='0'\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    shim = bin_dir / "python"
    shim.write_text(
        "#!/bin/bash\n"
        'if [ "$1" = "-m" ] && [ "$2" = "pytest" ]; then\n'
        f"  exit {exit_code}\n"
        "fi\n"
        "exit 0\n"
    )
    shim.chmod(0o755)
    r = subprocess.run(
        ["/bin/bash", str(PLUGIN_ROOT / "hooks" / "pre-commit")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={"PATH": f"{bin_dir}:/usr/bin:/bin"},
        timeout=60,
    )
    return r.returncode


def test_precommit_passes_when_pytest_collects_no_tests(tmp_path):
    # pytest exits 5 on zero collected tests; the hook treated that as
    # failure, bricking commits in test-less Python repos.
    assert run_precommit_with_pytest_exit(tmp_path, 5) == 0


def test_precommit_still_blocks_on_real_test_failure(tmp_path):
    assert run_precommit_with_pytest_exit(tmp_path, 1) == 1


# --- P5.T1: state_root precedence, Bash-written artifacts, QA matcher -------


def make_checkout(path: Path, kind: str = "dir") -> Path:
    path.mkdir(parents=True, exist_ok=True)
    if kind == "dir":
        (path / ".git").mkdir()
    else:
        (path / ".git").write_text("gitdir: ../elsewhere/.git/worktrees/wt\n")
    return path


def sessionstart_wf(project_dir: Path, cwd: Path | None, source: str = "startup"):
    payload: dict = {"source": source}
    if cwd is not None:
        payload["cwd"] = str(cwd)
    r = run_guard("cc10x_sessionstart_context.py", payload, project_dir)
    assert r.returncode == 0, r.stderr
    if not r.stdout.strip():
        return None
    context = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    return context.split("wf=", 1)[1].split()[0]


def test_state_root_follows_hook_cwd_into_a_worktree(tmp_path):
    main = make_checkout(tmp_path / "main")
    write_artifact(main, "wf-main")
    wt = make_worktree(tmp_path / "wt", main)
    write_artifact(wt, "wf-wt")
    deep = wt / "src" / "deep"
    deep.mkdir(parents=True)
    # CLAUDE_PROJECT_DIR stays on the main checkout; cwd follows Claude.
    assert sessionstart_wf(main, deep) == "wf-wt"


def test_state_root_never_selects_a_nested_cc10x(tmp_path):
    repo = make_checkout(tmp_path / "repo")
    write_artifact(repo, "wf-root")
    nested = repo / "plugins" / "cc10x"
    nested.mkdir(parents=True)
    write_artifact(nested, "wf-nested")
    assert sessionstart_wf(repo, nested) == "wf-root"


def test_state_root_without_any_git_entry_uses_claude_project_dir(tmp_path):
    proj = tmp_path / "proj"
    write_artifact(proj, "wf-proj")
    elsewhere = tmp_path / "elsewhere" / "sub"
    elsewhere.mkdir(parents=True)
    write_artifact(elsewhere, "wf-decoy")
    assert sessionstart_wf(proj, elsewhere) == "wf-proj"


def test_state_root_ignores_an_unrelated_checkout_around_the_hook_cwd(tmp_path):
    outer = make_checkout(tmp_path / "outer")
    write_artifact(outer, "wf-outer")
    wt = make_checkout(outer / "wt", kind="file")  # a .git file that links nowhere
    cwd = wt / "x"
    cwd.mkdir()
    proj = tmp_path / "proj"
    write_artifact(proj, "wf-proj")
    assert sessionstart_wf(proj, cwd) == "wf-proj"
    # A .git DIRECTORY at that root is another repository, not this project's.
    (wt / ".git").unlink()
    (wt / ".git").mkdir()
    write_artifact(wt, "wf-stale")
    assert sessionstart_wf(proj, cwd) == "wf-proj"


def test_state_root_never_picks_a_nested_repos_stale_cc10x(tmp_path):
    proj = make_checkout(tmp_path / "proj")
    write_artifact(proj, "wf-proj")
    nested = make_checkout(proj / "vendor" / "lib")
    write_artifact(nested, "wf-stale")
    cwd = nested / "src"
    cwd.mkdir()
    assert sessionstart_wf(proj, cwd) == "wf-proj"


def test_state_root_never_picks_a_home_repo_above_a_project_without_git(tmp_path):
    home = make_checkout(tmp_path / "home")
    write_artifact(home, "wf-home")
    proj = home / "work" / "proj"
    write_artifact(proj, "wf-proj")
    cwd = proj / "sub"
    cwd.mkdir()
    assert sessionstart_wf(proj, cwd) == "wf-proj"


def test_state_root_accepts_the_project_checkout_itself_and_its_worktree_both_ways(tmp_path):
    main = make_checkout(tmp_path / "main")
    write_artifact(main, "wf-main")
    sub = main / "pkg"
    sub.mkdir()
    assert sessionstart_wf(main, sub) == "wf-main"
    wt = make_worktree(tmp_path / "wt", main)
    write_artifact(wt, "wf-wt")
    # The session may also have been launched inside the linked worktree.
    assert sessionstart_wf(wt, main) == "wf-main"


def test_state_root_falls_back_to_project_dir_without_cwd(tmp_path):
    proj = make_checkout(tmp_path / "proj")
    write_artifact(proj, "wf-proj")
    assert sessionstart_wf(proj, None) == "wf-proj"


def test_state_root_never_creates_a_directory(tmp_path):
    checkout = make_checkout(tmp_path / "co")
    proj = tmp_path / "proj"
    proj.mkdir()
    cwd = checkout / "src"
    cwd.mkdir()
    runs = [
        ("cc10x_sessionstart_context.py", {"source": "startup"}, []),
        ("cc10x_state_persist.py", {}, ["stop"]),
        ("cc10x_state_persist.py", {}, ["precompact"]),
        ("cc10x_event_logger.py", {"agent_type": "cc10x:planner"}, ["subagent_stop"]),
        (
            "cc10x_posttooluse_artifact_guard.py",
            {"tool_name": "Write", "tool_input": {"file_path": "a.txt"}},
            [],
        ),
    ]
    for script, payload, argv in runs:
        r = run_guard(script, {**payload, "cwd": str(cwd)}, proj, argv=argv)
        assert r.returncode == 0, (script, r.stderr)
    assert not (checkout / ".cc10x").exists()
    assert not (proj / ".cc10x").exists()


def bash_posttool(project_dir: Path, command: str) -> subprocess.CompletedProcess:
    return run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Bash", "tool_input": {"command": command}},
        project_dir,
    )


def test_bash_command_writing_into_workflows_is_audited_never_blocked(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    commands = [
        "cp skeleton.json .cc10x/workflows/wf-x.json",
        "cat > .cc10x/workflows/wf-x.json <<'EOF'\n{}\nEOF",
        "echo '{}' >> .cc10x/workflows/wf-x.events.jsonl",
        "printf x | tee .cc10x/workflows/wf-x.json",
        "mv /tmp/a.json .cc10x/workflows/wf-x.json",
        "sed -i 's/a/b/' .cc10x/workflows/wf-x.json",
    ]
    for command in commands:
        r = bash_posttool(tmp_path, command)
        assert r.returncode == 0, (command, r.stderr)
        assert r.stderr == "" and r.stdout == "", command
    events = [
        e for e in hook_log_lines(tmp_path) if e["event"] == "bash_workflow_write"
    ]
    assert len(events) == len(commands)
    assert all(e["decision"] == "audit" for e in events)


def test_bash_reads_and_unrelated_writes_do_not_trip_the_workflow_audit(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    for command in [
        "cat .cc10x/workflows/wf-x.json",
        "ls .cc10x/workflows/",
        "grep wf .cc10x/workflows/wf-x.json > /tmp/out.txt",
        "echo hi > notes.txt",
        "mkdir -p .cc10x/workflows",
    ]:
        r = bash_posttool(tmp_path, command)
        assert r.returncode == 0, (command, r.stderr)
    assert not [
        e for e in hook_log_lines(tmp_path) if e["event"] == "bash_workflow_write"
    ]


def hooks_json_matcher(event: str, script: str) -> str:
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text())["hooks"]
    matchers = [
        group["matcher"]
        for group in hooks[event]
        if any(script in h["command"] for h in group["hooks"])
    ]
    assert len(matchers) == 1, matchers
    return matchers[0]


def test_posttool_artifact_guard_matcher_covers_edit_write_and_bash(tmp_path):
    # The only blocking guard must see artifact Edits and Writes, not just Bash.
    matcher = hooks_json_matcher("PostToolUse", "cc10x_posttooluse_artifact_guard.py")
    assert {"Edit", "Write", "Bash"} <= set(matcher.split("|")), matcher


def test_artifact_guard_hook_runs_synchronously(tmp_path):
    # An async hook's exit 2 reaches the model later, if at all; the guard must report with the write it checks.
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text())["hooks"]
    entries = [
        hook
        for group in hooks["PostToolUse"]
        for hook in group["hooks"]
        if "cc10x_posttooluse_artifact_guard.py" in hook["command"]
    ]
    assert len(entries) == 1, entries
    assert not {"async", "asyncRewake"} & set(entries[0]), entries[0]


# --- P5.T2: logger documented fields, SubagentHandback report, guard channels --


def write_agent_transcript(path: Path, *entries: dict, padding: int = 0) -> Path:
    lines = ["x" * padding] if padding else []
    lines += [json.dumps(entry) for entry in entries]
    path.write_text("\n".join(lines) + "\n")
    return path


def handback_entry(message: str) -> dict:
    return {
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "name": "SubagentHandback",
                    "input": {"message": message},
                }
            ],
        },
    }


def text_entry(text: str) -> dict:
    return {
        "type": "assistant",
        "message": {"role": "assistant", "content": [{"type": "text", "text": text}]},
    }


def subagent_stop_event(tmp_path: Path, payload: dict) -> dict:
    (tmp_path / ".cc10x").mkdir(exist_ok=True)
    r = run_guard("cc10x_event_logger.py", payload, tmp_path, argv=["subagent_stop"])
    assert r.returncode == 0, r.stderr
    assert r.stderr == ""
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "subagent_stop"]
    assert len(events) == 1, events
    return events[0]


CONTRACT_REPORT = 'CONTRACT {"s":"PASS","b":false,"cr":0}\n## Build: PASS'


def test_event_logger_reads_the_handback_report_when_the_final_message_is_empty(tmp_path):
    transcript = write_agent_transcript(
        tmp_path / "agent.jsonl",
        text_entry("working"),
        handback_entry(CONTRACT_REPORT),
    )
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:component-builder",
            "agent_id": "a1",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": "",
        },
    )
    assert e["contract_found"] is True
    assert e["reason"] == "contract_present"
    assert e["report_source"] == "handback_report"
    assert e["message_len"] == 0


def test_event_logger_uses_the_last_handback_found_near_the_end_of_a_large_transcript(tmp_path):
    transcript = write_agent_transcript(
        tmp_path / "agent.jsonl",
        handback_entry("an earlier report without an envelope"),
        text_entry("revised"),
        handback_entry(CONTRACT_REPORT),
        padding=3_000_000,
    )
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": "",
        },
    )
    assert e["contract_found"] is True
    assert e["report_source"] == "handback_report"


def test_event_logger_reports_a_miss_when_no_handback_report_exists(tmp_path):
    transcript = write_agent_transcript(
        tmp_path / "agent.jsonl", text_entry("no envelope here")
    )
    cases = [
        {"agent_transcript_path": str(transcript)},
        {"agent_transcript_path": ""},
        {},
    ]
    for extra in cases:
        e = subagent_stop_event(
            tmp_path,
            {"agent_type": "cc10x:code-reviewer", "last_assistant_message": "", **extra},
        )
        assert e["contract_found"] is False
        assert e["reason"] == "contract_missing"
        assert e["report_source"] == "none"
        (tmp_path / ".cc10x" / "cc10x-hook-events.log").unlink()


def test_event_logger_survives_a_corrupt_agent_transcript(tmp_path):
    transcript = tmp_path / "agent.jsonl"
    transcript.write_text("{not json\n" + json.dumps(handback_entry("no envelope")) + "\n{")
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": "",
        },
    )
    assert e["contract_found"] is False
    assert e["report_source"] == "handback_report"


def test_event_logger_prefers_the_final_message_over_the_transcript(tmp_path):
    transcript = write_agent_transcript(
        tmp_path / "agent.jsonl", handback_entry("no envelope in the report")
    )
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": CONTRACT_REPORT,
        },
    )
    assert e["contract_found"] is True
    assert e["report_source"] == "last_assistant_message"


def test_event_logger_instructions_loaded_logs_only_documented_fields(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    r = run_guard(
        "cc10x_event_logger.py",
        {
            "file_path": "/proj/CLAUDE.md",
            "memory_type": "Project",
            "load_reason": "session_start",
            "instructions_hash": "undocumented",
            "instruction_count": 9,
        },
        tmp_path,
        argv=["instructions_loaded"],
    )
    assert r.returncode == 0
    (e,) = [e for e in hook_log_lines(tmp_path) if e["event"] == "instructions_loaded"]
    assert e["file_path"] == "/proj/CLAUDE.md"
    assert e["memory_type"] == "Project"
    assert e["load_reason"] == "session_start"
    assert "instructions_hash" not in e and "instruction_count" not in e


def test_event_logger_stop_failure_logs_only_documented_fields(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    r = run_guard(
        "cc10x_event_logger.py",
        {"error": "rate_limit", "error_details": "429", "stop_hook_active": True},
        tmp_path,
        argv=["stop_failure"],
    )
    assert r.returncode == 0
    (e,) = [e for e in hook_log_lines(tmp_path) if e["event"] == "stop_failure"]
    assert e["error"] == "rate_limit"
    assert e["error_details"] == "429"
    assert "stop_hook_active" not in e


def test_event_logger_postcompact_without_a_workflow_id_writes_no_none_log(tmp_path):
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "wf-legacy.json").write_text(json.dumps({"phase_cursor": "p1"}))
    r = run_guard(
        "cc10x_event_logger.py",
        {"trigger": "auto", "compact_summary": "s"},
        tmp_path,
        argv=["postcompact"],
    )
    assert r.returncode == 0
    assert not list(workflows.glob("None*"))
    assert sorted(p.name for p in workflows.iterdir()) == ["wf-legacy.json"]


# --- P5.T3: hook-mode resolver ------------------------------------------------


def load_hooklib():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import cc10x_hooklib

    return cc10x_hooklib


class env_patch:
    """Set (str) or unset (None) environment variables for the with-block."""

    def __init__(self, **values: str | None):
        self.values = values

    def __enter__(self):
        self.saved = {k: os.environ.get(k) for k in self.values}
        for key, value in self.values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def __exit__(self, *exc):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def resolved_mode(
    tmp_path: Path, shipped: object | None, override: object | None = None, data_dir: bool = True
) -> tuple[dict, list[dict]]:
    """load_mode() against a synthetic plugin root, optional override file and
    an opted-in project (.cc10x exists so events are recorded)."""
    root = tmp_path / "plugin-root"
    (root / "config").mkdir(parents=True, exist_ok=True)
    cfg = root / "config" / "hook-mode.json"
    if shipped is not None:
        cfg.write_text(shipped if isinstance(shipped, str) else json.dumps(shipped))
    data = tmp_path / "plugin-data"
    if override is not None:
        data.mkdir(exist_ok=True)
        (data / "hook-mode.json").write_text(
            override if isinstance(override, str) else json.dumps(override)
        )
    proj = tmp_path / "proj"
    (proj / ".cc10x").mkdir(parents=True, exist_ok=True)
    with env_patch(
        CLAUDE_PLUGIN_ROOT=str(root),
        CLAUDE_PLUGIN_DATA=str(data) if data_dir else None,
        CLAUDE_PROJECT_DIR=str(proj),
    ):
        modes = load_hooklib().load_mode()
    return modes, [e for e in hook_log_lines(proj) if e["event"] == "invalid_hook_mode"]


DEFAULT_MODES = {"artifactIntegrity": "block"}


def test_load_mode_missing_shipped_file_returns_all_defaults(tmp_path):
    modes, events = resolved_mode(tmp_path, None)
    assert modes == DEFAULT_MODES
    assert events == []


def test_load_mode_corrupt_json_falls_back_and_records_an_event(tmp_path):
    modes, events = resolved_mode(tmp_path, "{not json")
    assert modes == DEFAULT_MODES
    assert len(events) == 1 and events[0]["source"] == "shipped"


def test_load_mode_unknown_value_falls_back_for_that_key_only(tmp_path):
    modes, events = resolved_mode(tmp_path, {"artifactIntegrity": "warn"})
    assert modes == {"artifactIntegrity": "block"}
    assert [e["key"] for e in events] == ["artifactIntegrity"]


def test_load_mode_partial_file_keeps_defaults_for_missing_keys(tmp_path):
    modes, events = resolved_mode(tmp_path, {})
    assert modes == {"artifactIntegrity": "block"}
    assert events == []


def test_load_mode_user_override_wins_over_the_shipped_file(tmp_path):
    modes, events = resolved_mode(
        tmp_path,
        {"artifactIntegrity": "block"},
        override={"artifactIntegrity": "audit", "extra": "block"},
    )
    assert modes == {"artifactIntegrity": "audit"}
    assert events == []


def test_load_mode_invalid_override_value_falls_back_to_the_shipped_value(tmp_path):
    modes, events = resolved_mode(
        tmp_path, {"artifactIntegrity": "audit"}, override={"artifactIntegrity": "banana"}
    )
    assert modes["artifactIntegrity"] == "audit"
    assert [e["source"] for e in events] == ["override"]
    modes, events = resolved_mode(
        tmp_path / "corrupt", {"artifactIntegrity": "audit"}, override="{oops"
    )
    assert modes["artifactIntegrity"] == "audit"
    assert [e["source"] for e in events] == ["override"]


def test_load_mode_data_dir_absent_or_empty_is_not_an_error(tmp_path):
    modes, events = resolved_mode(tmp_path, {"artifactIntegrity": "audit"}, data_dir=False)
    assert modes["artifactIntegrity"] == "audit" and events == []
    root = tmp_path / "plugin-root"
    with env_patch(
        CLAUDE_PLUGIN_ROOT=str(root),
        CLAUDE_PLUGIN_DATA=str(tmp_path / "does-not-exist"),
        CLAUDE_PROJECT_DIR=str(tmp_path / "proj"),
    ):
        again = load_hooklib().load_mode()
    assert again["artifactIntegrity"] == "audit"
    assert not (tmp_path / "does-not-exist").exists()


def test_load_mode_never_raises_and_always_returns_the_one_key(tmp_path):
    for bad in ('[]', '"block"', "null", "7", '{"artifactIntegrity": ["block"]}'):
        modes, _ = resolved_mode(tmp_path / f"c{abs(hash(bad))}", bad)
        assert modes == DEFAULT_MODES, bad
    unreadable = tmp_path / "dirfile"
    (unreadable / "config").mkdir(parents=True)
    (unreadable / "config" / "hook-mode.json").mkdir()  # a directory, not a file
    with env_patch(CLAUDE_PLUGIN_ROOT=str(unreadable), CLAUDE_PLUGIN_DATA=None):
        assert load_hooklib().load_mode() == DEFAULT_MODES
    # An unreadable data dir: Path.exists() raises PermissionError on Python 3.9.
    # The override carries a real value, so honoring it and ignoring it give
    # different answers: readable -> audit, unreadable -> the block default.
    locked = tmp_path / "locked"
    locked.mkdir()
    (locked / "hook-mode.json").write_text(json.dumps({"artifactIntegrity": "audit"}))
    plain = tmp_path / "plain-root"
    (plain / "config").mkdir(parents=True)
    with env_patch(CLAUDE_PLUGIN_ROOT=str(plain), CLAUDE_PLUGIN_DATA=str(locked)):
        assert load_hooklib().load_mode()["artifactIntegrity"] == "audit"
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return  # root reads a mode-0 directory; the unreadable half is meaningless
    locked.chmod(0)
    try:
        with env_patch(CLAUDE_PLUGIN_ROOT=str(plain), CLAUDE_PLUGIN_DATA=str(locked)):
            assert load_hooklib().load_mode() == DEFAULT_MODES
    finally:
        locked.chmod(0o700)


def test_shipped_hook_mode_file_is_valid_and_complete(tmp_path):
    shipped = json.loads((PLUGIN_ROOT / "config" / "hook-mode.json").read_text())
    assert shipped == DEFAULT_MODES
    assert shipped == load_hooklib().HOOK_MODE_DEFAULTS


def test_hooks_json_registers_no_removed_guard_and_every_registered_script_exists(tmp_path):
    text = (PLUGIN_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8")
    for removed in (
        "cc10x_git_guard.py",
        "cc10x_qa_isolation_guard.py",
        "cc10x_pretooluse_guard.py",
        "cc10x_task_completed_guard.py",
    ):
        assert removed not in text, removed
    for argv in registered_hook_commands():
        script = Path(argv[1])
        assert script.parent == SCRIPTS_DIR and script.is_file(), argv
    assert set(json.loads(text)["hooks"]) == {
        "SessionStart",
        "PostToolUse",
        "PostCompact",
        "SubagentStop",
        "PreCompact",
        "Stop",
        "StopFailure",
        "InstructionsLoaded",
    }


def test_hook_mode_defaults_hold_only_artifact_integrity(tmp_path):
    hooklib = load_hooklib()
    assert hooklib.HOOK_MODE_DEFAULTS == {"artifactIntegrity": "block"}
    assert hooklib.HOOK_MODE_VALUES == ("block", "audit")
    shipped = json.loads((PLUGIN_ROOT / "config" / "hook-mode.json").read_text())
    assert shipped == {"artifactIntegrity": "block"}


def test_an_override_with_obsolete_keys_resolves_without_an_invalid_hook_mode_event(tmp_path):
    modes, events = resolved_mode(
        tmp_path,
        None,
        override={
            "memoryWrites": "block",
            "taskMetadata": "block",
            "gitGuard": "ask",
            "artifactIntegrity": "audit",
        },
    )
    assert modes == {"artifactIntegrity": "audit"}
    assert events == []


def test_user_override_file_downgrades_the_artifact_guard_end_to_end(tmp_path):
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "hook-mode.json").write_text(json.dumps({"artifactIntegrity": "audit"}))
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(bad)}},
        tmp_path,
        extra_env={"CLAUDE_PLUGIN_DATA": str(data)},
    )
    assert r.returncode == 0
    assert hook_log_lines(tmp_path)[0]["decision"] == "audit"
    # Without the override file the shipped block default applies.
    r = run_posttool(tmp_path, bad)
    assert r.returncode == 2


# --- P5.T5: SessionStart coverage and terminal-artifact selection (B14) -------


def set_age(path: Path, seconds_ago: float) -> None:
    stamp = time.time() - seconds_ago
    os.utime(path, (stamp, stamp))


def test_sessionstart_matcher_covers_every_documented_source(tmp_path):
    matcher = hooks_json_matcher("SessionStart", "cc10x_sessionstart_context.py")
    assert set(matcher.split("|")) == {"startup", "resume", "clear", "compact", "fork"}
    assert hooks_json_matcher("SessionStart", "cc10x_preflight.sh") == matcher


def test_sessionstart_handler_tolerates_clear_and_fork_payloads(tmp_path):
    write_artifact(tmp_path, phase_status={"phase-1": "in_progress"})
    for source in ("clear", "fork"):
        payload = {
            "hook_event_name": "SessionStart",
            "source": source,
            "session_title": "t",
            "seconds_since_last_response": 12,
            "prompt_cache_likely_expired": False,
        }
        r = run_guard("cc10x_sessionstart_context.py", payload, tmp_path)
        assert r.returncode == 0, r.stderr
        assert r.stderr == ""
        context = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        assert f"({source})" in context and "wf=wf-test" in context


FINISHED_EVENTS = ("memory_finalized", "workflow_completed", "workflow_failed")


def test_hooks_pick_the_live_workflow_over_a_newer_finished_one(tmp_path):
    for event in FINISHED_EVENTS:
        live = write_artifact(tmp_path, "wf-aaa")
        done = write_artifact(
            tmp_path,
            "wf-bbb",
            status_history=[{"event": "started"}, {"event": event}],
        )
        set_age(live, 300)
        set_age(done, 10)  # the finished one is the newest by mtime
        assert sessionstart_wf(tmp_path, None) == "wf-aaa", event


def test_a_workflow_that_resumed_after_a_terminal_event_is_live(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    resumed = write_artifact(
        tmp_path,
        "wf-ccc",
        status_history=[{"event": "memory_finalized"}, {"event": "resumed"}],
    )
    set_age(live, 300)
    set_age(resumed, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-ccc"


def test_a_finalizing_workflow_without_the_finalized_event_is_still_live(tmp_path):
    write_artifact(
        tmp_path,
        "wf-ddd",
        phase_cursor="memory-finalize",
        status_history=[{"event": "started"}],
    )
    assert sessionstart_wf(tmp_path, None) == "wf-ddd"


def test_only_finished_workflows_means_no_resume_context(tmp_path):
    write_artifact(
        tmp_path, "wf-bbb", status_history=[{"event": "memory_finalized"}]
    )
    assert sessionstart_wf(tmp_path, None) is None


def test_a_corrupt_newest_artifact_is_surfaced_not_skipped_by_latest_selection(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    corrupt = tmp_path / ".cc10x" / "workflows" / "wf-zzz.json"
    corrupt.write_text("{not json")
    set_age(live, 300)
    set_age(corrupt, 10)
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "src.py")}},
        tmp_path,
    )
    assert r.returncode == 0
    assert any(
        "artifact-json:" in e["reason"] for e in hook_log_lines(tmp_path)
    )


def test_state_snapshots_follow_the_live_workflow_not_the_newest_file(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    done = write_artifact(
        tmp_path, "wf-bbb", status_history=[{"event": "workflow_completed"}]
    )
    set_age(live, 300)
    set_age(done, 10)
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    assert r.returncode == 0
    snapshot = json.loads((tmp_path / ".cc10x" / "stop-state.json").read_text())
    assert snapshot["workflow_uuid"] == "wf-aaa"


def test_resume_consumers_skip_a_workflow_finished_by_cursor_and_completed_phase(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    done = write_artifact(
        tmp_path,
        "wf-bbb",
        phase_cursor="memory-finalize",
        phase_status={"memory-finalize": "completed"},
    )
    set_age(live, 300)
    set_age(done, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"


def append_events(project: Path, wf: str, *records: dict) -> None:
    log = project / ".cc10x" / "workflows" / f"{wf}.events.jsonl"
    with log.open("a") as fh:
        for record in records:
            fh.write(json.dumps(record) + "\n")


def test_resume_consumers_read_a_terminal_event_from_the_events_log(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    done = write_artifact(tmp_path, "wf-bbb", status_history=[{"event": "started"}])
    append_events(
        tmp_path,
        "wf-bbb",
        {"event": "memory_finalized", "agent": "router"},
        {"event": "artifact_mutated", "agent": "hook"},
    )
    set_age(live, 300)
    set_age(done, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"


def test_a_workflow_resumed_after_a_terminal_events_log_record_is_live(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa")
    resumed = write_artifact(tmp_path, "wf-bbb", status_history=[{"event": "started"}])
    append_events(
        tmp_path,
        "wf-bbb",
        {"event": "memory_finalized", "agent": "router"},
        {"event": "phase_started", "agent": "router"},
    )
    set_age(live, 300)
    set_age(resumed, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-bbb"


def test_an_unreadable_newest_artifact_is_logged_by_every_consumer(tmp_path):
    older = write_artifact(tmp_path, "wf-aaa")
    set_age(older, 300)
    bad = tmp_path / ".cc10x" / "workflows" / "wf-zzz.json"
    bad.write_text("{not json")
    runs = [
        ("cc10x_state_persist.py", {}, ["stop"]),
        ("cc10x_event_logger.py", {"trigger": "auto"}, ["postcompact"]),
    ]
    for script, payload, argv in runs:
        before = len(hook_log_lines(tmp_path))
        r = run_guard(script, payload, tmp_path, argv=argv)
        assert r.returncode == 0, (script, r.stderr)
        new = hook_log_lines(tmp_path)[before:]
        assert any(e["event"] == "workflow_artifact_unreadable" for e in new), script



# --- P5 remediation 1, group C: visibility ------------------------------------


def test_sessionstart_survives_odd_artifact_field_shapes(tmp_path):
    shapes = (
        {"phase_status": ["a", "b"]},
        {"phase_status": "done"},
        {"research_quality": "high"},
        {"research_quality": 5, "phase_status": None},
    )
    for index, fields in enumerate(shapes):
        proj = tmp_path / f"p{index}"
        write_artifact(proj, "wf-shape", **fields)
        r = run_guard("cc10x_sessionstart_context.py", {"source": "resume"}, proj)
        assert r.returncode == 0 and r.stderr == "", (fields, r.stderr[-200:])
        context = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        assert "wf=wf-shape" in context, fields


def test_event_logger_survives_odd_payload_shapes(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    for argv in (["subagent_stop"], ["postcompact"], ["instructions_loaded"], ["stop_failure"]):
        for payload in ([], "text", 5, None):
            r = run_guard("cc10x_event_logger.py", payload, tmp_path, argv=argv)
            assert r.returncode == 0 and r.stderr == "", (argv, payload, r.stderr[-200:])
    odd = [
        {"agent_type": 5},
        {"agent_type": ["cc10x:planner"]},
        {"agent_type": "cc10x:planner", "last_assistant_message": ["x"], "agent_transcript_path": 7},
        {"agent_type": "cc10x:planner", "agent_id": {"a": 1}, "agent_transcript_path": ["p"]},
    ]
    for payload in odd:
        r = run_guard("cc10x_event_logger.py", payload, tmp_path, argv=["subagent_stop"])
        assert r.returncode == 0 and r.stderr == "", (payload, r.stderr[-200:])


def test_event_logger_skips_a_handback_block_with_a_non_object_input(tmp_path):
    bad = handback_entry("x")
    bad["message"]["content"][0]["input"] = ["not", "an", "object"]
    transcript = write_agent_transcript(
        tmp_path / "agent.jsonl", handback_entry(CONTRACT_REPORT), bad
    )
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": "",
        },
    )
    assert e["contract_found"] is True


def test_state_persist_logs_failed_not_saved_when_the_snapshot_cannot_be_written(tmp_path):
    write_artifact(tmp_path, "wf-aaa")
    (tmp_path / ".cc10x" / "stop-state.json").mkdir()
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    assert r.returncode == 0
    events = [e for e in hook_log_lines(tmp_path) if e["event"].startswith("stop_state_")]
    assert [e["decision"] for e in events] == ["failed"]
    assert events[0]["event"] == "stop_state_save_failed"
    assert events[0]["reason"] == "IsADirectoryError"
    # The healthy path still reports saved.
    (tmp_path / ".cc10x" / "stop-state.json").rmdir()
    run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    last = [e for e in hook_log_lines(tmp_path) if e["event"].startswith("stop_state_")][-1]
    assert (last["event"], last["decision"]) == ("stop_state_saved", "saved")


def test_postcompact_logs_append_failed_when_the_workflow_event_cannot_be_written(tmp_path):
    write_artifact(tmp_path, "wf-aaa")
    events_log = tmp_path / ".cc10x" / "workflows" / "wf-aaa.events.jsonl"
    events_log.unlink()
    events_log.mkdir()
    r = run_guard(
        "cc10x_event_logger.py", {"trigger": "auto"}, tmp_path, argv=["postcompact"]
    )
    assert r.returncode == 0
    (e,) = [e for e in hook_log_lines(tmp_path) if e["event"] == "compact_occurred"]
    assert e["decision"] == "append_failed"


def test_event_logger_reads_a_handback_with_a_unicode_line_separator(tmp_path):
    for char in (" ", " ", "\u0085"):
        proj = tmp_path / f"p{ord(char)}"
        transcript = proj / "agent.jsonl"
        proj.mkdir()
        entry = handback_entry(CONTRACT_REPORT + "\nnote" + char + "more")
        transcript.write_bytes((json.dumps(entry, ensure_ascii=False) + "\n").encode("utf-8"))
        e = subagent_stop_event(
            proj,
            {
                "agent_type": "cc10x:planner",
                "agent_transcript_path": str(transcript),
                "last_assistant_message": "",
            },
        )
        assert e["contract_found"] is True, repr(char)
        assert e["report_source"] == "handback_report", repr(char)


def test_event_logger_tells_an_unreadable_or_truncated_transcript_from_a_missing_contract(tmp_path):
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(tmp_path / "missing.jsonl"),
            "last_assistant_message": "",
        },
    )
    assert (e["contract_found"], e["reason"]) == (False, "transcript_unreadable")
    (tmp_path / ".cc10x" / "cc10x-hook-events.log").unlink()
    transcript = tmp_path / "agent.jsonl"
    transcript.write_text(
        json.dumps(handback_entry(CONTRACT_REPORT)) + "\n" + "x" * 1_200_000 + "\n"
    )
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(transcript),
            "last_assistant_message": "",
        },
    )
    assert (e["contract_found"], e["reason"]) == (False, "transcript_truncated")
    (tmp_path / ".cc10x" / "cc10x-hook-events.log").unlink()
    plain = write_agent_transcript(tmp_path / "plain.jsonl", text_entry("no envelope"))
    e = subagent_stop_event(
        tmp_path,
        {
            "agent_type": "cc10x:planner",
            "agent_transcript_path": str(plain),
            "last_assistant_message": "",
        },
    )
    assert (e["contract_found"], e["reason"]) == (False, "contract_missing")


def invalid_mode_events(project: Path) -> list[dict]:
    return [e for e in hook_log_lines(project) if e["event"] == "invalid_hook_mode"]


def test_load_mode_logs_an_unexpected_failure_once_per_process(tmp_path):
    from unittest import mock

    hooklib = load_hooklib()
    (tmp_path / ".cc10x").mkdir()
    with env_patch(CLAUDE_PROJECT_DIR=str(tmp_path)):
        with mock.patch.object(hooklib, "_read_mode_layer", side_effect=RuntimeError("boom")):
            assert hooklib.load_mode() == DEFAULT_MODES
            assert hooklib.load_mode() == DEFAULT_MODES
    events = invalid_mode_events(tmp_path)
    assert len(events) == 1
    assert events[0]["reason"] == "unexpected:RuntimeError"


def test_load_mode_logs_the_same_invalid_file_once_per_process(tmp_path):
    hooklib = load_hooklib()
    root = tmp_path / "plugin-root"
    (root / "config").mkdir(parents=True)
    (root / "config" / "hook-mode.json").write_text("{not json")
    proj = tmp_path / "proj"
    (proj / ".cc10x").mkdir(parents=True)
    with env_patch(
        CLAUDE_PLUGIN_ROOT=str(root), CLAUDE_PLUGIN_DATA=None, CLAUDE_PROJECT_DIR=str(proj)
    ):
        hooklib.load_mode()
        hooklib.load_mode()
    assert len(invalid_mode_events(proj)) == 1


def test_artifact_guard_does_not_load_the_mode_for_bash_calls(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "hook-mode.json").write_text('{"artifactIntegrity": "Audit"}')
    env = {"CLAUDE_PLUGIN_DATA": str(data)}
    for _ in range(3):
        r = run_guard(
            "cc10x_posttooluse_artifact_guard.py",
            {"tool_name": "Bash", "tool_input": {"command": "ls"}},
            tmp_path,
            extra_env=env,
        )
        assert r.returncode == 0
    assert invalid_mode_events(tmp_path) == []
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "a.txt")}},
        tmp_path,
        extra_env=env,
    )
    assert len(invalid_mode_events(tmp_path)) == 1


def test_a_workflow_id_from_artifact_content_cannot_escape_the_workflows_dir(tmp_path):
    escape = tmp_path / "escape.events.jsonl"
    escape.write_text("")
    path = write_artifact(tmp_path, "wf-aaa", workflow_uuid="../../escape", workflow_id="../../escape")
    # Posttool auto-append and postcompact both build an events path from the id.
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode in (0, 2)
    r = run_guard("cc10x_event_logger.py", {"trigger": "auto"}, tmp_path, argv=["postcompact"])
    assert r.returncode == 0
    assert escape.read_text() == ""
    assert sorted(p.name for p in tmp_path.iterdir()) == [".cc10x", "escape.events.jsonl"]
    assert not list((tmp_path / ".cc10x").glob("escape*"))



def test_an_unsafe_workflow_id_checks_the_events_log_by_the_artifact_name(tmp_path):
    path = write_artifact(tmp_path, "wf-aaa", workflow_uuid="../../nowhere", workflow_id="../../nowhere")
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode == 0, r.stderr
    assert "missing-event-log" not in " ".join(e["reason"] for e in hook_log_lines(tmp_path))


def make_worktree(path: Path, main: Path, name: str = "wt") -> Path:
    gitdir = main / ".git" / "worktrees" / name
    gitdir.mkdir(parents=True, exist_ok=True)
    (gitdir / "commondir").write_text("../..\n")
    (gitdir / "gitdir").write_text(str(path / ".git") + "\n")
    path.mkdir(parents=True, exist_ok=True)
    (path / ".git").write_text(f"gitdir: {gitdir}\n")
    return path


# --- P5 remediation 2, group B: readers and selection --------------------------

NON_OBJECT_JSON = ("[]", "[1]", '"s"', "5", "null", "true")


def _project_with_raw_artifact(root: Path, body: str, name: str = "wf-zzz") -> Path:
    workflows = root / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    path = workflows / f"{name}.json"
    path.write_text(body)
    return path


def test_a_non_object_artifact_never_crashes_a_hook_and_is_logged_once(tmp_path):
    for index, body in enumerate(NON_OBJECT_JSON):
        proj = tmp_path / f"p{index}"
        _project_with_raw_artifact(proj, body)
        runs = [
            ("cc10x_sessionstart_context.py", {"source": "startup"}, []),
            ("cc10x_state_persist.py", {}, ["stop"]),
            ("cc10x_event_logger.py", {"trigger": "auto"}, ["postcompact"]),
        ]
        for script, payload, argv in runs:
            before = len(hook_log_lines(proj))
            r = run_guard(script, payload, proj, argv=argv)
            assert r.returncode in (0, 2), (body, script, r.stderr[-300:])
            assert "Traceback" not in r.stderr, (body, script, r.stderr[-300:])
            events = [
                e
                for e in hook_log_lines(proj)[before:]
                if e["event"] == "workflow_artifact_unreadable"
            ]
            assert len(events) == 1, (body, script, events)
            assert events[0]["reason"] == "NotAnObject", (body, script)


def test_a_non_object_artifact_through_the_posttool_guard_is_a_corrupt_artifact(tmp_path):
    for index, body in enumerate(NON_OBJECT_JSON):
        proj = tmp_path / f"p{index}"
        path = _project_with_raw_artifact(proj, body)
        r = run_guard(
            "cc10x_posttooluse_artifact_guard.py",
            {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
            proj,
        )
        assert r.returncode == 2, (body, r.returncode, r.stderr[-300:])
        assert "Traceback" not in r.stderr, (body, r.stderr[-300:])
        assert any(
            "artifact-json:NotAnObject" in e.get("reason", "") for e in hook_log_lines(proj)
        ), body


def test_unhashable_phase_fields_never_crash_a_hook(tmp_path):
    shapes = (
        {"phase_cursor": ["qa-plan"]},
        {"phase_cursor": {"a": 1}},
        {"phase_cursor": None, "status_history": [{"phase": ["qa-plan"]}]},
        {"phase_cursor": None, "status_history": [{"phase": {"a": 1}}]},
        {"phase_cursor": ["x"], "phase_status": {"a": ["in_progress"]}},
    )
    for index, fields in enumerate(shapes):
        proj = tmp_path / f"p{index}"
        art = write_artifact(proj, "wf-odd", workflow_type="QA", **fields)
        for script, payload, argv, exits in (
            ("cc10x_sessionstart_context.py", {"source": "resume"}, [], (0,)),
            ("cc10x_state_persist.py", {}, ["stop"], (0,)),
            (
                "cc10x_posttooluse_artifact_guard.py",
                {"tool_name": "Write", "tool_input": {"file_path": str(art)}},
                [],
                (0, 2),
            ),
        ):
            r = run_guard(script, payload, proj, argv=argv)
            assert r.returncode in exits, (fields, script, r.stderr[-300:])
            assert "Traceback" not in r.stderr, (fields, script, r.stderr[-300:])


def test_a_stray_non_workflow_json_is_never_the_newest_artifact(tmp_path):
    set_age(write_artifact(tmp_path, "wf-a1"), 3000)
    stray = tmp_path / ".cc10x" / "workflows" / "settings.json"
    stray.write_text('{"unrelated": true}')
    set_age(stray, 10)
    r = run_guard("cc10x_event_logger.py", {"trigger": "manual"}, tmp_path, argv=["postcompact"])
    assert r.returncode == 0, r.stderr
    workflows = tmp_path / ".cc10x" / "workflows"
    assert "compact_occurred" in (workflows / "wf-a1.events.jsonl").read_text()
    assert not (workflows / "settings.events.jsonl").exists()
    live = write_artifact(tmp_path, "wf-aaa")
    set_age(live, 300)
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"


def test_an_unreadable_newer_artifact_does_not_hide_an_older_live_one_from_resume(tmp_path):
    live = write_artifact(tmp_path, "wf-aaa", phase_status={"phase-1": "in_progress"})
    set_age(live, 300)
    bad = tmp_path / ".cc10x" / "workflows" / "wf-zzz.json"
    bad.write_text("{not json")
    set_age(bad, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "workflow_artifact_unreadable"]
    assert len(events) == 1 and events[0]["path"].endswith("wf-zzz.json")
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    snapshot = json.loads((tmp_path / ".cc10x" / "stop-state.json").read_text())
    assert snapshot["workflow_uuid"] == "wf-aaa"


def test_sessionstart_says_an_unreadable_artifact_not_the_newest_one(tmp_path):
    _project_with_raw_artifact(tmp_path, "{not json", "wf-corrupt")
    r = run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    context = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "an unreadable workflow artifact wf-corrupt.json" in context
    assert "newest" not in context


def _bare_env_run(script: str, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    env = {"CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT), "PATH": "/usr/bin:/bin"}
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        timeout=30,
    )


def test_state_root_without_a_project_dir_env_uses_the_checkout_root_of_a_subdirectory(tmp_path):
    repo = make_checkout(tmp_path / "repo")
    write_artifact(repo, "wf-root")
    sub = repo / "pkg" / "deep"
    sub.mkdir(parents=True)
    r = _bare_env_run("cc10x_sessionstart_context.py", {"source": "startup", "cwd": str(sub)}, sub)
    assert r.returncode == 0, r.stderr
    assert "wf=wf-root" in json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    r = _bare_env_run("cc10x_sessionstart_context.py", {"source": "startup"}, sub)
    assert "wf=wf-root" in json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]


def test_a_relative_hook_input_cwd_is_made_absolute(tmp_path):
    import contextlib
    import io
    from unittest import mock

    import cc10x_hooklib

    repo = make_checkout(tmp_path / "repo")
    (repo / ".cc10x").mkdir()
    (repo / "sub").mkdir()
    previous = os.getcwd()
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    try:
        os.chdir(repo)
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, env, clear=True))
            stack.enter_context(mock.patch.object(sys, "stdin", io.StringIO(json.dumps({"cwd": "sub"}))))
            stack.enter_context(mock.patch.object(cc10x_hooklib, "_input_cwd", None))
            cc10x_hooklib.load_input()
            assert Path(cc10x_hooklib._input_cwd).is_absolute()
            assert cc10x_hooklib.state_root() == Path(os.getcwd()) / ".cc10x"
    finally:
        os.chdir(previous)


def _stamped(event: str, ts: str, **extra) -> dict:
    return {"event": event, "ts": ts, **extra}


def test_the_last_signal_in_time_decides_whether_a_workflow_is_finished(tmp_path):
    t1, t2, t3 = (
        "2026-01-01T00:00:01+00:00",
        "2026-01-01T00:00:02+00:00",
        "2026-01-01T00:00:03+00:00",
    )
    older = write_artifact(tmp_path, "wf-aaa")
    set_age(older, 300)
    resumed = write_artifact(
        tmp_path,
        "wf-bbb",
        status_history=[_stamped("memory_finalized", t1), _stamped("resumed", t3)],
    )
    append_events(tmp_path, "wf-bbb", _stamped("memory_finalized", t2, agent="router"))
    set_age(resumed, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-bbb"

    done = write_artifact(
        tmp_path,
        "wf-ccc",
        status_history=[_stamped("started", t1), _stamped("memory_finalized", t3)],
    )
    append_events(tmp_path, "wf-ccc", _stamped("phase_started", t2, agent="router"))
    set_age(done, 5)
    assert sessionstart_wf(tmp_path, None) == "wf-bbb"


# --- P5 remediation 2, group C: visibility and test gaps ----------------------


def _run_write_guard(project: Path, env: dict) -> subprocess.CompletedProcess:
    return run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(project / "a.txt")}},
        project,
        extra_env=env,
    )


def test_invalid_hook_mode_is_logged_once_across_processes_until_the_file_changes(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    data = tmp_path / "plugin-data"
    data.mkdir()
    override = data / "hook-mode.json"
    override.write_text('{"artifactIntegrity": "Audit"}')
    env = {"CLAUDE_PLUGIN_DATA": str(data)}
    for _ in range(10):
        assert _run_write_guard(tmp_path, env).returncode == 0
    assert len(invalid_mode_events(tmp_path)) == 1
    override.write_text('{"artifactIntegrity": "nope"}')
    for _ in range(3):
        assert _run_write_guard(tmp_path, env).returncode == 0
    assert len(invalid_mode_events(tmp_path)) == 2


def test_invalid_hook_mode_logging_survives_an_unwritable_marker_location(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    (tmp_path / ".cc10x" / "state").write_text("a file where the marker dir would go")
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "hook-mode.json").write_text('{"artifactIntegrity": "Audit"}')
    env = {"CLAUDE_PLUGIN_DATA": str(data)}
    for _ in range(2):
        r = _run_write_guard(tmp_path, env)
        assert r.returncode == 0 and "Traceback" not in r.stderr, r.stderr[-300:]
    assert len(invalid_mode_events(tmp_path)) == 2


def _hook_mode_markers(project: Path) -> list[Path]:
    state = project / ".cc10x" / "state"
    return sorted(state.glob("hook-mode-reported-*")) if state.is_dir() else []


def test_a_normal_setup_writes_no_invalid_hook_mode_event_or_marker(tmp_path):
    valid = tmp_path / "valid-data"
    valid.mkdir()
    (valid / "hook-mode.json").write_text('{"artifactIntegrity": "audit"}')
    empty = tmp_path / "empty-data"
    empty.mkdir()
    setups = {
        "unset": {},
        "nonexistent": {"CLAUDE_PLUGIN_DATA": str(tmp_path / "no-such-dir")},
        "empty": {"CLAUDE_PLUGIN_DATA": str(empty)},
        "valid": {"CLAUDE_PLUGIN_DATA": str(valid)},
    }
    for name, env in setups.items():
        project = tmp_path / f"proj-{name}"
        (project / ".cc10x").mkdir(parents=True)
        for _ in range(10):
            assert _run_write_guard(project, env).returncode == 0
        assert invalid_mode_events(project) == [], name
        assert _hook_mode_markers(project) == [], name


def test_a_corrupt_override_leaves_one_marker_across_repeated_runs(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "hook-mode.json").write_text("{not json")
    for _ in range(10):
        assert _run_write_guard(tmp_path, {"CLAUDE_PLUGIN_DATA": str(data)}).returncode == 0
    assert len(invalid_mode_events(tmp_path)) == 1
    assert len(_hook_mode_markers(tmp_path)) == 1


def test_a_new_hook_mode_marker_prunes_markers_older_than_a_day(tmp_path):
    state = tmp_path / ".cc10x" / "state"
    state.mkdir(parents=True)
    old = time.time() - 2 * 86400
    stale = [state / f"hook-mode-reported-{i:016x}" for i in range(3)]
    for marker in stale:
        marker.touch()
        os.utime(marker, (old, old))
    fresh = state / "hook-mode-reported-ffffffffffffffff"
    fresh.touch()
    unrelated = state / "other-state-file"
    unrelated.touch()
    os.utime(unrelated, (old, old))
    data = tmp_path / "plugin-data"
    data.mkdir()
    (data / "hook-mode.json").write_text("{not json")
    assert _run_write_guard(tmp_path, {"CLAUDE_PLUGIN_DATA": str(data)}).returncode == 0
    assert [m for m in stale if m.exists()] == []
    assert fresh.exists() and unrelated.exists()
    assert len(_hook_mode_markers(tmp_path)) == 2


def test_in_process_hooklib_tests_do_not_write_into_a_checkout_state_dir(tmp_path):
    sandbox = tmp_path / "checkout"
    (sandbox / ".git").mkdir(parents=True)
    (sandbox / ".cc10x").mkdir()
    code = (
        "import importlib.util, inspect, pathlib, sys, tempfile\n"
        "spec = importlib.util.spec_from_file_location('guards_under_test', sys.argv[1])\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "for name, fn in sorted(vars(mod).items()):\n"
        "    if not name.startswith('test_') or not callable(fn):\n"
        "        continue\n"
        "    if 'load_hooklib()' not in inspect.getsource(fn) or name == sys.argv[2]:\n"
        "        continue\n"
        "    with tempfile.TemporaryDirectory() as d:\n"
        "        try:\n"
        "            fn(pathlib.Path(d).resolve())\n"
        "        except Exception:\n"
        "            pass\n"
    )
    subprocess.run(
        [sys.executable, "-c", code, str(Path(__file__).resolve()), "test_in_process_hooklib_tests_do_not_write_into_a_checkout_state_dir"],
        env={"PATH": "/usr/bin:/bin"},
        cwd=sandbox,
        capture_output=True,
        text=True,
        timeout=120,
    )
    leaked = [p.name for p in (sandbox / ".cc10x").rglob("*") if p.is_file()]
    assert leaked == []


def test_an_unsafe_workflow_id_in_an_artifact_is_logged_when_its_event_is_dropped(tmp_path):
    path = write_artifact(tmp_path, "wf-aaa", workflow_uuid="../../escape", workflow_id="../../escape")
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode == 0, r.stderr
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "workflow_id_unsafe"]
    assert len(events) == 1
    assert events[0]["source"] == "posttool_artifact_mutated"
    assert not (tmp_path / "escape.events.jsonl").exists()


def test_a_failed_artifact_mutated_append_is_logged(tmp_path):
    path = write_artifact(tmp_path, "wf-aaa")
    log = path.with_name("wf-aaa.events.jsonl")
    log.unlink()
    log.mkdir()
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode == 0, r.stderr
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "workflow_event_append_failed"]
    assert len(events) == 1 and events[0]["wf"] == "wf-aaa"


def test_a_memory_finalize_cursor_that_is_still_in_progress_is_live(tmp_path):
    write_artifact(
        tmp_path,
        "wf-aaa",
        phase_cursor="memory-finalize",
        phase_status={"memory-finalize": "in_progress"},
        status_history=[{"event": "started"}],
    )
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"
    write_artifact(
        tmp_path,
        "wf-bbb",
        phase_cursor="memory-finalize",
        phase_status={"memory-finalize": "completed"},
        status_history=[{"event": "started"}],
    )
    newer = tmp_path / ".cc10x" / "workflows" / "wf-bbb.json"
    set_age(newer, 1)
    set_age(tmp_path / ".cc10x" / "workflows" / "wf-aaa.json", 100)
    assert sessionstart_wf(tmp_path, None) == "wf-aaa"


def registered_hook_commands() -> list[list[str]]:
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text())["hooks"]
    commands = [
        hook["command"]
        for groups in hooks.values()
        for group in groups
        for hook in group["hooks"]
    ]
    argvs = []
    for command in commands:
        words = shlex.split(command.replace("${CLAUDE_PLUGIN_ROOT}", str(PLUGIN_ROOT)))
        if words[0] == "python3":
            words[0] = sys.executable
        argvs.append(words)
    return argvs


def test_every_registered_hook_survives_valid_non_object_json_on_stdin(tmp_path):
    argvs = registered_hook_commands()
    assert len(argvs) == 9
    env = {
        "CLAUDE_PROJECT_DIR": str(tmp_path),
        "CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT),
        "PATH": "/usr/bin:/bin",
    }
    bad = []
    for argv in argvs:
        for body in ("[]", "null", "5", '"s"', "true"):
            r = subprocess.run(
                argv, input=body, capture_output=True, text=True, env=env,
                cwd=tmp_path, timeout=30,
            )
            if r.returncode not in (0, 2) or "Traceback" in r.stderr:
                label = " ".join([Path(argv[1]).name, *argv[2:]])
                bad.append(f"{label} {body}: exit {r.returncode}")
    assert not bad, bad


def hooklib_functions_called(script: str) -> set[str]:
    import ast

    tree = ast.parse((SCRIPTS_DIR / script).read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "cc10x_hooklib"
        for alias in node.names
    }
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    return imported & called


def test_hook_scripts_split_between_newest_artifact_and_live_artifact_selection(tmp_path):
    # The policy reference names which hooks take the newest artifact (finished
    # or not) and which skip finished ones; this pins the code side so the two
    # cannot drift apart again.
    newest = {"latest_workflow_payload", "read_latest_workflow_state", "latest_workflow_file"}
    live = {"read_live_workflow_state"}
    by_script = {
        "cc10x_posttooluse_artifact_guard.py": newest,
        "cc10x_event_logger.py": newest,
        "cc10x_sessionstart_context.py": live,
        "cc10x_state_persist.py": live,
    }
    for script, family in by_script.items():
        called = hooklib_functions_called(script)
        assert called & family, (script, called)
        assert not called & ((newest | live) - family), (script, called)


def main() -> int:
    """Dependency-free runner (repo convention: tests run on bare python3).

    Each test_* function receives a fresh temp dir, matching pytest's
    tmp_path fixture — the suite also runs unchanged under pytest.
    """
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    failures = 0
    for name, fn in tests:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                # Resolve: macOS tempdirs are symlinked (/var -> /private/var),
                # and pytest's tmp_path is resolved too.
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
