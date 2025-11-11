---
name: session-summary
description: Create comprehensive session summaries before compaction to preserve context. Use when approaching token limits, after major workflow phases, or before final deliverables. Analyzes conversation transcript to document actual accomplishments, file changes, tool usage, decisions, and next steps.
---

# Session Summary Skill

**CRITICAL**: This skill creates comprehensive session documentation to preserve context across compaction events. Use proactively before compaction or when context is large.

## When to Use

**Use this skill when**:

- Approaching token limits (75%+ usage or user indicates)
- After major workflow phase completion (Phase 4 or Phase 5)
- Before final deliverable phase (Phase 6)
- End of session or workflow completion
- User explicitly requests session summary

**Skip this skill when**:

- Context is small (<50% token usage)
- Workflow is very simple (complexity <=2)
- User explicitly skips
- No significant work has been done

## CRITICAL REQUIREMENT

**YOU MUST** output a clean, well-formatted session summary document **both in your response AND save to file** using the exact structure provided below.

## Your Task

**COMPLETE WORKFLOW** - Follow these steps in order:

### Step 1: Archive Management

1. **Check existing session**: Use Read tool on `.claude/memory/CURRENT_SESSION.md`
   - If file doesn't exist, proceed to Step 2
   - If file exists, continue to archive it

2. **Archive existing session**: If CURRENT_SESSION.md exists:
   - Create timestamp: `YYYY-MM-DD-HH-MM-SS` format
   - Ensure directory exists: `.claude/memory/session_summaries/`
   - Use Write tool to save to `.claude/memory/session_summaries/session-{timestamp}.md`
   - Copy exact content from CURRENT_SESSION.md

3. **Prune old archives**: Use ListDir or Bash tool to check `.claude/memory/session_summaries/`
   - Count existing session files (session-\*.md pattern)
   - If more than 10 files exist, delete oldest files to keep only 10 most recent
   - Use file modification times to determine age

### Step 2: Create New Session Summary

Analyze the conversation transcript and create a polished session summary document that captures:

- What actually happened (not what was planned)
- Real file changes and tool usage
- Concrete accomplishments and decisions
- Technical details and learning moments
- Current workflow state and progress
- Next steps explicitly

### Step 3: Save Session Record

Write the formatted session summary to `.claude/memory/CURRENT_SESSION.md`

## Analysis Process

1. **Parse Tool Calls**: Extract all Edit, Write, Bash, Grep, Read, CodebaseSearch tool calls with parameters
2. **Track File Changes**: List every file that was actually modified (check git status if available)
3. **Extract Commands**: Document important bash commands executed
4. **Identify Patterns**: Find architectural decisions and problem-solving approaches
5. **Capture Learning**: Note insights, discoveries, and knowledge gained
6. **Extract Workflow State**: Check for active workflow checkpoints and include current phase/progress
7. **Document Decisions**: Extract key decisions from conversation and WORKING_PLAN.md

## MANDATORY OUTPUT FORMAT

**You MUST output exactly this structure with proper formatting:**

```markdown
# 📋 Session Summary - [Month Day, Year]

## 🎯 Session Overview

[2-3 sentences describing the main focus, what was worked on, and key outcomes]

## 📁 Files Modified

### Code Changes

- **`src/path/file.ts`** - [Detailed description of what changed and why]
- **`templates/path/file.md`** - [Specific changes made with technical context]

### Documentation Updates

- **`README.md`** - [What documentation was added/updated]
- **`CLAUDE.md`** - [Any project instructions updated]

## ⚒️ Tool Calls & Operations

### File Operations

- **Edit**: `file.ts:45-67` - [What was edited]
- **Write**: `newfile.md` - [What was created]
- **Read**: `config.json` - [What was examined]

### System Commands

- **Bash**: `npm run lint:fix` - [Why command was run and result]
- **Bash**: `git commit -m "message"` - [Commit details]

## ✅ Key Accomplishments

- **[Feature/Fix Name]**: [Specific implementation details and impact]
- **[Bug Resolution]**: [Problem identified, solution implemented, verification]
- **[Architecture Change]**: [Design decision made and technical rationale]

## 🔧 Problems Solved

- **Issue**: [Problem description]
  - **Solution**: [How it was resolved with technical details]
  - **Files**: [Which files were modified]
  - **Verification**: [How solution was tested/validated]

## 💡 Technical Decisions

- **Decision**: [What was decided]
  - **Rationale**: [Why this approach was chosen]
  - **Impact**: [How this affects the project]
  - **Alternatives**: [Other options considered]

## 🔄 Next Steps

- **Immediate**: [Tasks that need to be done next session]
- **Short-term**: [Planned work for upcoming sessions]
- **Follow-up**: [Items to investigate or validate later]

## 🧠 Learning & Insights

- **Technical Patterns**: [Code patterns or architectural insights discovered]
- **Development Process**: [Process improvements or workflow learnings]
- **Project Context**: [Important project knowledge gained]

## 📊 Session Metrics

- **Duration**: [Estimated session length based on message count]
- **Tool Calls**: [Total number of tool calls made]
- **Files Changed**: [Number of files modified]
- **Commands Run**: [Number of bash commands executed]

## 🌳 Git Repository State

### Changes Made

- **Branch**: [Current branch]
- **Commits**: [Any commits made during session]
- **Modified Files**: [List from git status]
- **Status**: [Clean/dirty working tree]

### Repository Health

- **Build Status**: [If build was run, the result]
- **Tests**: [If tests were run, the result]
- **Linting**: [If linting was run, the result]

## 🔄 Active Workflow State

- **Workflow**: [Current workflow type if active]
- **Phase**: [Current phase and progress]
- **Checkpoint**: [Most recent checkpoint path if available]
- **Next Steps**: [Next phase or actions from checkpoint]
```

## Quality Requirements

- **Be Specific**: Use exact file paths, line numbers, function names
- **Show Impact**: Explain why changes matter and how they help
- **Include Details**: Technical specifics that aid future development
- **Format Consistently**: Use proper markdown, emojis, and structure
- **Focus on Facts**: Document what actually happened, not intentions
- **Add Context**: Explain the "why" behind decisions and changes
- **Include Workflow State**: Reference active workflows, phases, and checkpoints

## Integration with Workflows

This skill is integrated into all cc10x workflows:

- **Plan Workflow**: Create summary after Phase 4 (Synthesis) if context is large
- **Build Workflow**: Create summary after Phase 4 (Component Execution) if many components built
- **Review Workflow**: Create summary after Phase 4 (Synthesis) if many files reviewed
- **Debug Workflow**: Create summary after Phase 3 (Consolidation) if many bugs fixed

Workflows will call this skill in Phase 5.5 (Context Preservation) before final deliverables.

## CRITICAL REMINDERS

- **DUAL OUTPUT**: Create session document **both in your response AND save to file**
- **COMPLETE WORKFLOW**: Always follow the 3-step process (archive → analyze → save)
- **ARCHIVE MANAGEMENT**: Handle existing sessions automatically before creating new ones
- **EXACT FORMATTING**: Use the structure shown above with emojis and proper markdown
- **TECHNICAL DETAILS**: Include specific file paths, line numbers, and tool call parameters
- **PROFESSIONAL QUALITY**: Make it beautiful and comprehensive - this is permanent documentation
- **FILE PERSISTENCE**: Save formatted document to CURRENT_SESSION.md for future archiving
- **WORKFLOW INTEGRATION**: Reference active workflows, checkpoints, and next phases

## Quick Start

1. Load this skill using Skill tool
2. Execute the 3-step workflow (archive → analyze → save)
3. Output summary in conversation AND save to `.claude/memory/CURRENT_SESSION.md`
4. Document in Actions Taken: "Session summary created"

## Example Usage

```
User: "We're approaching token limits, create a session summary"

Claude: [Loads session-summary skill]
        [Executes archive management]
        [Analyzes conversation]
        [Creates comprehensive summary]
        [Saves to CURRENT_SESSION.md]
        [Outputs summary in conversation]
```
