# cc10x v2.1 Quick Start

**Focused orchestration. Does what you ask. Delivers fast.**

---

## Installation

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install
/plugin install cc10x@cc10x

# Verify
/plugin      # Should show: cc10x v2.1
/agents      # Should show: 11 agents
```

---

## First Use - The Killer Feature

```bash
/cc10x review src/your-code.js
```

**What happens:**
- 5 agents analyze in parallel (3-5 minutes)
- Finds security, quality, performance, UX, accessibility issues
- Reports with specific fixes

**Use before EVERY PR!**

---

## The Focus Rule (Why v2.1 Works)

**The Problem (v3.0 had this):**
```
You: "Build todo app"
→ cc10x: *starts security review*
→ cc10x: *analyzes 63 risks*
→ cc10x: *creates deployment strategy*
→ 4 hours later...
→ You: "I JUST WANTED A TODO APP!"
```

**The Fix (v2.1 has this):**
```
You: "Build todo app"
→ cc10x: "Building todo app."
→ 45 minutes: Done! Working app delivered.
→ cc10x: "Want me to review it?" (optional!)
```

**THE FOCUS RULE: Do what user asked. Nothing more.**

---

## Usage Examples

### Just Build Something (Fast)

```bash
/cc10x build user authentication
```

**Asks you:** "Quick build or systematic?"  
**Default:** Quick (delivers in 1-2 hours)  
**Systematic:** Full TDD (if you choose, 3-4 hours)

**YOU control the depth!**

---

### Review Code

```bash
/cc10x review src/auth.js
```

**Does:** Reviews the file  
**Doesn't do:** Everything else (unless you ask)  
**Time:** 3-5 minutes

---

### Fix a Bug

```bash
/cc10x fix login timeout issue
```

**Does:** Fixes the bug using LOG FIRST  
**Doesn't do:** Rewrite your entire auth system  
**Time:** 15-45 minutes

---

### Want Full Systematic? Just Ask!

```bash
/cc10x build authentication with full planning, risk analysis, and deployment strategy
```

**NOW it does the full orchestra** (you explicitly asked for it!)

---

## The 4 Workflows

**1. REVIEW** - Always valuable
- Finds issues fast
- Use liberally

**2. BUILD** - Delivers working code
- Asks: Quick or systematic?
- You choose!

**3. FIX** - LOG FIRST debugging
- Finds root cause
- Implements fix
- Done!

**4. VALIDATE** - Team projects
- Checks consistency
- Optional

---

## Common Questions

**Q: Will it spend 4 hours on security when I just want to build something?**  
A: NO! v2.1 has THE FOCUS RULE. It only does what you ask.

**Q: What if I want comprehensive analysis?**  
A: Just say so! "Build with full systematic approach" → Full orchestra

**Q: What changed from v2.0?**  
A: Added THE FOCUS RULE to prevent losing control

**Q: What happened to v3.0?**  
A: Reverted. It had meta-instructions that caused infinite loops.

---

## Troubleshooting

### Orchestrator not doing what I asked?

Check your request:
- ✅ "Build todo app" → Should build directly
- ✅ "Review security" → Should review security only
- ❌ If it's doing extra stuff → Report as bug!

THE FOCUS RULE should prevent this.

---

### Want systematic but getting quick mode?

Be explicit:
```bash
/cc10x build auth with comprehensive planning and risk analysis
```

Explicit request triggers systematic mode.

---

## What Makes v2.1 Different

**vs v2.0:**
- ✅ Added THE FOCUS RULE (prevents endless orchestration)
- ✅ Added PostToolUse hook (<500 line enforcement)
- ✅ Added helper skills (task-breakdown, progress-tracker)

**vs v3.0 (reverted):**
- ✅ Has actual execution logic (not meta-instructions)
- ✅ Doesn't cause infinite loops
- ✅ User controls flow
- ✅ Delivers results fast

---

**cc10x v2.1: Orchestration that works. Focus that delivers.**

**Try it:** `/cc10x review src/` (always valuable!)
