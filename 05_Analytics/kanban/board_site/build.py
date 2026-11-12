#!/usr/bin/env python3
"""Build the Studio Kanban site (the Studio app is the home page: Ben, 28 Oct 2026).

  python3 05_Analytics/kanban/board_site/build.py [--out DIR]    # default: …/board_site/dist

Outputs:
  dist/index.html     — Studio app (Ben, 28 Oct 2026): Overview, Videos, Review, Agents, Schedule (/)
  (/board, the five-lane per-video tracker, was retired on 10 Nov 2026: Ben, "This seems legacy. I think we can
   remove this section." The Studio app's Videos and Review tabs do its job. vercel.json redirects /board to /, so old
   links with #v=<video> or #k=<key> still land on the right page. Its files are in _archive/05_Analytics/kanban/.
   /classic, the October swim-lane board, was retired the same way on 28 Oct.)
  dist/tracker.html   — Channel Tracker web app (/tracker)
  dist/ai.html        — AI & credits: who is up, who is Chief, credit left per plan, where it went (/ai)
  dist/version.json, updater.js, static/, tracker.webmanifest

Data still comes from board.json on the `board-data` branch (scripts/board_publish.py). Page changes need a
direct upload to Cloudflare Pages: build, then `npx wrangler pages deploy` in this folder; data changes do not. api/checks.js (Ben's ticks → the studio thread / HOS #180)
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
AI_PAGE = HERE.parent / "ai_credits.html"
STUDIO = HERE.parent / "studio_app.html"
TRACKER = HERE.parent.parent / "dashboard" / "template.html"
TRACKER_DATA = HERE.parent.parent / "dashboard" / "data.json"



# The tracker wears the Studio's dark colours on the board site (Ben, 10 Nov 2026: one look across the pages on a
# phone). Its template already has a dark theme for `data-theme="dark"`; the colours below are studio_app.html's.
TRACKER_HEAD = """<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0B111B">
<link rel="manifest" href="/tracker.webmanifest">
<link rel="apple-touch-icon" href="/static/tracker-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/tracker-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tracker">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>body{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}.eyebrow a{color:inherit}
.studio-back{display:inline-flex;align-items:center;min-height:44px;margin:-10px 0 2px;font:600 .95rem var(--f-display);color:var(--accent);text-decoration:none}
#tracker-refresh{justify-self:start;min-height:44px}
html[data-theme="dark"]:root{--bg:#0B111B;--panel:#172433;--line:#243244;--grid:#1F2D3F;--chip:#1B2A3B;--ink:#F1F5F9;--ink-2:#B6C2D2;--ink-3:#94A3B8}</style>
</head><body>
"""

TRACKER_PATCHES = [
    ('<span class="eyebrow">YouTube · daily snapshot</span>',
     '<a class="studio-back" href="/">‹ Studio</a><span class="eyebrow">YouTube · daily snapshot · <a href="/">Studio board</a></span>'),
    ('<div class="stamp" id="stamp"></div>', '<div class="stamp" id="stamp"></div>\n  <div class="stamp" id="livestamp"></div><button type="button" id="tracker-refresh" class="tab">↻ Refresh data</button>'),
    ('(() => {\n  let DATA = { channels: [] };\n  try { DATA = JSON.parse(document.getElementById("tracker-data").textContent); } catch (e) { /* template without data */ }',
     'window.__trackerStart = (DATA) => {\n  DATA = DATA || { channels: [] };'),
]


def app_version() -> str:
    files = [TRACKER, AI_PAGE, STUDIO, HERE / "studio_app.js", HERE / "build.py",
             HERE / "ai_app.js", HERE / "tracker_loader.js", HERE / "updater.js", HERE / "api" / "checks.js",
             HERE / "api" / "data.js"]
    return hashlib.sha256(b"\0".join(f.read_bytes() for f in files if f.exists())).hexdigest()[:16]


def versioned_page(html: str) -> str:
    marker = f'<meta name="studio-version" content="{app_version()}"><script src="/updater.js" defer></script>'
    return html.replace("</head>", marker + "</head>", 1)


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


def build_host_config(out: pathlib.Path) -> None:
    # One routing/header list serves both hosts; never hand-maintain a second copy.
    config = json.loads((HERE / "vercel.json").read_text())
    redirects = [f"{x['source']} {x['destination']} {301 if x['permanent'] else 302}" for x in config["redirects"]]
    # Pages resolves .html files at their clean URL itself. A 200 rewrite back to
    # .html triggers its canonical redirect to the same clean URL and loops.
    for rule in config["rewrites"]:
        if rule["destination"] != rule["source"].rstrip("/") + ".html":
            redirects.append(f"{rule['source']} {rule['destination']} 200")
    (out / "_redirects").write_text("\n".join(redirects) + "\n")
    headers = []
    for rule in config["headers"]:
        headers.append(rule["source"])
        headers.extend(f"  {h['key']}: {h['value']}" for h in rule["headers"])
    (out / "_headers").write_text("\n".join(headers) + "\n")
    (out / "_routes.json").write_text(json.dumps({"version": 1, "include": ["/api/*"], "exclude": []}))
    # Only _worker.js is executable; no handler sources or secrets are public assets.
    worker = out / "_worker.js"
    worker.mkdir()
    for name in ("cf_adapter.js", "benauth.js", "r2sign.js", "watchsign.js"):
        shutil.copy(HERE / name, worker / name)
    shutil.copy(HERE / "cf_worker.js", worker / "index.js")
    shutil.copytree(HERE / "api", worker / "api")


def build(out: pathlib.Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    build_tracker(out)
    build_ai(out)
    build_studio(out)
    build_host_config(out)
    (out / "version.json").write_text(json.dumps({"version": app_version()}))
    shutil.copy(HERE / "updater.js", out / "updater.js")
    print(f"built {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "dist")
    build(ap.parse_args().out)
