# Hooks - Event-Driven Automation

## Overview

Hooks execute custom commands automatically when specific events occur in Claude Code.

## Configuration Location

```
~/.claude/settings.json          # User hooks
.claude/settings.json            # Project hooks
.claude/settings.local.json      # Local (not committed)
<plugin>/hooks/hooks.json        # Plugin hooks
```

## Hook Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // Optional for some events
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60  // Optional: seconds
          }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | When | Matcher |
|-------|------|---------|
| **PreToolUse** | Before tool executes | Tool name |
| **PostToolUse** | After tool executes | Tool name |
| **UserPromptSubmit** | User submits prompt | None |
| **Notification** | Claude sends notification | None |
| **Stop** | Main agent stops | None |
| **SubagentStop** | Subagent stops | None |
| **PreCompact** | Before context compact | `manual`, `auto` |
| **SessionStart** | Session starts | `startup`, `resume`, `clear`, `compact` |
| **SessionEnd** | Session ends | None |

## Matchers

Tool matchers are **case-sensitive** and support regex:

```json
// Exact match
"matcher": "Write"

// Multiple tools
"matcher": "Write|Edit"

// Regex pattern  
"matcher": "Notebook.*"

// All tools
"matcher": "*"
"matcher": ""  // or omit matcher
```

## Common Tool Names

- `Read`, `Write`, `Edit`
- `Bash`, `Grep`, `Glob`
- `Task` (subagent invocation)
- `WebFetch`, `WebSearch`
- MCP tools: `mcp__server__tool`

## Hook Examples

### 1. Code Formatting (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

### 2. Git Auto-Commit (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "git add . && git commit -m 'Auto-commit: Claude changes'"
          }
        ]
      }
    ]
  }
}
```

### 3. Notification (Desktop Alert)

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"$MESSAGE\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 4. Session Setup (SessionStart)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/setup-env.sh"
          }
        ]
      }
    ]
  }
}
```

### 5. Prompt Validation (UserPromptSubmit)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python $CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Input (JSON via stdin)

All hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/conversation.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

## Hook Output (Two Methods)

### Method 1: Exit Codes (Simple)

```bash
exit 0   # Success - stdout shown to user
exit 2   # Blocking error - stderr fed to Claude
exit 1   # Non-blocking error - stderr shown to user
```

**Exit Code 2 Behavior**:

| Event | Behavior |
|-------|----------|
| PreToolUse | Blocks tool call, shows stderr to Claude |
| PostToolUse | Shows stderr to Claude (tool already ran) |
| UserPromptSubmit | Blocks prompt, erases prompt, shows stderr to user |
| Stop | Blocks stoppage, shows stderr to Claude |
| SubagentStop | Blocks stoppage, shows stderr to subagent |

### Method 2: JSON Output (Advanced)

Return JSON via stdout for fine-grained control:

```json
{
  "continue": true,            // Continue processing? (default: true)
  "stopReason": "string",      // Message when continue=false
  "suppressOutput": true,       // Hide output from transcript
  "systemMessage": "warning",   // Warning shown to user
  
  // Event-specific fields
  "decision": "block",          // or undefined
  "reason": "Explanation",
  
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",  // allow, deny, ask
    "permissionDecisionReason": "Reason shown to user/Claude"
  }
}
```

## PreToolUse Hook (Advanced)

Control tool execution:

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")
tool_input = input_data.get("tool_input", {})

# Auto-approve documentation reads
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".txt", ".json")):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Doc file auto-approved"
            },
            "suppressOutput": True
        }
        print(json.dumps(output))
        sys.exit(0)

# Let normal permission flow proceed
sys.exit(0)
```

## PostToolUse Hook (Advanced)

Provide feedback after tool execution:

```python
#!/usr/bin/env python3
import json
import sys
import subprocess

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")

if tool_name in ["Write", "Edit"]:
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path")
    
    # Run linter
    result = subprocess.run(
        ["eslint", file_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        # Block with feedback to Claude
        output = {
            "decision": "block",
            "reason": f"Linting failed:\n{result.stdout}"
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

## UserPromptSubmit Hook

Add context or validate prompts:

```python
#!/usr/bin/env python3
import json
import sys
import datetime

input_data = json.load(sys.stdin)
prompt = input_data.get("prompt", "")

# Add timestamp to context
context = f"Current time: {datetime.datetime.now()}"

# Method 1: Print to stdout (exit 0)
print(context)
sys.exit(0)

# Method 2: JSON output (more control)
output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context
    }
}
print(json.dumps(output))
sys.exit(0)
```

## SessionStart Hook

Set up environment:

```bash
#!/bin/bash

# Persist environment variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-key' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

# Add context for Claude
output=$(cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current sprint: Sprint 42\nOpen issues: 5"
  }
}
EOF
)

echo "$output"
exit 0
```

## SessionEnd Hook

Cleanup tasks:

```bash
#!/bin/bash
input=$(cat)

# Extract session info
session_id=$(echo "$input" | jq -r '.session_id')
reason=$(echo "$input" | jq -r '.reason')

# Log session
echo "Session $session_id ended: $reason" >> ~/.claude/session.log

exit 0
```

## Environment Variables

Available in hook commands:

- `$CLAUDE_PROJECT_DIR`: Project root directory
- `$CLAUDE_PLUGIN_ROOT`: Plugin directory (plugin hooks only)
- `$CLAUDE_ENV_FILE`: Env file path (SessionStart only)
- `$CLAUDE_CODE_REMOTE`: "true" if web, empty if CLI

## MCP Tool Hooks

Target MCP tools:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation' >> ~/mcp.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Execution Details

- **Timeout**: 60 seconds default (configurable per command)
- **Parallelization**: All matching hooks run in parallel
- **Deduplication**: Identical commands auto-deduplicated
- **Environment**: Runs in current directory with Claude Code env
- **Input**: JSON via stdin
- **Output**: Varies by event (see above)

## Security Warning

⚠️ **USE AT YOUR OWN RISK**

Hooks execute arbitrary shell commands automatically. You are responsible for:
- Commands you configure
- File modifications
- Data access
- System damage risk

**Best Practices**:
1. Validate and sanitize inputs
2. Always quote shell variables: `"$VAR"`
3. Block path traversal (check for `..`)
4. Use absolute paths or `$CLAUDE_PROJECT_DIR`
5. Skip sensitive files (.env, .git/, keys)
6. Test in safe environment first

## Debugging

```bash
# Run with debug output
claude --debug

# Check configuration
/hooks

# View hook execution
# Progress shown in transcript mode (Ctrl-R)
```

Debug output shows:
```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Hook command completed with status 0
```

## Common Use Cases

1. **Formatting**: Auto-format on file write
2. **Linting**: Validate code after edits
3. **Git**: Auto-commit or auto-push
4. **Notifications**: Alert on events
5. **Security**: Scan for secrets
6. **Testing**: Run tests after changes
7. **Logging**: Track tool usage
8. **Validation**: Enforce project rules

