#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
REF_ROOT = ROOT / "ref-(dont-read-unless-specificly-mentioned)"
OUT_DIR = ROOT / "docs" / "benchmarks"
TODAY = date.today().isoformat()

ANTHROPIC_REPO = "anthropics-skills"
ANTHROPIC_REMOTE = "https://github.com/anthropics/skills.git"
ANTHROPIC_SKILL_PATH = "skills/skill-creator"
V7_REPO = "cc10x-v7.7.0-stable"
V7_TAG = "v7.7.0"

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
}

DEEP_BAKEOFF_TARGETS = {
    V7_REPO,
    "claude-code-harness",
    "claude-harness",
    "everything-claude-code",
    "babysitter",
    "metaswarm",
    "superpowers",
}

BAKEOFF_TOPLEVEL = {
    "README.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "AGENTS.md",
    "docs",
    "skills",
    "agents",
    "hooks",
    "scripts",
    "commands",
    "plugins",
    ".claude-plugin",
    ".claude",
}

BAKEOFF_CORE_DIRS = {"agents", "skills", "hooks", "scripts", "commands"}


@dataclass(frozen=True)
class RefRepo:
    name: str
    tier: str
    kind: str
    benchmark_path: str = "."
    notes: str = ""


@dataclass(frozen=True)
class Signal:
    key: str
    weight: int
    description: str


@dataclass(frozen=True)
class Scenario:
    key: str
    title: str
    expected: str
    strong_patterns: tuple[str, ...]
    weak_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeltaRule:
    path: str
    category: str
    feature_needles: tuple[tuple[str, str], ...]


REF_REPOS: tuple[RefRepo, ...] = (
    RefRepo(V7_REPO, "A", "harness", notes="Pinned stable baseline"),
    RefRepo(
        "claude-code-harness",
        "A",
        "harness",
        notes="Live GitHub candidate added from benchmark discovery",
    ),
    RefRepo(
        "claude-harness",
        "A",
        "harness",
        notes="Live GitHub candidate added from benchmark discovery",
    ),
    RefRepo("everything-claude-code", "A", "harness"),
    RefRepo("babysitter", "A", "harness"),
    RefRepo("metaswarm", "A", "harness"),
    RefRepo("superpowers", "A", "harness"),
    RefRepo("wshobson-agents", "A", "harness"),
    RefRepo("get-shit-done", "A", "harness"),
    RefRepo("agent-os", "B", "framework"),
    RefRepo("vercel-agent-skills", "B", "framework"),
    RefRepo("ralph-claude-code", "B", "framework"),
    RefRepo("system-prompts", "C", "prompt-library"),
    RefRepo("design-log-methodology", "C", "methodology"),
    RefRepo("symphony", "C", "methodology"),
    RefRepo(ANTHROPIC_REPO, "S", "skill-library", benchmark_path=ANTHROPIC_SKILL_PATH),
)


STRUCTURAL_SIGNALS: tuple[Signal, ...] = (
    Signal("router_orchestrator", 3, "Dedicated router/orchestrator entry point"),
    Signal("specialist_agents", 2, "Named specialist agents/subagents"),
    Signal("skills_layer", 1, "Reusable local skill layer"),
    Signal("plugin_hooks", 1, "Hook-based runtime guardrails"),
    Signal("workflow_artifacts", 3, "Durable workflow artifact model"),
    Signal("versioned_state", 2, "Versioned state root or namespace"),
    Signal("stable_workflow_identity", 2, "Stable workflow UUID/ULID-like identity"),
    Signal("plan_trust_gate", 3, "Explicit plan trust / open-decision gate"),
    Signal("phase_gating", 3, "Sequential phase cursor / phase-exit gating"),
    Signal("failure_stop", 2, "Explicit stop-on-failure behavior"),
    Signal("skill_precedence", 2, "User/project standards outrank internal patterns"),
    Signal("debug_generalization", 2, "Blast-radius / generalized debug remediation"),
    Signal(
        "fail_closed_verification", 3, "Fail-closed verification and evidence contracts"
    ),
    Signal("replay_harness", 3, "Replay fixtures / deterministic harness checks"),
    Signal("test_suite", 1, "Dedicated tests directory"),
)


SKILL_SIGNALS: tuple[Signal, ...] = (
    Signal("intent_capture", 3, "Captures skill intent before authoring"),
    Signal("trigger_design", 3, "Treats description/triggering as first-class"),
    Signal("eval_loop", 3, "Defines iterative eval and improvement loop"),
    Signal("quant_qual_review", 2, "Includes both quantitative and qualitative review"),
    Signal(
        "benchmark_outputs",
        2,
        "Has explicit benchmark/report schemas or viewer workflow",
    ),
    Signal(
        "skill_packaging",
        2,
        "Teaches structured skill packaging and progressive disclosure",
    ),
)


BAKEOFF_SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        "planner_agreement",
        "Planner does not silently diverge from agreed requirements",
        "The planning layer explicitly surfaces unresolved decisions or spec-compliance checks instead of silently choosing.",
        strong_patterns=(
            "differences_from_agreement",
            "open_decisions",
            "spec compliance verification against user request",
            "binary spec compliance",
        ),
        weak_patterns=("plan review", "spec alignment verification", "checkpoint"),
    ),
    Scenario(
        "plan_blocks_execution",
        "Unresolved plan decisions block execution",
        "Execution should not start when high-impact planning decisions are unresolved.",
        strong_patterns=(
            "blocking fail",
            "open_decisions=[]",
            "missing verification = blocking fail",
            "cannot start build",
        ),
        weak_patterns=("clarification", "recommended default"),
    ),
    Scenario(
        "sequential_execution",
        "Builder does not skip planned order",
        "Execution runs the current approved phase only and does not opportunistically reorder work.",
        strong_patterns=(
            "phase_cursor",
            "phase_exit_gate",
            "execute only the phase",
            "resume only after verification passes",
        ),
        weak_patterns=(
            "bite-sized tasks",
            "execute plan",
            "do not proceed to verification",
        ),
    ),
    Scenario(
        "failure_stop",
        "Failed phase does not continue silently",
        "When proof is missing or a phase fails, the system blocks or stops instead of apologizing later.",
        strong_patterns=(
            "failure_stop_gate",
            "stop immediately",
            "fail closed",
            "blocking fail",
        ),
        weak_patterns=("verification gate", "do not continue", "safe to proceed"),
    ),
    Scenario(
        "memory_persistence",
        "Memory persists on blocking exit",
        "Workflow state and memory should remain recoverable after interruption or blocking stops.",
        strong_patterns=(
            "workflow artifact",
            "resume interrupted",
            "persistent memory across sessions",
            "memory finalization",
        ),
        weak_patterns=("resume", "session state", "artifacts"),
    ),
    Scenario(
        "skill_precedence",
        "Internal pattern guidance does not override explicit user/project standards",
        "Project or user standards must outrank reusable pattern packs or defaults.",
        strong_patterns=(
            "user instructions always take precedence",
            "project-scoped instincts take precedence",
            "skill precedence",
            "outrank explicit user requirements",
        ),
        weak_patterns=("takes precedence", "user/project standards"),
    ),
    Scenario(
        "debug_generalization",
        "Debug fixes generalize beyond the reproducing case",
        "The debug workflow searches for nearby duplicates or variants instead of stopping at a one-off patch.",
        strong_patterns=(
            "blast_radius_scan",
            "blast radius",
            "same-file duplicates",
            "variant coverage",
        ),
        weak_patterns=("root cause", "variants"),
    ),
    Scenario(
        "verification_fail_closed",
        "Verification fails closed on missing or contradictory evidence",
        "Success claims require concrete evidence, and contradictory verification is rejected.",
        strong_patterns=(
            "scenario totals must reconcile",
            "expected vs actual",
            "claiming work is complete without verification is dishonesty",
            "missing verification = blocking fail",
        ),
        weak_patterns=(
            "verification-loop",
            "independent verification",
            "verification-before-completion",
        ),
    ),
)


DELTA_RULES: tuple[DeltaRule, ...] = (
    DeltaRule(
        "plugins/cc10x/skills/cc10x-router/SKILL.md",
        "router",
        (
            ("workflow_uuid", "stable workflow identity independent of task ids"),
            ("phase_exit_gate", "sequential phase gating"),
            ("skill_precedence_gate", "explicit instruction precedence enforcement"),
            (".claude/cc10x/v10", "versioned v10 state root"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/planner.md",
        "planner",
        (
            ("OPEN_DECISIONS", "open decisions are first-class"),
            ("DIFFERENCES_FROM_AGREEMENT", "differences from agreement are explicit"),
            ("STATUS=NEEDS_CLARIFICATION", "planner blocks on high-impact ambiguity"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/component-builder.md",
        "builder",
        (
            ("PHASE_STATUS", "phase-level completion reporting"),
            ("PHASE_EXIT_READY", "phase exit evidence gate"),
            (
                "Execute the current approved BUILD phase",
                "sequential execution contract",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/bug-investigator.md",
        "debugger",
        (
            ("BLAST_RADIUS_SCAN", "blast-radius scan is mandatory"),
            ("Variant Coverage", "variant coverage is explicit"),
            (".claude/cc10x/v10", "debug memory reads are versioned"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/integration-verifier.md",
        "verifier",
        (
            (
                'CONTRACT {"s":"PASS","b":false,"cr":0}',
                "verifier emits explicit machine-readable contract envelope",
            ),
            (
                "## Independence Rule",
                "verifier treats upstream approvals as inputs, not proof",
            ),
            (
                "Do not self-load internal CC10X skills",
                "verifier obeys router-owned internal skill precedence",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/code-reviewer.md",
        "reviewer",
        (
            ("REMEDIATION_NEEDED", "review output is structured for router handling"),
            ("REVERT_RECOMMENDED", "review can signal revert-worthy state"),
            (
                "REMEDIATION_SCOPE_REQUESTED",
                "review integrates with scoped remediation",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/agents/silent-failure-hunter.md",
        "hunter",
        (
            (".claude/cc10x/v10", "hunter reads only v10 memory state"),
            (
                "Do not self-load internal CC10X skills",
                "hunter obeys router-owned internal skill precedence",
            ),
            (
                "Coverage truthfulness",
                "hunter must state scan coverage and blind spots",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_hooklib.py",
        "hooks",
        (
            ('STATE_VERSION = "v10"', "hook state root is versioned"),
            ("workflow_uuid", "hooks prefer stable workflow identity"),
            ("state_root", "hook paths centralize v10 state"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_pretooluse_guard.py",
        "hooks",
        (
            ("state_root()", "memory protection is scoped to versioned state"),
            ("v10 memory markdown write", "guard reason is explicit"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_posttooluse_artifact_guard.py",
        "hooks",
        (
            ("workflow_uuid", "artifact guard expects stable ids"),
            ("phase_cursor", "artifact guard validates phase-aware state"),
            ("state_root", "artifact guard validates v10 schema"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_sessionstart_context.py",
        "hooks",
        (
            ("CC10X v10 workflow context", "session context is version-aware"),
            ("phase_cursor", "resume context includes phase cursor"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_task_completed_guard.py",
        "hooks",
        (("REQUIRED_METADATA", "task metadata enforcement remains explicit"),),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_harness_audit.py",
        "harness",
        (
            ("workflow-identity-v10.json", "harness covers workflow identity fixture"),
            ("build-phase-blocked.json", "harness covers blocked phase fixture"),
            ("OPEN_DECISIONS:", "harness validates planner trust fields"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/scripts/cc10x_workflow_replay_check.py",
        "harness",
        (
            ("workflow_uuid", "replay fixtures require stable workflow identity"),
            ("BLAST_RADIUS_SCAN", "replay validates debug generalization"),
            ("PHASE_EXIT_READY", "replay validates phase gating"),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/skills/frontend-patterns/SKILL.md",
        "internal-skill",
        (
            (
                "advisory in v10",
                "frontend patterns are advisory instead of authoritative",
            ),
            (
                "Explicit user instructions",
                "user/project standards outrank style guidance",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/skills/debugging-patterns/SKILL.md",
        "internal-skill",
        (
            (
                "advisory in v10",
                "debugging patterns are advisory instead of authoritative",
            ),
            (
                "same signature nearby",
                "debugging guidance includes nearby duplicate scan",
            ),
        ),
    ),
    DeltaRule(
        "plugins/cc10x/skills/architecture-patterns/SKILL.md",
        "internal-skill",
        (
            (
                "advisory in v10",
                "architecture patterns are advisory instead of authoritative",
            ),
            (
                "approved plan/design doc",
                "approved design outranks architecture heuristics",
            ),
        ),
    ),
    DeltaRule(
        "docs/router-invariants.md",
        "docs",
        (
            (
                "Agents use only the v10 state namespace",
                "v10-only agent state usage is codified",
            ),
            (
                "Verification is independent of upstream approval",
                "verifier independence is codified",
            ),
            (
                "Silent-failure analysis must state scan coverage truthfully",
                "hunter coverage truthfulness is codified",
            ),
        ),
    ),
    DeltaRule(
        "README.md",
        "docs",
        (
            ("What 10.0 adds", "v10 contract is documented"),
            (".claude/cc10x/v10/workflows", "versioned state root is documented"),
            ("Stable workflow UUIDs", "stable identity is documented"),
        ),
    ),
    DeltaRule(
        "CHANGELOG.md",
        "docs",
        (
            ("[10.1.0]", "v10 competition release is documented"),
            ("Trust-first recovery release", "release framing is explicit"),
        ),
    ),
)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def repo_path(name: str) -> Path:
    if name == "cc10x-current":
        return ROOT
    return REF_ROOT / name


def safe_rel(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return str(path)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_text_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in {
            ".md",
            ".json",
            ".py",
            ".txt",
            ".yaml",
            ".yml",
            ".toml",
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
        }:
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
            yield path, load_text(path)
        except OSError:
            continue


def git_head(repo: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], repo).stdout.strip()


def git_branch(repo: Path) -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()


def git_dirty(repo: Path) -> bool:
    return bool(run(["git", "status", "--porcelain"], repo).stdout.strip())


def ensure_ref_repo(entry: RefRepo) -> dict[str, Any]:
    path = repo_path(entry.name)
    result: dict[str, Any] = {
        "repo": entry.name,
        "tier": entry.tier,
        "kind": entry.kind,
        "benchmark_path": entry.benchmark_path,
        "notes": entry.notes,
        "present": path.exists(),
        "refresh_status": "present" if path.exists() else "missing",
    }
    if entry.name == ANTHROPIC_REPO and not path.exists():
        clone = run(["git", "clone", "--depth", "1", ANTHROPIC_REMOTE, str(path)], ROOT)
        result["refresh_status"] = "cloned" if clone.returncode == 0 else "clone_failed"
        result["refresh_detail"] = (
            (clone.stdout + clone.stderr).strip().splitlines()[-1]
            if (clone.stdout + clone.stderr).strip()
            else ""
        )
        result["present"] = path.exists()
    if not path.exists():
        return result

    result["head"] = git_head(path)[:12]
    result["branch"] = git_branch(path)
    result["dirty"] = git_dirty(path)
    result["benchmark_target"] = safe_rel(path / entry.benchmark_path, path)
    return result


def refresh_ref_repo(entry: RefRepo) -> dict[str, Any]:
    result = ensure_ref_repo(entry)
    path = repo_path(entry.name)
    if not path.exists():
        return result
    if entry.name == V7_REPO:
        result["refresh_status"] = "pinned_tag_skip"
        result["refresh_detail"] = V7_TAG
        return result
    if result.get("dirty"):
        result["refresh_status"] = "dirty_skip"
        return result
    upstream = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], path
    )
    if upstream.returncode != 0:
        result["refresh_status"] = "no_upstream_skip"
        result["refresh_detail"] = (
            upstream.stderr.strip().splitlines()[-1]
            if upstream.stderr.strip()
            else "no upstream"
        )
        return result
    pull = run(["git", "pull", "--ff-only"], path)
    result["refresh_status"] = "pulled" if pull.returncode == 0 else "pull_failed"
    detail = (pull.stdout + "\n" + pull.stderr).strip().splitlines()
    result["refresh_detail"] = detail[-1] if detail else ""
    result["head"] = git_head(path)[:12]
    result["branch"] = git_branch(path)
    result["dirty"] = git_dirty(path)
    return result


def inventory_entries(refresh: bool) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for entry in REF_REPOS:
        payload = refresh_ref_repo(entry) if refresh else ensure_ref_repo(entry)
        if payload.get("present"):
            if entry.tier == "S":
                payload["benchmark_status"] = "skill_benchmark"
            elif entry.name in DEEP_BAKEOFF_TARGETS:
                payload["benchmark_status"] = "deep_bakeoff"
            else:
                payload["benchmark_status"] = "structural_only"
        else:
            payload["benchmark_status"] = "missing"
        entries.append(payload)
    entries.sort(key=lambda row: (row["tier"], row["repo"]))
    return entries


def detect_harness_signals(repo: Path) -> dict[str, bool]:
    hits = {signal.key: False for signal in STRUCTURAL_SIGNALS}
    corpus = []
    for path, text in iter_text_files(repo):
        corpus.append(f"{safe_rel(path, repo)}\n{text}")
    blob = "\n".join(corpus)
    lower = blob.lower()

    hits["router_orchestrator"] = any(
        x in lower
        for x in (
            "cc10x-router",
            "orchestrator",
            "router owns orchestration",
            "swarm-coordinator",
        )
    )
    hits["specialist_agents"] = any(
        x in lower for x in ("subagents", "specialist agents", "agents/", "agent:")
    )
    hits["skills_layer"] = "/skills/" in blob or "skills:" in lower
    hits["plugin_hooks"] = any(
        x in lower for x in ("pretooluse", "taskcompleted", "hooks.json", '"hooks"')
    )
    hits["workflow_artifacts"] = any(
        x in lower
        for x in ("workflows/", "artifacts", "run artifacts", "transcript capture")
    )
    hits["versioned_state"] = (
        ".claude/cc10x/v10" in blob or "state_root" in lower or "runs-dir" in lower
    )
    hits["stable_workflow_identity"] = any(
        x in lower
        for x in ("workflow_uuid", "session_id", "replaycursor", "sequential step ids")
    )
    hits["plan_trust_gate"] = any(
        x in lower
        for x in (
            "open_decisions",
            "differences_from_agreement",
            "plan_trust_gate",
            "spec compliance",
        )
    )
    hits["phase_gating"] = any(
        x in lower
        for x in (
            "phase_cursor",
            "phase_exit_gate",
            "execute only the phase",
            "resume only after verification passes",
        )
    )
    hits["failure_stop"] = any(
        x in lower
        for x in (
            "failure_stop_gate",
            "stop immediately",
            "fail closed",
            "blocking fail",
        )
    )
    hits["skill_precedence"] = any(
        x in lower
        for x in (
            "user instructions always take precedence",
            "project-scoped instincts take precedence",
            "outrank explicit user requirements",
            "precedence",
        )
    )
    hits["debug_generalization"] = any(
        x in lower
        for x in (
            "blast_radius_scan",
            "blast radius",
            "same-file duplicates",
            "variant coverage",
        )
    )
    hits["fail_closed_verification"] = any(
        x in lower
        for x in (
            "expected vs actual",
            "scenarios_total",
            "verification-before-completion",
            "blocking fail",
            "convergence_state",
        )
    )
    hits["replay_harness"] = any(
        x in lower
        for x in (
            "workflow_replay_check",
            "fixtures",
            "replay",
            "e2e orchestration tests",
            "harness_audit",
        )
    )
    hits["test_suite"] = (repo / "tests").exists() or (
        repo / "plugins" / "cc10x" / "tests"
    ).exists()
    return hits


def detect_skill_signals(skill_root: Path) -> dict[str, bool]:
    hits = {signal.key: False for signal in SKILL_SIGNALS}
    blob = ""
    for path, text in iter_text_files(skill_root):
        blob += f"\n{safe_rel(path, skill_root)}\n{text}"
    lower = blob.lower()
    hits["intent_capture"] = (
        "capture intent" in lower or "understanding the user's intent" in lower
    )
    hits["trigger_design"] = "trigger" in lower and "description" in lower
    hits["eval_loop"] = (
        "create a few test prompts" in lower
        or "running and evaluating test cases" in lower
    )
    hits["quant_qual_review"] = "qualitatively and quantitatively" in lower or (
        "benchmark" in lower and "feedback" in lower
    )
    hits["benchmark_outputs"] = "benchmark.json" in lower or "eval-viewer" in lower
    hits["skill_packaging"] = (
        "progressive disclosure" in lower or "skill-name/" in lower
    )
    return hits


def score(signals: dict[str, bool], catalog: tuple[Signal, ...]) -> tuple[int, int]:
    earned = sum(sig.weight for sig in catalog if signals[sig.key])
    total = sum(sig.weight for sig in catalog)
    return earned, total


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def find_evidence(text: str, needles: tuple[str, ...]) -> dict[str, Any] | None:
    lower_lines = text.lower().splitlines()
    lines = text.splitlines()
    for needle in needles:
        needle_lower = needle.lower()
        for idx, line in enumerate(lower_lines, start=1):
            if needle_lower in line:
                return {
                    "line": idx,
                    "needle": needle,
                    "snippet": lines[idx - 1].strip(),
                }
    return None


def build_inventory(entries: list[dict[str, Any]]) -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / f"{TODAY}-reference-inventory.json"
    md_path = OUT_DIR / f"{TODAY}-reference-inventory.md"
    write_json(
        json_path,
        {
            "date": TODAY,
            "benchmark_root": safe_rel(REF_ROOT, ROOT),
            "entries": entries,
        },
    )

    lines = [
        "# Reference Inventory",
        "",
        f"Date: {TODAY}",
        "",
        "| Repo | Tier | Kind | HEAD | State | Refresh | Benchmark Status | Benchmark Target |",
        "|------|------|------|------|-------|---------|------------------|------------------|",
    ]
    for entry in entries:
        state = "dirty" if entry.get("dirty") else "clean"
        head = f"`{entry.get('head', 'missing')}`"
        lines.append(
            f"| {entry['repo']} | {entry['tier']} | {entry['kind']} | {head} | {state} | {entry.get('refresh_status', 'n/a')} | {entry.get('benchmark_status', 'unknown')} | `{entry.get('benchmark_target', entry.get('benchmark_path', '.'))}` |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def diff_names() -> list[str]:
    return [
        line
        for line in run(
            ["git", "diff", "--name-only", f"{V7_TAG}..HEAD"], ROOT
        ).stdout.splitlines()
        if line
    ]


def supporting_or_noncritical(
    paths: list[str], critical: set[str]
) -> dict[str, list[str]]:
    supporting = []
    noncritical = []
    for path in paths:
        if path in critical:
            continue
        if (
            path.startswith("docs/")
            or path.endswith(".json")
            or path in {"README.md", "CHANGELOG.md"}
        ):
            supporting.append(path)
        else:
            noncritical.append(path)
    return {"supporting": supporting, "noncritical": noncritical}


def v7_file_text(path: str) -> str:
    proc = run(["git", "show", f"{V7_TAG}:{path}"], ROOT)
    return proc.stdout if proc.returncode == 0 else ""


def build_delta_register() -> tuple[Path, Path, list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    changed = set(diff_names())
    critical_paths = {rule.path for rule in DELTA_RULES}
    partition = supporting_or_noncritical(sorted(changed), critical_paths)

    for rule in DELTA_RULES:
        current_path = ROOT / rule.path
        current_text = load_text(current_path) if current_path.exists() else ""
        baseline_text = v7_file_text(rule.path)
        deltas = []
        current_hits = []
        baseline_hits = []
        for needle, description in rule.feature_needles:
            current_evidence = find_evidence(current_text, (needle,))
            baseline_evidence = (
                find_evidence(baseline_text, (needle,)) if baseline_text else None
            )
            if current_evidence:
                current_hits.append({"needle": needle, **current_evidence})
            if baseline_evidence:
                baseline_hits.append({"needle": needle, **baseline_evidence})
            if current_evidence and not baseline_evidence:
                deltas.append(description)

        if deltas:
            verdict = "better"
        elif current_hits and baseline_hits:
            verdict = "unclear"
        elif current_hits and not baseline_text:
            verdict = "better"
        else:
            verdict = "unclear"

        entries.append(
            {
                "path": rule.path,
                "category": rule.category,
                "changed_since_v7": rule.path in changed,
                "verdict": verdict,
                "delta_summary": deltas
                or ["No clear trust-contract improvement detected automatically."],
                "current_evidence": current_hits,
                "v7_evidence": baseline_hits,
            }
        )

    json_path = OUT_DIR / f"{TODAY}-v7-delta-register.json"
    md_path = OUT_DIR / f"{TODAY}-v7-delta-register.md"
    payload = {
        "baseline_tag": V7_TAG,
        "critical_files_reviewed": len(entries),
        "partition": {
            "critical": sorted(critical_paths),
            "supporting": partition["supporting"],
            "noncritical": partition["noncritical"],
        },
        "entries": entries,
    }
    write_json(json_path, payload)

    lines = [
        "# V7 Delta Register",
        "",
        f"Baseline: `{V7_TAG}`",
        "",
        f"- Critical files reviewed: `{len(entries)}`",
        f"- Supporting changed files: `{len(partition['supporting'])}`",
        f"- Non-critical changed files: `{len(partition['noncritical'])}`",
        "",
        "| Path | Category | Verdict | Delta Summary |",
        "|------|----------|---------|---------------|",
    ]
    for entry in entries:
        summary = "; ".join(entry["delta_summary"])
        lines.append(
            f"| `{entry['path']}` | {entry['category']} | {entry['verdict']} | {summary} |"
        )
    lines.append("")
    lines.append("## Backlog Seed")
    lines.append("")
    for entry in entries:
        if entry["verdict"] != "better":
            lines.append(
                f"- `{entry['path']}`: {entry['verdict']} — review manually and decide whether to improve or keep as-is."
            )
    lines.append("")
    lines.append("## Evidence Notes")
    lines.append("")
    for entry in entries:
        lines.append(f"### `{entry['path']}`")
        current = entry["current_evidence"][0] if entry["current_evidence"] else None
        baseline = entry["v7_evidence"][0] if entry["v7_evidence"] else None
        if current:
            lines.append(
                f"- Current: line {current['line']} matches `{current['needle']}` -> `{current['snippet']}`"
            )
        else:
            lines.append("- Current: no automatic evidence match")
        if baseline:
            lines.append(
                f"- `{V7_TAG}`: line {baseline['line']} matches `{baseline['needle']}` -> `{baseline['snippet']}`"
            )
        else:
            lines.append(f"- `{V7_TAG}`: no matching baseline evidence")
        lines.append("")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path, entries


def build_structural_benchmark(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    current_signals = detect_harness_signals(ROOT)
    current_score, current_max = score(current_signals, STRUCTURAL_SIGNALS)
    rows.append(
        {
            "repo": "cc10x-current",
            "tier": "A",
            "kind": "harness",
            "head": git_head(ROOT)[:12],
            "score": current_score,
            "max_score": current_max,
            "signals": current_signals,
        }
    )

    for entry in entries:
        repo = repo_path(entry["repo"])
        if not repo.exists():
            continue
        benchmark_root = (
            repo / entry["benchmark_path"] if entry["kind"] == "skill-library" else repo
        )
        if entry["tier"] == "S":
            signals = detect_skill_signals(benchmark_root)
            earned, total = score(signals, SKILL_SIGNALS)
        else:
            signals = detect_harness_signals(benchmark_root)
            earned, total = score(signals, STRUCTURAL_SIGNALS)
        rows.append(
            {
                "repo": entry["repo"],
                "tier": entry["tier"],
                "kind": entry["kind"],
                "head": entry.get("head", "missing"),
                "score": earned,
                "max_score": total,
                "signals": signals,
            }
        )

    rows.sort(key=lambda row: (-row["score"], row["repo"]))
    return rows


def repo_documents(repo: Path) -> list[dict[str, str]]:
    docs = []
    for path, text in iter_text_files(repo):
        rel_parts = path.relative_to(repo).parts
        if not rel_parts:
            continue
        first = rel_parts[0]
        if first not in BAKEOFF_TOPLEVEL:
            continue
        rel_path = "/".join(rel_parts)
        is_core = any(part in BAKEOFF_CORE_DIRS for part in rel_parts)
        if first in {"docs", ".claude"} and len(rel_parts) > 3 and not is_core:
            continue
        if first == "plugins" and len(rel_parts) > 5 and not is_core:
            continue
        if (
            first in {"docs", "plugins", ".claude"}
            and path.name
            not in {
                "README.md",
                "CLAUDE.md",
                "AGENTS.md",
                "CHANGELOG.md",
                "hooks.json",
                "plugin.json",
                "marketplace.json",
                "SKILL.md",
            }
            and not is_core
            and not any(
                token in rel_path.lower()
                for token in (
                    "plan",
                    "spec",
                    "guide",
                    "usage",
                    "plugin",
                    "hook",
                    "verify",
                )
            )
        ):
            continue
        priority = (
            0
            if is_core
            else (
                1
                if first in {"README.md", "CLAUDE.md", "AGENTS.md", "CHANGELOG.md"}
                else 2
            )
        )
        docs.append(
            {"path": safe_rel(path, repo), "text": text, "priority": str(priority)}
        )
    docs.sort(key=lambda item: (item["priority"], item["path"]))
    return [{"path": item["path"], "text": item["text"]} for item in docs]


def find_evidence_in_documents(
    documents: list[dict[str, str]], needles: tuple[str, ...]
) -> dict[str, Any] | None:
    for document in documents:
        evidence = find_evidence(document["text"], needles)
        if evidence:
            return {"file": document["path"], **evidence}
    return None


def evaluate_scenario(
    documents: list[dict[str, str]], scenario: Scenario
) -> dict[str, Any]:
    strong = find_evidence_in_documents(documents, scenario.strong_patterns)
    weak = (
        find_evidence_in_documents(documents, scenario.weak_patterns)
        if scenario.weak_patterns
        else None
    )
    if strong:
        verdict = "pass"
        observed = strong["snippet"]
        evidence = strong
    elif weak:
        verdict = "partial"
        observed = weak["snippet"]
        evidence = weak
    else:
        verdict = "not-testable"
        observed = "No direct repository evidence found for this scenario."
        evidence = None
    return {
        "scenario": scenario.title,
        "expected": scenario.expected,
        "observed": observed,
        "verdict": verdict,
        "evidence_source": (
            f"{evidence['file']}:{evidence['line']}" if evidence else None
        ),
        "evidence": evidence,
    }


def build_bakeoff() -> tuple[Path, Path, list[dict[str, Any]]]:
    targets = [
        ("cc10x-current", ROOT, "A"),
        (V7_REPO, repo_path(V7_REPO), "A"),
        ("claude-code-harness", repo_path("claude-code-harness"), "A"),
        ("claude-harness", repo_path("claude-harness"), "A"),
        ("everything-claude-code", repo_path("everything-claude-code"), "A"),
        ("babysitter", repo_path("babysitter"), "A"),
        ("metaswarm", repo_path("metaswarm"), "A"),
        ("superpowers", repo_path("superpowers"), "A"),
    ]

    results: list[dict[str, Any]] = []
    for name, path, tier in targets:
        if not path.exists():
            continue
        documents = repo_documents(path)
        repo_results: list[dict[str, Any]] = []
        for scenario in BAKEOFF_SCENARIOS:
            repo_results.append(evaluate_scenario(documents, scenario))
        results.append({"repo": name, "tier": tier, "scenarios": repo_results})

    json_path = OUT_DIR / f"{TODAY}-behavior-bakeoff.json"
    md_path = OUT_DIR / f"{TODAY}-behavior-bakeoff.md"
    write_json(json_path, {"date": TODAY, "repos": results})

    lines = [
        "# Behavior Bakeoff",
        "",
        f"Date: {TODAY}",
        "",
        "Behavior bakeoffs are evidence-driven and conservative. Missing direct evidence is recorded as `not-testable`, not guessed.",
        "",
    ]
    for repo_result in results:
        lines.append(f"## {repo_result['repo']}")
        lines.append("")
        lines.append(
            "| Scenario | Expected Behavior | Observed Behavior | Evidence Source | Verdict |"
        )
        lines.append(
            "|----------|-------------------|-------------------|-----------------|---------|"
        )
        for scenario in repo_result["scenarios"]:
            source = (
                f"`{scenario['evidence_source']}`"
                if scenario["evidence_source"]
                else "None"
            )
            lines.append(
                f"| {scenario['scenario']} | {scenario['expected']} | `{scenario['observed']}` | {source} | {scenario['verdict']} |"
            )
        lines.append("")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path, results


def verdict_score(verdict: str) -> int:
    return {"pass": 3, "partial": 2, "not-testable": 1, "fail": 0}.get(verdict, 0)


def build_claim_scoreboard(
    rows: list[dict[str, Any]], bakeoff_results: list[dict[str, Any]]
) -> dict[str, list[str]]:
    bakeoff_map = {entry["repo"]: entry["scenarios"] for entry in bakeoff_results}
    current_scenarios = {
        item["scenario"]: item for item in bakeoff_map.get("cc10x-current", [])
    }
    stronger = []
    tied = []
    unproven = []

    for row in rows:
        repo = row["repo"]
        if repo == "cc10x-current":
            continue
        if repo not in DEEP_BAKEOFF_TARGETS:
            unproven.append(repo)
            continue
        comparison = bakeoff_map.get(repo, [])
        if not comparison:
            unproven.append(repo)
            continue
        repo_scenarios = {item["scenario"]: item for item in comparison}
        current_better = False
        repo_better = False
        all_equal = True
        for scenario_name, current in current_scenarios.items():
            other = repo_scenarios.get(scenario_name)
            if not other:
                repo_better = True
                all_equal = False
                continue
            current_value = verdict_score(current["verdict"])
            other_value = verdict_score(other["verdict"])
            if current_value > other_value:
                current_better = True
                all_equal = False
            elif current_value < other_value:
                repo_better = True
                all_equal = False
        if current_better and not repo_better:
            stronger.append(repo)
        elif all_equal:
            tied.append(repo)
        else:
            unproven.append(repo)

    return {
        "stronger_by_evidence": sorted(stronger),
        "tied_or_not_differentiated": sorted(tied),
        "unproven": sorted(unproven),
    }


def write_structural_benchmark(
    rows: list[dict[str, Any]], claim_scoreboard: dict[str, list[str]]
) -> tuple[Path, Path]:
    json_path = OUT_DIR / f"{TODAY}-reference-benchmark.json"
    md_path = OUT_DIR / f"{TODAY}-reference-benchmark.md"
    payload = {
        "date": TODAY,
        "rubric": "tiered",
        "notes": [
            "Tier S uses a skill-authoring rubric, not the harness rubric.",
            "Structural leads do not automatically imply product superiority.",
        ],
        "claim_scoreboard": claim_scoreboard,
        "rows": rows,
    }
    write_json(json_path, payload)

    lines = [
        "# Reference Benchmark",
        "",
        f"Date: {TODAY}",
        "",
        "This is a tiered structural benchmark. Tier S uses a skill-authoring rubric, not the harness rubric.",
        "",
        "| Repo | Tier | Kind | HEAD | Score |",
        "|------|------|------|------|-------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['repo']} | {row['tier']} | {row['kind']} | `{row['head']}` | {row['score']}/{row['max_score']} |"
        )
    lines.append("")
    lines.append("## Claim Scoreboard")
    lines.append("")
    lines.append(
        f"- Stronger by evidence: `{', '.join(claim_scoreboard['stronger_by_evidence']) if claim_scoreboard['stronger_by_evidence'] else 'None'}`"
    )
    lines.append(
        f"- Tied / not differentiated: `{', '.join(claim_scoreboard['tied_or_not_differentiated']) if claim_scoreboard['tied_or_not_differentiated'] else 'None'}`"
    )
    lines.append(
        f"- Unproven: `{', '.join(claim_scoreboard['unproven']) if claim_scoreboard['unproven'] else 'None'}`"
    )
    lines.append("")
    lines.append("## Claim Discipline")
    lines.append("")
    lines.append(
        "- Structural score alone is not enough for a universal superiority claim."
    )
    lines.append(
        "- `Stronger by evidence` is reserved for deep-bakeoff targets where CC10X never scores below the reference on the tested trust scenarios."
    )
    lines.append(
        "- `Unproven` includes mixed or insufficient evidence, even if the structural score is higher."
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def build_roadmap(
    delta_entries: list[dict[str, Any]], bakeoff_results: list[dict[str, Any]]
) -> Path:
    backlog = []
    for entry in delta_entries:
        if entry["verdict"] != "better":
            backlog.append(
                {
                    "priority": "high",
                    "source": "v7-delta",
                    "item": entry["path"],
                    "reason": entry["verdict"],
                }
            )
    for repo_result in bakeoff_results:
        if repo_result["repo"] == "cc10x-current":
            continue
        for scenario in repo_result["scenarios"]:
            if scenario["verdict"] in {"pass"}:
                continue
            backlog.append(
                {
                    "priority": (
                        "medium" if scenario["verdict"] == "partial" else "high"
                    ),
                    "source": repo_result["repo"],
                    "item": scenario["scenario"],
                    "reason": scenario["verdict"],
                }
            )

    claim_lines = [
        "# Benchmark Roadmap",
        "",
        f"Date: {TODAY}",
        "",
        "## What CC10X Can Prove Today",
        "",
        "- CC10X is structurally stronger than stable `v7.7.0` and the pulled reference set on the selected trust-harness rubric.",
        "- CC10X can prove explicit machinery for workflow identity, phase gating, skill precedence, fail-closed verification, and replay-backed validation.",
        "",
        "## What Is Still Not Proven",
        "",
        "- Universal superiority over every reference repo in real execution behavior.",
        "- Full apples-to-apples behavior proof for prompt libraries and skill libraries that are not orchestrators.",
        "- A legitimate `100% better` claim across all scenarios and repos.",
        "",
        "## Prioritized Backlog",
        "",
    ]
    for item in backlog:
        claim_lines.append(
            f"- [{item['priority']}] `{item['source']}` → `{item['item']}` ({item['reason']})"
        )
    path = OUT_DIR / f"{TODAY}-benchmark-roadmap.md"
    path.write_text("\n".join(claim_lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="CC10X world-class benchmark suite")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh clean ref repos with pull --ff-only",
    )
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = inventory_entries(refresh=args.refresh)
    inventory_json, inventory_md = build_inventory(inventory)
    delta_json, delta_md, delta_entries = build_delta_register()
    bakeoff_json, bakeoff_md, bakeoff_results = build_bakeoff()
    benchmark_rows = build_structural_benchmark(inventory)
    claim_scoreboard = build_claim_scoreboard(benchmark_rows, bakeoff_results)
    benchmark_json, benchmark_md = write_structural_benchmark(
        benchmark_rows, claim_scoreboard
    )
    roadmap_md = build_roadmap(delta_entries, bakeoff_results)

    summary = {
        "inventory_json": safe_rel(inventory_json, ROOT),
        "inventory_md": safe_rel(inventory_md, ROOT),
        "delta_json": safe_rel(delta_json, ROOT),
        "delta_md": safe_rel(delta_md, ROOT),
        "benchmark_json": safe_rel(benchmark_json, ROOT),
        "benchmark_md": safe_rel(benchmark_md, ROOT),
        "bakeoff_json": safe_rel(bakeoff_json, ROOT),
        "bakeoff_md": safe_rel(bakeoff_md, ROOT),
        "roadmap_md": safe_rel(roadmap_md, ROOT),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
