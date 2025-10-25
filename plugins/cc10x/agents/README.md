# cc10x Sub-Agents - What They Actually Are

## Reality Check

Most "agents" in cc10x are **specialized prompt templates**, not autonomous AI workers.

**Exception:** The 5 review agents ARE autonomous (parallel execution, working AI).

---

## The 11 Agents Explained

### ⭐⭐⭐⭐⭐ The 5 WORKING Agents (Review Only)

**Used exclusively by:** `/review` command

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

### The 4 NEW Planning Agents (v2.0)

**What they actually are:** Specialized prompt templates that commands invoke sequentially

**How they "work":**
- Command invokes agent explicitly
- Agent provides structured instructions to Claude
- Claude follows instructions (not separate AI)
- Agent returns formatted output

**The agents:**

6. **architect.md** - Architecture, complexity, manifests, risk assessment
   - **What it is:** Prompt template for architecture decisions
   - **What it does:** Loads feature-planning skill progressively, applies patterns
   - **Invoked by:** /feature-plan (Phases 3, 3a, 3b, 3c, 5b)
   - **Output:** Architecture decisions, complexity score, file manifest

7. **devops-planner.md** - Rollback strategies, deployment plans
   - **What it is:** Prompt template for deployment planning
   - **What it does:** Loads deployment-patterns skill, creates procedures
   - **Invoked by:** /feature-plan (Phases 6, 7)
   - **Output:** Rollback strategy, deployment plan

8. **requirements-analyst.md** - Requirements gathering, user stories
   - **What it is:** Prompt template for requirements extraction
   - **What it does:** Loads feature-planning Stage 1, structures requirements
   - **Invoked by:** /feature-plan (Phase 1)
   - **Output:** Requirements document, user stories

9. **tdd-enforcer.md** - Strict TDD enforcement, mandatory verification
   - **What it is:** Prompt template for TDD methodology
   - **What it does:** Loads test-driven-development skill, enforces RED-GREEN-REFACTOR
   - **Invoked by:** /feature-build (Phase 3)
   - **Output:** Implemented code with verified passing tests

**Why they're NOT "real" agents:**
- Not autonomous (require command to invoke)
- Not parallel (run sequentially)
- Claude follows their instructions (not separate AI instances)
- More like "structured prompts" than "AI workers"

**Why they're still valuable:**
- Provide systematic frameworks
- Load skills progressively (token-efficient)
- Enforce quality gates
- Prevent common mistakes

---

### The 2 Implementation Agents

10. **context-analyzer.md** - Codebase pattern discovery
    - **What it is:** Hybrid (can be autonomous or invoked)
    - **What it does:** Searches codebase for similar features, extracts conventions
    - **Invoked by:** /feature-plan (Phase 2), /feature-build (Phase 1)
    - **Status:** Enhanced in v2.0 with progressive skill loading

11. **implementer.md** - Feature implementation with TDD
    - **What it is:** Implementation executor
    - **What it does:** Follows TDD cycle, implements increments, verifies tests
    - **Invoked by:** /feature-build (Phase 3)
    - **⚠️ Warning:** Can report false success - MUST verify tests manually!
    - **Status:** Enhanced in v2.0 with File Manifest verification, mandatory test verification

---

## The Truth About "Autonomous Agents"

### What We Claimed (v1.x)

"cc10x uses autonomous sub-agents that work independently to implement features"

### What Actually Happens

**For /review:** ✅ TRUE
- 5 agents launch in parallel
- Each is a separate AI instance
- Work independently and return results

**For other commands:** ❌ MISLEADING
- "Agents" are prompt templates
- Commands invoke them sequentially
- Claude (same instance) follows their instructions
- Not separate AI workers

### More Accurate Description

**They are:**
- Specialized instruction sets
- Domain-specific checklists
- Workflow guides
- Progressive skill loaders

**They are NOT:**
- Autonomous AI workers (except review agents)
- Self-executing programs
- Independent decision-makers
- Truly parallel (except review)

---

## How to Think About Agents

### The 5 Review Agents (REAL AI Agents)

**Analogy:** Hiring 5 expert consultants who analyze your code simultaneously

- Security consultant finds vulnerabilities
- Quality consultant finds code smells
- Performance consultant finds bottlenecks
- UX consultant finds usability issues
- Accessibility consultant finds WCAG violations

**They work independently in parallel.** This is TRUE agent behavior.

---

### The 6 Other Agents (Specialized Prompts)

**Analogy:** Following detailed checklists from domain experts

- Architect checklist for design decisions
- DevOps checklist for deployment planning
- Requirements checklist for gathering needs
- TDD checklist for test-first development
- Context checklist for pattern discovery
- Implementation checklist for coding

**You follow the checklist.** They provide structure, not autonomy.

---

## Why This Architecture?

### Benefits

**Separation of Concerns:**
- Commands = orchestration logic (what to do when)
- Agents = execution templates (how to do it)
- Skills = knowledge bases (what patterns/frameworks to apply)

**Progressive Loading:**
- Commands don't embed everything (thin)
- Agents load only needed skill stages (efficient)
- Skills provide rich content on-demand (comprehensive)

**Maintainability:**
- Update skill content without touching commands
- Add new agents without changing commands
- Extend commands without bloating files

**Token Efficiency:**
- v1.x: 15k tokens upfront
- v2.0: 3.2k-5.2k tokens progressive
- Real 65-79% savings (vs v1.x embedded approach)

### Tradeoffs

**Costs:**
- Still 3-20x MORE than pure manual (structure has overhead)
- Complexity (3 layers to understand)
- Requires discipline (follow the process)

**When Worth It:**
- Complex features (4-5 complexity)
- High-risk changes (prevents disasters)
- Team collaboration (documentation valuable)

**When NOT Worth It:**
- Simple features (1-2 complexity)
- Time-sensitive (manual faster)
- Solo dev (don't need docs)

---

## Agent Development Guidelines

### Creating New Agents

**Template:**
```markdown
---
name: agent-name
description: What this agent does and when to use it
model: sonnet
---

# Agent Name

You are a [role] specialist.

## Your Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]

## Progressive Skill Loading Strategy

### For [Task Name]
1. Invoke Skill: `skill-name` Stage X
2. Load: ~X tokens
3. Apply: [what to do with skill content]
4. Output: [what to produce]

## Workflow
[Step-by-step instructions]

## Quality Standards
[What constitutes good output]

## Remember
[Key principles]
```

### When to Create an Agent vs Update Existing

**Create NEW agent when:**
- Truly distinct responsibility (not covered by existing)
- Reusable across multiple commands
- Loads different skills than existing agents

**Update EXISTING agent when:**
- Enhancing existing capability
- Adding new skill loading
- Improving quality standards

---

## Bottom Line

**5 agents are real AI workers** (/review agents) ⭐⭐⭐⭐⭐

**6 agents are structured prompts** (you do the work, they guide)

**All 11 provide value** through systematic frameworks, but only 5 are truly autonomous.

**Use `/review` liberally (it works!). Use others for complexity 4-5 only.**

