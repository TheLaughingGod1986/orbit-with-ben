#!/usr/bin/env python3
"""Part 03 v03 variety plates — mint the ids in part-03_flow_prompts_v03_variety.json that are missing.

Fixes the v01 batch race: after a submit we wait >= MIN_RENDER_S before trusting a "fresh" thumb, and
after each capture we wait for the gallery thumb keys to stabilise before starting the next stem.
Works inside the Flow project given by PROJECT_URL (opens a tab if none is on it).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_part03_flow_world_v01 import (  # noqa: E402
    OUT,
    WORLD_PREFIX,
    capture_by_click,
    credits_blocked,
    ensure_x1,
    set_prompt,
    start_generation,
    thumb_keys,
    thumb_rows,
)

CDP = "http://127.0.0.1:9222"
PROJECT_URL = "https://flow.google.com/project/59f2b559-4391-48da-a01b-f75a2fd2ec95"
HERE = Path(__file__).resolve().parent
PROMPTS = HERE / "parts/part-03_flow_prompts_v03_variety.json"
MIN_RENDER_S = 45
MAX_WAIT_S = 300


def key_of(src: str) -> str:
    m = re.search(r"/asb/([^?]+)", src) or re.search(r"/image/([0-9a-f-]{36})", src)
    return m.group(1) if m else src[-48:]


def stable_keys(page, settle_s: float = 2.0, tries: int = 8) -> set[str]:
    prev = thumb_keys(page)
    for _ in range(tries):
        page.wait_for_timeout(int(settle_s * 1000))
        now = thumb_keys(page)
        if now == prev:
            return now
        prev = now
    return prev


def main() -> None:
    rows = json.loads(PROMPTS.read_text())
    todo = [r for r in rows if not list(OUT.glob(f"{r['id']}_*.mp4"))]
    print(f"todo={[r['id'] for r in todo]}", flush=True)
    if not todo:
        return
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if "59f2b559" in (pg.url or "")), None)
        if page is None:
            page = ctx.new_page()
            page.goto(PROJECT_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(7000)
        page.bring_to_front()
        page.on("dialog", lambda d: d.dismiss())
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        ensure_x1(page)

        report = []
        for row in todo:
            stem = row["id"]
            if credits_blocked(page):
                print("BLOCKED credits", flush=True)
                report.append({"id": stem, "status": "blocked_credits"})
                break
            print(f"\n=== {stem} (bed {row.get('bed')}) ===", flush=True)
            before = stable_keys(page)
            set_prompt(page, WORLD_PREFIX + row["prompt"])
            try:
                start_generation(page)
            except Exception as e:  # noqa: BLE001
                print(f"  FAIL start: {e}", flush=True)
                report.append({"id": stem, "status": "fail", "error": str(e)})
                if "insufficient" in str(e):
                    break
                continue
            t0 = time.time()
            print("  submitted", flush=True)
            page.wait_for_timeout(MIN_RENDER_S * 1000)

            new_row = None
            while time.time() - t0 < MAX_WAIT_S:
                fresh = [k for k in thumb_keys(page) if k not in before]
                if fresh:
                    page.wait_for_timeout(4000)
                    for t in sorted(thumb_rows(page), key=lambda r: r["y"]):
                        if key_of(t["src"]) in fresh:
                            new_row = t
                            break
                    if new_row:
                        break
                if credits_blocked(page):
                    print("  credits died", flush=True)
                    break
                page.wait_for_timeout(3000)
                print(f"  waiting… {int(time.time() - t0)}s", flush=True)

            if not new_row:
                print("  no render seen", flush=True)
                report.append({"id": stem, "status": "no_render"})
                continue
            short = key_of(new_row["src"])[:8]
            dest = OUT / f"{stem}_{short}.mp4"
            ok = capture_by_click(page, new_row, dest)
            print(f"  capture {short} -> {ok}", flush=True)
            report.append({"id": stem, "status": "ok" if ok else "capture_fail", "file": dest.name})
            page.keyboard.press("Escape")
            stable_keys(page)

    (OUT / "_gen_report_v03_variety.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
