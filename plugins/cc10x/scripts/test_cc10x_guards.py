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
import re
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


# --- cc10x_git_guard.py ------------------------------------------------------


def test_git_guard_allows_safe_command(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git status"}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_git_guard_denies_push_without_token(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git push origin main"}},
        tmp_path,
    )
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "git push" in out["hookSpecificOutput"]["permissionDecisionReason"]


def test_git_guard_fresh_token_allows_push_once(tmp_path):
    state = tmp_path / ".cc10x" / "state"
    state.mkdir(parents=True)
    token = state / "git-approval.json"
    token.write_text(
        json.dumps(
            {
                "wf": "wf-test",
                "operations": ["push"],
                "expires_at": "2099-01-01T00:00:00+00:00",
            }
        )
    )
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git push origin main"}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""  # allowed, no deny envelope
    assert not token.exists()  # single-use: consumed

    # Second push without a token is denied again.
    r2 = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git push origin main"}},
        tmp_path,
    )
    out = json.loads(r2.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_force_push_blocked_even_with_token(tmp_path):
    state = tmp_path / ".cc10x" / "state"
    state.mkdir(parents=True)
    (state / "git-approval.json").write_text(
        json.dumps(
            {
                "wf": "wf-test",
                "operations": ["push"],
                "expires_at": "2099-01-01T00:00:00+00:00",
            }
        )
    )
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git push --force origin main"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_denies_reset_hard_with_no_token_path(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git reset --hard HEAD~1"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "no approval-token path" in out["hookSpecificOutput"]["permissionDecisionReason"]


# --- cc10x_pretooluse_guard.py ----------------------------------------------


def test_pretooluse_guard_ignores_ordinary_write(tmp_path):
    r = run_guard(
        "cc10x_pretooluse_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "src" / "a.py")}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    assert hook_log_lines(tmp_path) == []


def test_pretooluse_guard_audits_memory_write_in_shipped_mode(tmp_path):
    # Shipped config: memoryWrites=audit — the write is logged, never denied.
    target = tmp_path / ".cc10x" / "activeContext.md"
    r = run_guard(
        "cc10x_pretooluse_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(target)}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "pretool_guard" and e["decision"] == "audit" for e in events
    )


def test_pretooluse_guard_denies_memory_write_in_block_mode(tmp_path):
    root = mode_root(tmp_path, {"memoryWrites": "block"})
    target = tmp_path / ".cc10x" / "activeContext.md"
    r = run_guard(
        "cc10x_pretooluse_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(target)}},
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


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


# --- cc10x_task_completed_guard.py ------------------------------------------


CC10X_METADATA = (
    "wf:wf-test\nkind:agent\norigin:router\nphase:build-implement\n"
    "plan:N/A\nscope:N/A\nreason:test\n"
)


def test_task_guard_ignores_non_cc10x_tasks(tmp_path):
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {"task_subject": "Ordinary task", "task_description": "no metadata"},
        tmp_path,
    )
    assert r.returncode == 0
    assert hook_log_lines(tmp_path) == []


def test_task_guard_accepts_complete_metadata(tmp_path):
    write_artifact(tmp_path)
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t1",
        },
        tmp_path,
    )
    assert r.returncode == 0


def test_task_guard_audits_missing_metadata_in_shipped_mode(tmp_path):
    # Shipped config: taskMetadata=audit — missing lines log, never block.
    # A CC10X task implies the router already created the state dir.
    (tmp_path / ".cc10x").mkdir()
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {"task_subject": "CC10X planner: plan it", "task_description": "wf:wf-1"},
        tmp_path,
    )
    assert r.returncode == 0
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "task_completed_guard" and e["decision"] == "audit"
        for e in events
    )


def test_task_guard_blocks_missing_metadata_in_block_mode(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {"task_subject": "CC10X planner: plan it", "task_description": "wf:wf-1"},
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2
    assert "missing metadata" in r.stderr


def test_task_guard_circuit_breaker_warns_past_limit_in_shipped_mode(tmp_path):
    write_artifact(
        tmp_path,
        remediation_history=[{"cycle": i} for i in range(4)],
    )
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: remediation fix",
            "task_description": CC10X_METADATA.replace("kind:agent", "kind:remfix"),
            "task_id": "t2",
        },
        tmp_path,
    )
    # Shipped audit mode: a log event, not exit-0 stderr (the model never sees
    # it, per the hooks reference); does not block.
    assert r.returncode == 0
    assert r.stderr == ""
    assert any(
        e["event"] == "task_completed_circuit_breaker_exceeded"
        and e["decision"] == "audit"
        for e in hook_log_lines(tmp_path)
    )


def test_task_guard_circuit_breaker_blocks_in_block_mode(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    write_artifact(
        tmp_path,
        remediation_history=[{"cycle": i} for i in range(4)],
    )
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: remediation fix",
            "task_description": CC10X_METADATA.replace("kind:agent", "kind:remfix"),
            "task_id": "t2",
        },
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2
    assert "circuit breaker" in r.stderr


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


def test_pretooluse_guard_blocks_memory_write_through_symlinked_project(tmp_path):
    # Path-resolution bypass: the guard resolves the written path but built the
    # protected set from the unresolved project dir. A symlinked project dir
    # (macOS /var -> /private/var, or any alias) silently skipped protection.
    real = tmp_path / "real-project"
    real.mkdir()
    link = tmp_path / "alias"
    link.symlink_to(real)
    root = mode_root(tmp_path, {"memoryWrites": "block"})
    target = real / ".cc10x" / "activeContext.md"  # resolved form of the write
    r = run_guard(
        "cc10x_pretooluse_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(target)}},
        link,  # CLAUDE_PROJECT_DIR is the unresolved alias
        plugin_root=root,
    )
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


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


def test_task_guard_circuit_breaker_surfaces_missing_history(tmp_path):
    # The breaker counts remediation_history; when the router never wrote it
    # (the exact failure the backstop exists to catch) the guard silently
    # passed. It must at least emit an audit event.
    write_artifact(tmp_path, remediation_history=None)
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: remediation fix",
            "task_description": CC10X_METADATA.replace("kind:agent", "kind:remfix"),
            "task_id": "t3",
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "task_completed_circuit_breaker_missing_history"
        for e in events
    )


def test_git_guard_denies_push_with_directory_flag(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git -C /some/dir push origin main"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_denies_checkout_dot_in_compound_command(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git checkout . && ls"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_denies_restore_dot_on_any_line(tmp_path):
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "echo start\ngit restore .\necho done"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_denies_discard_with_trailing_comment(tmp_path):
    # End-anchored discard patterns were defeated by a trailing comment.
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git restore . # tidy up"}},
        tmp_path,
    )
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_guards_do_not_litter_foreign_repos(tmp_path):
    # Guards ran state_root()/workflows_dir() with mkdir on every event,
    # creating .cc10x/ in every repo the user touched — CC10x or not.
    run_guard(
        "cc10x_pretooluse_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "a.py")}},
        tmp_path,
    )
    run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "a.py")}},
        tmp_path,
    )
    run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git status"}},
        tmp_path,
    )
    assert not (tmp_path / ".cc10x").exists()


def test_task_guard_metadata_keys_must_anchor_line_starts(tmp_path):
    # Substring matching accepted prose that merely mentioned 'plan:' etc.
    # anywhere in the description; the seven keys must be real metadata lines.
    prose = (
        "This wf:embedded task is kind: of important; its origin:story "
        "explains the phase:moon plan:B scope:wide reason:because."
    )
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {"task_subject": "CC10X planner: plan it", "task_description": prose},
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2
    assert "missing metadata" in r.stderr


def test_task_guard_ignores_the_undocumented_task_created_at(tmp_path):
    # TaskCompleted carries no creation timestamp (hooks reference), so the
    # freshness check is the 300s wall-clock window alone: a payload-supplied
    # task_created_at, however late, cannot make a fresh artifact stale.
    write_artifact(tmp_path)
    created = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(time.time() + 600))
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t4",
            "task_created_at": created,
            "task": {"created_at": created},
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    assert not [
        e
        for e in hook_log_lines(tmp_path)
        if e["event"] == "task_completed_stale_artifact"
    ]


# --- P2.T4 characterization tests (pin CURRENT behavior; P5 updates them) ----
#
# These lock what the hooks do today so the P5 hook cleanup changes behavior
# deliberately. Where a test pins something P5 plans to change, the comment
# says which task.


MEMORY_TASK_SUBJECT = "CC10X Memory Update: persist phase 1"
MEMORY_TASK_DESCRIPTION = (
    "ROUTER ONLY: execute inline.\n"
    + CC10X_METADATA.replace("kind:agent", "kind:memory")
)


def memory_task_payload(**overrides) -> dict:
    payload = {
        "task_subject": MEMORY_TASK_SUBJECT,
        "task_description": MEMORY_TASK_DESCRIPTION,
        "task_id": "m1",
    }
    payload.update(overrides)
    return payload


def finalize_event_log(project_dir: Path, wf: str = "wf-test") -> None:
    log = project_dir / ".cc10x" / "workflows" / f"{wf}.events.jsonl"
    log.write_text(json.dumps({"wf": wf, "event": "memory_finalized"}) + "\n")


def memory_guard_reasons(project_dir: Path) -> list[str]:
    events = [
        e
        for e in hook_log_lines(project_dir)
        if e["event"] == "task_completed_memory_finalize_guard"
    ]
    assert len(events) == 1, events
    return events[0]["reason"].split(",")


def test_task_guard_memory_task_without_finalized_event_audits_in_shipped_mode(tmp_path):
    write_artifact(tmp_path)
    r = run_guard("cc10x_task_completed_guard.py", memory_task_payload(), tmp_path)
    assert r.returncode == 0  # shipped taskMetadata=audit: logged, not blocked
    assert memory_guard_reasons(tmp_path) == ["missing-memory-finalized-event"]
    event = hook_log_lines(tmp_path)[0]
    assert event["decision"] == "audit"
    assert event["wf"] == "wf-test"


def test_task_guard_memory_task_without_finalized_event_blocks_in_block_mode(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    write_artifact(tmp_path)
    r = run_guard(
        "cc10x_task_completed_guard.py",
        memory_task_payload(),
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2
    assert "memory-task completion blocked" in r.stderr
    assert "missing-memory-finalized-event" in r.stderr
    assert hook_log_lines(tmp_path)[0]["decision"] == "block"


def test_task_guard_memory_task_with_finalized_event_passes_silently(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    write_artifact(tmp_path)
    finalize_event_log(tmp_path)
    r = run_guard(
        "cc10x_task_completed_guard.py",
        memory_task_payload(),
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    assert hook_log_lines(tmp_path) == []


def test_task_guard_memory_event_is_a_substring_match_on_the_log(tmp_path):
    # UNOWNED defect: no P5 task changes the raw-text needle (hooklib workflow event check);
    # recorded as deferred, so fixing it means updating this test deliberately.
    # Current behavior: the needle is searched as raw text anywhere in the
    # event log, so any line mentioning the string satisfies the guard.
    write_artifact(tmp_path)
    log = tmp_path / ".cc10x" / "workflows" / "wf-test.events.jsonl"
    log.write_text('{"event": "note", "reason": "not yet memory_finalized"}\n')
    r = run_guard("cc10x_task_completed_guard.py", memory_task_payload(), tmp_path)
    assert r.returncode == 0
    assert hook_log_lines(tmp_path) == []


def test_task_guard_memory_task_reports_every_ownership_reason(tmp_path):
    # No artifact on disk, wrong origin, no marker, subject not router-owned.
    (tmp_path / ".cc10x").mkdir()
    description = CC10X_METADATA.replace("kind:agent", "kind:memory").replace(
        "origin:router", "origin:agent"
    )
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X Memory: persist",
            "task_description": description,
            "task_id": "m2",
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert memory_guard_reasons(tmp_path) == [
        "memory-task-origin-not-router",
        "memory-task-missing-router-only-marker",
        "memory-task-subject-not-router-owned",
        "missing-workflow-artifact",
        "missing-memory-finalized-event",
    ]


def test_task_guard_memory_task_flags_artifact_workflow_mismatch(tmp_path):
    path = write_artifact(tmp_path)
    data = json.loads(path.read_text())
    data["workflow_uuid"] = "wf-other"
    path.write_text(json.dumps(data))
    finalize_event_log(tmp_path)
    r = run_guard("cc10x_task_completed_guard.py", memory_task_payload(), tmp_path)
    assert r.returncode == 0
    assert memory_guard_reasons(tmp_path) == ["workflow-artifact-mismatch"]


def test_task_guard_memory_task_flags_unparseable_artifact(tmp_path):
    path = write_artifact(tmp_path)
    path.write_text("{not json")
    finalize_event_log(tmp_path)
    r = run_guard("cc10x_task_completed_guard.py", memory_task_payload(), tmp_path)
    assert r.returncode == 0
    assert memory_guard_reasons(tmp_path) == ["artifact-json:JSONDecodeError"]


def test_task_guard_validator_only_applies_to_kind_memory(tmp_path):
    # A non-memory task with no finalized event is not a memory violation.
    write_artifact(tmp_path)
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t5",
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert not any(
        e["event"] == "task_completed_memory_finalize_guard"
        for e in hook_log_lines(tmp_path)
    )


def test_task_guard_stale_artifact_is_audit_only_even_in_block_mode(tmp_path):
    # P5.T2: the exit-0 warning is a log event only (the model never sees
    # exit-0 stderr), and the undocumented task_created_at is not read.
    import os

    root = mode_root(tmp_path, {"taskMetadata": "block"})
    path = write_artifact(tmp_path)
    old = time.time() - 600
    os.utime(path, (old, old))
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t6",
        },
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "task_completed_stale_artifact" and e["decision"] == "audit"
        for e in events
    )


def test_task_guard_stale_artifact_uses_the_300s_window(tmp_path):
    # P5.T2: log event, no exit-0 stderr.
    import os

    path = write_artifact(tmp_path)
    old = time.time() - 600
    os.utime(path, (old, old))
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t7",
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    assert any(
        e["event"] == "task_completed_stale_artifact"
        for e in hook_log_lines(tmp_path)
    )


def test_task_guard_circuit_breaker_allows_exactly_the_limit(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    write_artifact(tmp_path, remediation_history=[{"cycle": i} for i in range(3)])
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: remediation fix",
            "task_description": CC10X_METADATA.replace("kind:agent", "kind:remfix"),
            "task_id": "t8",
        },
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 0
    assert "circuit breaker" not in r.stderr


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
    root = mode_root(tmp_path, {"memoryWrites": "block"})
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_posttool(tmp_path, bad, plugin_root=root)
    assert r.returncode == 2
    assert hook_log_lines(tmp_path)[0]["decision"] == "block"


def write_git_token(project_dir: Path, operations, expires_at: str | None) -> Path:
    state = project_dir / ".cc10x" / "state"
    state.mkdir(parents=True, exist_ok=True)
    token = state / "git-approval.json"
    body: dict[str, object] = {"wf": "wf-test", "operations": operations}
    if expires_at is not None:
        body["expires_at"] = expires_at
    token.write_text(json.dumps(body))
    return token


def run_branch_delete(project_dir: Path) -> subprocess.CompletedProcess:
    return run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git branch -D feature/old"}},
        project_dir,
    )


def assert_denied(r: subprocess.CompletedProcess) -> None:
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "git branch -D" in out["hookSpecificOutput"]["permissionDecisionReason"]


def test_git_guard_branch_delete_denied_without_token(tmp_path):
    r = run_branch_delete(tmp_path)
    assert_denied(r)
    assert "approval token" in json.loads(r.stdout)["hookSpecificOutput"][
        "permissionDecisionReason"
    ]


def test_git_guard_branch_delete_fresh_token_allows_once_and_logs(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    token = write_git_token(tmp_path, ["branch-delete"], "2099-01-01T00:00:00+00:00")
    r = run_branch_delete(tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    assert not token.exists()  # single-use
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "git_guard_token_consumed"
        and e["decision"] == "allow"
        and e["wf"] == "wf-test"
        and "branch-delete" in e["reason"]
        for e in events
    )
    assert_denied(run_branch_delete(tmp_path))  # consumed: second use denied


def test_git_guard_branch_delete_expired_token_denied_and_consumed(tmp_path):
    token = write_git_token(tmp_path, ["branch-delete"], "2000-01-01T00:00:00+00:00")
    assert_denied(run_branch_delete(tmp_path))
    assert not token.exists()


def test_git_guard_branch_delete_wrong_operation_token_denied_and_consumed(tmp_path):
    token = write_git_token(tmp_path, ["push"], "2099-01-01T00:00:00+00:00")
    assert_denied(run_branch_delete(tmp_path))
    assert not token.exists()  # a mismatched token must not linger


def test_git_guard_token_listing_both_operations_allows_branch_delete(tmp_path):
    write_git_token(
        tmp_path, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00"
    )
    r = run_branch_delete(tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_git_guard_branch_delete_token_older_than_backstop_is_stale(tmp_path):
    import os
    import time

    token = write_git_token(tmp_path, ["branch-delete"], "2099-01-01T00:00:00+00:00")
    old = time.time() - 3600  # MAX_TOKEN_AGE_SECONDS is 600
    os.utime(token, (old, old))
    assert_denied(run_branch_delete(tmp_path))
    assert not token.exists()


def test_git_guard_branch_delete_token_without_expiry_is_never_fresh(tmp_path):
    token = write_git_token(tmp_path, ["branch-delete"], None)
    assert_denied(run_branch_delete(tmp_path))
    assert not token.exists()


def test_git_guard_branch_delete_corrupt_token_denied_and_removed(tmp_path):
    state = tmp_path / ".cc10x" / "state"
    state.mkdir(parents=True)
    token = state / "git-approval.json"
    token.write_text("{not json")
    assert_denied(run_branch_delete(tmp_path))
    assert not token.exists()


def test_git_guard_lowercase_branch_delete_is_not_blocked(tmp_path):
    # Safe delete (-d) refuses unmerged branches; only -D is guarded.
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git branch -d feature/merged"}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_git_guard_long_form_force_delete_is_denied_like_short_form(tmp_path):
    # The pre-P5.T4 pattern only matched the short `-D`; the classifier closes
    # the gap and keeps the same approval-token operation (branch-delete).
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git branch --delete --force feature/old"}},
        tmp_path,
    )
    assert_denied(r)


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


def _qa_plan_phase_mkdir_denied(tmp_path: Path, command: str) -> bool:
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "wf-qa.json").write_text(
        json.dumps(
            {
                "workflow_uuid": "wf-qa",
                "workflow_id": "wf-qa",
                "workflow_type": "QA",
                "phase_cursor": "qa-plan",
                "qa": {"isolation": {"plan_phase_readonly": True}},
                "status_history": [{"event": "started", "phase": "qa-plan"}],
            }
        )
    )
    result = run_guard("cc10x_qa_isolation_guard.py", {"tool_name": "Bash", "tool_input": {"command": command}}, tmp_path)
    assert result.returncode == 0, result.stderr
    return '"permissionDecision": "deny"' in result.stdout


def test_qa_isolation_guard_allows_the_trailing_slash_mkdir_agent_common_prescribes(tmp_path):
    assert not _qa_plan_phase_mkdir_denied(tmp_path, "mkdir -p .cc10x/")


def test_qa_isolation_guard_denies_the_bare_mkdir_so_agent_common_must_not_prescribe_it(tmp_path):
    assert _qa_plan_phase_mkdir_denied(tmp_path, "mkdir -p .cc10x")


def test_qa_isolation_guard_allows_the_router_skeleton_copy_form(tmp_path):
    command = 'mkdir -p .cc10x/workflows && cp "/p/skills/cc10x-router/references/workflow-artifact.skeleton.json" .cc10x/workflows/wf-x.json'
    assert not _qa_plan_phase_mkdir_denied(tmp_path, command)


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
        ("cc10x_git_guard.py", {"tool_input": {"command": "git status"}}, []),
        (
            "cc10x_posttooluse_artifact_guard.py",
            {"tool_name": "Write", "tool_input": {"file_path": "a.txt"}},
            [],
        ),
        (
            "cc10x_pretooluse_guard.py",
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


def test_posttool_artifact_guard_matcher_covers_bash(tmp_path):
    assert "Bash" in hooks_json_matcher(
        "PostToolUse", "cc10x_posttooluse_artifact_guard.py"
    ).split("|")


def test_qa_isolation_matcher_lists_only_documented_tools(tmp_path):
    matcher = hooks_json_matcher("PreToolUse", "cc10x_qa_isolation_guard.py")
    assert "NotebookRead" not in matcher.split("|")  # not in the tools reference


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


def test_task_guard_block_mode_circuit_breaker_keeps_its_exit_2_message(tmp_path):
    root = mode_root(tmp_path, {"taskMetadata": "block"})
    write_artifact(tmp_path, remediation_history=[{"cycle": i} for i in range(4)])
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: remediation fix",
            "task_description": CC10X_METADATA.replace("kind:agent", "kind:remfix"),
            "task_id": "t9",
        },
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 2  # exit 2 stderr IS delivered to the model
    assert "circuit breaker" in r.stderr


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


DEFAULT_MODES = {
    "artifactIntegrity": "block",
    "memoryWrites": "audit",
    "taskMetadata": "audit",
    "gitGuard": "block",
}


def test_load_mode_missing_shipped_file_returns_all_defaults(tmp_path):
    modes, events = resolved_mode(tmp_path, None)
    assert modes == DEFAULT_MODES
    assert events == []


def test_load_mode_corrupt_json_falls_back_and_records_an_event(tmp_path):
    modes, events = resolved_mode(tmp_path, "{not json")
    assert modes == DEFAULT_MODES
    assert len(events) == 1 and events[0]["source"] == "shipped"


def test_load_mode_unknown_value_falls_back_for_that_key_only(tmp_path):
    modes, events = resolved_mode(
        tmp_path, {"artifactIntegrity": "warn", "memoryWrites": "block", "taskMetadata": 1}
    )
    assert modes == {
        "artifactIntegrity": "block",
        "memoryWrites": "block",
        "taskMetadata": "audit",
        "gitGuard": "block",
    }
    assert sorted(e["key"] for e in events) == ["artifactIntegrity", "taskMetadata"]


def test_load_mode_partial_file_keeps_defaults_for_missing_keys(tmp_path):
    modes, events = resolved_mode(tmp_path, {"taskMetadata": "block"})
    assert modes == {
        "artifactIntegrity": "block",
        "memoryWrites": "audit",
        "taskMetadata": "block",
        "gitGuard": "block",
    }
    assert events == []


def test_load_mode_user_override_wins_over_the_shipped_file(tmp_path):
    modes, events = resolved_mode(
        tmp_path,
        {"artifactIntegrity": "block", "memoryWrites": "block"},
        override={"artifactIntegrity": "audit", "taskMetadata": "block", "extra": "block"},
    )
    assert modes == {
        "artifactIntegrity": "audit",
        "memoryWrites": "block",
        "taskMetadata": "block",
        "gitGuard": "block",
    }
    assert events == []


def test_load_mode_invalid_override_value_falls_back_to_the_shipped_value(tmp_path):
    modes, events = resolved_mode(
        tmp_path, {"memoryWrites": "block"}, override={"memoryWrites": "banana"}
    )
    assert modes["memoryWrites"] == "block"
    assert [e["source"] for e in events] == ["override"]
    modes, events = resolved_mode(
        tmp_path / "corrupt", {"memoryWrites": "block"}, override="{oops"
    )
    assert modes["memoryWrites"] == "block"
    assert [e["source"] for e in events] == ["override"]


def test_git_guard_mode_accepts_ask_and_rejects_audit(tmp_path):
    modes, events = resolved_mode(tmp_path / "ask", None, override={"gitGuard": "ask"})
    assert modes["gitGuard"] == "ask"
    assert events == []
    # One directory per value: resolved_mode returns every event in its log.
    for i, v in enumerate(["audit", "Ask", 1, None]):
        modes, events = resolved_mode(tmp_path / f"v{i}", None, override={"gitGuard": v})
        assert modes["gitGuard"] == "block", v
        assert [(e["key"], e["source"]) for e in events] == [("gitGuard", "override")], v


def test_ask_is_invalid_on_the_block_audit_keys(tmp_path):
    modes, events = resolved_mode(
        tmp_path,
        None,
        override={"artifactIntegrity": "ask", "memoryWrites": "ask", "taskMetadata": "ask"},
    )
    assert modes == DEFAULT_MODES
    assert sorted(e["key"] for e in events) == ["artifactIntegrity", "memoryWrites", "taskMetadata"]


def test_hook_mode_values_cover_every_key_and_admit_each_default(tmp_path):
    hooklib = load_hooklib()
    assert set(hooklib.HOOK_MODE_VALUES) == set(hooklib.HOOK_MODE_DEFAULTS)
    for key, default in hooklib.HOOK_MODE_DEFAULTS.items():
        assert default in hooklib.HOOK_MODE_VALUES[key], key
    assert hooklib.HOOK_MODE_VALUES["gitGuard"] == ("block", "ask")
    for key in ("artifactIntegrity", "memoryWrites", "taskMetadata"):
        assert hooklib.HOOK_MODE_VALUES[key] == ("block", "audit"), key


def test_load_mode_data_dir_absent_or_empty_is_not_an_error(tmp_path):
    modes, events = resolved_mode(tmp_path, {"taskMetadata": "block"}, data_dir=False)
    assert modes["taskMetadata"] == "block" and events == []
    root = tmp_path / "plugin-root"
    with env_patch(
        CLAUDE_PLUGIN_ROOT=str(root),
        CLAUDE_PLUGIN_DATA=str(tmp_path / "does-not-exist"),
        CLAUDE_PROJECT_DIR=str(tmp_path / "proj"),
    ):
        again = load_hooklib().load_mode()
    assert again["taskMetadata"] == "block"
    assert not (tmp_path / "does-not-exist").exists()


def test_load_mode_never_raises_and_always_returns_all_four_keys(tmp_path):
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


def qa_workflow(project: Path, wf: str, age: float, **overrides) -> Path:
    secret = project / "secret" / "answer.md"
    fields = {
        "workflow_type": "QA",
        "phase_cursor": "qa-plan",
        "qa": {"isolation": {"denied_reads": [str(secret)], "plan_phase_readonly": True}},
    }
    fields.update(overrides)
    path = write_artifact(project, wf, **fields)
    set_age(path, age)
    return path


def qa_guard_decisions(project: Path) -> dict[str, str]:
    probes = {
        "write": {"tool_name": "Write", "tool_input": {"file_path": str(project / "src" / "app.py")}},
        "bash": {"tool_name": "Bash", "tool_input": {"command": "mkdir build"}},
        "read": {"tool_name": "Read", "tool_input": {"file_path": str(project / "secret" / "answer.md")}},
    }
    out = {}
    for name, payload in probes.items():
        r = run_guard("cc10x_qa_isolation_guard.py", payload, project)
        assert r.returncode == 0, r.stderr
        out[name] = "deny" if '"permissionDecision": "deny"' in r.stdout else "allow"
    return out


def test_qa_guard_stays_off_when_a_newer_build_finished_after_an_abandoned_qa(tmp_path):
    qa_workflow(tmp_path, "wf-a1", 3000)
    newer = write_artifact(
        tmp_path, "wf-b2", status_history=[{"event": "started"}, {"event": "memory_finalized"}]
    )
    set_age(newer, 10)
    assert qa_guard_decisions(tmp_path) == {"write": "allow", "bash": "allow", "read": "allow"}


def test_qa_guard_stays_off_for_a_newer_build_finished_by_cursor_alone(tmp_path):
    qa_workflow(tmp_path, "wf-a1", 3000)
    newer = write_artifact(tmp_path, "wf-b2", phase_cursor="memory-finalize")
    set_age(newer, 10)
    assert qa_guard_decisions(tmp_path) == {"write": "allow", "bash": "allow", "read": "allow"}


def test_qa_guard_stays_off_for_a_newest_qa_whose_cursor_is_the_only_finish_signal(tmp_path):
    qa_workflow(tmp_path, "wf-a1", 10, phase_cursor="memory-finalize")
    assert qa_guard_decisions(tmp_path) == {"write": "allow", "bash": "allow", "read": "allow"}


def test_qa_guard_engages_for_the_newest_live_qa_workflow(tmp_path):
    older = write_artifact(tmp_path, "wf-b2", status_history=[{"event": "memory_finalized"}])
    set_age(older, 3000)
    qa_workflow(tmp_path, "wf-a1", 10)
    assert qa_guard_decisions(tmp_path) == {"write": "deny", "bash": "deny", "read": "deny"}


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
        (
            "cc10x_qa_isolation_guard.py",
            {"tool_name": "Write", "tool_input": {"file_path": "a.txt"}},
            [],
        ),
        (
            "cc10x_pretooluse_guard.py",
            {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / ".cc10x" / "patterns.md")}},
            [],
        ),
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


def test_qa_guard_survives_a_non_string_workflow_type(tmp_path):
    for value in (["QA"], 5, {"a": 1}):
        proj = tmp_path / f"p{abs(hash(str(value)))}"
        write_artifact(proj, "wf-odd", workflow_type=value)
        r = run_guard(
            "cc10x_qa_isolation_guard.py",
            {"tool_name": "Bash", "tool_input": {"command": "mkdir x"}},
            proj,
        )
        assert r.returncode == 0 and r.stderr == "" and r.stdout == "", (value, r.stderr[-200:])


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



def test_hooks_readme_lists_the_git_guard_limits_and_does_not_oversell_the_logs(tmp_path):
    readme = (PLUGIN_ROOT / "hooks" / "README.md").read_text()
    section = readme.split("### Git guard limits", 1)[1].split("###", 1)[0]
    for needle in (
        "comment",
        "Pipe-fed executors",
        "One narrow allowance for quoted data (default deny)",
        "not `sort` or `uniq`",
        "Nesting deeper than 8 levels",
        "script written to a file",
        "Destructive text inside other quoted arguments",
        "`git_guard_classifier_failed`",
        "a model that can write files can",
    ):
        assert needle in section, needle
    assert "evidence trail" not in readme


def test_hooks_readme_git_guard_limits_name_every_ask_mode_event(tmp_path):
    # Derived from the guard source, so a renamed event cannot leave the docs stale.
    readme = (PLUGIN_ROOT / "hooks" / "README.md").read_text()
    section = readme.split("### Git guard limits", 1)[1].split("###", 1)[0]
    source = (PLUGIN_ROOT / "scripts" / "cc10x_git_guard.py").read_text()
    main_body = source.split("def main()", 1)[1]
    # Only the `"event":` values main() logs, including both arms of a conditional.
    emitted = set()
    for first, second in re.findall(
        r'"event":\s*"(git_guard_[a-z_]+)"(?:\s+if\s+\w+\s+else\s+"(git_guard_[a-z_]+)")?', main_body
    ):
        emitted |= {first, second} - {""}
    expected = {"git_guard_deferred", "git_guard_ask", "git_guard_mode_read_failed", "git_guard_blocked"}
    assert expected <= emitted, emitted
    for needle in sorted(emitted) + ["gitGuard"]:
        assert f"`{needle}`" in section, needle
    assert "the guard asks" in section  # branch -D prompts despite `Bash(git branch:*)`
    assert "only in a cc10x project" in section
    # The ask/defer counts the docs state come from the source, in words.
    words = dict(enumerate(("zero", "one", "two", "three", "four", "five", "six",
                            "seven", "eight", "nine", "ten", "eleven", "twelve")))
    n_keys = len(git_guard.PRIORITY)
    n_defer = len(git_guard.ASK_MODE_DEFERRED)
    n_ask = n_keys - n_defer
    counts = (
        f"Of the {words[n_keys]} verdict keys, {words[n_ask]} always ask and "
        f"{words[n_defer]} (`push`) defers only when the whole command is a plain push"
    )
    repo = PLUGIN_ROOT.parent.parent
    changelog = (repo / "CHANGELOG.md").read_text()
    unreleased = changelog.split("## [Unreleased]", 1)[1].split("\n## [", 1)[0]
    clause = (
        "a command that is only a plain `git push` defers to Claude Code's permissions; "
        "everything else prompts; see `plugins/cc10x/hooks/README.md`"
    )
    stale = (
        "push-rewrite",
        "do not affect the decision",
        "other git commands in the chain",
        "every guarded git operation in it is a plain push",
        "defers only a plain push",
        "provably plain",
    )
    # The full rule lives only in the hooks README section.
    flat = " ".join(section.split())
    assert counts in flat
    assert "a command that is only a plain `git push`" in flat
    assert "one command, no chains or other statements" in flat
    assert "a remote name, never a URL or path" in flat
    assert "`-C <path>`" in flat and "not visible" in flat.lower()
    for flag in sorted(git_guard.PLAIN_PUSH_FLAGS):
        assert f"`{flag}`" in flat, flag
    for redirect in sorted(git_guard.PLAIN_REDIRECTS):
        assert f"`{redirect}`" in flat, redirect
    # The CHANGELOG carries the counts and the classifier claim, not the list.
    flat = " ".join(unreleased.split())
    assert counts in flat
    assert f"each of the {words[len(ASK_CASES)]} other keys" in flat
    assert "the classifier and the deny set are unchanged from 12.10.0" in flat
    assert clause in flat
    for name, text in (("hooks README", " ".join(section.split())), ("CHANGELOG", flat)):
        for needle in stale:
            assert needle not in text, (name, needle)
    # Everywhere else: the one clause pointing at the hooks README, no list.
    for path in (
        repo / "README.md",
        repo / "docs" / "router-invariants.md",
        PLUGIN_ROOT / "skills" / "cc10x-guide" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "cc10x-router" / "references" / "workflow-artifact-and-hook-policy.md",
    ):
        flat = " ".join(path.read_text().split())
        assert clause in flat, path.name
        assert "`--porcelain`" not in flat and "`2>/dev/null`" not in flat, path.name
        for needle in stale + ("overwrites or deletes remote refs",):
            assert needle not in flat, (path.name, needle)


def test_an_unsafe_workflow_id_checks_the_events_log_by_the_artifact_name(tmp_path):
    path = write_artifact(tmp_path, "wf-aaa", workflow_uuid="../../nowhere", workflow_id="../../nowhere")
    r = run_guard(
        "cc10x_posttooluse_artifact_guard.py",
        {"tool_name": "Write", "tool_input": {"file_path": str(path)}},
        tmp_path,
    )
    assert r.returncode == 0, r.stderr
    assert "missing-event-log" not in " ".join(e["reason"] for e in hook_log_lines(tmp_path))


# --- cc10x_git_guard.py: classify_git_command (P5.T4, finding C5) -------------
#
# Seams: the pure classifier (imported) and the hook process (stdin JSON).
# Corpus strings are assembled from fragments so no destructive command is
# spelled out as one literal.

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
import cc10x_git_guard as git_guard  # noqa: E402


def classify(command):
    return git_guard.classify_git_command(command)


def git(*words: str) -> str:
    return " ".join(("git",) + words)


# Destructive set D, as the words after `git`.
DESTRUCTIVE = (
    ("clean", "--force"),
    ("clean", "-f"),
    ("clean", "-fd"),
    ("clean", "-df"),
    ("clean", "-xfd"),
    ("checkout", "-f"),
    ("checkout", "."),
    ("checkout", "--", "."),
    ("checkout", "*"),
    ("checkout", "HEAD", "--", "."),
    ("restore", "."),
    ("restore", "--", "."),
    ("restore", "./."),
    ("restore", ":/"),
    ("checkout", "--", "./."),
    ("checkout", ":/"),
    ("switch", "-f", "main"),
    ("switch", "--force", "main"),
    ("switch", "--discard-changes", "main"),
    ("worktree", "remove", "--force", "wt"),
    ("worktree", "remove", "-f", "wt"),
    ("branch", "-D", "old"),
    ("branch", "--delete", "--force", "old"),
    ("branch", "-d", "-f", "old"),
    ("stash", "clear"),
    ("reset", "--hard"),
    ("reset", "--hard", "HEAD~1"),
    ("push", "origin", "main"),
    ("push", "--force", "origin", "main"),
    ("push", "-f", "origin", "main"),
    ("push", "--force-with-lease", "origin", "main"),
    ("push", "origin", "+main"),
)

# Wrapper shapes applied to a whole command string.
PREFIX_WRAPPERS = {
    "bare": lambda c: c,
    "env": lambda c: "env VAR=1 " + c,
    "env-clean": lambda c: "env -i HOME=x " + c,
    "assignment": lambda c: "VAR=1 " + c,
    "command": lambda c: "command " + c,
    "nohup": lambda c: "nohup " + c,
    "xargs": lambda c: "xargs " + c,
    "xargs-flags": lambda c: "xargs -I {} -n 1 " + c,
    "sudo": lambda c: "sudo " + c,
    "sudo-user": lambda c: "sudo -u root " + c,
    "time": lambda c: "time " + c,
    "bash-c": lambda c: "bash -c " + shlex.quote(c),
    "bash-lc": lambda c: "bash -lc " + shlex.quote(c),
    "sh-c-dq": lambda c: 'sh -c "' + c + '"',
    "zsh-c": lambda c: "zsh -c " + shlex.quote(c),
    "eval-dq": lambda c: 'eval "' + c + '"',
    "eval-bare": lambda c: "eval " + c,
    "subst": lambda c: "echo $(" + c + ")",
    "subst-dq": lambda c: 'echo "$(' + c + ')"',
    "backtick": lambda c: "echo `" + c + "`",
    "and": lambda c: "true && " + c,
    "or": lambda c: "false || " + c,
    "semi": lambda c: "true; " + c,
    "pipe": lambda c: "true | " + c,
    "newline": lambda c: "true\n" + c,
    "and-after": lambda c: c + " && echo done",
    "semi-after": lambda c: c + "; ls",
    "newline-after": lambda c: c + "\nls",
    "heredoc-sh": lambda c: "sh <<EOF\n" + c + "\nEOF",
    "heredoc-bash": lambda c: "bash <<'EOF'\n" + c + "\nEOF",
    "subshell": lambda c: "(" + c + ")",
    "if-then": lambda c: "if true; then " + c + "; fi",
    "nested": lambda c: "bash -c " + shlex.quote("sudo env X=1 " + c),
    "nested-eval": lambda c: "sh -c " + shlex.quote("eval " + shlex.quote(c)),
}

# Wrapper shapes that rewrite the git invocation itself.
GIT_SHAPES = {
    "git-C": lambda w: git("-C", "/some/dir", *w),
    "git-no-pager": lambda w: git("--no-pager", *w),
    "git-c-other": lambda w: git("-c", "core.pager=cat", *w),
    "alias-plain": lambda w: "git -c "
    + shlex.quote("alias.zz=" + " ".join(w))
    + " zz",
    "alias-shell": lambda w: "git -c "
    + shlex.quote("alias.zz=!" + git(*w))
    + " zz",
}


def prefix_corpus() -> dict[str, str]:
    out = {}
    for words in DESTRUCTIVE:
        for name, wrap in PREFIX_WRAPPERS.items():
            out[f"{name} | {git(*words)}"] = wrap(git(*words))
    return out


def git_shape_corpus() -> dict[str, str]:
    out = {}
    for words in DESTRUCTIVE:
        for name, shape in GIT_SHAPES.items():
            out[f"{name} | {git(*words)}"] = shape(words)
    return out


# Destructive text the model runs through something that is not git itself,
# or as an argument that is not echo/grep/printf data: still denied.
EXECUTED_TEMPLATES = (
    "git commit -m '{}'",
    "ssh host '{}'",
    "python3 -c \"import os; os.system('{}')\"",
    "echo {}",
    "{} # tidy",
    "git -C . log && {}",
)

# Lexer bypass shapes: every one must be denied for every destructive command.
LEXER_TEMPLATES = (
    # A quote inside a shell comment must not open a quoted span that swallows
    # the next line, and ANSI-C quoting has its own escape rules.
    "echo \"x\" # model's note\n{} # it's ready",
    "echo ok # don't\n{}",
    "grep -q x f # say \"hi\n{} # and \"bye",
    "echo $'it\\'s'\n{} # it's ready",
    "printf '%s' $'a\\'b'\n{}\necho 'c' # it's",
    "echo $'it\\'s' ; {} ; echo # don't",
    # Quoted text spanning lines is not a single word of data.
    "echo 'first line\n{}\nlast line'",
)

# Destructive text in an echo/printf/grep quote whose output is consumed by
# something that executes it or writes it to a file. `@@` marks the text.
PIPE_EXECUTED_TEMPLATES = (
    "echo '@@' | xargs -I{} sh -c {}",
    "echo '@@' | xargs bash -c",
    "echo '@@' | while read c; do $c; done",
    "echo '@@' | source /dev/stdin",
    "echo '@@' | . /dev/stdin",
    "printf '%s' '@@' | python3 -c 'import os, sys; os.system(sys.stdin.read())'",
    "echo '@@' | perl -e 'system(<STDIN>)'",
    "echo '@@' | sed 's/a/b/' | sh",
    "echo '@@' |\nsh",
    "echo '@@' | tee run.sh",
    "echo '@@' | cat > run.sh",
    "echo '@@' > f.sh && sh f.sh",
    "echo '@@' >> .git/hooks/pre-commit",
    "printf '%s' '@@' > x.sh; sh x.sh",
    "grep '@@' notes > out.sh && sh out.sh",
    "echo a>b '@@'",
    "echo '@@' >(sh)",
    "bash <(echo '@@')",
    "echo \"$(echo '@@')\"",
    "sh -c \"$(echo '@@')\"",
    "bash -c \"echo '@@'\" | sh",
    "eval \"$(printf '%s' '@@')\"",
    "echo 'echo \"@@\"' | sh",
)

# Shapes from the second re-review. `@@` marks the destructive text. Each one
# once ran executable text past the exemption: a comment-like `#` inside a
# parameter expansion, a CR before `#`, a group or loop in front of a pipe or
# redirect, a quoted or escaped redirect target, and sort/uniq writing files.
BYPASS_TEMPLATES = (
    "echo ${y/ #/}; @@",
    "echo ${x:- # } ; @@",
    "echo ${x%% #*}; @@",
    "cd ${y/ #/}; @@",
    "{ echo ${y/ #/}; @@; }",
    "echo a\r# ; @@",
    "{ echo '@@'; } | sh",
    "( echo '@@' ) | sh",
    "( echo '@@' ) | bash",
    "for i in 1; do echo '@@'; done | sh",
    "while true; do echo '@@'; done | sh",
    "if true; then echo '@@'; fi | sh",
    "{ echo '@@'; } > run.sh",
    "( echo '@@' ) > run.sh",
    "{ echo '@@'; } | tee run.sh",
    "{ bash -c \"echo '@@'\"; } | sh",
    "exec 3> >(sh); echo '@@' >&3",
    "exec >run.sh; echo '@@'",
    "f() { echo '@@'; }; f | sh",
    "( grep -h '@@' notes.txt ) | sh",
    "{ echo '@@'; } | xargs -I{} sh -c {}",
    "echo '@@' >\"run.sh\"",
    "echo '@@' 2>\"run.sh\"",
    "echo '@@' &>\"run.sh\"",
    "echo '@@' >>\"run.sh\"",
    "echo '@@' >&\"run.sh\"",
    "echo '@@' >\\run.sh",
    "echo '@@' | cat >\"run.sh\"",
    "echo '@@' >\"$F\"",
    "echo '@@' 1<>run.sh",
    "echo '@@' | sort -o run.sh",
    "echo '@@' | sort --output=run.sh",
    "echo '@@' | sort -orun.sh",
    "echo '@@' | uniq - run.sh",
    "echo '@@' | uniq /dev/stdin run.sh",
    "echo '@@' | env sort -o run.sh",
    "echo '@@' | sudo sort -o run.sh",
    "echo '@@' | nice sort -o run.sh",
    "echo '@@' | xargs sort -o run.sh",
    "echo '@@' | ./cat",
    "echo '@@' | /usr/bin/sort",
    "cat notes | grep '@@'",
)


def bypass_corpus() -> dict[str, str]:
    return {
        template.replace("@@", git(*words)): template
        for words in DESTRUCTIVE
        for template in BYPASS_TEMPLATES
    }


# Reviewed quoted-data shapes: the destructive text is one quoted argument of
# echo, grep or printf and is never executed. The legacy list denies them all;
# the classifier is allowed to differ on exactly these.
QUOTED_DATA_TEMPLATES = (
    "echo '{}'",
    'echo "{}"',
    'grep "{}" notes.txt',
    "grep -rn '{}' docs/",
    "printf '%s\\n' \"{}\"",
    "echo '{}' | cat",
    "grep -h \"{}\" notes | head -5",
    "printf '%s\\n' '{}' | wc -l",
    "echo '{}' | grep -c x | tail -1",
)

# Copied verbatim from cc10x_git_guard.py at BASE (64b74ee) before the rewrite.
LEGACY_BLOCKED_PATTERNS = [
    (
        r"\bgit\s+push\b.*(--force\b|-f\b|--force-with-lease\b)",
        "git push --force — force-pushing rewrites remote history.",
        None,  # force-push is never token-approvable
    ),
    (
        r"\bgit\s+push\b",
        "git push — pushing to remote. Use a branch and PR instead.",
        "push",
    ),
    (
        r"\bgit\s+reset\s+--hard\b",
        "git reset --hard — destroys uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+clean\s+-[a-z]*f[a-z]*\b",
        "git clean -f — removes untracked files permanently.",
        None,
    ),
    (
        r"\bgit\s+branch\s+-D\b",
        "git branch -D — force-deletes a branch.",
        "branch-delete",
    ),
    (
        r"\bgit\s+checkout\s+\.\s*$",
        "git checkout . — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+checkout\s+--\s+\.\s*$",
        "git checkout -- . — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+checkout\s+\*\s*$",
        "git checkout * — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+restore\s+\.\s*$",
        "git restore . — discards all uncommitted changes (same as checkout .).",
        None,
    ),
]
LEGACY_GLOBAL_FLAGS = (
    r"\bgit\s+((-C\s+\S+|-c\s+\S+|--git-dir(=|\s+)\S+|--work-tree(=|\s+)\S+"
    r"|-P|--no-pager|--paginate)\s+)+"
)


def legacy_denies(command: str) -> bool:
    """The pre-rewrite guard's verdict: any pattern on any normalized segment."""
    parts = re.split(r"\n|;|\|\||&&|\|", command)
    segments = []
    for part in parts:
        if part.strip():
            seg = re.sub(r"\s+#.*$", "", part.strip())
            segments.append(re.sub(LEGACY_GLOBAL_FLAGS, "git ", seg))
    return any(
        re.search(pattern, seg)
        for pattern, _reason, _op in LEGACY_BLOCKED_PATTERNS
        for seg in segments
    )


QUOTED_DATA_EXCEPTIONS = frozenset(
    command
    for command in (
        template.format(git(*words))
        for words in DESTRUCTIVE
        for template in QUOTED_DATA_TEMPLATES
    )
    if legacy_denies(command)
)


def pipe_executed_corpus() -> dict[str, str]:
    return {
        template.replace("@@", git(*words)): template
        for words in DESTRUCTIVE
        for template in PIPE_EXECUTED_TEMPLATES
    }


def verdict(command: str) -> str:
    result = classify(command)
    return "allow" if result is None else f"deny({result[0]})"


def test_classifier_denies_every_destructive_command_in_every_wrapper_shape(tmp_path):
    corpus = {**prefix_corpus(), **git_shape_corpus()}
    assert len(corpus) > 800
    missed = [
        f"{label!r} -> {command!r}"
        for label, command in corpus.items()
        if classify(command) is None
    ]
    assert not missed, f"{len(missed)} undenied, first: {missed[:5]}"


def test_classifier_returns_reason_key_and_message(tmp_path):
    key, message = classify(git("push", "origin", "main"))
    assert key == "push"
    assert message.startswith("git push")
    assert classify(git("branch", "-D", "x"))[0] == "branch-delete"
    assert classify(git("branch", "--delete", "--force", "x"))[0] == "branch-delete"
    for words in DESTRUCTIVE:
        key = classify(git(*words))[0]
        if words == ("push", "origin", "main"):
            assert key == "push"
        elif words[0] == "branch":
            assert key == "branch-delete"
        else:
            assert key not in ("push", "branch-delete"), (words, key)


def test_classifier_allows_the_safe_set(tmp_path):
    safe = [
        git("status"),
        git("diff"),
        git("diff", "."),
        git("log", "--oneline", "-5"),
        git("add", "."),
        git("commit", "-m", "'tidy'"),
        git("checkout", "main"),
        git("checkout", "-b", "feature/x"),
        git("checkout", "--", "file.txt"),
        git("restore", "--staged", "."),
        git("restore", "file.txt"),
        git("branch", "-d", "merged"),
        git("branch", "-m", "new"),
        git("stash"),
        git("stash", "list"),
        git("stash", "pop"),
        git("clean", "-n"),
        git("clean", "--dry-run", "-d"),
        git("reset", "--soft", "HEAD~1"),
        git("reset", "HEAD", "file.txt"),
        git("fetch", "origin"),
        git("pull", "--ff-only"),
        git("-C", "/some/dir", "status"),
        "bash run.sh",
        "ls -la && true",
        "",
        "   ",
    ]
    wrongly_denied = [c for c in safe if classify(c) is not None]
    assert not wrongly_denied, wrongly_denied


def test_classifier_allows_quoted_destructive_text_as_echo_grep_printf_data(tmp_path):
    allowed_shapes = [
        "grep \"" + git("push", "origin", "main") + "\" docs/notes.md",
        "echo '" + git("reset", "--hard") + "'",
        "printf '%s\\n' \"" + git("clean", "-fd") + "\"",
        "grep -rn \"" + git("push", "--force") + "\" plugins/",
        "egrep '" + git("checkout", ".") + "' docs",
        "echo \"" + git("branch", "-D", "x") + "\" | cat",
        "echo '$(" + git("push") + ")'",
    ]
    wrongly_denied = [
        f"{c!r} -> {verdict(c)}" for c in allowed_shapes if classify(c) is not None
    ]
    assert not wrongly_denied, wrongly_denied


def test_classifier_still_denies_quoted_text_that_is_executed(tmp_path):
    executed = [
        "echo '" + git("reset", "--hard") + "' | sh",
        "printf '%s' \"" + git("clean", "-fd") + "\" | bash",
        "echo '" + git("push") + "' | sudo sh",
        "echo \"$(" + git("push") + ")\"",
        "echo `" + git("push") + "`",
        "grep \"x\" f; " + git("push"),
        "grep \"x\" f && " + git("reset", "--hard"),
        "echo hi | xargs " + git("clean", "-fd"),
        "echo " + git("reset", "--hard"),
    ]
    undenied = [c for c in executed if classify(c) is None]
    assert not undenied, undenied


def test_classifier_denies_forced_remote_publish_forms_non_approvably(tmp_path):
    for words in (
        ("push", "--force", "origin", "main"),
        ("push", "-f", "origin", "main"),
        ("push", "-fu", "origin", "main"),
        ("push", "--force-with-lease", "origin", "main"),
        ("push", "origin", "+main"),
    ):
        assert classify(git(*words))[0] == "push-force", words


def test_classifier_picks_the_non_approvable_reason_in_a_mixed_command(tmp_path):
    mixed = git("push", "origin", "main") + " && " + git("reset", "--hard")
    key = classify(mixed)[0]
    assert key not in ("push", "branch-delete")


def test_classifier_never_raises_and_returns_none_or_a_pair(tmp_path):
    odd = [
        "",
        "\x00",
        "'",
        '"',
        "`",
        "$(",
        "((((",
        "))))",
        "$(" * 40,
        "bash -c " * 20 + "'" + git("push") + "'",
        "git",
        "git -c",
        "git -C",
        "git -c alias.x= x",
        "git -c alias.x=x x",
        "git -c alias.x=!x x",
        "xargs",
        "sudo -u",
        "bash -c",
        "eval",
        "\\",
        "echo \\",
        "a" * 100000,
        "&&;;||||",
        git("push", '"unterminated'),
    ]
    for command in odd:
        result = classify(command)
        assert result is None or (
            isinstance(result, tuple)
            and len(result) == 2
            and all(isinstance(part, str) for part in result)
        ), (command[:40], result)


def test_classifier_alias_smuggling_is_resolved_not_trusted(tmp_path):
    alias_cmd = git("-c", shlex.quote("alias.pp=push"), "pp")
    assert classify(alias_cmd)[0] == "push"
    assert classify(git("-c", shlex.quote("alias.pp=status"), "pp")) is None
    assert classify(git("-c", shlex.quote("alias.pp=!echo hi"), "pp")) is None


def test_legacy_denied_corpus_stays_denied_except_reviewed_quoted_data(tmp_path):
    corpus = {
        **prefix_corpus(),
        **git_shape_corpus(),
        **{
            template.format(git(*words)): template
            for words in DESTRUCTIVE
            for template in EXECUTED_TEMPLATES + LEXER_TEMPLATES + QUOTED_DATA_TEMPLATES
        },
        **pipe_executed_corpus(),
        **bypass_corpus(),
        **glued_quote_corpus(),
    }
    legacy_denied = {
        c for c in corpus if legacy_denies(c)
    }
    assert len(legacy_denied) > 400
    lost = [
        f"{c!r}: legacy=deny, classifier={verdict(c)}"
        for c in sorted(legacy_denied)
        if c not in QUOTED_DATA_EXCEPTIONS and classify(c) is None
    ]
    assert not lost, f"{len(lost)} denials lost, first: {lost[:5]}"


TEXT_FILTERS = ("grep", "egrep", "fgrep", "cat", "head", "tail", "wc", "tr", "cut")


def test_quoted_data_exceptions_are_real_and_narrow(tmp_path):
    assert len(QUOTED_DATA_EXCEPTIONS) > 50
    for command in sorted(QUOTED_DATA_EXCEPTIONS):
        assert command.split()[0] in ("echo", "grep", "printf", "cat"), command
        for member in command.split("|"):
            assert member.split()[0] in ("echo", "printf") + TEXT_FILTERS, command
        assert not re.search(r"[<>&;(){}`#]", command), f"operator: {command!r}"
        assert "\\" not in command.replace("'%s\\n'", ""), f"backslash: {command!r}"
        assert legacy_denies(command), f"not a legacy denial, stale entry: {command!r}"
        assert classify(command) is None, f"still denied: {command!r}"


def test_newly_denied_forms_were_allowed_by_the_legacy_list(tmp_path):
    newly = [
        git("branch", "--delete", "--force", "old"),
        git("branch", "-d", "-f", "old"),
        git("checkout", "-f"),
        git("stash", "clear"),
        git("restore", "--", "."),
        git("checkout", "HEAD", "--", "."),
        git("-c", shlex.quote("alias.zz=clean --force"), "zz"),
        "bash -c " + shlex.quote(git("branch", "--delete", "--force", "old")),
        "env X=1 " + git("branch", "--delete", "--force", "old"),
    ]
    for command in newly:
        assert not legacy_denies(command), f"legacy already denied {command!r}"
        assert classify(command) is not None, f"not denied: {command!r}"


def test_git_guard_planning_time_false_positive_is_allowed_by_the_hook(tmp_path):
    command = 'grep -rn "' + git("push", "origin", "main") + '" plugins/ docs/'
    r = run_guard("cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_git_guard_hook_denies_wrapped_destructive_commands(tmp_path):
    for command in (
        "env FOO=1 " + git("branch", "--delete", "--force", "old"),
        "sudo " + git("stash", "clear"),
        "bash -c " + shlex.quote(git("checkout", "-f")),
        git("-c", shlex.quote("alias.zz=clean -fd"), "zz"),
    ):
        r = run_guard(
            "cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path
        )
        assert r.returncode == 0, command
        out = json.loads(r.stdout)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny", command


def test_git_guard_token_for_push_does_not_unlock_a_mixed_destructive_command(tmp_path):
    state = tmp_path / ".cc10x" / "state"
    state.mkdir(parents=True)
    (state / "git-approval.json").write_text(
        json.dumps(
            {
                "wf": "wf-test",
                "operations": ["push"],
                "expires_at": "2099-01-01T00:00:00+00:00",
            }
        )
    )
    command = git("push", "origin", "main") + " && " + git("reset", "--hard")
    r = run_guard("cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path)
    out = json.loads(r.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_git_guard_long_form_force_delete_honors_the_branch_delete_token(tmp_path):
    write_git_token(tmp_path, ["branch-delete"], "2099-01-01T00:00:00+00:00")
    command = git("branch", "--delete", "--force", "feature/old")
    r = run_guard("cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    assert not (tmp_path / ".cc10x" / "state" / "git-approval.json").exists()


def test_git_guard_malformed_empty_and_non_bash_payloads_exit_0_or_2_only(tmp_path):
    payloads = [
        None,
        [],
        "text",
        {},
        {"tool_input": None},
        {"tool_input": []},
        {"tool_input": "git status"},
        {"tool_input": {}},
        {"tool_input": {"command": ""}},
        {"tool_input": {"command": None}},
        {"tool_input": {"command": 123}},
        {"tool_input": {"command": ["git", "status"]}},
        {"tool_name": "Write", "tool_input": {"file_path": "a.txt", "content": "x"}},
        {"tool_name": "Read", "tool_input": {"file_path": "a.txt"}},
        {"tool_input": {"command": 'echo "unterminated'}},
        {"tool_input": {"command": "echo 'unterminated"}},
        {"tool_input": {"command": "$(((("}},
        {"tool_input": {"command": "\x00\x01"}},
    ]
    for payload in payloads:
        r = run_guard("cc10x_git_guard.py", payload, tmp_path)
        assert r.returncode in (0, 2), (payload, r.returncode, r.stderr[-300:])
    r = run_guard("cc10x_git_guard.py", None, tmp_path, extra_env={"X": "1"})
    assert r.returncode in (0, 2)


def test_git_guard_unterminated_quote_with_destructive_text_is_still_denied(tmp_path):
    command = git("push", '"origin', "main")
    r = run_guard("cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path)
    assert r.returncode in (0, 2)
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_classifier_denies_switch_force_wide_pathspecs_and_forced_worktree_remove(tmp_path):
    denied = {
        git("switch", "-f", "main"): "checkout-force",
        git("switch", "--force", "main"): "checkout-force",
        git("switch", "--discard-changes", "main"): "checkout-force",
        git("restore", "./."): "discard-all",
        git("restore", "':/'"): "discard-all",
        git("restore", "':(top)'"): "discard-all",
        git("checkout", "--", "./."): "discard-all",
        git("checkout", "':/'"): "discard-all",
        git("worktree", "remove", "--force", "wt"): "worktree-force",
        git("worktree", "remove", "-f", "wt"): "worktree-force",
        git("-C", "sub", "worktree", "remove", "-f", "-f", "wt"): "worktree-force",
    }
    for command, key in denied.items():
        verdict = classify(command)
        assert verdict is not None and verdict[0] == key, (command, verdict)


def test_classifier_keeps_plain_switch_worktree_and_staged_restore_allowed(tmp_path):
    for command in (
        git("switch", "main"),
        git("switch", "-c", "topic"),
        git("worktree", "add", "wt"),
        git("worktree", "remove", "wt"),
        git("worktree", "list"),
        git("restore", "--staged", "':/'"),
        git("restore", "src/./a.py"),
    ):
        assert classify(command) is None, command


def test_classifier_denies_every_executed_text_shape(tmp_path):
    corpus = {
        template.format(git(*words)): template
        for words in DESTRUCTIVE
        for template in LEXER_TEMPLATES
    }
    corpus.update(pipe_executed_corpus())
    corpus.update(bypass_corpus())
    assert len(corpus) > 1000
    undenied = [f"{c!r}" for c in sorted(corpus) if classify(c) is None]
    assert not undenied, f"{len(undenied)} undenied, first: {undenied[:6]}"


def test_classifier_denies_after_a_comment_holding_a_quote_character(tmp_path):
    push = git("push", "origin", "main")
    reset = git("reset", "--hard")
    clean = git("clean", "-fd")
    shapes = [
        'echo "x" # model\'s note\n' + push + " # it's ready",
        'echo "x" # model\'s note\n' + reset + " # it's ready",
        'echo "x" # model\'s note\n' + clean + " # it's ready",
        'echo "x" # say "hi\n' + push + ' # and "bye',
        "echo $'it\\'s'\n" + push + " # it's ready",
        "echo ok # don't\n" + reset,
    ]
    for command in shapes:
        assert classify(command) is not None, command
        r = run_guard("cc10x_git_guard.py", {"tool_input": {"command": command}}, tmp_path)
        assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_classifier_reads_comments_and_ansi_c_quotes_like_the_shell(tmp_path):
    assert classify("echo hi # " + git("push")) is not None
    assert classify("echo hi;# " + git("push")) is not None
    assert classify("echo hi # tidy") is None
    assert classify("echo a#b && " + git("push")) is not None
    assert classify("$'" + "git" + "' push origin main") is not None
    assert classify("echo $'it\\'s' && " + git("reset", "--hard")) is not None


def test_classifier_denies_quoted_text_spanning_lines(tmp_path):
    command = "echo 'notes\n" + git("push", "origin", "main") + "\nmore'"
    assert classify(command) is not None
    assert classify("echo 'one line " + git("push") + "'") is None


def test_classifier_allows_quoted_text_only_through_text_filter_pipes(tmp_path):
    allowed = [
        "grep -rn \"" + git("push", "origin", "main") + "\" plugins/ | head",
        "grep -h '" + git("reset", "--hard") + "' f | cut -d: -f1 | head -3",
        "grep -c \"" + git("clean", "-fd") + "\" f | tail -1",
        "echo '" + git("push") + "' | wc -l",
    ]
    wrongly_denied = [c for c in allowed if classify(c) is not None]
    assert not wrongly_denied, wrongly_denied
    denied = [
        "grep '" + git("push") + "' f | xargs sh -c",
        "git log | grep '" + git("push") + "'",
        "cat f | grep '" + git("reset", "--hard") + "' | head -3",
        "grep -c \"" + git("clean", "-fd") + "\" f 2>&1 | tail -1",
        "grep '" + git("push") + "' f 2>/dev/null",
        "grep '" + git("push") + "' f > out.sh",
        "echo '" + git("push") + "' <<< x",
    ]
    undenied = [c for c in denied if classify(c) is None]
    assert not undenied, undenied


def nested_substitution(levels: int, inner: str) -> str:
    return "echo $(" * levels + inner + ")" * levels


def test_classifier_denies_every_second_review_bypass_shape(tmp_path):
    corpus = bypass_corpus()
    assert len(corpus) > 900
    undenied = [c for c in sorted(corpus) if classify(c) is None]
    assert not undenied, f"{len(undenied)} undenied, first: {undenied[:6]}"


def test_classifier_floor_runs_over_the_whole_raw_command(tmp_path):
    checked = 0
    for words in DESTRUCTIVE:
        text = git(*words)
        for template in BYPASS_TEMPLATES:
            command = template.replace("@@", text)
            if legacy_denies(command):
                checked += 1
                assert classify(command) is not None, command
    assert checked > 400


def test_quoted_data_allowance_is_a_default_deny_allowlist(tmp_path):
    d = git("push", "origin", "main")
    allowed = [
        f"echo '{d}'",
        f'echo "{d}"',
        f"printf '%s\\n' '{d}' | wc -l",
        f"grep -rn '{d}' docs/ | head -5 | cut -d: -f1",
        f"egrep '{d}' notes | tr a-z A-Z",
        f"fgrep -c '{d}' notes | tail -1",
        f"echo '{d}' | cat | grep -c x | head",
        f"echo '$(rm -rf x) `y` ; & > # \\ {d}'",
    ]
    wrongly_denied = [c for c in allowed if classify(c) is not None]
    assert not wrongly_denied, wrongly_denied
    denied = [
        f"echo '{d}' | sort",
        f"echo '{d}' | uniq",
        f"echo '{d}' | ./cat",
        f"echo '{d}' | /bin/cat",
        f"echo '{d}' | tee f",
        f"echo '{d}' | xargs echo",
        f"echo '{d}' | sed s/a/b/",
        f"cat notes | grep '{d}'",
        f"ls | grep '{d}'",
        f"echo '{d}' ; ls",
        f"echo '{d}' && ls",
        f"echo '{d}' &",
        f"echo '{d}' || ls",
        f"echo '{d}' |& cat",
        f"echo '{d}' > f",
        f"echo '{d}' < f",
        f"echo '{d}' # note",
        f"echo '{d}' \\| sh",
        f"echo '{d}' \r| sh",
        f"echo '{d}'\nls",
        f"echo '{d}' $x",
        f"echo '{d}' `ls`",
        f"echo '{d}' $(ls)",
        f"echo \"$(true)\" '{d}'",
        f'echo "$x {d}"',
        f'echo "`ls` {d}"',
        f'echo "a\\"b" \'{d}\'',
        f"echo '{d}' ({d})",
        f"echo '{d}' {{ x }}",
        f"echo '{d}' | cat <<EOF",
        f"echo '{d}' if",
        f"echo '{d}' .",
        f"echo '{d}' exec",
        f"FOO=1 echo '{d}'",
        f"time echo '{d}'",
        f"env echo '{d}'",
        f"echo {d}",
        f"echo '{d}' {d}",
        f"echo ok | grep '{d}'",
        f"echo '{d}",
        f'echo "{d}',
        f"echo '{d}' | | cat",
        f"| echo '{d}'",
        f"echo '{d}' |",
    ]
    undenied = [c for c in denied if classify(c) is None]
    assert not undenied, undenied
    for word in (
        "exec", "eval", "source", ".", "function", "for", "while", "until", "if",
        "case", "do", "done", "then", "fi",
    ):
        assert classify(f"echo '{d}' {word}") is not None, word


def test_classifier_denies_at_the_depth_cap_instead_of_flooring(tmp_path):
    hidden = "g''i''t p''u''s''h origin main"
    assert classify(nested_substitution(3, hidden)) is not None
    nine = nested_substitution(9, hidden)
    result = classify(nine)
    assert result is not None and result[0] == "classifier-error", result
    assert classify(nested_substitution(12, "ls")) is not None
    deep = classify(nested_substitution(400, "ls"))
    assert deep is not None and deep[0] == "classifier-error"


def test_classifier_denies_comment_dropped_text_in_the_executable_tail(tmp_path):
    assert classify("echo ${y/ #/}; " + git("stash", "clear")) is not None
    assert classify("echo a\r# ; " + git("checkout", "-f")) is not None
    assert classify("echo hi # " + git("stash", "clear")) is not None


def test_classifier_crash_fallback_uses_a_git_word_boundary(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "classify_git_command", _boom)]
    for harmless in ("cat .gitignore", "echo digit legit", "ls gitlab-notes"):
        code, out = run_git_guard_in_process(tmp_path, harmless, patches)
        assert code == 0 and out.strip() == "", harmless
    for text in (git("status"), "env " + git("status"), "x;" + git("push"), "GIT status"):
        code, out = run_git_guard_in_process(tmp_path, text, patches)
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny", text


def test_classifier_crash_fallback_logs_the_decision_field(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "classify_git_command", _boom)]
    run_git_guard_in_process(tmp_path, git("status"), patches)
    run_git_guard_in_process(tmp_path, "ls .gitignore", patches)
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "git_guard_classifier_failed"]
    assert [e["decision"] for e in events] == ["deny", "allow"]


def test_normalize_segment_is_linear_on_long_whitespace_runs(tmp_path):
    import time

    for command in (
        "echo" + " " * 200_000,
        "echo" + " " * 200_000 + "x",
        git("restore") + " " * 200_000 + "x",
        git("") + "-P " * 60_000 + "status",
        "echo" + " \t" * 100_000 + "end",
        "echo '" + " " * 200_000 + "x' | sh",
        "ls " + " " * 200_000 + "x | sh",
        "echo \"" + " " * 200_000 + "x\" | cat | sh",
    ):
        started = time.monotonic()
        classify(command)
        assert time.monotonic() - started < 2.0, command[:20]
    assert classify("echo" + " " * 200_000 + "# " + git("push")) is not None


def test_classifier_floor_does_not_depend_on_the_lexer_scan(tmp_path):
    from unittest import mock

    corpus = {**prefix_corpus(), **pipe_executed_corpus(), **bypass_corpus()}
    legacy_denied = [
        c for c in corpus if legacy_denies(c) and c not in QUOTED_DATA_EXCEPTIONS
    ]
    assert len(legacy_denied) > 1000
    with mock.patch.object(git_guard, "_scan", lambda *args, **kwargs: []):
        lost = [c for c in legacy_denied if classify(c) is None]
    assert not lost, f"{len(lost)} lost without the scan, first: {lost[:5]}"


def test_classifier_reads_cr_as_an_ordinary_word_character(tmp_path):
    assert classify("git\rstash\rclear") is None
    assert classify("echo a\r# tidy") is None
    assert classify("echo a\r# ; " + git("stash", "clear")) is not None


def run_git_guard_in_process(
    project_dir: Path, command: str, patches=(), extra_env: dict[str, str] | None = None
):
    import contextlib
    import io
    from unittest import mock

    import cc10x_hooklib

    cc10x_hooklib._input_cwd = None
    stdout = io.StringIO()
    payload = json.dumps({"tool_input": {"command": command}})
    env = {
        "CLAUDE_PROJECT_DIR": str(project_dir),
        "CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT),
        **(extra_env or {}),
    }
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.dict(os.environ, env))
        if "CLAUDE_PLUGIN_DATA" not in env:
            # An ambient override (a developer's real hook-mode.json) must not
            # reach load_mode(); patch.dict restores it on exit.
            os.environ.pop("CLAUDE_PLUGIN_DATA", None)
        stack.enter_context(mock.patch.object(sys, "stdin", io.StringIO(payload)))
        stack.enter_context(contextlib.redirect_stdout(stdout))
        for target, name, value in patches:
            stack.enter_context(mock.patch.object(target, name, value))
        code = git_guard.main()
    return code, stdout.getvalue()


def _boom(*_args, **_kwargs):
    raise RuntimeError("simulated classifier bug")


def test_git_guard_classifier_crash_fails_closed_for_git_text_and_logs(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "classify_git_command", _boom)]
    code, out = run_git_guard_in_process(tmp_path, git("status"), patches)
    assert code == 0
    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "classifier" in decision["permissionDecisionReason"]
    events = [e for e in hook_log_lines(tmp_path) if e["event"] == "git_guard_classifier_failed"]
    assert len(events) == 1
    assert events[0]["reason"] == "classifier-error" and events[0]["error"] == "RuntimeError"


def test_git_guard_classifier_crash_allows_commands_without_git_text(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "classify_git_command", _boom)]
    code, out = run_git_guard_in_process(tmp_path, "ls -la", patches)
    assert code == 0 and out.strip() == ""
    assert any(
        e["event"] == "git_guard_classifier_failed" for e in hook_log_lines(tmp_path)
    )


def test_git_guard_classifier_error_is_not_unlockable_by_a_token(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    write_git_token(tmp_path, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00")
    patches = [(git_guard, "classify_git_command", _boom)]
    code, out = run_git_guard_in_process(tmp_path, git("push"), patches)
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert (tmp_path / ".cc10x" / "state" / "git-approval.json").exists()


def make_worktree(path: Path, main: Path, name: str = "wt") -> Path:
    gitdir = main / ".git" / "worktrees" / name
    gitdir.mkdir(parents=True, exist_ok=True)
    (gitdir / "commondir").write_text("../..\n")
    (gitdir / "gitdir").write_text(str(path / ".git") + "\n")
    path.mkdir(parents=True, exist_ok=True)
    (path / ".git").write_text(f"gitdir: {gitdir}\n")
    return path


def test_git_guard_honors_a_token_and_logs_in_the_linked_worktree(tmp_path):
    main = make_checkout(tmp_path / "main")
    (main / ".cc10x").mkdir()
    wt = make_worktree(tmp_path / "wt", main)
    token = write_git_token(wt, ["push"], "2099-01-01T00:00:00+00:00")
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": git("push", "origin", "feature")}, "cwd": str(wt)},
        main,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    assert not token.exists()
    assert any(e["event"] == "git_guard_token_consumed" for e in hook_log_lines(wt))
    assert hook_log_lines(main) == []


def test_git_guard_non_object_tokens_are_invalid_removed_and_deny(tmp_path):
    for body in ("[]", "null", '"x"', "7", "true"):
        proj = tmp_path / f"proj-{abs(hash(body))}"
        state = proj / ".cc10x" / "state"
        state.mkdir(parents=True)
        token = state / "git-approval.json"
        token.write_text(body)
        r = run_guard(
            "cc10x_git_guard.py", {"tool_input": {"command": git("push", "origin", "main")}}, proj
        )
        assert r.returncode == 0, (body, r.stderr[-200:])
        assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny", body
        assert not token.exists(), body
        assert any(
            e["event"] == "git_guard_token_invalid" for e in hook_log_lines(proj)
        ), body


def test_git_guard_a_crash_in_token_consumption_denies_and_logs(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "consume_approval", _boom)]
    code, out = run_git_guard_in_process(tmp_path, git("push", "origin", "main"), patches)
    assert code == 0
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert any(
        e["event"] == "git_guard_token_check_failed" for e in hook_log_lines(tmp_path)
    )


# --- gitGuard hook mode: block (default) | ask ---------------------------------


def git_guard_mode_data(tmp_path: Path, value: object) -> Path:
    """A CLAUDE_PLUGIN_DATA dir whose hook-mode.json sets gitGuard."""
    data = tmp_path / "plugin-data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "hook-mode.json").write_text(json.dumps({"gitGuard": value}))
    return data


def run_git_guard_mode(project_dir: Path, command: str, data: Path | None):
    (project_dir / ".cc10x").mkdir(parents=True, exist_ok=True)
    return run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": command}},
        project_dir,
        extra_env={"CLAUDE_PLUGIN_DATA": str(data)} if data is not None else None,
    )


def git_guard_events(project_dir: Path) -> list[dict]:
    return [e for e in hook_log_lines(project_dir) if e["event"].startswith("git_guard_")]


def test_git_guard_ask_mode_defers_push_only(tmp_path):
    assert git_guard.ASK_MODE_DEFERRED == frozenset({"push"})
    data = git_guard_mode_data(tmp_path, "ask")
    proj = tmp_path / "proj"
    token = write_git_token(proj, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00")
    r = run_git_guard_mode(proj, git("push", "origin", "main"), data)
    assert r.returncode == 0, r.stderr[-300:]
    assert r.stdout.strip() == ""
    events = git_guard_events(proj)
    assert [(e["event"], e["decision"]) for e in events] == [("git_guard_deferred", "defer")]
    assert token.exists()  # ask mode never reads or consumes the token


def test_git_guard_ask_mode_asks_for_branch_delete_and_keeps_the_token(tmp_path):
    # The shipped settings template allows `Bash(git branch:*)`, so a deferred
    # forced delete would run with no prompt; the guard asks instead.
    data = git_guard_mode_data(tmp_path, "ask")
    proj = tmp_path / "proj"
    token = write_git_token(proj, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00")
    r = run_git_guard_mode(proj, git("branch", "-D", "old"), data)
    assert r.returncode == 0, r.stderr[-300:]
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask"
    events = git_guard_events(proj)
    assert [(e["event"], e["decision"]) for e in events] == [("git_guard_ask", "ask")]
    assert token.exists()


ASK_CASES = {
    "branch-delete": git("branch", "-D", "old"),
    "push-force": git("push", "--force", "origin", "main"),
    "reset-hard": git("reset", "--hard", "HEAD~1"),
    "clean-force": git("clean", "-fd"),
    "discard-all": git("restore", "."),
    "checkout-force": git("switch", "-f", "main"),
    "worktree-force": git("worktree", "remove", "--force", "wt"),
    "stash-clear": git("stash", "clear"),
    "classifier-error": git("pu{sh,}", "origin"),
    "command-too-large": git("status") + " " + "x" * 65536,
}

# Pushes that are not plain (allow-list), each built from split literals so no
# command is spelled out whole. All of them ask in ask mode; in block mode each
# is a `push`, as in 12.10.0.
_P = "pu" + "sh"
_F = "--for" + "ce"
NON_PLAIN_PUSH_CASES = {
    # Remote-rewriting flags and refspecs.
    "mirror": git(_P, "--mirror", "origin"),
    "mirror-abbreviated": git(_P, "--mirr", "origin"),
    "delete": git(_P, "--delete", "origin", "old"),
    "delete-short": git(_P, "-d", "origin", "old"),
    "delete-short-combined": git(_P, "-ud", "origin", "old"),
    "colon-refspec": git(_P, "origin", ":old"),
    "bare-colon": git(_P, "origin", ":"),
    "prune": git(_P, "--prune", "origin", "refs/heads/*:refs/heads/*"),
    "unknown-flag": git(_P, "--receive-pack=x", "origin"),
    "end-of-options": git(_P, "--", "origin"),
    # Config overrides.
    "config-mirror": git("-c", "remote.origin.mirror=true", _P, "origin"),
    "config-mirror-bare": git("-c", "remote.origin.mirror", _P, "origin"),
    "config-mirror-false": git("-c", "remote.origin.mirror=false", _P, "origin"),
    "config-force-refspec": git("-c", "remote.origin.push=+refs/heads/*:refs/heads/*", _P, "origin"),
    "config-env-equals": git("--config-env=remote.origin.mirror=MIRROR", _P, "origin"),
    "config-env-two-word": git("--config-env", "remote.origin.mirror=MIRROR", _P, "origin"),
    "alias-under-remote-config": git("-c", "remote.o.mirror=true", "-c", "alias.p=" + _P, "p"),
    "alias": git("-c", "alias.p=" + _P, "p", "origin"),
    "paginate-then-force-w": git("-p", _P, _F[:-2] + "-w"),
    "no-replace-objects-then-force-w": git("--no-replace-objects", _P, _F[:-2] + "-w"),
    "git-dir": git("--git-dir=.git", _P, "origin"),
    # Env prefixes and wrappers.
    "git-config-count": "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=remote.origin.mirror "
    "GIT_CONFIG_VALUE_0=true " + git(_P, "origin"),
    "git-config-parameters": "GIT_CONFIG_PARAMETERS=\"'remote.origin.mirror=true'\" " + git(_P, "origin"),
    "env-wrapper": "env X=1 " + git(_P),
    "command-wrapper": "command " + git(_P, "origin"),
    "bash-c": "bash -c '" + git(_P, "origin", "main") + "'",
    "path-git": "/usr/bin/" + git(_P, "origin"),
    # Shell-built arguments.
    "brace-flag": git(_P, "--{" + _F[2:] + ",verbose}", "origin"),
    "brace-colon": git(_P, "origin", "{:x,}"),
    "ansi-c-plus": git(_P, "origin", "$'\\x2bmain'"),
    "ansi-c-flag": git(_P, "-$'\\x66'", "origin"),
    "substitution": git(_P, "origin", "$(echo +main)"),
    "backtick": git(_P, "origin", "`echo +main`"),
    "variable": git(_P, "origin", "$VAR"),
    "braced-variable": git(_P, "origin", "${VAR}"),
    "glob": git(_P, "origin", "ma*"),
    "quoted-arg": git(_P, "origin", '"main"'),
    "escaped-arg": git(_P, "origin", "ma\\in"),
    "quoted-subcommand": git("'" + _P + "'", "origin"),
    # zsh EXTENDED_GLOB globs `^pat` and `a~b`; `~` and `~user` tilde-expand
    # to a local path, which git then reads as a path remote.
    "caret-glob": git(_P, "origin", "^x"),
    "caret-glob-in-ref": git(_P, "origin", "refs/^x"),
    "tilde-glob": git(_P, "origin", "a~b"),
    "tilde-remote": git(_P, "~", "main"),
    "tilde-user-remote": git(_P, "~root", "main"),
    "tilde-in-refspec": git(_P, "origin", "HEAD~1:refs/heads/x"),
    # Redirects outside the harmless output set, and pipelines.
    "redirect-to-file": git(_P, "origin", "main", ">", "out.txt"),
    "redirect-to-file-joined": git(_P, "origin", "main", ">out.txt"),
    "input-redirect": git(_P, "origin", "main", "<", "in"),
    "heredoc": git(_P, "origin", "main", "<<", "EOF"),
    "clobber-redirect": git(_P, "origin", "main", ">|", "f"),
    "other-fd-dup": git(_P, "origin", "main", ">&2"),
    "redirect-not-trailing": git(_P, "2>&1", "origin", "main"),
    "quoted-dev-null": git(_P, "origin", "main", ">", "'/dev/null'"),
    "process-substitution": git(_P, "origin", "main", ">(cat)"),
    "pipe-to-tee": git(_P, "origin", "main", "2>&1") + " | tee log",
    "pipe-to-filter": git(_P, "origin", "main") + " | tail -1",
}

# A segment-plain push that the rest of the command can rewrite, or that
# names a URL or path remote. ask mode defers only a command that is one plain
# push and nothing else, so every one of these asks.
_PUSH_OM = git(_P, "origin", "main")
NOT_LONE_PUSH_CASES = {
    "function-parens": "git() { command " + git('"$@"', _F) + "; }; " + _PUSH_OM,
    "function-keyword": "function git { command " + git('"$@"', _F) + "; }; " + _PUSH_OM,
    "function-multiline": "git() {\n  command " + git('"$@"', _F) + "\n}\n" + _PUSH_OM,
    "alias-line": "alias git='" + git("-c", "remote.origin.mirror=true") + "'\n" + _PUSH_OM,
    "git-config-then-push": git("config", "remote.origin.mirror", "true") + "; " + _PUSH_OM,
    "export-git-config": "export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=remote.origin.mirror "
    "GIT_CONFIG_VALUE_0=true; " + _PUSH_OM,
    "path-assignment": "PATH=./bin:$PATH; " + _PUSH_OM,
    "path-prefix": "PATH=./bin " + _PUSH_OM,
    "set-positional": "set -- " + _F + "; " + _PUSH_OM,
    "heredoc-apostrophe-continuation": "cat <<'EOF'\nit's\nEOF\n" + _PUSH_OM + " \\\n" + _F,
    "continuation": _PUSH_OM + " \\\n" + _F,
    "cd-then-push": "cd x && " + _PUSH_OM,
    "background": _PUSH_OM + " &",
    "semicolon-after": _PUSH_OM + ";",
    "or-chain": _PUSH_OM + " || true",
    "subshell": "(" + _PUSH_OM + ")",
    "brace-group": "{ " + _PUSH_OM + "; }",
    "two-lines": _PUSH_OM + "\n" + _PUSH_OM,
    "comment-tail": _PUSH_OM + " # note",
    "chained-add-commit-push": git("add", ".") + " && " + git("commit", "-m", '"msg"') + " && " + _PUSH_OM,
    "url-remote": git(_P, "https://h/x.git", "main"),
    "scp-remote": git(_P, "git" + "@h:x/y.git"),
    "path-remote": git(_P, "../other", "main"),
    "ref-with-empty-side": git(_P, "origin", "main:"),
}

# The harmless output redirects a plain push may end with.
PLAIN_REDIRECT_SUFFIXES = (
    ("2>&1",), (">/dev/null",), ("2>/dev/null",), ("&>/dev/null",), ("1>/dev/null",),
    (">", "/dev/null"), ("2>", "/dev/null"), ("&>", "/dev/null"), ("1>", "/dev/null"),
    (">/dev/null", "2>&1"), ("2>/dev/null", "1>", "/dev/null"),
)

# Provably plain pushes: they defer in ask mode.
PLAIN_PUSH_CASES = (
    git(_P),
    git(_P, "origin"),
    git(_P, "-u", "origin", "feat/x-1"),
    git(_P, "origin", "HEAD"),
    git(_P, "origin", "main:main"),
    git(_P, "--tags", "origin"),
    git("-C", "some/dir", _P, "origin", "main"),
    git("-C", "a", "-C", "b/c", _P),
    git(_P, "--set-upstream", "--verbose", "--no-verify", "--atomic", "origin", "HEAD:refs/heads/x"),
    git(_P, "origin") + "\n",
) + tuple(git(_P, "origin", "main", *suffix) for suffix in PLAIN_REDIRECT_SUFFIXES) + tuple(
    git(_P, flag, "origin") for flag in sorted(git_guard.PLAIN_PUSH_FLAGS)
)


def ask_reason(verdict):
    # In ask mode a `push` verdict asks only when the command is not one plain push.
    return git_guard.MSG_NOT_LONE_PUSH if verdict[0] == "push" else verdict[1]


def test_git_guard_plain_word_admits_no_shell_special_character(tmp_path):
    # Each of these is expanded, globbed, quoted or split by bash or zsh.
    for ch in "$`{}*?[]^~#!=\\'\" \t\n":
        assert git_guard.PLAIN_WORD.match("a" + ch + "b") is None, repr(ch)
        assert git_guard.PLAIN_WORD.match(ch) is None, repr(ch)


def test_git_guard_classifier_keys_and_push_verdicts_are_unchanged(tmp_path):
    # Block mode: the verdict keys and the `push` verdict for every push table
    # entry match 12.10.0 (the classifier itself is checked by diff, not here).
    assert "push-rewrite" not in git_guard.PRIORITY
    assert git_guard.APPROVABLE == {"push": "push", "branch-delete": "branch-delete"}
    assert len(git_guard.PRIORITY) == 11
    for name, cmd in NON_PLAIN_PUSH_CASES.items():
        assert classify(cmd) == ("push", git_guard.MSG_PUSH), (name, classify(cmd))
    for cmd in PLAIN_PUSH_CASES:
        assert classify(cmd) == ("push", git_guard.MSG_PUSH), cmd


def test_git_guard_plain_push_flags_are_exactly_the_contract_set(tmp_path):
    assert git_guard.PLAIN_PUSH_FLAGS == frozenset({
        "-u", "--set-upstream", "-v", "--verbose", "-q", "--quiet", "-n", "--dry-run",
        "--tags", "--follow-tags", "--no-verify", "--porcelain", "--progress",
        "--no-progress", "--atomic",
    })
    for flag in git_guard.PLAIN_PUSH_FLAGS:
        assert classify(git(_P, flag, "origin")) == ("push", git_guard.MSG_PUSH), flag


def test_git_guard_ask_mode_defers_every_plain_push(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    for i, cmd in enumerate(PLAIN_PUSH_CASES):
        proj = tmp_path / f"plain-{i}"
        r = run_git_guard_mode(proj, cmd, data)
        assert r.returncode == 0 and r.stdout.strip() == "", (cmd, r.stdout)
        assert [(e["event"], e["decision"]) for e in git_guard_events(proj)] == [
            ("git_guard_deferred", "defer")
        ], cmd


def test_git_guard_ask_mode_asks_for_every_non_plain_push_and_keeps_the_token(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    env = {"CLAUDE_PLUGIN_DATA": str(data)}
    for name, cmd in {**NON_PLAIN_PUSH_CASES, **NOT_LONE_PUSH_CASES}.items():
        proj = tmp_path / f"rewrite-{name}"
        token = write_git_token(proj, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00")
        before = token.read_text()
        code, out = run_git_guard_in_process(proj, cmd, extra_env=env)
        assert code == 0, name
        assert out.strip(), name
        decision = json.loads(out)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "ask", name
        assert ask_reason(classify(cmd)) in decision["permissionDecisionReason"], name
        assert [(e["event"], e["decision"]) for e in git_guard_events(proj)] == [("git_guard_ask", "ask")], name
        assert token.read_text() == before, name


def test_git_guard_lone_plain_push_check_fails_closed(tmp_path):
    # Any exception inside the whole-command check means not plain: ask.
    data = git_guard_mode_data(tmp_path, "ask")
    (tmp_path / ".cc10x").mkdir()
    class Raising:
        match = staticmethod(_boom)

    # PLAIN_WORD is read only by the whole-command check, not by the classifier.
    patches = [(git_guard, "PLAIN_WORD", Raising())]
    code, out = run_git_guard_in_process(
        tmp_path, git(_P, "origin"), patches, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
    )
    assert code == 0
    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "ask"
    assert git_guard.MSG_NOT_LONE_PUSH in decision["permissionDecisionReason"]
    assert [(e["event"], e["decision"]) for e in git_guard_events(tmp_path)] == [("git_guard_ask", "ask")]


def test_git_guard_block_mode_rewrite_pushes_match_plain_push(tmp_path):
    def observe(proj, cmd, token_ops):
        token = write_git_token(proj, token_ops, "2099-01-01T00:00:00+00:00") if token_ops else None
        r = run_git_guard_mode(proj, cmd, None)
        events = [(e["event"], e["decision"], e["reason"]) for e in git_guard_events(proj)]
        return r.returncode, r.stdout, events, token is not None and token.exists()

    plain = observe(tmp_path / "plain", PUSH_CASE, None)
    plain_token = observe(tmp_path / "plain-token", PUSH_CASE, ["push"])
    assert json.loads(plain[1])["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert plain_token[1] == "" and plain_token[3] is False
    for name, cmd in NON_PLAIN_PUSH_CASES.items():
        assert observe(tmp_path / f"b-{name}", cmd, None) == plain, name
        assert observe(tmp_path / f"t-{name}", cmd, ["push"]) == plain_token, name


def test_git_guard_ask_mode_asks_for_every_non_deferred_key(tmp_path):
    assert set(ASK_CASES) == set(git_guard.PRIORITY) - git_guard.ASK_MODE_DEFERRED
    assert len(ASK_CASES) == 10
    data = git_guard_mode_data(tmp_path, "ask")
    for key, cmd in ASK_CASES.items():
        verdict = classify(cmd)
        assert verdict is not None and verdict[0] == key, key
        proj = tmp_path / f"proj-{key}"
        r = run_git_guard_mode(proj, cmd, data)
        assert r.returncode == 0, (key, r.stderr[-300:])
        decision = json.loads(r.stdout)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "ask", key
        assert ask_reason(verdict) in decision["permissionDecisionReason"], key
        events = git_guard_events(proj)
        assert [(e["event"], e["decision"]) for e in events] == [("git_guard_ask", "ask")], key


def test_git_guard_ask_mode_mixed_push_and_reset_asks(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    cmd = git("push", "origin", "main") + " && " + git("reset", "--hard")
    r = run_git_guard_mode(tmp_path / "proj", cmd, data)
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask"
    assert [e["event"] for e in git_guard_events(tmp_path / "proj")] == ["git_guard_ask"]


PUSH_CASE = git("push", "origin", "main")
CHAINED_PUSH_AND_BRANCH_DELETE = (
    PUSH_CASE + " && " + git("branch", "-D", "old"),
    git("branch", "-D", "old") + "; " + PUSH_CASE,
    PUSH_CASE + " && " + git("branch", "--delete", "--force", "old"),
    git("branch", "--delete", "--force", "old") + " && " + PUSH_CASE,
)


def test_git_guard_ask_mode_push_chained_with_branch_delete_asks(tmp_path):
    # A push in the chain must not carry a forced branch delete past the prompt.
    data = git_guard_mode_data(tmp_path, "ask")
    for i, cmd in enumerate(CHAINED_PUSH_AND_BRANCH_DELETE):
        proj = tmp_path / f"proj-{i}"
        token = write_git_token(proj, ["push", "branch-delete"], "2099-01-01T00:00:00+00:00")
        before = token.read_text()
        r = run_git_guard_mode(proj, cmd, data)
        assert r.returncode == 0, (cmd, r.stderr[-300:])
        assert r.stdout.strip(), cmd
        decision = json.loads(r.stdout)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "ask", cmd
        # The verdict is `push` (12.10.0 priority); the command is not one plain push.
        assert git_guard.MSG_NOT_LONE_PUSH in decision["permissionDecisionReason"], cmd
        events = git_guard_events(proj)
        assert [(e["event"], e["decision"]) for e in events] == [("git_guard_ask", "ask")], cmd
        assert token.read_text() == before, cmd


def test_git_guard_ask_mode_asks_for_every_pair_of_keys(tmp_path):
    # A chain is never one plain push, so no pair defers, `push && push` included.
    cases = {**ASK_CASES, "push": PUSH_CASE}
    assert set(cases) == set(git_guard.PRIORITY)
    data = git_guard_mode_data(tmp_path, "ask")
    env = {"CLAUDE_PLUGIN_DATA": str(data)}
    for a, cmd_a in cases.items():
        for b, cmd_b in cases.items():
            cmd = cmd_a + " && " + cmd_b
            proj = tmp_path / f"pair-{a}-{b}"
            (proj / ".cc10x").mkdir(parents=True)
            code, out = run_git_guard_in_process(proj, cmd, extra_env=env)
            assert code == 0, (a, b)
            events = [(e["event"], e["decision"]) for e in git_guard_events(proj)]
            decision = json.loads(out)["hookSpecificOutput"]
            assert decision["permissionDecision"] == "ask", (a, b)
            assert events == [("git_guard_ask", "ask")], (a, b)
            assert ask_reason(classify(cmd)) in decision["permissionDecisionReason"], (a, b)


def test_git_guard_block_mode_push_chained_with_branch_delete_is_unchanged(tmp_path):
    # 12.10.0 behavior: denied as push without a token; a push token approves the
    # bundled branch delete (pre-existing, recorded in the 12.10.0 entry).
    data = git_guard_mode_data(tmp_path, "block")
    for i, cmd in enumerate(CHAINED_PUSH_AND_BRANCH_DELETE):
        explicit = run_git_guard_mode(tmp_path / f"explicit-{i}", cmd, data)
        default = run_git_guard_mode(tmp_path / f"default-{i}", cmd, None)
        assert explicit.stdout == default.stdout, cmd
        decision = json.loads(default.stdout)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "deny", cmd
        assert decision["permissionDecisionReason"].startswith(
            "cc10x git guardrails blocked: git push — pushing to remote."
        ), cmd
        assert [(e["event"], e["decision"]) for e in git_guard_events(tmp_path / f"default-{i}")] == [
            ("git_guard_blocked", "deny")
        ], cmd
        proj = tmp_path / f"token-{i}"
        token = write_git_token(proj, ["push"], "2099-01-01T00:00:00+00:00")
        r = run_git_guard_mode(proj, cmd, None)
        assert r.returncode == 0 and r.stdout.strip() == "", cmd
        assert not token.exists(), cmd
        assert [(e["event"], e["decision"]) for e in git_guard_events(proj)] == [
            ("git_guard_token_consumed", "allow")
        ], cmd


def test_git_guard_ask_mode_classifier_crash_asks(tmp_path):
    # A push whose found set cannot be computed must not defer, and any other
    # git text asks too.
    data = git_guard_mode_data(tmp_path, "ask")
    patches = [(git_guard, "classify_git_command", _boom)]
    env = {"CLAUDE_PLUGIN_DATA": str(data), "CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT)}
    for i, cmd in enumerate((PUSH_CASE, git("status"))):
        proj = tmp_path / f"proj-{i}"
        (proj / ".cc10x").mkdir(parents=True)
        code, out = run_git_guard_in_process(proj, cmd, patches, extra_env=env)
        assert code == 0, cmd
        decision = json.loads(out)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "ask", cmd
        assert "classifier" in decision["permissionDecisionReason"], cmd
        # PP-G: git_guard_ask is the single decision event; the failure event
        # still records the crash but carries no decision of its own.
        events = git_guard_events(proj)
        assert [(e["event"], e.get("decision")) for e in events] == [
            ("git_guard_classifier_failed", None),
            ("git_guard_ask", "ask"),
        ], cmd
        assert events[0]["reason"] == "classifier-error" and events[0]["error"] == "RuntimeError"


def test_git_guard_a_crash_while_picking_the_verdict_fails_closed(tmp_path):
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "_pick", _boom)]
    code, out = run_git_guard_in_process(tmp_path, PUSH_CASE, patches)
    assert code == 0
    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert git_guard.MSG_CLASSIFIER_ERROR in decision["permissionDecisionReason"]
    assert [(e["event"], e.get("decision")) for e in git_guard_events(tmp_path)] == [
        ("git_guard_classifier_failed", "deny"),
        ("git_guard_blocked", "deny"),
    ]


def test_git_guard_mode_read_failure_takes_the_block_path(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "load_mode", _boom)]
    code, out = run_git_guard_in_process(
        tmp_path, git("push", "origin", "main"), patches, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
    )
    assert code == 0
    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "approval token (.cc10x/state/git-approval.json)" in decision["permissionDecisionReason"]
    events = git_guard_events(tmp_path)
    assert [(e["event"], e.get("decision")) for e in events] == [
        ("git_guard_mode_read_failed", None),
        ("git_guard_blocked", "deny"),
    ]
    assert "decision" not in events[0] and events[0]["error"] == "RuntimeError"


def test_git_guard_mode_read_failure_with_a_push_token_consumes_it(tmp_path):
    # 12.10.0's block path: a valid push token still releases the push.
    data = git_guard_mode_data(tmp_path, "ask")
    token = write_git_token(tmp_path, ["push"], "2099-01-01T00:00:00+00:00")
    patches = [(git_guard, "load_mode", _boom)]
    code, out = run_git_guard_in_process(
        tmp_path, git("push", "origin", "main"), patches, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
    )
    assert code == 0 and out == ""
    assert not token.exists()
    events = git_guard_events(tmp_path)
    assert [(e["event"], e.get("decision")) for e in events] == [
        ("git_guard_mode_read_failed", None),
        ("git_guard_token_consumed", "allow"),
    ]
    assert "decision" not in events[0] and events[0]["error"] == "RuntimeError"


def test_git_guard_classifier_crash_with_mode_read_failure_blocks(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    (tmp_path / ".cc10x").mkdir()
    patches = [(git_guard, "classify_git_command", _boom), (git_guard, "load_mode", _boom)]
    code, out = run_git_guard_in_process(
        tmp_path, git("status"), patches, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
    )
    assert code == 0
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
    events = git_guard_events(tmp_path)
    assert [(e["event"], e.get("decision")) for e in events] == [
        ("git_guard_classifier_failed", "deny"),
        ("git_guard_mode_read_failed", None),
        ("git_guard_blocked", "deny"),
    ]
    assert "decision" not in events[1]


def test_git_guard_classifier_crash_without_git_word_never_reads_mode(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    (tmp_path / ".cc10x").mkdir()
    reads = []
    patches = [
        (git_guard, "classify_git_command", _boom),
        (git_guard, "load_mode", lambda *a, **k: reads.append(1) or {"gitGuard": "ask"}),
    ]
    code, out = run_git_guard_in_process(
        tmp_path, "ls -la", patches, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
    )
    assert code == 0 and out == ""
    assert reads == []
    assert [(e["event"], e.get("decision")) for e in hook_log_lines(tmp_path)] == [
        ("git_guard_classifier_failed", "allow"),
    ]


def test_git_guard_audit_value_falls_back_to_block(tmp_path):
    data = git_guard_mode_data(tmp_path, "audit")
    proj = tmp_path / "proj"
    r = run_git_guard_mode(proj, git("push", "origin", "main"), data)
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
    invalid = [e for e in hook_log_lines(proj) if e["event"] == "invalid_hook_mode"]
    assert [e["key"] for e in invalid] == ["gitGuard"]


def test_git_guard_explicit_block_mode_matches_no_config(tmp_path):
    data = git_guard_mode_data(tmp_path, "block")
    for i, cmd in enumerate([git("reset", "--hard", "HEAD~1"), git("push", "origin", "main")]):
        explicit = run_git_guard_mode(tmp_path / f"explicit-{i}", cmd, data)
        default = run_git_guard_mode(tmp_path / f"default-{i}", cmd, None)
        assert explicit.stdout != ""
        assert explicit.stdout == default.stdout, cmd


def test_git_guard_ask_mode_ignores_commands_without_a_verdict(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    for i, cmd in enumerate(["ls -la", git("status")]):
        proj = tmp_path / f"proj-{i}"
        r = run_git_guard_mode(proj, cmd, data)
        assert r.returncode == 0 and r.stdout.strip() == "", cmd
        assert git_guard_events(proj) == [], cmd


def test_git_guard_in_process_helper_ignores_ambient_plugin_data(tmp_path):
    data = git_guard_mode_data(tmp_path, "ask")
    (tmp_path / ".cc10x").mkdir()
    cmd = git("reset", "--hard", "HEAD~1")
    with env_patch(CLAUDE_PLUGIN_DATA=str(data)):
        _, out = run_git_guard_in_process(tmp_path, cmd)
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
        _, out = run_git_guard_in_process(
            tmp_path, cmd, extra_env={"CLAUDE_PLUGIN_DATA": str(data)}
        )
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "ask"
        assert os.environ["CLAUDE_PLUGIN_DATA"] == str(data)


def test_git_guard_floor_tables_stay_aligned(tmp_path):
    assert len(git_guard.BLOCKED_PATTERNS) == len(git_guard.FLOOR_KEYS)
    for (pattern, _reason, operation), key in zip(
        git_guard.BLOCKED_PATTERNS, git_guard.FLOOR_KEYS
    ):
        assert git_guard.APPROVABLE.get(key) == operation, (pattern, key)
        assert key in git_guard.PRIORITY, key


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
            (
                "cc10x_qa_isolation_guard.py",
                {"tool_name": "Write", "tool_input": {"file_path": "a.txt"}},
                [],
            ),
            (
                "cc10x_pretooluse_guard.py",
                {"tool_name": "Write", "tool_input": {"file_path": str(proj / ".cc10x" / "patterns.md")}},
                [],
            ),
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


def test_unhashable_phase_fields_never_crash_the_qa_guard_or_sessionstart(tmp_path):
    shapes = (
        {"phase_cursor": ["qa-plan"]},
        {"phase_cursor": {"a": 1}},
        {"phase_cursor": None, "status_history": [{"phase": ["qa-plan"]}]},
        {"phase_cursor": None, "status_history": [{"phase": {"a": 1}}]},
        {"phase_cursor": ["x"], "phase_status": {"a": ["in_progress"]}},
    )
    for index, fields in enumerate(shapes):
        proj = tmp_path / f"p{index}"
        write_artifact(proj, "wf-odd", workflow_type="QA", **fields)
        for script, payload in (
            ("cc10x_qa_isolation_guard.py", {"tool_name": "Bash", "tool_input": {"command": "mkdir x"}}),
            ("cc10x_qa_isolation_guard.py", {"tool_name": "Write", "tool_input": {"file_path": "a.txt"}}),
            ("cc10x_sessionstart_context.py", {"source": "resume"}),
            ("cc10x_pretooluse_guard.py", {"tool_name": "Write", "tool_input": {"file_path": str(proj / ".cc10x" / "patterns.md")}}),
        ):
            r = run_guard(script, payload, proj)
            assert r.returncode in (0, 2), (fields, script, r.stderr[-300:])
            assert "Traceback" not in r.stderr, (fields, script, r.stderr[-300:])


def test_a_stray_non_workflow_json_is_never_the_newest_artifact(tmp_path):
    qa_workflow(tmp_path, "wf-a1", 3000)
    stray = tmp_path / ".cc10x" / "workflows" / "settings.json"
    stray.write_text('{"unrelated": true}')
    set_age(stray, 10)
    assert qa_guard_decisions(tmp_path)["write"] == "deny"
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
    override.write_text('{"artifactIntegrity": "Audit", "memoryWrites": "nope"}')
    for _ in range(3):
        assert _run_write_guard(tmp_path, env).returncode == 0
    assert len(invalid_mode_events(tmp_path)) == 3


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


def test_the_task_guard_logs_an_unsafe_workflow_id_instead_of_going_silent(tmp_path):
    (tmp_path / ".cc10x" / "workflows").mkdir(parents=True)
    for kind in ("agent", "remfix"):
        before = len(hook_log_lines(tmp_path))
        r = run_guard(
            "cc10x_task_completed_guard.py",
            {
                "task_subject": "CC10X component-builder: x",
                "task_description": CC10X_METADATA.replace("wf:wf-test", "wf:../../x").replace(
                    "kind:agent", f"kind:{kind}"
                ),
                "task_id": "t1",
            },
            tmp_path,
        )
        assert r.returncode == 0, r.stderr
        events = [
            e for e in hook_log_lines(tmp_path)[before:] if e["event"] == "workflow_id_unsafe"
        ]
        expected = {"freshness-not-checked"}
        if kind == "remfix":
            expected.add("circuit-breaker-not-checked")
        assert {e["reason"] for e in events} == expected, kind
        assert all(e["source"] == "task_completed_guard" for e in events)


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


# --- P5 remediation 3: git guard -----------------------------------------------

G3 = "g" + "it"


def glued_quote_corpus() -> dict[str, str]:
    commands = (
        'echo "x"' + G3 + " push",
        "echo " + G3 + ' push"x"',
        "echo " + G3 + ' clean -f"d"',
        "printf " + G3 + ' branch -D"x"',
        "grep -r " + G3 + ' push"origin" --force',
        "echo -e " + G3 + " clean -f'd'",
    )
    return {command: "glued-quote" for command in commands}


def test_quoted_region_glued_to_unquoted_destructive_text_is_denied(tmp_path):
    corpus = glued_quote_corpus()
    assert len(corpus) == 6
    for command in corpus:
        assert legacy_denies(command), f"legacy must deny {command!r}"
        assert classify(command) is not None, f"allowed: {command!r}"
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": 'echo "x"' + G3 + " push"}},
        tmp_path,
    )
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert classify('echo "' + G3 + ' push"') is None
    assert classify("echo 'a' \"b\" c") is None


GIT_VALUE_FLAG_FORMS = (
    "-C", "--git-dir", "--work-tree", "--namespace", "--super-prefix",
    "--config-env", "--attr-source",
)


def test_every_git_global_option_with_a_separate_value_is_skipped(tmp_path):
    for flag in GIT_VALUE_FLAG_FORMS:
        for words in (("push", "origin", "main"), ("reset", "--hard"), ("clean", "-fd")):
            command = git(flag, "HEAD", *words)
            assert classify(command) is not None, f"allowed: {command!r}"
        assert classify(git(flag, "HEAD", "status")) is None, flag
    assert set(GIT_VALUE_FLAG_FORMS) <= git_guard.GIT_VALUE_FLAGS


def test_env_split_string_argument_is_scanned_as_a_script(tmp_path):
    denied = (
        'env "-S' + G3 + ' push"',
        "env -S \"g'i't push\"",
        'env -i "-S' + G3 + ' reset --hard"',
        'env -S"' + G3 + ' push"',
        'env -S "' + G3 + ' clean -fd"',
        'env --split-string="' + G3 + ' push"',
        "env --split-string '" + G3 + " reset --hard'",
        'env -iS"' + G3 + ' push"',
        "sudo env -S '" + G3 + " push'",
    )
    for command in denied:
        assert classify(command) is not None, f"allowed: {command!r}"
    for command in (
        'env -S "ls -la"',
        'env -S"' + G3 + ' status"',
        "env -u HOME " + G3 + " status",
        "env -i ls",
    ):
        assert classify(command) is None, f"denied: {command!r}"


def _large_command(chars: int, word: str) -> str:
    return "echo " + (word + " ") * (chars // (len(word) + 1))


def test_commands_over_64k_that_name_git_are_denied_without_the_regex_floor(tmp_path):
    started = time.monotonic()
    big = _large_command(70_000, G3 + " push")
    result = classify(big)
    assert result is not None and result[0] == "command-too-large", result
    assert "too large" in result[1]
    assert time.monotonic() - started < 1.0
    assert classify(_large_command(70_000, "ls")) is None
    assert classify(_large_command(70_000, "digit")) is None
    just_under = _large_command(60_000, G3 + " status") + G3 + " push origin"
    started = time.monotonic()
    result = classify(just_under)
    assert result is not None and result[0] == "push", result
    assert time.monotonic() - started < 2.0
    assert classify(_large_command(60_000, G3 + " status")) is None
    r = run_guard(
        "cc10x_git_guard.py", {"tool_input": {"command": big}}, tmp_path
    )
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_command_too_large_is_never_token_approvable(tmp_path):
    assert git_guard.APPROVABLE.get("command-too-large") is None
    assert "command-too-large" in git_guard.PRIORITY


def test_built_git_command_and_subcommand_words_are_denied(tmp_path):
    denied = (
        G3 + " {push,} origin",
        G3 + " pu{sh,} origin",
        "{" + G3 + ",} push origin",
        "{" + G3 + ",} reset --hard",
        "/usr/bin/gi? push origin",
        "/usr/bin/gi[t] push origin",
        "/usr/bin/g* reset --hard",
        G3 + " pu* origin",
        G3 + " pus? origin",
        G3 + " re[s]et --hard",
        G3 + " cl{ean,} -fd",
        "$(echo " + G3 + ") push origin",
        '"$(which ' + G3 + ')" push origin',
        "`echo " + G3 + "` push origin",
        "env {" + G3 + ",} push origin",
        G3 + " $(echo push) origin",
        G3 + " -C . {push,}",
    )
    for command in denied:
        assert classify(command) is not None, f"allowed: {command!r}"
    allowed = (
        G3 + " status",
        G3 + " log --oneline {a,b}",
        G3 + " show $(" + G3 + " rev-parse HEAD)",
        G3 + ' commit -m "$(cat msg)"',
        G3 + ' -C "$(' + G3 + " rev-parse --show-toplevel)\" status",
        "ls /usr/bin/gi?",
        "echo {a,b} " + G3,
        "grep -r 'gi?' docs",
        "$HOME/bin/tool push",
        "${DOCKER} push image",
    )
    for command in allowed:
        assert classify(command) is None, f"denied: {command!r}"


def test_a_built_git_word_obeys_the_approval_token_like_a_literal_one(tmp_path):
    assert classify(G3 + " pu{sh,} origin")[0] == "classifier-error"
    assert classify("{" + G3 + ",} push origin")[0] == "push"


def test_documented_nesting_figures_are_the_real_ones(tmp_path):
    assert git_guard.MAX_DEPTH == 8
    assert classify(nested_substitution(8, "ls")) is None
    assert classify(nested_substitution(9, "ls"))[0] == "classifier-error"

    def quoted_levels(levels: int) -> str:
        command = "ls"
        for _ in range(levels):
            command = 'echo "$(' + command + ')"'
        return command

    assert classify(quoted_levels(4)) is None
    assert classify(quoted_levels(5))[0] == "classifier-error"
    readme = (PLUGIN_ROOT / "hooks" / "README.md").read_text()
    assert "8 levels" in readme and "four" in readme


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
    assert len(argvs) == 13
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
        "cc10x_pretooluse_guard.py": newest,
        "cc10x_qa_isolation_guard.py": newest,
        "cc10x_posttooluse_artifact_guard.py": newest,
        "cc10x_event_logger.py": newest,
        "cc10x_sessionstart_context.py": live,
        "cc10x_state_persist.py": live,
    }
    for script, family in by_script.items():
        called = hooklib_functions_called(script)
        assert called & family, (script, called)
        assert not called & ((newest | live) - family), (script, called)
    assert not hooklib_functions_called("cc10x_task_completed_guard.py") & (newest | live)


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
                # Resolve: macOS tempdirs are symlinked (/var -> /private/var);
                # the memory guard compares resolved-vs-unresolved paths, so an
                # unresolved project dir would trip the known T8 bypass bug.
                # The baseline exercises intended behavior; T8 adds the
                # symlinked-repro test alongside the fix.
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
