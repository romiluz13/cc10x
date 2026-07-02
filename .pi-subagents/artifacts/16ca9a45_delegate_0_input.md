# Task for delegate

DEEP ORCHESTRATION REVIEW — Router + References (THE BRAIN)

You are reviewing changes made by another agent to the cc10x router and its references. These are UNCOMMITTED changes in the working tree. Your job is to find ANY orchestration breakage, contradiction, or regression.

The #1 rule: if the orchestration layer is broken, the entire system is broken.

READ THESE FILES FULLY (every word):
1. plugins/cc10x/skills/cc10x-router/SKILL.md (the router — 725+ lines)
2. plugins/cc10x/skills/cc10x-router/references/build-workflow.md
3. plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md
4. plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md
5. plugins/cc10x/skills/cc10x-router/references/plan-workflow.md
6. plugins/cc10x/skills/cc10x-router/references/workflow-artifact.skeleton.json

For EACH file, check:
1. Does it reference any skill or agent that doesn't exist? (List all cc10x: references and verify they resolve to a directory in plugins/cc10x/skills/ or a file in plugins/cc10x/agents/)
2. Are there any contradictions between files? (e.g., one file says agents can read workflow artifacts, another says they can't)
3. Are there any stale references to old skill/agent names? (brainstorming, prototyping, frontend-patterns, frontend-design-critique, finding-duplicate-functions, codebase-deepening, session-memory, handoff-package, code-generation, test-driven-development, code-review-patterns, receiving-code-review, verification-before-completion, planning-patterns, debugging-patterns, architecture-patterns, silent-failure-hunter, web-researcher, github-researcher)
4. Is the reviewer/hunter duality resolved? (There should be ONE review task, not two. No build-hunt task. No parallel reviewer+hunter dispatch.)
5. Is the model-tier policy now implementable? (Should be advisory, not a HARD rule that can't be enforced)
6. Does the git-guard approval token logic in build-workflow.md make sense? (BUILD-DONE should document when the token is written)
7. Are contract fields consistent across router §8, the override table, and what agents actually emit?
8. Does the skeleton JSON match the documented schema? (Every field in the skeleton should be documented, every documented field should be in the skeleton)
9. Is the deferred_findings field now in the skeleton and schema?
10. Are there any broken markdown tables (unescaped pipes in table cells)?
11. Does the dispatcher table map to exactly 8 agents that exist?
12. Is the §14 hard rule about artifact access now consistent with dispatch hygiene?

Also check:
- Run: grep -rn "cc10x:" plugins/cc10x/skills/cc10x-router/ | grep -oE "cc10x:[a-z-]+" | sort -u
- Verify EVERY reference resolves to an existing skill or agent
- Run: grep -rn "build-hunt\|re-hunt\|silent-failure-hunter\|hunter" plugins/cc10x/skills/cc10x-router/
- These should be gone or documented as legacy back-compat only

Return a structured report with:
(A) Per-file analysis
(B) Orchestration integrity check (all references resolve, no orphans)
(C) Contradiction check (any two rules that conflict)
(D) Reviewer/hunter resolution verification
(E) Contract consistency check
(F) Skeleton/schema alignment
(G) Any NEW issues introduced by the changes
(H) VERDICT: is the orchestration layer intact or broken?

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/16ca9a45/file-only
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```