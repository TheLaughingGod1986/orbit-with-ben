#!/usr/bin/env python3
"""Build the self-updating Studio Kanban site from the claude.ai artifact page (Ben, 9 Oct).

  python3 05_Analytics/kanban/board_site/build.py [--out DIR]    # default: 05_Analytics/kanban/board_site/dist

Takes ../studio_kanban.html unchanged (the Claude artifact keeps working from it), inlines shim.js before the page's
script, and makes a few small text patches: ticks only show with a saving link, the header shows the real time of the
last data change, and the footer says where the data comes from. Output: dist/index.html.

Also builds the Channel Tracker as a phone web app (Ben, 10 Oct): dist/tracker.html, served at /tracker (vercel.json
rewrite), from ../../dashboard/template.html (the same template 07_Content-Ops/scripts/analytics-report.ts fills in for
dashboard.html). Its data isn't built in: tracker_loader.js reads tracker.json from the `board-data` branch at runtime
(main's 05_Analytics/dashboard/data.json, pushed there by scripts/board_publish.py after the 06:40 snapshot). The copy of
data.json on main at build time is built in only as the offline fallback, and the page says when it's showing it. Plus
tracker.webmanifest and static/ (home-screen icons), so "Add to Home Screen" opens it full screen.

Hosting: Vercel project studio-kanban (not git-connected, so pushes to main never deploy it). It is deployed from a
commit of this repo with root directory 05_Analytics/kanban/board_site, build command `python3 build.py`, output
directory `dist`; api/checks.js (Ben's ticks, Vercel Blob) and vercel.json sit next to this file. Data changes never
need a redeploy; only page changes do. Fails loudly if a patch target has moved, so a redesign of the page can't silently break the host.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE.parent / "studio_kanban.html"
TRACKER = HERE.parent.parent / "dashboard" / "template.html"
TRACKER_DATA = HERE.parent.parent / "dashboard" / "data.json"

FOOTER = ('<footer>This board updates itself. The Mac mini rebuilds its data from <span class="mono">main</span> of both '
          'repos whenever a job in the queue moves (claimed, done, blocked, released) and every 5 minutes, and pushes it only '
          'when something changed (<span class="mono">scripts/board_publish.py</span> → branch <span class="mono">board-data</span>). '
          'This page re-reads it every minute; the time at the top is the last real change. <b>HOS</b> comes from '
          '<span class="mono">00_Brand/Channel-Setup/PIPELINE.json</span> in history-of-science; <b>OWB</b> from each film\'s '
          '<span class="mono">02_Video-Projects/&lt;film&gt;/status.json</span>, the job queue and '
          '<span class="mono">05_Analytics/kanban/film_briefs.json</span> in orbit-with-ben ("chief" is shown as Grok). '
          'Your ticks are saved straight away with your board link; the studio agent picks them up within the hour. '
          'YouTube numbers: <a href="/tracker">Channel Tracker</a>.</footer>')

PATCHES = [
    ('<div class="sub" id="asof">Loading…</div>',
     '<div class="sub" id="asof">Loading…</div><div class="sub"><a href="/tracker" style="color:inherit">Channel Tracker →</a></div>'),
    ("dbApi = db;", "dbApi = db.canWrite===false ? null : db;"),
    ('t.textContent = `Updated by the studio agent · ${fw(fromDb.hosAt || fromDb.owbAt)}`;',
     't.textContent = `Last change ${fw((window.__boardData||{}).dataChangedAt || fromDb.hosAt || fromDb.owbAt)} · checks every minute`;'),
    ('bits.push(`HOS board updated ${fd(pd(data.updated))} by ${data.updated_by||"—"}`);',
     'bits.push(`HOS updated ${source==="db"&&fromDb.hosAt?fw(fromDb.hosAt):fd(pd(data.updated))} by ${data.updated_by||"—"}`);'),
]


TRACKER_HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f6f7f9">
<link rel="manifest" href="/tracker.webmanifest">
<link rel="apple-touch-icon" href="/static/tracker-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/tracker-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tracker">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>body{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}.eyebrow a{color:inherit}</style>
</head><body>
"""

TRACKER_PATCHES = [
    ('<span class="eyebrow">YouTube · daily snapshot</span>',
     '<span class="eyebrow">YouTube · daily snapshot · <a href="/">Studio board</a></span>'),
    ('<div class="stamp" id="stamp"></div>', '<div class="stamp" id="stamp"></div>\n  <div class="stamp" id="livestamp"></div>'),
    ('(() => {\n  let DATA = { channels: [] };\n  try { DATA = JSON.parse(document.getElementById("tracker-data").textContent); } catch (e) { /* template without data */ }',
     'window.__trackerStart = (DATA) => {\n  DATA = DATA || { channels: [] };'),
]


def build_tracker(out: pathlib.Path) -> None:
    html = TRACKER.read_text()
    for old, new in TRACKER_PATCHES:
        if html.count(old) != 1:
            sys.exit(f"build: expected one `{old[:60]}…` in dashboard/template.html; the page changed, update TRACKER_PATCHES")
        html = html.replace(old, new)
    end = "})();\n</script>"
    if html.count(end) != 1 or not html.rstrip().endswith("</script>"):
        sys.exit("build: expected the tracker script to end with one `})();` before </script>")
    html = html.replace(end, "};\n</script>\n<script>\n" + (HERE / "tracker_loader.js").read_text() + "</script>")
    try:  # offline fallback only; must be the real file from main, never anything made up
        baked = json.dumps(json.loads(TRACKER_DATA.read_text()), separators=(",", ":"))
    except (OSError, ValueError):
        baked = '{"channels":[]}'
    if html.count("__TRACKER_DATA__") != 1:
        sys.exit("build: expected one __TRACKER_DATA__ in dashboard/template.html")
    html = html.replace("__TRACKER_DATA__", baked.replace("<", "\\u003c"))
    (out / "tracker.html").write_text(TRACKER_HEAD + html + "\n</body></html>\n")
    shutil.copy(HERE / "tracker.webmanifest", out / "tracker.webmanifest")
    shutil.copytree(HERE / "static", out / "static")
    print(f"built {out / 'tracker.html'} ({len(html):,} bytes)")


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
    build_tracker(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "dist")
    build(ap.parse_args().out)
