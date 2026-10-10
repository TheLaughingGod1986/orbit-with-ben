#!/usr/bin/env python3
"""J0099 item 1: set the nine crop-safe Short covers in desktop Studio (Orbit browser, CDP 9223).

Covers come from 00_Brand/Channel-Setup/tools/build_crop_safe_short_covers_j0099.py (J0099_WORK/after).
Image-only file inputs: never Replace / video file, never visibility or dates.

  ONLY_IDS=xQlV9G9lqLI python3 scripts/apply_j0099_short_covers.py
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import apply_yellow_white_v04_thumbs as v04

v04.CDP = "http://127.0.0.1:9223"
WORK = Path(os.environ.get("J0099_WORK", "/tmp/j0099"))
v04.SHOTS = WORK / "apply_shots"
OUT = WORK / "apply_result.json"

IDS = ["xQlV9G9lqLI", "e-7hzJv4c80", "CtllH6VOhEI", "P9Jiw-MwUEU", "U5Baf_CjhKc",
       "17zpT_u7XsY", "QRi6Dxq0hz0", "ZnsJTCcrTlA", "tEOHYQbcgOw"]


def main() -> int:
    v04.SHOTS.mkdir(parents=True, exist_ok=True)
    only = {x.strip() for x in os.environ.get("ONLY_IDS", "").split(",") if x.strip()}
    jobs = [{"id": i, "cover": WORK / "after" / f"cover_{i}.jpg", "related": ""}
            for i in IDS if not only or i in only]
    prior = json.loads(OUT.read_text()) if OUT.exists() else {"studio_results": []}
    results = {r["id"]: r for r in prior["studio_results"]}
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = p.chromium.connect_over_cdp(v04.CDP).contexts[0]
        for n, s in enumerate(jobs, start=1):
            row = v04.apply_one(ctx, s, n)
            row["at"] = datetime.now(timezone.utc).isoformat()
            results[s["id"]] = row
            print(json.dumps({k: row.get(k) for k in ("id", "studio_thumb_uploaded", "saved", "error")}), flush=True)
            if row.get("error") == "BLOCKED_NEED_BEN_LOGIN":
                break
            time.sleep(0.4)
    OUT.write_text(json.dumps({"task": "j0099_short_covers", "studio_results": list(results.values())}, indent=2))
    ran = [results[s["id"]] for s in jobs if s["id"] in results]
    return 0 if ran and all(r.get("studio_thumb_uploaded") and r.get("saved") for r in ran) else 1


if __name__ == "__main__":
    raise SystemExit(main())
