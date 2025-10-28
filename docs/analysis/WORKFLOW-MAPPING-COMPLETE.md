# COMPLETE WORKFLOW MAPPING - Which Skills & Subagents for Each Workflow

**Visual guide showing exactly what gets activated in each workflow**

---

## 🔄 WORKFLOW 1: REVIEW (Coordinated Code Review)

**Trigger**: "review", "audit", "check security", "analyze code"  
**Pattern**: Shared Context (coordination needed)  
**Complexity**: Always worth it (prevents security breaches)

### Architecture Flow

```
User: "Review this authentication code for security"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: REVIEW workflow                              │
│ - Complexity: N/A (always worth it)                     │
│ - Routes to: review-workflow                            │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (review-workflow skill)                        │
│ - Loads skills progressively                            │
│ - Analyzes in shared context                            │
│ - Generates coordinated report                          │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (6 skills)                                │
│ ✅ risk-analysis (all 7 stages) - 5,000 tokens          │
│ ✅ security-patterns - 2,000 tokens                     │
│ ✅ performance-patterns - 2,000 tokens                  │
│ ✅ ux-patterns - 2,000 tokens                           │
│ ✅ accessibility-patterns - 2,000 tokens                │
│ ✅ code-quality-patterns - 2,000 tokens                 │
│ Total: 15,000 tokens                                    │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED                                    │
│ ❌ None (analysis, not execution)                       │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ OUTPUT                                                   │
│ - Executive summary                                      │
│ - Security findings (Critical/High/Medium/Low)          │
│ - Quality findings                                       │
│ - Performance findings                                   │
│ - UX findings                                            │
│ - Accessibility findings                                 │
│ - Risk score (1-10)                                     │
│ - Prioritized recommendations                            │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 22,000 tokens  
**Time**: 5 minutes  
**Efficiency**: 27% token savings vs current

---

## 🔄 WORKFLOW 2: PLAN (Feature Planning)

**Trigger**: "plan", "design", "architecture", "PRD"  
**Pattern**: Shared Context (sequential phases)  
**Complexity**: Worth it for 4-5 complexity (complex features)

### Architecture Flow

```
User: "Plan authentication feature with OAuth and 2FA"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: PLAN workflow                                │
│ - Complexity: 5 (auth system, OAuth, 2FA)              │
│ - Routes to: planning-workflow                          │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (planning-workflow skill)                      │
│ - Executes 6 phases sequentially                        │
│ - Each phase builds on previous                         │
│ - Generates comprehensive PRD                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (7 skills)                                │
│ ✅ feature-planning (6 phases) - 3,000 tokens           │
│ ✅ requirements-analysis - 2,000 tokens                 │
│ ✅ architecture-patterns - 3,000 tokens                 │
│ ✅ api-design-patterns - 2,000 tokens                   │
│ ✅ component-design-patterns - 2,000 tokens             │
│ ✅ risk-analysis (7 stages) - 5,000 tokens              │
│ ✅ deployment-patterns - 2,000 tokens                   │
│ Total: 19,000 tokens                                    │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED                                    │
│ ❌ None (analysis, not execution)                       │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ OUTPUT (Comprehensive PRD)                              │
│ Phase 1: Requirements (user stories, acceptance)        │
│ Phase 2: Architecture (components, data models, APIs)   │
│ Phase 3: Components (breakdown, responsibilities)       │
│ Phase 4: Contracts (API endpoints, schemas)             │
│ Phase 5: Edge Cases (7-dimension risk analysis)         │
│ Phase 6: Testing (strategy, coverage, scenarios)        │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 35,000 tokens  
**Time**: 7 minutes  
**Efficiency**: Comprehensive planning prevents rework

---

## 🔄 WORKFLOW 3: BUILD (TDD Implementation)

**Trigger**: "build", "implement", "create", "develop"  
**Pattern**: HYBRID (analysis in shared context, execution via subagents)  
**Complexity**: Worth it for 3+ complexity (multiple components)

### Architecture Flow

```
User: "Build user registration with email verification"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: BUILD workflow                               │
│ - Complexity: 3 (User model, API, Email verification)   │
│ - Routes to: build-workflow                             │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (build-workflow skill)                         │
│ - Analyzes complexity (3 components)                    │
│ - Creates implementation plan                           │
│ - Dispatches subagents for parallel execution           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (4 skills)                                │
│ ✅ test-driven-development - 3,000 tokens               │
│ ✅ code-generation - 2,000 tokens                       │
│ ✅ component-design-patterns - 2,000 tokens             │
│ ✅ integration-patterns - 2,000 tokens                  │
│ Total: 9,000 tokens                                     │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED (3 in PARALLEL)                    │
│                                                          │
│ ✅ component-builder #1: User model                     │
│    Input: Component spec, TDD skill                     │
│    Process: Write tests → Implement → Verify → Commit  │
│    Output: User model + tests                           │
│    Tokens: 10,000                                       │
│                                                          │
│ ✅ component-builder #2: Registration API               │
│    Input: Component spec, TDD skill                     │
│    Process: Write tests → Implement → Verify → Commit  │
│    Output: Registration API + tests                     │
│    Tokens: 10,000                                       │
│                                                          │
│ ✅ component-builder #3: Email verification             │
│    Input: Component spec, TDD skill                     │
│    Process: Write tests → Implement → Verify → Commit  │
│    Output: Email verification + tests                   │
│    Tokens: 10,000                                       │
│                                                          │
│ Total subagent tokens: 30,000                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ VERIFICATION SUBAGENT                                    │
│ ✅ code-reviewer                                         │
│    Input: All 3 components, integration-patterns        │
│    Process: Review for integration issues               │
│    Output: Review findings                              │
│    Tokens: 8,000                                        │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ INTEGRATION (in shared context)                         │
│ - Wire components together                              │
│ - Add integration tests                                 │
│ - Run full test suite                                   │
│ - Verify all tests pass                                 │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 51,000 tokens (more expensive but FASTER)  
**Time**: 5 minutes (vs 15 minutes sequential) - **3x faster!**  
**Efficiency**: Parallel execution, faster delivery

---

## 🔄 WORKFLOW 4: DEBUG (Bug Investigation)

**Trigger**: "debug", "fix", "not working", "error"  
**Pattern**: HYBRID (related bugs in shared context, independent bugs via subagents)  
**Complexity**: Depends on bug count and independence

### Architecture Flow

```
User: "Debug login issues - password validation, session timeout, email verification all broken"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: DEBUG workflow                               │
│ - Complexity: 3 (multiple independent bugs)             │
│ - Routes to: debug-workflow                             │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (debug-workflow skill)                         │
│ - Analyzes logs                                         │
│ - Identifies 3 independent bugs                         │
│ - Dispatches subagents for parallel investigation       │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (3 skills)                                │
│ ✅ systematic-debugging - 3,000 tokens                  │
│ ✅ log-analysis-patterns - 2,000 tokens                 │
│ ✅ debugging-strategies - 2,000 tokens                  │
│ Total: 7,000 tokens                                     │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED (3 in PARALLEL)                    │
│                                                          │
│ ✅ bug-investigator #1: Password validation             │
│    Input: Bug description, logs, systematic-debugging   │
│    Process: Analyze → Root cause → Fix → Verify        │
│    Output: Fix + root cause analysis                    │
│    Tokens: 12,000                                       │
│                                                          │
│ ✅ bug-investigator #2: Session timeout                 │
│    Input: Bug description, logs, systematic-debugging   │
│    Process: Analyze → Root cause → Fix → Verify        │
│    Output: Fix + root cause analysis                    │
│    Tokens: 12,000                                       │
│                                                          │
│ ✅ bug-investigator #3: Email verification              │
│    Input: Bug description, logs, systematic-debugging   │
│    Process: Analyze → Root cause → Fix → Verify        │
│    Output: Fix + root cause analysis                    │
│    Tokens: 12,000                                       │
│                                                          │
│ Total subagent tokens: 36,000                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ INTEGRATION (in shared context)                         │
│ - Merge all fixes                                       │
│ - Run full test suite                                   │
│ - Verify all bugs fixed                                 │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 45,000 tokens  
**Time**: 5 minutes (vs 15 minutes sequential) - **3x faster!**  
**Efficiency**: Parallel bug fixing, faster resolution

---

## 🔄 WORKFLOW 5: REFACTOR (Code Refactoring) - NEW!

**Trigger**: "refactor", "clean up", "improve code quality"  
**Pattern**: HYBRID (analysis in shared context, execution via subagents)  
**Complexity**: Worth it for 3+ independent refactorings

### Architecture Flow

```
User: "Refactor authentication module - extract methods, replace conditionals, introduce parameter objects"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: REFACTOR workflow                            │
│ - Complexity: 3 (3 independent refactorings)            │
│ - Routes to: refactor-workflow                          │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (refactor-workflow skill)                      │
│ - Analyzes code smells                                  │
│ - Creates refactoring plan                              │
│ - Dispatches subagents for parallel execution           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (4 skills)                                │
│ ✅ refactoring-patterns - 3,000 tokens                  │
│ ✅ code-smells - 2,000 tokens                           │
│ ✅ design-patterns - 2,000 tokens                       │
│ ✅ test-driven-development - 3,000 tokens               │
│ Total: 10,000 tokens                                    │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED (3 in PARALLEL)                    │
│                                                          │
│ ✅ refactor-executor #1: Extract method                 │
│    Input: Refactoring plan, code, TDD skill             │
│    Process: Refactor → Run tests → Verify unchanged    │
│    Output: Refactored code + verification               │
│    Tokens: 10,000                                       │
│                                                          │
│ ✅ refactor-executor #2: Replace conditional            │
│    Input: Refactoring plan, code, TDD skill             │
│    Process: Refactor → Run tests → Verify unchanged    │
│    Output: Refactored code + verification               │
│    Tokens: 10,000                                       │
│                                                          │
│ ✅ refactor-executor #3: Introduce parameter object     │
│    Input: Refactoring plan, code, TDD skill             │
│    Process: Refactor → Run tests → Verify unchanged    │
│    Output: Refactored code + verification               │
│    Tokens: 10,000                                       │
│                                                          │
│ Total subagent tokens: 30,000                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ INTEGRATION (in shared context)                         │
│ - Integrate all refactorings                            │
│ - Run full test suite                                   │
│ - Verify no behavior changes                            │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 43,000 tokens  
**Time**: 5 minutes (vs 15 minutes sequential) - **3x faster!**  
**Efficiency**: Parallel refactoring, behavior preservation

---

## 🔄 WORKFLOW 6: MIGRATE (Migration/Upgrade) - NEW!

**Trigger**: "migrate", "upgrade", "convert"  
**Pattern**: HYBRID (analysis in shared context, execution via subagents)  
**Complexity**: Worth it for multi-phase migrations

### Architecture Flow

```
User: "Migrate from Express to Fastify"
  ↓
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (cc10x-orchestrator skill)                 │
│ - Detects: MIGRATE workflow                             │
│ - Complexity: 4 (multi-phase migration)                 │
│ - Routes to: migrate-workflow                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW (migrate-workflow skill)                       │
│ - Analyzes dependencies                                 │
│ - Creates migration plan (5 phases)                     │
│ - Dispatches subagents for independent phases           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SKILLS LOADED (4 skills)                                │
│ ✅ migration-patterns - 3,000 tokens                    │
│ ✅ dependency-analysis - 2,000 tokens                   │
│ ✅ compatibility-checking - 2,000 tokens                │
│ ✅ deployment-patterns - 2,000 tokens                   │
│ Total: 9,000 tokens                                     │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ SUBAGENTS DISPATCHED (3 in PARALLEL)                    │
│                                                          │
│ ✅ migration-executor #1: Migrate routes                │
│    Input: Migration plan, compatibility-checking        │
│    Process: Migrate → Test → Verify                    │
│    Output: Migrated routes + tests                      │
│    Tokens: 12,000                                       │
│                                                          │
│ ✅ migration-executor #2: Migrate middleware            │
│    Input: Migration plan, compatibility-checking        │
│    Process: Migrate → Test → Verify                    │
│    Output: Migrated middleware + tests                  │
│    Tokens: 12,000                                       │
│                                                          │
│ ✅ migration-executor #3: Migrate error handling        │
│    Input: Migration plan, compatibility-checking        │
│    Process: Migrate → Test → Verify                    │
│    Output: Migrated error handling + tests              │
│    Tokens: 12,000                                       │
│                                                          │
│ Total subagent tokens: 36,000                           │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ INTEGRATION (in shared context)                         │
│ - Integrate all migrations                              │
│ - Run full test suite                                   │
│ - Create deployment plan                                │
│ - Create rollback plan                                  │
└─────────────────────────────────────────────────────────┘
```

**Token Usage**: 50,000 tokens  
**Time**: 6 minutes (vs 18 minutes sequential) - **3x faster!**  
**Efficiency**: Parallel migration, deployment planning

---

## 📊 SUMMARY TABLE

| Workflow | Skills | Subagents | Pattern | Tokens | Time | Speedup |
|----------|--------|-----------|---------|--------|------|---------|
| REVIEW | 6 | 0 | Shared | 22K | 5 min | 27% ↓ tokens |
| PLAN | 7 | 0 | Shared | 35K | 7 min | Same |
| BUILD | 4 | 3-4 | Hybrid | 51K | 5 min | **3x faster** |
| DEBUG | 3 | 3+ | Hybrid | 45K | 5 min | **3x faster** |
| REFACTOR | 4 | 3+ | Hybrid | 43K | 5 min | **3x faster** |
| MIGRATE | 4 | 3+ | Hybrid | 50K | 6 min | **3x faster** |

**Key Insights:**
- ✅ REVIEW/PLAN use shared context (coordination needed)
- ✅ BUILD/DEBUG/REFACTOR/MIGRATE use subagents (parallel execution)
- ✅ Hybrid workflows are 3x faster
- ✅ Token cost increases but speed gains justify it

---

## 🎯 ARCHITECTURE PRINCIPLES

1. **Shared Context** for ANALYSIS (coordination needed)
   - REVIEW: All reviewers see same code, avoid duplicates
   - PLAN: Sequential phases build on each other

2. **Subagents** for EXECUTION (parallelization possible)
   - BUILD: Independent components implemented in parallel
   - DEBUG: Independent bugs fixed in parallel
   - REFACTOR: Independent refactorings executed in parallel
   - MIGRATE: Independent phases migrated in parallel

3. **Skills are PRIMARY** (loaded by workflows for knowledge)
   - No redundant agent layer
   - Progressive loading (on-demand)

4. **Subagents are EXECUTORS** (dispatched for independent work)
   - Fresh context per task
   - True parallelization
   - Quality gates between tasks

**This is the COMPLETE workflow mapping!**

