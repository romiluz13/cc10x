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

## Approval Required

- [ ] User approves approach
- [ ] cc10x-orchestration-safety checklist completed
- [ ] Bible sync verified
- [ ] Smoke test baseline captured

**DO NOT IMPLEMENT WITHOUT EXPLICIT APPROVAL.**
