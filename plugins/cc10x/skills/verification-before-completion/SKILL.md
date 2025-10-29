---
name: verification-before-completion
description: Evidence-first gate that blocks success claims without fresh verification. Use before claiming completion, marking tasks as done, declaring fixes complete, or stating readiness without verification evidence. Apply before saying "done", "fixed", or "ready".
allowed-tools: Read, Grep, Glob, Bash
---

# Verification Before Completion

## Core Rule
```
No success claims without fresh, local evidence collected after the latest change.
```

## Required Actions
1. Identify the behaviour or acceptance criteria to prove.
2. Run the necessary commands (tests, lint, build, manual reproduction) on the current branch.
3. Capture command, arguments, exit code, and essential output.
4. Map evidence to each acceptance criterion and edge case.
5. Produce a Verification Summary and only then communicate completion.

## Verification Summary Template
```
# Verification Summary
Scope: <files/modules>
Criteria: <list>
Commands:
- <command> -> exit <code>
Evidence:
- <log/report snippet>
Risks / Follow-ups: <items still pending>
```

## Red Flags - Do Not Claim Completion If
- Output and exit codes are missing or from previous runs.
- Edge cases (error paths, limits, security checks) were not exercised.
- The verification relies solely on remote CI without local confirmation.
- Language such as "should", "probably", or "seems" replaces evidence.

## Interaction Notes
- Workflows must invoke this skill before presenting final results.
- Subagents (builder, reviewer, verifier, investigator) include the summary in their hand-off.
- If verification cannot be performed, state exactly why and request direction rather than assuming success.

## References
- Skill contract: `docs/reference/04-SKILLS.md`
