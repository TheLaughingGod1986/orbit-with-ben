#!/usr/bin/env python3
"""Focused Orbit channel create — fill Name+Handle, submit Create channel."""
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
KEYWORDS = (SETUP / "channel_keywords.txt").read_text().strip()
AUDIT = SETUP / "audit"
RESULT = SETUP / "CREATE_RESULT.json"
OPPTIAI = "UCXRVwrCxXpN_o9gvuHPKAPQ"
HANDLES = [
    "OrbitSpace",
    "OrbitStories",
    "MeetOrbit",
    "OrbitExplores",
    "OrbitWithBen",
    "OrbitCosmos",
    "OrbitSpaceStories",
    "HelloOrbit",
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip to YouTube Studio", re.I)).click(
            timeout=1200
        )
    except Exception:
        pass


def extract_cid(url: str) -> str | None:
    m = re.search(r"/channel/(UC[\w-]{20,})", url)
    return m.group(1) if m else None


def appear_dialog(page):
    return page.locator("[role='dialog']").filter(
        has_text=re.compile(r"How you'll appear", re.I)
    )


def create_channel(page, result: dict) -> str | None:
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    shot(page, "c01")

    # Close any leftover picture chooser
    for _ in range(2):
        try:
            if page.get_by_role("button", name="Cancel", exact=True).count():
                # only cancel if picture chooser
                if page.get_by_text("Choose your picture", exact=False).count():
                    page.get_by_role("button", name="Cancel", exact=True).first.click()
                    page.wait_for_timeout(800)
        except Exception:
            pass

    page.get_by_text("Create a channel", exact=True).first.click(force=True)
    page.wait_for_timeout(2500)
    shot(page, "c02_dialog")

    dlg = appear_dialog(page)
    dlg.wait_for(state="visible", timeout=10000)

    # Name field: placeholder or aria Name inside dialog
    name = dlg.get_by_placeholder("Name")
    if not name.count():
        name = dlg.locator('input[aria-label="Name"], input[aria-label*="Name" i]')
    if not name.count():
        name = dlg.locator("input").nth(0)
    name.first.click(force=True)
    name.first.fill("Orbit")
    page.wait_for_timeout(500)
    result["name_value"] = name.first.input_value()
    shot(page, "c03_name")

    handle_set = None
    handle_input = dlg.get_by_placeholder("Handle")
    if not handle_input.count():
        handle_input = dlg.locator('input[aria-label*="Handle" i]')
    if not handle_input.count():
        handle_input = dlg.locator("input").nth(1)

    for h in HANDLES:
        handle_input.first.click(force=True)
        handle_input.first.fill("")
        handle_input.first.fill(h)
        page.wait_for_timeout(2000)
        text = dlg.inner_text()
        create_btn = dlg.get_by_role("button", name=re.compile(r"^Create channel$", re.I))
        disabled = True
        if create_btn.count():
            disabled = create_btn.first.is_disabled()
            # also check aria-disabled
            ad = create_btn.first.get_attribute("aria-disabled")
            if ad == "true":
                disabled = True
            elif ad == "false":
                disabled = False
        result.setdefault("tries", []).append(
            {
                "handle": h,
                "disabled": disabled,
                "rejected": bool(
                    re.search(r"taken|unavailable|can't|invalid|not available", text, re.I)
                ),
            }
        )
        shot(page, f"c04_handle_{h}")
        if not disabled:
            handle_set = h
            break
        if re.search(r"taken|unavailable|can't|invalid|not available", text, re.I):
            continue

    result["handle_set"] = handle_set
    if not handle_set:
        # Try one more time with longer wait on first candidate
        handle_input.first.fill("OrbitSpace")
        page.wait_for_timeout(4000)
        create_btn = dlg.get_by_role("button", name=re.compile(r"^Create channel$", re.I))
        if create_btn.count() and not create_btn.first.is_disabled():
            handle_set = "OrbitSpace"
            result["handle_set"] = handle_set

    shot(page, "c05_ready")
    create_btn = dlg.get_by_role("button", name=re.compile(r"^Create channel$", re.I))
    if not create_btn.count():
        result["error"] = "Create channel button missing"
        return None
    if create_btn.first.is_disabled():
        # Dump dialog HTML for debugging
        result["dialog_html"] = dlg.evaluate("el => el.outerHTML.slice(0,4000)")
        result["dialog_text"] = dlg.inner_text()
        result["error"] = "Create channel still disabled"
        return None

    create_btn.first.click(force=True)
    page.wait_for_timeout(7000)
    shot(page, "c06_after")

    # Verify Orbit appears
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    shot(page, "c07_switcher")
    body = page.locator("body").inner_text()
    result["switcher_has_orbit"] = bool(re.search(r"\bOrbit\b", body))
    result["switcher_text"] = body[:2500]

    if not result["switcher_has_orbit"]:
        result["error"] = "Orbit not listed after create"
        return None

    # Click Orbit channel card
    page.evaluate(
        """() => {
        const items = [...document.querySelectorAll('ytd-account-item-renderer')];
        const hit = items.find(i => /\\bOrbit\\b/.test(i.innerText||'') && !/Oppti/i.test(i.innerText||''));
        if (hit) { hit.click(); return 'renderer'; }
        const all = [...document.querySelectorAll('a, button, div, span')];
        const h2 = all.find(n => (n.innerText||'').trim() === 'Orbit');
        if (h2) { h2.click(); return 'text'; }
        return null;
        }"""
    )
    page.wait_for_timeout(4000)

    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    skip(page)
    shot(page, "c08_studio")
    cid = extract_cid(page.url)
    result["channel_id"] = cid
    result["studio_url"] = page.url

    if cid == OPPTIAI:
        # Force switch
        try:
            page.click("#avatar-btn", timeout=3000)
            page.wait_for_timeout(1000)
            page.get_by_text(re.compile(r"Switch account", re.I)).first.click(force=True)
            page.wait_for_timeout(2000)
            page.get_by_text("Orbit", exact=True).first.click(force=True)
            page.wait_for_timeout(5000)
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            skip(page)
            cid = extract_cid(page.url)
            result["channel_id"] = cid
            result["studio_url"] = page.url
            shot(page, "c09_switched")
        except Exception as e:
            result["switch_err"] = str(e)

    if cid == OPPTIAI:
        result["error"] = "still on OpptiAI"
        return None
    return cid


def brand(page, cid: str, result: dict) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/details",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    shot(page, "d01_details")

    # Description
    try:
        desc = page.locator('#textbox[aria-label*="Description" i]')
        if not desc.count():
            boxes = page.locator("#textbox")
            desc = boxes.nth(1) if boxes.count() > 1 else boxes.first
        desc.first.click(force=True)
        page.keyboard.press("Meta+A")
        page.keyboard.insert_text(DESC)
        result["description_set"] = True
        page.wait_for_timeout(500)
    except Exception as e:
        result["description_error"] = str(e)
    shot(page, "d02_desc")

    # Keywords
    try:
        kw = page.locator("input[aria-label*='Keyword' i], #keywords-container input")
        if kw.count():
            kw.first.click(force=True)
            for part in [k.strip() for k in KEYWORDS.split(",") if k.strip()][:10]:
                page.keyboard.type(part)
                page.keyboard.press("Enter")
                page.wait_for_timeout(120)
            result["keywords_set"] = True
    except Exception as e:
        result["keywords_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["details_saved"] = True
    shot(page, "d03_saved")

    # Images
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/images",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    shot(page, "d04_images")

    inputs = page.locator('input[type="file"]')
    result["file_inputs"] = inputs.count()
    try:
        if inputs.count() >= 1:
            inputs.nth(0).set_input_files(str(AVATAR))
            page.wait_for_timeout(2500)
            for label in ("Done", "Apply", "Confirm", "Save"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(1000)
            result["avatar_ok"] = True
        shot(page, "d05_avatar")
    except Exception as e:
        result["avatar_error"] = str(e)

    try:
        inputs = page.locator('input[type="file"]')
        idx = 1 if inputs.count() > 1 else 0
        inputs.nth(idx).set_input_files(str(BANNER))
        page.wait_for_timeout(3000)
        for label in ("Done", "Apply", "Confirm", "Save"):
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                b.first.click(force=True)
                page.wait_for_timeout(1000)
        result["banner_ok"] = True
        shot(page, "d06_banner")
    except Exception as e:
        result["banner_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["branding_saved"] = True
    shot(page, "d07_done")

    page.goto(f"https://www.youtube.com/channel/{cid}", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    shot(page, "d08_public")
    result["public_url"] = page.url
    m = re.search(r"youtube\.com/@([\w.-]+)", page.url)
    if m:
        result["public_handle"] = "@" + m.group(1)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {"started_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            cid = create_channel(page, result)
            if cid:
                brand(page, cid, result)
                result["status"] = "ok"
            else:
                result["status"] = "failed"
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
