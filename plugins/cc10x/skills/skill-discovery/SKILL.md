---
name: skill-discovery
description: Provides mandatory skill discovery workflows for orchestrator-driven system. Use when starting any conversation - establishes mandatory workflows for finding and using skills in orchestrator-driven system. Ensures skills are discovered before workflow selection and prevents rationalization.
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST read the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

# Skill Discovery - Orchestrator-Driven System

## MANDATORY FIRST RESPONSE PROTOCOL

Before responding to ANY user message, you MUST complete this checklist:

1. ☐ **MANDATORY: Check for cc10x-orchestrator FIRST** - Scan user request for workflow keywords (plan, build, review, debug, validate, implement, create, design, architect, fix, error, bug, analyze, assess, verify, check)
2. ☐ **If workflow keywords found** → Load orchestrator skill IMMEDIATELY using Skill tool: `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`
3. ☐ **If orchestrator loaded** → Follow orchestrator's workflow selection and execution
4. ☐ **If no workflow keywords** → Still check orchestrator (it handles all code tasks) - Load orchestrator skill using Skill tool
5. ☐ **After orchestrator runs** → Check for additional skills that orchestrator may have missed
6. ☐ List available skills in your mind
7. ☐ Ask yourself: "Does ANY skill match this request?"
8. ☐ If yes → Use the Skill tool to read and run the skill file
9. ☐ Announce which skill you're using
10. ☐ Follow the skill exactly

**Responding WITHOUT completing this checklist = automatic failure.**

**CRITICAL**: If orchestrator not loaded and workflow keywords detected, STOP and load orchestrator IMMEDIATELY before proceeding.

## Quick Start

Always check for orchestrator first, then discover additional skills.

**Example:**

1. **User says**: "Review this code for security issues"
2. **Check orchestrator**: Detect "review" keyword → Load orchestrator skill
3. **Orchestrator activates**: REVIEW workflow loads code-review-patterns skill (consolidates security-patterns, code-quality-patterns, performance-patterns)
4. **Check for additional skills**: Verify no other skills needed
5. **Use skills**: Follow orchestrator workflow and code-review-patterns skill

**Result:** Correct skills loaded and used through orchestrator coordination.

## Integration with cc10x Orchestrator

**Orchestrator-Driven Discovery**:

- **MANDATORY: Load cc10x-orchestrator skill BEFORE any other skill check** - Orchestrator is the MANDATORY entry point for all workflows
- **Explicit Command**: Use Skill tool to load `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`
- **Validation**: If orchestrator not loaded and workflow keywords detected, STOP and load it immediately
- The cc10x orchestrator automatically loads skills based on workflow selection
- After orchestrator activates, check for additional skills that orchestrator may have missed
- The orchestrator coordinates workflow execution, but you should verify no skills are missed

**Orchestrator Keyword Detection**:

Before checking other skills, scan user request for workflow keywords:

**PLAN Keywords**: plan, planning, planner, design, designing, architect, architecture, roadmap, strategy
**BUILD Keywords**: build, building, implement, implementation, create, creating, write code, coding, develop, development, make, making
**REVIEW Keywords**: review, reviewing, audit, auditing, analyze, analysis, assess, assessment, evaluate, evaluation, inspect, inspection, examine, examination
**DEBUG Keywords**: debug, debugging, fix, fixing, error, errors, bug, bugs, investigate, investigation, failure, failures, broken, issue, issues, problem, problems, troubleshoot, troubleshooting, diagnose, diagnosis
**VALIDATE Keywords**: validate, validation, verify, verification, check, checking, confirm implementation, alignment check, consistency check

**Detection Logic**:

1. Scan user request for ANY workflow keyword above (case-insensitive)
2. If keywords found → Load orchestrator skill IMMEDIATELY using Skill tool
3. Then proceed with orchestrator's workflow selection
4. If no keywords found → Still load orchestrator (it handles all code tasks)

**Workflow Selection**:

- Orchestrator detects workflow intent (review/plan/build/debug/validate) FIRST
- Orchestrator then loads workflow-specific skills automatically
- After orchestrator runs, verify no additional skills are needed that orchestrator missed

## Critical Rules

1. **MANDATORY: Load orchestrator FIRST** - Before checking any other skills, load cc10x-orchestrator skill using Skill tool: `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`
2. **Follow mandatory workflows.** Check for relevant skills before ANY task.
3. **Execute skills with the Skill tool** - Load skills before announcing usage
4. **Orchestrator coordination** - Check orchestrator FIRST, then verify no additional skills needed
5. **If orchestrator not loaded** - STOP and load it immediately before proceeding

## Before Coding

**What did you understand about what I just said to you?**

**How will you go about implementing it?**

Please provide:

1. **Clear understanding**: Restate what you think I'm asking for
2. **Step-by-step plan**: Exactly how you will implement it
3. **File changes**: Which files you'll modify/create and what changes
4. **Potential issues**: Any risks, dependencies, or considerations
5. **Success criteria**: How we'll know it's working correctly

**CRITICAL**: Please wait for my review and confirmation before beginning your implementation. Do not start coding until I approve your plan.

This ensures we're aligned before you begin work and prevents miscommunication or wasted effort.

## Common Rationalizations That Mean You're About To Fail

If you catch yourself thinking ANY of these thoughts, STOP. You are rationalizing. Check for and use the skill.

- "This is just a simple question" → WRONG. Questions are tasks. Check for skills.
- "I can check git/files quickly" → WRONG. Files don't have conversation context. Check for skills.
- "Let me gather information first" → WRONG. Skills tell you HOW to gather information. Check for skills.
- "This doesn't need a formal skill" → WRONG. If a skill exists for it, use it.
- "I remember this skill" → WRONG. Skills evolve. Run the current version.
- "This doesn't count as a task" → WRONG. If you're taking action, it's a task. Check for skills.
- "The skill is overkill for this" → WRONG. Skills exist because simple things become complex. Use it.
- "I'll just do this one thing first" → WRONG. Check for skills BEFORE doing anything.
- "The orchestrator will load skills" → WRONG. Check orchestrator FIRST, then verify no additional skills needed.

**Why:** Skills document proven techniques that save time and prevent mistakes. Not using available skills means repeating solved problems and making known errors.

If a skill for your task exists, you must use it or you will fail at your task.

## Skills with Checklists

If a skill has a checklist, YOU MUST create TodoWrite todos for EACH item.

**Don't:**

- Work through checklist mentally
- Skip creating todos "to save time"
- Batch multiple items into one todo
- Mark complete without doing them

**Why:** Checklists without TodoWrite tracking = steps get skipped. Every time. The overhead of TodoWrite is tiny compared to the cost of missing steps.

# About these skills

**Many skills contain rigid rules (debugging, verification, service patterns).** Follow them exactly. Don't adapt away the discipline.

**Some skills are flexible patterns (architecture, naming).** Adapt core principles to your context.

The skill itself tells you which type it is.

## Instructions ≠ Permission to Skip Workflows

Your human partner's specific instructions describe WHAT to do, not HOW.

"Add X", "Fix Y" = the goal, NOT permission to skip verification, alignment, or proper implementation patterns.

**Red flags:** "Instruction was specific" • "Seems simple" • "Workflow is overkill"

**Why:** Specific instructions mean clear requirements, which is when workflows matter MOST. Skipping process on "simple" tasks is how simple tasks become complex problems.

## Summary

**Starting any task:**

1. If relevant skill exists → Use the skill
2. Announce you're using it
3. Follow what it says
4. Let orchestrator coordinate workflow-specific skills

**Skill has checklist?** TodoWrite for every item.

**Finding a relevant skill = mandatory to read and use it. Not optional.**

## Troubleshooting

**Common Issues:**

1. **Orchestrator not checked first**
   - **Symptom**: Other skills loaded but orchestrator missed
   - **Cause**: Didn't follow mandatory first response protocol
   - **Fix**: Always check orchestrator FIRST before other skills
   - **Prevention**: Follow mandatory checklist in order

2. **Skills not discovered**
   - **Symptom**: Relevant skill exists but not used
   - **Cause**: Didn't complete skill discovery checklist
   - **Fix**: Complete checklist, list available skills, check for matches
   - **Prevention**: Always complete discovery checklist before tasks

3. **Rationalizing skill usage away**
   - **Symptom**: Skill exists but not used, rationalizations given
   - **Cause**: Falling into rationalization traps
   - **Fix**: Review "Common Rationalizations" section, use skill anyway
   - **Prevention**: Never rationalize away skill usage

**If issues persist:**

- Verify orchestrator was checked first
- Complete mandatory first response protocol
- Review common rationalizations section
- Ensure skill discovery checklist completed

## Integration with cc10x Workflows

CRITICAL: Orchestrator runs FIRST, then verify skills:

1. **Check orchestrator FIRST** - Orchestrator is MANDATORY entry point for all workflows
2. **Orchestrator detects workflow** - Based on keywords (review/plan/build/debug/validate)
3. **Orchestrator loads workflow skills** - Automatically loads required and conditional skills
4. **Orchestrator coordinates subagents** - Dispatches subagents based on workflow needs
5. **You follow workflow phases** - Execute workflow phases as defined
6. **Verify no skills missed** - After orchestrator runs, check if any additional skills needed

**Your role**: Check orchestrator FIRST, then verify no additional skills needed. Orchestrator's role: Coordinate workflow execution.
