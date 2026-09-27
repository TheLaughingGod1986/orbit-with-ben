#!/usr/bin/env python3
"""Upload punch-first v02 Shorts to TikTok one-at-a-time with CDP reconnect.

Avoids long-lived page handles (TikTok Studio has been closing mid-batch).
"""
from __future__ import annotations

import importlib.util
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
SKIP_DONE = True

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
    q = []
    for ep, index_path, root in INDEXES:
        data = json.loads(index_path.read_text())
        for s in data.get("shorts") or []:
            fpath = root / (s.get("file") or "")
            if not fpath.exists():
                continue
            when_s = s.get("schedule_iso")
            when = datetime.fromisoformat(when_s) if when_s else now + timedelta(hours=2)
            if when.tzinfo is None:
                when = when.replace(tzinfo=LONDON)
            post_now = when <= now + timedelta(minutes=10)
            if when <= now:
                when = now + timedelta(hours=1, minutes=5 * int(s.get("id") or 1))
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


def upload_one_isolated(item: dict) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            page.bring_to_front()
            # Skip delete — prior delete_matching was closing the CDP browser mid-batch
            up = mod.upload_one(page, item)
            return {"ok": bool(up.get("ok")), "upload": up}
        finally:
            try:
                page.close()
            except Exception:
                pass


def main() -> None:
    only = set(sys.argv[1:])
    queue = build_queue()
    if only:
        queue = [i for i in queue if i["id"] in only or i["id"].split("-")[0] in only]
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"posted": {}}
    posted = ledger.setdefault("posted", {})
    prev = json.loads(RESULT.read_text()) if RESULT.exists() else {"results": []}
    done_ids = {
        r["id"]
        for r in prev.get("results") or []
        if r.get("phase") == "upload" and r.get("ok")
    }
    results = list(prev.get("results") or [])
    print(f"queue={len(queue)} already_ok={sorted(done_ids)}", flush=True)

    ok = len(done_ids)
    for item in queue:
        if SKIP_DONE and item["id"] in done_ids:
            print(f"skip {item['id']} (already ok)", flush=True)
            continue
        print(f"upload {item['id']}…", flush=True)
        row = {"id": item["id"], "phase": "upload"}
        try:
            out = upload_one_isolated(item)
            row.update(out)
            if out.get("ok"):
                ok += 1
                posted[f"tt:{item['id']}"] = {
                    "file": str(item["file"]),
                    "when": item["when"],
                    "caption_style": "finalverdict-yellow-white-v02-punch",
                    "yt_id": item.get("yt_id"),
                    "caption": item["caption"][:180],
                    "replaced_at": datetime.now(LONDON).isoformat(),
                }
                LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
            print(f"  → ok={row.get('ok')}", flush=True)
        except Exception as e:
            row["ok"] = False
            row["error"] = str(e)[:400]
            print(f"  → FAIL {e}", flush=True)
        # replace prior result for this id
        results = [r for r in results if not (r.get("id") == item["id"] and r.get("phase") == "upload")]
        results.append(row)
        summary = {
            "ran_at": datetime.now(LONDON).isoformat(),
            "ok": ok,
            "results": results,
        }
        RESULT.write_text(json.dumps(summary, indent=2) + "\n")

    print(json.dumps({"ok": ok, "n": len(queue)}, indent=2))


if __name__ == "__main__":
    main()
