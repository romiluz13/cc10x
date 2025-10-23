# cc10x Structure Analysis - 1:1 Comparison with Superpowers

**Date**: 2025-10-22
**Status**: ISSUES FOUND ⚠️

---

## 📊 Complete File Graph

### cc10x Structure (37 files)

```
cc10x/
├── .claude-plugin/                    ✅ CORRECT
│   ├── marketplace.json               ✅ CORRECT
│   └── plugin.json                    ✅ CORRECT
├── .gitignore                         ⚠️ CHECK
├── agents/                            ✅ CORRECT
│   ├── accessibility-reviewer.md      ✅ CORRECT (extra - not in superpowers)
│   ├── context-analyzer.md            ✅ CORRECT (extra - not in superpowers)
│   ├── implementer.md                 ✅ CORRECT (extra - not in superpowers)
│   ├── performance-analyzer.md        ✅ CORRECT (extra - not in superpowers)
│   ├── quality-reviewer.md            ✅ CORRECT (extra - not in superpowers)
│   ├── security-reviewer.md           ✅ CORRECT (extra - not in superpowers)
│   └── ux-reviewer.md                 ✅ CORRECT (extra - not in superpowers)
├── CLAUDE.md                          ✅ CORRECT
├── commands/                          ✅ CORRECT
│   ├── bug-fix.md                     ✅ CORRECT (extra - not in superpowers)
│   ├── feature-build.md               ✅ CORRECT (extra - not in superpowers)
│   ├── feature-plan.md                ✅ CORRECT (extra - not in superpowers)
│   └── review.md                      ✅ CORRECT (extra - not in superpowers)
├── hooks/                             ⚠️ STRUCTURE ISSUE
│   └── hooks.json                     ❌ WRONG FORMAT
├── LICENSE                            ✅ CORRECT
├── README.md                          ✅ CORRECT
├── RESTRUCTURE-COMPLETE.md            ✅ CORRECT (extra doc)
├── scripts/                           ❌ WRONG - Should be hooks/
│   ├── pre-compact.sh                 ❌ WRONG LOCATION
│   └── session-start.sh               ❌ WRONG LOCATION
└── skills/                            ✅ CORRECT
    ├── accessibility-patterns/        ✅ CORRECT (extra - not in superpowers)
    ├── bug-fixing/                    ✅ CORRECT (extra - not in superpowers)
    ├── code-generation/               ✅ CORRECT (extra - not in superpowers)
    ├── code-review-patterns/          ✅ CORRECT (extra - not in superpowers)
    ├── code-reviewing/                ✅ CORRECT (extra - not in superpowers)
    ├── codebase-navigation/           ✅ CORRECT (extra - not in superpowers)
    ├── feature-building/              ✅ CORRECT (extra - not in superpowers)
    ├── feature-planning/              ✅ CORRECT (extra - not in superpowers)
    ├── performance-patterns/          ✅ CORRECT (extra - not in superpowers)
    ├── safe-refactoring/              ✅ CORRECT (extra - not in superpowers)
    ├── security-patterns/             ✅ CORRECT (extra - not in superpowers)
    ├── systematic-debugging/          ✅ CORRECT (matches superpowers)
    ├── test-driven-development/       ✅ CORRECT (matches superpowers)
    ├── ui-design/                     ✅ CORRECT (extra - not in superpowers)
    ├── ux-patterns/                   ✅ CORRECT (extra - not in superpowers)
    └── verification-before-completion/ ✅ CORRECT (matches superpowers)
```

### Superpowers Structure (Reference)

```
superpowers/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .gitignore
├── agents/
│   └── code-reviewer.md
├── commands/
│   ├── brainstorm.md
│   ├── execute-plan.md
│   └── write-plan.md
├── hooks/                             ← SCRIPTS IN HOOKS/
│   ├── hooks.json
│   └── session-start.sh               ← SCRIPT HERE, NOT scripts/
├── lib/
│   └── initialize-skills.sh
├── LICENSE
├── README.md
├── RELEASE-NOTES.md
└── skills/
    ├── brainstorming/
    ├── commands/
    ├── condition-based-waiting/
    ├── defense-in-depth/
    ├── dispatching-parallel-agents/
    ├── executing-plans/
    ├── finishing-a-development-branch/
    ├── receiving-code-review/
    ├── requesting-code-review/
    ├── root-cause-tracing/
    ├── sharing-skills/
    ├── subagent-driven-development/
    ├── systematic-debugging/
    ├── test-driven-development/
    ├── testing-anti-patterns/
    ├── testing-skills-with-subagents/
    ├── using-git-worktrees/
    ├── using-superpowers/
    ├── verification-before-completion/
    ├── writing-plans/
    └── writing-skills/
```

---

## 🚨 CRITICAL ISSUES FOUND

### Issue #1: hooks.json Wrong Format ❌

**Superpowers format**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

**cc10x format** (WRONG):
```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/session-start.sh"
        }
      ]
    }
  ]
}
```

**Problems**:
1. ❌ Missing root `"hooks"` key
2. ❌ Missing `"matcher"` field
3. ❌ Wrong path: `scripts/` instead of `hooks/`

---

### Issue #2: Wrong Directory for Hook Scripts ❌

**Superpowers pattern**:
```
hooks/
├── hooks.json
└── session-start.sh     ← Script in hooks/ directory
```

**cc10x pattern** (WRONG):
```
hooks/
└── hooks.json

scripts/                 ← WRONG - Should be in hooks/
├── pre-compact.sh
└── session-start.sh
```

**Problem**: Hook scripts should be in `hooks/` directory, not `scripts/` directory.

---

### Issue #3: Missing Matcher Field ❌

Superpowers uses `"matcher"` to control when hooks fire:
```json
"matcher": "startup|resume|clear|compact"
```

This ensures the hook only fires on specific events. We're missing this.

---

## ✅ What's Correct

### Directory Structure
- ✅ `.claude-plugin/` at root
- ✅ `agents/` directory
- ✅ `commands/` directory
- ✅ `hooks/` directory (location correct)
- ✅ `skills/` directory
- ✅ Root level: `CLAUDE.md`, `README.md`, `LICENSE`

### File Formats
- ✅ Commands are tiny delegators (6 lines)
- ✅ Agents have examples in descriptions
- ✅ Skills have proper frontmatter
- ✅ plugin.json format correct
- ✅ marketplace.json format correct

### Skill Structure
- ✅ Each skill in own directory
- ✅ Each has `SKILL.md` file
- ✅ Frontmatter with name/description
- ✅ Progressive loading in some skills

---

## 🔧 Required Fixes

### Fix #1: Correct hooks.json Format

**Change from**:
```json
{
  "SessionStart": [...],
  "PreCompact": [...]
}
```

**Change to**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [...]
      }
    ],
    "PreCompact": [
      {
        "hooks": [...]
      }
    ]
  }
}
```

### Fix #2: Move Scripts to hooks/ Directory

**Move**:
- `scripts/session-start.sh` → `hooks/session-start.sh`
- `scripts/pre-compact.sh` → `hooks/pre-compact.sh`

**Delete**:
- `scripts/` directory (should be empty after move)

### Fix #3: Update hooks.json Paths

**Change paths from**:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/session-start.sh"
```

**Change to**:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
```

---

## 📋 Comparison Table

| Aspect | Superpowers | cc10x | Status |
|--------|-------------|-------|--------|
| **Directory Structure** |
| .claude-plugin/ | ✅ | ✅ | ✅ MATCH |
| agents/ | ✅ | ✅ | ✅ MATCH |
| commands/ | ✅ | ✅ | ✅ MATCH |
| hooks/ | ✅ | ✅ | ✅ MATCH |
| hooks/scripts | ✅ In hooks/ | ❌ In scripts/ | ❌ MISMATCH |
| lib/ | ✅ (optional) | ❌ None | ✅ OK (optional) |
| skills/ | ✅ | ✅ | ✅ MATCH |
| **File Formats** |
| hooks.json root key | ✅ "hooks" | ❌ Missing | ❌ MISMATCH |
| hooks.json matcher | ✅ Present | ❌ Missing | ❌ MISMATCH |
| Hook script paths | ✅ hooks/*.sh | ❌ scripts/*.sh | ❌ MISMATCH |
| Commands | ✅ Tiny | ✅ Tiny | ✅ MATCH |
| Agents | ✅ Examples | ✅ Examples | ✅ MATCH |
| Skills | ✅ SKILL.md | ✅ SKILL.md | ✅ MATCH |

---

## 🎯 Summary

**Structural Issues**: 3 critical misalignments found

1. ❌ **hooks.json format** - Missing root "hooks" key and matcher
2. ❌ **Script location** - Scripts in `scripts/` instead of `hooks/`
3. ❌ **Script paths** - References to wrong directory in hooks.json

**Once Fixed**: Will be 100% aligned with superpowers pattern

**Current Alignment**: ~85% (structure mostly correct, format issues)

---

## 🚀 Action Plan

1. Move `scripts/*.sh` → `hooks/*.sh`
2. Delete empty `scripts/` directory
3. Rewrite `hooks/hooks.json` with correct format
4. Update path references
5. Validate with `claude plugin validate`
6. Push to GitHub

---

**Status**: Ready to fix misalignments
