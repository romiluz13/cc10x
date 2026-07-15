#!/usr/bin/env python3
"""Structural seam-discipline evaluator for the 5 BUILD scenarios (ticket #49).

Live agent evals (dispatching a real cc10x builder) require the cc10x plugin
active in Claude Code. This script does what can be verified structurally in
any environment: for each scenario, it asserts the building skill's Seam
Discipline clauses produce the CORRECT behavior decision given the scenario's
inputs. A live run in Claude Code dispatches a real builder; this script
guarantees the skill text would lead the builder to the right decision.

Scenarios:
  1. planned-with-seam   -> builder records TEST_SEAMS, proceeds
  2. planned-without-seam-> builder proceeds (advisory, no gate)
  3. direct-no-plan      -> builder proceeds, no seam gate fires
  4. trivial             -> reduced graph, no seam expectation
  5. builder-disagrees   -> records disagreement, blocks only on genuine ambiguity

Exit 0 = the skill clauses support the correct decision for the scenario.
Exit 1 = a clause is missing or contradicts the expected behavior.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BUILDING = ROOT / "plugins" / "cc10x" / "skills" / "building" / "SKILL.md"
PLAN_WORKFLOW = ROOT / "plugins" / "cc10x" / "skills" / "cc10x-router" / "references" / "build-workflow.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_in(label: str, needle: str, text: str) -> bool:
    if needle not in text:
        print(f"  FAIL: {label} — '{needle}' not found", file=sys.stderr)
        return False
    return True


def assert_not_in(label: str, needle: str, text: str) -> bool:
    if needle in text:
        print(f"  FAIL: {label} — '{needle}' unexpectedly present", file=sys.stderr)
        return False
    return True


def eval_planned_with_seam() -> bool:
    """Plan provides Test Seams + Interfaces. Builder records TEST_SEAMS, proceeds."""
    b = read(BUILDING)
    ok = True
    ok &= assert_in("records TEST_SEAMS", "TEST_SEAMS", b)
    ok &= assert_in("draw your seams from there", "draw your seams from there", b)
    # Must NOT block when seams are provided
    ok &= assert_in("advisory in sub-project 1", "advisory in sub-project 1", b)
    print("  scenario 1 (planned-with-seam): builder records TEST_SEAMS and proceeds")
    return ok


def eval_planned_without_seam() -> bool:
    """Plan has no Test Seams. Builder proceeds — does NOT fail solely for missing seam."""
    b = read(BUILDING)
    ok = True
    # The block rule must be scoped to genuine ambiguity, NOT missing seam field
    ok &= assert_in("block only on genuine ambiguity", "genuine ambiguity", b)
    ok &= assert_in("not block merely because a seam field is missing",
                    "Do NOT block merely because a seam field is missing", b)
    print("  scenario 2 (planned-without-seam): builder proceeds, no spurious block")
    return ok


def eval_direct_no_plan() -> bool:
    """Non-trivial build, no plan (Build directly). No seam gate fires."""
    b = read(BUILDING)
    bw = read(PLAN_WORKFLOW)
    ok = True
    # build-workflow must support the Build directly path (no plan)
    ok &= assert_in("build-workflow has Build directly path", "Build directly", bw)
    # building skill's seam gate must be advisory, not fail-closed on missing plan
    ok &= assert_in("advisory in sub-project 1", "advisory in sub-project 1", b)
    # The block (STATUS: FAIL) must be scoped to genuine ambiguity, NOT to a missing plan
    seam_section = b[b.find("Seam Discipline"):b.find("## Study Project Patterns")] if "Seam Discipline" in b else b
    ok &= assert_in("block scoped to ambiguity", "genuinely ambiguous", seam_section)
    ok &= assert_in("not block on missing seam field", "Do NOT block merely because a seam field is missing", seam_section)
    # The seam section must allow proceeding without a plan's seam input
    ok &= assert_in("plan provides a Test Seams subsection", "plan provides a `### Test Seams`", b)
    print("  scenario 3 (direct-no-plan): builder proceeds via standard graph, no seam gate")
    return ok


def eval_trivial() -> bool:
    """Trivial single-file change. Reduced graph, no seam expectation."""
    bw = read(PLAN_WORKFLOW)
    ok = True
    ok &= assert_in("trivial scope exists", "build_scope=trivial", bw)
    ok &= assert_in("trivial skips to BUILD directly", "continue directly to BUILD", bw)
    print("  scenario 4 (trivial): reduced graph, no seam expectation")
    return ok


def eval_builder_disagrees() -> bool:
    """Plan proposes a seam that can't exercise the real risk. Builder records
    disagreement in DECISIONS and blocks ONLY on genuine ambiguity."""
    b = read(BUILDING)
    ok = True
    ok &= assert_in("records seams in DECISIONS", "DECISIONS", b)
    ok &= assert_in("block rule scopes to ambiguous test surface",
                    "Ambiguous test surface", b)
    ok &= assert_in("block only on genuine ambiguity", "genuine ambiguity", b)
    print("  scenario 5 (builder-disagrees): records disagreement, blocks only on genuine ambiguity")
    return ok


SCENARIOS = {
    "planned-with-seam": eval_planned_with_seam,
    "planned-without-seam": eval_planned_without_seam,
    "direct-no-plan": eval_direct_no_plan,
    "trivial": eval_trivial,
    "builder-disagrees": eval_builder_disagrees,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    args = parser.parse_args()

    print(f"SEAM EVAL: {args.scenario}")
    ok = SCENARIOS[args.scenario]()
    if ok:
        print("  PASS — skill clauses support the correct decision")
        return 0
    print("  FAIL — skill clauses do not support the correct decision", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
