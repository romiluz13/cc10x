# API Reference

## Claude Agent SDK

### Installation

```bash
# TypeScript
npm install @anthropic-ai/claude-agent-sdk

# Python
pip install anthropic-agent-sdk
```

### Basic Query

#### TypeScript

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const result = query({
  prompt: "Your task here",
  options: {
    workingDirectory: process.cwd(),
    model: 'sonnet',
    // ... other options
  }
});

for await (const message of result) {
  console.log(message);
}
```

#### Python

```python
from anthropic_agent_sdk import query

result = query(
    prompt="Your task here",
    options={
        "working_directory": os.getcwd(),
        "model": "sonnet",
    }
)

for message in result:
    print(message)
```

## Query Options

### TypeScript Interface

```typescript
interface QueryOptions {
  // Core configuration
  workingDirectory?: string;
  model?: 'sonnet' | 'opus' | 'haiku';
  systemPrompt?: string;
  
  // Settings
  settingSources?: ('project' | 'user')[];  // Load CLAUDE.md, skills
  
  // Agents
  agents?: Record<string, AgentDefinition>;
  
  // Tools
  allowedTools?: string[];
  disallowedTools?: string[];
  
  // Permissions
  permissionMode?: 'default' | 'plan' | 'acceptEdits' | 'bypassPermissions';
  
  // MCP
  mcpServers?: Record<string, MCPServerConfig>;
  
  // Plugins
  plugins?: string[];
  
  // Tracking
  trackCosts?: boolean;
}
```

### Python Type Hints

```python
from typing import TypedDict, Literal, List, Dict

class QueryOptions(TypedDict, total=False):
    working_directory: str
    model: Literal['sonnet', 'opus', 'haiku']
    system_prompt: str
    setting_sources: List[Literal['project', 'user']]
    agents: Dict[str, AgentDefinition]
    allowed_tools: List[str]
    disallowed_tools: List[str]
    permission_mode: Literal['default', 'plan', 'acceptEdits', 'bypassPermissions']
    mcp_servers: Dict[str, MCPServerConfig]
    plugins: List[str]
    track_costs: bool
```

## AgentDefinition

### TypeScript

```typescript
interface AgentDefinition {
  description: string;           // Required: When to use agent
  prompt: string;                // Required: System prompt
  tools?: string[];             // Optional: Allowed tools
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';
}
```

### Example

```typescript
const agents = {
  'code-reviewer': {
    description: 'Code review specialist. Use for quality and security reviews.',
    prompt: 'You are a senior code reviewer focusing on security and best practices.',
    tools: ['Read', 'Grep', 'Glob'],
    model: 'opus'
  }
};
```

## MCPServerConfig

### TypeScript

```typescript
interface MCPServerConfig {
  command: string;
  args?: string[];
  env?: Record<string, string>;
  cwd?: string;
}
```

### Example

```typescript
const mcpServers = {
  'project-db': {
    command: 'npx',
    args: ['-y', '@company/mcp-server'],
    env: {
      DATABASE_URL: process.env.DATABASE_URL,
      API_KEY: process.env.API_KEY
    },
    cwd: '${CLAUDE_PLUGIN_ROOT}'
  }
};
```

## Message Types

### TypeScript

```typescript
type Message = 
  | TextMessage
  | ToolUseMessage
  | ToolResultMessage
  | UsageMessage
  | ErrorMessage;

interface TextMessage {
  type: 'text';
  content: string;
}

interface ToolUseMessage {
  type: 'tool_use';
  tool: string;
  input: any;
}

interface ToolResultMessage {
  type: 'tool_result';
  tool: string;
  result: any;
}

interface UsageMessage {
  type: 'usage';
  tokens: {
    input: number;
    output: number;
    total: number;
  };
  cost: number;
}

interface ErrorMessage {
  type: 'error';
  error: string;
}
```

## Skills API (Claude API)

### List Skills

```typescript
// TypeScript
const skills = await client.beta.skills.list({
  source: 'anthropic',
  betas: ['skills-2025-10-02']
});

// Python
skills = client.beta.skills.list(
    source="anthropic",
    betas=["skills-2025-10-02"]
)
```

### Create Message with Skill

```typescript
// TypeScript
const response = await client.beta.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 4096,
  betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
  container: {
    skills: [
      {
        type: 'anthropic',
        skill_id: 'pptx',
        version: 'latest'
      }
    ]
  },
  messages: [{
    role: 'user',
    content: 'Create a presentation about AI'
  }],
  tools: [{
    type: 'code_execution_20250825',
    name: 'code_execution'
  }]
});

// Python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "pptx",
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Create a presentation about AI"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)
```

### Pre-built Skill IDs

- `pptx` - PowerPoint
- `xlsx` - Excel
- `docx` - Word
- `pdf` - PDF

### Required Beta Headers

```typescript
betas: [
  'code-execution-2025-08-25',  // Code execution container
  'skills-2025-10-02',          // Skills functionality
  'files-api-2025-04-14'        // File upload/download
]
```

## Session Management

### Create Session

```typescript
import { createSession } from '@anthropic-ai/claude-agent-sdk';

const session = await createSession({
  workingDirectory: '/path/to/project',
  model: 'sonnet',
  systemPrompt: 'You are an expert developer'
});

console.log('Session ID:', session.id);
```

### Continue Session

```typescript
import { continueSession } from '@anthropic-ai/claude-agent-sdk';

const result = await continueSession({
  sessionId: 'existing-session-id',
  prompt: 'Continue with next task'
});
```

## File Operations

### Download Generated File

```typescript
// TypeScript
const fileContent = await client.beta.files.download({
  file_id: fileId,
  betas: ['files-api-2025-04-14']
});

fileContent.write_to_file('output.pptx');

// Python
file_content = client.beta.files.download(
    file_id=file_id,
    betas=["files-api-2025-04-14"]
)

with open("output.pptx", "wb") as f:
    file_content.write_to_file(f.name)
```

## Custom Tools (SDK)

### Define Custom Tool

```typescript
interface CustomTool {
  name: string;
  description: string;
  input_schema: object;
}

const tools: CustomTool[] = [
  {
    name: 'search_database',
    description: 'Search internal database',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        limit: { type: 'number' }
      },
      required: ['query']
    }
  }
];

const result = query({
  prompt: "Search for users",
  options: {
    customTools: tools,
    toolHandler: async (toolName, toolInput) => {
      if (toolName === 'search_database') {
        // Implement search logic
        return await searchDB(toolInput.query, toolInput.limit);
      }
    }
  }
});
```

## Streaming Modes

### Streaming (Default)

```typescript
const result = query({ prompt: "Build feature" });

for await (const message of result) {
  if (message.type === 'text') {
    process.stdout.write(message.content);
  }
}
```

### Single Response

```typescript
import { querySingle } from '@anthropic-ai/claude-agent-sdk';

const result = await querySingle({
  prompt: "Build feature"
});

console.log(result.content);
```

## Error Handling

```typescript
try {
  const result = query({ prompt: "Task" });
  
  for await (const message of result) {
    if (message.type === 'error') {
      console.error('Agent error:', message.error);
      // Handle error
    }
  }
} catch (error) {
  console.error('Fatal error:', error);
  // Cleanup, retry, alert
}
```

## Cost Tracking

```typescript
const result = query({
  prompt: "Build feature",
  options: {
    trackCosts: true
  }
});

let totalCost = 0;
let totalTokens = 0;

for await (const message of result) {
  if (message.type === 'usage') {
    totalCost += message.cost;
    totalTokens += message.tokens.total;
    
    console.log(`Tokens: ${message.tokens.total}`);
    console.log(`Cost: $${message.cost.toFixed(4)}`);
  }
}

console.log(`\nTotal: ${totalTokens} tokens, $${totalCost.toFixed(4)}`);
```

## Environment Variables

| Variable | Scope | Description |
|----------|-------|-------------|
| `ANTHROPIC_API_KEY` | Global | API authentication |
| `CLAUDE_CODE_USE_BEDROCK` | Global | Enable Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Global | Enable Vertex AI |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin | Plugin directory path |
| `$CLAUDE_PROJECT_DIR` | Hook | Project root directory |
| `$CLAUDE_ENV_FILE` | SessionStart | Env persistence file |
| `$CLAUDE_CODE_REMOTE` | Hook | "true" if web, empty if CLI |

## Tool Permission Syntax

### Subagents (Markdown)

```yaml
tools: Read, Grep, Glob, Bash
```

### Skills (Markdown)

```yaml
allowed-tools: Read, Grep, Glob
```

### SDK (TypeScript/Python)

```typescript
allowedTools: ['Read', 'Grep', 'Glob']
disallowedTools: ['Edit', 'Write']
```

### Hooks (JSON)

```json
{
  "allowed-tools": "Bash(git*), Read"
}
```

## Complete SDK Example

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

async function buildAuthFeature() {
  const result = query({
    prompt: "Build user authentication with JWT",
    options: {
      // Basic config
      workingDirectory: process.cwd(),
      model: 'sonnet',
      
      // Load project settings
      settingSources: ['project'],
      
      // System prompt
      systemPrompt: 'You are an expert in secure authentication systems.',
      
      // Subagents
      agents: {
        'security-reviewer': {
          description: 'Security vulnerability scanner',
          prompt: 'Expert in auth security. Find vulnerabilities.',
          tools: ['Read', 'Grep', 'Glob'],
          model: 'opus'
        },
        'test-writer': {
          description: 'Test suite creator',
          prompt: 'Write comprehensive auth tests.',
          tools: ['Read', 'Write', 'Bash'],
          model: 'sonnet'
        }
      },
      
      // Tool restrictions
      allowedTools: ['Read', 'Edit', 'Write', 'Bash', 'Grep', 'Glob', 'Task'],
      
      // MCP servers
      mcpServers: {
        'auth-db': {
          command: 'npx',
          args: ['-y', '@company/auth-mcp'],
          env: {
            DB_URL: process.env.AUTH_DB_URL
          }
        }
      },
      
      // Permissions
      permissionMode: 'plan',
      
      // Tracking
      trackCosts: true
    }
  });
  
  for await (const message of result) {
    switch (message.type) {
      case 'text':
        console.log(message.content);
        break;
      case 'tool_use':
        console.log(`Using tool: ${message.tool}`);
        break;
      case 'usage':
        console.log(`Cost: $${message.cost.toFixed(4)}`);
        break;
      case 'error':
        console.error(`Error: ${message.error}`);
        break;
    }
  }
}

buildAuthFeature();
```

## Skills API Endpoints

### List Skills

**Endpoint**: `GET /v1/skills`

```bash
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02"
```

Response:
```json
{
  "data": [
    {
      "id": "pptx",
      "type": "skill",
      "display_title": "PowerPoint",
      "description": "Create and edit presentations"
    }
  ]
}
```

### Create Custom Skill

**Endpoint**: `POST /v1/skills`

```bash
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "name": "my-custom-skill",
    "description": "What it does and when to use",
    "files": {
      "SKILL.md": "content here..."
    }
  }'
```

### Get Skill

**Endpoint**: `GET /v1/skills/{skill_id}`

```bash
curl https://api.anthropic.com/v1/skills/skill-123 \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02"
```

### Update Skill

**Endpoint**: `PATCH /v1/skills/{skill_id}`

### Delete Skill

**Endpoint**: `DELETE /v1/skills/{skill_id}`

## Messages API with Skills

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "pptx",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Create a presentation about renewable energy"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

## Hook Input Schema

All hooks receive JSON via stdin:

```typescript
interface HookInput {
  // Common fields
  session_id: string;
  transcript_path: string;
  cwd: string;
  permission_mode: 'default' | 'plan' | 'acceptEdits' | 'bypassPermissions';
  hook_event_name: string;
  
  // Event-specific fields
  tool_name?: string;           // PreToolUse, PostToolUse
  tool_input?: any;             // PreToolUse, PostToolUse
  tool_response?: any;          // PostToolUse
  message?: string;             // Notification
  prompt?: string;              // UserPromptSubmit
  stop_hook_active?: boolean;   // Stop, SubagentStop
  trigger?: 'manual' | 'auto';  // PreCompact
  custom_instructions?: string; // PreCompact
  source?: 'startup' | 'resume' | 'clear' | 'compact';  // SessionStart
  reason?: string;              // SessionEnd
}
```

## Hook Output Schema

### Simple (Exit Code)

```bash
exit 0   # Success
exit 2   # Blocking error
exit 1   # Non-blocking error
```

### Advanced (JSON)

```typescript
interface HookOutput {
  // Common fields
  continue?: boolean;            // Continue processing? (default: true)
  stopReason?: string;           // Message when continue=false
  suppressOutput?: boolean;       // Hide stdout from transcript
  systemMessage?: string;         // Warning to user
  
  // Decision control
  decision?: 'block' | undefined;
  reason?: string;
  
  // Event-specific
  hookSpecificOutput?: {
    hookEventName: string;
    
    // PreToolUse
    permissionDecision?: 'allow' | 'deny' | 'ask';
    permissionDecisionReason?: string;
    
    // PostToolUse
    additionalContext?: string;
    
    // UserPromptSubmit
    additionalContext?: string;
    
    // SessionStart
    additionalContext?: string;
  };
}
```

## CLI Flags

```bash
claude [options] [prompt]

Options:
  --help                 Show help
  --version              Show version
  --debug                Enable debug logging
  --model <model>        Set model (sonnet, opus, haiku)
  --agents <json>        Define agents via JSON
  --working-dir <path>   Set working directory
  --resume               Resume last session
  --continue             Continue last session
  -p, --prompt <text>    Execute prompt and exit
```

## Settings File Schema

```json
{
  // Marketplaces
  "extraKnownMarketplaces": {
    "marketplace-id": {
      "source": {
        "source": "github",
        "repo": "owner/repo"
      }
    }
  },
  
  // Enabled plugins
  "enabledPlugins": [
    "plugin-name@marketplace-id"
  ],
  
  // Hooks
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh",
            "timeout": 60
          }
        ]
      }
    ]
  },
  
  // MCP servers
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "mcp-server-package"]
    }
  }
}
```

## Type Definitions Summary

### TypeScript

```typescript
// Core query function
function query(params: {
  prompt: string;
  options?: QueryOptions;
}): AsyncIterableIterator<Message>;

function querySingle(params: {
  prompt: string;
  options?: QueryOptions;
}): Promise<Response>;

// Session management
function createSession(options: SessionOptions): Promise<Session>;
function continueSession(params: {
  sessionId: string;
  prompt: string;
}): AsyncIterableIterator<Message>;

// Types
interface QueryOptions { /* see above */ }
interface AgentDefinition { /* see above */ }
interface MCPServerConfig { /* see above */ }
type Message = /* see above */;
```

### Python

```python
# Core query function
def query(
    prompt: str,
    options: Optional[QueryOptions] = None
) -> Iterator[Message]:
    ...

def query_single(
    prompt: str,
    options: Optional[QueryOptions] = None
) -> Response:
    ...

# Session management
def create_session(options: SessionOptions) -> Session:
    ...

def continue_session(
    session_id: str,
    prompt: str
) -> Iterator[Message]:
    ...
```

## GitHub Repositories

- **TypeScript SDK**: https://github.com/anthropics/claude-agent-sdk-typescript
- **Python SDK**: https://github.com/anthropics/claude-agent-sdk-python
- **Official Skills**: https://github.com/anthropics/skills
- **Cookbooks**: https://github.com/anthropics/claude-cookbooks
- **Claude Code**: https://github.com/anthropics/claude-code

## Bug Reporting

- **TypeScript SDK Issues**: https://github.com/anthropics/claude-agent-sdk-typescript/issues
- **Python SDK Issues**: https://github.com/anthropics/claude-agent-sdk-python/issues
- **Claude Code Issues**: https://github.com/anthropics/claude-code/issues

## Rate Limits & Pricing

See: https://docs.claude.com/en/docs/about-claude/pricing

Models (as of Oct 2025):
- **Claude Opus 4.5**: Most capable
- **Claude Sonnet 4.5**: Balanced (recommended)
- **Claude Haiku 4.5**: Fast and economical

## Best Practices for API Usage

1. **Use appropriate model** for task complexity
2. **Enable cost tracking** in production
3. **Handle errors gracefully** with try-catch
4. **Respect rate limits** with backoff
5. **Cache when possible** (prompt caching)
6. **Monitor token usage** to control costs
7. **Use skills** for specialized tasks
8. **Leverage subagents** for complex workflows

