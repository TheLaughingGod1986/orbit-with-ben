#!/usr/bin/env python3
"""Record TikTok app-review demo of Orbit Content Ops integration UI."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/demo")
RAW = OUT / "raw"
BASE = "http://127.0.0.1:3000"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    for p in RAW.glob("*"):
        p.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(RAW),
            record_video_size={"width": 1440, "height": 900},
        )
        page = context.new_page()

        # 1. Home
        page.goto(f"{BASE}/", wait_until="networkidle")
        page.wait_for_timeout(2500)

        # 2. Connections — TikTok card / Connect
        page.goto(f"{BASE}/settings/connections", wait_until="networkidle")
        page.wait_for_timeout(2000)
        # Highlight TikTok section if present
        try:
            page.get_by_text("TikTok", exact=True).first.scroll_into_view_if_needed()
            page.wait_for_timeout(1500)
        except Exception:
            pass
        page.wait_for_timeout(2500)

        # 3. Platform settings
        page.goto(f"{BASE}/settings", wait_until="networkidle")
        page.wait_for_timeout(2500)

        # 4. Pipeline / publishing surfaces
        for path in ("/pipeline", "/publishing", "/videos", "/calendar"):
            try:
                page.goto(f"{BASE}{path}", wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(2200)
            except Exception:
                continue

        # 5. Legal pages used for TikTok app URLs
        for path in ("/legal/terms", "/legal/privacy"):
            page.goto(f"{BASE}{path}", wait_until="networkidle")
            page.wait_for_timeout(2000)

        # Back to connections (CTA)
        page.goto(f"{BASE}/settings/connections", wait_until="networkidle")
        page.wait_for_timeout(3000)

        context.close()
        browser.close()

    videos = list(RAW.glob("*.webm"))
    print("raw videos", videos)
    if not videos:
        raise SystemExit("no video recorded")
    print("largest", max(videos, key=lambda p: p.stat().st_size))


if __name__ == "__main__":
    main()
