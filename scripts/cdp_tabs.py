#!/usr/bin/env python3
"""One tab per site in the Mini's CDP Chrome browsers (Ben, 4 Nov 2026: Studio jobs kept opening new YouTube Studio
tabs and the Mini crashed; "if there's a tab open, it will use the tab open rather than keep opening many tabs").

Two parts:

1. For scripts (Playwright), instead of `ctx.new_page()`:

       from cdp_tabs import reuse_page
       page = reuse_page(ctx, "studio.youtube.com")     # existing Studio tab, else a blank tab, else one new tab

   It never opens a second tab for a site that already has one, and it brings the tab it returns to the front.

2. Janitor (launchd com.owb.tab-janitor, every 5 min, stdlib only, talks to Chrome's /json HTTP endpoints):

       python3 scripts/cdp_tabs.py tidy                  # ports 9223 (Orbit Studio) and 9222 (HOS Flow)
       python3 scripts/cdp_tabs.py list --port 9223

   Per browser it keeps the newest tab of each site and closes older duplicates (blank/new-tab pages count as one
   site), then caps the browser at MAX_TABS by closing the oldest. A tab is only closed once it has been seen for
   MIN_AGE_MIN minutes (3 h while a `studio` job is claimed, so a long upload's tab is never pulled away). Sign-in pages
   (accounts.google.com) and the last remaining tab are never closed. First-seen times live in
   ~/.cache/owb-cdp-tabs.json.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

PORTS = (9223, 9222)
KEEP_PER_SITE = 1
MAX_TABS = 6
MIN_AGE_MIN = 20
BUSY_MIN_AGE_MIN = 180   # while a Studio job is claimed
NEVER_CLOSE = ("accounts.google.com",)
BLANK = "(blank)"
STATE = os.path.expanduser("~/.cache/owb-cdp-tabs.json")


def site(url):
    if not url or url.startswith(("about:", "chrome://newtab", "chrome://new-tab-page", "chrome-search://")):
        return BLANK
    return urllib.parse.urlsplit(url).hostname or url


# ---------- Playwright helper ----------

def reuse_page(ctx, host):
    """Return a page on `host` from this browser context, reusing what's open. Opens at most one new tab."""
    pages = [p for p in ctx.pages if not p.is_closed()]
    for p in reversed(pages):                      # newest first
        if site(p.url) == host:
            _front(p)
            return p
    for p in reversed(pages):
        if site(p.url) == BLANK:
            _front(p)
            return p
    return ctx.new_page()


def _front(p):
    try:
        p.bring_to_front()
    except Exception:
        pass


# ---------- janitor (pure decision + HTTP) ----------

def plan_closes(tabs, first_seen, now, keep=KEEP_PER_SITE, max_tabs=MAX_TABS, min_age_s=MIN_AGE_MIN * 60):
    """tabs: [{'id','url'}] (pages only). first_seen: {id: epoch}. Returns ids to close, oldest first."""
    age = lambda t: now - first_seen.get(t["id"], now)
    closable = lambda t: age(t) >= min_age_s and site(t["url"]) not in NEVER_CLOSE
    newest_first = sorted(tabs, key=lambda t: first_seen.get(t["id"], now), reverse=True)
    close, seen_sites = [], {}
    for t in newest_first:
        s = site(t["url"])
        seen_sites[s] = seen_sites.get(s, 0) + 1
        if seen_sites[s] > keep and closable(t):
            close.append(t["id"])
    left = [t for t in newest_first if t["id"] not in close]
    for t in reversed(left):                       # oldest first
        if len(left) - sum(1 for x in left if x["id"] in close) <= max_tabs:
            break
        if closable(t):
            close.append(t["id"])
    remaining = len(tabs) - len(close)
    if remaining < 1 and close:                    # never close every tab
        close = close[:-1]
    return sorted(close, key=lambda i: first_seen.get(i, now))


def http(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as r:
        return r.read().decode()


def page_tabs(port):
    return [{"id": t["id"], "url": t.get("url", "")} for t in json.loads(http(port, "/json/list")) if t.get("type") == "page"]


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"))


def studio_job_running(queue=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jobs", "queue.json")):
    """True while any Studio-browser job is claimed (its tab may be mid-upload)."""
    try:
        return any(j.get("status") == "claimed" and j.get("kind") == "studio" for j in json.load(open(queue))["jobs"])
    except Exception:
        return True                                 # unsure: be careful


def tidy(ports=PORTS, dry=False):
    state, now, report = load_state(), time.time(), []
    min_age_s = BUSY_MIN_AGE_MIN * 60 if studio_job_running() else MIN_AGE_MIN * 60
    for port in ports:
        try:
            tabs = page_tabs(port)
        except Exception as e:
            report.append(f"{port}: not reachable ({e.__class__.__name__})")
            continue
        seen = state.get(str(port), {})
        seen = {t["id"]: seen.get(t["id"], now) for t in tabs}   # forget closed tabs
        ids = plan_closes(tabs, seen, now, min_age_s=min_age_s)
        for i in ids:
            if not dry:
                try:
                    http(port, f"/json/close/{i}")
                except Exception:
                    continue
            seen.pop(i, None)
        state[str(port)] = seen
        url = {t["id"]: t["url"] for t in tabs}
        report.append(f"{port}: {len(tabs)} tabs, {'would close' if dry else 'closed'} {len(ids)}"
                      + "".join(f"\n  - {site(url[i])}" for i in ids))
    if not dry:
        save_state(state)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tidy"); t.add_argument("--port", type=int, action="append"); t.add_argument("--dry-run", action="store_true")
    l = sub.add_parser("list"); l.add_argument("--port", type=int, default=9223)
    a = ap.parse_args()
    if a.cmd == "list":
        for x in page_tabs(a.port):
            print(site(x["url"]), x["url"][:100])
        return 0
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *tidy(tuple(a.port or PORTS), dry=a.dry_run), sep="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
