# Advisory On-Ramp Workflows: TRIAGE + CODEBASE-HEALTH

Sub-project 2b added two new intent routes to the router's routing table —
TRIAGE (priority 5) and CODEBASE-HEALTH (priority 6) — as advisory-only
on-ramp workflows. Neither writes code; both produce inputs that feed
existing code-writing workflows (BUILD/DEBUG/PLAN) on a fresh user request.

## Context

cc10x had no workflow for incoming raw issues (bug reports, feature requests,
PRs) and no workflow for codebase health upkeep (finding shallow modules,
deepening opportunities). Matt Pocock's skills repo has both: `triage` (a
state machine moving issues through triage roles) and `improve-codebase-
architecture` (a scanner that surfaces deepening candidates as a visual
report). The question was how to add them without risking the zero-risk
invariant on the routing table.

## Decision

Add both as **advisory-only on-ramp workflows** at priority 5 and 6,
strictly additive to the routing table. The existing priority 1-4 routes
(ERROR/PLAN/REVIEW/ORIENT) are byte-for-byte unchanged; DEFAULT→BUILD moves
from priority 5 to 7 (stays last). Both new routes fire only on their
explicit keywords — they never fall through from an existing route.

A misroute produces a wrong advisory output (a wrong brief or a wrong
candidate list), not wrong code. The user must explicitly route from
TRIAGE/CODEBASE-HEALTH to BUILD/DEBUG/PLAN — neither auto-dispatches into a
code-writing workflow.

## Rejected alternatives

- **Code-writing workflows.** Rejected: a misroute into a code-writing
  workflow would produce wrong code, violating the zero-risk invariant.
  Advisory-only keeps the blast radius of a misroute to wrong advice, which
  the user catches before it reaches BUILD.
- **Integration into existing REVIEW/ORIENT.** Rejected: different intent,
  different output. REVIEW judges existing code quality; ORIENT explains
  structure; TRIAGE processes incoming issues; CODEBASE-HEALTH surfaces
  refactor candidates. Forcing them into REVIEW/ORIENT would overload those
  routes and muddle their keywords.

## Consequences

- The routing table has 7 rows (was 5). Priority 1-4 unchanged.
- DEFAULT→BUILD is now priority 7 (was 5) — still last, still the fallback.
- TRIAGE and CODEBASE-HEALTH are single-pass advisory workflows (no
  `phase_cursor`, no phases) — simpler artifacts than BUILD/DEBUG/PLAN.
- Category/wontfix decisions in TRIAGE are high-blast-radius: stop for human.
- CODEBASE-HEALTH writes a single HTML report to the OS temp dir, not the repo.
