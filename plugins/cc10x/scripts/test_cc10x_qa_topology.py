#!/usr/bin/env python3
"""Unit and CLI checks for scripts/cc10x_qa_topology.py.

No framework. Run:  python3 test_cc10x_qa_topology.py   (exit 0 = pass)

The topology record is machine-local memory: one file per system, keyed by a
slug derived from the system's git remotes. The script that reads and writes
it has three promises a reader cannot check by looking at a record:

- it never reads a record other than the one slug it is asked for;
- it never writes a line matching a secret shape;
- it never removes a member, and never mints a second record for a run that
  is a superset of an existing one.

These checks pin those promises at two seams: the pure functions (loaded with
`importlib`, no subprocess) and the CLI (a subprocess against temporary git
repositories and a temporary home). Every child process runs with
`capture_output=True, text=True` and its stderr is folded into the check
detail, so this suite's own stderr stays empty -- the invariants suite
(PP-51) treats any byte on it as a failure.

The final line is `topology unit checks: N passed` when every check holds.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Callable

SCRIPTS = Path(__file__).resolve().parent
TOOL = SCRIPTS / "cc10x_qa_topology.py"
TEMPLATE = SCRIPTS.parent / "templates" / "qa-topology.template.md"

# Remotes used by the CLI fixtures. Built from parts where a literal would be
# a secret-shaped string in source.
URL_ORIGIN = "git@github.com:Org/Repo.git"
URL_FORK = "https://github.com/someone/repo.git"
URL_API = "https://github.com/org/api.git"
URL_UNPARSEABLE = "file:///srv/git/local.git"
MEMBER_REPO = "github.com/org/repo"
MEMBER_FORK = "github.com/someone/repo"
MEMBER_API = "github.com/org/api"
SLUG_REPO = "github.com--org--repo"

FAKE_AWS = "AKIA" + "IOSFODNN7" + "EXAMPLE"
FAKE_BEARER = "Bearer " + "abcDEF123" + "456ghiJKL"
FAKE_DB_URI = "mongodb+srv://" + "appuser:" + "s3cretpw" + "@cluster0.example.net/db"
FAKE_LONG = "x9" * 21
FAKE_PASSWORD_LINE = "db pass" + "word=hunter2secret"
FAKE_PG_LINE = "POSTGRES_" + "PASSWORD=" + "supersecret1"
FAKE_JWT_LINE = "JWT_" + "SECRET=" + "jwt0123456789abc"
FAKE_GH_LINE = "GITHUB_" + "TOKEN=" + "ghp_abcDEF123456789"
FAKE_STRIPE_LINE = "STRIPE_API_" + "KEY=" + "sk_test_0123456789"
FAKE_YAML_PW_LINE = "DB_" + "PASSWORD: " + "hunter22x"
FAKE_LOWER_BEARER = "authorization: bearer " + "abcDEF123" + "456ghiJKL"
FAKE_UPPER_PW_LINE = "PASSWORD=" + "HUNTER2" + "SECRETX"
FAKE_TABLE_BEARER_LINE = "| API_TOKEN | Bearer " + "ABCDEFGHIJKLM" + "NOPQRSTUVWXYZ |"

# Set to "1" to make the suite add one deliberate failure: PP-51 runs the
# suite that way once to prove its failure path still exits 1.
SELFTEST_ENV = "CC10X_TOPOLOGY_SELFTEST_FAIL"

ENV_PLAN = "\n".join(
    [
        "# Test Environment Plan: demo",
        "",
        "## 1. Topology",
        "",
        "| Service | Port |",
        "| api | 8080 |",
        "SERVICE-LINE-MARKER",
        "leaked key " + FAKE_AWS,
        "",
        "### Wiring",
        "",
        "api -> db via DATABASE_URL",
        "WIRING-MARKER",
        "",
        "## 2. Feature flags, settings, and entitlements",
        "",
        "FLAGS-MARKER-NOT-COPIED",
        "",
        "## 3. Prerequisites",
        "",
        "## 4. Bring-up → manifest `setup[]` + `healthcheck`",
        "",
        "docker compose up -d",
        "BRINGUP-MARKER",
        "",
        "## 5. Data → manifest `reset[]` + `seed[]`",
        "",
        "seed via make seed",
        FAKE_PASSWORD_LINE,
        "DATA-MARKER",
        "",
        "## 6. Determinism",
        "",
        "## 7. Secrets and config → manifest `required_env` + `environment`",
        "",
        "| DATABASE_URL | from the vault path kv/app |",
        "| API_TOKEN | value: s3cr3tvalue-not-to-copy |",
        FAKE_UPPER_PW_LINE,
        FAKE_TABLE_BEARER_LINE,
        "",
        "## 8. Observability access",
        "",
        "OBSERVABILITY-MARKER-NOT-COPIED",
        "",
    ]
)
ENV_PLAN_AWS_LINE = ENV_PLAN.split("\n").index("leaked key " + FAKE_AWS) + 1
ENV_PLAN_PASSWORD_LINE = ENV_PLAN.split("\n").index(FAKE_PASSWORD_LINE) + 1
ENV_PLAN_UPPER_PW_LINE = ENV_PLAN.split("\n").index(FAKE_UPPER_PW_LINE) + 1
ENV_PLAN_TABLE_BEARER_LINE = ENV_PLAN.split("\n").index(FAKE_TABLE_BEARER_LINE) + 1

SETUP = "\n".join(
    [
        "# Setup Record: demo",
        "",
        "## 2. Measured facts",
        "",
        "| Fact | Volatility | How observed | Observed output |",
        "| ---- | ---------- | ------------ | --------------- |",
        "| analyzer image has no sshd | derived | docker run img which sshd | (none) |",
        "| opengrep on PATH | stable | which opengrep | /usr/local/bin/opengrep |",
        "",
        "## 3. Human prerequisites, measured",
        "",
        "| Item | Why |",
        "",
        "## 4. Corrections to `env-plan.md`",
        "",
        "| What `env-plan.md` predicted | What was measured | Section | Routed? | Class |",
        "| --- | --- | --- | --- | --- |",
        "| api on 8080 | api on 18080 | 1 | yes | wrong-guess |",
        "",
        "## 5. Superseded rows",
        "",
    ]
)

passed = 0
failures: list[str] = []
T: ModuleType | None = None


def check(name: str, ok: bool, detail: str) -> None:
    global passed
    status = "ok  " if ok else "FAIL"
    sys.stdout.write(f"  [{status}] {name}: {detail}\n")
    if ok:
        passed += 1
    else:
        failures.append(f"{name}: {detail}")


def case(name: str, fn: Callable[[], tuple[bool, str]]) -> None:
    """Run one check; an exception is a failure that names itself."""
    try:
        ok, detail = fn()
    except Exception as exc:  # the check reports, it never crashes the suite
        ok, detail = False, f"raised {type(exc).__name__}: {exc}"
    check(name, ok, detail)


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cc10x_qa_topology", TOOL)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build an import spec for {TOOL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tool() -> ModuleType:
    if T is None:
        raise RuntimeError(f"{TOOL.name} did not load")
    return T


def clean_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """The parent env without CC10X_HOME and without any GIT_* variable.

    A GIT_DIR inherited from a git hook would point `git init` at the real
    repository; dropping GIT_* keeps every child inside its temp directory.
    """
    env = {
        k: v
        for k, v in os.environ.items()
        if k != "CC10X_HOME" and not k.startswith("GIT_")
    }
    env.update(extra or {})
    return env


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, env=clean_env()
    )


def make_repo(
    root: Path, name: str, remotes: dict[str, str], files: dict[str, str] | None = None
) -> Path:
    repo = root / name
    repo.mkdir(parents=True)
    init = git(repo, "init", "-q")
    if init.returncode != 0:
        raise RuntimeError(f"git init failed in {repo}: {init.stderr.strip()[:200]}")
    for remote, url in remotes.items():
        added = git(repo, "remote", "add", remote, url)
        if added.returncode != 0:
            raise RuntimeError(f"git remote add {remote} failed: {added.stderr.strip()[:200]}")
    for rel, content in (files or {}).items():
        (repo / rel).write_text(content, encoding="utf-8")
    return repo


def cli(
    *args: str, env_extra: dict[str, str] | None = None
) -> tuple[int, dict | None, str, str]:
    """Run the CLI; returns (rc, parsed stdout JSON or None, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        env=clean_env(env_extra),
    )
    try:
        data = json.loads(result.stdout)
    except ValueError:
        data = None
    return result.returncode, data, result.stdout, result.stderr


def said(rc: int, data: object, err: str) -> str:
    """Detail fragment: rc, the JSON seen, and the child's stderr (trimmed)."""
    text = json.dumps(data, sort_keys=True) if data is not None else "no JSON"
    tail = f"; stderr={err.strip()[:200]!r}" if err.strip() else ""
    return f"rc={rc} out={text[:400]}{tail}"


def record_path(home: Path, slug: str) -> Path:
    return home / "qa" / "topology" / slug / "topology.md"


def plant_record(home: Path, slug: str, members: list[str], body: str) -> Path:
    path = record_path(home, slug)
    path.parent.mkdir(parents=True)
    front = {
        "aliases": [],
        "fingerprints": {},
        "ground_truth": "local",
        "members": members,
        "slug": slug,
        "status": "confirmed",
        "updated_at": "2026-01-01T00:00:00Z",
        "written_by": "wf",
    }
    path.write_text(
        "---\n" + json.dumps(front, sort_keys=True, indent=2) + "\n---\n\n" + body + "\n",
        encoding="utf-8",
    )
    return path


def front_of(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").split("\n")
    marks = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    return json.loads("\n".join(lines[marks[0] + 1 : marks[1]]))


def section_of(path: Path, number: str) -> str:
    """The body under `## <number>.` up to the next `## ` heading or `---`."""
    out: list[str] = []
    inside = False
    for ln in path.read_text(encoding="utf-8").split("\n"):
        if ln.startswith("## "):
            inside = ln.startswith(f"## {number}. ")
            continue
        if inside and ln.strip() == "---":
            break
        if inside:
            out.append(ln)
    return "\n".join(out)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------- pure seam


def pure_checks() -> None:
    nr = lambda url: tool().normalise_remote(url)  # noqa: E731

    remote_cases = [
        ("git@github.com:Org/Repo.git", MEMBER_REPO),
        ("ssh://git@github.com/org/repo", MEMBER_REPO),
        ("https://github.com/org/repo.git", MEMBER_REPO),
        ("https://github.com/org/repo/", MEMBER_REPO),
        ("github.com:org/repo", MEMBER_REPO),
        ("HTTPS://GitHub.COM/Org/Repo.GIT", MEMBER_REPO),
        ("ssh://git@Git.Example.com:2222/Team/App.git", "git.example.com:2222/team/app"),
    ]
    for url, want in remote_cases:
        case(
            f"normalise_remote({url!r})",
            lambda url=url, want=want: (nr(url) == want, f"got {nr(url)!r}, want {want!r}"),
        )
    case(
        "normalise_remote: unparseable remotes give None",
        lambda: (
            all(nr(u) is None for u in ("", "not a remote", "/srv/git/repo.git", URL_UNPARSEABLE)),
            f"got {[nr(u) for u in ('', 'not a remote', '/srv/git/repo.git', URL_UNPARSEABLE)]!r}",
        ),
    )

    good = ["github.com--org--repo", "a", "a.b_c-d", "git.example.com-2222--team--app"]
    bad = ["", "a/b", "a\\b", "..", "../x", ".hidden", "a..b", "Upper", "-lead"]
    case(
        "validate_slug: accepts well-formed slugs",
        lambda: (
            all(tool().validate_slug(s) for s in good),
            f"rejected {[s for s in good if not tool().validate_slug(s)]!r}",
        ),
    )
    case(
        "validate_slug: refuses /, \\, .., empty, leading dot, upper case",
        lambda: (
            not any(tool().validate_slug(s) for s in bad),
            f"accepted {[s for s in bad if tool().validate_slug(s)]!r}",
        ),
    )

    def derive(members: dict[str, list[str]], existing: set[str] | None = None) -> str:
        if existing is None:
            return tool().derive_slug(members)
        return tool().derive_slug(members, existing)

    def derive_case(members: dict[str, list[str]], want: str, existing: set[str] | None = None):
        def run() -> tuple[bool, str]:
            got = derive(members, existing)
            return (
                got == want and tool().validate_slug(got),
                f"got {got!r} (validate_slug={tool().validate_slug(got)}), want {want!r}",
            )

        return run

    case("derive_slug: one member", derive_case({MEMBER_REPO: [MEMBER_FORK]}, SLUG_REPO))
    case(
        "derive_slug: two members, the sorted first wins",
        derive_case({"github.com/zeta/z": [], "github.com/alpha/a": []}, "github.com--alpha--a"),
    )
    case(
        "derive_slug: host with upper case, dots and a port",
        derive_case({"Git.Example.com:2222/team/app": []}, "git.example.com-2222--team--app"),
    )
    case(
        "derive_slug: a collision gets the first free numbered suffix",
        derive_case(
            {MEMBER_REPO: []}, SLUG_REPO + "--3", {SLUG_REPO, SLUG_REPO + "--2", "unrelated"}
        ),
    )
    case(
        "derive_slug: same remotes give the same slug",
        lambda: (
            derive({MEMBER_REPO: [], MEMBER_API: []}) == derive({MEMBER_API: [], MEMBER_REPO: []}),
            f"got {derive({MEMBER_REPO: [], MEMBER_API: []})!r} and "
            f"{derive({MEMBER_API: [], MEMBER_REPO: []})!r}",
        ),
    )

    def derive_empty() -> tuple[bool, str]:
        try:
            got = tool().derive_slug({})
        except ValueError as exc:
            return True, f"ValueError: {exc}"
        return False, f"returned {got!r} on an empty member set"

    case("derive_slug: an empty member set raises ValueError", derive_empty)

    def resolve_case(run: dict[str, list[str]], records: list[dict], want_match: str, want_slugs: list[str]):
        def go() -> tuple[bool, str]:
            got = tool().resolve(run, records)
            slugs = sorted(got.get("records", []))
            return (
                got.get("match") == want_match and slugs == sorted(want_slugs),
                f"got match={got.get('match')!r} records={slugs!r}, want {want_match!r} {sorted(want_slugs)!r}",
            )

        return go

    def rec(slug: str, members: list[str], aliases: list[str] | None = None) -> dict:
        return {"slug": slug, "members": members, "aliases": aliases or []}

    case("resolve: zero records -> none", resolve_case({MEMBER_REPO: []}, [], "none", []))
    case(
        "resolve: a non-intersecting record -> none",
        resolve_case({MEMBER_REPO: []}, [rec("other", ["gitlab.com/x/y"])], "none", []),
    )
    case(
        "resolve: one record, exact -> one",
        resolve_case({MEMBER_REPO: []}, [rec("r", [MEMBER_REPO])], "one", ["r"]),
    )
    case(
        "resolve: run is a subset of the record -> one",
        resolve_case({MEMBER_REPO: []}, [rec("r", [MEMBER_REPO, MEMBER_API])], "one", ["r"]),
    )
    case(
        "resolve: run is a superset of the record -> superset",
        resolve_case({MEMBER_REPO: [], MEMBER_API: []}, [rec("r", [MEMBER_REPO])], "superset", ["r"]),
    )
    case(
        "resolve: partial overlap -> tie",
        resolve_case(
            {MEMBER_REPO: [], MEMBER_API: []},
            [rec("r", [MEMBER_REPO, "github.com/org/web"])],
            "tie",
            ["r"],
        ),
    )
    case(
        "resolve: two records both intersecting -> tie",
        resolve_case(
            {MEMBER_REPO: [], MEMBER_API: []},
            [rec("r1", [MEMBER_REPO]), rec("r2", [MEMBER_API])],
            "tie",
            ["r1", "r2"],
        ),
    )
    case(
        "resolve: run member only in the record's aliases -> one",
        resolve_case(
            {MEMBER_FORK: []}, [rec("r", [MEMBER_REPO], [MEMBER_FORK])], "one", ["r"]
        ),
    )

    secret_cases = [
        ("aws_key", "key = " + FAKE_AWS, ""),
        ("bearer", "Authorization: " + FAKE_BEARER, ""),
        ("db_uri_with_password", "MONGO=" + FAKE_DB_URI, ""),
        ("long_token", "token " + FAKE_LONG, ""),
        ("assignment", FAKE_PASSWORD_LINE, ""),
        ("assignment", FAKE_PG_LINE, " (POSTGRES_PASSWORD=)"),
        ("assignment", FAKE_JWT_LINE, " (JWT_SECRET=)"),
        ("assignment", FAKE_GH_LINE, " (GITHUB_TOKEN=)"),
        ("assignment", FAKE_STRIPE_LINE, " (STRIPE_API_KEY=)"),
        ("assignment", FAKE_YAML_PW_LINE, " (DB_PASSWORD: yaml)"),
        ("bearer", FAKE_LOWER_BEARER, " (lower-case header)"),
        ("assignment", FAKE_UPPER_PW_LINE, " (upper-case key)"),
        ("bearer", FAKE_TABLE_BEARER_LINE, " (upper-case value in a table cell)"),
    ]
    for shape, line, label in secret_cases:
        case(
            f"classify_secret: {shape}{label}",
            lambda shape=shape, line=line: (
                tool().classify_secret(line) == shape,
                f"got {tool().classify_secret(line)!r}, want {shape!r}",
            ),
        )
    clean = "| api | http://localhost:8080 | depends on db via DATABASE_URL |"
    case(
        "classify_secret: a clean line is None",
        lambda: (tool().classify_secret(clean) is None, f"got {tool().classify_secret(clean)!r}"),
    )
    bare_name = "- `API_TOKEN`"
    case(
        "classify_secret: a bare name in backticks is None",
        lambda: (tool().classify_secret(bare_name) is None, f"got {tool().classify_secret(bare_name)!r}"),
    )
    pointer = "token: see vault"
    case(
        "classify_secret: a pointer to the vault is None",
        lambda: (tool().classify_secret(pointer) is None, f"got {tool().classify_secret(pointer)!r}"),
    )
    single_mark = '---\n{"a": 1}\n'
    case(
        "parse_front_block: a single --- line is unparseable",
        lambda: (
            tool().parse_front_block(single_mark) is None,
            f"got {tool().parse_front_block(single_mark)!r}",
        ),
    )

    case(
        "parse_front_block: JSON between the first two --- lines",
        lambda: (
            tool().parse_front_block('---\n{"slug": "a", "members": []}\n---\nbody\n---\n')
            == {"slug": "a", "members": []},
            "parsed the front block",
        ),
    )
    unparseable_blocks = ("no block", "---\nnot json\n---\n", "---\n[1]\n---\n")
    case(
        "parse_front_block: absent or unparseable -> None",
        lambda: (
            [tool().parse_front_block(t) for t in unparseable_blocks] == [None, None, None],
            f"got {[tool().parse_front_block(t) for t in unparseable_blocks]!r}",
        ),
    )

    def render() -> tuple[bool, str]:
        template = TEMPLATE.read_text(encoding="utf-8")
        front = {"slug": "s-1", "members": [MEMBER_REPO], "status": "confirmed"}
        out = tool().render_record(template, front, {"1": "RENDER-ONE", "7": "- `API_TOKEN`"})
        tmp = Path(tempfile.mkdtemp()) / "t.md"
        tmp.write_text(out, encoding="utf-8")
        try:
            ok = (
                tool().parse_front_block(out) == front
                and "# Topology record: s-1" in out
                and "RENDER-ONE" in section_of(tmp, "1")
                and "API_TOKEN" in section_of(tmp, "7")
                and "{" + "slug}" not in out
                and "{" + "front_block_json}" not in out
            )
        finally:
            shutil.rmtree(tmp.parent)
        return ok, f"rendered {len(out)}B; front round-trips, sections land under their headings"

    case("render_record: placeholders filled, sections under their headings", render)

    def merge() -> tuple[bool, str]:
        got = tool().merge_members(
            {"members": ["github.com/b/b", "github.com/a/a"], "aliases": ["github.com/f/a"]},
            {"github.com/c/c": ["github.com/f/c"]},
        )
        want_m = ["github.com/a/a", "github.com/b/b", "github.com/c/c"]
        want_a = ["github.com/f/a", "github.com/f/c"]
        return (
            got.get("members") == want_m and got.get("aliases") == want_a,
            f"got {got!r}, want members={want_m!r} aliases={want_a!r}",
        )

    case("merge_members: union, never removal, sorted", merge)


# ---------------------------------------------------------------- CLI seam


def cli_checks(root: Path) -> None:
    for sub in ("resolve", "verify", "write"):
        case(
            f"CLI: {sub} --help exits 0",
            lambda sub=sub: (
                (lambda r: (r[0] == 0 and "usage" in r[2].lower(), f"rc={r[0]}; stderr={r[3].strip()[:200]!r}"))(
                    cli(sub, "--help")
                )
            ),
        )

    repo1 = make_repo(
        root,
        "repo1",
        {"origin": URL_ORIGIN, "fork": URL_FORK},
        {"docker-compose.yml": "services: {}\n", "package.json": "{}\n"},
    )
    repo2 = make_repo(root, "repo2", {"origin": URL_API}, {"Makefile": "all:\n"})
    repo_none = make_repo(root, "repo-none", {})
    repo_bad = make_repo(root, "repo-bad", {"origin": URL_UNPARSEABLE})

    # The fixture helper's deliberate duplicate: `origin` already exists, so
    # git refuses and writes to stderr on every git version. The child's
    # stderr must be captured, or it leaks onto this suite's stderr.
    def duplicate_remote() -> tuple[bool, str]:
        dup = subprocess.run(["git", "remote", "add", "origin", URL_ORIGIN], cwd=str(repo1), capture_output=True, text=True, env=clean_env())
        return (
            dup.returncode != 0 and "already exists" in dup.stderr,
            f"rc={dup.returncode}; captured stderr={dup.stderr.strip()[-120:]!r}",
        )

    case("fixture: a duplicate `git remote add origin` fails with captured stderr", duplicate_remote)

    home = root / "home"
    env_plan = root / "env-plan.md"
    env_plan.write_text(ENV_PLAN, encoding="utf-8")
    setup = root / "setup.md"
    setup.write_text(SETUP, encoding="utf-8")

    def resolve_none() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home))
        keys = {"match", "records", "run_members", "home", "derived_slug", "warnings"}
        ok = (
            rc == 0
            and data is not None
            and set(data) == keys
            and data["match"] == "none"
            and data["records"] == []
            and data["derived_slug"] == SLUG_REPO
            and data["warnings"] == []
            and data["home"] == str(home)
        )
        return ok, said(rc, data, err)

    case("CLI resolve: first run -> none, every key, derived_slug minted", resolve_none)

    def resolve_fork() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home))
        ok = rc == 0 and data is not None and data["run_members"] == {MEMBER_REPO: [MEMBER_FORK]}
        return ok, said(rc, data, err)

    case("CLI resolve: origin is the member, the fork is its alias", resolve_fork)

    def resolve_no_remote() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo_none), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and data["derived_slug"] is None
            and data["run_members"] == {}
            and len(data["warnings"]) == 1
            and str(repo_none) in data["warnings"][0]
        )
        return ok, said(rc, data, err)

    case("CLI resolve: no parseable remote -> exit 0, derived_slug null, one warning", resolve_no_remote)

    def resolve_unparseable() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), str(repo_bad), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and data["run_members"] == {MEMBER_REPO: [MEMBER_FORK]}
            and len(data["warnings"]) == 1
            and str(repo_bad) in data["warnings"][0]
            and data["derived_slug"] == SLUG_REPO
        )
        return ok, said(rc, data, err)

    case("CLI resolve: an unparseable remote is skipped with a warning", resolve_unparseable)

    def write_no_remote() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", "some-slug", "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo_none), "--home", str(home),
        )
        return rc == 2 and not record_path(home, "some-slug").exists(), said(rc, data, err)

    case("CLI write: an empty run set exits 2 and writes nothing", write_no_remote)

    def write_bad_slugs() -> tuple[bool, str]:
        rcs = {}
        for slug in ("../x", "a/b", "a\\b", ""):
            rc, _, _, _ = cli(
                "write", slug, "--from", str(env_plan), "--status", "confirmed",
                "--repos", str(repo1), "--home", str(home),
            )
            rcs[slug] = rc
        escaped = (
            (home / "qa" / "topology").exists()
            or (home / "qa" / "x").exists()
            or (home / "qa" / "topology" / "a").exists()
        )
        return all(v == 2 for v in rcs.values()) and not escaped, f"rcs={rcs!r} wrote={escaped}"

    case("CLI write: slugs with /, \\, .. or empty exit 2", write_bad_slugs)

    # A second record in the same home, carrying a marker no other record has.
    other_slug = "gitlab.com--other--thing"
    plant_record(home, other_slug, ["gitlab.com/other/thing"], "MARKER-OTHER-7f3a")

    def write_first() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home),
        )
        path = record_path(home, SLUG_REPO)
        if rc != 0 or not path.exists() or data is None:
            return False, said(rc, data, err)
        front = front_of(path)
        keys = ["aliases", "fingerprints", "ground_truth", "members", "slug", "status", "updated_at", "written_by"]
        ok = (
            set(data) == {"slug", "path", "status", "members", "refused", "corrupt_renamed", "warnings"}
            and data["path"] == str(path)
            and data["corrupt_renamed"] is None
            and sorted(front) == keys
            and front["members"] == [MEMBER_REPO]
            and front["aliases"] == [MEMBER_FORK]
            and front["status"] == "confirmed"
            and front["ground_truth"] == "local"
            and front["written_by"] == "wf"
            and front["fingerprints"]
            == {MEMBER_REPO: {"docker-compose.yml": sha("services: {}\n"), "package.json": sha("{}\n")}}
        )
        return ok, said(rc, data, err) + f" front={json.dumps(front, sort_keys=True)[:300]}"

    case("CLI write: first time -> record at <home>/qa/topology/<slug>/topology.md", write_first)

    path1 = record_path(home, SLUG_REPO)

    def write_sections() -> tuple[bool, str]:
        s = {n: section_of(path1, n) for n in "1234567"}
        ok = (
            "SERVICE-LINE-MARKER" in s["1"]
            and "WIRING-MARKER" in s["2"]
            and "WIRING-MARKER" not in s["1"]
            and "BRINGUP-MARKER" in s["3"]
            and "DATA-MARKER" in s["4"]
            and "DATABASE_URL" in s["7"]
            and "API_TOKEN" in s["7"]
        )
        text = path1.read_text(encoding="utf-8")
        ok = ok and "FLAGS-MARKER-NOT-COPIED" not in text and "OBSERVABILITY-MARKER-NOT-COPIED" not in text
        return ok, f"sections sized {[len(s[n]) for n in '1234567']}"

    case("CLI write: sections copied by heading, uncopied sections absent", write_sections)

    def write_secrets() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home),
        )
        text = path1.read_text(encoding="utf-8")
        refused = data["refused"] if data else []
        ok = (
            rc == 0
            and {"section": "1. Services", "line_no": ENV_PLAN_AWS_LINE, "shape": "aws_key"} in refused
            and {"section": "4. Data stores", "line_no": ENV_PLAN_PASSWORD_LINE, "shape": "assignment"} in refused
            and FAKE_AWS not in text
            and "hunter2secret" not in text
            and "s3cr3tvalue" not in text
            and "SERVICE-LINE-MARKER" in text
            and FAKE_AWS not in json.dumps(data)
        )
        return ok, said(rc, data, err)

    case("CLI write: secret-shaped lines refused and named, the rest written", write_secrets)

    def secrets_section() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home),
        )
        refused = data["refused"] if data else []
        text = path1.read_text(encoding="utf-8")
        sec7 = section_of(path1, "7")
        title = "7. Secrets — locations only"
        ok = (
            rc == 0
            and {"section": title, "line_no": ENV_PLAN_UPPER_PW_LINE, "shape": "assignment"} in refused
            and {"section": title, "line_no": ENV_PLAN_TABLE_BEARER_LINE, "shape": "bearer"} in refused
            and "HUNTER2SECRETX" not in text
            and "ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in text
            and "- `DATABASE_URL`" in sec7
            and "- `API_TOKEN`" in sec7
        )
        return ok, said(rc, data, err) + f" sec7={sec7.strip()[-160:]!r}"

    case("CLI write: a §7 value line is refused whole and no name is taken from it", secrets_section)

    # Guard cases write into their own home: a guard that fails open must not
    # plant records that change the main home's resolve results.
    home_g = root / "home-guards"

    def write_missing_from() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", "absent-from", "--from", str(root / "absent.md"), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home_g),
        )
        ok = rc == 2 and data is not None and "--from" in data.get("error", "")
        return ok, said(rc, data, err)

    case("CLI write: a missing --from exits 2", write_missing_from)

    not_a_repo = root / "not-a-repo"
    not_a_repo.mkdir()

    def write_no_member() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", "no-member-slug", "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), str(not_a_repo), "--home", str(home_g),
        )
        error = data.get("error", "") if data else ""
        rc2, data2, _, err2 = cli(
            "write", "dup-path-slug", "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), str(repo1), "--home", str(root / "home-dup-path"),
        )
        ok = (
            rc == 2
            and "not-a-repo" in error
            and "no member" in error
            and not record_path(home_g, "no-member-slug").exists()
            and rc2 == 0
        )
        return ok, said(rc, data, err) + " | duplicate path: " + said(rc2, data2, err2)

    case("CLI write: a --repos entry with no member exits 2 and names it", write_no_member)

    def write_no_heading() -> tuple[bool, str]:
        notes = root / "notes.md"
        notes.write_text("# notes\n\nA paragraph with no env-plan heading.\n", encoding="utf-8")
        rc, data, _, err = cli(
            "write", "no-heading-slug", "--from", str(notes), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home_g),
        )
        ok = (
            rc == 2
            and data is not None
            and data.get("error") == "--from does not contain an env-plan heading"
            and not record_path(home_g, "no-heading-slug").exists()
        )
        return ok, said(rc, data, err)

    case("CLI write: --from without an env-plan heading exits 2", write_no_heading)

    def corrections_no_table() -> tuple[bool, str]:
        bare = root / "setup-bare.md"
        bare.write_text("# setup\n", encoding="utf-8")
        rc, data, _, err = cli(
            "write", "no-table-slug", "--from", str(env_plan), "--corrections", str(bare),
            "--status", "confirmed", "--repos", str(repo1), "--home", str(home_g),
        )
        return rc == 2 and not record_path(home_g, "no-table-slug").exists(), said(rc, data, err)

    case("CLI write: --corrections without a facts or corrections table exits 2", corrections_no_table)

    def template_no_placeholders() -> tuple[bool, str]:
        bare = root / "bare-template.md"
        bare.write_text("# nothing\n", encoding="utf-8")
        rc, data, _, err = cli(
            "write", "no-template-slug", "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--template", str(bare), "--home", str(home_g),
        )
        ok = (
            rc == 2
            and data is not None
            and data.get("error") == "--template lacks placeholders"
            and not record_path(home_g, "no-template-slug").exists()
        )
        return ok, said(rc, data, err)

    case("CLI write: a --template without placeholders exits 2", template_no_placeholders)

    def unexpected_failure() -> tuple[bool, str]:
        home_file = root / "home-is-a-file"
        home_file.write_text("not a directory\n", encoding="utf-8")
        rc, data, out, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home_file),
        )
        ok = (
            rc == 1
            and data is not None
            and re.match(r"[A-Za-z]+Error: ", data.get("error", "")) is not None
            and len(out.strip().split("\n")) == 1
            and err == ""
        )
        return ok, said(rc, data, err)

    case("CLI write: an unexpected failure exits 1 with a one-line error", unexpected_failure)

    def resolve_one_idempotent() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and data["match"] == "one"
            and data["records"] == [SLUG_REPO]
            and data["derived_slug"] == SLUG_REPO
        )
        return ok, said(rc, data, err)

    case("CLI resolve: after the write -> one; the derived slug is stable", resolve_one_idempotent)

    def resolve_superset() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), str(repo2), "--home", str(home))
        ok = rc == 0 and data is not None and data["match"] == "superset" and data["records"] == [SLUG_REPO]
        return ok, said(rc, data, err)

    case("CLI resolve: run adds a repo -> superset of the existing record", resolve_superset)

    def write_superset() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "executed",
            "--repos", str(repo1), str(repo2), "--home", str(home),
        )
        front = front_of(path1)
        others = sorted(p.name for p in (home / "qa" / "topology").iterdir())
        ok = (
            rc == 0
            and front["members"] == [MEMBER_API, MEMBER_REPO]
            and data is not None
            and data["members"] == [MEMBER_API, MEMBER_REPO]
            and front["status"] == "executed"
            and others == sorted([SLUG_REPO, other_slug])
        )
        return ok, said(rc, data, err) + f" dirs={others}"

    case("CLI write: superset -> members unioned into the same record", write_superset)

    def isolation() -> tuple[bool, str]:
        text = path1.read_text(encoding="utf-8")
        return "MARKER-OTHER-7f3a" not in text, f"{path1.name} {len(text)}B; marker absent"

    case("CLI write: another slug's content never appears in this record", isolation)

    def append_only() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo2), "--home", str(home),
        )
        front = front_of(path1)
        ok = (
            rc == 0
            and front["members"] == [MEMBER_API, MEMBER_REPO]
            and MEMBER_REPO in front["fingerprints"]
            and front["aliases"] == [MEMBER_FORK]
        )
        return ok, said(rc, data, err) + f" members={front['members']}"

    case("CLI write: a run missing a member never removes it", append_only)

    def resolve_subset() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home))
        return rc == 0 and data is not None and data["match"] == "one", said(rc, data, err)

    case("CLI resolve: run is a subset of the record -> one", resolve_subset)

    def corrections() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--corrections", str(setup),
            "--status", "confirmed", "--repos", str(repo1), "--home", str(home),
        )
        g = section_of(path1, "5")
        ok = (
            rc == 0
            and "analyzer image has no sshd" in g
            and "opengrep on PATH" not in g
            and "api on 18080" in g
            and "What was measured" not in g
        )
        return ok, said(rc, data, err) + f" gotchas={g.strip()[:200]!r}"

    case("CLI write: gotchas <- derived facts + every correction row", corrections)

    def gotchas_kept() -> tuple[bool, str]:
        before = section_of(path1, "5")
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home),
        )
        after = section_of(path1, "5")
        return rc == 0 and before == after and "no sshd" in after, said(rc, data, err)

    case("CLI write: without --corrections the existing gotchas are kept verbatim", gotchas_kept)

    def corrections_zero_rows() -> tuple[bool, str]:
        setup_empty = root / "setup-empty.md"
        setup_empty.write_text(
            SETUP.replace("| analyzer image has no sshd | derived | docker run img which sshd | (none) |\n", "")
            .replace("| api on 8080 | api on 18080 | 1 | yes | wrong-guess |\n", ""),
            encoding="utf-8",
        )
        before = section_of(path1, "5")
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--corrections", str(setup_empty),
            "--status", "executed", "--repos", str(repo1), "--home", str(home),
        )
        after = section_of(path1, "5")
        ok = rc == 0 and after == before and "no sshd" in before
        return ok, said(rc, data, err) + f" before={before.strip()[:160]!r} after={after.strip()[:160]!r}"

    case("CLI write: --corrections carrying zero rows keeps section 5 byte-identical", corrections_zero_rows)

    def corrections_append() -> tuple[bool, str]:
        extra = "| db on 5432 | db on 15432 | 1 | yes | wrong-guess |"
        setup_plus = root / "setup-plus.md"
        setup_plus.write_text(
            SETUP.replace(
                "| api on 8080 | api on 18080 | 1 | yes | wrong-guess |\n",
                "| api on 8080 | api on 18080 | 1 | yes | wrong-guess |\n" + extra + "\n",
            ),
            encoding="utf-8",
        )
        before = section_of(path1, "5")
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--corrections", str(setup_plus),
            "--status", "executed", "--repos", str(repo1), "--home", str(home),
        )
        after = section_of(path1, "5")
        ok = (
            rc == 0
            and after.rstrip("\n") == before.rstrip("\n") + "\n" + extra
            and after.count("api on 18080") == 1
        )
        return ok, said(rc, data, err) + f" before={before.strip()[-160:]!r} after={after.strip()[-200:]!r}"

    case("CLI write: --corrections carrying one new row appends it after the existing rows", corrections_append)

    def ground_truth() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--ground-truth", "staging", "--home", str(home),
        )
        first = front_of(path1)["ground_truth"]
        sec = section_of(path1, "6")
        rc2, data2, _, err2 = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home),
        )
        ok = (
            rc == 0
            and rc2 == 0
            and first == "deployed:staging"
            and "staging" in sec
            and front_of(path1)["ground_truth"] == "deployed:staging"
            and section_of(path1, "6") == sec
        )
        return ok, said(rc, data, err) + " | " + said(rc2, data2, err2)

    case("CLI write: --ground-truth recorded, then kept when omitted", ground_truth)

    def collision() -> tuple[bool, str]:
        home_c = root / "home-collision"
        plant_record(home_c, SLUG_REPO, ["gitlab.com/x/y"], "unrelated")
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home_c))
        ok = rc == 0 and data is not None and data["match"] == "none" and data["derived_slug"] == SLUG_REPO + "--2"
        return ok, said(rc, data, err)

    case("CLI resolve: an unrelated record on the slug -> --2, never a merge", collision)

    def corrupt() -> tuple[bool, str]:
        home_k = root / "home-corrupt"
        bad = record_path(home_k, SLUG_REPO)
        bad.parent.mkdir(parents=True)
        bad.write_text("---\nnot json at all\n---\nbody\n", encoding="utf-8")
        rc0, data0, _, err0 = cli("resolve", "--repos", str(repo1), "--home", str(home_k))
        absent = rc0 == 0 and data0 is not None and data0["match"] == "none" and len(data0["warnings"]) == 1
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home_k),
        )
        renamed = data.get("corrupt_renamed") if data else None
        ok = (
            absent
            and rc == 0
            and isinstance(renamed, str)
            and Path(renamed).name.startswith("topology.md.corrupt-")
            and Path(renamed).read_text(encoding="utf-8").startswith("---\nnot json")
            and front_of(bad)["members"] == [MEMBER_REPO]
        )
        return ok, said(rc0, data0, err0) + " | " + said(rc, data, err)

    case("CLI write: a corrupt record is renamed, reported, and rewritten fresh", corrupt)

    home_u = root / "home-nonutf8"
    undecodable = record_path(home_u, SLUG_REPO)
    undecodable.parent.mkdir(parents=True)
    undecodable.write_bytes(b"\xff\xfe\x00\x00---\n")

    def nonutf8_resolve() -> tuple[bool, str]:
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(home_u))
        ok = (
            rc == 0
            and data is not None
            and data["match"] == "none"
            and len(data["warnings"]) == 1
            and "unparseable front block" in data["warnings"][0]
        )
        return ok, said(rc, data, err)

    case("CLI resolve: a non-UTF-8 record is warned and treated as absent", nonutf8_resolve)

    def nonutf8_verify() -> tuple[bool, str]:
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo1), "--home", str(home_u))
        return rc == 2, said(rc, data, err)

    case("CLI verify: a non-UTF-8 record is no record (exit 2, not 1)", nonutf8_verify)

    def nonutf8_write() -> tuple[bool, str]:
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo1), "--home", str(home_u),
        )
        renamed = data.get("corrupt_renamed") if data else None
        ok = (
            rc == 0
            and isinstance(renamed, str)
            and Path(renamed).name.startswith("topology.md.corrupt-")
            and isinstance(tool().read_front(Path(data["path"])), dict)
        )
        return ok, said(rc, data, err)

    case("CLI write: a non-UTF-8 record is renamed, reported, and rewritten fresh", nonutf8_write)

    def bad_front_fields() -> tuple[bool, str]:
        home_b = root / "home-bad-front"
        got = {}
        for key, value in (("status", "done"), ("slug", "../x")):
            path = plant_record(home_b, f"bad-{key}", [MEMBER_REPO], "body")
            front = front_of(path)
            front[key] = value
            path.write_text(
                "---\n" + json.dumps(front, sort_keys=True, indent=2) + "\n---\n\nbody\n",
                encoding="utf-8",
            )
            got[key] = tool().read_front(path)
        return all(v is None for v in got.values()), f"read_front gave {got!r}"

    case("read_front: a front block with a bad status or slug is unparseable", bad_front_fields)

    def atomic_no_tmp() -> tuple[bool, str]:
        target = root / "aw" / "f.md"
        try:
            tool()._atomic_write(target, "\ud800")
        except UnicodeEncodeError:
            raised = True
        else:
            raised = False
        leftover = (root / "aw" / "f.md.tmp").exists()
        return raised and not leftover, f"raised UnicodeEncodeError={raised}, .tmp left={leftover}"

    case("_atomic_write: a failed write leaves no .tmp", atomic_no_tmp)

    def home_flag_beats_env() -> tuple[bool, str]:
        h1, h2 = root / "h-flag", root / "h-env"
        rc, data, _, err = cli("resolve", "--repos", str(repo1), "--home", str(h1), env_extra={"CC10X_HOME": str(h2)})
        return rc == 0 and data is not None and data["home"] == str(h1), said(rc, data, err)

    case("CLI home: --home beats $CC10X_HOME", home_flag_beats_env)

    def env_beats_default() -> tuple[bool, str]:
        h2, fake_home = root / "h-env", root / "fake-user"
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed", "--repos", str(repo1),
            env_extra={"CC10X_HOME": str(h2), "HOME": str(fake_home)},
        )
        ok = (
            rc == 0
            and data is not None
            and data["path"] == str(record_path(h2, SLUG_REPO))
            and record_path(h2, SLUG_REPO).exists()
            and not (fake_home / ".cc10x").exists()
        )
        return ok, said(rc, data, err)

    case("CLI home: $CC10X_HOME beats ~/.cc10x", env_beats_default)

    def default_home() -> tuple[bool, str]:
        fake_home = root / "fake-user"
        rc, data, _, err = cli("resolve", "--repos", str(repo1), env_extra={"HOME": str(fake_home)})
        return rc == 0 and data is not None and data["home"] == str(fake_home / ".cc10x"), said(rc, data, err)

    case("CLI home: default is ~/.cc10x", default_home)

    verify_checks(root, env_plan)


def verify_checks(root: Path, env_plan: Path) -> None:
    files = {"docker-compose.yml": "services: {}\n", "package.json": "{}\n"}

    def fresh(tag: str, with_files: bool = True) -> tuple[Path, Path]:
        repo = make_repo(root, f"v-{tag}", {"origin": URL_ORIGIN}, files if with_files else None)
        home = root / f"vh-{tag}"
        rc, data, _, err = cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo), "--home", str(home),
        )
        if rc != 0:
            raise RuntimeError("fixture write failed: " + said(rc, data, err))
        return repo, home

    def equal() -> tuple[bool, str]:
        repo, home = fresh("equal")
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and set(data) == {"slug", "status", "mismatched", "missing_repo", "warnings"}
            and data["status"] == "confirmed"
            and data["mismatched"] == []
            and data["missing_repo"] == []
        )
        return ok, said(rc, data, err)

    case("CLI verify: fingerprints equal -> status kept", equal)

    def changed() -> tuple[bool, str]:
        repo, home = fresh("changed")
        (repo / "package.json").write_text('{"name": "changed"}\n', encoding="utf-8")
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and data["status"] == "unverified"
            and data["mismatched"] == [{"member": MEMBER_REPO, "file": "package.json"}]
            and front_of(record_path(home, SLUG_REPO))["status"] == "unverified"
        )
        return ok, said(rc, data, err)

    case("CLI verify: a changed file -> unverified, record rewritten", changed)

    def missing_file() -> tuple[bool, str]:
        repo, home = fresh("missing")
        (repo / "docker-compose.yml").unlink()
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and data["status"] == "unverified"
            and {"member": MEMBER_REPO, "file": "docker-compose.yml"} in data["mismatched"]
        )
        return ok, said(rc, data, err)

    case("CLI verify: a fingerprinted file now missing -> unverified", missing_file)

    def empty_fp() -> tuple[bool, str]:
        repo, home = fresh("empty", with_files=False)
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = rc == 0 and data is not None and data["status"] == "confirmed" and data["mismatched"] == []
        return ok, said(rc, data, err)

    case("CLI verify: a record with empty fingerprints -> status kept", empty_fp)

    def missing_repo() -> tuple[bool, str]:
        repo, home = fresh("partial")
        api = make_repo(root, "v-partial-api", {"origin": URL_API})
        cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo), str(api), "--home", str(home),
        )
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = rc == 0 and data is not None and data["missing_repo"] == [MEMBER_API] and data["status"] == "confirmed"
        return ok, said(rc, data, err)

    case("CLI verify: a member with no repo in the run is reported", missing_repo)

    def no_member_flips() -> tuple[bool, str]:
        repo, home = fresh("nomember")
        api = make_repo(root, "v-nomember-api", {"origin": URL_API})
        cli(
            "write", SLUG_REPO, "--from", str(env_plan), "--status", "confirmed",
            "--repos", str(repo), str(api), "--home", str(home),
        )
        stray = root / "v-not-a-repo"
        stray.mkdir()
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), str(stray), "--home", str(home))
        warnings = data.get("warnings", []) if data else []
        ok = (
            rc == 0
            and data is not None
            and len(warnings) == 1
            and "v-not-a-repo" in warnings[0]
            and "no member" in warnings[0]
            and data["missing_repo"] == [MEMBER_API]
            and data["status"] == "unverified"
            and tool().read_front(record_path(home, SLUG_REPO))["status"] == "unverified"
        )
        return ok, said(rc, data, err)

    case("CLI verify: a --repos entry with no member is warned, reported and flips status", no_member_flips)

    def non_candidate() -> tuple[bool, str]:
        repo, home = fresh("outside")
        path = record_path(home, SLUG_REPO)
        front = tool().read_front(path)
        front["fingerprints"][MEMBER_REPO]["../outside.txt"] = "0" * 64
        tool()._atomic_write(path, tool()._rewrite_front(path.read_text(encoding="utf-8"), front))
        (root / "outside.txt").write_text("outside the repo\n", encoding="utf-8")
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(home))
        ok = (
            rc == 0
            and data is not None
            and {"member": MEMBER_REPO, "file": "../outside.txt"} in data["mismatched"]
            and data["status"] == "unverified"
        )
        return ok, said(rc, data, err)

    case("CLI verify: a non-candidate fingerprint path is never hashed", non_candidate)

    def verify_no_record() -> tuple[bool, str]:
        repo = make_repo(root, "v-norecord", {"origin": URL_ORIGIN})
        rc, data, _, err = cli("verify", SLUG_REPO, "--repos", str(repo), "--home", str(root / "vh-norecord"))
        return rc == 2, said(rc, data, err)

    case("CLI verify: no record for the slug exits 2", verify_no_record)


def main() -> int:
    global T
    try:
        T = load_tool()
        check("load", True, f"{TOOL.name} imported")
    except Exception as exc:
        check("load", False, f"{TOOL} did not import: {type(exc).__name__}: {exc}")
    pure_checks()
    root = Path(tempfile.mkdtemp(prefix="cc10x-topology-"))
    try:
        case("CLI fixtures", lambda: (cli_checks(root) is None, "CLI checks ran"))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    if os.environ.get(SELFTEST_ENV) == "1":
        check("selftest: a deliberate failure", False, f"{SELFTEST_ENV}=1 — this run must exit 1")
    if failures:
        sys.stdout.write(f"\nFAILED ({len(failures)}):\n")
        for f in failures:
            sys.stdout.write(f"  - {f}\n")
        sys.stdout.write(f"topology unit checks: {passed} passed, {len(failures)} failed\n")
        return 1
    sys.stdout.write(f"topology unit checks: {passed} passed\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
