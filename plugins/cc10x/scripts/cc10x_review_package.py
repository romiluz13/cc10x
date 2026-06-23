#!/usr/bin/env python3
"""Generate a review package: commit list, stat summary, and the net diff with
extended context, written to one file the reviewer reads in a single call, so
the diff never has to be pasted through the router's context. cc10x's analog of
superpowers' review-package.

Usage: cc10x_review_package.py [--repo DIR] BASE [HEAD]
  BASE   the sha/ref recorded BEFORE the phase started
  HEAD   end ref (default HEAD)
  --repo the git repo to diff (default: $CC10X_REPO_DIR, else the process cwd).
         Lets the router drive a build against a repo OTHER than the process
         cwd (a sibling repo, or one repo reached from a parent dir) so the
         review/verify diff targets the repo that actually changed.

Writes <state_root>/review-<base7>..<head7>.diff (state_root = .cc10x, resolved
like the hooklib: CLAUDE_PROJECT_DIR env, else git toplevel, else cwd) and
prints 'wrote <path>: <n> commit(s), <bytes> bytes'. NOTE: --repo / CC10X_REPO_DIR
only redirects the git QUERIES; the package is still written to the standard
state_root (so the orchestrator reads it where it always does).

CRITICAL: BASE must be the sha recorded before the phase started, NEVER HEAD~1.
HEAD~1 silently drops all but the last commit of a multi-commit phase, so the
reviewer sees a partial diff and approves work it never read.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path


def project_dir() -> Path:
    value = os.environ.get("CLAUDE_PROJECT_DIR")
    if value:
        return Path(value)
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if top:
            return Path(top)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return Path.cwd()


def state_root() -> Path:
    path = project_dir() / ".cc10x"
    path.mkdir(parents=True, exist_ok=True)
    return path


def repo_dir() -> str | None:
    """The git repo the diff queries run against. `CC10X_REPO_DIR` lets the
    router drive a build against a repo OTHER than the process cwd; unset
    returns None so git runs in the process cwd exactly as before (default
    behavior is unchanged). project_dir()/state_root() are intentionally NOT
    affected — only the git source moves, not where the package is written."""
    return os.environ.get("CC10X_REPO_DIR") or None


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_dir(),
    ).stdout


def resolve(ref: str) -> str | None:
    """Return the full sha for ref, or None if it does not resolve."""
    try:
        return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").strip()
    except subprocess.CalledProcessError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cc10x_review_package.py",
        description="Write a BASE..HEAD review package to one .cc10x diff file.",
    )
    parser.add_argument("base", help="sha/ref recorded BEFORE the phase started")
    parser.add_argument("head", nargs="?", default="HEAD", help="end ref (default HEAD)")
    parser.add_argument(
        "--repo",
        default=None,
        help="git repo to diff (default: $CC10X_REPO_DIR, else cwd). Lets the "
        "router review a repo other than the process cwd.",
    )
    args = parser.parse_args()

    # --repo takes precedence over the env; both feed git() via CC10X_REPO_DIR
    # so every git query in this run targets the same repo.
    if args.repo:
        os.environ["CC10X_REPO_DIR"] = args.repo

    print(
        "note: BASE must be the sha recorded before the phase started, "
        "NEVER HEAD~1 (that drops all but the last commit of a multi-commit phase).",
        file=sys.stderr,
    )

    base_sha = resolve(args.base)
    if base_sha is None:
        print(f"bad BASE: {args.base}", file=sys.stderr)
        return 2
    head_sha = resolve(args.head)
    if head_sha is None:
        print(f"bad HEAD: {args.head}", file=sys.stderr)
        return 2

    if base_sha == head_sha:
        print(
            f"BASE and HEAD resolve to the same commit ({base_sha[:7]}); "
            "nothing to review. BASE must predate the phase's commits.",
            file=sys.stderr,
        )
        return 2

    rng = f"{base_sha}..{head_sha}"
    body = (
        "# Review package\n"
        f"\nRange: {args.base}..{args.head}  ({base_sha[:7]}..{head_sha[:7]})\n"
        "\n## Commits\n"
        f"{git('log', '--oneline', rng)}"
        "\n## Files changed\n"
        f"{git('diff', '--stat', rng)}"
        "\n## Diff\n"
        f"{git('diff', '-U10', rng)}"
    )

    out = state_root() / f"review-{base_sha[:7]}..{head_sha[:7]}.diff"
    try:
        out.write_text(body, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write review package {out}: {exc}", file=sys.stderr)
        return 2

    commits = git("rev-list", "--count", rng).strip()
    print(f"wrote {out}: {commits} commit(s), {len(body.encode('utf-8'))} bytes")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        msg = (exc.stderr or "").strip() or str(exc)
        print(f"git failed: {msg}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print("git not found on PATH", file=sys.stderr)
        sys.exit(2)
