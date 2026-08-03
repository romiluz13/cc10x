#!/usr/bin/env python3
"""Assert README counts/versions match disk + plugin.json. Exit 1 on any drift.

Counting rule (must match the README "1 router · N specialist agents · M skills"
marquee and the "## The N Agents" / "## The M Skills" headings):
- agents = every plugins/cc10x/agents/*.md
- skills = every plugins/cc10x/skills/*/ EXCEPT the router (cc10x-router),
           which the marquee counts separately as "1 router"
The version string everywhere must equal plugins/cc10x/.claude-plugin/plugin.json.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins" / "cc10x"

EXCLUDED_FROM_SKILL_COUNT = {"cc10x-router"}


def main() -> int:
    errors = []

    agents = sorted(p.stem for p in (PLUGIN / "agents").glob("*.md"))
    skill_dirs = sorted(p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir())
    skills = [s for s in skill_dirs if s not in EXCLUDED_FROM_SKILL_COUNT]
    n_agents, n_skills = len(agents), len(skills)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    version = json.loads(
        (PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )["version"]

    # Marquee counts
    m = re.search(r"(\d+)\s+specialist agents", readme)
    if not m:
        errors.append("README marquee 'N specialist agents' not found")
    elif int(m.group(1)) != n_agents:
        errors.append(f"README marquee agents={m.group(1)} but disk has {n_agents}")

    m = re.search(r"(\d+)\s+skills", readme)
    if not m:
        errors.append("README marquee 'N skills' not found")
    elif int(m.group(1)) != n_skills:
        errors.append(f"README marquee skills={m.group(1)} but disk has {n_skills}")

    # Section headings
    if f"## The {n_agents} Agents" not in readme:
        errors.append(f"README missing heading '## The {n_agents} Agents'")
    if f"## The {n_skills} Skills" not in readme:
        errors.append(f"README missing heading '## The {n_skills} Skills'")

    # Every agent named somewhere in the README
    for a in agents:
        if a not in readme:
            errors.append(f"agent '{a}' not mentioned in README")

    # Every skill dir must appear in the README file-tree block (the decorative
    # `skills/` tree silently drifted when skills were added — the marquee/table
    # updates are forced by n_skills, but nothing forced the tree). Locate the
    # fenced block that holds the skills tree (contains 'cc10x-router/') and
    # assert each skill dir name is present in it.
    tree_block = ""
    for block in re.findall(r"```[a-zA-Z]*\n(.*?)```", readme, re.DOTALL):
        if "cc10x-router/" in block and "skills/" in block:
            tree_block = block
            break
    if not tree_block:
        errors.append("README file-tree block (skills/ with cc10x-router/) not found")
    else:
        for s in skill_dirs:
            if s not in tree_block:
                errors.append(f"skill '{s}' missing from README file-tree block")

    # Version banner matches plugin.json
    if f"**Current version:** {version}" not in readme:
        errors.append(f"README banner version != plugin.json ({version})")

    # No 'cc10x v<other>' string contradicts plugin.json (catches phantom footers)
    for v in set(re.findall(r"cc10x v(\d+\.\d+\.\d+)", readme)):
        if v != version:
            errors.append(f"README 'cc10x v{v}' contradicts plugin.json {version}")

    # Marketplace manifest versions match plugin.json (the marketplace install
    # surface silently drifted from plugin.json because nothing asserted it).
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    meta_version = marketplace.get("metadata", {}).get("version")
    if meta_version != version:
        errors.append(
            f"marketplace.json metadata.version={meta_version} != plugin.json {version}"
        )
    plugin_entries = marketplace.get("plugins", [])
    if not plugin_entries:
        errors.append("marketplace.json has no plugins[] entries")
    else:
        entry_version = plugin_entries[0].get("version")
        if entry_version != version:
            errors.append(
                f"marketplace.json plugins[0].version={entry_version} != plugin.json {version}"
            )
    # The marketplace description embeds the version ("cc10x v12.8.0 - ...").
    for v in set(re.findall(r"cc10x v(\d+\.\d+\.\d+)", json.dumps(marketplace))):
        if v != version:
            errors.append(f"marketplace.json 'cc10x v{v}' contradicts plugin.json {version}")

    if errors:
        print("DOC CONSISTENCY: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"DOC CONSISTENCY: OK ({n_agents} agents, {n_skills} skills, v{version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
