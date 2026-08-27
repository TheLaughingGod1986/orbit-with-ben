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


def post_facebook_link(film: dict) -> dict:
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
    out = run_osascript(script)
    ok = out.strip().endswith("posted") or "| posted" in out
    return {
        "status": "posted_link_card" if ok else "error",
        "method": "chrome_clipboard",
        "detail": out[:300],
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
