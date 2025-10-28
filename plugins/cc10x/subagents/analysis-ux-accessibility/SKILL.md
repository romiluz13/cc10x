---
name: analysis-ux-accessibility
description: Parallel subagent for REVIEW workflow. Analyzes code for UX problems and accessibility violations. Loads ux-patterns and accessibility-patterns skills. Runs in parallel with other analysis subagents for 3x faster reviews.
---

# Analysis UX & Accessibility Subagent

**Parallel analysis of UX problems and accessibility violations.**

## When Used

Dispatched by REVIEW workflow when analyzing code for:
- User experience issues
- Usability problems
- Accessibility violations
- WCAG compliance
- Design consistency

## Workflow

**Pattern**: Parallel execution (runs simultaneously with other subagents)  
**Skills Loaded**: ux-patterns, accessibility-patterns  
**Time**: ~2-3 minutes (parallel with others)  

---

## Phase 1: Load Skills

**Load in independent context:**

1. **ux-patterns**
   - User experience design
   - Usability principles
   - User flows
   - Design consistency
   - Accessibility concerns

2. **accessibility-patterns**
   - WCAG 2.1 compliance
   - Keyboard navigation
   - Screen reader support
   - Color contrast
   - Semantic HTML

---

## Phase 2: Analyze UX

**Check for user experience issues:**

### User Experience
- [ ] Clear user flows
- [ ] Intuitive navigation
- [ ] Consistent design
- [ ] Responsive layout
- [ ] Fast load times

### Usability
- [ ] Easy to understand
- [ ] Clear labels
- [ ] Helpful error messages
- [ ] Undo/redo available
- [ ] Shortcuts available

### User Feedback
- [ ] Loading indicators
- [ ] Progress feedback
- [ ] Success messages
- [ ] Error messages
- [ ] Confirmation dialogs

### Design Consistency
- [ ] Consistent colors
- [ ] Consistent typography
- [ ] Consistent spacing
- [ ] Consistent components
- [ ] Consistent interactions

---

## Phase 3: Analyze Accessibility

**Check for accessibility violations:**

### WCAG 2.1 Compliance
- [ ] Level A compliant
- [ ] Level AA compliant
- [ ] Level AAA compliant
- [ ] No critical violations
- [ ] No major violations

### Keyboard Navigation
- [ ] All features keyboard accessible
- [ ] Tab order logical
- [ ] Focus visible
- [ ] No keyboard traps
- [ ] Shortcuts available

### Screen Reader Support
- [ ] Semantic HTML used
- [ ] ARIA labels present
- [ ] Alt text for images
- [ ] Form labels associated
- [ ] Landmarks defined

### Color & Contrast
- [ ] Sufficient contrast (4.5:1)
- [ ] Not color-only
- [ ] Color blind friendly
- [ ] High contrast mode
- [ ] Dark mode support

### Semantic HTML
- [ ] Proper heading hierarchy
- [ ] Semantic elements used
- [ ] Lists properly marked
- [ ] Tables properly marked
- [ ] Forms properly marked

---

## Phase 4: Compile Findings

**Organize UX and accessibility findings:**

### Critical Issues ð´
- WCAG violations
- Keyboard inaccessible
- Screen reader incompatible
- Major UX problems

### Important Issues ð¡
- Accessibility concerns
- UX improvements
- Usability issues
- Design inconsistencies

### Nice to Have ð¢
- UX enhancements
- Accessibility improvements
- Design refinements

---

## Phase 5: Return Results

**Provide UX and accessibility analysis:**

```markdown
## UX Analysis

### User Experience Issues
- [Issue 1]: [Description]
  - Location: [Component]
  - Impact: [Impact]
  - Fix: [Suggestion]

### Usability Problems
- [Problem 1]: [Description]
  - Location: [Component]
  - Fix: [Suggestion]

## Accessibility Analysis

### WCAG Violations
- [Violation 1]: [Description]
  - Location: [Component]
  - Level: [A/AA/AAA]
  - Fix: [Suggestion]

### Keyboard Navigation
- [Issue 1]: [Description]
  - Location: [Component]
  - Fix: [Suggestion]

### Screen Reader Support
- [Issue 1]: [Description]
  - Location: [Component]
  - Fix: [Suggestion]

### Accessibility Metrics
- WCAG compliance: X%
- Keyboard accessible: X%
- Screen reader compatible: X%
- Color contrast: X%
```

---

## Integration

**Runs in parallel with:**
- analysis-risk-security
- analysis-performance-quality

**Merged by**: review-workflow

**Result**: 3x faster code review (2-3 min vs 7 min)

