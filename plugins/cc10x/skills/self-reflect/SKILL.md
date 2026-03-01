---
name: self-reflect
description: "Extract learnings from current session and update patterns.md. Mines conversation context for high-value insights: architectural decisions, gotchas, non-obvious behaviors. Quality over quantity."
allowed-tools: Read, Edit, Bash, Grep, AskUserQuestion
---

# Self-Reflect

**Philosophy:** Be judicious. Quality over quantity. Each learning must make future sessions measurably better.

## When to Use

Run after: complex debugging (5+ cycles), multi-file refactoring, architectural decisions, surprising discoveries, completed workflows.

## Phase A: Mine Session Context

Scan the current conversation window for these high-value signal patterns:

| Pattern | Usually Indicates | Value |
|---------|------------------|-------|
| "The problem was..." | Debugging insight | High |
| "It turns out..." | Discovery moment | High |
| "We decided to..." | Architectural decision | Very High |
| "The reason we..." | Rationale worth preserving | Very High |
| "Unlike what you'd expect..." | Non-obvious behavior | High |
| "Never do X because..." | Gotcha/pitfall | High |
| DEBUG-N cycles (3+) | Repeated mistakes | High |
| "Deferred:" entries in Memory Notes | Pending gotchas | Medium |

**Filter — only capture insights that are ALL of:**
- Codebase-specific OR cc10x-specific (not universal programming truisms)
- Non-obvious (would surprise a skilled developer)
- Actionable (agent can change behavior based on it)
- Durable (still relevant next session)

## Phase B: Load Existing Patterns (Deduplication)

```
Read(file_path=".claude/cc10x/patterns.md")
```

Check `## Common Gotchas` for semantic duplicates before proposing candidates.

## Phase C: Present Candidates

Present learnings as numbered list:

```markdown
## Candidate Learnings

1. **[Brief title]** — [One sentence. Type: pattern|gotcha|decision|api_behavior]
   Why accepted: [Reason it meets all 4 filter criteria]

2. **[Brief title]** — [One sentence]
   Why accepted: [Reason]

---

Which numbers do you want to capture? (all / 1,2,3 / none)
```

## Phase D: Classify and Confirm

For each approved learning, confirm interactively:

```
Fact: [extracted core insight]
Type: [pattern|gotcha|decision|behavior|security|performance]
Applies to: [file patterns or components affected]
Confidence: [high|medium|low]

Does this look right? (yes / edit / skip)
```

**Conflict resolution:**
| Situation | Action |
|-----------|--------|
| New is more specific/accurate | New supersedes old — update in-place |
| Both capture different aspects | Keep both, add distinguishing context |
| New contradicts old | Ask user which is correct |
| Old is subset of new | Merge into comprehensive entry |

## Phase E: Write to patterns.md

For each confirmed learning, use Read-Edit-Verify pattern:

```
Read(file_path=".claude/cc10x/patterns.md")
# If Read returns "file not found" error:
#   Write(file_path=".claude/cc10x/patterns.md", content="# Project Patterns\n<!-- CC10X MEMORY CONTRACT: Do not rename headings. Used as Edit anchors. -->\n\n## Common Gotchas\n")
#   Then proceed with Edit below.

Edit(file_path=".claude/cc10x/patterns.md",
     old_string="## Common Gotchas",
     new_string="## Common Gotchas\n- [Fact in imperative mood, includes WHY]: [solution/implication]\n")

Read(file_path=".claude/cc10x/patterns.md")  # Verify
```

**Canonicalization rules (apply before writing):**
1. Remove session-specific references ("in this session...", "task #42...") — keep the principle
2. Use imperative mood: "Consider X" → "Use X"
3. Include the WHY: "Use X" → "Use X because Y"
4. Keep under 200 characters when possible
5. Generalize file paths: `src/lib/specific.ts` → `src/lib/**/*.ts`

## Phase F: Report

```markdown
## Self-Reflection Results

### Summary
- Session patterns scanned: [estimated items reviewed]
- Candidates proposed: [count]
- Accepted: [count]
- Rejected (low value): [count]
- Total new facts written: [count]

### Learnings Added
[list each with type and why accepted]

### Rejected / Deferred
[list with reason for rejection]
```

## Anti-Patterns

1. **Quantity over quality** — 10 great facts beat 100 mediocre ones
2. **Missing the WHY** — "Use X" without reason is less useful
3. **Over-specificity** — "Use X in file Y on line 34" → generalize
4. **Under-specificity** — "Write good tests" is not actionable — skip it
5. **Ignoring duplicates** — Always check patterns.md before adding
6. **Blindly capturing everything** — Apply the 4-filter test (codebase-specific, non-obvious, actionable, durable)
