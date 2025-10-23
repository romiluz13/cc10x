# Changelog

All notable changes to cc10x are documented here.

## [1.1.0] - 2025-10-23

### Added
- **Risk Assessment Integration**: Phase 3b in feature planning with probability x impact scoring
- **Development Constitution**: Formal `.claude/memory/CONSTITUTION.md` defining immutable principles
- **Workflow Visualizations**: Mermaid diagrams in all 4 core commands
- **Validation Command**: New `/validate` for cross-artifact consistency checks
- **Video Production Script**: Complete walkthrough script for demos
- **Installation Guides**: Multiple installation methods documented

### Enhanced
- Feature planning now includes risk identification, scoring, and mitigation
- All commands have visual workflow diagrams
- README updated with constitution section
- Documentation massively improved

### Fixed
- Installation process clarified (manual copy method documented)
- All YAML frontmatter validated
- Plugin structure verified against official Anthropic specs
- Removed confusing marketplace.json (cc10x is standalone plugin)

### Changed
- Archived all planning/research docs to `docs/archive/`
- Production structure cleaned
- Version bumped to 1.1.0

## [1.0.0] - 2025-10-22

### Added
- Initial release
- 4 core commands: feature-plan, feature-build, bug-fix, review
- 7 sub-agents for specialized tasks
- 16 skills for domain expertise
- Progressive 3-stage loading (93% token savings)
- Auto-healing context preservation
- Strict TDD enforcement
- Multi-dimensional parallel code review

