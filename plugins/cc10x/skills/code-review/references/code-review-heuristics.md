# Code Review Heuristics

## Table of Contents
- [Maintainability Scan](#maintainability-scan)
- [Performance Scan](#performance-scan)
- [Hidden Failure Scan](#hidden-failure-scan)
- [Edge-Case Taxonomy](#edge-case-taxonomy)
- [Sloppy Pattern Scan](#sloppy-pattern-scan)
- [UI Quick Scan](#ui-quick-scan)
- [Type Design Red Flags](#type-design-red-flags)

## Maintainability Scan

Look for:
- unclear naming
- multiple responsibilities in one function
- dense nested branching
- duplication with minor variations
- hardcoded values that should be centralized

Flag only when the problem materially increases bug risk or future change cost.

## Performance Scan

Look for:
- N+1 database or network calls
- expensive work inside loops or render paths
- missing early returns on large collections
- repeated parsing, sorting, or serialization
- missing caching where the code clearly expects reuse

Performance concerns without concrete impact are soft findings, not automatic
blockers.

## Hidden Failure Scan

Watch for patterns that suppress truth:
- optional chaining that swallows missing state without logging
- fallback defaults masking null or undefined source errors
- catch-log-continue flows that never surface failure to the caller
- retries that end silently
- background jobs that drop errors into logs only

Hidden failures are high value because tests often miss them.

## Edge-Case Taxonomy

Use only the categories relevant to the change:
- missing else/default branch
- unguarded input
- off-by-one bounds
- arithmetic edge case
- implicit type coercion
- race condition or shared mutable state
- timeout, retry, or cancellation gap

Do not run the full taxonomy mechanically. Pick the few categories the code
shape makes plausible.

## Sloppy Pattern Scan

After the main review, do a quick debt scan:
- dead imports
- leftover debug prints
- commented-out code blocks
- inconsistent naming in the same file
- copy-paste blocks with tiny variations

These usually produce LOW or MEDIUM findings unless they touch trust-critical
paths.

## UI Quick Scan

If the diff includes UI:
- loading, error, empty, and success states exist
- interactive elements use semantic controls
- focus and keyboard behavior are preserved
- labels and names exist for controls

For deep UI review, pair this with `frontend-patterns` references.

## Type Design Red Flags

Typed code deserves an extra pass for:
- mutable internals exposed to callers
- invariants documented but not enforced
- constructors or factories that allow invalid objects
- anemic models where domain rules live in unrelated helpers

Flag these when they make the current change unsafe or misleading, not as a
generic architecture lecture.
