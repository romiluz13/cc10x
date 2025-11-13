---
name: brainstorming
description: Use when creating or developing, before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning, alternative exploration, and incremental validation. Integrated with PLAN workflow Phase 1.
---

# Brainstorming Ideas Into Designs - PLAN Workflow Integration

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue. This skill is integrated into the PLAN workflow Phase 1 for requirements refinement.

**🚨 CRITICAL REQUIREMENT**: Create the plan file `.claude/docs/plans/<topic>-design.md` BEFORE asking questions, then update it incrementally after EACH answer. Do NOT wait until the end to write everything at once.

Start by understanding the current project context, then ask multiple related questions together (up to 4 at once) to efficiently refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## Quick Start

Refine ideas into designs through collaborative questioning and incremental validation.

**Example:**

1. **Create plan file**: `.claude/docs/plans/file-upload-design.md` (BEFORE asking questions)
2. **Ask questions**: "What file types? What size limits? Where stored?"
3. **Update plan**: Add answers to plan file immediately
4. **Present design**: Show architecture section (200-300 words), validate
5. **Refine**: Adjust based on feedback, update plan file

**Result:** Fully-formed design document ready for implementation planning.

## Integration with PLAN Workflow

**PLAN Workflow Phase 1**: This skill is used in Phase 1 for requirements refinement:

- After Phase 0 (Functionality Analysis), use brainstorming to refine requirements
- Create design document incrementally
- Ask questions to clarify requirements
- Present design sections for validation
- Output feeds into Phase 2 (planning-patterns skill, which consolidates feature-planning)

**Orchestrator Coordination**: The orchestrator loads this skill in PLAN Phase 1, coordinates question-answer cycles, then transitions to planning-patterns in Phase 2.

## The Process

**CRITICAL FIRST STEP - Create Plan File Immediately:**

- **Before asking ANY questions, create `.claude/docs/plans/<topic>-design.md` using Write tool**
- Write initial context: problem statement, initial understanding (even if incomplete)
- Structure: Use headings like "Goals", "Requirements", "Architecture", "Open Questions"
- This file is your working document - update it continuously throughout brainstorming
- **DO NOT wait until the end** - write first, refine continuously

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- **After EACH round of answers, immediately update the plan file using Edit tool**
- Ask multiple related questions together using the AskUserQuestion tool (up to 4 per call)
- **CRITICAL**: Always use the AskUserQuestion tool for ALL questions - NEVER output questions as plain text
- Prefer multiple choice questions when possible (the tool supports multiSelect when needed)
- Group related questions together for efficiency (e.g., scope + timeline + constraints in one call)
- Focus on understanding: purpose, constraints, success criteria
- After each round of answers, ask follow-up questions to drill deeper into areas that need clarification
- **Pattern: Question → Answer → Update plan file → Next question**

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Use AskUserQuestion tool after each section to confirm it looks right (e.g., "Does this architecture look right?")
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**

- The plan file `.claude/docs/plans/<topic>-design.md` should already exist and be complete
- **You should have been updating it throughout the entire brainstorming process**
- If you haven't been updating it incrementally, you made a mistake - fix it now
- Final pass: Review for clarity, completeness, and consistency
- Use elements-of-style:writing-clearly-and-concisely skill if available for polish

**Incremental Writing Pattern (THE CORRECT WAY):**

```
WRONG ❌:
1. Ask all questions
2. Get all answers
3. Write entire plan at the end

CORRECT ✅:
1. Write initial plan file with problem statement
2. Ask question batch 1
3. Immediately update plan file with answers
4. Ask question batch 2
5. Immediately update plan file with answers
6. Present design section by section
7. Update plan file with any refinements
8. Final review and polish
```

Example workflow:

1. **Start**: Write `.claude/docs/plans/2025-11-05-pcc-sync-design.md` with initial understanding
2. **Question 1**: Ask about goals → User answers → Edit plan file "Goals" section
3. **Question 2**: Ask about technical constraints → User answers → Edit plan file "Requirements" section
4. **Question 3**: Ask about data types → User answers → Edit plan file "Data Types" section
5. **Design**: Present architecture → User approves → Edit plan file "Architecture" section
6. **Refinement**: User asks about error handling → Edit plan file to add "Error Handling" section
7. **Complete**: Plan file reflects entire conversation

The plan file is your **working document**, not a final deliverable to write at the end

**Handoff to Planning Patterns**:

- After design is complete, orchestrator transitions to Phase 2
- Phase 2 uses planning-patterns skill (consolidates feature-planning) to create detailed implementation plan
- Design document feeds into planning-patterns as input

## Key Principles

- **Use AskUserQuestion tool** - ALWAYS use the tool for questions, never plain text
- **Ask multiple questions** - Group related questions together (up to 4) for efficiency
- **Multiple choice preferred** - The tool makes it easy for users to select from options
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each with AskUserQuestion
- **Be flexible** - Go back and clarify when something doesn't make sense

## Summary

**For PLAN Workflow Phase 1**:

- Create design document immediately
- Ask questions incrementally, update document after each answer
- Present design in sections, validate each section
- Complete design document feeds into Phase 2 (planning-patterns, which consolidates feature-planning)

**Result**: Refined requirements and complete design document ready for implementation planning.

## Troubleshooting

**Common Issues:**

1. **Plan file not created before asking questions**
   - **Symptom**: Questions asked but plan file doesn't exist
   - **Cause**: Skipped CRITICAL FIRST STEP
   - **Fix**: Create plan file immediately, then ask questions
   - **Prevention**: Always create plan file BEFORE asking questions

2. **Plan file not updated incrementally**
   - **Symptom**: Plan file written at end, missing intermediate updates
   - **Cause**: Didn't update plan file after each answer
   - **Fix**: Update plan file after EACH answer immediately
   - **Prevention**: Always update plan file incrementally

3. **Questions not using AskUserQuestion tool**
   - **Symptom**: Questions output as plain text instead of tool
   - **Cause**: Didn't use AskUserQuestion tool
   - **Fix**: Use AskUserQuestion tool for ALL questions
   - **Prevention**: Always use AskUserQuestion tool, never plain text

**If issues persist:**

- Verify plan file was created before questions
- Check that plan file is updated after each answer
- Ensure AskUserQuestion tool is used for questions
- Review incremental writing pattern section
