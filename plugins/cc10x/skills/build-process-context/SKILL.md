---
name: build-process-context
description: This skill should be used when starting ANY workflow (build, plan, review, debug, validate), at session start, or when user says "load context", "where are we", "continue", "resume", "what's the status", "next steps". MANDATORY for ALL workflows - ensures perfect AI context across sessions. Must load BEFORE other skills.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Build Process Context - Perfect AI Memory Across Sessions

## 🚨 THIS IS AUTOMATIC - NO MANUAL STEPS REQUIRED 🚨

The orchestrator handles everything automatically:
- **AUTO-INIT**: Creates folders if they don't exist
- **AUTO-LOAD**: Reads context at session/workflow start
- **AUTO-UPDATE**: Updates after each phase
- **AUTO-SAVE**: Saves state at workflow end

**You just code. The system remembers.**

## Purpose

Maintain perfect context for AI coding across different chat sessions. This is the MOST CRITICAL capability of cc10x - without it, every session starts blind. With it, AI picks up exactly where it left off.

**Core Value**: Load 3 files, get full context. Updates happen automatically.

## The 5-Folder System

Location: `.claude/build-process/`

| Folder | Purpose | Key Files |
|--------|---------|-----------|
| **requirements/** | WHAT we're building | REQUIREMENTS.md, user-stories.md, constraints.md |
| **decisions/** | WHY this approach | DECISIONS-INDEX.md, ADR-*.md, rejected-approaches.md |
| **progress/** | WHERE we are now | STATUS.md, NEXT-STEPS.md, blockers.md |
| **learnings/** | WHAT we discovered | patterns.md, gotchas.md, solutions.md |
| **context/** | HOW things connect | CONTEXT-SNAPSHOT.md, architecture.md, file-map.md |

## Mandatory Protocols

### Session Start Protocol (ALWAYS FIRST)

Before ANY work, read these 3 files in order:

```bash
# Quick context load - run at session start
cat .claude/build-process/progress/STATUS.md
cat .claude/build-process/progress/NEXT-STEPS.md
cat .claude/build-process/context/CONTEXT-SNAPSHOT.md
```

**Enforcement**: Do NOT proceed with any workflow until these files are read.

### Session End Protocol (ALWAYS LAST)

Before session ends, update:

1. `progress/STATUS.md` - Current state summary
2. `progress/NEXT-STEPS.md` - What to do next (prioritized)
3. `progress/in-progress.md` - Any work in flight

**Enforcement**: Do NOT end session without updating these files.

### Workflow Update Protocol

After EACH workflow phase, update relevant folders:

| Workflow | Update After Phase |
|----------|-------------------|
| BUILD | progress/, decisions/, learnings/ |
| PLAN | requirements/, decisions/, context/ |
| REVIEW | learnings/, progress/ |
| DEBUG | learnings/, progress/ |
| VALIDATE | progress/ |

## File Templates

### STATUS.md (Most Critical File)

```markdown
## Current State
[One sentence: what's happening right now]

## Last Session
- Date: [YYYY-MM-DD HH:MM]
- What was done: [2-3 bullet summary]
- Exit state: [clean/in-progress/blocked]

## Active Work
- Component: [name or "none"]
- Phase: [workflow phase]
- Status: [status description]

## Critical Context
- [Key fact 1 that AI must know]
- [Key fact 2 that AI must know]
- [Key fact 3 that AI must know]

## Blockers
[None / list of blockers with status]
```

### NEXT-STEPS.md (Action Priority)

```markdown
## Immediate (Do First)
1. [Highest priority action]
2. [Second priority action]

## Soon (After Immediate)
- [Action with context]
- [Action with context]

## Later (When Time Permits)
- [Future action]

## Dependencies
- [Action X] depends on [Action Y]
```

### CONTEXT-SNAPSHOT.md (Project Overview)

```markdown
## Project
[One paragraph: what this project is and its purpose]

## Tech Stack
- Language: [language]
- Framework: [framework]
- Key Libraries: [list]

## Architecture
[Brief architecture description - how components connect]

## Key Files
- `path/to/file` - [purpose]
- `path/to/file` - [purpose]

## Current Focus
[What area of codebase is being worked on]
```

## Initialization

Run this command to create the folder structure:

```bash
bash plugins/cc10x/skills/build-process-context/scripts/init-build-process.sh
```

Or manually create:

```bash
mkdir -p .claude/build-process/{requirements,decisions,progress,learnings,context}
```

## Integration with Workflows

### Before Any Workflow Starts

```
1. Load build-process-context skill (this skill)
2. Execute Session Start Protocol (read 3 files)
3. Proceed with workflow
```

### After Any Workflow Ends

```
1. Execute Workflow Update Protocol
2. Execute Session End Protocol (update 3 files)
3. Workflow complete
```

## Validation Gates

**Pre-Workflow Gate** (before starting):
- [ ] STATUS.md exists and was read
- [ ] NEXT-STEPS.md exists and was read
- [ ] CONTEXT-SNAPSHOT.md exists and was read

**Post-Phase Gate** (after each phase):
- [ ] Relevant progress/ files updated
- [ ] Any new decisions recorded in decisions/
- [ ] Any learnings recorded in learnings/

**Post-Workflow Gate** (after completion):
- [ ] STATUS.md updated with new state
- [ ] NEXT-STEPS.md updated with new priorities
- [ ] CONTEXT-SNAPSHOT.md updated if architecture changed

## Automatic Update Functions

Use these Edit tool patterns to auto-update context:

### Update STATUS.md (After Each Phase)

Use Edit tool to update the "Current State" and "Active Work" sections:

```
Edit file: .claude/build-process/progress/STATUS.md
old_string: "## Current State\n[previous state]"
new_string: "## Current State\n[new state description]"
```

### Update NEXT-STEPS.md (When Priorities Change)

Use Edit tool to update "Immediate" section:

```
Edit file: .claude/build-process/progress/NEXT-STEPS.md
old_string: "## Immediate (Do First)\n[old priorities]"
new_string: "## Immediate (Do First)\n1. [new top priority]\n2. [second priority]"
```

### Add to completed.md (After Component/Feature Done)

Use Edit tool to prepend new completion:

```
Edit file: .claude/build-process/progress/completed.md
old_string: "# Completed Work"
new_string: "# Completed Work\n\n## [Today's Date]\n\n### [Component Name]\n- **What**: [description]\n- **Evidence**: [test results, exit codes]\n- **Files**: [files changed]"
```

### Add Learning (When Pattern/Gotcha Discovered)

Use Edit tool to add to relevant file:

```
Edit file: .claude/build-process/learnings/patterns.md
old_string: "# Codebase Patterns"
new_string: "# Codebase Patterns\n\n### [Pattern Name]\n**Location**: `path/to/file`\n**Use When**: [description]\n**Example**: [code]"
```

## Quick Reference

**Load Context Fast**:
```bash
cat .claude/build-process/progress/STATUS.md && \
cat .claude/build-process/progress/NEXT-STEPS.md
```

**Check What's Tracked**:
```bash
ls -la .claude/build-process/*/
```

## Additional Resources

### Reference Files

For detailed specifications:
- **`references/folder-structure.md`** - Complete folder/file specifications
- **`references/templates.md`** - All file templates with examples
- **`references/enforcement-rules.md`** - Detailed enforcement mechanisms

### Scripts

- **`scripts/init-build-process.sh`** - Initialize folder structure with templates

### Examples

- **`examples/example-project/`** - Complete example of populated build-process folder

## Why This Matters

Without this system:
- Every session starts blind
- Decisions get repeated or contradicted
- Progress gets lost
- Context gets forgotten
- AI codes worse over time

With this system:
- Sessions resume instantly
- Decisions are traceable
- Progress is preserved
- Context is always available
- AI codes better over time

**This is the foundation of continuous AI-assisted development.**
