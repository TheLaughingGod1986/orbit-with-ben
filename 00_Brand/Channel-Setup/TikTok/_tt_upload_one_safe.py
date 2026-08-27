#!/usr/bin/env python3
"""Upload one TikTok Short with a fresh Chrome+CDP each run (dialog-crash workaround).

Usage:
  python3 _tt_upload_one_safe.py aliens-02
  python3 _tt_upload_one_safe.py --all-remaining
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup/TikTok"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".orbit-chrome-tiktok-dev")
CDP = "http://127.0.0.1:9222"
LONDON = ZoneInfo("Europe/London")
RESULT = SETUP / "TIKTOK_V02_PUNCH_REUPLOAD_RESULT.json"
LEDGER = SETUP / "TIKTOK_POSTED.json"

sys.path.insert(0, str(SETUP / "auto"))
from caption import tiktok_caption  # noqa: E402
from upload_block import MESSAGE, uploads_paused  # noqa: E402

# Use the verified uploader (schedule value checks + Studio needle confirm).
# The older _replace_scheduled_v02_cdp.upload_one falsely marked ok on CTA click.
spec = importlib.util.spec_from_file_location("tt", SETUP / "_upload_missing_v02_cdp.py")
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


def safe_dialog(dialog) -> None:
    try:
        dialog.dismiss()
    except Exception:
        try:
            dialog.accept()
        except Exception:
            pass


def kill_chrome() -> None:
    subprocess.run(
        ["pkill", "-f", "user-data-dir=/Users/ben/.orbit-chrome-tiktok-dev"],
        check=False,
        capture_output=True,
    )
    time.sleep(2)


def start_chrome() -> None:
    subprocess.Popen(
        [
            CHROME,
            f"--user-data-dir={PROFILE}",
            "--remote-debugging-port=9222",
            "--no-first-run",
            "--disable-blink-features=AutomationControlled",
            "--window-size=1400,1000",
            "https://www.tiktok.com/tiktokstudio/upload?from=upload",
        ],
        stdout=open("/tmp/tt-chrome-9222.log", "a"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(20):
        try:
            import urllib.request

            with urllib.request.urlopen(f"{CDP}/json/version", timeout=2) as r:
                if r.status == 200:
                    time.sleep(2)
                    return
        except Exception:
            time.sleep(1)
    raise SystemExit("Chrome CDP failed to start")


def build_item(item_id: str) -> dict:
    INDEXES = [
        (
            "aliens",
            ROOT
            / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json",
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
    now = datetime.now(LONDON)
    for ep, ip, root in INDEXES:
        data = json.loads(ip.read_text())
        for s in data["shorts"]:
            iid = f"{ep}-{s['id']}"
            if iid != item_id:
                continue
            when = datetime.fromisoformat(s["schedule_iso"])
            if when.tzinfo is None:
                when = when.replace(tzinfo=LONDON)
            if when <= now:
                when = now + timedelta(hours=1, minutes=5 * int(s["id"]))
            return {
                "id": iid,
                "file": root / s["file"],
                "needle": (s["title"] or "").split("#")[0].strip()[:40],
                "when": when.isoformat(),
                "post_now": False,
                "caption": tiktok_caption(s),
                "yt_id": s.get("video_id"),
            }
    raise SystemExit(f"Unknown id {item_id}")


def remaining_ids() -> list[str]:
    prev = json.loads(RESULT.read_text()) if RESULT.exists() else {"results": []}
    done = {
        r["id"]
        for r in prev.get("results") or []
        if r.get("phase") == "upload" and r.get("ok")
    }
    all_ids = []
    for ep, n in (("aliens", 4), ("blackhole", 6), ("exoplanets", 6)):
        for i in range(1, n + 1):
            iid = f"{ep}-{i:02d}"
            if iid not in done:
                all_ids.append(iid)
    return all_ids


def record(item: dict, row: dict) -> None:
    prev = json.loads(RESULT.read_text()) if RESULT.exists() else {"results": []}
    results = [
        r
        for r in prev.get("results") or []
        if not (r.get("id") == item["id"] and r.get("phase") == "upload")
    ]
    results.append(row)
    ok = sum(1 for r in results if r.get("phase") == "upload" and r.get("ok"))
    RESULT.write_text(
        json.dumps(
            {"ran_at": datetime.now(LONDON).isoformat(), "ok": ok, "results": results},
            indent=2,
        )
        + "\n"
    )
    if row.get("ok"):
        ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"posted": {}}
        ledger.setdefault("posted", {})[f"tt:{item['id']}"] = {
            "file": str(item["file"]),
            "when": item["when"],
            "caption_style": "finalverdict-yellow-white-v02-punch",
            "yt_id": item.get("yt_id"),
            "replaced_at": datetime.now(LONDON).isoformat(),
        }
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")


def upload_id(item_id: str) -> bool:
    item = build_item(item_id)
    print(f"== {item_id} ==", flush=True)
    kill_chrome()
    start_chrome()
    row = {"id": item_id, "phase": "upload"}
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP)
            ctx = browser.contexts[0]
            page = ctx.new_page()
            page.on("dialog", safe_dialog)
            page.bring_to_front()
            up = mod.upload_one(page, item)
            row["upload"] = up
            row["ok"] = bool(up.get("ok"))
            try:
                page.close()
            except Exception:
                pass
    except Exception as e:
        row["ok"] = False
        row["error"] = str(e)[:400]
        print(f"FAIL {e}", flush=True)
    record(item, row)
    print(f"→ ok={row.get('ok')}", flush=True)
    kill_chrome()
    return bool(row.get("ok"))


def main() -> None:
    if uploads_paused():
        raise SystemExit(MESSAGE)
    args = sys.argv[1:]
    if not args:
        raise SystemExit("pass an id or --all-remaining")
    if args[0] == "--all-remaining":
        ids = remaining_ids()
    else:
        ids = args
    print("ids", ids, flush=True)
    ok = 0
    for iid in ids:
        if upload_id(iid):
            ok += 1
        time.sleep(2)
    print(json.dumps({"ok": ok, "n": len(ids)}))


if __name__ == "__main__":
    main()
