# Lessons Learned — What Broke and How to Avoid It

Every lesson here was learned from a real failure during v10.1.14, v10.1.15, or v10.1.16. These are not theoretical — each one cost time and effort to diagnose.

---

## Execution Failures

### "File has not been read yet" (v10.1.14)
**What happened:** Launched 5 parallel Edit calls in Batch 1. All 5 failed because none of the files had been Read in the current session.
**Root cause:** The Edit tool requires a prior Read of the file in the same conversation.
**Fix:** Always read ALL target files in a parallel batch BEFORE any edits. This is Batch 1 of every execution.
**Prevention:** The pipeline now has an explicit "Batch 1: Read all files" step.

### FIND block mismatch (v10.1.14)
**What happened:** The FIND block for code-reviewer scope guard contained `## Process\n\n1. **Read Memory**` but the actual text started with `0. **Output contract envelope`.
**Root cause:** Wrote FIND text from memory/plan instead of from actual Read output.
**Fix:** Always copy FIND text directly from the Read tool output, character-for-character.
**Prevention:** Read agents now capture verbatim text at insertion points before plan writing.

### marketplace.json double version (v10.1.15)
**What happened:** `"version": "10.1.14"` appeared twice in the file. The first Edit updated one, but the second FIND matched the wrong instance.
**Root cause:** Non-unique FIND text. Both lines were identical.
**Fix:** Include more surrounding context in the FIND block to uniquely identify each instance.
**Prevention:** For files with duplicate strings, include 1-2 adjacent lines in the FIND block.

### README version stale (v10.1.15)
**What happened:** README.md was still at 10.1.13 when the rest was at 10.1.15. Harness audit caught it.
**Root cause:** README was not in the version bump checklist for v10.1.14.
**Fix:** Added README.md to the mandatory version bump list.
**Prevention:** The pipeline now lists ALL 5 version files explicitly.

### Pre-commit reformats Python (v10.1.15)
**What happened:** Black formatter auto-reformatted the 4 new Python hook scripts. Commit failed because staging was stale.
**Root cause:** Pre-commit hooks run formatters that modify files after `git add`.
**Fix:** Re-stage the reformatted files before committing.
**Prevention:** After any `git commit` failure from pre-commit hooks, re-add the affected files and create a NEW commit (never amend).

### Router SKILL.md truncation (multiple)
**What happened:** Read tool returned only first 2000 lines of the router SKILL.md (>1100 lines). Did not realize the file was incomplete.
**Root cause:** Claude Code has a hard 2000-line Read limit with no warning on truncation.
**Fix:** Run `wc -l` before reading any file. If >2000 lines, read in chunks with offset/limit.
**Prevention:** The pipeline now mandates `wc -l` check before first Read of any unknown file.

---

## Design Failures

### SubagentStart hook COMPETED with router (v10.1.15)
**What happened:** Initially proposed 6 hooks including SubagentStart (inject context at agent start). The user challenged: "you sure the hooks not support the router? they compete?"
**Root cause:** SubagentStart would create a SECOND context injection path alongside the router's scaffold. If the two paths drifted, agents would receive inconsistent context.
**Fix:** Dropped SubagentStart and TaskCreated. Kept only 4 pure persistence/telemetry hooks.
**Prevention:** Apply the Challenge Test: "Does this SUPPORT or COMPETE with the router?"

### Accepting too many ACCEPTABLE patterns (v10.1.14 early draft)
**What happened:** Initial harmony mapping accepted 56 patterns. After cross-layer dedup and stricter review, only 29 survived.
**Root cause:** First-pass mappers were rating some ACCEPTABLE patterns as NATIVE because they "could work."
**Fix:** Tightened NATIVE criteria: "A developer reading the file would not be able to tell where the original text ends and the new text begins."
**Prevention:** The "could not tell where new text begins" test is now in the harmony rating criteria.

---

## Process Failures

### Bottom-up editing order matters (multiple)
**What happened:** Editing line 100 first, then line 200 second. But the first edit shifted line 200 to line 205. The second FIND block didn't match.
**Root cause:** Edits change line numbers for everything below them.
**Fix:** When multiple edits target the same file, apply them bottom-up (highest line number first).
**Prevention:** The plan template now specifies "bottom-up to preserve line numbers" for same-file edits.

### Plan file got stale from previous release (v10.1.16)
**What happened:** Plan file still contained v10.1.15 content when starting v10.1.16 work.
**Root cause:** Plan file is reused across sessions.
**Fix:** Completely rewrite the plan file at the start of each new release.
**Prevention:** Use Write (not Edit) for the plan file when starting a new release.

---

## What Always Works

| Practice | Why It Works | Release |
|----------|-------------|---------|
| Parallel extraction agents | 2x faster than sequential, no quality loss | All |
| 3 parallel harmony mappers | Each layer has different DNA criteria. Mappers catch patterns the others miss. | v10.1.14, v10.1.16 |
| Cross-layer dedup | Same pattern rated NATIVE by 2-3 layers → strongest patterns bubble up. Conflicts → conservative rejection. | v10.1.14, v10.1.16 |
| DNA fingerprint before every integration | CC10x evolves. Stale fingerprint → stale ratings. | All |
| "Could not tell where new text begins" test | The ultimate harmony test. If you can tell, it's not NATIVE. | v10.1.14 |
| Challenge Test ("support or compete?") | Caught 2 hooks that would have been accepted. | v10.1.15 |
| Harness audit after every release | Catches version mismatches, missing references, broken contracts | All |
| Reference benchmark after every release | Confirms CC10x still leads all reference repos (33/33) | v10.1.16 |
| User challenging assumptions | "you sure they don't compete?" was the most valuable input of v10.1.15 | v10.1.15 |
