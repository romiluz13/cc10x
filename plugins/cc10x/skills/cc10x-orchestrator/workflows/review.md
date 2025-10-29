# REVIEW Workflow - Evidence Based Code Analysis

**Triggered by:** User asks for review, audit, or quality/security checks.

## Phase 0 - Input Validation
1. Confirm files, directories, or patterns to review.
2. Ask for clarification if the scope is ambiguous.
3. If the code scope is very small, warn and confirm before proceeding.
4. If resuming after compaction or context is unclear, read the latest snapshot and working plan:
   - Read `.claude/memory/snapshots/` most recent `snapshot-*.md`
   - Read `.claude/memory/WORKING_PLAN.md`

## Phase 1 - Load Required Skills
Load these domain skills (all exist under `plugins/cc10x/skills/`):
- `risk-analysis`
- `security-patterns`
- `performance-patterns`
- `code-quality-patterns`
- `ux-patterns`
- `accessibility-patterns`

## Phase 2 - Dispatch Analysis Subagents
Run the bundled subagents one after another (no simulated parallel execution):
1. `analysis-risk-security`
2. `analysis-performance-quality`
3. `analysis-ux-accessibility`

For each subagent, pass the scoped files and relevant user notes. Require every subagent to produce:
- Findings grouped by severity (critical, high, medium, low).
- File references including path and line numbers.
- Specific remediation steps tied to the skill guidance that surfaced them.

Invocation pattern:
- Read the subagent's SKILL.md to load its process and output format.
- Pass the same scope and relevant notes to the subagent.
- Require the specified outputs with file:line evidence.
- If the subagent fails, stop and ask whether to retry or continue.

## Phase 3 - Synthesis
1. Merge the subagent outputs, deduplicating identical issues.
2. Flag conflicts or open questions for the user.
3. Highlight blockers (critical/high) before suggestions.
4. File size sanity check: If any reviewed file exceeds ~500 lines, flag it for refactor/splitting and suggest a concrete split plan.

## Phase 4 - Verification Summary
Before claiming the review is complete, compose a verification block:
```
# Verification Summary
Scope: <files reviewed>
Evidence: cited lines + tool outputs if any static analysis commands were executed
Outstanding Questions: <if clarification is needed>
```
Use this summary when presenting results.

Examples:
- Good evidence: "high - SQL injection via string concatenation - src/db/user.ts:42 - Evidence: user input concatenated into query without parameterization. Mitigation: use prepared statements (see security-patterns 'SQL Injection')."
- Weak evidence: "maybe insecure DB calls somewhere in user code"

## Phase 5 - Present Results
Return a markdown report with:
- Executive summary (issues by severity + go/no-go recommendation).
- Detailed findings grouped by category (security, quality, performance, UX, accessibility).
- Actionable next steps linked to the responsible code sections.
- Optional follow-up offer (plan fixes, run build workflow, etc.) without assuming consent.

## Failure Handling
- If any skill or subagent fails to load, stop and ask the user how to proceed.
- Never fabricate findings for missing data; report the failure explicitly.

## References
- Skill usage rules: `docs/reference/04-SKILLS.md`
- Subagent contract: `docs/reference/03-SUBAGENTS.md`
