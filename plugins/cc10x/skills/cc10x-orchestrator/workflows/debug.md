# DEBUG Workflow - Root Cause First

**Triggered by:** User requests help investigating bugs, errors, or unexpected behaviour.

## Phase 0 - Intake

**Memory Integration** (optimized):
- **Load Failure Modes Once**: Read `.claude/memory/failure_modes.json` ONCE, cache for workflow duration
- **Semantic Match**: Use `jq` + `grep` to match error_pattern (regex) against current error message
- **Top Matches Only**: Return top 3 failure modes with highest success_rate (>60%)
- **Fix Patterns**: Check `.claude/memory/patterns.json` for fix_patterns matching error type

**Bug Information Gathering**:
1. Gather reproduction steps, error messages, logs, and recent changes.
2. Confirm scope (single bug per run unless explicitly broadened).

**External Resource Check** (smart caching):
- **Check Cache First**: Lookup URLs in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - Error docs: 30-day TTL
  - If cached and TTL valid → use cache (skip fetch)
  - If cached but expired → re-fetch
  - If not cached → fetch and cache
- Check if debug needs external resources:
  - Error documentation? → Check cache first, then fetch if needed
  - Stack trace analysis? → Check cache first, then fetch if needed
  - Library-specific issues? → Check cache first, then fetch library troubleshooting docs if needed
- Ask user: "Should I fetch external debugging resources? Found {N} in cache. Fetch missing? (yes/no)"
3. **Bug Classification**: Classify bug type before investigation:
   - **Reproducible**: Clear steps, consistent failure
   - **Intermittent**: Fails sometimes, unclear pattern
   - **Non-reproducible**: Cannot reproduce with given steps
   - **External**: Requires environment/data not available
   - **Performance**: Slow response, resource exhaustion
   - **Functional**: Wrong behavior, crash, error

**Action by Bug Type**:
- **Reproducible**: Proceed with standard workflow
- **Intermittent**: Add monitoring/logging, investigate patterns, estimate probability, may require multiple attempts
- **Non-reproducible**: Request more data (logs, environment, steps), pause investigation until data available
- **External**: Investigate external dependency, document limitation
- **Performance**: Focus on profiling, bottlenecks, resource usage (load performance-patterns skill)
- **Functional**: Focus on logic, state, data flow

**Multiple Bugs Handling**:
- If scope spans multiple independent failures, queue them and tackle serially unless the user approves separate runs.
- If bugs are NOT independent (related failures), investigate together as single root cause may affect multiple symptoms.

**Workflow State Persistence** (Checkpoint System):
- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/debug_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "debug",
    "phase": "Phase_2_Bug_Investigation_Loop",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "bugs": [{name, status, investigation_attempts, root_cause}],
      "investigation_history": [...],
      "fixes_applied": [...],
      "current_bug": "BugName"
    },
    "next_phase": "Phase_3_Consolidation"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/debug_*.json`
  2. Validate checkpoint state (bugs present, investigation valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}, Bug {name}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2 (after each bug), Phase 3, Phase 4 completion

**Context Restoration**:
- **If resuming after compaction or context is unclear**, use checkpoint system:
  - Read most recent checkpoint from `.claude/memory/workflow_state/debug_*.json`
  - If checkpoint exists: Restore state and continue from `next_phase`
  - If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

## Phase 1 - Shared Skills

**Required Skills**:
- `systematic-debugging`
- `log-analysis-patterns`
- `root-cause-analysis`
- `test-driven-development`
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external resources needed)

**Skill Loading Verification Protocol**:
For each skill above:
1. Read first 100 chars of `plugins/cc10x/skills/{skill-name}/SKILL.md` to verify file exists
2. Parse YAML frontmatter to verify valid format
3. Check body content exists (not empty)
4. If any verification fails:
   - Report immediately: "Skill '{name}' failed to load: {error details}"
   - Present options: Continue without {skill} / Abort workflow / Retry loading
   - Wait for user decision before proceeding
5. Document successfully loaded skills in Actions Taken section

**Bug Type Skill Selection**:
- For performance bugs: Also load `performance-patterns`
- For security-related bugs: Also load `security-patterns`
- For integration bugs: Also load `integration-patterns`

## Phase 2 - Bug Investigation Loop
For each identified bug:
1. Invoke `bug-investigator` with all context. Require:
   - Reproduction of the failure.
   - Collection of relevant logs/metrics (LOG FIRST).
   - Written hypothesis before implementing fixes.
   - Failing regression test proving the bug.
2. Once the fix is proposed, re-run the regression test to verify GREEN and document commands run.
3. Send the changes to `code-reviewer` for validation (quality, security, performance).
4. Use `integration-verifier` to confirm there are no regressions in the broader flow.

File size sanity check: As fixes accumulate, if any modified file exceeds ~500 lines, propose a focused refactor/split plan (after green tests).

**Subagent Invocation Pattern** (per bug):
- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SKILL.md` or `SUBAGENT.md`
- Read the subagent's SKILL.md to load its process and output format.
- Provide the repro steps, logs, and scope from Phase 0.
- Require the specified outputs with file:line evidence and command outputs.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (root cause, evidence, fix, regression test)
    - [ ] File references include path:line where applicable
    - [ ] Commands included with exit codes (RED → GREEN proof)
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (root cause identified, fix provided)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
- **On failure or missing repro**: Use Error Recovery Protocol
  - If bug not reproducible: Request more data, pause investigation
  - If subagent fails: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Investigation Timeout** (CRITICAL):
- **Timeout Threshold**: 3 attempts to find root cause
- **Attempt Tracking**: Count investigation attempts per bug:
  - Attempt 1: Initial investigation (logs, tests, hypothesis)
  - Attempt 2: Deeper investigation (additional logging, more tests, refined hypothesis)
  - Attempt 3: Comprehensive investigation (all available data, multiple hypotheses)
- **Timeout Trigger**: After 3 attempts without root cause identification:
  1. Document all investigation attempts:
     ```
     Investigation Attempts (3/3):
     - Attempt 1: [logs checked, tests run, hypotheses tested]
     - Attempt 2: [additional investigation details]
     - Attempt 3: [comprehensive investigation details]
     ```
  2. Present escalation options:
     ```
     Investigation Timeout (3 attempts):
     Root cause not identified after 3 investigation attempts.
     
     Options:
     1. Add strategic logging → Capture bug when it occurs naturally
     2. Request more data → User provides environment details, logs, reproduction steps
     3. Skip investigation → Mark as "cannot reproduce, needs manual investigation"
     4. Escalate to user → User provides domain expertise or manual investigation
     ```
  3. **Wait for user decision** (with 5-minute timeout per orchestrator error recovery)
  4. **Document timeout**: Log to Actions Taken: "Investigation timeout after 3 attempts"

**Escalation Paths**:
If bug-investigator cannot determine root cause (before timeout):
1. Document investigation attempts:
   - Logs checked: [list]
   - Tests run: [list with results]
   - Hypotheses tested: [list with outcomes]
2. List remaining possibilities with probability estimates:
   - Hypothesis A: 60% probability - [reason]
   - Hypothesis B: 30% probability - [reason]
   - Hypothesis C: 10% probability - [reason]
3. Recommend next steps:
   - **Additional logging/monitoring**: Add strategic logging to capture bug when it occurs
   - **User-provided reproduction environment**: Request environment details (OS, dependencies, data, config)
   - **External dependency investigation**: Check external services, APIs, databases
   - **Escalation to domain expert**: Requires knowledge not in skills
4. Ask user which path to pursue (if not at timeout)

**External Dependency Handling**:
If bug investigation requires external services unavailable:
1. Check if service available: ping/health check
2. If unavailable:
   - **Option A**: Mock services (document limitation: "Investigation limited - external service unavailable")
   - **Option B**: Skip investigation, verify contract/structure only
   - **Option C**: Request user to provide test environment
3. Document approach chosen and limitations

## Phase 3 - Consolidation
- Summarise root cause, fix, and verification evidence for each bug.
- List any follow-up work (monitoring, additional tests) recommended by the skills used.

## Phase 4 - Verification Summary

**MANDATORY**: Use exact template:

```
## Verification Summary
Scope: <bugs investigated>
Bugs fixed: <list>
Criteria: <what was verified - reproduction, fix, regression prevention>
Commands:
- <command> -> exit <code>
- <command> -> exit <code>
Evidence:
- <log snippets showing bug>
- <test output showing RED then GREEN>
- <integration test results>
Residual risk: <items to monitor, edge cases not covered>
```

**Example**:
```
## Verification Summary
Scope: Cart null pointer exception
Bugs fixed: Cart crash when items array is null
Criteria: Bug reproduces, fix prevents crash, regression test passes
Commands:
- npm test test/cart.spec.ts -> exit 1 (RED - null pointer)
- Apply null check in src/cart.ts:85
- npm test test/cart.spec.ts -> exit 0 (GREEN)
- npm test test/integration/cart-flow.spec.ts -> exit 0
Evidence:
- Log: "TypeError: Cannot read property 'length' of null at cart.ts:42"
- Test: "should handle null items array" -> passes
Residual risk: Add e2e test for empty cart state
```

## Phase 5 - Report

**Before Reporting** (optimized memory):
- **Validate Fix Success**:
  - Did fix actually resolve the bug? (verify with tests/verification)
  - Track success: fixed successfully? (true/false)
- **Store Failure Mode** (only if fix validated successful):
  - Save to `.claude/memory/failure_modes.json` ONLY if fix worked
  - Format: `{error_pattern, root_causes: [{cause, fix, success_rate, occurrences, last_seen}]}`
  - If failure mode exists: update success_rate, increment occurrences, update last_seen
  - If success_rate < 60% after 5+ fixes → mark for deletion
- **Store Fix Pattern** (only validated):
  - Save fix approach ONLY if validated successful
  - Track success_rate across multiple uses
- **Auto-Delete Rules**:
  - Delete failure modes unused > 30 days
  - Delete failure modes with success_rate < 60%
- **Run Cleanup**: Execute memory cleanup script

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Debug Report

## Executive Summary
[2-3 sentences summarizing root cause, fix status, and overall resolution]

## Actions Taken
- Skills loaded: systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development, verification-before-completion
- Subagents invoked: bug-investigator, code-reviewer, integration-verifier
- Bugs investigated: [list]
- Tools used: [Read, Edit, Write, Bash, Grep, Glob]

## Findings / Decisions

### Bug {name}
- **Root Cause**: [what failed and why]
- **Evidence**: [log excerpts, stack traces, code paths]
- **Fix**: [what changed, file:line]
- **Regression Test**: [test name, file:line]
- **Verification**: [command outputs showing RED → GREEN]

### Reproduction
- Steps: [detailed reproduction steps]
- Environment: [OS, dependencies, config]
- Error Messages: [full error messages]
- Logs: [relevant log snippets]

### Investigation Timeline
- [Hypothesis 1]: [result]
- [Hypothesis 2]: [result]
- [Root Cause Found]: [explanation]

### Fix & Regression Test
- Changes: [file:line diffs summary]
- Tests Added: [list]
- GREEN Proof: [command outputs]

### Reviews & Integration
- code-reviewer findings: [resolved/open]
- integration-verifier scenarios: [pass/fail with logs]

## Verification Summary
[Use exact template from Phase 4]

## Recommendations / Next Steps
[Prioritized: Monitoring setup, additional tests, prevention measures]

## Open Questions / Assumptions
[If escalation needed, external dependencies unavailable, or assumptions made]
```

**Validation Before Presenting**:
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes commands with exit codes
- [ ] Root cause clearly explained with evidence
- [ ] Regression test documented with RED → GREEN proof
- [ ] Reviews and integration status documented
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken

**Offer Optional Next Steps**:
- "Want a code review of the patch?" (without assuming consent)
- "Run review workflow on fixed code?" (without assuming consent)

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

**If Reproduction Cannot Be Established**:
1. **Context**: What was attempted (reproduction steps tried, logs checked)
2. **Problem**: Cannot reproduce bug with provided information
3. **Options**:
   - **Request more data**: User provides additional logs, environment details, or steps
   - **Add logging**: Add strategic logging to capture bug when it occurs
   - **Skip investigation**: Mark as "cannot reproduce" and document limitation
4. **Impact**: Explain what each choice means
5. **Default**: Request more data (ensures proper investigation)

**If Fix Fails Review/Integration**:
1. **Context**: What was attempted (fix applied, tests run)
2. **Problem**: Review rejects fix or integration test fails
3. **Options**:
   - **Return to bug-investigator**: Revise fix based on feedback
   - **Accept review concerns**: Document as risk or limitation
   - **Fix integration**: Update integration code
4. **Impact**: Explain what each choice means
5. **Default**: Return to bug-investigator (ensures quality)

**Critical Rules**:
- Never mark bugs as fixed without captured test or log evidence
- Never proceed without user decision when failure occurs
- Document all failures in Actions Taken section
- If bug cannot be reproduced after multiple attempts, escalate to user with options

## References
- Debugging discipline: `plugins/cc10x/skills/systematic-debugging/SKILL.md`
- Official guidance: `docs/reference/03-SUBAGENTS.md`, `docs/reference/04-SKILLS.md`
