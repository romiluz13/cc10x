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
            "never --abort",
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
