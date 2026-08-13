#!/usr/bin/env python3
"""Re-upload Giant Eye v04 cover + scroll Studio Shorts list to Aug 13–19 greys."""
from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

AUD = Path(__file__).resolve().parent
SHOTS = AUD / "studio_after"
COVER = AUD / "covers/OlwENQcY-jg_cover_v04.jpg"


def dismiss(page) -> None:
    for name in ("Done", "Got it", "Close", "Not now", "Dismiss", "Skip"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=400)
            page.wait_for_timeout(100)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True).first
        if b.count() and b.is_enabled():
            b.click(force=True, timeout=2500)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def main() -> None:
    assert COVER.exists(), COVER
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        page = ctx.new_page()

        vid = "OlwENQcY-jg"
        page.goto(
            f"https://studio.youtube.com/video/{vid}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)
        page.locator("ytcp-thumbnail-uploader input#file-loader, input#file-loader").first.set_input_files(
            str(COVER)
        )
        page.wait_for_timeout(5000)
        saved = save_edit(page)
        page.wait_for_timeout(2000)
        page.goto(
            f"https://studio.youtube.com/video/{vid}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        dismiss(page)
        page.screenshot(path=str(SHOTS / "OlwENQcY-jg_after_v04.png"), full_page=False)

        # Shorts content list — search for Three Suns
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        dismiss(page)
        # try search box
        found = False
        for sel in ('input[placeholder*="Search"]', "#search-input input", "ytcp-text-menu", 'input[aria-label*="Search"]'):
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(timeout=2000)
                    loc.fill("Three Suns")
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(4000)
                    found = True
                    break
            except Exception:
                pass
        page.screenshot(path=str(SHOTS / "shorts_list_three_suns_search.png"), full_page=False)

        # Also open filter-free list and scroll looking for titles
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)
        for i in range(18):
            page.mouse.wheel(0, 1800)
            page.wait_for_timeout(400)
            text = page.locator("body").inner_text()
            if "Three Suns" in text or "Haven't We Found Aliens" in text or "Giant Eye" in text:
                page.screenshot(path=str(SHOTS / f"shorts_list_scroll_{i}.png"), full_page=False)
                if "Three Suns" in text and "Giant Eye" in text:
                    break

        page.screenshot(path=str(SHOTS / "shorts_list_final.png"), full_page=False)
        page.close()

    (AUD / "STUDIO_EYE_V04.json").write_text(
        json.dumps(
            {
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "id": "OlwENQcY-jg",
                "cover": str(COVER),
                "saved": saved,
                "search_attempted": found,
            },
            indent=2,
        )
        + "\n"
    )
    print("OK saved=", saved, "search=", found)


if __name__ == "__main__":
    main()
