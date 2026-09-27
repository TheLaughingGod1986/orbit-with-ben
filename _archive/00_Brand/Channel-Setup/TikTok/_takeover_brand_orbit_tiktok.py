#!/usr/bin/env python3
"""Log into TikTok with Google and apply full Orbit branding."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AVATAR = SETUP / "avatar_800x800.png"
BIO = (SETUP / "bio.txt").read_text().strip()
WEBSITE = "https://www.youtube.com/@OrbitWithBen"
DISPLAY = "Orbit with Ben"
AUDIT = SETUP / "audit"
RESULT = SETUP / "BRAND_RESULT.json"
META = SETUP / "TIKTOK_META.json"
CREATE = SETUP / "CREATE_RESULT.json"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)
        print("shot", name)
    except Exception as e:
        print("shot fail", name, e)


def save_all(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    CREATE.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        meta.update(
            {
                "handle": data.get("handle"),
                "public_url": data.get("public_url"),
                "status": data.get("status"),
                "created_at": data.get("created_at") or meta.get("created_at"),
                "notes": data.get("notes", meta.get("notes")),
            }
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")


def body(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def has(page, pat: str) -> bool:
    return bool(re.search(pat, body(page), re.I | re.S))


def logged_in(page) -> bool:
    # Login button visible = not logged in
    try:
        login = page.locator('[data-e2e="top-login-button"]')
        if login.count() and login.first.is_visible():
            return False
    except Exception:
        pass
    if has(page, r"^Log in$") and page.locator('button:has-text("Log in")').count():
        # sidebar login still present when logged out
        try:
            if page.locator('[data-e2e="top-login-button"]').count():
                return False
        except Exception:
            pass
    # Profile avatar in header / upload available
    url = page.url.lower()
    if "/login" in url or "/signup" in url:
        return False
    try:
        # When logged in, top-right usually has profile / messages, not Log in
        if page.get_by_role("button", name=re.compile(r"^Log in$", re.I)).count() == 0:
            return True
        # data-e2e profile icon
        if page.locator('[data-e2e="nav-profile"], a[href*="/@" ]').count() > 2:
            return True
    except Exception:
        pass
    return "login" not in url and not has(page, r"Sign up for TikTok")


def google_login(page, context) -> bool:
    page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    shot(page, "takeover_00_login")

    # Dismiss cookies
    for pat in (r"Accept all", r"Allow all", r"^Got it$"):
        try:
            b = page.get_by_role("button", name=re.compile(pat, re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1500)
                page.wait_for_timeout(600)
        except Exception:
            pass

    google = page.get_by_text(re.compile(r"Continue with Google", re.I))
    if not google.count():
        # expand / alternate
        try:
            page.get_by_text(re.compile(r"Google", re.I)).first.click()
        except Exception:
            shot(page, "takeover_00_no_google")
            return False

    popup = None
    try:
        with context.expect_page(timeout=25000) as pi:
            google.first.click(force=True)
        popup = pi.value
    except Exception as e:
        print("no popup", e)
        page.wait_for_timeout(4000)
        shot(page, "takeover_00_same_tab")
        # maybe same-tab or already logged in
        if logged_in(page):
            return True
        # QR login page?
        if has(page, r"QR|scan"):
            shot(page, "takeover_00_qr")
            print("QR login shown — waiting 120s for phone scan...")
            for _ in range(24):
                page.wait_for_timeout(5000)
                page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
                if logged_in(page):
                    return True
            return False
        return False

    popup.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    shot(popup, "takeover_01_google")

    try:
        acc = popup.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
        if acc.count():
            acc.first.click()
            popup.wait_for_timeout(3500)
        else:
            # first account
            row = popup.locator("[data-identifier], [data-email]")
            if row.count():
                row.first.click()
                popup.wait_for_timeout(3500)
    except Exception as e:
        print("pick account", e)

    for lab in (r"^Continue$", r"^Allow$", r"^Confirm$"):
        try:
            b = popup.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible():
                b.first.click()
                popup.wait_for_timeout(2500)
        except Exception:
            pass

    # Wait for auth to settle
    for i in range(20):
        page.wait_for_timeout(1500)
        try:
            if popup.is_closed():
                break
        except Exception:
            break
    page.wait_for_timeout(3000)
    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    shot(page, "takeover_02_home")
    return logged_in(page)


def extract_handle(page) -> str | None:
    m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
    if m:
        return m.group(1)
    for sel in (
        '[data-e2e="user-title"]',
        '[data-e2e="user-subtitle"]',
        "h1",
        "h2",
    ):
        try:
            t = page.locator(sel).first.inner_text(timeout=1500)
            m2 = re.search(r"@([\w.]+)", t)
            if m2:
                return m2.group(1)
            if re.match(r"^[\w.]+$", t.strip()) and " " not in t.strip():
                return t.strip()
        except Exception:
            continue
    return None


def open_edit_profile(page) -> bool:
    for url in (
        "https://www.tiktok.com/profile",
        "https://www.tiktok.com/setting",
    ):
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "takeover_03_profile")
        try:
            edit = page.get_by_text(re.compile(r"^Edit profile$", re.I))
            if edit.count() and edit.first.is_visible():
                edit.first.click(force=True)
                page.wait_for_timeout(2000)
                shot(page, "takeover_04_edit")
                return True
        except Exception:
            pass
        # button role
        try:
            b = page.get_by_role("button", name=re.compile(r"Edit profile", re.I))
            if b.count():
                b.first.click(force=True)
                page.wait_for_timeout(2000)
                shot(page, "takeover_04_edit")
                return True
        except Exception:
            pass
    return False


def apply_branding(page) -> dict:
    out = {"name": False, "bio": False, "link": False, "avatar": False}

    # Name / nickname
    for loc in (
        page.get_by_placeholder(re.compile(r"^Name$|Nickname|Display", re.I)),
        page.locator('input[name*="nick" i]'),
        page.locator('input[placeholder*="Name" i]'),
    ):
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.click(force=True)
                loc.first.fill("")
                loc.first.fill(DISPLAY)
                out["name"] = True
                break
        except Exception:
            pass

    # Bio
    try:
        ta = page.locator("textarea")
        if ta.count() and ta.first.is_visible():
            ta.first.click(force=True)
            ta.first.fill("")
            ta.first.fill(BIO)
            out["bio"] = True
    except Exception as e:
        print("bio", e)

    # Website — sometimes under Bio / links section
    try:
        link = page.get_by_placeholder(re.compile(r"website|link|url|bio link", re.I))
        if link.count() and link.first.is_visible():
            link.first.fill(WEBSITE)
            out["link"] = True
        else:
            # click Add link / Website
            add = page.get_by_text(re.compile(r"Add.*(link|website)|Website", re.I))
            if add.count() and add.first.is_visible():
                add.first.click()
                page.wait_for_timeout(1000)
                link2 = page.locator('input[type="url"], input[placeholder*="http" i], input').last
                if link2.count():
                    link2.fill(WEBSITE)
                    out["link"] = True
    except Exception as e:
        print("link", e)

    # Avatar — click change photo then file input
    try:
        # Prefer file input directly
        fi = page.locator('input[type="file"]')
        if fi.count():
            fi.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(3000)
            shot(page, "takeover_05_avatar_crop")
            for lab in (r"^Apply$", r"^Confirm$", r"^Done$", r"^Save$", r"^OK$", r"^Upload$"):
                try:
                    b = page.get_by_role("button", name=re.compile(lab, re.I))
                    if b.count() and b.first.is_visible():
                        b.first.click(force=True)
                        page.wait_for_timeout(2000)
                        break
                except Exception:
                    pass
            out["avatar"] = True
        else:
            # click avatar area to trigger upload
            for pat in (r"Change photo", r"Upload", r"Edit photo", r"Select photo"):
                if page.get_by_text(re.compile(pat, re.I)).count():
                    with page.expect_file_chooser(timeout=5000) as fc:
                        page.get_by_text(re.compile(pat, re.I)).first.click()
                    fc.value.set_files(str(AVATAR))
                    page.wait_for_timeout(3000)
                    out["avatar"] = True
                    break
    except Exception as e:
        print("avatar", e)

    shot(page, "takeover_06_before_save")
    for lab in (r"^Save$", r"^Save changes$"):
        try:
            b = page.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                b.first.click(force=True)
                page.wait_for_timeout(3000)
                break
        except Exception:
            pass
    shot(page, "takeover_07_after_save")
    return out


def maybe_rename_username(page, preferred: str = "OrbitWithBen") -> str | None:
    """Try to set username if editable and available."""
    try:
        # Username field often separate
        u = page.get_by_placeholder(re.compile(r"Username", re.I))
        if not u.count():
            u = page.locator('input[name*="unique" i], input[name*="user" i]')
        if u.count() and u.first.is_visible():
            current = u.first.input_value()
            if current.lower() == preferred.lower():
                return preferred
            u.first.fill(preferred)
            page.wait_for_timeout(2000)
            if has(page, r"already taken|not available"):
                print("username taken:", preferred)
                u.first.fill(current)  # revert
                return current
            return preferred
    except Exception as e:
        print("username edit", e)
    return None


def main() -> None:
    result = {
        "status": "started",
        "display_name": DISPLAY,
        "bio": BIO,
        "website": WEBSITE,
        "handle": None,
        "public_url": None,
        "created_at": time.strftime("%Y-%m-%d"),
        "steps": [],
    }
    AUDIT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            slow_mo=60,
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "takeover_00_home")

        if not logged_in(page):
            ok = google_login(page, context)
            result["steps"].append(f"google_login={ok}")
            if not ok:
                # QR fallback — TikTok often prefers QR for desktop
                page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                shot(page, "takeover_00_qr_wait")
                print("Scan the QR with TikTok app (Profile → Menu → Linked devices / QR). Waiting 150s...")
                result["status"] = "awaiting_qr_scan"
                result["notes"] = "Scan QR in open browser with TikTok phone app to link session."
                save_all(result)
                for i in range(30):
                    page.wait_for_timeout(5000)
                    try:
                        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                        page.wait_for_timeout(1500)
                        if logged_in(page):
                            result["steps"].append("qr_login_ok")
                            break
                    except Exception:
                        pass
                else:
                    result["status"] = "not_logged_in"
                    save_all(result)
                    print(json.dumps(result, indent=2))
                    page.wait_for_timeout(5000)
                    context.close()
                    return
        else:
            result["steps"].append("already_logged_in")

        shot(page, "takeover_02b_authed")
        if not open_edit_profile(page):
            result["status"] = "no_edit_profile"
            result["notes"] = "Logged in but could not open Edit profile. See audit."
            save_all(result)
            print(json.dumps(result, indent=2))
            page.wait_for_timeout(8000)
            context.close()
            return

        handle_try = maybe_rename_username(page, "OrbitWithBen")
        if handle_try:
            result["steps"].append(f"username_field={handle_try}")

        branding = apply_branding(page)
        result["branding"] = branding
        result["steps"].append("branding_applied")

        # Back to profile for handle
        page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        handle = extract_handle(page) or handle_try
        if not handle:
            # try page source / links
            try:
                hrefs = page.locator('a[href*="/@"]').evaluate_all(
                    "els => els.map(e => e.getAttribute('href'))"
                )
                for h in hrefs:
                    m = re.search(r"/@([\w.]+)", h or "")
                    if m and m.group(1).lower() not in ("tiktok", "music"):
                        handle = m.group(1)
                        break
            except Exception:
                pass

        result["handle"] = handle
        if handle:
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            page.goto(result["public_url"], wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            shot(page, "takeover_99_public")
            result["status"] = "branded"
            result["notes"] = (
                f"Public profile {result['public_url']} — verify avatar/bio/name. "
                f"branding={branding}"
            )
        else:
            result["status"] = "branded_unknown_handle"
            result["notes"] = f"Branding attempted: {branding}. Could not read @handle."

        save_all(result)
        print(json.dumps(result, indent=2))
        page.wait_for_timeout(8000)
        context.close()


if __name__ == "__main__":
    main()
