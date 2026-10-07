"""Hermetic tests for the validator tools, driven through their CLI seam against a temp copy of the tree.

CC10X_REPO_ROOT points a validator at the copy, so a mutation never touches the real repo.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

os.environ.pop("CC10X_REPO_ROOT", None)  # in-process imports below must not inherit a host-set root

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "plugins" / "cc10x" / "tools"
COPIED = ("plugins", "docs", ".claude-plugin", "README.md", "CHANGELOG.md")
FIVE_FILES = (
    "harness_audit.py",
    "doc_consistency_check.py",
    "prompt_clause_assertions.py",
    "workflow_replay_check.py",
    "fixture_registry.py",
)


def make_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for name in COPIED:
        src = REPO / name
        if src.is_dir():
            shutil.copytree(src, root / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, root / name)
    return root


def run_tool(script: str, root: Path | None = None, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "CC10X_REPO_ROOT"}
    if root is not None:
        env["CC10X_REPO_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(TOOLS / script), *args], capture_output=True, text=True, env=env
    )


def rewrite(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not found in {path.name}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_replay_check_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/tests/fixtures/plan-direct.json").unlink()
    assert run_tool("workflow_replay_check.py").returncode == 0
    bad = run_tool("workflow_replay_check.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "plan-direct.json" in bad.stdout + bad.stderr


def test_clause_assertions_read_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / "plugins/cc10x/skills/building/SKILL.md", "seam, one test", "seam, one xxxx")
    assert run_tool("prompt_clause_assertions.py", None, "--allow-no-yaml").returncode == 0
    bad = run_tool("prompt_clause_assertions.py", root, "--allow-no-yaml")
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "building: one-seam-one-test cycle" in bad.stdout


def test_harness_audit_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/tests/fixtures/plan-direct.json").unlink()
    assert run_tool("harness_audit.py").returncode == 0
    bad = run_tool("harness_audit.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "missing replay fixture plan-direct.json" in bad.stderr


def test_doc_consistency_reads_the_overridden_root(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / "README.md", "**Current version:**", "**Current versionx:**")
    assert run_tool("doc_consistency_check.py").returncode == 0
    bad = run_tool("doc_consistency_check.py", root)
    assert bad.returncode != 0, bad.stdout + bad.stderr
    assert "README banner version" in bad.stdout


def test_fixture_registry_plugin_root_follows_the_override(tmp_path):
    root = make_tree(tmp_path)
    code = "import fixture_registry as f; print(f.PLUGIN_ROOT)"
    env = {**os.environ, "CC10X_REPO_ROOT": str(root)}
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=str(TOOLS)
    )
    assert out.returncode == 0, out.stderr
    assert Path(out.stdout.strip()) == root / "plugins" / "cc10x"


@pytest.mark.parametrize("script", FIVE_FILES)
def test_non_repo_root_fails_clearly(script, tmp_path):
    result = run_tool(script, tmp_path)
    assert result.returncode != 0
    assert "CC10X_REPO_ROOT" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("script", FIVE_FILES)
def test_an_empty_repo_root_override_is_an_error_not_a_silent_fallback(script):
    env = {**os.environ, "CC10X_REPO_ROOT": ""}
    result = subprocess.run([sys.executable, str(TOOLS / script)], capture_output=True, text=True, env=env)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "CC10X_REPO_ROOT is set but empty" in result.stderr
    assert "Traceback" not in result.stderr


# --- living-doc checks and the docs-rot ratchet -----------------------------------------------

sys.path.insert(0, str(TOOLS))
import harness_audit  # noqa: E402

BASELINE_REL = "plugins/cc10x/tools/docs_rot_baseline.json"


def load_baseline(root: Path) -> list:
    return json.loads((root / BASELINE_REL).read_text(encoding="utf-8"))["entries"]


def write_baseline(root: Path, entries: list) -> None:
    (root / BASELINE_REL).write_text(json.dumps({"entries": entries}), encoding="utf-8")


def entry(key: str, owner: str = "P6.T2", message: str = "msg") -> dict:
    return {"key": key, "owner": owner, "reason": "test", "message": message}


def baseline_for(root: Path, owner: str = "P6.T2") -> list:
    return [entry(key, owner, message) for key, message in harness_audit.check_living_docs(root).items()]


def drop_section(path: Path, heading: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.index(f"### {heading}\n")
    end = text.find("\n### ", start + 1)
    end = len(text) if end == -1 else end + 1
    path.write_text(text[:start] + text[end:], encoding="utf-8")


BANNER_DOCS = ("router-invariants.md", "prompt-invariants.md", "agent-contract-registry.md", "prompt-surface-inventory.md")


def set_banner(root: Path, version: str, doc: str = "router-invariants.md") -> None:
    """Point the first backticked version in the doc's status-note line at `version`."""
    path = root / "docs" / doc
    text = path.read_text(encoding="utf-8")
    start = text.index("> **Status note:**")
    end = text.index("\n", start)
    line = re.sub(r"`v\d+\.\d+\.\d+`", f"`v{version}`", text[start:end], count=1)
    path.write_text(text[:start] + line + text[end:], encoding="utf-8")


def plugin_version(root: Path) -> str:
    return json.loads((root / "plugins/cc10x/.claude-plugin/plugin.json").read_text())["version"]


def test_real_tree_passes_and_warns_while_the_baseline_is_non_empty():
    result = run_tool("harness_audit.py")
    assert result.returncode == 0, result.stdout + result.stderr
    if load_baseline(REPO):
        assert "WARN" in result.stdout and "baseline" in result.stdout


PLAN = REPO / "docs" / "plans" / "2026-10-06-cc10x-remediation-plan.md"


def test_baseline_entries_are_owned_by_a_p6_task_and_all_still_fail():
    entries = load_baseline(REPO)
    live = harness_audit.check_living_docs()
    for item in entries:
        assert re.fullmatch(r"P6\.T\d+", item["owner"]), item
        assert item["reason"].strip(), item
    assert {e["key"]: e["message"] for e in entries} == live
    if PLAN.exists():
        phase6 = PLAN.read_text(encoding="utf-8").split("## Phase 6:", 1)[1].split("\n## Phase 7:", 1)[0]
        for item in entries:
            assert f"**{item['owner']} " in phase6, item


def test_baselined_banner_rot_is_owned_by_the_doc_rewrite_task():
    expected = {
        "registry-banner-stale:docs/prompt-surface-inventory.md": "P6.T2",
        "registry-banner-stale:docs/agent-contract-registry.md": "P6.T3",
        "registry-banner-stale:docs/prompt-invariants.md": "P6.T4",
        "registry-banner-stale:docs/router-invariants.md": "P6.T4",
    }
    for item in load_baseline(REPO):
        if item["key"] in expected:
            assert item["owner"] == expected[item["key"]], item


def test_a_baselined_failure_that_gets_worse_fails_with_message_drift(tmp_path):
    errors, _ = harness_audit.apply_rot_ratchet({"k:1": "now 14 agents"}, [entry("k:1", message="then 11 agents")])
    assert errors == ["baseline message drifted: k:1 (baseline: 'then 11 agents'; live: 'now 14 agents')"]
    root = make_tree(tmp_path)
    set_guide_count(root, "specialist agents", 11)
    write_baseline(root, baseline_for(root, "P6.T9"))
    assert run_tool("harness_audit.py", root).returncode == 0
    set_guide_count(root, "specialist agents", 3)
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "baseline message drifted: guide-agent-count" in result.stderr


def test_ratchet_rejects_duplicate_keys_bad_owners_and_missing_messages():
    errors, _ = harness_audit.apply_rot_ratchet(
        {"a:1": "x"}, [entry("a:1", message="x"), entry("a:1", message="x")]
    )
    assert any("duplicate baseline key: a:1" in e for e in errors)
    for owner in ("P6.T", "P7.T1", "P6.T2b", "later", " P6.T2"):
        errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [entry("a:1", owner, "x")])
        assert any("owner" in e and "P6.T<n>" in e for e in errors), owner
    bare = {"key": "a:1", "owner": "P6.T2", "reason": "r"}
    errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [bare])
    assert any("message" in e for e in errors)


@pytest.mark.parametrize(
    "content",
    ["{not json", "[]", '{"entries": "x"}', '{"entries": [1]}', '{"entries": [{"key": 3}]}', None],
)
def test_a_malformed_or_missing_baseline_is_a_clear_error_not_a_traceback(content, tmp_path):
    root = make_tree(tmp_path)
    if content is None:
        (root / BASELINE_REL).unlink()
    else:
        (root / BASELINE_REL).write_text(content, encoding="utf-8")
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "docs rot baseline" in result.stderr
    assert "Traceback" not in result.stderr


def test_phantom_registry_row_is_a_new_failure(tmp_path):
    root = make_tree(tmp_path)
    registry = root / "docs" / "agent-contract-registry.md"
    rewrite(registry, "## Read-Only Review Agents", "| `ghost-agent` | YAML | `PASS` | x | `MEMORY_NOTES` |\n\n## Read-Only Review Agents")
    assert "registry-phantom-row:ghost-agent" in harness_audit.check_living_docs(root)
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "new rot: registry-phantom-row:ghost-agent" in result.stderr


def test_deleted_inventory_entry_is_a_new_failure(tmp_path):
    root = make_tree(tmp_path)
    drop_section(root / "docs" / "prompt-surface-inventory.md", "mcp-cli")
    assert "inventory-missing-entry:mcp-cli" in harness_audit.check_living_docs(root)
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "new rot: inventory-missing-entry:mcp-cli" in result.stderr


def test_unresolved_inventory_path_is_a_new_failure(tmp_path):
    root = make_tree(tmp_path)
    rewrite(
        root / "docs" / "prompt-surface-inventory.md",
        "`plugins/cc10x/agents/planner.md`",
        "`plugins/cc10x/agents/planner-gone.md`",
    )
    assert "inventory-path:plugins/cc10x/agents/planner-gone.md" in harness_audit.check_living_docs(root)


def test_agent_missing_from_the_registry_is_a_new_failure(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / "docs" / "agent-contract-registry.md", "| `planner` |", "| `planner-renamed` |")
    found = harness_audit.check_living_docs(root)
    assert "registry-missing-row:planner" in found
    assert "registry-phantom-row:planner-renamed" in found


@pytest.mark.parametrize("doc", BANNER_DOCS)
def test_stale_product_line_banner_is_detected_and_a_current_one_is_not(doc, tmp_path):
    root = make_tree(tmp_path)
    key = f"registry-banner-stale:docs/{doc}"
    set_banner(root, "11.0.0", doc)
    assert key in harness_audit.check_living_docs(root)
    set_banner(root, plugin_version(root), doc)
    assert key not in harness_audit.check_living_docs(root)
    set_banner(root, "12.0.0", doc)
    assert key in harness_audit.check_living_docs(root)


@pytest.mark.parametrize("doc", BANNER_DOCS)
def test_a_banner_that_cannot_be_parsed_is_a_failure_not_a_skip(doc, tmp_path):
    root = make_tree(tmp_path)
    path = root / "docs" / doc
    rewrite(path, "> **Status note:**", "> **Note:**")
    assert f"registry-banner-unparseable:docs/{doc}" in harness_audit.check_living_docs(root)


@pytest.mark.parametrize("doc", ("router-invariants.md", "prompt-invariants.md"))
def test_a_missing_banner_doc_is_a_failure_not_a_skip(doc, tmp_path):
    root = make_tree(tmp_path)
    (root / "docs" / doc).unlink()
    assert f"registry-banner-unparseable:docs/{doc}" in harness_audit.check_living_docs(root)


def test_a_fixed_baseline_entry_must_be_removed(tmp_path):
    root = make_tree(tmp_path)
    key = "registry-banner-stale:docs/router-invariants.md"
    set_banner(root, "11.0.0")
    write_baseline(root, baseline_for(root, "P6.T4"))
    assert run_tool("harness_audit.py", root).returncode == 0
    set_banner(root, plugin_version(root))
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "stale baseline entry" in result.stderr
    assert key in result.stderr


def test_re_added_disable_model_invocation_on_agent_common_fails(tmp_path):
    root = make_tree(tmp_path)
    skill = root / "plugins/cc10x/skills/agent-common/SKILL.md"
    rewrite(skill, "user-invocable: false", "user-invocable: false\ndisable-model-invocation: true")
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "preloads agent-common, which sets disable-model-invocation: true" in result.stderr


def test_the_brainstorming_entry_is_no_longer_hard_coded(tmp_path):
    root = make_tree(tmp_path)
    inventory = root / "docs" / "prompt-surface-inventory.md"
    inventory.write_text(inventory.read_text(encoding="utf-8").replace("### brainstorming\n", "### exploration\n"), encoding="utf-8")
    result = run_tool("harness_audit.py", root)
    assert "missing required entry ### brainstorming" not in result.stderr


def test_ratchet_a_failure_outside_the_baseline_is_an_error():
    errors, _ = harness_audit.apply_rot_ratchet({"k:new": "boom"}, [])
    assert errors == ["new rot: k:new: boom"]


def test_ratchet_a_baseline_key_that_no_longer_fails_is_an_error():
    errors, _ = harness_audit.apply_rot_ratchet({}, [entry("k:old")])
    assert len(errors) == 1 and "stale baseline entry" in errors[0] and "k:old" in errors[0]


def test_ratchet_a_non_empty_baseline_warns_with_count_and_owners():
    errors, warnings = harness_audit.apply_rot_ratchet(
        {"a:1": "x", "b:2": "y", "c:3": "z"},
        [entry("a:1", "P6.T2", "x"), entry("b:2", "P6.T2", "y"), entry("c:3", "P6.T3", "z")],
    )
    assert errors == []
    assert len(warnings) == 1
    assert "3" in warnings[0] and "P6.T2" in warnings[0] and "P6.T3" in warnings[0]


def test_ratchet_strict_fails_on_any_baseline_entry():
    errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [entry("a:1", message="x")], strict=True)
    assert errors and "--strict" in errors[0]
    assert harness_audit.apply_rot_ratchet({}, [], strict=True) == ([], [])


def test_ratchet_an_entry_without_an_owner_is_an_error():
    errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [{"key": "a:1", "reason": "r"}])
    assert any("owner" in e for e in errors)


def ghost_tree_with_matching_baseline(tmp_path: Path) -> Path:
    root = make_tree(tmp_path)
    registry = root / "docs" / "agent-contract-registry.md"
    rewrite(registry, "## Read-Only Review Agents", "| `ghost-agent` | YAML | `PASS` | x | `MEMORY_NOTES` |\n\n## Read-Only Review Agents")
    write_baseline(root, baseline_for(root))
    return root


def test_harness_audit_strict_fails_on_a_non_empty_baseline(tmp_path):
    root = ghost_tree_with_matching_baseline(tmp_path)
    assert run_tool("harness_audit.py", root).returncode == 0
    strict = run_tool("harness_audit.py", root, "--strict")
    assert strict.returncode == 1
    assert "--strict" in strict.stderr


def test_harness_audit_rejects_unknown_arguments():
    result = run_tool("harness_audit.py", None, "--bogus")
    assert result.returncode == 2
    assert "--bogus" in result.stderr


def test_release_gate_strict_is_forwarded_to_harness_audit(tmp_path):
    root = ghost_tree_with_matching_baseline(tmp_path)
    gate = REPO / "plugins" / "cc10x" / "tools" / "release_gate.py"
    env = {**os.environ, "CC10X_REPO_ROOT": str(root)}

    def gate_run(*extra):
        return subprocess.run(
            [sys.executable, str(gate), "--only", "harness_audit", *extra], capture_output=True, text=True, env=env
        )

    assert gate_run().returncode == 0
    strict = gate_run("--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "RELEASE GATE: FAIL (harness_audit)" in strict.stdout


# --- hook registration derived from hooks.json ------------------------------------------------

HOOKS_REL = "plugins/cc10x/hooks/hooks.json"


def test_hook_registration_passes_on_the_real_tree():
    assert harness_audit.check_hook_registration() == []


def test_a_removed_hook_script_is_named(tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/scripts/cc10x_state_persist.py").unlink()
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "hooks.json references missing script cc10x_state_persist.py" in result.stderr


def test_a_dropped_qa_isolation_registration_is_named(tmp_path):
    root = make_tree(tmp_path)
    hooks = json.loads((root / HOOKS_REL).read_text(encoding="utf-8"))
    hooks["hooks"]["PreToolUse"] = [
        group
        for group in hooks["hooks"]["PreToolUse"]
        if "cc10x_qa_isolation_guard.py" not in json.dumps(group)
    ]
    (root / HOOKS_REL).write_text(json.dumps(hooks), encoding="utf-8")
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "hooks.json does not register cc10x_qa_isolation_guard.py" in result.stderr


def test_a_dropped_preflight_and_git_guard_registration_are_named(tmp_path):
    root = make_tree(tmp_path)
    text = (root / HOOKS_REL).read_text(encoding="utf-8")
    text = text.replace("cc10x_preflight.sh", "cc10x_state_persist.py").replace("cc10x_git_guard.py", "cc10x_state_persist.py")
    (root / HOOKS_REL).write_text(text, encoding="utf-8")
    stderr = run_tool("harness_audit.py", root).stderr
    assert "hooks.json does not register cc10x_preflight.sh" in stderr
    assert "hooks.json does not register cc10x_git_guard.py" in stderr


def edit_hooks(root: Path, mutate) -> None:
    edit_json(root / HOOKS_REL, mutate)


def drop_hook_script(data: dict, script: str) -> None:
    for event, groups in data["hooks"].items():
        for group in groups:
            group["hooks"] = [h for h in group["hooks"] if script not in h["command"]]


@pytest.mark.parametrize(
    "script",
    [
        "cc10x_pretooluse_guard.py",
        "cc10x_posttooluse_artifact_guard.py",
        "cc10x_sessionstart_context.py",
        "cc10x_task_completed_guard.py",
        "cc10x_event_logger.py",
        "cc10x_state_persist.py",
    ],
)
def test_dropping_any_registered_core_hook_script_is_named(script, tmp_path):
    root = make_tree(tmp_path)
    edit_hooks(root, lambda d: drop_hook_script(d, script))
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"hooks.json does not register {script}" in result.stderr


def test_an_emptied_task_completed_hook_list_is_named(tmp_path):
    root = make_tree(tmp_path)
    edit_hooks(root, lambda d: d["hooks"]["TaskCompleted"][0].update(hooks=[]))
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "hooks.json event TaskCompleted registers no hook command" in result.stderr
    assert "hooks.json does not register cc10x_task_completed_guard.py" in result.stderr


def test_an_event_with_no_groups_registers_no_command(tmp_path):
    root = make_tree(tmp_path)
    edit_hooks(root, lambda d: d["hooks"].update(Stop=[]))
    errors = harness_audit.check_hook_registration(root / "plugins" / "cc10x")
    assert "hooks.json event Stop registers no hook command" in errors


def test_a_hook_script_on_disk_but_not_registered_is_named(tmp_path):
    root = make_tree(tmp_path)
    scripts = root / "plugins/cc10x/scripts"
    (scripts / "cc10x_newhook.py").write_text('if __name__ == "__main__":\n    pass\n', encoding="utf-8")
    (scripts / "cc10x_newhook.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    (scripts / "cc10x_helperlib.py").write_text("VALUE = 1\n", encoding="utf-8")
    errors = harness_audit.check_hook_registration(root / "plugins" / "cc10x")
    assert "hooks.json does not register cc10x_newhook.py" in errors
    assert "hooks.json does not register cc10x_newhook.sh" in errors
    assert not any("cc10x_helperlib.py" in e for e in errors)


def test_a_script_named_only_in_prose_is_not_registered(tmp_path):
    root = make_tree(tmp_path)

    def mutate(data):
        group = data["hooks"]["PreToolUse"][0]
        group["hooks"][0]["command"] = 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc10x_git_guard.py"'
        group["hooks"][0]["statusMessage"] = "see scripts/cc10x_pretooluse_guard.py"

    edit_hooks(root, mutate)
    errors = harness_audit.check_hook_registration(root / "plugins" / "cc10x")
    assert "hooks.json does not register cc10x_pretooluse_guard.py" in errors


def test_unparseable_hooks_json_is_one_clear_error(tmp_path):
    root = make_tree(tmp_path)
    (root / HOOKS_REL).write_text("{not json", encoding="utf-8")
    errors = harness_audit.check_hook_registration(root / "plugins" / "cc10x")
    assert len(errors) == 1 and errors[0].startswith("hooks.json is not valid JSON")


CORE_SCRIPTS = (
    "cc10x_pretooluse_guard.py",
    "cc10x_git_guard.py",
    "cc10x_qa_isolation_guard.py",
    "cc10x_posttooluse_artifact_guard.py",
    "cc10x_sessionstart_context.py",
    "cc10x_preflight.sh",
    "cc10x_task_completed_guard.py",
    "cc10x_event_logger.py",
    "cc10x_state_persist.py",
)


@pytest.mark.parametrize("script", CORE_SCRIPTS)
def test_the_pinned_floor_catches_a_core_script_deleted_from_disk_and_hooks_json(script, tmp_path):
    root = make_tree(tmp_path)
    (root / "plugins/cc10x/scripts" / script).unlink()
    edit_hooks(root, lambda d: drop_hook_script(d, script))
    errors = harness_audit.check_hook_registration(root / "plugins" / "cc10x")
    assert f"hooks.json does not register {script}" in errors


def hook_errors(root: Path) -> list[str]:
    return harness_audit.check_hook_registration(root / "plugins" / "cc10x")


def first_hook(data: dict, event: str) -> dict:
    return data["hooks"][event][0]["hooks"][0]


@pytest.mark.parametrize(
    "event, mutate, expected",
    [
        ("PostCompact", lambda h: h.update(comand=h.pop("command")), "hooks.json event PostCompact hook has no non-empty string command"),
        ("PostCompact", lambda h: h.update(type="prompt"), "hooks.json event PostCompact hook type is 'prompt', expected 'command'"),
        ("PostCompact", lambda h: h.update(command=7), "hooks.json event PostCompact hook has no non-empty string command"),
        ("PostCompact", lambda h: h.update(command="  "), "hooks.json event PostCompact hook has no non-empty string command"),
        ("PostCompact", lambda h: h.update(command='python3 "${CLAUDE_PLUGIN_ROOT}/scrips/cc10x_event_logger.py" postcompact'), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command="echo scripts/cc10x_event_logger.py"), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command=h["command"] + " || true"), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command=h["command"] + "; true"), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command=h["command"] + " && true"), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command='python3 -c pass'), "hooks.json event PostCompact command is not"),
        ("PostCompact", lambda h: h.update(command=h["command"].replace("python3", "sh")), "hooks.json event PostCompact command runs cc10x_event_logger.py with sh, expected python3"),
        ("PostCompact", lambda h: h.update(command=h["command"].replace("event_logger.py", "nonesuch.py")), "hooks.json references missing script cc10x_nonesuch.py"),
        ("PreCompact", lambda h: h.update(command=h["command"].replace("state_persist", "event_logger")), "hooks.json does not register cc10x_state_persist.py on event PreCompact"),
    ],
)
def test_a_malformed_or_retargeted_hook_entry_is_named(event, mutate, expected, tmp_path):
    root = make_tree(tmp_path)
    edit_hooks(root, lambda d: mutate(first_hook(d, event)))
    errors = hook_errors(root)
    assert any(expected in e for e in errors), errors


@pytest.mark.parametrize("script", ["cc10x_git_guard.py", "cc10x_qa_isolation_guard.py", "cc10x_pretooluse_guard.py"])
def test_a_pretooluse_guard_must_keep_its_matcher(script, tmp_path):
    root = make_tree(tmp_path)

    def drop_matcher(data):
        for group in data["hooks"]["PreToolUse"]:
            if script in json.dumps(group):
                del group["matcher"]

    edit_hooks(root, drop_matcher)
    assert f"hooks.json PreToolUse hook for {script} has no matcher" in hook_errors(root)


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda d: d["hooks"].update(Stop={"hooks": []}), "hooks.json event Stop must be a list of hook groups"),
        (lambda d: d["hooks"].update(Stop=["x"]), "hooks.json event Stop has a group that is not an object with a 'hooks' list"),
        (lambda d: d["hooks"].update(Stop=[{"hooks": "x"}]), "hooks.json event Stop has a group that is not an object with a 'hooks' list"),
        (lambda d: d["hooks"]["Stop"][0].update(hooks=["x"]), "hooks.json event Stop has a hook entry that is not an object"),
        (lambda d: d.update(hooks=[]), "hooks.json top-level 'hooks' must be an object keyed by event"),
    ],
)
def test_malformed_hooks_json_shapes_give_a_clear_error_not_a_traceback(mutate, expected, tmp_path):
    root = make_tree(tmp_path)
    edit_hooks(root, mutate)
    errors = hook_errors(root)
    assert any(expected in e for e in errors), errors
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1 and "Traceback" not in result.stderr, result.stderr


def test_a_top_level_list_or_missing_hooks_json_is_one_clear_error(tmp_path):
    root = make_tree(tmp_path)
    (root / HOOKS_REL).write_text("[]", encoding="utf-8")
    errors = hook_errors(root)
    assert len(errors) == 1 and errors[0].startswith("hooks.json is not valid JSON")
    (root / HOOKS_REL).unlink()
    errors = hook_errors(root)
    assert len(errors) == 1 and errors[0].startswith("hooks.json is not valid JSON")


# --- PyYAML-dependent clause check ------------------------------------------------------------

NO_YAML_RUNNER = (
    "import os, runpy, sys\n"
    "sys.modules['yaml'] = None\n"
    "sys.argv = sys.argv[1:]\n"
    "sys.path.insert(0, os.path.dirname(sys.argv[0]))\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)


def run_clauses_without_yaml(*args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "CC10X_REPO_ROOT"}
    return subprocess.run(
        [sys.executable, "-c", NO_YAML_RUNNER, str(TOOLS / "prompt_clause_assertions.py"), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_missing_pyyaml_fails_with_an_install_hint():
    result = run_clauses_without_yaml()
    assert result.returncode == 1, result.stdout + result.stderr
    assert "PyYAML" in result.stdout and "pip install pyyaml" in result.stdout
    assert "--allow-no-yaml" in result.stdout
    assert "(1 failure(s))" in result.stdout


def test_missing_pyyaml_passes_with_the_explicit_flag():
    result = run_clauses_without_yaml("--allow-no-yaml")
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_skipped_yaml_assertion_is_reported_and_not_counted_as_passed():
    import prompt_clause_assertions

    total = len(prompt_clause_assertions.ASSERTIONS)
    result = run_clauses_without_yaml("--allow-no-yaml")
    assert "SKIPPED-YAML" in result.stdout
    assert f"OK ({total - 1} assertions passed, 1 skipped)" in result.stdout
    assert f"OK ({total} assertions passed)" not in result.stdout


def test_clause_assertions_reject_unknown_arguments():
    result = run_tool("prompt_clause_assertions.py", None, "--bogus")
    assert result.returncode == 2
    assert "--bogus" in result.stderr


# --- count and claim checks (doc_consistency_check) -------------------------------------------

import doc_consistency_check  # noqa: E402

README_REL = "README.md"
GUIDE_REL = "plugins/cc10x/skills/cc10x-guide/SKILL.md"
PLUGIN_JSON_REL = "plugins/cc10x/.claude-plugin/plugin.json"
MARKETPLACE_REL = ".claude-plugin/marketplace.json"


def set_guide_count(root: Path, noun: str, count: int) -> None:
    """Set the guide's `<N> <noun>` claim to `count`, whatever it says today (asserts the claim exists)."""
    path = root / GUIDE_REL
    text = path.read_text(encoding="utf-8")
    new, hits = re.subn(rf"\d+ {re.escape(noun)}", f"{count} {noun}", text, count=1)
    assert hits == 1, f"guide has no '<N> {noun}' claim"
    path.write_text(new, encoding="utf-8")


def disk_counts() -> tuple:
    plugin = REPO / "plugins" / "cc10x"
    agents = len(list((plugin / "agents").glob("*.md")))
    skills = len([p for p in (plugin / "skills").iterdir() if p.is_dir() and p.name != "cc10x-router"])
    return agents, skills


def claims(root: Path = REPO) -> dict:
    return doc_consistency_check.check_claims(root)


def edit_json(path: Path, mutate) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_readme_workflow_count_must_equal_the_router_table(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / README_REL, "<strong>8 workflows</strong>", "<strong>9 workflows</strong>")
    assert "readme-workflow-count" in claims(root)
    assert "readme-workflow-count" not in claims()


def test_router_table_row_count_is_read_from_the_router(tmp_path):
    root = make_tree(tmp_path)
    router = root / "plugins/cc10x/skills/cc10x-router/SKILL.md"
    text = router.read_text(encoding="utf-8")
    router.write_text(re.sub(r"^\| 7 \| CODEBASE-HEALTH .*\n", "", text, count=1, flags=re.M), encoding="utf-8")
    assert "readme-workflow-count" in claims(root)


def test_readme_hook_table_must_equal_the_registered_hook_events(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / README_REL, "| `StopFailure` | Log API failure telemetry asynchronously |\n", "")
    assert "readme-hook-count" in claims(root)
    assert "readme-hook-count" not in claims()


def test_readme_numeric_hook_claim_must_equal_the_registered_hook_events(tmp_path):
    root = make_tree(tmp_path)
    rewrite(root / README_REL, "These hooks are intentionally minimal.", "These 4 hooks are intentionally minimal.")
    assert "readme-hook-count" in claims(root)


def test_guide_counts_must_equal_disk(tmp_path):
    root = make_tree(tmp_path)
    agents, skills = disk_counts()
    set_guide_count(root, "specialist agents", agents)
    set_guide_count(root, "skills", skills)
    fixed = claims(root)
    assert "guide-agent-count" not in fixed and "guide-skill-count" not in fixed
    set_guide_count(root, "specialist agents", agents + 1)
    set_guide_count(root, "skills", skills + 1)
    broken = claims(root)
    assert "guide-agent-count" in broken and "guide-skill-count" in broken


def test_unverifiable_percentage_claims_are_rejected_in_both_manifests(tmp_path):
    root = make_tree(tmp_path)
    edit_json(root / PLUGIN_JSON_REL, lambda d: d.update(description="A plugin. 40% leaner than before."))
    edit_json(root / MARKETPLACE_REL, lambda d: d["plugins"][0].update(description="Now 12 % leaner."))
    found = claims(root)
    assert "manifest-unverifiable-claim:plugin.json" in found
    assert "manifest-unverifiable-claim:marketplace.json" in found
    edit_json(root / PLUGIN_JSON_REL, lambda d: d.update(description="A plugin."))
    assert "manifest-unverifiable-claim:plugin.json" not in claims(root)


def test_manifest_description_and_keywords_must_agree(tmp_path):
    root = make_tree(tmp_path)
    plugin = json.loads((root / PLUGIN_JSON_REL).read_text(encoding="utf-8"))

    def align(data):
        data["plugins"][0]["description"] = plugin["description"]
        data["plugins"][0]["keywords"] = list(reversed(plugin["keywords"]))

    edit_json(root / MARKETPLACE_REL, align)
    found = claims(root)
    assert "manifest-description-mismatch" not in found
    assert "manifest-keywords-mismatch" not in found
    edit_json(root / MARKETPLACE_REL, lambda d: d["plugins"][0]["keywords"].append("extra"))
    assert "manifest-keywords-mismatch" in claims(root)


def test_doc_consistency_fails_on_a_new_claim_failure_and_warns_on_baselined_ones(tmp_path):
    ok = run_tool("doc_consistency_check.py")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    root = make_tree(tmp_path)
    rewrite(root / README_REL, "<strong>8 workflows</strong>", "<strong>9 workflows</strong>")
    bad = run_tool("doc_consistency_check.py", root)
    assert bad.returncode == 1
    assert "readme-workflow-count" in bad.stdout
    assert "guide-agent-count" not in bad.stdout


def test_a_fixed_claim_baseline_entry_must_be_removed_by_harness_audit(tmp_path):
    root = make_tree(tmp_path)
    agents, _ = disk_counts()
    set_guide_count(root, "specialist agents", agents + 3)
    write_baseline(root, baseline_for(root, "P6.T9"))
    assert run_tool("harness_audit.py", root).returncode == 0
    set_guide_count(root, "specialist agents", agents)
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "stale baseline entry" in result.stderr and "guide-agent-count" in result.stderr


def test_doc_consistency_reports_a_missing_baseline_file_clearly(tmp_path):
    root = make_tree(tmp_path)
    (root / BASELINE_REL).unlink()
    result = run_tool("doc_consistency_check.py", root)
    assert result.returncode == 1
    assert "docs rot baseline is missing" in result.stdout
    assert "Traceback" not in result.stderr


def test_the_qa_routing_row_is_pinned(tmp_path):
    root = make_tree(tmp_path)
    assert run_tool("prompt_clause_assertions.py", None, "--allow-no-yaml").returncode == 0
    router = root / "plugins/cc10x/skills/cc10x-router/SKILL.md"
    rewrite(router, "| 5 | QA | test, QA, e2e,", "| 5 | QA | test, e2e,")
    bad = run_tool("prompt_clause_assertions.py", root, "--allow-no-yaml")
    assert bad.returncode == 1
    assert "router routing table: priority-5 QA row" in bad.stdout


def test_a_worsened_baselined_failure_fails_the_standalone_doc_consistency_run(tmp_path):
    root = make_tree(tmp_path)
    set_guide_count(root, "specialist agents", 11)
    write_baseline(root, baseline_for(root, "P6.T9"))
    assert run_tool("doc_consistency_check.py", root).returncode == 0
    set_guide_count(root, "specialist agents", 3)
    result = run_tool("doc_consistency_check.py", root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "baseline message drifted: guide-agent-count" in result.stdout


@pytest.mark.parametrize("content", ["[]", '{"entries": [1]}', '{"entries": "x"}', "{not json"])
def test_doc_consistency_reports_a_malformed_baseline_clearly(content, tmp_path):
    root = make_tree(tmp_path)
    (root / BASELINE_REL).write_text(content, encoding="utf-8")
    result = run_tool("doc_consistency_check.py", root)
    assert result.returncode == 1
    assert "docs rot baseline" in result.stdout
    assert "Traceback" not in result.stderr


def test_there_is_one_baseline_loader():
    import doc_consistency_check

    assert harness_audit.load_rot_baseline is doc_consistency_check.load_rot_baseline


def test_a_plugin_version_bump_does_not_drift_the_baselined_banner_messages(tmp_path):
    root = make_tree(tmp_path)
    edit_json(root / "plugins/cc10x/.claude-plugin/plugin.json", lambda d: d.update(version="12.10.0"))
    live = harness_audit.check_living_docs(root)
    for item in load_baseline(REPO):
        if item["key"].startswith("registry-banner-stale:"):
            assert live[item["key"]] == item["message"], item["key"]
            assert "12.9.1" not in item["message"] and "12.10.0" not in item["message"]


def test_the_suite_ignores_a_poisoned_outer_repo_root():
    env = {**os.environ, "CC10X_REPO_ROOT": "/nonexistent-poisoned-root"}
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(Path(__file__)), "-k", "test_hook_registration_passes_on_the_real_tree"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# --- P3.T2: end-state shape fixtures and the single-artifact mode of the replay checker ---

FIXTURES_REL = "plugins/cc10x/tests/fixtures"
SKELETON = REPO / "plugins/cc10x/skills/cc10x-router/references/workflow-artifact.skeleton.json"


def _drop_task(name):
    return lambda d: d["relevant_tasks"].pop(name)


def _dup_memory_finalized(d):
    d["starting_artifact"]["status_history"].append({"event": "memory_finalized", "ts": "2026-10-07T09:20:00Z", "phase": "memory-finalize"})


def _share_workflow_id(d):
    d["other_artifact"]["workflow_id"] = d["starting_artifact"]["workflow_id"]
    d["other_artifact"]["workflow_uuid"] = d["starting_artifact"]["workflow_id"]


def _pop_remfix_field(field):
    return lambda d: d["agent_outputs"]["remfix_report"].pop(field)


def _empty_remfix_field(field):
    return lambda d: d["agent_outputs"]["remfix_report"].update({field: []})


def _set_remfix_field(field, value):
    return lambda d: d["agent_outputs"]["remfix_report"].update({field: value})


def _drop_adjudication(d):
    d["agent_outputs"].pop("verifier_adjudication")


def _adjudication_empty(d):
    d["agent_outputs"]["verifier_adjudication"].update({"DISPUTE_UPHELD": [], "DISPUTE_REJECTED": []})


def _adjudication_both(d):
    adjudication = d["agent_outputs"]["verifier_adjudication"]
    adjudication["DISPUTE_REJECTED"] = list(adjudication["DISPUTE_UPHELD"])


def _builder_self_adjudicates(d):
    d["agent_outputs"]["remfix_report"]["DISPUTE_UPHELD"] = list(d["agent_outputs"]["remfix_report"]["FINDING_DISPUTED"])


def _remfix_in_progress(d):
    d["relevant_tasks"]["completed_remfix"]["status"] = "in_progress"


def _case(name, mutate):
    def apply(d):
        mutate(next(c for c in d["additional_cases"] if c["name"] == name))

    return apply


def _case_adjudication(name, **fields):
    return _case(name, lambda c: c["verifier_adjudication"].update(fields))


def _case_contract(name, **fields):
    return _case(name, lambda c: c["executor_contract"].update(fields))


def _case_task(name, **fields):
    return _case(name, lambda c: c["task"].update(fields))


def _case_report(name, **fields):
    return _case(name, lambda c: c["remfix_report"].update(fields))


def _case_scenario(case_name, index, **fields):
    return _case(case_name, lambda c: c["executor_contract"]["SCENARIOS"][index].update(fields))


def _case_drop_scenario(name):
    return _case(name, lambda c: c["executor_contract"]["SCENARIOS"].pop())


def _case_set(name, **fields):
    return _case(name, lambda c: c.update(fields))


def _case_pop(name, key):
    return _case(name, lambda c: c.pop(key))


def _case_loop(name, **fields):
    return _case(name, lambda c: c["executor_contract"]["FEEDBACK_LOOP"].update(fields))


def _case_closeout(name, **fields):
    return _case(name, lambda c: c["executor_contract"]["DEBUG_CLOSEOUT"].update(fields))


def _set_expected(**fields):
    return lambda d: d["expected"].update(fields)


def _pop_expected(key):
    return lambda d: d["expected"].pop(key)


def _dispute_only_undispute_one(c):
    c["remfix_report"]["FINDING_DISPUTED"] = c["remfix_report"]["FINDING_DISPUTED"][:1]
    c["remfix_report"]["VERIFY_COMMAND"] = c["remfix_report"]["VERIFY_COMMAND"][:1]
    c["remfix_report"]["VERIFY_OUTPUT"] = c["remfix_report"]["VERIFY_OUTPUT"][:1]
    c["verifier_adjudication"] = {"DISPUTE_UPHELD": [1], "DISPUTE_REJECTED": []}
    c["dispute_outcomes"] = ["finding_dropped: dispute upheld"]


def _dispute_only_drop_contract(c):
    c.pop("executor_contract")


def _memory_blocked_by_early_task_only(d):
    d["relevant_tasks"]["memory_finalize"]["blockedBy"] = ["verifier_phase_1"]


def _memory_blocked_by_last_and_early_task(d):
    d["relevant_tasks"]["memory_finalize"]["blockedBy"] = ["verifier_phase_2", "builder_phase_1"]


def _legacy_phase_id_key(d):
    for phase in d["starting_artifact"]["normalized_phases"]:
        phase["id"] = phase.pop("phase_id")


def _qa_open_isolation(d):
    d["starting_artifact"]["qa"]["isolation"]["plan_phase_readonly"] = False


def _qa_unfinalized(d):
    d["starting_artifact"]["status_history"].pop()


def _foreign_task(d):
    d["relevant_tasks"]["a_builder"]["wf"] = d["other_artifact"]["workflow_id"]


def _qa_foreign_wf(d):
    d["relevant_tasks"]["qa_hunt"]["wf"] = "wf-other"


def _unfinalized_memory(d):
    d["starting_artifact"]["status_history"] = [
        e for e in d["starting_artifact"]["status_history"] if e["event"] != "memory_finalized"
    ]


def _memory_blocked_by_doc_sync(d):
    tasks = d["relevant_tasks"]
    tasks["doc_sync"] = {"wf": tasks["memory_finalize"]["wf"], "phase": "build-doc-sync", "status": "completed", "blockedBy": ["verifier_phase_2"]}
    tasks["memory_finalize"]["blockedBy"] = ["doc_sync"]


def _memory_blocked_by_doc_sync_of_wrong_verifier(d):
    _memory_blocked_by_doc_sync(d)
    d["relevant_tasks"]["doc_sync"]["blockedBy"] = ["verifier_phase_1"]


def _memory_blocked_by_early_doc_sync_only(d):
    _memory_blocked_by_doc_sync(d)
    d["relevant_tasks"]["doc_sync"]["blockedBy"] = ["verifier_phase_1"]
    d["relevant_tasks"]["memory_finalize"]["blockedBy"] = ["doc_sync"]


def _second_memory_task(d):
    d["relevant_tasks"]["memory_finalize_again"] = dict(d["relevant_tasks"]["memory_finalize"])


def _triage_needs_info_with_memory(d):
    d["agent_outputs"]["triage_agent_contract"]["STATUS"] = "NEEDS_INFO"


def _triage_needs_grilling_with_memory(d):
    d["agent_outputs"]["triage_agent_contract"]["NEEDS_GRILLING"] = True


def _health_choice_pending_with_memory(d):
    d["expected"]["candidate_choice"] = "pending"


def _paused_add_memory_task(d):
    tasks = d["relevant_tasks"]
    agent = next(iter(tasks))
    tasks["memory_finalize"] = {"wf": tasks[agent]["wf"], "kind": "memory", "phase": "memory-finalize", "status": "pending", "blockedBy": [agent]}


def _paused_finalized(d):
    art = d["starting_artifact"]
    art["phase_cursor"] = "memory-finalize"
    art["status_history"] = [{"event": "memory_finalized", "phase": "memory-finalize", "ts": "2026-10-07T13:30:00Z"}]


def _paused_no_gate(d):
    d["starting_artifact"]["pending_gate"] = None


def _terminal_keeps_gate(d):
    d["starting_artifact"]["pending_gate"] = "needs_info"


def _paused_drop_notes(d):
    d["starting_artifact"]["memory_notes"] = []


def _paused_drop_one_note(d):
    d["starting_artifact"]["memory_notes"][0]["learnings"] = []


def _resume_drop_boundary(d):
    case = d["cases"][1]
    case["events"] = [e for e in case["events"] if not (e["event"] == "remediation_created" and e["decision"] == "cycle 2")]


def _resume_stale_phase_id(d):
    case = d["cases"][0]
    case["events"][-1]["details"]["phase_id"] = "phase-1"


def _resume_expect_flat_results(d):
    d["cases"][0]["expected_runnable"] = ["build-verify"]


def _resume_stale_slots_empty(d):
    d["starting_artifact"]["results"]["reviewer"] = None


def _resume_boundary_after_results(d):
    case = d["cases"][1]
    boundary = next(e for e in case["events"] if e["event"] == "remediation_created" and e["decision"] == "cycle 2")
    case["events"].remove(boundary)
    case["events"].insert(5, boundary)


def _resume_omit_remfix_result(d):
    case = d["cases"][1]
    last = max(i for i, e in enumerate(case["events"]) if e["agent"] == "component-builder")
    del case["events"][last]


def _resume_no_plan_stale_phase_id(d):
    d["cases"][2]["events"][2]["details"]["phase_id"] = "phase-1"


def _resume_pause_decision_is_terminal(d):
    d["cases"][3]["events"][1]["decision"] = "TRIAGED"


def _resume_drop_pass_two(d):
    del d["cases"][4]["events"][2]


def _resume_grilling_pause_is_terminal(d):
    d["cases"][6]["events"][1]["decision"] = "TRIAGED"


def _resume_candidates_is_a_pause(d):
    d["cases"][5]["events"][1]["decision"] = "NEEDS_INFO"


def _locator_clear_gate(d):
    d["locator_cases"][0]["artifacts"][0]["pending_gate"] = None


def _locator_unterminate(d):
    d["locator_cases"][0]["artifacts"][1]["status_history"] = [{"event": "workflow_started"}]


def _locator_single_paused(d):
    del d["locator_cases"][1]["artifacts"][1]


def _locator_drop_request_match(d):
    d["locator_cases"][3]["request_matches"] = []


def _triage_pause_wrong_gate(d):
    d["starting_artifact"]["pending_gate"] = "needs_grilling"


def _health_pause_wrong_gate(d):
    d["starting_artifact"]["pending_gate"] = "needs_info"


def _advisory_converged(d):
    d["starting_artifact"]["quality"]["convergence_state"] = "converged"


def _advisory_four_remediations(d):
    d["starting_artifact"]["remediation_history"] = [
        {"ts": "2026-10-07T13:00:00Z", "phase": "triage", "reason": "x", "cycle_number": n} for n in range(1, 5)
    ]


def _triage_wontfix_with_grilling(d):
    contract = d["agent_outputs"]["triage_agent_contract"]
    contract["STATUS"] = "WONTFIX"
    contract["NEEDS_GRILLING"] = True


def _builder2_blocked_by_verifier_only(d):
    d["relevant_tasks"]["builder_phase_2"]["blockedBy"] = ["verifier_phase_1"]


def _builder2_unblocked(d):
    d["relevant_tasks"]["builder_phase_2"]["blockedBy"] = []


def _memory_blocked_by_early_doc_sync_with_last(d):
    d["relevant_tasks"]["memory_finalize"]["blockedBy"] = ["doc_sync_phase_2", "doc_sync_phase_1"]


L1_MUTATIONS = [
    ("qa-route-happy-path.json", _drop_task("qa_hunt"), "QA route phases"),
    ("qa-route-happy-path.json", _qa_open_isolation, "plan_phase_readonly"),
    ("qa-route-happy-path.json", _qa_unfinalized, "memory_finalized"),
    ("qa-route-happy-path.json", _qa_foreign_wf, "qa_hunt carries wf"),
    ("remfix-gate.json", _pop_remfix_field("COVERING_TESTS"), "REM-FIX report missing COVERING_TESTS"),
    ("remfix-gate.json", _empty_remfix_field("COVERING_TESTS"), "REM-FIX report empty COVERING_TESTS"),
    ("remfix-gate.json", _pop_remfix_field("TEST_COMMAND"), "REM-FIX report missing TEST_COMMAND"),
    ("remfix-gate.json", _pop_remfix_field("TEST_OUTPUT"), "REM-FIX report missing TEST_OUTPUT"),
    ("remfix-gate.json", _set_remfix_field("COVERING_TESTS", [""]), "blank entry in COVERING_TESTS"),
    ("remfix-gate.json", _set_remfix_field("COVERING_TESTS", [None]), "blank entry in COVERING_TESTS"),
    ("remfix-gate.json", _set_remfix_field("COVERING_TESTS", ["  "]), "blank entry in COVERING_TESTS"),
    ("remfix-gate.json", _set_remfix_field("COVERING_TESTS", "tests/a.py"), "REM-FIX report empty COVERING_TESTS"),
    ("remfix-gate.json", _set_remfix_field("TEST_COMMAND", " "), "REM-FIX report empty TEST_COMMAND"),
    ("remfix-gate.json", _set_remfix_field("TEST_COMMAND", 7), "REM-FIX report empty TEST_COMMAND"),
    ("remfix-gate.json", _set_remfix_field("TEST_OUTPUT", " \n"), "REM-FIX report empty TEST_OUTPUT"),
    ("remfix-gate.json", _set_remfix_field("TEST_OUTPUT", ["x"]), "REM-FIX report empty TEST_OUTPUT"),
    ("remfix-gate.json", _remfix_in_progress, "completed_remfix must be completed"),
    ("remfix-gate.json", _drop_adjudication, "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _adjudication_empty, "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _adjudication_both, "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _builder_self_adjudicates, "DISPUTE_UPHELD is produced by integration-verifier"),
    ("remfix-gate.json", _set_remfix_field("VERIFY_COMMAND", [" "]), "blank entry in VERIFY_COMMAND"),
    ("remfix-gate.json", _set_remfix_field("VERIFY_OUTPUT", []), "must be equal-length lists"),
    ("remfix-gate.json", _case_adjudication("dispute-only", DISPUTE_REJECTED=[]), "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _case_adjudication("dispute-only", DISPUTE_REJECTED=[1, 2]), "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _case_adjudication("dispute-only", DISPUTE_UPHELD=[], DISPUTE_REJECTED=[]), "needs exactly one verifier adjudication"),
    ("remfix-gate.json", _case_adjudication("dispute-only", DISPUTE_REJECTED=[3]), "indexes into FINDING_DISPUTED"),
    ("remfix-gate.json", _case_adjudication("dispute-only", DISPUTE_UPHELD=["F1 (HIGH): save handler swallows a timeout"]), "indexes into FINDING_DISPUTED"),
    ("remfix-gate.json", _case_adjudication("dispute-only", validated_false=[2]), "validated:false"),
    ("remfix-gate.json", _case_contract("dispute-only", TDD_RED_EXIT=1), "dispute-only report must leave TDD_RED_EXIT"),
    ("remfix-gate.json", _case_contract("dispute-only", TDD_GREEN_EXIT=0), "dispute-only report must leave TDD_GREEN_EXIT"),
    ("remfix-gate.json", _case_contract("dispute-only", PHASE_EXIT_READY=True), "dispute-only report must carry PHASE_EXIT_READY false"),
    ("remfix-gate.json", _case_contract("dispute-only", STATUS="FIXED"), "dispute-only STATUS"),
    ("remfix-gate.json", _case("dispute-only", _dispute_only_drop_contract), "dispute-only report needs the executor contract"),
    ("remfix-gate.json", _case("dispute-only", _dispute_only_undispute_one), "REM-FIX report empty COVERING_TESTS"),
    ("remfix-gate.json", _case_task("debug-workflow-remfix", subject="CC10X component-builder: REM-FIX x"), "must name its executor bug-investigator"),
    ("remfix-gate.json", _case_task("debug-workflow-remfix", executor="component-builder"), "executor must be bug-investigator"),
    ("remfix-gate.json", _case("debug-workflow-remfix", lambda c: c.update({"verifier_handoff_key": "results.builder"})), "hands the verifier results.investigator"),
    ("remfix-gate.json", _case_task("debug-workflow-remfix", workflow_type="BUILD"), "executor must be component-builder"),
    ("remfix-gate.json", _case_task("dispute-only", workflow_type="DEBUG"), "executor must be bug-investigator"),
    ("remfix-gate.json", _case("dispute-only", lambda c: c.update({"dispute_outcomes": ["remfix_created", "remfix_created"]})), "dispute_outcomes"),
    ("remfix-gate.json", _pop_expected("phase_status_after"), "must carry phase_status_after"),
    ("remfix-gate.json", _set_expected(phase_status_after={"before_adjudication": "partial", "after_adjudication": "partial"}), "phase_status_after must be"),
    ("remfix-gate.json", _set_expected(phase_status_after={"before_adjudication": "completed", "after_adjudication": "completed"}), "phase_status_after must be"),
    ("remfix-gate.json", lambda d: d["agent_outputs"]["verifier_adjudication"].update({"verifier_status": "FAIL"}), "phase_status_after must be"),
    ("remfix-gate.json", lambda d: d["agent_outputs"]["verifier_adjudication"].pop("verifier_status"), "must carry the verifier_status"),
    ("remfix-gate.json", _case_set("dispute-only", phase_status_after={"before_adjudication": "partial", "after_adjudication": "completed"}), "phase_status_after must be"),
    ("remfix-gate.json", _case_set("dispute-only", phase_status_after={"before_adjudication": "completed", "after_adjudication": "partial"}), "phase_status_after must be"),
    ("remfix-gate.json", _case_pop("dispute-only", "phase_status_after"), "must carry phase_status_after"),
    ("remfix-gate.json", _case_set("dispute-only-all-upheld", phase_exit_gate_reads=["verifier_return", "dispute_only_report"]), "phase_exit_gate reads the verifier return"),
    ("remfix-gate.json", _case_set("dispute-only-all-upheld", phase_exit_gate_reads=["verifier_return", "original_builder_completion", "dispute_only_report"]), "phase_exit_gate reads the verifier return"),
    ("remfix-gate.json", _case_pop("dispute-only-all-upheld", "phase_exit_gate_reads"), "phase_exit_gate reads the verifier return"),
    ("remfix-gate.json", _case("dispute-only-all-upheld", lambda c: c["verifier_adjudication"].update({"verifier_status": "FAIL"})), "phase_status_after must be"),
    ("remfix-gate.json", _case_report("dispute-only", FINDING_DISPUTED=["F1 (HIGH): save handler swallows a timeout", "F1 (HIGH): save handler swallows a timeout"]), "FINDING_DISPUTED entries must be distinct"),
    ("remfix-gate.json", _case_report("dispute-only", FINDING_DISPUTED=["F1 (HIGH): save handler swallows a timeout", "F9 (HIGH): an unrelated finding"]), "must map to exactly one distinct finding"),
    ("remfix-gate.json", _case_report("dispute-only", FINDING_DISPUTED=["F1 (HIGH): save handler swallows a timeout", "F1 (HIGH): the same finding restated"]), "must map to exactly one distinct finding"),
    ("remfix-gate.json", _case_contract("dispute-only", PHASE_STATUS="completed"), "must carry PHASE_STATUS partial"),
    ("remfix-gate.json", _case_contract("dispute-only", PROOF_STATUS="passed"), "must carry PROOF_STATUS gaps_found"),
    ("remfix-gate.json", _case_contract("dispute-only", TDD_RED_REASON_KIND="behavioral"), "must leave TDD_RED_REASON_KIND null"),
    ("remfix-gate.json", _case_contract("dispute-only", TDD_RED_REASON="expected 1 received 0"), "must leave TDD_RED_REASON null"),
    ("remfix-gate.json", _case_contract("dispute-only", BLOCKED_ITEMS=["cannot run"]), "must carry empty BLOCKED_ITEMS"),
    ("remfix-gate.json", _case_drop_scenario("dispute-only"), "one scenario per dispute"),
    ("remfix-gate.json", _case_contract("dispute-only", SCENARIOS=[]), "one scenario per dispute"),
    ("remfix-gate.json", _case_scenario("dispute-only", 1, command="npm test"), "carries the VERIFY_COMMAND"),
    ("remfix-gate.json", _case_scenario("dispute-only", 0, expected=""), "non-empty name, expected and actual"),
    ("remfix-gate.json", _case_contract("dispute-only-investigator", STATUS="PASS"), "dispute-only STATUS must be FIXED"),
    ("remfix-gate.json", _case_contract("dispute-only-investigator", TDD_RED_EXIT=1), "must leave TDD_RED_EXIT null"),
    ("remfix-gate.json", _case_loop("dispute-only-investigator", rung="none"), "FEEDBACK_LOOP.rung cli_snapshot"),
    ("remfix-gate.json", _case_loop("dispute-only-investigator", command=None), "FEEDBACK_LOOP.rung cli_snapshot"),
    ("remfix-gate.json", _case_closeout("dispute-only-investigator", instrumentation_removed=True), "leaves DEBUG_CLOSEOUT.instrumentation_removed"),
    ("remfix-gate.json", _case_closeout("dispute-only-investigator", repro_no_longer_fires=True), "leaves DEBUG_CLOSEOUT.instrumentation_removed"),
    ("remfix-gate.json", _case_scenario("dispute-only-investigator", 0, name="Dispute: F1 the cart total uses the locale"), "is a Regression: scenario"),
    ("remfix-gate.json", _case_set("dispute-only-investigator", phase_status_after={"before_adjudication": "partial", "after_adjudication": "completed"}), "phase_status_after must be"),
    ("remfix-gate.json", _case_set("dispute-only-investigator", verifier_handoff_key="results.builder"), "hands the verifier results.investigator"),
    ("multi-phase-memory-finalize.json", _memory_blocked_by_early_task_only, "must be blocked by the last phase's verifier"),
    ("multi-phase-memory-finalize.json", _memory_blocked_by_last_and_early_task, "blocked by an earlier-phase task"),
    ("multi-phase-memory-finalize.json", _memory_blocked_by_doc_sync_of_wrong_verifier, "last phase's verifier"),
    ("multi-phase-memory-finalize.json", _memory_blocked_by_early_doc_sync_only, "last phase's verifier"),
    ("multi-phase-memory-finalize.json", _builder2_blocked_by_verifier_only, "must be blocked on the previous phase's last task"),
    ("multi-phase-memory-finalize.json", _builder2_unblocked, "must be blocked on the previous phase's last task"),
    ("multi-phase-memory-finalize.json", _memory_blocked_by_early_doc_sync_with_last, "blocked by an earlier-phase task"),
    ("multi-phase-memory-finalize.json", _legacy_phase_id_key, "phase_id"),
    ("multi-phase-memory-finalize.json", _dup_memory_finalized, "memory_finalized appears 2 times"),
    ("multi-phase-memory-finalize.json", _unfinalized_memory, "memory_finalized appears 0 times"),
    ("multi-phase-memory-finalize.json", _second_memory_task, "exactly one memory-finalize task"),
    ("triage-happy-path.json", _triage_needs_info_with_memory, "Memory Update must not exist before the terminal state"),
    ("triage-happy-path.json", _triage_needs_grilling_with_memory, "Memory Update must not exist before the terminal state"),
    ("triage-happy-path.json", _terminal_keeps_gate, "must not carry a pending_gate"),
    ("codebase-health-happy-path.json", _health_choice_pending_with_memory, "Memory Update must not exist before the terminal state"),
    ("triage-needs-info-pause.json", _paused_add_memory_task, "Memory Update must not exist before the terminal state"),
    ("triage-needs-info-pause.json", _paused_finalized, "memory_finalized recorded before the terminal state"),
    ("triage-needs-info-pause.json", _paused_no_gate, "must carry a pending_gate"),
    ("codebase-health-candidate-pause.json", _paused_add_memory_task, "Memory Update must not exist before the terminal state"),
    ("codebase-health-candidate-pause.json", _paused_finalized, "memory_finalized recorded before the terminal state"),
    ("codebase-health-candidate-pause.json", _paused_no_gate, "must carry a pending_gate"),
    ("triage-needs-info-pause.json", _paused_drop_notes, "paused artifact memory_notes is missing"),
    ("triage-needs-info-pause.json", _paused_drop_one_note, "paused artifact memory_notes is missing"),
    ("codebase-health-candidate-pause.json", _paused_drop_notes, "paused artifact memory_notes is missing"),
    ("codebase-health-candidate-pause.json", _paused_drop_one_note, "paused artifact memory_notes is missing"),
    ("multi-phase-resume-events.json", _resume_drop_boundary, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_stale_phase_id, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_expect_flat_results, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_stale_slots_empty, "stale slot"),
    ("multi-phase-resume-events.json", _resume_boundary_after_results, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_omit_remfix_result, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_no_plan_stale_phase_id, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_pause_decision_is_terminal, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_drop_pass_two, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_grilling_pause_is_terminal, "runnable steps"),
    ("multi-phase-resume-events.json", _resume_candidates_is_a_pause, "runnable steps"),
    ("multi-phase-resume-events.json", _locator_clear_gate, "resume locator"),
    ("multi-phase-resume-events.json", _locator_unterminate, "resume locator"),
    ("multi-phase-resume-events.json", _locator_single_paused, "resume locator"),
    ("multi-phase-resume-events.json", _locator_drop_request_match, "resume locator"),
    ("triage-needs-info-pause.json", _triage_pause_wrong_gate, "pending_gate must be 'needs_info'"),
    ("codebase-health-candidate-pause.json", _health_pause_wrong_gate, "pending_gate must be 'candidate_choice'"),
    ("triage-needs-info-pause.json", _advisory_converged, "advisory workflow must carry convergence_state N/A"),
    ("codebase-health-candidate-pause.json", _advisory_converged, "advisory workflow must carry convergence_state N/A"),
    ("triage-happy-path.json", _advisory_converged, "advisory workflow must carry convergence_state N/A"),
    ("triage-needs-info-pause.json", _advisory_four_remediations, "advisory workflow must carry no remediation_history"),
    ("codebase-health-happy-path.json", _advisory_four_remediations, "advisory workflow must carry no remediation_history"),
    ("triage-happy-path.json", _triage_wontfix_with_grilling, "expected TRIAGED"),
    ("two-workflow-resume.json", _share_workflow_id, "distinct workflow_id"),
    ("two-workflow-resume.json", _foreign_task, "resumed task a_builder carries wf"),
]


def test_multi_phase_fixture_accepts_memory_blocked_by_the_last_phase_doc_sync_task(tmp_path):
    root = make_tree(tmp_path)
    edit_json(root / FIXTURES_REL / "multi-phase-memory-finalize.json", _memory_blocked_by_doc_sync)
    result = run_tool("workflow_replay_check.py", root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_remfix_gate_replay_accepts_a_multiline_string_in_the_proof_field(tmp_path):
    root = make_tree(tmp_path)
    block = "PASS tests/team_settings.test.ts\n  saves the team id\n  rejects a non-admin\nTests: 2 passed"
    edit_json(root / FIXTURES_REL / "remfix-gate.json", _set_remfix_field("TEST_OUTPUT", block))
    result = run_tool("workflow_replay_check.py", root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_replay_registers_the_p3_fixtures_and_the_two_advisory_pause_fixtures():
    result = run_tool("workflow_replay_check.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "fixtures=35" in result.stdout


@pytest.mark.parametrize("name,mutate,message", L1_MUTATIONS, ids=lambda v: getattr(v, "__name__", str(v)))
def test_a_mutated_p3_fixture_fails_with_a_specific_message(name, mutate, message, tmp_path):
    root = make_tree(tmp_path)
    edit_json(root / FIXTURES_REL / name, mutate)
    result = run_tool("workflow_replay_check.py", root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert name in result.stderr and message in result.stderr, result.stderr


@pytest.mark.parametrize(
    "name,path",
    [
        ("build-happy-path.json", ("agent_outputs", "builder_contract")),
        ("debug-fixed.json", ("agent_outputs", "investigator_contract")),
    ],
)
def test_replay_accepts_any_nonzero_red_exit_and_rejects_zero_or_null(name, path, tmp_path):
    def with_red(value):
        def mutate(d):
            node = d
            for key in path:
                node = node[key]
            node["TDD_RED_EXIT"] = value

        return mutate

    for value in (2, 127):
        (tmp_path / f"ok{value}").mkdir()
        root = make_tree(tmp_path / f"ok{value}")
        edit_json(root / FIXTURES_REL / name, with_red(value))
        result = run_tool("workflow_replay_check.py", root)
        assert result.returncode == 0, (value, result.stdout + result.stderr)
    for value in (0, None, True):
        (tmp_path / f"bad{value}").mkdir()
        root = make_tree(tmp_path / f"bad{value}")
        edit_json(root / FIXTURES_REL / name, with_red(value))
        result = run_tool("workflow_replay_check.py", root)
        assert result.returncode == 1 and ("RED evidence" in result.stderr or "regression RED" in result.stderr), (value, result.stderr)


def skeleton_artifact(tmp_path, workflow_type, **overrides):
    text = SKELETON.read_text(encoding="utf-8")
    text = text.replace("__WORKFLOW_UUID__", "wf-20261007T090000Z-aaaaaaaa").replace("__WORKFLOW_TYPE__", workflow_type)
    text = text.replace("__USER_REQUEST__", "x").replace("__ISO_TIMESTAMP__", "2026-10-07T09:00:00Z")
    data = json.loads(text.replace("__PHASE__", workflow_type.lower()))
    data.update(overrides)
    path = tmp_path / f"{workflow_type}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.mark.parametrize("workflow_type", ["PLAN", "BUILD"])
def test_artifact_mode_accepts_a_fresh_skeleton_artifact(workflow_type, tmp_path):
    artifact = skeleton_artifact(tmp_path, workflow_type)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "artifact OK" in result.stdout


def test_artifact_mode_rejects_a_missing_key_and_a_double_memory_finalize(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD")
    data = json.loads(artifact.read_text(encoding="utf-8"))
    del data["traceability"]
    artifact.write_text(json.dumps(data), encoding="utf-8")
    missing = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert missing.returncode == 1 and "missing keys ['traceability']" in missing.stderr, missing.stderr

    twice = {"event": "memory_finalized", "ts": "2026-10-07T09:30:00Z", "phase": "memory-finalize"}
    artifact = skeleton_artifact(tmp_path, "PLAN", phase_cursor="memory-finalize", status_history=[twice, twice])
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "memory_finalized appears 2 times" in result.stderr, result.stderr


def test_artifact_mode_rejects_an_unreadable_or_missing_file(tmp_path):
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(tmp_path / "nope.json"))
    assert result.returncode == 1 and "Traceback" not in result.stderr
    assert "nope.json" in result.stderr


# --- P3-REMFIX1: --artifact mode counts memory_finalized in status_history AND the sibling events.jsonl ---

def _write_events(artifact, *events):
    sibling = artifact.with_name(artifact.stem + ".events.jsonl")
    sibling.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")


FINALIZED = {"event": "memory_finalized", "ts": "2026-10-07T09:30:00Z", "phase": "memory-finalize"}
STARTED = {"event": "workflow_started", "ts": "2026-10-07T09:00:00Z", "phase": "build"}


def test_artifact_mode_counts_a_finalize_recorded_only_in_events_jsonl(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD")
    _write_events(artifact, STARTED, FINALIZED, FINALIZED)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "memory_finalized appears 2 times in events.jsonl" in result.stderr, result.stderr


def test_artifact_mode_accepts_one_finalize_recorded_in_both_sources(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD", phase_cursor="memory-finalize", status_history=[STARTED, FINALIZED])
    _write_events(artifact, STARTED, FINALIZED)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 0, result.stdout + result.stderr


def test_artifact_mode_requires_phase_cursor_when_only_events_jsonl_has_the_finalize(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD")
    _write_events(artifact, STARTED, FINALIZED)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "phase_cursor is not memory-finalize" in result.stderr, result.stderr


def test_artifact_mode_rejects_a_completed_workflow_that_never_finalized_memory(tmp_path):
    done = {"event": "workflow_completed", "ts": "2026-10-07T09:40:00Z", "phase": "memory-finalize"}
    artifact = skeleton_artifact(tmp_path, "BUILD", status_history=[STARTED, done])
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "completed but memory_finalized is recorded in neither" in result.stderr, result.stderr

    artifact = skeleton_artifact(tmp_path, "PLAN", status_history=[STARTED])
    _write_events(artifact, STARTED, done)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "completed but memory_finalized is recorded in neither" in result.stderr, result.stderr


DONE = {"event": "workflow_completed", "ts": "2026-10-07T09:40:00Z", "phase": "memory-finalize"}


@pytest.mark.parametrize("workflow_type", ["ORIENT", "pending"])
def test_artifact_mode_accepts_a_completed_workflow_type_without_a_memory_task(workflow_type, tmp_path):
    artifact = skeleton_artifact(tmp_path, workflow_type, status_history=[STARTED, DONE])
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("workflow_type", ["BUILD", "DEBUG", "REVIEW", "PLAN", "QA", "TRIAGE", "CODEBASE-HEALTH"])
def test_artifact_mode_still_requires_a_finalize_for_memory_workflow_types(workflow_type, tmp_path):
    artifact = skeleton_artifact(tmp_path, workflow_type, status_history=[STARTED, DONE])
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "completed but memory_finalized is recorded in neither" in result.stderr, result.stderr


@pytest.mark.parametrize("history", [[STARTED, DONE, {"event": "note", "ts": "t"}], [DONE, STARTED]])
def test_artifact_mode_sees_workflow_completed_anywhere_in_status_history(history, tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD", status_history=history)
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "completed but memory_finalized is recorded in neither" in result.stderr, result.stderr


def test_artifact_mode_sees_workflow_completed_anywhere_in_events(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD", status_history=[STARTED])
    _write_events(artifact, STARTED, DONE, {"event": "build_finished"})
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "completed but memory_finalized is recorded in neither" in result.stderr, result.stderr


def test_artifact_mode_rejects_an_event_from_a_foreign_workflow(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD", phase_cursor="memory-finalize")
    _write_events(artifact, dict(STARTED, wf="wf-20261007T090000Z-aaaaaaaa"), dict(FINALIZED, wf="wf-other"))
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "foreign wf" in result.stderr, result.stderr


def test_artifact_mode_accepts_events_carrying_the_matching_wf(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD", phase_cursor="memory-finalize", status_history=[STARTED, FINALIZED])
    _write_events(artifact, dict(STARTED, wf="wf-20261007T090000Z-aaaaaaaa"))
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 0, result.stdout + result.stderr


def test_artifact_mode_rejects_a_malformed_events_jsonl(tmp_path):
    artifact = skeleton_artifact(tmp_path, "BUILD")
    artifact.with_name(artifact.stem + ".events.jsonl").write_text("not json\n", encoding="utf-8")
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(artifact))
    assert result.returncode == 1 and "events.jsonl" in result.stderr and "Traceback" not in result.stderr


@pytest.mark.parametrize("payload", ["null", "7", "[]"])
def test_artifact_mode_names_a_non_object_artifact(payload, tmp_path):
    path = tmp_path / "x.json"
    path.write_text(payload, encoding="utf-8")
    result = run_tool("workflow_replay_check.py", None, "--artifact", str(path))
    assert result.returncode == 1 and "must be a JSON object" in result.stderr, result.stderr


HOOKS_README_REL = "plugins/cc10x/hooks/README.md"


def readme_errors(root: Path) -> list[str]:
    return harness_audit.check_hooks_readme(root / "plugins" / "cc10x")


def test_hooks_readme_lists_every_registered_hook_exactly_once_on_the_real_tree():
    assert harness_audit.check_hooks_readme() == []


def test_a_hook_missing_from_the_hooks_readme_is_named(tmp_path):
    root = make_tree(tmp_path)
    readme = root / HOOKS_README_REL
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("`cc10x_qa_isolation_guard.py`", "the QA guard"),
        encoding="utf-8",
    )
    assert any("cc10x_qa_isolation_guard.py" in e and "0 times" in e for e in readme_errors(root))
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1 and "hooks README" in result.stderr


def test_each_event_logger_registration_must_be_listed_by_its_argument(tmp_path):
    root = make_tree(tmp_path)
    readme = root / HOOKS_README_REL
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("`cc10x_event_logger.py stop_failure`", "the failure logger"),
        encoding="utf-8",
    )
    assert any("cc10x_event_logger.py stop_failure" in e for e in readme_errors(root))


def test_a_hook_listed_twice_in_the_hooks_readme_is_named(tmp_path):
    root = make_tree(tmp_path)
    readme = root / HOOKS_README_REL
    readme.write_text(readme.read_text(encoding="utf-8") + "\nAgain: `cc10x_git_guard.py`.\n", encoding="utf-8")
    assert any("cc10x_git_guard.py" in e and "2 times" in e for e in readme_errors(root))


def test_a_phantom_hook_script_in_the_hooks_readme_is_named(tmp_path):
    root = make_tree(tmp_path)
    readme = root / HOOKS_README_REL
    readme.write_text(readme.read_text(encoding="utf-8") + "\nAlso `cc10x_ghost_guard.py`.\n", encoding="utf-8")
    assert any("cc10x_ghost_guard.py" in e for e in readme_errors(root))


@pytest.mark.parametrize(
    "phrase",
    ["the only two enforcement points", "only 2 enforcement points", "the only three blocking hooks", "Only one enforcement point"],
)
@pytest.mark.parametrize(
    "rel",
    [HOOKS_README_REL, "README.md", "plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md"],
)
def test_the_only_n_enforcement_points_claim_is_rejected_wherever_it_appears(phrase, rel, tmp_path):
    root = make_tree(tmp_path)
    path = root / rel
    path.write_text(path.read_text(encoding="utf-8") + f"\n**Blocking** ({phrase}):\n", encoding="utf-8")
    assert any("enforcement" in e and rel in e for e in readme_errors(root))


ARCHIVED_DOCS = (
    "2026-06-17-HANDOFF.md",
    "2026-04-19-diff-driven-docs-plan.md",
    "2026-06-17-upstream-steal-list.md",
    "harmony-release-2026-04-12.md",
    "latency-reduction-note.md",
    "cc10x-orchestration-bible.md",
    "cc10x-orchestration-logic-analysis.md",
    "v12-keep-inventory.md",
    "2026-07-02-cc10x-v12-loop-engine-plan.md",
    "cc10x-explorer.html",
    "cc10x-architecture-explorer.html",
    "playgrounds",
)
BANNERED_IN_PLACE = (
    "docs/benchmarks/2026-03-12-first-place-strategy.md",
    "docs/benchmarks/2026-03-12-prompt-engineering-round-2-head-to-head.md",
    "docs/benchmarks/2026-03-12-session-learnings.md",
    "docs/benchmarks/2026-03-14-prompt-steal-hardening.md",
    "docs/benchmarks/2026-03-16-planning-recovery.md",
    "docs/adr/0002-advisory-onramp-workflows.md",
)
BANNER = re.compile(r"HISTORICAL: records past work; not maintained against the current release\. Superseded by: (\S+)\.(?:\s|$)")


def test_archived_docs_are_visible_to_git_and_carry_a_resolving_banner():
    history = REPO / "docs" / "history"
    names = [p.name for p in history.iterdir() if p.name != "playgrounds"] if history.is_dir() else []
    assert sorted(names + (["playgrounds"] if (history / "playgrounds").is_dir() else [])) == sorted(ARCHIVED_DOCS)
    banner_files = [history / n for n in names if n.endswith((".md", ".html"))]
    banner_files += sorted((history / "playgrounds").glob("*.html"))
    for path in banner_files + [REPO / r for r in BANNERED_IN_PLACE]:
        text = path.read_text(encoding="utf-8")
        match = BANNER.search(text[:600])
        assert match, f"{path.name} has no historical banner in its first lines"
        assert (REPO / match.group(1).strip("`")).exists(), f"{path.name} points at missing {match.group(1)}"
        ignored = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=REPO).returncode
        assert ignored == 1, f"{path} is ignored by git"


def test_archived_docs_are_gone_from_their_old_locations():
    old = [REPO / "docs" / n for n in ARCHIVED_DOCS[:7]]
    old += [REPO / "docs" / "plans" / n for n in ARCHIVED_DOCS[7:9]]
    old += [REPO / n for n in ARCHIVED_DOCS[9:]]
    assert [str(p.relative_to(REPO)) for p in old if p.exists()] == []


@pytest.mark.parametrize("name", ["cc10x-orchestration-bible.md", "cc10x-orchestration-logic-analysis.md", "latency-reduction-note.md"])
def test_harness_audit_does_not_require_the_archived_docs(name, tmp_path):
    root = make_tree(tmp_path)
    old = root / "docs" / name
    if old.exists():
        old.unlink()
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_version_tag_requirement_covers_the_three_maintained_registries(tmp_path):
    root = make_tree(tmp_path)
    for name in ("router-invariants.md", "prompt-invariants.md", "agent-contract-registry.md"):
        path = root / "docs" / name
        tag = f"v{plugin_version(root)}"
        path.write_text(path.read_text(encoding="utf-8").replace(tag, "vX.Y.Z"), encoding="utf-8")
        result = run_tool("harness_audit.py", root)
        assert result.returncode != 0 and "not synced to current version tag" in result.stderr, name
        path.write_text(path.read_text(encoding="utf-8").replace("vX.Y.Z", tag), encoding="utf-8")


def test_readme_local_links_resolve():
    text = (REPO / "README.md").read_text(encoding="utf-8")
    missing = [
        href
        for href in re.findall(r'href="([^"#:]+?)"', text)
        if not (REPO / href).exists()
    ]
    assert missing == []


def test_adr_0001_says_pre_seam_fixtures_are_rejected_now():
    text = " ".join((REPO / "docs/adr/0001-enforced-seam-gate.md").read_text(encoding="utf-8").split())
    assert "fixtures predating the fields are rejected" in text
    assert "still accepted" not in text


def test_adr_0002_records_the_current_route_priorities():
    text = (REPO / "docs/adr/0002-advisory-onramp-workflows.md").read_text(encoding="utf-8")
    assert "## Amendment" in text
    assert "QA=5, TRIAGE=6, CODEBASE-HEALTH=7, DEFAULT=8" in text.split("## Amendment", 1)[1]


@pytest.mark.parametrize("name", ["DESIGN.md", "PRODUCT.md"])
def test_keynote_deck_docs_state_their_scope(name):
    text = (REPO / name).read_text(encoding="utf-8")
    scope = re.search(r"^Scope: .*keynote deck.*not the cc10x plugin.*$", text, re.M)
    assert scope, f"{name} has no one-line scope sentence"


def test_anthropic_comparison_open_items_live_in_the_tracked_known_flaws_doc():
    text = (REPO / "docs/known-flaws.md").read_text(encoding="utf-8")
    assert "2026-07-30 Anthropic prompting-guide comparison" in text
    assert "/tmp/" not in text and "/Users/" not in text


GATE_HEADING = "## 7. Release Gate"
GATE_DOCS = ("docs/cc10x-orchestration-safety.md", "docs/EVAL-STANDARD.md", "docs/prompt-change-checklist.md")


def gate_section() -> str:
    text = (REPO / "docs/prompt-change-checklist.md").read_text(encoding="utf-8")
    return text.split(f"\n{GATE_HEADING}\n", 1)[1].split("\n## ", 1)[0]


def test_the_release_gate_section_lists_every_step_and_flag_of_the_runner():
    import release_gate

    section = gate_section()
    for step_id, _ in release_gate.GATE_STEPS:
        assert f"`{step_id}`" in section, step_id
    help_text = subprocess.run(
        [sys.executable, str(TOOLS / "release_gate.py"), "--help"], capture_output=True, text=True, check=True
    ).stdout
    for flag in sorted(set(re.findall(r"--[a-z][a-z-]+", help_text)) - {"--help"}):
        assert flag in section, flag


def test_the_gate_list_exists_once_and_the_other_gate_docs_point_to_it():
    owners = [doc for doc in GATE_DOCS if f"\n{GATE_HEADING}\n" in (REPO / doc).read_text(encoding="utf-8")]
    assert owners == ["docs/prompt-change-checklist.md"]
    for doc in GATE_DOCS:
        text = (REPO / doc).read_text(encoding="utf-8")
        assert "7. Release Gate" in text, doc
        if doc != "docs/prompt-change-checklist.md":
            assert "python3 plugins/cc10x/tools/" not in text, f"{doc} carries its own gate command list"


def test_checklist_section_5_points_to_the_gate_and_uses_the_changelog_as_the_change_record():
    text = (REPO / "docs/prompt-change-checklist.md").read_text(encoding="utf-8")
    section = text.split("## 5.", 1)[1].split("\n## ", 1)[0]
    assert GATE_HEADING in section
    assert "CHANGELOG.md" in section and "benchmark note" not in text.lower()


ROUTING_BLOCK_START = "# CC10x Orchestration (Always On)"
ROUTING_BLOCK_END = "No interpretation. No guessing. Only these exact opt-out phrases."


def routing_block(text: str) -> str:
    return text.split(ROUTING_BLOCK_START, 1)[1].split(ROUTING_BLOCK_END, 1)[0]


def test_readme_install_template_routing_block_is_identical_to_root_claude_md():
    claude = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert ROUTING_BLOCK_END in claude and ROUTING_BLOCK_END in readme
    assert routing_block(readme) == routing_block(claude)


def test_root_claude_md_has_no_placeholder_skill_table_and_no_entry_directive():
    claude = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    for name in ("mongodb-agent-skills", "react-best-practices", "vercel-agent-skills", "Complementary Skills"):
        assert name not in claude, name
    assert "[CC10x]|entry:" not in claude and "[CC10x]|entry:" not in readme
    assert "plugins/cc10x/skills/cc10x-router/SKILL.md" in claude
    assert "need not pay full routing" not in claude and "need not pay full routing" not in readme


def readme_text() -> str:
    return (REPO / "README.md").read_text(encoding="utf-8")


def readme_tree_paths() -> list[str]:
    """Repo-relative paths of the plugins/cc10x/ file tree in the README, braces expanded."""
    block = next(
        b for b in re.findall(r"```[a-z]*\n(.*?)```", readme_text(), re.S) if b.startswith("plugins/cc10x/\n")
    )
    stack: list[str] = []
    paths: list[str] = []
    for line in block.splitlines()[1:]:
        match = re.match(r"^((?:│   |    )*)(?:├── |└── )(\S+)", line)
        if not match:
            continue
        depth = len(match.group(1)) // 4
        del stack[depth:]
        stack.append(match.group(2))
        brace = re.search(r"\{([^}]*)\}", match.group(2))
        names = [match.group(2)] if not brace else [
            match.group(2).replace(brace.group(0), part) for part in brace.group(1).split(",")
        ]
        base = "".join(stack[:-1])
        paths.extend("plugins/cc10x/" + base + name for name in names)
    return paths


def test_readme_file_tree_lists_only_paths_that_exist_and_every_agent():
    paths = readme_tree_paths()
    assert len(paths) > 40
    assert [p for p in paths if not (REPO / p).exists()] == []
    for agent in (REPO / "plugins/cc10x/agents").glob("*.md"):
        assert f"plugins/cc10x/agents/{agent.name}" in paths, agent.name
    for name in ("qa-workflow.md", "cc10x_qa_isolation_guard.py", "templates/"):
        assert any(p.endswith(name) for p in paths), name


def test_readme_names_every_workflow_in_the_router_table():
    router = (REPO / "plugins/cc10x/skills/cc10x-router/SKILL.md").read_text(encoding="utf-8")
    table = router.split("## 1. Intent Routing", 1)[1].split("\n---", 1)[0]
    workflows = re.findall(r"(?m)^\|\s*\d+\s*\|[^|]*\|[^|]*\|\s*([A-Z][A-Z-]*)\s*\|", table)
    assert len(set(workflows)) == 8
    section = readme_text().split("## The 8 Workflows", 1)[1].split("\n## ", 1)[0]
    assert [w for w in sorted(set(workflows)) if f"**{w}**" not in section] == []


def test_readme_has_no_flagged_tagline_and_no_stale_plugin_command():
    text = readme_text()
    assert "Stop chasing better models" not in text
    assert "/plugins enable" not in text
    assert "silent-failure-red-flags" not in text


def test_readme_documents_install_update_python_and_env_vars():
    text = readme_text()
    for needle in (
        "claude plugin marketplace add romiluz13/cc10x",
        "claude plugin install cc10x@cc10x",
        "claude plugin update cc10x@cc10x --scope",
        "/reload-plugins",
        "Python 3.9",
        "3.13",
        "auto-update",
        "CLAUDE_CODE_ENABLE_TODO_TOOLS=1",
        "CLAUDE_CODE_TASK_LIST_ID",
        "CLAUDE_CONFIG_DIR",
        "CLAUDE_CODE_PLUGIN_CACHE_DIR",
        "plugins/cc10x/hooks/README.md",
    ):
        assert needle in text, needle
    assert re.search(r"(?mi)^.*gitignore.*`\.cc10x/`", text)
    assert re.search(r"(?m)^#+ .*auto-memory", text, re.I)


def test_readme_release_table_covers_every_release_from_v11_to_the_current_version():
    current = json.loads((REPO / "plugins/cc10x/.claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    wanted = [v for v in re.findall(r"(?m)^## \[(\d+\.\d+\.\d+)\]", changelog) if int(v.split(".")[0]) >= 11]
    assert current in wanted
    text = readme_text()
    assert [v for v in wanted if f"| **v{v}** |" not in text] == []
    assert f"Release history (v5.3 → v{current})" in text


def readme_setup_rules() -> list[str]:
    """The permission rules the README's setup step tells Claude to merge."""
    setup = readme_text().split("### Step 3", 1)[1].split("### Step 4", 1)[0]
    block = re.search(r"```json\n(.*?)```", setup, re.S).group(1)
    return re.findall(r'"([^"]+)"', block)


def test_settings_template_and_readme_setup_step_carry_the_same_rules():
    template = json.loads((REPO / "claude-settings-template.json").read_text(encoding="utf-8"))
    assert readme_setup_rules() == template["permissions"]["allow"]


def test_memory_permission_rule_uses_the_edit_form_that_covers_nested_paths():
    template = json.loads((REPO / "claude-settings-template.json").read_text(encoding="utf-8"))
    allow = template["permissions"]["allow"]
    assert "Edit(.cc10x/**)" in allow
    assert [rule for rule in allow if rule.startswith("Write(")] == []
    text = readme_text()
    assert '"Write(' not in text
    troubleshooting = text.split("### Claude Code keeps asking for permission to edit memory files", 1)[1].split("\n---", 1)[0]
    assert '"Edit(.cc10x/**)"' in troubleshooting
    assert "Bash(python3:*)" in text and "any `python3` command" in text


def guide_text() -> str:
    return (REPO / GUIDE_REL).read_text(encoding="utf-8")


def test_guide_has_one_workflow_section_covering_all_eight_workflows():
    text = guide_text()
    assert "## The 4 workflows" not in text and "The 4 Workflows" not in text
    section = text.split("## The 8 workflows", 1)[1].split("\n## ", 1)[0]
    for name in ("BUILD", "DEBUG", "REVIEW", "PLAN", "QA", "ORIENT", "TRIAGE", "CODEBASE-HEALTH"):
        assert re.search(rf"(?m)^\| {name} \|", section), name


def test_guide_describes_hooks_and_allowed_tools_as_they_behave():
    text = guide_text()
    assert "can be blocked" not in text and "enforce guardrails" not in text
    assert "audit by default" in text
    assert "pre-approves" in text and "does not restrict" in text
    assert "docs/cc10x-orchestration-bible.md" not in text.replace("docs/history/cc10x-orchestration-bible.md", "")
    assert (REPO / "docs/history/cc10x-orchestration-bible.md").exists()


def test_marketplace_plugin_entry_carries_no_version_of_its_own(tmp_path):
    manifest = json.loads((REPO / MARKETPLACE_REL).read_text(encoding="utf-8"))
    assert "version" not in manifest["plugins"][0]
    root = make_tree(tmp_path)
    for tool in ("harness_audit.py", "doc_consistency_check.py"):
        result = run_tool(tool, root)
        assert result.returncode == 0, tool + result.stdout + result.stderr
    version = json.loads((root / PLUGIN_JSON_REL).read_text(encoding="utf-8"))["version"]
    edit_json(root / MARKETPLACE_REL, lambda d: d["plugins"][0].update(version=version))
    for tool in ("harness_audit.py", "doc_consistency_check.py"):
        result = run_tool(tool, root)
        assert result.returncode == 1, tool
        assert "must not duplicate the version" in result.stdout + result.stderr, tool


def test_manifest_descriptions_have_no_unverifiable_claim_and_keywords_name_qa():
    plugin = json.loads((REPO / PLUGIN_JSON_REL).read_text(encoding="utf-8"))
    marketplace = json.loads((REPO / MARKETPLACE_REL).read_text(encoding="utf-8"))
    assert "leaner" not in json.dumps(plugin) + json.dumps(marketplace)
    assert plugin["description"] == marketplace["plugins"][0]["description"]
    assert set(plugin["keywords"]) == set(marketplace["plugins"][0]["keywords"])
    assert "qa" in plugin["keywords"]
