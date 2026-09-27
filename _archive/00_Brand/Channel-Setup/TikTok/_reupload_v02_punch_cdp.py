#!/usr/bin/env python3
"""Re-upload punch-first v02 Shorts to TikTok + delete older dupes.

Reads SHORTS_UPLOAD_INDEX.json files, builds existential captions via caption.py,
schedules at existing schedule_iso (or +1h from now if past). Uses CDP :9222.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup/TikTok"
sys.path.insert(0, str(SETUP / "auto"))
from caption import tiktok_caption  # noqa: E402

# Reuse upload helpers from replace script
sys.path.insert(0, str(SETUP))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "tt_replace", SETUP / "_replace_scheduled_v02_cdp.py"
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

LONDON = ZoneInfo("Europe/London")
RESULT = SETUP / "TIKTOK_V02_PUNCH_REUPLOAD_RESULT.json"
LEDGER = SETUP / "TIKTOK_POSTED.json"
CDP = "http://127.0.0.1:9222"

INDEXES = [
    (
        "aliens",
        ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json",
        ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens",
    ),
    (
        "blackhole",
        ROOT
        / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/SHORTS_UPLOAD_INDEX.json",
        ROOT / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole",
    ),
    (
        "exoplanets",
        ROOT
        / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/SHORTS_UPLOAD_INDEX.json",
        ROOT / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds",
    ),
]


def build_queue() -> list[dict]:
    now = datetime.now(LONDON)
    q: list[dict] = []
    for ep, index_path, root in INDEXES:
        data = json.loads(index_path.read_text())
        for s in data.get("shorts") or []:
            rel = s.get("file") or ""
            fpath = root / rel
            if not fpath.exists():
                print(f"missing {fpath}", flush=True)
                continue
            when_s = s.get("schedule_iso")
            when = datetime.fromisoformat(when_s) if when_s else now + timedelta(hours=2)
            if when.tzinfo is None:
                when = when.replace(tzinfo=LONDON)
            post_now = when <= now + timedelta(minutes=10)
            if when <= now:
                when = now + timedelta(hours=1, minutes=5)
                post_now = False
            title = (s.get("title") or "").strip()
            needle = title.split("#")[0].strip()[:40] or title[:40]
            q.append(
                {
                    "id": f"{ep}-{s.get('id')}",
                    "file": fpath,
                    "needle": needle,
                    "when": when.isoformat(),
                    "post_now": post_now,
                    "caption": tiktok_caption(s),
                    "yt_id": s.get("video_id"),
                }
            )
    return q


def main() -> None:
    queue = build_queue()
    print(f"queue={len(queue)}", flush=True)
    results = []
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"posted": {}}
    posted = ledger.setdefault("posted", {})

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]

        def fresh_page():
            # Close stray pages that are not TikTok studio to reduce crash surface
            page = ctx.new_page()
            page.goto(mod.CONTENT, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(3000)
            page.bring_to_front()
            return page

        page = fresh_page()

        # Optional light dupe delete — recreate page if browser closes mid-scan
        for item in queue:
            print(f"delete-scan {item['id']} · {item['needle']}", flush=True)
            try:
                if page.is_closed():
                    page = fresh_page()
                d = mod.delete_matching(page, item["needle"])
            except Exception as e:
                d = {"error": str(e)[:200]}
                try:
                    page = fresh_page()
                except Exception:
                    pass
            results.append({"id": item["id"], "phase": "delete", "delete": d})

        for item in queue:
            print(f"upload {item['id']}…", flush=True)
            row: dict = {"id": item["id"], "phase": "upload"}
            try:
                if page.is_closed():
                    page = fresh_page()
                up = mod.upload_one(page, item)
                row["upload"] = up
                row["ok"] = bool(up.get("ok"))
                posted[f"tt:{item['id']}"] = {
                    "file": str(item["file"]),
                    "when": item["when"],
                    "mode": "post_now" if item.get("post_now") else "scheduled",
                    "caption_style": "finalverdict-yellow-white-v02-punch",
                    "yt_id": item.get("yt_id"),
                    "caption": item["caption"][:180],
                    "replaced_at": datetime.now(LONDON).isoformat(),
                }
                print(f"  → ok={row['ok']}", flush=True)
            except Exception as e:
                row["ok"] = False
                row["error"] = str(e)[:400]
                print(f"  → FAIL {e}", flush=True)
                try:
                    page = fresh_page()
                except Exception as e2:
                    row["reconnect"] = str(e2)[:160]
            results.append(row)

        try:
            if not page.is_closed():
                page.close()
        except Exception:
            pass

    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
    summary = {
        "ran_at": datetime.now(LONDON).isoformat(),
        "ok": sum(1 for r in results if r.get("phase") == "upload" and r.get("ok")),
        "results": results,
    }
    RESULT.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"ok": summary["ok"], "n": len(queue)}, indent=2))


if __name__ == "__main__":
    main()
