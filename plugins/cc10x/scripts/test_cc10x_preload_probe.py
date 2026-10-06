"""Unit tests for tools/preload_probe.py pure functions and failure reporting (no model calls)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import preload_probe  # noqa: E402

PRELOAD = "[Agent: cc10x:{agent}] Preloaded skill 'cc10x:agent-common'"


def make_plugin(tmp_path: Path, agents: dict) -> Path:
    (tmp_path / "agents").mkdir()
    for name, text in agents.items():
        (tmp_path / "agents" / f"{name}.md").write_text(text, encoding="utf-8")
    return tmp_path


def test_judge_passes_on_anchored_preload_line():
    ok, detail = preload_probe.judge(PRELOAD.format(agent="component-builder"), "component-builder")
    assert ok and "agent-common" in detail


def test_judge_rejects_preload_line_from_a_different_agent():
    log = PRELOAD.format(agent="planner")
    ok, detail = preload_probe.judge(log, "component-builder")
    assert not ok and "component-builder" in detail


def test_judge_rejects_unanchored_preload_line():
    ok, _ = preload_probe.judge("Preloaded skill 'cc10x:agent-common'", "component-builder")
    assert not ok


def test_judge_does_not_confuse_agent_name_prefixes():
    log = PRELOAD.format(agent="qa-executor-extra")
    ok, _ = preload_probe.judge(log, "qa-executor")
    assert not ok


def test_judge_fails_on_not_found_warning_even_with_preload_line():
    log = PRELOAD.format(agent="a") + "\nWarning: Skill 'cc10x:agent-common' not found\n"
    ok, detail = preload_probe.judge(log, "a")
    assert not ok and "not found" in detail


def test_judge_fails_on_empty_log():
    assert preload_probe.judge("", "a")[0] is False


def test_agent_names_lists_only_agents_preloading_agent_common(tmp_path):
    plugin = make_plugin(
        tmp_path,
        {
            "with": "---\nname: with\nskills:\n  - cc10x:agent-common\n---\n",
            "without": "---\nname: without\n---\n",
            "nofm": "no frontmatter",
        },
    )
    assert preload_probe.agent_names(plugin) == ["with"]


def test_agent_names_empty_when_agents_dir_missing(tmp_path):
    assert preload_probe.agent_names(tmp_path) == []


def test_all_with_empty_agents_dir_fails(tmp_path, capsys):
    plugin = make_plugin(tmp_path, {})
    assert preload_probe.main(["--all", "--plugin-dir", str(plugin)]) == 1
    assert "no agents" in capsys.readouterr().out


def test_all_with_mistyped_plugin_dir_fails(tmp_path, capsys):
    assert preload_probe.main(["--all", "--plugin-dir", str(tmp_path / "nope")]) == 1
    assert "no agents" in capsys.readouterr().out


def test_all_with_agents_but_none_preloading_fails(tmp_path, capsys):
    plugin = make_plugin(tmp_path, {"a": "---\nname: a\n---\n"})
    assert preload_probe.main(["--all", "--plugin-dir", str(plugin)]) == 1
    assert "no agents" in capsys.readouterr().out


def fake_claude(monkeypatch, log: str, stderr: str, returncode: int):
    monkeypatch.setattr(preload_probe.shutil, "which", lambda name: "/fake/claude")

    def run(cmd, **kwargs):
        Path(cmd[cmd.index("--debug-file") + 1]).write_text(log, encoding="utf-8")
        return subprocess.CompletedProcess(cmd, returncode, stdout="", stderr=stderr)

    monkeypatch.setattr(preload_probe.subprocess, "run", run)


def test_failure_surfaces_stderr_tail_and_exit_status(tmp_path, monkeypatch):
    plugin = make_plugin(tmp_path, {"a": "---\nname: a\n---\n"})
    stderr = "\n".join(f"noise {i}" for i in range(30)) + "\nError: credit balance too low\n"
    fake_claude(monkeypatch, log="no preload here", stderr=stderr, returncode=1)
    ok, detail = preload_probe.probe("a", plugin, "haiku")
    assert not ok
    assert "credit balance too low" in detail
    assert "exit 1" in detail
    assert "noise 0" not in detail


def test_success_does_not_dump_stderr(tmp_path, monkeypatch):
    plugin = make_plugin(tmp_path, {"a": "---\nname: a\n---\n"})
    fake_claude(monkeypatch, log=PRELOAD.format(agent="a"), stderr="harmless", returncode=0)
    ok, detail = preload_probe.probe("a", plugin, "haiku")
    assert ok and "harmless" not in detail


def test_missing_debug_log_still_reports_stderr(tmp_path, monkeypatch):
    plugin = make_plugin(tmp_path, {"a": "---\nname: a\n---\n"})
    monkeypatch.setattr(preload_probe.shutil, "which", lambda name: "/fake/claude")
    monkeypatch.setattr(
        preload_probe.subprocess,
        "run",
        lambda cmd, **kw: subprocess.CompletedProcess(cmd, 2, stdout="", stderr="Invalid API key"),
    )
    ok, detail = preload_probe.probe("a", plugin, "haiku")
    assert not ok and "Invalid API key" in detail and "exit 2" in detail


def test_runs_under_python_OO(tmp_path):
    plugin = make_plugin(tmp_path, {})
    run = subprocess.run(
        [sys.executable, "-OO", str(TOOLS / "preload_probe.py"), "--agent", "ghost", "--plugin-dir", str(plugin)],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1
    assert "unknown agent" in run.stdout
    assert "Traceback" not in run.stderr


def test_stderr_note_does_not_redact_a_root_home(monkeypatch):
    monkeypatch.setattr(preload_probe.Path, "home", classmethod(lambda cls: Path("/")))
    run = subprocess.CompletedProcess([], 1, stdout="", stderr="open /var/log/x failed")
    assert "/var/log/x" in preload_probe.stderr_note(run)


def test_stderr_note_redacts_a_real_home(monkeypatch):
    monkeypatch.setattr(preload_probe.Path, "home", classmethod(lambda cls: Path("/Users/someone")))
    run = subprocess.CompletedProcess([], 1, stdout="", stderr="open /Users/someone/x failed")
    note = preload_probe.stderr_note(run)
    assert "~/x" in note and "someone" not in note


def test_timeout_reports_stderr_tail(tmp_path, monkeypatch):
    plugin = make_plugin(tmp_path, {"a": "---\nname: a\n---\n"})
    monkeypatch.setattr(preload_probe.shutil, "which", lambda name: "/fake/claude")

    def run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 1, stderr=b"rate limited, retrying\n")

    monkeypatch.setattr(preload_probe.subprocess, "run", run)
    ok, detail = preload_probe.probe("a", plugin, "haiku")
    assert not ok and "timed out" in detail and "rate limited, retrying" in detail
