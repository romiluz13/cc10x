---
name: session-memory
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Write, Edit, Bash
---

# Session Memory (MANDATORY)

## The Iron Law

```
EVERY WORKFLOW MUST:
1. LOAD memory at START (and before key decisions)
2. UPDATE memory at END (and after learnings/decisions)
```

### READ Side (Equally Important)
**If memory is not loaded:** You work blind, repeat mistakes, lose context.
**If decisions made without checking memory:** You contradict prior choices, waste effort.

### WRITE Side
**If memory is not updated:** Next session loses everything learned.
**If learnings not recorded:** Same mistakes will be repeated.

**BOTH SIDES ARE NON-NEGOTIABLE.**

## Permission-Free Operations (CRITICAL)

**ALL memory operations are PERMISSION-FREE using the correct tools.**

| Operation | Tool | Permission |
|-----------|------|------------|
| Create memory directory | `Bash(command="mkdir -p .claude/cc10x")` | FREE |
| **Read memory files** | `Read(file_path=".claude/cc10x/activeContext.md")` | **FREE** |
| **Create NEW memory file** | `Write(file_path="...", content="...")` | **FREE** (file doesn't exist) |
| **Update EXISTING memory** | `Edit(file_path="...", old_string="...", new_string="...")` | **FREE** |
| Save plan/design files | `Write(file_path="docs/plans/...", content="...")` | FREE |

### CRITICAL: Write vs Edit

| Tool | Use For | Asks Permission? |
|------|---------|------------------|
| **Write** | Creating NEW files | NO (if file doesn't exist) |
| **Write** | Overwriting existing files | **YES - asks "Do you want to overwrite?"** |
| **Edit** | Updating existing files | **NO - always permission-free** |

**RULE: Use Write for NEW files, Edit for UPDATES.**

### CRITICAL: Use Read Tool, NOT Bash(cat)

**NEVER use Bash compound commands** (`mkdir && cat`) - they ASK PERMISSION.
**ALWAYS use Read tool** for reading files - it's PERMISSION-FREE.

```
# WRONG (asks permission - compound Bash command)
mkdir -p .claude/cc10x && cat .claude/cc10x/activeContext.md

# RIGHT (permission-free - separate tools)
Bash(command="mkdir -p .claude/cc10x")
Read(file_path=".claude/cc10x/activeContext.md")
```

**NEVER use heredoc writes** (`cat > file << 'EOF'`) - they ASK PERMISSION.
**Use Write for NEW files, Edit for EXISTING files.**

```
# WRONG (asks permission - heredoc)
cat > .claude/cc10x/activeContext.md << 'EOF'
content here
EOF

# RIGHT for NEW files (permission-free)
Write(file_path=".claude/cc10x/activeContext.md", content="content here")

# RIGHT for EXISTING files (permission-free)
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context\n\n[new content]")
```

## Why This Matters

> "My memory resets between sessions. The Memory Bank is my ONLY link to previous work."

Without memory persistence:
- Context lost on conversation compaction
- Patterns relearned from scratch
- Decisions forgotten and remade differently
- Progress tracking lost
- Same mistakes repeated

**Memory is the difference between an expert who learns and a novice who forgets.**

## Memory Structure

```
.claude/
└── cc10x/
    ├── activeContext.md   # Current focus + learnings + decisions (MOST IMPORTANT)
    ├── patterns.md        # Project patterns, conventions, gotchas
    └── progress.md        # What works, what's left, verification evidence
```

## Memory Efficiency (Token-Aware Loading)

### Quick Index Pattern (OPTIONAL)

When a memory file exceeds ~200 lines, add a Quick Index at the top for faster scanning:

```markdown
## Quick Index
| Section | Summary | Lines |
|---------|---------|-------|
| Current Focus | [1-line summary of active work] | 5-15 |
| Recent Changes | [count] changes recorded | 20-50 |
| Active Decisions | [count] decisions | 10-30 |
| Learnings | [count] insights | 15-25 |
| Blockers | [None / count active] | 5-10 |

---
[Rest of file content below...]
```

**When to add Quick Index:**
- File exceeds 200 lines
- Multiple distinct sections with significant content
- Frequent partial reads needed

**When NOT needed:**
- File under 200 lines (most projects)
- Simple, focused content
- File rarely referenced

### Selective Loading

For large memory files (200+ lines), agents MAY load selectively:

```
# Step 1: Load first 50 lines (Quick Index + Current Focus)
Read(file_path=".claude/cc10x/activeContext.md", limit=50)

# Step 2: Decide which sections are relevant to current task
# - Building new feature → Load "Active Decisions", "Patterns"
# - Debugging → Load "Learnings", "Recent Changes"
# - Continuing work → Load "Current Focus", "Next Steps"

# Step 3: Load specific sections using offset/limit
Read(file_path=".claude/cc10x/activeContext.md", offset=100, limit=50)
```

**Selective Loading Decision Matrix:**
| Task Type | Load First | Then Load If Needed |
|-----------|------------|---------------------|
| BUILD (new feature) | Current Focus, Active Decisions | Patterns, Recent Changes |
| DEBUG (fix issue) | Learnings, Recent Changes | Blockers, Patterns |
| REVIEW (audit code) | Patterns, Active Decisions | Recent Changes |
| PLAN (design) | Current Focus, Active Decisions | Full file |
| Continue session | Current Focus, Next Steps | As needed |

**DEFAULT: For files under 200 lines, load the entire file. Selective loading adds complexity—only use when needed.**

### Pruning Guidelines

Keep memory files trim for token efficiency:

**When to prune (any file exceeding 200 lines):**

| Memory File | Prune By | Move To |
|-------------|----------|---------|
| **activeContext.md** | Archive completed decisions | patterns.md (if reusable) |
| **activeContext.md** | Remove old "Recent Changes" | Keep last 10 only |
| **activeContext.md** | Move resolved blockers | progress.md "Completed" |
| **patterns.md** | Archive rarely-used patterns | Separate archive file |
| **progress.md** | Collapse old completed items | Keep last 2 workflows |

**Pruning Rules:**
1. **Recent Changes**: Keep last 10 entries. Older changes move to git history.
2. **Active Decisions**: Archive decisions older than 2 workflows if no longer referenced.
3. **Learnings**: Promote repeated learnings to patterns.md, then remove from activeContext.
4. **Completed Tasks**: Summarize completed workflows into a single line after verification.

**Pruning is a READ operation first:**
```
# Step 1: Read and assess size
Read(file_path=".claude/cc10x/activeContext.md")

# Step 2: If > 200 lines, identify prunable content
# Step 3: Move reusable content to appropriate file
# Step 4: Edit to remove old content
```

**DO NOT prune:**
- Active decisions still being referenced
- Recent learnings (< 2 sessions old)
- Unresolved blockers
- Current focus content

## Pre-Compaction Memory Safety

### Context Length Awareness

Conversations auto-compact when they get too long. If memory isn't updated before compaction, context is lost forever.

**The Risk:**
```
Long session → Auto-compact → Memory NOT updated → Context LOST
```

### Proactive Update Triggers

Update memory IMMEDIATELY when you notice:
- Extended debugging sessions (5+ error cycles)
- Long planning discussions
- Multi-file refactoring
- Any session with 30+ tool calls
- User says "we've been at this a while"

### The Rule

**When in doubt, update memory NOW.**

Don't wait for workflow end. It's better to have duplicate entries than lost context.

### Checkpoint Pattern

During long sessions, periodically checkpoint:
```
# After significant progress, even mid-task:
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Current Focus",
     new_string="## Current Focus

[Updated focus with recent progress]

### Checkpoint (mid-session)
- [Key decision made]
- [Important learning]
- [Current state]")
```

### Red Flags - Update Memory NOW

| Situation | Action |
|-----------|--------|
| "We've made several decisions" | Checkpoint decisions to activeContext.md |
| "We've been debugging for a while" | Record learnings + what we've tried |
| "Let me try a different approach" | Record why previous approach failed |
| "This is getting complex" | Update memory before continuing |

## Context Tiers (Reference Pattern)

**Optimize context for relevance, not completeness:**

### Quick Context (< 500 tokens)
Use for simple tasks and handoffs:
- Current task and immediate goals
- Recent decisions affecting current work
- Active blockers or dependencies

### Full Context (< 2000 tokens)
Use for complex tasks and session starts:
- Project architecture overview
- Key design decisions
- Integration points and APIs
- Active work streams

### Archived Context (stored in memory files)
Reference when needed:
- Historical decisions with rationale
- Resolved issues and solutions
- Pattern library
- Performance benchmarks

**Good context accelerates work; bad context creates confusion.**

## Context Management Functions (Reference Pattern)

### Context Capture (at workflow end)
1. Extract key decisions and rationale from outputs
2. Identify reusable patterns and solutions
3. Document integration points between components
4. Track unresolved issues and TODOs

### Context Distribution (at workflow start)
1. Prepare minimal, relevant context for the task
2. Maintain a context index for quick retrieval
3. Prune outdated or irrelevant information

### Memory Management (ongoing)
- Store critical project decisions in memory
- Maintain a rolling summary of recent changes
- Create context checkpoints at major milestones

## File Purposes

### activeContext.md (Read/Write EVERY session)

**Current state of work - ALWAYS check this first:**

```markdown
# Active Context

## Current Focus
[What we're actively working on RIGHT NOW]

## Recent Changes
- [Change 1] - [file:line]
- [Change 2] - [file:line]

## Next Steps
1. [Immediate next action]
2. [Following action]
3. [After that]

## Active Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| [Decision 1] | [What we chose] | [Reasoning] |
| [Decision 2] | [What we chose] | [Reasoning] |

## Learnings This Session
- [Insight 1]: [What we learned]
- [Insight 2]: [What we learned]

## Blockers / Issues
- [Blocker 1]: [Status]

## User Preferences Discovered
- [Preference]: [Details]

## Last Updated
[timestamp]
```

### patterns.md (Accumulates over time)

**Project-specific knowledge that persists:**

```markdown
# Project Patterns

## Architecture Patterns
- [Pattern]: [How this project implements it]

## Code Conventions
- [Convention]: [Example]

## File Structure
- [File type]: [Where it goes, naming convention]

## Testing Patterns
- [Test type]: [How to write, where to put]

## Common Gotchas
- [Gotcha]: [How to avoid / solution]

## API Patterns
- [Endpoint pattern]: [Convention used]

## Error Handling
- [Error type]: [How project handles it]

## Dependencies
- [Dependency]: [Why used, how configured]
```

### progress.md (Tracks completion)

**What's done, what's not:**

```markdown
# Progress Tracking

## Current Workflow
[PLAN | BUILD | REVIEW | DEBUG]

## Completed
- [x] [Task 1] - [verification evidence]
- [x] [Task 2] - [verification evidence]

## In Progress
- [ ] [Task 3] - [current status]

## Remaining
- [ ] [Task 4]
- [ ] [Task 5]

## Verification Evidence
| Check | Command | Result |
|-------|---------|--------|
| Tests | `npm test` | exit 0 (34/34) |
| Build | `npm run build` | exit 0 |

## Known Issues
- [Issue 1]: [Status]

## Evolution of Decisions
- [Date]: [Decision changed from X to Y because Z]

## Implementation Results (append-only after build)
| Planned | Actual | Deviation Reason |
|---------|--------|------------------|
| [What was planned] | [What happened] | [Why it differed] |
```

## READ Triggers - When to Load Memory

### ALWAYS Read (Non-Negotiable)

| Trigger | Action | Why |
|---------|--------|-----|
| **Session start** | Load ALL 3 files | Fresh context needed |
| **Workflow start** | Load ALL 3 files | Before BUILD/REVIEW/DEBUG/PLAN |
| **Continuation session** | Load ALL 3 files | Resume from where we left |
| **User says "continue"** | Load activeContext.md | Get current state |

### Read BEFORE These Actions

| Before This Action | Read This File | Why |
|--------------------|----------------|-----|
| **Making architectural decision** | patterns.md | Check existing patterns |
| **Choosing implementation approach** | patterns.md + activeContext.md | Align with conventions + prior decisions |
| **Starting to build something** | progress.md | Check if already done |
| **Debugging an error** | activeContext.md + patterns.md | May have seen before + known gotchas |
| **Planning next steps** | progress.md | Know what's remaining |
| **Reviewing code** | patterns.md | Apply project conventions |
| **Making any decision** | activeContext.md (Active Decisions table) | Check prior decisions |

### Read WHEN You Notice

| Situation | Action | Why |
|-----------|--------|-----|
| User references "what we did" | Load activeContext.md | Get history |
| You're about to repeat work | Load progress.md | Check if done |
| You're unsure of convention | Load patterns.md | Project standards |
| Error seems familiar | Load patterns.md (Common Gotchas) | Known issues |
| Decision feels arbitrary | Load activeContext.md | Prior reasoning |

### File Selection Matrix

```
What do I need?              → Which file?
─────────────────────────────────────────
Current state / focus        → activeContext.md
Prior decisions + reasoning  → activeContext.md (Active Decisions)
What we learned              → activeContext.md (Learnings)
Project conventions          → patterns.md
How to structure code        → patterns.md
Common gotchas to avoid      → patterns.md
What's done / remaining      → progress.md
Verification evidence        → progress.md
```

### Decision Integration

**Before ANY decision, ask:**

1. **Did we decide this before?** → Check activeContext.md Active Decisions table
2. **Is there a project pattern?** → Check patterns.md
3. **Did we learn something relevant?** → Check activeContext.md Learnings

**If memory has relevant info:**
- Follow prior decision (or document why changing)
- Apply project pattern
- Use learned insight

**If memory is empty/irrelevant:**
- Make decision
- RECORD it in activeContext.md for next time

---

## Mandatory Operations

### At Workflow START (REQUIRED)

**Use separate tool calls (PERMISSION-FREE):**

```
# Step 1: Create directory (single Bash command - permission-free)
Bash(command="mkdir -p .claude/cc10x")

# Step 2: Load ALL 3 memory files using Read tool (permission-free)
Read(file_path=".claude/cc10x/activeContext.md")
Read(file_path=".claude/cc10x/patterns.md")
Read(file_path=".claude/cc10x/progress.md")

# Step 3: Git Context - Understand project state (RECOMMENDED)
Bash(command="git status")                 # Current working state
Bash(command="git ls-files | head -50")    # Project file structure
Bash(command="git log --oneline -10")      # Recent commits
```

**NEVER use this (asks permission):**
```bash
# WRONG - compound command asks permission
mkdir -p .claude/cc10x && cat .claude/cc10x/activeContext.md
```

**If file doesn't exist:** Read tool returns an error - that's fine, means starting fresh.

### At Workflow END (REQUIRED)

**MUST update before completing ANY workflow. Use Edit tool (NO permission prompt):**

```
# First, read the existing content
Read(file_path=".claude/cc10x/activeContext.md")

# Then use Edit to replace (matches first line, replaces entire content)
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context

## Current Focus
[What we just finished / what's next]

## Recent Changes
- [Changes made this session]

## Next Steps
1. [What to do next]

## Active Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| [Decisions made] | [Choice] | [Reason] |

## Learnings This Session
- [What we learned]

## Last Updated
[current date/time]")
```

**WHY Edit not Write?** Write asks "Do you want to overwrite?" for existing files. Edit is always permission-free.

### When Learning Patterns (APPEND)

**Read existing patterns.md, then append using Edit:**

```
# Read existing content
Read(file_path=".claude/cc10x/patterns.md")

# Append by matching end of file and adding new content
Edit(file_path=".claude/cc10x/patterns.md",
     old_string="[last section heading]",
     new_string="[last section heading]

## [New Category]
- [Pattern]: [Details learned]")
```

### When Completing Tasks (UPDATE)

```
# Read progress.md, find the task, mark it complete using Edit
Read(file_path=".claude/cc10x/progress.md")

Edit(file_path=".claude/cc10x/progress.md",
     old_string="- [ ] [Task being completed]",
     new_string="- [x] [Task being completed] - [verification evidence]")
```

## Integration with Agents

**ALL agents MUST:**

1. **START**: Load memory files before any work
2. **DURING**: Note learnings and decisions
3. **END**: Update memory files with new context

**Failure to update memory = incomplete work.**

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Starting work WITHOUT loading memory
- Making decisions WITHOUT checking Active Decisions table
- Completing work WITHOUT updating memory
- Saying "I'll remember" instead of writing to memory

**STOP. Load/update memory FIRST.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what we decided" | Check the Active Decisions table. |
| "Small task, no need" | Small tasks have context too. Always update. |
| "I'll remember" | You won't. Conversation compacts. Write it down. |
| "Memory is optional" | Memory is MANDATORY. No exceptions. |

## Verification Checklist

- [ ] Memory loaded at workflow start
- [ ] Decisions checked before making new ones
- [ ] Learnings documented in activeContext.md
- [ ] Progress updated in progress.md

**Cannot check all boxes? Memory cycle incomplete.**

## The Bottom Line

```
START → Load Memory → Do Work → Update Memory → END
         ↑               ↑              ↑
      MANDATORY    Check before    MANDATORY
                   decisions
```

**The Full Cycle:**
```
1. LOAD all memory (START)
2. CHECK memory before decisions (DURING)
3. UPDATE memory with learnings (END)
```

**Memory persistence is not a feature. It's a requirement.**

Your effectiveness depends entirely on memory accuracy. Treat it with the same importance as the code itself.

READ without WRITE = Stale memory.
WRITE without READ = Contradictory decisions.
**Both are equally critical.**
