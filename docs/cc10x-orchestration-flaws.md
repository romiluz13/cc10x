# cc10x Orchestration Flaws Analysis

> **Context:** These are flaws in the **English orchestration layer** - gaps, ambiguities, and conflicts in the prompt engineering that may cause AI to behave unexpectedly.

---

## Critical Flaws (High Impact)

### FLAW 1: Skill Loading Gap Between Router and Agents

**Severity:** CRITICAL
**Location:** `cc10x-router/SKILL.md:213-214` vs all agent files

**Problem:**
The router says: "SKILL_HINTS are MANDATORY. Agent MUST call `Skill(skill="...")` for each hint immediately after loading memory."

However, agents have THREE conflicting mechanisms for skill loading:

1. **Frontmatter `skills:`** - Listed in YAML header (auto-loaded?)
2. **Skill Triggers section** - Conditional loading based on patterns
3. **SKILL_HINTS from router** - Passed in prompt

**Example Conflict:**
- Router passes `SKILL_HINTS: cc10x:frontend-patterns` to code-reviewer
- Agent frontmatter lists: `skills: cc10x:session-memory, cc10x:code-review-patterns, cc10x:verification-before-completion`
- Agent's internal trigger: "UI code (.tsx, .jsx, components/, ui/) → load frontend-patterns"

**Questions unanswered:**
- Are frontmatter skills auto-loaded or just declarations?
- If agent's trigger doesn't match router's detection, what happens?
- Can skills be double-loaded? What's the effect?

**Impact:** Skills may be:
- Not loaded when needed (agent ignores SKILL_HINTS)
- Double-loaded (wasted tokens)
- Conflicting (router says load X, agent's trigger says don't)

**Suggested Fix:**
```markdown
## Skill Loading (Definitive)

1. Frontmatter `skills:` = DECLARATIONS ONLY (documentation)
2. SKILL_HINTS from router = MANDATORY to load immediately
3. Agent's Skill Triggers = ADDITIONAL skills if conditions met

Order: Router SKILL_HINTS first → Agent triggers second
Duplicates: OK to load same skill twice (idempotent)
```

---

### FLAW 2: Plan File → Agent Context Propagation is Broken

**Severity:** CRITICAL
**Location:** `cc10x-router:70-107` vs `component-builder.md:21-29`

**Problem:**
The router creates tasks with `metadata.planFile`:
```javascript
TaskCreate({
  metadata: { planFile: "docs/plans/..." }
})
```

The component-builder expects to find this:
```markdown
If task metadata contains `planFile`:
1. Read(file_path="{metadata.planFile}")
```

**Gap:** How does component-builder ACCESS task metadata?

The router passes context via PROMPT TEXT:
```
Task(subagent_type="cc10x:component-builder", prompt="
Your task ID: {taskId}
User request: {request}
...")
```

But `metadata` is NOT included in the prompt template!

**Impact:** component-builder cannot access `planFile` because:
1. It's stored in task metadata
2. Router doesn't include metadata in prompt
3. Agent would need to call `TaskGet(taskId)` to retrieve it
4. No instruction tells agent to call TaskGet

**Suggested Fix:**
Add to router's Agent Invocation template:
```
Task(subagent_type="cc10x:component-builder", prompt="
Your task ID: {taskId}
Plan file: {planFile or 'N/A'}  ← ADD THIS
User request: {request}
...")
```

Or add instruction to component-builder:
```markdown
## First Action: Retrieve Task Context
TaskGet(taskId="{TASK_ID_FROM_PROMPT}")
# Extract metadata.planFile if present
```

---

### FLAW 3: Research Persistence Atomicity is Not Enforced

**Severity:** CRITICAL
**Location:** `github-research/SKILL.md:157-163`

**Problem:**
The skill says:
```
### ATOMIC CHECKPOINT (DO NOT PROCEED UNTIL BOTH COMPLETE)
- ✓ Research file saved to docs/research/
- ⏸️ IMMEDIATELY proceed to Step 2 (do not invoke agents, do not pass go)
```

But this is just English instruction. Nothing prevents:
- Context compaction between Step 1 and Step 2
- Claude getting distracted after saving research file
- Forgetting to update memory reference

**Impact:** Research can be:
- Conducted → saved to file → memory NEVER updated → orphaned file
- File exists but activeContext.md has no reference
- Next session can't find the research

**Suggested Fix:**
Combine into single Edit operation where possible:
```markdown
## Single-Operation Persistence (Atomic)

Read existing activeContext.md → Modify to include research reference → Edit in one operation

DO NOT:
1. Save research file
2. [gap where compaction can occur]
3. Update memory

DO:
1. Save research file
2. SAME MESSAGE: Update memory reference
```

---

### FLAW 4: Parallel Agent Results Are Not Merged

**Severity:** HIGH
**Location:** `cc10x-router:293-307`

**Problem:**
The router invokes parallel agents:
```
Task(subagent_type="cc10x:code-reviewer", prompt="...")
Task(subagent_type="cc10x:silent-failure-hunter", prompt="...")
```

And says: "CRITICAL: Both Task calls in same message = both complete before you continue."

**Missing:**
- How are results from BOTH agents collected?
- How does integration-verifier know what EACH found?
- What if code-reviewer finds CRITICAL issues and silent-failure-hunter finds CRITICAL issues?
- What if they contradict (one says OK, one says NOT OK)?

**Impact:**
- Information lost in handoff
- integration-verifier may not know about issues found
- Conflicting results not reconciled

**Suggested Fix:**
```markdown
## Parallel Agent Result Collection

After parallel agents complete:
1. Collect output from BOTH agents
2. Merge findings:
   - All CRITICAL issues from both
   - All HIGH issues from both
   - Conflicts: Present both perspectives to user
3. Pass merged findings to next agent:
   Task(subagent_type="cc10x:integration-verifier", prompt="
   ...
   Previous agent findings:
   - code-reviewer: {reviewer_output}
   - silent-failure-hunter: {hunter_output}
   ...")
```

---

### FLAW 5: Memory File Race Condition in Parallel Execution

**Severity:** HIGH
**Location:** `session-memory/SKILL.md` + parallel execution pattern

**Problem:**
During BUILD workflow:
- code-reviewer and silent-failure-hunter run in PARALLEL
- Both may try to update activeContext.md
- Both read → modify → Edit
- Last writer wins, first agent's changes LOST

**Scenario:**
```
T0: code-reviewer reads activeContext.md (version A)
T0: silent-failure-hunter reads activeContext.md (version A)
T1: code-reviewer edits → version B (adds learning)
T2: silent-failure-hunter edits version A → version C (OVERWRITES B)
Result: code-reviewer's learning LOST
```

**Impact:** Memory corruption, lost learnings, inconsistent state

**Suggested Fix:**
```markdown
## Memory Update Coordination (Parallel Agents)

During parallel execution, ONLY router updates memory:
1. Parallel agents DO NOT update memory directly
2. Parallel agents RETURN findings in output
3. After ALL parallel agents complete:
   - Router collects all outputs
   - Router merges updates
   - Router performs SINGLE memory update

Exception: If agent finds something CRITICAL, can update but must use unique section:
Edit(old_string="## Learnings This Session",
     new_string="## Learnings This Session\n- [code-reviewer]: {learning}")
```

---

## High Impact Flaws

### FLAW 6: Agent Task Completion is Self-Reported Without Verification

**Severity:** HIGH
**Location:** All agent files "Task Completion" sections

**Problem:**
Every agent is told to call `TaskUpdate(taskId, status="completed")` when done.

No verification that:
- Work was actually completed
- Output format was followed
- Gates were passed
- Exit codes were captured

Router's "Post-Agent Validation" (lines 218-224) is "soft validation" - notes for improvement, doesn't block.

**Impact:** Agent can mark itself "completed" without completing properly.

**Suggested Fix:**
```markdown
## Post-Agent Verification (HARD)

After agent returns, router MUST verify:
1. Output contains required sections (Summary, Evidence, Task Status)
2. For component-builder: RED and GREEN exit codes present
3. For integration-verifier: Scenario table present
4. For code-reviewer: Confidence scores present

If verification fails:
- DO NOT proceed to next agent
- Create follow-up task: "Complete missing: {section}"
- OR ask user: "Agent output incomplete. Continue anyway?"
```

---

### FLAW 7: Task ID Propagation is Fragile

**Severity:** HIGH
**Location:** Agent files "Task Completion" sections

**Problem:**
All agents say:
```
If task ID was provided in prompt (check for "Your task ID:"):
```

This relies on:
1. Router including exact string "Your task ID:" in prompt
2. Agent parsing that string correctly

If wording changes or is omitted, task won't be marked complete.

**Impact:** Orphaned tasks that never complete, breaking chain execution.

**Suggested Fix:**
```markdown
## Task ID Contract (Strict)

Router MUST include (exact format):
```
Your task ID: {taskId}
```

Agent MUST:
1. Extract task ID from first line containing "Your task ID:"
2. If not found, LOG WARNING but continue
3. Call TaskUpdate at end regardless
```

---

### FLAW 8: Debug Workflow Research Trigger is Undefined

**Severity:** HIGH
**Location:** `cc10x-router:150-162`

**Problem:**
Research trigger says: "3+ local debugging attempts failed (check activeContext Recent Changes for attempt count)"

**Undefined:**
- What constitutes an "attempt"?
- How is attempt count stored in activeContext?
- What format should Recent Changes use for counting?

**Example: Is this 1 attempt or 3?**
```
## Recent Changes
- Tried fixing null check - still failing
- Added error handling - still failing
- Changed API call - still failing
```

**Impact:** Research may never trigger when needed, or trigger incorrectly.

**Suggested Fix:**
```markdown
## Debug Attempt Tracking (Explicit)

In activeContext.md Recent Changes, use format:
- [DEBUG ATTEMPT 1]: {what was tried} - {result}
- [DEBUG ATTEMPT 2]: {what was tried} - {result}

When checking for research trigger:
- Count lines matching "[DEBUG ATTEMPT N]"
- If count >= 3 AND all show failure → trigger research
```

---

### FLAW 9: Skill → Agent Tool Access Mismatch

**Severity:** HIGH
**Location:** Agent frontmatter `tools:` vs Skill `allowed-tools:`

**Problem:**
github-research skill lists:
```yaml
allowed-tools: WebFetch, mcp__octocode__githubSearchCode, mcp__octocode__*...
```

But planner agent has:
```yaml
tools: Read, Write, Bash, Grep, Glob, Skill, LSP
```

No WebFetch or mcp__octocode in planner's tools!

**How is planner supposed to execute github-research skill?**

**Impact:** Skills may fail silently because agent lacks required tools.

**Suggested Fix:**
Two options:

1. **Skills inherit agent's tools:**
```markdown
Skills use AGENT'S tools, not their own allowed-tools.
allowed-tools is documentation only.
```

2. **Router executes research, not agent:**
```markdown
For github-research:
- Router executes octocode tools directly (has access)
- Router passes results to agent in prompt
- Agent doesn't need octocode tools
```

(Option 2 matches the THREE-PHASE pattern in router)

---

### FLAW 10: Component-Builder TDD Gate is Unenforced

**Severity:** HIGH
**Location:** `component-builder.md:75-94`

**Problem:**
Output format says:
```
**GATE: If either exit code is missing above, task is NOT complete.**
```

But:
- No enforcement mechanism
- Agent can simply not follow the format
- No external check verifies exit codes were captured

This is English instruction, not programmatic gate.

**Impact:** Components marked "built" without TDD evidence.

**Suggested Fix:**
```markdown
## TDD Evidence Verification (Router Side)

After component-builder completes, router checks output for:
1. String "Exit code: **1**" in RED Phase section
2. String "Exit code: **0**" in GREEN Phase section

If EITHER missing:
- DO NOT mark task complete
- Return to agent: "Missing TDD evidence. Please run tests and report exit codes."
```

---

## Medium Impact Flaws

### FLAW 11: Workflow Task Hierarchy Creates Duplicate State

**Severity:** MEDIUM
**Location:** `cc10x-router` "Task-Based Orchestration" vs `session-memory` "progress.md"

**Problem:**
Two parallel tracking systems:
1. TaskCreate/TaskList/TaskUpdate (ephemeral, session-scoped)
2. progress.md file (persistent, file-based)

planning-patterns shows updating progress.md with task IDs:
```
## Active Workflow Tasks
| Task ID | Subject | Status |
| {id}    | ...     | ...    |
```

But Task IDs are session-scoped! They won't persist across sessions.

**After session restart:**
- TaskList is empty (new session)
- progress.md references stale IDs like "task_abc123"
- No way to reconcile

**Impact:** Progress tracking breaks across sessions.

**Suggested Fix:**
```markdown
## Task ID Persistence Strategy

Option A: Don't store task IDs in progress.md
- Store task SUBJECTS instead
- Match by subject on resume

Option B: Use deterministic task IDs
- Generate ID from: workflow + feature + timestamp
- Same input → same ID across sessions

Option C: Two-tier tracking
- progress.md: Human-readable status (no IDs)
- TaskList: Session execution (with IDs)
- On resume: Create NEW tasks from progress.md state
```

---

### FLAW 12: Skill Detection Patterns Overlap

**Severity:** MEDIUM
**Location:** `cc10x-router:229-236`

**Problem:**
Detection patterns overlap:
- Frontend: "components/, ui/, pages/, .tsx, .jsx"
- API/Backend: "api/, routes/, services/"

What if file is `pages/api/users.ts`? (Next.js API route)
- Matches "pages/" → Frontend
- Matches "api/" → Backend

No priority order defined.

**Impact:** Wrong skills loaded, or duplicate skills loaded.

**Suggested Fix:**
```markdown
## Skill Detection Priority

When patterns overlap, apply in order:
1. EXPLICIT path takes precedence over parent
   - `pages/api/` → Backend (more specific than `pages/`)
2. File extension breaks ties
   - `.tsx/.jsx` → Frontend
   - `.ts/.js` in api/ → Backend
3. If still ambiguous: Load BOTH skills

Pattern Priority Order:
1. api/, routes/, services/ → architecture-patterns FIRST
2. components/, ui/ → frontend-patterns
3. pages/ without api/ → frontend-patterns
4. pages/api/ → architecture-patterns
```

---

### FLAW 13: REVIEW Workflow Clarification Not Enforced

**Severity:** MEDIUM
**Location:** `cc10x-router:166-172`

**Problem:**
Step 2 says "CLARIFY (REQUIRED): Use AskUserQuestion to confirm scope"

But:
- No gate like BUILD's REQUIREMENTS_CLARIFIED
- No consequence for skipping
- Agent (code-reviewer) doesn't mention waiting for clarification

**Impact:** Reviews may proceed without clear scope.

**Suggested Fix:**
Add explicit gate:
```markdown
### REVIEW
1. Load memory
2. **CLARIFY (REQUIRED)** (GATE: SCOPE_CLARIFIED)
   - Use AskUserQuestion
   - CANNOT proceed until user responds
3. Create task hierarchy...
```

---

### FLAW 14: Planning Task Structure Doesn't Match Router's Expected Structure

**Severity:** MEDIUM
**Location:** `planning-patterns/SKILL.md` "Task-Based Execution Tracking" vs `cc10x-router`

**Problem:**
Router creates agent tasks:
```javascript
TaskCreate({
  subject: "component-builder: Implement {feature}",
  metadata: { agent: "component-builder" }
})
```

Planner creates phase tasks:
```javascript
TaskCreate({
  subject: "Phase 1: {phase_title}",
  metadata: { phase: "1" }
})
```

Different structures! Router expects to find agent tasks to route. Planner creates phase tasks.

**Impact:** When executing a plan, router may not recognize phase tasks as part of its workflow.

**Suggested Fix:**
```markdown
## Task Structure Consistency

ALL workflow tasks follow this format:
- subject: "{WORKFLOW}: {summary}" for parent
- subject: "{agent}: {action}" for agent tasks

Phase tasks are SUB-tasks of agent tasks:
```
BUILD: Feature X
  └── component-builder: Implement Feature X
        ├── Phase 1: Setup (sub-task)
        └── Phase 2: Core (sub-task)
```
```

---

### FLAW 15: No Connection Between Design and Plan Files

**Severity:** MEDIUM
**Location:** `brainstorming/SKILL.md` vs `planning-patterns/SKILL.md`

**Problem:**
- Brainstorming saves: `docs/plans/YYYY-MM-DD-<feature>-design.md`
- Planning saves: `docs/plans/YYYY-MM-DD-<feature>-plan.md`
- Same directory, similar names

planning-patterns header says:
```
> **Design:** See `docs/plans/YYYY-MM-DD-<feature>-design.md` for full specification.
```

But no mechanism to:
- Find matching design file
- Verify design exists before planning
- Link plan back to design

**Impact:** Plans created without designs, or wrong design referenced.

**Suggested Fix:**
```markdown
## Design → Plan Linking

When creating plan:
1. Check for existing design file:
   Glob(pattern="docs/plans/*-{feature}-design.md")
2. If found: Include in plan header
3. If NOT found: Ask user:
   "No design found for {feature}. Create design first?"

When referencing:
- Use exact filename from Glob result, not assumed pattern
```

---

### FLAW 16: Silent-Failure-Hunter CRITICAL Fix Mandate Unverifiable

**Severity:** MEDIUM
**Location:** `silent-failure-hunter.md:44-47`

**Problem:**
Says: "CRITICAL Issues MUST be fixed before task completion"
And: "GATE: Cannot mark complete if CRITICAL issues exist."

But:
- Who verifies the agent actually fixed issues?
- Agent self-reports completion
- No external validation

**Impact:** CRITICAL silent failures may pass through.

**Suggested Fix:**
```markdown
## Critical Issue Verification

After silent-failure-hunter completes:
1. Parse output for "### Critical (must fix)" section
2. If section has items:
   - Check for corresponding "Fixed:" notation
   - OR check git diff for the file:line mentioned
3. If CRITICAL unfixed:
   - Block workflow
   - Create fix task
```

---

### FLAW 17: No Error Handling for Agent Failures

**Severity:** MEDIUM
**Location:** `cc10x-router` "Chain Execution Loop"

**Problem:**
The loop says:
```
If none ready AND uncompleted tasks exist → Wait (error state)
OR critical error detected (create error task, halt)
```

But:
- No definition of "critical error"
- No recovery mechanism
- "Halt" means workflow stuck forever
- What happens if agent throws exception?

**Impact:** Errors can halt entire workflow with no recovery.

**Suggested Fix:**
```markdown
## Error Recovery Protocol

### Agent Failure
If agent returns error or exception:
1. Log error to activeContext.md (Blockers section)
2. Ask user: "Agent {name} failed: {error}. Options:
   A. Retry agent
   B. Skip agent, continue workflow
   C. Abort workflow"

### Task Stuck
If task blocked for > 3 agent calls with no progress:
1. Mark task as BLOCKED (not completed, not pending)
2. Notify user: "Task {subject} appears stuck. Investigating..."

### Workflow Abort
If user requests abort:
1. Mark all pending tasks as "cancelled"
2. Update memory with current state
3. Return to idle
```

---

## Lower Impact Flaws

### FLAW 18: Memory "Quick Index" Pattern Adds Complexity Without Trigger

**Severity:** LOW
**Location:** `session-memory/SKILL.md:107-133`

**Problem:**
Quick Index is "optional" when file exceeds 200 lines. But:
- No mechanism to detect when 200 lines exceeded
- Manual decision adds cognitive load
- Inconsistent formats across sessions

**Suggested Fix:**
Either remove the pattern (YAGNI) or make it automatic:
```markdown
## Quick Index (Automatic)

When updating memory file:
1. Count lines in file
2. If > 200 AND no Quick Index exists:
   - Generate Quick Index automatically
   - Prepend to file

OR: Remove Quick Index pattern entirely (most projects don't need it)
```

---

### FLAW 19: Integration-Verifier Rollback Decision Lacks Criteria

**Severity:** LOW
**Location:** `integration-verifier.md:69-90`

**Problem:**
Three options for rollback, but no criteria for when to choose each:
- Option A: Create Fix Task
- Option B: Revert Branch
- Option C: Document & Continue

**Suggested Fix:**
```markdown
## Rollback Decision Tree

Is blocker fixable without architectural changes?
└── YES → Option A (Create Fix Task)
└── NO → Is this a fundamental design issue?
         └── YES → Option B (Revert Branch)
         └── NO → Is shipping with limitation acceptable?
                  └── YES → Option C (Document & Continue)
                  └── NO → Escalate to user
```

---

### FLAW 20: Verification Skill Stub Detection is Language-Specific

**Severity:** LOW
**Location:** `verification-before-completion/SKILL.md:275-314`

**Problem:**
Stub detection patterns are JavaScript/TypeScript specific:
```bash
grep -rE "onClick=\{?\(\) => \{\}\}?" src/
```

Won't work for Python, Go, Rust, etc.

**Suggested Fix:**
```markdown
## Language-Aware Stub Detection

### Universal (All Languages)
grep -rE "(TODO|FIXME|placeholder|not implemented)" src/

### JavaScript/TypeScript
grep -rE "onClick=\{?\(\) => \{\}\}?" src/
grep -rE "return (null|undefined|\{\}|\[\])" src/

### Python
grep -rE "(pass$|raise NotImplementedError)" src/

### Go
grep -rE "(panic\(\"not implemented\"\)|// TODO)" src/
```

---

## Summary: Priority Order for Fixes

### Must Fix (Breaks Core Functionality)
1. **FLAW 2:** Plan File → Agent Context Propagation (plans won't be followed)
2. **FLAW 4:** Parallel Agent Results Merging (information lost)
3. **FLAW 5:** Memory Race Condition (data corruption)

### Should Fix (Degrades Quality)
4. **FLAW 1:** Skill Loading Gap (skills may not load correctly)
5. **FLAW 6:** Self-Reported Completion (no verification)
6. **FLAW 9:** Tool Access Mismatch (skills may fail)
7. **FLAW 10:** TDD Gate Unenforced (no TDD evidence)

### Nice to Fix (Edge Cases)
8. **FLAW 3:** Research Atomicity (research can be lost)
9. **FLAW 7:** Task ID Fragile (orphaned tasks)
10. **FLAW 8:** Debug Attempt Tracking (research trigger unclear)
11. **FLAW 11-20:** Various (see individual descriptions)
