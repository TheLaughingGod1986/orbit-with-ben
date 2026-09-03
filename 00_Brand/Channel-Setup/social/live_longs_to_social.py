#!/usr/bin/env python3
"""
Share live YouTube longs as soft link posts on Threads + Facebook Page.

Usage:
  python3 live_longs_to_social.py --list
  python3 live_longs_to_social.py --once
  python3 live_longs_to_social.py --once --platform threads
  python3 live_longs_to_social.py --seed-all

Uses Google Chrome + clipboard paste (logged-in session). TikTok stays paused.
Shorts stay on the existing Meta/Threads Shorts watchers.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

AUTO = Path(__file__).resolve().parent
SETUP = AUTO.parent
sys.path.insert(0, str(SETUP / "social"))

import live_longs as longs  # noqa: E402

LOG = SETUP / "social" / "live_longs_auto.log"


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def set_clipboard(text: str) -> None:
    proc = subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
    _ = proc


def run_osascript(script: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".applescript", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        proc = subprocess.run(
            ["osascript", path], capture_output=True, text=True, timeout=180
        )
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout or "osascript failed")[:400])
        return (proc.stdout or "").strip()
    finally:
        Path(path).unlink(missing_ok=True)


def ensure_orbit_chrome() -> None:
    script = r'''
tell application "Google Chrome"
  activate
  if (count of windows) = 0 then make new window
end tell
'''
    try:
        run_osascript(script)
    except Exception as e:
        log(f"chrome activate warn: {e}")


def post_threads_link(film: dict) -> dict:
    set_clipboard(film["_caption"])
    time.sleep(0.2)
    script = r'''
tell application "Google Chrome"
  activate
  if (count of windows) = 0 then make new window
  set URL of active tab of front window to "https://www.threads.com/"
  delay 4
  set opened to execute active tab of front window javascript "(() => {
    for (const n of document.querySelectorAll('div[role=button], button, span, a')) {
      const t=(n.innerText||'').trim();
      const al=(n.getAttribute('aria-label')||'');
      if (/What.?s new|Create|New thread|Post/i.test(t) || /new|create|compose/i.test(al)) {
        const r=n.getBoundingClientRect();
        if (r.width>30 && r.height>12) { n.click(); return 'composer'; }
      }
    }
    return 'no composer';
  })()"
  delay 1.5
end tell
tell application "System Events"
  tell process "Google Chrome"
    set frontmost to true
    delay 0.3
    keystroke "v" using {command down}
  end tell
end tell
delay 1
tell application "Google Chrome"
  set posted to execute active tab of front window javascript "(() => {
    for (const b of document.querySelectorAll('button, div[role=button]')) {
      const t=(b.innerText||'').trim();
      if (/^Post$/i.test(t)) {
        const r=b.getBoundingClientRect();
        if (r.width>30 && r.height>10) { b.click(); return 'posted'; }
      }
    }
    return 'no post btn';
  })()"
  delay 3
  return opened & " | " & posted
end tell
'''
    out = run_osascript(script)
    ok = out.strip().endswith("posted") or "| posted" in out
    return {
        "status": "posted_link_card" if ok else "error",
        "method": "chrome_clipboard",
        "detail": out[:300],
    }


def _cdp_ports() -> list[int]:
    # Prefer takeover Chrome (9333), then Meta profile (9223), then Threads (9222).
    return [9333, 9223, 9222]


def post_facebook_link_cdp(film: dict) -> dict:
    """Post Orbit Page link card via Playwright CDP (mouse clicks; Create → Next → Post)."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return {"status": "error", "method": "cdp", "detail": f"no playwright: {e}"}

    page_url = "https://www.facebook.com/profile.php?id=61592833318203"
    caption = film["_caption"]
    last_err = ""

    for port in _cdp_ports():
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
                if not browser.contexts:
                    last_err = f"port {port}: no context"
                    continue
                ctx = browser.contexts[0]
                page = ctx.new_page()
                page.set_viewport_size({"width": 1400, "height": 900})
                page.goto(page_url, wait_until="domcontentloaded", timeout=90000)
                time.sleep(3)
                for _ in range(3):
                    page.keyboard.press("Escape")
                    time.sleep(0.15)

                # Switch into Orbit Page if prompted
                body = page.inner_text("body")
                if "Switch into Orbit" in body:
                    page.evaluate(
                        """() => {
                      for (const n of document.querySelectorAll('div[role=button], button')) {
                        if ((n.innerText||'').trim()==='Switch') { n.click(); break; }
                      }
                    }"""
                    )
                    time.sleep(2)
                    dlg = page.locator("[role=dialog]").filter(has_text="Switch profiles")
                    if dlg.count():
                        btn = dlg.locator(
                            'div[role=button]:has-text("Switch"), button:has-text("Switch")'
                        )
                        if btn.count():
                            box = btn.last.bounding_box()
                            if box:
                                page.mouse.click(
                                    box["x"] + box["width"] / 2,
                                    box["y"] + box["height"] / 2,
                                )
                            time.sleep(5)

                mind = page.get_by_text("What's on your mind?", exact=True)
                if not mind.count():
                    page.close()
                    last_err = f"port {port}: no composer"
                    continue
                box = mind.first.bounding_box()
                if not box:
                    page.close()
                    last_err = f"port {port}: no mind box"
                    continue
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(2)

                create = page.locator("[role=dialog]").filter(has_text="Create post")
                if not create.count():
                    page.close()
                    last_err = f"port {port}: create dialog missing"
                    continue
                ed = create.locator("[contenteditable=true]").first
                ebox = ed.bounding_box()
                if not ebox:
                    page.close()
                    last_err = f"port {port}: no editor"
                    continue
                page.mouse.click(ebox["x"] + 20, ebox["y"] + 20)
                page.keyboard.insert_text(caption)
                time.sleep(2)

                next_coords = page.evaluate(
                    """() => {
                  const d=[...document.querySelectorAll('[role=dialog]')]
                    .find(x=>/Create post/i.test(x.innerText||''));
                  if(!d) return null;
                  for (const el of d.querySelectorAll('[role=button],button')) {
                    if ((el.innerText||'').trim()==='Next') {
                      const r=el.getBoundingClientRect();
                      return {x:r.x+r.width/2,y:r.y+r.height/2};
                    }
                  }
                  return null;
                }"""
                )
                if not next_coords:
                    page.close()
                    last_err = f"port {port}: no Next"
                    continue
                page.mouse.click(next_coords["x"], next_coords["y"])
                time.sleep(2)

                post_coords = page.evaluate(
                    """() => {
                  const d=[...document.querySelectorAll('[role=dialog]')]
                    .find(x=>/Post settings/i.test(x.innerText||''));
                  if(!d) return null;
                  const posts=[...d.querySelectorAll('[role=button],button')]
                    .filter(el => (el.innerText||'').trim()==='Post');
                  if(!posts.length) return null;
                  const r=posts.at(-1).getBoundingClientRect();
                  return {x:r.x+r.width/2,y:r.y+r.height/2};
                }"""
                )
                if not post_coords:
                    page.close()
                    last_err = f"port {port}: no Post on settings"
                    continue
                page.mouse.click(post_coords["x"], post_coords["y"])

                ok = False
                for _ in range(45):
                    body = page.inner_text("body")
                    settings = page.locator("[role=dialog]").filter(
                        has_text="Post settings"
                    ).count()
                    create_n = page.locator("[role=dialog]").filter(
                        has_text="Create post"
                    ).count()
                    if settings == 0 and create_n == 0 and "Posting" not in body:
                        ok = True
                        break
                    time.sleep(1)
                page.close()
                if ok:
                    return {
                        "status": "posted_link_card",
                        "method": "cdp_mouse",
                        "port": port,
                    }
                last_err = f"port {port}: posting timeout"
        except Exception as e:
            last_err = f"port {port}: {e}"[:240]
            continue

    return {"status": "error", "method": "cdp_mouse", "detail": last_err[:300]}


def post_facebook_link(film: dict) -> dict:
    """Prefer CDP mouse flow; fall back to AppleScript clipboard paste."""
    cdp = post_facebook_link_cdp(film)
    if cdp.get("status") in {"posted_link_card", "posted", "ok"}:
        return cdp

    set_clipboard(film["_caption"])
    time.sleep(0.2)
    page_url = "https://www.facebook.com/profile.php?id=61592833318203"
    script = f'''
tell application "Google Chrome"
  activate
  if (count of windows) = 0 then make new window
  set URL of active tab of front window to "{page_url}"
  delay 5
  set opened to execute active tab of front window javascript "(() => {{
    for (const n of document.querySelectorAll('[role=button], div, span')) {{
      const t=(n.innerText||'').trim();
      if (/What.?s on your mind|Create post|Write something/i.test(t)) {{
        const r=n.getBoundingClientRect();
        if (r.width>60 && r.height>12 && r.height<90) {{ n.click(); return 'composer'; }}
      }}
    }}
    return 'no composer';
  }})()"
  delay 2
end tell
tell application "System Events"
  tell process "Google Chrome"
    set frontmost to true
    delay 0.3
    keystroke "v" using {{command down}}
  end tell
end tell
delay 1.2
tell application "Google Chrome"
  set posted to execute active tab of front window javascript "(() => {{
    for (const b of document.querySelectorAll('[role=button], button')) {{
      const t=(b.innerText||'').trim();
      if (/^Post$/i.test(t) || /^Publish$/i.test(t)) {{
        const r=b.getBoundingClientRect();
        if (r.width>40 && r.height>12) {{ b.click(); return 'posted'; }}
      }}
    }}
    return 'no post btn';
  }})()"
  delay 3
  return opened & " | " & posted
end tell
'''
    try:
        out = run_osascript(script)
        ok = out.strip().endswith("posted") or "| posted" in out
        return {
            "status": "posted_link_card" if ok else "error",
            "method": "chrome_clipboard_fallback",
            "detail": out[:300],
            "cdp_error": cdp.get("detail"),
        }
    except Exception as e:
        return {
            "status": "error",
            "method": "cdp_then_applescript",
            "detail": (cdp.get("detail") or "")[:200],
            "applescript_error": str(e)[:200],
        }


def seed_all() -> int:
    """Seed only films already live so catch-up does not spam forever after first share."""
    n = 0
    data = longs.load_ledger()
    posted = data.setdefault("posted", {})
    rss = longs.rss_public_ids()
    for film in longs.KNOWN_LONGS:
        vid = film["video_id"]
        if vid in {"REXYxuLOBoI", "NbW5G1BpPY0"}:
            # premiere / future — never seed as done early
            continue
        if vid not in rss:
            continue
        key = f"yt:{vid}"
        entry = posted.get(key) or {
            "youtube_id": vid,
            "title": film["title"],
            "youtube_url": film["url"],
        }
        changed = False
        for plat in ("threads", "facebook"):
            if not isinstance(entry.get(plat), dict):
                entry[plat] = {
                    "status": "seeded",
                    "when": datetime.now(longs.LONDON).isoformat(),
                    "note": "optional seed",
                }
                changed = True
        if changed:
            entry["status"] = "seeded"
            entry["marked_at"] = datetime.now(longs.LONDON).isoformat()
            posted[key] = entry
            n += 1
            log(f"seeded {key}")
    longs.save_ledger(data)
    return n


def run_once(*, platform: str | None, dry_run: bool) -> int:
    platforms = [platform] if platform else ["threads", "facebook"]
    posted_n = 0
    for plat in platforms:
        pending = longs.pending_live_longs(platform=plat)
        if not pending:
            log(f"{plat}: nothing pending")
            continue
        film = pending[0]
        log(f"{plat}: {film['video_id']} · {film['title']}")
        if dry_run:
            log(f"dry-run caption:\n{film['_caption']}")
            continue
        if plat == "threads":
            result = post_threads_link(film)
        elif plat == "facebook":
            result = post_facebook_link(film)
        else:
            log(f"skip unsupported platform {plat}")
            continue
        log(f"{plat} result: {result}")
        if result.get("status") in {"posted_link_card", "posted", "ok", "partial"}:
            longs.mark_posted(
                film["video_id"], plat, result, title=film.get("title") or ""
            )
            posted_n += 1
    return posted_n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed-all", action="store_true")
    ap.add_argument("--platform", choices=["threads", "facebook", "instagram"])
    args = ap.parse_args()

    if args.seed_all:
        log(f"seeded {seed_all()}")
        return 0

    if args.list:
        for plat in ("threads", "facebook"):
            pending = longs.pending_live_longs(platform=plat)
            print(f"== {plat} pending {len(pending)}")
            for p in pending:
                print(f"  {p['video_id']}  {p['title']}")
        return 0

    if args.once or args.dry_run:
        ensure_orbit_chrome()
        n = run_once(platform=args.platform, dry_run=args.dry_run)
        log(f"done posted={n}")
        return 0 if n or args.dry_run else 1

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
