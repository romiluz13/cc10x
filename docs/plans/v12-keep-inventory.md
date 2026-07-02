# v12 Keep Inventory — What Must Survive the Refactor

Every item here is a unique cc10x innovation. Removing any one causes quality regression.

## Router (the brain)

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 1 | Workflow artifacts (`.cc10x/workflows/{uuid}.json`) | Durable state — the model doesn't hold everything in context. Router remembers phase, tasks, event log. |
| 2 | Intent routing table (ERROR > PLAN > REVIEW > ORIENT > BUILD) | Different work needs different workflows. Correct routing is the first quality gate. |
| 3 | Complexity gradient (trivial vs standard) | Trivial tasks don't get planner/reviewer/hunter — prevents over-processing. Escalates on scope growth. |
| 4 | Per-role model-tier policy | Cheap models for mechanical work, capable models for planning/verification. Cost optimization. |
| 5 | Inline-fallback mode | Graceful degradation when Agent primitive unavailable — workflow still runs. |
| 6 | Dispatcher table (phase → agent mapping) | Single source of truth for which agent runs in which phase. |
| 7 | Dispatch-by-reference | Agents receive paths, not pasted content. Orchestrator stays lean. |
| 8 | CONTRACT envelope + validation | Structured quality gates, not prose assertions. Router parses and validates. |
| 9 | Change-something-before-re-dispatch | Never re-dispatches same agent+model+input. Forces variation. |
| 10 | Circuit breaker (max 3 remediation cycles) | Caps infinite retry loops. Cycle-cap gate enforces. |
| 11 | Re-review precondition gate | REM-FIX must contain COVERING_TESTS+TEST_COMMAND+TEST_OUTPUT before re-review. |
| 12 | Task metadata format (wf:kind:origin:phase:plan:scope:reason) | Router resume/hydration depends on this format. |
| 13 | Memory finalization (router-owned single-writer) | Only router writes `.cc10x/memory.md`. Compaction KEEP/SUMMARIZE/DROP rubric. |

## Build Phase

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 14 | Clean-baseline diff | Records baseline failures BEFORE build. Post-build diff against baseline_failures separates new from pre-existing. |
| 15 | Per-phase BASE sha | Records HEAD before each phase. Review/verify sees exact phase changes, not noise. |
| 16 | SCOPE_INCREASES escalation (component-builder) | If scope grows beyond trivial, escalates to standard BUILD with planner + reviewer. |

## Debug Phase

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 17 | Feedback Loop FIRST (10-rung repro ladder) | Construction before hypothesis. Prevents speculative fixes. |
| 18 | Blast radius scan after debug fixes | Variant scan dimensions — catches same-file duplicates, similar patterns elsewhere. |
| 19 | Verify-before-implement dispute | REM-FIX must restate findings. Can dispute with VERIFY_COMMAND. Verifier adjudicates. |

## Review Phase

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 20 | Anti-anchoring plan review | plan-gap-reviewer gets FRESH context — no `.cc10x/*.md` loaded. No inherited bias. |
| 21 | Two Isolated Assessments | reviewer + hunter in parallel, WEAVE protocol. Independent reviewers don't anchor each other. |
| 22 | Code-reviewer Pass 5 (Plan Validity) | Catches "built the wrong thing well" — reviews plan alignment. |
| 23 | Code-reviewer Pass 6 (Spec Compliance) | Reviews against original spec, not just code quality. |

## Verification

| # | Innovation | Why it stays |
|---|-----------|--------------|
| 24 | Test Honesty Gates | False-green detection: mock assertions, schema-incomplete mocks, DB-bypass, test-tampering, condition-based-waiting. Unique to cc10x. |

## Planning

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 25 | Interfaces block (Consumes/Produces) | Cross-phase contract — each phase declares what it consumes and produces. |
| 26 | Codebase Reality Check with ADR reading | Planner reads pre-existing decision records as constraints, not suggestions. |

## Cross-Cutting

| # | Innovation | Why it stays |
| --- | ----------- | -------------- |
| 27 | Scar-note convention | Dated notes on gates explaining what failure was prevented. Audit trail. |
| 28 | Diff-driven docs (3-layer impact classifier) | Classifies changes by impact layer. Fast-path skip for low-impact. |
| 29 | Handoff package (temp dir, path references, secret redaction) | Clean handoffs between sessions without context bloat. |
| 30 | Prototyping Hard Wall | Prototype rules never leak into BUILD. Absorbing a prototype = fresh BUILD. |

---

## What Gets Cut (zero regression)

- Rationalization Prevention tables (~200 lines across 8 skills)
- "Red Flags - STOP" sections (~150 lines)
- "BAD: ... GOOD: ..." code examples (~100 lines)
- Duplicated LSP-Powered tables (same content in 4 skills → 1 reference)
- Duplicated Validation Levels table (in planning + verification → keep 1)
- Duplicated Functionality Flow Mapping (in planning + architecture → keep 1)
- Common Patterns code examples (model generates better from context)
- Quick Five-Step Process in debugging (duplicates the 4 phases)
- Procedural step-by-step hand-holding (modern Claude knows how to debug, review, test)
- Agent boilerplate that moves to native frontmatter (memory, effort, maxTurns, skills)
