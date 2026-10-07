#!/usr/bin/env python3
"""Static prompt-clause assertions for cc10x skill bodies.

The router-contract fixtures (tests/fixtures/*.json + workflow_replay_check.py)
validate contract-envelope SHAPE, not skill CONTENT. This script greps each
modified skill/agent file for required clauses so a swapped/edited skill body
cannot pass silently with wrong or missing content.

Exit 0 only when all assertions pass; exit 1 with a named failure on any miss.
Deterministic — no network, no agent load.

Usage: python3 plugins/cc10x/tools/prompt_clause_assertions.py [--allow-no-yaml]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from harness_audit import FrontmatterError, fm_scalar, parse_frontmatter

if os.environ.get("CC10X_REPO_ROOT") == "":
    raise SystemExit("CC10X_REPO_ROOT is set but empty: unset it or point it at a cc10x repo")
ROOT = Path(os.environ.get("CC10X_REPO_ROOT") or Path(__file__).resolve().parents[3])
if not (ROOT / "plugins" / "cc10x").is_dir():
    raise SystemExit(f"CC10X_REPO_ROOT is not a cc10x repo (no plugins/cc10x): {ROOT}")
PLUGIN = ROOT / "plugins" / "cc10x"
SKILLS = PLUGIN / "skills"
AGENTS = PLUGIN / "agents"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class A:
    def __init__(self, name: str, path: Path, check, description: str):
        self.name, self.path, self.check, self.description = (
            name,
            path,
            check,
            description,
        )

    def eval(self) -> bool:
        try:
            return bool(self.check(read(self.path)))
        except FileNotFoundError:
            return False


def contains(needle: str):
    return lambda text: needle in text


def contains_all(*needles):
    return lambda text: all(n in text for n in needles)


def contains_none(*needles):
    return lambda text: all(n not in text for n in needles)


def matches(pattern: str):
    return lambda text: re.search(pattern, text) is not None


def skill_description(text: str) -> str:
    """The frontmatter `description` value (quoted, block or folded scalar) as one whitespace-normalized string."""
    block = re.match(r"---\n(.*?)\n---", text, re.S)
    if block is None:
        return ""
    lines = block.group(1).splitlines()
    for i, line in enumerate(lines):
        if line.startswith("description:"):
            out = [line[len("description:"):].strip()]
            for follow in lines[i + 1:]:
                if re.match(r"[A-Za-z][\w-]*:", follow):
                    break
                out.append(follow.strip())
            return " ".join(" ".join(out).strip("|>-\"' ").split())
    return ""


def frontmatter_is(key: str, value: str):
    """True only when the frontmatter block has `key: value` as a real key; malformed frontmatter is False."""

    def check(text: str) -> bool:
        try:
            return parse_frontmatter(text).get(key, (None, []))[0] == value
        except FrontmatterError:
            return False

    return check


def frontmatter_skills_are(*expected: str):
    """True only when the frontmatter `skills:` list is exactly `expected` (order-free); malformed frontmatter is False."""

    def check(text: str) -> bool:
        try:
            listed = parse_frontmatter(text).get("skills", (None, []))[1]
        except FrontmatterError:
            return False
        return sorted(item.strip().lstrip("- ").strip() for item in listed) == sorted(expected)

    return check


def frontmatter_tools_exclude(tool: str):
    """True only when frontmatter has a parseable `tools:` scalar and `tool` is not one of its entries."""

    def check(text: str) -> bool:
        try:
            listed = fm_scalar(parse_frontmatter(text), "tools")
        except FrontmatterError:
            return False
        return listed is not None and tool not in [item.strip() for item in listed.split(",")]

    return check


def frontmatter_tools_include(*tools: str):
    """True only when frontmatter has a parseable `tools:` scalar naming every one of `tools`."""

    def check(text: str) -> bool:
        try:
            listed = fm_scalar(parse_frontmatter(text), "tools")
        except FrontmatterError:
            return False
        return listed is not None and set(tools) <= {item.strip() for item in listed.split(",")}

    return check


def router_description(text: str) -> str:
    return text.split("\n---", 1)[0].split("description:", 1)[1] if text.startswith("---") and "description:" in text else ""


POLICY_REF = SKILLS / "cc10x-router" / "references" / "workflow-artifact-and-hook-policy.md"
ROUTER_REFS = SKILLS / "cc10x-router" / "references"
ROUTER_EVALS = SKILLS / "cc10x-router" / "evals"
PRELOAD_TABLE = {
    "architecture-scanner": ("agent-common", "codebase-hygiene", "codebase-design"),
    "bug-investigator": ("agent-common", "debugging", "building", "verification", "codebase-design"),
    "code-reviewer": ("agent-common", "code-review", "verification", "codebase-design"),
    "component-builder": ("agent-common", "building", "verification", "codebase-design", "domain-modeling"),
    "doc-syncer": ("agent-common", "diff-driven-docs", "verification", "domain-modeling"),
    "failure-hunter": ("agent-common", "code-review"),
    "integration-verifier": ("agent-common", "verification"),
    "plan-gap-reviewer": (),
    "planner": ("agent-common", "planning", "codebase-design", "domain-modeling"),
    "qa-executor": ("agent-common", "qa-strategy", "verification"),
    "qa-harness-builder": ("agent-common", "qa-strategy", "verification"),
    "qa-researcher": ("agent-common", "qa-strategy"),
    "researcher": ("agent-common",),
    "triage-agent": ("agent-common", "domain-modeling"),
}
POLICY_TABLE_AGENTS = (
    "component-builder",
    "bug-investigator",
    "planner",
    "researcher",
    "doc-syncer",
    "code-reviewer",
    "failure-hunter",
    "integration-verifier",
    "triage-agent",
    "architecture-scanner",
    "qa-harness-builder",
    "qa-executor",
)


def policy_required_rows(text: str) -> dict[str, str]:
    section = text.split("### Write-agent YAML required fields", 1)[-1].split("### Contract overrides", 1)[0]
    rows = {}
    for line in section.splitlines():
        if line.startswith("| ") and not line.startswith(("| Agent", "| ---")):
            cells = [c.strip() for c in line.strip().strip("|").split("|", 1)]
            rows[cells[0]] = cells[1]
    return rows


def agent_yaml_keys(agent: str) -> set[str]:
    text = read(AGENTS / f"{agent}.md")
    keys: set[str] = set()
    for block in re.findall(r"```yaml\n(.*?)```", text, re.S):
        keys |= set(re.findall(r"^([A-Z][A-Z0-9_]+):", block, re.M))
    return keys


def yaml_has_keys(*keys: str):
    """True when every key is a top-level key of some fenced yaml block in the text."""

    def check(text: str) -> bool:
        found: set[str] = set()
        for block in re.findall(r"```yaml\n(.*?)```", text, re.S):
            found |= set(re.findall(r"^([A-Z][A-Z0-9_]+):", block, re.M))
        return set(keys) <= found

    return check


def policy_table_matches_agents(text: str) -> bool:
    rows = policy_required_rows(text)
    if set(POLICY_TABLE_AGENTS) - set(rows):
        return False
    for agent, cell in rows.items():
        named = set(re.findall(r"`([A-Z][A-Z0-9_]+)`", cell))
        if not named <= agent_yaml_keys(agent):
            return False
    return True


ALLOW_NO_YAML = False
YAML_SKIPS = [0]
YAML_HINT = (
    "PyYAML is not importable: install it (pip install pyyaml, or run through "
    "`uv run --no-project --with pyyaml`) or pass --allow-no-yaml to skip the YAML parse check"
)


def yaml_alternatives_parse(marker: str, expected_blocks: int):
    """True when exactly expected_blocks fenced yaml blocks contain marker and each parses.

    Without PyYAML the parse cannot run: that is a FAIL with an install hint, because a
    silent pass hid broken yaml on interpreters that lack it. --allow-no-yaml opts out.
    """

    def check(text: str) -> bool:
        try:
            import yaml
        except ImportError:
            if ALLOW_NO_YAML:
                YAML_SKIPS[0] += 1
                return True
            print(YAML_HINT)
            return False
        blocks = [
            b for b in re.findall(r"```yaml\n(.*?)```", text, re.S) if marker in b
        ]
        if len(blocks) != expected_blocks:
            return False
        for block in blocks:
            try:
                yaml.safe_load(block)
            except yaml.YAMLError:
                return False
        return True

    return check


ASSERTIONS = [
    A(
        "router routing table: priority-5 QA row",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains(
            '| 5 | QA | test, QA, e2e, end-to-end, integration test, test plan, test coverage, regression, smoke test, "verify my feature", "prove it works" | QA | qa-researcher (fan-out) → qa-plan → plan-gap-reviewer → qa-preflight → qa-harness-builder → [code-reviewer ‖ failure-hunter] → qa-executor |'
        ),
        "the QA workflow keeps priority 5, its trigger keywords and its full agent chain in the routing table",
    ),
    # building — Seam Discipline (ticket #40)
    A(
        "building: one-seam-one-test cycle",
        SKILLS / "building" / "SKILL.md",
        contains("seam, one test"),
        "Seam Discipline subsection present",
    ),
    A(
        "building: implementation-coupled anti-pattern",
        SKILLS / "building" / "SKILL.md",
        contains("implementation-coupled"),
        "implementation-coupled anti-pattern present",
    ),
    A(
        "building: TEST_SEAMS + SEAM_GATE_STATUS (enforced)",
        SKILLS / "building" / "SKILL.md",
        contains_all(
            "TEST_SEAMS",
            "SEAM_GATE_STATUS",
            "confirmed",
            "proposed",
            "disagreed",
            "not_applicable",
        ),
        "builder records enforced seam-gate contract fields + 4 statuses",
    ),
    # component-builder contract — enforced seam gate (sub-project 2a)
    A(
        "component-builder: enforced seam-gate fields in contract",
        AGENTS / "component-builder.md",
        contains_all(
            "TEST_SEAMS",
            "SEAM_GATE_STATUS",
            "confirmed",
            "proposed",
            "disagreed",
            "not_applicable",
        ),
        "builder contract has the enforced seam-gate fields + 4 statuses",
    ),
    # workflow-artifact-and-hook-policy — enforced gate + pre-existing gap fixes (sub-project 2a)
    A(
        "policy: component-builder seam-gate override",
        PLUGIN
        / "skills"
        / "cc10x-router"
        / "references"
        / "workflow-artifact-and-hook-policy.md",
        contains_all(
            "SEAM_GATE_STATUS", "confirmed", "proposed", "disagreed", "not_applicable"
        ),
        "override enforces the 4 seam-gate statuses per build_scope",
    ),
    A(
        "policy: non-empty TDD_RED_REASON enforced",
        PLUGIN
        / "skills"
        / "cc10x-router"
        / "references"
        / "workflow-artifact-and-hook-policy.md",
        contains("non-empty `TDD_RED_REASON`"),
        "override requires non-empty TDD_RED_REASON for behavioral RED (gap fix)",
    ),
    A(
        "policy: bug-investigator feedback loop + closeout enforced",
        PLUGIN
        / "skills"
        / "cc10x-router"
        / "references"
        / "workflow-artifact-and-hook-policy.md",
        contains_all(
            "FEEDBACK_LOOP.rung",
            "DEBUG_CLOSEOUT.instrumentation_removed",
            "DEBUG_CLOSEOUT.repro_no_longer_fires",
        ),
        "override requires feedback loop + debug close-out for FIXED (gap fix)",
    ),
    A(
        "policy: planner >=2 alternatives for decision_rfc",
        PLUGIN
        / "skills"
        / "cc10x-router"
        / "references"
        / "workflow-artifact-and-hook-policy.md",
        contains("length ≥2"),
        "override requires >=2 alternatives for decision_rfc (gap fix)",
    ),
    # resolving-merge-conflicts skill (sub-project 2a)
    A(
        "resolving-merge-conflicts: exists with 5 steps + never-abort",
        SKILLS / "resolving-merge-conflicts" / "SKILL.md",
        contains_all(
            "See the current state",
            "Find the primary sources",
            "Resolve each hunk",
            "Run the project's automated checks",
            "Finish the merge",
            "Never `--abort`.",
        ),
        "resolving-merge-conflicts skill has all 5 steps (incl. run checks) + never-abort rule",
    ),
    # sub-project 2b — TRIAGE + CODEBASE-HEALTH routing + agents
    A(
        "router: TRIAGE route row anchored",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 6 | TRIAGE | triage, \"incoming issues\", \"look at #\", \"triage #\" | TRIAGE | triage-agent",
        ),
        "TRIAGE row anchored with non-colliding keywords + chain",
    ),
    A(
        "router: CODEBASE-HEALTH route row anchored",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 7 | CODEBASE-HEALTH | \"codebase health\", \"improve architecture\", \"deepening\", \"ball of mud\", \"shallow modules\", \"architecture audit\" | CODEBASE-HEALTH | architecture-scanner",
        ),
        "CODEBASE-HEALTH row anchored with non-colliding keywords + chain",
    ),
    A(
        "router: TRIAGE keywords do not collide with ERROR",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_none("\"bug report\"", "\"issue #\"", "\"feature request\""),
        "TRIAGE keywords do not include bug report/issue #/feature request (would collide with ERROR/steal BUILD)",
    ),
    A(
        "router: CODEBASE-HEALTH keywords do not collide with REVIEW",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_none("\"audit architecture\""),
        "CODEBASE-HEALTH keywords do not include audit architecture (would collide with REVIEW's audit)",
    ),
    A(
        "router: priority 1-4 rows anchored unchanged",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue | DEBUG | bug-investigator -> code-reviewer -> integration-verifier |",
            "| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, brainstorm | PLAN | exploration -> planner -> bounded fresh review loop |",
            "| 3 | REVIEW | review, audit, analyze, assess, \"is this good\" | REVIEW | code-reviewer |",
            "| 4 | ORIENT | zoom out, explain, understand, \"how does X work\", unfamiliar, \"map this\", \"walk me through\", \"where is\", \"what does this do\" | ORIENT | advisory orientation (no agents) |",
        ),
        "priority 1-4 rows byte-for-byte anchored (ERROR/PLAN/REVIEW/ORIENT unchanged)",
    ),
    A(
        "router: DEFAULT row anchored at priority 8",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 8 | DEFAULT | Everything else | BUILD | component-builder",
        ),
        "DEFAULT row at priority 8 with BUILD chain unchanged",
    ),
    A(
        "router: TRIAGE primary-deliverable rule",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all("Primary-deliverable rule", "TRIAGE applies only when triage", "asks to implement/fix/change it is BUILD or DEBUG"),
        "TRIAGE primary-deliverable rule prevents BUILD-stealing",
    ),
    A(
        "router: CODEBASE-HEALTH primary-deliverable rule",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all("CODEBASE-HEALTH applies only when discovery", "refactor/fix/change specific code is BUILD"),
        "CODEBASE-HEALTH primary-deliverable rule prevents BUILD-stealing",
    ),
    A(
        "router: TRIAGE advisory-only rule",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all("TRIAGE is advisory-only", "never auto-routes"),
        "TRIAGE advisory-only rule present",
    ),
    A(
        "router: CODEBASE-HEALTH advisory-only rule",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all("CODEBASE-HEALTH is advisory-only upkeep", "never writes code"),
        "CODEBASE-HEALTH advisory-only rule present",
    ),
    A(
        "triage-agent: read-only tools + YAML contract + no TaskUpdate",
        AGENTS / "triage-agent.md",
        contains_all(
            "tools: Read, Bash, Grep, Glob, Skill, LSP, WebFetch",
            "STATUS: TRIAGED | NEEDS_INFO | WONTFIX",
            "CATEGORY:",
            "STATE:",
            "BRIEF_PATH:",
            "cc10x:domain-modeling",
        ),
        "triage-agent has read-only tools (no TaskUpdate), YAML contract with STATUS/CATEGORY/STATE/BRIEF_PATH, loads domain-modeling (codebase-hygiene preload dropped by C4.3)",
    ),
    A(
        "triage-agent: no Edit/TaskUpdate in tools line",
        AGENTS / "triage-agent.md",
        lambda text: "Edit" not in text.split("tools:", 1)[1].split("\n", 1)[0] and "TaskUpdate" not in text.split("tools:", 1)[1].split("\n", 1)[0],
        "triage-agent tools line has no Edit/TaskUpdate (read-only, router-owned completion)",
    ),
    A(
        "architecture-scanner: read-only tools (Write for temp only) + YAML contract",
        AGENTS / "architecture-scanner.md",
        contains_all(
            "tools: Read, Bash, Grep, Glob, Skill, LSP, Write",
            "STATUS: CANDIDATES_FOUND | NO_CANDIDATES",
            "CANDIDATES:",
            "REPORT_PATH:",
            "cc10x:codebase-design",
            "deletion test",
        ),
        "architecture-scanner has Write (temp HTML only) + YAML contract with STATUS/CANDIDATES/REPORT_PATH + canonical vocab",
    ),
    A(
        "architecture-scanner: no Edit/TaskUpdate in tools line",
        AGENTS / "architecture-scanner.md",
        lambda text: "Edit" not in text.split("tools:", 1)[1].split("\n", 1)[0] and "TaskUpdate" not in text.split("tools:", 1)[1].split("\n", 1)[0],
        "architecture-scanner tools line has no Edit/TaskUpdate (read-only source, router-owned completion)",
    ),
    A(
        "triage-workflow reference exists",
        PLUGIN / "skills" / "cc10x-router" / "references" / "triage-workflow.md",
        contains_all("TRIAGE workflow", "dvisory-only", "triage-agent"),
        "triage-workflow.md reference exists",
    ),
    A(
        "codebase-health-workflow reference exists",
        PLUGIN
        / "skills"
        / "cc10x-router"
        / "references"
        / "codebase-health-workflow.md",
        contains_all(
            "CODEBASE-HEALTH workflow", "dvisory-only", "architecture-scanner"
        ),
        "codebase-health-workflow.md reference exists",
    ),
    # codebase-hygiene — deletion test fixed (ticket #38)
    A(
        "codebase-hygiene: deletion test not inverted",
        SKILLS / "codebase-hygiene" / "SKILL.md",
        contains("pass-through"),
        "deletion test says vanishes -> pass-through",
    ),
    A(
        "codebase-hygiene: no 'earning its keep' near vanishes",
        SKILLS / "codebase-hygiene" / "SKILL.md",
        contains_none("earning its keep"),
        "inverted verdict removed",
    ),
    # architecture — deduped, points to codebase-design (ticket #38)
    A(
        "architecture: no duplicated vocab table",
        SKILLS / "architecture" / "SKILL.md",
        contains_none("Ousterhout's \"A Philosophy of Software Design"),
        "duplicated Ousterhout vocabulary table removed",
    ),
    A(
        "architecture: points to codebase-design",
        SKILLS / "architecture" / "SKILL.md",
        contains("cc10x:codebase-design"),
        "architecture references canonical codebase-design",
    ),
    # codebase-design — canonical skill exists (ticket #37)
    A(
        "codebase-design: exists with glossary",
        SKILLS / "codebase-design" / "SKILL.md",
        contains_all(
            "Module", "Interface", "Depth", "Seam", "Adapter", "Leverage", "Locality"
        ),
        "canonical glossary terms present",
    ),
    A(
        "codebase-design: no broken companion refs",
        SKILLS / "codebase-design" / "SKILL.md",
        contains_all("DEEPENING.md", "DESIGN-IT-TWICE.md"),
        "companion references present (files ported)",
    ),
    A(
        "codebase-design: DEEPENING.md exists",
        SKILLS / "codebase-design" / "DEEPENING.md",
        contains("Deepening"),
        "DEEPENING companion ported",
    ),
    A(
        "codebase-design: DESIGN-IT-TWICE.md exists",
        SKILLS / "codebase-design" / "DESIGN-IT-TWICE.md",
        contains("Design It Twice"),
        "DESIGN-IT-TWICE companion ported",
    ),
    # domain-modeling — autonomous transform (ticket #37)
    A(
        "domain-modeling: exists with autonomous transform",
        SKILLS / "domain-modeling" / "SKILL.md",
        contains_all(
            "evidence + blast radius",
            "NOT auto-answered",
            "READ-ONLY",
            "NEEDS_CLARIFICATION",
        ),
        "autonomous transform rules present",
    ),
    A(
        "domain-modeling: no broken companion refs",
        SKILLS / "domain-modeling" / "SKILL.md",
        contains_all("CONTEXT-FORMAT.md", "ADR-FORMAT.md"),
        "companion references present (files ported)",
    ),
    A(
        "domain-modeling: CONTEXT-FORMAT.md exists",
        SKILLS / "domain-modeling" / "CONTEXT-FORMAT.md",
        contains("CONTEXT.md Format"),
        "CONTEXT-FORMAT companion ported",
    ),
    A(
        "domain-modeling: ADR-FORMAT.md exists",
        SKILLS / "domain-modeling" / "ADR-FORMAT.md",
        contains("ADR Format"),
        "ADR-FORMAT companion ported",
    ),
    A(
        "agent-common: user-invocable false so agent preload delivers it",
        SKILLS / "agent-common" / "SKILL.md",
        frontmatter_is("user-invocable", "false"),
        "frontmatter must hide the skill instead of disable-model-invocation (agent skills: preload skips disabled skills)",
    ),
    # agent-common — read-only glossary, no mutation (ticket #39)
    A(
        "agent-common: read CONTEXT.md rule",
        SKILLS / "agent-common" / "SKILL.md",
        contains("CONTEXT.md` at the repo root"),
        "read-only glossary rule present",
    ),
    A(
        "agent-common: prohibits mutation",
        SKILLS / "agent-common" / "SKILL.md",
        contains("Do NOT write or edit `CONTEXT.md`"),
        "explicit prohibition on writing/editing CONTEXT.md",
    ),
    # planning — Test Seams augmented + Wide-Refactor (ticket #42)
    A(
        "planning: prefer existing seams",
        SKILLS / "planning" / "SKILL.md",
        contains_all("Prefer existing seams", "ideal number is one"),
        "Test-Seam section augmented with prefer-existing/ideal=1",
    ),
    A(
        "planning: seams feed the enforced builder gate",
        SKILLS / "planning" / "SKILL.md",
        contains("feed the builder's **enforced** seam gate"),
        "planned seams are the starting contract for the enforced SEAM_GATE_STATUS gate",
    ),
    A(
        "planning: Wide-Refactor Phasing",
        SKILLS / "planning" / "SKILL.md",
        contains_all("Wide-Refactor Phasing", "expand", "contract"),
        "expand-contract wide-refactor section present",
    ),
    # debugging — tighten-loop + red-capable + REPL + perf + cleanup (ticket #43)
    A(
        "debugging: tighten-the-loop",
        SKILLS / "debugging" / "SKILL.md",
        contains_all("Tighten the loop", "Faster", "Sharper", "deterministic"),
        "tighten-the-loop tactics present",
    ),
    A(
        "debugging: red-capable completion criteria",
        SKILLS / "debugging" / "SKILL.md",
        contains_all("Red-capable", "Deterministic", "Fast", "Agent-runnable"),
        "red-capable 4-checkbox completion criteria present",
    ),
    A(
        "debugging: REPL/debugger-first",
        SKILLS / "debugging" / "SKILL.md",
        matches(r"Debugger / REPL inspection|debugger / REPL|REPL inspection"),
        "debugger/REPL-first instrumentation preference present",
    ),
    A(
        "debugging: perf branch",
        SKILLS / "debugging" / "SKILL.md",
        contains_all("Performance branch", "baseline measurement"),
        "measurement-first performance branch present",
    ),
    A(
        "debugging: throwaway cleanup",
        SKILLS / "debugging" / "SKILL.md",
        contains("Cleanup"),
        "Phase 4 cleanup step present",
    ),
    # exploration — active domain-term challenge (ticket #44)
    A(
        "exploration: challenge domain terms",
        SKILLS / "exploration" / "SKILL.md",
        contains_all("Challenge domain terms", "CONTEXT.md", "contradiction"),
        "active domain-term challenge step present in DESIGN mode",
    ),
    # doc-syncer + diff-driven-docs — docs/adr/ canonical (ticket #45)
    A(
        "doc-syncer: docs/adr/ canonical",
        AGENTS / "doc-syncer.md",
        contains("docs/adr/"),
        "doc-syncer targets docs/adr/",
    ),
    A(
        "doc-syncer: NNNN convention",
        AGENTS / "doc-syncer.md",
        contains("NNNN"),
        "NNNN-numbered ADR filename convention",
    ),
    A(
        "doc-syncer: 4 layers evaluated",
        AGENTS / "doc-syncer.md",
        contains_all("business", "technical", "audit", "glossary"),
        "DOC_LAYERS_EVALUATED includes all 4 layers",
    ),
    A(
        "diff-driven-docs: docs/adr/ canonical",
        SKILLS / "diff-driven-docs" / "SKILL.md",
        contains("docs/adr/"),
        "diff-driven-docs targets docs/adr/",
    ),
    A(
        "diff-driven-docs: glossary layer",
        SKILLS / "diff-driven-docs" / "SKILL.md",
        contains_all("Glossary Layer", "CONTEXT.md", "Glossary Layer |", "four layers"),
        "CONTEXT.md listed as a 4th classifier layer (glossary)",
    ),
    # code-reviewer — 12 smells incl Refused Bequest + codebase-design load (ticket #41)
    A(
        "code-reviewer: all 12 smells",
        AGENTS / "code-reviewer.md",
        contains_all(
            "Mysterious Name",
            "Duplicated Code",
            "Feature Envy",
            "Data Clumps",
            "Primitive Obsession",
            "Repeated Switches",
            "Shotgun Surgery",
            "Divergent Change",
            "Speculative Generality",
            "Message Chains",
            "Middle Man",
            "Refused Bequest",
        ),
        "all 12 Fowler smells inline including Refused Bequest",
    ),
    A(
        "code-reviewer: loads codebase-design",
        AGENTS / "code-reviewer.md",
        contains("cc10x:codebase-design"),
        "codebase-design in frontmatter skills",
    ),
    # frontmatter skills changes (ticket #46)
    A(
        "component-builder: loads codebase-design + domain-modeling",
        AGENTS / "component-builder.md",
        contains_all("cc10x:codebase-design", "cc10x:domain-modeling"),
        "builder frontmatter loads both new skills",
    ),
    A(
        "bug-investigator: loads codebase-design",
        AGENTS / "bug-investigator.md",
        contains("cc10x:codebase-design"),
        "investigator frontmatter loads codebase-design",
    ),
    A(
        "planner: loads codebase-design + domain-modeling",
        AGENTS / "planner.md",
        contains_all("cc10x:codebase-design", "cc10x:domain-modeling"),
        "planner frontmatter loads both new skills",
    ),
    A(
        "doc-syncer: loads domain-modeling",
        AGENTS / "doc-syncer.md",
        contains("cc10x:domain-modeling"),
        "doc-syncer frontmatter loads domain-modeling",
    ),
    # read-only agents unchanged (ticket #46 negative checks)
    A(
        "failure-hunter: no new skills",
        AGENTS / "failure-hunter.md",
        contains_none("cc10x:codebase-design", "cc10x:domain-modeling"),
        "failure-hunter frontmatter unchanged (read-only)",
    ),
    A(
        "integration-verifier: no new skills",
        AGENTS / "integration-verifier.md",
        contains_none("cc10x:codebase-design", "cc10x:domain-modeling"),
        "integration-verifier frontmatter unchanged (read-only)",
    ),
    # --- Router kernel reconciliation (ticket #69) ---
    A(
        "router: phase enum covers triage + codebase-health",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("research-github|triage|codebase-health}"),
        "task-metadata phase enum includes the TRIAGE and CODEBASE-HEALTH phases their workflows create",
    ),
    A(
        "router: dispatcher row for triage-agent",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all("| `triage` | `cc10x:triage-agent` |"),
        "dispatcher table alone resolves phase:triage",
    ),
    A(
        "router: dispatcher row for architecture-scanner",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all("| `codebase-health` | `cc10x:architecture-scanner` |"),
        "dispatcher table alone resolves phase:codebase-health",
    ),
    A(
        "router: routing table carries primary-deliverable tie-break",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("A keyword hit only NOMINATES a row"),
        "keyword table is explicitly subordinate to the primary-deliverable rules",
    ),
    A(
        "router: ORIENT artifact rule single-voiced",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("no NEW workflow artifact"),
        "ORIENT law reconciles with the pre-created-artifact enum entries",
    ),
    A(
        "router: events-log append mechanism explicit",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "NEVER `Write` only the new line",
            "Write it back with the new line added at the end",
        ),
        "a literal reading of the append instruction cannot overwrite the event log",
    ),
    A(
        "router: single verifier-handoff template",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: text.count("**Critical Issues:**") == 2,
        "the Previous Agent Findings template exists exactly once (dispatcher section points at §13)",
    ),
    A(
        "router: circuit breaker single-sourced",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_none("more than 3 cycles"),
        "kernel defers to the >= 3 circuit breaker in remediation-and-research.md",
    ),
    A(
        "remediation: no undefined cycle-cap gate",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_none("cycle-cap gate"),
        "re-review loop references the defined circuit breaker, not an undefined gate name",
    ),
    A(
        "remediation: re-review loop numbering coherent",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "3. Create a re-hunt task",
            "4. Reuse the pending verifier",
            "7. Increment telemetry loop counters",
        ),
        "ordered steps 1-7 are unique so cross-references resolve unambiguously",
    ),
    A(
        "policy: every router gate operationally defined",
        SKILLS / "cc10x-router" / "references" / "workflow-artifact-and-hook-policy.md",
        contains_all(
            "`plan_trust_gate` —",
            "`phase_exit_gate` —",
            "`failure_stop_gate` —",
            "`memory_sync_gate` —",
            "`skill_precedence_gate` —",
        ),
        "no router gate exists as a bare name without semantics",
    ),
    A(
        "policy: reviewer rubber-stamp override deduplicated",
        SKILLS / "cc10x-router" / "references" / "workflow-artifact-and-hook-policy.md",
        lambda text: text.count("fewer than 3 file:line evidence citations") == 1,
        "the code-reviewer zero-findings override row appears exactly once",
    ),
    # --- Build workflow + skeleton reconciliation (ticket #70) ---
    A(
        "build: escalation rule includes the failure-hunter",
        SKILLS / "cc10x-router" / "references" / "build-workflow.md",
        contains_all(
            "never skip the hunter on escalation",
            "they are one rule, not two",
        ),
        "trivial->full escalation is a single rule that always adds the failure-hunter",
    ),
    A(
        "build: preparation list numbering coherent",
        SKILLS / "cc10x-router" / "references" / "build-workflow.md",
        contains_all(
            "12. Builder may execute only the phase at `phase_cursor`.",
            "13. Router handoff for the current BUILD phase must be phase-local:",
        ),
        "the 1-13 preparation sequence has no duplicate step numbers",
    ),
    A(
        "skeleton: carries BUILD/DEBUG state fields",
        SKILLS / "cc10x-router" / "references" / "workflow-artifact.skeleton.json",
        contains_all(
            '"build_scope"',
            '"worktree"',
            '"execution_mode"',
            '"git_preflight"',
            '"baseline"',
            '"git_base_sha"',
            '"doc_syncer"',
            '"finishing"',
            '"final_branch_review"',
        ),
        "the canonical skeleton includes the fields BUILD/DEBUG workflows persist",
    ),
    # --- Agent contract unification + prompt fixes (tickets #71/#72) ---
    # 71.1 — every agent prescribes the canonical envelope + fenced-YAML shape
    *[
        A(
            f"{stem}: canonical envelope + fenced YAML contract",
            AGENTS / f"{stem}.md",
            contains_all('CONTRACT {"s":', "```yaml"),
            "output section shows the line-1 CONTRACT envelope and a fenced yaml Router Contract block",
        )
        for stem in (
            "architecture-scanner",
            "bug-investigator",
            "code-reviewer",
            "component-builder",
            "doc-syncer",
            "failure-hunter",
            "integration-verifier",
            "plan-gap-reviewer",
            "planner",
            "researcher",
            "triage-agent",
        )
    ],
    A(
        "agent-common: canonical shape prescribed once for the fleet",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all(
            "fenced ```yaml Router Contract block",
            "never call a tool (including TaskUpdate) after emitting it",
        ),
        "agent-common mandates envelope + fenced-YAML shape and forbids post-contract tool calls",
    ),
    # 71.2 — worked examples show the envelope FIRST
    A(
        "architecture-scanner: example shows envelope before YAML block",
        AGENTS / "architecture-scanner.md",
        lambda text: 0
        <= text.find('CONTRACT {"s":"CANDIDATES_FOUND"')
        < text.find("STATUS: CANDIDATES_FOUND | NO_CANDIDATES"),
        "worked example emits the CONTRACT envelope before the Router Contract YAML",
    ),
    A(
        "triage-agent: example shows envelope before YAML block",
        AGENTS / "triage-agent.md",
        lambda text: 0
        <= text.find('CONTRACT {"s":"TRIAGED"')
        < text.find("STATUS: TRIAGED | NEEDS_INFO | WONTFIX"),
        "worked example emits the CONTRACT envelope before the Router Contract YAML",
    ),
    # 71.3 — no agent instructs tool calls after the final contract response
    # 71.4 — verifier per-finding validation is a single merged paragraph
    A(
        "integration-verifier: single per-finding validation paragraph",
        AGENTS / "integration-verifier.md",
        lambda text: text.count("Per-finding validation (MANDATORY") == 1
        and all(
            n in text
            for n in ("validated: true", "validated: false", "validated: degraded")
        ),
        "the two near-duplicate validation paragraphs are merged, keeping the validated taxonomy",
    ),
    # 72.5 — reviewer CONFIDENCE worked example obeys its own formula
    A(
        "code-reviewer: CONFIDENCE example arithmetic is valid",
        AGENTS / "code-reviewer.md",
        contains_all(
            "performance: [SOFT] 95",
            "maintainability: [SOFT] 95",
            "CONFIDENCE: 85  (min HARD=85, avg SOFT=95 → cap 85)",
        ),
        "worked example: min(HARD)=85 within avg(SOFT)-10=85 cap, so CONFIDENCE 85 is valid",
    ),
    # 72.6 — hunter settles the verdict before emitting, no revision of line 1
    A(
        "failure-hunter: single-emission verdict (no preliminary/revise)",
        AGENTS / "failure-hunter.md",
        lambda text: "Decide the verdict BEFORE writing the final response" in text
        and "line 1 cannot be revised" in text
        and "both are preliminary" not in text
        and "Revise BOTH" not in text,
        "step 0 computes the final verdict internally and emits the envelope exactly once",
    ),
    # 72.7 — planner has an honest path when open decisions remain
    A(
        "planner: open decisions route to NEEDS_CLARIFICATION",
        AGENTS / "planner.md",
        contains_all(
            "If OPEN_DECISIONS is non-empty:",
            "STATUS MUST be `NEEDS_CLARIFICATION`",
            "USER_INPUT_NEEDED",
            "Never present an open decision as settled",
        ),
        "non-empty OPEN_DECISIONS must return NEEDS_CLARIFICATION with the decisions in USER_INPUT_NEEDED",
    ),
    # 72.8 — bug-investigator memory-write carve-out declared in agent-common
    A(
        "agent-common: bug-investigator [DEBUG-N] carve-out",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all("Sole carve-out:", "[DEBUG-N]", "## Debug History"),
        "memory-ownership ban carries the narrow bug-investigator Debug History carve-out",
    ),
    A(
        "bug-investigator: [DEBUG-N] tracking cites the carve-out anchor",
        AGENTS / "bug-investigator.md",
        contains_all("## Debug History", "sole memory-write carve-out"),
        "debug attempt tracking appends under ## Debug History per the agent-common carve-out",
    ),
    # 72.9 — triage-agent can Write, scoped to .scratch/ and .out-of-scope/
    A(
        "triage-agent: Write tool present and scoped",
        AGENTS / "triage-agent.md",
        lambda text: ", Write" in text.split("tools:", 1)[1].split("\n", 1)[0]
        and "ONLY under `.scratch/` and `.out-of-scope/`" in text,
        "Write in frontmatter tools, prompt law scopes it to .scratch/ and .out-of-scope/ only",
    ),
    # 72.10 — red-flags reference relocated out of the agent auto-registration path
    A(
        "silent-failure-red-flags: lives under skills/agent-common/references",
        SKILLS / "agent-common" / "references" / "silent-failure-red-flags.md",
        contains("Silent Failure Red Flags"),
        "red-flags reference exists at the non-agent path",
    ),
    A(
        "silent-failure-red-flags: absent from agents/references",
        SKILLS / "agent-common" / "references" / "silent-failure-red-flags.md",
        lambda text: not (AGENTS / "references" / "silent-failure-red-flags.md").exists(),
        "agents/references/ no longer contains the file, so it cannot register as an all-tools agent",
    ),
    # 72.11 — BUILD_PREFLIGHT exception declared in builder and mirrored in agent-common
    A(
        "component-builder: BUILD_PREFLIGHT is the single mid-run exception",
        AGENTS / "component-builder.md",
        contains("SINGLE permitted mid-run status line"),
        "builder declares the token as the sole exception to the zero-mid-turn-text rule",
    ),
    A(
        "agent-common: mirrors the BUILD_PREFLIGHT exception",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all("Single exception:", "BUILD_PREFLIGHT:"),
        "zero-mid-turn-text rule carries the mirrored component-builder exception",
    ),
    # --- Skills library reconciliation (ticket #74) ---
    A(
        "planning: seam gate acknowledged as enforced",
        SKILLS / "planning" / "SKILL.md",
        contains_all("SEAM_GATE_STATUS", "enforced", "fail-closed"),
        "planner-facing seam note names the builder's enforced SEAM_GATE_STATUS contract",
    ),
    A(
        "planning: stale advisory seam note removed",
        SKILLS / "planning" / "SKILL.md",
        contains_none(
            "The enforced seam gate is sub-project 2",
            "advisory input to the builder",
            "without a fail-closed gate",
        ),
        "pre-sub-project-2 advisory framing no longer present",
    ),
    A(
        "planning: validation levels point at verification",
        SKILLS / "planning" / "SKILL.md",
        contains_all("cc10x:verification", "Live"),
        "planning defers to verification's canonical Validation Levels incl. Live",
    ),
    A(
        "planning: no divergent validation-levels table",
        SKILLS / "planning" / "SKILL.md",
        contains_none("| **Deterministic** | Automated test with exit code |"),
        "the old three-level table no longer defines levels divergently",
    ),
    A(
        "verification: canonical validation levels retain Live",
        SKILLS / "verification" / "SKILL.md",
        contains_all("## Validation Levels", "**Live**"),
        "verification remains the single owner of the four-level table",
    ),
    A(
        "doc-target-overlay: current ADR path, no deprecated path",
        PLUGIN / "templates" / "doc-target-overlay.md",
        lambda text: "docs/adr/" in text and "docs/decisions/" not in text,
        "template prescribes docs/adr/NNNN, not the deprecated docs/decisions/ path",
    ),
    A(
        "exploration: no subagent spawn in doubt pass",
        SKILLS / "exploration" / "SKILL.md",
        contains_none("spawn a fresh-context adversarial review"),
        "DOUBT no longer instructs spawning a subagent the agent cannot spawn",
    ),
    A(
        "exploration: doubt folded as inline DESIGN sub-procedure",
        SKILLS / "exploration" / "SKILL.md",
        contains_all("Doubt Pass", "not a third mode"),
        "doubt is an inline self-check sub-procedure, keeping the two-mode inventory true",
    ),
    A(
        "update: working patch form, no in-cache git apply --3way",
        SKILLS / "update" / "SKILL.md",
        lambda text: "patch --forward" in text
        and 'git apply --3way "$BACKUP_DIR' not in text,
        "Phase 6 uses patch with an explicit target; broken in-cache git apply --3way removed",
    ),
    A(
        "memory-and-handoff: single knowledge compounding loop",
        SKILLS / "memory-and-handoff" / "SKILL.md",
        lambda text: text.count("## Knowledge Compounding Loop") == 1,
        "the two duplicate sections are merged into one",
    ),
    A(
        "code-review: smell count matches table",
        SKILLS / "code-review" / "SKILL.md",
        lambda text: (
            lambda m, rows: m is not None and int(m.group(1)) == rows
        )(
            re.search(r"Scan for these (\d+) named smells", text),
            len(
                [
                    line
                    for line in text.split("### Code Smells (Fowler Catalog)")[1]
                    .split("\n### ")[0]
                    .splitlines()
                    if line.startswith("| **")
                ]
            ),
        ),
        "the claimed smell count equals the number of table rows",
    ),
    A(
        "code-review: sub-threshold security findings surface as questions",
        SKILLS / "code-review" / "SKILL.md",
        contains_all("Security exception:", "open question"),
        "security findings below 80 confidence surface in the Summary instead of vanishing",
    ),
    A(
        "architecture: term count matches bullets",
        SKILLS / "architecture" / "SKILL.md",
        contains("Three extra terms specific to greenfield architecture"),
        "the extra-terms count matches the three bullets",
    ),
    A(
        "architecture: note no longer self-denying",
        SKILLS / "architecture" / "SKILL.md",
        contains_none("There is no second copy", "Architecture Vocabulary (Precise Language)"),
        "the closing note no longer denies an existing duplicate or cites a nonexistent heading",
    ),
    A(
        "building: reference list has load triggers",
        SKILLS / "building" / "SKILL.md",
        lambda text: text.count("load when") >= 3,
        "each of the three references states when to load it",
    ),
    A(
        "code-review: reference list has load triggers",
        SKILLS / "code-review" / "SKILL.md",
        lambda text: text.count("load when") >= 2 and "load whenever" in text,
        "each of the three references states when to load it",
    ),
    A(
        "memory-and-handoff: reference list has load triggers",
        SKILLS / "memory-and-handoff" / "SKILL.md",
        lambda text: text.count("load when") >= 4,
        "each of the four references states when to load it",
    ),
    # --- Core-workflow contradiction fixes (ticket #78) ---
    # 78.1 — building: RED defined once as behavioral failure, never bare exit code
    A(
        "building: RED = behavioral failure, single statement",
        SKILLS / "building" / "SKILL.md",
        contains_all(
            "RED = a behavioral failure",
            "never a bare exit code",
            "broken harness, not a RED",
            "Record the observed failure reason verbatim",
        ),
        "RED criterion stated once: behavioral failure, exit 1 from harness error is a broken harness",
    ),
    A(
        "building: exit-1-equals-RED contradiction removed",
        SKILLS / "building" / "SKILL.md",
        contains_none("Exit 1 = RED achieved"),
        "the bolded exit-code rule the false-RED guard had to un-teach is gone",
    ),
    # 78.2 — building: framework-trust reconciled with rationalization row
    A(
        "building: framework trust reconciled (production code vs pin with test)",
        SKILLS / "building" / "SKILL.md",
        contains_all(
            "Trust internal code and framework guarantees in production code",
            "depends on a framework behavior, pin it with a test",
        ),
        "trust guarantees in production code; pin depended-on framework behavior with a test",
    ),
    A(
        "building: rationalization row aligned, no contradictory verify-everything row",
        SKILLS / "building" / "SKILL.md",
        contains_all(
            '| "The framework handles this" | Pin the depended-on behavior with a test',
        ),
        "rationalization-table row agrees with the Minimal Diffs rule",
    ),
    A(
        "building: old framework-trust contradiction absent",
        SKILLS / "building" / "SKILL.md",
        contains_none(
            "Verify with a test. Framework guarantees have edge cases.",
        ),
        "the coin-flip counter-instruction is gone",
    ),
    # 78.3 — debugging: Sharpen/Tighten merged under one name
    A(
        "debugging: single tighten-the-loop passage",
        SKILLS / "debugging" / "SKILL.md",
        lambda text: "Sharpen the loop" not in text
        and "sub-second beats sub-minute" in text
        and "same input → same red, no drift" in text,
        "Sharpen folded into Tighten: one name, content preserved",
    ),
    # 78.4 — debugging: one hypothesis count, one confidence table, phase order restored
    A(
        "debugging: unified hypothesis count in Phase 3",
        SKILLS / "debugging" / "SKILL.md",
        contains_all(
            "Generate 3-5 ranked hypotheses",
            "fewer than 3 means you anchored",
        ),
        "one count (3-5, anchoring rationale) stated in Phase 3",
    ),
    A(
        "debugging: drifted counts and trailing sections removed",
        SKILLS / "debugging" / "SKILL.md",
        contains_none(
            "Form H1/H2/H3",
            "## Ranked Hypotheses Before Testing",
            "## Repro Minimisation",
        ),
        "H1/H2/H3 three-count and post-Phase-4 orphan sections are gone",
    ),
    A(
        "debugging: repro minimisation sits before Pattern Analysis",
        SKILLS / "debugging" / "SKILL.md",
        lambda text: 0
        <= text.find("Repro Minimisation")
        < text.find("Phase 2: Pattern Analysis"),
        "minimisation rule reads before the phase that consumes it",
    ),
    A(
        "investigation-hygiene: points at canonical confidence table",
        SKILLS / "debugging" / "references" / "investigation-hygiene.md",
        contains_all(
            "canonical Hypothesis Confidence Scoring table",
            "act only",
        ),
        "reference defers to SKILL.md's table instead of restating bands",
    ),
    A(
        "investigation-hygiene: drifted bands and count removed",
        SKILLS / "debugging" / "references" / "investigation-hygiene.md",
        contains_none(
            "50-79 = needs more evidence",
            "below 50 = speculation",
            "Maintain 2-3 hypotheses",
        ),
        "the conflicting 50/80 bands and 2-3 count no longer exist",
    ),
    # 78.5 — debugging: ending no longer disarms the gates
    A(
        "debugging: ending keeps pressure questions, gates pay for themselves",
        SKILLS / "debugging" / "SKILL.md",
        contains_all(
            'Would this gate hold if the user said "just fix it now"?',
            "Would this gate hold if the bug seemed obvious?",
            "Would this gate hold at 3am with no sleep?",
            "pay for themselves",
        ),
        "three pressure questions retained; ending carries the gates' rationale",
    ),
    A(
        "debugging: advisory self-disarm removed",
        SKILLS / "debugging" / "SKILL.md",
        contains_none(
            "The debugging gates here are advisory",
            "the gate is advisory, not enforced",
        ),
        "the final-sentence advisory framing is gone",
    ),
    # 78.6 — code-review: mode selector replaces maintainer Note; >=80 floor has its why
    A(
        "code-review: mode selector line present",
        SKILLS / "code-review" / "SKILL.md",
        contains_all(
            "Run ADVERSARIAL when producing findings on a diff",
            "run RECEIVING when acting on findings someone else produced",
            "apply in both modes",
        ),
        "one-line mode selector tells a standalone reader which mode is active",
    ),
    A(
        "code-review: maintainer Note removed",
        SKILLS / "code-review" / "SKILL.md",
        contains_none("## Note", "There is no second copy"),
        "maintainer-facing closing Note is gone; file ends on Precedence",
    ),
    A(
        "code-review: >=80 floor carries its rationale",
        SKILLS / "code-review" / "SKILL.md",
        contains_all(
            "more likely noise than signal",
            "Do not inflate a score to smuggle a hunch through",
        ),
        "the confidence floor states why it exists and bans score inflation",
    ),
    # 78.7 — planning: builder-side seam enum restated once, pointer to building
    A(
        "planning: seam gate is a pointer, not a restated enum",
        SKILLS / "planning" / "SKILL.md",
        contains_all(
            "the builder must confirm or formally disagree; see `cc10x:building`",
        ),
        "planning points at building for the enum instead of duplicating it",
    ),
    A(
        "planning: duplicated enum semantics removed",
        SKILLS / "planning" / "SKILL.md",
        contains_none(
            "`confirmed` when it used the plan's seams",
            "records the disagreement and proposes a better seam or blocks",
        ),
        "the long parenthetical restating the builder-side enum is gone",
    ),
    # --- Agent-prompt contradiction fixes (ticket #79) ---
    # 79.1 — agent-common: final-response rule agrees with TaskUpdate-owning agent bodies
    A(
        "agent-common: final-response rule says the router completes the task and no agent calls TaskUpdate",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "The router completes your task after it validates the contract; do not call TaskUpdate." in text
        and "If your agent doc says to call TaskUpdate" not in text
        and "If you own task completion" not in text,
        "no agent holds TaskUpdate or is told to call it, so the conditional carve-out was dead text; step 2 now states the one true rule and agrees with the CONTRACT Envelope paragraph",
    ),
    A(
        "agent-common: unconditional auto-completion sentence removed",
        SKILLS / "agent-common" / "SKILL.md",
        contains_none(
            "Stop your turn — the router handles task completion automatically",
        ),
        "the sentence that told TaskUpdate-owning agents the router completes for them is gone",
    ),
    # 79.2 — triage-agent: every wontfix outcome is a recommendation that stops
    A(
        "triage-agent: wontfix is a recommendation that stops for human",
        AGENTS / "triage-agent.md",
        contains_all(
            "recommend wontfix",
            "every wontfix outcome",
            "STOP for human sign-off",
        ),
        "rows 3-4 and step 4 agree: evidence-gathering proceeds, the wontfix action stops",
    ),
    A(
        "triage-agent: proceed-to-wontfix rows removed",
        AGENTS / "triage-agent.md",
        contains_none(
            "Proceed — if found, wontfix with a pointer",
            "Proceed — if found, wontfix with a link",
        ),
        "the table rows that let a wontfix proceed autonomously are gone",
    ),
    # 79.3 — bug-investigator: checkpoints name their STATUS per bullet
    A(
        "bug-investigator: checkpoints return the named STATUS",
        AGENTS / "bug-investigator.md",
        contains_all(
            "stop and return the named STATUS when:",
            ">3 files → `STATUS: BLOCKED`",
            "public API/interface → `STATUS: BLOCKED`",
            "→ `STATUS: INVESTIGATING`",
        ),
        "Decision Checkpoints header no longer promises BLOCKED for a bullet that returns INVESTIGATING",
    ),
    A(
        "bug-investigator: BLOCKED-only checkpoint header removed",
        AGENTS / "bug-investigator.md",
        contains_none("Decision Checkpoints — return `STATUS: BLOCKED` when:"),
        "the header that contradicted the INVESTIGATING bullet is gone",
    ),
    # 79.4 — code-reviewer: per-finding vs review-level confidence are named scales
    A(
        "code-reviewer: two confidence scales named",
        AGENTS / "code-reviewer.md",
        contains_all(
            "per-finding confidence",
            "different scale",
            "maxes at 90 by construction",
        ),
        "per-finding confidence and the review-level CONFIDENCE field are explicitly different scales, cap stated",
    ),
    A(
        "code-reviewer: zero-finding rule is one number",
        AGENTS / "code-reviewer.md",
        lambda text: "set CONFIDENCE to exactly 70" in text
        and "min(CONFIDENCE, 70)" not in text
        and "A zero-finding review at CONFIDENCE >= 90 is invalid" not in text,
        "zero findings after the positive-assertion pass → CONFIDENCE exactly 70; the min()/≥90 tangle is gone",
    ),
    # 79.5 — doc-syncer: four-layer prose + unbraided audit step 2
    A(
        "doc-syncer: prose names the same four layers as the template",
        AGENTS / "doc-syncer.md",
        lambda text: "all four layers are SKIP" in text
        and "business, technical, audit, glossary" in text
        and "all three layers are SKIP" not in text,
        "Impact Classification names business/technical/audit/glossary and counts four, matching DOC_LAYERS_EVALUATED",
    ),
    A(
        "doc-syncer: audit step 2 unbraided into a checklist",
        AGENTS / "doc-syncer.md",
        lambda text: "If an existing doc covers this topic:\n\n   1." in text
        and "Record the path in `AUDIT_DOCS_UPDATED` **and** `DOC_FILES_UPDATED`" in text
        and "missing from `DOC_FILES_UPDATED` is invisible to the router" in text
        and "**Also add the path to `DOC_FILES_UPDATED`** — the router override accepts" not in text,
        "the mega-sentence is a numbered 3-step checklist keeping every field name and the router-reads-DOC_FILES_UPDATED why",
    ),
    # --- Router prose contradiction fixes (ticket #80) ---
    # 80.1 — §1 opener: nominate/decide rule replaces the self-contradicting first-match sentence
    A(
        "router: §1 opens with nominate/decide, first-match opener gone",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "Route using the first matching signal" not in text
        and "the request's primary deliverable DECIDES the route" in text
        and "the lower Priority number wins" in text,
        "a skimming model can no longer obey the retracted first-matching-signal sentence; the tie-break is the Priority column",
    ),
    # 80.2 — §12 step 6: 'stricter verdict' operationalized as the blocking verdict
    A(
        "router: verdict contradiction resolves to the blocking verdict",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "treat the stricter verdict as authoritative" not in text
        and "treat the blocking verdict as authoritative (FAIL over PASS, CHANGES_REQUESTED over APPROVE)" in text
        and "never average or reconcile" in text,
        "'stricter' is defined by which verdict blocks advancement; contradiction still logged in status_history",
    ),
    # 80.3 — §2 JUST_GO: the four exceptions co-located at the definition
    A(
        "router: JUST_GO definition carries its four exceptions",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "auto-default all non-REVERT AskUserQuestion gates" not in text
        and "EXCEPT: REVERT, failure-stop gates, destructive finishing options" in text
        and "never merge/push/discard" in text
        and "plans with unresolved Open Decisions (BUILD may not start)" in text,
        "all four pre-existing exceptions (Trust rule, §14, build-workflow finishing) are stated where JUST_GO is defined",
    ),
    # 80.4 — §8: 'too short or malformed' made checkable
    A(
        "router: malformed-output rule is checkable",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "If output is too short or malformed" not in text
        and "If the YAML block is absent or any required contract field is missing, whatever the envelope and heading say, run inline verification" in text,
        "inline verification triggers on concrete absence conditions (YAML block or a required field), not a vibe about output length",
    ),
    # 80.5 — §11b Cycle row: checkpoint-at-3 semantics, not a hard cap
    A(
        "router: Cycle row states checkpoint-at-3, not caps-at-3",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "caps cycles at 3" not in text
        and "pauses the loop for a human checkpoint before a 4th remediation cycle is created" in text
        and "cycles beyond 3 run only on explicit user go-ahead" in text,
        "matches what remediation-and-research.md and §14 enforce: count >= 3 -> human checkpoint before a 4th cycle, not a hard stop",
    ),
    # --- Design-cluster contradiction fixes (ticket #81) ---
    # 81.1 — architecture: two-adapter gloss matches canonical ports-only formulation, both occurrences
    A(
        "architecture: two-adapter gloss is ports-only, caller/adapter gloss gone",
        SKILLS / "architecture" / "SKILL.md",
        lambda text: "only one caller/adapter exists" not in text
        and "callers and tests don't count as adapters" not in text
        and text.count(
            "fails the two-adapter rule (it is a port with only one adapter — an ordinary caller or test exercising the interface is not an adapter)"
        )
        == 1,
        "matches codebase-design verbatim: an ordinary caller or test exercising the interface is NOT an adapter (a test ADAPTER implementing the port still counts, per DEEPENING.md production+test); P4.T7.3 removed the duplicate, so the one remaining occurrence carries it",
    ),
    # 81.2 — codebase-hygiene: deletion-test question uses canonical inline-at-call-site phrasing
    A(
        "codebase-hygiene: deletion test question canonical, CONCENTRATE/MOVE gone",
        SKILLS / "codebase-hygiene" / "SKILL.md",
        lambda text: "CONCENTRATE" not in text
        and "just MOVE elsewhere" not in text
        and "If I deleted this module and inlined its code at every call site, where does the complexity go?"
        in text,
        "question and its vanish/reappear answers finally share codebase-design's vocabulary; the CONCENTRATE/MOVE dichotomy contradicted its own answers",
    ),
    # 81.3 — codebase-hygiene: scope-before-you-scan step precedes catalog extraction
    A(
        "codebase-hygiene: step 0 scoping restored before catalog extraction",
        SKILLS / "codebase-hygiene" / "SKILL.md",
        lambda text: "**Scope before you scan**" in text
        and "git log --oneline" in text
        and "deepening pays off in proportion to future change" in text
        and text.index("Scope before you scan") < text.index("Extract catalog"),
        "restores the benchmark's YAGNI scoping and its rationale: weight recently-changed code, take a user-named target verbatim",
    ),
    # 81.4 — codebase-design: canonicity self-commentary deleted, canonical content intact
    A(
        "codebase-design: canonicity no-ops deleted, deletion test intact",
        SKILLS / "codebase-design" / "SKILL.md",
        lambda text: "This skill is the **canonical source**" not in text
        and "This verdict is **canonical**" not in text
        and "If I deleted this module and inlined its code at every call site" in text
        and "apply it before accepting any new module boundary" in text,
        "canonicity lives in frontmatter; the agreement claim steered nothing — the test itself must survive the deletion",
    ),
    # --- Meta/process dedup (ticket #82) ---
    # 82.1 — verification: one Excuses and Tells table owns the anti-"should" meaning
    A(
        "verification: single excuses-and-tells table",
        SKILLS / "verification" / "SKILL.md",
        lambda text: "## Excuses and Tells" in text
        and "## Rationalization Table" not in text
        and "## Red Flags" not in text
        and "**Forbidden language before proof:**" not in text
        and "## Auditor Posture" not in text
        and '"Should" is not evidence.' in text
        and "Weakening an assertion to make a test pass" in text,
        "the three anti-should sites (Forbidden language, Rationalization Table, Red Flags) merged into one table; Auditor Posture folded into the opener",
    ),
    A(
        "verification: authoring rule out of runtime body, opener owns auditor clause",
        SKILLS / "verification" / "SKILL.md",
        lambda text: "**Authoring Rule: Keep Gates High.**" not in text
        and "<!-- Authoring rule (maintenance, not runtime)" in text
        and "A claim is not verification." not in text
        and "Gates are scar notes" not in text
        and "If you cannot independently reproduce a claimed success, return FAIL."
        in text,
        "author-facing rule survives only as an HTML comment; decoratives deleted; the one novel Auditor Posture clause lives in the opener",
    ),
    # 82.2 — diff-driven-docs: Impact Classifier is the sole SKIP owner; IMPACT_LEVEL decidable
    A(
        "diff-driven-docs: classifier sole SKIP owner + IMPACT_LEVEL defined",
        SKILLS / "diff-driven-docs" / "SKILL.md",
        lambda text: "**SKIP audit docs if:**" not in text
        and "**SKIP when:**" not in text
        and "`low` = only the technical layer triggered" in text
        and "`medium` = technical layer triggered with signature changes" in text
        and "the audit layer requires a new decision record" in text
        and "`low` = only CHECK verdicts, no CREATE" not in text
        and "**CREATE new when:**" in text
        and "**UPDATE existing when:**" in text,
        "SKIP set stated once (the classifier table); low/medium/high have assignment procedures; CREATE/UPDATE detail kept",
    ),
    A(
        "doc-target-heuristics: no duplicate SKIP rows or index rule",
        SKILLS / "diff-driven-docs" / "references" / "doc-target-heuristics.md",
        lambda text: "## CLAUDE.md Index Rule" not in text
        and "| Routine bug fix | SKIP |" not in text
        and "CREATE decision record" in text,
        "reference keeps CREATE/UPDATE signal rows; SKIP rows and the CLAUDE.md index rule live only in SKILL.md",
    ),
    A(
        "diff-driven-docs: SKILL.md still owns the CLAUDE.md index rule",
        SKILLS / "diff-driven-docs" / "SKILL.md",
        contains_all(
            "it is indexed in the relevant `## Docs` section",
            "No doc content was duplicated in `CLAUDE.md`",
        ),
        "the surviving copy of the index rule is Step 5 self-review",
    ),
    # 82.3 — memory-and-handoff: one ownership statement, hedge resolved, one redaction rule
    A(
        "memory-and-handoff: ownership single-sourced with named carve-out",
        SKILLS / "memory-and-handoff" / "SKILL.md",
        lambda text: "sole carve-out: bug-investigator's `[DEBUG-N]` lines" in text
        and "Redact per `### Secret Redaction` above." in text
        and "<redacted:pii>" in text
        and "This closes the loop" not in text,
        "SKILL.md ### Ownership is authoritative (absolute rule + carve-out); handoff rule 3 points at Secret Redaction which now owns the pii token",
    ),
    A(
        "memory-model-and-ownership: pointer instead of duplicate ownership/surfaces",
        SKILLS
        / "memory-and-handoff"
        / "references"
        / "memory-model-and-ownership.md",
        lambda text: "see SKILL.md `### Ownership`" in text
        and "### WRITE Agents" not in text
        and "## Contents" not in text
        and "current focus" not in text,
        "ownership section and Memory Surfaces list replaced by pointers; ToC deleted",
    ),
    A(
        "memory-operations: hedge gone, pointer present",
        SKILLS / "memory-and-handoff" / "references" / "memory-operations.md",
        lambda text: "normally" not in text
        and "see SKILL.md `### Ownership`" in text,
        "the 'normally do not edit' hedge no longer contradicts the absolute ownership rule",
    ),
    A(
        "memory-file-contracts: ToC deleted",
        SKILLS / "memory-and-handoff" / "references" / "memory-file-contracts.md",
        contains_none("## Contents"),
        "the second reference ToC is gone",
    ),
    # 82.4 — frontend: motion rules single-sourced, lint modality resolved, honest-score line
    A(
        "frontend: motion rules single-sourced in SKILL.md",
        SKILLS / "frontend" / "SKILL.md",
        contains_all(
            "### Motion Rules",
            "No layout-shifting hover effects.",
            "motion must not block user action",
        ),
        "the reference's unique motion bullets merged into the surviving SKILL.md copy",
    ),
    A(
        "frontend/performance-and-layout: motion rules deleted",
        SKILLS / "frontend" / "references" / "performance-and-layout.md",
        lambda text: "\n## Motion Rules" not in text
        and "Motion rules live in SKILL.md `### Motion Rules`." in text,
        "reference points at SKILL.md instead of duplicating the four motion rules",
    ),
    A(
        "frontend/design-md-authoring: one lint rule, errors block",
        SKILLS / "frontend" / "references" / "design-md-authoring.md",
        lambda text: "when practical and non-disruptive" not in text
        and text.count("npx @google/design.md lint DESIGN.md") == 1
        and "errors block, warnings are review items" in text,
        "the lint gate is stated once with one modality: errors block; skip only when Node/network unavailable",
    ),
    A(
        "frontend: anti-grade-inflation line, no 'Be honest' filler",
        SKILLS / "frontend" / "SKILL.md",
        lambda text: "Most real interfaces score 2; anti-grade-inflation is the job."
        in text
        and "Be honest." not in text,
        "the rubric-band reminder keeps only the behavioral sentence",
    ),
    # 82.5 — mcp-cli: recap and transience restatements deleted
    A(
        "mcp-cli: no Discipline recap, transience stated once",
        SKILLS / "mcp-cli" / "SKILL.md",
        lambda text: "## Discipline" not in text
        and "monthly `/mcp` review" not in text
        and "used then released, never resident" not in text
        and "This keeps accelerators **transient**" in text,
        "the recap section and the second/third transience statements are gone; one statement carries it",
    ),
    # 82.6 — resolving-merge-conflicts: single statements, marker gate only
    A(
        "resolving-merge-conflicts: dedup — single never-abort/never-invent, marker gate",
        SKILLS / "resolving-merge-conflicts" / "SKILL.md",
        lambda text: "## Before you commit" in text
        and "## Hard rules" not in text
        and "Use when a git merge or rebase reports conflicts and the operation is in progress."
        in text
        and "Do not stop mid-rebase." not in text
        and "it's a larger conflict" not in text
        and text.count("Never invent new behavior") == 1
        and text.count("`--abort` throws away") == 1
        and "never pick one side blind" in text,
        "intro owns never-abort with its why, step 3 owns never-invent, the commit gate owns markers; duplicates deleted",
    ),
    # --- Output-format integrity (ticket #83) ---
    # 83.1 — code-reviewer: SPEC_COMPLIANCE / PLAN_DEFECT / CANNOT_VERIFY_CROSS_PHASE
    # exemplified as literal valid YAML (both alternatives), prose-in-brackets gone
    A(
        "code-reviewer: literal YAML alternatives for spec fields",
        AGENTS / "code-reviewer.md",
        contains_all(
            "SPEC_COMPLIANCE: PASS",
            "- bucket: MISSING",
            'item: "rate-limit guard on /login"',
            "- bucket: EXTRA",
            "PLAN_DEFECT: false",
            "CANNOT_VERIFY_CROSS_PHASE: None",
            "emit exactly ONE alternative per field",
        ),
        "each spec field shows the scalar alternative and the structured alternative as literal block YAML",
    ),
    A(
        "code-reviewer: prose-in-brackets field examples deleted",
        AGENTS / "code-reviewer.md",
        contains_none(
            "SPEC_COMPLIANCE: [PASS | list of {bucket, item}",
            '{MISSING, "rate-limit guard on /login"}',
            "PLAN_DEFECT: [false |",
            "CANNOT_VERIFY_CROSS_PHASE: [None |",
        ),
        "the invalid-YAML prose-in-brackets examples no longer exist",
    ),
    A(
        "code-reviewer: field-alternative YAML blocks parse",
        AGENTS / "code-reviewer.md",
        yaml_alternatives_parse("either the scalar", expected_blocks=3),
        "the three Field-Alternatives fenced yaml blocks are valid YAML (yaml.safe_load)",
    ),
    # 83.15 — envelope `b` defined per status (code-reviewer + failure-hunter)
    A(
        "code-reviewer: envelope b rule defined",
        AGENTS / "code-reviewer.md",
        contains_all(
            "`b:true` iff STATUS=CHANGES_REQUESTED with ≥1 CRITICAL finding",
            "keeps `b:false`",
        ),
        "b is defined per status: true only for CHANGES_REQUESTED with >=1 CRITICAL",
    ),
    A(
        "failure-hunter: envelope b rule defined",
        AGENTS / "failure-hunter.md",
        contains_all(
            "`s=ISSUES_FOUND` when any CRITICAL or HIGH exists",
            "`b=true` only when CRITICAL>0",
            "HIGH-only findings: `s=ISSUES_FOUND`, `b=false`",
        ),
        "s and b defined per status; HIGH-only middle case resolved (b=false)",
    ),
    # 83.4f — bug-investigator: Regression:/Variant: prefixes exemplified in SCENARIOS
    A(
        "bug-investigator: scenario-name prefixes exemplified",
        AGENTS / "bug-investigator.md",
        contains_all(
            '- name: "Regression: empty cart returns NaN total"',
            '- name: "Variant: total stays correct with locale=de-DE"',
            'literal prefix "Regression:"',
            'literal prefix "Variant:"',
        ),
        "the SCENARIOS template shows one example row per required name prefix",
    ),
    A(
        "bug-investigator: bare scenario-name placeholder gone",
        AGENTS / "bug-investigator.md",
        contains_none('- name: "[scenario name]"'),
        "the unprefixed placeholder row no longer hides the prefix requirement",
    ),
    # 83.9 — TDD_RED_EXIT defined as the observed exit code; =1 rule kept (replay
    # checker enforces ==1 literally, so the clarifier rides alongside, not against)
    A(
        "bug-investigator: TDD_RED_EXIT observed-exit-code clarifier",
        AGENTS / "bug-investigator.md",
        contains_all(
            "TDD_RED_EXIT: [the observed exit code of the RED run",
            "1 is the conventional recorded value",
            "`TDD_RED_EXIT=1`",
        ),
        "field defined as observation; conventional value 1 kept for the replay gate",
    ),
    A(
        "component-builder: TDD_RED_EXIT observed-exit-code clarifier",
        AGENTS / "component-builder.md",
        contains_all(
            "TDD_RED_EXIT: [the observed exit code of the RED run",
            "any non-zero exit with TDD_RED_REASON_KIND=`behavioral` qualifies as RED evidence",
            "TDD_RED_EXIT=1",
        ),
        "field defined as observation, aligned to the behavioral-RED rule; =1 kept for the replay gate",
    ),
    # 83.8 — component-builder: seam proposal located in TEST_SEAMS; token frozen
    A(
        "component-builder: seam proposal lives in TEST_SEAMS, token frozen",
        AGENTS / "component-builder.md",
        contains_all(
            "record the seams in TEST_SEAMS in your final contract",
            "decide them before emitting BUILD_PREFLIGHT",
            "The token itself stays exactly four fields — never extend it.",
        ),
        "the proposal location is explicit and the BUILD_PREFLIGHT token stays four fields",
    ),
    A(
        "component-builder: seam gate table tense unified",
        AGENTS / "component-builder.md",
        lambda text: text.count("`proposed` (you proposed the seams)") == 2
        and "(you propose at BUILD_PREFLIGHT)" not in text
        and "(you proposed at BUILD_PREFLIGHT)" not in text,
        "rows 2 and 3 use identical wording; the at-BUILD_PREFLIGHT location claim is gone",
    ),
    # 83.5 — integration-verifier: BLOCKED scenarios have a home; Option B inlined
    A(
        "integration-verifier: SCENARIOS_BLOCKED optional field + arithmetic",
        AGENTS / "integration-verifier.md",
        contains_all(
            "SCENARIOS_BLOCKED: [count — OPTIONAL field; omit or 0 when no scenario is blocked]",
            "SCENARIOS_TOTAL = PASSED + FAILED + BLOCKED (SCENARIOS_BLOCKED is optional and defaults to 0 when absent)",
            "UNVERIFIED by a Test-Honesty hit, counts in SCENARIOS_BLOCKED",
        ),
        "BLOCKED/UNVERIFIED scenarios get a bucket; arithmetic includes it with an additive default",
    ),
    A(
        "integration-verifier: Option-B forward reference inlined",
        AGENTS / "integration-verifier.md",
        lambda text: "REVERT_RECOMMENDED: [true if decision = revert]" in text
        and "[true if Option B]" not in text,
        "the YAML field no longer forward-references a term defined 40 lines later",
    ),
    # --- Core/design/agent dedup (ticket #84) ---
    # 84.1 — reference-file Tables of Contents deleted (LLMs don't scroll)
    *[
        A(
            f"{skill}/{ref}: no Table of Contents",
            SKILLS / skill / "references" / ref,
            contains_none("## Table of Contents"),
            "anchor-link ToC blocks steer nothing; deleted",
        )
        for skill, ref in (
            ("building", "testing-patterns.md"),
            ("building", "test-data-and-mocks.md"),
            ("building", "integration-and-live-proof.md"),
            ("code-review", "security-review-checklist.md"),
            ("code-review", "review-order-and-checkpoints.md"),
            ("code-review", "code-review-heuristics.md"),
            ("debugging", "investigation-hygiene.md"),
            ("debugging", "root-cause-playbooks.md"),
        )
    ],
    # 84.1b — third-party attributions gone, the rules they introduced survive
    A(
        "investigation-hygiene: GSD attribution gone, context rule survives",
        SKILLS / "debugging" / "references" / "investigation-hygiene.md",
        lambda text: "GSD" not in text
        and "Read only the files on the active failure path." in text,
        "undefined external-framework token deleted; the context-budget rule stands alone",
    ),
    A(
        "review-order: BMAD attribution gone, concern-order rule survives",
        SKILLS / "code-review" / "references" / "review-order-and-checkpoints.md",
        lambda text: "BMAD" not in text
        and "Reconstruct the change in the order that builds understanding" in text,
        "undefined external-framework token deleted; the read-by-concern rule stands alone",
    ),
    # 84.2 — building: Leading Words glossary deleted; single-statement slicing + behavior focus
    A(
        "building: Leading Words table deleted",
        SKILLS / "building" / "SKILL.md",
        contains_none("## Leading Words", "| Word | Means | Replaces |"),
        "red/green/tight/seam are defined by use; deep/shallow were never used",
    ),
    A(
        "building: horizontal-slicing prohibition stated once",
        SKILLS / "building" / "SKILL.md",
        lambda text: "or all tests first, then all implementation" in text
        and "Don't write all tests first then all implementation" not in text,
        "Vertical Slicing owns the prohibition; Seam Discipline no longer restates it",
    ),
    A(
        "building: behavior-over-implementation stated once in-skill",
        SKILLS / "building" / "SKILL.md",
        lambda text: "**Behavioral focus:**" not in text
        and "Test through the public interface, not internals" in text,
        "the implementation-coupled anti-pattern is the single in-skill statement",
    ),
    A(
        "testing-patterns: Behavior Over Internals reference survives",
        SKILLS / "building" / "references" / "testing-patterns.md",
        contains("Behavior Over Internals"),
        "the reference copy of behavior-over-implementation is the surviving second source",
    ),
    # 84.3 — architecture: maintainer Note gone; vocabulary is a clean pointer; app rule byte-identical x2
    A(
        "architecture: maintainer Note deleted",
        SKILLS / "architecture" / "SKILL.md",
        contains_none("## Note", "deliberately repeated at its two points of use"),
        "the maintainer changelog section is gone; file ends on Decision Framework",
    ),
    A(
        "architecture: vocabulary paragraph is pointer-only",
        SKILLS / "architecture" / "SKILL.md",
        lambda text: "**Use those terms exactly.**" in text
        and "don't restate them here" not in text
        and "NOT a lines-ratio" not in text,
        "pointer + enforcement rule only; the restated depth definition and Ousterhout clause are gone",
    ),
    A(
        "architecture: the application rule is stated once, byte-identical to the canonical sentence",
        SKILLS / "architecture" / "SKILL.md",
        lambda text: text.count(
            "Before finalizing any component boundary, apply the **Deletion Test** and "
            "**Two-Adapter Rule** as defined in `cc10x:codebase-design`. A component that "
            "fails the deletion test (complexity vanishes if deleted) or fails the "
            "two-adapter rule (it is a port with only one adapter — an ordinary caller "
            "or test exercising the interface is not an adapter) is not a real boundary "
            "yet — fold it into its "
            "caller or defer the split until a second concrete need appears."
        )
        == 1,
        "E7: the sentence was repeated at Design Components and again at Architecture Vocabulary (ticket #84.3 kept both on purpose); P4.T7.3 removed the second copy, so one copy remains and a returning duplicate fails",
    ),
    # 84.4 — exploration: never-ships single-sourced at Hard Wall; Doubt Pass unbraided
    A(
        "exploration: never-ships collapsed to Hard Wall + pointer",
        SKILLS / "exploration" / "SKILL.md",
        lambda text: "The spike's code does not become production by surviving." in text
        and "<!-- scar: 2026-06-17" in text
        and "ABSORB triggers a fresh BUILD (see Hard Wall)" in text
        and "The prototype skill NEVER transitions itself into BUILD" not in text
        and "re-implement the core under TDD/reviewer/verifier" not in text,
        "Hard Wall + scar own the meaning; ABSORB points; the closer restatement is gone",
    ),
    A(
        "exploration: What This Is NOT deleted, DOUBT owns artifacts-only rule",
        SKILLS / "exploration" / "SKILL.md",
        lambda text: "#### What This Is NOT" not in text
        and "work from the ARTIFACT + CONTRACT only" in text,
        "the three-negation section is gone; its load-bearing clause lives in DOUBT step 3",
    ),
    A(
        "exploration: DOUBT orchestration aside is a one-line note outside the steps",
        SKILLS / "exploration" / "SKILL.md",
        lambda text: "has NO `Agent`/subagent tool" not in text
        and "request router-mediated dispatch in the handoff" in text,
        "step 3 keeps only the procedure; the router-plumbing aside is a trailing note",
    ),
    # 84.5 — code-reviewer: READ-ONLY, spec-independence, PLAN_DEFECT each single-sourced
    A(
        "code-reviewer: READ-ONLY stated once",
        AGENTS / "code-reviewer.md",
        lambda text: text.count("**Mode:** READ-ONLY") == 1
        and "You do NOT have Edit tool" not in text,
        "the opening Mode line is the single READ-ONLY statement",
    ),
    A(
        "code-reviewer: spec-independence single-sourced in Output",
        AGENTS / "code-reviewer.md",
        lambda text: "see **SPEC_COMPLIANCE gating** under Output" in text
        and "A FIRST-CLASS verdict, SEPARATE from code quality" not in text
        and text.count("gates to CHANGES_REQUESTED on its own") == 1,
        "Pass 6 points at the authoritative SPEC_COMPLIANCE gating paragraph next to the field",
    ),
    A(
        "code-reviewer: PLAN_DEFECT routing single-sourced in Output",
        AGENTS / "code-reviewer.md",
        lambda text: "see **PLAN_DEFECT routing** under Output" in text
        and "NOT to the implementer as a code fix" not in text
        and text.count("routes it to the planner") == 1,
        "Pass 5 points at the authoritative PLAN_DEFECT routing paragraph next to the field",
    ),
    # 84.6 — self-activation rule: one canonical sentence across the fleet
    *[
        A(
            f"{name}: canonical self-activation sentence",
            path,
            lambda text: "Do not self-activate internal cc10x skills not passed in SKILL_HINTS"
            in text
            and "self-load" not in text
            and "internal CC10X skills" not in text,
            "agent-common's sentence is canonical; drifted variants are gone",
        )
        for name, path in (
            ("agent-common", SKILLS / "agent-common" / "SKILL.md"),
            ("code-reviewer", AGENTS / "code-reviewer.md"),
            ("failure-hunter", AGENTS / "failure-hunter.md"),
        )
    ],
    A(
        "code-reviewer: frontend delta preserved as including-clause",
        AGENTS / "code-reviewer.md",
        contains_all(
            "(including `cc10x:frontend`)",
            "note that gap in Memory Notes and continue within the router-provided scope",
        ),
        "the reviewer's genuine delta (frontend example + gap procedure) survives the alignment",
    ),
    # --- Adjectives to decision procedures (ticket #85) ---
    A(
        "plan-review-gate: mode-fit is a threshold, not a mood",
        SKILLS / "plan-review-gate" / "SKILL.md",
        lambda text: "Request changes ≥3 files or any contract/schema/auth surface while mode is `direct`"
        in text
        and "mode is not `decision_rfc`" in text
        and "Mode is too weak for the request" not in text,
        "mode-fit row carries the ≥3-files/contract-surface/decision_rfc thresholds; 'too weak' is gone",
    ),
    A(
        "plan-review-gate: over-engineered replaced by requirement-row mapping",
        SKILLS / "plan-review-gate" / "SKILL.md",
        lambda text: "The plan introduces a file, abstraction, or dependency that no requirement row maps to"
        in text
        and "Solution is over-engineered for the problem" not in text,
        "complexity row is decidable via requirement-row mapping; 'over-engineered' adjective is gone",
    ),
    A(
        "plan-review-gate: edge cases enumerated per input surface",
        SKILLS / "plan-review-gate" / "SKILL.md",
        lambda text: "For each input surface the plan touches, find its empty, invalid, and failure case"
        in text
        and "why none applies" in text
        and "Obvious error paths" not in text,
        "edge-case row enumerates empty/invalid/failure per input (or why none applies); 'Obvious' is gone",
    ),
    A(
        "plan-review-gate: Checks 2 and 3 carry How-to-verify procedures",
        SKILLS / "plan-review-gate" / "SKILL.md",
        lambda text: text.count("| Criterion | How to verify | Blocking if |") == 3
        and "List each sentence of the user request; cite the plan item covering it"
        in text
        and "For each new file, abstraction, or dependency, cite the requirement row that needs it"
        in text,
        "Checks 2 and 3 each have a How-to-verify column with an observation procedure per row",
    ),
    A(
        "plan-review-gate: critical-path work defined in-file",
        SKILLS / "plan-review-gate" / "SKILL.md",
        contains(
            "**Critical-path work** = auth, payment, data-destructive operations, migrations, or work the user labeled critical."
        ),
        "the rigor row's 'critical-path work' term is defined in one line",
    ),
    A(
        "plan-review-gate: one independence disclosure",
        SKILLS / "plan-review-gate" / "SKILL.md",
        lambda text: "not reviewer isolation" in text
        and "fake reviewer independence" not in text
        and "Important limit" not in text,
        "the two adjacent independence disclosures are merged into one sentence",
    ),
    A(
        "plan-review-gate: hard rules carry their whys",
        SKILLS / "plan-review-gate" / "SKILL.md",
        contains_all(
            "comments get ignored; FAILs get fixed",
            "three failed revisions means the premise is wrong, not the wording",
        ),
        "no-APPROVED-WITH-COMMENTS and the 3-iteration escalation each state their why",
    ),
    A(
        "planning: task sizing is context-window based",
        SKILLS / "planning" / "SKILL.md",
        lambda text: "fit a single fresh context window" in text
        and "implement, and test it without compaction" in text
        and "30-90 minutes" not in text,
        "task granularity is agent-perceivable (context window), not human minutes",
    ),
    A(
        "planning: risk score is a lookup, not ordinal arithmetic",
        SKILLS / "planning" / "SKILL.md",
        lambda text: "high/high or high/med (either order) → deterministic test required"
        in text
        and "med/med → deterministic or probabilistic with stated flake policy" in text
        and "anything involving a low → manual checklist acceptable" in text
        and "take the stricter one" in text
        and "Score = Probability × Impact" not in text,
        "the risk matrix maps cells directly to test requirements; the undefined Score formula is gone",
    ),
    A(
        "planning: sprint-blind horizons removed",
        SKILLS / "planning" / "SKILL.md",
        lambda text: '"near-term-refactor" (refactor likely)' in text
        and ">1 caller in this plan" in text
        and "sprint" not in text
        and "(Advisory)" not in text,
        "Durability-Horizon and Prefactor use in-plan/near-term-refactor/stable; sprints and the softening label are gone",
    ),
    A(
        "architecture-scanner: walk-the-modules procedure with stop rule",
        AGENTS / "architecture-scanner.md",
        lambda text: "Walk the codebase module by module" in text
        and "stop when you have 3-5 candidates or have covered the hot spots from step 1"
        in text
        and "Explore organically" not in text,
        "'Explore organically' replaced by a module walk with an explicit stop condition",
    ),
    A(
        "architecture-scanner: strength badges have assignment criteria",
        AGENTS / "architecture-scanner.md",
        contains_all(
            '`Strong` = deletion test says "concentrates" AND the files appear in git-log hot spots',
            "`Speculative` = single-read impression, no churn or test-pain evidence",
            "everything else = `Worth exploring`",
        ),
        "two runs badge the same candidate the same way",
    ),
    A(
        "planner: gate iterations and fresh-review passes disambiguated",
        AGENTS / "planner.md",
        lambda text: "Gate iterations (max 3) and fresh-review passes (max 2, `PLANNING_REVIEW_RUNS`) are different counters"
        in text
        and "a different counter from the plan-review-gate's 3 iterations" in text,
        "the two review counters are named as different at both mention sites; YAML fields unrenamed",
    ),
    A(
        "planner: CONFIDENCE is scored, not asserted",
        AGENTS / "planner.md",
        lambda text: "start at 90; subtract 15 per critical assumption classified `inferred`"
        in text
        and "subtract 25 if RECOMMENDED_DEFAULTS is non-empty" in text
        and "cap at the Research Quality tier (high → 90, medium → 75, low → 60, none → 50)"
        in text
        and "The CONFIDENCE≥50 requirement reads this computed value" in text,
        "CONFIDENCE bound to checkables; the ≥50 gate reads the computed value",
    ),
    A(
        "bug-investigator: hypothesis 80+ bound to checkables",
        AGENTS / "bug-investigator.md",
        lambda text: "A hypothesis reaches 80+ only when BOTH hold" in text
        and "at least one prediction confirmed by instrumentation" in text
        and "Otherwise cap it at 60" in text,
        "80+ requires complete causal chain plus a confirmed prediction; otherwise capped at 60",
    ),
    A(
        "failure-hunter: || defaultValue has a discrimination test",
        AGENTS / "failure-hunter.md",
        lambda text: "could the left side be falsy because an operation FAILED?" in text
        and "a default for optional config/input is fine" in text
        and "| Masks errors | Check explicitly first |" not in text
        and "Log when a short-circuit to null is not an expected state" in text,
        "fallible-call returns are flagged, optional-config defaults ignored; ?. logging is conditioned on unexpected state",
    ),
    # --- Missing-WHY pass and benchmark restorations (ticket #86) ---
    A(
        "building: run-mode carries the watch-mode-never-exits why",
        SKILLS / "building" / "SKILL.md",
        contains("watch mode never exits, so the agent hangs"),
        "CI=true/run-mode rule states that watch mode never exits so the agent hangs",
    ),
    A(
        "agent-common: run-mode carries the watch-mode-never-exits why (the canonical copy the agents point at)",
        SKILLS / "agent-common" / "SKILL.md",
        contains("watch mode never exits, so the agent hangs"),
        "CI=true/run-mode rule states that watch mode never exits so the agent hangs",
    ),
    A(
        "debugging: LOG FIRST carries the highest-density-evidence why",
        SKILLS / "debugging" / "SKILL.md",
        contains_all(
            "highest-density evidence",
            "acting first destroys or masks it",
        ),
        "LOG FIRST states that error text is the highest-density evidence and acting first destroys it",
    ),
    A(
        "debugging: red-capable criterion restores paste-the-output evidence",
        SKILLS / "debugging" / "SKILL.md",
        contains("(paste the invocation and its output)"),
        "loop completion criterion requires pasting the invocation and its output",
    ),
    A(
        "agent-common: shell-write ban carries the bypasses-file-tracking why",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all(
            "shell writes bypass the harness's file tracking and permission model",
            "invisible to review",
        ),
        "shell-redirection ban states writes bypass file tracking/permission model and are invisible to review",
    ),
    A(
        "agent-common: no-tool-after-contract carries the last-message why",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all(
            "the router parses only your last message",
            "a trailing tool result would become it",
        ),
        "no-tool-after-contract rule explains the router parses only the last message",
    ),
    A(
        "exploration: interview restores bewildering why and facts-vs-decisions",
        SKILLS / "exploration" / "SKILL.md",
        contains_all(
            "asking several questions at once is bewildering",
            "look it up rather than asking; the decisions are the user's",
        ),
        "one-question rule carries its why; facts are looked up, decisions go to the user",
    ),
    A(
        "research: primary-source principle restored",
        SKILLS / "research" / "SKILL.md",
        contains_all(
            "prefer the source that owns the claim",
            "A secondary write-up citing a primary loses to the primary",
        ),
        "synthesis prefers the owning primary source over secondary write-ups",
    ),
    A(
        "research: conflict-resolution bullets merged with docs-vs-code why",
        SKILLS / "research" / "SKILL.md",
        lambda text: "docs describe intent; code is what runs" in text
        and "Conflict resolution (when sources disagree, prefer GitHub real code over docs)"
        not in text,
        "one conflict-resolution rule, carrying the docs-describe-intent / code-is-what-runs why",
    ),
    A(
        "router: step-1 no-parallelize carries its why",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("Do not parallelize step 1 with reads — the reads assume the directory exists."),
        "no-parallelize rule states the reads assume the directory exists",
    ),
    A(
        "router: main-session rule carries the sub-agent-gates why",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "never inside a sub-agent",
            "only dispatcher of phase agents",
            "up to three layers",
        ),
        "router-in-main-session rule keeps router-only dispatch and states the documented sub-agent spawn depth (A4)",
    ),
    A(
        "router: Memory Update sub-agent ban carries the payload why",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("a sub-agent lacks the captured payload and the memory files' session context"),
        "Memory Update ban states a sub-agent lacks the payload and session context",
    ),
    A(
        "router: dead wf:PENDING_SELF line removed",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_none("PENDING_SELF"),
        "the noise line about the unused wf:PENDING_SELF value is deleted",
    ),
    A(
        "plan-workflow: fresh-review cap carries its why",
        SKILLS / "cc10x-router" / "references" / "plan-workflow.md",
        contains("pass-2 findings escalate to the human; more passes polish a wrong plan"),
        "max-2 fresh-review passes states pass-2 escalates and more passes polish a wrong plan",
    ),
    A(
        "verification: re-run-once carries the blip-vs-flake why",
        SKILLS / "verification" / "SKILL.md",
        contains_all(
            "one retry separates environment blips from real flake",
            "more retries launder genuine failures",
        ),
        "flaky re-run cap explains one retry separates blips from flake; more launders failures",
    ),
    A(
        "integration-verifier: re-run-once carries the blip-vs-flake why",
        AGENTS / "integration-verifier.md",
        contains_all(
            "one retry separates environment blips from real flake",
            "more retries launder genuine failures",
        ),
        "flaky re-run cap explains one retry separates blips from flake; more launders failures",
    ),
    # --- Router prose polish (ticket #87) ---
    A(
        "router: consolidated research pointer section present",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "## 10. Research (Trigger, Quality, Files)",
            "whenever research is triggered (including research task creation), consumed, summarized, or handed to planner/investigator",
            "apply its `## 10. Research Orchestration`, `## Research Quality`, and `## Research Files` blocks",
        ),
        "one consolidated research section points at remediation-and-research.md for trigger, quality, and files",
    ),
    A(
        "router: duplicate research pointer headings deleted",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: all(
            re.search(pattern, text, re.M) is None
            for pattern in (
                r"^## 10\. Research Orchestration$",
                r"^## Research Quality$",
                r"^## Research Files$",
                r"^### Research tasks$",
            )
        ),
        "the four redundant research pointer sections collapsed into the single §10 pointer",
    ),
    A(
        "router: tier table marked ADVISORY with live rules separated",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "ADVISORY — for humans tuning frontmatter; the router does not act on this table at dispatch time.",
            "The Agent tool accepts a per-invocation `model` that outranks frontmatter, but the router passes none: model selection stays in agent frontmatter.",
            "never edit a gating agent's",
            "frontmatter below mid-tier — the cheapest tier rubber-stamps",
            "never downgrade a gating role to save tokens, including under `JUST_GO`",
        ),
        "model-tier section: two live rules agent-facing, table prefixed as advisory-only, per-invocation model stated truthfully (A4)",
    ),
    A(
        "router: capture-memory-payload is literal step 0 before the pre-check",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: (
            "0. Capture memory payload FIRST" in text
            and "1. Pre-check" in text
            and "compaction can fire between agent return and parse; an uncaptured payload is lost"
            in text
            and text.find("0. Capture memory payload FIRST")
            < text.find("1. Pre-check")
        ),
        "step 0 (capture payload + compaction why) appears before step 1 pre-check on the page",
    ),
    A(
        "policy: SELF-CHECK BLOCKLIST is the single source with the full union",
        SKILLS
        / "cc10x-router"
        / "references"
        / "workflow-artifact-and-hook-policy.md",
        contains_all(
            "SELF-CHECK BLOCKLIST",
            "`do not flag`",
            "`don't treat X as a defect`",
            "`don't worry about`",
            "`at most minor`",
            "`the plan chose`",
            "`already verified, just`",
            "`should be fine`",
            "`no need to check`",
        ),
        "policy blocklist holds the full union of both former phrase lists",
    ),
    A(
        "router: anti-pre-judging guard points at the policy blocklist",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "grep the drafted prompt against the SELF-CHECK BLOCKLIST in `references/workflow-artifact-and-hook-policy.md`",
            "any hit → rewrite it out before dispatch",
        ),
        "SKILL.md §7 keeps the principle and defers the phrase list to the policy reference",
    ),
    A(
        "router: inline bias-phrase list no longer duplicated in SKILL.md",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_none('scan the constructed prompt for bias phrases — "do not flag"'),
        "the old inline SKILL.md phrase enumeration is gone; policy file is the single source",
    ),
    A(
        "update skill: discovers installs through the plugin CLI",
        SKILLS / "update" / "SKILL.md",
        contains_all(
            "claude plugin list --json",
            "claude plugin marketplace update cc10x",
            "claude plugin update cc10x@cc10x --scope",
            "/reload-plugins",
        ),
        "update flow must be CLI-driven: list, refresh marketplace, update per scope, then restart or reload",
    ),
    A(
        "update skill: marketplace located, then patches captured, before the refresh",
        SKILLS / "update" / "SKILL.md",
        lambda t: 0
        < t.find("## Phase 2: Locate The Marketplace")
        < t.find("## Phase 3: Capture Local Patches")
        < t.find("## Phase 4: Refresh The Marketplace")
        < t.find("## Phase 5: Update Each Scope"),
        "carry-over must read the old version before `marketplace update` moves the checkout to the new one",
    ),
    A(
        "update skill: carry-over baseline is a pinned git commit or an abort",
        SKILLS / "update" / "SKILL.md",
        contains_all(
            "log --format=%H -S",
            "tail -1",
            'show "$SHA:plugins/cc10x/',
            "ABORT carry-over",
        ),
        "pristine baseline = file at the commit that set the old version; unresolvable baseline aborts instead of guessing",
    ),
    A(
        "update skill: carry-over limits stated honestly",
        SKILLS / "update" / "SKILL.md",
        lambda t: "can no longer be read" not in t
        and "checkout depth" in t
        and "carry-over is unavailable" in t
        and "Ask the user whether they have modified" in t
        and "every discovered entry" in t,
        "carry-over needs a resolvable baseline (checkout depth is the real limit); capture covers every discovered entry; modification is asked, not assumed",
    ),
    A(
        "update skill: refresh failure and vanished projectPath are handled",
        SKILLS / "update" / "SKILL.md",
        contains_all(
            "exits non-zero",
            "no longer exists",
        ),
        "a failed marketplace refresh must not read as success; a deleted project is skipped with a note",
    ),
    A(
        "update skill: no registry hand-editing or hard-coded cache root",
        SKILLS / "update" / "SKILL.md",
        contains_none(
            "installed_plugins.json",
            "known_marketplaces.json",
            "cache/cc10x/cc10x",
            "$HOME/.claude",
        ),
        "the skill must not edit the registry or assume a cache path; installPath comes from the CLI",
    ),
    # --- P4.T1.1: remediation reference (B1, B6, B9 part, B10 part, A4 part) ---
    A(
        "remediation: REM-FIX TaskCreate template exists with the standard shape",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "### REM-FIX TaskCreate template",
            "kind:remfix\\norigin:{originating agent}",
            "COVERING_TESTS, TEST_COMMAND and TEST_OUTPUT",
        ),
        "the router has one literal REM-FIX TaskCreate whose body asks the fix agent for the re-review proof fields",
    ),
    A(
        "remediation: every REM-FIX proof field names exactly one producer",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "### Producers of the REM-FIX gate fields",
            "`COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT` are produced by the remediating builder",
            "`FINDING_DISPUTED`, `VERIFY_COMMAND` and `VERIFY_OUTPUT` are produced by the remediating builder",
            "`DISPUTE_UPHELD` and `DISPUTE_REJECTED` are produced by `integration-verifier`",
        ),
        "the gate fields have a named producer so the fail-closed gate can be satisfied",
    ),
    A(
        "remediation: circuit breaker defined once, other phrasings are pointers",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: text.count("\n### Circuit breaker\n") == 1
        and re.search(r"- If count >= 3, ask the user how to proceed BEFORE creating a 4th remediation cycle\.", text) is not None
        and len(re.findall(r">= ?3", text)) == 1
        and "`>= 3` circuit breaker above" not in text
        and "count >= 3 circuit-breaker gate" not in text
        and "(count `>= 3` -> ask the user)" not in text
        and "Apply the circuit breaker above" not in text,
        "one definition of the 3-cycle limit; the fan-out, loop and consolidation texts point at it",
    ),
    A(
        "remediation: breaker backstop is audit-mode accurate, not claimed hook-enforced",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "Hook-enforced" not in text
        and "hook-enforced" not in text
        and "`taskMetadata`" in text
        and "audit" in text,
        "the guard blocks only when taskMetadata is block; the shipped default is audit, so the backstop is a warning",
    ),
    A(
        "remediation: unreachable branches are marked, not presented as live",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "Legacy agent-created remediation tasks are still accepted" not in text
        and "or on the re-reviewer for REVIEW" not in text
        and "REVIEW never creates a REM-FIX" in text,
        "REVIEW creates no REM-FIX and agents create none, so those branches cannot run",
    ),
    # --- P4.T1.2: policy reference and skeleton (B7, B8, B10, C2 part, B14 part) ---
    A(
        "policy: every agent row names only fields that agent's contract carries",
        POLICY_REF,
        policy_table_matches_agents,
        "required-field rows exist for every router-validated agent and no row demands a field the agent never emits",
    ),
    A(
        "policy: planner row carries the revision fields and the amendment-lane fields",
        POLICY_REF,
        lambda text: all(
            token in policy_required_rows(text).get("planner", "")
            for token in ("`PLAN_REVISION`", "`LAST_REVIEWED_REVISION`", "`AMENDED_FILES`", "`STALE_SWEEP`", "`RECONCILIATION_RERUN`")
        )
        and "IMPLEMENTATIONS_FOUND" not in text,
        "the planner revision pair and the qa-re-plan sweep fields are required where the router reads them; the unused researcher alias is gone",
    ),
    A(
        "policy: contract parsing direction is STATUS from the YAML block for every agent",
        POLICY_REF,
        lambda text: "the router branches on `STATUS` from the fenced YAML block that follows the `### Router Contract (MACHINE-READABLE)` heading" in text
        and "the YAML block decides" in text
        and "For write agents, parse the final fenced YAML block" not in text,
        "the policy no longer implies the envelope is primary for some agents",
    ),
    A(
        "policy: normalized_phases uses the build-workflow field names",
        POLICY_REF,
        lambda text: all(
            name in text.split("- `normalized_phases` stores", 1)[-1].split("- Bright Data MCP", 1)[0]
            for name in ("`phase_id`", "`title`", "`objective`", "`inputs`", "`files/surfaces`", "`expected_artifacts`", "`required_checks`", "`checkpoint_type`", "`exit_criteria`", "`test_seams`")
        )
        and all(
            name in read(SKILLS / "cc10x-router" / "references" / "build-workflow.md")
            for name in ("`files/surfaces`", "`expected_artifacts`", "`required_checks`", "`checkpoint_type`")
        ),
        "one set of phase field names across the artifact schema and BUILD preparation",
    ),
    A(
        "policy: plan_trust_gate has one definition, no phantom plan_trust anchor",
        POLICY_REF,
        lambda text: text.count("`plan_trust_gate` —") == 1
        and "`plan_trust` anchor" not in text
        and "BUILD preparation step 3" in text,
        "the gate points at the checks in build-workflow.md instead of citing an artifact key that does not exist",
    ),
    A(
        "policy: DIFF_DRIVEN_DOCS skip is stated where the router reads it",
        POLICY_REF,
        contains_all("`DIFF_DRIVEN_DOCS: skip`", "`activeContext.md ## Session Settings`"),
        "the opt-out lives in activeContext.md Session Settings, which is what the router reads",
    ),
    A(
        "policy: verification_rigor ships null and must be set explicitly",
        POLICY_REF,
        contains_all("`verification_rigor` ships as `null`", "set explicitly"),
        "a pre-filled default made the must-be-explicit check unable to fire",
    ),
    A(
        "policy: CONVERGENCE_STATES defined and listed",
        POLICY_REF,
        contains_all("`CONVERGENCE_STATES`", "`pending`", "`needs_iteration`", "`converged`", "`N/A`"),
        "quality.convergence_state has a defined value set the replay check enforces",
    ),
    A(
        "policy: event types split into emitted, hook-emitted and not emitted",
        POLICY_REF,
        lambda text: all(
            name in text
            for name in ("`result_persisted`", "`inline_fallback_entered`", "`compact_occurred`", "`artifact_mutated`")
        )
        and "Not emitted by any router step or hook" in text
        and text.index("Not emitted by any router step or hook") < text.index("`agent_started`")
        and text.index("Not emitted by any router step or hook") < text.index("`scope_decision_resolved`"),
        "the event list says which types are real and which are reserved names",
    ),
    A(
        "policy: PostToolUse behavior stated as documented, not as rejection",
        POLICY_REF,
        lambda text: "the PostToolUse guard rejects" not in text
        and "cannot undo the write" in text
        and "malformed artifact stays on disk" in text,
        "exit 2 feeds stderr to the model after the write has happened",
    ),
    A(
        "policy: hooks key on the newest artifact and phase_exit_gate is router-enforced",
        POLICY_REF,
        contains_all(
            "newest modification time",
            "`phase_exit_gate` is enforced by the router, not by any hook",
        ),
        "two live workflows can make a hook read the other one; no hook checks phase exit",
    ),
    A(
        "policy: hooks skip finished workflows when choosing the newest artifact",
        POLICY_REF,
        lambda text: text.count("newest modification time in `.cc10x/workflows/` that is not finished") == 1
        and "last `status_history` event is not `memory_finalized`, `workflow_completed` or `workflow_failed`" in text,
        "P5.T5 hooks ignore artifacts whose last status_history event is terminal; the reference must say so",
    ),
    A(
        "policy: zero-finding bounce keeps the floor and says what it is",
        POLICY_REF,
        lambda text: text.count("fewer than 3 file:line evidence citations") == 1
        and "does not change the per-finding reporting floor" in text,
        "the 3-citation check on a zero-finding approval is kept; the per-finding confidence floor is untouched",
    ),
    A(
        "build-workflow: multi-phase iteration rule has one home",
        ROUTER_REFS / "build-workflow.md",
        contains_all(
            "#### Multi-phase iteration",
            "only after the previous phase's `phase_exit_gate` passes",
            "Memory Update is created once per workflow",
            "never finalized after an earlier phase",
        ),
        "next-phase graph follows phase_exit_gate; one Memory Update after the last phase (B3)",
    ),
    A(
        "build-workflow: Memory Update blocks on the last phase's verifier or doc-sync",
        ROUTER_REFS / "build-workflow.md",
        contains_all("blocked on the LAST phase's `integration-verifier`", "or its doc-sync task"),
        "matches the multi-phase-memory-finalize fixture blockedBy rule",
    ),
    A(
        "debug-workflow: fan-out scope stays inside the task-metadata enum",
        ROUTER_REFS / "debug-workflow.md",
        lambda text: "scope:{files" not in text
        and "Files you own (do NOT edit outside this set)" in text
        and "`scope:` is a closed enum" in text,
        "the owned file set travels in the description body; scope: stays N/A (B8)",
    ),
    A(
        "policy: inline verification is defined by pointing at the inline-mode section",
        POLICY_REF,
        contains_all("`SKILL.md` section \"Inline no-subagent execution\"", "inline verification pass"),
        "the phrase 'run inline verification' has one definition (B10)",
    ),
    A(
        "triage-workflow: Memory Update task blocked on the triage task, advisory-only unchanged",
        ROUTER_REFS / "triage-workflow.md",
        contains_all("phase:memory-finalize", "addBlockedBy: [triage_task_id]", "Never spawn Agent() for this task", "Advisory-only"),
        "TRIAGE graph gains the router-inline Memory Update task (B2, ADR 0002 keeps it advisory)",
    ),
    A(
        "codebase-health-workflow: Memory Update task blocked on the scanner task",
        ROUTER_REFS / "codebase-health-workflow.md",
        contains_all("phase:memory-finalize", "addBlockedBy: [scanner_task_id]", "Never spawn Agent() for this task", "Advisory-only"),
        "CODEBASE-HEALTH graph gains the router-inline Memory Update task (B2)",
    ),
    A(
        "qa-workflow: no citation of a decision record that does not exist",
        ROUTER_REFS / "qa-workflow.md",
        lambda text: not re.search(r"ADR-\d|RFC §|\(RFC", text),
        "docs/adr holds only 0001 and 0002; the QA numbered ADR-n and RFC section citations pointed at nothing (B9)",
    ),
    A(
        "qa-workflow: circuit-breaker backstop is called audit, not hook-enforced",
        ROUTER_REFS / "qa-workflow.md",
        lambda text: "hook-enforced" not in text and text.count("audit backstop for the 3-cycle breaker") == 1,
        "taskMetadata ships as audit; consistent with remediation-and-research.md (B1/B9)",
    ),
    A(
        "qa-workflow: qa-plan dispatch overrides the planner's docs/plans save path",
        ROUTER_REFS / "qa-workflow.md",
        contains_all("Do NOT save a plan under `docs/plans/`", "the two artifacts named here are the plan"),
        "planner.md saves to docs/plans; the QA scaffold names the sole write targets (A5)",
    ),
    A(
        "router: precedence stated once; QA/ORIENT/REVIEW cases are applications of it (B4)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: text.count("the lower Priority number wins") == 1
        and "applications of this test, not exceptions to it" in text
        and "**QA over REVIEW**" in text
        and "QA beats REVIEW" not in text
        and "prefer ORIENT" not in text,
        "the three precedence statements reduce to one rule: the primary-deliverable test first, the lower number only on a genuine tie",
    ),
    A(
        "router: TRIAGE and CODEBASE-HEALTH references are route-and-load pointed (B2)",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "`references/triage-workflow.md`",
            "`### TRIAGE preparation`",
            "`### TRIAGE task graph`",
            "`references/codebase-health-workflow.md`",
            "`### CODEBASE-HEALTH preparation`",
            "`### CODEBASE-HEALTH task graph`",
        ),
        "the two advisory routes load their workflow reference like every other route",
    ),
    A(
        "router: hydration covers TRIAGE and CODEBASE-HEALTH, which create no parent task (B2)",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all("TRIAGE and CODEBASE-HEALTH create no parent task", "`CC10X triage-agent:`", "`CC10X architecture-scanner:`"),
        "resume can find an advisory workflow by its agent task or pending Memory Update task, scoped by wf:",
    ),
    A(
        "router: marker rules keep only the read markers (B10)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "[BUILD-START" not in text
        and "[PLAN-START" not in text
        and "[DEBUG-RESET: wf:{workflow_uuid}]" in text
        and "[QA-START: wf:{workflow_uuid}]" in text,
        "BUILD-START and PLAN-START were written and read nowhere; DEBUG-RESET and QA-START are read",
    ),
    A(
        "router: circuit breaker has no second count phrasing outside the pinned pointers (B6)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "`### Circuit breaker` in `references/remediation-and-research.md`" in text
        and "3-cycle remediation limit" not in text,
        "the inline-mode rule points at the single circuit-breaker definition instead of restating the count",
    ),
    A(
        "router: only an explicit opt-out skips the router gates (B5)",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all("Only an explicit user opt-out", "\"skip cc10x\""),
        "a small edit still routes as BUILD trivial scope; opt-out phrases are the sole bypass",
    ),
    A(
        "router: plugin-root resolver line is a substituted body line (B11)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: any(
            line.startswith("Plugin root for commands in reference files: ${CLAUDE_PLUGIN_ROOT};")
            and line.count("${CLAUDE_PLUGIN_ROOT}") == 1
            and "plugin-root placeholder" in line
            for line in text.splitlines()
        ),
        "one body line carries the substituted root once and tells the router what a literal placeholder in a reference means",
    ),
    A(
        "router: task tools optional, artifact is the source of truth (A3)",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "Task tools are optional.",
            "artifact is the source of truth",
            "`CLAUDE_CODE_ENABLE_TODO_TOOLS=1`",
            "`CLAUDE_CODE_TASK_LIST_ID`",
        ),
        "the router tolerates absent TaskCreate/TaskList and names the opt-in variables",
    ),
    A(
        "router: write-agent completion text states the router completes every task (A3, C4.1c, remediation 1)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "should already have called" not in text
        and "may have called `TaskUpdate" not in text
        and "No write agent holds `TaskUpdate` or is told to call it. The router completes the task with `TaskUpdate(status=\"completed\")` after the contract validates." in text
        and "told to call `TaskUpdate` before their contract" not in text
        and "write agents' own `TaskUpdate` instruction is suppressed" not in text
        and "because no agent holds `TaskUpdate` or is told to call it (the router completes every task after contract validation)" in text,
        "no agent holds or is told to call TaskUpdate (P4.T4.5b), so the three router sentences that said write agents may complete their own task are replaced by the true one",
    ),
    A(
        "router: A4 claims corrected (TaskOutput, per-invocation model, handback channel)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "cannot set it per dispatch" not in text
        and "the router cannot set a model per dispatch" not in text
        and "TaskOutput with block=false" not in text
        and "`TaskOutput` is deprecated" in text
        and "SubagentHandback" in text
        and "in the background" in text,
        "no stale per-dispatch-model or TaskOutput claim; the agent report may arrive by handback or notification",
    ),
    A(
        "router: ORIENT names base-install tools, Octocode only as optional accelerators (B9)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "optional accelerators" in text.split("### ORIENT move", 1)[1].split("## 2. Memory Load", 1)[0]
        and "(use `localViewStructure`" not in text,
        "ORIENT procedure works without Octocode tools",
    ),
    A(
        "router: skeleton claim matches the null-ships-undecided skeleton (A6/B7)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "ships every required key already populated with safe defaults" not in text
        and "ship as `null`" in text,
        "the router no longer claims every key is populated; verification_rigor is router-filled",
    ),
    A(
        "router: hints law states preload versus SKILL_HINTS and the spike line is not a hint (C4.3, B10)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: all(
            token in text
            for token in (
                "Frontmatter `skills:` preloads carry each agent's role-core skills",
                "everything else reaches an agent only through SKILL_HINTS",
                "the router is the only authority that adds situational skills",
                "never passes a skill the agent already preloads",
                "`cc10x:exploration` is not a SKILL_HINTS entry",
            )
        )
        and "Include `cc10x:exploration` only" not in text,
        "the hints law names the real rule and the unreachable spike hint is marked as inline-only",
    ),
    # --- P4.T1.5c: router description and prose (B13, E11 part) ---
    A(
        "router: description is third-person, unshouted, keeps trigger verbs, hands off guide/update (B13)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: router_description(text).lstrip("| \n").startswith("Routes ")
        and "CRITICAL" not in router_description(text)
        and "THE ONLY ENTRY POINT" not in router_description(text)
        and "Route and execute immediately" not in router_description(text)
        and all(
            verb in router_description(text)
            for verb in ("build", "implement", "create", "write", "add", "update", "change", "fix", "review", "plan", "test", "refactor")
        )
        and "`cc10x-guide`" in router_description(text)
        and "`update` skill" in router_description(text),
        "the activation text names what the router does, keeps the verbs the product activates on (over-trigger risk unmeasured, no paid eval), and sends questions about cc10x and 'update cc10x' to the skills that own them",
    ),
    A(
        "router: audit-named no-op sentences removed (E11)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "Runtime contract only." not in text
        and "as the canonical" not in text
        and "Turn-count dominates price" not in text
        and "Maintain professional objectivity" not in text
        and "Drift accumulates silently" not in text
        and "Treat it as load-bearing orchestration law" not in text
        and "Do not rationalize a failing workflow as \"close enough\"" in text,
        "the label, the repeated 'canonical law' sentences, the unactionable cost paragraph and the two ceremonial openers are gone; the operative rationalization rule stays",
    ),
    A(
        "router: each workflow preparation block still names its reference and both blocks (E11 guard)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: all(
            f"immediately read `references/{ref}-workflow.md`" in text and f"`### {blk} preparation`" in text and f"`### {blk} task graph`" in text
            for ref, blk in (("build", "BUILD"), ("debug", "DEBUG"), ("review", "REVIEW"), ("qa", "QA"), ("plan", "PLAN"))
        ),
        "tightening the preparation bullets keeps the read-first instruction and both block names for the five routes",
    ),
    # --- P4.T1.6: amendment-lane anchors in qa-workflow.md ---
    A(
        "qa-workflow: amendment-lane sweep fields are defined and gate the pass-2 task (A5)",
        ROUTER_REFS / "qa-workflow.md",
        contains_all(
            "- `AMENDED_FILES:` every artifact touched",
            "**All three plan artifacts are in scope on every amendment.**",
            "- `STALE_SWEEP:` for each corrected fact",
            "- `RECONCILIATION_RERUN:` the arithmetic restated after the amendment",
            "If any of the three is missing or empty, the gate fails closed: do **NOT** create the pass-2 task.",
        ),
        "the three sweep fields carry their definitions and the fail-closed rule in the QA reference, not only their names",
    ),
    A(
        "router evals: eval-01 teaches the primary-deliverable rule and the DEFAULT row is priority 8 (B4)",
        ROUTER_EVALS / "eval-01-error-beats-build.md",
        lambda text: "primary deliverable" in text and "priority-8" in text and "priority-7" not in text and "first matching signal" not in text,
        "the ERROR-vs-BUILD eval decides by deliverable, not first keyword, and names the table's real DEFAULT priority",
    ),
    A(
        "router evals: eval-02 and eval-03 agree with the table (B4)",
        ROUTER_EVALS / "eval-02-review-stays-advisory.md",
        lambda text: "primary-deliverable test" in text and "priority 3" in text,
        "the REVIEW eval applies the same deliverable test as eval-01 and cites the REVIEW row number",
    ),
    A(
        "router evals: eval-03 names the DEFAULT row as priority 8 (B4)",
        ROUTER_EVALS / "eval-03-skip-router-multifile.md",
        lambda text: "priority-8 DEFAULT" in text and "priority-7" not in text,
        "the DEFAULT row is priority 8 in the routing table",
    ),
    A(
        "router evals: README names the real checker path (C12)",
        ROUTER_EVALS / "README.md",
        lambda text: "tools/doc_consistency_check.py" in text and "cc10x_doc_consistency_check" not in text,
        "the README points at the checker that exists",
    ),
    # --- P4A remediation 1, commit 1: artifact-only graph mode and the single breaker count ---
    A(
        "router: Task tools absent selects artifact-only graph mode, agents still dispatched through the Agent tool",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"ARTIFACT-ONLY GRAPH MODE\..{0,500}every agent is still dispatched through the Agent tool with fresh context",
            text,
            re.S,
        )
        is not None
        and "The inline no-subagent fallback (§12) applies only when the Agent/dispatch primitive itself is unavailable" in text
        and "take the inline fallback (§12, trigger 1)" not in text,
        "missing Task tools must not collapse reviewer, hunter and verifier into the router's own context",
    ),
    A(
        "router: artifact-only resume reads the artifact by scope, pending_gate first, never newest-by-mtime alone",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"Artifact-only resume.{0,300}never by modification time alone.{0,900}`pending_gate` first.{0,300}`phase_cursor`.{0,60}`phase_status`.{0,60}`results`",
            text,
            re.S,
        )
        is not None,
        "without TaskList the resume path is artifact-based and scoped like the task-based one",
    ),
    A(
        "router: inline trigger 1 means no Agent primitive; missing Task tools alone is not that trigger",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "Absent `TaskCreate`/`TaskList` alone is not this trigger" in text
        and "(no `Agent(...)` dispatch path, or `TaskCreate`/`TaskList` are absent)" not in text
        and re.search(r"inline verification pass.{0,600}reviewer pass and a hunter pass", text, re.S) is not None
        and "inline mode does not skip" in text,
        "inline mode keeps the reviewer and hunter passes inside the verifier pass; trigger 1 is the dispatch primitive only",
    ),
    A(
        "router: chain loop and hard rules name artifact-only graph mode beside the other sanctioned degrades",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"Artifact-only graph mode: read .task. in this loop as a graph step recorded in the artifact", text) is not None
        and "artifact-only graph mode when the Task tools are missing" in text,
        "sections 4, 12 and 14 describe the same two modes",
    ),
    A(
        "remediation: breaker counts remediation_history entries, asks BEFORE creating a 4th cycle, task count is a cross-check only",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: re.search(r"- Count the entries in the workflow artifact's `remediation_history`[^\n]{0,200}authoritative without Task tools[^\n]{0,200}BOTH modes", text) is not None
        and re.search(r"- If count >= 3, ask the user how to proceed BEFORE creating a 4th remediation cycle", text) is not None
        and re.search(r"[Oo]nly when Task tools exist[^\n]{0,200}mismatch[^\n]{0,120}LARGER of the two counts", text) is not None
        and "- Count tasks whose descriptions contain both" not in text
        and len(re.findall(r"count >= 3", text)) == 1,
        "the single breaker is evaluable without Task tools; one definition, asked before the 4th cycle exists",
    ),
    A(
        "remediation: each remediation round appends one remediation_history entry in both modes; hook counts stay one cycle behind",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: re.search(r"each remediation round appends exactly one entry[^\n]{0,300}(artifact-only|without Task tools)", text) is not None
        and "deliberately one cycle BEHIND" in text
        and "`taskMetadata` mode ships as `audit`" in text,
        "the audit backstop wording survives and the append rule no longer needs a REM-FIX task to exist",
    ),
    A(
        "router: Cycle row and hard rule say before a 4th cycle, matching the breaker",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "pauses the loop for a human checkpoint before a 4th remediation cycle is created" in text
        and re.search(r"Never let a remediation loop create a 4th cycle without a human checkpoint", text) is not None
        and "at the 3rd remediation cycle" not in text
        and "reach 3 cycles" not in text,
        "SKILL.md no longer restates the breaker at a different count than its single definition",
    ),
    # --- P4A remediation 1, commit 2: advisory Memory Update only at the terminal state ---
    A(
        "triage-workflow: Memory Update is a kind:memory task created only at the terminal state; NEEDS_INFO and NEEDS_GRILLING pause with none runnable",
        ROUTER_REFS / "triage-workflow.md",
        lambda text: "Memory Update is created ONLY at the terminal state" in text
        and re.search(r"terminal states are `STATUS=TRIAGED` with `NEEDS_GRILLING` not true, and `STATUS=WONTFIX`", text) is not None
        and re.search(r"`STATUS=NEEDS_INFO`, or on `NEEDS_GRILLING=true`, the workflow pauses on `pending_gate`[^\n]{0,200}no Memory Update task exists or is runnable", text) is not None
        and re.search(r"kind:memory\\norigin:router\\nphase:memory-finalize", text) is not None
        and re.search(r"second pass.{0,300}blocked by that pass's triage task", text, re.S) is not None,
        "a pause must not finalize memory; a re-dispatch must not land on a finalized workflow (double-finalize)",
    ),
    A(
        "codebase-health-workflow: Memory Update is a kind:memory task created only after the report is presented and any chosen grill completed",
        ROUTER_REFS / "codebase-health-workflow.md",
        lambda text: "Memory Update is created ONLY at the terminal state" in text
        and re.search(r"terminal state is `STATUS=NO_CANDIDATES`, or `STATUS=CANDIDATES_FOUND` with the report presented and the user declined or moved on, or the chosen candidate's grill completed", text) is not None
        and re.search(r"`pending_gate` \(`candidate_choice`\)[^\n]{0,200}no Memory Update task exists or is runnable", text) is not None
        and re.search(r"kind:memory\\norigin:router\\nphase:memory-finalize", text) is not None,
        "the grill after a chosen candidate happens before memory finalizes, not after",
    ),
    A(
        "router: advisory routes finalize memory only at their terminal state, pointers say so",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"single-pass: the agent task now, the router-inline Memory Update only at the terminal state; no parent task", text) is not None
        and re.search(r"a paused workflow has no Memory Update task yet", text) is not None,
        "SKILL.md pointers match the reference graphs",
    ),
    # --- P4A remediation 1, commit 3: contract direction, phase ordering, rigor, misc ---
    A(
        "router: read-only contracts follow one rule, the YAML STATUS decides; envelope and heading are fast-path or fallback only",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"the `STATUS` in the fenced YAML Router Contract block decides\..{0,400}fast-path signals.{0,200}only when the YAML block is absent.{0,200}the YAML decides",
            text,
            re.S,
        )
        is not None
        and "Primary signal:" not in text
        and "1. Try the envelope on line 1." not in text,
        "SKILL.md no longer says the envelope is primary while the policy says the YAML decides",
    ),
    A(
        "router: YAML anchor by position for the read-only agents without the heading, and plan-gap-reviewer's own status field",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"otherwise take the first fenced `yaml` block after the envelope and heading \(`code-reviewer`, `failure-hunter`, `integration-verifier`, `plan-gap-reviewer`, `triage-agent` and `architecture-scanner` carry no such heading\)",
            text,
        )
        is not None
        and re.search(r"`plan-gap-reviewer` emits `PLANNING_REVIEW_STATUS: PASS\|FINDINGS`[^\n]{0,40}not `STATUS`", text) is not None
        and "If the YAML block is absent or any required contract field is missing, whatever the envelope and heading say, run inline verification rather than approving" in text,
        "the router finds the contract block of agents that lack the heading anchor, and reads the right status field for the plan reviewer",
    ),
    A(
        "build-workflow: next phase's builder is blocked on the previous phase's LAST task so the BASE is re-recorded after doc-sync",
        ROUTER_REFS / "build-workflow.md",
        lambda text: re.search(
            r"its builder is blocked on the previous phase's LAST task \(its doc-sync task when one exists, else its `integration-verifier`\), so step 11a re-records `results.git_base_sha` only after phase N is fully done",
            text,
        )
        is not None
        and "the doc-syncer diffs `results.git_base_sha..HEAD`" in text,
        "doc-sync of phase N must not race the next phase's BASE re-record",
    ),
    A(
        "build-workflow: both task-graph templates say Memory Update is created only with the last phase's graph",
        ROUTER_REFS / "build-workflow.md",
        lambda text: text.count("// Memory Update: create ONLY with the LAST phase's graph (see Multi-phase iteration); omit it for earlier phases.") == 2,
        "the multi-phase exception sits where the template is applied, not only in prose above",
    ),
    A(
        "router: BUILD task-graph pointer carries the multi-phase memory exception",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"`### BUILD task graph` block verbatim, including its multi-phase exception \(Memory Update is created once, with the LAST phase's graph\)",
            text,
        )
        is not None,
        "'apply verbatim' no longer contradicts the once-per-workflow memory rule",
    ),
    A(
        "router: verification_rigor is set at workflow preparation, standard when no plan exists",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"`verification_rigor`: `standard` \| `critical_path`; the router sets it at workflow preparation: `standard` when no plan exists[^\n]{0,160}planner contract once a plan exists",
            text,
        )
        is not None,
        "non-plan routes (direct BUILD, DEBUG, REVIEW, QA) no longer leave the skeleton null",
    ),
    A(
        "build-workflow: step 7 sets standard rigor when plan path is N/A",
        ROUTER_REFS / "build-workflow.md",
        lambda text: re.search(r"7\. Persist the approved `plan_mode` and `verification_rigor` from the planner contract[^\n]{0,200}when plan path is `N/A`, set `verification_rigor` to `standard`", text) is not None,
        "the direct-BUILD route has a setter for the field the gate requires",
    ),
    A(
        "policy: verification_rigor has one setter sentence, standard until a plan exists, then the planner contract",
        POLICY_REF,
        lambda text: re.search(
            r"must set explicitly `standard` or `critical_path`: `standard` at workflow preparation whenever no plan artifact exists yet[^\n]{0,200}overwritten from the planner contract once a plan exists",
            text,
        )
        is not None
        and "before dispatching planner or builder" not in text,
        "the policy no longer asks for the planner's value before the planner has run",
    ),
    A(
        "router: parent-task pattern is scoped to the routes that create a parent task",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"Use this pattern for every new workflow that has a parent task \(BUILD, DEBUG, REVIEW, PLAN, QA\)\. TRIAGE and CODEBASE-HEALTH create no parent task[^\n]{0,200}skip the `TaskCreate` step",
            text,
        )
        is not None
        and "Use this pattern for every new workflow:" not in text,
        "section 6 no longer contradicts the advisory routes' no-parent-task rule",
    ),
    A(
        "router: convergence_state is set to converged at memory finalization, N/A for the advisory routes",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"set `quality\.convergence_state=converged` when[^\n]{0,300}final phase's `phase_exit_gate`[^\n]{0,300}memory is finalized[^\n]{0,200}`N/A`",
            text,
        )
        is not None,
        "something writes converged and N/A; CONVERGENCE_STATES stays the value set",
    ),
    A(
        "policy: event lists add inline_fallback_exited and parallel_fallback; finding_dropped is a status_history entry",
        POLICY_REF,
        lambda text: re.search(r"  - `inline_fallback_exited`", text) is not None
        and re.search(r"  - `parallel_fallback`", text) is not None
        and re.search(r"`finding_dropped` is a `status_history` entry[^\n]{0,160}not an event-log type", text) is not None,
        "the policy event lists name what the router text actually logs",
    ),
    A(
        "router: failure-hunter is a remfix origin and has a dispatcher row handled by the builder",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"origin:\{router\|component-builder\|bug-investigator\|code-reviewer\|failure-hunter\|", text) is not None
        and re.search(r"`kind:remfix` \+ `origin:code-reviewer` / `origin:failure-hunter` / `origin:integration-verifier` / `origin:router` \| `cc10x:component-builder`", text) is not None,
        "a hunter-originated REM-FIX is a valid origin and is dispatched like a reviewer-originated one",
    ),
    # --- P4A remediation 1, commit 4: pins on the decisive clause of each behavior ---
    A(
        "router: ORIENT-vs-REVIEW tie-break clause, only a genuine tie goes to REVIEW",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"\"help me understand\" is ORIENT, \"tell me what's wrong\" is REVIEW; only a genuine tie goes to REVIEW \(lower number\)\.",
            text,
        )
        is not None
        and re.search(r"genuinely holds for more than one row, the lower Priority number wins", text) is not None,
        "the deliverable decides first; a swapped or widened tie-break would send explanation requests to REVIEW",
    ),
    A(
        "router: plugin-root line says reference files read through Read arrive literal and the placeholder is never run as-is",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: any(
            line.startswith("Plugin root for commands in reference files: ${CLAUDE_PLUGIN_ROOT};")
            and re.search(r"reference files read through Read arrive with the placeholder literal", line) is not None
            and re.search(r"build the absolute path from the value on this line; never run the placeholder as-is\.$", line) is not None
            and "agent prompts" not in line
            for line in text.splitlines()
        ),
        "the operative clause is pinned, and the line claims only what is certain (agent bodies are substituted by the host too)",
    ),
    A(
        "policy: memory_sync_gate names the router-inline Memory Update and the memory_finalized event",
        POLICY_REF,
        lambda text: re.search(
            r"- `memory_sync_gate` — the workflow may not reach final state until Memory Update ran \(router-inline, never a subagent\) and the `memory_finalized` event is in the event log",
            text,
        )
        is not None,
        "the gate's two evidence conditions and the inline-only rule are one clause; dropping either re-opens a subagent memory task",
    ),
    A(
        "skeleton: verification_rigor ships null (undecided), pinned on the JSON file",
        ROUTER_REFS / "workflow-artifact.skeleton.json",
        lambda text: json.loads(text).get("verification_rigor", "missing") is None,
        "a pre-filled default makes plan_trust_gate's must-be-explicit check unable to fire",
    ),
    A(
        "remediation: producers of the gate fields are named per agent, declared in the contracts, and the gates still fail closed",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: re.search(r"`AMENDED_FILES`, `STALE_SWEEP` and `RECONCILIATION_RERUN` are produced by `planner` on a `phase:qa-re-plan` return", text) is not None
        and re.search(r"The producers are declared in the agent contracts, and the gates still fail closed when an agent omits them[^\n]{0,200}a `qa-re-plan` return without the three sweep fields creates no pass-2 task", text) is not None
        and "Until the agent files declare these producers" not in text
        and "agent-file work, P4B" not in text,
        "H3: the present state is stated (the producers exist), the router does not paper over a missing field, and the stale future-tense clause is gone",
    ),
    # --- P4A remediation 2, commit 1: resume, step completion, notes sink, terminal state, advisory failure ---
    A(
        "router: artifact-only step completion comes from the phase-keyed events log, newer than the phase boundary event, never from a results slot",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"a graph step is complete only if the events log holds a `result_persisted` event for its agent and task phase with `details\.phase_id` equal to the current `phase_cursor`, appended after the latest `phase_started` or `remediation_created` event for that phase_id",
            text,
        )
        is not None
        and re.search(r"`results\.\*` holds only the latest value and never proves a step done", text) is not None
        and "the next step is the first step of that route's graph with no completed `results` entry" not in text,
        "flat results slots from an earlier phase or REM-FIX cycle must not make a step of the current phase look done",
    ),
    A(
        "router: the artifact-only ordering text and the chain-loop paragraph use the same events-log completion rule",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"Blockers are the ordering rules of the route's `references/\*-workflow\.md` graph, evaluated with the events-log completion rule of §4", text) is not None
        and "evaluated from `results` and `phase_status`" not in text,
        "section 12 must not restate completion from the flat results slots",
    ),
    A(
        "router: result_persisted events carry details.phase_id so the completion rule can key on the phase",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r'"event":"result_persisted","phase":"<phase>","task_id":"<task_id>","agent":"<agent_name>"[^\n]{0,160}"details":\{"phase_id":"<phase_cursor>"\}', text) is not None,
        "an event without the plan phase id cannot be matched to the current phase_cursor",
    ),
    A(
        "build-workflow: step 11a appends a phase_started event with details.phase_id when it re-records the BASE",
        ROUTER_REFS / "build-workflow.md",
        lambda text: re.search(r"11a\..{0,1800}append a `phase_started` event[^\n]{0,200}`details\.phase_id`", text, re.S) is not None,
        "the boundary event exists because a router step appends it",
    ),
    A(
        "policy: event lists add phase_started and remediation_created as router-appended, with details.phase_id",
        POLICY_REF,
        lambda text: re.search(r"  - `phase_started` \(", text) is not None
        and re.search(r"  - `remediation_created` \(", text) is not None
        and not re.search(r"Not emitted by any router step or hook[^\n]*\n(  - `[a-z_]+`\n)*  - `remediation_created`\n", text)
        and "`details.phase_id`" in text,
        "the two boundary events moved from not-emitted to emitted together with the steps that append them",
    ),
    A(
        "remediation: the audit-backstop append also appends a remediation_created event with details.phase_id",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: re.search(r"append a `remediation_created` event[^\n]{0,160}`details\.phase_id`", text) is not None,
        "the REM-FIX boundary is written where the remediation_history entry is written",
    ),
    A(
        "router: captured Memory Notes always append to artifact memory_notes, and also to the memory task description when one exists",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"Append the captured notes to the artifact `memory_notes` at once, always,[^\n]{0,200}no memory task exists", text) is not None
        and re.search(r"append the extracted notes to the artifact `memory_notes`, and to the memory task description when one exists", text) is not None,
        "notes captured during an advisory pause have no memory task and must still have a sink",
    ),
    A(
        "router: Memory Update reads memory_notes from the artifact plus any task payload and clears nothing before persistence succeeds",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"artifact `memory_notes` plus any task description payload[^\n]{0,200}(Leave|leave)[^\n]{0,120}`memory_notes`[^\n]{0,120}every (persistence )?write has succeeded", text) is not None,
        "a failed memory write must not lose the notes",
    ),
    A(
        "router: resume drops terminal workflows first and defines the terminal test",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"Terminal test: a workflow is terminal when its events log or `status_history` holds `memory_finalized`, `workflow_completed` or `workflow_failed`, or its `phase_cursor` is `memory-finalize` and completed",
            text,
        )
        is not None
        and re.search(r"1\. Identify the active parent workflow, dropping every terminal workflow first", text) is not None,
        "a finished advisory workflow must not capture a fresh request",
    ),
    A(
        "router: a non-terminal artifact's pending_gate is answered by the user's reply and then cleared with the exact words recorded",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"the user's reply answers it[^\n]{0,300}CLEARS it \(sets null and records the answer in `status_history` in the user's exact words\)[^\n]{0,200}reaches a terminal state",
            text,
        )
        is not None,
        "nothing else clears pending_gate, so a terminal advisory workflow would keep it",
    ),
    A(
        "router: zero non-terminal matches starts a new workflow, more than one asks which, advisory routes fall back to artifacts with a pending_gate",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"none starts a new workflow \(say so\)", text) is not None
        and re.search(r"more than one,? ask which", text) is not None
        and re.search(r"fall back to the non-terminal artifacts that carry a `pending_gate` and have `workflow_type` TRIAGE or CODEBASE-HEALTH", text) is not None,
        "the paused advisory workflow has no parent task and needs a locator in Task-tools mode",
    ),
    A(
        "router: memory finalization clears pending_gate",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"persist workflow artifact results \+ Memory Notes[^\n]{0,300}set `pending_gate` to null", text) is not None,
        "a terminal advisory artifact carries no pending_gate",
    ),
    A(
        "triage-workflow: agent failure sets failure_stop_gate with a naming pending_gate, creates no Memory Update, only the user's decline finalizes a pause",
        ROUTER_REFS / "triage-workflow.md",
        lambda text: re.search(r"### TRIAGE failure and abandonment", text) is not None
        and re.search(r"error or a malformed contract sets `failure_stop_gate`[^\n]{0,200}`pending_gate` `triage_agent_failed`", text) is not None
        and re.search(r"creates NO Memory Update", text) is not None
        and re.search(r"Only the user's decline or end finalizes a pause[^\n]{0,300}stays open", text) is not None,
        "an advisory failure has a stated state and an unanswered pause is honestly open",
    ),
    A(
        "codebase-health-workflow: scanner failure sets failure_stop_gate with a naming pending_gate, creates no Memory Update, only the user's decline finalizes a pause",
        ROUTER_REFS / "codebase-health-workflow.md",
        lambda text: re.search(r"### CODEBASE-HEALTH failure and abandonment", text) is not None
        and re.search(r"error or a malformed contract sets `failure_stop_gate`[^\n]{0,200}`pending_gate` `architecture_scanner_failed`", text) is not None
        and re.search(r"creates NO Memory Update", text) is not None
        and re.search(r"Only the user's decline or end finalizes a pause[^\n]{0,300}stays open", text) is not None,
        "an advisory failure has a stated state and an unanswered pause is honestly open",
    ),
    A(
        "router: advisory agent error or malformed contract sets failure_stop_gate instead of inline verification",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"for TRIAGE and CODEBASE-HEALTH[^\n]{0,200}sets `failure_stop_gate`[^\n]{0,160}no Memory Update", text) is not None,
        "inline verification means nothing for an advisory route",
    ),
    # --- P4A remediation 2, commit 2: breaker, backstop, templates, YAML selection, scaffold, misc ---
    A(
        "router: remediation_history is described as one entry per remediation round, not as a decisions log",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"exactly one `remediation_history` entry per remediation round \(see `### Circuit breaker`\)", text) is not None
        and "status_history and remediation_history entries when decisions change workflow state" not in text,
        "a general-decisions reading would break the breaker count",
    ),
    A(
        "policy: remediation_history holds exactly one entry per remediation round",
        POLICY_REF,
        lambda text: re.search(r"`remediation_history` holds exactly one entry per remediation round \(see `### Circuit breaker`", text) is not None
        and "`status_history` and `remediation_history` are append-only summaries of major router decisions" not in text,
        "the schema note must agree with the breaker's count rule",
    ),
    A(
        "remediation: on a task-count mismatch the breaker uses the LARGER of the two counts and reports it",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: re.search(r"on a mismatch, report it to the user and use the LARGER of the two counts", text) is not None
        and not re.search(r"mismatch[^\n]{0,120}artifact (count )?wins", text),
        "a missed append or a missed REM-FIX task must never lower the count",
    ),
    A(
        "remediation: the hook backstop also flags a user-authorized cycle beyond 3, so block mode is not for authorized extra cycles",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "deliberately one cycle BEHIND" in text
        and "so it fires only if the router already missed its checkpoint" not in text
        and re.search(r"cannot see the user's authorization, so it also flags a cycle the user authorized beyond 3", text) is not None
        and re.search(r"do not set `taskMetadata` to `block` when cycles beyond 3 may be authorized", text) is not None,
        "the guard counts entries and cannot see consent; the old text claimed it only fires on a router miss",
    ),
    A(
        "build-workflow: both builder templates block the builder on the previous phase's last task for phases after the first",
        ROUTER_REFS / "build-workflow.md",
        lambda text: text.count("// Phases after the first: block the builder on the previous phase's LAST task") == 2
        and text.count("TaskUpdate({ taskId: builder_task_id, addBlockedBy: [previous_phase_last_task_id] })") == 2
        and text.count("with `DIFF_DRIVEN_DOCS: skip` there is no doc-sync task, so the verifier") == 2,
        "the multi-phase ordering rule lives in the template where the task is created, not only in prose",
    ),
    A(
        "build-workflow: trivial-to-full escalation re-blocks Memory Update only when this phase's graph carries one",
        ROUTER_REFS / "build-workflow.md",
        lambda text: text.count("when this phase's graph carries a Memory Update task (only the LAST phase's does), re-block it on `doc_sync_task_id`") == 2
        and "re-block Memory Update on `doc_sync_task_id`" not in text,
        "an earlier phase has no memory task to re-block under the multi-phase rule",
    ),
    A(
        "router: one YAML-block selection rule for read-only agents, matching write agents and the policy",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"take the fenced `yaml` block that follows the `### Router Contract \(MACHINE-READABLE\)` heading when that heading exists[^\n]{0,200}otherwise take the first fenced `yaml` block after the envelope and heading",
            text,
        )
        is not None
        and re.search(r"parse the fenced YAML block that follows the `### Router Contract \(MACHINE-READABLE\)` heading", text) is not None
        and "the final fenced YAML block under" not in text,
        "first-after-envelope versus final-under-heading selected different blocks for an agent with several yaml blocks",
    ),
    A(
        "policy: the YAML-block selection rule is the router's rule",
        POLICY_REF,
        lambda text: re.search(
            r"the fenced YAML block that follows the `### Router Contract \(MACHINE-READABLE\)` heading when the heading exists, otherwise the first fenced `yaml` block after the envelope and heading",
            text,
        )
        is not None
        and "the final fenced YAML Router Contract block" not in text,
        "one selection rule in both files",
    ),
    A(
        "router: artifact-only dispatch scaffold passes Task ID N/A and tells write agents to skip TaskUpdate",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"Artifact-only mode \(Task tools absent\): pass `- Task ID: N/A`[^\n]{0,200}`Task tools are absent: skip TaskUpdate; the router records completion`", text) is not None
        and "completion, validation and every gate are unchanged" not in text
        and "completion is recorded by the router in the artifact" in text,
        "the scaffold would otherwise hand agents an empty Task ID and an instruction to call a tool that does not exist",
    ),
    A(
        "router: SELF_REMEDIATED detection is blockedBy based and cannot fire in artifact-only mode",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"blockedBy` based, so it cannot fire in artifact-only mode; there the structured remediation fields decide", text) is not None,
        "without Task tools no blockedBy exists to detect self-remediation",
    ),
    A(
        "router and policy: the verifier findings handoff and post-verifier validation are cited as section 12",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "**Verifier findings handoff** law in §12" in text and "**Verifier findings handoff** law in §13" not in text,
        "the handoff law lives in section 12 (Chain Execution Loop), not 13 (Memory Finalization)",
    ),
    A(
        "policy: finding_dropped citation names section 12",
        POLICY_REF,
        lambda text: re.search(r"post-verifier finding validation, `SKILL\.md` §12\)", text) is not None and "`SKILL.md` §13)" not in text,
        "same section-number fix in the policy reference",
    ),
    # --- P4A remediation 2, commit 3: survivors of the hunt that are cheap to pin ---
    A(
        "remediation: the backstop append names artifact-only and inline mode, where no task exists and the hook does not run",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "when the router records the REM-FIX step in artifact-only mode or inline mode (no task exists then, and the hook below does not run)" in text,
        "without this clause the append rule reads as task-bound and the artifact count goes stale in those modes",
    ),
    A(
        "router: artifact-only mode is recorded once in status_history",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "Record the mode once in `status_history`." in text,
        "resume and audit need to see which mode produced the graph",
    ),
    A(
        "router: a paused advisory workflow's pending_gate names the open question",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "its artifact `pending_gate` names the open question" in text,
        "a paused workflow has no task, so the gate is its only locator of the question",
    ),
    A(
        "router: inline mode appends remediation_history entries too",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "inline mode appends `remediation_history` entries too" in text,
        "the breaker count must exist in inline mode",
    ),
    A(
        "build-workflow: Memory Update is created once per workflow with the LAST phase's graph, never an earlier one",
        ROUTER_REFS / "build-workflow.md",
        lambda text: re.search(
            r"Memory Update is created once per workflow, with the LAST phase's graph, blocked on the LAST phase's `integration-verifier`[^\n]{0,80}It is never created with an earlier phase's graph and never finalized after an earlier phase",
            text,
        )
        is not None,
        "phase 1 of a multi-phase plan must not write memory",
    ),
    A(
        "triage-workflow: a NEEDS_GRILLING pause ends in Memory Update only after a second pass returns a terminal state",
        ROUTER_REFS / "triage-workflow.md",
        lambda text: re.search(r"`pending_gate: needs_grilling`\) with no Memory Update task until the grilled result has fed a second triage-agent pass that returns a terminal state", text) is not None
        and re.search(r"On a terminal result it then creates the Memory Update task \(blocked by that triage task\)", text) is not None,
        "the grill result must reach a terminal pass before memory finalizes",
    ),
    A(
        "triage-workflow: WONTFIX is terminal regardless of NEEDS_GRILLING, matching the replay checker",
        ROUTER_REFS / "triage-workflow.md",
        lambda text: re.search(r"terminal states are `STATUS=TRIAGED` with `NEEDS_GRILLING` not true, and `STATUS=WONTFIX`\. On `STATUS=NEEDS_INFO`", text) is not None,
        "the checker's triage_is_terminal and this sentence must stay the same rule",
    ),
    # --- P4A remediation 3, commit 1: pending-gate locator, pause results, remediation graph, N/A phase id ---
    A(
        "router: artifact-only resume with no scope match looks up non-terminal artifacts carrying a pending_gate; exactly one answers, more than one asks which, none starts a new workflow",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"never by modification time alone; one match resumes it, more than one, ask which; when none matches, look up the paused workflow a bare reply answers: the candidates are the non-terminal artifacts with a non-null `pending_gate`",
            text,
        )
        is not None
        and re.search(r"exactly one candidate means the reply is the answer to its `pending_gate`", text) is not None
        and re.search(r"more than one, ask which \(list each gate name and `user_request`\), none starts a new workflow \(say so\)", text) is not None,
        "a new session's bare reply to a paused question matches no uuid and no user_request, and would orphan the paused artifact",
    ),
    A(
        "router: the step 0 stop-state hint is a candidate source for the pending-gate lookup",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"the `wf` the step 0 hint names counts when its artifact is non-terminal and has one", text) is not None,
        "the hint is already described as a locator of the live wf; the lookup must be allowed to use it",
    ),
    A(
        "router: a result_persisted whose decision is NEEDS_INFO or NEEDS_GRILLING does not complete its step, only a terminal-status result does",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"a `result_persisted` whose `decision` is `NEEDS_INFO` or `NEEDS_GRILLING` is the pause of a pass that a second pass of the same agent and task phase follows, so it does not complete its step and only a terminal-status result does",
            text,
        )
        is not None,
        "the advisory second pass reuses (agent, task phase); pass 1's event must not make resume jump to Memory Update",
    ),
    A(
        "router: CANDIDATES_FOUND completes the scanner step because no second scanner pass follows",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"`CANDIDATES_FOUND` completes the scanner step: no second pass follows and `pending_gate` carries the pause", text) is not None,
        "treating CANDIDATES_FOUND as a pause would re-dispatch the scanner after the user answered",
    ),
    A(
        "router: the event decision is NEEDS_GRILLING when a TRIAGED result sets NEEDS_GRILLING=true, in the router and the policy",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"`decision` is the contract status, written `NEEDS_GRILLING` when a TRIAGED result sets `NEEDS_GRILLING=true`", text) is not None
        and re.search(r"`decision` is the contract status, written `NEEDS_GRILLING` when a TRIAGED result sets `NEEDS_GRILLING=true`", POLICY_REF.read_text(encoding="utf-8")) is not None,
        "the pause rule keys on decision, and TRIAGED alone cannot tell a grilling pause from a terminal result",
    ),
    A(
        "router: the artifact-only remediation graph names the REM-FIX agent and phase, the pending verifier slot, and doc-sync after the verifier",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(
            r"the remediation graph: REM-FIX, re-review, re-hunt, re-verify \(REM-FIX is the `component-builder` step with the originating task phase; a pending original verifier that has not run takes the re-verify slot and keeps its task phase; doc-sync follows the verifier on the BUILD route as usual\)",
            text,
        )
        is not None,
        "Task-tools mode reuses the pending verifier and keeps doc-sync after it; artifact-only mode must match",
    ),
    A(
        "router: phase_id is the literal N/A when phase_cursor is null, and resume compares null, missing and N/A as equal",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: re.search(r"`details\.phase_id` is the `phase_cursor` value, written as the literal `N/A` when `phase_cursor` is null", text) is not None
        and re.search(r"null, missing and `N/A` `phase_id` values compare equal", text) is not None,
        "a no-plan BUILD keeps phase_cursor null; a model writing null, N/A or phase-1 would break the completion key after compaction",
    ),
    A(
        "policy: result_persisted phase_id is the literal N/A when phase_cursor is null",
        POLICY_REF,
        lambda text: re.search(r"`details\.phase_id` is the `phase_cursor` value, written as the literal `N/A` when `phase_cursor` is null", text) is not None,
        "the policy event list must match the router's event template",
    ),
    A(
        "build-workflow: a BUILD with no plan phases has a null phase_cursor and writes N/A as the phase_id",
        ROUTER_REFS / "build-workflow.md",
        lambda text: re.search(r"initialize `phase_cursor` to the first incomplete phase \(null when there are no plan phases; the events then carry the literal `N/A` as `phase_id`\)", text) is not None
        and re.search(r"`details\.phase_id` set to the `phase_cursor` value \(the literal `N/A` when it is null\)", text) is not None,
        "the phase_started boundary and the result events must use the same phase_id value for a no-plan BUILD",
    ),
    # --- P4A remediation 3, commit 3: wording that must agree with the finalize rule ---
    A(
        "triage-workflow: the advisory graph has no phases but its phase_cursor is set to memory-finalize at finalize, not absent",
        ROUTER_REFS / "triage-workflow.md",
        lambda text: re.search(r"Single-pass advisory workflow \(no phases; `phase_cursor` stays null until finalize sets it to `memory-finalize`\)", text) is not None
        and "(no `phase_cursor`, no phases)" not in text,
        "SKILL.md sets phase_cursor to memory-finalize at finalize and the checker requires it on a terminal advisory artifact",
    ),
    A(
        "codebase-health-workflow: the advisory graph has no phases but its phase_cursor is set to memory-finalize at finalize, not absent",
        ROUTER_REFS / "codebase-health-workflow.md",
        lambda text: re.search(r"Single-pass advisory workflow \(no phases; `phase_cursor` stays null until finalize sets it to `memory-finalize`\)", text) is not None
        and "(no `phase_cursor`, no phases)" not in text,
        "same rule as the triage reference",
    ),
    # --- P4.T4.1 commit 1: agent-common reconciled with the agent bodies and the router (A1, A6, A7) ---
    A(
        "agent-common: Memory First mkdir is for writers; the router creates the directories (qa-researcher row)",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "the router creates `.cc10x/` and `.cc10x/qa/<workflow>/` for you" in text
        and "unless your agent doc is read-only" in text,
        "the preamble no longer tells a read-only agent to mkdir; the router owns directory creation",
    ),
    A(
        "agent-common: qa-researcher is on the narrower-protocol list",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "`qa-researcher` creates no files and runs no `mkdir`" in text
        and "Narrower agent protocols win" in text,
        "the qa-researcher mkdir prohibition survives the shared preamble",
    ),
    A(
        "qa-researcher: the mkdir and file-creation prohibition stays",
        AGENTS / "qa-researcher.md",
        contains_all("**You may not**, by any tool or command: create, edit, move, or delete files; `mkdir`;"),
        "agent-common narrowing does not loosen the QA read-only prohibition",
    ),
    A(
        "agent-common: Shell Safety is a rule over the agent's own doc, not a name list, and keeps the redirection ban",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "Bash is for what your own agent doc names" in text
        and "test runners, builds, the harness runner, scripts, docker, `mkdir` or `open`" in text
        and "read-only agents included, but a read-only agent never writes file content" in text
        and "No agent writes file content through shell redirection or heredoc" in text
        and "component-builder, bug-investigator, qa-harness-builder, qa-executor" not in text
        and "Read-only agents use Bash for inspection only" not in text
        and "Bash is for read-only commands (git diff, grep, file existence) only" not in text,
        "three read-only agents run tests, builds and scripts their docs name; the old inspection-only line contradicted them; the redirection ban stays",
    ),
    A(
        "agent-common: memory-file ban names the three files, the DEBUG carve-out, and the QA and router paths",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "`.cc10x/activeContext.md`, `.cc10x/patterns.md`, `.cc10x/progress.md`" in text
        and "Sole carve-out:" in text
        and "under `.cc10x/qa/`" in text
        and "`.cc10x/workflows/*` is router-owned" in text
        and "Do NOT edit `.cc10x/*.md` files directly" not in text,
        "the ban names the memory files; other .cc10x paths are written only where the agent doc says so",
    ),
    A(
        "agent-common: glossary section says every agent but plan-gap-reviewer loads it",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "`agent-common` is loaded by every agent except `plan-gap-reviewer`" in text
        and "loaded by read-only agents" not in text
        and "Do NOT write or edit `CONTEXT.md`" in text,
        "the stale read-only-agents claim is gone; the no-write rule stays",
    ),
    A(
        "agent-common: SKILL_HINTS states preloads versus hints and the planner's own gate skill",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "Frontmatter `skills:` preloads are your role-core skills" in text
        and "the router is the only authority that adds situational skills" in text
        and "the planner may invoke `cc10x:plan-review-gate` itself" in text
        and "Do not self-activate internal cc10x skills not passed in SKILL_HINTS" in text,
        "the self-activation rule is stated per C4.3 with the one agent-owned invocation named",
    ),
    A(
        "agent-common: Memory Notes block versus YAML key",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "Read-only agents emit this block" in text
        and "write agents carry `MEMORY_NOTES` in their YAML Router Contract" in text
        and "where it prescribes both, keep them identical" in text,
        "the router extracts the block from read-only agents and the YAML key from write agents",
    ),
    A(
        "agent-common: no agent holds TaskUpdate, the router completes every task",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "No agent holds the `TaskUpdate` tool or owns task completion: the router completes every task after it validates your contract" in text
        and "An agent without the `TaskUpdate` tool never calls it" not in text,
        "the conditional wording suggested some agent still owns completion; none does (a frontmatter pin keeps TaskUpdate out of every tools line)",
    ),
    A(
        "agent-common: the YAML STATUS decides, envelope is the fast path",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "`STATUS` in the fenced YAML block decides" in text
        and "fast-path signal" in text
        and "Router reads envelope first" not in text
        and "primary machine-readable signal" not in text,
        "agent-common matches the router's YAML-first contract rule",
    ),
    *[
        A(
            f"{name}: Memory First body carries no mkdir (agent-common owns it, router creates the directory)",
            AGENTS / f"{name}.md",
            lambda text: "mkdir -p .cc10x" not in text and "Read(file_path=\".cc10x/" in text,
            "the duplicate mkdir is gone; the reads stay",
        )
        for name in ("architecture-scanner", "code-reviewer", "failure-hunter", "triage-agent", "doc-syncer")
    ],
    *[
        A(
            f"{name}: SKILL_HINTS paragraph is single-sourced in agent-common",
            AGENTS / f"{name}.md",
            lambda text: "invoke each skill via" not in text
            and "agent-common's SKILL_HINTS section" in text
            and "Do not self-activate internal cc10x skills not passed in SKILL_HINTS" in text,
            "the reviewers point at the shared SKILL_HINTS procedure and keep the canonical sentence",
        )
        for name in ("code-reviewer", "failure-hunter")
    ],
    # --- P4.T4.1 commit 2: the C4.3 preload table, one pin per agent (A6, RD-6) ---
    *[
        A(
            f"{agent}: frontmatter skills are exactly the C4.3 role-core set",
            AGENTS / f"{agent}.md",
            frontmatter_skills_are(*(f"cc10x:{skill}" for skill in skills)),
            "agent-common everywhere but plan-gap-reviewer; role-core skills only; situational skills arrive through SKILL_HINTS",
        )
        for agent, skills in PRELOAD_TABLE.items()
    ],
    A(
        "preload table covers every agent file",
        AGENTS / "planner.md",
        lambda text: sorted(path.stem for path in AGENTS.glob("*.md")) == sorted(PRELOAD_TABLE),
        "a new agent file must be added to the preload table in the same change",
    ),
    # --- P4.T4.1 commit 3: contract direction, one Test Process Discipline, git_base_sha source (A1, A6, A7) ---
    *[
        A(
            f"{name}: the YAML STATUS decides; envelope is the fast path, not the primary signal",
            AGENTS / f"{name}.md",
            lambda text: "`STATUS` in the fenced YAML block decides" in text
            and "primary machine-readable signal" not in text
            and "Router reads envelope first" not in text,
            "the agent's contract-direction sentences match the router's YAML-first rule",
        )
        for name in (
            "architecture-scanner",
            "code-reviewer",
            "failure-hunter",
            "integration-verifier",
            "plan-gap-reviewer",
            "triage-agent",
        )
    ],
    A(
        "agent-common: one canonical Test Process Discipline with the strictest semantics",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "## Test Process Discipline" in text
        and "`npx vitest run` (NOT `npx vitest`)" in text
        and "watch mode never exits" in text
        and "`timeout 60s npx vitest run`" in text
        and 'pgrep -f "vitest|jest" || echo "Clean"' in text
        and "Kill if found: `pkill -f \"vitest\" 2>/dev/null || true`" in text
        and "trust CLI over IDE/LSP errors" in text,
        "the strictest of the three former copies is the single canonical one",
    ),
    *[
        A(
            f"{name}: Test Process Discipline points at agent-common instead of carrying a copy",
            AGENTS / f"{name}.md",
            lambda text: "agent-common's Test Process Discipline" in text and "Always use run mode" not in text,
            "the agent keeps only its role-specific lines (escape hatch, leaked containers)",
        )
        for name in ("component-builder", "integration-verifier", "qa-harness-builder")
    ],
    A(
        "integration-verifier: environment escape hatch stays",
        AGENTS / "integration-verifier.md",
        contains_all("**Environment escape hatch:**", "Mark scenarios BLOCKED, not FAIL"),
        "role-specific verifier rule survives the dedupe",
    ),
    A(
        "qa-harness-builder: leaked-containers rule stays",
        AGENTS / "qa-harness-builder.md",
        contains("**Leaked containers:**"),
        "role-specific harness rule survives the dedupe",
    ),
    *[
        A(
            f"{name}: git_base_sha is read from the workflow artifact named in the Task Context",
            AGENTS / f"{name}.md",
            contains("from the Workflow Artifact named in your Task Context"),
            "an agent that uses results.git_base_sha is told where to read it",
        )
        for name in ("code-reviewer", "failure-hunter", "doc-syncer")
    ],
    # --- P4.T4.2: builder REM-FIX producer fields, verifier adjudication, BASE tamper check, E2, any non-zero RED (A5, E2) ---
    A(
        "component-builder: YAML contract carries the six REM-FIX producer fields",
        AGENTS / "component-builder.md",
        yaml_has_keys("COVERING_TESTS", "TEST_COMMAND", "TEST_OUTPUT", "FINDING_DISPUTED", "VERIFY_COMMAND", "VERIFY_OUTPUT"),
        "the router's re-review gate and dispute path name the remediating builder as the producer, so its contract must declare the fields",
    ),
    A(
        "component-builder: kind:remfix proof is the covering tests only and fails closed without all three",
        AGENTS / "component-builder.md",
        contains_all(
            "## REM-FIX Tasks (`kind:remfix`)",
            "only the files that would fail if the fix were wrong",
            "fails closed without all three",
        ),
        "the builder is told which tests count and that the router sends an incomplete REM-FIX back",
    ),
    A(
        "component-builder: a dispute needs a proving command",
        AGENTS / "component-builder.md",
        contains_all(
            "is valid only when `VERIFY_COMMAND` is a reproducible command whose output proves the finding false",
            "is not a dispute",
        ),
        "prose disagreement is never grounds to dispute (evidence-gated, not an escape hatch)",
    ),
    A(
        "component-builder: the builder never adjudicates its own dispute",
        AGENTS / "component-builder.md",
        contains_all(
            "You never adjudicate your own dispute",
            "`DISPUTE_UPHELD` or `DISPUTE_REJECTED`",
        ),
        "integration-verifier is the only adjudicator; a rejected dispute means the finding is applied",
    ),
    A(
        "integration-verifier: adjudicates disputed findings and is the only adjudicator",
        AGENTS / "integration-verifier.md",
        contains_all(
            "## Disputed Findings (adjudication)",
            "you are the only adjudicator",
            "must never pass on the builder's claim alone",
            "Re-run `VERIFY_COMMAND` yourself",
        ),
        "a builder-disputed CRITICAL or HIGH finding is re-proven by the verifier, never accepted on the builder's word",
    ),
    A(
        "integration-verifier: DISPUTE_UPHELD only on the verifier's own proof, otherwise REJECTED and the finding stands",
        AGENTS / "integration-verifier.md",
        contains_all(
            "Rule `DISPUTE_UPHELD` only when your own output proves the finding false",
            "Rule `DISPUTE_REJECTED` when the output does not prove it false",
            "never `DISPUTE_UPHELD`",
        ),
        "the verifier fails closed: unproven, unreproducible or unrunnable disputes never remove a finding",
    ),
    A(
        "integration-verifier: YAML contract carries DISPUTE_UPHELD and DISPUTE_REJECTED",
        AGENTS / "integration-verifier.md",
        yaml_has_keys("DISPUTE_UPHELD", "DISPUTE_REJECTED"),
        "the router names integration-verifier as the producer of both fields",
    ),
    A(
        "integration-verifier: tamper check compares against the recorded BASE, not HEAD alone",
        AGENTS / "integration-verifier.md",
        lambda text: all(
            n in text
            for n in (
                "git diff $BASE -- '*.test.*'",
                "`results.git_base_sha`",
                "from the Workflow Artifact named in your Task Context",
                "that key only",
            )
        )
        and "git diff HEAD -- '*.test.*'" not in text,
        "a phase makes several commits, so a HEAD-only diff misses committed test tampering; the BASE is read from the artifact, that key only",
    ),
    A(
        "integration-verifier: tamper check falls back to HEAD only when no BASE is recorded, and says so",
        AGENTS / "integration-verifier.md",
        contains_all("`unavailable`", "fall back to `git diff HEAD` and say so"),
        "the router records git_base_sha=unavailable when git preflight degrades; the fallback is stated, not silent",
    ),
    A(
        "builder and investigator: no-runner exception never fabricates TDD exits (E2, one rule)",
        AGENTS / "component-builder.md",
        lambda text: "Never fabricate `TDD_RED_EXIT` or `TDD_GREEN_EXIT`" in text
        and "require a runner or block" in text
        and "`PROOF_STATUS: human_needed`" in text
        and "`CHECKPOINT_TYPE: human_verify`" in text
        and "TDD evidence may use manual browser verification" not in text,
        "the manual-browser exception no longer sets TDD_RED_EXIT=1 and TDD_GREEN_EXIT=0 from a manual check; it blocks to a human_verify checkpoint",
    ),
    A(
        "bug-investigator: no-runner exception never fabricates TDD exits (E2, one rule)",
        AGENTS / "bug-investigator.md",
        lambda text: "Never fabricate `TDD_RED_EXIT` or `TDD_GREEN_EXIT`" in text
        and "require a runner or block" in text
        and "`NO_LOOP_BLOCKED.ask`" in text
        and "Set `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0` with manual check evidence" not in text,
        "the investigator blocks with NO_LOOP_BLOCKED instead of reporting FIXED on a manual check",
    ),
    *[
        A(
            f"{name}: PASS needs a non-zero TDD_RED_EXIT, 1 is only the convention",
            AGENTS / f"{name}.md",
            lambda text: "non-zero `TDD_RED_EXIT` (conventionally `TDD_RED_EXIT=1`)" in text
            and "the replay gate checks" not in text,
            "any non-zero behavioral RED qualifies; the contract no longer demands the literal 1",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "policy: contract overrides accept any non-zero TDD_RED_EXIT",
        POLICY_REF,
        lambda text: text.count("a non-zero `TDD_RED_EXIT` (1 by convention)") == 2
        and "requires `TDD_RED_EXIT=1`" not in text
        and "`TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`" not in text,
        "the router table agrees with the agents and the replay check: builder and investigator rows both say non-zero",
    ),
    # --- P4.T4.3: review agents, one smell count, one vocabulary, one zero-finding semantics, disputes (A5, E1; C4.2 floor unchanged) ---
    A(
        "code-reviewer: the smell count lives in the code-review skill catalog only",
        AGENTS / "code-reviewer.md",
        lambda text: "the `code-review` skill's Fowler smell catalog" in text
        and "do not restate a count here" in text
        and re.search(r"\b\d+ named smells", text) is None,
        "the agent said 12 while the skill said 16; the count is stated once, in the skill (a pin there keeps it equal to the table rows)",
    ),
    A(
        "code-reviewer: one severity and verdict vocabulary",
        AGENTS / "code-reviewer.md",
        lambda text: "Severities are `CRITICAL`, `HIGH`, `MEDIUM` and `LOW`, as the `code-review` skill defines them" in text
        and "verdicts are `APPROVE` and `CHANGES_REQUESTED`" in text
        and "no CRITICAL, MAJOR, or MEDIUM" not in text
        and "HIGH/MEDIUM/MINOR issues" not in text
        and "[MEDIUM/MINOR issues" not in text,
        "MAJOR and MINOR map to the skill's HIGH and LOW; CLEAN is the hunter's word, not the reviewer's",
    ),
    A(
        "code-reviewer: zero-finding gate asks for the router's three citations",
        AGENTS / "code-reviewer.md",
        lambda text: "name at least three specific positive assertions with file:line evidence" in text
        and "fewer than 3 file:line evidence citations" in text
        and "name at least one specific positive assertion" not in text
        and "set CONFIDENCE to exactly 70" in text,
        "the agent asked for 1 citation, the router bounces a zero-finding APPROVE with fewer than 3: the agent now meets the router's check",
    ),
    A(
        "code-reviewer: the 80 floor stays per-finding and the zero-finding approval is the stated exception",
        AGENTS / "code-reviewer.md",
        lambda text: "the per-finding `>=80` reporting floor is unchanged" in text
        and "The one exception is the Zero-Finding Gate approval, which sits at exactly 70 by design" in text,
        "C4.2: the floor is unchanged; the APPROVE-at-80 sentence and the zero-finding 70 no longer contradict",
    ),
    A(
        "code-reviewer: a disputed finding is ruled on by the verifier, never the reviewer",
        AGENTS / "code-reviewer.md",
        lambda text: "`integration-verifier` rules on a finding the builder disputed (`FINDING_DISPUTED`), never you" in text
        and "do not drop a finding because it was disputed" in text,
        "the router: a dispute is adjudicated by the independent verifier, never by the reviewer who raised it",
    ),
    A(
        "failure-hunter: same severity vocabulary, its own verdict words",
        AGENTS / "failure-hunter.md",
        lambda text: "Severities are `CRITICAL`, `HIGH`, `MEDIUM` and `LOW`, as the `code-review` skill defines them" in text
        and "your verdicts are `CLEAN` and `ISSUES_FOUND`, never `APPROVE` or `CHANGES_REQUESTED`" in text,
        "the hunter and the reviewer share one severity set and do not borrow each other's verdict words",
    ),
    A(
        "failure-hunter: a CLEAN with an empty scan scope triggers the router's fallback",
        AGENTS / "failure-hunter.md",
        lambda text: "makes the router run fallback inline verification" in text
        and "zero error-handling sites inspected or zero files scanned" in text,
        "the zero-results path no longer reads as a guaranteed CLEAN: the router's policy row bounces an empty scope",
    ),
    A(
        "failure-hunter: a disputed finding is ruled on by the verifier, never the hunter",
        AGENTS / "failure-hunter.md",
        lambda text: "`integration-verifier` rules on a finding the builder disputed (`FINDING_DISPUTED`), never you" in text
        and "do not drop a finding because it was disputed" in text,
        "the router: a dispute is adjudicated by the independent verifier, never by the hunter who raised it",
    ),

    # --- P4.T4.4: planner, gap reviewer, doc-syncer, triage, scanner (A5, B12, A7) ---
    A(
        "planner: the qa-re-plan amendment-lane fields are in its YAML contract and rules",
        AGENTS / "planner.md",
        lambda text: yaml_has_keys("AMENDED_FILES", "STALE_SWEEP", "RECONCILIATION_RERUN")(text)
        and "On a `phase:qa-re-plan` dispatch, `AMENDED_FILES`, `STALE_SWEEP` and `RECONCILIATION_RERUN` are required and non-empty" in text
        and "all three plan artifacts are in scope" in text,
        "the router's pass-2 gate fails closed without all three; the planner is their producer (A5, addenda item 2)",
    ),
    A(
        "planner: QA routes write only under .cc10x/qa/, never docs/plans",
        AGENTS / "planner.md",
        lambda text: "On `phase:qa-plan` the only write targets are `.cc10x/qa/{workflow_uuid}/test-plan.md` and `.cc10x/qa/{workflow_uuid}/env-plan.md`" in text
        and "`phase:qa-re-plan` may also amend `.cc10x/qa/{workflow_uuid}/feature-map.md`" in text
        and "Do NOT write under `docs/plans/` on a QA route" in text
        and "create no file outside `.cc10x/`" in text,
        "the docs/plans-only write rule contradicted the QA dispatch and the QA isolation guard (A5)",
    ),
    A(
        "planner: writes what plan-review-gate checks",
        AGENTS / "planner.md",
        lambda text: "`## Durable Decisions` section" in text
        and "`Depends on:` and `Enables:`" in text
        and "`## Differences from agreement` section" in text
        and "plan-review-gate" in text,
        "the gate fails a multi-phase plan without Durable Decisions, enables statements or Differences from agreement (B12)",
    ),
    A(
        "plan-gap-reviewer: states it emits a YAML block, anchored by position",
        AGENTS / "plan-gap-reviewer.md",
        lambda text: "no YAML Router Contract block" not in text
        and "this agent emits a fenced YAML block" in text
        and "`PLANNING_REVIEW_STATUS`" in text
        and "never a per-agent key on the line-1 `CONTRACT` envelope" in text
        and "the first fenced `yaml` block after the line-1 envelope and the line-2 heading" in text,
        "the body said it had no YAML block while its Output section emits one; REVIEW_MODE stays a dispatch input (A5)",
    ),
    A(
        "doc-syncer: legacy ADR cleanup is propose-only, deletes are user-run",
        AGENTS / "doc-syncer.md",
        lambda text: "Never delete a file: you have no delete tool and Bash is not for `rm`" in text
        and "USER_RUN: remove legacy ADR" in text
        and "delete old" not in text
        and "delete the legacy duplicate" not in text,
        "the migrate-and-delete steps had no tool that could perform the delete; the cleanup is now a reported proposal (A7)",
    ),
    A(
        "triage-agent: no source-code writes, and no read-only claim",
        AGENTS / "triage-agent.md",
        lambda text: "No source-code writes" in text
        and "Read-only." not in text
        and "READ-ONLY for source code" not in text
        and "do not switch branches or modify the working tree" in text
        and "`.scratch/` and `.out-of-scope/`" in text,
        "the agent writes briefs and rejection records, so 'read-only' was false (A7)",
    ),
    A(
        "triage-agent: BLOCKING is derived, not hard-coded",
        AGENTS / "triage-agent.md",
        lambda text: "BLOCKING: false\n" not in text
        and "BLOCKING: [true when the run stops for human input" in text
        and "`b` mirrors `BLOCKING`" in text
        and "b=true` only if wontfix is contested" not in text,
        "BLOCKING true for NEEDS_INFO, WONTFIX or NEEDS_GRILLING=true, else false (A7)",
    ),
    A(
        "architecture-scanner: temp-dir-only Write is a prompt rule, not enforced",
        AGENTS / "architecture-scanner.md",
        lambda text: "temp-directory-only Write is a prompt rule: no hook or tool restriction enforces it" in text,
        "F3 (path guard) stays deferred; the agent file now says plainly that the boundary is prose",
    ),
    # --- P4.T4.5a: qa-executor report rule satisfiable with Write only (A5, A7) ---
    A(
        "qa-executor: the report is rewritten whole with Write (no Edit tool)",
        AGENTS / "qa-executor.md",
        lambda text: "Read that file, then rewrite the whole file with `Write`" in text
        and "you have no `Edit` tool" in text
        and "fill it in\nplace" not in text
        and "tools: Read, Write, Bash, Grep, Glob, Skill, WebFetch" in text,
        "the body said to fill report.md in place but the agent has no Edit; the router seeds, the executor rewrites it whole (A5)",
    ),
    A(
        "qa-strategy: report.md row matches the executor's Write-only rewrite",
        SKILLS / "qa-strategy" / "SKILL.md",
        lambda text: "`qa-executor` rewrites it whole with `Write`" in text and "`qa-executor` fills it in place" not in text,
        "the skill table said the executor fills report.md in place, contradicting the Write-only rule (A5)",
    ),
    # --- P4.T4.5b: the router completes tasks; no agent lists or calls TaskUpdate (A3 part, ASM-A1, C4.1 c) ---
    *[
        A(
            f"{path.stem}: tools line does not list TaskUpdate",
            path,
            frontmatter_tools_exclude("TaskUpdate"),
            "the router completes tasks after contract validation; an agent that holds TaskUpdate can complete its own task before the contract is checked",
        )
        for path in sorted(AGENTS.glob("*.md"))
    ],
    *[
        A(
            f"{name}: task completion is router-owned, no TaskUpdate call instruction",
            AGENTS / f"{name}.md",
            lambda text: "Task completion is handled by the router. Do NOT call TaskUpdate directly." in text
            and "TaskUpdate({" not in text
            and "no tool calls after it" not in text
            and "After outputting Router Contract" not in text
            and "After emitting the Router Contract" not in text,
            "replaces the 'call TaskUpdate before the final response' instruction; also keeps the 71.3 rule that no instruction asks for a tool call after the contract",
        )
        for name in ("component-builder", "bug-investigator", "doc-syncer", "planner", "researcher")
    ],
    # --- P4B-4: REM-FIX report reaches the verifier so a disputed finding can be adjudicated ---
    A(
        "remediation: the re-verify dispatch carries the REM-FIX report by reference",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "Verifier hand-off:",
            "`### REM-FIX report` sub-block",
            "`results.builder`",
            "a reference, not pasted bodies",
            "re-runs `VERIFY_COMMAND` itself",
            "Include the REM-FIX report's proof and dispute fields in the `### REM-FIX report` sub-block of `## Previous Agent Findings`.",
        ),
        "without the report the only adjudicator never sees FINDING_DISPUTED, so a disputed CRITICAL or HIGH finding could never leave the blocking set",
    ),
    A(
        "router: the verifier findings handoff adds the REM-FIX report sub-block on a re-verify",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "add a `### REM-FIX report` sub-block that references the persisted REM-FIX report (`results.builder`, or `results.investigator` when `bug-investigator` executed the REM-FIX)",
            "Re-review precondition gate",
        ),
        "the section 12 handoff is the single source of the verifier's Previous Agent Findings; it must name the REM-FIX report",
    ),
    A(
        "integration-verifier: reads the REM-FIX report sub-block and re-checks primary evidence",
        AGENTS / "integration-verifier.md",
        contains_all(
            "`### REM-FIX report` sub-block",
            "read that key only",
            "`VERIFY_OUTPUT` is a claim to re-check, never evidence you cite",
            "you are not a reviewer",
        ),
        "the verifier is the sanctioned adjudication path; anti-anchoring holds because it re-runs the command and rules on its own output",
    ),
    # --- P4B remediation 1, commit 1: REM-FIX producers for both executors, dispute consumption, dispute-only return, proof format ---
    A(
        "bug-investigator: REM-FIX section and the six gate fields, same wording as the builder",
        AGENTS / "bug-investigator.md",
        lambda text: yaml_has_keys("COVERING_TESTS", "TEST_COMMAND", "TEST_OUTPUT", "FINDING_DISPUTED", "VERIFY_COMMAND", "VERIFY_OUTPUT")(text)
        and contains_all(
            "## REM-FIX Tasks (`kind:remfix`)",
            "dispatches a `kind:remfix` task to you when it is created in a DEBUG workflow, whatever its `origin:`",
            "or when it carries `origin:bug-investigator`",
            "only the files that would fail if the fix were wrong",
            "fails closed without all three",
            "in the same order in all three lists",
            "is valid only when `VERIFY_COMMAND` is a reproducible command whose output proves the finding false",
            "You never adjudicate your own dispute",
        )(text),
        "the router dispatches kind:remfix origin:bug-investigator to the investigator, so it must declare the gate fields the router's re-review gate and dispute path read",
    ),
    *[
        A(
            f"{name}: dispute-only return is defined, no fabricated RED, a mixed report keeps full proof",
            AGENTS / f"{name}.md",
            contains_all(
                "**Dispute-only return.**",
                "When EVERY finding in the task is disputed",
                "there is no RED to observe and none to invent",
                "Never fabricate a RED to fill the gap",
                "A report where even one finding was applied is not dispute-only",
                "`TEST_COMMAND: null`",
            ),
            "an all-disputed REM-FIX changes no code, so the builder-PASS requirement of a RED would force fabricated TDD evidence; the return is defined instead",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "component-builder: dispute-only PASS keeps PHASE_EXIT_READY false until the verifier adjudicates",
        AGENTS / "component-builder.md",
        contains_all("`PHASE_STATUS: partial`, `PHASE_EXIT_READY: false` and `PROOF_STATUS: gaps_found`", "The phase does not exit until the verifier adjudicates, so `PHASE_EXIT_READY` stays false"),
        "the only PASS with PHASE_EXIT_READY false; the router forwards it to the verifier instead of advancing the phase",
    ),
    *[
        A(
            f"{name}: raw proof output is a YAML block scalar or single-line-escaped, never a quoted multi-line scalar",
            AGENTS / f"{name}.md",
            contains_all(
                "write each as a YAML block scalar (`|`)",
                "the last 20 lines with newlines escaped inside one single-line scalar",
                "Never paste multi-line output into a quoted scalar",
            ),
            "raw command output in a quoted YAML scalar breaks the contract on a stray quote or colon; the proof fields use a block scalar",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "remediation: the REM-FIX subject names the executing agent per origin",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "{executing agent: component-builder | bug-investigator}: REM-FIX {short reason}" in text
        and "`bug-investigator` when the REM-FIX is created in a DEBUG workflow or has `origin:bug-investigator`" in text
        and "`origin:` names the agent whose findings triggered the fix, never the executor" in text
        and 'subject: "CC10X component-builder: REM-FIX' not in text
        and "`component-builder`, or `bug-investigator` when the REM-FIX is created in a DEBUG workflow or has `origin:bug-investigator`; both declare them" in text,
        "the template hard-coded component-builder while the dispatch table sends origin bug-investigator to the investigator",
    ),
    A(
        "remediation: dispute consumption, the verifier ruling is binding and nothing else adjudicates",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "Dispute consumption",
            "a re-review or re-hunt that re-raises it creates NO new REM-FIX",
            "`DISPUTE_UPHELD` drops the finding exactly as `validated: false` does",
            "`finding_dropped: dispute upheld`",
            "the stricter-verdict rule of the default loop does not override it",
            "`DISPUTE_REJECTED` keeps the finding in the blocking set and the router creates the REM-FIX for it",
            "listed `DISPUTE_UPHELD` (upheld by validation)",
        ),
        "DISPUTE_UPHELD and DISPUTE_REJECTED had no consumer: a re-raise by the reviewer or hunter beat an upheld dispute and nothing created the REM-FIX for a rejected one",
    ),
    A(
        "remediation: adjudication validity fails closed, an absent verifier leaves the gate closed",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "every position 1..N of `FINDING_DISPUTED` must appear in exactly one of `DISPUTE_UPHELD` or `DISPUTE_REJECTED`",
            "is invalid output: every dispute in it stays unadjudicated",
            "When the verifier is absent, blocked or unavailable, the disputes stay unadjudicated and the gate stays closed",
        ),
        "partial, doubled or out-of-range adjudication, or no verifier at all, must never remove a finding or advance the phase",
    ),
    A(
        "remediation: a dispute-only report satisfies the re-review gate without covering tests",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "the report is dispute-only",
            "the count of `FINDING_DISPUTED` entries equals the count of findings in the task",
            "A report with any applied finding keeps the full proof requirement",
        ),
        "the gate required non-empty COVERING_TESTS even when every finding was disputed and no code changed",
    ),
    A(
        "router: step 6 contradictory-verdict rule excepts an upheld dispute",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "(FAIL over PASS, CHANGES_REQUESTED over APPROVE), except that a re-raised finding whose dispute the verifier upheld is dropped per the Re-review precondition gate",
        ),
        "without the exception the stricter verdict beats an UPHELD dispute",
    ),
    A(
        "integration-verifier: every disputed position is adjudicated exactly once, by index",
        AGENTS / "integration-verifier.md",
        contains_all(
            "1-based position of its entry in `FINDING_DISPUTED`",
            "an index, not the restated text",
            "must appear in exactly one of `DISPUTE_UPHELD` or `DISPUTE_REJECTED`: none omitted, none in both, none out of range",
            "invalid output and the router treats every dispute in it as unadjudicated",
            "A disputed finding you also mark `validated: false` is upheld by validation: list it in `DISPUTE_UPHELD`",
            "list the entry in `DISPUTE_REJECTED` (unverifiable, the finding stands)",
        ),
        "write-only rulings: with no identity rule and no exactly-once rule a dispute could be in neither list, both, or restated so the router cannot match it",
    ),
    A(
        "integration-verifier: re-runs VERIFY_COMMAND only when read-only and bounded, and checks the tree afterwards",
        AGENTS / "integration-verifier.md",
        contains_all(
            "Run it only when it is read-only and bounded",
            "compare `git status --short` before and after",
            "rule it `DISPUTE_REJECTED` as unverifiable and never run it a second time",
            "Refuse, without running it, any command that uses the network, writes or redirects output to a file, installs packages, runs a mutating git verb, or chains shell steps beyond a single pipeline of read-only tools",
            "say which of these it breaks",
            "If the status changed, report exactly what changed in the verdict text",
        ),
        "the verifier is read-only; re-running another agent's command verbatim could mutate the tree (prompt-level guard only: nothing but this text stops a run)",
    ),
    A(
        "integration-verifier: a dispute-only report is expected to carry null TDD exits",
        AGENTS / "integration-verifier.md",
        contains_all("A dispute-only report (every finding disputed, no code changed) arrives with null `TDD_*` exits and empty proof fields by design"),
        "the verifier does not read the missing RED of a dispute-only return as a defect of its own",
    ),
    *[
        A(
            f"{name}: the router applies the verifier's ruling to a re-raised disputed finding",
            AGENTS / f"{name}.md",
            contains("the router applies the verifier's ruling to a re-raised disputed finding, so your report never decides the dispute"),
            "the agent keeps reporting the finding; the verifier's ruling, applied by the router, decides it",
        )
        for name in ("code-reviewer", "failure-hunter")
    ],
    A(
        "policy: builder and investigator rows define the dispute-only return",
        POLICY_REF,
        lambda text: "**`kind:remfix` proof:**" in text
        and "the **dispute-only return**: every dispatched finding is in `FINDING_DISPUTED` (equal count, the entries distinct and each mapping to one finding in the task)" in text
        and "the only `PASS` accepted with `PHASE_EXIT_READY=false`" in text
        and "`PHASE_STATUS=partial`, `PROOF_STATUS=gaps_found`" in text
        and "A fabricated RED or GREEN on a dispute-only return is invalid output" in text
        and "**`kind:remfix`:** `STATUS=FIXED` also requires" in text
        and "A fabricated RED or GREEN there is invalid output" in text,
        "the override rows required a RED for every PASS and every FIXED, which an all-disputed REM-FIX cannot honestly satisfy",
    ),
    A(
        "policy: integration-verifier row requires every dispute adjudicated exactly once and fails closed",
        POLICY_REF,
        contains_all(
            "every 1-based position of that list must appear in exactly one of `DISPUTE_UPHELD` or `DISPUTE_REJECTED`",
            "makes the whole return invalid output and every dispute in it stays unadjudicated (fail closed)",
            "upheld by validation and is listed in `DISPUTE_UPHELD`",
            "A verifier that is absent, blocked or unavailable leaves the disputes unadjudicated and the gate closed",
        ),
        "the router-side validity rule for the verifier's adjudication lists",
    ),
    # --- P4B remediation 1, commit 2: researcher Skill, docs-only TDD path, DEBUG BASE, mkdir form, Shell Safety ---
    A(
        "researcher: Skill is a tool (the mcp-cli SKILL_HINT needs it) and the MCP lanes stay",
        AGENTS / "researcher.md",
        frontmatter_tools_include("Skill", "mcp__brightdata", "mcp__octocode", "WebSearch", "WebFetch"),
        "the router may add cc10x:mcp-cli as a SKILL_HINT for the researcher and agent-common says hints are invoked via Skill; without the tool the hint is dead",
    ),
    *[
        A(
            f"{name}: documentation, prompt and config-only work has a scripted RED",
            AGENTS / f"{name}.md",
            contains_all(
                "**Documentation, prompt and config-only phases:**",
                "a validator, grep or replay check with a real exit code",
                "failing before the edit and passing after",
                "`behavioral` when it asserts content",
            ),
            "the manual-browser rule left a Markdown-only phase with no stated way to produce a RED; the scripted check is named",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "policy: documentation, prompt and config-only phases state the scripted RED in both write-agent rows",
        POLICY_REF,
        contains_all(
            "**Documentation, prompt and config-only phases** have the same RED/GREEN requirement",
            "RED is that check failing before the edit and passing after",
            "`behavioral` when it asserts content, `error` when it only failed to run",
            "For a bug in a documentation, prompt or config file the loop is a validator, grep or replay check with a real exit code",
        ),
        "the router table agrees with the agents: a docs/prompt/config phase is not exempt from RED/GREEN",
    ),
    A(
        "failure-hunter: a site in a prompt or doc diff is a gate, contract, field or fail-closed clause, and zero sites still bounces",
        AGENTS / "failure-hunter.md",
        contains_all(
            "**Sites in a prompt, doc or config diff:**",
            "a gate, a contract, a field or a fail-closed clause",
            "A Markdown-only diff has sites to inspect",
            "Zero sites and zero files scanned stays a bounce (step 9)",
            "sites as defined in step 1: gates, contracts, fields and fail-closed clauses",
            "makes the router run fallback inline verification",
        ),
        "'Nothing found is a valid result' conflicted with the router's bounce of a CLEAN that states zero sites on a Markdown-only diff; the diff now has sites",
    ),
    A(
        "debug-workflow: the DEBUG preparation records results.git_base_sha before the first investigator",
        ROUTER_REFS / "debug-workflow.md",
        contains_all(
            "**Record the BASE sha (runs once, at the start of the investigation phase, before the first investigator is dispatched).**",
            "`results.git_base_sha`",
            "the same producer rule as BUILD step 11a",
            "does not re-record it",
            "`git_base_sha=unavailable`",
        ),
        "the BASE tamper clauses in the verifier and reviewer had no DEBUG producer, so DEBUG always fell back to git diff HEAD",
    ),
    A(
        "agent-common: Memory First mkdir keeps the trailing slash the QA isolation guard allows, and is a no-op safety net",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: 'Bash(command="mkdir -p .cc10x/")' in text
        and 'Bash(command="mkdir -p .cc10x")' not in text
        and "so the step is a no-op safety net" in text
        and "Keep the trailing slash" in text
        and "denies the bare form `mkdir -p .cc10x` in QA plan phases" in text,
        "the guard's allowlist is the prefix `.cc10x/`, so the bare form was denied for the planner in QA plan phases (a behavioral guard test pins both forms)",
    ),
    # --- P4B remediation 2, commit 1: the bare mkdir form is prescribed nowhere ---
    A(
        "no prompt file prescribes the bare `mkdir -p .cc10x` form (the QA isolation guard denies it in QA plan phases)",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda _text: not [
            path
            for path in [*AGENTS.glob("*.md"), *SKILLS.rglob("*.md")]
            if path != SKILLS / "agent-common" / "SKILL.md" and re.search(r"mkdir -p \.cc10x(?![/\w.-])", read(path))
        ],
        "the guard's allowlist is the prefix `.cc10x/`; a prescribed bare form is denied for every caller in a QA plan phase (agent-common is the one file that may mention the bare form, and only to say it is denied)",
    ),
    A(
        "router memory load and memory-operations use the trailing-slash mkdir",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: 'Bash("mkdir -p .cc10x/")' in text
        and (SKILLS / "memory-and-handoff" / "references" / "memory-operations.md").read_text(encoding="utf-8").count("mkdir -p .cc10x/\n") == 1,
        "the memory load is the first step of every workflow and runs before any QA plan phase guard",
    ),
    # --- P4B remediation 2, commit 2: dispute-only phase transition, re-raise matching, persisted set, named stall exit, executor rule ---
    A(
        "router: step 6 stop rule excepts a valid dispute-only REM-FIX return, which proceeds to the Re-Review loop",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains_all(
            "persist `phase_status={partial|blocked}` and stop, except that a valid dispute-only REM-FIX return persists `partial` and proceeds to the Re-Review loop",
            "and one whose dispute is still in flight continues to the verifier under the same gate",
        ),
        "step 6 stopped on every non-complete phase, so a dispute-only phase stayed partial forever; and a blocking re-raise of an in-flight dispute stopped the chain before the verifier",
    ),
    A(
        "build-workflow: the BUILD stop rule excepts the dispute-only return, and finishing waits for the verifier's adjudication",
        ROUTER_REFS / "build-workflow.md",
        contains_all(
            "the one exception is a valid dispute-only REM-FIX return, which records `partial` and proceeds to the Re-Review loop",
            "A phase left `partial` by a dispute-only REM-FIX is green only after the verifier's adjudication has set it `completed`.",
        ),
        "the BUILD graph rule said stop on incomplete phase evidence with no exception",
    ),
    A(
        "remediation: dispute-only phase transition names what phase_exit_gate reads",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "Dispute-only phase transition.",
            "When the verifier adjudicates EVERY dispute validly (by index) and returns `PASS`, the router sets `phase_status=completed` and runs `phase_exit_gate` on exactly two things",
            "the verifier return, and the phase's earlier builder evidence",
            "The gate never reads the dispute-only report's `PHASE_EXIT_READY=false`",
            "If the verifier rejects any dispute, the phase stays `partial`",
        ),
        "without a named transition and named gate inputs the gate reads the dispute-only report (PHASE_EXIT_READY=false) and the phase never completes",
    ),
    A(
        "remediation: a re-raise of an in-flight dispute is matched by identity, creates no REM-FIX and continues to the verifier",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "Re-raise matching.",
            "the same file and the same summary as the disputed finding",
            "When the router cannot match confidently it treats the finding as new",
            "A matched re-raise creates no REM-FIX and the chain CONTINUES to the verifier",
            "does not stop the chain before the verifier",
        ),
        "the reviewer's blocking verdict on a re-raised disputed finding stopped the chain before the only adjudicator ran",
    ),
    A(
        "remediation: the in-flight dispute set is persisted in results.disputes_in_flight (policy and skeleton agree)",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        lambda text: "Persisted dispute set." in text
        and "`results.disputes_in_flight` entry per disputed position: `{cycle_number, position, finding, ruling}`" in text
        and "`ruling` null until the verifier adjudicates" in text
        and "`results.disputes_in_flight` is the router-written list of disputed REM-FIX findings" in POLICY_REF.read_text(encoding="utf-8")
        and "disputes_in_flight" in (ROUTER_REFS / "workflow-artifact.skeleton.json").read_text(encoding="utf-8"),
        "the dispute set lived only in conversation, so it did not survive compaction or resume",
    ),
    A(
        "skeleton: results.disputes_in_flight ships as an empty list",
        ROUTER_REFS / "workflow-artifact.skeleton.json",
        lambda text: json.loads(text).get("results", {}).get("disputes_in_flight", "missing") == [],
        "the key the router writes and the policy names must exist in the skeleton, empty",
    ),
    A(
        "remediation: the unadjudicated-dispute stall has a named exit (one changed re-dispatch, then BLOCKED and ask; inline mode asks)",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "Unadjudicated-dispute exit.",
            "re-dispatches the verifier ONCE with a changed input",
            "an explicit `### Disputed findings` list",
            "the router stops with `BLOCKED`",
            "it creates no REM-FIX and advances no phase",
            "In inline mode (no Agent primitive) the router states that it cannot adjudicate its own builder's disputes and asks the user",
        ),
        "an invalid or absent verifier return left the chain stalled with no owner and no way out",
    ),
    A(
        "remediation: a REM-FIX created from DISPUTE_REJECTED carries the ruling and the verifier's reason",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "{rejected disputes block, only when created from a DISPUTE_REJECTED ruling}",
            "under `Rejected disputes:` after the findings, each rejected finding with the ruling (`DISPUTE_REJECTED`) and the verifier's rejection reason",
            "does not dispute the same `VERIFY_COMMAND` again unless it has new evidence",
            "carrying the ruling and the verifier's rejection reason as the template section above says",
        ),
        "the REM-FIX template carried only the findings, so the executor never saw the ruling and could re-dispute the same command",
    ),
    A(
        "remediation: dispute-only requires distinct FINDING_DISPUTED entries that each map to a task finding",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all("the `FINDING_DISPUTED` entries are distinct, each maps to exactly one finding in the task by its id or restated file and summary, and the count of `FINDING_DISPUTED` entries equals the count of findings in the task"),
        "an equal count alone let two copies of one dispute pass for an all-disputed report",
    ),
    A(
        "router dispatch: a REM-FIX created in a DEBUG workflow executes with bug-investigator, any origin",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("| `kind:remfix` created in a DEBUG workflow (any `origin:`; wins over the origin rows below), or `kind:remfix` + `origin:bug-investigator` | `cc10x:bug-investigator` |"),
        "nothing produced origin:bug-investigator, so the investigator never executed a REM-FIX; origin names who raised the findings, the workflow decides the executor",
    ),
    A(
        "policy: dispute-only FIXED row defines FEEDBACK_LOOP and DEBUG_CLOSEOUT so the investigator invents nothing",
        POLICY_REF,
        contains_all(
            "(the `kind:remfix` dispute-only return below is the one exception)",
            "`FEEDBACK_LOOP.rung=cli_snapshot` with `command` the first `VERIFY_COMMAND`",
            "`DEBUG_CLOSEOUT.instrumentation_removed` and `repro_no_longer_fires` both null (nothing was changed or reproduced)",
        ),
        "the FIXED row required instrumentation_removed=true and a non-none rung, which a no-code-change dispute-only return could only satisfy with invented values",
    ),
    A(
        "policy: the dispute-only row says what phase_exit_gate reads after adjudication",
        POLICY_REF,
        contains_all(
            "the router sets `phase_status=completed` and runs `phase_exit_gate` on the verifier return and the phase's earlier builder evidence, never on the dispute-only report",
        ),
        "the contract row carried the partial state but not the transition out of it",
    ),
    *[
        A(
            f"{name}: a REM-FIX carrying Rejected disputes is applied, the same command is not re-disputed without new evidence, entries name distinct findings",
            AGENTS / f"{name}.md",
            contains_all(
                "A REM-FIX that carries `Rejected disputes:` is that ruling already made",
                "apply those findings, and do not dispute the same `VERIFY_COMMAND` again unless you have new evidence (a different command or new output)",
                "each entry naming a different finding of the task",
            ),
            "the executor must know what to do with a rejected dispute, or it re-disputes the same command in a loop",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "bug-investigator: dispute-only return defines FEEDBACK_LOOP.rung and the DEBUG_CLOSEOUT values, null where nothing happened",
        AGENTS / "bug-investigator.md",
        contains_all(
            "`FEEDBACK_LOOP.rung: cli_snapshot` with `FEEDBACK_LOOP.command` set to the first `VERIFY_COMMAND`",
            "`DEBUG_CLOSEOUT.instrumentation_removed` and `DEBUG_CLOSEOUT.repro_no_longer_fires` both `null` (nothing was changed or reproduced, so there is nothing to confirm)",
            "instrumentation_removed: [true | false | null on a kind:remfix dispute-only return]",
            "(both `null` on a `kind:remfix` dispute-only return, REM-FIX section item 5)",
        ),
        "the dispute-only return left rung and closeout to be invented, which the FIXED requirements could only satisfy with fabricated values",
    ),
    # --- P4B remediation 2, commit 3: verifier command guard, both hand-off keys, rejection reason ---
    A(
        "integration-verifier: the REM-FIX hand-off names both results.builder and results.investigator",
        AGENTS / "integration-verifier.md",
        contains("(`results.builder`, or `results.investigator` when `bug-investigator` executed the REM-FIX); read that key only"),
        "the verifier read only results.builder, so an investigator-executed REM-FIX report was invisible to it",
    ),
    A(
        "integration-verifier: each DISPUTE_REJECTED position carries a stated reason for the router to pass on",
        AGENTS / "integration-verifier.md",
        contains("State the rejection reason for each rejected position in the verdict text; the router passes it to the executor."),
        "the router's REM-FIX from a rejected dispute carries the verifier's reason, so the verifier must produce one",
    ),
    # --- P4B remediation 1, commit 3: stale text and the pins the hunt showed unprotected ---
    A(
        "remediation: the REM-FIX report reaches the verifier from results.investigator when the origin is bug-investigator",
        SKILLS / "cc10x-router" / "references" / "remediation-and-research.md",
        contains_all(
            "It names `results.builder`, or `results.investigator` when `bug-investigator` executed the REM-FIX, of the workflow artifact",
            "where the router persisted the report",
        ),
        "the investigator is an executor of kind:remfix, so its report is persisted under its own key and the hand-off must name it",
    ),
    A(
        "router: artifact-only REM-FIX is dispatched to the origin's executing agent, not always component-builder",
        SKILLS / "cc10x-router" / "SKILL.md",
        contains("dispatched through the Agent tool to the executing agent the dispatch table names (`component-builder`, or `bug-investigator` in a DEBUG workflow or for `origin:bug-investigator`)"),
        "the artifact-only sentence hard-coded component-builder while the dispatch table sends origin bug-investigator to the investigator",
    ),
    A(
        "component-builder: BUILD_PREFLIGHT proof is the contract field, not a hook",
        AGENTS / "component-builder.md",
        lambda text: "A hook greps for" not in text
        and "No hook reads this line and the router sees only your final message" in text
        and "the router rejects a PASS whose value is false" in text,
        "no script greps BUILD_PREFLIGHT: and the router receives only the final message, so the claim of a hook was false; the contract field carries the proof",
    ),
    A(
        "agent-common: the BUILD_PREFLIGHT exception names no hook",
        SKILLS / "agent-common" / "SKILL.md",
        lambda text: "a hook greps for it" not in text
        and "no hook reads it and the router sees only your last message, so the contract field `BUILD_PREFLIGHT_EMITTED` carries the proof" in text,
        "the preamble repeated the unverified hook claim",
    ),
    A(
        "component-builder: a no-runner phase never fabricates exits, a scripted check is evidence, manual is not",
        AGENTS / "component-builder.md",
        contains_all(
            "a scripted check with real exit codes is TDD evidence; manual browser verification is not",
            "Never fabricate `TDD_RED_EXIT` or `TDD_GREEN_EXIT`: leave both `null`",
            "return `STATUS: FAIL`, `PHASE_STATUS: blocked`",
        ),
        "the decisive values of the no-runner rule: leave both null, FAIL and blocked, and a manual check is not evidence",
    ),
    A(
        "bug-investigator: a no-runner phase returns BLOCKED, leaves both exits null, a scripted loop is evidence and a manual check is not",
        AGENTS / "bug-investigator.md",
        contains_all(
            "a scripted loop with real exit codes (the `headless_browser` rung, for example) is TDD evidence; a manual browser check is not",
            "Never fabricate `TDD_RED_EXIT` or `TDD_GREEN_EXIT`: leave both `null`",
            "return `STATUS: BLOCKED`, name the missing runner or the human check in `NO_LOOP_BLOCKED.ask`",
        ),
        "the decisive values of the investigator's no-runner rule: BLOCKED, both null, and a manual check is not evidence",
    ),
    *[
        A(
            f"{name}: REM-FIX dispute lists keep one order, and the PASS rule names the dispute alternative",
            AGENTS / f"{name}.md",
            contains_all(
                "one entry per disputed finding, in the same order in all three lists",
                "`COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT` for every finding you applied, or a dispute per the REM-FIX section",
            ),
            "positions pair a finding with its command and output (and the verifier rules by position), so order drift misattributes a ruling; a REM-FIX PASS needs proof or a dispute",
        )
        for name in ("component-builder", "bug-investigator")
    ],
    A(
        "component-builder: the REM-FIX PASS rule sits in the contract rules and names the dispute alternative",
        AGENTS / "component-builder.md",
        contains("on a `kind:remfix` task, `STATUS=PASS` also requires non-empty `COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT` for every finding you applied, or a dispute per the REM-FIX section"),
        "the PASS gate for a REM-FIX builder is stated where STATUS=PASS is defined",
    ),
    A(
        "integration-verifier: the fail-closed tail of DISPUTE_REJECTED",
        AGENTS / "integration-verifier.md",
        contains(
            "when the command does not reproduce, or when no `VERIFY_COMMAND` was given: the finding stands, set `REMEDIATION_NEEDED: true`, and the verdict cannot be PASS while it is CRITICAL or HIGH"
        ),
        "a non-reproducing or missing command must never remove a CRITICAL or HIGH finding or let the verdict pass",
    ),
    A(
        "planner: every non-qa-re-plan dispatch emits the three amendment-lane fields as []",
        AGENTS / "planner.md",
        contains("On every other dispatch emit all three as `[]`."),
        "the router fails closed on qa-re-plan without the fields; elsewhere the fields are present and empty rather than absent or invented",
    ),
    *[
        A(
            f"{path.stem}: no instruction to call TaskUpdate anywhere in the body, every mention is a prohibition",
            path,
            lambda text: "TaskUpdate({" not in text
            and re.search(r"(?i)\b(?:call|use|run|invoke)\s+`?TaskUpdate", re.sub(r"(?i)(?:do not|don't|never|not|does not|do NOT)[^.\n]{0,60}\bcall\b[^.\n]{0,30}TaskUpdate", "", text.split("\n---\n", 1)[-1])) is None
            and "call TaskUpdate BEFORE" not in text
            and "you own task completion" not in text,
            "the body of every agent file, not a five-name list: no body tells an agent to call TaskUpdate (a mention is allowed only as a prohibition)",
        )
        for path in sorted(AGENTS.glob("*.md"))
    ],
    # --- P4.T7.1: code-review, verification and building skills (E1, E2, E3 part; C4.2 floor unchanged) ---
    A(
        "code-review: one vocabulary, MINOR is defined, zero-finding verdict words and the three-citation rule are stated",
        SKILLS / "code-review" / "SKILL.md",
        lambda text: "before reporting zero findings (Zero-Finding Halt re-scan)" in text
        and "`APPROVE` for `code-reviewer`, `CLEAN` for `failure-hunter`" in text
        and "at least three positive assertions with file:line evidence" in text
        and "Findings of any severity that do not block and that you don't fix in this pass (the router's non-blocking \"Minor\" class)" in text
        and "appends every non-blocking item to" in text
        and "triage labels for received feedback, not the review severities above" in text
        and "before reporting CLEAN" not in text
        and "Minor/Medium findings" not in text
        and "non-blocking Minor item" not in text,
        "the skill said CLEAN for a reviewer who says APPROVE, used Minor without defining it, and never named the router's three-citation validity check",
    ),
    A(
        "code-review: the router-merge verdict rule agrees with router step 6, including the upheld-dispute exception",
        SKILLS / "code-review" / "SKILL.md",
        lambda text: "the blocking verdict is authoritative (`CHANGES_REQUESTED` over `APPROVE`, `FAIL` over `PASS`)" in text
        and "except that a re-raised finding whose dispute the verifier upheld (`DISPUTE_UPHELD`) is dropped by the router" in text
        and "one whose dispute is still in flight continues to the verifier" in text
        and "stricter verdict wins" not in text
        and "treat the blocking verdict as authoritative (FAIL over PASS, CHANGES_REQUESTED over APPROVE), except that a re-raised finding whose dispute the verifier upheld is dropped"
        in read(SKILLS / "cc10x-router" / "SKILL.md"),
        "the skill said the stricter verdict wins with no exception, while step 6 (as amended in P4B) exempts an upheld dispute; both texts now say the same",
    ),
    A(
        "code-review: the >=80 floor is unchanged (C4.2)",
        SKILLS / "code-review" / "SKILL.md",
        contains_all(
            "Only report issues with confidence ≥80",
            "| <80 | Do not report — insufficient evidence |",
            "a security-category finding below 80 confidence is NOT silently dropped",
        ),
        "C4.2: the P4C vocabulary edits must not move the confidence floor or the security exception",
    ),
    A(
        "verification: manual evidence is a validation level, never a TDD exit code (E2)",
        SKILLS / "verification" / "SKILL.md",
        lambda text: "Manual evidence is a validation level for verification, never a substitute for a TDD RED or GREEN exit code: with no test runner and no scripted check, require a runner or block." in text,
        "the Manual row alone would let a builder pass on a human checklist; the verification skill now says the same single rule as the agents",
    ),
    A(
        "building: the no-runner exception is the same single rule as the two agents (E2, three sites)",
        SKILLS / "building" / "SKILL.md",
        lambda text: all(
            "Never fabricate `TDD_RED_EXIT` or `TDD_GREEN_EXIT`: leave both `null`." in body
            and "the rule is: require a runner or block" in body
            for body in (
                text,
                read(AGENTS / "component-builder.md"),
                read(AGENTS / "bug-investigator.md"),
            )
        )
        and "a scripted check with real exit codes is TDD evidence; manual browser verification is not" in text
        and "TDD evidence may use manual browser verification" not in text
        and "Set TDD_RED_EXIT=1" not in text,
        "the skill still told the builder to set TDD_RED_EXIT=1 and TDD_GREEN_EXIT=0 from a manual check, contradicting its own RED rule and both agents",
    ),
    A(
        "building reference: live proof does not send a BUILD agent to qa-strategy (E3)",
        SKILLS / "building" / "references" / "integration-and-live-proof.md",
        lambda text: "qa-strategy" not in text
        and "defined there" not in text
        and "the plan's `### Live Verification Strategy`" in text,
        "the router forbids loading qa-strategy outside the QA route; the reference now points at the plan's own live-verification section",
    ),
    # --- P4.T7.2: qa-strategy and codebase-design (E3, E7 part) ---
    A(
        "qa-strategy: no DRAFT or PLACEHOLDER marker, no claim that BUILD sends readers here, and no pointer to a reference file that is not there",
        SKILLS / "qa-strategy" / "SKILL.md",
        lambda text: "DRAFT" not in text
        and "PLACEHOLDER" not in text
        and "sends a BUILD phase to" not in text
        and "## Reference files" not in text
        and all(
            (SKILLS / "qa-strategy" / ref).exists()
            for ref in re.findall(r"`(references/[^`]+\.md)`", text)
        ),
        "the skill carried a DRAFT status, a PLACEHOLDER header and four references/*.md pointers to files that do not exist, and said BUILD sends readers here after the router forbade it",
    ),
    A(
        "qa-strategy: log access guidance stays as plain guidance",
        SKILLS / "qa-strategy" / "SKILL.md",
        contains(
            "**Log access strategy.** How the harness reads logs differs sharply by environment (local stdout, container logs, a log platform); state the access method in the plan for the environment in use."
        ),
        "the placeholder marker is gone and the one true sentence it carried is kept",
    ),
    A(
        "qa-strategy: the artifact template table and its pinned row text are byte-stable (PP-43)",
        SKILLS / "qa-strategy" / "SKILL.md",
        contains_all(
            "| `test-plan.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-test-plan.template.md` |",
            "| `env-plan.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-env-plan.template.md` |",
            "| `feature-map.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-feature-map.template.md` (router-owned, inline consolidation) |",
            "| `report.md` | `${CLAUDE_PLUGIN_ROOT}/templates/qa-report.template.md` (router-seeded at `qa-execute`; `qa-executor` rewrites it whole with `Write`) |",
            "| harness manifest | `${CLAUDE_PLUGIN_ROOT}/templates/live-harness.template.json` |",
            "**Why deletion is forbidden.**",
        ),
        "P4C removes markers and dead pointers only; the template table that PP-43 pins is not edited",
    ),
    A(
        "codebase-design: names only the skills that point at it",
        SKILLS / "codebase-design" / "SKILL.md",
        lambda text: re.search(r"other skills \(architecture,\s+codebase-hygiene\) point here instead of restating them", text) is not None
        and re.search(r"codebase-hygiene,\s+building", text) is None
        and all(
            "cc10x:codebase-design" in read(SKILLS / name / "SKILL.md")
            for name in ("architecture", "codebase-hygiene")
        ),
        "the description said building and planning point here; the description claimed pointers from building and planning; the claim now names the skills that actually reference it",
    ),
    A(
        "building: the seam definition is the codebase-design one",
        SKILLS / "building" / "SKILL.md",
        lambda text: "A seam is the place where a module's interface lives" in text
        and "(`cc10x:codebase-design` defines the term)" in text
        and "A seam is the public boundary where you observe behavior without reaching inside" not in text
        and "the _location_ at which a module's interface lives" in read(SKILLS / "codebase-design" / "SKILL.md"),
        "building defined a seam as a public boundary while codebase-design defines it as where a module's interface lives; one definition, pointed at the canonical skill",
    ),
    # --- P4.T7.3: memory-and-handoff, mcp-cli, research, descriptions, misc (E4, E5, E6, E7, E10) ---
    A(
        "memory-and-handoff: the surface list names .cc10x/qa/ and .cc10x/state/",
        SKILLS / "memory-and-handoff" / "SKILL.md",
        contains_all(
            "| `.cc10x/qa/` |",
            "`env/{env_key}/setup.md`",
            "| `.cc10x/state/git-approval.json` |",
        ),
        "the surface table omitted two router-owned surfaces that exist on disk",
    ),
    A(
        "memory-and-handoff: the compounding loop says what the router implements and what is deferred",
        SKILLS / "memory-and-handoff" / "SKILL.md",
        contains_all(
            "**What the router implements today.**",
            "no session-start loader reads it",
            "Deferred, not implemented by the router",
            "consolidate-at-3+ on `patterns.md` (step 3)",
            "the periodic refresh with the five-outcome model (step 4",
            "the CLAUDE.md/AGENTS.md discover step (step 5)",
        ),
        "the skill described a five-step loop in the imperative while the router implements capture and the solution-doc threshold only",
    ),
    A(
        "mcp-cli: a specific non-auto-fire description and a manual, unpinned-free install step",
        SKILLS / "mcp-cli" / "SKILL.md",
        lambda text: skill_description(text).startswith(
            "Use when a research task needs a single tool from a named MCP server that is not already mounted"
        )
        and "Not for servers already mounted" in skill_description(text)
        and "git clone" not in text
        and "go build" not in text
        and "## Prerequisite (manual, user-installed)" in text
        and "The agent does not install it" in text,
        "the description invited auto-fire on any MCP talk and the prerequisite had the agent clone and build an unpinned third-party binary into the PATH",
    ),
    A(
        "research: no branch on a marker no agent emits, and allowed-tools is described as pre-approval",
        SKILLS / "research" / "SKILL.md",
        lambda text: "[Web phase unavailable]" not in text
        and "`allowed-tools: Read` in this skill's frontmatter pre-approves Read; it does not restrict other tools" in text,
        "no agent emits [Web phase unavailable]; and the Read-only grant was read as a write ban",
    ),
    A(
        "debugging playbooks: git bisect run uses env so the command can execute",
        SKILLS / "debugging" / "references" / "root-cause-playbooks.md",
        lambda text: "git bisect run env CI=true npm test" in text and "git bisect run CI=true" not in text,
        "bisect run exec'd `CI=true` as a program name (exit 127)",
    ),
    A(
        "coverage-thresholds template: the install note names no repo-relative plugin path and the file is valid JSON",
        PLUGIN / "templates" / "coverage-thresholds.json",
        lambda text: "plugins/cc10x" not in text
        and json.loads(text)["_install"].startswith("Copy this file from the plugin's templates/ directory into the project root")
        and json.loads(text)["lines"] == 80,
        "a user project has no plugins/cc10x directory; the note now says where the file comes from",
    ),
    A(
        "diff-driven-docs: the opt-out is read from activeContext.md Session Settings, where the router reads it",
        SKILLS / "diff-driven-docs" / "SKILL.md",
        lambda text: "`DIFF_DRIVEN_DOCS: skip` to the `## Session Settings` section of `activeContext.md`" in text
        and "`DIFF_DRIVEN_DOCS: skip` to the `## Session Settings` section of `CLAUDE.md`" not in text,
        "the skill said CLAUDE.md; the router reads activeContext.md ## Session Settings",
    ),
    *[
        A(
            f"{name}: the description is a trigger, not a statement of which agent loads the skill",
            SKILLS / name / "SKILL.md",
            lambda text: skill_description(text).startswith("Use when ")
            and re.search(r"(?i)\bloaded by\b|\bpreloaded\b|\bloaded via\b|\bloads? (?:into|in)\b", skill_description(text)) is None,
            "eight internal skills named the loading agent instead of a trigger (the finding counted six); the trigger style is what the other skills use",
        )
        for name in ("agent-common", "building", "debugging", "domain-modeling", "planning", "qa-strategy", "research", "verification")
    ],
]


def main(argv: list[str] | None = None) -> int:
    global ALLOW_NO_YAML
    parser = argparse.ArgumentParser(description="cc10x prompt clause assertions")
    parser.add_argument("--allow-no-yaml", action="store_true", help="skip the YAML parse check when PyYAML is missing")
    ALLOW_NO_YAML = parser.parse_args(argv).allow_no_yaml
    failures = []
    skipped = []
    for a in ASSERTIONS:
        before = YAML_SKIPS[0]
        if not a.eval():
            failures.append(
                f"  - {a.name} [{a.path.relative_to(ROOT)}]: {a.description}"
            )
        elif YAML_SKIPS[0] > before:
            skipped.append(a.name)
    for name in skipped:
        print(f"SKIPPED-YAML {name}: PyYAML is not importable (--allow-no-yaml)")

    if failures:
        print(f"PROMPT CLAUSE ASSERTIONS: FAIL ({len(failures)} failure(s))")
        for f in failures:
            print(f)
        return 1
    passed = len(ASSERTIONS) - len(skipped)
    suffix = f", {len(skipped)} skipped" if skipped else ""
    print(f"PROMPT CLAUSE ASSERTIONS: OK ({passed} assertions passed{suffix})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
