# Changelog

All notable changes to cc10x are documented here.

## [1.1.0] - 2025-10-23

### 🎉 Major Change: Transformed to Marketplace

cc10x is now a **marketplace** that distributes the cc10x plugin, following the official Anthropic marketplace pattern.

### Added
- **Marketplace Structure**: Proper marketplace.json with plugin catalog
- **Plugin Subdirectory**: All plugin files now in `plugins/cc10x/`
- **Clean Separation**: Marketplace docs vs plugin docs
- **Professional Structure**: Matches EveryInc/every-marketplace pattern

### Installation Method Changed

**Old (Standalone):**
```bash
# Manual copy required
cp -r cc10x/{.claude-plugin,commands,agents,skills,hooks} .
```

**New (Marketplace):**
```bash
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
```

Much simpler and follows Claude Code conventions!

### Features (Plugin v1.1.0)
- **Risk Assessment**: Phase 3b in feature planning with probability x impact scoring
- **Development Constitution**: Formal governance document
- **Workflow Visualizations**: Mermaid diagrams in all commands
- **Validation Command**: Cross-artifact consistency checks
- **5 Commands**: feature-plan, feature-build, bug-fix, review, validate
- **7 Sub-Agents**: Specialized AI workers
- **16 Skills**: Domain expertise modules
- **3 Hooks**: Automation scripts

### Structure
```
cc10x/                        (Marketplace)
  ├── .claude-plugin/
  │   └── marketplace.json    (Marketplace definition)
  ├── plugins/
  │   └── cc10x/              (The plugin)
  │       ├── .claude-plugin/plugin.json
  │       ├── commands/
  │       ├── agents/
  │       ├── skills/
  │       └── hooks/
  └── README.md               (Marketplace docs)
```

## [1.0.0] - 2025-10-22

### Initial Release (Standalone Plugin)
- First version as standalone plugin
- 4 core commands
- Progressive loading, TDD enforcement
- Multi-dimensional code review

