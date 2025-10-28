# 🎯 LEAN ARCHITECTURE IMPLEMENTATION PLAN

## Overview

Transform cc10x from 31 skills (35% unused) to 20 lean, efficient skills while maintaining 95% use case coverage.

---

## PHASE 1: DELETE UNUSED SKILLS (11 skills)

### Skills to Delete

```
1. ui-design
   - Reason: Not used in any workflow
   - Can add later: Yes (UI design is optional)
   - Risk: Low

2. task-breakdown
   - Reason: Not used in any workflow
   - Can add later: Yes (task breakdown is optional)
   - Risk: Low

3. code-review-patterns
   - Reason: DUPLICATE of code-quality-patterns
   - Consolidation: Merge content into code-quality-patterns
   - Risk: Low (verify no unique content)

4. feature-building
   - Reason: DUPLICATE of build-workflow
   - Consolidation: Merge content into build-workflow
   - Risk: Low (verify no unique content)

5. codebase-navigation
   - Reason: Not used in any workflow
   - Can add later: Yes (codebase navigation is optional)
   - Risk: Low

6. bug-fixing
   - Reason: DUPLICATE of systematic-debugging
   - Consolidation: Merge content into systematic-debugging
   - Risk: Medium (verify LOG FIRST pattern is complete)

7. code-reviewing
   - Reason: DUPLICATE of review-workflow
   - Consolidation: Merge content into review-workflow
   - Risk: Low (verify no unique content)

8. safe-refactoring
   - Reason: Not used in any workflow
   - Can add later: Yes (refactoring is optional)
   - Risk: Low

9. verification-before-completion
   - Reason: Can be part of test-driven-development
   - Consolidation: Merge verification checklist into TDD Stage 3
   - Risk: Medium (verify TDD covers all verification points)

10. progress-tracker
    - Reason: Not used in any workflow
    - Can add later: Yes (progress tracking is optional)
    - Risk: Low

11. architecture-patterns
    - Reason: Not explicitly loaded in workflows
    - Consolidation: Merge into design-patterns
    - Risk: Medium (verify system-level design guidance is preserved)
```

### Deletion Steps

```bash
# Backup first
cp -r plugins/cc10x/skills plugins/cc10x/skills.backup

# Delete unused skills
rm -rf plugins/cc10x/skills/ui-design
rm -rf plugins/cc10x/skills/task-breakdown
rm -rf plugins/cc10x/skills/codebase-navigation
rm -rf plugins/cc10x/skills/safe-refactoring
rm -rf plugins/cc10x/skills/progress-tracker

# Delete duplicates (after merging content)
rm -rf plugins/cc10x/skills/code-review-patterns
rm -rf plugins/cc10x/skills/feature-building
rm -rf plugins/cc10x/skills/bug-fixing
rm -rf plugins/cc10x/skills/code-reviewing
rm -rf plugins/cc10x/skills/verification-before-completion
rm -rf plugins/cc10x/skills/architecture-patterns
```

---

## PHASE 2: CONSOLIDATE DESIGN PATTERNS (4 → 2)

### Create Consolidated design-patterns Skill

**Merge content from:**
- api-design-patterns
- component-design-patterns
- integration-patterns

**Into:** design-patterns/SKILL.md

**Structure:**
```
# Design Patterns

## Stage 1: Metadata
- API Design Patterns
- Component Design Patterns
- Integration Patterns

## Stage 2: Quick Reference
- API Design Checklist
- Component Design Checklist
- Integration Checklist

## Stage 3: Detailed Guide
- API Design Best Practices
- Component Design Best Practices
- Integration Best Practices
```

### Keep Separate
- architecture-patterns (system-level design, different scope)

---

## PHASE 3: UPDATE WORKFLOWS

### REVIEW Workflow (No change)
```
Skills: 6
- risk-analysis
- security-patterns
- performance-patterns
- ux-patterns
- accessibility-patterns
- code-quality-patterns
```

### PLAN Workflow (Update)
```
Skills: 6 (was 7)
- feature-planning
- requirements-analysis
- architecture-patterns
- design-patterns (consolidated)
- risk-analysis
- deployment-patterns
```

### BUILD Workflow (Update)
```
Skills: 5 (same)
- feature-planning
- requirements-analysis
- design-patterns (consolidated)
- code-generation
- test-driven-development

Subagents: 3 (was 1)
Phase 1: component-builder (parallel)
Phase 2: code-reviewer (parallel)
Phase 3: integration-verifier (parallel)
```

### DEBUG Workflow (Update)
```
Skills: 4 (same)
- systematic-debugging
- log-analysis-patterns
- root-cause-analysis
- test-driven-development

Subagents: 3 (was 1)
Phase 1: bug-investigator (parallel)
Phase 2: code-reviewer (parallel)
Phase 3: integration-verifier (parallel)
```

---

## PHASE 4: MERGE DUPLICATE CONTENT

### code-quality-patterns ← code-review-patterns
- Verify no unique content in code-review-patterns
- Merge any missing patterns
- Update description

### systematic-debugging ← bug-fixing
- Verify LOG FIRST pattern is complete
- Merge any missing debugging techniques
- Update description

### review-workflow ← code-reviewing
- Verify no unique review methodology
- Merge any missing review steps
- Update description

### test-driven-development ← verification-before-completion
- Add verification checklist to Stage 3
- Ensure all quality gates are covered
- Update description

---

## PHASE 5: UPDATE ORCHESTRATOR

Update cc10x-orchestrator/SKILL.md:
```
- Update skill count: 31 → 20
- Update workflow descriptions
- Update subagent usage
- Update efficiency metrics
```

---

## PHASE 6: UPDATE plugin.json

Update .claude-plugin/plugin.json:
```
- Update description to reflect 20 skills
- Update efficiency metrics
- Update use case coverage
```

---

## PHASE 7: TESTING & VERIFICATION

### Test Each Workflow
1. REVIEW workflow - Verify all 6 skills load correctly
2. PLAN workflow - Verify all 6 skills load correctly
3. BUILD workflow - Verify 5 skills + 3 subagents work
4. DEBUG workflow - Verify 4 skills + 3 subagents work

### Verify Use Case Coverage
- [ ] Security review still works
- [ ] Feature planning still works
- [ ] Component building still works
- [ ] Bug fixing still works
- [ ] All 95% use cases covered

### Performance Metrics
- [ ] Token usage reduced by ~15-20%
- [ ] No functionality lost
- [ ] All workflows execute successfully

---

## FINAL RESULT

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Skills | 31 | 20 | 35% ↓ |
| Unused | 11 | 0 | 100% ↓ |
| Duplicates | 3 | 0 | 100% ↓ |
| Subagent Usage | 50% | 100% | 2x ↑ |
| Efficiency | 9/10 | 9.5/10 | Better |

---

## TIMELINE

- Phase 1: 30 min (delete skills)
- Phase 2: 1 hour (consolidate patterns)
- Phase 3: 30 min (update workflows)
- Phase 4: 30 min (merge content)
- Phase 5: 15 min (update orchestrator)
- Phase 6: 15 min (update plugin.json)
- Phase 7: 1 hour (testing)

**Total: ~4 hours**

---

## ROLLBACK PLAN

If issues found:
```bash
# Restore from backup
rm -rf plugins/cc10x/skills
cp -r plugins/cc10x/skills.backup plugins/cc10x/skills
```

---

**Status**: Ready for implementation
**Risk Level**: Low (mostly deletions and consolidations)
**Approval**: Pending

