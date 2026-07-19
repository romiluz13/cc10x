# Memory Operations

## Purpose

This file records the detailed file-operation rules behind CC10X memory.

Ownership: see SKILL.md `### Ownership` — the authoritative statement.

These patterns matter for router maintenance, template repair, and manual audits.

## Permission-Free Rules

| Operation | Preferred tool | Rule |
|-----------|----------------|------|
| read memory | `Read(...)` | always use direct reads |
| create directory | `Bash("mkdir -p ...")` | single simple command only |
| create missing file | `Write(...)` | only when the file does not exist |
| update existing file | `Edit(...)` | do not use overwrite-style `Write(...)` |

Avoid:

- compound bash commands such as `mkdir && cat ...`
- heredoc writes such as `cat > file <<'EOF'`
- overwriting existing memory files when a targeted `Edit(...)` will do

## Read-Edit-Verify Pattern

When router or maintenance code updates memory markdown:

1. `Read(...)` the file
2. verify the anchor exists
3. `Edit(...)` with a small targeted change
4. `Read(...)` again and confirm the change landed

If the anchor is missing:

- stop
- re-read the file
- add the missing canonical section using the file contract rules
- retry with the corrected anchor

## Router-Only Finalization Pattern

The router memory-finalize step:

- reads the workflow artifact and memory task payload
- persists learnings to `activeContext.md ## Learnings`
- persists reusable gotchas to `patterns.md ## Common Gotchas`
- persists verification truth to `progress.md ## Verification`
- writes deferred items as `[Deferred]: ...` under `patterns.md ## Common Gotchas`
- refreshes `progress.md ## Tasks`
- trims `progress.md ## Completed`
- removes the matching `[cc10x-internal] memory_task_id` line

## Minimal Examples

### Create the directory

```bash
mkdir -p .cc10x
```

### Read memory files

```text
Read(file_path=".cc10x/activeContext.md")
Read(file_path=".cc10x/patterns.md")
Read(file_path=".cc10x/progress.md")
```

### Add a missing canonical section

```text
Edit(
  file_path=".cc10x/activeContext.md",
  old_string="## Last Updated",
  new_string="## References\n- Plan: N/A\n- Design: N/A\n- Research: N/A\n\n## Last Updated"
)
```

### Append verification evidence

```text
Edit(
  file_path=".cc10x/progress.md",
  old_string="## Verification",
  new_string="## Verification\n- `npm test` -> exit 0"
)
```

### Verify the write

```text
Read(file_path=".cc10x/progress.md")
```
