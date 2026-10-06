"""Hermetic tests for the strict frontmatter reader behind harness_audit's agent checks.

Every negative fixture is a tree the old exact-line matching passed silently.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import harness_audit  # noqa: E402

GOOD_SKILL = "---\nname: {name}\nuser-invocable: false\n---\nbody\n"


def agent(skills_block: str, color: str = "blue") -> str:
    return f"---\nname: a\ncolor: {color}\n{skills_block}---\nbody\n"


def tree(tmp_path: Path, agents: dict, skills: dict):
    agents_dir, skills_dir = tmp_path / "agents", tmp_path / "skills"
    agents_dir.mkdir()
    for name, text in agents.items():
        (agents_dir / f"{name}.md").write_bytes(text.encode("utf-8"))
    for name, text in skills.items():
        (skills_dir / name).mkdir(parents=True)
        (skills_dir / name / "SKILL.md").write_bytes(text.encode("utf-8"))
    return agents_dir, skills_dir


def preload_errors(tmp_path, agent_text, skills=None):
    skills = {"good": GOOD_SKILL.format(name="good")} if skills is None else skills
    agents_dir, skills_dir = tree(tmp_path, {"a": agent_text}, skills)
    return harness_audit.check_preloaded_skills_invocable(agents_dir, skills_dir)


def test_current_repo_passes():
    assert harness_audit.check_preloaded_skills_invocable() == []
    assert harness_audit.check_researcher_mcp_lanes() == []
    assert harness_audit.check_agent_colors() == []


def test_valid_tree_passes(tmp_path):
    assert preload_errors(tmp_path, agent("skills:\n  - cc10x:good\n")) == []


@pytest.mark.parametrize(
    "label,block",
    [
        ("block", "skills:\n  - cc10x:ghost\n"),
        ("flow", "skills: [cc10x:good, cc10x:ghost]\n"),
        ("four-space indent", "skills:\n    - cc10x:ghost\n"),
        ("trailing space", "skills: \n  - cc10x:ghost\n"),
        ("trailing comment", "skills: # preload\n  - cc10x:ghost\n"),
        ("blank line after key", "skills:\n\n  - cc10x:good\n  - cc10x:ghost\n"),
        ("comment line in list", "skills:\n  - cc10x:good\n  # note\n  - cc10x:ghost\n"),
        ("item comment", "skills:\n  - cc10x:good # keep\n  - cc10x:ghost # drop\n"),
        ("quoted items", 'skills:\n  - "cc10x:ghost"\n'),
    ],
)
def test_missing_skill_found_in_every_supported_shape(tmp_path, label, block):
    errors = preload_errors(tmp_path, agent(block))
    assert any("ghost" in e for e in errors), (label, errors)


def test_bom_agent_is_still_inspected(tmp_path):
    errors = preload_errors(tmp_path, "﻿" + agent("skills:\n  - cc10x:ghost\n"))
    assert any("ghost" in e for e in errors), errors


def test_crlf_agent_is_inspected_and_clean_when_valid(tmp_path):
    good = agent("skills:\n  - cc10x:good\n").replace("\n", "\r\n")
    assert preload_errors(tmp_path, good) == []


def test_crlf_agent_missing_skill_is_found(tmp_path):
    bad = agent("skills:\n  - cc10x:ghost\n").replace("\n", "\r\n")
    assert any("ghost" in e for e in preload_errors(tmp_path, bad))


@pytest.mark.parametrize(
    "label,block",
    [
        ("tab indent", "skills:\n\t- cc10x:good\n"),
        ("scalar instead of list", "skills: cc10x:good\n"),
        ("mapping", "skills: {a: b}\n"),
        ("empty list", "skills:\n"),
        ("junk line in list", "skills:\n  - cc10x:good\n  junk\n"),
        ("empty item", "skills:\n  -\n"),
        ("unterminated flow", "skills: [cc10x:good\n"),
    ],
)
def test_unparseable_skills_value_fails_loudly(tmp_path, label, block):
    errors = preload_errors(tmp_path, agent(block))
    assert any("skills" in e for e in errors), (label, errors)


def test_agent_without_closed_frontmatter_fails_loudly(tmp_path):
    errors = preload_errors(tmp_path, "---\nname: a\nskills:\n  - cc10x:good\n")
    assert errors and "a.md" in errors[0]


def test_agent_without_frontmatter_fails_loudly(tmp_path):
    errors = preload_errors(tmp_path, "no frontmatter here\n")
    assert errors and "a.md" in errors[0]


@pytest.mark.parametrize(
    "flag",
    [
        "disable-model-invocation: true",
        "disable-model-invocation: True",
        "disable-model-invocation: TRUE",
        'disable-model-invocation: "true"',
        "disable-model-invocation: 'true'",
        "disable-model-invocation: true # internal",
        "disable-model-invocation:   true   ",
    ],
)
def test_disable_model_invocation_true_variants_flagged(tmp_path, flag):
    skills = {"bad": f"---\nname: bad\n{flag}\n---\nbody\n"}
    errors = preload_errors(tmp_path, agent("skills:\n  - cc10x:bad\n"), skills)
    assert any("disable-model-invocation" in e for e in errors), errors


def test_disable_model_invocation_false_not_flagged(tmp_path):
    skills = {"ok": "---\nname: ok\ndisable-model-invocation: false\n---\n"}
    assert preload_errors(tmp_path, agent("skills:\n  - cc10x:ok\n"), skills) == []


def test_bom_skill_with_disable_flag_flagged(tmp_path):
    skills = {"bad": "﻿---\nname: bad\ndisable-model-invocation: true\n---\n"}
    errors = preload_errors(tmp_path, agent("skills:\n  - cc10x:bad\n"), skills)
    assert any("disable-model-invocation" in e for e in errors), errors


def test_unparseable_disable_flag_fails_loudly(tmp_path):
    skills = {"odd": "---\nname: odd\ndisable-model-invocation: maybe\n---\n"}
    errors = preload_errors(tmp_path, agent("skills:\n  - cc10x:odd\n"), skills)
    assert any("disable-model-invocation" in e for e in errors), errors


def test_skill_block_scalar_description_is_tolerated(tmp_path):
    text = "---\nname: s\ndescription: |\n  line one\n  # not a comment\n\n  line two\nuser-invocable: false\n---\n"
    assert preload_errors(tmp_path, agent("skills:\n  - cc10x:s\n"), {"s": text}) == []


def test_empty_agents_dir_fails(tmp_path):
    agents_dir, skills_dir = tree(tmp_path, {}, {})
    errors = harness_audit.check_preloaded_skills_invocable(agents_dir, skills_dir)
    assert errors and "no agents" in errors[0]


def test_no_agent_declares_skills_fails(tmp_path):
    errors = preload_errors(tmp_path, "---\nname: a\ncolor: blue\n---\n")
    assert errors and "no agents" in errors[0]


def test_indented_skills_key_is_not_silently_skipped(tmp_path):
    errors = preload_errors(tmp_path, agent("  skills:\n    - cc10x:good\n"))
    assert errors


def color_errors(tmp_path, color_line):
    agents_dir, _ = tree(tmp_path, {"a": f"---\nname: a\n{color_line}\n---\n"}, {})
    return harness_audit.check_agent_colors(agents_dir)


@pytest.mark.parametrize(
    "line", ["color: blue", 'color: "blue"', "color: 'blue'", "color: blue # ok", "color:   blue  "]
)
def test_documented_color_variants_pass(tmp_path, line):
    assert color_errors(tmp_path, line) == []


@pytest.mark.parametrize("line", ["color: chartreuse", 'color: "chartreuse"', "color: [blue]"])
def test_bad_color_flagged(tmp_path, line):
    assert color_errors(tmp_path, line)


def test_bom_agent_bad_color_flagged(tmp_path):
    agents_dir, _ = tree(tmp_path, {"a": "﻿---\nname: a\ncolor: chartreuse\n---\n"}, {})
    assert harness_audit.check_agent_colors(agents_dir)


def test_colors_empty_dir_fails(tmp_path):
    agents_dir, _ = tree(tmp_path, {}, {})
    assert harness_audit.check_agent_colors(agents_dir)


def researcher_errors(tmp_path, text):
    agents_dir, _ = tree(tmp_path, {"researcher": text}, {})
    return harness_audit.check_researcher_mcp_lanes(agents_dir)


def test_researcher_lanes_present_passes(tmp_path):
    text = "---\nname: researcher\ntools: Read, mcp__brightdata, mcp__octocode # lanes\n---\n"
    assert researcher_errors(tmp_path, text) == []


def test_researcher_with_bom_is_read(tmp_path):
    text = "﻿---\nname: researcher\ntools: Read, mcp__brightdata, mcp__octocode\n---\n"
    assert researcher_errors(tmp_path, text) == []


def test_researcher_missing_lane_flagged(tmp_path):
    text = "---\nname: researcher\ntools: Read, mcp__brightdata\n---\n"
    assert any("mcp__octocode" in e for e in researcher_errors(tmp_path, text))


def test_researcher_block_list_tools_supported(tmp_path):
    text = "---\nname: researcher\ntools:\n  - Read\n  - mcp__brightdata\n  - mcp__octocode\n---\n"
    assert researcher_errors(tmp_path, text) == []


def test_researcher_missing_file_fails(tmp_path):
    agents_dir, _ = tree(tmp_path, {}, {})
    assert harness_audit.check_researcher_mcp_lanes(agents_dir)


import prompt_clause_assertions as pca  # noqa: E402


def agent_common_pin():
    return next(a for a in pca.ASSERTIONS if a.name.startswith("agent-common: user-invocable false"))


def test_user_invocable_pin_accepts_real_key():
    assert agent_common_pin().check("---\nname: x\nuser-invocable: false\n---\nbody\n") is True


@pytest.mark.parametrize(
    "text",
    [
        "---\nname: x\n# user-invocable: false\n---\nbody\n",
        "---\nname: x\n---\nuser-invocable: false\n",
        "---\nname: x\nuser-invocable: true\n---\n",
        "---\nname: x\nxuser-invocable: false\n---\n",
    ],
)
def test_user_invocable_pin_rejects_lookalikes(text):
    assert not agent_common_pin().check(text)


@pytest.mark.parametrize("text", ["", "no frontmatter", "---\nname: x\n", "---\n"])
def test_malformed_frontmatter_is_a_fail_not_a_crash(text):
    assert not agent_common_pin().check(text)


def test_assertion_runner_reports_malformed_file_as_failure(tmp_path):
    bad = tmp_path / "SKILL.md"
    bad.write_text("no frontmatter at all", encoding="utf-8")
    pin = agent_common_pin()
    assert pca.A(pin.name, bad, pin.check, pin.description).eval() is False


def test_duplicate_skills_key_fails_loudly(tmp_path):
    errors = preload_errors(tmp_path, agent("skills:\n  - cc10x:good\nskills:\n  - cc10x:good\n"))
    assert any("duplicate" in e for e in errors), errors


def test_duplicate_disable_flag_fails_loudly(tmp_path):
    text = "---\nname: s\ndisable-model-invocation: true\ndisable-model-invocation: false\n---\nbody\n"
    errors = preload_errors(tmp_path, agent("skills:\n  - cc10x:s\n"), {"s": text})
    assert any("duplicate" in e for e in errors), errors


def two_agent_errors(tmp_path, hidden_text):
    agents_dir, skills_dir = tree(
        tmp_path,
        {"a": agent("skills:\n  - cc10x:good\n"), "b": hidden_text},
        {"good": GOOD_SKILL.format(name="good")},
    )
    return harness_audit.check_preloaded_skills_invocable(agents_dir, skills_dir)


def test_skills_hidden_in_block_scalar_trips_coverage_cross_check(tmp_path):
    hidden = "---\nname: b\ndescription: |\n  skills:\n    - cc10x:ghost\n---\nbody\n"
    errors = two_agent_errors(tmp_path, hidden)
    assert any("1 of 2" in e for e in errors), errors


def test_bom_agent_with_skills_text_only_in_body_is_not_declared(tmp_path):
    body_only = "﻿---\nname: b\n---\nskills: not frontmatter\n"
    assert two_agent_errors(tmp_path, body_only) == []


def test_scalar_guard_rejects_block_scalar_indicators():
    for line in ("color: |", "color: >"):
        with pytest.raises(harness_audit.FrontmatterError):
            harness_audit.fm_scalar(harness_audit.parse_frontmatter(f"---\n{line}\n---\n"), "color")


@pytest.mark.parametrize("inline", ["[a, [b]]", "[a, {b: c}]"])
def test_flow_list_complexity_guard(inline):
    fields = harness_audit.parse_frontmatter(f"---\nskills: {inline}\n---\n")
    with pytest.raises(harness_audit.FrontmatterError, match="too complex"):
        harness_audit.fm_list(fields, "skills")


def test_mixed_inline_and_indented_list_guard():
    fields = harness_audit.parse_frontmatter("---\nskills: [a]\n  - b\n---\n")
    with pytest.raises(harness_audit.FrontmatterError, match="mixes"):
        harness_audit.fm_list(fields, "skills")


def test_frontmatter_must_open_on_first_line():
    with pytest.raises(harness_audit.FrontmatterError, match="must start"):
        harness_audit.parse_frontmatter("junk\n---\nname: a\n---\n")
