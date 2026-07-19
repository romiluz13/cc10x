---
name: building
description: |
  Implementation skill for writing production code with TDD. Covers the RED-GREEN-REFACTOR
  cycle, false-RED detection, vertical slicing, scope escalation, test process discipline,
  and code generation patterns. Loaded by component-builder and bug-investigator.
allowed-tools: Read Write Edit Bash Grep Glob LSP
user-invocable: false
---

# Building (Code Generation + TDD)

**Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

## Reference Files

Read only what's needed:

- `references/testing-patterns.md` — test structure, isolation, naming; load when writing the first test of a cycle or a test feels awkward to structure
- `references/test-data-and-mocks.md` — mock discipline, test data factories; load when a test needs fixtures/factories or you are about to mock anything
- `references/integration-and-live-proof.md` — integration test guidance, live verification; load when the slice crosses a service/DB/API boundary or the plan names live proof

## Test Process Discipline

- **Always use run mode:** `CI=true npm test`, `npx vitest run` (NOT `npx vitest`), `CI=true npx jest`
- **Timeout guard:** `timeout 60s npx vitest run` if uncertain about CI=true
- **After TDD cycle:** `pgrep -f "vitest|jest" || echo "Clean"`. Kill if found.
- **IDE vs CLI truth:** If CLI tests pass with exit 0, trust CLI over IDE/LSP errors (stale cache)

## RED → GREEN → REFACTOR

### RED — Failing Test First

Write one failing test for the current slice. Run it. **RED = a behavioral failure** ("X is not a function", "expected 3, received undefined") — never a bare exit code.

**False-RED guard (CRITICAL):** Exit 1 from an import/syntax/collection ERROR is a broken harness, not a RED — fix the harness and re-run. Record the observed failure reason verbatim.

### GREEN — Minimal Code

Write the minimum code to pass the test. No extra features, no abstractions for hypothetical futures. No unrelated test breakage. If existing tests break, fix the code not the tests.

### REFACTOR — Clean Up

Improve code quality while keeping tests green. If tests fail during refactor, revert. Re-run after every refactor step.

**Safety-Check Guard (MANDATORY):** Never simplify away a safety check during refactoring. Safety checks include:

- Input validation at trust boundaries (API entry points, user input, external data)
- Error handling that prevents data loss or corruption
- Security checks (auth, authorization, sanitization)
- Accessibility checks (ARIA, keyboard navigation, semantic HTML)

If a safety check seems unnecessary, verify with a test that proves it's dead code before removing. "Looks redundant" is not sufficient evidence.

### Vertical Slicing (CRITICAL)

Build in thin vertical slices that cross all layers: UI → API → logic → data → test. A horizontal slice (all UI, then all API, then all logic — or all tests first, then all implementation) defers integration risk to the end and produces untestable layers. Each slice should be independently verifiable and shippable.

### Seam Discipline

**One seam, one test, one minimal implementation per cycle.** Each test is a tracer bullet that responds to what the last cycle taught you — work one vertical slice at a time.

**Test only at pre-agreed seams.** A seam is the public boundary where you observe behavior without reaching inside. Before writing any test, know which seam you're testing at. Prefer existing seams to new ones; use the highest seam possible; the fewer seams across the codebase, the better (ideal is one). If the plan provides a `### Test Seams` subsection or an Interfaces block, draw your seams from there.

**Implementation-coupled anti-pattern.** A test is implementation-coupled if it mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed. Test through the public interface, not internals.

**Record your seams (enforced contract fields).** Your Router Contract carries two seam fields:

- `TEST_SEAMS: [seam names you actually tested at]`
- `SEAM_GATE_STATUS: "confirmed" | "proposed" | "disagreed" | "not_applicable"`

Set `SEAM_GATE_STATUS` as follows:

- **`confirmed`** — the plan provided `test_seams` and you used them (TEST_SEAMS non-empty, matching the plan).
- **`proposed`** — no plan (direct/no-plan path) OR a legacy plan whose phase omits `test_seams`; you proposed seams at BUILD_PREFLIGHT (TEST_SEAMS non-empty).
- **`disagreed`** — the plan's proposed seam cannot exercise the phase's real risk. Record the disagreement in `DECISIONS` and either propose a better seam (TEST_SEAMS non-empty with the better seam) or block on genuine ambiguity (`STATUS: FAIL`, `REMEDIATION_REASON: "Ambiguous test surface — no seam exercises the real risk"`).
- **`not_applicable`** — `build_scope=trivial`; no seam expectation.

The router validates these per `build_scope` (see the contract-override table). This is the enforced gate — not advisory.

## Study Project Patterns First

Before writing code: read 2-3 existing similar components in the repo. Match naming, file structure, export style, test patterns. Follow the project's conventions — don't introduce a new pattern when an existing one works.

**LSP before writing:** Use LSP to find definitions, references, and type information before writing code that interfaces with existing modules.

## Scope Escalation (SCOPE_INCREASES)

If the build scope grows beyond the approved phase — new files not in the plan, new dependencies, API contract changes — emit `SCOPE_INCREASES: ["new scope item"]` in the contract. The router decides whether to escalate to a full BUILD (with planner + reviewer) or approve the expansion.

**Decision Checkpoints (return FAIL when triggered):**

| Trigger | Action |
| --------- | -------- |
| Changing >3 files not in plan | FAIL with extra files named |
| Choosing between 2+ valid patterns | FAIL with competing options |
| Breaking existing API contract | FAIL with impacted callers |
| Adding dependency not in plan | FAIL with dependency name |
| Touching a later planned phase early | FAIL with skipped phase |

## Minimal Diffs

Write minimal diffs. A bug fix doesn't need surrounding cleanup. A one-shot operation doesn't need a helper. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees in production code — no runtime re-validation for scenarios the types or the framework already exclude; only validate at system boundaries. When your feature depends on a framework behavior, pin it with a test instead: guarantees have edge cases, and the test costs less than the defensive code.

## Rationalization Table

| Excuse | Reality |
| ------ | ------ |
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll write tests after" | "After" never comes. Write the test first — it IS the spec. |
| "It's just a refactor" | Refactors break things. Run the tests before AND after. |
| "The existing tests cover this" | Then your new test will pass immediately — that's a false RED. |
| "I manually tested it" | Manual testing doesn't survive the next refactor or CI run. |
| "Adding tests would slow down delivery" | Debugging untested code takes longer than writing the test. |
| "The framework handles this" | Pin the depended-on behavior with a test — don't re-validate at runtime. |

## Red Flags — STOP and Reconsider

- You're about to write production code without a failing test
- You're skipping the RED step because "the test will obviously fail"
- You're adding error handling for a scenario that can't happen
- You're introducing an abstraction with only one caller
- You're changing code unrelated to the current phase
- You're about to commit without running the full test suite
- You're considering deleting a test to make the build pass
- You're adding a dependency not in the plan

## Tautological Test Anti-Pattern

A tautological test recomputes the expected value the same way the code does — it passes by construction and can never disagree.

```typescript
// BAD — tautological: recomputes expected value using same logic
const expected = items.reduce((sum, x) => sum + x.value, 0);
expect(calculateTotal(items)).toBe(expected);

// GOOD — expected value comes from an independent source of truth
expect(calculateTotal([{value: 10}, {value: 20}, {value: 30}])).toBe(60);
```

**Rule:** Expected values must come from a known-good literal, a worked example, or the spec — never from re-running the same algorithm the code uses.

## Loop Caps

- **TDD Failure Cap:** GREEN fails 3 consecutive times on same test → FAIL with error
- **Build/Lint Loop Cap:** Same error recurs after 3 fix attempts → FAIL with error_code + file

## Coverage Threshold

If `coverage-thresholds.json` exists, run coverage and compare. Below thresholds → FAIL. If no thresholds file, skip coverage check.

## Test Prioritization

1. Behavioral tests (does the function do what it should?)
2. Edge case tests (empty input, null, boundary values)
3. Integration tests (does it work with real dependencies?)
4. Performance tests (only if performance is a stated requirement)

## Design for Testability

If tests are hard to write, the code is hard to test — fix the code, not the test. Pure functions are easy to test. Side effects are hard. Isolate side effects at boundaries; keep core logic pure.

## When Stuck

- RED won't fail: check if the test is actually exercising the code path
- GREEN won't pass: re-read the test, check if the assertion matches the requirement
- Existing tests break: your change has a side effect you didn't expect — revert and isolate

**Pure HTML/CSS/JS exception:** If no test runner exists, TDD evidence may use manual browser verification. Set TDD_RED_EXIT=1, TDD_GREEN_EXIT=0 with manual check evidence.
