#!/usr/bin/env python3
"""Static prompt-clause assertions for cc10x skill bodies.

The router-contract fixtures (tests/fixtures/*.json + workflow_replay_check.py)
validate contract-envelope SHAPE, not skill CONTENT. This script greps each
modified skill/agent file for required clauses so a swapped/edited skill body
cannot pass silently with wrong or missing content.

Exit 0 only when all assertions pass; exit 1 with a named failure on any miss.
Deterministic — no network, no agent load.

Usage: python3 plugins/cc10x/tools/prompt_clause_assertions.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
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


ASSERTIONS = [
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
        "building: TEST_SEAMS recording",
        SKILLS / "building" / "SKILL.md",
        contains("TEST_SEAMS"),
        "builder records TEST_SEAMS in DECISIONS",
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
        "planning: advisory to builder",
        SKILLS / "planning" / "SKILL.md",
        contains("advisory input to the builder"),
        "seams marked advisory not fail-closed",
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
]


def main() -> int:
    failures = []
    for a in ASSERTIONS:
        if not a.eval():
            failures.append(
                f"  - {a.name} [{a.path.relative_to(ROOT)}]: {a.description}"
            )

    if failures:
        print(f"PROMPT CLAUSE ASSERTIONS: FAIL ({len(failures)} failure(s))")
        for f in failures:
            print(f)
        return 1
    print(f"PROMPT CLAUSE ASSERTIONS: OK ({len(ASSERTIONS)} assertions passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
