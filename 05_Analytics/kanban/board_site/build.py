#!/usr/bin/env python3
"""Build the Studio Kanban site (Ben, 24 Oct 2026: simple per-video tracker is the home page).

  python3 05_Analytics/kanban/board_site/build.py [--out DIR]    # default: …/board_site/dist

Outputs:
  dist/index.html     — Studio app (Ben, 28 Oct 2026): Overview, Videos, Review, Agents, Schedule (/)
  dist/board.html     — five-lane per-video tracker, where Ben ticks OK / changes (/board)
  (/classic, the October swim-lane board, is retired: vercel.json redirects it to /; build_classic stays for reference)
  dist/tracker.html   — Channel Tracker web app (/tracker)
  dist/ai.html        — AI & credits: who is up, who is Chief, credit left per plan, where it went (/ai)
  dist/version.json, updater.js, static/, tracker.webmanifest

Data still comes from board.json on the `board-data` branch (scripts/board_publish.py). Page changes need a
redeploy of the Vercel project studio-kanban; data changes do not. api/checks.js (Ben's ticks → OWB #264 / HOS #180)
and vercel.json sit next to this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE.parent / "studio_kanban.html"
SIMPLE = HERE.parent / "video_tracker.html"
AI_PAGE = HERE.parent / "ai_credits.html"
STUDIO = HERE.parent / "studio_app.html"
TRACKER = HERE.parent.parent / "dashboard" / "template.html"
TRACKER_DATA = HERE.parent.parent / "dashboard" / "data.json"
ROOT = HERE.parents[2]

FOOTER = ('<footer><details><summary>Data sources and refresh</summary>This board updates itself. The Mac mini rebuilds its data from <span class="mono">main</span> of both '
          'repos whenever a job in the queue moves (claimed, a step done, done, blocked, released) and checks every minute, and pushes it only '
          'when something changed (<span class="mono">scripts/board_publish.py</span> → branch <span class="mono">board-data</span>). '
          'This page re-reads it every minute; the time at the top is the last real change. <b>HOS</b> comes from '
          '<span class="mono">00_Brand/Channel-Setup/PIPELINE.json</span> in history-of-science; <b>OWB</b> from each film\'s '
          '<span class="mono">02_Video-Projects/&lt;film&gt;/status.json</span>, the job queue and '
          '<span class="mono">05_Analytics/kanban/film_briefs.json</span> in orbit-with-ben ("chief" is shown as Grok). '
          'Your ticks are saved straight away with your board link; the Mac mini picks them up within about a minute. '
          'YouTube numbers: <a href="/tracker">Channel Tracker</a>. Studio app: <a href="/">/</a> · video board: <a href="/board">/board</a>.</details></footer>')

sys.path.insert(0, str(ROOT / "scripts"))
from kanban_snapshot import release_record

RELEASE_RECORDS = {}
for status_file in (ROOT / "02_Video-Projects").glob("*/status.json"):
    film = json.loads(status_file.read_text()).get("film", "")
    receipt = release_record(film)
    if receipt:
        RELEASE_RECORDS["OWB:" + film] = receipt

PATCHES = [
    ("const RELEASE_RECORDS = {};", "const RELEASE_RECORDS = " + json.dumps(RELEASE_RECORDS).replace("</", "<\\/") + ";"),
    ('<div class="sub" id="asof">Loading…</div>',
     '<div class="sub" id="asof">Loading…</div><div class="sub"><a href="/board" style="color:inherit">Video board →</a> · <a href="/tracker" style="color:inherit">Channel Tracker →</a></div>'),
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
    ('<div class="stamp" id="stamp"></div>', '<div class="stamp" id="stamp"></div>\n  <div class="stamp" id="livestamp"></div><button type="button" id="tracker-refresh" class="tab">Refresh data</button>'),
    ('(() => {\n  let DATA = { channels: [] };\n  try { DATA = JSON.parse(document.getElementById("tracker-data").textContent); } catch (e) { /* template without data */ }',
     'window.__trackerStart = (DATA) => {\n  DATA = DATA || { channels: [] };'),
]


def app_version() -> str:
    files = [SIMPLE, PAGE, TRACKER, AI_PAGE, STUDIO, HERE / "studio_app.js", HERE / "build.py", HERE / "shim.js", HERE / "live.js",
             HERE / "tracker_app.js", HERE / "ai_app.js", HERE / "tracker_loader.js", HERE / "updater.js", HERE / "api" / "checks.js"]
    return hashlib.sha256(b"\0".join(f.read_bytes() for f in files if f.exists())).hexdigest()[:16]


def versioned_page(html: str) -> str:
    marker = f'<meta name="studio-version" content="{app_version()}"><script src="/updater.js" defer></script>'
    return html.replace("</head>", marker + "</head>", 1)


def baked_tracker() -> dict:
    """Best-effort offline tracker from this checkout (+ optional /tmp/hos-sparse PIPELINE)."""
    try:
        from video_tracker import build_videos
        hos_path = pathlib.Path("/tmp/hos-sparse/00_Brand/Channel-Setup/PIPELINE.json")
        if not hos_path.exists():
            # On Vercel there is no HOS checkout: bake the Mini's last published tracker instead (offline fallback).
            import urllib.request
            url = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json"
            with urllib.request.urlopen(url, timeout=15) as r:
                live = json.loads(r.read().decode())
            tracker = live.get("tracker") or {}
            if tracker.get("videos"):
                return tracker
            return {"updatedAt": "", "lanes": [], "videos": [], "note": "no HOS PIPELINE at build time"}
        hos = json.loads(hos_path.read_text())
        owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
        for film in owb:
            receipt = release_record(str(film.get("film", "")))
            if receipt:
                film["release"] = receipt
        briefs = {}
        bf = ROOT / "05_Analytics" / "kanban" / "film_briefs.json"
        if bf.exists():
            briefs = json.loads(bf.read_text()).get("films") or {}
        jobs = []
        q = ROOT / "jobs" / "queue.json"
        if q.exists():
            jobs = json.loads(q.read_text()).get("jobs") or []
        checks = {}
        try:
            import urllib.request
            with urllib.request.urlopen("https://studio-kanban.vercel.app/api/checks", timeout=10) as r:
                checks = json.loads(r.read().decode()).get("checks") or {}
        except Exception:
            pass
        return build_videos(hos=hos, owb=owb, briefs=briefs, jobs=jobs, checks=checks)
    except Exception as e:
        return {"updatedAt": "", "lanes": [], "videos": [], "error": str(e)[:200]}


def build_simple(out: pathlib.Path) -> None:
    html = SIMPLE.read_text()
    marker = "<script>\n/* VIDEO_TRACKER_BOOT */\n</script>"
    if html.count(marker) != 1:
        sys.exit("build: expected one VIDEO_TRACKER_BOOT script block in video_tracker.html")
    boot = (HERE / "tracker_app.js").read_text()
    baked = json.dumps(baked_tracker(), ensure_ascii=False).replace("</", "<\\/")
    inject = f'<script type="application/json" id="baked-tracker">{baked}</script>\n<script>\n{boot}\n</script>'
    html = html.replace(marker, inject)
    (out / "board.html").write_text(versioned_page(html))
    print(f"built {out / 'board.html'} ({len(html):,} bytes)")


def build_studio(out: pathlib.Path) -> None:
    html = STUDIO.read_text()
    marker = "<script>\n/* STUDIO_APP_BOOT */\n</script>"
    if html.count(marker) != 1:
        sys.exit("build: expected one STUDIO_APP_BOOT script block in studio_app.html")
    html = html.replace(marker, "<script>\n" + (HERE / "studio_app.js").read_text() + "\n</script>")
    (out / "index.html").write_text(versioned_page(html))
    print(f"built {out / 'index.html'} ({len(html):,} bytes)")


def build_ai(out: pathlib.Path) -> None:
    html = AI_PAGE.read_text()
    marker = "<script>\n/* AI_APP_BOOT */\n</script>"
    if html.count(marker) != 1:
        sys.exit("build: expected one AI_APP_BOOT script block in ai_credits.html")
    html = html.replace(marker, "<script>\n" + (HERE / "ai_app.js").read_text() + "\n</script>")
    (out / "ai.html").write_text(versioned_page(html))
    print(f"built {out / 'ai.html'} ({len(html):,} bytes)")


def build_classic(out: pathlib.Path) -> None:
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
    end = "</script>\n\n</body></html>"
    if html.count(end) != 1:
        sys.exit("build: expected the page to end with its script, then </body></html>")
    html = html.replace(end, "</script>\n<script>\n" + (HERE / "live.js").read_text() + "</script>\n\n</body></html>")
    (out / "classic.html").write_text(versioned_page(html))
    print(f"built {out / 'classic.html'} ({len(html):,} bytes)")


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
    try:
        baked = json.dumps(json.loads(TRACKER_DATA.read_text()), separators=(",", ":"))
    except (OSError, ValueError):
        baked = '{"channels":[]}'
    if html.count("__TRACKER_DATA__") != 1:
        sys.exit("build: expected one __TRACKER_DATA__ in dashboard/template.html")
    html = html.replace("__TRACKER_DATA__", baked.replace("<", "\\u003c"))
    (out / "tracker.html").write_text(versioned_page(TRACKER_HEAD + html + "\n</body></html>\n"))
    shutil.copy(HERE / "tracker.webmanifest", out / "tracker.webmanifest")
    if (out / "static").exists():
        shutil.rmtree(out / "static")
    shutil.copytree(HERE / "static", out / "static")
    print(f"built {out / 'tracker.html'} ({len(html):,} bytes)")


def build(out: pathlib.Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    build_simple(out)
    build_tracker(out)
    build_ai(out)
    build_studio(out)
    (out / "version.json").write_text(json.dumps({"version": app_version()}))
    shutil.copy(HERE / "updater.js", out / "updater.js")
    print(f"built {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "dist")
    build(ap.parse_args().out)
