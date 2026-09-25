#!/usr/bin/env python3
"""Create Orbit YouTube Brand Account — careful dialog targeting."""
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
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Dismiss", "Got it", "Not now", "No thanks"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


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


def dialog(page):
    # Prefer the How you'll appear dialog
    for sel in (
        "yt-channel-creation-dialog-renderer",
        "ytd-channel-creation-dialog-renderer",
        "tp-yt-paper-dialog",
        "[role='dialog']",
    ):
        loc = page.locator(sel).filter(has_text=re.compile(r"How you'll appear|Create channel", re.I))
        if loc.count() and loc.first.is_visible():
            return loc.first
    loc = page.locator("[role='dialog']")
    return loc.first if loc.count() else None


def create_orbit(page, result: dict) -> str | None:
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    dismiss(page)
    shot(page, "a01_switcher")

    # Click Create a channel card/button — not the top nav Create
    clicked = page.evaluate(
        """() => {
        const nodes = [...document.querySelectorAll('button, a, yt-formatted-string, span, div')];
        const hit = nodes.find(n => {
          const t = (n.innerText || '').trim();
          return t === 'Create a channel' || t === '+ Create a channel';
        });
        if (!hit) return false;
        hit.click();
        return true;
        }"""
    )
    result["create_card_clicked"] = clicked
    page.wait_for_timeout(2500)
    shot(page, "a02_dialog")

    dlg = dialog(page)
    if not dlg:
        result["error"] = "create dialog not found"
        return None

    # Inspect inputs inside dialog
    info = page.evaluate(
        """() => {
        const d = document.querySelector('yt-channel-creation-dialog-renderer, ytd-channel-creation-dialog-renderer, [role=dialog]');
        if (!d) return {ok:false};
        const inputs = [...d.querySelectorAll('input, textarea, [contenteditable=true], #textbox')].map(el => ({
          tag: el.tagName,
          type: el.getAttribute('type'),
          id: el.id,
          name: el.getAttribute('name'),
          aria: el.getAttribute('aria-label'),
          placeholder: el.getAttribute('placeholder'),
          value: el.value || el.textContent || ''
        }));
        const buttons = [...d.querySelectorAll('button, yt-button-renderer, tp-yt-paper-button')].map(el => ({
          text: (el.innerText||'').trim(),
          disabled: !!(el.disabled || el.getAttribute('aria-disabled') === 'true' || el.hasAttribute('disabled'))
        }));
        return {ok:true, inputs, buttons, html: d.outerHTML.slice(0, 2500)};
        }"""
    )
    result["dialog_inspect"] = {
        "ok": info.get("ok"),
        "inputs": info.get("inputs"),
        "buttons": info.get("buttons"),
    }
    (AUDIT / "dialog_inspect.json").write_text(json.dumps(info, indent=2))

    # Fill Name — prefer aria/placeholder Name inside dialog
    name_ok = page.evaluate(
        """(name) => {
        const d = document.querySelector('yt-channel-creation-dialog-renderer, ytd-channel-creation-dialog-renderer, [role=dialog]');
        if (!d) return false;
        const inputs = [...d.querySelectorAll('input')];
        // Usually first text input is Name, second is Handle
        let nameInput = inputs.find(i => /name/i.test(i.getAttribute('aria-label')||'') || /name/i.test(i.placeholder||''));
        if (!nameInput) nameInput = inputs.find(i => i.type === 'text' || !i.type);
        if (!nameInput) return false;
        nameInput.focus();
        nameInput.value = '';
        nameInput.dispatchEvent(new Event('input', {bubbles:true}));
        const native = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        native.call(nameInput, name);
        nameInput.dispatchEvent(new Event('input', {bubbles:true}));
        nameInput.dispatchEvent(new Event('change', {bubbles:true}));
        return true;
        }""",
        "Orbit",
    )
    result["name_ok_js"] = name_ok

    # Also try Playwright fill on dialog inputs
    d_inputs = dlg.locator("input")
    if d_inputs.count() >= 1:
        d_inputs.nth(0).click(force=True)
        d_inputs.nth(0).fill("")
        d_inputs.nth(0).fill("Orbit")
        page.wait_for_timeout(400)
        result["name_playwright"] = d_inputs.nth(0).input_value()

    shot(page, "a03_name")

    # Handle candidates
    handle_set = None
    for h in HANDLES:
        if d_inputs.count() >= 2:
            d_inputs.nth(1).click(force=True)
            d_inputs.nth(1).fill("")
            d_inputs.nth(1).fill(h)
        else:
            page.evaluate(
                """(h) => {
                const d = document.querySelector('yt-channel-creation-dialog-renderer, ytd-channel-creation-dialog-renderer, [role=dialog]');
                const inputs = [...d.querySelectorAll('input')];
                let hi = inputs.find(i => /handle/i.test(i.getAttribute('aria-label')||'') || /handle/i.test(i.placeholder||''));
                if (!hi) hi = inputs[1];
                if (!hi) return false;
                const native = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                native.call(hi, h);
                hi.dispatchEvent(new Event('input', {bubbles:true}));
                hi.dispatchEvent(new Event('change', {bubbles:true}));
                return true;
                }""",
                h,
            )
        page.wait_for_timeout(1800)
        body = dlg.inner_text()
        if re.search(r"already taken|not available|unavailable|can't use", body, re.I):
            result.setdefault("handle_rejected", []).append(h)
            continue
        # Check Create channel enabled
        enabled = page.evaluate(
            """() => {
            const d = document.querySelector('yt-channel-creation-dialog-renderer, ytd-channel-creation-dialog-renderer, [role=dialog]');
            const btns = [...d.querySelectorAll('button, yt-button-shape button, tp-yt-paper-button')];
            const create = btns.find(b => /create channel/i.test(b.innerText||''));
            if (!create) return {found:false};
            const disabled = create.disabled || create.getAttribute('aria-disabled') === 'true';
            return {found:true, disabled, text: create.innerText};
            }"""
        )
        result.setdefault("handle_tries", []).append({"handle": h, "enabled": enabled})
        if enabled.get("found") and not enabled.get("disabled"):
            handle_set = h
            break
        # Sometimes availability is async — if no explicit rejection, try create
        if not re.search(r"taken|unavailable|can't|invalid", body, re.I):
            handle_set = h
            # still try clicking
            break

    result["handle_set"] = handle_set
    shot(page, "a04_handle")

    # Optional: select picture during create
    try:
        file_inputs = dlg.locator('input[type="file"]')
        if file_inputs.count():
            file_inputs.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(1500)
            for label in ("Done", "Apply", "Confirm"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible():
                    b.first.click(force=True)
                    page.wait_for_timeout(800)
            result["picture_at_create"] = True
        else:
            # Click Select picture then set file
            if dlg.get_by_text("Select picture", exact=False).count():
                with page.expect_file_chooser(timeout=3000) as fc:
                    dlg.get_by_text("Select picture", exact=False).first.click(force=True)
                fc.value.set_files(str(AVATAR))
                page.wait_for_timeout(1500)
                for label in ("Done", "Apply", "Confirm"):
                    b = page.get_by_role("button", name=label, exact=True)
                    if b.count() and b.first.is_visible():
                        b.first.click(force=True)
                        page.wait_for_timeout(800)
                result["picture_at_create"] = True
    except Exception as e:
        result["picture_at_create_error"] = str(e)

    shot(page, "a05_before_submit")

    # Click Create channel INSIDE dialog only
    submitted = page.evaluate(
        """() => {
        const d = document.querySelector('yt-channel-creation-dialog-renderer, ytd-channel-creation-dialog-renderer, [role=dialog]');
        if (!d) return {ok:false, reason:'no dialog'};
        const btns = [...d.querySelectorAll('button')];
        const create = btns.find(b => /^\\s*Create channel\\s*$/i.test(b.innerText||''));
        if (!create) return {ok:false, reason:'no button', texts: btns.map(b=>b.innerText.trim())};
        if (create.disabled || create.getAttribute('aria-disabled') === 'true') {
          return {ok:false, reason:'disabled', texts: btns.map(b=>b.innerText.trim())};
        }
        create.click();
        return {ok:true};
        }"""
    )
    result["submit"] = submitted
    page.wait_for_timeout(6000)
    shot(page, "a06_after_submit")

    # If still on switcher, look for Orbit
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    shot(page, "a07_switcher_after")
    listing = page.locator("body").inner_text()
    result["switcher_has_orbit"] = bool(re.search(r"\bOrbit\b", listing))
    result["switcher_snippet"] = listing[:2000]

    if result["switcher_has_orbit"]:
        # Click Orbit row (not OpptiAI)
        page.evaluate(
            """() => {
            const nodes = [...document.querySelectorAll('ytd-account-item-renderer, a, button, div')];
            const hit = nodes.find(n => {
              const t = (n.innerText||'').trim();
              return /^Orbit\\b/m.test(t) && !/Oppti/i.test(t) && t.length < 80;
            });
            if (hit) { hit.click(); return true; }
            return false;
            }"""
        )
        page.wait_for_timeout(4000)

    # Studio
    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(4500)
    skip(page)
    shot(page, "a08_studio")
    cid = extract_cid(page.url)
    result["studio_url"] = page.url
    result["channel_id"] = cid

    # If still OpptiAI but Orbit exists, switch via studio avatar
    if cid == OPPTIAI and result["switcher_has_orbit"]:
        try:
            page.locator("#avatar-btn, button#avatar-btn").first.click(timeout=3000)
            page.wait_for_timeout(1200)
            page.get_by_text(re.compile(r"Switch account|All channels", re.I)).first.click(
                force=True
            )
            page.wait_for_timeout(2000)
            page.get_by_text("Orbit", exact=True).first.click(force=True)
            page.wait_for_timeout(4000)
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            skip(page)
            cid = extract_cid(page.url)
            result["channel_id"] = cid
            result["studio_url"] = page.url
            shot(page, "a09_studio_switched")
        except Exception as e:
            result["studio_switch_error"] = str(e)

    return cid


def brand(page, cid: str, result: dict) -> None:
    # Details
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/details",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    dismiss(page)
    shot(page, "b01_details")

    # Description box
    desc_ok = False
    try:
        # Find description textbox by aria-label
        tb = page.locator('#textbox[aria-label*="Description" i], [aria-label*="Description" i] #textbox')
        if not tb.count():
            # Fallback: all #textbox — description is usually the taller one
            tbs = page.locator("ytcp-social-suggestions-textbox #textbox, #textbox")
            if tbs.count() >= 2:
                tb = tbs.nth(1)
            elif tbs.count() == 1:
                tb = tbs.first
        if tb.count():
            tb.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.insert_text(DESC)
            desc_ok = True
            page.wait_for_timeout(600)
    except Exception as e:
        result["desc_error"] = str(e)
    result["description_set"] = desc_ok
    shot(page, "b02_desc")

    # Keywords
    try:
        kw = page.locator("#keywords-container input, input[aria-label*='Keyword' i]")
        if kw.count():
            kw.first.click(force=True)
            for part in [k.strip() for k in KEYWORDS.split(",") if k.strip()][:12]:
                page.keyboard.type(part)
                page.keyboard.press("Tab")
                page.wait_for_timeout(150)
            result["keywords_set"] = True
    except Exception as e:
        result["keywords_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["details_saved"] = True
    shot(page, "b03_saved_details")

    # Branding images
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/images",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4500)
    skip(page)
    dismiss(page)
    shot(page, "b04_images")

    inputs = page.locator('input[type="file"]')
    result["file_input_count"] = inputs.count()
    try:
        if inputs.count() >= 1:
            inputs.nth(0).set_input_files(str(AVATAR))
            page.wait_for_timeout(2500)
            for label in ("Done", "Apply", "Save", "Confirm"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(1200)
            result["avatar_uploaded"] = True
        shot(page, "b05_avatar")
    except Exception as e:
        result["avatar_error"] = str(e)

    try:
        inputs = page.locator('input[type="file"]')
        idx = 1 if inputs.count() > 1 else 0
        inputs.nth(idx).set_input_files(str(BANNER))
        page.wait_for_timeout(3000)
        for label in ("Done", "Apply", "Save", "Confirm"):
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                b.first.click(force=True)
                page.wait_for_timeout(1200)
        result["banner_uploaded"] = True
        shot(page, "b06_banner")
    except Exception as e:
        result["banner_error"] = str(e)

    save = page.get_by_role("button", name="Save", exact=True)
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(3500)
        result["branding_saved"] = True
    shot(page, "b07_branding_saved")

    # Public verify
    page.goto(f"https://www.youtube.com/channel/{cid}", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    shot(page, "b08_public")
    result["public_url"] = page.url
    m = re.search(r"youtube\.com/@([\w.-]+)", page.url)
    if m:
        result["public_handle"] = "@" + m.group(1)
    result["public_text_has_orbit"] = "Orbit" in page.locator("body").inner_text()


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "guard_opptiai": OPPTIAI,
    }
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            cid = create_orbit(page, result)
            if not cid:
                result["status"] = "failed_no_cid"
            elif cid == OPPTIAI:
                result["status"] = "aborted_opptiai"
            else:
                brand(page, cid, result)
                result["status"] = "ok"
                result["channel_id"] = cid
            result["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            try:
                shot(page, "z_error")
            except Exception:
                pass
        RESULT.write_text(json.dumps(result, indent=2))
        ctx.close()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
