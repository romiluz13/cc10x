# Implementation Guide for Building Marketplace Features

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           User's Claude Code Instance           │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Marketplaces │  │   Plugins    │            │
│  │  (Catalogs)  │→│  (Installed) │            │
│  └──────────────┘  └──────────────┘            │
│         ↓                  ↓                    │
│  ┌─────────────────────────────────┐           │
│  │      Plugin Components          │           │
│  ├─────────────────────────────────┤           │
│  │ Commands │ Agents │ Skills      │           │
│  │ Hooks    │ MCP    │             │           │
│  └─────────────────────────────────┘           │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Marketplace Implementation

### Core Requirements

1. **Marketplace Discovery**
   - Parse marketplace.json
   - Validate schema
   - Extract plugin metadata

2. **Plugin Resolution**
   - Resolve source (GitHub, Git, local, URL)
   - Download/clone plugin
   - Verify structure

3. **Component Loading**
   - Load commands from `commands/`
   - Load agents from `agents/`
   - Load skills from `skills/*/SKILL.md`
   - Load hooks from `hooks/hooks.json`
   - Load MCP from `.mcp.json`

4. **Lifecycle Management**
   - Install/uninstall
   - Enable/disable
   - Update
   - Version tracking

### Data Structures

#### Marketplace Registry

```typescript
interface MarketplaceRegistry {
  marketplaces: Map<string, Marketplace>;
  plugins: Map<string, InstalledPlugin>;
}

interface Marketplace {
  id: string;
  name: string;
  source: MarketplaceSource;
  plugins: PluginEntry[];
  metadata?: MarketplaceMetadata;
}

interface MarketplaceSource {
  type: 'github' | 'git' | 'local' | 'url';
  location: string;  // repo, url, or path
}

interface PluginEntry {
  name: string;
  source: PluginSource;
  version?: string;
  description?: string;
  // ... metadata
}

interface InstalledPlugin {
  name: string;
  version: string;
  marketplaceId: string;
  installPath: string;
  enabled: boolean;
  components: PluginComponents;
}

interface PluginComponents {
  commands: Command[];
  agents: Agent[];
  skills: Skill[];
  hooks: Hook[];
  mcpServers: MCPServer[];
}
```

#### Skill System

```typescript
interface Skill {
  // Metadata (Level 1 - always loaded)
  name: string;
  description: string;
  allowedTools?: string[];
  
  // Location
  skillPath: string;
  skillMdPath: string;
  
  // Content (Level 2 - loaded when triggered)
  instructions?: string;
  
  // Additional files (Level 3 - loaded as needed)
  bundledFiles: string[];
}

interface SkillRegistry {
  skills: Map<string, Skill>;
  
  // Load skill metadata (startup)
  loadMetadata(skillPath: string): Skill;
  
  // Load skill instructions (when triggered)
  loadInstructions(skillName: string): string;
  
  // Load additional file (as needed)
  loadFile(skillName: string, filePath: string): string;
}
```

## Plugin Loading Flow

```typescript
async function loadPlugin(pluginPath: string): Promise<Plugin> {
  // 1. Load manifest
  const manifest = await loadManifest(pluginPath);
  
  // 2. Discover components
  const components = {
    commands: await discoverCommands(pluginPath, manifest),
    agents: await discoverAgents(pluginPath, manifest),
    skills: await discoverSkills(pluginPath, manifest),
    hooks: await loadHooks(pluginPath, manifest),
    mcpServers: await loadMCPServers(pluginPath, manifest)
  };
  
  // 3. Register components
  await registerComponents(components);
  
  return {
    name: manifest.name,
    version: manifest.version,
    components
  };
}

async function discoverSkills(
  pluginPath: string,
  manifest: Manifest
): Promise<Skill[]> {
  const skillsPath = path.join(pluginPath, 'skills');
  const skillDirs = await fs.readdir(skillsPath);
  
  const skills: Skill[] = [];
  
  for (const dir of skillDirs) {
    const skillMdPath = path.join(skillsPath, dir, 'SKILL.md');
    
    if (await fs.exists(skillMdPath)) {
      // Load only metadata (Level 1)
      const metadata = await loadSkillMetadata(skillMdPath);
      
      skills.push({
        name: metadata.name,
        description: metadata.description,
        allowedTools: metadata.allowedTools,
        skillPath: path.join(skillsPath, dir),
        skillMdPath,
        bundledFiles: await listBundledFiles(path.join(skillsPath, dir))
      });
    }
  }
  
  return skills;
}

async function loadSkillMetadata(skillMdPath: string): Promise<SkillMetadata> {
  const content = await fs.readFile(skillMdPath, 'utf-8');
  
  // Parse YAML frontmatter
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    throw new Error('Missing YAML frontmatter');
  }
  
  const yaml = parseYAML(match[1]);
  
  // Validate
  validateSkillMetadata(yaml);
  
  return yaml;
}
```

## Skill Progressive Loading Implementation

```typescript
class SkillLoader {
  private loadedInstructions = new Map<string, string>();
  private loadedFiles = new Map<string, string>();
  
  // Level 1: Load metadata (at startup)
  async loadAllMetadata(): Promise<SkillMetadata[]> {
    const skills = await this.discoverSkills();
    
    // Only parse YAML frontmatter, not body!
    return skills.map(skill => ({
      name: skill.name,
      description: skill.description
    }));
  }
  
  // Level 2: Load instructions (when triggered)
  async loadInstructions(skillName: string): Promise<string> {
    if (this.loadedInstructions.has(skillName)) {
      return this.loadedInstructions.get(skillName)!;
    }
    
    const skill = this.getSkill(skillName);
    const content = await fs.readFile(skill.skillMdPath, 'utf-8');
    
    // Parse YAML frontmatter and body
    const { body } = this.parseMarkdown(content);
    
    this.loadedInstructions.set(skillName, body);
    return body;
  }
  
  // Level 3: Load additional file (as needed)
  async loadFile(skillName: string, fileName: string): Promise<string> {
    const key = `${skillName}:${fileName}`;
    
    if (this.loadedFiles.has(key)) {
      return this.loadedFiles.get(key)!;
    }
    
    const skill = this.getSkill(skillName);
    const filePath = path.join(skill.skillPath, fileName);
    const content = await fs.readFile(filePath, 'utf-8');
    
    this.loadedFiles.set(key, content);
    return content;
  }
}
```

## Skill Matching Algorithm

```typescript
interface SkillMatcher {
  // Match skills to user request
  matchSkills(
    userPrompt: string,
    availableSkills: SkillMetadata[]
  ): SkillMetadata[];
}

class SemanticSkillMatcher implements SkillMatcher {
  matchSkills(
    userPrompt: string,
    availableSkills: SkillMetadata[]
  ): SkillMetadata[] {
    const matches: Array<{skill: SkillMetadata, score: number}> = [];
    
    for (const skill of availableSkills) {
      const score = this.calculateMatchScore(
        userPrompt,
        skill.description
      );
      
      if (score > 0.3) {  // Threshold
        matches.push({ skill, score });
      }
    }
    
    // Sort by relevance
    matches.sort((a, b) => b.score - a.score);
    
    // Return top matches
    return matches.slice(0, 3).map(m => m.skill);
  }
  
  private calculateMatchScore(
    prompt: string,
    description: string
  ): number {
    const promptLower = prompt.toLowerCase();
    const descLower = description.toLowerCase();
    
    // Extract keywords from description
    const keywords = this.extractKeywords(descLower);
    
    // Count keyword matches
    let matches = 0;
    for (const keyword of keywords) {
      if (promptLower.includes(keyword)) {
        matches++;
      }
    }
    
    // Semantic similarity (simplified)
    const score = matches / keywords.length;
    
    return score;
  }
  
  private extractKeywords(description: string): string[] {
    // Extract important terms
    // In production: Use embeddings or NLP
    return description
      .split(/\s+/)
      .filter(word => word.length > 3)
      .slice(0, 20);
  }
}
```

## Marketplace Source Handlers

```typescript
interface SourceHandler {
  fetch(source: PluginSource): Promise<string>;  // Returns path
}

class GitHubSourceHandler implements SourceHandler {
  async fetch(source: GitHubSource): Promise<string> {
    const { repo } = source;
    const [owner, repoName] = repo.split('/');
    
    // 1. Clone repository
    const tempDir = await this.createTempDir();
    await exec(`git clone https://github.com/${repo} ${tempDir}`);
    
    // 2. Verify .claude-plugin/plugin.json exists
    const pluginJsonPath = path.join(tempDir, '.claude-plugin', 'plugin.json');
    if (!await fs.exists(pluginJsonPath)) {
      throw new Error('Invalid plugin: missing .claude-plugin/plugin.json');
    }
    
    // 3. Return path
    return tempDir;
  }
}

class GitSourceHandler implements SourceHandler {
  async fetch(source: GitSource): Promise<string> {
    const { url } = source;
    
    const tempDir = await this.createTempDir();
    await exec(`git clone ${url} ${tempDir}`);
    
    // Verify structure
    const pluginJsonPath = path.join(tempDir, '.claude-plugin', 'plugin.json');
    if (!await fs.exists(pluginJsonPath)) {
      throw new Error('Invalid plugin structure');
    }
    
    return tempDir;
  }
}

class LocalSourceHandler implements SourceHandler {
  async fetch(source: LocalSource): Promise<string> {
    const { path: localPath } = source;
    
    // Validate path exists
    if (!await fs.exists(localPath)) {
      throw new Error(`Path not found: ${localPath}`);
    }
    
    // Return absolute path
    return path.resolve(localPath);
  }
}
```

## Component Registration

```typescript
class ComponentRegistry {
  private commands = new Map<string, Command>();
  private agents = new Map<string, Agent>();
  private skills = new Map<string, Skill>();
  private hooks: Hook[] = [];
  
  async registerPlugin(plugin: Plugin): Promise<void> {
    // Register each component type
    for (const cmd of plugin.components.commands) {
      this.registerCommand(cmd, plugin);
    }
    
    for (const agent of plugin.components.agents) {
      this.registerAgent(agent, plugin);
    }
    
    for (const skill of plugin.components.skills) {
      this.registerSkill(skill, plugin);
    }
    
    for (const hook of plugin.components.hooks) {
      this.registerHook(hook, plugin);
    }
  }
  
  private registerSkill(skill: Skill, plugin: Plugin): void {
    // Check for conflicts
    if (this.skills.has(skill.name)) {
      const existing = this.skills.get(skill.name)!;
      console.warn(
        `Skill name conflict: ${skill.name} ` +
        `(existing: ${existing.source}, new: ${plugin.name})`
      );
      // Plugin skills have lower priority than project/user skills
      return;
    }
    
    // Register skill
    this.skills.set(skill.name, {
      ...skill,
      source: `plugin:${plugin.name}`
    });
    
    console.log(`Registered skill: ${skill.name} from ${plugin.name}`);
  }
}
```

## Hook Execution Engine

```typescript
class HookExecutor {
  async executeHooks(
    event: HookEvent,
    context: HookContext
  ): Promise<HookResult[]> {
    // Find matching hooks
    const matchingHooks = this.findMatchingHooks(event, context);
    
    if (matchingHooks.length === 0) {
      return [];
    }
    
    // Execute in parallel
    const results = await Promise.all(
      matchingHooks.map(hook => this.executeHook(hook, context))
    );
    
    // Process results
    return this.processResults(results, event);
  }
  
  private async executeHook(
    hook: Hook,
    context: HookContext
  ): Promise<HookResult> {
    // Prepare input
    const input = this.prepareHookInput(hook, context);
    
    // Execute command
    const proc = spawn(hook.command, {
      cwd: context.cwd,
      env: {
        ...process.env,
        CLAUDE_PROJECT_DIR: context.projectDir,
        CLAUDE_PLUGIN_ROOT: hook.pluginRoot
      },
      timeout: hook.timeout || 60000
    });
    
    // Send input via stdin
    proc.stdin.write(JSON.stringify(input));
    proc.stdin.end();
    
    // Collect output
    const stdout = await collectStream(proc.stdout);
    const stderr = await collectStream(proc.stderr);
    const exitCode = await proc.exitCode;
    
    return {
      hook,
      exitCode,
      stdout,
      stderr
    };
  }
  
  private processResults(
    results: HookResult[],
    event: HookEvent
  ): ProcessedResult {
    // Check for blocking errors (exit code 2)
    const blockers = results.filter(r => r.exitCode === 2);
    
    if (blockers.length > 0) {
      return {
        blocked: true,
        reason: blockers.map(b => b.stderr).join('\n')
      };
    }
    
    // Collect outputs
    const outputs = results
      .filter(r => r.exitCode === 0)
      .map(r => r.stdout);
    
    return {
      blocked: false,
      outputs
    };
  }
}
```

## Skill Invocation Implementation

```typescript
class SkillInvoker {
  private skillLoader: SkillLoader;
  private skillMatcher: SkillMatcher;
  
  async handleUserRequest(prompt: string): Promise<void> {
    // 1. Match relevant skills
    const matchedSkills = this.skillMatcher.matchSkills(
      prompt,
      this.skillLoader.getAllMetadata()
    );
    
    // 2. For each matched skill
    for (const skillMeta of matchedSkills) {
      // Load Level 2: Instructions
      const instructions = await this.skillLoader.loadInstructions(
        skillMeta.name
      );
      
      // Add to context
      this.addToContext({
        type: 'skill_instructions',
        skillName: skillMeta.name,
        content: instructions
      });
      
      // 3. Monitor for file references
      // When Claude reads: cat skill-path/REFERENCE.md
      // → Load Level 3: Additional file
      this.onFileRead((filePath) => {
        if (this.isSkillFile(skillMeta.name, filePath)) {
          return this.skillLoader.loadFile(skillMeta.name, filePath);
        }
      });
    }
  }
}
```

## Subagent Delegation Implementation

```typescript
class SubagentOrchestrator {
  private agents = new Map<string, Agent>();
  
  async delegateToSubagent(
    agentName: string,
    task: string
  ): Promise<string> {
    const agent = this.agents.get(agentName);
    if (!agent) {
      throw new Error(`Agent not found: ${agentName}`);
    }
    
    // Create separate context for subagent
    const subagentContext = new Context({
      systemPrompt: agent.prompt,
      tools: agent.tools || this.getAllTools(),
      model: agent.model || 'sonnet'
    });
    
    // Execute task in subagent context
    const result = await this.executeInContext(
      subagentContext,
      task
    );
    
    // Return result (don't pollute main context)
    return result;
  }
  
  private async executeInContext(
    context: Context,
    task: string
  ): Promise<string> {
    // Use Messages API with subagent configuration
    const response = await anthropic.messages.create({
      model: context.model,
      system: context.systemPrompt,
      messages: [{
        role: 'user',
        content: task
      }],
      tools: context.tools,
      max_tokens: 4096
    });
    
    return response.content[0].text;
  }
}
```

## Settings Merge Implementation

```typescript
class SettingsManager {
  async loadSettings(): Promise<Settings> {
    // Load from multiple sources (priority order)
    const sources = [
      await this.loadEnterpriseSettings(),   // Highest
      await this.loadProjectSettings(),      // High
      await this.loadLocalSettings(),        // Medium
      await this.loadUserSettings()          // Lowest
    ];
    
    // Merge with priority
    return this.mergeSettings(sources);
  }
  
  private mergeSettings(sources: Settings[]): Settings {
    const merged: Settings = {
      extraKnownMarketplaces: {},
      enabledPlugins: [],
      hooks: {}
    };
    
    // Merge from lowest to highest priority
    for (const settings of sources.reverse()) {
      // Marketplaces: Merge
      Object.assign(merged.extraKnownMarketplaces, settings.extraKnownMarketplaces);
      
      // Plugins: Union
      merged.enabledPlugins = [
        ...new Set([...merged.enabledPlugins, ...settings.enabledPlugins])
      ];
      
      // Hooks: Merge by event
      for (const [event, hooks] of Object.entries(settings.hooks)) {
        merged.hooks[event] = [
          ...(merged.hooks[event] || []),
          ...hooks
        ];
      }
    }
    
    return merged;
  }
}
```

## Plugin Validation

```typescript
interface PluginValidator {
  validate(pluginPath: string): ValidationResult;
}

class DefaultPluginValidator implements PluginValidator {
  validate(pluginPath: string): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    
    // Check manifest exists
    const manifestPath = path.join(pluginPath, '.claude-plugin', 'plugin.json');
    if (!fs.existsSync(manifestPath)) {
      errors.push('Missing .claude-plugin/plugin.json');
      return { valid: false, errors, warnings };
    }
    
    // Parse and validate manifest
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    
    if (!manifest.name) {
      errors.push('Manifest missing required field: name');
    }
    
    if (!/^[a-z0-9-]+$/.test(manifest.name)) {
      errors.push('Invalid name format (use kebab-case)');
    }
    
    // Check component directories
    const componentDirs = ['commands', 'agents', 'skills', 'hooks'];
    
    for (const dir of componentDirs) {
      const dirPath = path.join(pluginPath, dir);
      
      if (fs.existsSync(dirPath)) {
        // Verify it's at root, not in .claude-plugin/
        const wrongPath = path.join(pluginPath, '.claude-plugin', dir);
        if (fs.existsSync(wrongPath)) {
          errors.push(
            `Component directory ${dir} should be at plugin root, ` +
            `not inside .claude-plugin/`
          );
        }
      }
    }
    
    // Validate skills
    const skillsPath = path.join(pluginPath, 'skills');
    if (fs.existsSync(skillsPath)) {
      const skillDirs = fs.readdirSync(skillsPath);
      
      for (const skillDir of skillDirs) {
        const skillMdPath = path.join(skillsPath, skillDir, 'SKILL.md');
        
        if (!fs.existsSync(skillMdPath)) {
          warnings.push(`Skill directory ${skillDir} missing SKILL.md`);
          continue;
        }
        
        // Validate SKILL.md
        const skillErrors = this.validateSkillMd(skillMdPath);
        errors.push(...skillErrors);
      }
    }
    
    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  }
  
  private validateSkillMd(skillMdPath: string): string[] {
    const errors: string[] = [];
    const content = fs.readFileSync(skillMdPath, 'utf-8');
    
    // Check YAML frontmatter
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) {
      errors.push(`${skillMdPath}: Missing YAML frontmatter`);
      return errors;
    }
    
    try {
      const yaml = parseYAML(match[1]);
      
      // Validate required fields
      if (!yaml.name) {
        errors.push(`${skillMdPath}: Missing 'name' field`);
      }
      
      if (!yaml.description) {
        errors.push(`${skillMdPath}: Missing 'description' field`);
      }
      
      // Validate name format
      if (yaml.name && !/^[a-z0-9-]+$/.test(yaml.name)) {
        errors.push(`${skillMdPath}: Invalid name format (use lowercase, numbers, hyphens)`);
      }
      
      // Validate name length
      if (yaml.name && yaml.name.length > 64) {
        errors.push(`${skillMdPath}: Name exceeds 64 characters`);
      }
      
      // Validate description length
      if (yaml.description && yaml.description.length > 1024) {
        errors.push(`${skillMdPath}: Description exceeds 1024 characters`);
      }
      
      // Check for reserved words
      if (yaml.name && /anthropic|claude/.test(yaml.name)) {
        errors.push(`${skillMdPath}: Name contains reserved word`);
      }
      
    } catch (e) {
      errors.push(`${skillMdPath}: Invalid YAML syntax`);
    }
    
    return errors;
  }
}
```

## System Prompt Construction

```typescript
class SystemPromptBuilder {
  buildSystemPrompt(config: SystemPromptConfig): string {
    const sections: string[] = [];
    
    // 1. Base system prompt
    sections.push(config.basePrompt);
    
    // 2. Skill metadata (Level 1)
    if (config.skills.length > 0) {
      sections.push('\n## Available Skills\n');
      
      for (const skill of config.skills) {
        sections.push(
          `- ${skill.name}: ${skill.description}`
        );
      }
    }
    
    // 3. Agent metadata
    if (config.agents.length > 0) {
      sections.push('\n## Available Agents\n');
      
      for (const agent of config.agents) {
        sections.push(
          `- ${agent.name}: ${agent.description}`
        );
      }
    }
    
    // 4. Custom instructions (CLAUDE.md)
    if (config.claudeMd) {
      sections.push('\n## Project Instructions\n');
      sections.push(config.claudeMd);
    }
    
    return sections.join('\n');
  }
}
```

## Database Schema (for Persistence)

```sql
-- Marketplaces
CREATE TABLE marketplaces (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source_type TEXT NOT NULL,  -- github, git, local, url
  source_location TEXT NOT NULL,
  metadata JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Plugins
CREATE TABLE plugins (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT NOT NULL,
  marketplace_id TEXT NOT NULL,
  install_path TEXT NOT NULL,
  enabled BOOLEAN DEFAULT TRUE,
  manifest JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (marketplace_id) REFERENCES marketplaces(id)
);

-- Skills
CREATE TABLE skills (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL,
  skill_path TEXT NOT NULL,
  source TEXT NOT NULL,  -- project, user, plugin:name
  allowed_tools TEXT,     -- JSON array
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commands
CREATE TABLE commands (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  file_path TEXT NOT NULL,
  source TEXT NOT NULL,  -- project, user, plugin:name
  namespace TEXT,         -- subdirectory name
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  transcript_path TEXT NOT NULL,
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ended_at TIMESTAMP,
  model TEXT,
  total_tokens INTEGER DEFAULT 0,
  total_cost REAL DEFAULT 0
);
```

## Performance Optimizations

### 1. Lazy Loading

```typescript
class LazySkillLoader {
  // Don't load skill body until needed
  private loadedSkills = new Map<string, string>();
  
  async getSkillInstructions(skillName: string): Promise<string> {
    if (!this.loadedSkills.has(skillName)) {
      const instructions = await this.loadFromDisk(skillName);
      this.loadedSkills.set(skillName, instructions);
    }
    return this.loadedSkills.get(skillName)!;
  }
}
```

### 2. Caching

```typescript
class CachedMarketplaceLoader {
  private cache = new Map<string, Marketplace>();
  private cacheExpiry = 3600000; // 1 hour
  
  async loadMarketplace(source: string): Promise<Marketplace> {
    const cached = this.cache.get(source);
    
    if (cached && !this.isExpired(cached)) {
      return cached;
    }
    
    const marketplace = await this.fetchMarketplace(source);
    this.cache.set(source, {
      ...marketplace,
      cachedAt: Date.now()
    });
    
    return marketplace;
  }
}
```

### 3. Parallel Loading

```typescript
async function loadPlugins(pluginSources: PluginSource[]): Promise<Plugin[]> {
  // Load plugins in parallel
  return await Promise.all(
    pluginSources.map(source => loadPlugin(source))
  );
}
```

## Testing Strategy

### Unit Tests

```typescript
describe('SkillLoader', () => {
  it('should load skill metadata only', async () => {
    const loader = new SkillLoader();
    const metadata = await loader.loadMetadata('test-skill');
    
    expect(metadata.name).toBe('test-skill');
    expect(metadata.description).toBeDefined();
    // Body should NOT be loaded yet
  });
  
  it('should load instructions when triggered', async () => {
    const loader = new SkillLoader();
    const instructions = await loader.loadInstructions('test-skill');
    
    expect(instructions).toContain('## Quick Start');
  });
});
```

### Integration Tests

```typescript
describe('Plugin System', () => {
  it('should install and load plugin', async () => {
    const marketplace = await addMarketplace('./test-marketplace');
    const plugin = await installPlugin('test-plugin', marketplace.id);
    
    expect(plugin.enabled).toBe(true);
    expect(plugin.components.skills.length).toBeGreaterThan(0);
  });
  
  it('should resolve skill at runtime', async () => {
    await installPlugin('test-plugin', 'test-marketplace');
    
    const matched = await matchSkills('Extract text from PDF');
    
    expect(matched.some(s => s.name === 'pdf-processing')).toBe(true);
  });
});
```

## Security Implementation

### Input Validation

```typescript
function validateHookInput(input: any): HookInput {
  // Validate JSON structure
  if (typeof input !== 'object') {
    throw new Error('Invalid hook input: must be object');
  }
  
  // Sanitize file paths
  if (input.tool_input?.file_path) {
    const filePath = input.tool_input.file_path;
    
    // Block path traversal
    if (filePath.includes('..')) {
      throw new Error('Path traversal blocked');
    }
    
    // Block sensitive files
    const sensitive = ['.env', '.git/', 'id_rsa', '.aws/'];
    if (sensitive.some(s => filePath.includes(s))) {
      throw new Error('Sensitive file access blocked');
    }
  }
  
  return input as HookInput;
}
```

### Sandbox Execution

```typescript
class SandboxedHookExecutor {
  async executeHook(hook: Hook, context: HookContext): Promise<HookResult> {
    // Create sandbox environment
    const sandbox = await this.createSandbox({
      allowedCommands: this.parseAllowedCommands(hook.allowedTools),
      workingDirectory: context.cwd,
      timeout: hook.timeout || 60000
    });
    
    try {
      return await sandbox.execute(hook.command, context);
    } finally {
      await sandbox.cleanup();
    }
  }
}
```

## Error Handling Patterns

```typescript
class RobustPluginLoader {
  async loadPlugin(source: PluginSource): Promise<Plugin | null> {
    try {
      // Fetch plugin
      const pluginPath = await this.fetchPlugin(source);
      
      // Validate structure
      const validation = await this.validatePlugin(pluginPath);
      if (!validation.valid) {
        console.error(`Plugin validation failed:`, validation.errors);
        return null;
      }
      
      // Load components
      const components = await this.loadComponents(pluginPath);
      
      return {
        source,
        path: pluginPath,
        components
      };
      
    } catch (error) {
      console.error(`Failed to load plugin:`, error);
      
      // Clean up
      await this.cleanup(source);
      
      return null;
    }
  }
}
```

## Monitoring & Analytics

```typescript
class UsageTracker {
  trackSkillUsage(skillName: string, success: boolean): void {
    analytics.track('skill_used', {
      skill_name: skillName,
      success,
      timestamp: Date.now()
    });
  }
  
  trackPluginInstall(pluginName: string, marketplaceId: string): void {
    analytics.track('plugin_installed', {
      plugin_name: pluginName,
      marketplace_id: marketplaceId,
      timestamp: Date.now()
    });
  }
  
  trackHookExecution(
    event: string,
    hook: Hook,
    duration: number,
    success: boolean
  ): void {
    analytics.track('hook_executed', {
      event,
      hook_command: hook.command,
      duration_ms: duration,
      success,
      timestamp: Date.now()
    });
  }
}
```

## Implementation Checklist

### Marketplace System
- [ ] Parse marketplace.json
- [ ] Validate schema
- [ ] Handle Git/GitHub/local sources
- [ ] Cache marketplace data
- [ ] Update mechanism
- [ ] Conflict resolution

### Plugin System
- [ ] Load plugin manifest
- [ ] Discover components
- [ ] Register components with priority
- [ ] Handle enable/disable
- [ ] Update plugins
- [ ] Version management

### Skill System (CRITICAL)
- [ ] Load metadata at startup (Level 1)
- [ ] Match skills to requests
- [ ] Load instructions on trigger (Level 2)
- [ ] Load additional files on demand (Level 3)
- [ ] Execute bundled scripts
- [ ] Validate SKILL.md format
- [ ] Handle tool restrictions

### Subagent System
- [ ] Separate context per agent
- [ ] Tool restrictions
- [ ] Model override
- [ ] Automatic delegation
- [ ] Explicit invocation

### Hook System
- [ ] Event triggering
- [ ] Matcher evaluation
- [ ] Parallel execution
- [ ] Input/output handling
- [ ] Timeout enforcement
- [ ] Error handling

### SDK
- [ ] Query interface
- [ ] Streaming support
- [ ] Agent configuration
- [ ] Cost tracking
- [ ] Session management
- [ ] Error handling

