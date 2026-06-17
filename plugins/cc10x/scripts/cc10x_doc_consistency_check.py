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

    # Version banner matches plugin.json
    if f"**Current version:** {version}" not in readme:
        errors.append(f"README banner version != plugin.json ({version})")

    # No 'cc10x v<other>' string contradicts plugin.json (catches phantom footers)
    for v in set(re.findall(r"cc10x v(\d+\.\d+\.\d+)", readme)):
        if v != version:
            errors.append(f"README 'cc10x v{v}' contradicts plugin.json {version}")

    if errors:
        print("DOC CONSISTENCY: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"DOC CONSISTENCY: OK ({n_agents} agents, {n_skills} skills, v{version})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
