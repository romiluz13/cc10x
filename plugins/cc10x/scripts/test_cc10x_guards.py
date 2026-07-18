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
