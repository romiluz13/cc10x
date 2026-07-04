# Verification: System Prompt Consistency

## Methodology

Read all 9 agent files in `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/` and the shared preamble at `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/agent-common/SKILL.md`. Verified 10 criteria per agent plus 3 additional cross-cutting checks. All skill references were validated against the actual skills directory contents. File references (live_harness_runner.py, review_package.py) were verified to exist.

### Reference: Skills That Exist

```
agent-common, architecture, building, cc10x-router, code-review, codebase-hygiene,
debugging, diff-driven-docs, exploration, frontend, mcp-cli, memory-and-handoff,
plan-review-gate, planning, research, update, verification
```

### Cross-Cutting Checks

| Check | Result | Evidence |
| ------- | -------- | ---------- |
| References to "Pass 1b" that should have been removed | **PASS** — none found | `grep -r "Pass 1b" agents/` → no matches |
| References to hunter as "LEGACY" | **PASS** — none found | `grep -r "LEGACY" agents/` → no matches |
| Stale references to old skill names | **PASS** — none found | Searched for `cc10x:hunting`, `cc10x:silent-failure`, `cc10x:bug-hunt`, `cc10x:memory-and-handoff`, `cc10x:update`, `cc10x:exploration` — no matches. All `cc10x:` references point to existing skills. |
| Broken file references | **PASS** — none found | `live_harness_runner.py` exists at `tools/live_harness_runner.py`; `review_package.py` exists at `tools/review_package.py` |

---

## Per-Agent Verification

### 1. planner.md — **PASS** (with observations)

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: cyan` |
| 4 | Correct `tools` list | ✅ PASS | Has Edit/Write — planner writes plan files to `docs/plans/`, not read-only |
| 5 | CONTRACT envelope format | ⚠️ OBSERVATION | Uses YAML `Router Contract (MACHINE-READABLE)` block, not `CONTRACT {json}` envelope. No `CONTRACT {` line found in file. |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated in body; inherited via `cc10x:agent-common` preamble |
| 7 | Memory First protocol | ✅ PASS | Inherited via `cc10x:agent-common` preamble (which contains Memory First) |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:planning`, `cc10x:architecture` — all exist. Body references `cc10x:plan-review-gate` which exists. |
| 9 | Broken references | ✅ PASS | `docs/plans/`, `docs/adr/`, `docs/decisions/`, `docs/rfcs/` are pattern globs, not broken file refs |
| 10 | Memory Notes format | ⚠️ OBSERVATION | Has `MEMORY_NOTES` in YAML contract (learnings, patterns, verification) — no `### Memory Notes` section. Missing `deferred` field. |

**Verdict: PASS** — core frontmatter and skill loading are correct. The YAML-vs-CONTRACT-envelope format difference is a design choice shared by all builder agents.

---

### 2. bug-investigator.md — **PASS** (with observations)

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: red` |
| 4 | Correct `tools` list | ✅ PASS | Has Edit/Write — bug-investigator fixes bugs via TDD, not read-only |
| 5 | CONTRACT envelope format | ⚠️ OBSERVATION | Uses YAML `Router Contract (MACHINE-READABLE)` block, not `CONTRACT {json}` envelope |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated in body; inherited via `cc10x:agent-common` preamble |
| 7 | Memory First protocol | ✅ PASS | Inherited via `cc10x:agent-common` preamble. Also references `.cc10x/activeContext.md` for debug tracking. |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:debugging`, `cc10x:building`, `cc10x:verification` — all exist. Body references `cc10x:researcher` (agent, not skill) and `cc10x:research` (skill, told NOT to call directly) — both valid. |
| 9 | Broken references | ✅ PASS | No broken file references found |
| 10 | Memory Notes format | ⚠️ OBSERVATION | Has `MEMORY_NOTES` in YAML contract (learnings, patterns, verification, deferred) — no `### Memory Notes` section |

**Verdict: PASS** — core frontmatter and skill loading are correct.

---

### 3. component-builder.md — **PASS** (with observations)

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: medium` |
| 3 | Correct `color` field | ✅ PASS | `color: green` |
| 4 | Correct `tools` list | ✅ PASS | Has Edit/Write — component-builder implements code via TDD, not read-only |
| 5 | CONTRACT envelope format | ⚠️ OBSERVATION | Uses YAML `Router Contract (MACHINE-READABLE)` block, not `CONTRACT {json}` envelope |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated in body; inherited via `cc10x:agent-common` preamble |
| 7 | Memory First protocol | ✅ PASS | Inherited via `cc10x:agent-common` preamble |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:building`, `cc10x:verification` — all exist |
| 9 | Broken references | ✅ PASS | No broken file references found |
| 10 | Memory Notes format | ⚠️ OBSERVATION | Has `MEMORY_NOTES` in YAML contract (learnings, patterns, verification, deferred) — no `### Memory Notes` section |

**Verdict: PASS** — core frontmatter and skill loading are correct.

---

### 4. code-reviewer.md — **PASS**

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: blue` |
| 4 | Correct `tools` list | ✅ PASS | `Read, Bash, Grep, Glob, Skill, LSP, WebFetch` — no Edit/Write. READ-ONLY agent correctly lacks mutation tools. |
| 5 | CONTRACT envelope format | ✅ PASS | `CONTRACT {"s":"APPROVE","b":false,"cr":0}` — present in output template |
| 6 | SINGLE FINAL RESPONSE RULE | ✅ PASS | Explicitly stated: `SINGLE FINAL RESPONSE RULE (CRITICAL — this is why output reaches the router)` |
| 7 | Memory First protocol (anti-anchoring variant) | ✅ PASS | Has `## Memory First (CRITICAL - DO NOT SKIP)` — reads `patterns.md` and `progress.md` but explicitly skips `activeContext.md` (anti-anchoring). Documented as deliberate override of agent-common three-file protocol. |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:code-review`, `cc10x:verification`, `cc10x:codebase-hygiene` — all exist |
| 9 | Broken references | ✅ PASS | References `tools/review_package.py` which exists at `tools/review_package.py` |
| 10 | Memory Notes format | ✅ PASS | Has `### Memory Notes (For Workflow-Final Persistence)` section with Learnings, Patterns, Verification, Deferred |

**Verdict: PASS** — all 10 criteria satisfied. This is the gold-standard agent file.

---

### 5. silent-failure-hunter.md — **PASS**

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: red` |
| 4 | Correct `tools` list | ✅ PASS | `Read, Bash, Grep, Glob, Skill, LSP, WebFetch` — no Edit/Write. READ-ONLY agent correctly lacks mutation tools. |
| 5 | CONTRACT envelope format | ✅ PASS | `CONTRACT {"s":"CLEAN","b":false,"cr":0}` — present in output template |
| 6 | SINGLE FINAL RESPONSE RULE | ✅ PASS | Explicitly stated: `SINGLE FINAL RESPONSE RULE (CRITICAL — this is why output reaches the router)` |
| 7 | Memory First protocol (anti-anchoring variant) | ✅ PASS | Has `## Memory First (CRITICAL — DO NOT SKIP)` — reads `patterns.md` and `progress.md` but skips `activeContext.md` (anti-anchoring) |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:code-review` — both exist |
| 9 | Broken references | ✅ PASS | No broken file references found |
| 10 | Memory Notes format | ✅ PASS | Has `### Memory Notes (For Workflow-Final Persistence)` section with Learnings, Patterns, Verification, Deferred |

**Verdict: PASS** — all 10 criteria satisfied.

---

### 6. integration-verifier.md — **PASS**

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: yellow` |
| 4 | Correct `tools` list | ✅ PASS | `Read, Bash, Grep, Glob, Skill, LSP, WebFetch` — no Edit/Write. READ-ONLY agent correctly lacks mutation tools. |
| 5 | CONTRACT envelope format | ✅ PASS | `CONTRACT {"s":"PASS","b":false,"cr":0}` — present in output template. Explicitly states: "Line 1 envelope IS the contract. No separate YAML block." |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated as a named rule; inherited via `cc10x:agent-common` preamble. The output format implies single response. |
| 7 | Memory First protocol | ✅ PASS | Inherited via `cc10x:agent-common` preamble |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:verification` — both exist |
| 9 | Broken references | ✅ PASS | References `live_harness_runner.py` which exists at `tools/live_harness_runner.py` |
| 10 | Memory Notes format | ✅ PASS | Has `### Memory Notes` section with Learnings, Patterns, Verification (missing Deferred — minor) |

**Verdict: PASS** — all core criteria satisfied.

---

### 7. doc-syncer.md — **PASS** (with observations)

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ✅ PASS | `effort: medium` |
| 3 | Correct `color` field | ✅ PASS | `color: cyan` |
| 4 | Correct `tools` list | ✅ PASS | Has Edit/Write — doc-syncer updates documentation files, not read-only |
| 5 | CONTRACT envelope format | ⚠️ OBSERVATION | Uses YAML `Router Contract (MACHINE-READABLE)` block, not `CONTRACT {json}` envelope |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated in body; inherited via `cc10x:agent-common` preamble |
| 7 | Memory First protocol | ✅ PASS | Has explicit `## Memory First (CRITICAL — DO NOT SKIP)` section reading all 3 memory files + `CLAUDE.md` |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:diff-driven-docs`, `cc10x:verification` — all exist. Body references `cc10x:diff-driven-docs` skill which exists. |
| 9 | Broken references | ✅ PASS | `docs/decisions/` and `docs/` are pattern globs |
| 10 | Memory Notes format | ⚠️ OBSERVATION | Has `MEMORY_NOTES` in YAML contract (learnings, patterns, verification, deferred) — no `### Memory Notes` section |

**Verdict: PASS** — core frontmatter and skill loading are correct. Uses `model: haiku` (other agents use `model: inherit`) — not a violation, just a difference.

---

### 8. plan-gap-reviewer.md — **FAIL**

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ❌ **FAIL** | **No `skills:` field in frontmatter at all.** Does not load `cc10x:agent-common`. Frontmatter is: `name`, `description`, `model`, `color`, `effort`, `tools` — no `skills:` list. |
| 2 | Correct `effort` field | ✅ PASS | `effort: high` |
| 3 | Correct `color` field | ✅ PASS | `color: purple` |
| 4 | Correct `tools` list | ✅ PASS | `Read, Grep, Glob, LSP` — no Edit/Write/Bash/Skill. READ-ONLY agent correctly lacks mutation tools. Note: also lacks `Bash` and `Skill` tools, which is intentional for anti-anchoring (no memory access, no skill loading). |
| 5 | CONTRACT envelope format | ✅ PASS | `CONTRACT {"s":"PASS","b":false,"cr":0}` — present in output template |
| 6 | SINGLE FINAL RESPONSE RULE | ✅ PASS | Has `**Single final response rule**` in process step 0 (inlined, not inherited) |
| 7 | Memory First protocol (anti-anchoring variant) | ⚠️ OBSERVATION | Deliberately reads NO memory at all: "Do NOT load `.cc10x/*.md`". This is the extreme anti-anchoring variant. The agent-common preamble notes: "if your agent doc deliberately narrows this protocol (anti-anchoring reviewers such as `code-reviewer` skip `activeContext.md`; `plan-gap-reviewer` reads no memory at all), follow the agent doc". So this is acknowledged as intentional. **However**, since it doesn't load `cc10x:agent-common`, this narrowing protocol is self-contained, not inherited. |
| 8 | Correct skills references | ❌ **FAIL** | No `skills:` list at all. No skills loaded. Body makes no skill references. |
| 9 | Broken references | ✅ PASS | No broken file references found |
| 10 | Memory Notes format | ❌ **FAIL** | No `### Memory Notes` section in output template. Output template has: Summary, Blocking Findings, Findings, Planner Action, Task Status — no Memory Notes. This is consistent with the anti-anchoring design (reads no memory, writes no memory) but violates the criterion. |

**Verdict: FAIL** — Missing `skills:` frontmatter (criterion 1), no skills loaded (criterion 8), no Memory Notes format (criterion 10). The anti-anchoring design (no memory) is acknowledged in agent-common as intentional, but the missing `skills:` field means the agent doesn't load the shared preamble at all, missing the CONTRACT envelope rules, SINGLE FINAL RESPONSE RULE, Shell Safety, Spirit vs Letter, and Untrusted Input Handling sections from agent-common. The agent does inline its own "Single final response rule" and CONTRACT envelope, so it partially compensates.

**Severity: MEDIUM** — The agent functions correctly by inlining the rules it needs, but it's inconsistent with the system design where ALL agents should load `cc10x:agent-common`.

---

### 9. researcher.md — **FAIL**

| # | Criterion | Verdict | Evidence |
| --- | ----------- | --------- | ---------- |
| 1 | Loads `cc10x:agent-common` | ✅ PASS | `skills:` list includes `cc10x:agent-common` |
| 2 | Correct `effort` field | ❌ **FAIL** | **No `effort` field in frontmatter.** Frontmatter has: `name`, `description`, `model`, `color`, `tools`, `skills` — no `effort`. |
| 3 | Correct `color` field | ✅ PASS | `color: orange` |
| 4 | Correct `tools` list | ✅ PASS | `Read, Write, Edit, Bash, WebFetch, WebSearch, TaskUpdate` — has Write/Edit which is correct (writes research files). Note: lacks `Grep`, `Glob`, `Skill`, `LSP` tools — researcher doesn't need code search tools, and `Skill` absence means it can't invoke skills directly (loads them via frontmatter preamble only). |
| 5 | CONTRACT envelope format | ⚠️ OBSERVATION | Uses YAML `Router Contract (REQUIRED)` block, not `CONTRACT {json}` envelope |
| 6 | SINGLE FINAL RESPONSE RULE | ⚠️ OBSERVATION | Not explicitly stated in body; inherited via `cc10x:agent-common` preamble |
| 7 | Memory First protocol | ✅ PASS | Inherited via `cc10x:agent-common` preamble |
| 8 | Correct skills references | ✅ PASS | `cc10x:agent-common`, `cc10x:mcp-cli` — both exist |
| 9 | Broken references | ✅ PASS | `docs/research/` is a pattern |
| 10 | Memory Notes format | ⚠️ OBSERVATION | Has `MEMORY_NOTES` in YAML contract (learnings, verification only) — no `### Memory Notes` section. Missing `patterns` and `deferred` fields. |

**Verdict: FAIL** — Missing `effort` field (criterion 2). All other criteria pass or have observations shared with other builder agents.

**Severity: LOW** — The missing `effort` field is a frontmatter gap. The agent will likely default to some effort level, but it should be explicit for consistency.

---

## Summary Table

| Agent | #1 agent-common | #2 effort | #3 color | #4 tools | #5 CONTRACT | #6 SFR | #7 Memory | #8 skills | #9 refs | #10 MemNotes | Verdict |
| ------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--: |
| planner | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | **PASS** |
| bug-investigator | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | **PASS** |
| component-builder | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | **PASS** |
| code-reviewer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **PASS** |
| silent-failure-hunter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **PASS** |
| integration-verifier | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | **PASS** |
| doc-syncer | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | **PASS** |
| plan-gap-reviewer | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ❌ | **FAIL** |
| researcher | ✅ | ❌ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | **FAIL** |

**Legend:** ✅ = Pass | ❌ = Fail | ⚠️ = Observation (design inconsistency, not a hard failure)

---

## Issues Found

### FAIL — plan-gap-reviewer.md: Missing `skills:` frontmatter

- **Severity:** MEDIUM
- **File:** `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/plan-gap-reviewer.md`
- **Issue:** No `skills:` field in YAML frontmatter. Agent does not load `cc10x:agent-common`. Consequently does not inherit: CONTRACT envelope rules, SINGLE FINAL RESPONSE RULE (preamble version), Shell Safety, Spirit vs Letter, Untrusted Input Handling.
- **Impact:** Agent inlines its own CONTRACT envelope and "Single final response rule", so it partially compensates. But it's inconsistent with the system design where ALL agents should load `cc10x:agent-common`.
- **Also missing:** No Memory Notes format in output template (by design — reads no memory).

### FAIL — researcher.md: Missing `effort` field

- **Severity:** LOW
- **File:** `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/agents/researcher.md`
- **Issue:** No `effort` field in YAML frontmatter. All other 8 agents have explicit `effort` values.
- **Impact:** Agent may default to an unspecified effort level. Should be explicit for consistency.

### OBSERVATION — Builder agents use YAML contract instead of CONTRACT envelope

- **Severity:** INFORMATIONAL
- **Files:** planner.md, bug-investigator.md, component-builder.md, doc-syncer.md, researcher.md
- **Issue:** These 5 agents use a YAML `Router Contract (MACHINE-READABLE)` block instead of the `CONTRACT {json}` envelope format defined in agent-common. The 4 reviewer/verifier agents (code-reviewer, silent-failure-hunter, integration-verifier, plan-gap-reviewer) correctly use the CONTRACT envelope.
- **Impact:** The agent-common preamble defines the CONTRACT envelope as "Line 1 of your final response" for all agents. The builder agents deviate from this. This appears to be a deliberate design choice (builder contracts are richer YAML, reviewer contracts are quick-parse envelopes), but it creates an inconsistency with the shared preamble's contract format definition.

### OBSERVATION — Builder agents embed MEMORY_NOTES in YAML, not as `### Memory Notes` section

- **Severity:** INFORMATIONAL
- **Files:** planner.md, bug-investigator.md, component-builder.md, doc-syncer.md, researcher.md
- **Issue:** These agents embed `MEMORY_NOTES` as a YAML block within their Router Contract, rather than emitting a `### Memory Notes (For Workflow-Final Persistence)` section as defined in agent-common. The reviewer agents correctly use the section format.
- **Impact:** The router may need to parse both formats. The YAML approach is machine-readable but doesn't match the section-based format in agent-common.

### OBSERVATION — researcher.md MEMORY_NOTES missing `patterns` and `deferred` fields

- **Severity:** INFORMATIONAL
- **File:** researcher.md
- **Issue:** YAML `MEMORY_NOTES` has only `learnings` and `verification` fields. Missing `patterns` and `deferred` that other agents include.
- **Impact:** Minor — research findings may not contribute to patterns.md or deferred tracking.

---

## Residual Risks

1. **plan-gap-reviewer without agent-common:** If agent-common is updated with new shared rules (e.g., new output format, new safety protocol), plan-gap-reviewer will NOT inherit them since it doesn't load the preamble. This creates a maintenance burden — any preamble change must be manually synced to plan-gap-reviewer.

2. **CONTRACT format inconsistency:** The router must handle two different contract formats (JSON envelope for reviewers, YAML block for builders). If the router's parsing logic changes, one format could break silently.

3. **researcher missing effort:** Without an explicit effort field, the agent's resource allocation is undefined. This could lead to inconsistent behavior across invocations.
