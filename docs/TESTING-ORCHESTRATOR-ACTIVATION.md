# Testing Orchestrator Activation

**Purpose**: Test all keyword triggers and enforcement mechanisms to ensure orchestrator activates correctly.

## Test Cases

### 1. Individual Workflow Keyword Testing

Test each workflow keyword individually:

**PLAN Keywords:**

- [ ] "plan a feature" → Orchestrator loads → PLAN workflow activates
- [ ] "planning user authentication" → Orchestrator loads → PLAN workflow activates
- [ ] "design a component" → Orchestrator loads → PLAN workflow activates
- [ ] "architect a system" → Orchestrator loads → PLAN workflow activates
- [ ] "create a roadmap" → Orchestrator loads → PLAN workflow activates

**BUILD Keywords:**

- [ ] "build a component" → Orchestrator loads → BUILD workflow activates
- [ ] "implement authentication" → Orchestrator loads → BUILD workflow activates
- [ ] "create a feature" → Orchestrator loads → BUILD workflow activates
- [ ] "write code for login" → Orchestrator loads → BUILD workflow activates
- [ ] "develop user profile" → Orchestrator loads → BUILD workflow activates

**REVIEW Keywords:**

- [ ] "review this code" → Orchestrator loads → REVIEW workflow activates
- [ ] "audit security" → Orchestrator loads → REVIEW workflow activates
- [ ] "analyze performance" → Orchestrator loads → REVIEW workflow activates
- [ ] "assess code quality" → Orchestrator loads → REVIEW workflow activates
- [ ] "evaluate this implementation" → Orchestrator loads → REVIEW workflow activates

**DEBUG Keywords:**

- [ ] "debug this error" → Orchestrator loads → DEBUG workflow activates
- [ ] "fix this bug" → Orchestrator loads → DEBUG workflow activates
- [ ] "investigate failure" → Orchestrator loads → DEBUG workflow activates
- [ ] "troubleshoot issue" → Orchestrator loads → DEBUG workflow activates
- [ ] "diagnose problem" → Orchestrator loads → DEBUG workflow activates

**VALIDATE Keywords:**

- [ ] "validate implementation" → Orchestrator loads → VALIDATE workflow activates
- [ ] "verify code matches plan" → Orchestrator loads → VALIDATE workflow activates
- [ ] "check alignment" → Orchestrator loads → VALIDATE workflow activates
- [ ] "confirm consistency" → Orchestrator loads → VALIDATE workflow activates

### 2. Keyword Variation Testing

Test keyword variations and synonyms:

- [ ] "planning" (not just "plan") → PLAN workflow
- [ ] "planner" → PLAN workflow
- [ ] "plan a" → PLAN workflow
- [ ] "plan the" → PLAN workflow
- [ ] "building" (not just "build") → BUILD workflow
- [ ] "implementing" → BUILD workflow
- [ ] "creating" → BUILD workflow
- [ ] "reviewing" → REVIEW workflow
- [ ] "analyzing" → REVIEW workflow
- [ ] "debugging" → DEBUG workflow
- [ ] "fixing" → DEBUG workflow
- [ ] "validating" → VALIDATE workflow
- [ ] "verifying" → VALIDATE workflow

### 3. Multiple Keywords Testing

Test requests with multiple keywords:

- [ ] "plan and build a feature" → Intent Disambiguation → User selects workflow
- [ ] "review then plan" → Sequential execution → Both workflows run
- [ ] "build and debug" → Intent Disambiguation → User selects workflow

### 4. Ambiguous Requests Testing

Test ambiguous or unclear requests:

- [ ] "make it better" → No keywords → Ask user: "Which workflow?"
- [ ] "improve this" → No keywords → Ask user: "Which workflow?"
- [ ] "work on this" → No keywords → Ask user: "Which workflow?"

### 5. Orchestrator Auto-Loading Testing

Verify orchestrator loads automatically:

- [ ] User says "plan" → Orchestrator skill description matches → Skill loads automatically
- [ ] User says "build" → Orchestrator skill description matches → Skill loads automatically
- [ ] User says "review" → Orchestrator skill description matches → Skill loads automatically
- [ ] User says "debug" → Orchestrator skill description matches → Skill loads automatically
- [ ] User says "validate" → Orchestrator skill description matches → Skill loads automatically

### 6. Skill-Discovery Enforcement Testing

Verify skill-discovery forces orchestrator loading:

- [ ] User says "plan" → Skill-discovery detects keyword → Forces orchestrator load
- [ ] User says "build" → Skill-discovery detects keyword → Forces orchestrator load
- [ ] User says workflow keyword → Skill-discovery checklist item 1 → Load orchestrator IMMEDIATELY

### 7. Workflow Selection Testing

Verify correct workflow selected:

- [ ] "plan a feature" → PLAN workflow selected (not BUILD)
- [ ] "build a component" → BUILD workflow selected (not PLAN)
- [ ] "review this code" → REVIEW workflow selected (not DEBUG)
- [ ] "debug this error" → DEBUG workflow selected (not REVIEW)
- [ ] "validate implementation" → VALIDATE workflow selected (not REVIEW)

### 8. Enforcement Mechanisms Testing

Verify all enforcement mechanisms activate:

- [ ] Actions Taken section created and updated
- [ ] Skills Inventory Check performed before Phase 3
- [ ] Subagents Inventory Check performed before Phase 4
- [ ] TDD cycle followed (for BUILD workflow)
- [ ] Memory integration used (patterns queried/stored)
- [ ] Web fetch integration used (if external APIs mentioned)
- [ ] Validation gates stop workflow if checks fail

### 9. Fallback Mechanisms Testing

Test fallback scenarios:

- [ ] Orchestrator doesn't load → Skill-discovery forces load
- [ ] Keywords don't match → Ask user: "Which workflow?"
- [ ] Multiple workflows match → Intent Disambiguation → User selects
- [ ] No workflows match → Ask user: "Which workflow?"

### 10. Context.json Rules Testing

Verify context.json rules enforce orchestrator:

- [ ] Context.json rule loads orchestrator skill
- [ ] AlwaysApply rules active
- [ ] Orchestrator rule description includes keyword triggers
- [ ] Example in description: "plan a feature → orchestrator loads"

## Success Criteria

After testing, verify:

1. ✅ Orchestrator auto-loads for 95%+ of workflow requests
2. ✅ Correct workflow selected for 98%+ of requests
3. ✅ All enforcement mechanisms activate automatically
4. ✅ No bypass possible - direct code writing prevented
5. ✅ Validation gates work correctly
6. ✅ Fallback mechanisms handle edge cases

## Testing Checklist

- [ ] All individual keywords tested
- [ ] All keyword variations tested
- [ ] Multiple keywords tested
- [ ] Ambiguous requests tested
- [ ] Orchestrator auto-loading verified
- [ ] Skill-discovery enforcement verified
- [ ] Workflow selection verified
- [ ] Enforcement mechanisms verified
- [ ] Fallback mechanisms verified
- [ ] Context.json rules verified

## Expected Results

**Before Implementation:**

- Orchestrator may not load when user says "plan"
- Workflow selection may be incorrect
- Enforcement mechanisms may not activate

**After Implementation:**

- Orchestrator loads automatically for all workflow keywords
- Correct workflow selected consistently
- All enforcement mechanisms activate automatically
- No bypass possible
