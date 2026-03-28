---
name: building-cc10x
description: "Systematic methodology for improving CC10x by analyzing external reference repos, extracting prompt engineering patterns, harmony-mapping them against CC10x DNA, and surgically integrating only NATIVE patterns. Use when: analyzing a reference repo, comparing against cc10x, extracting patterns, running a harmony integration, stealing patterns, improving cc10x orchestration, cloning a reference, running a DNA fingerprint, prompt engineering uplift, multi-repo analysis, or any mention of improving cc10x from external sources. This is the proven pipeline behind v10.1.14 (29 patterns from 11 repos), v10.1.15 (4 audit-only hooks), and v10.1.16 (10 patterns from BMAD-METHOD)."
user-invocable: true
---

# Building CC10x — Reference Repo Harmony Integration

This skill encodes a **battle-tested methodology** for systematically improving CC10x by learning from external reference repos. Every step has been proven across 3 releases. The pipeline produces perfect harmony — every addition feels natively built, never patched.

**Track record:**
- v10.1.14: 396 raw patterns → 56 mapped → 29 certified NATIVE (7.3% acceptance rate), 11 repos, 10 files, +109 lines
- v10.1.15: 25 hook events researched → 6 proposed → 4 certified safe (dropped 2 that COMPETED with router), 13 files, +330 lines
- v10.1.16: ~40 patterns → 23 NATIVE → 10 certified after cross-layer dedup, 14 files, +95 lines

---

## The Pipeline (7 Phases)

```
Phase 1: Clone + Parallel Extraction ──→ Raw patterns from target repo
Phase 2: CC10x DNA Fingerprint ────────→ Current state characteristics
Phase 3: 3 Parallel Harmony Mappers ───→ NATIVE/ACCEPTABLE/RISKY per layer
Phase 4: Cross-Layer Dedup ────────────→ Certified pattern list
Phase 5: Surgical Plan ───────────────→ Exact FIND/REPLACE blocks
Phase 6: Execute ─────────────────────→ Read → Edit → Verify
Phase 7: Version Bump + Release ──────→ Commit → Push → Audit
```

Every phase uses parallel sub-agents where possible. Sequential only when there are data dependencies.

---

### Phase 1: Clone + Parallel Extraction

**Goal:** Get the raw material. Deep-read the target repo and capture every pattern worth evaluating.

**Steps:**
1. Clone the target repo to `ref-(dont-read-unless-specificly-mentioned)/`
2. Launch **2 parallel agents:**

| Agent | Type | Task | Thoroughness |
|-------|------|------|-------------|
| **Target Extractor** | Explore (very thorough) | Read EVERY file in the target repo. Capture: prompt engineering patterns, orchestration patterns, memory/context management, quality gates, safety rails, novel ideas. Be EXHAUSTIVE. | Read every .md, .js, .py, .yaml, .json |
| **CC10x DNA Fingerprint** | Explore (thorough) | Read current CC10x state: router SKILL.md, 3-4 agent files, 3-4 skill files, hooks.json, config. Produce DNA fingerprint. | Read `references/dna-fingerprint.md` for the template |

**Output:** Two comprehensive reports — one describing what the target repo does, one describing CC10x's current DNA.

**Prompt template for Target Extractor:**
> Very thorough exploration of {REPO_PATH}. Read ALL files. For EVERY file, capture: (1) exact prompt engineering patterns (voice, structure, formatting), (2) orchestration patterns (agent chains, routing, state), (3) memory/context management, (4) quality gates and verification, (5) safety rails, (6) novel ideas not commonly seen. Be EXHAUSTIVE.

**Prompt template for CC10x DNA Fingerprint:**
> Read `references/dna-fingerprint.md` for the DNA template, then read the current CC10x files and produce an updated fingerprint. Focus on: voice, formatting, rule expression, structural patterns, safety patterns, context management, quality gates, what feels NATIVE vs what would feel PATCHED ON.

---

### Phase 2: CC10x DNA Fingerprint

The DNA fingerprint is the filter that determines what passes through. It captures the defining characteristics that make CC10x feel like CC10x.

Read `references/dna-fingerprint.md` for the full current fingerprint. Key dimensions:

| Dimension | CC10x DNA | Foreign Signal |
|-----------|-----------|---------------|
| Voice | Imperative with consequence. MUST/NEVER first, then justify. | Conversational, suggestive, passive |
| Formatting | Pipe tables, YAML contracts, numbered steps, code blocks as specs | Prose paragraphs, emoji, decorative headers |
| Rules | Three-tier: Hard Rules (CRITICAL), Gates (conditional), Heuristics ([EASY TO MISS]) | Flat lists, no severity, no consequences |
| Safety | Fail-closed gates, circuit breakers, proof reconciliation triple | Advisory warnings, optional checks |
| Context | Explicit handoff via structured scaffold. Memory is source of truth. | Conversation history leakage, implicit context |
| Quality | Three verification levels. Evidence before claims. | Prose-only verdicts, "looks good" |
| Output | Single-response. CONTRACT envelope. YAML Router Contract. | Multi-turn conversation, personality |

**The DNA fingerprint is NOT static.** Regenerate it before every integration because CC10x evolves with each release.

---

### Phase 3: 3 Parallel Harmony Mappers

**Goal:** Rate every extracted pattern as NATIVE, ACCEPTABLE, or RISKY — from three independent perspectives.

Launch **3 parallel agents**, one per CC10x layer:

| Mapper | Reads | Evaluates Against | Key Question |
|--------|-------|-------------------|-------------|
| **Agent Layer** | All CC10x agent .md files | Agent DNA (single-response, contract-producing, posture not persona) | Would this pattern feel native in an agent file? |
| **Skill Layer** | All CC10x skill SKILL.md files | Skill DNA (monolithic, tables, imperative, no step-files) | Would this pattern feel native in a skill file? |
| **Router Layer** | Router SKILL.md (read in chunks if >2000 lines) | Router DNA (sole authority, fail-closed, deterministic) | Does this strengthen the router without competing? |

**Each mapper must output this table:**

```
| # | Pattern | Rating | Justification | Target File | Surgical Change |
```

**Rating criteria — Read `references/harmony-rating.md` for full details:**

| Rating | Meaning | Action |
|--------|---------|--------|
| **NATIVE** | Fits CC10x DNA perfectly. Feels like it was always there. | Accept — specify exact target file and surgical change |
| **ACCEPTABLE** | Could work but feels slightly foreign. | Drop — perfect harmony means no compromises |
| **RISKY** | Conflicts with CC10x architecture or philosophy. | Reject — explain the conflict |

**Mapper prompt template:**
> You are a CC10x HARMONY MAPPER for the {LAYER} LAYER. Read the CC10x {layer} files at {paths}. Then evaluate each extracted pattern for {layer} fit. For EACH pattern, produce a table row with: #, Pattern, Rating (NATIVE/ACCEPTABLE/RISKY), Justification, Target File, Surgical Change. Be RUTHLESS — only NATIVE survives.

Include the full DNA fingerprint in each mapper's prompt so they have the standard to judge against.

---

### Phase 4: Cross-Layer Dedup + Certified List

**Goal:** Merge results from all 3 mappers. Deduplicate patterns rated NATIVE by multiple layers. Detect conflicts.

This phase runs **inline** (not as a sub-agent) because it requires judgment:

1. **Collect all NATIVE patterns** from all 3 mappers
2. **Identify cross-layer overlaps** — same pattern rated NATIVE by 2-3 mappers targeting different files. These are COMPLEMENTARY (different enforcement points for the same principle). Merge into single certified entries.
3. **Detect conflicts** — same pattern rated NATIVE by one mapper and RISKY by another. The RISKY rating wins (conservative). Investigate why the conflict exists.
4. **Produce the Certified List** — final table of patterns that survived, with exact target files and surgical changes.

**Output format:**

```
| # | Certified Pattern | Layers | Target Files | Type |
```

**Key rules:**
- If a pattern requires creating new files → flag it as a separate initiative, not part of this release
- If a pattern touches YAML contracts, state machine transitions, or workflow graphs → REJECT regardless of rating
- If a pattern adds personality, emoji, conversational tone, or user interaction within agents → REJECT

---

### Phase 5: Surgical Plan

**Goal:** Build exact FIND/REPLACE blocks for every certified pattern. This is the specification that Phase 6 executes.

**Steps:**
1. Launch **parallel read agents** to get exact text at every insertion point (line numbers, verbatim text, 5-10 lines of surrounding context)
2. Write the plan with this structure for each file:

```
### FILE N: `path/to/file.md`

#### Edit Na — Pattern Name (~line NNN)

**FIND:**
(exact text to match)

**REPLACE:**
(exact replacement text)
```

**Critical plan rules:**
- **Bottom-up editing** — when multiple edits target the same file, order them from highest line number to lowest. This preserves line numbers for subsequent edits.
- **Unique FIND blocks** — each FIND must be unique in the file. If not unique, include more surrounding context.
- **Version bumps in separate batch** — version files are simple and go last.
- **Include execution order** — group edits into batches: independent edits in parallel, dependent edits sequential.

**Plan must include:**
- Files Modified table (count + list)
- Execution Order (batched)
- Verification section (what to check after)
- "What Was NOT Changed" safety section

---

### Phase 6: Execute

**Goal:** Apply all edits. The execution follows strict rules learned from past failures.

**Execution rules (learned from breaking things):**

| Rule | Why | Learned From |
|------|-----|-------------|
| **Read every file before editing** | Edit tool fails with "File has not been read yet" error | v10.1.14 Batch 1 failure — all 5 edits rejected |
| **Read in chunks if >2000 lines** | Claude Code silently truncates at 2000 lines. Run `wc -l` first. | Router SKILL.md is >1100 lines |
| **Bottom-up within same file** | Edits at lower line numbers shift lines above. Higher edits first preserves line numbers. | Multiple experiences |
| **Parallel edits across files** | Independent files can be edited simultaneously | Batches 3-4 pattern |
| **Sequential edits within same file** | Each edit changes line numbers for subsequent edits | Router 6-edit sequence |
| **Verify FIND block matches** | FIND text must be exact — whitespace, formatting, everything. Copy from Read output, not from memory. | Code-reviewer scope guard mismatch (v10.1.14) |
| **Re-stage after pre-commit hooks** | Black/prettier may reformat. Re-stage the formatted files. | v10.1.15 black auto-format |

**Batch execution pattern:**
```
Batch 1: Read all target files (parallel)
Batch 2: Edit primary file (sequential, bottom-up)
Batch 3: Edit agent files (parallel)
Batch 4: Edit skill files (parallel)
Batch 5: Version bumps (parallel)
```

---

### Phase 7: Version Bump + Release

**Version files to update (ALWAYS all of these):**

| File | Field |
|------|-------|
| `plugins/cc10x/.claude-plugin/plugin.json` | `"version"` |
| `.claude-plugin/marketplace.json` | `"version"` (TWO instances — metadata AND plugins[0]) |
| `CHANGELOG.md` | New entry before previous version |
| `docs/router-invariants.md` | Status note version + date |
| `README.md` | `**Current version:**` line |

**CHANGELOG entry format:**
```markdown
## [X.Y.Z] - YYYY-MM-DD

### {Source} — {count} certified prompt engineering patterns

{One-line summary}. All prompt-text additions. Zero YAML contracts changed. Zero new files.

#### Added
- **Pattern Name:** Description of what it does and why.
{repeat for each pattern}

#### Changed
- **Router SKILL.md:** N surgical additions (Sections X, Y, Z)
- **N agent files:** list
- **N skill files:** list
```

**Verification suite (run ALL of these):**
```bash
cd plugins/cc10x
python3 scripts/cc10x_harness_audit.py          # Must say OK
python3 scripts/cc10x_workflow_replay_check.py   # Must say OK
python3 scripts/cc10x_reference_benchmark.py     # Must show 33/33
```

**Content grep checks** — for every pattern added, grep to confirm it exists in the target file.

**Commit pattern:**
```bash
git add {specific files}
git commit -m "Release X.Y.Z {source} prompt engineering integration"
git push origin main
```

---

## Safety Rails (Inviolable)

These are the boundaries that must NEVER be crossed, regardless of how attractive a pattern looks:

| Boundary | Why |
|----------|-----|
| Zero YAML contract field changes | Contracts are the machine-readable API between router and agents. Changing them breaks the entire system. |
| Zero state machine transitions changed | The phase cursor model is the heartbeat of workflow execution. |
| Zero workflow graph alterations | Agent chains and dispatch tables are calibrated. Changing them cascades. |
| Zero new task metadata fields | Task metadata is the scoped recovery mechanism. New fields must go through full design. |
| Hooks SUPPORT the router, never COMPETE | Hooks that inject context or validate router output create a parallel control plane. Only persistence/telemetry hooks are safe. |
| Router is sole orchestration authority | No agent, hook, or skill may make routing decisions. Period. |
| All additions are prompt-text only | No new Python dependencies, no new runtime behavior, no new file formats. |
| No deletions of existing text | Every integration is purely additive. Existing behavior must not change. |

**The Challenge Test:** When uncertain about a pattern, ask: "Does this SUPPORT the router or COMPETE with it?" If it creates a second source of truth, a second decision point, or a second context injection path — it competes. Drop it.

---

## The Harmony Philosophy

CC10x is like Neuralink — many moving pieces in perfect harmony. Every new addition must feel like it was always there. The acceptance rate should be low (5-15%). If you're accepting >20% of raw patterns, you're not being ruthless enough.

**NATIVE means:** A CC10x developer reading the file would not be able to tell where the original text ends and the new text begins. Same voice, same formatting, same severity model, same evidence requirements.

**The bar is intentionally high.** It is better to ship 5 NATIVE patterns than 20 ACCEPTABLE ones. Acceptable patterns accumulate into drift. NATIVE patterns compound into strength.

Read `references/harmony-rating.md` for detailed rating criteria with examples from actual releases.

---

## Quick Reference: Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| "File has not been read yet" | Edit tool rejects all edits | Read ALL files before any edit |
| FIND block doesn't match | Edit fails silently or matches wrong location | Copy exact text from Read output, not from plan |
| marketplace.json double version | Only one instance updated | Provide unique surrounding context for each FIND |
| README version stale | Harness audit fails | Always include README.md in version bump batch |
| Pre-commit reformats files | Commit fails or includes unexpected changes | Re-stage after black/prettier runs |
| Hook competes with router | Creates parallel control plane | Drop the hook. Only persistence/telemetry is safe. |
| Pattern feels foreign | Breaks the "could not tell where new text begins" test | Rate as ACCEPTABLE, not NATIVE. Drop it. |
| Router SKILL.md truncated | Read only returns first 2000 lines | Run `wc -l` first, read in chunks with offset/limit |

---

## When to Use This Skill

Invoke this skill when ANY of these are true:
- You have a reference repo to analyze for CC10x improvements
- You want to compare CC10x against another agent framework
- You're planning a prompt engineering uplift release
- You want to extract patterns from external sources
- Someone says "what can we learn from X?"
- A new version of an existing reference repo is available
- You want to run the full harmony integration pipeline

This skill is NOT for:
- Day-to-day CC10x usage (use cc10x-router instead)
- Bug fixes or feature work within CC10x (use cc10x-router)
- Hook implementation (use cc10x-orchestration-safety instead)
