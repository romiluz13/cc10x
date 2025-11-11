---
name: deployment-patterns
description: Plans deployment with functionality-first, context-dependent approach. Use PROACTIVELY when planning feature deployments. First understands functionality using universal questions and context-dependent flows, then plans deployment strategy to support that functionality. Understands project deployment patterns and conventions. Focuses on deployment that enables functionality, not generic deployment patterns. Provides specific deployment and rollback strategies with examples.
allowed-tools: Read, Grep, Glob
---

# Deployment Patterns - Functionality First, Context-Dependent

## The Iron Law

```
NO DEPLOYMENT WITHOUT VERIFICATION FIRST
```

**CRITICAL**: Before planning deployment, understand functionality using context-dependent analysis. Verify deployment supports functionality at each step.

## Functionality First Mandate

**CRITICAL**: Before planning deployment, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs deployment (using universal questions and context-dependent flows), then plan deployment strategy to support that functionality. Deployment exists to enable functionality, not for its own sake.

## Quick Decision Tree

```
DEPLOYMENT NEEDED?
│
├─ Understand Functionality First
│  ├─ Context-dependent analysis complete? → Continue
│  └─ Not complete? → STOP, complete functionality analysis first
│
├─ Understand Project Patterns
│  ├─ Deployment method identified? → Continue
│  └─ Not identified? → Analyze project configs first
│
├─ Plan Deployment Strategy
│  ├─ Supports functionality flows? → Continue
│  └─ Generic patterns? → STOP, refocus on functionality
│
└─ Execute Deployment
   ├─ Verify functionality at each step? → Continue
   └─ Skip verification? → STOP, add verification
```

## When to Use

**Use PROACTIVELY when**:

- Planning feature deployments
- Creating rollback strategies
- Setting up monitoring
- Designing staged rollouts

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Understand project deployment patterns and conventions
3. **Then**: Plan deployment strategy to support that functionality
4. **Then**: Provide specific deployment strategies with examples
5. **Focus**: Deployment that enables functionality, not generic deployment patterns

## Core Process Overview

### Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

**Process**:

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type (User Flow, System Flow, Integration Flow, etc.)

### Step 2: Understand Project Deployment Patterns (BEFORE Planning)

**CRITICAL**: Understand how this project deploys before planning deployment strategy.

**Project Context Analysis**:

1. **Read Deployment Configuration**: `package.json` scripts, `Dockerfile`, CI/CD configs, infrastructure configs
2. **Identify Deployment Patterns**: Deployment method, rollback strategy, staging strategy, monitoring approach
3. **Understand Project Conventions**: How features deployed, how rollbacks handled, how monitoring set up

### Step 3: Plan Deployment Strategy (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only plan deployment AFTER you understand functionality and project deployment patterns.

**Functionality-Focused Deployment Checklist**:

**Priority: Critical (Core Functionality)**:

- [ ] Deployment steps support functionality flows
- [ ] Deployment order supports functionality dependencies
- [ ] Rollback strategy supports functionality
- [ ] Monitoring supports functionality (tracks functionality metrics)
- [ ] Health checks verify functionality

**Priority: Important (Supporting Functionality)**:

- [ ] Staged rollout tests functionality
- [ ] Feature flags support functionality
- [ ] Environment variables support functionality
- [ ] Database migrations support functionality

## Deployment Strategies

**CRITICAL**: Provide specific, actionable deployment strategies with examples, not generic patterns.

### Strategy 1: Deployment Steps

Plan deployment steps aligned with functionality flows. Deploy dependencies first, verify functionality at each step.

**Reference**: `references/deployment-steps.md` for detailed guidance with examples.

### Strategy 2: Rollback Strategy

3-level rollback model: Feature Flag (< 5 min), Configuration Rollback (< 10 min), Code Rollback (< 15 min). All aligned with functionality.

**Reference**: `references/rollback-strategies.md` for detailed rollback patterns and triggers.

### Strategy 3: Staged Deployment

Staged rollout that tests functionality at each stage (10% → 50% → 100%). Monitor functionality metrics, not just deployment success.

**Reference**: `references/staged-deployment.md` for detailed staged rollout patterns.

### Strategy 4: Monitoring Setup

Monitor functionality metrics aligned with flows (User Flow, System Flow, Integration Flow). Set up alerts and rollback triggers based on functionality health.

**Reference**: `references/monitoring-observability.md` for detailed monitoring patterns and setup.

## Red Flags - STOP

If you catch yourself thinking:

- "Just deploy it, we'll fix issues later"
- "Skip verification, deployment looks good"
- "Use generic deployment pattern, it works for others"
- "Monitor generic metrics, functionality will be fine"
- "Rollback later if needed, deploy now"

**ALL of these mean: STOP. Return to Step 1 (Functionality Analysis).**

## Quick Reference

| Phase                         | Key Activities                                          | Success Criteria                 |
| ----------------------------- | ------------------------------------------------------- | -------------------------------- |
| **1. Functionality Analysis** | Context-dependent analysis, universal questions, flows  | Functionality understood         |
| **2. Project Patterns**       | Read configs, identify patterns, understand conventions | Deployment method identified     |
| **3. Plan Strategy**          | Align deployment with functionality, plan rollback      | Strategy supports functionality  |
| **4. Execute**                | Deploy with verification, monitor functionality         | Functionality works at each step |

## Reference Files

**For detailed deployment strategies, see**:

- **`references/deployment-steps.md`**: Detailed deployment steps aligned with functionality flows, deployment order, verification steps
- **`references/rollback-strategies.md`**: 3-level rollback model, rollback triggers, functionality-based rollback decisions
- **`references/staged-deployment.md`**: Staged rollout patterns (10% → 50% → 100%), functionality testing at each stage
- **`references/monitoring-observability.md`**: Functionality metrics, monitoring setup, alert configuration, rollback triggers

**For additional patterns and reference materials, see**:

- **PATTERNS.md**: Deployment Pattern Library (Blue-Green, Canary, Feature Flag) and Rollback-Ready Design Patterns
- **REFERENCE.md**: Deployment Strategy Decision Matrix, 5-Stage Deployment Sequence, Monitoring Metrics, Deployment Timing, Post-Rollback Procedure, Pre-Deployment Checklist, Decision Framework

## Integration with Orchestrator

This skill is loaded by orchestrator workflows when deployment planning is detected. The orchestrator coordinates:

- Functionality analysis (Phase 0)
- Skill loading (Phase 2)
- Deployment planning execution

**CRITICAL**: Maintain functionality-first approach. Deployment planning must follow functionality analysis.

## Priority Classification

**Critical (Must Have)**:

- Deployment steps support functionality flows
- Deployment order supports functionality dependencies
- Rollback strategy supports functionality
- Monitoring supports functionality (tracks functionality metrics)
- Health checks verify functionality

**Important (Should Have)**:

- Staged rollout tests functionality
- Feature flags support functionality
- Environment variables support functionality
- Database migrations support functionality

**Minor (Can Defer)**:

- Perfect deployment pipeline (if functionality is supported)
- Ideal rollback strategy (if functionality is supported)
- Perfect monitoring setup (if functionality is supported)

---

**Remember**: Deployment exists to support functionality. Don't plan deployment for deployment's sake! Understand functionality first, understand project patterns second, then plan deployment to support functionality.
