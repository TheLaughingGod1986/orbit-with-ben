#!/usr/bin/env python3
"""Create Orbit with Ben TikTok — v2 (custom birthday UI + stay on signup flow)."""
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

HANDLES = [
    "OrbitWithBen",
    "OrbitWithBenYT",
    "MeetOrbit",
    "OrbitExplores",
    "HelloOrbit",
    "OrbitCosmos",
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)
    except Exception as e:
        print("shot fail", name, e)


def save(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        for k in ("handle", "public_url", "status", "created_at", "notes"):
            if data.get(k) is not None:
                meta[k] = data[k]
        META.write_text(json.dumps(meta, indent=2) + "\n")


def dismiss(page) -> None:
    for pat in (r"^Got it$", r"Accept all", r"Allow all", r"^Accept$"):
        try:
            b = page.get_by_role("button", name=re.compile(pat, re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1200)
                page.wait_for_timeout(600)
        except Exception:
            pass


def body_has(page, pat: str) -> bool:
    try:
        return bool(re.search(pat, page.inner_text("body"), re.I))
    except Exception:
        return False


def click_re(page, pat: str, role: str | None = "button") -> bool:
    try:
        if role:
            loc = page.get_by_role(role, name=re.compile(pat, re.I))
        else:
            loc = page.get_by_text(re.compile(pat, re.I))
        if loc.count() and loc.first.is_visible():
            loc.first.click(force=True)
            page.wait_for_timeout(900)
            return True
    except Exception:
        pass
    return False


def fill_birthday(page) -> bool:
    """TikTok uses custom div dropdowns, not <select>."""
    if not body_has(page, r"birthday|When.?s your birth"):
        return False
    shot(page, "v2_01_birthday")

    def pick(label: str, option: str) -> None:
        # Click the closed dropdown that shows the placeholder label
        box = page.locator("div").filter(has_text=re.compile(rf"^{label}$")).first
        # Prefer role combobox / visible Month Day Year tiles
        tiles = page.locator(f'text="{label}"')
        if tiles.count():
            tiles.first.click(force=True)
        else:
            box.click(force=True)
        page.wait_for_timeout(500)
        opt = page.get_by_text(option, exact=True)
        # Prefer visible option in list
        for i in range(opt.count()):
            try:
                if opt.nth(i).is_visible():
                    opt.nth(i).click(force=True)
                    page.wait_for_timeout(400)
                    return
            except Exception:
                continue
        page.locator(f'text="{option}"').first.click(force=True)
        page.wait_for_timeout(400)

    # Month / Day / Year placeholders
    try:
        pick("Month", "July")
    except Exception as e:
        print("month:", e)
        # fallback click sequence via data attributes
        try:
            page.locator('[aria-label="Month"], [id*="Month"]').first.click()
            page.get_by_text("July", exact=True).first.click()
        except Exception as e2:
            print("month2:", e2)

    try:
        pick("Day", "15")
    except Exception as e:
        print("day:", e)

    try:
        pick("Year", "1990")
    except Exception as e:
        print("year:", e)
        # scroll year list — click Year then type via keyboard
        try:
            page.get_by_text("Year", exact=True).first.click()
            page.wait_for_timeout(300)
            for _ in range(40):
                page.keyboard.press("ArrowDown")
            # try find 1990
            if page.get_by_text("1990", exact=True).count():
                page.get_by_text("1990", exact=True).first.click()
        except Exception as e2:
            print("year2:", e2)

    shot(page, "v2_02_birthday_filled")
    page.wait_for_timeout(500)
    if click_re(page, r"^Next$"):
        page.wait_for_timeout(2500)
        shot(page, "v2_03_after_birthday")
        return True
    return False


def continue_google(page, context) -> str:
    """Returns 'ok' | 'birthday' | 'fail'."""
    shot(page, "v2_00_signup")
    google = page.get_by_text(re.compile(r"Continue with Google", re.I))
    if not google.count():
        return "fail"

    popup = None
    try:
        with context.expect_page(timeout=20000) as pi:
            google.first.click(force=True)
        popup = pi.value
    except Exception:
        # same-tab or already progressed
        page.wait_for_timeout(3000)
        if body_has(page, r"birthday|When.?s your birth"):
            return "birthday"
        if body_has(page, r"username|Create nickname|Create a username"):
            return "ok"
        shot(page, "v2_00_no_popup")
        return "fail"

    popup.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    shot(popup, "v2_00_google")

    # Account chooser
    try:
        acc = popup.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
        if acc.count():
            acc.first.click()
            popup.wait_for_timeout(3000)
        else:
            # any account
            link = popup.locator("[data-email], [data-identifier]")
            if link.count():
                link.first.click()
                popup.wait_for_timeout(3000)
    except Exception as e:
        print("account:", e)

    for lab in (r"^Continue$", r"^Allow$", r"^Confirm$"):
        try:
            b = popup.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible():
                b.first.click()
                popup.wait_for_timeout(2000)
        except Exception:
            pass

    # Wait for popup close / redirect
    for _ in range(30):
        page.wait_for_timeout(1000)
        if body_has(page, r"birthday|When.?s your birth"):
            return "birthday"
        if body_has(page, r"username|Create nickname|Create a username|Sign up"):
            # still signup-ish
            if body_has(page, r"username|nickname"):
                return "ok"
        # logged in home?
        if "tiktok.com" in page.url and not body_has(page, r"Sign up for TikTok|Continue with Google"):
            if page.locator('[data-e2e="top-login-button"]').count() == 0:
                return "ok"
        try:
            if popup.is_closed():
                break
        except Exception:
            break

    page.wait_for_timeout(2000)
    shot(page, "v2_00_after_google")
    if body_has(page, r"birthday|When.?s your birth"):
        return "birthday"
    return "ok"


def set_username(page, handle: str) -> bool:
    shot(page, f"v2_04_user_{handle}")
    field = None
    for loc in (
        page.get_by_placeholder(re.compile(r"username|user name|nickname", re.I)),
        page.locator('input[name*="user" i]'),
        page.locator('input[type="text"]'),
    ):
        try:
            if loc.count() and loc.first.is_visible():
                field = loc.first
                break
        except Exception:
            continue
    if not field:
        print("no username field")
        return False

    field.click(force=True)
    field.fill("")
    field.fill(handle)
    page.wait_for_timeout(2200)
    if body_has(page, r"already taken|not available|can.?t be used"):
        print("taken:", handle)
        return False

    for lab in (r"^Sign up$", r"^Continue$", r"^Next$", r"^Create$"):
        if click_re(page, lab):
            page.wait_for_timeout(2500)
            break
    if body_has(page, r"already taken|not available"):
        return False
    shot(page, f"v2_05_user_ok_{handle}")
    return True


def skip_extras(page) -> None:
    for _ in range(6):
        if not click_re(page, r"^Skip$|^Not now$|^Maybe later$|^I.?ll do this later$"):
            break
        page.wait_for_timeout(1000)


def apply_brand(page) -> dict:
    out = {"name": False, "bio": False, "link": False, "avatar": False}
    shot(page, "v2_10_edit")

    # Name
    for loc in (
        page.get_by_placeholder(re.compile(r"Name|Nickname", re.I)),
        page.locator('input[name*="nick" i]'),
        page.locator('input[name*="name" i]'),
    ):
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.fill(DISPLAY)
                out["name"] = True
                break
        except Exception:
            pass

    try:
        ta = page.locator("textarea")
        if ta.count() and ta.first.is_visible():
            ta.first.fill(BIO)
            out["bio"] = True
    except Exception:
        pass

    try:
        link = page.get_by_placeholder(re.compile(r"website|link|url|bio link", re.I))
        if link.count() and link.first.is_visible():
            link.first.fill(WEBSITE)
            out["link"] = True
    except Exception:
        pass

    try:
        fi = page.locator('input[type="file"]')
        if fi.count():
            fi.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(3000)
            click_re(page, r"^Apply$|^Confirm$|^Done$|^Save$|^OK$")
            page.wait_for_timeout(1500)
            out["avatar"] = True
    except Exception as e:
        print("avatar:", e)

    click_re(page, r"^Save$|^Save changes$")
    page.wait_for_timeout(2500)
    shot(page, "v2_11_saved")
    return out


def extract_handle(page) -> str | None:
    m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
    if m:
        return m.group(1)
    try:
        t = page.locator('[data-e2e="user-title"]').first.inner_text(timeout=2000)
        m2 = re.search(r"@?([\w.]+)", t)
        if m2:
            return m2.group(1)
    except Exception:
        pass
    return None


def logged_in(page) -> bool:
    try:
        if page.locator('[data-e2e="top-login-button"]').count() and page.locator(
            '[data-e2e="top-login-button"]'
        ).first.is_visible():
            return False
    except Exception:
        pass
    # Profile nav without login CTA
    return "login" not in page.url.lower() and not body_has(page, r"Sign up for TikTok")


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
            slow_mo=80,
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.tiktok.com/signup", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        dismiss(page)

        # If already mid-flow on birthday
        state = "fresh"
        if body_has(page, r"When.?s your birth|birthday"):
            state = "birthday"
        elif logged_in(page):
            state = "logged_in"
        else:
            state = continue_google(page, context)
            result["steps"].append(f"google={state}")

        if state == "fail":
            # Manual assist window
            result["status"] = "needs_manual_google"
            result["notes"] = "Click Continue with Google in the open window. Script waits 3 min."
            save(result)
            print("Waiting 180s for manual Google login...")
            for i in range(36):
                page.wait_for_timeout(5000)
                if body_has(page, r"birthday|When.?s your birth"):
                    state = "birthday"
                    break
                if body_has(page, r"username|nickname"):
                    state = "ok"
                    break
                try:
                    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(1500)
                    if logged_in(page):
                        state = "logged_in"
                        break
                    page.goto("https://www.tiktok.com/signup", wait_until="domcontentloaded")
                    page.wait_for_timeout(1000)
                except Exception:
                    pass
            result["steps"].append(f"after_wait={state}")

        if state == "birthday":
            if fill_birthday(page):
                result["steps"].append("birthday_ok")
                state = "ok"
            else:
                result["steps"].append("birthday_fail")
                # leave browser for manual
                result["status"] = "needs_manual_birthday"
                save(result)
                print("Fill birthday manually — waiting 120s...")
                page.wait_for_timeout(120000)
                state = "ok"

        if state in ("ok", "fresh") and body_has(page, r"username|nickname|User name"):
            chosen = None
            for h in HANDLES:
                if set_username(page, h):
                    chosen = h
                    break
            result["handle"] = chosen
            result["steps"].append(f"username={chosen}")
            skip_extras(page)

        # Branding pass
        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        dismiss(page)
        shot(page, "v2_09_home")

        if not logged_in(page) and page.locator('[data-e2e="top-login-button"]').count():
            result["status"] = "not_logged_in"
            result["notes"] = "Signup did not complete — still seeing Log in. See audit/."
            save(result)
            print(json.dumps(result, indent=2))
            page.wait_for_timeout(8000)
            context.close()
            return

        # Open profile edit
        page.goto("https://www.tiktok.com/setting", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "v2_10_settings")
        if not click_re(page, r"Edit profile|Profile", role=None):
            page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            click_re(page, r"^Edit profile$")
            page.wait_for_timeout(2000)

        handle = result.get("handle") or extract_handle(page)
        branding = apply_brand(page)
        result["branding"] = branding

        if handle:
            result["handle"] = handle
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            page.goto(result["public_url"], wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            shot(page, "v2_99_public")

        result["status"] = "created_or_branded" if handle else "partial_logged_in"
        result["notes"] = "Verify public profile avatar, bio, and YT link."
        save(result)
        print(json.dumps(result, indent=2))
        page.wait_for_timeout(5000)
        context.close()


if __name__ == "__main__":
    main()
