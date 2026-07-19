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


def yaml_alternatives_parse(marker: str, expected_blocks: int):
    """True when exactly expected_blocks fenced yaml blocks contain marker and each parses.

    PyYAML is a dev-environment dependency, not a runtime one; if it is not
    installed the structural contains-assertions still guard the content, so
    the parse check degrades to pass rather than crashing the suite.
    """

    def check(text: str) -> bool:
        try:
            import yaml
        except ImportError:
            return True
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
            "| 5 | TRIAGE | triage, \"incoming issues\", \"look at #\", \"triage #\" | TRIAGE | triage-agent",
        ),
        "TRIAGE row anchored with non-colliding keywords + chain",
    ),
    A(
        "router: CODEBASE-HEALTH route row anchored",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 6 | CODEBASE-HEALTH | \"codebase health\", \"improve architecture\", \"deepening\", \"ball of mud\", \"shallow modules\", \"architecture audit\" | CODEBASE-HEALTH | architecture-scanner",
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
        "router: DEFAULT row anchored at priority 7",
        PLUGIN / "skills" / "cc10x-router" / "SKILL.md",
        contains_all(
            "| 7 | DEFAULT | Everything else | BUILD | component-builder",
        ),
        "DEFAULT row at priority 7 with BUILD chain unchanged",
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
            "cc10x:codebase-hygiene",
        ),
        "triage-agent has read-only tools (no TaskUpdate), YAML contract with STATUS/CATEGORY/STATE/BRIEF_PATH, loads codebase-hygiene",
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
        contains("|triage|codebase-health|"),
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
    A(
        "researcher: TaskUpdate before final contract response",
        AGENTS / "researcher.md",
        lambda text: "Before emitting your final response" in text
        and "no tool calls after it" in text
        and "After outputting Router Contract" not in text,
        "TaskUpdate ordered before the final contract response, never after",
    ),
    A(
        "doc-syncer: TaskUpdate before final contract response",
        AGENTS / "doc-syncer.md",
        lambda text: "Before emitting your final response" in text
        and "no tool calls after it" in text
        and "After emitting the Router Contract" not in text,
        "TaskUpdate ordered before the final contract response, never after",
    ),
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
        "Phase 4 uses patch with an explicit target; broken in-cache git apply --3way removed",
    ),
    A(
        "update: find predicates parenthesized",
        SKILLS / "update" / "SKILL.md",
        contains('-type f \\( -name "*.md" -o -name "*.json" -o -name "*.py" \\)'),
        "Phase 2 find applies -type f to all three name predicates",
    ),
    A(
        "update: registry updated after swap",
        SKILLS / "update" / "SKILL.md",
        contains("Update registry only after the swap succeeded"),
        "Phase 3 records the new version only once the cache swap has happened",
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
        "agent-common: final-response rule carries the TaskUpdate carve-out",
        SKILLS / "agent-common" / "SKILL.md",
        contains_all(
            "If your agent doc says to call TaskUpdate",
            "otherwise the router completes the task for you",
        ),
        "SINGLE FINAL RESPONSE RULE step 2 restates the CONTRACT-Envelope carve-out instead of contradicting it",
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
        and "If the line-1 envelope AND the first-5-lines fallback heading are both absent, or any required contract field is missing" in text,
        "inline verification triggers on concrete absence conditions, not a vibe about output length",
    ),
    # 80.5 — §11b Cycle row: checkpoint-at-3 semantics, not a hard cap
    A(
        "router: Cycle row states checkpoint-at-3, not caps-at-3",
        SKILLS / "cc10x-router" / "SKILL.md",
        lambda text: "caps cycles at 3" not in text
        and "pauses the loop for a human checkpoint at the 3rd remediation cycle" in text
        and "cycles beyond 3 run only on explicit user go-ahead" in text,
        "matches what remediation-and-research.md and §14 already enforce: >= 3 -> human checkpoint, not a hard stop",
    ),
    # --- Design-cluster contradiction fixes (ticket #81) ---
    # 81.1 — architecture: two-adapter gloss matches canonical ports-only formulation, both occurrences
    A(
        "architecture: two-adapter gloss is ports-only, caller/adapter gloss gone",
        SKILLS / "architecture" / "SKILL.md",
        lambda text: "only one caller/adapter exists" not in text
        and text.count(
            "fails the two-adapter rule (it is a port with only one adapter — callers and tests don't count as adapters)"
        )
        == 2,
        "codebase-design's canonical rule says an ordinary caller or test is NOT an adapter; the old gloss would veto nearly every single-caller module",
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
        and "`low` = only CHECK verdicts, no CREATE" in text
        and "`medium` = at least one UPDATE" in text
        and "CREATE in two or more layers" in text
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
        "architecture: application rule byte-identical at both points of use",
        SKILLS / "architecture" / "SKILL.md",
        lambda text: text.count(
            "Before finalizing any component boundary, apply the **Deletion Test** and "
            "**Two-Adapter Rule** as defined in `cc10x:codebase-design`. A component that "
            "fails the deletion test (complexity vanishes if deleted) or fails the "
            "two-adapter rule (it is a port with only one adapter — callers and tests "
            "don't count as adapters) is not a real boundary yet — fold it into its "
            "caller or defer the split until a second concrete need appears."
        )
        == 2,
        "the deliberate repetition at Design Components and Architecture Vocabulary cannot drift",
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
