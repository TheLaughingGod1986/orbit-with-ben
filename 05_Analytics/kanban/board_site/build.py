#!/usr/bin/env python3
"""Build the self-updating Studio Kanban site from the claude.ai artifact page (Ben, 9 Oct).

  python3 05_Analytics/kanban/board_site/build.py [--out DIR]    # default: 05_Analytics/kanban/board_site/dist

Takes ../studio_kanban.html unchanged (the Claude artifact keeps working from it), inlines shim.js before the page's
script, and makes a few small text patches: ticks only show with a saving link, the header shows the real time of the
last data change, and the footer says where the data comes from. Output: dist/index.html.

Hosting: Vercel project studio-kanban (not git-connected, so pushes to main never deploy it). It is deployed from a
commit of this repo with root directory 05_Analytics/kanban/board_site, build command `python3 build.py`, output
directory `dist`; api/checks.js (Ben's ticks, Vercel Blob) and vercel.json sit next to this file. Data changes never
need a redeploy; only page changes do. Fails loudly if a patch target has moved, so a redesign of the page can't silently break the host.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE.parent / "studio_kanban.html"

FOOTER = ('<footer>This board updates itself. The Mac mini rebuilds its data from <span class="mono">main</span> of both '
          'repos whenever a job in the queue moves (claimed, done, blocked, released) and every 5 minutes, and pushes it only '
          'when something changed (<span class="mono">scripts/board_publish.py</span> → branch <span class="mono">board-data</span>). '
          'This page re-reads it every minute; the time at the top is the last real change. <b>HOS</b> comes from '
          '<span class="mono">00_Brand/Channel-Setup/PIPELINE.json</span> in history-of-science; <b>OWB</b> from each film\'s '
          '<span class="mono">02_Video-Projects/&lt;film&gt;/status.json</span>, the job queue and '
          '<span class="mono">05_Analytics/kanban/film_briefs.json</span> in orbit-with-ben ("chief" is shown as Grok). '
          'Your ticks are saved with this link and reach the studio agent within 15 minutes.</footer>')

PATCHES = [
    ("dbApi = db;", "dbApi = db.canWrite===false ? null : db;"),
    ('t.textContent = `Updated by the studio agent · ${fw(fromDb.hosAt || fromDb.owbAt)}`;',
     't.textContent = `Last change ${fw((window.__boardData||{}).dataChangedAt || fromDb.hosAt || fromDb.owbAt)} · checks every minute`;'),
    ('bits.push(`HOS board updated ${fd(pd(data.updated))} by ${data.updated_by||"—"}`);',
     'bits.push(`HOS updated ${source==="db"&&fromDb.hosAt?fw(fromDb.hosAt):fd(pd(data.updated))} by ${data.updated_by||"—"}`);'),
]


def build(out: pathlib.Path) -> None:
    html = PAGE.read_text()
    for old, new in PATCHES:
        if html.count(old) != 1:
            sys.exit(f"build: expected one `{old[:60]}…` in studio_kanban.html; the page changed, update PATCHES")
        html = html.replace(old, new)
    start, end = html.find("<footer>"), html.find("</footer>")
    if start < 0 or end < start or html.count("<footer>") != 1:
        sys.exit("build: expected one <footer> in studio_kanban.html")
    html = html[:start] + FOOTER + html[end + len("</footer>"):]
    marker = "\n<script>\n"
    if html.count(marker) != 1:
        sys.exit("build: expected one bare <script> line in studio_kanban.html")
    html = html.replace(marker, "\n<script>\n" + (HERE / "shim.js").read_text() + "</script>" + marker, 1)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "index.html").write_text(html)
    print(f"built {out} ({len(html):,} bytes index.html)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "dist")
    build(ap.parse_args().out)
