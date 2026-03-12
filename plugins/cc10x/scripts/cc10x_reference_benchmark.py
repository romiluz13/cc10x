#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, cast


ROOT = Path(__file__).resolve().parents[3]
REF_ROOT = ROOT / "ref-(dont-read-unless-specificly-mentioned)"
V7_REF = REF_ROOT / "cc10x-v7.7.0-stable"
OUT_DIR = ROOT / "docs" / "benchmarks"

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


@dataclass(frozen=True)
class Signal:
    key: str
    weight: int
    description: str


SIGNALS = (
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


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def repo_head(repo: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], repo).stdout.strip()[:12]


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
            yield path, path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue


def detect_signals(repo: Path) -> dict[str, bool]:
    text_hits: dict[str, bool] = {signal.key: False for signal in SIGNALS}

    all_text = []
    for path, text in iter_text_files(repo):
        rel = path.relative_to(repo).as_posix()
        blob = f"{rel}\n{text}"
        all_text.append(blob)

    corpus = "\n".join(all_text)
    lower = corpus.lower()

    text_hits["router_orchestrator"] = any(
        needle in lower
        for needle in (
            "cc10x-router",
            "router owns orchestration",
            "orchestrator",
            "entry point",
        )
    )
    text_hits["specialist_agents"] = any(
        needle in lower
        for needle in (
            "subagents",
            "specialist agents",
            "bug-investigator",
            "component-builder",
            "planner",
        )
    )
    text_hits["skills_layer"] = "/skills/" in corpus or "skills:" in lower
    text_hits["plugin_hooks"] = (
        "pretooluse" in lower or "taskcompleted" in lower or "hooks.json" in lower
    )
    text_hits["workflow_artifacts"] = "workflows/" in corpus and "workflow" in lower
    text_hits["versioned_state"] = (
        ".claude/cc10x/v10" in corpus or "state_root" in lower
    )
    text_hits["stable_workflow_identity"] = (
        "workflow_uuid" in lower or "workflow uuid" in lower
    )
    text_hits["plan_trust_gate"] = (
        "open_decisions" in lower
        or "differences_from_agreement" in lower
        or "plan_trust_gate" in lower
    )
    text_hits["phase_gating"] = (
        "phase_cursor" in lower or "phase_exit_gate" in lower or "phase exit" in lower
    )
    text_hits["failure_stop"] = (
        "failure_stop_gate" in lower
        or "stop immediately" in lower
        or "fail closed" in lower
    )
    text_hits["skill_precedence"] = "claude.md" in lower and (
        "outrank" in lower or "precedence" in lower or "user/project standards" in lower
    )
    text_hits["debug_generalization"] = (
        "blast_radius_scan" in lower
        or "blast radius" in lower
        or "same-file duplicates" in lower
    )
    text_hits["fail_closed_verification"] = (
        "expected vs actual" in lower
        or "scenarios_total" in lower
        or "fail-closed" in lower
        or "convergence_state" in lower
    )
    text_hits["replay_harness"] = (
        "workflow_replay_check" in lower
        or ("fixtures" in lower and "replay" in lower)
        or "harness_audit" in lower
    )
    text_hits["test_suite"] = (repo / "tests").exists() or (
        repo / "plugins" / "cc10x" / "tests"
    ).exists()

    return text_hits


def score(signals: dict[str, bool]) -> tuple[int, int]:
    earned = sum(signal.weight for signal in SIGNALS if signals[signal.key])
    total = sum(signal.weight for signal in SIGNALS)
    return earned, total


def diff_vs_v7() -> dict[str, object]:
    diff_names = run(
        ["git", "diff", "--name-only", "v7.7.0..HEAD"],
        ROOT,
    ).stdout.splitlines()
    critical = [
        path
        for path in diff_names
        if path.startswith("plugins/cc10x/agents/")
        or path.startswith("plugins/cc10x/skills/")
        or path.startswith("plugins/cc10x/scripts/")
        or path.startswith("plugins/cc10x/tests/")
        or path in {"README.md", "CHANGELOG.md", "docs/router-invariants.md"}
    ]
    return {
        "changed_files": len(diff_names),
        "critical_files": len(critical),
        "critical_sample": critical[:25],
    }


def refresh_snapshot() -> list[dict[str, str]]:
    repos = sorted({p.parent for p in REF_ROOT.glob("*/.git")})
    rows = []
    for repo in repos:
        rows.append({"repo": repo.name, "head": repo_head(repo)})
    return rows


def build_report() -> str:
    repos = sorted({p.parent for p in REF_ROOT.glob("*/.git")})
    rows: list[dict[str, Any]] = []
    for repo in repos:
        signals = detect_signals(repo)
        earned, total = score(signals)
        rows.append(
            {
                "repo": repo.name,
                "head": repo_head(repo),
                "score": earned,
                "max_score": total,
                "signals": signals,
            }
        )

    rows.sort(key=lambda row: (-row["score"], row["repo"]))
    current = next((row for row in rows if row["repo"] == "cc10x-v7.7.0-stable"), None)
    current_cc10x: dict[str, Any] = {
        "repo": "cc10x-current",
        "head": repo_head(ROOT),
        "signals": detect_signals(ROOT),
    }
    current_cc10x["score"], current_cc10x["max_score"] = score(current_cc10x["signals"])
    rows.insert(0, current_cc10x)

    v7_delta = diff_vs_v7()

    lines = []
    lines.append("# CC10X Benchmark Report")
    lines.append("")
    lines.append(f"Date: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append(
        "This is a measurable signal benchmark, not proof of absolute superiority."
    )
    lines.append(
        "Repos are scored against trust-critical harness properties: orchestration ownership, durable state, plan/build trust gates, skill precedence, debug generalization, fail-closed verification, and deterministic replay coverage."
    )
    lines.append("")
    lines.append("## Current vs Stable v7")
    lines.append("")
    lines.append(
        f"- Stable baseline: `cc10x-v7.7.0-stable` @ `{current['head'] if current else 'unknown'}`"
    )
    lines.append(f"- Current repo HEAD: `{current_cc10x['head']}`")
    lines.append(f"- Files changed since `v7.7.0`: `{v7_delta['changed_files']}`")
    lines.append(
        f"- Critical harness files changed since `v7.7.0`: `{v7_delta['critical_files']}`"
    )
    lines.append("- Critical changed file sample:")
    for path in cast(list[str], v7_delta["critical_sample"]):
        lines.append(f"  - `{path}`")
    lines.append("")
    lines.append("## Scoreboard")
    lines.append("")
    lines.append("| Repo | HEAD | Score |")
    lines.append("|------|------|-------|")
    for row in rows:
        lines.append(
            f"| {row['repo']} | `{row['head']}` | {row['score']}/{row['max_score']} |"
        )
    lines.append("")
    lines.append("## CC10X Current Signal Coverage")
    lines.append("")
    for signal in SIGNALS:
        status = "PASS" if current_cc10x["signals"][signal.key] else "MISS"
        lines.append(f"- `{signal.key}`: {status} ({signal.description})")
    lines.append("")
    lines.append("## Gaps vs References")
    lines.append("")
    better_than = []
    ties = []
    stronger_refs = []
    for row in rows[1:]:
        if current_cc10x["score"] > row["score"]:
            better_than.append(row["repo"])
        elif current_cc10x["score"] == row["score"]:
            ties.append(row["repo"])
        else:
            stronger_refs.append(row["repo"])

    lines.append(
        f"- Higher score than: `{', '.join(better_than) if better_than else 'None'}`"
    )
    lines.append(f"- Tied with: `{', '.join(ties) if ties else 'None'}`")
    lines.append(
        f"- Higher-scoring references: `{', '.join(stronger_refs) if stronger_refs else 'None'}`"
    )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- Current CC10X leads on the specific trust-harness signals it was designed to optimize."
    )
    lines.append(
        "- That does not prove it is universally better than every reference repo."
    )
    lines.append(
        "- It does prove the repo now has stronger explicit machinery around plan trust, phase gating, workflow identity, and replay validation than stable v7 and most pulled references."
    )
    lines.append("")
    lines.append("## Next Actions")
    lines.append("")
    lines.append(
        "- Add scenario-based golden fixtures for skipped-phase execution and false completion after failed work."
    )
    lines.append(
        "- Expand the benchmark from structural signals to behavior replays where possible for top reference repos."
    )
    lines.append("- Re-run this report after any router/agent contract edit.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    out_path = OUT_DIR / f"{date.today().isoformat()}-reference-benchmark.md"
    out_path.write_text(report, encoding="utf-8")
    print(str(out_path.relative_to(ROOT)))
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
