#!/usr/bin/env python3
"""Harvest every rendered video from the Part 03 v02 Flow project into a staging dir.

The batch gen captured several renders under the wrong stem (fresh-thumb race after a
successful click), so this pulls all gallery items by thumb key for manual identification.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_part03_flow_world_v01 import capture_by_click, thumb_rows  # noqa: E402

CDP = "http://127.0.0.1:9222"
PROJECT_URL = "https://flow.google.com/project/59f2b559-4391-48da-a01b-f75a2fd2ec95"
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
STAGE = PROJ / "04_Generated-Clips/part03/_harvest_v02_2026-09-10"
KNOWN_DIRS = [
    PROJ / "04_Generated-Clips/part03/flow_world_v01",
    PROJ / "04_Generated-Clips/part03/_rejected_tidal_plane_2026-09-10",
]


def key_of(src: str) -> str:
    m = re.search(r"/asb/([^?]+)", src) or re.search(r"/image/([0-9a-f-]{36})", src)
    return (m.group(1) if m else src[-48:])[:8]


def main() -> None:
    STAGE.mkdir(parents=True, exist_ok=True)
    known_md5 = {
        hashlib.md5(f.read_bytes()).hexdigest(): f.name
        for d in KNOWN_DIRS
        for f in d.glob("*.mp4")
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (pg for pg in ctx.pages if "flow.google.com/project/59f2b559" in (pg.url or "")),
            None,
        ) or ctx.new_page()
        if "59f2b559" not in page.url:
            page.goto(PROJECT_URL, wait_until="domcontentloaded")
        page.bring_to_front()
        page.wait_for_timeout(6000)
        page.keyboard.press("Escape")

        # scroll the whole gallery so every thumb has a src
        for _ in range(8):
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(300)
        for _ in range(10):
            page.mouse.wheel(0, -800)
            page.wait_for_timeout(200)

        rows = thumb_rows(page)
        seen_keys: set[str] = set()
        report = []
        print(f"gallery thumbs={len(rows)}", flush=True)
        for t in sorted(rows, key=lambda r: (r["y"], r["x"])):
            k = key_of(t["src"])
            if k in seen_keys:
                continue
            seen_keys.add(k)
            dest = STAGE / f"h_{k}.mp4"
            if dest.exists():
                print(f"have {k}", flush=True)
                continue
            ok = capture_by_click(page, t, dest, timeout_s=45)
            if not ok or not dest.exists():
                print(f"FAIL {k}", flush=True)
                report.append({"key": k, "status": "fail"})
                continue
            h = hashlib.md5(dest.read_bytes()).hexdigest()
            dup = known_md5.get(h)
            if dup:
                dest.unlink()
                print(f"dup  {k} == {dup}", flush=True)
                report.append({"key": k, "status": "dup", "of": dup})
                continue
            known_md5[h] = dest.name
            print(f"new  {k} {dest.stat().st_size}", flush=True)
            report.append({"key": k, "status": "new", "file": dest.name})
            page.wait_for_timeout(800)

    (STAGE / "_harvest_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
