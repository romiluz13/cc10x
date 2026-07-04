# Deep Comparison: TDD & Testing Methodology

> **Projects compared:** cc10x · Superpowers · Matt Pocock
> **Scope:** How each project teaches TDD, handles anti-patterns, test verification, mocking, and unique patterns.

---

## 1. How Each Project Teaches TDD (RED-GREEN-REFACTOR)

### cc10x

cc10x's TDD methodology lives primarily in **`building/SKILL.md`** with supporting reference files. The core framing:

- **Iron Law:** `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST` — identical headline to Superpowers.
- **RED → GREEN → REFACTOR cycle** is explicitly defined with three sub-sections:
  - **RED:** Write one failing test for the current slice. Run it. Exit 1 = RED achieved.
  - **GREEN:** Write the minimum code to pass. No extra features, no abstractions for hypothetical futures.
  - **REFACTOR:** Improve code quality while keeping tests green. If tests fail during refactor, revert.
- **False-RED guard (CRITICAL):** Exit 1 from import/syntax/collection ERROR is NOT a real RED. A genuine RED is a behavioral failure. Record the observed failure reason verbatim. This is enforced at the **contract level** — `TDD_RED_REASON_KIND=behavioral` is required for `STATUS=PASS`; a `TDD_RED_REASON_KIND=error` is rejected as if RED never happened.
- **Vertical Slicing (CRITICAL):** Build in thin vertical slices crossing all layers (UI → API → logic → data → test). Horizontal slices defer integration risk and produce untestable layers.
- **Leading Words vocabulary:** cc10x introduces a compact vocabulary (`red`, `green`, `tight`, `deep`, `shallow`, `seam`) that replaces verbose instructions with terse, shared terms. This is unique — neither Superpowers nor Matt Pocock does this.
- **Test Process Discipline:** Explicit run-mode commands (`CI=true npm test`, `npx vitest run`), timeout guards, process cleanup (`pgrep -f "vitest|jest" || echo "Clean"`), and IDE-vs-CLI truth guidance.
- **Loop Caps:** GREEN fails 3 consecutive times on same test → FAIL. Same error recurs after 3 fix attempts → FAIL. This is a hard stop mechanism absent from both other projects.
- **Scope Escalation:** If build scope grows beyond the approved plan, emit `SCOPE_INCREASES`. Decision checkpoints with specific triggers (changing >3 files not in plan, choosing between 2+ valid patterns, breaking existing API, adding dependency, touching later phase).
- **Coverage Threshold:** If `coverage-thresholds.json` exists, run coverage and compare. Below thresholds → FAIL.
- **Test Prioritization hierarchy:** 1) Behavioral, 2) Edge case, 3) Integration, 4) Performance (only if stated requirement).
- **Design for Testability:** "If tests are hard to write, the code is hard to test — fix the code, not the test." Pure functions easy, side effects hard, isolate at boundaries.
- **Pure HTML/CSS/JS exception:** If no test runner exists, TDD evidence may use manual browser verification with `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0` and manual check evidence.

### Superpowers

Superpowers' TDD methodology lives in **`test-driven-development/SKILL.md`** with a companion **`testing-anti-patterns.md`**. The approach is deeply pedagogical and anti-rationalization focused:

- **Iron Law:** `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST` — same headline.
- **Core principle:** "If you didn't watch the test fail, you don't know if it tests the right thing."
- **RED-GREEN-REFACTOR cycle** with a **graphviz DOT diagram** visualizing the loop with decision diamonds for "Verify fails correctly" and "Verify passes / All green." This visual is unique to Superpowers.
- **Verify RED is MANDATORY. Never skip.** Must confirm: test fails (not errors), failure message is expected, fails because feature missing (not typos). Test passes? → testing existing behavior, fix test. Test errors? → fix error, re-run until it fails correctly.
- **Verify GREEN is MANDATORY.** Must confirm: test passes, other tests still pass, output pristine (no errors, warnings).
- **Good/Bad code examples** inline for each phase (RED, GREEN) with `<Good>` and `<Bad>` tags — very didactic.
- **"Why Order Matters" section:** Addresses 4 specific rationalizations with detailed rebuttals: "I'll write tests after," "I already manually tested," "Deleting X hours of work is wasteful," "TDD is dogmatic."
- **Common Rationalizations table:** 11 rationalizations mapped to reality. This is the most comprehensive anti-rationalization toolkit of the three projects.
- **Red Flags list:** 13 specific stop signals that mean "Delete code. Start over with TDD."
- **Good Tests table:** Minimal (one thing, "and" in name? Split it), Clear (name describes behavior), Shows intent (demonstrates desired API).
- **Debugging Integration:** "Bug found? Write failing test reproducing it. Never fix bugs without a test."
- **Verification Checklist:** 8-item checklist before marking work complete.
- **When Stuck table:** 4 common problems with solutions.
- **Final Rule:** `Production code → test exists and failed first / Otherwise → not TDD`. No exceptions without human partner's permission.
- **Refactoring is part of the cycle** (unlike Matt Pocock who separates it).

### Matt Pocock

Matt Pocock's TDD methodology is split across three files: **`SKILL.md`** (the loop), **`tests.md`** (good/bad test examples), **`mocking.md`** (mocking guidelines). The approach is more conceptual and design-focused:

- **TDD is the red → green loop.** Refactoring is explicitly **NOT** part of the loop — "It belongs to the review stage, not the red → green implementation cycle." This is a notable philosophical difference from both cc10x and Superpowers.
- **What a good test is:** "Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification."
- **Seams concept:** "A seam is the public boundary you test at." This concept is also used by cc10x (in the Leading Words vocabulary) but Matt Pocock makes it central: **"Test only at pre-agreed seams. Before writing any test, write down the seams under test and confirm them with the user."** This user-confirmation step is unique.
- **Anti-patterns (3 defined):**
  1. **Implementation-coupled** — mocks internal collaborators, tests private methods, verifies through side channel. The tell: test breaks when you refactor but behavior hasn't changed.
  2. **Tautological** — assertion recomputes expected value the way code does. "Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec."
  3. **Horizontal slicing** — writing all tests first, then all implementation. "Bulk tests verify imagined behavior." Work in vertical slices instead — "one test → one implementation → repeat, each test a tracer bullet."
- **Rules of the loop (3):** Red before green, one slice at a time, refactoring is not part of the loop.
- **CONTEXT.md:** "When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs." This is unique — neither cc10x nor Superpowers mentions CONTEXT.md or ADRs.
- **tests.md** provides concise good/bad examples of integration-style vs implementation-detail tests and tautological tests.
- **mocking.md** covers dependency injection and SDK-style interfaces (see section 4 below).

### Summary Table: TDD Teaching

| Dimension | cc10x | Superpowers | Matt Pocock |
|-----------|-------|-------------|-------------|
| Iron Law | ✅ Identical | ✅ Identical | ❌ (implied, not stated as law) |
| RED-GREEN-REFACTOR explicit | ✅ | ✅ | ✅ (but REFACTOR excluded from loop) |
| False-RED guard | ✅ Contract-enforced | ✅ (verify RED step) | ❌ Not mentioned |
| Vertical slicing | ✅ Critical | ❌ Not mentioned | ✅ (anti-horizontal-slicing) |
| Visual diagram | ❌ | ✅ DOT graph | ❌ |
| Good/Bad examples inline | ❌ (in references) | ✅ (in SKILL.md) | ✅ (in tests.md) |
| Anti-rationalization toolkit | ❌ | ✅ (11 entries) | ❌ |
| Red flags / stop signals | ❌ | ✅ (13 signals) | ❌ |
| Loop caps / hard stops | ✅ (3-strike) | ❌ | ❌ |
| Scope escalation | ✅ (decision checkpoints) | ❌ | ❌ |
| Seams concept | ✅ (leading word) | ❌ | ✅ (central, user-confirmed) |
| Test process discipline (run mode) | ✅ | ❌ | ❌ |
| Coverage threshold | ✅ | ❌ | ❌ |
| CONTEXT.md / ADRs | ❌ | ❌ | ✅ |

---

## 2. Testing Anti-Patterns Each Project Warns About

### cc10x

cc10x addresses anti-patterns across `building/SKILL.md` and its three reference files:

**From `testing-patterns.md`:**
- **Test Smells:** giant setup blocks, dependent tests, mock-heavy tests that don't execute real logic, assertions on implementation internals, no assertions at all, names that lie about behavior.
- **Pre-Run Sanity Check:** no test depends on execution order, no arbitrary sleeps, no mocking the module under test, assertions target behavior not structure.
- **Near-Miss Negative Tests:** add rejection tests for values that are almost valid (boundary minus one, wrong type with plausible shape, missing required field, expired/stale state). This is unique — neither other project mentions near-miss testing.

**From `test-data-and-mocks.md`:**
- **Mock Quality Gate:** reconsider design when mock setup is longer than test body, mock defines more behavior than production code path, assertion proves mock was called but not that behavior changed.

**From `building/SKILL.md`:**
- **False-RED:** Exit 1 from import/syntax/collection error is not a real RED.
- **Behavioral focus:** Test what the function DOES, not how it's implemented. Implementation tests break on refactor; behavioral tests survive.

### Superpowers

Superpowers has a dedicated **`testing-anti-patterns.md`** with 5 named anti-patterns, each with a **Gate Function** (a structured decision procedure):

1. **Testing Mock Behavior** — asserting on mock elements (`getByTestId('sidebar-mock')`). Gate: "Am I testing real component behavior or just mock existence?"
2. **Test-Only Methods in Production** — adding `destroy()` to a class only used in tests. Gate: "Is this only used by tests?" + "Does this class own this resource's lifecycle?"
3. **Mocking Without Understanding** — mocking a method that had side effects the test depended on. Gate: 3 questions about side effects and dependency chain. Red flags: "I'll mock this to be safe," "This might be slow, better mock it."
4. **Incomplete Mocks** — partial mock missing fields downstream code uses. Iron Rule: "Mock the COMPLETE data structure as it exists in reality." Gate: examine actual API response, include ALL fields.
5. **Integration Tests as Afterthought** — implementation complete with no tests written. Fix: TDD cycle.

**Additional from `test-driven-development/SKILL.md`:**
- Test passes immediately (didn't watch it fail)
- Can't explain why test failed
- Tests added "later"
- Vague test names (`test('retry works')`)
- Testing mock not code
- Over-engineered GREEN (YAGNI violations)

**Red Flags quick reference:** assertion checks for `*-mock` test IDs, methods only called in test files, mock setup is >50% of test, test fails when you remove mock, can't explain why mock is needed, mocking "just to be safe."

### Matt Pocock

Matt Pocock defines 3 anti-patterns in `SKILL.md` with concise descriptions:

1. **Implementation-coupled** — mocks internal collaborators, tests private methods, verifies through side channel (querying DB instead of using interface). The tell: test breaks when you refactor but behavior hasn't changed.
2. **Tautological** — assertion recomputes expected value the way code does (`expect(add(a, b)).toBe(a + b)`). Expected values must come from an independent source of truth.
3. **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify imagined behavior. Work in vertical slices instead.

**From `tests.md`:**
- Implementation-detail tests: mocking internal collaborators, testing private methods, asserting on call counts/order, test breaks when refactoring without behavior change, test name describes HOW not WHAT, verifying through external means instead of interface.
- Tautological tests with concrete example: `expected = items.reduce(...)` then `expect(calculateTotal(items)).toBe(expected)` — passes by construction.

### Summary Table: Anti-Patterns

| Anti-Pattern | cc10x | Superpowers | Matt Pocock |
|--------------|-------|-------------|-------------|
| Testing mock behavior | ✅ (mock quality gate) | ✅ (Anti-Pattern 1, gate function) | ✅ (implementation-coupled) |
| Test-only methods in production | ❌ | ✅ (Anti-Pattern 2, gate function) | ❌ |
| Mocking without understanding | ✅ (mock quality gate) | ✅ (Anti-Pattern 3, gate function) | ❌ (implied) |
| Incomplete mocks | ❌ | ✅ (Anti-Pattern 4, gate function) | ❌ |
| Tests as afterthought | ✅ (Iron Law) | ✅ (Anti-Pattern 5) | ✅ (horizontal slicing) |
| Tautological tests | ❌ | ❌ | ✅ (named anti-pattern) |
| Horizontal slicing | ✅ (vertical slicing critical) | ❌ | ✅ (named anti-pattern) |
| Implementation-coupled tests | ✅ (behavioral focus) | ✅ | ✅ |
| Near-miss negative tests | ✅ (unique) | ❌ | ❌ |
| Dependent tests | ✅ (test smells) | ❌ | ❌ |
| Arbitrary sleeps | ✅ (pre-run sanity) | ❌ | ❌ |
| Gate Functions (structured decisions) | ❌ | ✅ (5 gates) | ❌ |

---

## 3. Test Verification (Test Honesty Gates, etc.)

### cc10x

cc10x has the most sophisticated verification system of the three, spread across **`verification/SKILL.md`**, the **router hook policy**, and **`integration-and-live-proof.md`**:

- **The Gate Function:** `COMPLETION → TRUTH → PROOF`. Three levels: (1) Did the agent finish? (2) Is the work actually correct? (3) Can you prove it with evidence? "A PASS without proof is a claim. A claim is not verification."
- **Self-Critique Gate (BEFORE Verification Commands):** A pre-verification checklist with two sections — Code Quality (no TODO/FIXME/stubs, no commented-out code, no debug logging, error handling, types correct) and Implementation Completeness (every acceptance criterion has code, every named scenario has a test, every error path has handling, no silent failures, build succeeds). "If any check fails, fix it BEFORE running verification. Don't run tests you know will fail on code quality issues."
- **Validation Levels:** Deterministic (automated test, exit 0/1), Probabilistic (known flake rate, retry policy), Manual (human checklist), Live (production-like environment). Every verification must state its validation level.
- **Evidence Array Protocol (MANDATORY for PASS):** Structured format with `scenarios`, `regressions`, `edge_cases`. Every scenario needs non-empty Expected and Actual. Every scenario maps to exactly one EVIDENCE entry. SCENARIOS_PASSED must equal EVIDENCE.scenarios with exit 0.
- **Goal-Backward Lens:** 4-step backward walk from goal: (1) What was the goal? (2) What would prove it? (3) Do I have that evidence? (4) Does the evidence actually prove the goal? "Not 'tests pass' but 'the tests test the right thing.'"
- **Forbidden language before proof:** "should pass", "looks good", "seems fine", "builder reported success", "the tests cover this" (without showing which test), "no regressions detected" (without listing what was tested).
- **Common Failures table:** False green (test passes without exercising real code path → Test Honesty Gates), Scope skip ("all tests pass" but untested scenarios exist), Stale evidence ("tests pass" but didn't run them this session), Claim without proof, Environment escape.
- **Contract-enforced TDD gates:** The router hook policy requires `TDD_RED_EXIT=1`, `TDD_RED_REASON_KIND=behavioral` (false-RED rejected), `TDD_GREEN_EXIT=0` for `STATUS=PASS`. This is machine-enforced, not just guidance.
- **Auditor Posture:** "You are an independent auditor. A reviewer approval, green unit test, or builder claim is never sufficient by itself for PASS. If you cannot independently reproduce a claimed success, return FAIL."
- **Production-Like Live Proof:** Harness runner with manifest, fail-closed rules (no substituting unit tests for required live proof), flaky test handling (re-run once, pass on re-run → mark `flaky: true`, fail both → FAIL).
- **Integration escalation framework:** Unit → Integration → E2E/Live. Explicit triggers for escalation ("production-like", "real data", "real API calls", "stress test").

### Superpowers

Superpowers' verification methodology lives in **`verification-before-completion/SKILL.md`**:

- **Iron Law:** `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`. "If you haven't run the verification command in this message, you cannot claim it passes."
- **Gate Function:** 5-step procedure: IDENTIFY (what command proves this?), RUN (execute FULL command), READ (full output, check exit code, count failures), VERIFY (does output confirm claim?), ONLY THEN (make the claim). "Skip any step = lying, not verifying."
- **Common Failures table:** 8 claim types mapped to what's required vs what's not sufficient (e.g., "Tests pass" requires test command output with 0 failures, not sufficient: previous run, "should pass").
- **Red Flags - STOP:** Using "should/probably/seems", expressing satisfaction before verification, about to commit without verification, trusting agent success reports, relying on partial verification, thinking "just this once", tired, ANY wording implying success without having run verification.
- **Rationalization Prevention table:** 8 excuses mapped to reality ("Should work now" → RUN the verification, "I'm confident" → confidence ≠ evidence, "Agent said success" → verify independently).
- **Key Patterns:** Concrete examples for tests (✅ run test command, see 34/34 pass; ❌ "should pass now"), regression tests (✅ write → run pass → revert fix → run MUST FAIL → restore → run pass; ❌ "I've written a regression test" without red-green verification), build, requirements, agent delegation.
- **Why This Matters:** References 24 failure memories including "your human partner said 'I don't believe you' - trust broken," undefined functions shipped, missing requirements shipped. "Violates: 'Honesty is a core value. If you lie, you'll be replaced.'"
- **Scope:** Applies before ANY variation of success/completion claims, ANY expression of satisfaction, ANY positive statement about work state, committing/PR/task completion, moving to next task, delegating to agents.

### Matt Pocock

Matt Pocock does **not** have a dedicated verification skill. Verification is implicit in the TDD loop rules:

- **Red before green** is the core verification — you must see the test fail first.
- **One slice at a time** ensures each cycle is independently verifiable.
- The **seams concept** is a form of verification discipline — test only at pre-agreed seams, confirmed with the user.
- **No explicit evidence protocol, no gate function, no forbidden language, no auditor posture.**

### Summary Table: Test Verification

| Verification Feature | cc10x | Superpowers | Matt Pocock |
|---------------------|-------|-------------|-------------|
| Dedicated verification skill | ✅ | ✅ | ❌ |
| Gate function (structured) | ✅ (COMPLETION→TRUTH→PROOF) | ✅ (5-step) | ❌ |
| Self-critique gate (pre-test) | ✅ | ❌ | ❌ |
| Evidence array protocol | ✅ (mandatory) | ❌ | ❌ |
| Goal-backward lens | ✅ | ❌ (implicit) | ❌ |
| Forbidden language list | ✅ | ✅ (red flags) | ❌ |
| Contract-enforced TDD gates | ✅ (machine-enforced) | ❌ | ❌ |
| Auditor posture | ✅ | ✅ (implicit) | ❌ |
| Validation levels (4 types) | ✅ | ❌ | ❌ |
| Live/production proof | ✅ (harness) | ❌ | ❌ |
| Regression test verification | ✅ (evidence array) | ✅ (red-green-revert-restore) | ❌ |
| Anti-rationalization | ✅ (some) | ✅ (8 entries) | ❌ |
| Failure memory references | ❌ | ✅ (24 memories) | ❌ |

---

## 4. Mocking

### cc10x

cc10x covers mocking in **`test-data-and-mocks.md`** and **`testing-patterns.md`**:

- **Factory Pattern:** Prefer small factory helpers over repeated object literals. Example: `getMockUser` with overrides pattern.
- **Mock Only Boundaries:** Mock network calls, databases (when isolation requires), time, third-party services. Do NOT mock your own core business logic, internal collaborators you control, the module under test. "If you must mock everything to write the test, the design probably needs work."
- **Common Boundary Mocks:** `global.fetch`, database client wrapper, cache/queue adapters, auth provider SDKs. "Keep mocks thin. The point is to isolate the boundary, not recreate the system."
- **Environment And Time:** Set env vars in setup, clean in teardown. Use fake timers deliberately. Restore global state after test. "Leaking env or timer state across tests creates false failures."
- **Mock Quality Gate:** Reconsider design when (1) mock setup is longer than test body, (2) mock defines more behavior than production code path, (3) assertion proves mock was called but not that behavior changed. "The test should still teach you something real about the system."

### Superpowers

Superpowers covers mocking primarily in **`testing-anti-patterns.md`** (Anti-Patterns 1, 3, 4) and in **`test-driven-development/SKILL.md`**:

- **Iron Laws of mocking:** (1) NEVER test mock behavior, (2) NEVER add test-only methods to production classes, (3) NEVER mock without understanding dependencies.
- **Gate Functions for mocking:** Each mock-related anti-pattern has a structured gate function — a series of questions to ask before proceeding.
- **"When Mocks Become Too Complex"** section: Warning signs (mock setup longer than test logic, mocking everything to make test pass, mocks missing methods, test breaks when mock changes). Consider integration tests with real components.
- **Mocking Without Understanding gate:** Before mocking, ask (1) What side effects does the real method have? (2) Does this test depend on any of those side effects? (3) Do I fully understand what this test needs? If unsure, run test with real implementation FIRST, observe, then add minimal mocking.
- **Incomplete Mocks rule:** "Mock the COMPLETE data structure as it exists in reality, not just fields your immediate test uses."
- **TDD SKILL.md:** "Real code (no mocks unless unavoidable)" as a test requirement. "Must mock everything? Code too coupled. Use dependency injection."

### Matt Pocock

Matt Pocock has a dedicated **`mocking.md`** file with a clear, concise philosophy:

- **Mock at system boundaries only:** External APIs, databases (sometimes — prefer test DB), time/randomness, file system (sometimes).
- **Don't mock:** Your own classes/modules, internal collaborators, anything you control.
- **Designing for Mockability — two techniques:**
  1. **Dependency injection:** Pass external dependencies in rather than creating them internally. Example: `processPayment(order, paymentClient)` vs `processPayment(order)` with `new StripeClient()` inside.
  2. **Prefer SDK-style interfaces over generic fetchers:** Create specific functions for each external operation instead of one generic function with conditional logic. Benefits: each mock returns one specific shape, no conditional logic in test setup, easier to see which endpoints a test exercises, type safety per endpoint.
- **From `tests.md`:** Bad tests mock internal collaborators and assert on call counts/order. Good tests use public API and test observable behavior.

### Summary Table: Mocking

| Mocking Feature | cc10x | Superpowers | Matt Pocock |
|----------------|-------|-------------|-------------|
| Dedicated mocking file | ✅ (test-data-and-mocks.md) | ✅ (testing-anti-patterns.md) | ✅ (mocking.md) |
| Factory pattern for test data | ✅ | ❌ | ❌ |
| Boundary-only mocking | ✅ | ✅ | ✅ |
| Mock quality gate | ✅ (3 conditions) | ✅ (gate functions) | ❌ |
| Dependency injection guidance | ❌ | ✅ (mentioned) | ✅ (detailed) |
| SDK-style interfaces | ❌ | ❌ | ✅ (unique) |
| Incomplete mocks warning | ❌ | ✅ (Anti-Pattern 4) | ❌ |
| Mocking without understanding | ✅ (implicit) | ✅ (Anti-Pattern 3, gate) | ❌ |
| Environment/time handling | ✅ | ❌ | ✅ (time/randomness listed) |
| Iron Laws of mocking | ❌ | ✅ (3 laws) | ❌ (implied) |

---

## 5. TDD Patterns cc10x Has That Others DON'T

| Unique cc10x Pattern | Description | Value |
|---------------------|-------------|-------|
| **Contract-enforced TDD gates** | `TDD_RED_EXIT=1`, `TDD_RED_REASON_KIND=behavioral`, `TDD_GREEN_EXIT=0` are machine-verified in the router hook policy. STATUS=PASS is rejected without them. | **Very High** — this is the only project where TDD compliance is enforced at the system level, not just guidance. |
| **False-RED classification** | Distinguishes behavioral failure (real RED) from import/syntax/collection error (false RED). Contract rejects false REDs. | **High** — catches a common AI failure mode where a broken import looks like a passing test cycle. |
| **Loop Caps (3-strike)** | GREEN fails 3 consecutive times → FAIL. Same error recurs 3 times → FAIL. Hard stops prevent infinite loops. | **High** — prevents agent death spirals that neither other project addresses. |
| **Scope Escalation** | `SCOPE_INCREASES` signal with decision checkpoints (>3 files, 2+ patterns, API break, new dependency, touching later phase). | **High** — manages scope creep during TDD, unique to cc10x's multi-agent architecture. |
| **Evidence Array Protocol** | Mandatory structured format with scenarios, regressions, edge_cases. Every scenario needs Expected and Actual. | **High** — forces concrete evidence, not narrative claims. |
| **Self-Critique Gate** | Pre-verification checklist (code quality + implementation completeness) to run BEFORE tests. | **Medium-High** — catches issues before wasting test runs. |
| **Validation Levels (4 types)** | Deterministic, Probabilistic, Manual, Live — each with explicit criteria. | **Medium** — formalizes what other projects leave implicit. |
| **Goal-Backward Lens** | 4-step backward walk from goal to evidence. | **Medium** — structured approach to "are we actually done?" |
| **Leading Words vocabulary** | Compact vocabulary (red, green, tight, deep, shallow, seam) replacing verbose instructions. | **Medium** — efficiency in multi-agent communication. |
| **Test Process Discipline** | Explicit run-mode commands, timeout guards, process cleanup, IDE-vs-CLI truth. | **Medium** — practical operational guidance absent from others. |
| **Near-Miss Negative Tests** | Rejection tests for values that are almost valid (boundary minus one, wrong type with plausible shape). | **Medium** — specific testing technique unique to cc10x. |
| **Coverage Threshold** | If `coverage-thresholds.json` exists, run coverage and compare. Below → FAIL. | **Medium** — automated quality gate. |
| **Live/Production Proof harness** | Harness runner with manifest, fail-closed rules, flaky test handling, stress mode. | **High** — only project with a real production-like verification system. |
| **Auditor Posture** | "You are an independent auditor. If you cannot independently reproduce a claimed success, return FAIL." | **Medium** — unique framing of the verifier's role. |
| **Forbidden language list** | Specific phrases banned before proof ("should pass", "looks good", "seems fine", "builder reported success"). | **Medium** — Superpowers has red flags but cc10x's are more specific to agent-to-agent communication. |
| **Pure HTML/CSS/JS exception** | Manual browser verification when no test runner exists, with explicit exit code encoding. | **Low-Medium** — niche but pragmatic. |

---

## 6. TDD Patterns Others Have That cc10x SHOULD Adopt

| Pattern | Source | Description | Why cc10x Should Adopt It |
|---------|--------|-------------|--------------------------|
| **Anti-rationalization toolkit** | Superpowers | 11 rationalizations mapped to reality, 13 red flags / stop signals. "Too simple to test," "I'll test after," "Deleting X hours is wasteful," "TDD is dogmatic," etc. | cc10x operates on the assumption that agents will follow the Iron Law, but doesn't address the *internal monologue* that leads to skipping TDD. Adding a rationalization table would strengthen the human-equivalent of "don't fool yourself." |
| **Good/Bad inline examples in SKILL.md** | Superpowers, Matt Pocock | `<Good>` and `<Bad>` code examples directly in the skill, not just in references. | cc10x pushes examples to reference files. While this keeps the SKILL.md compact, examples are the most effective teaching tool. Consider adding 1-2 key examples inline. |
| **Tautological test anti-pattern** | Matt Pocock | Tests where the assertion recomputes the expected value the way the code does — passes by construction, can never disagree. | cc10x doesn't explicitly warn about this. It's a subtle but common failure mode, especially for AI-generated tests. |
| **Pre-agreed seams with user confirmation** | Matt Pocock | "Before writing any test, write down the seams under test and confirm them with the user." | cc10x uses "seam" as a leading word but doesn't require confirmation. In a multi-agent context, having the planner pre-agree seams would add a coordination layer. |
| **CONTEXT.md / ADR awareness** | Matt Pocock | Read `CONTEXT.md` for domain language, respect ADRs in the area you're touching. | cc10x has "Study Project Patterns First" but doesn't mention CONTEXT.md or ADRs explicitly. ADRs often contain testing conventions and constraints. |
| **Refactoring excluded from TDD loop** | Matt Pocock | Refactoring belongs to the review stage, not the red → green cycle. | cc10x includes REFACTOR in the cycle. Matt Pocock's separation is cleaner — it prevents refactoring from becoming a source of test drift during the implementation cycle. cc10x could at least note this as a valid alternative. |
| **Gate Functions for anti-patterns** | Superpowers | Structured decision procedures (IF/THEN) for each anti-pattern, not just descriptions. | cc10x's Mock Quality Gate is similar but less structured. Superpowers' gate functions are executable mental procedures. |
| **Visual diagram of TDD cycle** | Superpowers | DOT graph showing the cycle with decision diamonds. | Minor, but visual aids help comprehension, especially for onboarding. |
| **"Why Order Matters" section** | Superpowers | Detailed rebuttals to 4 specific arguments against test-first. | cc10x states the Iron Law but doesn't explain *why* order matters. Adding this would strengthen the rationale. |
| **Regression test verification pattern** | Superpowers | Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass). | cc10x has regression scenarios in the evidence array but doesn't prescribe this specific verification pattern for bug fixes. |
| **SDK-style interfaces for mockability** | Matt Pocock | Specific functions for each external operation vs one generic fetcher. | cc10x's mocking guidance is about *when* to mock, not *how to design for mockability*. Adding this would bridge testing and design. |

---

## 7. Rating Each Project's TDD Methodology

### cc10x: **8.5/10**

**Strengths:**
- Most operationally complete TDD system. Contract-enforced gates (`TDD_RED_EXIT`, `TDD_RED_REASON_KIND`, `TDD_GREEN_EXIT`) mean TDD compliance is machine-verified, not just aspirational.
- False-RED classification is a genuinely novel contribution that addresses an AI-specific failure mode.
- Loop caps prevent death spirals. Scope escalation manages creep. Evidence array protocol forces concrete proof.
- Live/production proof harness is the only real production-verification system among the three.
- Rich reference file ecosystem (testing-patterns, test-data-and-mocks, integration-and-live-proof).
- Validation levels formalize what others leave implicit.

**Weaknesses:**
- No anti-rationalization toolkit. Assumes agents will follow the Iron Law without addressing the internal monologue that leads to skipping.
- No explicit tautological test warning.
- Examples are in reference files, not inline in SKILL.md.
- Refactoring-in-the-loop vs. separate is not debated; cc10x just picks one.
- Doesn't address how to design for mockability (only when to mock).
- The system is complex — many moving parts (gates, contracts, evidence arrays, validation levels) could overwhelm. The leading words vocabulary helps but the cognitive load is still high.

### Superpowers: **7.5/10**

**Strengths:**
- Best pedagogical design. The anti-rationalization toolkit (11 entries) and red flags (13 signals) are the most comprehensive "don't fool yourself" system.
- Good/Bad inline examples for every phase make it immediately actionable.
- Visual DOT diagram of the TDD cycle.
- Dedicated testing-anti-patterns.md with 5 named anti-patterns, each with a structured Gate Function.
- "Why Order Matters" section provides the philosophical foundation.
- Verification-before-completion skill with 5-step gate function, forbidden language, and 24 failure memory references.
- Regression test verification pattern (write → pass → revert → fail → restore → pass).

**Weaknesses:**
- No contract enforcement — everything is guidance. An agent could skip TDD and nothing would mechanically stop it.
- No false-RED classification.
- No loop caps or hard stops.
- No scope escalation mechanism.
- No live/production proof system.
- No test process discipline (run-mode commands, timeout guards, process cleanup).
- No coverage threshold.
- No vertical slicing (Matt Pocock and cc10x both have it; Superpowers doesn't mention it).
- Verification skill is separate from TDD skill, creating a gap — TDD skill's checklist is lighter than the verification skill's gate.

### Matt Pocock: **6.5/10**

**Strengths:**
- Most conceptually clean. Three files, clear separation of concerns (loop, tests, mocking).
- Seams concept is central and user-confirmed — a unique coordination mechanism.
- Tautological test anti-pattern is a unique and valuable contribution.
- Horizontal slicing anti-pattern with "tracer bullet" metaphor is well-articulated.
- SDK-style interfaces for mockability is unique design-for-testability guidance.
- CONTEXT.md / ADR awareness is unique.
- Refactoring excluded from loop is a clean philosophical position.
- Dependency injection guidance is the most concrete of the three.

**Weaknesses:**
- No dedicated verification skill. Verification is implicit in "red before green."
- No evidence protocol, no gate function, no auditor posture.
- No anti-rationalization toolkit.
- No false-RED guard.
- No loop caps, scope escalation, or hard stops.
- No contract enforcement.
- No live/production proof.
- No test process discipline.
- No coverage threshold.
- No near-miss negative tests.
- No visual diagram.
- Mocking guidance is concise but lacks the depth of Superpowers' gate functions or cc10x's quality gate.
- The "confirm seams with user" step, while valuable, may not translate well to a fully automated agent context.

---

## Verdict

**cc10x has the most operationally rigorous TDD methodology**, distinguished by its contract-enforced gates, false-RED classification, loop caps, and evidence array protocol. It is the only system where TDD compliance is machine-verified rather than guidance-based. However, it lacks the pedagogical depth of Superpowers (anti-rationalization toolkit, inline examples, "why order matters") and the conceptual clarity of Matt Pocock (tautological tests, seam confirmation, SDK-style mockability).

**Superpowers has the best teaching design**, with the most comprehensive anti-rationalization toolkit and inline examples. It is the best starting point for humans learning TDD. However, it lacks the operational enforcement mechanisms that make cc10x's system robust in an agent context.

**Matt Pocock has the most conceptually elegant framework**, with unique contributions (tautological tests, seam confirmation, SDK-style interfaces, CONTEXT.md awareness). However, it is the least operationally complete — no verification skill, no enforcement, no evidence protocol.

### Recommended cc10x Adoptions (Priority Order)

1. **Tautological test anti-pattern** (from Matt Pocock) — subtle, common, AI-relevant
2. **Anti-rationalization toolkit** (from Superpowers) — strengthens the "soft" side of TDD compliance
3. **"Why Order Matters" section** (from Superpowers) — provides philosophical foundation
4. **SDK-style interfaces for mockability** (from Matt Pocock) — bridges testing and design
5. **Regression test verification pattern** (from Superpowers) — concrete bug-fix verification protocol
6. **Gate Functions for anti-patterns** (from Superpowers) — structured decision procedures
7. **CONTEXT.md / ADR awareness** (from Matt Pocock) — domain language alignment
8. **Pre-agreed seams** (from Matt Pocock) — coordination mechanism for multi-agent planning
9. **Inline Good/Bad examples** (from Superpowers) — pedagogical reinforcement
10. **Refactoring-as-separate-stage debate** (from Matt Pocock) — at least acknowledge the alternative

---