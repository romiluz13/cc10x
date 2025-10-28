# Agents Directory (Deprecated)

⚠️ **This directory is deprecated and no longer used.**

## Architecture Change

The cc10x system has been redesigned to use a **hybrid workflow + subagent architecture** instead of instruction-based agents.

### Old Architecture (Deprecated)
- 11 instruction-based agents
- All agents loaded into same context
- Sequential execution
- No true parallelization

### New Architecture (Current)
- 4 core workflows (REVIEW, PLAN, BUILD, DEBUG)
- 21 domain skills
- 4 specialized subagents
- Hybrid approach: shared context for analysis, subagents for execution
- 3x faster for BUILD and DEBUG workflows
- 27% token savings for REVIEW workflow

## Subagents (New)

Subagents are located in `../subagents/`:

- **component-builder**: Implements single components using TDD
  - Loads: test-driven-development, component-design-patterns, code-generation
  - Dispatched by: BUILD workflow
  - Pattern: One component per subagent instance

- **bug-investigator**: Investigates and fixes individual bugs
  - Loads: systematic-debugging, log-analysis-patterns, root-cause-analysis
  - Dispatched by: DEBUG workflow
  - Pattern: One bug per subagent instance

- **code-reviewer**: Reviews code changes for quality and security
  - Loads: code-quality-patterns, security-patterns, performance-patterns
  - Dispatched by: BUILD and DEBUG workflows
  - Pattern: Reviews each component/fix

- **integration-verifier**: Verifies component integration and system functionality
  - Loads: integration-patterns, test-driven-development
  - Dispatched by: BUILD and DEBUG workflows
  - Pattern: Verifies each integration point

## Workflows (New)

Workflows are located in `../skills/`:

- **review-workflow**: Coordinated multi-dimensional code analysis
  - Loads: 6 skills (risk-analysis, security-patterns, performance-patterns, ux-patterns, accessibility-patterns, code-quality-patterns)
  - Pattern: Shared context (coordination needed)
  - Token cost: ~22K

- **planning-workflow**: Comprehensive feature planning
  - Loads: 7 skills (feature-planning, requirements-analysis, architecture-patterns, api-design-patterns, component-design-patterns, risk-analysis, deployment-patterns)
  - Pattern: Shared context (sequential phases)
  - Token cost: ~35K

- **build-workflow**: Parallel component building with subagents
  - Loads: 5 skills (feature-planning, requirements-analysis, component-design-patterns, code-generation, test-driven-development)
  - Dispatches: component-builder subagents in parallel
  - Pattern: Hybrid (analysis in shared context, execution via subagents)
  - Token cost: ~51K
  - Speed: 3x faster than sequential

- **debug-workflow**: Parallel bug fixing with subagents
  - Loads: 4 skills (systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development)
  - Dispatches: bug-investigator subagents in parallel
  - Pattern: Hybrid (related bugs in shared context, independent bugs via subagents)
  - Token cost: ~45K
  - Speed: 3x faster than sequential

## Migration Notes

All old agent files have been deleted:
- accessibility-reviewer.md ❌
- architect.md ❌
- context-analyzer.md ❌
- devops-planner.md ❌
- implementer.md ❌
- performance-analyzer.md ❌
- quality-reviewer.md ❌
- requirements-analyst.md ❌
- security-reviewer.md ❌
- tdd-enforcer.md ❌
- ux-reviewer.md ❌

The system now uses:
1. **Workflows** for orchestration and coordination
2. **Skills** for domain knowledge and patterns
3. **Subagents** for parallel execution of independent tasks

## Efficiency Improvements

### REVIEW Workflow
- **Before**: 11 agents + 20 skills = ~30K tokens
- **After**: 6 skills in shared context = ~22K tokens
- **Savings**: 27% token reduction

### BUILD Workflow
- **Before**: Sequential component building = 15 minutes
- **After**: Parallel subagents = 5 minutes
- **Speed**: 3x faster

### DEBUG Workflow
- **Before**: Sequential bug fixing = 15 minutes
- **After**: Parallel subagents = 5 minutes
- **Speed**: 3x faster

## Architecture Benefits

1. **Simpler**: No redundant agent layer
2. **Faster**: Parallel execution for independent tasks
3. **Cheaper**: 27% token savings for REVIEW
4. **Cleaner**: Direct skill loading
5. **More Efficient**: Hybrid approach (shared context + subagents)

## For Developers

If you need to add new functionality:
- **New analysis capability?** → Create a new skill
- **New workflow?** → Create a new workflow skill
- **New execution task?** → Create a new subagent

Do NOT create new instruction-based agents. Use the new architecture!

