#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(os.environ.get("CC10X_REPO_ROOT") or Path(__file__).resolve().parents[3])
if not (ROOT / "plugins" / "cc10x").is_dir():
    raise SystemExit(f"CC10X_REPO_ROOT is not a cc10x repo (no plugins/cc10x): {ROOT}")
PLUGIN_ROOT = ROOT / "plugins" / "cc10x"
ROUTER = PLUGIN_ROOT / "skills" / "cc10x-router" / "SKILL.md"
ROUTER_REFERENCES_DIR = PLUGIN_ROOT / "skills" / "cc10x-router" / "references"
ROUTER_ARTIFACT_POLICY_REFERENCE = (
    ROUTER_REFERENCES_DIR / "workflow-artifact-and-hook-policy.md"
)
ROUTER_BUILD_REFERENCE = ROUTER_REFERENCES_DIR / "build-workflow.md"
ROUTER_DEBUG_REFERENCE = ROUTER_REFERENCES_DIR / "debug-workflow.md"
ROUTER_REVIEW_REFERENCE = ROUTER_REFERENCES_DIR / "review-workflow.md"
ROUTER_PLAN_REFERENCE = ROUTER_REFERENCES_DIR / "plan-workflow.md"
ROUTER_REMEDIATION_REFERENCE = ROUTER_REFERENCES_DIR / "remediation-and-research.md"
ROUTER_ARTIFACT_SKELETON = ROUTER_REFERENCES_DIR / "workflow-artifact.skeleton.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
TASK_COMPLETED_GUARD = PLUGIN_ROOT / "scripts" / "cc10x_task_completed_guard.py"
INVARIANTS = ROOT / "docs" / "router-invariants.md"
PROMPT_INVARIANTS = ROOT / "docs" / "prompt-invariants.md"
PROMPT_SURFACE_INVENTORY = ROOT / "docs" / "prompt-surface-inventory.md"
PROMPT_CHANGE_CHECKLIST = ROOT / "docs" / "prompt-change-checklist.md"
ORCHESTRATION_BIBLE = ROOT / "docs" / "cc10x-orchestration-bible.md"
ORCHESTRATION_LOGIC = ROOT / "docs" / "cc10x-orchestration-logic-analysis.md"
ORCHESTRATION_SAFETY = ROOT / "docs" / "cc10x-orchestration-safety.md"
AGENT_CONTRACT_REGISTRY = ROOT / "docs" / "agent-contract-registry.md"
VERIFIER_LATENCY_MODEL = ROOT / "docs" / "verifier-latency-model.md"
LATENCY_REDUCTION_NOTE = ROOT / "docs" / "latency-reduction-note.md"
REPLAY_CHECK = PLUGIN_ROOT / "tools" / "workflow_replay_check.py"
LATENCY_AUDIT = PLUGIN_ROOT / "tools" / "latency_audit.py"
LIVE_HARNESS_RUNNER = PLUGIN_ROOT / "tools" / "live_harness_runner.py"
SESSION_MEMORY_SKILL = PLUGIN_ROOT / "skills" / "memory-and-handoff" / "SKILL.md"
PLANNER_AGENT = PLUGIN_ROOT / "agents" / "planner.md"
PLANNING_PATTERNS_SKILL = PLUGIN_ROOT / "skills" / "planning" / "SKILL.md"
BRAINSTORMING_SKILL = PLUGIN_ROOT / "skills" / "exploration" / "SKILL.md"
FIXTURES_DIR = PLUGIN_ROOT / "tests" / "fixtures"
LIVE_MANIFEST_TEMPLATE = PLUGIN_ROOT / "templates" / "live-harness.template.json"
PLANNING_LIVE_REFERENCE = (
    PLUGIN_ROOT / "skills" / "planning" / "references" / "live-verification-strategy.md"
)
VERIFY_LIVE_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "verification"
    / "references"
    / "live-production-testing.md"
)
LIVE_MANIFEST_BOOTSTRAP = (
    PLUGIN_ROOT / "tests" / "live" / "manifests" / "cc10x-bootstrap.json"
)
DEBUGGING_PLAYBOOKS_REFERENCE = (
    PLUGIN_ROOT / "skills" / "debugging" / "references" / "root-cause-playbooks.md"
)
DEBUGGING_HYGIENE_REFERENCE = (
    PLUGIN_ROOT / "skills" / "debugging" / "references" / "investigation-hygiene.md"
)
REVIEW_ORDER_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "code-review"
    / "references"
    / "review-order-and-checkpoints.md"
)
REVIEW_SECURITY_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "code-review"
    / "references"
    / "security-review-checklist.md"
)
REVIEW_HEURISTICS_REFERENCE = (
    PLUGIN_ROOT / "skills" / "code-review" / "references" / "code-review-heuristics.md"
)
FRONTEND_STATE_REFERENCE = (
    PLUGIN_ROOT / "skills" / "frontend" / "references" / "ui-state-and-feedback.md"
)
FRONTEND_A11Y_REFERENCE = (
    PLUGIN_ROOT / "skills" / "frontend" / "references" / "accessibility-and-forms.md"
)
FRONTEND_LAYOUT_REFERENCE = (
    PLUGIN_ROOT / "skills" / "frontend" / "references" / "performance-and-layout.md"
)
FRONTEND_DESIGN_MD_REFERENCE = (
    PLUGIN_ROOT / "skills" / "frontend" / "references" / "design-md-authoring.md"
)
FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "frontend"
    / "references"
    / "design-md-inspiration-index.md"
)
TDD_PATTERNS_REFERENCE = (
    PLUGIN_ROOT / "skills" / "building" / "references" / "testing-patterns.md"
)
TDD_MOCKS_REFERENCE = (
    PLUGIN_ROOT / "skills" / "building" / "references" / "test-data-and-mocks.md"
)
TDD_LIVE_PROOF_REFERENCE = (
    PLUGIN_ROOT / "skills" / "building" / "references" / "integration-and-live-proof.md"
)
SESSION_MEMORY_MODEL_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "memory-and-handoff"
    / "references"
    / "memory-model-and-ownership.md"
)
SESSION_MEMORY_OPERATIONS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "memory-and-handoff"
    / "references"
    / "memory-operations.md"
)
SESSION_MEMORY_FILE_CONTRACTS_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "memory-and-handoff"
    / "references"
    / "memory-file-contracts.md"
)
SESSION_MEMORY_CONTEXT_BUDGET_REFERENCE = (
    PLUGIN_ROOT
    / "skills"
    / "memory-and-handoff"
    / "references"
    / "context-budget-and-checkpointing.md"
)
FIRST_PLACE_STRATEGY = (
    ROOT / "docs" / "benchmarks" / "2026-03-12-first-place-strategy.md"
)
import doc_consistency_check  # noqa: E402 count and claim checks share the docs-rot ratchet
from fixture_registry import REQUIRED_FIXTURES  # noqa: E402 shared with workflow_replay_check

PROMPT_STEAL_NOTE = (
    ROOT / "docs" / "benchmarks" / "2026-03-14-prompt-steal-hardening.md"
)
PLANNING_RECOVERY_NOTE = (
    ROOT / "docs" / "benchmarks" / "2026-03-16-planning-recovery.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    return 1


class FrontmatterError(ValueError):
    pass


_KEY = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
_BOOLS = {"true": True, "True": True, "TRUE": True, "false": False, "False": False, "FALSE": False}


def _strip_comment(value: str) -> str:
    quote = ""
    for i, ch in enumerate(value):
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or value[i - 1] in " \t"):
            return value[:i].strip()
    return value.strip()


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, tuple[str, list[str]]]:
    """Map each top-level key to (inline value without comment, indented body lines).

    Raises FrontmatterError instead of guessing when the block is not delimited.
    """
    lines = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines[0].rstrip() != "---":
        raise FrontmatterError("frontmatter must start with a '---' line")
    close = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if close is None:
        raise FrontmatterError("frontmatter has no closing '---' line")
    fields: dict[str, tuple[str, list[str]]] = {}
    key = ""
    for raw in lines[1:close]:
        if not raw.strip() or raw.lstrip(" ").startswith("#"):
            continue
        if raw[0] in " \t":
            if not key:
                raise FrontmatterError(f"indented line before any key: {raw.strip()!r}")
            fields[key][1].append(raw)
            continue
        match = _KEY.match(raw)
        if not match:
            raise FrontmatterError(f"cannot parse frontmatter line: {raw.strip()!r}")
        key = match.group(1)
        if key in fields:
            raise FrontmatterError(f"duplicate frontmatter key: {key}")
        fields[key] = (_strip_comment(match.group(2)), [])
    return fields


def fm_scalar(fields: dict, key: str) -> str | None:
    if key not in fields:
        return None
    inline, body = fields[key]
    if not inline or body or inline[0] in "[{|>":
        raise FrontmatterError(f"{key} must be a single-line scalar")
    return _unquote(inline)


def fm_bool(fields: dict, key: str) -> bool | None:
    value = fm_scalar(fields, key)
    if value is None:
        return None
    if value not in _BOOLS:
        raise FrontmatterError(f"{key} must be a boolean, got {value!r}")
    return _BOOLS[value]


def fm_list(fields: dict, key: str) -> list[str] | None:
    if key not in fields:
        return None
    inline, body = fields[key]
    if inline and body:
        raise FrontmatterError(f"{key} mixes an inline value with indented lines")
    if inline:
        if not (inline.startswith("[") and inline.endswith("]")):
            raise FrontmatterError(f"{key} must be a list, got {inline!r}")
        inner = inline[1:-1]
        if any(ch in inner for ch in "[]{}"):
            raise FrontmatterError(f"{key} flow list is too complex to read")
        items = [_unquote(part.strip()) for part in inner.split(",")]
    else:
        items = []
        for raw in body:
            indent = raw[: len(raw) - len(raw.lstrip(" \t"))]
            if "\t" in indent:
                raise FrontmatterError(f"{key} list uses tab indentation")
            if raw.lstrip().startswith("#"):
                continue
            stripped = raw.strip()
            if stripped != "-" and not stripped.startswith("- "):
                raise FrontmatterError(f"{key} list has a non-item line: {stripped!r}")
            items.append(_unquote(_strip_comment(stripped[1:])))
    if not items or any(not item for item in items):
        raise FrontmatterError(f"{key} has an empty list or an empty item")
    return items


def check_preloaded_skills_invocable(
    agents_dir: Path = PLUGIN_ROOT / "agents",
    skills_dir: Path = PLUGIN_ROOT / "skills",
) -> list[str]:
    errors: list[str] = []
    inspected = 0
    declared = 0
    for agent in sorted(agents_dir.glob("*.md")):
        text = read(agent)
        head = re.split(r"^---[ \t]*$", text.replace("\ufeff", ""), maxsplit=2, flags=re.M)
        if re.search(r"^[ \t]*skills[ \t]*:", head[1] if len(head) > 2 else text, re.M):
            declared += 1
        try:
            skills = fm_list(parse_frontmatter(text), "skills")
        except FrontmatterError as exc:
            errors.append(f"{agent.name}: {exc}")
            continue
        if skills is None:
            continue
        inspected += 1
        for name in skills:
            name = name.removeprefix("cc10x:")
            skill = skills_dir / name / "SKILL.md"
            if not skill.exists():
                errors.append(f"{agent.name} preloads missing skill {name}")
                continue
            try:
                disabled = fm_bool(parse_frontmatter(read(skill)), "disable-model-invocation")
            except FrontmatterError as exc:
                errors.append(f"{name}/SKILL.md: {exc}")
                continue
            if disabled:
                errors.append(
                    f"{agent.name} preloads {name}, which sets disable-model-invocation: true (agent preload skips it)"
                )
    if inspected == 0:
        errors.append(f"no agents with a skills: list were inspected under {agents_dir.name}/")
    elif inspected < declared:
        errors.append(
            f"only {inspected} of {declared} agents declaring skills: were inspected (a skills: key was not read)"
        )
    return errors


def check_researcher_mcp_lanes(agents_dir: Path = PLUGIN_ROOT / "agents") -> list[str]:
    path = agents_dir / "researcher.md"
    if not path.exists():
        return [f"{path.name} not found under {agents_dir.name}/"]
    try:
        fields = parse_frontmatter(read(path))
        if fields.get("tools", ("", []))[1]:
            granted = set(fm_list(fields, "tools") or [])
        else:
            granted = {t.strip() for t in (fm_scalar(fields, "tools") or "").split(",")}
    except FrontmatterError as exc:
        return [f"{path.name}: {exc}"]
    return [
        f"researcher.md tools: missing {name} (a tools allowlist excludes MCP tools unless named)"
        for name in ("mcp__brightdata", "mcp__octocode")
        if name not in granted
    ]


DOCUMENTED_AGENT_COLORS = {
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "cyan",
}


def check_agent_colors(agents_dir: Path = PLUGIN_ROOT / "agents") -> list[str]:
    errors: list[str] = []
    agents = sorted(agents_dir.glob("*.md"))
    if not agents:
        return [f"no agents found under {agents_dir.name}/"]
    for agent in agents:
        try:
            color = fm_scalar(parse_frontmatter(read(agent)), "color")
        except FrontmatterError as exc:
            errors.append(f"{agent.name}: {exc}")
            continue
        if color is not None and color not in DOCUMENTED_AGENT_COLORS:
            errors.append(f"{agent.name} color {color!r} is not a documented agent color")
    return errors


_HOOK_SCRIPT = re.compile(r"scripts/([A-Za-z0-9_.-]+)")
REQUIRED_HOOK_SCRIPTS = ("cc10x_git_guard.py", "cc10x_qa_isolation_guard.py", "cc10x_preflight.sh")


def check_hook_registration(plugin_root: Path = PLUGIN_ROOT) -> list[str]:
    registered = set(_HOOK_SCRIPT.findall(read(plugin_root / "hooks" / "hooks.json")))
    errors = [
        f"hooks.json does not register {script}"
        for script in REQUIRED_HOOK_SCRIPTS
        if script not in registered
    ]
    errors.extend(
        f"hooks.json references missing script {script}"
        for script in sorted(registered)
        if not (plugin_root / "scripts" / script).exists()
    )
    return errors


DOCS_ROT_BASELINE = PLUGIN_ROOT / "tools" / "docs_rot_baseline.json"
_INVENTORY_PATH = re.compile(r"`((?:plugins|docs|\.claude-plugin)/[^`\s*]+)`")
_INVENTORY_ENTRY = re.compile(r"^### (\S+)[ \t]*$", re.M)
_REGISTRY_ROW = re.compile(r"^\|[ \t]*`([A-Za-z0-9_-]+)`[ \t]*\|", re.M)
_PRODUCT_LINE = re.compile(r"Current product line is `v(\d+)\.(\d+)\.\d+`")
PRODUCT_LINE_DOCS = (
    "router-invariants.md",
    "prompt-invariants.md",
    "agent-contract-registry.md",
    "prompt-surface-inventory.md",
)


def check_living_docs(root: Path = ROOT) -> dict[str, str]:
    """Map each rot key (`<check>:<subject>`) to its message; the ratchet decides what fails."""
    plugin = root / "plugins" / "cc10x"
    docs = root / "docs"
    agents = {p.stem for p in (plugin / "agents").glob("*.md")}
    skills = {p.name for p in (plugin / "skills").iterdir() if p.is_dir()}
    failures: dict[str, str] = {}

    inventory = read(docs / "prompt-surface-inventory.md")
    for path in sorted(set(_INVENTORY_PATH.findall(inventory))):
        if not (root / path.rstrip("/")).exists():
            failures[f"inventory-path:{path}"] = f"prompt-surface-inventory.md names {path}, which does not exist"
    entries = set(_INVENTORY_ENTRY.findall(inventory))
    for name in sorted((agents | skills) - entries):
        failures[f"inventory-missing-entry:{name}"] = f"prompt-surface-inventory.md has no '### {name}' entry"
    for name in sorted(entries - (agents | skills)):
        failures[f"inventory-phantom-entry:{name}"] = (
            f"prompt-surface-inventory.md has an entry '### {name}' for a nonexistent agent or skill"
        )

    rows = set(_REGISTRY_ROW.findall(read(docs / "agent-contract-registry.md")))
    for name in sorted(agents - rows):
        failures[f"registry-missing-row:{name}"] = f"agent-contract-registry.md has no row for agent {name}"
    for name in sorted(rows - agents):
        failures[f"registry-phantom-row:{name}"] = f"agent-contract-registry.md has a row for nonexistent agent {name}"

    version = json.loads(read(plugin / ".claude-plugin" / "plugin.json")).get("version", "")
    current = tuple(int(part) for part in version.split(".")[:2])
    for doc in PRODUCT_LINE_DOCS:
        path = docs / doc
        match = _PRODUCT_LINE.search(read(path)) if path.exists() else None
        if match and (int(match.group(1)), int(match.group(2))) < current:
            failures[f"registry-banner-stale:docs/{doc}"] = (
                f"docs/{doc} claims product line v{match.group(1)}.{match.group(2)}.x, older than the current {version}"
            )
    failures.update(doc_consistency_check.check_claims(root))
    return failures


def load_rot_baseline(path: Path = DOCS_ROT_BASELINE) -> list[dict]:
    return json.loads(read(path)).get("entries", []) if path.exists() else []


def apply_rot_ratchet(
    failures: dict[str, str], baseline: list[dict], strict: bool = False
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    known: dict[str, dict] = {}
    for item in baseline:
        if not item.get("key") or not item.get("owner") or not item.get("reason"):
            errors.append(f"docs rot baseline entry needs a key, an owner and a reason: {item}")
        if item.get("key"):
            known[item["key"]] = item
    for key in sorted(set(failures) - set(known)):
        errors.append(f"new rot: {key}: {failures[key]}")
    for key in sorted(set(known) - set(failures)):
        errors.append(f"stale baseline entry (no longer fails, remove it from docs_rot_baseline.json): {key}")
    warnings: list[str] = []
    remaining = [known[key] for key in sorted(set(known) & set(failures))]
    if remaining:
        owners: dict[str, int] = {}
        for item in remaining:
            owners[item.get("owner", "?")] = owners.get(item.get("owner", "?"), 0) + 1
        summary = f"{len(remaining)} docs rot baseline entries remain (owners: " + ", ".join(
            f"{owner} x{count}" for owner, count in sorted(owners.items())
        ) + ")"
        warnings.append(summary)
        if strict:
            errors.append(f"--strict: {summary}")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc10x harness audit")
    parser.add_argument("--strict", action="store_true", help="fail while the docs rot baseline is non-empty")
    args = parser.parse_args(argv)
    errors: list[str] = []

    plugin = json.loads(read(PLUGIN_JSON))
    hooks = json.loads(read(HOOKS_JSON))
    marketplace = (
        json.loads(read(MARKETPLACE_JSON)) if MARKETPLACE_JSON.exists() else {}
    )
    router = read(ROUTER)
    router_artifact_policy_reference = read(ROUTER_ARTIFACT_POLICY_REFERENCE)
    router_build_reference = read(ROUTER_BUILD_REFERENCE)
    router_debug_reference = read(ROUTER_DEBUG_REFERENCE)
    router_review_reference = read(ROUTER_REVIEW_REFERENCE)
    router_plan_reference = read(ROUTER_PLAN_REFERENCE)
    router_remediation_reference = read(ROUTER_REMEDIATION_REFERENCE)
    router_artifact_skeleton = read(ROUTER_ARTIFACT_SKELETON)
    router_surface = "\n\n".join(
        [
            router,
            router_artifact_policy_reference,
            router_build_reference,
            router_debug_reference,
            router_review_reference,
            router_plan_reference,
            router_remediation_reference,
            router_artifact_skeleton,
        ]
    )
    task_completed_guard = read(TASK_COMPLETED_GUARD)
    readme = read(README)
    changelog = read(CHANGELOG)
    invariants = read(INVARIANTS)
    prompt_invariants = read(PROMPT_INVARIANTS)
    prompt_surface_inventory = read(PROMPT_SURFACE_INVENTORY)
    prompt_change_checklist = read(PROMPT_CHANGE_CHECKLIST)
    orchestration_bible = read(ORCHESTRATION_BIBLE)
    orchestration_logic = read(ORCHESTRATION_LOGIC)
    orchestration_safety = read(ORCHESTRATION_SAFETY)
    session_memory = read(SESSION_MEMORY_SKILL)
    planner_agent = read(PLANNER_AGENT)
    planning_patterns = read(PLANNING_PATTERNS_SKILL)
    brainstorming = read(BRAINSTORMING_SKILL)
    verifier_latency_model = read(VERIFIER_LATENCY_MODEL)
    latency_reduction_note = read(LATENCY_REDUCTION_NOTE)

    version = plugin.get("version")
    if f"**Current version:** {version}" not in readme:
        errors.append(
            f"README.md current version does not match plugin.json ({version})"
        )
    if f"## [{version}]" not in changelog:
        errors.append(f"CHANGELOG.md missing release section for {version}")
    if MARKETPLACE_JSON.exists():
        marketplace_version = ((marketplace.get("metadata") or {}).get("version")) or ""
        if marketplace_version != version:
            errors.append(
                f"marketplace.json metadata.version ({marketplace_version}) does not match plugin.json ({version})"
            )
        plugins = marketplace.get("plugins") or []
        if not plugins:
            errors.append("marketplace.json has no plugins entries")
        else:
            plugin_entry = plugins[0]
            if plugin_entry.get("version") != version:
                errors.append(
                    f"marketplace.json plugin entry version ({plugin_entry.get('version')}) does not match plugin.json ({version})"
                )
            if plugin_entry.get("source") != "./plugins/cc10x":
                errors.append(
                    f"marketplace.json plugin source changed unexpectedly ({plugin_entry.get('source')})"
                )

    errors.extend(check_hook_registration())

    if not REPLAY_CHECK.exists():
        errors.append("missing workflow replay checker script")
    if not FIXTURES_DIR.exists():
        errors.append("missing workflow replay fixtures directory")
    else:
        for fixture in REQUIRED_FIXTURES:
            if not (FIXTURES_DIR / fixture).exists():
                errors.append(f"missing replay fixture {fixture}")
    if not FIRST_PLACE_STRATEGY.exists():
        errors.append("missing first-place strategy document")
    if not PROMPT_INVARIANTS.exists():
        errors.append("missing prompt invariant registry")
    if not PROMPT_SURFACE_INVENTORY.exists():
        errors.append("missing prompt surface inventory")
    if not PROMPT_CHANGE_CHECKLIST.exists():
        errors.append("missing prompt change checklist")
    if not ORCHESTRATION_BIBLE.exists():
        errors.append("missing orchestration bible")
    if not ORCHESTRATION_LOGIC.exists():
        errors.append("missing orchestration logic analysis")
    if not ORCHESTRATION_SAFETY.exists():
        errors.append("missing orchestration safety doc")
    if not AGENT_CONTRACT_REGISTRY.exists():
        errors.append("missing agent contract registry")
    if not PROMPT_STEAL_NOTE.exists():
        errors.append("missing latest prompt benchmark note")
    if not PLANNING_RECOVERY_NOTE.exists():
        errors.append("missing planning recovery benchmark note")
    if not VERIFIER_LATENCY_MODEL.exists():
        errors.append("missing verifier latency model")
    if not LATENCY_REDUCTION_NOTE.exists():
        errors.append("missing latency reduction note")
    if not LATENCY_AUDIT.exists():
        errors.append("missing latency audit script")
    if not LIVE_HARNESS_RUNNER.exists():
        errors.append("missing live harness runner script")
    if not LIVE_MANIFEST_TEMPLATE.exists():
        errors.append("missing live harness template manifest")
    if not PLANNING_LIVE_REFERENCE.exists():
        errors.append("missing planning live verification reference")
    if not VERIFY_LIVE_REFERENCE.exists():
        errors.append("missing verification live testing reference")
    if not LIVE_MANIFEST_BOOTSTRAP.exists():
        errors.append("missing live harness bootstrap manifest")
    if not DEBUGGING_PLAYBOOKS_REFERENCE.exists():
        errors.append("missing debugging root-cause playbooks reference")
    if not DEBUGGING_HYGIENE_REFERENCE.exists():
        errors.append("missing debugging investigation hygiene reference")
    if not REVIEW_ORDER_REFERENCE.exists():
        errors.append("missing code review order/checkpoints reference")
    if not REVIEW_SECURITY_REFERENCE.exists():
        errors.append("missing code review security checklist reference")
    if not REVIEW_HEURISTICS_REFERENCE.exists():
        errors.append("missing code review heuristics reference")
    if not FRONTEND_STATE_REFERENCE.exists():
        errors.append("missing frontend UI state reference")
    if not FRONTEND_A11Y_REFERENCE.exists():
        errors.append("missing frontend accessibility/forms reference")
    if not FRONTEND_LAYOUT_REFERENCE.exists():
        errors.append("missing frontend performance/layout reference")
    if not FRONTEND_DESIGN_MD_REFERENCE.exists():
        errors.append("missing frontend DESIGN.md authoring reference")
    if not FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE.exists():
        errors.append("missing frontend DESIGN.md inspiration reference")
    if not TDD_PATTERNS_REFERENCE.exists():
        errors.append("missing TDD testing patterns reference")
    if not TDD_MOCKS_REFERENCE.exists():
        errors.append("missing TDD test-data-and-mocks reference")
    if not TDD_LIVE_PROOF_REFERENCE.exists():
        errors.append("missing TDD integration/live-proof reference")
    if not SESSION_MEMORY_MODEL_REFERENCE.exists():
        errors.append("missing memory-and-handoff model/ownership reference")
    if not SESSION_MEMORY_OPERATIONS_REFERENCE.exists():
        errors.append("missing memory-and-handoff operations reference")
    if not SESSION_MEMORY_FILE_CONTRACTS_REFERENCE.exists():
        errors.append("missing memory-and-handoff file-contract reference")
    if not SESSION_MEMORY_CONTEXT_BUDGET_REFERENCE.exists():
        errors.append("missing memory-and-handoff context-budget reference")

    for required in ("brightdata", "octocode"):
        if required not in router_surface:
            errors.append(f"router no longer mentions MCP server '{required}'")
        if required not in readme:
            errors.append(
                f"README no longer documents optional MCP server '{required}'"
            )

    if ".cc10x/" not in readme:
        errors.append("README does not document the live .cc10x memory namespace")
    # The retired version-segmented namespace must not be presented as live.
    # Historical/migration mentions (legacy, residue, relocated, de-versioned,
    # or a version-history table row) are allowed.
    _history_markers = ("legacy", "residue", "relocated", "de-version", "| **v")
    for line in readme.splitlines():
        if ".cc10x/v10/" in line and not any(
            m in line.lower() for m in _history_markers
        ):
            errors.append(
                "README presents the retired .cc10x/v10/ namespace as live: "
                f"{line.strip()[:80]}"
            )

    required_router_inline = [
        "## 2a. Workflow Artifact And Hook Policy",
        "references/workflow-artifact-and-hook-policy.md",
        "references/build-workflow.md",
        "references/debug-workflow.md",
        "references/review-workflow.md",
        "references/plan-workflow.md",
        "references/remediation-and-research.md",
        "## 12. Chain Execution Loop",
        "## 13. Memory Finalization",
        "## 14. Hard Rules",
    ]
    for heading in required_router_inline:
        if heading not in router:
            errors.append(f"router missing required inline reference/text: {heading}")

    required_router_surface_text = [
        "## 1. Intent Routing",
        "## 2a. Workflow Artifact And Hook Policy",
        "## 3. Task Metadata Contract",
        "Scope-decision resume:",
        "## 8. Post-Agent Validation",
        "## 10. Research Orchestration",
        "## 12. Chain Execution Loop",
        "## 13. Memory Finalization",
        ".cc10x/workflows",
        "workflow_uuid",
        "phase_cursor",
        "plan_mode",
        "verification_rigor",
        "proof_status",
        "traceability",
        "telemetry",
        "planning_review_runs",
        "planning_review_findings",
        "planning_review_status",
        "task_metrics_available",
        "phase_exit_proof_runs",
        "extended_audit_runs",
        "plan_trust_gate",
        "phase_exit_gate",
        "skill_precedence_gate",
        "Convergence rule:",
    ]
    for heading in required_router_surface_text:
        if heading not in router_surface:
            errors.append(f"router surface missing required heading/text: {heading}")

    reference_expectations = {
        ROUTER_ARTIFACT_POLICY_REFERENCE: (
            "## 2a. Workflow Artifact And Hook Policy",
            "Artifact schema must include:",
            "Hook policy:",
        ),
        ROUTER_BUILD_REFERENCE: (
            "### BUILD preparation",
            "### BUILD task graph",
            "plan_trust_gate",
        ),
        ROUTER_DEBUG_REFERENCE: (
            "### DEBUG preparation",
            "### DEBUG task graph",
            "[DEBUG-RESET:",
        ),
        ROUTER_REVIEW_REFERENCE: (
            "### REVIEW preparation",
            "### REVIEW task graph",
            "CHANGES_REQUESTED",
        ),
        ROUTER_PLAN_REFERENCE: (
            "### PLAN preparation",
            "### PLAN task graph",
            "decision_rfc",
        ),
        ROUTER_REMEDIATION_REFERENCE: (
            "## 9. Remediation And Workflow Rules",
            "## 10. Research Orchestration",
            "## 11. Re-Review Loop",
        ),
    }
    for path, expected_phrases in reference_expectations.items():
        text = read(path)
        for phrase in expected_phrases:
            if phrase not in text:
                errors.append(f"{path.name} missing required reference text: {phrase}")

    required_task_metadata = (
        "wf:",
        "kind:",
        "origin:",
        "phase:",
        "plan:",
        "scope:",
        "reason:",
    )
    for field in required_task_metadata:
        if field not in router_surface:
            errors.append(
                f"router surface missing task metadata contract field {field}"
            )

    if "Task Metadata Contract" not in invariants and "Status note:" not in invariants:
        errors.append(
            "router-invariants.md appears malformed or missing the current audit banner"
        )
    if "Prompt Behavioral Invariant Registry" not in prompt_invariants:
        errors.append("prompt-invariants.md appears malformed")
    if "Prompt Surface Inventory" not in prompt_surface_inventory:
        errors.append("prompt-surface-inventory.md appears malformed")
    if "Prompt Change Checklist" not in prompt_change_checklist:
        errors.append("prompt-change-checklist.md appears malformed")
    if "CC10X Orchestration Bible" not in orchestration_bible:
        errors.append("cc10x-orchestration-bible.md appears malformed")
    if "CC10x Orchestration Logic Analysis" not in orchestration_logic:
        errors.append("cc10x-orchestration-logic-analysis.md appears malformed")
    if "CC10x Orchestration Safety" not in orchestration_safety:
        errors.append("cc10x-orchestration-safety.md appears malformed")
    if "CC10X Agent Contract Registry" not in read(AGENT_CONTRACT_REGISTRY):
        errors.append("agent-contract-registry.md appears malformed")
    if "Verifier Latency Model" not in verifier_latency_model:
        errors.append("verifier-latency-model.md appears malformed")
    if "Latency Reduction Note" not in latency_reduction_note:
        errors.append("latency-reduction-note.md appears malformed")
    if "MEMORY_FINAL_EVENT" not in task_completed_guard:
        errors.append("task_completed_guard missing memory finalize event guard")
    for phrase in (
        'metadata.get("kind") != "memory"',
        "workflow_event_log_contains(workflow_id, MEMORY_FINAL_EVENT)",
        "missing-memory-finalized-event",
        "CC10X Memory Update:",
    ):
        if phrase not in task_completed_guard:
            errors.append(
                f"task_completed_guard missing memory finalize phrase '{phrase}'"
            )

    for required in (
        "memory-model-and-ownership.md",
        "memory-operations.md",
        "memory-file-contracts.md",
        "context-budget-and-checkpointing.md",
        "MEMORY_NOTES",
    ):
        if required not in session_memory:
            errors.append(
                f"memory-and-handoff skill missing required reference/text: {required}"
            )

    if "cc10x:agent-common" not in planner_agent:
        errors.append(
            "planner agent no longer loads agent-common (which owns the .cc10x memory namespace law)"
        )

    if "### memory-and-handoff" not in prompt_surface_inventory:
        errors.append("prompt surface inventory missing memory-and-handoff entry")
    if "PINV-012" not in prompt_invariants:
        errors.append("prompt invariants missing memory-and-handoff invariant")

    version_tag = f"v{version}"
    for name, body in (
        ("router invariants", invariants),
        ("prompt invariants", prompt_invariants),
        ("orchestration bible", orchestration_bible),
        ("orchestration logic analysis", orchestration_logic),
        ("agent contract registry", read(AGENT_CONTRACT_REGISTRY)),
    ):
        if version_tag not in body:
            errors.append(f"{name} is not synced to current version tag {version_tag}")

    for name, body in (
        ("orchestration bible", orchestration_bible),
        ("orchestration logic analysis", orchestration_logic),
        ("orchestration safety", orchestration_safety),
    ):
        if ".cc10x/workflows" not in body:
            errors.append(f"{name} does not reference the .cc10x workflow namespace")

    expected_router_fields = {
        "component-builder": [
            "PHASE_ID:",
            "PHASE_STATUS:",
            "PHASE_EXIT_READY:",
            "CHECKPOINT_TYPE:",
            "PROOF_STATUS:",
            "INPUTS:",
            "EXPECTED_ARTIFACTS:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "BLOCKED_ITEMS:",
            "SKIPPED_ITEMS:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "bug-investigator": [
            "VERIFICATION_RIGOR:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "BLAST_RADIUS_SCAN:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "planner": [
            "PLAN_MODE:",
            "VERIFICATION_RIGOR:",
            "SCENARIOS:",
            "ASSUMPTIONS:",
            "DECISIONS:",
            "OPEN_DECISIONS:",
            "DIFFERENCES_FROM_AGREEMENT:",
            "PLANNING_REVIEW_STATUS:",
            "PLANNING_REVIEW_RUNS:",
            "ALTERNATIVES:",
            "DRAWBACKS:",
            "PROVABLE_PROPERTIES:",
            "MEMORY_NOTES:",
            "NEXT_ACTION:",
        ],
        "plan-gap-reviewer": [
            'CONTRACT {"s":"PASS","b":false,"cr":0}',
            "## Planning Review: Pass",
            "PLANNING_REVIEW_STATUS:",
            "BLOCKING_FINDINGS_COUNT:",
            "FINDING_BUCKETS:",
            "REPLAN_NEEDED:",
            "REPLAN_REASON:",
        ],
        "integration-verifier": [
            "Proof Status:",
            "SCENARIOS_TOTAL",
            "SCENARIOS_PASSED",
            "SCENARIOS_FAILED",
            "REMEDIATION_NEEDED:",
            "REVERT_RECOMMENDED:",
        ],
        "code-reviewer": [
            "REMEDIATION_NEEDED:",
            "REMEDIATION_REASON:",
            "REMEDIATION_SCOPE_REQUESTED:",
            "REVERT_RECOMMENDED:",
        ],
    }

    for agent_name, fields in expected_router_fields.items():
        agent_path = PLUGIN_ROOT / "agents" / f"{agent_name}.md"
        text = read(agent_path)
        for field in fields:
            if field not in text:
                errors.append(
                    f"{agent_name}.md missing expected contract field '{field}'"
                )

    prompt_phrase_guards: dict[str, list[str]] = {
        "planner": [
            "No hidden assumptions, no implied approval",
            "A structurally neat but repo-wrong plan is a failed plan",
            "Codebase Reality Check",
            "Plan-vs-Code Gaps",
            "Hidden-Assumption Pass",
            "Plan Self-Review",
            "Expose unproven critical assumptions",
            "keep unapproved",
            "DIFFERENCES_FROM_AGREEMENT",
        ],
        "component-builder": [
            "Task completion is not goal achievement",
            "No work outside the current phase",
            "a phase is complete only when its proof reconciles",
        ],
        "integration-verifier": [
            "Task completion is not goal achievement",
            "Verify that the phase achieved its goal, not that prior agents said it did",
            "**Truths** (what must be true)",
            "**Artifacts** (what must exist)",
            "**Wiring** (what must be wired)",
            "You are an independent auditor",
            "### Timing & Workload",
        ],
        "plan-review-gate": [
            'No leniency. "Close enough" is FAIL.',
            'There is no "APPROVED WITH COMMENTS"',
            "A structurally neat but repo-wrong plan is FAIL.",
            "invented or unverified file/module assumptions",
            "missing touched surfaces or integration points",
            "This gate is an auditor, not a collaborator",
        ],
        "plan-gap-reviewer": [
            "Freshness rule:",
            "Do NOT load `.cc10x/*.md`.",
            "Return structured findings only.",
            "You do not own orchestration, plan approval, or plan edits.",
        ],
    }
    for stem, guard_phrases in prompt_phrase_guards.items():
        path = (
            PLUGIN_ROOT / "agents" / f"{stem}.md"
            if (PLUGIN_ROOT / "agents" / f"{stem}.md").exists()
            else PLUGIN_ROOT / "skills" / stem / "SKILL.md"
        )
        text = read(path)
        for phrase in guard_phrases:
            if phrase not in text:
                errors.append(f"{path.name} missing prompt safety phrase '{phrase}'")

    verification_skill = read(PLUGIN_ROOT / "skills" / "verification" / "SKILL.md")
    for phrase in (
        "Task completion is not goal achievement",
        "A PASS without proof is a claim",
        "## Goal-Backward Lens",
        "If you cannot independently reproduce a claimed success, return FAIL.",
        "EVIDENCE:",
        "live-production-testing.md",
    ):
        if phrase not in verification_skill:
            errors.append(f"verification missing prompt safety phrase '{phrase}'")

    if "live-verification-strategy.md" not in planning_patterns:
        errors.append("planning missing live verification reference link")

    forbidden_direct_memory_writes = (
        'Edit(file_path=".cc10x/activeContext.md"',
        'Edit(file_path=".cc10x/progress.md"',
        'Edit(file_path=".cc10x/patterns.md"',
    )
    for forbidden in forbidden_direct_memory_writes:
        if forbidden in planning_patterns:
            errors.append(
                "planning still contains direct memory writes instead of router-owned MEMORY_NOTES"
            )
        if forbidden in brainstorming:
            errors.append(
                "brainstorming still contains direct memory writes instead of router-owned handoff"
            )

    for phrase in ("## Plan Completeness Gate (MANDATORY — before save)",):
        if phrase not in planning_patterns:
            errors.append(f"planning missing harmony phrase '{phrase}'")
    if "MEMORY_NOTES" not in planner_agent:
        errors.append("planner missing router-owned MEMORY_NOTES contract field")

    for phrase in (
        "### Brainstorming Handoff (MACHINE-READABLE)",
        "DESIGN_FILE:",
        "router-owned — do NOT write memory directly",
    ):
        if phrase not in brainstorming:
            errors.append(f"brainstorming missing harmony phrase '{phrase}'")

    for phrase in (
        "parse `### Brainstorming Handoff (MACHINE-READABLE)`",
        "persist it into the workflow artifact `design_file` field",
        "fall back to the pre-existing memory design reference",
    ):
        if phrase not in router_plan_reference:
            errors.append(f"plan-workflow missing design handoff phrase '{phrase}'")

    for phrase in (
        "### Inline exploration handoff",
        "persist it into workflow artifact `design_file`",
        "- Ensure `- Design: {design_file}` remains correct",
    ):
        if phrase not in router:
            errors.append(f"router missing design-handoff phrase '{phrase}'")

    if "Explore project first, then invoke the router." in readme:
        errors.append(
            "README still contains the stale explore-before-router instruction"
        )
    if "The plugin ships four Claude Code-native hooks:" in readme:
        errors.append("README still contains the stale four-hooks inventory")
    if "query-optimize," in planner_agent or " query-optimize " in planner_agent:
        errors.append("planner still contains stale MongoDB example 'query-optimize'")

    frontend_skill = read(PLUGIN_ROOT / "skills" / "frontend" / "SKILL.md")
    frontend_design_md = read(FRONTEND_DESIGN_MD_REFERENCE)
    frontend_design_md_inspiration = read(FRONTEND_DESIGN_MD_INSPIRATION_REFERENCE)
    for phrase in (
        "DESIGN.md authoring",
        "creating/updating DESIGN.md from screenshots",
        "references/design-md-authoring.md",
        "references/design-md-inspiration-index.md",
        "style references when user asks for direction",
    ):
        if phrase not in frontend_skill:
            errors.append(
                f"frontend missing DESIGN.md trigger/reference phrase '{phrase}'"
            )
    for phrase in (
        "`DESIGN.md` is a project-local visual contract.",
        "Do not copy a screenshot or a brand.",
        "## Format Contract",
        "## Stable Structure",
        "## Token Rules",
        "## Screenshot-Specific Rules",
        "npx @google/design.md lint DESIGN.md",
        "Use inspiration references to choose a direction, not to clone",
    ):
        if phrase not in frontend_design_md:
            errors.append(
                f"design-md-authoring reference missing required phrase '{phrase}'"
            )
    for phrase in (
        "inspect only the requested company/style entry.",
        "Choose at most one primary reference and one secondary accent.",
        "Never paste a company `DESIGN.md` into project memory.",
        "YAML token front matter first",
    ):
        if phrase not in frontend_design_md_inspiration:
            errors.append(
                f"design-md-inspiration-index reference missing required phrase '{phrase}'"
            )

    description_hygiene = {
        PLUGIN_ROOT / "skills" / "frontend" / "SKILL.md": (
            "description: |",
            "workflow",
        ),
        PLUGIN_ROOT / "skills" / "debugging" / "SKILL.md": (
            "description: |",
            "workflow",
        ),
        PLUGIN_ROOT / "skills" / "verification" / "SKILL.md": (
            "description: |",
            "workflow",
        ),
        PLUGIN_ROOT / "skills" / "plan-review-gate" / "SKILL.md": (
            'description: "Use after',
            "workflow",
        ),
    }
    for path, (required_prefix, banned_word) in description_hygiene.items():
        text = read(path)
        if required_prefix not in text:
            errors.append(
                f"{path.name} description no longer matches trigger-style format"
            )
        first_lines = "\n".join(text.splitlines()[:6]).lower()
        if banned_word in first_lines:
            errors.append(f"{path.name} description appears to summarize workflow")

    # Runtime state-root drift guard.
    # Prompt surfaces, fixtures, and hook runtime (cc10x_hooklib.py) must agree on
    # the workflow state root. Drift between them produces split-brain: agents write
    # to one location, hooks read from another, and guards silently stop firing.
    # Scope the scan to runtime Python so historical CHANGELOG entries stay accurate.
    # This audit file itself is excluded because it has to name the legacy literal
    # in order to detect drift.
    runtime_scripts = sorted(
        p
        for p in (PLUGIN_ROOT / "scripts").glob("*.py")
        if p.name not in {"__init__.py", "harness_audit.py"}
    )
    for script in runtime_scripts:
        body = read(script)
        if ".claude/cc10x" in body or '.claude" / "cc10x' in body:
            errors.append(
                f"{script.name} still references the legacy .claude/cc10x state root"
            )

    errors.extend(check_preloaded_skills_invocable())
    errors.extend(check_researcher_mcp_lanes())
    errors.extend(check_agent_colors())

    rot_errors, rot_warnings = apply_rot_ratchet(
        check_living_docs(), load_rot_baseline(), strict=args.strict
    )
    errors.extend(rot_errors)
    for warning in rot_warnings:
        print(f"WARN: {warning}")

    if errors:
        return fail(errors)

    print("cc10x_harness_audit: OK")
    print(f"version={version}")
    print("mcp_servers=user-configured:brightdata,octocode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
