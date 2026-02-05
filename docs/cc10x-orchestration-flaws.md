# CC10x Orchestration Roadmap

> **Source of Truth:** Only `plugins/cc10x/skills/` and `plugins/cc10x/agents/` are authoritative.
> **Last updated:** 2026-02-05

---

## Priority Formula

`Priority = Impact × (6 - Fix Risk)`

| Impact | Meaning |
|--------|---------|
| 5 | Complete workflow failure |
| 4 | System produces incorrect results |
| 3 | Can ship broken code |
| 2 | Reduces efficiency |
| 1 | Minor inconvenience |

| Fix Risk | Meaning |
|----------|---------|
| 5 | Foundational change, could break everything |
| 4 | Core orchestration, high coupling |
| 3 | Multiple components, moderate coupling |
| 2 | One component, low coupling |
| 1 | Isolated change, no side effects |

---

## Open Flaws (10 Remaining)

| # | Flaw | Impact | Fix Risk | Priority | Files to Change |
|---|------|--------|----------|----------|-----------------|
| **4** | No Plan Update During Execution | 4 | 3 | **12** | Router + Planner |
| **6** | No Error Handling for Agent Failures | 4 | 3 | **12** | Router |
| **7** | PLAN Workflow No Verification | 4 | 3 | **12** | Planner |
| **9** | Memory File Corruption Recovery | 4 | 3 | **12** | Router |
| **10** | Plan File Drift Detection | 3 | 2 | **12** | component-builder |
| **11** | /cc10x:init Command | 3 | 2 | **12** | New skill |
| **12** | No Workflow Abort/Cancel | 2 | 1 | **10** | Router |
| **13** | Research Fallback No Terminal | 2 | 1 | **10** | github-research |
| **14** | User Override Without Audit | 2 | 1 | **10** | Router |
| **15** | Skills Lack Progressive Disclosure | 2 | 2 | **8** | Large skills (5-6 files) |

---

## Tier 2: High Priority (Priority 12)

### FLAW-4: No Plan Update During Execution

**Problem:** Plans are READ-ONLY after execution starts. If user discovers issues during BUILD, no mechanism to update plan. User feels "derailed" and loses orchestration power.

**Source:** User feedback - "when I identify something wrong mid-execution, I feel I've lost the full power"

**Scenario:**
```
Planner creates plan → READ-ONLY
component-builder starts following plan
User: "Wait, this approach won't work because X"
→ No way to update plan mid-execution
→ Options: A) Abort and re-plan, B) Continue with bad plan, C) Feel derailed
```

**Fix:**
```markdown
## Plan Checkpoint (Before Each Phase)

Before starting a new phase:
1. Ask user: "About to start {phase}. Any changes to plan?"
2. If changes:
   A) Append amendment to plan file (break READ-ONLY for amendments only)
   B) Update activeContext.md with amendment
   C) Continue with updated plan
3. If no changes: proceed
```

**Files:** `cc10x-router/SKILL.md`, `planner.md`

---

### FLAW-6: No Error Handling for Agent Failures

**Problem:** Router says "OR critical error detected (create error task, halt)" but no definition of "critical error" or recovery mechanism.

**Fix:** Add Error Recovery Protocol:
```markdown
## Error Recovery Protocol

On agent failure:
1. Identify error type:
   - TOOL_ERROR: Tool call failed (network, permission, etc.)
   - VALIDATION_ERROR: Output missing required sections
   - RUNTIME_ERROR: Agent crashed mid-execution

2. Recovery options:
   - RETRY: Re-invoke agent (max 2 retries)
   - SKIP: Mark task completed with warning, continue chain
   - ABORT: Delete CC10X tasks, update memory, ask user

3. Default behavior:
   - TOOL_ERROR → RETRY
   - VALIDATION_ERROR → Ask user (skip or retry?)
   - RUNTIME_ERROR → ABORT
```

**Files:** `cc10x-router/SKILL.md`

---

### FLAW-7: PLAN Workflow No Verification

**Problem:** PLAN chain has only `planner` agent. No review, no verification. Bad plans flow directly to BUILD.

**Fix:** Add self-verification checklist to planner output:
```markdown
## Plan Self-Verification (Required)

Before completing, planner MUST include:

### Plan Verification
| Criterion | Status | Evidence |
|-----------|--------|----------|
| All user requirements addressed | ✓/✗ | [list requirements → plan sections] |
| Technical feasibility confirmed | ✓/✗ | [how verified] |
| Dependencies identified | ✓/✗ | [list external deps] |
| Risk assessment included | ✓/✗ | [risks + mitigations] |
| Confidence Score | X/10 | [reasoning] |

If Confidence < 7: "⚠️ Plan requires user review before BUILD"
```

**Files:** `planner.md`

---

### ~~FLAW-8: Agent Output Parsing Fragility~~ ✅ RESOLVED (2026-02-05)

**Problem:** Router extracts findings via markdown string matching. Format variation breaks parsing silently.

**Resolution:** Implemented "Router Contract" pattern:
- All 6 agents now output `### Router Contract (MACHINE-READABLE)` section with YAML block
- Router parses contract for validation decisions (BLOCKING, REQUIRES_REMEDIATION, MEMORY_NOTES)
- Standardized fields: STATUS, CONFIDENCE, CRITICAL_ISSUES, BLOCKING, REQUIRES_REMEDIATION, REMEDIATION_REASON
- Circuit breaker: 3+ REM-FIX tasks → ask user for direction

**Changes Made:**
- +99 lines to agents (Router Contract sections)
- -97 lines from router (removed legacy validation, added contract parsing)
- Bible and orchestration docs updated

---

### FLAW-9: Memory File Corruption Recovery

**Problem:** Template Validation Gate only adds missing sections. Doesn't detect deeper corruption (duplicate headers, malformed markdown).

**Fix:** Extend Template Validation Gate:
```markdown
## Memory Corruption Detection

After loading memory, check for:
1. Duplicate section headers (grep -c "^## ")
2. Broken markdown (unclosed code blocks, malformed tables)
3. Circular references

If corruption detected:
→ "⚠️ Memory file appears corrupted: {file}"
→ "Options: A) Reset to template, B) Attempt repair, C) Continue anyway"
→ Log decision to progress.md
```

**Files:** `cc10x-router/SKILL.md`

---

### FLAW-10: Plan File Drift Detection

**Problem:** Old plan references files that no longer exist. component-builder follows stale plan.

**Fix:** Add plan freshness check:
```markdown
## Plan Freshness Check (component-builder)

If plan file provided:
1. Check plan age: `stat -f %m {plan_file}` or file header date
2. If plan > 7 days old:
   → "⚠️ Plan is {N} days old"
   → Verify key file paths still exist
   → If >50% paths missing: "Plan appears stale. Re-plan or continue?"
3. If plan fresh: proceed
```

**Files:** `component-builder.md`

---

### FLAW-11: /cc10x:init Command

**Problem:** Users who install CC10x don't have automatic activation. No AGENTS.md/CLAUDE.md in their project.

**Fix:** Create `/cc10x:init` skill:
```markdown
## /cc10x:init

Creates:
1. `.claude/cc10x/` folder with template memory files
2. `AGENTS.md` with CC10x orchestration index
3. `CLAUDE.md` symlink or content

Output:
"✓ CC10x initialized in {project}"
"Memory folder: .claude/cc10x/"
"Router active: AGENTS.md installed"
"Run any development task to start orchestration"
```

**Files:** New skill `cc10x-init/SKILL.md`

---

## Tier 3: Medium Priority (Priority 10)

### FLAW-12: No Workflow Abort/Cancel

**Problem:** No documented way to cleanly exit mid-workflow. Tasks left in limbo.

**Fix:** Add abort protocol:
```markdown
## Workflow Abort Protocol

User says "abort" / "cancel" / "stop":
1. TaskList() → Find all CC10X tasks
2. For each CC10X task with status != completed:
   → TaskUpdate({ taskId, status: "deleted" })
3. Update memory:
   → activeContext.md: "Workflow aborted: {reason}"
   → progress.md: "Aborted: {workflow} - {timestamp}"
4. Acknowledge: "Workflow aborted. Ready for new task."
```

**Files:** `cc10x-router/SKILL.md`

---

### FLAW-13: Research Fallback No Terminal

**Problem:** github-research defines fallback: Octocode → Context7 → WebFetch. No instruction if ALL fail.

**Fix:** Add terminal failure handling:
```markdown
## Research Fallback (Terminal)

If all research sources fail:
1. Log failure: "Research unavailable: {topic} - all sources failed"
2. Ask user:
   - "Provide manual context (paste docs/links)"
   - "Proceed without research (may miss best practices)"
   - "Abort workflow"
3. Record decision in activeContext.md
```

**Files:** `github-research/SKILL.md`

---

### FLAW-14: User Override Without Audit

**Problem:** User can bypass gates but no audit trail of what was bypassed and why.

**Fix:** Log bypass decisions:
```markdown
## Gate Bypass Audit

When user bypasses a gate (TDD, review, etc.):
1. Log to progress.md:
   ```
   ## Bypasses
   - {timestamp}: {gate_name} bypassed - "{user_reason}"
   ```
2. Continue workflow
3. Include in final summary: "Note: {N} gates bypassed this session"
```

**Files:** `cc10x-router/SKILL.md`

---

## Tier 4: Low Priority (Priority 8)

### FLAW-15: Skills Lack Progressive Disclosure

**Problem:** Large skills (500+ lines) load entirely into context when triggered. Per Anthropic best practices, skills should use progressive disclosure - main SKILL.md as overview pointing to detailed reference files loaded on-demand.

**Source:** Anthropic Skill Authoring Best Practices - "Keep SKILL.md body under 500 lines for optimal performance. Split content into separate files when approaching this limit."

**Current state:**
| Skill | Lines | Status |
|-------|-------|--------|
| cc10x-router | 690 | ❌ Over 500 |
| frontend-patterns | 583 | ❌ Over 500 |
| session-memory | 556 | ❌ Over 500 |
| debugging-patterns | 528 | ❌ Over 500 |
| planning-patterns | 510 | ❌ Over 500 |
| verification-before-completion | 399 | ✅ OK |

**Why this matters:** Context window is a shared resource. Loading 690 lines when 200 would suffice wastes tokens that could be used for conversation history or other context.

**Fix:** Restructure large skills into progressive disclosure pattern:

```
skills/session-memory/
├── SKILL.md              # Overview + navigation (under 300 lines)
│   - Iron Law
│   - When to Use
│   - Quick Reference (links to details)
├── TEMPLATES.md          # Memory file templates
├── READ-PROTOCOL.md      # When/how to read memory
└── WRITE-PROTOCOL.md     # Update patterns with anchors
```

**Router special case:** Router is special - it needs everything upfront for decision-making. May not benefit from splitting. See "Router Split Ideas" below.

**Implementation approach:**
1. Start with one skill (session-memory - clearest split)
2. Test that agents still load skills correctly via frontmatter
3. Verify progressive disclosure works (Claude reads reference files when needed)
4. If successful, apply to remaining skills

**Files:** `session-memory/SKILL.md`, `frontend-patterns/SKILL.md`, `debugging-patterns/SKILL.md`, `planning-patterns/SKILL.md`

**Note:** Router (690 lines) excluded from initial fix - requires special consideration.

---

## Accepted Limitations (No Fix Planned)

| Limitation | Why Accept |
|------------|------------|
| Deleted Task State Not in Router | Deleted tasks don't appear in TaskList(); implicit exclusion is sufficient |
| TDD in Untestable Contexts | Core philosophy; document alternatives instead |
| Integration-Verifier Can't Always Verify | Can't force tests to exist; improve visibility only |
| Router Single Point of Failure | Current mitigation (AGENTS.md) is best practical option |
| Confidence Scores Self-Assessed | Inherent LLM limitation; require evidence WITH confidence |
| Variant Coverage Honor System | Documentation is the intervention |
| Orchestration Assumes Good Faith | Fundamental AI limitation; evidence is verifiable |

---

## Implementation Phases

### Phase 1: Quick Wins (Router-only, ~2 hours)
| # | Flaw | Effort |
|---|------|--------|
| 6 | Error Handling (basic) | 30 min |
| 12 | Workflow Abort/Cancel | 30 min |
| 13 | Research Fallback Terminal | 30 min |
| 14 | User Override Audit | 30 min |

### Phase 2: Important (Multiple files, ~6 hours)
| # | Flaw | Effort |
|---|------|--------|
| 4 | Plan Update During Execution | 2 hours |
| 7 | PLAN No Verification | 1 hour |
| 9 | Memory Corruption | 2 hours |
| 10 | Plan File Drift | 1 hour |

### Phase 3: New Features (~2 hours)
| # | Flaw | Effort |
|---|------|--------|
| 11 | /cc10x:init Command | 2 hours |

### Phase 4: Optimization (~4 hours)
| # | Flaw | Effort |
|---|------|--------|
| 15 | Progressive Disclosure (4 skills) | 4 hours |

---

## Quick Reference

**Next action:** Start with FLAW-6 (Error Handling) - Phase 1 quick win, router-only.

**Total remaining:** 10 flaws
**Estimated total effort:** ~14 hours

---

## Resolved Flaws

| # | Flaw | Resolved | How |
|---|------|----------|-----|
| 8 | Agent Output Parsing Fragility | 2026-02-05 | Router Contract (YAML) pattern |
