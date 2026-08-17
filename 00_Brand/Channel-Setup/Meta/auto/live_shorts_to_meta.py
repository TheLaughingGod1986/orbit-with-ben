#!/usr/bin/env python3
"""
Post live YouTube Shorts to Instagram Reels + Facebook Page Reels.

Usage:
  python3 live_shorts_to_meta.py --once
  python3 live_shorts_to_meta.py --watch
  python3 live_shorts_to_meta.py --dry-run
  python3 live_shorts_to_meta.py --seed-all --seed-project 001_Will-We-Ever-Meet-Aliens

Prefers Graph API (META_CREDENTIALS.json). Falls back to Meta Business Suite CDP
on port 9223 (profile ~/.orbit-chrome-meta-dev).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from _sib import load  # noqa: E402

caption = load("caption")
config = load("config")
discover = load("discover")
ensure_chrome = load("ensure_chrome")
graph_publish = load("graph_publish")
ledger = load("ledger")
studio_upload = load("studio_upload")

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
    n = 0
    for s in discover.iter_index_shorts():
        if projects and s.get("_project") not in projects:
            continue
        if not all_indexed and not s["_live"]:
            continue
        if all_indexed and not (s.get("video_id") or s.get("file")):
            continue
        if ledger.is_posted(s):
            continue
        ledger.mark_posted(s, {"status": "seeded"})
        n += 1
        log(f"seeded {s['_ledger_key']} {s.get('title')}")
    return n


def _post_one(s: dict, *, page=None) -> dict:
    text = s.get("_caption") or caption.meta_caption(s)
    needle = s.get("_needle") or text[:40]
    path = Path(s["_abs_file"])
    creds = config.load_credentials()
    ready, missing = config.credentials_ready(creds)
    preferred = str(creds.get("preferred_method") or "graph").lower()

    if preferred == "graph" and ready:
        return graph_publish.publish_both(
            video_path=path, caption=text, creds=creds
        )

    if preferred == "cdp" or not ready:
        if page is None:
            chrome = ensure_chrome.ensure_chrome()
            if not chrome.get("ok"):
                return {
                    "status": "chrome_unavailable",
                    "error": chrome.get("error"),
                    "graph_missing": missing,
                }
        return studio_upload.post_short(
            video_path=path,
            caption=text,
            confirm_needle=needle,
            audit_dir=AUDIT,
            page=page,
            port=int(creds.get("cdp_port") or 9223),
        )

    return graph_publish.publish_both(video_path=path, caption=text, creds=creds)


def run_once(*, dry_run: bool = False) -> dict:
    pending = discover.pending_live_shorts()
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
    }
    if dry_run:
        log(f"dry-run pending={len(pending)}")
        return summary
    if not pending:
        log("nothing pending")
        return summary

    creds = config.load_credentials()
    ready, _missing = config.credentials_ready(creds)
    preferred = str(creds.get("preferred_method") or "graph").lower()
    use_cdp = preferred == "cdp" or not ready

    if use_cdp:
        from playwright.sync_api import sync_playwright

        chrome = ensure_chrome.ensure_chrome()
        if not chrome.get("ok"):
            summary["error"] = chrome.get("error") or "chrome_unavailable"
            summary["graph_missing"] = _missing
            log(f"chrome fail: {summary['error']} graph_missing={_missing}")
            return summary
        if chrome.get("started"):
            log("started Chrome CDP Meta profile")
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(
                f"http://127.0.0.1:{chrome.get('port')}"
            )
            ctx = browser.contexts[0]

            def _leave(d):
                try:
                    if getattr(d, "type", "") == "beforeunload":
                        d.accept()
                    else:
                        d.dismiss()
                except Exception:
                    try:
                        d.accept()
                    except Exception:
                        pass

            ctx.on("dialog", _leave)
            # Close leftover Reels composer tabs from crashed/retried runs.
            for extra in list(ctx.pages):
                try:
                    extra.on("dialog", _leave)
                    if "reels_composer" in (extra.url or ""):
                        extra.close()
                except Exception:
                    pass
            page = ctx.new_page()
            page.on("dialog", _leave)
            page.bring_to_front()
            for s in pending:
                log(f"posting {s['_ledger_key']} · {s.get('title')}")
                result = _post_one(s, page=page)
                summary["results"].append(
                    {"key": s["_ledger_key"], "title": s.get("title"), **result}
                )
                if result.get("status") in {"ok", "partial"}:
                    ledger.mark_posted(s, result)
                    log(f"ok {s['_ledger_key']} status={result.get('status')}")
                else:
                    log(f"FAIL {s['_ledger_key']} status={result.get('status')}")
                page.wait_for_timeout(2000)
            try:
                page.close()
            except Exception:
                pass
    else:
        for s in pending:
            log(f"posting {s['_ledger_key']} · {s.get('title')} via graph")
            result = _post_one(s)
            summary["results"].append(
                {"key": s["_ledger_key"], "title": s.get("title"), **result}
            )
            if result.get("status") in {"ok", "partial"}:
                ledger.mark_posted(s, result)
                log(f"ok {s['_ledger_key']} status={result.get('status')}")
            else:
                log(f"FAIL {s['_ledger_key']} status={result.get('status')}")

    out_path = SETUP / "AUTO_LAST_RUN.json"
    out_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed-posted", action="store_true")
    ap.add_argument("--seed-all", action="store_true")
    ap.add_argument("--seed-project", action="append", default=[])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check-creds", action="store_true")
    args = ap.parse_args()

    if args.check_creds:
        creds = config.load_credentials()
        ready, missing = config.credentials_ready(creds)
        print(
            json.dumps(
                {
                    "ready": ready,
                    "missing": missing,
                    "method": creds.get("preferred_method"),
                },
                indent=2,
            )
        )
        return

    if args.seed_posted or args.seed_all:
        projects = set(args.seed_project) or None
        n = seed_posted(all_indexed=args.seed_all, projects=projects)
        log(f"seeded {n} entries → {SETUP / 'META_POSTED.json'}")
        return

    if args.list:
        for s in discover.iter_index_shorts():
            flag = "POSTED" if s["_posted"] else ("LIVE" if s["_live"] else "wait")
            print(
                f"{flag:6} {s['_project']}/{s.get('id')} {s.get('title', '')[:50]}",
                flush=True,
            )
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

    run_once(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
