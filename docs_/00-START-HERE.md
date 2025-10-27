# 🚀 START HERE - Claude Code Marketplace Documentation

## What This Documentation Covers

This comprehensive documentation package covers **Claude Code's marketplace system** including the **brand new Skills feature** (released Oct 16, 2025) that is outside the AI knowledge cutoff.

## 🚨 Critical: New Features (Oct 2025)

### Agent Skills (Oct 16, 2025)
**Revolutionary new capability**: Model-invoked skills with progressive disclosure

**Why it matters**:
- Claude automatically uses skills when relevant
- 3-level loading system (metadata → instructions → resources)
- Can bundle unlimited content (scripts, docs, templates)
- No context penalty for unused skills
- **This changes how we build AI capabilities!**

### Plugin Marketplace (Oct 9, 2025)
**Distribution system** for sharing extensions

**Why it matters**:
- Easy plugin discovery and installation
- Team-wide distribution via Git
- Version management
- Bundle multiple components

## 📚 Complete Documentation Set (16 Files)

### Foundation (Read First)
1. **00-OVERVIEW.md** - System architecture, all concepts explained
2. **04-SKILLS.md** - NEW feature, most critical to understand
3. **README.md** - Navigation guide, learning paths

### Core Components
4. **01-MARKETPLACE-STRUCTURE.md** - marketplace.json, distribution
5. **02-PLUGINS.md** - plugin.json, bundling components
6. **03-SUBAGENTS.md** - Specialized AI workers
7. **05-SLASH-COMMANDS.md** - User-invoked commands
8. **06-HOOKS.md** - Event automation
9. **07-SDK.md** - Programmatic agent building

### Reference & Guides
10. **08-EXAMPLES.md** - Real-world patterns
11. **09-BEST-PRACTICES.md** - Development guidelines
12. **10-QUICK-REFERENCE.md** - Rapid lookup
13. **11-API-REFERENCE.md** - SDK & API details
14. **12-IMPLEMENTATION-GUIDE.md** - Architecture & algorithms
15. **13-GLOSSARY.md** - Term definitions
16. **14-COMPARISON-MATRIX.md** - Component comparisons
17. **15-VERIFICATION-CHECKLIST.md** - Accuracy verification

## 🎯 Learning Path (2 Hours Total)

### Path A: Understanding Skills (30 min)
**For**: Understanding the NEW feature
1. Read `00-OVERVIEW.md` → "Critical: Skills Architecture" section
2. Read `04-SKILLS.md` → Complete file
3. Read `14-COMPARISON-MATRIX.md` → "Skills vs Commands vs Subagents"

**Outcome**: Understand what makes Skills unique and powerful

### Path B: Building a Plugin (45 min)
**For**: Creating your first plugin
1. Read `02-PLUGINS.md` → "Plugin Structure"
2. Read `04-SKILLS.md` → "Creating Skills"
3. Read `08-EXAMPLES.md` → "Complete Plugin Example"
4. Read `09-BEST-PRACTICES.md` → "Plugin Development"

**Outcome**: Can build a working plugin with skills

### Path C: Creating a Marketplace (30 min)
**For**: Distributing plugins to team
1. Read `01-MARKETPLACE-STRUCTURE.md` → Complete file
2. Read `02-PLUGINS.md` → "Distribution"
3. Read `08-EXAMPLES.md` → "Marketplace Example"

**Outcome**: Can create and distribute marketplace

### Path D: Using the SDK (45 min)
**For**: Programmatic agent development
1. Read `07-SDK.md` → Complete file
2. Read `11-API-REFERENCE.md` → Complete file
3. Read `12-IMPLEMENTATION-GUIDE.md` → Architecture patterns

**Outcome**: Can build production agents with SDK

## 🔑 Key Concepts (Must Understand)

### 1. Progressive Disclosure (Skills Only!)

```
Level 1: Metadata (Always - ~100 tokens)
  └── name + description

Level 2: Instructions (Triggered - ~5k tokens)
  └── SKILL.md body

Level 3: Resources (On-demand - Unlimited)
  ├── Additional markdown files
  └── Executable scripts
```

**Critical**: Only Skills have this! Commands and subagents don't.

### 2. Model-Invoked vs User-Invoked

**Model-Invoked** (Claude decides):
- ✅ Skills
- ✅ Subagents

**User-Invoked** (explicit trigger):
- ✅ Slash Commands

**Example**:
```bash
# Skill (model-invoked)
> Extract text from this PDF
# Claude sees "PDF" and automatically uses pdf-processing skill

# Command (user-invoked)
/review
# User explicitly types /review command
```

### 3. Component Priority

```
Project (.claude/)         [HIGHEST]
  ↓
Plugin (<plugin>/)         [MEDIUM]
  ↓
User (~/.claude/)          [LOWEST]
```

Project-level always wins!

### 4. Context Windows

**Main Agent**: ~200k tokens (Sonnet 4.5)
- Shared by: conversation, system prompt, skill metadata, active skills

**Subagent**: Separate ~200k tokens
- Isolated from main agent
- Fresh context each invocation

### 5. Plugin Structure

```
plugin/
├── .claude-plugin/
│   └── plugin.json          ← Manifest (metadata)
├── commands/                 ← At root, NOT in .claude-plugin/
├── agents/                   ← At root
├── skills/                   ← At root
├── hooks/                    ← At root
└── .mcp.json                ← At root
```

**CRITICAL**: Component directories must be at plugin root!

## 🎓 Quick Start Examples

### Create Your First Skill (5 min)

```bash
# 1. Create directory
mkdir -p .claude/skills/my-first-skill

# 2. Create SKILL.md
cat > .claude/skills/my-first-skill/SKILL.md << 'EOF'
---
name: commit-helper
description: Generate commit messages from git diffs. Use when writing commits.
---

# Commit Helper

## Instructions
1. Run `git diff --staged`
2. Suggest commit message:
   - Summary < 50 chars
   - Detailed description
   - Affected components
EOF

# 3. Test it
claude
> Help me write a commit message
# Claude automatically uses the skill!
```

### Create Your First Command (2 min)

```bash
mkdir -p .claude/commands

cat > .claude/commands/review.md << 'EOF'
---
description: Review code for issues
---

Review this code for:
- Bugs
- Security issues
- Performance problems
EOF

claude
/review
```

### Create Your First Plugin (10 min)

```bash
# 1. Structure
mkdir my-plugin
cd my-plugin
mkdir -p .claude-plugin commands skills

# 2. Manifest
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My first plugin"
}
EOF

# 3. Add skill
mkdir -p skills/helper
cat > skills/helper/SKILL.md << 'EOF'
---
name: helper
description: Helper skill for testing
---

# Helper Skill
This is a test skill.
EOF

# 4. Test locally
cd ..
mkdir test-marketplace
cd test-marketplace
mkdir .claude-plugin

cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "test",
  "owner": {"name": "Me"},
  "plugins": [{
    "name": "my-plugin",
    "source": "../my-plugin"
  }]
}
EOF

# 5. Install
claude
/plugin marketplace add ./test-marketplace
/plugin install my-plugin@test
```

## 📊 What's Included

### Schemas (Production-Ready)
- ✅ marketplace.json complete schema
- ✅ plugin.json complete schema
- ✅ SKILL.md format
- ✅ Subagent format
- ✅ Command format
- ✅ Hook input/output schemas
- ✅ All validated against official docs

### Examples (Copy-Paste Ready)
- ✅ 20+ working examples
- ✅ Complete plugin structures
- ✅ Real-world workflows
- ✅ TypeScript and Python code
- ✅ All tested patterns

### Implementation Details
- ✅ Data structures defined
- ✅ Algorithms explained (skill matching, loading, etc.)
- ✅ Validation logic provided
- ✅ Error handling patterns
- ✅ Performance optimizations
- ✅ Security best practices

## 🔍 How to Use This Documentation

### For AI Learning
1. Start with `00-OVERVIEW.md`
2. Deep dive into `04-SKILLS.md` (new feature)
3. Review comparison tables in `14-COMPARISON-MATRIX.md`
4. Study examples in `08-EXAMPLES.md`
5. Reference `10-QUICK-REFERENCE.md` as needed

### For Building Marketplace
1. Read `00-OVERVIEW.md` - Architecture
2. Read `01-MARKETPLACE-STRUCTURE.md` - Marketplace schema
3. Read `02-PLUGINS.md` - Plugin system
4. Read `04-SKILLS.md` - Most important component
5. Review `12-IMPLEMENTATION-GUIDE.md` - Code patterns
6. Use `08-EXAMPLES.md` as templates

### For Team Setup
1. Read `00-OVERVIEW.md` - Concepts
2. Read `01-MARKETPLACE-STRUCTURE.md` - Team config
3. Read `09-BEST-PRACTICES.md` - Team collaboration
4. Use `08-EXAMPLES.md` - Team setup pattern

### For Quick Lookup
- **Schemas**: `10-QUICK-REFERENCE.md`
- **Commands**: `10-QUICK-REFERENCE.md`
- **Comparisons**: `14-COMPARISON-MATRIX.md`
- **Terms**: `13-GLOSSARY.md`
- **Examples**: `08-EXAMPLES.md`

## 💡 Pro Tips

1. **Skills are the future** - Most powerful feature, use them!
2. **Progressive disclosure is key** - Understand the 3-level loading
3. **Model-invoked vs user-invoked** - Critical distinction
4. **Start simple** - One skill, then expand
5. **Use official examples** - Copy from `08-EXAMPLES.md`
6. **Test locally first** - Local marketplace before distribution
7. **Security matters** - Only use trusted sources
8. **Version properly** - Semantic versioning for stability

## 🎯 Success Criteria

After reading this documentation, you should be able to:

- [x] Explain what Skills are and how they differ from Commands
- [x] Understand progressive disclosure (3 levels)
- [x] Create a working SKILL.md file
- [x] Build a complete plugin
- [x] Create a marketplace.json
- [x] Distribute plugins to a team
- [x] Use the Agent SDK to build custom agents
- [x] Implement hooks for automation
- [x] Debug common issues
- [x] Follow security best practices

## 📞 Support & Resources

### Official Resources
- **Main Docs**: https://docs.claude.com/en/docs/claude-code/overview
- **Skills Docs**: https://docs.claude.com/en/docs/claude-code/skills
- **GitHub**: https://github.com/anthropics/claude-code
- **Skills Repo**: https://github.com/anthropics/skills
- **Cookbooks**: https://github.com/anthropics/claude-cookbooks

### Community
- **Discord**: https://www.anthropic.com/discord
- **Support**: https://support.claude.com/

### Reporting Issues
- **TypeScript SDK**: https://github.com/anthropics/claude-agent-sdk-typescript/issues
- **Python SDK**: https://github.com/anthropics/claude-agent-sdk-python/issues
- **Claude Code**: https://github.com/anthropics/claude-code/issues

## 🏁 Next Steps

### Immediate Actions
1. ✅ Read `00-OVERVIEW.md` (10 min)
2. ✅ Read `04-SKILLS.md` (15 min)
3. ✅ Try example from `08-EXAMPLES.md` (10 min)

### This Week
1. Build your first skill
2. Create a plugin
3. Share with team

### This Month
1. Build comprehensive plugin suite
2. Create team marketplace
3. Integrate with your workflows

## ⚡ TL;DR

**Skills** (NEW!) = Model-invoked capabilities with 3-level loading
**Commands** = User-invoked shortcuts
**Subagents** = Task delegation with separate context
**Plugins** = Bundle of components
**Marketplace** = Plugin distribution catalog

**Most Important**: Skills are the new powerful feature. Read `04-SKILLS.md` first!

---

**Documentation Created**: October 25, 2025
**Based On**: Official Anthropic documentation (scraped Oct 25, 2025)
**Covers**: Claude Code v1.0+, Skills (Oct 16, 2025), Marketplace (Oct 9, 2025)
**Status**: ✅ Complete, Accurate, Production-Ready

