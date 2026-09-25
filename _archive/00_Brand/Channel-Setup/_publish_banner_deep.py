#!/usr/bin/env python3
"""Publish Orbit Deep Universe banner (v05) to YouTube Studio — banner only."""
from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup")
BANNER = SETUP / "banner_2560x1440.png"
AUDIT = SETUP / "audit"
CID = "UC_esArsDKd3GJvOkeO0DUog"
RESULT = SETUP / "BANNER_DEEP_PUBLISH.json"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"banner_deep_{name}.png"), full_page=False)


def dismiss(page) -> None:
    for label in ("Continue", "Got it", "Dismiss", "Not now", "OK", "Close", "No thanks"):
        try:
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=1500)
                page.wait_for_timeout(600)
        except Exception:
            pass


def main() -> None:
    result = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "channel_id": CID,
        "banner": str(BANNER),
        "bytes": BANNER.stat().st_size,
        "slogan": "BIG QUESTIONS. DEEP UNIVERSE.",
    }
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            # Ensure Orbit channel context
            page.goto(
                f"https://studio.youtube.com/channel/{CID}/editing/profile",
                wait_until="domcontentloaded",
                timeout=90000,
            )
            page.wait_for_timeout(4500)
            dismiss(page)
            shot(page, "01_profile")

            # Switch channel if account switcher shows wrong one
            title = page.title()
            body = page.locator("body").inner_text()[:500]
            result["page_title"] = title
            if "Orbit" not in title and "Orbit" not in body:
                # try switcher
                try:
                    page.locator("#avatar-btn, button#avatar-btn, img#img").first.click(timeout=3000)
                    page.wait_for_timeout(1000)
                    page.get_by_text("Orbit with Ben", exact=False).first.click(timeout=5000)
                    page.wait_for_timeout(4000)
                    page.goto(
                        f"https://studio.youtube.com/channel/{CID}/editing/profile",
                        wait_until="domcontentloaded",
                        timeout=90000,
                    )
                    page.wait_for_timeout(3500)
                except Exception as e:
                    result["switch_note"] = str(e)

            dismiss(page)
            shot(page, "02_ready")

            banner_upload = page.locator(
                "xpath=//*[contains(normalize-space(.),'Banner image')]/following::input[@type='file'][1]"
            )
            if banner_upload.count():
                banner_upload.first.set_input_files(str(BANNER))
            else:
                inputs = page.locator('input[type="file"]')
                if not inputs.count():
                    raise RuntimeError("no file inputs on profile page")
                inputs.first.set_input_files(str(BANNER))

            page.wait_for_timeout(4000)
            dismiss(page)
            shot(page, "03_after_upload")

            # Crop / confirm dialogs
            for label in ("Done", "Apply", "Confirm", "Save", "Crop"):
                try:
                    b = page.get_by_role("button", name=label, exact=True)
                    if b.count() and b.first.is_visible() and b.first.is_enabled():
                        b.first.click(force=True)
                        page.wait_for_timeout(1500)
                        result["crop_confirm"] = label
                except Exception:
                    pass
            dismiss(page)
            shot(page, "04_after_crop")

            # Publish
            pub = page.get_by_role("button", name="Publish", exact=True)
            if pub.count() and pub.first.is_enabled():
                pub.first.click(force=True)
                page.wait_for_timeout(5000)
                result["published"] = True
            else:
                # Sometimes it's "Publish" disabled until change detected
                result["published"] = False
                result["publish_enabled"] = bool(pub.count() and pub.first.is_enabled())
            dismiss(page)
            shot(page, "05_after_publish")

            # Verify public channel banner
            page.goto("https://www.youtube.com/@OrbitWithBen", wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(4000)
            dismiss(page)
            shot(page, "06_public")
            banners = page.evaluate(
                """() => [...document.querySelectorAll('img')].filter(i =>
                  /banner|channel|googleusercontent/i.test(i.src) && i.width > 400
                ).slice(0,6).map(i => ({src:i.src, w:i.width, h:i.height}))"""
            )
            result["banner_imgs"] = banners
            result["status"] = "ok" if result.get("published") else "upload_maybe_unpublished"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            try:
                shot(page, "err")
            except Exception:
                pass
        finally:
            RESULT.write_text(json.dumps(result, indent=2))
            ctx.close()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
