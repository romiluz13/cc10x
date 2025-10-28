# Practical Examples & Patterns

## Complete Plugin Example

### Directory Structure

```
my-company-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md
│   └── review-pr.md
├── agents/
│   ├── security-reviewer.md
│   └── performance-tester.md
├── skills/
│   ├── code-quality/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── lint.sh
│   └── deployment/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── scripts/
│   ├── security-scan.sh
│   └── format-code.py
└── README.md
```

### plugin.json

```json
{
  "name": "my-company-plugin",
  "version": "2.0.0",
  "description": "Company development tools",
  "author": {
    "name": "Engineering Team",
    "email": "eng@company.com"
  },
  "homepage": "https://docs.company.com/claude-plugin",
  "repository": "https://github.com/company/claude-plugin",
  "license": "MIT",
  "keywords": ["deployment", "security", "code-review"]
}
```

### commands/deploy.md

```markdown
---
description: Deploy application to environment
argument-hint: [environment] [branch]
allowed-tools: Bash(git*), Bash(npm*), Bash(docker*)
---

# Deploy Command

Deploy to $1 from branch $2

## Pre-deployment checks:
!`git status`
!`npm test`

## Your task:
1. Verify tests pass
2. Build production bundle
3. Deploy to $1
4. Verify deployment
```

### agents/security-reviewer.md

```markdown
---
name: security-reviewer
description: Security vulnerability scanner. Use proactively before deployments or after security-related code changes.
tools: Read, Grep, Glob, Bash
model: opus
---

# Security Reviewer

Expert in identifying security vulnerabilities.

## When Invoked
1. Scan codebase for common vulnerabilities
2. Check dependencies for known issues
3. Review authentication/authorization
4. Verify input validation
5. Check for exposed secrets

## Security Checklist
- SQL injection risks
- XSS vulnerabilities
- CSRF protection
- Secrets in code
- Insecure dependencies
- Input validation
- Authentication bypass
- Authorization issues

## Output Format
**Critical**: Must fix immediately
**High**: Should fix before deployment
**Medium**: Fix in next sprint
**Low**: Consider fixing

Include specific file/line and remediation steps.
```

### skills/code-quality/SKILL.md

```markdown
---
name: code-quality-checker
description: Check code quality, maintainability, and best practices. Use when reviewing code or improving code quality.
allowed-tools: Read, Grep, Glob
---

# Code Quality Checker

Comprehensive code quality analysis.

## Analysis Areas

### 1. Code Organization
- Module structure
- Separation of concerns
- Naming conventions

### 2. Maintainability
- Code complexity
- Duplicate code
- Comment quality

### 3. Best Practices
- Error handling
- Logging
- Type safety

## Process
1. Read target files
2. Analyze structure
3. Check patterns
4. Generate report

## Report Format
```markdown
# Code Quality Report

## Summary
Overall score: X/10

## Issues Found
### Critical
- Issue 1: Description [file:line]

### Warnings
- Issue 2: Description [file:line]

## Recommendations
1. Specific action
2. Specific action
```
```

### hooks/hooks.json

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.py",
          "timeout": 30
        }
      ]
    }
  ],
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh"
        }
      ]
    }
  ]
}
```

### .mcp.json

```json
{
  "mcpServers": {
    "company-jira": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/jira-mcp",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/jira-config.json"],
      "env": {
        "JIRA_URL": "${JIRA_URL}",
        "JIRA_TOKEN": "${JIRA_TOKEN}"
      }
    }
  }
}
```

## Marketplace Example

### marketplace.json

```json
{
  "name": "company-marketplace",
  "owner": {
    "name": "Engineering Team",
    "email": "eng@company.com"
  },
  "metadata": {
    "description": "Internal company development tools",
    "version": "2.0.0"
  },
  "plugins": [
    {
      "name": "deployment-tools",
      "source": "./plugins/deployment",
      "description": "Deployment automation",
      "version": "2.1.0",
      "category": "deployment"
    },
    {
      "name": "security-scanner",
      "source": {
        "source": "github",
        "repo": "company/security-plugin"
      },
      "description": "Security scanning tools",
      "version": "1.5.0",
      "category": "security"
    },
    {
      "name": "code-quality",
      "source": {
        "source": "git",
        "url": "https://git.company.com/plugins/quality.git"
      },
      "description": "Code quality tools",
      "version": "3.0.0",
      "category": "quality"
    }
  ]
}
```

## Workflow Examples

### 1. Automated Code Review

**Setup**: Create review-workflow plugin

```
review-workflow/
├── .claude-plugin/plugin.json
├── agents/
│   └── code-reviewer.md
├── skills/
│   └── code-review/
│       └── SKILL.md
└── hooks/
    └── hooks.json
```

**hooks.json**:
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Use code-reviewer agent to review changes' | claude -p -"
        }
      ]
    }
  ]
}
```

### 2. PDF Processing Pipeline

**skills/pdf-processor/SKILL.md**:

```markdown
---
name: pdf-processor
description: Extract text from PDFs, fill forms, merge documents. Use when working with PDF files.
---

# PDF Processor

## Workflow

1. Analyze PDF: `python scripts/analyze.py input.pdf`
2. Extract text or fill forms based on analysis
3. Validate output: `python scripts/validate.py output.pdf`

## Quick Operations

**Extract text**:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Fill form**:
See [FORMS.md](FORMS.md) for detailed workflow.
```

**skills/pdf-processor/FORMS.md**:

```markdown
# PDF Form Filling

## Steps

1. **Analyze form**:
   ```bash
   python scripts/analyze_form.py input.pdf > fields.json
   ```

2. **Edit field values**:
   Edit `fields.json` with desired values

3. **Validate mapping**:
   ```bash
   python scripts/validate_fields.py fields.json
   ```
   Fix errors if any.

4. **Fill form**:
   ```bash
   python scripts/fill_form.py input.pdf fields.json output.pdf
   ```

5. **Verify output**:
   ```bash
   python scripts/verify_output.py output.pdf
   ```
```

### 3. Multi-Agent Development Workflow

**SDK Example**:

```typescript
const result = query({
  prompt: "Build a user authentication feature",
  options: {
    agents: {
      'backend-dev': {
        description: 'Backend API development',
        prompt: 'Expert in Node.js, Express, JWT authentication',
        tools: ['Read', 'Edit', 'Write', 'Bash'],
        model: 'sonnet'
      },
      'frontend-dev': {
        description: 'Frontend UI development',
        prompt: 'Expert in React, TypeScript, form validation',
        tools: ['Read', 'Edit', 'Write', 'Bash'],
        model: 'sonnet'
      },
      'security-reviewer': {
        description: 'Security review and validation',
        prompt: 'Security expert focusing on auth vulnerabilities',
        tools: ['Read', 'Grep', 'Glob'],
        model: 'opus'
      },
      'test-writer': {
        description: 'Test creation specialist',
        prompt: 'Write comprehensive tests for auth flows',
        tools: ['Read', 'Write', 'Bash'],
        model: 'sonnet'
      }
    }
  }
});
```

Claude orchestrates these agents to:
1. Backend-dev creates API
2. Frontend-dev creates UI  
3. Security-reviewer validates
4. Test-writer creates tests

### 4. Team Setup Example

**.claude/settings.json** (committed to repo):

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  },
  "enabledPlugins": [
    "deployment-tools@company-tools",
    "security-scanner@company-tools"
  ],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

When team members clone and trust repo:
- Marketplace auto-added
- Plugins auto-installed
- Hooks auto-configured

### 5. BigQuery Analysis Skill

```markdown
---
name: bigquery-analysis
description: Analyze BigQuery datasets, write SQL queries, generate reports. Use when working with BigQuery, SQL, or data analysis.
---

# BigQuery Analysis

## Available Datasets

**Finance**: Revenue, billing → [reference/finance.md](reference/finance.md)
**Sales**: Pipeline, opportunities → [reference/sales.md](reference/sales.md)
**Product**: Usage, features → [reference/product.md](reference/product.md)

## Quick Start

```bash
# List datasets
bq ls

# Run query
bq query --use_legacy_sql=false 'SELECT ...'
```

## Best Practices
- Always filter by date for large tables
- MUST exclude test accounts: `WHERE account_type != 'test'`
- Use table partitioning for queries
- Cost-effective queries: Limit scans

## Search Reference
Find specific metrics:
```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
```
```

## Pattern: Feedback Loop with Validation

For tasks requiring validation:

```markdown
## Document Editing Workflow

1. Make edits to `document.xml`
2. **Validate immediately**: `python scripts/validate.py document.xml`
3. If validation fails:
   - Review error message
   - Fix issues
   - **Run validation again**
4. **Only proceed when validation passes**
5. Finalize output
```

## Pattern: Progressive Disclosure

**SKILL.md** (high-level):
```markdown
## PDF Operations

**Text Extraction**: [Quick guide below]
**Form Filling**: See [FORMS.md](FORMS.md)
**Advanced**: See [REFERENCE.md](REFERENCE.md)

## Quick Text Extraction
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**FORMS.md** (loaded when needed):
```markdown
# Form Filling Guide

[Detailed 100+ line guide]
...
```

**REFERENCE.md** (loaded when needed):
```markdown
# Complete API Reference

[Complete 500+ line reference]
...
```

## Pattern: Conditional Workflows

```markdown
## Document Processing

1. Determine document type:
   - **PDF?** → Use [pdf-workflow](PDF.md)
   - **Word?** → Use [word-workflow](WORD.md)
   - **Excel?** → Use [excel-workflow](EXCEL.md)

2. Process accordingly
3. Validate output
```

## Real-World: Security Plugin

```json
{
  "name": "security-tools",
  "plugins": [
    {
      "name": "security-scanner",
      "source": "./plugins/security",
      "description": "Comprehensive security scanning",
      "version": "2.0.0",
      "commands": ["./commands/scan.md"],
      "agents": ["./agents/security-reviewer.md"],
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-bash.py"
              }
            ]
          }
        ],
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/scan-secrets.sh"
              }
            ]
          }
        ]
      },
      "mcpServers": {
        "security-db": {
          "command": "${CLAUDE_PLUGIN_ROOT}/servers/security-mcp",
          "args": ["--db", "${CLAUDE_PLUGIN_ROOT}/vulnerabilities.db"]
        }
      }
    }
  ]
}
```

## Real-World: Testing Workflow

### Test Runner Subagent

**agents/test-runner.md**:

```markdown
---
name: test-runner
description: Execute tests and fix failures. Use proactively after code changes.
tools: Bash, Read, Edit, Grep
---

# Test Runner

Automated testing specialist.

## When Invoked
1. Identify test framework (Jest, pytest, etc.)
2. Run appropriate tests
3. Analyze failures
4. Fix issues while preserving test intent

## Process
- Run tests: `npm test` or `pytest`
- Capture output
- Analyze failures
- Fix code (not tests, unless tests are wrong)
- Re-run to verify
- Repeat until all pass

## Output
- Number of tests run
- Failures fixed
- Changes made
- Test coverage impact
```

### Test Generation Skill

**skills/test-generator/SKILL.md**:

```markdown
---
name: test-generator
description: Generate comprehensive unit tests. Use when creating tests or improving test coverage.
---

# Test Generator

## Test Structure

For each function:
1. **Happy path**: Normal inputs, expected outputs
2. **Edge cases**: Boundaries, empty, null
3. **Error cases**: Invalid inputs, exceptions
4. **Integration**: Dependencies, mocks

## Example: Jest Tests

```javascript
describe('calculateTotal', () => {
  it('should sum positive numbers', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });
  
  it('should handle empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
  
  it('should throw on invalid input', () => {
    expect(() => calculateTotal(null)).toThrow();
  });
});
```

## Coverage Goals
- Functions: 100%
- Branches: >80%
- Lines: >90%
```

## Real-World: Data Analysis Pipeline

### BigQuery Skill with Domain Organization

**skills/bigquery/SKILL.md**:

```markdown
---
name: bigquery-analysis
description: Query BigQuery datasets for finance, sales, product data. Use when analyzing data or writing SQL queries.
---

# BigQuery Analysis

## Available Datasets

**Finance**: Revenue, ARR, billing
- Tables: `finance.revenue`, `finance.subscriptions`
- See [reference/finance.md](reference/finance.md)

**Sales**: Opportunities, pipeline, accounts
- Tables: `sales.opportunities`, `sales.accounts`
- See [reference/sales.md](reference/sales.md)

**Product**: API usage, features, adoption
- Tables: `product.api_usage`, `product.features`
- See [reference/product.md](reference/product.md)

## Common Queries

List tables:
```bash
bq ls finance
```

Run query:
```bash
bq query --use_legacy_sql=false '
SELECT 
  DATE(created_at) as date,
  SUM(amount) as revenue
FROM finance.revenue
WHERE created_at >= "2025-01-01"
  AND account_type != "test"
GROUP BY date
ORDER BY date DESC
'
```

## Best Practices
- **ALWAYS exclude test accounts**: `account_type != 'test'`
- Filter by date to reduce scan cost
- Use table partitioning
- Limit results for exploration: `LIMIT 100`
```

**skills/bigquery/reference/finance.md**:

```markdown
# Finance Dataset Reference

## Tables

### finance.revenue
- `id`: Revenue record ID
- `account_id`: Customer account
- `amount`: Revenue amount (USD)
- `created_at`: Timestamp
- `account_type`: "production" or "test"
- `subscription_id`: Related subscription

### finance.subscriptions
- `id`: Subscription ID
- `account_id`: Customer account
- `plan`: Plan name
- `mrr`: Monthly recurring revenue
- `created_at`: Start date
- `cancelled_at`: Cancellation date (nullable)

## Common Patterns

**Monthly Revenue**:
```sql
SELECT 
  DATE_TRUNC(DATE(created_at), MONTH) as month,
  SUM(amount) as revenue
FROM finance.revenue
WHERE account_type = 'production'
GROUP BY month
ORDER BY month DESC
```

**Active Subscriptions**:
```sql
SELECT COUNT(*) as active_subs
FROM finance.subscriptions
WHERE cancelled_at IS NULL
```
```

## Real-World: Development Container Setup

**.devcontainer/devcontainer.json** with Claude Code:

```json
{
  "name": "Project Dev Container",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:18",
  "customizations": {
    "vscode": {
      "extensions": [
        "anthropic.claude-code"
      ]
    }
  },
  "postCreateCommand": "npm install && /plugin marketplace add company/plugins && /plugin install dev-tools@company"
}
```

## SDK Complete Example

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';
import fs from 'fs';

async function buildFeature(featureName: string) {
  const result = query({
    prompt: `Build a ${featureName} feature with tests`,
    options: {
      workingDirectory: process.cwd(),
      
      // Load project settings (CLAUDE.md, skills, etc.)
      settingSources: ['project'],
      
      // Define specialized agents
      agents: {
        'feature-dev': {
          description: 'Feature development specialist',
          prompt: 'Expert full-stack developer. Build features with tests.',
          tools: ['Read', 'Edit', 'Write', 'Bash', 'Grep', 'Glob'],
          model: 'sonnet'
        },
        'code-reviewer': {
          description: 'Code quality and security reviewer',
          prompt: 'Senior reviewer focusing on quality and security.',
          tools: ['Read', 'Grep', 'Glob'],
          model: 'opus'
        },
        'test-writer': {
          description: 'Test suite specialist',
          prompt: 'Expert in writing comprehensive tests.',
          tools: ['Read', 'Write', 'Bash'],
          model: 'sonnet'
        }
      },
      
      // Configure permissions
      permissionMode: 'plan',  // Safe mode
      
      // MCP tools
      mcpServers: {
        'project-db': {
          command: 'npx',
          args: ['-y', '@company/db-mcp-server'],
          env: {
            DB_URL: process.env.DATABASE_URL
          }
        }
      },
      
      // Model selection
      model: 'sonnet',
      
      // Track costs
      trackCosts: true
    }
  });

  let totalCost = 0;
  
  for await (const message of result) {
    if (message.type === 'text') {
      console.log(message.content);
    }
    if (message.type === 'usage') {
      totalCost += message.cost;
      console.log(`Cost: $${message.cost.toFixed(4)}`);
    }
  }
  
  console.log(`\nTotal cost: $${totalCost.toFixed(4)}`);
}

buildFeature('user-authentication');
```

## Testing Pattern

### Create Evaluation Suite

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract text from document.pdf",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads PDF using appropriate library",
    "Extracts text from all pages",
    "Saves to output.txt in readable format"
  ]
}
```

Run tests to validate skill effectiveness.

## Progressive Disclosure in Action

User request: "Analyze Q4 sales"

```
1. Claude sees skill metadata:
   "bigquery-analysis: Analyze BigQuery datasets..."

2. Match found! Load SKILL.md:
   bash: cat .claude/skills/bigquery/SKILL.md

3. SKILL.md says: "For sales, see reference/sales.md"

4. Load sales reference:
   bash: cat .claude/skills/bigquery/reference/sales.md

5. Execute query using loaded knowledge

Result: Only sales reference loaded, not finance or product!
```

