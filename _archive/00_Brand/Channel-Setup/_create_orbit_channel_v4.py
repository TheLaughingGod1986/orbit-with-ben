#!/usr/bin/env python3
"""Create Orbit channel trying alternate display names (YouTube rejected bare 'Orbit')."""
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

# Display name candidates — keep Orbit-first branding
NAME_HANDLE_PAIRS = [
    ("Orbit Stories", "OrbitStories"),
    ("Orbit Space", "OrbitSpace"),
    ("Meet Orbit", "MeetOrbit"),
    ("Orbit Explores", "OrbitExplores"),
    ("Orbit with Ben", "OrbitWithBen"),
    ("Hello Orbit", "HelloOrbit"),
    ("Orbit Cosmos", "OrbitCosmos"),
    ("Orbit Space Stories", "OrbitSpaceStories"),
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip to YouTube Studio", re.I)).click(
            timeout=1000
        )
    except Exception:
        pass


def extract_cid(url: str) -> str | None:
    m = re.search(r"/channel/(UC[\w-]{20,})", url)
    return m.group(1) if m else None


def dlg(page):
    return page.locator("[role='dialog']").filter(
        has_text=re.compile(r"How you'll appear", re.I)
    )


def open_create(page) -> None:
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    # Dismiss leftover dialogs
    for _ in range(3):
        try:
            if page.get_by_text("Choose your picture", exact=False).count():
                page.get_by_role("button", name="Cancel", exact=True).first.click()
                page.wait_for_timeout(600)
            d = dlg(page)
            if d.count() and d.first.is_visible():
                page.get_by_role("button", name="Cancel", exact=True).first.click()
                page.wait_for_timeout(600)
        except Exception:
            break
    page.get_by_text("Create a channel", exact=True).first.click(force=True)
    page.wait_for_timeout(2000)
    dlg(page).wait_for(state="visible", timeout=10000)


def try_create(page, name: str, handle: str, result: dict) -> bool:
    d = dlg(page)
    name_in = d.get_by_placeholder("Name")
    if not name_in.count():
        name_in = d.locator("input").nth(0)
    handle_in = d.get_by_placeholder("Handle")
    if not handle_in.count():
        handle_in = d.locator("input").nth(1)

    name_in.first.click(force=True)
    name_in.first.fill("")
    name_in.first.fill(name)
    page.wait_for_timeout(400)

    handle_in.first.click(force=True)
    handle_in.first.fill("")
    handle_in.first.fill(handle)
    page.wait_for_timeout(2500)

    create_btn = d.get_by_role("button", name=re.compile(r"^Create channel$", re.I))
    disabled = create_btn.first.is_disabled() if create_btn.count() else True
    ad = create_btn.first.get_attribute("aria-disabled") if create_btn.count() else "true"
    if ad == "true":
        disabled = True
    text = d.inner_text()
    entry = {
        "name": name,
        "handle": handle,
        "disabled": disabled,
        "text_snip": text[-400:],
    }
    result.setdefault("attempts", []).append(entry)
    shot(page, f"n_{re.sub(r'[^A-Za-z0-9]+', '_', name)}_{handle}")

    if disabled:
        return False

    create_btn.first.click(force=True)
    page.wait_for_timeout(8000)
    shot(page, f"n_after_{handle}")

    # Still open with error?
    if dlg(page).count() and dlg(page).first.is_visible():
        t = dlg(page).inner_text()
        entry["after"] = t[-500:]
        if re.search(r"Failed to create|try changing|error", t, re.I):
            entry["failed"] = True
            return False
        # maybe still loading
        page.wait_for_timeout(4000)

    return True


def brand(page, cid: str, result: dict) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/details",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    shot(page, "brand_details")

    try:
        desc = page.locator('#textbox[aria-label*="Description" i]')
        if not desc.count():
            boxes = page.locator("#textbox")
            desc = boxes.nth(1) if boxes.count() > 1 else boxes.first
        desc.first.click(force=True)
        page.keyboard.press("Meta+A")
        page.keyboard.insert_text(DESC)
        result["description_set"] = True
    except Exception as e:
        result["description_error"] = str(e)

    try:
        kw = page.locator("input[aria-label*='Keyword' i], #keywords-container input")
        if kw.count():
            kw.first.click(force=True)
            for part in [k.strip() for k in KEYWORDS.split(",") if k.strip()][:10]:
                page.keyboard.type(part)
                page.keyboard.press("Enter")
                page.wait_for_timeout(100)
            result["keywords_set"] = True
    except Exception as e:
        result["keywords_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["details_saved"] = True
    shot(page, "brand_details_saved")

    # Try rename display name to just Orbit if Studio allows (optional)
    try:
        name_box = page.locator('#textbox[aria-label*="Name" i], #textbox').first
        # leave as created for now
    except Exception:
        pass

    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/images",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    shot(page, "brand_images")

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
        shot(page, "brand_avatar")
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
        shot(page, "brand_banner")
    except Exception as e:
        result["banner_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["branding_saved"] = True
    shot(page, "brand_done")

    page.goto(f"https://www.youtube.com/channel/{cid}", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    shot(page, "brand_public")
    result["public_url"] = page.url
    m = re.search(r"youtube\.com/@([\w.-]+)", page.url)
    if m:
        result["public_handle"] = "@" + m.group(1)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"started_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            open_create(page)
            shot(page, "n00_open")
            created = False
            for name, handle in NAME_HANDLE_PAIRS:
                # Ensure dialog open
                if not (dlg(page).count() and dlg(page).first.is_visible()):
                    open_create(page)
                ok = try_create(page, name, handle, result)
                if ok:
                    created = True
                    result["created_name"] = name
                    result["created_handle"] = handle
                    break

            if not created:
                result["status"] = "failed_all_names"
                RESULT.write_text(json.dumps(result, indent=2))
                ctx.close()
                print(json.dumps(result, indent=2))
                return

            page.wait_for_timeout(3000)
            page.goto(
                "https://www.youtube.com/channel_switcher", wait_until="domcontentloaded"
            )
            page.wait_for_timeout(3500)
            shot(page, "n_switcher")
            body = page.locator("body").inner_text()
            result["switcher_text"] = body[:2500]
            result["switcher_has_orbit"] = "Orbit" in body

            # Click the new channel (match created name)
            target = result.get("created_name", "Orbit")
            page.evaluate(
                """(target) => {
                const items = [...document.querySelectorAll('ytd-account-item-renderer')];
                let hit = items.find(i => (i.innerText||'').includes(target) && !/Oppti/i.test(i.innerText||''));
                if (!hit) hit = items.find(i => /Orbit/i.test(i.innerText||'') && !/Oppti/i.test(i.innerText||''));
                if (hit) { hit.click(); return true; }
                return false;
                }""",
                target,
            )
            page.wait_for_timeout(4000)

            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            skip(page)
            cid = extract_cid(page.url)
            result["channel_id"] = cid
            result["studio_url"] = page.url
            shot(page, "n_studio")

            if cid == OPPTIAI:
                try:
                    page.click("#avatar-btn", timeout=3000)
                    page.wait_for_timeout(800)
                    page.get_by_text(re.compile(r"Switch account", re.I)).first.click(
                        force=True
                    )
                    page.wait_for_timeout(2000)
                    page.get_by_text(re.compile(r"Orbit", re.I)).first.click(force=True)
                    page.wait_for_timeout(4000)
                    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(4000)
                    skip(page)
                    cid = extract_cid(page.url)
                    result["channel_id"] = cid
                    result["studio_url"] = page.url
                except Exception as e:
                    result["switch_err"] = str(e)

            if not cid or cid == OPPTIAI:
                result["status"] = "created_but_could_not_switch"
            else:
                brand(page, cid, result)
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
