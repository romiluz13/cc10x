---
name: brainstorming
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Brainstorming Ideas Into Designs

## Overview

Help turn rough ideas into fully formed designs through collaborative dialogue. Don't jump to solutions - explore the problem space first.

**Core principle:** Understand what to build BEFORE designing how to build it.

**Violating the letter of this process is violating the spirit of brainstorming.**

## The Iron Law

```
NO DESIGN WITHOUT UNDERSTANDING PURPOSE AND CONSTRAINTS
```

If you can't articulate why the user needs this and what success looks like, you're not ready to design.

## When to Use

**ALWAYS before:**
- Creating new features
- Building new components
- Adding new functionality
- Modifying existing behavior
- Making architectural decisions

**Signs you need to brainstorm:**
- Requirements feel vague
- Multiple approaches seem valid
- Success criteria unclear
- User intent ambiguous

## Spec File Workflow (Optional)

If user references a spec file (SPEC.md, spec.md, plan.md):

1. **Read existing spec** - Use as interview foundation
2. **Interview to expand** - Fill gaps using Phase 2 questions
3. **Write back** - Save expanded design to same file

```
# Check for existing spec (permission-free)
Read(file_path="SPEC.md")  # or spec.md if that doesn't exist
```

## The Process

### Phase 1: Understand Context

**Before asking questions:**

1. Check project state (files, docs, recent commits)
2. Understand what exists
3. Identify relevant patterns

```
# Check recent context (permission-free)
Bash(command="git log --oneline -10")
Bash(command="ls -la src/")  # or relevant directory
```

### Phase 2: Explore the Idea (One Question at a Time)

**Use `AskUserQuestion` tool** - provides multiple choice options, better UX than text questions.

**Ask questions sequentially, not all at once.**

**Question 1: Purpose**
> "What problem does this solve for users?"

Options format:
> A. [Specific use case 1]
> B. [Specific use case 2]
> C. Something else (please describe)

**Question 2: Users**
> "Who will use this feature?"

**Question 3: Success Criteria**
> "How will we know this works well?"

**Question 4: Constraints**
> "What limitations or requirements exist?"
> (Performance, security, compatibility, timeline)

**Question 5: Scope**
> "What's explicitly OUT of scope for this?"

### Phase 3: Explore Approaches

**Always present 2-3 options with trade-offs:**

```markdown
## Approaches

### Option A: [Name] (Recommended)
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Why recommended**: [Reasoning]

### Option B: [Name]
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]

### Option C: [Name]
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]

Which direction feels right?
```

### Phase 4: Present Design Incrementally

**Once approach chosen, present design in sections (200-300 words each):**

1. **Architecture Overview** - High-level structure
   > "Does this architecture make sense so far?"

2. **Components** - Key pieces
   > "Do these components cover what you need?"

3. **Data Flow** - How data moves
   > "Does this data flow work for your use case?"

4. **Error Handling** - What can go wrong
   > "Are these error cases covered?"

5. **Testing Strategy** - How to verify
   > "Does this testing approach give you confidence?"

**After each section, ask if it looks right before continuing.**

## Key Principles

### One Question at a Time
```
✅ "What problem does this solve?"
   [Wait for answer]
   "Who will use it?"
   [Wait for answer]

❌ "What problem does this solve, who will use it,
    what are the constraints, and what's the success criteria?"
```

### Multiple Choice Preferred
```
✅ "Which approach fits better?
    A. Simple file-based storage
    B. Database with caching
    C. External service integration"

❌ "How do you want to handle storage?"
```

### YAGNI Ruthlessly
```
✅ "You mentioned analytics - is that needed for v1
    or can we defer it?"

❌ Adding analytics, caching, and multi-tenancy
   because "we might need them later"
```

### Explore Alternatives
```
✅ Presenting 3 approaches with trade-offs
   before asking which to pursue

❌ Jumping straight to your preferred solution
```

### Incremental Validation
```
✅ "Here's the data model [200 words].
    Does this match your mental model?"

❌ Presenting the entire design in one 2000-word block
```

## Red Flags - STOP and Ask More Questions

If you find yourself:

- Designing without knowing the purpose
- Jumping to implementation details
- Presenting one approach without alternatives
- Asking multiple questions at once
- Assuming you know what the user wants
- Not validating incrementally

**STOP. Go back to Phase 2.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what they need" | Ask. You might be wrong. |
| "Multiple questions is faster" | Overwhelms. One at a time. |
| "One approach is obviously best" | Present options. Let them choose. |
| "They'll say if it's wrong" | Validate incrementally. Don't assume. |
| "Details can wait" | Get details now. Assumptions cause rework. |

## Output: Design Document

After brainstorming, save the validated design:

```markdown
# [Feature Name] Design

## Purpose
[What problem this solves]

## Users
[Who will use this]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

## Approach Chosen
[Which option and why]

## Architecture
[High-level structure]

## Components
[Key pieces]

## Data Flow
[How data moves]

## Error Handling
[What can go wrong and how handled]

## Testing Strategy
[How to verify]

## Observability (if applicable)
- Logging: [what to log]
- Metrics: [what to track]
- Alerts: [when to alert]

## UI Mockup (if applicable)
[ASCII mockup for UI features]

## Questions Resolved
- Q: [Question asked]
  A: [Answer given]
```

## UI Mockup (For UI Features Only)

For UI features, include ASCII mockup in the design:

```
┌─────────────────────────────────────────┐
│  [Component Name]                       │
├─────────────────────────────────────────┤
│  [Header/Navigation]                    │
├─────────────────────────────────────────┤
│                                         │
│  [Main content area]                    │
│                                         │
│  [Input fields, buttons, etc.]          │
│                                         │
├─────────────────────────────────────────┤
│  [Footer/Actions]                       │
└─────────────────────────────────────────┘
```

**Skip this for API-only or backend features.**

## Saving the Design (MANDATORY)

**Two saves are required - design file AND memory update:**

### Step 1: Save Design File (Use Write tool - NO PERMISSION NEEDED)

```
# First create directory
Bash(command="mkdir -p docs/plans")

# Then save design using Write tool (permission-free)
Write(file_path="docs/plans/YYYY-MM-DD-<feature>-design.md", content="[full design content from template above]")

# Then commit (separate commands to avoid permission prompt)
Bash(command="git add docs/plans/*.md")
Bash(command="git commit -m 'docs: add <feature> design'")
```

### Step 2: Update Memory (CRITICAL - Links Design to Memory)

**Use Edit tool (NO permission prompt):**

```
# First read existing content
Read(file_path=".claude/cc10x/activeContext.md")

# Then use Edit to replace (matches first line, replaces entire content)
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context

## Current Focus
Design created for [feature]. Ready for planning or building.

## Recent Changes
- Design saved to docs/plans/YYYY-MM-DD-<feature>-design.md

## Next Steps
1. Create implementation plan (if complex)
2. Or start building directly (if simple)
3. Reference design at docs/plans/YYYY-MM-DD-<feature>-design.md

## Active Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| [Key decisions from design] | [Choice] | [Reason] |

## Design Reference
**Design:** `docs/plans/YYYY-MM-DD-<feature>-design.md`

## Last Updated
[current date/time]")
```

**WHY BOTH:** Design files are artifacts. Memory is the index. Without memory update, next session won't know the design exists.

**This is non-negotiable.** Memory is the single source of truth.

## After Brainstorming

**Ask the user:**

> "Design captured. What's next?"
> A. Create implementation plan (use planning-patterns skill)
> B. Start building (use build workflow)
> C. Review and refine further

## Final Check

Before completing brainstorming:

- [ ] Purpose clearly articulated
- [ ] Users identified
- [ ] Success criteria defined
- [ ] Constraints documented
- [ ] Out of scope explicit
- [ ] Multiple approaches explored
- [ ] Design validated incrementally
- [ ] Document saved
