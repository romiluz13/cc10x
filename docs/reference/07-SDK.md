# Claude Agent SDK

## Overview

Build production-ready AI agents programmatically using TypeScript or Python.

**Renamed from**: Claude Code SDK → Claude Agent SDK

## Installation

### TypeScript

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Python

```bash
pip install anthropic-agent-sdk
```

## Basic Usage

### TypeScript

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const result = query({
  prompt: "Review the authentication module for security issues",
  options: {
    workingDirectory: process.cwd(),
    model: 'sonnet'
  }
});

for await (const message of result) {
  console.log(message);
}
```

### Python

```python
from anthropic_agent_sdk import query

result = query(
    prompt="Review the authentication module for security issues",
    options={
        "working_directory": os.getcwd(),
        "model": "sonnet"
    }
)

for message in result:
    print(message)
```

## Why Use the SDK?

Built on Claude Code's agent harness:

- **Context ManagementMenuAutomatic compaction
- **Rich Tool EcosystemMenuFile ops, code execution, web search, MCP
- **Advanced Permissions**: Fine-grained control
- **Production EssentialsMenuError handling, session management
- **Optimized Integration**: Automatic prompt caching

## What You Can Build

### Coding Agents
- SRE agents (diagnose/fix production issues)
- Security review bots
- Oncall engineering assistants
- Code review agents

### Business Agents
- Legal assistants (contract review)
- Finance advisors (report analysis)
- Customer support agents
- Content creation assistants

## Authentication

### Anthropic API (Default)

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Get key from: https://console.anthropic.com/

### Amazon Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
# Configure AWS credentials
```

### Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=1
# Configure Google Cloud credentials
```

## SDK Features

All Claude Code features work via filesystem-based configuration:

| Feature | Location | SDK Support |
|---------|----------|-------------|
| **Subagents** | `.claude/agents/*.md` | ✅ Auto-loaded |
| **Skills** | `.claude/skills/*/SKILL.md` | ✅ Auto-loaded |
| **Hooks** | `.claude/settings.json` | ✅ Auto-loaded |
| **Slash Commands** | `.claude/commands/*.md` | ✅ Auto-loaded |
| **Plugins** | Via `plugins` option | ✅ Programmatic |
| **Memory (CLAUDE.md)** | `.claude/CLAUDE.md` | ✅ Requires `settingSources` |

## Subagents in SDK

### Programmatic Definition (Recommended)

```typescript
import { query, AgentDefinition } from '@anthropic-ai/claude-agent-sdk';

const result = query({
  prompt: "Review the authentication module",
  options: {
    agents: {
      'code-reviewer': {
        description: 'Expert code review. Use for quality, security reviews.',
        prompt: `You are a code review specialist.
        
When reviewing:
- Identify security vulnerabilities
- Check performance issues
- Verify coding standards
- Suggest improvements`,
        tools: ['Read', 'Grep', 'Glob'],
        model: 'sonnet'
      },
      'test-runner': {
        description: 'Run and analyze test suites.',
        prompt: `You are a test execution specialist.
        
Focus on:
- Running test commands
- Analyzing output
- Identifying failures
- Suggesting fixes`,
        tools: ['Bash', 'Read', 'Grep']
      }
    }
  }
});
```

### AgentDefinition Interface

```typescript
interface AgentDefinition {
  description: string;           // Required: when to use this agent
  prompt: string;                // Required: system prompt
  tools?: string[];             // Optional: allowed tools
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';
}
```

### Filesystem-Based (Alternative)

Place in `.claude/agents/*.md`:

```markdown
---
name: code-reviewer
description: Expert code review specialist
tools: Read, Grep, Glob, Bash
---

Your subagent's system prompt...
```

Programmatic agents override filesystem agents with same name.

## Skills in SDK

Skills auto-load from `.claude/skills/*/SKILL.md`:

```typescript
const result = query({
  prompt: "Process this PDF document",
  options: {
    // Skills automatically discovered from:
    // - .claude/skills/
    // - ~/.claude/skills/
    settingSources: ['project']  // Required to load CLAUDE.md
  }
});
```

Enable Skills by including `"Skill"` in `allowed_tools` (if restricting tools).

## System Prompts

### Method 1: CLAUDE.md Files

```
.claude/CLAUDE.md         # Project-level
~/.claude/CLAUDE.md       # User-level
CLAUDE.md                 # Root-level
```

Load via:

```typescript
// TypeScript
{
  settingSources: ['project']
}

// Python
{
  setting_sources: ["project"]
}
```

### Method 2: Programmatic

```typescript
const result = query({
  prompt: "Build a REST API",
  options: {
    systemPrompt: "You are an expert backend developer specializing in Node.js and Express."
  }
});
```

## Tool Permissions

### Allow Specific Tools

```typescript
const result = query({
  prompt: "Analyze this codebase",
  options: {
    allowedTools: ['Read', 'Grep', 'Glob']  // Read-only
  }
});
```

### Disallow Specific Tools

```typescript
const result = query({
  prompt: "Review code",
  options: {
    disallowedTools: ['Edit', 'Write']  // No modifications
  }
});
```

### Permission Modes

```typescript
{
  permissionMode: 'default'          // Ask for permission
  // or 'plan'                       // Plan mode (safe)
  // or 'acceptEdits'                // Auto-accept edits
  // or 'bypassPermissions'          // Auto-approve all
}
```

## Model Context Protocol (MCP)

Connect to external tools via MCP:

```typescript
const result = query({
  prompt: "Query the database",
  options: {
    mcpServers: {
      'my-database': {
        command: 'npx',
        args: ['-y', '@company/mcp-server'],
        env: {
          DB_CONNECTION: process.env.DB_CONNECTION
        }
      }
    }
  }
});
```

MCP tools appear as: `mcp__server__tool`

## Session Management

```typescript
import { createSession, continueSession } from '@anthropic-ai/claude-agent-sdk';

// Create new session
const session = await createSession({
  workingDirectory: '/path/to/project',
  model: 'sonnet'
});

// Continue session
const result = await continueSession({
  sessionId: session.id,
  prompt: "Continue with the next task"
});
```

## Cost Tracking

```typescript
const result = query({
  prompt: "Build a feature",
  options: {
    trackCosts: true
  }
});

for await (const message of result) {
  if (message.type === 'usage') {
    console.log('Tokens:', message.tokens);
    console.log('Cost:', message.cost);
  }
}
```

## Dynamic Agent Configuration

```typescript
function createSecurityAgent(level: 'basic' | 'strict'): AgentDefinition {
  return {
    description: 'Security code reviewer',
    prompt: `You are a ${level === 'strict' ? 'strict' : 'balanced'} security reviewer...`,
    tools: ['Read', 'Grep', 'Glob'],
    model: level === 'strict' ? 'opus' : 'sonnet'
  };
}

const result = query({
  prompt: "Review this PR for security",
  options: {
    agents: {
      'security-reviewer': createSecurityAgent('strict')
    }
  }
});
```

## Common Tool Combinations

### Read-Only Agents (Analysis)
```typescript
tools: ['Read', 'Grep', 'Glob']
```

### Test Execution
```typescript
tools: ['Bash', 'Read', 'Grep']
```

### Code Modification
```typescript
tools: ['Read', 'Edit', 'Write', 'Grep', 'Glob']
```

### Full-Stack Development
```typescript
tools: ['Read', 'Edit', 'Write', 'Bash', 'Grep', 'Glob', 'WebSearch']
```

## Complete Example: Code Review Agent

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

async function reviewCode(filePath: string) {
  const result = query({
    prompt: `Review ${filePath} for security and performance issues`,
    options: {
      workingDirectory: process.cwd(),
      
      // Define specialized reviewer subagent
      agents: {
        'security-scanner': {
          description: 'Security vulnerability scanner',
          prompt: 'You are a security expert. Focus on finding vulnerabilities.',
          tools: ['Read', 'Grep', 'Glob'],
          model: 'opus'
        },
        'performance-analyzer': {
          description: 'Performance optimization specialist',
          prompt: 'You are a performance expert. Find bottlenecks and suggest optimizations.',
          tools: ['Read', 'Bash', 'Grep'],
          model: 'sonnet'
        }
      },
      
      // Restrict main agent tools
      allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
      
      // Configure model
      model: 'sonnet',
      
      // Track costs
      trackCosts: true
    }
  });

  for await (const message of result) {
    if (message.type === 'text') {
      console.log(message.content);
    }
    if (message.type === 'usage') {
      console.log(`Cost: $${message.cost}`);
    }
  }
}

reviewCode('src/auth/login.ts');
```

## Streaming vs Single Mode

### Streaming Mode (Default)

```typescript
const result = query({
  prompt: "Build a feature"
});

for await (const message of result) {
  // Process messages as they arrive
  console.log(message);
}
```

### Single Mode

```typescript
const result = await querySingle({
  prompt: "Build a feature"
});

console.log(result);
```

## Error Handling

```typescript
try {
  const result = query({
    prompt: "Build a feature",
    options: { workingDirectory: '/invalid/path' }
  });
  
  for await (const message of result) {
    if (message.type === 'error') {
      console.error('Error:', message.error);
    }
  }
} catch (error) {
  console.error('Fatal error:', error);
}
```

## Plugins in SDK

Load plugins programmatically:

```typescript
const result = query({
  prompt: "Deploy to production",
  options: {
    plugins: ['deployment-tools', 'security-scanner']
  }
});
```

## Reporting Bugs

- **TypeScript SDK**: https://github.com/anthropics/claude-agent-sdk-typescript/issues
- **Python SDK**: https://github.com/anthropics/claude-agent-sdk-python/issues

## Changelog

- **TypeScript**: https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md
- **Python**: https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md

