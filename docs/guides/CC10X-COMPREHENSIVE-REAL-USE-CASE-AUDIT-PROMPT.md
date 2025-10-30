# Real Use Case Audit Prompt for cc10x

Copy this entire prompt into a new chat session to conduct a comprehensive audit of cc10x through real-world scenarios.

---

# CC10X COMPREHENSIVE REAL-USE-CASE AUDIT

## Your Mission

You are the world's most thorough prompt engineering auditor and systems analyst. Your task is to audit cc10x (the Claude Code orchestration system) by:

1. **Understanding the complete system architecture** by reading all documentation (docs/reference/*.md)
2. **Testing with real use cases** that trigger different workflows
3. **Tracing execution flow** to see which workflows activate, which skills/subagents contribute, and how
4. **Identifying gaps** - what should happen vs what actually happens
5. **Evaluating prompt engineering quality** of each component

## Critical Audit Principles

- **NO ASSUMPTIONS**: Read actual files, trace actual execution, verify actual behavior
- **REAL USE CASES ONLY**: Test with scenarios a developer would actually encounter
- **END-TO-END TRACING**: Follow the entire flow from user request → orchestrator → workflow → skills/subagents → output
- **GAP ANALYSIS**: Compare expected behavior (from docs) vs actual behavior (from code)
- **PROMPT ENGINEERING EVALUATION**: Rate clarity, specificity, completeness, actionability (1-10 scale)

## Phase 1: System Understanding

**READ ALL DOCUMENTATION FIRST**:
1. Read `docs/reference/00-START-HERE.md` - Understand the system overview
2. Read `docs/reference/00-OVERVIEW.md` - Understand architecture
3. Read `docs/reference/01-MARKETPLACE-STRUCTURE.md` - Understand plugin structure
4. Read `docs/reference/02-PLUGINS.md` - Understand plugin configuration
5. Read `docs/reference/03-SUBAGENTS.md` - Understand subagent format and behavior
6. Read `docs/reference/04-SKILLS.md` - Understand skills format and progressive disclosure
7. Read `docs/reference/05-SLASH-COMMANDS.md` - Understand commands
8. Read `docs/reference/06-HOOKS.md` - Understand hooks

**READ ORCHESTRATOR LOGIC**:
1. Read `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md` - Understand how orchestrator works
   - How does intent detection work? (Intent Keyword Mapping)
   - How does complexity scoring work? (Complexity Rubric)
   - How does workflow selection work?
   - How does evidence-first verification work?
   - How does memory integration work?
   - How does web-fetch integration work?

**READ ALL WORKFLOWS**:
1. Read `plugins/cc10x/skills/cc10x-orchestrator/workflows/review.md`
   - What triggers this workflow?
   - What phases does it have?
   - Which skills does it load?
   - Which subagents does it invoke?
   - What are the "when to invoke" and "when NOT to invoke" conditions?
   - What output format does it produce?

2. Read `plugins/cc10x/skills/cc10x-orchestrator/workflows/plan.md`
   - Same questions as above
   - How does it handle requirements intake?
   - How does it delegate to planning subagents?
   - How does conflict resolution work?

3. Read `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`
   - Same questions as above
   - How does component execution work?
   - How does failure cascading work?
   - How does TDD enforcement work?

4. Read `plugins/cc10x/skills/cc10x-orchestrator/workflows/debug.md`
   - Same questions as above
   - How does LOG FIRST work?
   - How does investigation timeout work?
   - How does root cause analysis work?

5. Read `plugins/cc10x/skills/cc10x-orchestrator/workflows/validate.md`
   - Same questions as above
   - How does plan vs code comparison work?
   - How does code vs tests verification work?
   - How does documentation freshness checking work?

**READ SUBAGENTS**:
1. Read all 9 subagent SUBAGENT.md files:
   - `code-reviewer/SUBAGENT.md`
   - `component-builder/SUBAGENT.md`
   - `integration-verifier/SUBAGENT.md`
   - `bug-investigator/SUBAGENT.md`
   - `analysis-risk-security/SUBAGENT.md`
   - `analysis-performance-quality/SUBAGENT.md`
   - `analysis-ux-accessibility/SUBAGENT.md`
   - `planning-architecture-risk/SUBAGENT.md`
   - `planning-design-deployment/SUBAGENT.md`

   For each subagent, verify:
   - Does it follow `03-SUBAGENTS.md` format? (frontmatter, structure)
   - Is description clear about when to use it?
   - Are tools specified correctly?
   - Is the system prompt clear and actionable?
   - Does it reference required skills correctly?

**READ KEY SKILLS**:
1. Read `verification-before-completion/SKILL.md` - How does evidence-first work?
2. Read `memory-tool-integration/SKILL.md` - How does memory work?
3. Read `web-fetch-integration/SKILL.md` - How does web fetch work?
4. Read a few domain skills to understand progressive disclosure:
   - `security-patterns/SKILL.md`
   - `test-driven-development/SKILL.md`
   - `risk-analysis/SKILL.md`

## Phase 2: Real Use Case Testing

For EACH use case below, trace the COMPLETE execution flow:

### Use Case 1: "Review the authentication module for security issues"

**Expected Flow**:
1. Orchestrator should detect intent: "review" keyword → review workflow
2. Review workflow should scope files (authentication module)
3. Review workflow should load skills: security-patterns, code-quality-patterns, etc.
4. Review workflow should invoke subagents:
   - `analysis-risk-security` (security-focused, so only this one?)
   - OR all 3 sequentially if general review?
5. Each subagent should:
   - Receive scope and context
   - Load required skills
   - Produce findings with file:line citations
6. Workflow should synthesize results
7. Workflow should produce verification summary with evidence

**Trace and Document**:
- ✅ Which workflow activated? (verify from orchestrator logic)
- ✅ Which skills were loaded? (verify from workflow file)
- ✅ Which subagents were invoked? (verify activation logic)
- ✅ Was subagent selection correct? (security-focused = only security subagent?)
- ✅ Did each subagent receive proper context?
- ✅ Did each subagent produce expected output format?
- ✅ Was evidence-first verification applied?
- ✅ Did output include verification summary?

**Gap Analysis**:
- What SHOULD happen (from docs/workflows)?
- What ACTUALLY happens (from code)?
- Any missing steps?
- Any incorrect sequencing?
- Any missing validation?

### Use Case 2: "Plan a user authentication system with email/password login"

**Expected Flow**:
1. Orchestrator should detect intent: "plan" keyword → plan workflow
2. Plan workflow should intake requirements
3. Plan workflow should check complexity (multi-component = high complexity)
4. Plan workflow should check requirements completeness threshold
5. Plan workflow should invoke subagents:
   - `planning-architecture-risk` (FIRST - architecture needed)
   - `planning-design-deployment` (SECOND - receives architecture outputs)
6. Each subagent should:
   - Load required skills (architecture-patterns, risk-analysis, etc.)
   - Produce architecture/design outputs
   - Reference skill sections
7. Workflow should handle conflicts if subagents disagree
8. Workflow should produce complete plan

**Trace and Document**:
- ✅ Which workflow activated?
- ✅ Was complexity scored correctly?
- ✅ Were requirements checked for completeness?
- ✅ Were both planning subagents invoked? (or skipped due to complexity?)
- ✅ Was sequencing correct? (architecture → design)
- ✅ Did architecture subagent produce required outputs? (system context, containers, components, risk register)
- ✅ Did design subagent receive architecture outputs?
- ✅ Did design subagent produce required outputs? (API design, component design, implementation roadmap, testing strategy, deployment strategy)
- ✅ Was conflict resolution applied if needed?
- ✅ Did plan reference requirements?

### Use Case 3: "Build a login form component with email and password fields"

**Expected Flow**:
1. Orchestrator should detect intent: "build" keyword → build workflow
2. Build workflow should break down into components
3. Build workflow should check complexity (single component = low complexity?)
4. Build workflow should execute component loop:
   - Invoke `component-builder` (TDD: RED → GREEN → REFACTOR)
   - Invoke `code-reviewer` (unless skipped)
   - Invoke `integration-verifier` (unless skipped)
5. Each subagent should:
   - Receive component brief
   - Load required skills
   - Produce evidence (commands, exit codes)
6. Workflow should verify each component before next
7. Workflow should handle blocking review feedback

**Trace and Document**:
- ✅ Which workflow activated?
- ✅ Was complexity scored correctly?
- ✅ Were components identified correctly?
- ✅ Was `component-builder` invoked correctly? (TDD enforced?)
- ✅ Was `code-reviewer` invoked? (or skipped for trivial change?)
- ✅ Was `integration-verifier` invoked?
- ✅ Did component-builder produce RED → GREEN → REFACTOR evidence?
- ✅ Did code-reviewer produce file:line citations?
- ✅ Did integration-verifier run integration tests?
- ✅ Was verification summary included?

### Use Case 4: "Debug the login form - submitting email without @ symbol crashes the app"

**Expected Flow**:
1. Orchestrator should detect intent: "debug" keyword → debug workflow
2. Debug workflow should scope the bug
3. Debug workflow should invoke `bug-investigator`:
   - LOG FIRST mandate
   - Form hypothesis
   - Implement minimal fix
   - Write regression test (RED before fix, GREEN after)
4. Debug workflow should invoke `code-reviewer` (unless skipped)
5. Debug workflow should invoke `integration-verifier` (unless skipped)
6. Investigation timeout should apply (3 attempts max)

**Trace and Document**:
- ✅ Which workflow activated?
- ✅ Was bug scoped correctly?
- ✅ Was `bug-investigator` invoked?
- ✅ Did bug-investigator follow LOG FIRST?
- ✅ Did bug-investigator produce root cause analysis?
- ✅ Did bug-investigator write regression test (RED → GREEN)?
- ✅ Was code-reviewer invoked? (unless trivial fix)
- ✅ Was integration-verifier invoked?
- ✅ Was investigation timeout handled correctly?

### Use Case 5: "Validate that the authentication system matches the plan and all tests pass"

**Expected Flow**:
1. Orchestrator should detect intent: "validate" keyword → validate workflow
2. Validate workflow should:
   - Compare plan vs code (drift classification)
   - Compare code vs tests (coverage thresholds)
   - Compare code vs documentation (freshness verification)
3. Validate workflow should produce alignment matrix
4. Validate workflow should produce verification summary

**Trace and Document**:
- ✅ Which workflow activated?
- ✅ Was plan vs code comparison performed?
- ✅ Were drift types classified? (intentional, accidental, missing, extra)
- ✅ Was code vs tests comparison performed?
- ✅ Were coverage thresholds checked? (unit, integration, E2E)
- ✅ Was documentation freshness checked?
- ✅ Was alignment matrix produced?
- ✅ Were all comparisons evidence-based?

## Phase 3: Prompt Engineering Evaluation

For EACH component below, rate (1-10) and provide specific feedback:

### Orchestrator (`cc10x-orchestrator/SKILL.md`)
- **Clarity**: Are instructions clear and unambiguous? (1-10)
- **Specificity**: Are steps specific enough to follow? (1-10)
- **Completeness**: Are all edge cases covered? (1-10)
- **Actionability**: Can Claude execute without guessing? (1-10)
- **Error Handling**: Are failure modes handled? (1-10)

**Specific Questions**:
- Is intent keyword mapping clear and deterministic?
- Is complexity rubric detailed enough?
- Are skip conditions for workflows clear?
- Is evidence-first verification clearly mandated?
- Are error recovery protocols complete?

### Each Workflow (review.md, plan.md, build.md, debug.md, validate.md)
- **Clarity**: (1-10)
- **Specificity**: (1-10)
- **Completeness**: (1-10)
- **Actionability**: (1-10)
- **Subagent Integration**: Are invocation patterns clear? (1-10)

**Specific Questions**:
- Are "when to invoke" conditions clear?
- Are "when NOT to invoke" conditions clear?
- Are subagent outputs validated?
- Are conflicts prevented/resolved?
- Are verification requirements clear?

### Each Subagent (all 9 SUBAGENT.md files)
- **Format Compliance**: Follows `03-SUBAGENTS.md` format? (1-10)
- **Description Clarity**: Is "when to use" clear? (1-10)
- **System Prompt**: Is role and approach clear? (1-10)
- **Tool Restrictions**: Are tools appropriate? (1-10)
- **Output Format**: Is expected output clear? (1-10)

**Specific Questions**:
- Does description help Claude auto-delegate?
- Is scope clearly defined?
- Are required skills listed?
- Is output format specified with examples?
- Are constraints documented?

## Phase 4: Gap Analysis Report

Create a comprehensive report with:

### 4.1 Execution Flow Verification
For each use case:
- ✅ **Expected vs Actual**: What should happen vs what actually happens
- ❌ **Missing Steps**: Steps that should occur but don't
- ⚠️ **Incorrect Sequencing**: Steps in wrong order
- ❓ **Ambiguities**: Unclear instructions that could cause confusion

### 4.2 Prompt Engineering Gaps
- Missing clarity in [component]
- Missing specificity in [component]
- Missing error handling in [component]
- Missing validation in [component]
- Missing conflict resolution in [component]

### 4.3 Skill/Subagent Integration Gaps
- Skills that should be loaded but aren't
- Subagents that should be invoked but aren't
- Skills/subagents invoked incorrectly
- Missing validation of skill/subagent outputs
- Missing error handling for skill/subagent failures

### 4.4 Workflow Logic Gaps
- Workflow selection logic issues
- Complexity gating issues
- State persistence issues
- Conflict resolution issues
- Verification issues

### 4.5 Missing Features
- Features that should exist based on use cases
- Edge cases not handled
- User preferences not respected
- Memory integration gaps
- Web-fetch integration gaps

## Phase 5: Recommendations

Provide prioritized recommendations:

1. **Critical Issues** (blocks correct execution):
   - [List critical gaps]

2. **Important Issues** (causes incorrect behavior):
   - [List important gaps]

3. **Enhancements** (improves quality):
   - [List enhancement opportunities]

4. **Prompt Engineering Improvements**:
   - [List specific prompt improvements]

## Final Deliverable

Produce a comprehensive audit report with:

1. **System Understanding Summary**: One-paragraph summary of how cc10x works
2. **Use Case Execution Traces**: Detailed trace for each of the 5 use cases
3. **Prompt Engineering Scores**: Rating table for all components
4. **Gap Analysis Matrix**: Table of gaps by category
5. **Recommendations**: Prioritized list of fixes/enhancements
6. **Overall System Rating**: 1-10 rating with justification

**Format**: Save report to `nonprod/COMPREHENSIVE-REAL-USE-CASE-AUDIT-{timestamp}.md`

---

## CRITICAL INSTRUCTIONS FOR AUDITOR

1. **READ FIRST, TEST SECOND**: Never assume - always read actual files
2. **TRACE EVERYTHING**: Follow execution from start to finish
3. **VERIFY ASSERTIONS**: When you say "X should happen", verify it's actually in the code
4. **TEST REAL SCENARIOS**: Use actual developer requests, not theoretical ones
5. **DOCUMENT GAPS**: Every gap should reference what SHOULD happen vs what DOES happen
6. **RATE OBJECTIVELY**: Use 1-10 scale consistently, provide justification
7. **BE BRUTAL**: This system needs to be perfect - find every flaw

**Remember**: This is a production system. Every gap could cause real bugs. Be thorough.

