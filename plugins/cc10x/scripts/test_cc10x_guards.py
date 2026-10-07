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

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent


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


def test_sessionstart_silent_on_corrupt_artifact(tmp_path):
    # Violation path (also locks cc10x_hooklib.read_latest_workflow_state's
    # never-raise contract): a corrupt artifact yields no context injection.
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "wf-corrupt.json").write_text("{not json")
    r = run_guard("cc10x_sessionstart_context.py", {"source": "startup"}, tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""


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
    wt = make_checkout(tmp_path / "wt", kind="file")
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


def test_state_root_uses_the_nearest_git_entry_file_or_directory(tmp_path):
    outer = make_checkout(tmp_path / "outer")
    write_artifact(outer, "wf-outer")
    wt = make_checkout(outer / "wt", kind="file")  # no .cc10x of its own
    cwd = wt / "x"
    cwd.mkdir()
    proj = tmp_path / "proj"
    write_artifact(proj, "wf-proj")
    # The worktree's .git FILE ends the walk: the outer checkout's .cc10x is
    # not an ancestor to borrow, so resolution falls to CLAUDE_PROJECT_DIR.
    assert sessionstart_wf(proj, cwd) == "wf-proj"
    # The same layout with a .git DIRECTORY at the worktree root selects it.
    (wt / ".git").unlink()
    (wt / ".git").mkdir()
    write_artifact(wt, "wf-wt")
    assert sessionstart_wf(proj, cwd) == "wf-wt"


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
        {"agent_transcript_path": str(tmp_path / "missing.jsonl")},
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


DEFAULT_MODES = {"artifactIntegrity": "block", "memoryWrites": "audit", "taskMetadata": "audit"}


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
    assert modes == {"artifactIntegrity": "block", "memoryWrites": "block", "taskMetadata": "audit"}
    assert sorted(e["key"] for e in events) == ["artifactIntegrity", "taskMetadata"]


def test_load_mode_partial_file_keeps_defaults_for_missing_keys(tmp_path):
    modes, events = resolved_mode(tmp_path, {"taskMetadata": "block"})
    assert modes == {"artifactIntegrity": "block", "memoryWrites": "audit", "taskMetadata": "block"}
    assert events == []


def test_load_mode_user_override_wins_over_the_shipped_file(tmp_path):
    modes, events = resolved_mode(
        tmp_path,
        {"artifactIntegrity": "block", "memoryWrites": "block"},
        override={"artifactIntegrity": "audit", "taskMetadata": "block", "extra": "block"},
    )
    assert modes == {"artifactIntegrity": "audit", "memoryWrites": "block", "taskMetadata": "block"}
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


def test_load_mode_never_raises_and_always_returns_the_three_keys(tmp_path):
    for bad in ('[]', '"block"', "null", "7", '{"artifactIntegrity": ["block"]}'):
        modes, _ = resolved_mode(tmp_path / f"c{abs(hash(bad))}", bad)
        assert modes == DEFAULT_MODES, bad
    unreadable = tmp_path / "dirfile"
    (unreadable / "config").mkdir(parents=True)
    (unreadable / "config" / "hook-mode.json").mkdir()  # a directory, not a file
    with env_patch(CLAUDE_PLUGIN_ROOT=str(unreadable), CLAUDE_PLUGIN_DATA=None):
        assert load_hooklib().load_mode() == DEFAULT_MODES
    # An unreadable data dir: Path.exists() raises PermissionError on Python 3.9.
    locked = tmp_path / "locked"
    locked.mkdir()
    (locked / "hook-mode.json").write_text("{}")
    locked.chmod(0)
    try:
        with env_patch(CLAUDE_PLUGIN_ROOT=str(unreadable), CLAUDE_PLUGIN_DATA=str(locked)):
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
        live = write_artifact(tmp_path, "wf-live")
        done = write_artifact(
            tmp_path,
            "wf-done",
            status_history=[{"event": "started"}, {"event": event}],
        )
        set_age(live, 300)
        set_age(done, 10)  # the finished one is the newest by mtime
        assert sessionstart_wf(tmp_path, None) == "wf-live", event


def test_a_workflow_that_resumed_after_a_terminal_event_is_live(tmp_path):
    live = write_artifact(tmp_path, "wf-live")
    resumed = write_artifact(
        tmp_path,
        "wf-resumed",
        status_history=[{"event": "memory_finalized"}, {"event": "resumed"}],
    )
    set_age(live, 300)
    set_age(resumed, 10)
    assert sessionstart_wf(tmp_path, None) == "wf-resumed"


def test_a_finalizing_workflow_without_the_finalized_event_is_still_live(tmp_path):
    write_artifact(
        tmp_path,
        "wf-fin",
        phase_cursor="memory-finalize",
        status_history=[{"event": "started"}],
    )
    assert sessionstart_wf(tmp_path, None) == "wf-fin"


def test_only_finished_workflows_means_no_resume_context(tmp_path):
    write_artifact(
        tmp_path, "wf-done", status_history=[{"event": "memory_finalized"}]
    )
    assert sessionstart_wf(tmp_path, None) is None


def test_a_corrupt_newest_artifact_is_surfaced_not_skipped_by_latest_selection(tmp_path):
    live = write_artifact(tmp_path, "wf-live")
    corrupt = tmp_path / ".cc10x" / "workflows" / "wf-corrupt.json"
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
    live = write_artifact(tmp_path, "wf-live")
    done = write_artifact(
        tmp_path, "wf-done", status_history=[{"event": "workflow_completed"}]
    )
    set_age(live, 300)
    set_age(done, 10)
    r = run_guard("cc10x_state_persist.py", {}, tmp_path, argv=["stop"])
    assert r.returncode == 0
    snapshot = json.loads((tmp_path / ".cc10x" / "stop-state.json").read_text())
    assert snapshot["workflow_uuid"] == "wf-live"


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
    "cat notes | grep \"{}\" | head -5",
    "grep '{}' f 2>/dev/null",
    "grep -c '{}' f 2>&1 | tail -1",
    "printf '%s\\n' '{}' | sort | uniq -c",
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
        "cat notes | grep \"" + git("clean", "-f") + "\"",
        "sudo grep \"" + git("push") + "\" file",
        "echo '$(" + git("push") + ")'",
        "bash run.sh && grep \"" + git("push") + "\" log.txt",
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


TEXT_FILTERS = ("grep", "egrep", "fgrep", "cat", "head", "tail", "wc", "sort", "uniq", "tr", "cut")


def test_quoted_data_exceptions_are_real_and_narrow(tmp_path):
    assert len(QUOTED_DATA_EXCEPTIONS) > 50
    for command in sorted(QUOTED_DATA_EXCEPTIONS):
        assert command.split()[0] in ("echo", "grep", "printf", "cat"), command
        for member in command.split("|"):
            assert member.split()[0] in ("echo", "printf") + TEXT_FILTERS, command
        stripped = re.sub(r"\d?>(&\d|/dev/null)", "", command)
        assert not re.search(r"[<>]|\$\(|`", stripped), f"redirect or subst: {command!r}"
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


def test_classifier_denies_every_executed_text_shape(tmp_path):
    corpus = {
        template.format(git(*words)): template
        for words in DESTRUCTIVE
        for template in LEXER_TEMPLATES
    }
    corpus.update(pipe_executed_corpus())
    assert len(corpus) > 500
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
    assert classify("echo hi # " + git("push")) is None
    assert classify("echo hi;# " + git("push")) is None
    assert classify("echo a#b && " + git("push")) is not None
    assert classify("$'" + "git" + "' push origin main") is not None
    assert classify("echo $'it\\'s' && " + git("reset", "--hard")) is not None


def test_classifier_denies_quoted_text_spanning_lines(tmp_path):
    command = "echo 'notes\n" + git("push", "origin", "main") + "\nmore'"
    assert classify(command) is not None
    assert classify("echo 'one line " + git("push") + "'") is None


def test_classifier_allows_quoted_text_only_through_text_filter_pipes(tmp_path):
    allowed = [
        "grep -rn \"" + git("push", "origin", "main") + "\" plugins/ 2>/dev/null",
        "cat f | grep '" + git("reset", "--hard") + "' | head -3",
        "grep -c \"" + git("clean", "-fd") + "\" f 2>&1 | tail -1",
        "echo '" + git("push") + "' | wc -l",
    ]
    wrongly_denied = [c for c in allowed if classify(c) is not None]
    assert not wrongly_denied, wrongly_denied
    denied = [
        "grep '" + git("push") + "' f | xargs sh -c",
        "git log | grep '" + git("push") + "'",
        "grep '" + git("push") + "' f > out.sh",
        "echo '" + git("push") + "' <<< x",
    ]
    undenied = [c for c in denied if classify(c) is None]
    assert not undenied, undenied


def run_git_guard_in_process(project_dir: Path, command: str, patches=()):
    import contextlib
    import io
    from unittest import mock

    import cc10x_hooklib

    cc10x_hooklib._input_cwd = None
    stdout = io.StringIO()
    payload = json.dumps({"tool_input": {"command": command}})
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(project_dir)}))
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


def test_git_guard_floor_tables_stay_aligned(tmp_path):
    assert len(git_guard.BLOCKED_PATTERNS) == len(git_guard.FLOOR_KEYS)
    for (pattern, _reason, operation), key in zip(
        git_guard.BLOCKED_PATTERNS, git_guard.FLOOR_KEYS
    ):
        assert git_guard.APPROVABLE.get(key) == operation, (pattern, key)
        assert key in git_guard.PRIORITY, key


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
