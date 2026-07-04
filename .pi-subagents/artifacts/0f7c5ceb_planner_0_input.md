# Task for planner

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
Create a precise implementation plan to restore parallel review to cc10x v12.1.

## Context

cc10x v12.1 merged the `silent-failure-hunter` agent into `code-reviewer` as "Pass 1b" to reduce agent count from 10 to 8. This was a mistake — it lost genuine parallelism, context isolation, and the router's merge orchestration pattern. The user lost confidence in the refactoring because of this.

Three parallel patterns were LOST:
1. **BUILD review+hunt parallel dispatch** — two agents in same message, both blocked verifier
2. **BUILD re-review+re-hunt parallel dispatch** — two separate tasks after remediation
3. **Router-owned merged findings summary** — router synthesized findings before verifier handoff

One pattern was PARTIALLY PRESERVED:
4. **Research dual-dispatch** — data model survives but weaker enforcement

One was PRESERVED:
5. **DEBUG fan-out** — unchanged

## What Needs to Be Restored

### 1. Restore `silent-failure-hunter` as a separate agent
- Recreate `plugins/cc10x/agents/silent-failure-hunter.md` from v11 (git show 584049d~1:plugins/cc10x/agents/silent-failure-hunter.md)
- Update frontmatter to v12 conventions (effort field, agent-common skill, color=red)
- The hunter was: read-only, narrow-spectrum (error handling only), zero tolerance, no confidence threshold, no self-healing, separate contract (CLEAN/ISSUES_FOUND vs APPROVE/CHANGES_REQUESTED), suspicion gate

### 2. Restore parallel dispatch in router (§12 step 5)
- Change from "BUILD dispatches exactly ONE code-reviewer" back to "If code-reviewer and silent-failure-hunter are both ready in BUILD: mark both in_progress first, invoke them in the same message"
- Restore the fallback: "If parallel invocation fails: fall back to sequential (reviewer first, then hunter). Never block. Log event=parallel_fallback."
- Restore the parallel-safety rule: "Reviewer and hunter are read-only and safe to parallelize."

### 3. Restore router merge logic (§12 step 6)
- Restore: "if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff"
- Restore contradiction resolution: "stricter verdict wins, log in status_history"

### 4. Restore build-workflow.md task DAG
- Add back the `phase:build-hunt` task (blocked by builder)
- Change verifier to be blocked by [reviewer_task_id, hunter_task_id] (fan-in)
- Restore the escalation path (trivial → full adds both reviewer AND hunter)

### 5. Restore re-hunt in remediation-and-research.md
- Add back the `phase:re-hunt` task after remediation
- Block verifier on [re-review, re-hunt]
- Restore `telemetry.loop_counts.re_hunt`

### 6. Restore verifier handoff format
- Change "Code Reviewer (Pass 1b: Silent Failure Scan)" back to "Silent Failure Hunter" as a separate section

### 7. Restore routing table
- Change routing table row 5 back to: `component-builder -> [code-reviewer || silent-failure-hunter] -> integration-verifier`

### 8. Restore dispatcher table
- Add `build-hunt` → `cc10x:silent-failure-hunter`
- Add `re-hunt` → `cc10x:silent-failure-hunter`

### 9. Remove Pass 1b from code-reviewer
- Remove the "Pass 1b: Silent Failure Scan" step from code-reviewer.md (it goes back to the standalone hunter)
- Remove the "This pass replaces the former standalone silent-failure-hunter agent" line
- Keep the red-flags reference file as a hunter reference, not a reviewer reference

### 10. Fix stale references
- Fix `skills/code-review/SKILL.md` — the "Two Isolated Assessments + WEAVE" section is stale and must either be updated to match the restored parallel pattern or removed if the WEAVE pattern is replaced by the router-owned merge
- Update `workflow-artifact-and-hook-policy.md` — the LEGACY hunter keys become ACTIVE again
- Update skeleton JSON — `hunter` keys are no longer LEGACY

### 11. Restore metadata contract
- Add `phase:build-hunt` and `phase:re-hunt` back to the metadata contract
- Add `build-hunt` and `re-hunt` to the dispatcher table

### 12. Update agent count references
- Plugin manifest, README, CHANGELOG: 8 agents → 9 agents
- Doc consistency check will need updating

### 13. Consider research parallel pattern
- The research dual-dispatch is partially preserved but weaker. Should we also strengthen this? The user might want to know about this too.

## Constraints
- Do NOT lose any v12.1 improvements (effort frontmatter, agent-common skill, model-tier honesty, etc.)
- The restored hunter must have v12 conventions (effort field, agent-common preamble via skills)
- Keep the red-flags reference file
- Maintain the stress test fixes from the latest commit (artifact freshness, event log sync)
- The router's read-back gate and event log append instructions must survive

## Files That Need Changes
1. `plugins/cc10x/agents/silent-failure-hunter.md` — NEW (restored from v11 + v12 conventions)
2. `plugins/cc10x/agents/code-reviewer.md` — Remove Pass 1b
3. `plugins/cc10x/skills/cc10x-router/SKILL.md` — Restore parallel dispatch, merge logic, routing table, dispatcher table, metadata contract
4. `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` — Restore parallel task DAG
5. `plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md` — Restore re-hunt
6. `plugins/cc10x/skills/cc10x-router/references/workflow-artifact-and-hook-policy.md` — Un-LEGACY the hunter keys
7. `plugins/cc10x/skills/cc10x-router/references/workflow-artifact.skeleton.json` — Un-LEGACY hunter keys
8. `plugins/cc10x/skills/code-review/SKILL.md` — Fix stale WEAVE section
9. `plugins/cc10x/agents/integration-verifier.md` — Update verifier handoff to expect separate hunter findings
10. `plugins/cc10x/.claude-plugin/plugin.json` — Agent count 8→9
11. `README.md` — Agent count update
12. `CHANGELOG.md` — Document the restoration

Create a step-by-step plan with exact file paths, what changes in each file, and the order of operations. Include verification steps. The plan must be precise enough that another agent could execute it without ambiguity.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/0f7c5ceb/parallel-review-restoration-plan.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

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