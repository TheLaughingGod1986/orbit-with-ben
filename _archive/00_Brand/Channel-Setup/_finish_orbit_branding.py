#!/usr/bin/env python3
"""Finish Orbit channel branding on Studio Customisation > Profile."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup")
AVATAR = SETUP / "avatar_800x800.png"
BANNER = SETUP / "banner_2560x1440.png"
DESC = (SETUP / "channel_description.txt").read_text().strip()
AUDIT = SETUP / "audit"
CID = "UC_esArsDKd3GJvOkeO0DUog"
RESULT = SETUP / "BRAND_RESULT.json"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"f_{name}.png"), full_page=False)


def dismiss_modals(page) -> None:
    for label in ("Continue", "Got it", "Dismiss", "Not now", "OK", "Close"):
        try:
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=1500)
                page.wait_for_timeout(800)
        except Exception:
            pass
    # Error dialogs
    try:
        if page.get_by_text("Error:", exact=False).count():
            page.get_by_role("button", name="Cancel", exact=True).first.click(force=True)
            page.wait_for_timeout(600)
    except Exception:
        pass


def publish(page, result: dict, key: str) -> None:
    btn = page.get_by_role("button", name="Publish", exact=True)
    if btn.count() and btn.first.is_enabled():
        btn.first.click(force=True)
        page.wait_for_timeout(4000)
        result[key] = True
        dismiss_modals(page)
    else:
        result[key] = False


def main() -> None:
    result = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "channel_id": CID,
        "avatar_bytes": AVATAR.stat().st_size,
        "banner_bytes": BANNER.stat().st_size,
    }
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(
                f"https://studio.youtube.com/channel/{CID}/editing/profile",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(4000)
            dismiss_modals(page)
            page.wait_for_timeout(1000)
            dismiss_modals(page)
            shot(page, "01_profile")

            # ---- Banner upload via labeled Upload near "Banner image" ----
            try:
                # Prefer set_input_files on the first file input in Banner section
                # Structure: Banner image section then Picture section
                banner_upload = page.locator(
                    "xpath=//*[contains(normalize-space(.),'Banner image')]/following::input[@type='file'][1]"
                )
                if banner_upload.count():
                    banner_upload.first.set_input_files(str(BANNER))
                else:
                    # Click Upload under Banner image
                    with page.expect_file_chooser(timeout=5000) as fc:
                        page.locator(
                            "xpath=//*[contains(normalize-space(.),'Banner image')]/following::*[normalize-space()='Upload'][1]"
                        ).click(force=True)
                    fc.value.set_files(str(BANNER))
                page.wait_for_timeout(3500)
                dismiss_modals(page)
                for label in ("Done", "Apply", "Confirm", "Save"):
                    b = page.get_by_role("button", name=label, exact=True)
                    if b.count() and b.first.is_visible() and b.first.is_enabled():
                        b.first.click(force=True)
                        page.wait_for_timeout(1200)
                result["banner_uploaded"] = True
                shot(page, "02_banner")
            except Exception as e:
                result["banner_error"] = str(e)
                shot(page, "02_banner_err")

            # ---- Picture / avatar ----
            try:
                pic_upload = page.locator(
                    "xpath=//*[contains(normalize-space(.),'Picture')]/following::input[@type='file'][1]"
                )
                # More specific: "Your profile picture" nearby
                alt = page.locator(
                    "xpath=//*[contains(.,'profile picture')]/following::input[@type='file'][1]"
                )
                target = alt if alt.count() else pic_upload
                if target.count():
                    # Avoid using banner's input — pick last file input if needed
                    inputs = page.locator('input[type="file"]')
                    # Heuristic: banner is usually input 0, picture input 1
                    if inputs.count() >= 2:
                        inputs.nth(1).set_input_files(str(AVATAR))
                    else:
                        target.first.set_input_files(str(AVATAR))
                else:
                    with page.expect_file_chooser(timeout=5000) as fc:
                        page.locator(
                            "xpath=//*[contains(.,'profile picture')]/following::*[normalize-space()='Upload'][1]"
                        ).click(force=True)
                    fc.value.set_files(str(AVATAR))
                page.wait_for_timeout(3000)
                dismiss_modals(page)
                for label in ("Done", "Apply", "Confirm", "Save"):
                    b = page.get_by_role("button", name=label, exact=True)
                    if b.count() and b.first.is_visible() and b.first.is_enabled():
                        b.first.click(force=True)
                        page.wait_for_timeout(1200)
                result["avatar_uploaded"] = True
                shot(page, "03_avatar")
            except Exception as e:
                result["avatar_error"] = str(e)
                shot(page, "03_avatar_err")

            # ---- Name → try Orbit ----
            try:
                page.evaluate("window.scrollTo(0, 400)")
                page.wait_for_timeout(400)
                name = page.locator('#textbox[aria-label*="Name" i], input[aria-label*="Name" i]')
                if not name.count():
                    # labeled Name section textbox
                    name = page.locator(
                        "xpath=//*[normalize-space()='Name']/following::div[@id='textbox' or self::input][1]"
                    )
                if name.count():
                    name.first.click(force=True)
                    page.keyboard.press("Meta+A")
                    page.keyboard.insert_text("Orbit")
                    page.wait_for_timeout(600)
                    result["name_set_to_orbit"] = True
                shot(page, "04_name")
            except Exception as e:
                result["name_error"] = str(e)

            # ---- Description ----
            try:
                page.evaluate("window.scrollTo(0, 1200)")
                page.wait_for_timeout(500)
                desc = page.locator('#textbox[aria-label*="Description" i]')
                if not desc.count():
                    desc = page.locator(
                        "xpath=//*[normalize-space()='Description']/following::div[@id='textbox'][1]"
                    )
                if not desc.count():
                    # any textbox after description heading
                    boxes = page.locator("#textbox")
                    result["textbox_count"] = boxes.count()
                    # Name is often 0, description later
                    if boxes.count() >= 2:
                        desc = boxes.nth(1)
                    elif boxes.count() == 1:
                        desc = boxes.first
                if desc.count():
                    desc.first.click(force=True)
                    page.keyboard.press("Meta+A")
                    page.keyboard.insert_text(DESC)
                    page.wait_for_timeout(500)
                    result["description_set"] = True
                shot(page, "05_desc")
            except Exception as e:
                result["description_error"] = str(e)

            # Inspect page text for Description field presence
            body = page.locator("body").inner_text()
            result["has_description_label"] = "Description" in body
            result["body_tail"] = body[-1500:]

            publish(page, result, "published")
            shot(page, "06_published")

            # If rename failed, revert isn't needed — check feedback
            page.wait_for_timeout(2000)
            feedback = page.locator("body").inner_text()
            result["post_publish_snip"] = feedback[:1200]

            # Public verify
            page.goto("https://www.youtube.com/@OrbitWithBen", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            dismiss_modals(page)
            shot(page, "07_public")
            result["public_url"] = page.url
            result["public_text"] = page.locator("body").inner_text()[:1800]

            # About / more
            try:
                more = page.get_by_text(re.compile(r"more about this channel|\.\.\.more|More", re.I))
                if more.count():
                    more.first.click(force=True)
                    page.wait_for_timeout(1500)
                    shot(page, "08_about_popup")
                    result["about_popup"] = page.locator("body").inner_text()[:2000]
            except Exception as e:
                result["about_click_err"] = str(e)

            page.goto(
                f"https://studio.youtube.com/channel/{CID}/editing/profile",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3500)
            dismiss_modals(page)
            shot(page, "09_final_studio")
            result["status"] = "ok"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            try:
                shot(page, "z_err")
            except Exception:
                pass
        result["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        RESULT.write_text(json.dumps(result, indent=2))
        ctx.close()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
