# Router-Agent Responsibility Refactor Plan

> **Status:** ROADMAP (NOT YET APPROVED)
> **Risk Level:** CRITICAL - This touches orchestration core
> **Created:** 2026-02-05
> **Last Updated:** 2026-02-05

---

## Executive Summary

**Original Hypothesis:** Move validation logic from router into agents to reduce router bloat.

**Research Finding:** This would VIOLATE Claude Code's core design philosophy.

**Revised Approach:** Keep validation in router, but SIMPLIFY it by standardizing agent output format.

---

## Part 1: The Research (Claude Code Design Philosophy)

### Source: Claude Code Guide Agent (claude-code-guide)

We consulted the official Claude Code and Agent SDK documentation. Key findings:

### 1.1 Responsibility Split (Official)

**Parent (orchestrator) responsibilities:**
- Orchestration decisions - deciding WHICH subagent and WHEN
- Context synthesis - combining results from multiple subagents
- **Validation of output quality**
- High-level reasoning about user intent

**Subagent responsibilities:**
- Focused, bounded tasks - handle ONE specific type of work
- Self-containment - complete task and return results
- **NOT responsible for validating against higher-level criteria**

### 1.2 Key Quote from Docs

> "The orchestrating layer is everything."

This is EXACTLY what CC10x's router is. The Bible says: "If orchestration breaks, CC10x breaks."

### 1.3 Anti-Pattern Warning

From official docs:

> **Anti-pattern: Moving validation INTO subagents**
> "If validation logic lives in the subagent, you lose the orchestrator's ability to make decisions."

This directly warns against our original hypothesis.

### 1.4 What Subagents CAN Do

- Internal error handling (try/catch patterns)
- Intermediate quality checks that don't stop execution
- **Structured output that parent can validate against** ← THIS IS THE KEY

---

## Part 2: Why the Original Plan Was Dangerous

### 2.1 Scenario Analysis: If We Moved Validation to Agents

**Scenario A: Agent lies about self-validation**
- Agent outputs `### Self-Validation: PASS` but actually has bugs
- Router trusts it, proceeds to next agent
- Bug propagates through entire workflow
- **Result:** Silent failures ship to production

**Scenario B: Agent validation logic diverges**
- Router has v1 validation rules
- Agent has v2 (after someone updated agent but forgot router)
- Inconsistent behavior depending on which runs
- **Result:** Non-deterministic orchestration

**Scenario C: Agent can't validate cross-agent concerns**
- code-reviewer PASSES
- silent-failure-hunter FAILS
- Who resolves the conflict?
- Agent can't - it doesn't see other agent's output
- **Result:** Conflict resolution breaks

**Scenario D: Remediation loop breaks**
- Agent self-validates and creates its own remediation task
- But agent can't block downstream tasks (it doesn't see TaskList)
- Remediation runs in parallel with downstream instead of blocking
- **Result:** Broken task dependencies

### 2.2 Why Router MUST Own Validation

| Concern | Why Router Must Handle |
|---------|----------------------|
| Cross-agent conflicts | Only router sees all outputs |
| Task dependencies | Only router can block downstream |
| Remediation loops | Only router knows the full chain |
| User bypass decisions | Only router talks to user |
| Memory Notes collection | Only router aggregates from all agents |

---

## Part 3: The Safe Alternative

### 3.1 Problem Reframed

The real problem isn't "validation is in the wrong place."
The real problem is "validation logic is verbose because agent output isn't standardized enough."

### 3.2 Solution: Standardize Agent Output → Simplify Router Validation

**Current state:** Each agent has slightly different output format. Router has ~100 lines parsing each format.

**Target state:** All agents output in IDENTICAL structure. Router validation becomes ~20 lines.

### 3.3 Proposed Standard Output Format (All Agents)

```markdown
## {Agent Action}: {summary}

### Dev Journal (User Transparency)
[Already implemented - user engagement section]

### Results
{agent-specific content - review findings, TDD evidence, etc.}

### Router Contract (MACHINE-READABLE)
```yaml
STATUS: PASS | FAIL | BLOCKED
CONFIDENCE: 0-100
CRITICAL_ISSUES: 0
CRITICAL_LIST:
  - {file}:{line} - {issue} → {fix}
BLOCKING: true | false
REQUIRES_REMEDIATION: true | false
MEMORY_NOTES:
  learnings: ["..."]
  patterns: ["..."]
  verification: ["..."]
```

### Task Status
- Task {TASK_ID}: COMPLETED | BLOCKED
```

### 3.4 How This Simplifies Router

**Before (current):**
```
# 100+ lines of validation logic
if agent == "component-builder":
    check TDD Evidence section
    parse exit codes from text
    verify both RED and GREEN
elif agent == "code-reviewer":
    check Critical Issues section
    parse confidence from text
    check verdict is present
elif agent == "silent-failure-hunter":
    check Router Handoff section
    parse CRITICAL_COUNT
    ...
```

**After (with standardization):**
```
# 20 lines of validation logic
parse agent.output["Router Contract"] as YAML
if contract.STATUS == "FAIL":
    create_remediation_task()
if contract.CRITICAL_ISSUES > 0:
    block_downstream()
if contract.BLOCKING:
    halt_workflow()
collect contract.MEMORY_NOTES for persistence
```

---

## Part 4: Clarification Questions - The Correct Pattern

### 4.1 Research Finding

From Claude Code docs:
> "Subagents should be designed to work WITHOUT asking clarifying questions. The parent asks clarifications first, THEN delegates to appropriately-scoped subagent."

### 4.2 What This Means for CC10x

**Current (CORRECT):**
- Router asks clarification questions BEFORE invoking agent
- Agent receives clear requirements in prompt
- Agent executes without needing to ask

**Proposed change we should NOT make:**
- ~~Move clarification questions into agents~~
- ~~Let agents ask their own questions~~

**Why this would be wrong:**
- Subagents have `context: fork` - fresh context each time
- If agent asks questions, it loses the answer when next agent runs
- Router maintains continuity across agents

### 4.3 What We CAN Improve

Router clarification questions are workflow-specific. We can:
1. Keep them in router (correct placement)
2. Make them more concise
3. Reference agent-specific needs without duplicating agent knowledge

---

## Part 5: Research Detection - The Correct Pattern

### 5.1 Current Implementation

Router detects research triggers:
- 3+ debug attempts failed
- External service error
- User explicitly requests

### 5.2 Why This Should Stay in Router

Research detection is a **routing decision**:
- It affects WHICH workflow runs (research before planner)
- It affects WHAT gets passed to agents (research findings)
- It's a cross-cutting concern (affects multiple agents)

### 5.3 What Agents CAN Do

Agents can REQUEST research when they hit a wall:
```markdown
### Agent Request
RESEARCH_NEEDED: true
RESEARCH_TOPIC: "Error handling patterns for X"
REASON: "3 local fixes attempted, all failed"
```

Router then decides whether to honor the request.

---

## Part 6: Implementation Phases

### Phase 1: Standardize Agent Output (SAFE)

**Changes:**
- Add `### Router Contract` section to all 6 agents
- Keep existing output sections (backward compatible)
- Router can parse new format OR fall back to old parsing

**Risk:** LOW - additive change only
**Bible invariants affected:** None
**Smoke test:** All existing tests pass

### Phase 2: Simplify Router Validation (SAFE)

**Changes:**
- Add new validation path that uses Router Contract
- Keep old validation as fallback
- Gradually migrate to new path

**Risk:** LOW - old code still works
**Bible invariants affected:** None (validation is internal detail)
**Smoke test:** All existing tests pass

### Phase 3: Remove Old Validation (REQUIRES CAUTION)

**Changes:**
- Remove legacy validation code from router
- All agents MUST output Router Contract

**Risk:** MEDIUM - breaking change if any agent forgot
**Bible invariants affected:** None (validation is internal)
**Smoke test:** Verify all agents output Router Contract

---

## Part 7: What Could Go Wrong

### 7.1 Phase 1 Risks

| Risk | Mitigation |
|------|------------|
| Agent forgets Router Contract section | Old parsing still works |
| YAML parsing error | Fallback to text parsing |
| Contract format changes over time | Version field in contract |

### 7.2 Phase 2 Risks

| Risk | Mitigation |
|------|------------|
| New validation misses edge case | Old validation runs in parallel |
| Performance regression | YAML parsing is fast |
| Contract fields missing | Required fields enforced |

### 7.3 Phase 3 Risks

| Risk | Mitigation |
|------|------------|
| Agent without Router Contract | Pre-flight check before merge |
| Old CC10x version incompatible | Version gate in router |
| User confusion about new format | Dev Journal provides narrative |

---

## Part 8: Decision Matrix

| Proposed Change | Safe? | Valuable? | Aligned with Claude Code? | Decision |
|-----------------|-------|-----------|---------------------------|----------|
| Move validation to agents | NO | Maybe | NO - anti-pattern | REJECT |
| Move clarification to agents | NO | No | NO - anti-pattern | REJECT |
| Move research detection to agents | NO | No | Partially | REJECT |
| Standardize agent output | YES | YES | YES | APPROVE |
| Simplify router validation | YES | YES | YES | APPROVE |

---

## Part 9: Bible Invariant Check

Before ANY change, verify against orchestration invariants:

1. ✅ Router remains ONLY entry point - unchanged
2. ✅ Memory load mandatory before decision - unchanged
3. ✅ Task-based orchestration mandatory - unchanged
4. ✅ Workflow selection uses decision tree - unchanged
5. ✅ Agent chain must complete - unchanged
6. ✅ Parallel execution in single message - unchanged
7. ✅ Research prerequisite if triggered - unchanged
8. ✅ Memory updated at workflow end - unchanged

**All invariants preserved.**

---

## Part 10: Success Criteria

### 10.1 Measurable Outcomes

| Metric | Current | Target |
|--------|---------|--------|
| Router validation lines | ~100 | ~20 |
| Agent output consistency | Variable | 100% standardized |
| Validation failure rate | Unknown | 0% false positives |
| Context window usage | High | Reduced by ~30% |

### 10.2 Quality Gates

- [ ] All 6 agents have Router Contract section
- [ ] Router parses all contracts successfully
- [ ] Smoke test passes
- [ ] 3 test workflows complete without manual intervention
- [ ] Bible invariants verified

---

## Part 11: Appendix - Claude Code Research Evidence

### A. Official Docs Quote on Subagent Responsibility

> "Subagents don't inherit skills from the parent conversation; you must list them explicitly."

This proves subagents are ISOLATED. They can't make orchestration decisions.

### B. Official Docs Quote on Validation

> "The parent conversation decides whether to act on subagent results."

This proves validation belongs in parent (router), not subagent (agent).

### C. Official Docs Quote on Clarification

> "The parent asks clarifications first, THEN delegates to appropriately-scoped subagent."

This proves router should ask questions, not agents.

---

## Conclusion

**Original hypothesis was dangerous.** Moving validation to agents would:
- Violate Claude Code design philosophy
- Break cross-agent conflict resolution
- Create silent failure paths
- Make orchestration non-deterministic

**Safe alternative identified.** Standardizing agent output:
- Keeps validation in router (correct placement)
- Simplifies validation logic (~80% reduction)
- Maintains all Bible invariants
- Aligns with Claude Code philosophy

**Recommendation:** Proceed with Phases 1-2 (standardization + simplification). Defer Phase 3 until proven stable.

---

## Part 12: EXACT IMPLEMENTATION DIFFS

### 12.1 Phase 1: Add Router Contract to Each Agent

---

#### 12.1.1 component-builder.md

**File:** `plugins/cc10x/agents/component-builder.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: PASS | FAIL
CONFIDENCE: [0-100]
TDD_RED_EXIT: [1 or missing]
TDD_GREEN_EXIT: [0 or missing]
CRITICAL_ISSUES: 0
BLOCKING: false
REQUIRES_REMEDIATION: false
REMEDIATION_REASON: null | "Missing TDD evidence - need RED exit=1 and GREEN exit=0"
MEMORY_NOTES:
  learnings: ["What was built and key patterns used"]
  patterns: ["Any new conventions discovered"]
  verification: ["TDD evidence summary"]
```

**IMPORTANT:** STATUS=PASS requires BOTH TDD_RED_EXIT=1 AND TDD_GREEN_EXIT=0
**KEY:** REMEDIATION_REASON tells router exactly what to put in REM-FIX task description
```

**Why safe:**
- ADDITIVE ONLY - no existing content removed
- Existing `### Task Status` still works
- Router can use new OR old format
- If agent forgets this section, old parsing kicks in

---

#### 12.1.2 code-reviewer.md

**File:** `plugins/cc10x/agents/code-reviewer.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: APPROVE | CHANGES_REQUESTED
CONFIDENCE: [80-100]
CRITICAL_ISSUES: [count]
CRITICAL_LIST:
  - file:line - issue → fix
HIGH_ISSUES: [count]
BLOCKING: [true if CRITICAL_ISSUES > 0]
REQUIRES_REMEDIATION: [true if CHANGES_REQUESTED]
REMEDIATION_REASON: null | "Fix critical issues: {CRITICAL_LIST summary}"
MEMORY_NOTES:
  learnings: ["Code quality insights"]
  patterns: ["Conventions or anti-patterns found"]
  verification: ["Review verdict summary"]
```
```

**Why safe:**
- ADDITIVE ONLY - existing Router Handoff section preserved
- New section is MORE structured, easier to parse
- Backward compatible - old parsing still works

---

#### 12.1.3 silent-failure-hunter.md

**File:** `plugins/cc10x/agents/silent-failure-hunter.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: CLEAN | ISSUES_FOUND
CRITICAL_ISSUES: [count]
CRITICAL_LIST:
  - file:line - issue → fix
HIGH_ISSUES: [count]
BLOCKING: [true if CRITICAL_ISSUES > 0]
REQUIRES_REMEDIATION: [true if CRITICAL_ISSUES > 0]
REMEDIATION_REASON: null | "Fix silent failures: {CRITICAL_LIST summary}"
MEMORY_NOTES:
  learnings: ["Error handling insights"]
  patterns: ["Silent failure patterns found"]
  verification: ["Hunt result summary"]
```
```

**Why safe:**
- ADDITIVE ONLY - existing Router Handoff section preserved
- Duplicates info in machine-readable format
- If conflict with old format, router uses new (more reliable)

---

#### 12.1.4 integration-verifier.md

**File:** `plugins/cc10x/agents/integration-verifier.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: PASS | FAIL
SCENARIOS_TOTAL: [count]
SCENARIOS_PASSED: [count]
BLOCKERS: [count]
BLOCKER_LIST:
  - scenario - error → action
BLOCKING: [true if STATUS=FAIL]
REQUIRES_REMEDIATION: [true if BLOCKERS > 0]
REMEDIATION_REASON: null | "Fix E2E failures: {BLOCKER_LIST summary}"
MEMORY_NOTES:
  learnings: ["Integration insights"]
  patterns: ["Edge cases discovered"]
  verification: ["E2E test results"]
```
```

**Why safe:**
- ADDITIVE ONLY
- Existing Router Handoff preserved
- Machine-readable version of same data

---

#### 12.1.5 bug-investigator.md

**File:** `plugins/cc10x/agents/bug-investigator.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: FIXED | INVESTIGATING | BLOCKED
CONFIDENCE: [0-100]
ROOT_CAUSE: "[one-line summary]"
TDD_RED_EXIT: [1 or missing]
TDD_GREEN_EXIT: [0 or missing]
VARIANTS_COVERED: [count]
BLOCKING: [true if STATUS != FIXED]
REQUIRES_REMEDIATION: [true if missing TDD or variants]
REMEDIATION_REASON: null | "Add regression test (RED→GREEN) + variant coverage"
MEMORY_NOTES:
  learnings: ["Root cause and fix approach"]
  patterns: ["Bug pattern for Common Gotchas"]
  verification: ["Regression test evidence"]
```

**IMPORTANT:** STATUS=FIXED requires TDD_RED_EXIT=1 AND TDD_GREEN_EXIT=0 AND VARIANTS_COVERED >= 1
**KEY:** Agent sets REMEDIATION_REASON if requirements not met
```

**Why safe:**
- ADDITIVE ONLY
- Existing TDD Evidence section preserved (human-readable)
- Contract is machine-readable summary

---

#### 12.1.6 planner.md

**File:** `plugins/cc10x/agents/planner.md`
**Location:** AFTER `### Task Status` section (end of output template)
**Action:** ADD (not delete anything)

```markdown
### Router Contract (MACHINE-READABLE)
```yaml
STATUS: PLAN_CREATED | NEEDS_CLARIFICATION
CONFIDENCE: [1-10]
PLAN_FILE: "[path to saved plan]"
PHASES: [count]
RISKS_IDENTIFIED: [count]
BLOCKING: false
REQUIRES_REMEDIATION: false
MEMORY_NOTES:
  learnings: ["Planning insights"]
  patterns: ["Architectural decisions"]
  verification: ["Plan confidence factors"]
```
```

**Why safe:**
- ADDITIVE ONLY
- Existing output preserved
- Contract makes plan status explicit

---

### 12.2 Phase 2: TRIM THE ROUTER

**File:** `plugins/cc10x/skills/cc10x-router/SKILL.md`

#### WEIGHT TRANSFER SUMMARY

| Component | Current Lines | After Trim | Change |
|-----------|---------------|------------|--------|
| Router validation | ~100 | ~25 | **-75 lines** |
| Router tables | ~15 | 0 | **-15 lines** |
| Agent output (each) | ~30 | ~45 | +15 lines each |
| **NET ROUTER** | **~115** | **~25** | **-90 lines** |
| **NET AGENTS (6x)** | **~180** | **~270** | +90 lines total |

**Result:** Router loses 90 lines, distributed to 6 agents (15 each). Same total, better distribution.

---

#### DELETE BLOCK 1: Required Output Table (lines 380-394)

**CURRENT (DELETE THIS):**
```markdown
### Required Output by Agent

| Agent | Mode | Required Sections | Required Evidence |
|-------|------|-------------------|-------------------|
| component-builder | WRITE | TDD Evidence (RED + GREEN) | Exit codes: 1 (RED), 0 (GREEN) |
| code-reviewer | READ-ONLY | Critical Issues, Verdict, **Memory Notes** | Confidence scores (≥80) |
| silent-failure-hunter | READ-ONLY | Critical (blocks ship), Router Handoff, **Memory Notes** | Count of issues found |
| integration-verifier | READ-ONLY | Scenarios table, Verdict, **Memory Notes** | PASS/FAIL per scenario |
| bug-investigator | WRITE | Root cause, TDD Evidence (RED + GREEN), Variant Coverage, Fix applied | Exit codes: 1 (RED), 0 (GREEN) |
| planner | WRITE | Plan saved path, Phases | Confidence score |

**Memory Notes schema (READ-ONLY agents):**
- **Learnings:** [insights for activeContext.md]
- **Patterns:** [gotchas for patterns.md]
- **Verification:** [results for progress.md]
```

**WHY DELETE:** This duplicates what agents already know. With Router Contract, each agent declares its own requirements. Router doesn't need to maintain a parallel list.

**LINES SAVED:** 15

---

#### DELETE BLOCK 2: Verbose Validation Logic (lines 396-473)

**CURRENT (DELETE THIS - 77 lines):**

```
### Validation Logic

After agent completes:

1. Check for required sections in output
2. Check for skill loading evidence (SKILL_HINTS loaded?)

3. If REQUIRED sections are missing:
   → Create remediation task (evidence-only; no code changes intended):
     TaskCreate({
       subject: "CC10X REM-EVIDENCE: {agent} missing {sections}",
       description: "Agent output incomplete..."
     })
   → Task-enforced gate...
   → STOP.

**Circuit breaker:** Before creating REM-FIX task, if count ≥ 3 → AskUserQuestion...

4. If silent-failure-hunter reports CRITICAL issues (count > 0):
   → **Conflict check:** If code-reviewer verdict is "APPROVE"...
   → Create remediation task:
     TaskCreate({ subject: "CC10X REM-FIX: Fix CRITICAL silent failures"... })
   → Block downstream tasks
   → STOP.

4b. If code-reviewer verdict is "Changes Requested":
   → Create remediation task:
     TaskCreate({ subject: "CC10X REM-FIX: Address code-reviewer issues"... })
   → Block downstream tasks
   → STOP.

5. If bug-investigator missing TDD Evidence or Variant Coverage:
   → Create remediation task:
     TaskCreate({ subject: "CC10X REM-FIX: bug-investigator missing TDD/variants"... })
   → STOP.

6. If NON-CRITICAL missing → Note for improvement, continue
7. If validation PASSES → Proceed to next agent
```

**WHY DELETE:** This is agent-specific if/else logic. With Router Contract:
- Agents declare `BLOCKING: true/false` and `REQUIRES_REMEDIATION: true/false`
- Agents include `REMEDIATION_REASON: "..."`
- Router just reads the contract - no agent-specific parsing

**LINES SAVED:** 75

---

#### REPLACEMENT: Simplified Validation (25 lines)

```markdown
### Validation Logic (Simplified via Router Contract)

```
After agent completes:

1. PARSE Router Contract:
   - Look for "### Router Contract" section
   - Parse YAML block
   - If not found → FALLBACK to legacy parsing (see 12.2.1)

2. VALIDATE Contract:
   contract = parse_yaml(agent_output)

   if contract.BLOCKING == true:
       → Create remediation task
       → Block downstream tasks
       → STOP

   if contract.REQUIRES_REMEDIATION == true:
       → Create REM-FIX task
       → Block downstream tasks
       → STOP

   if contract.CRITICAL_ISSUES > 0:
       → Log critical issues
       → If code-reviewer APPROVE + silent-failure-hunter CRITICAL:
           AskUserQuestion: "Conflict: Reviewer approved, Hunter found issues. Investigate or Skip?"

   → Collect contract.MEMORY_NOTES for workflow-final persistence
   → Proceed to next agent

3. VALIDATION EVIDENCE (include in response):
   ### Agent Validation: {agent_name}
   - Contract Found: [Yes/No]
   - Status: [contract.STATUS]
   - Blocking: [contract.BLOCKING]
   - Proceeding: [Yes/No + reason]
```

#### 12.2.1 LEGACY FALLBACK (KEEP - do not delete)

```markdown
### Legacy Validation Fallback

If Router Contract section NOT found, use original parsing:

**component-builder:** Check for "### TDD Evidence", parse exit codes from text
**code-reviewer:** Check for "### Critical Issues", parse CRITICAL_COUNT from Router Handoff
**silent-failure-hunter:** Check for "### Router Handoff", parse CRITICAL_COUNT
**integration-verifier:** Check for "### Router Handoff", parse STATUS
**bug-investigator:** Check for "### TDD Evidence" + "### Variant Coverage"
**planner:** Check for "Plan saved:" in output

This fallback ensures backward compatibility with older agent versions.
```

**Why safe:**
- OLD LOGIC PRESERVED as fallback
- New logic only activates if Router Contract exists
- If new logic fails, old logic catches it
- No behavior change for existing agents until they add Contract
- Gradual migration - each agent can add Contract independently

---

### 12.3 Phase 3: Remove Legacy Fallback (FUTURE - NOT NOW)

**DO NOT IMPLEMENT PHASE 3 until Phase 1+2 stable for 2+ weeks.**

When ready:
- DELETE the "Legacy Validation Fallback" section
- All agents MUST have Router Contract
- Add pre-flight check: `grep -l "Router Contract" plugins/cc10x/agents/*.md | wc -l` must equal 6

---

### 12.4 Safety Verification Checklist

Before implementing each phase:

#### Phase 1 (Agent Changes):
- [ ] Each change is ADDITIVE ONLY (grep for deletions = 0)
- [ ] Existing output sections unchanged
- [ ] New section follows YAML format exactly
- [ ] Run smoke test after each agent update

#### Phase 2 (Router Changes):
- [ ] Legacy fallback section EXISTS and is COMPLETE
- [ ] New validation only activates on "### Router Contract" presence
- [ ] Conflict resolution logic preserved
- [ ] Remediation loop logic preserved
- [ ] Memory Notes collection preserved
- [ ] Run smoke test
- [ ] Run 3 test workflows: BUILD, DEBUG, REVIEW

#### Phase 3 (Legacy Removal):
- [ ] All 6 agents confirmed to have Router Contract
- [ ] 2+ weeks of stable operation with Phase 1+2
- [ ] User explicitly approves removal
- [ ] Backup of legacy code saved somewhere

---

### 12.5 Rollback Plan

If anything breaks:

**Phase 1 rollback:** `git revert` the agent changes - no router impact
**Phase 2 rollback:** Legacy fallback handles everything - just remove new validation code
**Phase 3 rollback:** Restore legacy fallback section from git history

Each phase is independently reversible.

---

## Approval Required

- [ ] User approves approach
- [ ] cc10x-orchestration-safety checklist completed
- [ ] Bible sync verified
- [ ] Smoke test baseline captured

**DO NOT IMPLEMENT WITHOUT EXPLICIT APPROVAL.**
