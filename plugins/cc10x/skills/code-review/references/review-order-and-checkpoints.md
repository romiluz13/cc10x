# Review Order And Checkpoints

## Table of Contents
- [Read By Concern, Not File Order](#read-by-concern-not-file-order)
- [Recommended Review Sequence](#recommended-review-sequence)
- [Checkpoint Questions](#checkpoint-questions)
- [Partial-Phase Reviews](#partial-phase-reviews)
- [Zero-Finding Halt](#zero-finding-halt)
- [Re-Review After Fixes](#re-review-after-fixes)

## Read By Concern, Not File Order

Borrow the best part of BMAD's checkpoint thinking: reconstruct the change in
the order that builds understanding, not the order `git diff` prints files.

Review by concern:
- contract change
- state change
- side effects
- verification evidence

This prevents reviewing helpers before you understand what they are helping.

## Recommended Review Sequence

1. Orient:
   - what was requested?
   - what changed?
   - what is the highest-risk boundary?
2. Verify spec compliance:
   - requirements
   - acceptance criteria
   - phase exit criteria if this is partial work
3. Review trust-critical boundaries:
   - auth
   - data writes
   - public API
   - migrations
   - retries/timeouts
4. Review maintainability and hidden failure patterns.
5. Re-run the relevant proof.

## Checkpoint Questions

Use these pauses during review:
- "What is this change trying to accomplish?"
- "Where would being wrong hurt the most?"
- "What observable proof exists that the requirement is satisfied?"
- "What assumption changed across files?"

If the answer is unclear, do not continue scanning code mechanically. Rebuild
the story first.

## Partial-Phase Reviews

For a single phase of a larger plan:
- verify this phase's exit criteria
- verify interfaces exposed to later phases
- do not reject the phase for future work that belongs to later phases
- note out-of-scope concerns separately

The review succeeds when the approved scope is correct, complete, and verified.

## Zero-Finding Halt

If a non-trivial review produces zero findings, halt and re-examine. Zero
findings may be real, but they require proof of depth.

Minimum re-examination:
1. Re-read every changed file.
2. Re-run the security scan.
3. Apply the sloppy-pattern and hidden-failure scans.
4. Name the checks performed if findings still remain zero.

A bare "looks good" is invalid.

## Re-Review After Fixes

After requested changes:
1. confirm the original issue is actually fixed
2. verify the fix did not create a regression
3. remove resolved findings from the active list
4. keep unresolved findings explicit

Do not approve based on intent. Approve based on fresh proof.
