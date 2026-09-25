#!/usr/bin/env python3
"""Create a brand-new Orbit YouTube Brand Account channel and brand it.

Uses the existing Google login (benoats86@gmail.com) via the Playwright
YouTube profile. Does NOT modify OpptiAI (UCXRVwrCxXpN_o9gvuHPKAPQ).
"""
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
CHANNEL_NAME = "Orbit"
HANDLE_CANDIDATES = [
    "OrbitSpace",
    "OrbitStories",
    "MeetOrbit",
    "OrbitExplores",
    "OrbitWithBen",
    "OrbitCosmos",
]


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip to YouTube Studio", re.I)).click(
            timeout=1500
        )
        page.wait_for_timeout(400)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Dismiss", "Got it", "Not now", "No thanks", "Cancel"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
                page.wait_for_timeout(300)
        except Exception:
            pass


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def extract_channel_id(url: str) -> str | None:
    m = re.search(r"/channel/(UC[\w-]{20,})", url)
    return m.group(1) if m else None


def list_existing_channels(page) -> list[dict]:
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "01_channel_switcher")
    return page.evaluate(
        """() => {
        const out = [];
        const items = [...document.querySelectorAll('ytd-account-item-renderer, yt-account-item-renderer, a[href*="/channel/"], a[href*="/@"]')];
        for (const el of items) {
          const text = (el.innerText || '').trim().replace(/\\s+/g, ' ');
          const href = el.href || el.querySelector('a')?.href || '';
          if (text && (href.includes('/channel/') || href.includes('/@') || text.length < 80)) {
            out.push({ text: text.slice(0, 120), href });
          }
        }
        // Also capture all visible account rows
        const rows = [...document.querySelectorAll('[role="link"], ytd-account-item-renderer')];
        for (const r of rows) {
          const t = (r.innerText || '').trim().replace(/\\s+/g, ' ');
          if (t && t.length < 100) out.push({ text: t.slice(0, 120), href: r.href || '' });
        }
        return out;
        }"""
    )


def create_channel(page, result: dict) -> str | None:
    """Create a new Brand Account channel named Orbit. Returns channel id."""
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    dismiss(page)
    shot(page, "02_before_create")

    # Prefer explicit Create a channel control
    created = False
    for label in (
        "Create a channel",
        "Create channel",
        "New channel",
        "Add account",
    ):
        loc = page.get_by_role("link", name=re.compile(label, re.I))
        if not loc.count():
            loc = page.get_by_role("button", name=re.compile(label, re.I))
        if not loc.count():
            loc = page.get_by_text(re.compile(rf"^{label}$", re.I))
        if loc.count():
            try:
                loc.first.click(force=True, timeout=3000)
                created = True
                page.wait_for_timeout(2500)
                break
            except Exception as e:
                result.setdefault("create_click_errors", []).append(f"{label}: {e}")

    if not created:
        # Fallback: YouTube create_channel URL
        page.goto("https://www.youtube.com/create_channel", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        shot(page, "02b_create_channel_url")

    shot(page, "03_create_dialog")
    body = page.locator("body").inner_text()
    result["create_dialog_snippet"] = body[:1500]

    # Fill channel name
    name_filled = False
    for sel in (
        'input[aria-label*="Name" i]',
        'input[name="name"]',
        'input[type="text"]',
        "#channel-name-input",
        'tp-yt-paper-input input',
        "ytcp-social-suggestions-textbox #textbox",
    ):
        loc = page.locator(sel)
        if loc.count() and loc.first.is_visible():
            loc.first.click(force=True)
            loc.first.fill("")
            loc.first.fill(CHANNEL_NAME)
            name_filled = True
            page.wait_for_timeout(500)
            break

    if not name_filled:
        # Contenteditable name fields
        editable = page.locator('[contenteditable="true"], #textbox')
        if editable.count():
            editable.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.type(CHANNEL_NAME)
            name_filled = True

    result["name_filled"] = name_filled
    shot(page, "04_name_filled")

    # Confirm create
    for label in ("Create", "Create channel", "Done", "Next", "Continue"):
        btn = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
        if btn.count() and btn.first.is_visible() and btn.first.is_enabled():
            btn.first.click(force=True)
            page.wait_for_timeout(4000)
            result["confirm_clicked"] = label
            break

    dismiss(page)
    shot(page, "05_after_create")

    # Detect new channel id from URL or studio redirect
    page.wait_for_timeout(2000)
    url = page.url
    cid = extract_channel_id(url)
    if not cid:
        # Try Studio home
        page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        shot(page, "06_studio_home")
        url = page.url
        cid = extract_channel_id(url)

    if cid == OPPTIAI:
        result["warning"] = "Landed on OpptiAI — will switch to Orbit if present"
        # Open switcher inside studio
        try:
            page.locator("#avatar-btn, button#avatar-btn, #account-button").first.click(
                force=True, timeout=3000
            )
            page.wait_for_timeout(1500)
            shot(page, "06b_avatar_menu")
            # Switch account / Switch channel
            for t in ("Switch account", "Switch channel", "All channels"):
                if page.get_by_text(t, exact=False).count():
                    page.get_by_text(t, exact=False).first.click(force=True)
                    page.wait_for_timeout(2000)
                    break
            shot(page, "06c_switch_list")
            if page.get_by_text("Orbit", exact=True).count():
                page.get_by_text("Orbit", exact=True).first.click(force=True)
                page.wait_for_timeout(4000)
                cid = extract_channel_id(page.url)
        except Exception as e:
            result["switch_error"] = str(e)

    result["channel_id"] = cid
    result["studio_url"] = page.url
    return cid


def set_basic_info(page, channel_id: str, result: dict) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{channel_id}/editing/details",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    shot(page, "07_details")

    # Name
    try:
        name_box = page.locator("#textbox").first
        if name_box.count():
            # First textbox is often name on details
            pass
    except Exception:
        pass

    # Description — look for Description heading then textbox
    desc_set = False
    try:
        # Studio uses ytcp-social-suggestions-textbox for description
        boxes = page.locator("ytcp-social-suggestions-textbox, #description-container #textbox, #textbox")
        # Prefer the larger description box
        for i in range(boxes.count()):
            box = boxes.nth(i)
            label = ""
            try:
                label = (box.get_attribute("label") or "") + " " + (box.inner_text() or "")
            except Exception:
                pass
            aria = ""
            try:
                aria = box.locator("#textbox").get_attribute("aria-label") or ""
            except Exception:
                pass
            blob = (label + aria).lower()
            target = box.locator("#textbox") if box.locator("#textbox").count() else box
            if "description" in blob or i == 1:
                target.click(force=True)
                page.keyboard.press("Meta+A")
                page.keyboard.insert_text(DESC)
                desc_set = True
                page.wait_for_timeout(800)
                break
        if not desc_set and boxes.count() >= 2:
            t = boxes.nth(1).locator("#textbox")
            t.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.insert_text(DESC)
            desc_set = True
    except Exception as e:
        result["desc_error"] = str(e)
    result["description_set"] = desc_set
    shot(page, "08_description")

    # Handle if editable
    handle_set = None
    for candidate in HANDLE_CANDIDATES:
        try:
            handle_input = page.locator(
                'input[aria-label*="Handle" i], input[name*="handle" i], #handle-input input'
            )
            if not handle_input.count():
                # Sometimes a link "Create handle" / edit handle
                edit = page.get_by_text(re.compile(r"Handle|Create your handle", re.I))
                if edit.count():
                    edit.first.click(force=True)
                    page.wait_for_timeout(1000)
                handle_input = page.locator('input[type="text"]')
            if handle_input.count():
                handle_input.first.click(force=True)
                handle_input.first.fill("")
                handle_input.first.fill(candidate)
                page.wait_for_timeout(1500)
                body = page.locator("body").inner_text()
                if re.search(r"already taken|not available|unavailable", body, re.I):
                    continue
                handle_set = candidate
                break
        except Exception as e:
            result.setdefault("handle_errors", []).append(f"{candidate}: {e}")
    result["handle_set"] = handle_set
    shot(page, "09_handle")

    # Keywords
    try:
        kw = page.locator(
            'input[aria-label*="Keyword" i], #keywords-container input, ytcp-chip-bar input'
        )
        if kw.count():
            kw.first.click(force=True)
            for part in [k.strip() for k in KEYWORDS.split(",") if k.strip()]:
                page.keyboard.type(part)
                page.keyboard.press("Enter")
                page.wait_for_timeout(200)
            result["keywords_set"] = True
    except Exception as e:
        result["keywords_error"] = str(e)

    # Save
    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["details_saved"] = True
    else:
        result["details_saved"] = False
    shot(page, "10_details_saved")


def set_branding_images(page, channel_id: str, result: dict) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{channel_id}/editing/images",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    shot(page, "11_branding")

    # Picture upload
    try:
        # Prefer Picture section file input
        inputs = page.locator('input[type="file"]')
        result["file_inputs"] = inputs.count()
        if inputs.count() >= 1:
            inputs.nth(0).set_input_files(str(AVATAR))
            page.wait_for_timeout(2500)
            # Confirm crop dialogs
            for label in ("Done", "Apply", "Save", "Confirm"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(1500)
            result["avatar_uploaded"] = True
        shot(page, "12_avatar")
    except Exception as e:
        result["avatar_error"] = str(e)

    # Banner upload — usually second file input
    try:
        inputs = page.locator('input[type="file"]')
        idx = 1 if inputs.count() > 1 else 0
        inputs.nth(idx).set_input_files(str(BANNER))
        page.wait_for_timeout(3000)
        for label in ("Done", "Apply", "Save", "Confirm"):
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                b.first.click(force=True)
                page.wait_for_timeout(1500)
        result["banner_uploaded"] = True
        shot(page, "13_banner")
    except Exception as e:
        result["banner_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["branding_saved"] = True
    shot(page, "14_branding_saved")


def verify(page, channel_id: str, result: dict) -> None:
    page.goto(f"https://www.youtube.com/channel/{channel_id}", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "15_public_channel")
    text = page.locator("body").inner_text()
    result["public_has_orbit"] = "Orbit" in text
    result["public_url"] = page.url
    # Handle from URL if redirected to /@
    m = re.search(r"youtube\.com/@([\w.-]+)", page.url)
    if m:
        result["public_handle"] = "@" + m.group(1)

    page.goto(
        f"https://studio.youtube.com/channel/{channel_id}",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(3000)
    skip(page)
    shot(page, "16_studio_final")
    result["final_studio_url"] = page.url
    result["not_opptiai"] = channel_id != OPPTIAI


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "channel_name": CHANNEL_NAME,
        "opptiai_guard": OPPTIAI,
        "avatar": str(AVATAR),
        "banner": str(BANNER),
    }
    assert AVATAR.exists(), AVATAR
    assert BANNER.exists(), BANNER

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            existing = list_existing_channels(page)
            result["existing_channels_preview"] = existing[:20]

            # Abort if an Orbit channel already exists — still OK to brand it only if brand-new empty?
            orbit_existing = [
                e
                for e in existing
                if re.search(r"\bOrbit\b", e.get("text", ""), re.I)
                and "Oppti" not in e.get("text", "")
            ]
            result["orbit_already_listed"] = orbit_existing

            if orbit_existing:
                # Do not silently reuse — user asked for brand NEW. Still report.
                result["status"] = "orbit_name_already_present"
                # Try to open it and capture id for user decision
                page.get_by_text("Orbit", exact=False).first.click(force=True)
                page.wait_for_timeout(3000)
                cid = extract_channel_id(page.url)
                if not cid:
                    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(3500)
                    cid = extract_channel_id(page.url)
                result["channel_id"] = cid
            else:
                cid = create_channel(page, result)

            if not cid:
                result["status"] = "failed_no_channel_id"
                RESULT.write_text(json.dumps(result, indent=2))
                context.close()
                print(json.dumps(result, indent=2))
                return

            if cid == OPPTIAI:
                result["status"] = "aborted_would_edit_opptiai"
                RESULT.write_text(json.dumps(result, indent=2))
                context.close()
                print(json.dumps(result, indent=2))
                return

            set_basic_info(page, cid, result)
            set_branding_images(page, cid, result)
            verify(page, cid, result)
            result["status"] = "ok"
            result["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            try:
                shot(page, "99_error")
            except Exception:
                pass
        RESULT.write_text(json.dumps(result, indent=2))
        context.close()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
