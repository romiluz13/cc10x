---
name: session-memory
description: MANDATORY skill that MUST be loaded at start and updated at end of EVERY workflow. Persists context, learnings, decisions, and progress to .claude/cc10x/ folder. Without this, context is lost on compaction.
allowed-tools: Read, Write, Bash
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

```bash
# MUST run before ANY work
echo "=== LOADING MEMORY ==="
mkdir -p .claude/cc10x

# Load active context (CRITICAL)
if [ -f .claude/cc10x/activeContext.md ]; then
  echo "--- Active Context ---"
  cat .claude/cc10x/activeContext.md
else
  echo "No active context found - starting fresh"
fi

# Load patterns
if [ -f .claude/cc10x/patterns.md ]; then
  echo "--- Patterns ---"
  cat .claude/cc10x/patterns.md
else
  echo "No patterns found"
fi

# Load progress
if [ -f .claude/cc10x/progress.md ]; then
  echo "--- Progress ---"
  cat .claude/cc10x/progress.md
else
  echo "No progress found"
fi

echo "=== MEMORY LOADED ==="
```

### At Workflow END (REQUIRED)

**MUST update before completing ANY workflow:**

```bash
# Update active context with current state
cat > .claude/cc10x/activeContext.md << 'EOF'
# Active Context

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
[current date/time]
EOF

echo "Memory updated successfully"
```

### When Learning Patterns (APPEND)

```bash
# Append new pattern to patterns.md
cat >> .claude/cc10x/patterns.md << 'EOF'

## [Category]
- [Pattern]: [Details learned]
EOF
```

### When Completing Tasks (UPDATE)

```bash
# Update progress.md with completion status
# Include verification evidence!
```

## Integration with Agents

**ALL agents MUST:**

1. **START**: Load memory files before any work
2. **DURING**: Note learnings and decisions
3. **END**: Update memory files with new context

**Failure to update memory = incomplete work.**

## Red Flags - STOP IMMEDIATELY

### READ Red Flags
If you catch yourself:
- Starting work WITHOUT loading memory
- Making a decision WITHOUT checking Active Decisions table
- Choosing an approach WITHOUT checking patterns.md
- Building something WITHOUT checking progress.md (might be done)
- Debugging WITHOUT checking Common Gotchas
- Saying "I think we should..." without checking what we decided before

### WRITE Red Flags
If you catch yourself:
- Completing work WITHOUT updating memory
- Saying "I'll remember" instead of writing to memory
- Skipping memory because "task is small"
- Not recording a decision or learning
- Making a decision without recording the reasoning

**STOP. Load/update memory FIRST.**

## Rationalization Prevention

### READ Excuses
| Excuse | Reality |
|--------|---------|
| "I know what we decided" | You might not. Check the Active Decisions table. |
| "No patterns yet" | Check anyway. Absence of pattern is also info. |
| "Fresh project" | Still load - may have user preferences recorded. |
| "I just read it" | Conversation may have compacted. Re-read to be sure. |
| "Quick question, no need" | Quick questions often need prior context. |

### WRITE Excuses
| Excuse | Reality |
|--------|---------|
| "Small task, no need" | Small tasks have context too. Always update. |
| "I'll remember" | You won't. Conversation compacts. Write it down. |
| "Takes too long" | 30 seconds to save vs losing hours of context. |
| "Memory is optional" | Memory is MANDATORY. No exceptions. |
| "Already in conversation" | Conversation gets compacted. Files persist. |
| "Just this once skip" | One skip = lost context = repeated mistakes. |

## Verification

### READ Verification (At Start)
- [ ] All 3 memory files loaded at session/workflow start
- [ ] Active Decisions table checked before making decisions
- [ ] patterns.md checked before choosing approach
- [ ] progress.md checked before starting new work

### WRITE Verification (At End)
- [ ] Learnings documented in activeContext.md
- [ ] Decisions recorded with reasoning in Active Decisions table
- [ ] New patterns added to patterns.md
- [ ] Progress updated in progress.md
- [ ] Active context reflects current state
- [ ] Next steps documented

**Cannot check all boxes? Memory cycle incomplete. Fix before continuing.**

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
