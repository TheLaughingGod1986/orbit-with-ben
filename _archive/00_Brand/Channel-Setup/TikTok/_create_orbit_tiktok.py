#!/usr/bin/env python3
"""Create Orbit with Ben TikTok account using existing Google Playwright profile."""
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
RESULT = SETUP / "CREATE_RESULT.json"
META = SETUP / "TIKTOK_META.json"

HANDLE_CANDIDATES = [
    "OrbitWithBen",
    "OrbitWithBenYT",
    "MeetOrbit",
    "OrbitExplores",
    "HelloOrbit",
    "OrbitCosmos",
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def save_result(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        meta.update(
            {
                "handle": data.get("handle"),
                "public_url": data.get("public_url"),
                "status": data.get("status"),
                "created_at": data.get("created_at"),
                "notes": data.get("notes", meta.get("notes")),
            }
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")


def dismiss_cookies(page) -> None:
    for label in (
        r"Accept all",
        r"Allow all",
        r"Agree and continue",
        r"^Accept$",
        r"Got it",
    ):
        try:
            btn = page.get_by_role("button", name=re.compile(label, re.I))
            if btn.count() and btn.first.is_visible():
                btn.first.click(timeout=1500)
                page.wait_for_timeout(800)
                return
        except Exception:
            pass


def click_text(page, pattern: str, timeout: int = 2500) -> bool:
    try:
        loc = page.get_by_text(re.compile(pattern, re.I)).first
        if loc.is_visible(timeout=timeout):
            loc.click(force=True)
            page.wait_for_timeout(1000)
            return True
    except Exception:
        pass
    try:
        btn = page.get_by_role("button", name=re.compile(pattern, re.I)).first
        if btn.is_visible(timeout=800):
            btn.click(force=True)
            page.wait_for_timeout(1000)
            return True
    except Exception:
        pass
    return False


def already_logged_in(page) -> bool:
    url = page.url.lower()
    if any(x in url for x in ("/foryou", "/following", "/friends", "/@")):
        # Profile icon / upload often present when logged in
        try:
            if page.locator('[data-e2e="nav-profile"], [data-e2e="top-login-button"]').count():
                login = page.locator('[data-e2e="top-login-button"]')
                if login.count() and login.first.is_visible():
                    return False
                return True
        except Exception:
            pass
    try:
        if page.locator('[data-e2e="top-login-button"]').count() and page.locator(
            '[data-e2e="top-login-button"]'
        ).first.is_visible():
            return False
    except Exception:
        pass
    # Avatar in top nav suggests logged in
    try:
        if page.locator('div[data-e2e="profile-icon"], a[href*="/@"]').count() > 0:
            if "login" not in url and "signup" not in url:
                return page.locator('[data-e2e="top-login-button"]').count() == 0
    except Exception:
        pass
    return False


def google_signup(page, context) -> bool:
    """Start Google OAuth from TikTok signup/login."""
    # Prefer Continue with Google
    for sel in (
        'div[data-e2e="channel-item"]:has-text("Google")',
        'div[data-e2e="channel-item"]',
    ):
        try:
            items = page.locator(sel)
            n = items.count()
            for i in range(n):
                t = items.nth(i).inner_text()
                if re.search(r"google", t, re.I):
                    with context.expect_page(timeout=15000) as popup_info:
                        items.nth(i).click(force=True)
                    popup = popup_info.value
                    popup.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(1500)
                    shot(popup, "01_google_popup")
                    return pick_google_account(popup, page)
        except Exception as e:
            print("google channel-item fail:", e)

    # Fallback: text match
    try:
        with context.expect_page(timeout=15000) as popup_info:
            if not click_text(page, r"Continue with Google|Sign up with Google|Google"):
                return False
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        shot(popup, "01_google_popup")
        return pick_google_account(popup, page)
    except Exception as e:
        print("google popup fail:", e)
        # Maybe same-tab redirect
        shot(page, "01_google_same_tab")
        return pick_google_account(page, page)


def pick_google_account(popup, main_page) -> bool:
    """Select benoats86@gmail.com if shown."""
    try:
        popup.wait_for_timeout(2000)
        # Account chooser
        acc = popup.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
        if acc.count():
            acc.first.click()
            popup.wait_for_timeout(3000)
        else:
            # Click first account row
            rows = popup.locator('[data-identifier], div[role="link"]')
            if rows.count():
                rows.first.click()
                popup.wait_for_timeout(3000)

        # Continue / Allow
        for label in (r"^Continue$", r"^Allow$", r"^Confirm$", r"Yes"):
            try:
                b = popup.get_by_role("button", name=re.compile(label, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    popup.wait_for_timeout(2500)
            except Exception:
                pass

        shot(popup, "02_after_google")
        main_page.wait_for_timeout(4000)
        shot(main_page, "03_back_on_tiktok")
        return True
    except Exception as e:
        print("pick account fail:", e)
        shot(popup, "02_google_error")
        return False


def fill_birthday(page) -> None:
    """TikTok often asks month/day/year."""
    shot(page, "04_birthday_check")
    # Try select elements
    try:
        selects = page.locator("select")
        if selects.count() >= 3:
            # Month, Day, Year — adult DOB placeholder (user can change later)
            # Use July 15, 1990 as safe adult default consistent with brand owner age band
            try:
                selects.nth(0).select_option(label=re.compile(r"July|Jul|7", re.I))
            except Exception:
                selects.nth(0).select_option(index=7)
            try:
                selects.nth(1).select_option(label="15")
            except Exception:
                selects.nth(1).select_option(index=15)
            try:
                selects.nth(2).select_option(label="1990")
            except Exception:
                # pick a mid option
                opts = selects.nth(2).locator("option")
                if opts.count() > 20:
                    selects.nth(2).select_option(index=min(25, opts.count() - 1))
            page.wait_for_timeout(500)
            click_text(page, r"^Next$|^Continue$")
            page.wait_for_timeout(2000)
    except Exception as e:
        print("birthday skip:", e)


def try_set_username(page, handle: str) -> bool:
    shot(page, f"05_username_{handle}")
    # Common username field
    candidates = [
        page.get_by_placeholder(re.compile(r"username|user name", re.I)),
        page.locator('input[name*="user" i]'),
        page.locator('input[autocomplete="username"]'),
        page.locator('input[type="text"]'),
    ]
    field = None
    for c in candidates:
        try:
            if c.count() and c.first.is_visible():
                field = c.first
                break
        except Exception:
            continue
    if not field:
        print("no username field for", handle)
        return False

    field.click(force=True)
    field.fill("")
    field.fill(handle)
    page.wait_for_timeout(2000)

    # Availability messaging
    body = page.inner_text("body")
    if re.search(r"already taken|not available|can.?t be used|unavailable", body, re.I):
        print("handle taken:", handle)
        return False

    if click_text(page, r"^Sign up$|^Continue$|^Next$|^Skip$|^Create$"):
        page.wait_for_timeout(3000)
        body2 = page.inner_text("body")
        if re.search(r"already taken|not available", body2, re.I):
            return False
        return True
    return True


def go_edit_profile(page) -> bool:
    # Direct edit profile URL patterns vary; try profile then Edit
    page.goto("https://www.tiktok.com/setting/profile", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    dismiss_cookies(page)
    shot(page, "10_settings_profile")

    if "login" in page.url.lower() or page.locator('[data-e2e="top-login-button"]').count():
        return False

    # Alternate: profile page
    if "setting" not in page.url:
        page.goto("https://www.tiktok.com/@OrbitWithBen", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

    click_text(page, r"^Edit profile$|^Edit$")
    page.wait_for_timeout(2000)
    shot(page, "11_edit_profile")
    return True


def apply_branding(page, handle: str) -> dict:
    out = {"handle": handle, "bio_set": False, "name_set": False, "avatar_set": False, "link_set": False}

    # Name / nickname
    for ph in (r"Name", r"Nickname", r"Display"):
        try:
            inp = page.get_by_placeholder(re.compile(ph, re.I))
            if inp.count() and inp.first.is_visible():
                inp.first.fill(DISPLAY)
                out["name_set"] = True
                break
        except Exception:
            pass
    if not out["name_set"]:
        try:
            # labeled inputs
            name_inp = page.locator('input[name*="nick" i], input[name*="name" i]').first
            if name_inp.is_visible():
                name_inp.fill(DISPLAY)
                out["name_set"] = True
        except Exception:
            pass

    # Bio
    try:
        bio = page.locator("textarea").first
        if bio.is_visible():
            bio.fill(BIO)
            out["bio_set"] = True
    except Exception:
        pass

    # Website / link
    try:
        link = page.get_by_placeholder(re.compile(r"website|link|url", re.I))
        if link.count() and link.first.is_visible():
            link.first.fill(WEBSITE)
            out["link_set"] = True
    except Exception:
        pass

    # Avatar upload
    try:
        file_inputs = page.locator('input[type="file"]')
        if file_inputs.count():
            file_inputs.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(2500)
            click_text(page, r"^Apply$|^Save$|^Confirm$|^Done$|^OK$")
            page.wait_for_timeout(2000)
            out["avatar_set"] = True
    except Exception as e:
        print("avatar upload:", e)

    click_text(page, r"^Save$|^Save changes$")
    page.wait_for_timeout(2500)
    shot(page, "12_branding_saved")
    return out


def extract_handle(page) -> str | None:
    m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
    if m:
        return m.group(1)
    try:
        # profile header
        h = page.locator('[data-e2e="user-title"], h1, h2').first.inner_text(timeout=2000)
        m2 = re.search(r"@([\w.]+)", h)
        if m2:
            return m2.group(1)
    except Exception:
        pass
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
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        dismiss_cookies(page)
        shot(page, "00_home")
        result["steps"].append("opened_home")

        logged_in = already_logged_in(page)
        result["steps"].append(f"logged_in_check={logged_in}")

        if not logged_in:
            page.goto("https://www.tiktok.com/signup", wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            dismiss_cookies(page)
            shot(page, "00b_signup")

            # Expand "Use phone / email / username" path sometimes hides Google —
            # but Google is usually visible on signup.
            if not google_signup(page, context):
                # Try login page
                page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                dismiss_cookies(page)
                shot(page, "00c_login")
                if not google_signup(page, context):
                    result["status"] = "needs_manual_google_auth"
                    result["notes"] = (
                        "Could not complete Google OAuth automatically. "
                        "Complete Continue with Google in the open browser, then re-run."
                    )
                    save_result(result)
                    print(json.dumps(result, indent=2))
                    print("Browser left open for manual Google sign-in (120s)...")
                    page.wait_for_timeout(120000)
                    # re-check
                    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                    if not already_logged_in(page):
                        result["status"] = "failed_not_logged_in"
                        save_result(result)
                        context.close()
                        return
                    result["steps"].append("manual_login_succeeded")

            fill_birthday(page)

            # Username step
            chosen = None
            for h in HANDLE_CANDIDATES:
                if try_set_username(page, h):
                    # confirm not still on username error
                    page.wait_for_timeout(1500)
                    body = page.inner_text("body")
                    if re.search(r"already taken|not available", body, re.I):
                        continue
                    chosen = h
                    break
            result["handle"] = chosen
            result["steps"].append(f"username_attempted={chosen}")

            # Skip interests / follows if shown
            for _ in range(4):
                if click_text(page, r"^Skip$|^Not now$|^Maybe later$"):
                    page.wait_for_timeout(1200)
                else:
                    break

        # Branding
        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "09_post_auth_home")

        if go_edit_profile(page):
            handle = result.get("handle") or extract_handle(page) or "OrbitWithBen"
            branding = apply_branding(page, handle)
            result["branding"] = branding
            result["handle"] = handle
            result["steps"].append("branding_applied")
        else:
            # Try navigating to me
            page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            shot(page, "10b_profile")
            handle = extract_handle(page)
            if handle:
                result["handle"] = handle
            click_text(page, r"^Edit profile$")
            page.wait_for_timeout(2000)
            if page.locator("textarea").count():
                branding = apply_branding(page, result.get("handle") or "unknown")
                result["branding"] = branding

        handle = result.get("handle") or extract_handle(page)
        if handle:
            result["handle"] = handle
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            page.goto(result["public_url"], wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            shot(page, "99_public_profile")
            result["status"] = "created_or_branded"
            result["notes"] = "TikTok profile reached; verify avatar/bio/link on public page."
        else:
            result["status"] = "partial"
            result["notes"] = "Logged in or mid-signup but handle not confirmed. Check audit screenshots."

        save_result(result)
        print(json.dumps(result, indent=2))
        page.wait_for_timeout(5000)
        context.close()


if __name__ == "__main__":
    main()
