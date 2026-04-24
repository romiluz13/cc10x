#!/usr/bin/env python3
"""Context migration script for CC10X version upgrades.

Merges valuable content from previous state version directories into the
current STATE_VERSION on first SessionStart after an upgrade.  Idempotent
via a ``.migrated`` marker file inside the target state root.
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Set

from cc10x_hooklib import (
    STATE_VERSION,
    extract_bullets,
    load_input,
    log_event,
    normalize_bullet,
    now_iso,
    parse_markdown_sections,
    project_dir,
    session_context,
    state_root,
)

# ---------------------------------------------------------------------------
# Contract headings that are safe to merge into
# ---------------------------------------------------------------------------

PATTERNS_HEADINGS: Set[str] = {
    "User Standards",
    "Architecture Patterns",
    "Code Conventions",
    "File Structure",
    "Testing Patterns",
    "Common Gotchas",
    "API Patterns",
    "Error Handling",
    "Dependencies",
    "Project SKILL_HINTS",
}

ACTIVE_CONTEXT_HEADINGS: Set[str] = {
    "Decisions",
    "Learnings",
}

PROGRESS_HEADINGS: Set[str] = {
    "Completed",
    "Verification",
}

# ---------------------------------------------------------------------------
# Templates — used when a target file does not yet exist
# ---------------------------------------------------------------------------

ACTIVE_CONTEXT_TEMPLATE = """\
# Active Context
<!-- CC10X: Do not rename headings. Used as Edit anchors. -->

## Current Focus

## Recent Changes

## Next Steps

## Decisions

## Learnings

## References

## Blockers

## Session Settings
# AUTO_PROCEED: false

## Last Updated
"""

PATTERNS_TEMPLATE = """\
# Project Patterns
<!-- CC10X MEMORY CONTRACT: Do not rename headings. Used as Edit anchors. -->

## User Standards

## Architecture Patterns

## Code Conventions

## File Structure

## Testing Patterns

## Common Gotchas

## API Patterns

## Error Handling

## Dependencies

## Project SKILL_HINTS

## Last Updated
"""

PROGRESS_TEMPLATE = """\
# Progress Tracking
<!-- CC10X: Do not rename headings. Used as Edit anchors. -->

## Current Workflow

## Tasks

## Completed

## Verification

## Last Updated
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _version_sort_key(dirname: str) -> int:
    """Extract numeric version from ``vN`` directory name."""
    if dirname.startswith("v") and dirname[1:].isdigit():
        return int(dirname[1:])
    return -1  # legacy (root) sorts first


def _current_version_number() -> int:
    """Return the integer portion of STATE_VERSION (e.g. ``v10`` -> 10)."""
    if STATE_VERSION.startswith("v") and STATE_VERSION[1:].isdigit():
        return int(STATE_VERSION[1:])
    return 0


def _discover_sources(cc10x_base: Path) -> List[Dict[str, Any]]:
    """Find all migration sources ordered oldest-first."""
    sources: List[Dict[str, Any]] = []
    current_num = _current_version_number()

    # Legacy root-level files
    if (cc10x_base / "activeContext.md").exists():
        sources.append({"label": "legacy", "path": cc10x_base, "sort_key": -1})

    # Versioned directories
    if cc10x_base.is_dir():
        for child in sorted(cc10x_base.iterdir()):
            if not child.is_dir():
                continue
            name = child.name
            if not (name.startswith("v") and name[1:].isdigit()):
                continue
            ver_num = int(name[1:])
            if ver_num >= current_num:
                continue  # skip current and future versions
            # Must have at least one memory file
            if any((child / f).exists() for f in ("activeContext.md", "patterns.md", "progress.md")):
                sources.append({"label": name, "path": child, "sort_key": ver_num})

    sources.sort(key=lambda s: s["sort_key"])
    return sources


def _load_migrated(target_root: Path) -> Dict[str, Any]:
    """Load the .migrated marker file, or return empty structure."""
    marker = target_root / ".migrated"
    if not marker.exists():
        return {"version": STATE_VERSION, "migrations": []}
    try:
        return json.loads(marker.read_text(encoding="utf-8"))
    except Exception:
        return {"version": STATE_VERSION, "migrations": []}


def _save_migrated(target_root: Path, data: Dict[str, Any]) -> None:
    """Atomically write the .migrated marker."""
    marker = target_root / ".migrated"
    tmp = marker.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")
    tmp.replace(marker)


def _already_migrated(migrated: Dict[str, Any], label: str) -> bool:
    """Check if a source has already been migrated."""
    return any(m.get("source") == label for m in migrated.get("migrations", []))


def _ensure_file(path: Path, template: str) -> None:
    """Create a memory file from template if it doesn't exist."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template, encoding="utf-8")


def _backup(path: Path) -> None:
    """Create a .pre-migration.bak copy if the file exists."""
    if path.exists():
        bak = path.with_suffix(".pre-migration.bak")
        if not bak.exists():  # don't overwrite an existing backup
            shutil.copy2(path, bak)


def _merge_sections(
    source_text: str,
    target_text: str,
    allowed_headings: Set[str],
) -> tuple[str, int]:
    """Merge bullets from source sections into target sections.

    Returns the updated target text and the count of bullets added.
    """
    source_sections = parse_markdown_sections(source_text)
    target_sections = parse_markdown_sections(target_text)

    total_added = 0

    for heading in allowed_headings:
        if heading not in source_sections:
            continue
        source_bullets = extract_bullets(source_sections[heading])
        if not source_bullets:
            continue

        # Build dedup set from existing target bullets
        existing: Set[str] = set()
        if heading in target_sections:
            for b in extract_bullets(target_sections[heading]):
                existing.add(normalize_bullet(b))

        new_bullets: List[str] = []
        for bullet in source_bullets:
            norm = normalize_bullet(bullet)
            if norm and norm not in existing:
                new_bullets.append(bullet.rstrip())
                existing.add(norm)

        if not new_bullets:
            continue

        total_added += len(new_bullets)

        # Insert new bullets into the target text after the heading line
        anchor = f"## {heading}"
        if anchor in target_text:
            insert_block = "\n".join(new_bullets)
            target_text = target_text.replace(
                anchor, f"{anchor}\n{insert_block}", 1
            )
        # If the heading doesn't exist in target but is in the contract,
        # insert it before ## Last Updated
        elif "## Last Updated" in target_text:
            section_block = f"## {heading}\n" + "\n".join(new_bullets) + "\n\n"
            target_text = target_text.replace(
                "## Last Updated", f"{section_block}## Last Updated", 1
            )

    return target_text, total_added


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    data = load_input()
    _ = data  # consumed for hook contract compliance

    target_root = state_root()
    cc10x_base = project_dir() / ".claude" / "cc10x"

    if not cc10x_base.exists():
        return 0  # fresh install, nothing to migrate

    sources = _discover_sources(cc10x_base)
    if not sources:
        return 0  # nothing to migrate

    migrated = _load_migrated(target_root)
    pending = [s for s in sources if not _already_migrated(migrated, s["label"])]

    if not pending:
        return 0  # all sources already migrated

    # Ensure target files exist with proper templates
    _ensure_file(target_root / "patterns.md", PATTERNS_TEMPLATE)
    _ensure_file(target_root / "activeContext.md", ACTIVE_CONTEXT_TEMPLATE)
    _ensure_file(target_root / "progress.md", PROGRESS_TEMPLATE)

    # Back up target files before any modifications
    _backup(target_root / "patterns.md")
    _backup(target_root / "activeContext.md")
    _backup(target_root / "progress.md")

    total_bullets = 0
    migrated_labels: List[str] = []

    for source in pending:
        source_path: Path = source["path"]
        label: str = source["label"]
        source_bullets = 0
        files_merged: List[str] = []

        # --- patterns.md (full section merge) ---
        src_patterns = source_path / "patterns.md"
        if src_patterns.exists():
            tgt_text = (target_root / "patterns.md").read_text(encoding="utf-8")
            src_text = src_patterns.read_text(encoding="utf-8")
            updated, count = _merge_sections(src_text, tgt_text, PATTERNS_HEADINGS)
            if count > 0:
                tmp = (target_root / "patterns.md").with_suffix(".tmp")
                tmp.write_text(updated, encoding="utf-8")
                tmp.replace(target_root / "patterns.md")
                files_merged.append("patterns.md")
                source_bullets += count

        # --- activeContext.md (Decisions + Learnings only) ---
        src_active = source_path / "activeContext.md"
        if src_active.exists():
            tgt_text = (target_root / "activeContext.md").read_text(encoding="utf-8")
            src_text = src_active.read_text(encoding="utf-8")
            updated, count = _merge_sections(src_text, tgt_text, ACTIVE_CONTEXT_HEADINGS)
            if count > 0:
                tmp = (target_root / "activeContext.md").with_suffix(".tmp")
                tmp.write_text(updated, encoding="utf-8")
                tmp.replace(target_root / "activeContext.md")
                files_merged.append("activeContext.md")
                source_bullets += count

        # --- progress.md (Completed + Verification only) ---
        src_progress = source_path / "progress.md"
        if src_progress.exists():
            tgt_text = (target_root / "progress.md").read_text(encoding="utf-8")
            src_text = src_progress.read_text(encoding="utf-8")
            updated, count = _merge_sections(src_text, tgt_text, PROGRESS_HEADINGS)
            if count > 0:
                tmp = (target_root / "progress.md").with_suffix(".tmp")
                tmp.write_text(updated, encoding="utf-8")
                tmp.replace(target_root / "progress.md")
                files_merged.append("progress.md")
                source_bullets += count

        # Record migration
        migration_record = {
            "source": label,
            "timestamp": now_iso(),
            "files_merged": files_merged,
            "bullets_added": source_bullets,
        }
        migrated["migrations"].append(migration_record)
        _save_migrated(target_root, migrated)

        total_bullets += source_bullets
        migrated_labels.append(label)

        log_event(
            "context_migration",
            {
                "source": label,
                "target": STATE_VERSION,
                "files_merged": files_merged,
                "bullets_added": source_bullets,
                "decision": "merge",
                "reason": "version_upgrade",
            },
        )

    # Emit session context so Claude knows migration occurred
    if total_bullets > 0:
        sources_str = ", ".join(migrated_labels)
        session_context(
            f"CC10X context migration: merged {total_bullets} items from "
            f"[{sources_str}] into {STATE_VERSION}. "
            f"Historical decisions, learnings, patterns, and verification "
            f"evidence have been preserved."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
