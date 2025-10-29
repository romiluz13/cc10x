# REVIEW Workflow - Evidence Based Code Analysis

**Triggered by:** User asks for review, audit, or quality/security checks.

## Phase 0 - Input Validation

**Memory Integration** (optimized):
- **Load Preferences**: Query `.claude/memory/preferences.json` for review preferences (if exists)
- **Load Patterns Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration
- **Query Common Issues**: Use `jq` to filter patterns matching code type/structure (top 5 only)
- **Validation**: Only use patterns with high success_rate or frequent occurrences

1. Confirm files, directories, or patterns to review.
2. Ask for clarification if the scope is ambiguous.
3. **Scope Size Validation**: Define "very small" and handle accordingly:
   - Single file < 50 lines = warn: "Scope is small (1 file, {N} lines). Continue or use lighter review?"
   - Single function < 20 lines = warn: "Scope is very small (1 function, {N} lines). Continue?"
   - If user confirms, proceed; if not, ask for broader scope

**External Resource Check** (smart caching):
- **Check Cache First**: Lookup URLs in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - Standards/Guidelines: 90-day TTL (stable content)
  - If cached and TTL valid → use cache (skip fetch)
  - If cached but expired → re-fetch
  - If not cached → fetch and cache
- Check if review needs external standards:
  - Security standards? → Check cache first, then fetch OWASP guidelines if needed
  - Coding standards? → Check cache first, then fetch guidelines if needed
  - Performance standards? → Check cache first, then fetch guides if needed
- Ask user: "Should I fetch external standards? Found {N} in cache. Fetch missing? (yes/no)"

**Workflow State Persistence** (Checkpoint System):
- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/review_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "review",
    "phase": "Phase_2_Dispatch_Analysis_Subagents",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "files_reviewed": [...],
      "subagents_completed": [...],
      "findings": {...},
      "conflicts": [...]
    },
    "next_phase": "Phase_3_Synthesis"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/review_*.json`
  2. Validate checkpoint state (files present, subagents valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2 (after each subagent), Phase 3, Phase 4 completion

**If resuming after compaction or context is unclear**, use checkpoint system:
  - Read most recent checkpoint from `.claude/memory/workflow_state/review_*.json`
  - If checkpoint exists: Restore state and continue from `next_phase`
  - If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

## Phase 1 - Load Required Skills

**Required Skills** (all exist under `plugins/cc10x/skills/`):
- `risk-analysis`
- `security-patterns`
- `performance-patterns`
- `code-quality-patterns`
- `ux-patterns`
- `accessibility-patterns`
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external standards needed)

**Skill Loading Verification Protocol**:
For each skill above:
1. Read first 100 chars of `plugins/cc10x/skills/{skill-name}/SKILL.md` to verify file exists
2. Parse YAML frontmatter to verify valid format
3. Check body content exists (not empty)
4. If any verification fails:
   - Report immediately: "Skill '{name}' failed to load: {error details}"
   - Present options:
     - **Continue without {skill}**: Proceed with reduced analysis (functionality reduced)
     - **Abort workflow**: Stop and verify skill exists (ensures complete analysis)
     - **Retry loading**: Attempt again (if transient error)
   - Wait for user decision before proceeding
5. Document successfully loaded skills in Actions Taken section

**If Skill Missing**:
- Report: "Required skill '{name}' not found. Available skills: [list]"
- Ask user: "Continue without {skill} or abort workflow?"

## Phase 2 - Dispatch Analysis Subagents
Run the bundled subagents one after another (no simulated parallel execution):
1. `analysis-risk-security`
2. `analysis-performance-quality`
3. `analysis-ux-accessibility`

For each subagent, pass the scoped files and relevant user notes. Require every subagent to produce:
- Findings grouped by severity (critical, high, medium, low).
- File references including path and line numbers.
- Specific remediation steps tied to the skill guidance that surfaced them.

**Subagent Invocation Pattern**:
- Read the subagent's SKILL.md to load its process and output format.
- Verify subagent exists before invoking: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SKILL.md` or `SUBAGENT.md`
- Pass the same scope and relevant notes to the subagent.
- Require the specified outputs with file:line evidence.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (findings by severity, file:line references, remediation steps)
    - [ ] File references include path:line where applicable
    - [ ] Findings grouped by severity (critical, high, medium, low)
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (remediation steps provided)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
- **If subagent fails**:
  - Use Error Recovery Protocol (see orchestrator)
  - Report: "Subagent '{name}' failed: {error}"
  - Options: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Subagent Empty Findings Handling**:
- If subagent returns no findings, this may be normal (clean code) or suspicious (subagent didn't analyze)
- Verify: Did subagent analyze the correct scope? Check subagent output for confirmation
- If suspicious: Ask user "Subagent '{name}' found no issues. Is this expected, or should I investigate?"

## Phase 3 - Synthesis

**Conflict Resolution Protocol**:
If subagents report conflicting findings:
1. Document the conflict explicitly with both positions:
   ```
   Conflict Detected:
   - analysis-risk-security: [finding/position]
   - analysis-performance-quality: [conflicting finding/position]
   ```
2. Identify root cause:
   - Different assumptions
   - Different priorities (security vs performance)
   - Different interpretations of code
3. Present to user with options:
   - **Accept both**: Document as alternative approaches
   - **Choose priority**: User selects which concern takes precedence
   - **Resolve with context**: Provide additional context to resolve
4. Document resolution in final report

**Synthesis Steps**:
1. Merge the subagent outputs, deduplicating identical issues (same file:line, same issue type).
2. Apply Conflict Resolution Protocol for any conflicts.
3. Highlight blockers (critical/high) before suggestions (medium/low).
4. **File size sanity check**: If any reviewed file exceeds ~500 lines:
   - Flag immediately in synthesis (don't wait for final report)
   - Provide concrete split plan: "File {path} ({N} lines) exceeds 500-line guideline. Suggested split: [list components/files]"
   - Ask user: "Proceed with split recommendation or mark as tech debt?"

## Phase 4 - Verification Summary

**MANDATORY**: Compose verification block using exact template:

```
## Verification Summary
Scope: <files reviewed>
Criteria: <list of what was verified - security, performance, quality, UX, accessibility>
Commands:
- <command> -> exit <code> (if any static analysis was run)
- <command> -> exit <code>
Evidence:
- <cited file:line references>
- <tool output snippets if any>
Outstanding Questions: <if clarification is needed>
```

**Evidence Quality Examples**:
- ✅ **Good evidence**: "HIGH - SQL injection via string concatenation - src/db/user.ts:42 - Evidence: user input concatenated into query without parameterization. Mitigation: use prepared statements (see security-patterns 'SQL Injection')."
- ❌ **Weak evidence**: "maybe insecure DB calls somewhere in user code" (reject - must cite specific file:line)

**Required**: Every finding must include file:line citation. If unable to cite, state "Insufficient evidence - requires manual review" instead of guessing.

## Phase 5 - Present Results

**Before Presenting** (optimized memory):
- **Store Common Issues** (only high-value):
  - Save issue patterns ONLY if appear frequently (>3 occurrences across files)
  - Format: `{issue_type, occurrence_count, common_location, fix_pattern}`
  - Update existing patterns: increment occurrence_count if pattern exists
- **Store Review Patterns** (only validated):
  - Save successful review approaches ONLY if validated effective
  - Track success rate: did approach find real issues?
- **Run Cleanup**: Execute memory cleanup script

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Review Report

## Executive Summary
[2-3 sentences summarizing total issues by severity, go/no-go recommendation, and overall code health status]

## Actions Taken
- Skills loaded: risk-analysis, security-patterns, performance-patterns, code-quality-patterns, ux-patterns, accessibility-patterns
- Subagents invoked: analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility
- Files reviewed: [list]
- Tools used: [Read, Grep, Glob, Bash if any]

## Findings / Decisions

### Security Findings
- **CRITICAL**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **HIGH**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **MEDIUM**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **LOW**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]

### Performance Findings
[Same format as Security]

### Code Quality Findings
[Same format as Security]

### UX Findings
[Same format as Security]

### Accessibility Findings
[Same format as Security]

## Verification Summary
[Use exact template from Phase 4]

## Recommendations / Next Steps
[Prioritized list - CRITICAL first, then HIGH, then others]

## Open Questions / Assumptions
[If any conflicts were detected or clarification needed]
```

**Validation Before Presenting**:
- [ ] Executive Summary present (2-3 sentences)
- [ ] All findings include file:line citations
- [ ] Verification Summary includes commands (if any) with exit codes
- [ ] Recommendations prioritized (CRITICAL → HIGH → MEDIUM → LOW)
- [ ] All subagents/skills documented in Actions Taken
- [ ] Conflicts documented if any

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

If any skill or subagent fails:
1. **Context**: What was attempted (skill/subagent name, file path, command if any)
2. **Problem**: What failed (error message, exit code, file not found, etc.)
3. **Options**:
   - **Retry**: Attempt again (if transient error likely)
   - **Continue without {component}**: Proceed with reduced functionality
   - **Abort workflow**: Stop and restart
4. **Impact**: Explain what each choice means
5. **Default**: Recommended action

**Critical Rules**:
- Never fabricate findings for missing data; report the failure explicitly
- Never proceed without user decision when failure occurs
- Document all failures in Actions Taken section

## References
- Skill usage rules: `docs/reference/04-SKILLS.md`
- Subagent contract: `docs/reference/03-SUBAGENTS.md`
