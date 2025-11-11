# Orchestrator Reference Guide

Tool usage guides, search guidance, and reference materials for the cc10x orchestrator.

## Tool Access Precedence

When multiple skills are active, the orchestrator/workflow tool set governs delegation and verification. Domain skills may restrict themselves (e.g., Read/Grep/Glob), but they do not prevent the orchestrator/workflow from using `Task` or `Bash` to delegate/verify.

## Ask Questions Tool Usage

**Purpose**: Clarify requirements and gather missing information before proceeding

**When to Use**:

- Phase 0: Functionality Analysis (when functionality unclear)
- Plan Workflow: Requirements gathering
- Build Workflow: UI requirements for UI components
- Debug Workflow: Bug clarification

**Usage Pattern**:

```
Use the askquestion tool to clarify requirements:
- [Specific questions about functionality/requirements]
```

**Example**:

```
Use the askquestion tool to clarify requirements:
- What are the specific user flows?
- What are the acceptance criteria?
- What are the constraints?
```

## Task Tool Usage

**Purpose**: Track workflow progress and manage task queues

**When to Use**:

- Phase tracking (all workflows)
- Component build queue (Build workflow)
- Review findings tracking (Review workflow)
- Planning checklist (Plan workflow)

**Usage Pattern**:

```
Task: Create tasks for [purpose]
- Task 1: [description] (status)
- Task 2: [description] (status)

Task: Update [task] status to [new_status]
```

**Example**:

```
Task: Create tasks for workflow phases
- Phase 0: Functionality Analysis (in_progress)
- Phase 1: Input Validation (pending)
- Phase 2: Load Skills (pending)
```

## Tool Selection Guide

| Task                    | Tool          | When to Use                                                            | Example                                    |
| ----------------------- | ------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| Clarify requirements    | Ask Questions | Functionality unclear, missing requirements, need user input           | "What are the specific user flows?"        |
| Track workflow progress | Task          | Phase tracking, component queue, findings tracking, planning checklist | "Task: Create tasks for workflow phases"   |
| Find files by pattern   | Glob          | Need to find files matching pattern (e.g., `*.ts`, `**/test/**`)       | `Glob("**/*.test.ts")`                     |
| Search file content     | Grep          | Need to find text/patterns in files                                    | `Grep("function.*test")`                   |
| Read file contents      | Read          | Need to read specific file or section                                  | `Read("path/to/file.ts")`                  |
| Execute shell commands  | Bash          | Need to run commands, check exit codes, verify functionality           | `Bash("npm test")`                         |
| Fetch external docs     | WebFetch      | Need external API docs, library docs, reference materials              | `WebFetch("https://api.example.com/docs")` |

**Tool Selection Logic**:

- **Finding files**: Use `Glob` for pattern matching, `Grep` for content search
- **Reading files**: Use `Read` for specific files, `Grep` for searching across files
- **User interaction**: Use `Ask Questions` for clarification, `Task` for progress tracking
- **Verification**: Use `Bash` to run tests/commands, check exit codes
- **External resources**: Use `WebFetch` for documentation, cache results

## Search Guidance

**CRITICAL**: Choose the right tool for the search task. Using the wrong tool wastes tokens and time.

**When to Use Glob** (file discovery):

- Finding files by name pattern: `Glob("**/*.test.ts")`
- Finding files in specific directories: `Glob("src/components/**/*.tsx")`
- Discovering project structure: `Glob("**/*.json")` to find config files
- **Example**: "Find all test files" → `Glob("**/*.test.{ts,tsx,js,jsx}")`

**When to Use Grep** (content search):

- Searching for function/class names: `Grep("function.*authenticate")`
- Finding imports/exports: `Grep("import.*from.*api")`
- Searching for patterns across files: `Grep("TODO|FIXME|HACK")`
- Finding specific code patterns: `Grep("useState|useEffect")`
- **Example**: "Find all uses of authentication function" → `Grep("authenticate")`

**When to Use Read** (specific file access):

- Reading a known file: `Read("src/api/auth.ts")`
- Reading configuration files: `Read("package.json")`
- Reading workflow/skill files: `Read("plugins/cc10x/skills/review-workflow/SKILL.md")`
- Reading specific sections: `Read("file.ts", offset=100, limit=50)`
- **Example**: "Read the orchestrator skill" → `Read("plugins/cc10x/skills/cc10x-orchestrator/SKILL.md")`

**Search Strategy** (combine tools efficiently):

1. **Discovery Phase**: Use `Glob` to find relevant files
2. **Content Phase**: Use `Grep` to search within discovered files
3. **Detail Phase**: Use `Read` to read specific files/sections
4. **Example**:
   - Step 1: `Glob("**/*auth*.ts")` → Find auth-related files
   - Step 2: `Grep("function.*login", path="src/auth/")` → Find login functions
   - Step 3: `Read("src/auth/login.ts")` → Read specific implementation

**Anti-Patterns** (what NOT to do):

- ❌ Using `Grep` to find files by name (use `Glob` instead)
- ❌ Using `Read` to search for patterns (use `Grep` instead)
- ❌ Reading entire large files when you only need a section (use `Read` with offset/limit)
- ❌ Using `Glob` to search file contents (use `Grep` instead)

## Session Summary Skill Usage

**Purpose**: Create comprehensive session summaries before compaction to preserve context across token limit events.

**When to Use**:

- Approaching token limits (75%+ usage or user indicates)
- After major workflow phase completion (Phase 4 or Phase 5)
- Before final deliverable phase (Phase 6)
- End of session or workflow completion
- User explicitly requests session summary

**Skill Path**: `plugins/cc10x/skills/session-summary/SKILL.md`

**Usage Pattern**:

```
1. Load session-summary skill using Skill tool
2. Execute skill to create comprehensive summary
3. Archive previous session if exists
4. Analyze conversation transcript
5. Extract tool calls, file changes, accomplishments, decisions
6. Save summary to .claude/memory/CURRENT_SESSION.md
7. Archive to .claude/memory/session_summaries/session-{timestamp}.md
```

**Integration**:

- Integrated into all workflows as Phase 5.5 - Context Preservation
- Workflows automatically load and execute skill when approaching token limits
- Session summaries complement programmatic snapshot extraction
- Post-compact hook loads session summaries as highest priority context source

**Output Format**:

- Session overview (2-3 sentences)
- Files modified (with detailed descriptions)
- Tool calls & operations
- Key accomplishments
- Problems solved
- Technical decisions
- Next steps
- Learning & insights
- Session metrics
- Git repository state
- Active workflow state

**Example**:

```
User: "We're approaching token limits, create a session summary"

Claude: [Loads session-summary skill]
        [Executes archive management]
        [Analyzes conversation]
        [Creates comprehensive summary]
        [Saves to CURRENT_SESSION.md]
        [Outputs summary in conversation]
```
