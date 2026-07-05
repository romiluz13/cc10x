# Stale-Reference Sweep — cc10x Codebase (plugins/cc10x/ + keynote.html)

**Scope:** Every `.md`, `.json`, `.py` file under `plugins/cc10x/`, plus `keynote.html` at repo root.
**Method:** `grep -rn` for each old name across all three extensions; manual context inspection of every hit.
**Verdict:** 8 stale references found — all in two tool/audit scripts. Zero stale references in agent prompts, skill text, hook scripts, router SKILL.md, or keynote.html.

---

## Summary Table

| # | File | Line | Stale Text | Category | Severity | Executing Code? |
| --- | ------ | ------ | ------------ | ---------- | ---------- | ----------------- |
| 1 | tools/worldclass_benchmark.py | 268 | `"verification-before-completion"` | Old skill name | Medium | Yes (benchmark tool) |
| 2 | tools/worldclass_benchmark.py | 729 | `"verification-before-completion"` | Old skill name | Medium | Yes (benchmark tool) |
| 3 | tools/worldclass_benchmark.py | 437 | `"plugins/cc10x/skills/debugging-patterns/SKILL.md"` | Old skill path | Medium | Yes (benchmark tool) |
| 4 | tools/worldclass_benchmark.py | 451 | `"plugins/cc10x/skills/architecture-patterns/SKILL.md"` | Old skill path | Medium | Yes (benchmark tool) |
| 5 | tools/worldclass_benchmark.py | 346-347 | Comment: "The standalone failure-hunter agent is retired; its hunting duty is consolidated into code-reviewer Pass 1b." | Old concept (Pass 1b + retired hunter) | Medium | Yes (benchmark tool) |
| 6 | tools/worldclass_benchmark.py | 352 | `"Pass 1b: Silent Failure Scan"` | Old concept (Pass 1b) | Medium | Yes (benchmark tool) |
| 7 | tools/worldclass_benchmark.py | 353 | `"silent-failure hunting is consolidated into the reviewer"` | Old concept | Low | Yes (benchmark tool) |
| 8 | tools/harness_audit.py | 530 | `and "### session-memory" not in prompt_surface_inventory` | Old skill name | Low | Yes (audit script) |

---

## Detailed Findings

### Finding 1 — worldclass_benchmark.py:268 — Old skill name in scenario weak_patterns

```
weak_patterns=(
    "verification-loop",
    "independent verification",
    "verification-before-completion",   # ← stale
),
```

**Context:** `Scenario("verification_fail_closed", ...)` weak_patterns tuple. The benchmark scans repo text for these needles to score the scenario. The skill was renamed to `verification` in v12.1.0, so this string will never match current code.
**Impact:** Scenario may score lower than it should because the old needle can't be found. Should be `"verification"` (the new skill name) or removed.
**Classification:** Executing code (benchmark measurement tool, not orchestration runtime).

### Finding 2 — worldclass_benchmark.py:729 — Old skill name in harness signal detection

```python
hits["fail_closed_verification"] = any(
    x in lower
    for x in (
        "expected vs actual",
        "scenarios_total",
        "verification-before-completion",   # ← stale
        "blocking fail",
        "convergence_state",
    )
)
```

**Context:** `detect_harness_signals()` function. Scans the repo corpus for fail-closed verification signals. The old skill name won't appear in current code.
**Impact:** Signal detection may miss the current `verification` skill, undercounting the fail-closed-verification signal. Should be `"verification"` or `"cc10x:verification"`.
**Classification:** Executing code (benchmark signal detection).

### Finding 3 — worldclass_benchmark.py:437 — Old skill path in DeltaRule

```python
DeltaRule(
    "plugins/cc10x/skills/debugging-patterns/SKILL.md",   # ← stale path
    "internal-skill",
    (
        ("advisory", "debugging patterns are advisory instead of authoritative"),
        ("same signature nearby", "debugging guidance includes nearby duplicate scan"),
    ),
),
```

**Context:** `DELTA_RULES` tuple. The `build_delta_register()` function (line 869) does `current_path = ROOT / rule.path` and checks `current_path.exists()`. The path `skills/debugging-patterns/` does NOT exist — it's now `skills/debugging/`.
**Impact:** `current_path.exists()` returns `False` → `current_text = ""` → no needles match → DeltaRule produces zero deltas. This is a **dead/broken rule** that silently contributes nothing.
**Fix:** Path should be `"plugins/cc10x/skills/debugging/SKILL.md"`.
**Classification:** Executing code (benchmark delta register).

### Finding 4 — worldclass_benchmark.py:451 — Old skill path in DeltaRule

```python
DeltaRule(
    "plugins/cc10x/skills/architecture-patterns/SKILL.md",   # ← stale path
    "internal-skill",
    (
        ("advisory", "architecture patterns are advisory instead of authoritative"),
        ("approved plan/design doc", "approved design outranks architecture heuristics"),
    ),
),
```

**Context:** Same as Finding 3. Path `skills/architecture-patterns/` does NOT exist — it's now `skills/architecture/`.
**Impact:** Dead/broken DeltaRule — produces zero deltas.
**Fix:** Path should be `"plugins/cc10x/skills/architecture/SKILL.md"`.
**Classification:** Executing code (benchmark delta register).

### Finding 5 — worldclass_benchmark.py:346-347 — Stale comment (retired hunter + Pass 1b)

```python
DeltaRule(
    # The standalone failure-hunter agent is retired; its hunting
    # duty is consolidated into code-reviewer Pass 1b.
    "plugins/cc10x/agents/code-reviewer.md",
    "hunter",
    ...
```

**Context:** Comment above the "hunter" DeltaRule. Two stale claims:

1. "The standalone failure-hunter agent is retired" — **FALSE**. `agents/failure-hunter.md` exists and is active. The router dispatches it as a separate parallel agent (confirmed in `SKILL.md:578-579`, `build-workflow.md:120`, `code-reviewer.md:210`).
2. "duty is consolidated into code-reviewer Pass 1b" — **FALSE**. Pass 1b was removed; failure-hunter is now a separate parallel agent.

**Impact:** Misleading comment that documents a state that no longer exists. The DeltaRule itself (Finding 6) is also broken.
**Fix:** Comment should reflect that failure-hunter is a standalone parallel agent, and the DeltaRule should point at `agents/failure-hunter.md` instead of `code-reviewer.md`.
**Classification:** Executing code (benchmark delta register comment).

### Finding 6 — worldclass_benchmark.py:352 — Stale needle "Pass 1b: Silent Failure Scan"

```python
(
    "Pass 1b: Silent Failure Scan",                          # ← stale needle
    "silent-failure hunting is consolidated into the reviewer",  # ← stale description
),
```

**Context:** `feature_needles` for the "hunter" DeltaRule targeting `code-reviewer.md`. Confirmed via grep: `code-reviewer.md` does NOT contain "Pass 1b" or "Silent Failure Scan" anywhere. The other two needles in this rule ("Do not self-activate internal CC10X skills" and "Zero-Finding Gate") DO exist in `code-reviewer.md` (lines 47 and 116 respectively).
**Impact:** One of three needles never matches → that delta description never fires. The rule partially works but encodes a stale concept.
**Fix:** Replace the "hunter" DeltaRule to target `agents/failure-hunter.md` with needles from that file (e.g., the red-flags table reference, scan-coverage mandate).
**Classification:** Executing code (benchmark delta register).

### Finding 7 — worldclass_benchmark.py:353 — Stale description string

Paired with Finding 6 (same tuple entry). The description `"silent-failure hunting is consolidated into the reviewer"` encodes the removed consolidation concept. Low severity on its own since it's just a label, but it documents a false architecture claim.
**Classification:** Executing code (benchmark delta register description).

### Finding 8 — harness_audit.py:530 — Old skill name in fallback check

```python
if (
    "### memory-and-handoff" not in prompt_surface_inventory
    and "### session-memory" not in prompt_surface_inventory   # ← stale fallback
):
    errors.append("prompt surface inventory missing memory-and-handoff entry")
```

**Context:** Audit check that the prompt surface inventory contains the memory-and-handoff entry. The logic errors only if BOTH the new name AND old name are absent. The `### session-memory` check is a legacy tolerance shim — if the inventory still has the old `### session-memory` heading, the error is suppressed.
**Impact:** Low. If the inventory correctly uses `### memory-and-handoff`, no error fires and the stale check is dead code. If the inventory still has `### session-memory` (stale), the error is incorrectly suppressed, masking a real problem. The fallback should be removed so the audit fails on stale inventory entries.
**Fix:** Remove the `and "### session-memory" not in prompt_surface_inventory` clause.
**Classification:** Executing code (audit script).

---

## Items Checked and Found CLEAN

| Search Term | Result in plugins/cc10x/ |
| ------------- | -------------------------- |
| `planning-patterns` | No matches |
| `frontend-patterns` | No matches |
| `code-review-patterns` | No matches |
| `silent-failure-hunter` (agent name) | No matches (the `references/silent-failure-red-flags.md` file is about the pattern, correctly excluded) |
| `web-researcher` | No matches |
| `github-researcher` | No matches |
| `RESIDUAL_FINDINGS` | No matches |
| `residual-review-findings` | No matches |
| `LEGACY` next to `hunter` in artifact policy | Clean — `workflow-artifact-and-hook-policy.md:87` shows `hunter` (ACTIVE — the standalone failure-hunter agent's evidence). No LEGACY label. |
| `Pass 1b` / `Pass 1B` in .md files | No matches (only in `worldclass_benchmark.py`) |
| `silent-failure` (pattern concept) | 3 matches, all describe the failure pattern, not the old agent name — OK |

### keynote.html — CLEAN

Searched for all old skill names, old agent names, `Pass 1b`, `RESIDUAL_FINDINGS`, `residual-review-findings`, and `LEGACY`. **Zero stale references found.**

### Current names verified to exist

All renamed skills confirmed present at their new paths:

- `skills/verification/SKILL.md` ✓
- `skills/debugging/SKILL.md` ✓
- `skills/architecture/SKILL.md` ✓
- `skills/frontend/SKILL.md` ✓
- `skills/code-review/SKILL.md` ✓
- `skills/planning/SKILL.md` ✓
- `skills/memory-and-handoff/SKILL.md` ✓
- `agents/failure-hunter.md` ✓

---

## Out-of-Scope Notes (Historical Documentation)

The task scope was `plugins/cc10x/` + `keynote.html`. For completeness, old names also appear in `docs/` historical files (research notes, old plans, handoff docs dated 2026-06-17 and 2026-07-02). These are historical artifacts written when the old names were current — equivalent to CHANGELOG entries and OK to keep. No action needed unless the parent wants a docs/ sweep too.

---

## Residual Risks

1. **worldclass_benchmark.py is the only file with material stale refs.** It's a benchmark/measurement tool, not part of the orchestration runtime. The stale DeltaRules (Findings 3, 4, 6) silently produce no output, so benchmark reports may undercount cc10x's delta advantages without any error signal. The stale signal needles (Findings 1, 2) may cause lower scenario scores.

2. **harness_audit.py:530** tolerates a stale `### session-memory` heading in the prompt surface inventory, which could mask a real audit failure if the inventory regresses to the old name.

3. **No stale references in agent prompts, skill text, hook scripts, or the router.** The orchestration runtime is clean — these stale refs cannot affect live workflow behavior.
