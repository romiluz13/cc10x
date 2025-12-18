# Build Process Context - Enforcement Rules

## Core Principle

**The build process context system only works if it's updated religiously.**

Without enforcement, files become stale and useless. With enforcement, context is always accurate.

## Mandatory Load Order

### At Session Start

**ALWAYS execute this sequence before ANY work:**

```
1. Load build-process-context skill
2. Read .claude/build-process/progress/STATUS.md
3. Read .claude/build-process/progress/NEXT-STEPS.md
4. Read .claude/build-process/context/CONTEXT-SNAPSHOT.md
5. Acknowledge context loaded
6. Begin workflow
```

**If files don't exist:**
- Run initialization script
- Create minimal templates
- Then proceed

**Enforcement Check:**
```bash
# Verify context files exist
[ -f ".claude/build-process/progress/STATUS.md" ] && \
[ -f ".claude/build-process/progress/NEXT-STEPS.md" ] && \
[ -f ".claude/build-process/context/CONTEXT-SNAPSHOT.md" ] && \
echo "Context ready" || echo "STOP: Initialize build-process first"
```

## Update Triggers

### Must Update Immediately

| Event | Files to Update |
|-------|-----------------|
| Session start | Read STATUS.md, NEXT-STEPS.md, CONTEXT-SNAPSHOT.md |
| Decision made | decisions/DECISIONS-INDEX.md, decisions/ADR-*.md |
| Approach rejected | decisions/rejected-approaches.md |
| Component completed | progress/completed.md, progress/STATUS.md |
| Blocker discovered | progress/blockers.md, progress/STATUS.md |
| Blocker resolved | progress/blockers.md |
| Pattern discovered | learnings/patterns.md |
| Gotcha found | learnings/gotchas.md |
| Solution found | learnings/solutions.md |
| Failure encountered | learnings/failures.md |
| Architecture changed | context/architecture.md, context/CONTEXT-SNAPSHOT.md |
| Session end | progress/STATUS.md, progress/NEXT-STEPS.md |

### Workflow-Specific Updates

#### BUILD Workflow

| Phase | Update After |
|-------|-------------|
| Phase 0 (Functionality Analysis) | requirements/REQUIREMENTS.md, context/CONTEXT-SNAPSHOT.md |
| Phase 1 (Complexity Gate) | progress/STATUS.md |
| Phase 2 (Shared Context) | context/file-map.md, learnings/patterns.md |
| Phase 3 (Component Queue) | progress/in-progress.md |
| Phase 4 (Component Loop) | progress/in-progress.md, progress/completed.md per component |
| Phase 5 (Verification) | progress/completed.md, learnings/solutions.md |
| Phase 6 (Delivery) | progress/STATUS.md, progress/NEXT-STEPS.md |

#### PLAN Workflow

| Phase | Update After |
|-------|-------------|
| Phase 0 (Requirements) | requirements/REQUIREMENTS.md, requirements/user-stories.md |
| Phase 1 (Analysis) | requirements/constraints.md, context/CONTEXT-SNAPSHOT.md |
| Phase 2 (Design) | decisions/ADR-*.md, context/architecture.md |
| Phase 3 (Delivery) | progress/STATUS.md, progress/NEXT-STEPS.md |

#### REVIEW Workflow

| Phase | Update After |
|-------|-------------|
| Findings | learnings/patterns.md, learnings/gotchas.md |
| Recommendations | progress/NEXT-STEPS.md |
| Completion | progress/STATUS.md |

#### DEBUG Workflow

| Phase | Update After |
|-------|-------------|
| Investigation | learnings/gotchas.md, learnings/failures.md |
| Fix | learnings/solutions.md, progress/completed.md |
| Verification | progress/STATUS.md |

## Validation Gates

### Pre-Workflow Gate

**Before starting ANY workflow, validate:**

```bash
# Check all critical files exist and are recent
CHECK_PASSED=true

# STATUS.md must exist
if [ ! -f ".claude/build-process/progress/STATUS.md" ]; then
    echo "FAIL: STATUS.md missing"
    CHECK_PASSED=false
fi

# NEXT-STEPS.md must exist
if [ ! -f ".claude/build-process/progress/NEXT-STEPS.md" ]; then
    echo "FAIL: NEXT-STEPS.md missing"
    CHECK_PASSED=false
fi

# CONTEXT-SNAPSHOT.md must exist
if [ ! -f ".claude/build-process/context/CONTEXT-SNAPSHOT.md" ]; then
    echo "FAIL: CONTEXT-SNAPSHOT.md missing"
    CHECK_PASSED=false
fi

if [ "$CHECK_PASSED" = true ]; then
    echo "PASS: Pre-workflow gate passed"
else
    echo "STOP: Initialize build-process or update files"
fi
```

### Post-Phase Gate

**After EACH workflow phase, validate updates:**

Checklist (must verify):
- [ ] Relevant folder files updated
- [ ] STATUS.md reflects current state
- [ ] No stale information preserved
- [ ] Evidence/file references included where applicable

### Post-Workflow Gate

**Before marking workflow complete:**

- [ ] STATUS.md updated with completion state
- [ ] NEXT-STEPS.md updated with new priorities
- [ ] All learnings captured in learnings/
- [ ] All decisions captured in decisions/
- [ ] CONTEXT-SNAPSHOT.md reflects any architecture changes

## Staleness Prevention

### Maximum Age Rules

| File | Max Age | Action if Stale |
|------|---------|-----------------|
| STATUS.md | 1 session | Update at session start/end |
| NEXT-STEPS.md | 1 session | Review and update priorities |
| in-progress.md | 1 session | Archive or update |
| CONTEXT-SNAPSHOT.md | 1 week | Review for accuracy |
| Others | 1 month | Review for relevance |

### Staleness Check

```bash
# Check if STATUS.md was modified today
if [ "$(date -r .claude/build-process/progress/STATUS.md +%Y%m%d)" != "$(date +%Y%m%d)" ]; then
    echo "WARNING: STATUS.md not updated today - review needed"
fi
```

## Error Recovery

### Missing Files

If critical files missing:

1. Check if `.claude/build-process/` exists
2. If not, run initialization script
3. If folder exists but files missing, create from templates
4. Document the recovery in progress/STATUS.md

### Corrupted Files

If files appear corrupted or inconsistent:

1. Check git history for previous versions
2. Restore from git if available
3. If not in git, recreate from memory/context
4. Document the recovery

### Conflicting Information

If information conflicts between files:

1. Prioritize: STATUS.md > in-progress.md > completed.md
2. For decisions: Most recent ADR takes precedence
3. Resolve conflict and update all affected files
4. Document resolution in learnings/gotchas.md

## Integration Points

### With Orchestrator

The cc10x-orchestrator MUST:
- Load build-process-context skill FIRST (before other skills)
- Execute Session Start Protocol before workflow
- Enforce Post-Phase Gates after each phase
- Execute Session End Protocol after workflow

### With Subagents

Subagents SHOULD:
- Read relevant context files before starting
- Update learnings/ with discoveries
- Report status that gets captured in progress/

### With Memory System

Build-process-context complements (not replaces) existing memory:
- `.claude/memory/` = Technical state (checkpoints, patterns cache)
- `.claude/build-process/` = Human-readable project knowledge

## Non-Negotiable Rules

1. **NEVER skip Session Start Protocol** - Always read context first
2. **NEVER skip Session End Protocol** - Always update before ending
3. **NEVER leave in-progress.md stale** - Update or archive
4. **NEVER make decisions without recording** - Always add to decisions/
5. **NEVER encounter a gotcha without documenting** - Always add to learnings/
6. **NEVER complete work without evidence** - Always include file:line, exit codes

## Consequences of Non-Compliance

If enforcement is bypassed:
- Context becomes stale
- Next session starts blind
- Decisions get forgotten
- Work gets repeated
- AI performance degrades

**The entire value of cc10x depends on religious adherence to these rules.**
