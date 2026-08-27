#!/usr/bin/env python3
"""
Post live YouTube Shorts to TikTok Studio automatically.

Usage:
  python3 live_shorts_to_tiktok.py --once          # single pass (launchd / cron)
  python3 live_shorts_to_tiktok.py --watch         # loop every N seconds
  python3 live_shorts_to_tiktok.py --dry-run       # show pending only
  python3 live_shorts_to_tiktok.py --seed-posted   # mark all currently-live as already posted

Requires Chrome CDP on :9222 logged into @orbitwithben
(profile ~/.orbit-chrome-tiktok-dev — auto-started if missing).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Allow `python3 auto/live_shorts_to_tiktok.py` from anywhere
AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from caption import tiktok_caption  # noqa: E402
from discover import iter_index_shorts, pending_live_shorts  # noqa: E402
from ensure_chrome import ensure_chrome  # noqa: E402
from ledger import (  # noqa: E402
    is_posted,
    mark_posted,
    key_for,
    seed_scheduled_covers,
    should_skip_for_backoff,
    record_failure,
    clear_failure,
)
from studio_upload import post_short  # noqa: E402
from upload_block import blocked_result, uploads_paused  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

SETUP = AUTO.parent
AUDIT = SETUP / "audit" / "auto"
LOG = SETUP / "auto_post.log"


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    try:
        with LOG.open("a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def seed_posted(*, all_indexed: bool = False, projects: set[str] | None = None) -> int:
    """Mark shorts as already posted (avoid re-uploads).

    Default: currently-live only.
    --seed-all: every indexed short with a video_id (optional project filter).
    """
    n = 0
    for s in iter_index_shorts():
        if projects and s.get("_project") not in projects:
            continue
        if not all_indexed and not s["_live"]:
            continue
        if all_indexed and not (s.get("video_id") or s.get("file")):
            continue
        if is_posted(s):
            continue
        mark_posted(s, {"status": "seeded"})
        n += 1
        log(f"seeded {s['_ledger_key']} {s.get('title')}")
    return n


def run_once(*, dry_run: bool = False) -> dict:
    if uploads_paused() and not dry_run:
        log("paused: TikTok uploads blocked (account ban) — no post")
        return {"pending": [], "results": [], "skipped": [], **blocked_result()}

    # Keep pre-scheduled batch covered so we never Post-now duplicates.
    seeded = seed_scheduled_covers()
    if seeded:
        log(f"seeded {seeded} scheduled-cover ledger keys")

    pending = pending_live_shorts()
    summary: dict = {
        "pending": [
            {
                "key": s["_ledger_key"],
                "title": s.get("title"),
                "project": s.get("_project"),
                "file": s.get("_abs_file"),
            }
            for s in pending
        ],
        "results": [],
        "skipped": [],
    }
    if dry_run:
        log(f"dry-run pending={len(pending)}")
        return summary
    if not pending:
        log("nothing pending")
        return summary

    chrome = ensure_chrome()
    if not chrome.get("ok"):
        summary["error"] = chrome.get("error") or "chrome_unavailable"
        log(f"chrome fail: {summary['error']}")
        return summary
    if chrome.get("started"):
        log("started Chrome CDP profile")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = browser.contexts[0].new_page()
        page.bring_to_front()
        for s in pending:
            skip = should_skip_for_backoff(s)
            if skip:
                log(f"skip {s['_ledger_key']} · {skip}")
                summary["skipped"].append({"key": s["_ledger_key"], "reason": skip})
                continue
            caption = s.get("_caption") or tiktok_caption(s)
            needle = s.get("_needle") or caption[:40]
            log(f"posting {s['_ledger_key']} · {s.get('title')}")
            result = post_short(
                video_path=Path(s["_abs_file"]),
                caption=caption,
                confirm_needle=needle,
                audit_dir=AUDIT,
                page=page,
            )
            summary["results"].append(
                {"key": s["_ledger_key"], "title": s.get("title"), **result}
            )
            status = result.get("status")
            if status == "ok":
                mark_posted(s, result)
                clear_failure(s)
                log(f"ok {s['_ledger_key']}")
            else:
                reason = status or "unknown"
                record_failure(s, reason)
                log(f"FAIL {s['_ledger_key']} status={status}")
                # Hard-stop the pass on daily check limit — further posts will fail too
                if status == "check_limit":
                    log("abort pass: TikTok content-check daily limit")
                    break
            page.wait_for_timeout(2000)
        try:
            page.close()
        except Exception:
            pass

    out_path = SETUP / "AUTO_LAST_RUN.json"
    out_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--once", action="store_true", help="Single pass then exit")
    ap.add_argument("--watch", action="store_true", help="Loop forever")
    ap.add_argument("--interval", type=int, default=300, help="Watch interval seconds")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--seed-posted",
        action="store_true",
        help="Mark currently-live index shorts as already on TikTok",
    )
    ap.add_argument(
        "--seed-all",
        action="store_true",
        help="Mark all indexed shorts as already on TikTok (use after a manual batch)",
    )
    ap.add_argument(
        "--seed-project",
        action="append",
        default=[],
        help="Limit seeding to project folder name (repeatable)",
    )
    ap.add_argument(
        "--seed-scheduled",
        action="store_true",
        help="Mark pre-scheduled TikTok batch as covered (no Post-now duplicates)",
    )
    ap.add_argument("--list", action="store_true", help="List live/posted status")
    args = ap.parse_args()

    if args.seed_posted or args.seed_all:
        projects = set(args.seed_project) or None
        n = seed_posted(all_indexed=args.seed_all, projects=projects)
        log(f"seeded {n} entries → {SETUP / 'TIKTOK_POSTED.json'}")
        return

    if getattr(args, "seed_scheduled", False):
        n = seed_scheduled_covers()
        log(f"seeded scheduled covers {n} → {SETUP / 'TIKTOK_POSTED.json'}")
        return

    if args.list:
        for s in iter_index_shorts():
            flag = "POSTED" if s["_posted"] else ("LIVE" if s["_live"] else "wait")
            print(
                f"{flag:6} {s['_project']}/{s.get('id')} {s.get('title', '')[:50]}",
                flush=True,
            )
        return

    if uploads_paused() and not args.dry_run:
        log("paused: TikTok uploads blocked (account ban) — no post")
        return

    if args.watch:
        log(f"watch interval={args.interval}s")
        while True:
            try:
                run_once(dry_run=args.dry_run)
            except Exception as e:
                log(f"error {e}")
            time.sleep(max(60, args.interval))
        return

    # default: once
    run_once(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
