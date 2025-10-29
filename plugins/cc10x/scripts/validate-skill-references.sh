#!/usr/bin/env bash
set -euo pipefail

# Validate that all skills referenced by subagents exist under plugins/cc10x/skills/
# Portable (macOS/BSD + GNU) and CI-friendly.

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILLS_DIR="$ROOT_DIR/plugins/cc10x/skills"
SUBAGENTS_DIR="$ROOT_DIR/plugins/cc10x/subagents"

if [[ ! -d "$SKILLS_DIR" ]] || [[ ! -d "$SUBAGENTS_DIR" ]]; then
  echo "Error: Expected directories not found:"
  echo "  $SKILLS_DIR"
  echo "  $SUBAGENTS_DIR"
  exit 2
fi

# Build set of existing skill names by locating SKILL.md files
# Result: one name per line
existing_skills=$(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type f -name 'SKILL.md' \
  | sed -E 's#.*/skills/([^/]+)/SKILL.md#\1#' \
  | sort -u)

# Function: trim whitespace
trim() { sed -E 's/^ +//; s/ +$//'; }

missing_count=0

# Iterate all subagent definition files
while IFS= read -r subfile; do
  # Collect references from patterns commonly used in our repo:
  # 1) Markdown bullets: - **skill-name**
  # 2) Inline list: Skills Loaded: skill-a, skill-b

  refs_from_bullets=$(grep -hoE '\*\*[a-z0-9-]+\*\*' "$subfile" 2>/dev/null | sed 's/\*//g' || true)

  # Normalize and de-duplicate
  refs=$(printf "%s\n" "$refs_from_bullets" \
         | sed -E 's/[`*]//g; s/^[-0-9. )]+//; s/[[:space:]]+$//' \
         | tr -d '\r' \
         | grep -E '^[a-z0-9][a-z0-9-]*$' \
         | sort -u || true)

  # Check each reference exists
  while IFS= read -r skill; do
    [[ -z "$skill" ]] && continue
    if ! echo "$existing_skills" | grep -qx "$skill"; then
      echo "Missing skill reference: $skill in ${subfile#$ROOT_DIR/}"
      missing_count=$((missing_count + 1))
    fi
  done <<< "$refs"

done < <(find "$SUBAGENTS_DIR" -type f \( -name 'SUBAGENT.md' -o -name 'SKILL.md' \) | sort)

if [[ $missing_count -gt 0 ]]; then
  echo "\nERROR: $missing_count missing skill reference(s) found."
  echo "Hint: Add the missing skills under plugins/cc10x/skills/<name>/SKILL.md or update the subagent references."
  exit 1
fi

echo "All subagent skill references are valid. ($(/usr/bin/wc -l <<<"$existing_skills" | tr -d ' ' ) skills)"

