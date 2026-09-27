#!/usr/bin/env python3
"""
Post live YouTube Shorts to Threads (@orbitwithben).

Usage:
  python3 live_shorts_to_threads.py --once
  python3 live_shorts_to_threads.py --watch
  python3 live_shorts_to_threads.py --dry-run
  python3 live_shorts_to_threads.py --seed-all --seed-project 001_Will-We-Ever-Meet-Aliens

Prefers CDP on port 9222 (shared IG/TikTok Chrome profile). Graph API when
THREADS_CREDENTIALS has access_token + threads_user_id + public media URL.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

AUTO = Path(__file__).resolve().parent

import importlib.util as _ilu
from pathlib import Path as _P
def _threads_load(name: str):
    auto = _P(__file__).resolve().parent
    key = f"orbit_threads_auto_{name}"
    import sys as _sys
    if key in _sys.modules:
        return _sys.modules[key]
    path = auto / f"{name}.py"
    spec = _ilu.spec_from_file_location(key, path)
    mod = _ilu.module_from_spec(spec)
    _sys.modules[key] = mod
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

load = _threads_load

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
    text = s.get("_caption") or caption.threads_caption(s)
    needle = s.get("_needle") or text[:40]
    path = Path(s["_abs_file"])
    creds = config.load_credentials()
    ready, missing = config.credentials_ready(creds)
    preferred = str(creds.get("preferred_method") or "cdp").lower()

    if preferred == "graph" and ready:
        result = graph_publish.publish_video(
            video_path=path, caption=text, creds=creds
        )
        if result.get("status") == "ok":
            return result

    if preferred == "cdp" or not ready or preferred == "graph":
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
            port=int(creds.get("cdp_port") or 9222),
        )

    return graph_publish.publish_video(video_path=path, caption=text, creds=creds)


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
    preferred = str(creds.get("preferred_method") or "cdp").lower()
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
            log("started Chrome CDP Threads/TikTok profile")
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(
                f"http://127.0.0.1:{chrome.get('port')}"
            )
            page = browser.contexts[0].new_page()
            page.bring_to_front()
            for s in pending:
                log(f"posting {s['_ledger_key']} · {s.get('title')}")
                result = _post_one(s, page=page)
                summary["results"].append(
                    {"key": s["_ledger_key"], "title": s.get("title"), **result}
                )
                if result.get("status") in {"ok", "unconfirmed"}:
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
            if result.get("status") in {"ok", "unconfirmed"}:
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
                    "username": creds.get("threads_username") or creds.get("username"),
                },
                indent=2,
            )
        )
        return

    if args.seed_posted or args.seed_all:
        projects = set(args.seed_project) or None
        n = seed_posted(all_indexed=args.seed_all, projects=projects)
        log(f"seeded {n} entries → {SETUP / 'THREADS_POSTED.json'}")
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
