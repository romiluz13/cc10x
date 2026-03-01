# CC10x Router Behavioral Invariant Registry

**Purpose:** Maps every load-bearing section of `cc10x-router/SKILL.md` to the failure mode it prevents.

**Rule for editors:** Before removing ANY text from the router, find its invariant entry.
Confirm its coverage exists elsewhere. Update the entry to point to the new location.
No entry = load-bearing = do not remove.

**Rule for PR reviews:** Any PR removing router lines must reference the invariant IDs
for each removed section and state where coverage now lives.

---

## Core Orchestration

### INV-001: Memory Notes compaction safety
**Covers:** Chain Execution Loop step 3a
**Enforces:** After each READ-ONLY agent completes, Memory Notes are immediately
written into the Memory Update task description (filesystem-backed).
**Fails silently if removed:** Memory Notes exist only in conversation history.
After context compaction, the Memory Update task finds nothing to persist.
Every learning from code-reviewer, silent-failure-hunter, integration-verifier
is permanently lost. Memory system accumulates nothing over time.
**Safe to remove:** Never. Unless Memory Update reads from another compaction-safe
source that isn't conversation history.

### INV-002: memory_task_id durability
**Covers:** Step 3a → `Edit(activeContext.md ## References, [cc10x-internal] memory_task_id)`
**Enforces:** After context compaction, the router can reconstruct `memory_task_id`
from `activeContext.md ## References` rather than losing it.
**Fails silently if removed:** After compaction, `memory_task_id` is undefined.
Step 3a calls `TaskUpdate({ taskId: undefined })` silently failing. Memory Notes
are never captured into the task description. Compaction kills all Memory Notes.
**Safe to remove:** Never. This is the compaction recovery anchor for step 3a.

### INV-003: Parallel execution — dual TaskUpdate before invocation
**Covers:** Chain Execution Loop step 2, parallel case bullet
**Enforces:** Both parallel agents (code-reviewer + silent-failure-hunter)
must be set to `in_progress` BEFORE either Task() call fires.
**Fails silently if removed:** One task remains "pending" during execution.
If TaskList() is called before both complete, the pending agent appears
available and may be double-invoked.
**Safe to remove:** Never. Required for accurate task state tracking.

### INV-004: Circuit Breaker active-only count
**Covers:** Router Contract Validation → Circuit Breaker
**Enforces:** Counts only ACTIVE (pending/in_progress) REM-FIX tasks, not completed ones.
**Fails silently if removed:** If counting all REM-FIX tasks (including completed),
prior sessions' completed fixes inflate the count. First REM-FIX of a clean
new workflow immediately trips the breaker. Users get blocked on every fix cycle.
**Safe to remove:** Never. The "active only" filter is what makes the breaker
session-safe.

### INV-005: Step 3 fallback blockedBy exclusion
**Covers:** Chain Execution Loop step 3, fallback completion check
**Enforces:** Router checks `blockedBy` before force-completing a task. If
`blockedBy` is non-empty, the agent intentionally blocked itself (self-healing
SELF_REMEDIATED protocol) — do NOT force to completed.
**Fails silently if removed:** When integration-verifier or code-reviewer
self-heals (creates REM-FIX, blocks itself), the router's fallback immediately
force-completes the blocked task. Self-healing protocol is silently destroyed.
REM-FIX runs but the verifier never re-runs. Broken code ships.
**Safe to remove:** Never while SELF_REMEDIATED protocol exists.

---

## Contract Validation Rules

### INV-006: Rule 0 — CONTRACT RULE enforcement table
**Covers:** Contract validation rule 0 (runs before rules 1a/1b/2)
**Enforces:** If agent self-reports STATUS=PASS but TDD evidence is missing
(or CONFIDENCE below threshold), router overrides the status to FAIL/BLOCKED.
**Fails silently if removed:** Agents that skip TDD can self-report PASS and
the workflow proceeds as if tests were run. No tests = no regression protection.
**Safe to remove:** Only if all agents can be trusted never to emit false STATUS.
In practice: never remove.

### INV-007: Rule 1a NOT IN exclusion list
**Covers:** Rule 1a condition: `AND contract.STATUS NOT IN [...]`
**Enforces:** Statuses that have their own handlers (INVESTIGATING, BLOCKED,
SELF_REMEDIATED, REVERT_RECOMMENDED, LIMITATION_ACCEPTED, NEEDS_CLARIFICATION)
do NOT trigger a generic REM-FIX task creation.
**Fails silently if removed:** An investigator returning INVESTIGATING creates
a spurious REM-FIX task AND continues investigating. Double-handling, infinite
loops, wrong workflow branches. Every special status becomes a REM-FIX.
**Safe to remove per entry:** Each entry can be removed only if its named
handler (2b, 2c, 2d, 2f, 0b) is also removed. They are paired.

### INV-008: Rule 1b — unconditional AskUserQuestion for HIGH issues
**Covers:** Contract validation rule 1b
**Enforces:** When REQUIRES_REMEDIATION=true and BLOCKING=false, the user
is ALWAYS asked whether to fix HIGH issues before continuing.
**Fails silently if removed:** HIGH issues from code-reviewer or
silent-failure-hunter are silently ignored. Workflow continues with
known quality problems. User never gets to decide.
**Safe to remove:** Never. This is the original feature request (v6.0.26)
that started all of v6.0.x.

### INV-009: Rule 0c — NEEDS_EXTERNAL_RESEARCH pre-check
**Covers:** Contract validation rule 0c
**Enforces:** When bug-investigator signals it needs external research,
the THREE-PHASE research process runs BEFORE creating any REM-FIX.
**Fails silently if removed:** Bug-investigator exhausts local attempts,
signals research needed, but router creates REM-FIX instead. Builder fixes
what investigator couldn't fix without the external context. Fix is blind.
**Safe to remove:** Only if bug-investigator handles all research internally
(partially done in v6.0.36 — investigator calls github-research directly,
but rule 0c handles the case where it signals via contract).

### INV-010: Rule 2 — parallel conflict check (Cases A and B)
**Covers:** Contract validation rule 2, Cases A and B
**Enforces:** When code-reviewer APPROVES but silent-failure-hunter found
CRITICAL or HIGH issues, user is asked to resolve the conflict before verifier runs.
**Fails silently if removed:** Reviewer approves, hunter finds critical gaps,
verifier runs on approved code. Hunter's findings are silently discarded.
Silent failures ship.
**Safe to remove:** Never while both parallel agents run in BUILD workflow.

### INV-011: Rule 2b — NEEDS_CLARIFICATION handler for planner
**Covers:** Contract validation rule 2b
**Enforces:** When planner returns NEEDS_CLARIFICATION, router collects
user answers before proceeding to BUILD.
**Fails silently if removed:** Planner signals its plan has unresolved
assumptions. Workflow proceeds to BUILD anyway. Builder works from
an incomplete plan. Wrong thing gets built.
**Safe to remove:** Only if planner is guaranteed to never emit
STATUS=NEEDS_CLARIFICATION.

### INV-012: Rule 2c — INVESTIGATING handler for bug-investigator
**Covers:** Contract validation rule 2c
**Enforces:** When bug-investigator returns INVESTIGATING (still working,
no fix yet), router creates a continuation task and re-invokes.
**Fails silently if removed:** Investigator returns INVESTIGATING.
Router treats it as a generic failure, creates REM-FIX. Builder tries
to fix a problem the investigator hasn't diagnosed yet. Wrong fix.
**Safe to remove:** Only if bug-investigator is guaranteed to always
return FIXED or BLOCKED in one pass (not currently guaranteed).

### INV-013: Rule 2f — BLOCKED terminal state handler
**Covers:** Contract validation rule 2f
**Enforces:** When bug-investigator is permanently stuck (BLOCKED),
user is asked: research / manual fix / abort.
**Fails silently if removed:** BLOCKED status falls through to rule 1a.
Router creates a REM-FIX task for a problem that has no known fix.
Builder spins indefinitely. Infinite REM-FIX loop until Circuit Breaker fires.
**Safe to remove:** Never while BLOCKED is a valid bug-investigator status.

### INV-014: Rule 2d — REVERT_RECOMMENDED and LIMITATION_ACCEPTED handlers
**Covers:** Contract validation rule 2d
**Enforces:** When integration-verifier's inline AskUserQuestion results in
a revert decision or accepted limitation, router routes correctly:
REVERT_RECOMMENDED → stop workflow; LIMITATION_ACCEPTED → proceed to Memory Update.
**Fails silently if removed:** These statuses fall through to rule 1a.
A user-confirmed revert becomes a REM-FIX task. A user-accepted limitation
creates a spurious fix task. User's inline decision is ignored.
**Safe to remove:** Never while integration-verifier emits these statuses.

### INV-015: Rule 0b — SELF_REMEDIATED handler
**Covers:** Contract validation rule 0b
**Enforces:** When an agent self-heals (creates its own REM-FIX, blocks itself),
router acknowledges without creating a DUPLICATE REM-FIX.
**Fails silently if removed:** SELF_REMEDIATED falls through to rule 1a.
Router creates a second REM-FIX task for a problem the agent already
created a REM-FIX for. Two fix tasks, double work, possible conflicts.
**Safe to remove:** Only if SELF_REMEDIATED protocol is removed from all agents.

---

## Remediation Re-Review Loop

### INV-016: Re-Review Loop — spawns NEW verifier task (not reactivates old)
**Covers:** Re-Review Loop steps 1-3
**Enforces:** After REM-FIX completes, Re-Review Loop creates NEW
code-reviewer, silent-failure-hunter, AND integration-verifier tasks.
**Fails silently if removed:** After a fix, the original completed verifier
task is never re-run. Fixed code ships without re-verification.
Broken code that passed the original build before the fix is never checked.
**Safe to remove:** Never. Code changes from REM-FIX must be re-verified.
Note: addBlockedBy on a completed task is a no-op — must spawn NEW tasks.

### INV-017: Cycle Cap — AskUserQuestion after 2+ REM-FIX cycles
**Covers:** Re-Review Loop step 0
**Enforces:** After 2+ completed REM-FIX cycles, asks user whether to
continue, research patterns, accept issues, or abort.
**Fails silently if removed:** Infinite remediation loop. Fix introduces
new bug → re-review finds it → new REM-FIX → fix introduces new bug → ...
No termination condition except Circuit Breaker (which only fires at 3 active).
**Safe to remove:** Never while REM-FIX tasks can trigger re-review loops.

### INV-018: Cycle Cap — completed count (not active)
**Covers:** Re-Review Loop step 0 filter condition
**Enforces:** Cycle Cap counts COMPLETED REM-FIX tasks (not active ones).
**Fails silently if removed (if switched to active count):** Cap fires only
when 2+ REM-FIX tasks are simultaneously active — extremely rare. In normal
flow, one REM-FIX runs at a time. Cap effectively never fires. Infinite loops
are not prevented.
**Note:** Circuit Breaker uses ACTIVE count (pile-up prevention).
Cycle Cap uses COMPLETED count (loop detection). These are different. Do not merge.

### INV-019: Re-Review Loop — DEBUG workflow skips silent-failure-hunter
**Covers:** Re-Review Loop step 2 conditional
**Enforces:** In DEBUG workflows, silent-failure-hunter is not in the original
chain and is not created in re-reviews.
**Fails silently if removed:** After a REM-FIX in a DEBUG workflow, a
silent-failure-hunter task is created and must complete before the verifier
can run. Hunter runs on a codebase it has no context for. Adds latency.
Task hierarchy becomes inconsistent with original workflow definition.
**Safe to remove:** Never while DEBUG chain excludes silent-failure-hunter.

---

## Memory System

### INV-020: DEBUG-RESET marker uses Parent Workflow ID (not agent's own task ID)
**Covers:** bug-investigator.md ## DEBUG-RESET Marker section
**Enforces:** The DEBUG-RESET marker uses the PARENT DEBUG workflow task ID
(passed by router as "Parent Workflow ID"), not the investigator's own task ID.
**Fails silently if removed (or if using wrong ID):** Marker is written as
`[DEBUG-RESET: wf:{investigator_task_id}]`. Memory Update task anchors on
`[DEBUG-RESET: wf:{parent_task_id}]`. IDs never match. Recent Changes is
never trimmed. Memory bloats silently across all future DEBUG sessions.
**Safe to change:** Only if Memory Update task is updated to anchor on the
investigator's own task ID consistently.

### INV-021: Memory files Auto-Heal pattern
**Covers:** Memory section Auto-Heal pattern (cc10x-router/SKILL.md)
**Enforces:** If required sections are missing from memory files, the router
inserts them before any workflow runs.
**Fails silently if removed:** Old projects without required sections cause
Edit anchors to fail silently throughout the workflow. Memory updates appear
to succeed but actually do nothing. Learnings are lost. Decisions not recorded.
**Safe to remove:** Never for projects that may have been created before
required sections were added to templates. Idempotent — no cost to keep.

### INV-022: Memory Update task — READ-ONLY agents only
**Covers:** Memory Update task descriptions (BUILD/DEBUG/REVIEW)
**Enforces:** Memory Update collects notes from READ-ONLY agents only.
WRITE agents (component-builder, bug-investigator, planner) already wrote
memory directly — skipping their Memory Notes avoids duplicate entries.
**Fails silently if removed:** Memory Update also processes Memory Notes
from WRITE agents. Every entry appears twice in memory. Patterns file
becomes polluted with duplicates. Memory degrades over time.
**Safe to remove:** Only if WRITE agents stop writing memory directly.

---

## Agent Isolation Invariants

### INV-023: Task ID in every agent prompt
**Covers:** Agent Invocation template — Task ID field
**Enforces:** Every agent knows its own task ID and calls
`TaskUpdate({ taskId, status: "completed" })` at the end.
**Fails silently if removed:** Agents cannot mark their own tasks complete.
Router calls `TaskList()` and sees all tasks still `in_progress`. Fallback
tries to force-complete but finds blockedBy (self-healing agents) and skips.
Workflow never advances. Permanent hang.
**Safe to remove:** Never.

### INV-024: Parent Workflow ID in every agent prompt
**Covers:** Agent Invocation template — Parent Workflow ID field
**Enforces:** Agents know the parent workflow task ID for scoping markers
(primarily used by bug-investigator for DEBUG-RESET anchor).
**Fails silently if removed:** bug-investigator has no Parent Workflow ID.
DEBUG-RESET marker uses fallback (own task ID). Anchor mismatch.
Memory trimming never fires. See INV-020.
**Safe to remove:** Never while bug-investigator needs PARENT_WORKFLOW_ID
for DEBUG-RESET scoping.

### INV-025: NEVER call EnterPlanMode
**Covers:** Planner agent frontmatter warning + router PLAN workflow
**Enforces:** No agent or router workflow calls EnterPlanMode.
**Fails visibly if removed:** EnterPlanMode blocks Write/Edit tools in the
invoked agent context. Plan files can never be saved. Builder can never
write code. Router hangs waiting for agent to complete.
**Safe to remove:** Never. This is a hard platform constraint.

---

## Verification Conditions

### INV-026: Integration-verifier ALL checks must pass before STATUS: PASS
**Covers:** integration-verifier.md verification checklist
**Enforces:** Verifier cannot emit STATUS: PASS unless every check has passed.
Skipping any check = STATUS: FAIL.
**Fails silently if removed:** Verifier cherry-picks which checks to run.
Broken tests, missing builds, or failing linters are silently ignored.
Code ships with known failures.
**Safe to remove:** Never. This is the final quality gate.

### INV-027: TDD evidence required for component-builder STATUS: PASS
**Covers:** component-builder.md CONTRACT RULE + router rule 0
**Enforces:** Builder must provide TDD_RED_EXIT=1 AND TDD_GREEN_EXIT=0
before STATUS=PASS is accepted by the router. Rule 0 overrides if missing.
**Fails silently if removed:** Builder can claim PASS without running tests.
No regression protection. Changes ship without test coverage.
**Safe to remove:** Never. TDD is the fundamental quality guarantee.

---

## How to Use This Document

**When editing the router:**
1. Find all INV entries that reference the lines you're changing
2. For each entry: confirm the invariant is still covered after your change
3. If you're moving logic: update "Covered by" to point to new location
4. If you're removing logic: prove failure mode no longer applies

**When this document becomes stale:**
The router changed but this document wasn't updated. That's a bug.
Fix: update the relevant INV entries before merging.

**When adding new logic to the router:**
Ask: does this prevent a new failure mode? If yes: add an INV entry.
If no: it's probably prose — compress it.

---

*Last updated: v6.0.38 — 2026-03-01*
*Router version at last audit: 6.0.38 (802 lines)*
