#!/usr/bin/env python3
"""Refresh the snapshots built into the Studio Kanban page (https://claude.ai/artifact/Hhk519dkbHMzeaZfp3efhc).

The page reads both repos live through the viewer's GitHub connector. When that link isn't available, it shows the
snapshot built into the page, so Claude rebuilds that snapshot a few times a day from:
  - HOS: 00_Brand/Channel-Setup/PIPELINE.json in history-of-science (main)
  - OWB: every 02_Video-Projects/*/status.json in this repo (main)

  python3 scripts/kanban_snapshot.py <page.html> --hos <history-of-science checkout> [--out <page.html>]
  python3 scripts/kanban_snapshot.py --hos <checkout> --db-out <dir>    # board/hos, board/owb, board/credits for ArtifactData

Since 7 Oct the page also reads `board/hos` ({updatedAt, pipeline}) and `board/owb` ({updatedAt, films}) from its own
store, which Claude writes on a schedule with ArtifactData (file_path = the JSON files --db-out writes). That keeps
the board current without the viewer's GitHub connector.

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
    ap.add_argument("page", type=Path, nargs="?")
    ap.add_argument("--hos", type=Path, required=True, help="history-of-science checkout on main")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--db-out", type=Path, default=None, help="write hos.json and owb.json store documents here")
    ap.add_argument("--chief", default="", help="acting Chief from the relay's last thread line, e.g. Cursor (into owb.json)")
    ap.add_argument("--chief-since", default="", help="ISO time that agent became Chief")
    ap.add_argument("--chief-next", default="", help="comma list: next in line")
    ap.add_argument("--chief-note", default="", help="one short line, e.g. Grok Bot out of credit")
    a = ap.parse_args(argv)
    hos = json.loads((a.hos / "00_Brand/Channel-Setup/PIPELINE.json").read_text())
    if not isinstance(hos.get("films"), list):
        raise SystemExit("PIPELINE.json has no films list; not touching the page")
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    if a.db_out:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        a.db_out.mkdir(parents=True, exist_ok=True)
        (a.db_out / "hos.json").write_text(json.dumps({"updatedAt": now, "pipeline": hos}, ensure_ascii=False))
        q = ROOT / "jobs" / "queue.json"
        live = [dict({k: j.get(k, "") for k in ("id", "title", "needs", "status", "by", "eta", "film", "stage", "after", "ref", "result")},
                     last=(j.get("history") or [{}])[-1])  # who touched it last, when, and their note (the board shows it)
                for j in (json.loads(q.read_text())["jobs"] if q.exists() else []) if j["status"] in ("open", "claimed", "blocked")]
        doc = {"updatedAt": now, "films": owb, "jobs": live}
        if a.chief:
            doc["chief"] = {"name": a.chief, "since": a.chief_since, "note": a.chief_note,
                            "next": [x.strip() for x in a.chief_next.split(",") if x.strip()]}
        (a.db_out / "owb.json").write_text(json.dumps(doc, ensure_ascii=False))
        # board/credits (Ben, 8 Oct): the AI spend month from scripts/ai_spend.py, plus HOS's own credit checks
        sys.path.insert(0, str(ROOT / "scripts"))
        import ai_spend
        credits = ai_spend.build_doc(ai_spend.load())
        credits["hosChecks"] = hos.get("credits", [])
        (a.db_out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False))
        print(f"store documents: {a.db_out}/hos.json ({len(hos['films'])} HOS films), {a.db_out}/owb.json ({len(owb)} OWB films), "
              f"{a.db_out}/credits.json ({credits['lines']} spend lines since {credits['period'].get('start')})")
        if not a.page:
            return 0
    if not a.page:
        raise SystemExit("give a page file, --db-out, or both")
    old = a.page.read_text()
    new = rebuild(old, hos, owb)
    (a.out or a.page).write_text(new)
    print("unchanged" if new == old else f"updated: HOS {hos.get('updated')} ({len(hos['films'])} films), OWB {len(owb)} films")
    return 0


if __name__ == "__main__":
    sys.exit(main())
