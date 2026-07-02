---
name: codebase-hygiene
description: |
  Two-mode skill: (1) find semantic duplicates — functions doing the same thing
  under different names, invisible to copy-paste detectors; (2) deepen shallow
  modules — thin wrappers and pass-through layers that spread complexity.
  Advisory and read-only; changes route through BUILD with full gates.
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Codebase Hygiene (Duplicate Detection + Module Deepening)

Advisory and read-heavy. Diagnoses and proposes; does not refactor. Any actual change goes through BUILD with full gates.

## Mode: DUPLICATE DETECTION

Semantic duplicates: functions serving the same purpose but implemented independently under different names. Copy-paste detectors catch syntactic duplicates; this finds "same intent, different implementation."

### Method

1. **Extract catalog** — Grep/Glob for exported functions. Record `name | file:line | signature`.
2. **Categorize by domain** (cheap tier) — validation, formatting, path manipulation, HTTP shaping, date handling. Mechanical bucketing to shrink comparison space.
3. **Drop categories with <3 functions** — can't hide a meaningful duplication pattern.
4. **Detect duplicates per category** (capable tier) — read implementations, decide which share intent. **Never use cheap tier for detection** — it anchors on names and rubber-stamps "these look different."
5. **Emit findings** — group by confidence, highest first. Each finding: what is duplicated, why it matters, the fix, `file:line` evidence. Route through code-reviewer finding contract.

### High-Risk Zones

| Zone | Why it duplicates |
| ------ | ------------------- |
| `utils/`, `helpers/`, `lib/` | Catch-all dumping grounds |
| Validation code | "Is this a valid email/id/url" rewritten per feature |
| Error formatting | Every module invents its own Error → string |
| Path manipulation | Join/normalize/relativize reimplemented |
| String formatting | Truncate, slugify, titlecase, pad re-rolled |
| Date formatting | Parse/format/diff scattered |
| API response shaping | Envelope/pagination/error-body copied per endpoint |

### Consolidation Discipline

Never delete a duplicate until all three hold:

1. **Survivor has tests** — pick the implementation with real coverage. If neither has tests, write the test against the chosen survivor first.
2. **All callers updated** — Grep to enumerate callers. Missing one is a silent break.
3. **Re-run after consolidation** — test suite + build/typecheck pass. Green tests on the survivor license the deletion.

---

## Mode: MODULE DEEPENING

Existing code works; the problem is **shape**, not features. LLM-grown codebases accrete shallow modules — thin wrappers, pass-through layers, near-duplicate helpers. Each looks harmless; together they spread complexity across every caller.

**Deep module:** hides a lot of behavior behind a small interface.
**Shallow module:** interface is almost as complex as its implementation — callers learn a thing without getting much.

### The Deletion Test

For each candidate: **If I deleted this module, would the complexity it holds CONCENTRATE somewhere, or just MOVE elsewhere?**

- Complexity vanishes/stays put → module is earning its keep (real abstraction). Leave it alone.
- Complexity just moves → module is a pass-through. Deepening candidate.

| Smell | Usually |
| ------- | --------- |
| Thin wrapper (`doX(a){ return lib.doX(a) }`) | Shallow |
| Pass-through layer (service maps 1:1 to repo) | Shallow |
| Near-duplicate helper (same intent, different name) | Shallow — consolidate first |
| Config/leverage module (small interface, branching/retry/state inside) | Deep — keep |

### Diagnosis Flow (READ-ONLY)

1. Enumerate exported surface (`name | file:line | signature`)
2. Flag shallow shapes
3. Cross-reference near-duplicates (run duplicate detection mode first — consolidate before deepening)
4. Run deletion test on each survivor
5. Output: candidate list, not a refactor

### Present Candidates Before Proposing Interfaces

Badge each candidate: **Strong** (unambiguous), **Worth-exploring** (real cost/risk), **Speculative** (hunch, low confidence).

For each: before/after sketch (current shallow interface vs proposed deeper one) with deletion test result. Then stop and ask which to pursue. Do not design interfaces for candidates the user hasn't chosen.

### Two-Adapters Rule for Seam Placement

When designing the deeper interface, the seam must have two concrete adapters:

1. **First adapter:** production caller(s) using the new interface
2. **Second adapter:** test exercising the same interface

If only production code crosses the seam and you can't name a second adapter → the seam is a guess. Put the interface where a test can reach it, or don't introduce it.

### Handoff to BUILD

This skill ends at: chosen candidate + deeper-interface proposal + named seam. It does NOT edit code. The refactor routes through planner → BUILD workflow (builder → reviewer → verifier → doc-sync → memory). The deepening is verified: survivor interface has tests at its seam, every caller is repointed, suite + typecheck pass after merge.

Proposing is read-only; changing is gated.
