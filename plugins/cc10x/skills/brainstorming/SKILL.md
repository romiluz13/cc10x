---
name: brainstorming
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, AskUserQuestion, Write, Edit, Bash
user-invocable: false
---

# Brainstorming Ideas Into Designs

## Overview

Help turn rough ideas into fully formed designs through collaborative dialogue. Don't jump to solutions - explore the problem space first.

**Core principle:** Understand what to build BEFORE designing how to build it.
Use the user's language for domain concepts; do not invent new terminology when the repo or prompt already has a stable name for the thing.

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
# Check recent context (permission-free) — skip if commands fail (new/empty project)
Bash(command="git log --oneline -10 2>/dev/null || echo 'No git history'")
Bash(command="ls src/ 2>/dev/null || ls . 2>/dev/null || echo 'Empty project'")
```
**If project is empty/new:** Skip project scan, start from user's description.

### Phase 2: Explore the Idea (One Question at a Time)

**MANDATORY: Cover all 5 dimensions below, but only call AskUserQuestion for dimensions that are still unresolved after reading the user prompt, repo context, and any existing design/spec. Stop as soon as the intent contract is complete.**

Skip a question when the answer is already explicit and high-confidence. In that case:
- write the inferred answer into your working notes
- mention the assumption in the final design summary
- continue to the next unresolved dimension

If only 1-2 dimensions remain unclear, ask only those 1-2 questions. Do not force a 5-question interview when the request is already concrete.

**Q1 — Call AskUserQuestion NOW:**
```
AskUserQuestion({
  questions: [{
    question: "What problem does this solve for users?",
    header: "Purpose",
    multiSelect: false,
    options: [
      { label: "New feature", description: "Adding new functionality" },
      { label: "Bug fix", description: "Fixing broken behavior" },
      { label: "Refactor", description: "Improving existing code structure" },
      { label: "Something else", description: "I'll describe it" }
    ]
  }]
})
```

**Q2 — Call AskUserQuestion NOW (after Q1 answered):**
```
AskUserQuestion({
  questions: [{
    question: "Who will use this?",
    header: "Users",
    multiSelect: false,
    options: [
      { label: "Developers", description: "Engineering team or API consumers" },
      { label: "End users", description: "People using the product UI" },
      { label: "Admins", description: "Administrative or ops users" },
      { label: "Internal team", description: "Internal tooling only" }
    ]
  }]
})
```

**Q3 — Call AskUserQuestion NOW (after Q2 answered):**
```
AskUserQuestion({
  questions: [{
    question: "How will we know this works well?",
    header: "Success",
    multiSelect: false,
    options: [
      { label: "Tests pass", description: "Automated tests verify behavior" },
      { label: "Performance target met", description: "Specific speed or throughput goal" },
      { label: "User completes task", description: "End-to-end user flow works" },
      { label: "Describe it", description: "I'll type my own success criteria" }
    ]
  }]
})
```

**Q4 — Call AskUserQuestion NOW (after Q3 answered):**
```
AskUserQuestion({
  questions: [{
    question: "What limitations or requirements exist?",
    header: "Constraints",
    multiSelect: true,
    options: [
      { label: "No constraints", description: "No special requirements" },
      { label: "Performance", description: "Speed, memory, or throughput targets" },
      { label: "Security", description: "Auth, permissions, or data protection" },
      { label: "Time / deadline", description: "Must ship by a specific date" }
    ]
  }]
})
```

**Q5 — Call AskUserQuestion NOW (after Q4 answered):**
```
AskUserQuestion({
  questions: [{
    question: "What's the scope of this change?",
    header: "Scope",
    multiSelect: false,
    options: [
      { label: "Single module", description: "One focused area of the codebase (Recommended)" },
      { label: "Single file", description: "Isolated to one file" },
      { label: "Full feature", description: "Multiple files, end-to-end" },
      { label: "Cross-cutting", description: "Touches many parts of the system" }
    ]
  }]
})
```

**Optional Q6 (ask only when the user seems to have unexpressed aspirations):** "If there were no constraints, what would the ideal version look like?" This unlocks hidden requirements and aspirational features — capture them, then apply YAGNI to defer what is not essential.

**Q7 — Out-of-scope discovery (always ask):** "What is explicitly NOT part of this? What should we defer?" Document answers in the Out of Scope section of the design document. This prevents scope creep from assumptions about what "should" be included.

**After the unresolved dimensions are answered:** Proceed to Phase 3 with collected answers. Do not force the full 7-question sequence when the intent contract is already complete.

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

1. **Architecture Overview** - High-level structure (establishes shared mental model before details)
   > "Does this architecture make sense so far?"

2. **Components** - Key pieces (names the parts referenced in all later discussion)
   > "Do these components cover what you need?"

3. **Data Flow** - How data moves (validates components actually connect — catches orphaned pieces)
   > "Does this data flow work for your use case?"

4. **Error Handling** - What can go wrong (only meaningful after happy path is agreed)
   > "Are these error cases covered?"

5. **Testing Strategy** - How to verify (depends on all prior sections being stable)
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
- Asking leading questions that steer toward a pre-decided solution ("Should we use React?" instead of "What UI approach fits?")
- Asking compound questions (more than one decision per question)
- Accepting vague answers without probing ("It should be fast" → "What response time is acceptable?")

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
# Resolve absolute project directory FIRST (prevents wrong-CWD save — CC10X-006)
Bash(command="pwd")  # Store output as PROJECT_DIR
# Example: if pwd = /workspace/github-horoscope, use that as prefix

# Create directory using absolute path
Bash(command="mkdir -p {PROJECT_DIR}/docs/plans")

# Then save design using Write tool (permission-free)
# IMPORTANT: Use absolute path. Relative paths save to workspace root, not project dir.
Write(file_path="{PROJECT_DIR}/docs/plans/YYYY-MM-DD-<feature>-design.md", content="[full design content from template above]")
# Naming convention: always use -design.md suffix (brainstorming output) vs -plan.md suffix (planner output) — prevents collision in docs/plans/

# Do NOT auto-commit — let the user decide when to commit
```

### Step 2: Update Memory (CRITICAL - Links Design to Memory)

**Use Read-Edit-Verify with stable anchors:**

```
# Step 1: READ
Read(file_path=".claude/cc10x/v10/activeContext.md")

# Step 2: VERIFY anchors exist (## References, ## Recent Changes, ## Next Steps)

# Step 3: EDIT using stable anchors
# Add design to References
Edit(file_path=".claude/cc10x/v10/activeContext.md",
     old_string="## References",
     new_string="## References\n- Design: `{PROJECT_DIR}/docs/plans/YYYY-MM-DD-<feature>-design.md`")

# Index the design creation in Recent Changes
Edit(file_path=".claude/cc10x/v10/activeContext.md",
     old_string="## Recent Changes",
     new_string="## Recent Changes\n- Design saved: docs/plans/YYYY-MM-DD-<feature>-design.md")

# Make the next step explicit
Edit(file_path=".claude/cc10x/v10/activeContext.md",
     old_string="## Next Steps",
     new_string="## Next Steps\n1. [BRAINSTORM-DONE] Planner agent pending — design at docs/plans/YYYY-MM-DD-<feature>-design.md")

# Step 4: VERIFY (do not skip)
Read(file_path=".claude/cc10x/v10/activeContext.md")
```

**WHY BOTH:** Design files are artifacts. Memory is the index. Without memory update, next session won't know the design exists.

**This is non-negotiable.** Memory is the single source of truth.

## Pre-Handoff Design Check (Optional)

Before presenting the saved design to the user, consider reviewing it for:

- **Architecture:** Does this follow existing codebase patterns? Are dependencies sound? Are integration points clean?
- **Security:** Auth/authz at every entry point? Input validation defined? No secrets in design?

If concerns found, revise the design file before presenting. This is a self-review — no agents spawned.

## After Brainstorming

**Announce to the user:**

> "Design saved to `{design_file_path}`. Memory updated with design reference."

The router handles workflow transitions — do not prompt the user for next steps. The router will proceed to research and/or planning automatically.

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
