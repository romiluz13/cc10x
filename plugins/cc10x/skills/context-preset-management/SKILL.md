---
name: context-preset-management
description: Provides automatic context preset detection and loading. Use when orchestrator needs to detect task type and load appropriate context presets automatically. Detects task type from user request and file patterns, selects appropriate preset (frontend/backend/app), loads rules, and stores preset preference in memory. Works autonomously through orchestrator Phase 0 - no commands required.
allowed-tools: Read, Grep, Glob, Bash
---

# Context Preset Management

## Purpose

Automatically detect task type and load appropriate context presets for cc10x orchestrator. This skill enables task-specific context loading without requiring user commands - the orchestrator detects the task type and loads the appropriate preset automatically.

## When to Use

**Always used by orchestrator Phase 0** after functionality analysis and before skill loading. The orchestrator automatically invokes this skill to detect task type and load context presets.

## Core Principle

**Automatic Detection**: The orchestrator analyzes the user request and file patterns to determine task type, then automatically loads the appropriate context preset. No user commands required.

## Quick Start

Orchestrator automatically detects task type and loads appropriate context preset.

**Example:**

1. **User says**: "Build a React component for file upload"
2. **Orchestrator detects**: Frontend indicators ("React", "component") → Frontend task
3. **Load preset**: Automatically loads frontend context preset
4. **Store preference**: Saves preset preference in memory for future use

**Result:** Appropriate context preset loaded automatically without user commands.

## Detection Logic

### Step 1: Analyze User Request

Scan user request for task type indicators:

- **Frontend indicators**: "component", "UI", "React", "Vue", "Angular", "frontend", "client-side", "styling", "CSS", "TSX", "JSX"
- **Backend indicators**: "API", "backend", "server", "database", "service", "endpoint", "route", "controller"
- **Full-stack indicators**: "full-stack", "e2e", "end-to-end", "feature", "both", "all"

### Step 2: File Pattern Detection

Use `Glob` to detect file patterns:

```bash
# Frontend patterns
Glob("**/*.{tsx,jsx}")  # React/Vue components
Glob("src/components/**")
Glob("src/pages/**")
Glob("**/*.css")
Glob("**/*.scss")

# Backend patterns
Glob("**/api/**")
Glob("**/routes/**")
Glob("**/controllers/**")
Glob("**/services/**")
Glob("**/*.service.ts")
Glob("**/*.controller.ts")
```

### Step 3: Preset Selection

**Decision Tree**:

```
Task type detected?
├─ Frontend indicators + frontend files → frontend preset
├─ Backend indicators + backend files → backend preset
├─ Both indicators + both file types → app preset
├─ No clear indicators → Check memory for last used preset
│   └─ Found in memory → Use remembered preset
│   └─ Not found → Use default preset (app)
└─ Ambiguous → Use app preset (default)
```

### Step 4: Load Preset Rules

1. Read `.claude/context.json`
2. Select preset based on detection
3. Load alwaysApply rules (always loaded)
4. Load preset-specific rules
5. Generate context summary for orchestrator

## Integration with Orchestrator

**Called by**: Orchestrator Phase 0 (after functionality analysis, before skill loading)

**Input**: User request, file patterns detected

**Output**: Selected preset name, loaded rules list, context summary

**Memory Integration**: Stores selected preset in `.claude/memory/preset_preferences.json`

## Troubleshooting

**Common Issues:**

1. **Wrong preset detected**
   - **Symptom**: Frontend preset loaded for backend task or vice versa
   - **Cause**: Detection logic didn't match user request or file patterns
   - **Fix**: Review detection logic, check user request and file patterns
   - **Prevention**: Verify detection logic matches task type

2. **Preset not loaded**
   - **Symptom**: No preset loaded, rules missing
   - **Cause**: Orchestrator didn't invoke skill or detection failed
   - **Fix**: Verify orchestrator invoked skill, check detection logic
   - **Prevention**: Ensure orchestrator invokes skill in Phase 0

3. **Preset preference not stored**
   - **Symptom**: Preset selected but not saved to memory
   - **Cause**: Memory storage failed or wrong location
   - **Fix**: Store to `.claude/memory/preset_preferences.json`
   - **Prevention**: Always store preset preference after selection

**If issues persist:**

- Verify orchestrator invoked skill in Phase 0
- Check that detection logic matches task type
- Ensure preset preference stored to memory
- Review detection logic section

## Memory Integration

**Storage**: `.claude/memory/preset_preferences.json`

**Structure**:

```json
{
  "project_path": "/path/to/project",
  "preset": "frontend",
  "last_used": "2025-01-27T10:30:00Z",
  "usage_count": 5
}
```

**Usage**:

- Store preset preference after selection
- Load preset preference on next session
- Suggest remembered preset if task type unclear

## Implementation Steps

1. **Read context.json**: Load `.claude/context.json` to get rules and presets
2. **Detect task type**: Analyze user request and file patterns
3. **Select preset**: Use decision tree to select appropriate preset
4. **Load rules**: Combine alwaysApply rules + preset rules
5. **Generate summary**: Create context summary for orchestrator
6. **Store preference**: Save selected preset to memory

## Context Summary Format

After preset selection, generate summary:

```markdown
**Context Preset**: frontend
**Rules Loaded**:

- project-status (alwaysApply)
- app-design (alwaysApply)
- tech-stack (alwaysApply)
- react (preset)
- styling (preset)
- ui-components (preset)

**Task Type**: Frontend development
**File Patterns**: **/\*.{tsx,jsx}, src/components/**
```

## Error Handling

**If context.json missing**:

- Use default preset (app)
- Log warning: "context.json not found, using default preset"
- Continue with workflow

**If preset not found**:

- Use default preset (app)
- Log warning: "Preset '{name}' not found, using default preset"
- Continue with workflow

**If rules missing**:

- Skip missing rules
- Log warning: "Rule '{name}' not found at '{path}', skipping"
- Continue with available rules

## Examples

### Example 1: Frontend Task

**User Request**: "Build a React modal component"

**Detection**:

- User request: "React" → frontend indicator
- File patterns: `Glob("**/*.{tsx,jsx}")` → found React files
- Selection: frontend preset

**Result**: frontend preset loaded with React, styling, UI component rules

### Example 2: Backend Task

**User Request**: "Create API endpoint for user authentication"

**Detection**:

- User request: "API", "endpoint" → backend indicators
- File patterns: `Glob("**/api/**")` → found API files
- Selection: backend preset

**Result**: backend preset loaded with API, database, service rules

### Example 3: Full-Stack Task

**User Request**: "Build user authentication feature"

**Detection**:

- User request: "feature" → full-stack indicator
- File patterns: Both frontend and backend files found
- Selection: app preset

**Result**: app preset loaded with all rules

### Example 4: Ambiguous Task

**User Request**: "Review the code"

**Detection**:

- User request: No clear indicators
- File patterns: Mixed frontend and backend files
- Memory check: Last used preset was "frontend"
- Selection: frontend preset (from memory)

**Result**: frontend preset loaded (remembered preference)

## Key Principles

1. **Automatic**: No user commands required - orchestrator detects and loads automatically
2. **Memory-Aware**: Remembers preset preferences per project
3. **Fallback**: Always falls back to default preset if detection fails
4. **Non-Breaking**: Never blocks workflow execution - always continues even if preset detection fails
5. **Orchestrator-Driven**: All functionality flows through orchestrator Phase 0
