#!/usr/bin/env python3
"""Decoupling ratchet (docs/MULTI_CHANNEL_PLAN.md phase 1: "a test that fails if an engine script names a channel").

The engine must ask scripts/channels.py instead of naming a channel. On 10 Nov 2026, 26 engine scripts still named
one. They cannot all be fixed in one go while the studio runs, so each script has a ceiling in
scripts/channel_ratchet.json: the number of code lines in it that name a channel. The ceiling can only go down.

  - A script over its ceiling fails: new hard-coding is refused.
  - A script not in the file has a ceiling of 0: a new engine script starts clean.
  - A script under its ceiling fails too, with the new number to write down, so progress is locked in.

  python3 scripts/test_channel_ratchet.py            run the test
  python3 scripts/test_channel_ratchet.py --report   every line still counted, per script
  python3 scripts/test_channel_ratchet.py --lower    lower ceilings to today's counts (never raises one)

What counts: a code line whose string or name mentions a channel's label, slug, name or repo (OWB, HOS, 'owb', 'hos',
orbit-with-ben, history-of-science, Orbit With Ben, History of Science, next_hos, OWB_..., hos_...). Comments and
docstrings do not count: they are history, not behaviour.
"""
from __future__ import annotations

import ast
import json
import pathlib
import re
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
RATCHET = HERE / "channel_ratchet.json"
# The loader itself, and this test, are where channel names are allowed to live.
EXEMPT = {"channels.py"}

IN_TEXT = re.compile(r"(?<![A-Za-z0-9_])(?:OWB|HOS|owb|hos)(?![A-Za-z0-9])|orbit-with-ben|history-of-science|"
                     r"Orbit With Ben|History [Oo]f Science|next_hos")
IN_NAME = re.compile(r"(?:^|_)(?:owb|hos)(?:_|$)", re.I)


def engine_scripts() -> list[pathlib.Path]:
    return sorted(p for p in HERE.glob("*.py") if not p.name.startswith("test_") and p.name not in EXEMPT)


def _docstrings(tree: ast.AST) -> set[int]:
    """ids of the string nodes that are docstrings."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                out.add(id(first.value))
    return out


def channel_lines(source: str) -> dict[int, str]:
    """{line number: why} for each code line that names a channel."""
    tree = ast.parse(source)
    docs = _docstrings(tree)
    hits: dict[int, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
            m = IN_TEXT.search(node.value)
            if m:
                # a string spread over several lines counts on each line that carries a mention
                for offset, part in enumerate(node.value.split("\n")):
                    if IN_TEXT.search(part):
                        hits.setdefault(node.lineno + offset, m.group(0))
        else:
            for name in (getattr(node, "id", None), getattr(node, "attr", None), getattr(node, "arg", None),
                         getattr(node, "name", None)):
                if isinstance(name, str) and IN_NAME.search(name) and hasattr(node, "lineno"):
                    hits.setdefault(node.lineno, name)
    return hits


def counts() -> dict[str, int]:
    return {p.name: len(channel_lines(p.read_text())) for p in engine_scripts()}


def ceilings() -> dict[str, int]:
    return json.loads(RATCHET.read_text())["ceilings"]


class Counting(unittest.TestCase):
    def test_strings_and_names_count_but_comments_and_docstrings_do_not(self):
        src = '''"""Module about OWB and HOS: history, not behaviour."""
import os
# the HOS repo used to be named here
def f(job):
    """Works for OWB."""
    repo = os.environ.get("HOS_REPO")        # counts: a string
    hos_at = job.get("at")                   # counts: a name
    label = "HOS" if job.get("repo") == "hos" else "OWB"   # counts once: one line
    return f"{label}:{job['film']}", "chosen", "those", "owbject"
'''
        self.assertEqual(sorted(channel_lines(src)), [6, 7, 8])

    def test_words_that_only_contain_the_letters_are_not_channels(self):
        self.assertEqual(channel_lines('x = ["those", "chosen", "showboat", "whose", "ghost"]\nshos = 1\n'), {})

    def test_repo_and_channel_names_count(self):
        src = 'a = "https://github.com/x/history-of-science.git"\nb = "Orbit With Ben"\nc = wip["next_hos"]\n'
        self.assertEqual(sorted(channel_lines(src)), [1, 2, 3])


class Ratchet(unittest.TestCase):
    def test_no_engine_script_names_a_channel_more_than_its_ceiling(self):
        cap = ceilings()
        over = {n: (c, cap.get(n, 0)) for n, c in counts().items() if c > cap.get(n, 0)}
        self.assertEqual(over, {}, "these engine scripts name a channel on more code lines than their ceiling "
                                   "(count, ceiling). Ask scripts/channels.py instead; see "
                                   "`python3 scripts/test_channel_ratchet.py --report`")

    def test_progress_is_locked_in(self):
        cap = ceilings()
        now = counts()
        slack = {n: (now.get(n, 0), c) for n, c in cap.items() if now.get(n, 0) < c}
        self.assertEqual(slack, {}, "these scripts are now under their ceiling (count, ceiling): run "
                                    "`python3 scripts/test_channel_ratchet.py --lower` and commit the file")

    def test_the_ratchet_lists_only_real_scripts_and_no_zeros(self):
        cap = ceilings()
        names = {p.name for p in engine_scripts()}
        self.assertEqual(sorted(n for n in cap if n not in names), [], "ceiling for a script that is gone")
        self.assertEqual(sorted(n for n, c in cap.items() if c <= 0), [], "a clean script needs no entry")


def _write(cap: dict[str, int]) -> None:
    data = json.loads(RATCHET.read_text()) if RATCHET.exists() else {}
    data["_about"] = ("Decoupling ratchet (scripts/test_channel_ratchet.py). For each engine script: how many code lines "
                      "still name a channel. Ceilings only go down; a script not listed must have none. "
                      "Lower them with `python3 scripts/test_channel_ratchet.py --lower`.")
    data["total"] = sum(cap.values())
    data["ceilings"] = dict(sorted(cap.items(), key=lambda kv: (-kv[1], kv[0])))
    RATCHET.write_text(json.dumps(data, indent=2) + "\n")


def main() -> int:
    if "--report" in sys.argv:
        total = 0
        for p in engine_scripts():
            hits = channel_lines(p.read_text())
            if hits:
                total += len(hits)
                print(f"{p.name}: {len(hits)}")
                lines = p.read_text().split("\n")
                for n in sorted(hits):
                    print(f"  {n}: {lines[n - 1].strip()[:150]}")
        print(f"total: {total}")
        return 0
    if "--lower" in sys.argv or "--init" in sys.argv:
        now = {n: c for n, c in counts().items() if c}
        if "--init" in sys.argv and not RATCHET.exists():
            _write(now)
            print(f"wrote {RATCHET.name}: {sum(now.values())} lines in {len(now)} scripts")
            return 0
        cap = ceilings()
        new = {n: min(c, now.get(n, 0)) for n, c in cap.items() if min(c, now.get(n, 0)) > 0}
        _write(new)
        print(f"ceilings: {sum(cap.values())} -> {sum(new.values())} lines, {len(cap)} -> {len(new)} scripts")
        return 0
    unittest.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
