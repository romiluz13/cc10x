# cc10x v3 Agents: The 4+5 Architecture

## Reality Check

Most "agents" in cc10x are **specialized prompt templates**, not autonomous AI workers.

**Exception:** The 5 review agents ARE autonomous (parallel execution, working AI).

---

## The v3 Architecture: 9 Agents Total (4+5)

### ⭐⭐⭐⭐⭐ The 5 Review Agents (Parallel Execution - KEPT from v2)

**Used exclusively by:** REVIEW workflow

**How they work:**
- Launch in parallel (5 agents simultaneously)
- Each has isolated context and specialized instructions
- Analyze code from their specific dimension
- Return detailed findings independently
- Results assembled into comprehensive review

**The agents:**

1. **security-reviewer.md** - Security vulnerability analysis
   - Finds: SQL injection, XSS, auth bypasses, data exposure
   - Uses: risk-analysis Stages 1+2+5 + security-patterns skill
   - Real test: Found 5 CRITICAL security issues

2. **quality-reviewer.md** - Code quality and maintainability
   - Finds: Code smells, duplication, complexity, refactoring opportunities
   - Uses: risk-analysis ALL 7 stages + code-review-patterns skill
   - Real test: Found 12 HIGH quality issues

3. **performance-analyzer.md** - Performance bottlenecks
   - Finds: O(n²) loops, memory leaks, N+1 queries, caching opportunities
   - Uses: risk-analysis Stages 3+6 + performance-patterns skill
   - Real test: Found 8 performance issues

4. **ux-reviewer.md** - User experience issues
   - Finds: Error message problems, loading states, UX friction
   - Uses: risk-analysis Stage 4 + ux-patterns skill
   - Real test: Found 7 UX improvements

5. **accessibility-reviewer.md** - WCAG compliance
   - Finds: Keyboard navigation issues, ARIA problems, color contrast
   - Uses: risk-analysis Stage 4 + accessibility-patterns skill
   - Real test: Found 6 accessibility violations

**Why these work:**
- True parallel execution (5 separate AI instances)
- Isolated contexts (can't interfere with each other)
- Read-only operations (safe to parallelize)
- Well-defined outputs (structured findings)

**Verified:** ⭐⭐⭐⭐⭐ (5/5 stars) in brutal real-world testing

---

### The 4 Core Execution Agents (Sequential - NEW in v3)

**What they actually are:** Specialized prompt templates with complexity-aware scaling

**How they work:**
- Orchestrator invokes agents sequentially
- Each agent provides structured instructions
- Agents scale output based on complexity (1-5)
- Progressive skill loading for token efficiency

**The agents:**

6. **feature-planner.md** (NEW in v3)
   - **Replaces:** requirements-analyst
   - **From:** cc10x_V2-main pattern
   - **Role:** Product manager creating comprehensive PRDs
   - **Enhancements:** Risk-aware planning, assumption validation
   - **Complexity scaling:** 
     - Simple (1-2): 200-line PRD, 3-5 user stories
     - Complex (4-5): 1,000+ line PRD, 20+ user stories
   - **Invoked by:** PLANNING workflow (Phase 1)

7. **architect.md** (Enhanced in v3)
   - **Enhancements:** Technology decision framework, file size enforcement
   - **From:** cc10x_V2-main patterns merged with existing
   - **Role:** System design, technology decisions, complexity assessment, file manifests
   - **Complexity scaling:**
     - Simple (1-2): 150 lines, basic diagrams, 2-3 components
     - Complex (4-5): 1,000+ lines, comprehensive diagrams, 10+ components
   - **Invoked by:** PLANNING workflow (Phases 3, 3a, 3b, 3c, 5b)

8. **code-writer.md** (NEW in v3)
   - **Merges:** implementer + tdd-enforcer logic
   - **From:** cc10x_V2-main with TDD integration
   - **Role:** TDD implementation with strict quality enforcement
   - **Enforces:** <500 lines per file, no placeholders, production-ready only
   - **Features:** Risk analysis before each increment, RED-GREEN-REFACTOR cycles
   - **Complexity scaling:**
     - Simple (1-2): 2-3 files, 50-150 lines total
     - Complex (4-5): 10-20 files, 1,000+ lines
   - **Invoked by:** BUILDING workflow (Phase 2-4)

9. **test-generator.md** (NEW in v3)
   - **From:** cc10x_V2-main with verification requirements
   - **Role:** Comprehensive test creation with mandatory user verification
   - **Enforces:** >80% coverage, user must manually verify tests pass
   - **Features:** Prevents false success reports
   - **Complexity scaling:**
     - Simple (1-2): 10-20 tests, basic coverage
     - Complex (4-5): 80-200 tests, unit + integration + e2e
   - **Invoked by:** BUILDING workflow (Phase 5)

---

## What Changed in v3?

### Consolidated from 11 → 9 Agents

**DELETED (merged into new agents):**
- `requirements-analyst.md` → Merged into `feature-planner`
- `implementer.md` → Merged into `code-writer`
- `tdd-enforcer.md` → Merged into `code-writer`
- `devops-planner.md` → Logic moved to `deployment-patterns` skill
- `context-analyzer.md` → Logic moved to `codebase-navigation` skill

**Why consolidate?**
- **Simpler:** 4 clear roles vs 6 overlapping ones
- **Clearer:** Each agent has distinct purpose
- **Inspired by:** cc10x_V2-main's focused 4-agent model
- **Better:** Less confusion about who does what

### Review Agents Unchanged

**Why keep review agents separate?**
- They actually work as advertised (5-star performance)
- Parallel execution proven effective
- Found 38 real issues in testing
- No changes needed - already excellent

---

## The 4+5 Workflow

### PLANNING Workflow (Phases 1-7)
1. **feature-planner** → Creates PRD with assumptions, user stories, requirements
2. **architect** (Phase 3) → Designs architecture with technology decisions
3. **architect** (Phase 3a) → Critical risk analysis (data flow + security)
4. **architect** (Phase 3b) → Comprehensive risk assessment
5. **architect** (Phase 3c) → Complexity assessment (recommends skip if 1-2)
6. **architect** (Phase 5b) → File change manifest
7. **architect** (Phases 6-7) → Rollback + deployment strategies (using deployment-patterns skill)

### BUILDING Workflow (Phases 1-6)
1. **Context analysis** (using codebase-navigation skill)
2. **Task breakdown** (using task-breakdown skill)
3. **code-writer** → TDD implementation (RED-GREEN-REFACTOR with risk analysis)
4. **code-writer** → File manifest verification
5. **test-generator** → Comprehensive test creation
6. **User verification** → MANDATORY manual test verification

### REVIEW Workflow (Parallel Execution)
- **All 5 review agents in parallel** → Comprehensive multi-dimensional analysis
- **Assembly** → Findings compiled into structured report

---

## Which Agents Are "Real"?

### The 5 Review Agents: TRUE Autonomous AI Agents ⭐⭐⭐⭐⭐

**They are:**
- ✅ Separate AI instances running in parallel
- ✅ Independent contexts (no interference)
- ✅ Autonomous analysis (you don't do their work)
- ✅ Real bug-finding capability (38 issues found)

**Analogy:** Hiring 5 expert consultants who analyze your code simultaneously

### The 4 Execution Agents: Structured Workflow Templates ⭐⭐⭐☆☆

**They are:**
- ⚠️ Sequential prompt templates (not parallel)
- ⚠️ You follow their instructions (not autonomous)
- ✅ Provide systematic frameworks (valuable!)
- ✅ Scale to complexity (efficient!)

**Analogy:** Following detailed checklists from domain experts

**Still valuable because:**
- Provide structure and completeness
- Prevent common mistakes
- Scale naturally to complexity
- Load skills progressively

---

## Complexity-Aware Scaling

All 4 core agents automatically scale output based on complexity:

| Complexity | feature-planner | architect | code-writer | test-generator |
|------------|----------------|-----------|-------------|----------------|
| Simple (1-2) | 200 lines, 3-5 stories | 150 lines, basic | 2-3 files, 50-150 LOC | 10-20 tests |
| Moderate (3) | 500 lines, 8-12 stories | 400 lines, detailed | 5-8 files, 300-600 LOC | 30-50 tests |
| Complex (4-5) | 1,000+ lines, 20+ stories | 1,000+ lines, comprehensive | 10-20 files, 1,000+ LOC | 80-200 tests |

**Same systematic process, different depth.**

This replaces v2's separate simple/complex workflows with one adaptive workflow.

---

## Token Efficiency: Progressive Loading

**How it works:**
- Commands are thin (100-200 tokens)
- Agents load skills on-demand (500-2,000 tokens per stage)
- Only load what's needed for current phase

**Example (PLANNING workflow):**
```
Orchestrator: 100 tokens
↓
feature-planner: +500 tokens (planning skill Stage 1)
↓
architect: +800 tokens (planning skill Stage 2 - architecture)
↓
architect: +1,400 tokens (risk-analysis Stages 1+5)
↓
architect: +600 tokens (planning skill Stage 4 - complexity)
↓
If complexity >= 4, continue:
  architect: +500 tokens (planning skill Stage 5 - manifest)
  architect: +1,100 tokens (deployment-patterns Stages 1-2)
  
Total: 5,000 tokens (complex) or 3,400 tokens (stops early if simple)

vs v1.x: 15,000 tokens upfront (65-79% savings!)
```

---

## The Truth About "Autonomous Agents"

### What We Claimed (v1.x-v2.0)

"cc10x uses autonomous sub-agents that work independently"

### What Actually Happens in v3

**For REVIEW workflow:** ✅ TRUE
- 5 agents launch in parallel
- Each is a separate AI instance
- Work independently and return results
- **Truly autonomous**

**For PLANNING/BUILDING workflows:** ⚠️ PARTIALLY TRUE
- Agents are prompt templates
- Orchestrator invokes them sequentially
- Claude (same instance) follows their instructions
- **Structured prompts, not autonomous workers**

**But still valuable:**
- Systematic frameworks prevent mistakes
- Complexity-aware scaling (no overkill)
- Progressive skill loading (token-efficient)
- Proven patterns from cc10x_V2-main

---

## When to Use Each Workflow

### REVIEW Workflow: Use Liberally ⭐⭐⭐⭐⭐

**When:** Before EVERY PR, any complexity
**Why:** Finds real bugs, prevents disasters
**Cost:** 20k-50k tokens
**ROI:** One prevented security breach = infinite value

### PLANNING Workflow: Use for Complexity 4-5 ⭐⭐⭐☆☆

**When:** Complex features (500+ lines, 7+ files, novel patterns)
**Why:** Prevents architecture mistakes, systematic approach
**Cost:** 30k-60k tokens (vs 15k manual)
**ROI:** Worth it for complex features (prevents costly rework)

**Skip for:** Simple features (1-2 complexity) - just use library docs

### BUILDING Workflow: Use with Caution ⭐⭐☆☆☆

**When:** Want strict TDD enforcement, mandatory verification
**Why:** Systematic implementation, prevents edge cases
**Cost:** 40k-80k tokens (vs 20k manual)
**Warning:** MUST verify tests manually (can report false success)

**Skip for:** Time-sensitive, simple implementations

---

## Agent Development Guidelines

### Creating New Agents

**Template:**
```markdown
---
name: agent-name
description: What this agent does, when to use it, what it enforces
tools: Read, Write, Grep, Glob
model: sonnet
---

# Agent Name

Expert in [domain] with [special capabilities].

## Complexity-Aware Output Scaling

- Simple (1-2): [minimal output]
- Moderate (3): [detailed output]
- Complex (4-5): [comprehensive output]

## Your Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]

## Workflow
[Step-by-step instructions]

## Quality Standards
[What constitutes good output]

## Remember
[Key principles]
```

### When to Create vs Merge

**Create NEW agent when:**
- Truly distinct responsibility (not covered by existing 9)
- Reusable across multiple workflows
- Clear separation from existing agents

**Merge into EXISTING agent when:**
- Overlapping responsibilities
- Always used together
- Simpler to have one comprehensive agent

**v3 philosophy:** Fewer, more comprehensive agents > Many overlapping agents

---

## Bottom Line

**5 review agents are real AI workers** ⭐⭐⭐⭐⭐
- Use before EVERY PR
- Truly autonomous, parallel execution
- Find real bugs

**4 execution agents are workflow guides** ⭐⭐⭐☆☆
- Use for complexity 4-5
- Systematic frameworks
- Complexity-aware scaling
- You still do the work

**The 4+5 architecture is simpler, clearer, and inspired by proven patterns from cc10x_V2-main.**

**Use `/review` liberally. Use PLANNING/BUILDING for complexity 4-5 only.**
