#!/usr/bin/env python3
"""Resolve, verify and write the QA route's machine-local topology record.

A system's topology -- which services run, how they are wired, the order they
come up in, the data stores and the gotchas a past run learned the hard way --
is the same on every QA run against that system. Without a record, every run
reconstructs it from scratch. This script keeps one record per system at

    <home>/qa/topology/<slug>/topology.md

where <home> is `--home`, else `$CC10X_HOME`, else `~/.cc10x`, and <slug> is
minted from the system's git remotes by `derive_slug`.

Subcommands (every one writes one JSON object to stdout):

    resolve --repos <path>... [--home DIR]
        Which existing record, if any, covers this run's repositories:
        {"match": "one|none|tie|superset", "records": [slug, ...],
         "run_members": {member: [aliases]}, "home": "<home>",
         "derived_slug": "<slug>|null", "warnings": [...]}
    verify <slug> --repos <path>... [--home DIR]
        Re-hash the fingerprinted files; any mismatch rewrites the record's
        status to `unverified`.
    write <slug> --from <env-plan.md> [--corrections <setup.md>]
          --status confirmed|executed --repos <path>... [--ground-truth NAME]
          [--home DIR] [--template PATH]
        Copy the env plan's sections into the record by heading. Every copied
        line passes through `classify_secret`; a hit is dropped and reported
        under `refused`, never written.

Exit codes: 0 on a result (`none` is a result), 2 on a usage error (including
a slug with `/`, `\\`, `..`, or an empty slug, and a `write` whose run has no
parseable remote), 1 on an unexpected failure (one-line JSON `{"error": ...}`,
no traceback).

Promises the unit suite (scripts/test_cc10x_qa_topology.py) pins:

- `verify` and `write` read only the record of the slug they are given;
- no copied line matching a secret shape is ever written;
- members are only ever added, never removed;
- a run that is a superset of an existing record resolves to that record
  (`superset`), never to a second record;
- an unparseable record is treated as absent: `resolve` skips it with a
  warning, `write` renames it to `topology.md.corrupt-<ts>` and reports it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE_DEFAULT = Path(__file__).resolve().parent.parent / "templates" / "qa-topology.template.md"
GIT_TIMEOUT_SECONDS = 30

FINGERPRINT_CANDIDATES = (
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "Tiltfile",
    "skaffold.yaml",
    "Procfile",
    "Makefile",
    "Dockerfile",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
    "requirements.txt",
    "go.sum",
    "Cargo.lock",
)

SECRET_SHAPES = (
    ("aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")),
    ("db_uri_with_password", re.compile(r"\b[a-z][a-z0-9+]*://[^/\s:@]+:[^@\s]+@")),
    ("long_token", re.compile(r"\b[A-Za-z0-9_\-]{40,}\b")),
    ("assignment", re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*\S{6,}")),
)

SLUG_SHAPE = re.compile(r"[a-z0-9][a-z0-9._-]{0,120}")
GROUND_TRUTH_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,120}")
SECRET_NAME = re.compile(r"(?<![^|`\s])[A-Z][A-Z0-9_]{2,}(?![^|`\s])")
SECTION_HEADING = re.compile(r"## (\d+)\. ")
TABLE_SEPARATOR = re.compile(r"\|[\s:|-]+\|?")
# Marks a scan_repos warning for a --repos entry that produced no member.
NO_MEMBER_MARK = ": no member — "
VALID_STATUSES = frozenset({"confirmed", "executed", "unverified"})

SECTION_TITLES = {
    "1": "1. Services",
    "2": "2. Wiring",
    "3": "3. Startup order",
    "4": "4. Data stores",
    "5": "5. Gotchas",
    "6": "6. Deployed ground truth",
    "7": "7. Secrets — locations only",
}

# env-plan heading -> record section: (record section, start, stop-or-None).
# A slice also ends at the next `## ` heading.
ENV_PLAN_SLICES = (
    ("1", re.compile(r"## 1\. "), re.compile(r"### Wiring\b")),
    ("2", re.compile(r"### Wiring\b"), None),
    ("3", re.compile(r"## 4\. "), None),
    ("4", re.compile(r"## 5\. "), None),
)
ENV_PLAN_SECRETS = re.compile(r"## 7\. ")
SETUP_FACTS = re.compile(r"## 2\. Measured facts")
SETUP_CORRECTIONS = re.compile(r"## 4\. Corrections to ")

_SCHEME_URL = re.compile(r"(?:ssh|git|git\+ssh|https?)://(?:[^@/]*@)?([^/]+)/(.+)")
_SCP_URL = re.compile(r"(?:[^@/:]+@)?([^/:]+):(?!//)(.+)")
_BARE_URL = re.compile(r"([^/:]+)/(.+)")
_HOST = re.compile(r"(?:[a-z0-9-]+(?:\.[a-z0-9-]+)+|localhost)(?::\d+)?")
_PATH_SEGMENT = re.compile(r"[a-z0-9._~-]+")


class UsageError(Exception):
    """A request the CLI refuses: exit 2."""


# ------------------------------------------------------------ pure functions


def validate_slug(slug: str) -> bool:
    """True iff the slug is safe as one path component under the home."""
    return bool(SLUG_SHAPE.fullmatch(slug)) and ".." not in slug


def derive_slug(run_members: dict[str, list[str]], existing_slugs: set[str] = frozenset()) -> str:
    """Mint a slug from the lexicographically first member, numbered on collision.

    `host/org/repo` -> `host--org--repo`, lower-cased, any character outside
    `[a-z0-9._-]` replaced by `-`. The same members give the same slug on
    every machine; the result always satisfies `validate_slug`.
    """
    if not run_members:
        raise ValueError("an empty member set has no slug")
    first = sorted(run_members)[0]
    base = re.sub(r"[^a-z0-9._-]", "-", first.replace("/", "--").lower())
    base = re.sub(r"\.{2,}", ".", base).lstrip("._-")[:110]
    if not base:
        raise ValueError(f"member {first!r} yields no slug characters")
    if base not in existing_slugs:
        return base
    n = 2
    while f"{base}--{n}" in existing_slugs:
        n += 1
    return f"{base}--{n}"


def normalise_remote(url: str) -> str | None:
    """A git remote URL as lower-case `host/org/repo`, or None when it does not parse."""
    text = url.strip().lower()
    if not text or any(ch.isspace() for ch in text):
        return None
    for pattern in (_SCHEME_URL, _SCP_URL, _BARE_URL):
        match = pattern.fullmatch(text)
        if match:
            break
    else:
        return None
    host, path = match.group(1), match.group(2).strip("/")
    if not _HOST.fullmatch(host):
        return None
    if path.endswith(".git"):
        path = path[: -len(".git")]
    segments = [seg for seg in path.split("/") if seg]
    if len(segments) < 2 or not all(
        _PATH_SEGMENT.fullmatch(seg) and seg.strip(".") for seg in segments
    ):
        return None
    return host + "/" + "/".join(segments)


def resolve(run_members: dict[str, list[str]], records: list[dict]) -> dict:
    """Match a run's members against the existing records.

    For each record R, `R_set = members | aliases`; `run_set` is the run's
    members plus all their aliases. Records whose set intersects the run's
    are the candidates: none -> `none`; two or more -> `tie`; exactly one ->
    `one` when every run member is in `R_set`, `superset` when the run's
    members strictly contain R's members, otherwise `tie`.
    """
    run_keys = set(run_members)
    run_set = run_keys | {alias for aliases in run_members.values() for alias in aliases}
    hits: list[tuple[str, set[str], set[str]]] = []
    for record in records:
        members = set(record.get("members", []))
        record_set = members | set(record.get("aliases", []))
        if run_set & record_set:
            hits.append((record["slug"], members, record_set))
    if not hits:
        match = "none"
    elif len(hits) >= 2:
        match = "tie"
    elif run_keys <= hits[0][2]:
        match = "one"
    elif run_keys > hits[0][1]:
        match = "superset"
    else:
        match = "tie"
    return {"match": match, "records": [slug for slug, _, _ in hits]}


def classify_secret(line: str) -> str | None:
    """The name of the first secret shape the line matches, or None."""
    for shape, pattern in SECRET_SHAPES:
        if pattern.search(line):
            return shape
    return None


def parse_front_block(text: str) -> dict | None:
    """The JSON object between the first two `---` lines; None when absent or unparseable."""
    lines = text.split("\n")
    marks = [i for i, line in enumerate(lines) if line.strip() == "---"][:2]
    if len(marks) < 2:
        return None
    try:
        data = json.loads("\n".join(lines[marks[0] + 1 : marks[1]]))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def render_record(template: str, front: dict, sections: dict[str, str]) -> str:
    """Fill the template: the front block, the slug, and each section's body.

    `sections` is keyed by section number ("1".."7"); a body lands directly
    under its `## N.` heading and that heading's description comment.
    """
    filled = template.replace("{slug}", str(front.get("slug", ""))).replace(
        "{front_block_json}", json.dumps(front, sort_keys=True, indent=2)
    )
    lines = filled.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        heading = SECTION_HEADING.match(lines[i])
        if heading:
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("<!--"):
                i += 1
                out.append(lines[i])
            body = sections.get(heading.group(1), "").strip("\n")
            if body:
                out.append(body)
        i += 1
    return "\n".join(out)


def merge_members(existing: dict, new_members: dict[str, list[str]]) -> dict:
    """Union of members and of aliases; nothing is ever removed; sorted."""
    members = set(existing.get("members", [])) | set(new_members)
    aliases = set(existing.get("aliases", [])) | {
        alias for group in new_members.values() for alias in group
    }
    return {"members": sorted(members), "aliases": sorted(aliases)}


# ------------------------------------------------------------- impure edges


def resolve_home(flag: str | None) -> Path:
    """`--home` > `$CC10X_HOME` > `~/.cc10x`."""
    chosen = flag or os.environ.get("CC10X_HOME") or "~/.cc10x"
    return Path(os.path.abspath(os.path.expanduser(chosen)))


def record_path(home: Path, slug: str) -> Path:
    return home / "qa" / "topology" / slug / "topology.md"


def _git_remotes(repo: str) -> tuple[dict[str, str], str | None]:
    """`{remote name: fetch URL}` for a repository, or ({}, why it failed)."""
    # GIT_* from a calling hook (GIT_DIR above all) would redirect `-C`.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    try:
        result = subprocess.run(
            ["git", "-C", repo, "remote", "-v"],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {}, f"git did not run ({type(exc).__name__})"
    if result.returncode != 0:
        return {}, "not a git repository (git remote -v failed)"
    remotes: dict[str, str] = {}
    for line in result.stdout.splitlines():
        name, _, rest = line.partition("\t")
        url, _, kind = rest.rpartition(" ")
        if kind == "(fetch)":
            remotes[name] = url
    if not remotes:
        return {}, "no git remote"
    return remotes, None


def scan_repos(repos: list[str]) -> tuple[dict[str, list[str]], list[str], dict[str, Path]]:
    """Run members from the repos' remotes: (run_members, warnings, member -> repo).

    A repo's member is its `origin` remote, else its first remote by name;
    its other remotes are aliases. A repo that produces no member is warned
    with NO_MEMBER_MARK; a partial parse is warned without it. Remote URLs
    are never echoed in a warning: one may carry credentials.
    """
    run_members: dict[str, list[str]] = {}
    warnings: list[str] = []
    member_repo: dict[str, Path] = {}
    for repo in repos:
        remotes, why = _git_remotes(repo)
        if why:
            warnings.append(f"{repo}{NO_MEMBER_MARK}{why}")
            continue
        parsed = {name: normalise_remote(url) for name, url in remotes.items()}
        good = {name: member for name, member in parsed.items() if member}
        bad = sorted(name for name, member in parsed.items() if not member)
        unparsed = f"remote(s) {', '.join(bad)} did not parse as host/org/repo"
        if not good:
            warnings.append(f"{repo}{NO_MEMBER_MARK}{unparsed}")
            continue
        if bad:
            # Partial parse: the repo still produces its member; unmarked.
            warnings.append(f"{repo}: {unparsed}")
        member = good["origin"] if "origin" in good else good[sorted(good)[0]]
        aliases = {m for m in good.values() if m != member} | set(run_members.get(member, []))
        run_members[member] = sorted(aliases)
        member_repo[member] = Path(repo)
    return run_members, warnings, member_repo


def _valid_front(front: dict | None) -> bool:
    if front is None:
        return False
    lists_ok = all(
        isinstance(front.get(key), list) and all(isinstance(v, str) for v in front[key])
        for key in ("members", "aliases")
    )
    return (
        lists_ok
        and isinstance(front.get("fingerprints"), dict)
        and front.get("status") in VALID_STATUSES
        and isinstance(front.get("slug"), str)
        and validate_slug(front["slug"])
    )


def read_front(path: Path) -> dict | None:
    """The record's front block when it parses, decodes as UTF-8, and has the expected shape."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    front = parse_front_block(text)
    return front if _valid_front(front) else None


def load_records(home: Path) -> tuple[list[dict], list[str]]:
    """Every parseable record under the home (resolve only); unparseable ones warned."""
    base = home / "qa" / "topology"
    records: list[dict] = []
    warnings: list[str] = []
    if not base.is_dir():
        return records, warnings
    for entry in sorted(base.iterdir()):
        path = entry / "topology.md"
        if not validate_slug(entry.name) or not path.is_file():
            continue
        front = read_front(path)
        if front is None:
            warnings.append(f"{path}: unparseable front block; treated as absent")
            continue
        records.append({"slug": entry.name, "members": front["members"], "aliases": front["aliases"]})
    return records, warnings


def hash_candidates(repo: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for name in FINGERPRINT_CANDIDATES:
        path = repo / name
        if path.is_file():
            out[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def _slice(lines: list[str], start: re.Pattern[str], stop: re.Pattern[str] | None) -> list[tuple[int, str]]:
    """(1-based line number, line) after the first `start` line, up to `stop` or the next `## `."""
    for i, line in enumerate(lines):
        if start.match(line):
            body: list[tuple[int, str]] = []
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("## ") or (stop is not None and stop.match(lines[j])):
                    break
                body.append((j + 1, lines[j]))
            return body
    return []


def _copy(numbered: list[tuple[int, str]], section: str, refused: list[dict]) -> str:
    """The lines with every secret-shaped one dropped and recorded in `refused`."""
    kept: list[str] = []
    for line_no, line in numbered:
        if line.strip() == "---":
            continue
        shape = classify_secret(line)
        if shape:
            refused.append({"section": SECTION_TITLES[section], "line_no": line_no, "shape": shape})
            continue
        kept.append(line)
    return "\n".join(kept).strip("\n")


def _cells(row: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", row.strip().strip("|"))]


def gotchas_from_setup(lines: list[str]) -> list[tuple[int, str]]:
    """Derived measured facts plus every correction row of a setup record."""
    rows = [(n, ln) for n, ln in _slice(lines, SETUP_FACTS, None) if ln.lstrip().startswith("|")]
    picked = [(n, ln) for n, ln in rows if "derived" in _cells(ln)]
    table = [(n, ln) for n, ln in _slice(lines, SETUP_CORRECTIONS, None) if ln.lstrip().startswith("|")]
    picked += [(n, ln) for n, ln in table[1:] if not TABLE_SEPARATOR.fullmatch(ln.strip())]
    return picked


def secret_names(lines: list[str], refused: list[dict]) -> str:
    """The NAMES in the env plan's secrets section, one per line, never values: a line that is itself a secret shape is refused whole and yields no name."""
    names: list[str] = []
    for line_no, line in _slice(lines, ENV_PLAN_SECRETS, None):
        shape = classify_secret(line)
        if shape:
            refused.append({"section": SECTION_TITLES["7"], "line_no": line_no, "shape": shape})
            continue
        for name in SECRET_NAME.findall(line):
            if name not in names:
                names.append(name)
    return "\n".join(f"- `{name}`" for name in names)


def record_sections(text: str) -> dict[str, str]:
    """Section number -> body of an existing record (comment line excluded)."""
    lines = text.split("\n")
    marks = [i for i, line in enumerate(lines) if line.strip() == "---"]
    out: dict[str, list[str]] = {}
    current: str | None = None
    i = marks[1] + 1 if len(marks) >= 2 else 0
    while i < len(lines):
        line = lines[i]
        heading = SECTION_HEADING.match(line)
        if heading:
            current = heading.group(1)
            out[current] = []
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("<!--"):
                i += 1
        elif line.startswith("## ") or line.strip() == "---":
            current = None
        elif current is not None:
            out[current].append(line)
        i += 1
    return {key: "\n".join(body).strip("\n") for key, body in out.items()}


def _rewrite_front(text: str, front: dict) -> str:
    lines = text.split("\n")
    marks = [i for i, line in enumerate(lines) if line.strip() == "---"][:2]
    head = lines[: marks[0] + 1]
    return "\n".join(head + [json.dumps(front, sort_keys=True, indent=2)] + lines[marks[1] :])


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def _rename_corrupt(path: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = path.with_name(f"{path.name}.corrupt-{stamp}")
    n = 2
    while target.exists():
        target = path.with_name(f"{path.name}.corrupt-{stamp}-{n}")
        n += 1
    os.replace(path, target)
    return target


def _has_heading(lines: list[str], *patterns: re.Pattern[str]) -> bool:
    """True when any line is matched by any of the patterns."""
    return any(pattern.match(line) for line in lines for pattern in patterns)


def _probe_template(template_text: str, slug: str) -> None:
    """Refuse a template whose render does not round-trip the front block and headings."""
    front = {
        "aliases": [],
        "fingerprints": {},
        "ground_truth": "local",
        "members": [],
        "slug": slug,
        "status": "confirmed",
        "updated_at": "1970-01-01T00:00:00Z",
        "written_by": "wf",
    }
    rendered = render_record(template_text, front, {})
    if parse_front_block(rendered) != front or not all(
        f"## {title}" in rendered for title in SECTION_TITLES.values()
    ):
        raise UsageError("--template lacks placeholders")


def _require_slug(slug: str) -> str:
    if not validate_slug(slug):
        raise UsageError(f"refused slug {slug!r}: it must match [a-z0-9][a-z0-9._-]* without '..'")
    return slug


def _require_file(value: str, flag: str) -> Path:
    path = Path(value)
    if not path.is_file():
        raise UsageError(f"{flag} {value}: not a file")
    return path


# ---------------------------------------------------------------- commands


def cmd_resolve(args: argparse.Namespace, home: Path) -> dict:
    run_members, warnings, _ = scan_repos(args.repos)
    records, record_warnings = load_records(home)
    result = resolve(run_members, records)
    related = set(result["records"])
    unrelated = {record["slug"] for record in records if record["slug"] not in related}
    try:
        derived: str | None = derive_slug(run_members, unrelated)
    except ValueError:
        derived = None
    return {
        "match": result["match"],
        "records": result["records"],
        "run_members": run_members,
        "home": str(home),
        "derived_slug": derived,
        "warnings": warnings + record_warnings,
    }


def cmd_verify(args: argparse.Namespace, home: Path) -> dict:
    slug = _require_slug(args.slug)
    path = record_path(home, slug)
    front = read_front(path) if path.is_file() else None
    if front is None:
        raise UsageError(f"no parseable record for slug {slug!r} under {home}")
    run_members, warnings, member_repo = scan_repos(args.repos)
    lookup: dict[str, Path] = {}
    for member, aliases in run_members.items():
        for name in [member] + aliases:
            lookup.setdefault(name, member_repo[member])
    mismatched: list[dict] = []
    missing: list[str] = []
    for member in front["members"]:
        repo = lookup.get(member)
        if repo is None:
            missing.append(member)
            continue
        recorded = front["fingerprints"].get(member, {})
        for rel in sorted(recorded):
            # Only candidate names are ever hashed: a record cannot point the
            # verifier at an arbitrary path.
            target = repo / rel
            now = None
            if rel in FINGERPRINT_CANDIDATES and target.is_file():
                now = hashlib.sha256(target.read_bytes()).hexdigest()
            if now != recorded[rel]:
                mismatched.append({"member": member, "file": rel})
    status = front.get("status")
    # A bare missing_repo (a partial run) never flips; a --repos entry that
    # produced no member (a warning) does: nothing it named was hashed.
    if mismatched or warnings:
        status = "unverified"
        front["status"] = status
        _atomic_write(path, _rewrite_front(path.read_text(encoding="utf-8"), front))
    return {
        "slug": slug,
        "status": status,
        "mismatched": mismatched,
        "missing_repo": sorted(missing),
        "warnings": warnings,
    }


def cmd_write(args: argparse.Namespace, home: Path) -> dict:
    slug = _require_slug(args.slug)
    env_plan = _require_file(args.from_path, "--from")
    setup = _require_file(args.corrections, "--corrections") if args.corrections else None
    template = _require_file(args.template, "--template") if args.template else TEMPLATE_DEFAULT
    if args.ground_truth is not None and not GROUND_TRUTH_NAME.fullmatch(args.ground_truth):
        raise UsageError(f"refused --ground-truth {args.ground_truth!r}")
    run_members, warnings, member_repo = scan_repos(args.repos)
    no_member = [w for w in warnings if NO_MEMBER_MARK in w]
    if no_member:
        raise UsageError("a --repos entry produced no member: " + "; ".join(no_member))
    if not run_members:
        raise UsageError("no repo in the run has a parseable remote; an empty run set cannot be written")
    plan_lines = env_plan.read_text(encoding="utf-8").split("\n")
    if not _has_heading(plan_lines, *(start for _, start, _ in ENV_PLAN_SLICES)):
        raise UsageError("--from does not contain an env-plan heading")
    setup_lines = setup.read_text(encoding="utf-8").split("\n") if setup is not None else None
    if setup_lines is not None and not _has_heading(setup_lines, SETUP_FACTS, SETUP_CORRECTIONS):
        raise UsageError("--corrections has neither a measured-facts nor a corrections table")
    template_text = template.read_text(encoding="utf-8")
    _probe_template(template_text, slug)

    # Every exit-2 guard has run: only now is the existing record read.
    path = record_path(home, slug)
    existing: dict = {}
    sections_before: dict[str, str] = {}
    corrupt: Path | None = None
    if path.is_file():
        front = read_front(path)
        if front is None:
            corrupt = _rename_corrupt(path)
        else:
            existing = front
            sections_before = record_sections(path.read_text(encoding="utf-8"))

    refused: list[dict] = []
    sections = {key: _copy(_slice(plan_lines, start, stop), key, refused) for key, start, stop in ENV_PLAN_SLICES}
    if setup_lines is not None:
        sections["5"] = _copy(gotchas_from_setup(setup_lines), "5", refused)
    else:
        sections["5"] = sections_before.get("5", "")
    if args.ground_truth is not None:
        ground_truth = f"deployed:{args.ground_truth}"
        sections["6"] = f"`{ground_truth}`"
    else:
        ground_truth = existing.get("ground_truth", "local")
        sections["6"] = sections_before.get("6", "")
    sections["7"] = secret_names(plan_lines, refused)

    merged = merge_members(existing, run_members)
    fingerprints = dict(existing.get("fingerprints", {}))
    for member, repo in member_repo.items():
        fingerprints[member] = hash_candidates(repo)
    front = {
        "aliases": merged["aliases"],
        "fingerprints": fingerprints,
        "ground_truth": ground_truth,
        "members": merged["members"],
        "slug": slug,
        "status": args.status,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "written_by": "wf",
    }
    _atomic_write(path, render_record(template_text, front, sections))
    return {
        "slug": slug,
        "path": str(path),
        "status": args.status,
        "members": merged["members"],
        "refused": refused,
        "corrupt_renamed": str(corrupt) if corrupt else None,
        "warnings": warnings,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cc10x_qa_topology.py",
        description="Resolve, verify and write the machine-local QA topology record.",
    )
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--repos", nargs="+", required=True, metavar="PATH", help="the run's repositories")
        p.add_argument("--home", default=None, help="overrides $CC10X_HOME and ~/.cc10x")

    p_resolve = sub.add_parser("resolve", help="which record covers these repositories")
    common(p_resolve)
    p_resolve.set_defaults(handler=cmd_resolve)

    p_verify = sub.add_parser("verify", help="re-hash fingerprinted files; mark mismatches unverified")
    p_verify.add_argument("slug")
    common(p_verify)
    p_verify.set_defaults(handler=cmd_verify)

    p_write = sub.add_parser("write", help="write or extend the record from an env plan")
    p_write.add_argument("slug")
    p_write.add_argument("--from", dest="from_path", required=True, metavar="ENV_PLAN")
    p_write.add_argument("--corrections", default=None, metavar="SETUP_MD")
    p_write.add_argument("--status", required=True, choices=("confirmed", "executed"))
    p_write.add_argument("--ground-truth", default=None, metavar="NAME")
    p_write.add_argument("--template", default=None, metavar="PATH")
    common(p_write)
    p_write.set_defaults(handler=cmd_write)
    return parser


def _emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = args.handler(args, resolve_home(args.home))
    except UsageError as exc:
        _emit({"error": str(exc)})
        return 2
    except Exception as exc:  # one-line JSON, no traceback
        _emit({"error": f"{type(exc).__name__}: {exc}"})
        return 1
    _emit(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
