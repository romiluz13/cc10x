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


# --- living-doc checks and the docs-rot ratchet -----------------------------------------------

sys.path.insert(0, str(TOOLS))
import harness_audit  # noqa: E402

BASELINE_REL = "plugins/cc10x/tools/docs_rot_baseline.json"


def load_baseline(root: Path) -> list:
    return json.loads((root / BASELINE_REL).read_text(encoding="utf-8"))["entries"]


def write_baseline(root: Path, entries: list) -> None:
    (root / BASELINE_REL).write_text(json.dumps({"entries": entries}), encoding="utf-8")


def entry(key: str, owner: str = "P6.T2") -> dict:
    return {"key": key, "owner": owner, "reason": "test"}


def drop_section(path: Path, heading: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.index(f"### {heading}\n")
    end = text.find("\n### ", start + 1)
    end = len(text) if end == -1 else end + 1
    path.write_text(text[:start] + text[end:], encoding="utf-8")


def set_banner(root: Path, version: str) -> None:
    path = root / "docs" / "router-invariants.md"
    text = path.read_text(encoding="utf-8")
    banner = f"Current product line is `v{version}`"
    if "Current product line is `v" in text:
        text = re.sub(r"Current product line is `v[^`]*`", banner, text, count=1)
    else:
        text = f"> **Status note:** {banner}.\n\n" + text
    path.write_text(text, encoding="utf-8")


def plugin_version(root: Path) -> str:
    return json.loads((root / "plugins/cc10x/.claude-plugin/plugin.json").read_text())["version"]


def test_real_tree_passes_and_warns_while_the_baseline_is_non_empty():
    result = run_tool("harness_audit.py")
    assert result.returncode == 0, result.stdout + result.stderr
    if load_baseline(REPO):
        assert "WARN" in result.stdout and "baseline" in result.stdout


def test_baseline_entries_are_owned_by_a_p6_task_and_all_still_fail():
    entries = load_baseline(REPO)
    for item in entries:
        assert item["owner"].startswith("P6.T"), item
        assert item["reason"].strip(), item
    assert {e["key"] for e in entries} == set(harness_audit.check_living_docs())


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


def test_stale_product_line_banner_is_detected_and_a_current_one_is_not(tmp_path):
    root = make_tree(tmp_path)
    key = "registry-banner-stale:docs/router-invariants.md"
    set_banner(root, "11.0.0")
    assert key in harness_audit.check_living_docs(root)
    set_banner(root, plugin_version(root))
    assert key not in harness_audit.check_living_docs(root)
    set_banner(root, "12.0.0")
    assert key in harness_audit.check_living_docs(root)


def test_a_fixed_baseline_entry_must_be_removed(tmp_path):
    root = make_tree(tmp_path)
    key = "registry-banner-stale:docs/router-invariants.md"
    set_banner(root, "11.0.0")
    write_baseline(root, [entry(k, "P6.T4") for k in harness_audit.check_living_docs(root)])
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
        [entry("a:1", "P6.T2"), entry("b:2", "P6.T2"), entry("c:3", "P6.T3")],
    )
    assert errors == []
    assert len(warnings) == 1
    assert "3" in warnings[0] and "P6.T2" in warnings[0] and "P6.T3" in warnings[0]


def test_ratchet_strict_fails_on_any_baseline_entry():
    errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [entry("a:1")], strict=True)
    assert errors and "--strict" in errors[0]
    assert harness_audit.apply_rot_ratchet({}, [], strict=True) == ([], [])


def test_ratchet_an_entry_without_an_owner_is_an_error():
    errors, _ = harness_audit.apply_rot_ratchet({"a:1": "x"}, [{"key": "a:1", "reason": "r"}])
    assert any("owner" in e for e in errors)


def ghost_tree_with_matching_baseline(tmp_path: Path) -> Path:
    root = make_tree(tmp_path)
    registry = root / "docs" / "agent-contract-registry.md"
    rewrite(registry, "## Read-Only Review Agents", "| `ghost-agent` | YAML | `PASS` | x | `MEMORY_NOTES` |\n\n## Read-Only Review Agents")
    write_baseline(root, [entry(key) for key in harness_audit.check_living_docs(root)])
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


def test_the_hard_coded_hook_script_tuple_is_gone():
    source = (TOOLS / "harness_audit.py").read_text(encoding="utf-8")
    assert '"cc10x_task_completed_guard.py",\n        "cc10x_event_logger.py",\n        "",' not in source


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
CLAIM_KEYS = {
    "guide-agent-count",
    "guide-skill-count",
    "manifest-unverifiable-claim:plugin.json",
    "manifest-description-mismatch",
    "manifest-keywords-mismatch",
}


def claims(root: Path = REPO) -> dict:
    return doc_consistency_check.check_claims(root)


def edit_json(path: Path, mutate) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_real_tree_claim_failures_are_exactly_the_known_rot():
    assert set(claims()) == CLAIM_KEYS


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
    guide = root / GUIDE_REL
    text = guide.read_text(encoding="utf-8")
    guide.write_text(text.replace("11 specialist agents", "14 specialist agents").replace("20 skills", "21 skills"), encoding="utf-8")
    fixed = claims(root)
    assert "guide-agent-count" not in fixed and "guide-skill-count" not in fixed
    assert {"guide-agent-count", "guide-skill-count"} <= set(claims())
    guide.write_text(text.replace("11 specialist agents", "15 specialist agents"), encoding="utf-8")
    assert "guide-agent-count" in claims(root)


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
    guide = root / GUIDE_REL
    guide.write_text(guide.read_text(encoding="utf-8").replace("11 specialist agents", "14 specialist agents"), encoding="utf-8")
    result = run_tool("harness_audit.py", root)
    assert result.returncode == 1
    assert "stale baseline entry" in result.stderr and "guide-agent-count" in result.stderr


def test_the_qa_routing_row_is_pinned(tmp_path):
    root = make_tree(tmp_path)
    assert run_tool("prompt_clause_assertions.py", None, "--allow-no-yaml").returncode == 0
    router = root / "plugins/cc10x/skills/cc10x-router/SKILL.md"
    rewrite(router, "| 5 | QA | test, QA, e2e,", "| 5 | QA | test, e2e,")
    bad = run_tool("prompt_clause_assertions.py", root, "--allow-no-yaml")
    assert bad.returncode == 1
    assert "router routing table: priority-5 QA row" in bad.stdout
