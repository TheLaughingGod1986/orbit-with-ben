#!/usr/bin/env python3
"""Keep the rule copies in step with AGENTS.md, and catch rule lines that have gone stale.

  python3 scripts/sync_rules.py           # rewrite every SYNC block from AGENTS.md
  python3 scripts/sync_rules.py --check   # CI: exit 1 if a block is out of date or a stale line is found

AGENTS.md is the source (Claude owns it, Ben 5 Oct 2026). A copy elsewhere sits between markers:

  <!-- SYNC: AGENTS.md#Never -->
  ...generated, do not edit by hand...
  <!-- /SYNC -->

The text after "#" names the AGENTS.md "## " heading; the block holds that section's body verbatim.
STALE lists phrases from superseded orders. Add one whenever an order changes, so old wording can't creep back.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "AGENTS.md"
TARGETS = [
    ".cursor/rules/orbit-studio.mdc",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
]
SCAN = [
    "AGENTS.md",
    "docs/ORBIT_PLAYBOOK_LESSONS.md",
    "docs/PRODUCTION_THREAD.md",
    "00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md",
    ".cursor/rules/*.mdc",
]
# (pattern, why it is stale)
STALE = [
    (r"Stop (and wait )?for Ben's OK", "sign-offs go to Claude first (3 Oct 2026)"),
    (r"NEEDS BEN\*\* → Chief of Staff", "NEEDS BEN goes to Claude first (3 Oct 2026)"),
    (r"Home: Google AI Studio", "picture runs on Vertex (free credit), never AI Studio prepaid"),
    (r"\*\*Tools:\*\* Google AI Studio", "picture runs on Vertex (free credit), never AI Studio prepaid"),
    (r"Ben OKs anything public", "Claude gives the final OK (3 Oct 2026)"),
    (r"until Ben reviews", "Claude reviews KEEP (3 Oct 2026)"),
    (r"shot list (goes )?to \**Ben before generation", "shot lists go to Claude (3 Oct 2026)"),
    (r"back catalogue needs Ben's OK", "back catalogue goes to Claude (3 Oct 2026)"),
    (r"edit_post` with Ben's OK", "queued Buffer edits go to Claude (3 Oct 2026)"),
]
BLOCK = re.compile(r"(<!-- SYNC: AGENTS\.md#(?P<head>[^>]+?) -->\n)(?P<body>.*?)(<!-- /SYNC -->)", re.S)


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"sync_rules: AGENTS.md has no '## {heading}' section")
    return m.group(1).strip("\n") + "\n"


def sync(text, source):
    return BLOCK.sub(lambda m: m.group(1) + section(source, m.group("head").strip()) + m.group(4), text)


def stale_hits():
    hits = []
    for pattern in SCAN:
        for path in sorted(ROOT.glob(pattern)):
            for n, line in enumerate(path.read_text().splitlines(), 1):
                for rx, why in STALE:
                    if re.search(rx, line, re.I):
                        hits.append(f"{path.relative_to(ROOT)}:{n}: stale ({why}): {line.strip()[:120]}")
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    source = SOURCE.read_text()
    problems = []
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text()
        if not BLOCK.search(text):
            problems.append(f"{rel}: no SYNC block")
            continue
        new = sync(text, source)
        if new != text:
            if a.check:
                problems.append(f"{rel}: SYNC block out of date (run python3 scripts/sync_rules.py)")
            else:
                path.write_text(new)
                print(f"synced {rel}")
    problems += stale_hits()
    for p in problems:
        print(p)
    if problems:
        return 1
    print("rules OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
