#!/usr/bin/env python3
"""Refresh the snapshots built into the Studio Kanban page (https://claude.ai/artifact/Hhk519dkbHMzeaZfp3efhc).

The page reads both repos live through the viewer's GitHub connector. When that link isn't available, it shows the
snapshot built into the page, so Claude rebuilds that snapshot a few times a day from:
  - HOS: 00_Brand/Channel-Setup/PIPELINE.json in history-of-science (main)
  - OWB: every 02_Video-Projects/*/status.json in this repo (main)

  python3 scripts/kanban_snapshot.py <page.html> --hos <history-of-science checkout> [--out <page.html>]

It replaces only the two `const SNAPSHOT = …;` / `const OWB_SNAPSHOT = …;` lines, fails if either is missing, and
prints "unchanged" when the data is the same (so nothing needs republishing).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def js(obj) -> str:
    # `</` escaped so no value can close the page's script tag.
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def rebuild(html: str, hos: dict, owb: list[dict]) -> str:
    for name in ("SNAPSHOT", "OWB_SNAPSHOT"):
        if len(re.findall(rf"^const {name} = .*;$", html, flags=re.M)) != 1:
            raise SystemExit(f"page has no single `const {name} = …;` line; not touching it")
    html = re.sub(r"^const SNAPSHOT = .*;$", lambda m: "const SNAPSHOT = " + js(hos) + ";", html, flags=re.M)
    return re.sub(r"^const OWB_SNAPSHOT = .*;$", lambda m: "const OWB_SNAPSHOT = " + js(owb) + ";", html, flags=re.M)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", type=Path)
    ap.add_argument("--hos", type=Path, required=True, help="history-of-science checkout on main")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    hos = json.loads((a.hos / "00_Brand/Channel-Setup/PIPELINE.json").read_text())
    if not isinstance(hos.get("films"), list):
        raise SystemExit("PIPELINE.json has no films list; not touching the page")
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    old = a.page.read_text()
    new = rebuild(old, hos, owb)
    (a.out or a.page).write_text(new)
    print("unchanged" if new == old else f"updated: HOS {hos.get('updated')} ({len(hos['films'])} films), OWB {len(owb)} films")
    return 0


if __name__ == "__main__":
    sys.exit(main())
