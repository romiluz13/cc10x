---
name: mcp-cli
description: "Use when you need a one-off MCP server capability during research or debugging without permanently mounting it as a context-polluting integration."
allowed-tools: Read Bash
user-invocable: false
---

# MCP CLI (Transient MCP Access)

## Overview

The `mcp` CLI (from `github.com/f/mcptools`) discovers and invokes MCP server capabilities on-demand, then releases them. Use it when a task needs ONE server's tool — a doc fetch, a single query, a quick lookup — instead of permanently mounting that server as an always-loaded integration.

This keeps accelerators **transient**: spun up for the task, used, and dropped. A permanently mounted MCP server costs context on every session whether you call it or not. The CLI costs nothing until you run it. This is the same context-hygiene principle behind disabling unused MCP servers in monthly `/mcp` review.

Composes with `cc10x:research` (transient retrieval, used then released, never resident).

## Prerequisite (install once)

Check first: `command -v mcp`. If absent, install:

```bash
git clone https://github.com/f/mcptools /tmp/mcptools
CGO_ENABLED=0 go build -o ~/.local/bin/mcp /tmp/mcptools/cmd/mcptools
# ensure ~/.local/bin is on PATH
```

If `go` is unavailable, report that the accelerator is missing and proceed with built-in tools — do NOT treat the missing binary as a task blocker (it is a fallback message, not a wall).

## Flow: discover → call → release

**1. Discover first — always.** Never call a tool whose schema you have not seen.

```bash
mcp tools <server-command>                 # list tools
mcp tools --format json <server-command>   # full param schema for parsing
mcp resources <server-command>             # list resources
mcp prompts <server-command>               # list prompts
```

**2. Lead read-only when exploring.** Restrict the surface before you touch an unfamiliar server:

```bash
mcp guard --allow 'tools:read_*,list_*' --deny 'tools:write_*,delete_*' <server-command>
```

Drop the guard only once you know exactly which write you intend.

**3. Call** with params matching the discovered signature exactly (`param:str`, `param:num`, `[optional]`):

```bash
mcp call <tool_name> --params '<json>' -f json <server-command>
```

Output `-f json` for parsing, `-f pretty` for reading. Check exit code and stderr on failure — a non-zero exit is a real error, not a fallback message.

**Server-command examples:**
- stdio: `npx -y @modelcontextprotocol/server-filesystem /path`
- HTTP: pass the URL (auto-detected); SSE via `--transport sse`
- auth: `--auth-header "Bearer <token>"`, `--auth-user user:pass`, or `-e ENV_VAR` for docker servers

## Aliases (only for repeated use in one task)

If you call the same server several times, alias it; remove it when the task ends so nothing lingers:

```bash
mcp alias add <name> <server-command>   # then: mcp tools <name>, mcp call ... <name>
mcp alias remove <name>                 # release when done
```

Aliases persist in `~/.mcpt/aliases.json`. Cleaning them up is part of keeping the accelerator transient.

## Discipline

- Discover before calling; match param signatures exactly.
- Use JSON output when a downstream step parses the result.
- Guard to read-only while exploring; widen only with intent.
- Release aliases when the task is done — do not leave a transient tool resident.
