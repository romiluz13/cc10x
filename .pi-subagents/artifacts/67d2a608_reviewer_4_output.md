## Review

### Scope covered
Read in full: `memory-and-handoff/SKILL.md` + all 4 references; `diff-driven-docs/SKILL.md` + `doc-target-heuristics.md` + both evals + eval README; `codebase-hygiene/SKILL.md`; `update/SKILL.md`; `doc-syncer.md`. Baseline diffs pulled via `git show v11.1.0:<path>` for `session-memory/SKILL.md` (293L), `handoff-package/SKILL.md` (157L), `diff-driven-docs/SKILL.md` (v11), `finding-duplicate-functions/SKILL.md` (92L), `codebase-deepening/SKILL.md` (117L), `update/SKILL.md` (461L), and `doc-syncer.md` history via `docs/known-flaws.md` FLAW-004. Current HEAD is `4985cfe` (v12.4.0), 40 commits past the v11.1.0 tag.

### Verdict per required check

**Item 27 — Scar-note convention: INTACT**
- Convention described: `skills/verification/SKILL.md:31` — "Gates are scar notes — they encode hard-won lessons."
- Actually used (not just described): `skills/exploration/SKILL.md:128` — `<!-- scar: 2026-06-17 — spike's "move fast, no tests" code promoted to production by inertia, skipping TDD/verifier gates. -->` — dated, explains the exact failure prevented, matches the format claimed.
- Origin traced to `docs/2026-06-17-upstream-steal-list.md:122` (item 54: "Per-rule dated 'why this gate exists' scar notes on Iron Laws/gates").
- **Note (LOW):** Only one literal `scar:` comment exists project-wide despite the convention being framed as general practice across "Iron Laws/gates." Adoption is thin — one instance, not a pervasive pattern across the many gated skills that could use it (e.g., `cc10x-router`, `verification`, `code-review` gates have no scar notes themselves, only the meta-description).

**Item 28 — Diff-driven docs 3-layer impact classifier: INTACT**
- Full 3-layer table present: `diff-driven-docs/SKILL.md` Impact Classifier section (Business/Technical/Audit columns), fast-path skip rule: "If all three layers are SKIP, set `IMPACT_LEVEL: none` and emit a SKIPPED contract immediately without opening any doc files."
- Wired into the agent: `doc-syncer.md` "Impact Classification" section assigns `IMPACT_LEVEL` and short-circuits on `none`.
- Evals confirm the classifier is exercised correctly for the two documented pressure cases (small-diff-skip-temptation, new-exported-function-no-UI-change) — both assert the agent must NOT wrongly skip.
- **Note (LOW):** Neither eval actually exercises the true `IMPACT_LEVEL: none` fast-path (both evals test that docs should NOT be skipped). No eval verifies the genuine skip path (test-only/style-only diff) is honored without wasted doc reads — a coverage gap, not a functional break.
- Minor formatting-only diff vs v11 baseline (table pipe spacing, blank lines) — no substantive content change except one dropped frontmatter line (`skills: - cc10x:verification-before-completion` removed from `diff-driven-docs/SKILL.md` frontmatter). This isn't a functional loss: the equivalent skill is loaded by the consuming agent instead — `doc-syncer.md` frontmatter still lists `cc10x:verification` under `skills:`.

**Item 29 — Handoff package (temp dir, path refs, secret redaction): INTACT**
- Temp dir: `memory-and-handoff/SKILL.md` HANDOFF PACKAGE mode, Rule 1 — "Write to OS temp dir, never into the repo. `HANDOFF="${TMPDIR:-/tmp}/handoff-$(date +%Y%m%d-%H%M%S).md"`. Print the absolute path."
- Path references not pasted content: Rule 2 — "Reference artifacts by path/URL, never paste contents."
- Secret redaction: Rule 3 — "Redact secrets and PII before writing. Replace with `<redacted:secret>`, `<redacted:pii>`."
- Wired into router: `cc10x-router/SKILL.md:402` — "Include `cc10x:memory-and-handoff` only when work is being handed to a coworker, a different tool, or a fresh non-cc10x session," and `:66` — "Create it using the `cc10x:memory-and-handoff` template."
- Consolidation of `handoff-package/SKILL.md` (157L) + `session-memory/SKILL.md` (293L) → `memory-and-handoff/SKILL.md` (184L body + 4 reference files) is documented in `CHANGELOG.md:165` ("450→113 lines, 75% cut") — content substance preserved through the merge, verified functionally equivalent by direct read.

**doc-syncer path/TaskUpdate check: INTACT (FLAW-004 fix holds)**
- `docs/known-flaws.md:77-83` — FLAW-004: doc-syncer previously read `.claude/cc10x/v10/` and lacked `TaskUpdate`; fixed in v11.0.0.
- Current `doc-syncer.md` frontmatter: `tools: Read, Edit, Write, Bash, Grep, Glob, TaskUpdate, Skill` — `TaskUpdate` present.
- Current `doc-syncer.md` "Memory First" section reads `.cc10x/activeContext.md`, `.cc10x/patterns.md`, `.cc10x/progress.md` — correct de-versioned path, no legacy path reference anywhere in the file.
- "Task Completion" section explicitly calls `TaskUpdate({ taskId: "{TASK_ID}", status: "completed" })` after emitting the contract.

**Memory finalization single-writer claim (item 13 cross-reference): INTACT / consistent**
- `memory-and-handoff/SKILL.md` Ownership section: "WRITE agents read memory but do NOT edit `.cc10x/*.md` directly," "WRITE agents emit structured `MEMORY_NOTES`," "READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`," "Router-owned memory-finalize task is the only final writer of memory markdown files."
- `references/memory-model-and-ownership.md` reinforces: WRITE Agents "do not edit `.cc10x/*.md` directly"; READ-ONLY Agents "never mutate markdown memory files."
- `references/memory-operations.md` "Router-Only Finalization Pattern" spells out exactly what the router's memory-finalize step persists, confirming single-writer ownership at the operational level.
- Cross-checked against `cc10x-router/SKILL.md` phase enum (line 114) which includes `memory-finalize` as a distinct router-owned phase, and lines 605/646/707 describing router extraction of `MEMORY_NOTES` and cleanup of `memory_task_id` — consistent, no contradiction found. The skill does not imply agents write memory.md directly anywhere in the text I read.

### Additional findings

- **MEDIUM — `update/SKILL.md` compression dropped explicit safety guidance.** v11.1.0 (461 lines) had an explicit Anti-Patterns table ("Don't `rm -rf` any directory → Do `mv` to timestamped backup"; "Don't use `jq` for JSON → Use `python3 -c`"; "Always `patch --dry-run` first"; "Auto-resolve conflicts → Ask user per conflict via `AskUserQuestion`") and an Edge Cases table (10 rows: diverged history, missing python3, registry drift, etc.). Current `update/SKILL.md` (82 lines) compresses this to one line each: "If conflict: report the conflict, show both versions, ask user to resolve" (no file:line — end of Phase 4) and `rm -rf "$CACHE_ROOT.old"` at line 82 with only "(only after user confirms)" as the safety rail. The underlying workflow (stash→pull→rebuild→rebase→verify) and tool grants (`AskUserQuestion` still in frontmatter line 12) are preserved, but the prescriptive safety detail that prevented specific failure modes (jq unavailability, unguarded rm -rf, non-dry-run patch conflicts) is gone. This is a real regression in explicitness even if the five-phase skeleton survived — flag for follow-up, not blocking.
- **LOW — stale path reference outside reviewed scope.** `plugins/cc10x/tests/live/manifests/cc10x-bootstrap.json:46` references `python3 plugins/cc10x/scripts/cc10x_doc_consistency_check.py`, but the actual file lives at `plugins/cc10x/tools/doc_consistency_check.py` (confirmed via `find`; `plugins/cc10x/scripts/` contains only hook scripts, no `cc10x_doc_consistency_check.py`). `update/SKILL.md:80` itself correctly references `$CACHE_ROOT/tools/doc_consistency_check.py`, so the update skill is fine — but the test manifest is stale. Outside my assigned file scope; noting for the codebase-hygiene angle since it's a real broken reference.
- **LOW — codebase-hygiene merge dropped some rationalization/red-flag tables.** v11's `finding-duplicate-functions/SKILL.md` had a "Common Mistakes" table and `codebase-deepening/SKILL.md` had "Red Flags — STOP" and "Rationalization Prevention" tables; current `codebase-hygiene/SKILL.md` retains the Deletion Test, Two-Adapters Rule, High-Risk Zones, and Consolidation Discipline (core mechanics intact) but drops those two anti-pattern tables. Functional core is INTACT/IMPROVED (single 2-mode skill, less duplication across two files); the softer guardrail prose is WEAKENED.

### Publish-readiness verdict

This area is publish-ready. All three specifically-flagged innovations (scar-notes, 3-layer impact classifier with fast-path skip, handoff package with temp-dir/path-refs/redaction) are functionally intact and verifiable in the current code, not just described in prose; the doc-syncer FLAW-004 fix (`.cc10x/` path + `TaskUpdate`) holds at HEAD; and the memory-finalize single-writer model is stated consistently across `memory-and-handoff/SKILL.md` and its four reference files with no contradiction. The one real risk is the `update/SKILL.md` compression (461→82 lines), which lost explicit anti-pattern/edge-case prescriptions (jq-vs-python3, dry-run-before-patch, rm-rf guardrails) — worth a follow-up pass to re-inject the safety rail as short bullet reminders, but it does not block publishing since the workflow skeleton and tool grants are unchanged.