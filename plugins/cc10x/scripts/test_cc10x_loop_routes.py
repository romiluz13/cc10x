#!/usr/bin/env python3
"""Pins the loop pane's route table (hooks/loop-routes.ts) to router law.

Every `phase: '<token>'` in the table must be in the router's `phase:{...}` enum
(skills/cc10x-router/SKILL.md), every `agent: '<name>'` other than `router` must
be a file under agents/, and every route key must be present. A `phase:`/`agent:`
token with any other value spelling fails the token count; shorthand, quoted or
computed keys, spreads other than `finish`/`memory`, and imports fail `escapes`.
Other spellings (a row built by a function call, `Object.assign`) are not detected.

Runs as a dependency-free script (`python3 test_cc10x_loop_routes.py`) and
unchanged under pytest.
"""

from __future__ import annotations

import re
import traceback
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent
ROUTES_TS = PLUGIN_ROOT / "hooks" / "loop-routes.ts"
ROUTER_SKILL = PLUGIN_ROOT / "skills" / "cc10x-router" / "SKILL.md"
AGENTS_DIR = PLUGIN_ROOT / "agents"
ROUTE_KEYS = ("BUILD", "BUILD_TRIVIAL", "PLAN", "DEBUG", "REVIEW", "QA", "QA_REGRESSION", "TRIAGE", "CODEBASE-HEALTH")


def router_phase_enum() -> set[str]:
    for line in ROUTER_SKILL.read_text().splitlines():
        m = re.match(r"^phase:\{(.*)\}$", line)
        if m:
            return set(m.group(1).split("|"))
    raise AssertionError(f"no `phase:{{...}}` enum line in {ROUTER_SKILL}")


def routes_source() -> str:
    assert ROUTES_TS.is_file(), f"{ROUTES_TS} missing"
    return ROUTES_TS.read_text()


def route_rows() -> tuple[str, int]:
    """The table rows (everything after the `export type Route` line) and the file line they start on."""
    source = routes_source()
    start = source.index("\n", source.index("export type Route"))
    return source[start:], source.count("\n", 0, start) + 1


def quoted_values(key: str, rows: str | None = None) -> set[str]:
    """Every `key: '<value>'` in the rows; a `key:` whose value is written another way (double quotes, a
    template literal, a variable, `key:'x'`, `key : 'x'`) would slip past the pin, so the token count must
    equal the quoted-value count. Spellings with no `key:` token at all are caught by `escapes` instead."""
    rows, first = route_rows() if rows is None else (rows, 1)
    values = list(re.finditer(rf"\b{key}: '([^']+)'", rows))
    tokens = list(re.finditer(rf"\b{key}\s*:", rows))
    matched = {v.start() for v in values}
    lines = [first + rows.count("\n", 0, t.start()) for t in tokens if t.start() not in matched]
    assert len(tokens) == len(values), (
        f"{len(tokens)} `{key}:` tokens but {len(values)} single-quoted values; unmatched tokens on lines {lines}"
    )
    return {v.group(1) for v in values}


ALLOWED_SPREADS = {"finish", "memory"}


def escapes(source: str) -> list[str]:
    """Spellings that put a row in the table without a `key: '<value>'` token: shorthand `{ agent, phase }`,
    a quoted or computed key (`'phase':`, `['phase']:`), a spread of anything but the file's own
    `finish`/`memory` helpers, and any import (an outside table could only arrive through one)."""
    found = re.findall(r"\b(?:agent|phase)\s*[,}]", source)
    found += re.findall(r"""\[?\s*['"`](?:agent|phase)['"`]\s*\]?\s*:""", source)
    found += [f"...{name}" for name in re.findall(r"\.\.\.\s*([\w$.]+)", source) if name not in ALLOWED_SPREADS]
    found += re.findall(r"^\s*import\b.*$", source, re.M)
    return found


def test_route_rows_use_only_pinned_spellings():
    found = escapes(routes_source())
    assert not found, f"route rows spelled past the pin: {found}"


def test_escape_check_catches_each_spelling():
    for mutant in (
        "{ agent, phase }",
        "{ agent: 'a', phase }",
        "{ agent: 'a', ['phase']: 'x' }",
        "{ 'agent': 'a', \"phase\": 'x' }",
        "[...OUTSIDE, memory]",
        "import { OUTSIDE } from './elsewhere'",
    ):
        assert escapes(mutant), f"escape check missed {mutant!r}"
    assert not escapes("[{ agent: 'a', phase: 'x' }, ...finish, memory]"), "escape check flags the pinned spelling"


def test_value_pin_catches_each_spelling():
    for key in ("agent", "phase"):
        for mutant in (f"{{ {key} : 'x' }}", f"{{ {key}:'x' }}", f'{{ {key}: "x" }}', f"{{ {key}: X }}"):
            try:
                quoted_values(key, mutant)
            except AssertionError:
                continue
            raise AssertionError(f"value pin missed {mutant!r}")
        assert quoted_values(key, f"{{ {key}: 'x' }}") == {"x"}, "value pin rejects the pinned spelling"


def test_value_pin_names_the_unmatched_lines():
    try:
        quoted_values("phase", "{ phase: 'a' }\n{ phase : 'b' }\n{ phase: 'c' }\n{ phase: X }")
    except AssertionError as e:
        assert "lines [2, 4]" in str(e), f"unmatched lines not named: {e}"
        return
    raise AssertionError("value pin missed the unmatched tokens")


def test_every_route_phase_is_in_the_router_enum():
    phases = quoted_values("phase")
    assert phases, "no phase: '<token>' rows found"
    assert phases <= router_phase_enum(), f"phases outside the router enum: {sorted(phases - router_phase_enum())}"


def test_every_route_agent_is_router_or_an_agent_file():
    agents = quoted_values("agent")
    assert agents, "no agent: '<name>' rows found"
    missing = [a for a in sorted(agents) if a != "router" and not (AGENTS_DIR / f"{a}.md").is_file()]
    assert not missing, f"agents without a file under agents/: {missing}"


def test_route_table_names_every_route():
    source = routes_source()
    assert re.search(r"^export const REMEDIATION", source, re.M), "REMEDIATION table missing"
    routes = source[source.index("export const ROUTES") : source.index("export const REMEDIATION")]
    missing = [k for k in ROUTE_KEYS if not re.search(rf"^  (?:'{re.escape(k)}'|{re.escape(k)}): \[", routes, re.M)]
    assert not missing, f"route keys missing from ROUTES: {missing}"


def main() -> int:
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_") and callable(fn)]
    failures = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except Exception:
            failures += 1
            print(f"FAIL {name}")
            traceback.print_exc()
    print(f"{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
