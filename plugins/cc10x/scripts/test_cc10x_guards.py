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
import subprocess
import sys
import tempfile
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
) -> subprocess.CompletedProcess:
    env = {
        "CLAUDE_PROJECT_DIR": str(project_dir),
        "CLAUDE_PLUGIN_ROOT": str(plugin_root or PLUGIN_ROOT),
        "PATH": "/usr/bin:/bin",
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
    # Shipped audit mode: surfaces on stderr but does not block.
    assert r.returncode == 0
    assert "circuit breaker" in r.stderr


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


def test_hooklib_corrupt_mode_config_downgrades_block_to_audit(tmp_path):
    # Baseline lock of cc10x_hooklib.load_mode's fallback: a corrupt
    # hook-mode.json silently drops artifactIntegrity to audit, so a
    # key-missing artifact write that would exit 2 under the shipped
    # config exits 0. (Current behavior; whether it SHOULD fail open is
    # a T8/#73 design question.)
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
    assert r.returncode == 0


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


def test_event_logger_ignores_non_cc10x_subagents(tmp_path):
    r = run_guard(
        "cc10x_event_logger.py",
        {"agent_type": "general-purpose", "last_assistant_message": "done"},
        tmp_path,
        argv=["subagent_stop"],
    )
    assert r.returncode == 0
    assert hook_log_lines(tmp_path) == []


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


def test_task_guard_freshness_compares_against_task_creation(tmp_path):
    # The check warned whenever the artifact mtime was >300s old — pure
    # wall-clock recency. An artifact updated AFTER the task was created is
    # fresh, however long ago that was.
    import os
    import time

    path = write_artifact(tmp_path)
    old = time.time() - 600
    os.utime(path, (old, old))  # updated 10 min ago...
    created = time.strftime(
        "%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(old - 600)
    )  # ...but the task started 20 min ago
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t4",
            "task_created_at": created,
        },
        tmp_path,
    )
    assert r.returncode == 0
    assert "stale" not in r.stderr


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
    import os
    import time

    root = mode_root(tmp_path, {"taskMetadata": "block"})
    path = write_artifact(tmp_path)
    old = time.time() - 600
    os.utime(path, (old, old))
    created = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(old + 300))
    r = run_guard(
        "cc10x_task_completed_guard.py",
        {
            "task_subject": "CC10X component-builder: Execute phase 1",
            "task_description": CC10X_METADATA,
            "task_id": "t6",
            "task_created_at": created,  # task started AFTER the last artifact write
        },
        tmp_path,
        plugin_root=root,
    )
    assert r.returncode == 0
    assert "appears stale" in r.stderr
    events = hook_log_lines(tmp_path)
    assert any(
        e["event"] == "task_completed_stale_artifact" and e["decision"] == "audit"
        for e in events
    )


def test_task_guard_stale_artifact_falls_back_to_300s_window_without_created_at(tmp_path):
    import os
    import time

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
    assert "appears stale" in r.stderr


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


def test_artifact_guard_mode_file_without_the_key_silently_means_audit(tmp_path):
    # Current behavior (P5.T3 changes it): load_mode returns the file verbatim,
    # so a hook-mode.json lacking artifactIntegrity downgrades block to audit.
    root = mode_root(tmp_path, {"memoryWrites": "block"})
    workflows = tmp_path / ".cc10x" / "workflows"
    workflows.mkdir(parents=True)
    bad = workflows / "wf-bad.json"
    bad.write_text(json.dumps({"workflow_uuid": "wf-bad"}))
    r = run_posttool(tmp_path, bad, plugin_root=root)
    assert r.returncode == 0
    assert hook_log_lines(tmp_path)[0]["decision"] == "audit"


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


def test_git_guard_push_token_does_not_cover_branch_delete_but_both_ops_can(tmp_path):
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


def test_git_guard_long_form_force_delete_is_not_blocked_today(tmp_path):
    # Documented current gap: the pattern only matches the short `-D`.
    # P5.T4's classifier deliberately closes it; update this test then.
    r = run_guard(
        "cc10x_git_guard.py",
        {"tool_input": {"command": "git branch --delete --force feature/old"}},
        tmp_path,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""


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
