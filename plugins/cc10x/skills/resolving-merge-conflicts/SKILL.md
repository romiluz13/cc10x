---
name: resolving-merge-conflicts
description: |
  Resolve an in-progress git merge or rebase conflict hunk by hunk — see the
  state, find the primary sources for each side's intent, resolve by intent
  (never --abort), run the project's checks, and finish the operation. Model-
  invoked: agents reach for it when a git operation reports conflicts.
allowed-tools: Read Bash Grep Glob
user-invocable: false
---

<!-- Upstream: github.com/mattpocock/skills @ e9fcdf95 (skills/engineering/resolving-merge-conflicts)
     Classification: ADAPTED (cc10x frontmatter + output conventions; 5-step body is Matt's). -->

# Resolving Merge Conflicts

Work through an in-progress git merge or rebase conflict **hunk by hunk**, resolving each by intent traced to each side's primary source. **Never `--abort`.** Always resolve; `--abort` throws away work and hides the real incompatibility.

## The 5 steps

### 1. See the current state

Check git status, the conflicting files, and the conflict markers:

```bash
git status
git diff --name-only --diff-filter=U   # the unmerged paths
```

Read each conflicting file's conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) to see exactly what's contested. Know whether you're in a merge (`MERGE_HEAD` set) or a rebase (`rebase-merge/` or `rebase-apply/` present in `.git/`).

### 2. Find the primary sources for each side

For each conflict hunk, understand **why** each change was made and what its original intent was — don't just pick the bigger diff. Read:

- The commit messages on both sides (`git log --oneline -5 -- <file>` for each side)
- The PRs or issues/tickets the commits reference
- The surrounding code to confirm what each side was trying to achieve

### 3. Resolve each hunk by intent

For each hunk:

- **Preserve both intents where possible** — the two sides usually want different things; merge both.
- **Where incompatible**, pick the one matching the merge's stated goal (the feature, the fix, the branch's purpose) and **note the trade-off** in the commit message — what was given up and why.
- **Never invent new behavior.** A conflict resolution is not a place to add new code neither side wrote.
- **Always resolve.** Never `--abort`, never leave markers, never pick one side blind.

### 4. Run the project's automated checks

Discover the project's checks and run them in order — typically typecheck, then tests, then format:

```bash
# node: npx tsc --noEmit (or per package.json scripts)
# python: ruff check . && python -m pytest -q
# go: go build ./... && go test ./...
```

Fix anything the merge broke. A conflict resolution that breaks the build is not a resolution — it's a larger conflict.

### 5. Finish the merge/rebase

Stage everything and commit:

```bash
git add <resolved-files>
git commit   # merge: completes the merge commit
# rebase: git rebase --continue (repeat for each conflicted commit until done)
```

If rebasing, continue the rebase process until ALL commits are rebased. Do not stop mid-rebase.

## Hard rules

- **Never `git merge --abort` or `git rebase --abort`.** Abort throws away the work and the incompatibility.
- **Never leave conflict markers in a committed file.** `grep -rn '^<<<<<<< \|^=======$\|^>>>>>>> ' .` must return nothing before you commit.
- **Never invent new behavior** during a resolution — only reconcile the two existing intents.
