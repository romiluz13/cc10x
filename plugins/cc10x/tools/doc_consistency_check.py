#!/usr/bin/env python3
"""Assert README counts/versions match disk + plugin.json. Exit 1 on any drift.

Counting rule (must match the README "1 router · N specialist agents · M skills"
marquee and the "## The N Agents" / "## The M Skills" headings):
- agents = every plugins/cc10x/agents/*.md
- skills = every plugins/cc10x/skills/*/ EXCEPT the router (cc10x-router),
           which the marquee counts separately as "1 router"
The version string everywhere must equal plugins/cc10x/.claude-plugin/plugin.json.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

if os.environ.get("CC10X_REPO_ROOT") == "":
    raise SystemExit("CC10X_REPO_ROOT is set but empty: unset it or point it at a cc10x repo")
ROOT = Path(os.environ.get("CC10X_REPO_ROOT") or Path(__file__).resolve().parents[3])
if not (ROOT / "plugins" / "cc10x").is_dir():
    raise SystemExit(f"CC10X_REPO_ROOT is not a cc10x repo (no plugins/cc10x): {ROOT}")
PLUGIN = ROOT / "plugins" / "cc10x"

EXCLUDED_FROM_SKILL_COUNT = {"cc10x-router"}
DOCS_ROT_BASELINE = PLUGIN / "tools" / "docs_rot_baseline.json"


_ROUTER_ROW = re.compile(r"^\| \d+ \| ", re.M)
_HOOK_EVENT_ROW = re.compile(r"^\| `([A-Za-z]+)` \|", re.M)
_HOOK_CLAIM = re.compile(r"^(?!\|).*?\b(\d+) (?:\w+-)?hooks\b", re.M)
_PERCENT_LEANER = re.compile(r"\d+\s*%\s*leaner", re.I)


def check_claims(root: Path = ROOT) -> dict[str, str]:
    """Count and claim failures as `<check>:<subject>` keys; harness_audit's ratchet decides what fails."""
    plugin = root / "plugins" / "cc10x"
    failures: dict[str, str] = {}
    readme = (root / "README.md").read_text(encoding="utf-8")

    router = (plugin / "skills" / "cc10x-router" / "SKILL.md").read_text(encoding="utf-8")
    table = router.split("## 1. Intent Routing", 1)[-1].split("\n---", 1)[0]
    rows = len(_ROUTER_ROW.findall(table))
    match = re.search(r"<strong>(\d+) workflows</strong>", readme)
    if not match or int(match.group(1)) != rows:
        claimed = match.group(1) if match else "no"
        failures["readme-workflow-count"] = f"README claims {claimed} workflows but the router routing table has {rows} rows"

    hooks = json.loads((plugin / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    section = readme.split("### Hooks", 1)[-1].split("\n### ", 1)[0]
    documented = set(_HOOK_EVENT_ROW.findall(section))
    if documented != set(hooks):
        failures["readme-hook-count"] = (
            f"README hook table lists {len(documented)} events ({', '.join(sorted(documented ^ set(hooks)))} differ) "
            f"but hooks.json registers {len(hooks)}"
        )
    for claim in _HOOK_CLAIM.findall(readme):
        if int(claim) != len(hooks):
            failures["readme-hook-count"] = f"README claims {claim} hooks but hooks.json registers {len(hooks)} events"

    guide = (plugin / "skills" / "cc10x-guide" / "SKILL.md").read_text(encoding="utf-8")
    n_agents = len(list((plugin / "agents").glob("*.md")))
    n_skills = len([p for p in (plugin / "skills").iterdir() if p.is_dir() and p.name not in EXCLUDED_FROM_SKILL_COUNT])
    for label, found, disk in (
        ("agent", re.search(r"(\d+) specialist agents", guide), n_agents),
        ("skill", re.search(r"(\d+) skills", guide), n_skills),
    ):
        if not found or int(found.group(1)) != disk:
            claimed = found.group(1) if found else "no"
            failures[f"guide-{label}-count"] = f"cc10x-guide claims {claimed} {label}s but disk has {disk}"

    plugin_json = json.loads((plugin / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entry = (marketplace.get("plugins") or [{}])[0]
    descriptions = {
        "plugin.json": [plugin_json.get("description", "")],
        "marketplace.json": [marketplace.get("metadata", {}).get("description", ""), entry.get("description", "")],
    }
    for name, texts in descriptions.items():
        if any(_PERCENT_LEANER.search(text) for text in texts):
            failures[f"manifest-unverifiable-claim:{name}"] = f"{name} description carries an unverifiable '<N>% leaner' claim"
    if plugin_json.get("description") != entry.get("description"):
        failures["manifest-description-mismatch"] = "plugin.json description differs from marketplace.json plugins[0].description"
    if set(plugin_json.get("keywords", [])) != set(entry.get("keywords", [])):
        failures["manifest-keywords-mismatch"] = "plugin.json keywords differ from marketplace.json plugins[0].keywords"
    return failures


def load_rot_baseline(path: Path = DOCS_ROT_BASELINE) -> tuple[list[dict], list[str]]:
    """Return (entries, errors); a missing or malformed file is an error, never a traceback."""
    if not path.exists():
        return [], [f"docs rot baseline is missing: {path.name} (an empty baseline is {{\"entries\": []}})"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"docs rot baseline {path.name} is not valid JSON: {exc}"]
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return [], [f"docs rot baseline {path.name} must be an object with an 'entries' list"]
    errors = [f"docs rot baseline entry is not an object: {item!r}" for item in entries if not isinstance(item, dict)]
    return [item for item in entries if isinstance(item, dict)], errors


def rot_errors(failures: dict[str, str], known: dict[str, dict]) -> list[str]:
    """Failures absent from the baseline are new rot; a baselined failure whose message changed got worse."""
    errors = [f"new rot: {key}: {failures[key]}" for key in sorted(set(failures) - set(known))]
    errors.extend(
        f"baseline message drifted: {key} (baseline: {known[key].get('message')!r}; live: {failures[key]!r})"
        for key in sorted(set(known) & set(failures))
        if known[key].get("message") != failures[key]
    )
    return errors


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
        if "version" in plugin_entries[0]:
            errors.append(
                "marketplace.json plugins[0] must not duplicate the version: plugin.json owns it"
            )
    # The marketplace description embeds the version ("cc10x v12.8.0 - ...").
    for v in set(re.findall(r"cc10x v(\d+\.\d+\.\d+)", json.dumps(marketplace))):
        if v != version:
            errors.append(f"marketplace.json 'cc10x v{v}' contradicts plugin.json {version}")

    baseline, baseline_errors = load_rot_baseline()
    errors.extend(baseline_errors)
    known = {item["key"]: item for item in baseline if isinstance(item.get("key"), str)}
    errors.extend(rot_errors(check_claims(), known))

    if errors:
        print("DOC CONSISTENCY: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"DOC CONSISTENCY: OK ({n_agents} agents, {n_skills} skills, v{version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
