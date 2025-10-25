# cc10x Plugin - Technical Architecture

**Version:** 2.0.0 | **Type:** Claude Code Plugin | **Status:** Production

---

## Architecture Overview

cc10x implements a 3-layer architecture for systematic development workflows:

```
LAYER 1: COMMANDS (5 files, 150-300 lines each)
├── feature-plan.md        Orchestrates 7-phase planning
├── feature-build.md       Orchestrates 5-phase TDD implementation
├── bug-fix.md             Orchestrates LOG FIRST debugging
├── review.md              Orchestrates 5-agent parallel review ⭐⭐⭐⭐⭐
└── validate.md            Orchestrates 5-dimension validation

LAYER 2: SUB-AGENTS (11 files, 300-900 lines each)
├── Working Agents (Review)
│   ├── security-reviewer.md        ⭐⭐⭐⭐⭐
│   ├── quality-reviewer.md         ⭐⭐⭐⭐⭐
│   ├── performance-analyzer.md     ⭐⭐⭐⭐⭐
│   ├── ux-reviewer.md              ⭐⭐⭐⭐⭐
│   └── accessibility-reviewer.md   ⭐⭐⭐⭐⭐
├── Planning Agents (v2.0 NEW)
│   ├── architect.md                Complexity, manifests, architecture
│   ├── devops-planner.md           Rollback, deployment
│   ├── requirements-analyst.md     Requirements, user stories
│   └── tdd-enforcer.md             TDD enforcement, verification
└── Implementation Agents
    ├── context-analyzer.md         Pattern discovery
    └── implementer.md              Feature implementation

LAYER 3: SKILLS (17 directories, 500-2000 lines each)
├── NEW in v2.0
│   ├── risk-analysis/              "What Could Go Wrong?" 7 dimensions
│   └── deployment-patterns/        Rollback & deployment strategies
├── Enhanced in v2.0
│   ├── feature-planning/           Added 5 progressive stages
│   └── test-driven-development/    Added verification stage
└── Existing (13 skills)
    ├── accessibility-patterns/
    ├── bug-fixing/
    ├── code-generation/
    ├── code-review-patterns/
    ├── code-reviewing/
    ├── codebase-navigation/
    ├── feature-building/
    ├── performance-patterns/
    ├── safe-refactoring/
    ├── security-patterns/
    ├── systematic-debugging/
    ├── ui-design/
    └── ux-patterns/
```

---

## How Commands Orchestrate Agents

### Example: /feature-plan

**Command file:** 250 lines (thin orchestrator)

**Execution flow:**
```
User: /feature-plan Add authentication

Command (200 tokens):
  ↓ Phase 1
requirements-analyst agent:
  → Loads feature-planning Skill Stage 1 (500 tokens)
  → Returns: Requirements document
  
  ↓ Phase 2  
context-analyzer agent:
  → Loads codebase-navigation Skill (1,100 tokens)
  → Returns: Context report
  
  ↓ Phase 3
architect agent:
  → Loads feature-planning Skill Stage 2 (800 tokens)
  → Returns: Architecture decisions
  
  ↓ Phase 3a (NEW!)
architect agent (same):
  → Loads risk-analysis Stages 1+5 (1,400 tokens)
  → Returns: Critical risks
  
  ↓ Phase 3b
architect agent:
  → Loads feature-planning Skill Stage 3 (400 tokens)
  → Returns: Risk matrix
  
  ↓ Phase 3c (NEW! - Complexity)
architect agent:
  → Loads feature-planning Skill Stage 4 (600 tokens)
  → Returns: Complexity score + recommendation
  → If complexity < 3: RECOMMENDS SKIP!
  
  ↓ If complexity >= 4 or user proceeds...
  
  ↓ Phases 4-7
architect + devops-planner:
  → Load testing, roadmap, manifest, rollback, deployment
  → Additional 2,400 tokens

Total tokens:
- Simple (stops at Phase 3c): 3,200 tokens (79% vs v1.x 15k)
- Complex (all phases): 5,200 tokens (65% vs v1.x 15k)

Output: Comprehensive 15-section plan in .claude/plans/
```

---

## Progressive Loading Explained

### What It Actually Means

**Traditional approach (v1.x):**
```
Command loads ALL instructions upfront: 15,000 tokens
  ↓
Claude reads everything (most not relevant)
  ↓
Executes relevant parts
  ↓
Wasted: ~10,000 tokens of unused instructions
```

**Progressive approach (v2.0):**
```
Command loads orchestration logic: 200 tokens
  ↓
Agent 1 loads ONLY Skill Stage 1: 500 tokens
  ↓
Agent 2 loads ONLY Skill Stages 1-2: 1,100 tokens
  ↓
Agent 3 loads ONLY Skill Stage 2: 800 tokens
  ↓
... (continues for each phase)
  ↓
Total: ~5,200 tokens (only what's actually needed)

Savings: 65% (15k → 5.2k)
```

**If feature is simple (complexity 2):**
```
Stops after Complexity Assessment (Phase 3c):
  ↓
Only loads: 200 + 500 + 1,100 + 1,400 = 3,200 tokens
  ↓
Savings: 79% (15k → 3.2k)
```

**This is REAL progressive loading.** v1.x claimed it but didn't implement it.

---

## Token Economics Reality

### Comparison to Manual Implementation

| Feature Type | cc10x Tokens | Manual Tokens | Multiplier |
|--------------|--------------|---------------|------------|
| TRIVIAL (1) | 40k | 2k | **20x MORE** ❌ |
| SIMPLE (2) | 80k | 5k | **16x MORE** ❌ |
| MODERATE (3) | 100k | 15k | **7x MORE** ⚠️ |
| COMPLEX (4) | 120k | 30k | **4x MORE** ✅ |
| VERY COMPLEX (5) | 180k | 50k | **4x MORE** ✅ |

**Exception:** `/review` - Always worth it (prevents security breaches)

### Why MORE Expensive?

1. **Systematic Analysis** - Multiple phases, comprehensive checks
2. **Risk Analysis** - "What Could Go Wrong?" adds thoroughness
3. **Documentation** - Generates plans, manifests, rollback procedures
4. **Quality Gates** - Verification at each phase
5. **Parallel Reviews** - 5 agents analyzing simultaneously

**Is it worth it?**
- Complexity 1-2: ❌ NO (absurdly expensive)
- Complexity 3: ⚠️ MAYBE (if team docs valued)
- Complexity 4-5: ✅ YES (prevents costly mistakes)

---

## Skill Progressive Loading Details

### Example: feature-planning Skill

**Structure:**
```markdown
Stage 1: Requirements (~500 tokens)
  - User story patterns
  - Acceptance criteria templates
  
Stage 2: Architecture (~800 tokens)
  - ADR templates
  - Technology comparison frameworks
  
Stage 3: Risk Assessment (~400 tokens)
  - Probability × Impact scoring
  - Mitigation strategy templates
  
Stage 4: Complexity (~600 tokens)
  - 1-5 scoring rubric
  - cc10x value analysis
  
Stage 5: File Manifest (~500 tokens)
  - CREATE/MODIFY/DELETE templates
  - Integration point mapping

Total if ALL stages loaded: ~2,800 tokens
Typical usage (Stages 1-4): ~2,300 tokens
```

**Agents load only what they need:**
- requirements-analyst: Stage 1 only (500 tokens)
- architect Phase 3: Stage 2 only (800 tokens)
- architect Phase 3b: Stage 3 only (400 tokens)
- architect Phase 3c: Stage 4 only (600 tokens)

**Result:** Never loads all 2,800 tokens at once

---

## "What Could Go Wrong?" Integration

### risk-analysis Skill Structure

**7 Progressive Stages:**
```markdown
Stage 1: Data Flow (~600 tokens)
Stage 2: Dependencies (~500 tokens)
Stage 3: Timing & Concurrency (~700 tokens)
Stage 4: UX & Accessibility (~600 tokens)
Stage 5: Security (~800 tokens)
Stage 6: Performance (~600 tokens)
Stage 7: Failure Modes (~700 tokens)

Total if ALL loaded: ~4,500 tokens
```

**Who invokes which stages:**

| Agent | Stages | Tokens | When |
|-------|--------|--------|------|
| architect | 1+5 | 1,400 | Planning (data + security) |
| implementer | 1+3+7 | 2,000 | Before each increment |
| quality-reviewer | ALL 7 | 4,500 | Comprehensive review |
| security-reviewer | 1+2+5 | 1,900 | Security-focused |
| devops-planner | 7 | 700 | Failure mode planning |

**Result:** Different agents load different stages (token-efficient!)

---

## File Structure

```
plugins/cc10x/
├── .claude-plugin/
│   └── plugin.json                 Plugin metadata
├── commands/                        5 thin orchestrators
│   ├── bug-fix.md                  180 lines
│   ├── feature-build.md            280 lines
│   ├── feature-plan.md             250 lines
│   ├── review.md                   Minor updates (5⭐)
│   └── validate.md                 280 lines
├── agents/                          11 specialized agents
│   ├── accessibility-reviewer.md   Review agent (5⭐)
│   ├── architect.md                NEW! Planning agent
│   ├── context-analyzer.md         Enhanced v2.0
│   ├── devops-planner.md           NEW! Deployment agent
│   ├── implementer.md              Enhanced v2.0
│   ├── performance-analyzer.md     Review agent (5⭐)
│   ├── quality-reviewer.md         Review agent (5⭐)
│   ├── requirements-analyst.md     NEW! Requirements agent
│   ├── security-reviewer.md        Review agent (5⭐)
│   ├── tdd-enforcer.md             NEW! TDD agent
│   └── ux-reviewer.md              Review agent (5⭐)
├── skills/                          17 knowledge bases
│   ├── accessibility-patterns/
│   ├── bug-fixing/
│   ├── code-generation/
│   ├── code-review-patterns/
│   ├── code-reviewing/
│   ├── codebase-navigation/
│   ├── deployment-patterns/        NEW! v2.0
│   ├── feature-building/
│   ├── feature-planning/           Enhanced v2.0 (5 stages)
│   ├── performance-patterns/
│   ├── risk-analysis/              NEW! v2.0 (7 stages)
│   ├── safe-refactoring/
│   ├── security-patterns/
│   ├── systematic-debugging/
│   ├── test-driven-development/    Enhanced v2.0 (3 stages)
│   ├── ui-design/
│   ├── ux-patterns/
│   └── verification-before-completion/
├── hooks/
│   ├── hooks.json                   Lifecycle hooks
│   ├── pre-compact.sh               Auto-healing context
│   └── session-start.sh             Session initialization
├── CLAUDE.md                        User guide
└── README.md                        This file
```

---

## Development Principles

### 1. Honest Positioning

**v1.x made false claims:**
- "93% token savings" (was actually using MORE)
- "Auto-triggering skills" (never worked)
- "10x faster" (not true)

**v2.0 is brutally honest:**
- "3-20x MORE tokens" (structure has a cost)
- "Explicitly invokes" (no auto-triggering)
- "More systematic" (not faster)
- "Use for complexity 4-5 only"

### 2. Verify Everything

**v1.x trusted agent reports:**
- Agent: "✅ All 33 tests passing!"
- Reality: 3/7 tests FAILED

**v2.0 requires verification:**
- Run actual test command
- See results with YOUR eyes
- Never trust reports

### 3. Know When to Skip

**v2.0 recommends NOT using cc10x for:**
- Simple features (complexity 1-2)
- Well-documented libraries
- Time-sensitive tasks
- Token-budget-constrained scenarios

**No shame in manual implementation!**

---

## Technical Details

### Agent Invocation

Commands use explicit agent invocation (not relying on auto-triggering):

```markdown
Example in feature-plan.md:

### Phase 1: Requirements Analysis

**Invoke:** `requirements-analyst` sub-agent

Agent will:
1. Load feature-planning Skill Stage 1
2. Parse requirements
3. Return document
```

Claude Code executes this by launching the agent with the specified configuration.

### Skill Loading

Agents use explicit skill loading with stage parameters:

```markdown
Example in architect agent:

Invoke Skill: "cc10x:feature-planning"
Stage: "Stage 4: Complexity Assessment"
Loads: ~600 tokens (only that stage)
```

This enables true progressive loading (load only what's needed).

### Parallel Execution

**Only /review uses parallel execution:**
```
review command
  ↓ Launches 5 agents simultaneously
  ├── security-reviewer
  ├── quality-reviewer
  ├── performance-analyzer
  ├── ux-reviewer
  └── accessibility-reviewer
  ↓ All run in parallel (safe because read-only)
  ↓ Results assembled
  → Comprehensive review in 2-3 minutes
```

**All other commands use sequential execution** (prevents file conflicts)

---

## Version History

### v2.0.0 (2025-10-24) - 3-Layer Architecture

**Breaking Changes:**
- Commands no longer embed instructions (now thin orchestrators)
- Skills require explicit invocation (don't auto-trigger)
- Token economics completely changed (now 3-20x MORE, not savings)

**New Features:**
- 4 NEW sub-agents (architect, devops-planner, requirements-analyst, tdd-enforcer)
- 2 NEW skills (risk-analysis, deployment-patterns)
- "What Could Go Wrong?" 7-dimension methodology
- Complexity Assessment (recommends skip if simple)
- File Change Manifests (prevents scope creep)
- Rollback Strategies (< 5 min recovery)
- Deployment Plans (staged rollout)
- Mandatory test verification (prevents false success)

**Enhancements:**
- feature-planning skill: Added 5 progressive stages
- test-driven-development skill: Added verification stage
- All agents: Progressive skill loading
- /review: Emphasized as 5⭐ killer feature

**Honest Positioning:**
- Removed ALL false claims
- Added "When NOT to Use" to all commands
- Token economics brutally honest
- Real progressive loading implemented

See [CHANGELOG.md](../../CHANGELOG.md) for complete history.

### v1.1.0 (2025-10-22) - Marketplace Transformation

Restructured as marketplace with cc10x plugin.

### v1.0.0 (2025-10-21) - Initial Release

First public release with commands, agents, skills.

---

## Testing & Validation

### Brutal Testing Results (Real-World Usage)

**Test 1: Rate Limiting (Complexity 2)**
- Result: ❌ cc10x WORSE than manual
- cc10x: 100k tokens, false success, tests failed
- Manual: 5k tokens, 30 min, working code
- Lesson: Don't use for simple features!

**Test 2: /review Command**
- Result: ⭐⭐⭐⭐⭐ EXCELLENT
- Found: 38 issues (5 CRITICAL security issues)
- Time: 3 minutes
- Verdict: Worth every token!

**Test 3: Autonomous Development (No cc10x)**
- Task: Build landing page
- Result: Base Claude built it in 10 min, 15k tokens, professional quality
- Lesson: cc10x is NOT required for straightforward tasks!

**Test 4: /bug-fix with LOG FIRST**
- Result: ⭐⭐☆☆☆ Pattern works, but not always faster
- Saved: 2 hours vs random guessing
- Cost: 20k tokens
- Verdict: Good for complex bugs only

### What We Learned

1. **Only /review truly works** (5⭐, use liberally)
2. **Other commands are checklists** (systematic, not autonomous)
3. **Skills don't auto-trigger** (must be explicitly invoked)
4. **Agents can report false success** (must verify independently)
5. **cc10x is overkill for simple features** (manual is better)
6. **cc10x shines for complexity 4-5** (prevents costly mistakes)

---

## Contributing

### Found an Issue?

Check if it's one of these known patterns:
- Agent reported success but tests failed → Use mandatory verification
- Skills didn't trigger → They don't auto-trigger (working as designed)
- Used too many tokens → Check if feature is complexity <3 (shouldn't use cc10x)

If it's a real bug, file an issue with:
1. Command used
2. Feature complexity
3. Expected vs actual behavior
4. Token usage

### Suggesting Enhancements?

We're especially interested in:
- Better complexity assessment heuristics
- Additional risk analysis dimensions
- Improved verification procedures
- Real-world test case studies

---

## License

MIT - See LICENSE file

---

## Credits

**Created by:** Rom Iluz (@romiluz13)

**Inspired by:**
- GitHub Spec Kit (Spec-Driven Development)
- BMAD Method (AI-Driven Agile Development)
- Cursor IDE (Complexity Assessment, File Manifests, Rollback Plans)

**Special thanks to:**
- Brutal real-world testing that revealed false claims
- Claude Code for the plugin framework
- The Claude AI community

---

## Support

- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Discussions:** https://github.com/romiluz13/cc10x/discussions
- **Documentation:** Full docs in [CLAUDE.md](CLAUDE.md)

---

**Remember:** cc10x is a tool, not magic. Use `/review` liberally, use systematic workflows for complex features, go manual for simple features.

**Know when to use the right tool for the job.**
