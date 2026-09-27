#!/usr/bin/env python3
"""Create Orbit TikTok via mobile-emulated Chromium (web signup is app-walled)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Fresh profile — mobile UA; don't reuse desktop youtube profile cookies that may force app wall
PROFILE = "/Users/ben/code/youtube/.playwright-tiktok-mobile-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AVATAR = SETUP / "avatar_800x800.png"
BIO = (SETUP / "bio.txt").read_text().strip()
WEBSITE = "https://www.youtube.com/@OrbitWithBen"
DISPLAY = "Orbit with Ben"
AUDIT = SETUP / "audit"
RESULT = SETUP / "CREATE_RESULT.json"
META = SETUP / "TIKTOK_META.json"
GOOGLE_PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"

HANDLES = [
    "OrbitWithBen",
    "OrbitWithBenYT",
    "MeetOrbit",
    "OrbitExplores",
    "HelloOrbit",
    "OrbitCosmos",
]

IPHONE = {
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1"
    ),
    "viewport": {"width": 390, "height": 844},
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)
    except Exception as e:
        print("shot", name, e)


def save(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        for k in ("handle", "public_url", "status", "created_at", "notes"):
            if data.get(k) is not None:
                meta[k] = data[k]
        META.write_text(json.dumps(meta, indent=2) + "\n")


def body_has(page, pat: str) -> bool:
    try:
        return bool(re.search(pat, page.inner_text("body"), re.I | re.S))
    except Exception:
        return False


def click_re(page, pat: str, role: str | None = "button") -> bool:
    try:
        loc = (
            page.get_by_role(role, name=re.compile(pat, re.I))
            if role
            else page.get_by_text(re.compile(pat, re.I))
        )
        if loc.count() and loc.first.is_visible():
            loc.first.click(force=True)
            page.wait_for_timeout(800)
            return True
    except Exception:
        pass
    return False


def dismiss(page) -> None:
    for pat in (r"^Got it$", r"Accept all", r"Allow all", r"^Accept$", r"^Close$"):
        click_re(page, pat)


def fill_birthday(page) -> bool:
    if not body_has(page, r"birthday|When.?s your birth"):
        return False
    shot(page, "m_01_birthday")

    def pick(placeholder: str, value: str) -> None:
        page.get_by_text(placeholder, exact=True).first.click(force=True)
        page.wait_for_timeout(400)
        page.get_by_text(value, exact=True).first.click(force=True)
        page.wait_for_timeout(350)

    pick("Month", "July")
    pick("Day", "15")
    pick("Year", "1990")
    shot(page, "m_02_bday_filled")
    if click_re(page, r"^Next$"):
        page.wait_for_timeout(2500)
        shot(page, "m_03_after_bday")
        return True
    return False


def set_username(page, handle: str) -> bool:
    shot(page, f"m_04_{handle}")
    field = None
    for loc in (
        page.get_by_placeholder(re.compile(r"username|nickname|user name", re.I)),
        page.locator("input[type='text']"),
    ):
        if loc.count() and loc.first.is_visible():
            field = loc.first
            break
    if not field:
        return False
    field.fill(handle)
    page.wait_for_timeout(2000)
    if body_has(page, r"already taken|not available|can.?t be used"):
        return False
    for lab in (r"^Sign up$", r"^Continue$", r"^Next$", r"^Create$"):
        if click_re(page, lab):
            page.wait_for_timeout(2500)
            break
    return not body_has(page, r"already taken|not available")


def apply_brand(page) -> dict:
    out = {"name": False, "bio": False, "avatar": False, "link": False}
    for loc in (
        page.get_by_placeholder(re.compile(r"Name|Nickname", re.I)),
        page.locator("input").nth(0),
    ):
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.fill(DISPLAY)
                out["name"] = True
                break
        except Exception:
            pass
    try:
        if page.locator("textarea").count():
            page.locator("textarea").first.fill(BIO)
            out["bio"] = True
    except Exception:
        pass
    try:
        link = page.get_by_placeholder(re.compile(r"website|link|url", re.I))
        if link.count() and link.first.is_visible():
            link.first.fill(WEBSITE)
            out["link"] = True
    except Exception:
        pass
    try:
        fi = page.locator('input[type="file"]')
        if fi.count():
            fi.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(2500)
            click_re(page, r"^Apply$|^Confirm$|^Done$|^Save$")
            out["avatar"] = True
    except Exception as e:
        print("avatar", e)
    click_re(page, r"^Save$|^Save changes$")
    page.wait_for_timeout(2000)
    shot(page, "m_11_brand")
    return out


def google_via_desktop_then_transfer() -> None:
    """Not used — kept as note: mobile Google OAuth is preferred."""
    pass


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
        "mode": "mobile_emulation",
    }
    AUDIT.mkdir(parents=True, exist_ok=True)
    Path(PROFILE).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Copy Google cookies from youtube profile into mobile context for SSO
        desktop = p.chromium.launch_persistent_context(
            GOOGLE_PROFILE,
            headless=True,
            viewport={"width": 1280, "height": 800},
        )
        google_cookies = []
        try:
            google_cookies = [
                c
                for c in desktop.cookies()
                if any(d in (c.get("domain") or "") for d in ("google.", "youtube.", "tiktok."))
            ]
        finally:
            desktop.close()

        context = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            **IPHONE,
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            slow_mo=60,
        )
        if google_cookies:
            try:
                context.add_cookies(google_cookies)
                result["steps"].append(f"cookies={len(google_cookies)}")
            except Exception as e:
                result["steps"].append(f"cookie_fail={e}")

        page = context.pages[0] if context.pages else context.new_page()

        # Mobile signup entry
        for url in (
            "https://www.tiktok.com/signup/phone-or-email/email",
            "https://www.tiktok.com/signup",
            "https://m.tiktok.com/signup",
        ):
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            dismiss(page)
            shot(page, "m_00_entry")
            result["steps"].append(f"open={url}")
            if body_has(page, r"Continue on the TikTok app|Scan this QR"):
                result["steps"].append("app_wall")
                continue
            break

        shot(page, "m_00_current")

        # If app wall still — save QR path for user and also try login/google
        if body_has(page, r"Continue on the TikTok app|Scan this QR"):
            result["status"] = "app_wall_mobile_too"
            result["notes"] = (
                "TikTok requires the mobile app to finish signup. "
                "Scan the QR on phone, create @OrbitWithBen, then re-run branding."
            )
            save(result)
            print(json.dumps(result, indent=2))
            print("Leaving browser open 3 min for QR scan / manual app signup...")
            page.wait_for_timeout(180000)
            context.close()
            return

        # Birthday?
        if body_has(page, r"birthday|When.?s your birth"):
            fill_birthday(page)
            result["steps"].append("birthday")

        # Choose email or Google
        if body_has(page, r"Continue with Google|Google"):
            google = page.get_by_text(re.compile(r"Continue with Google|Google", re.I))
            try:
                with context.expect_page(timeout=20000) as pi:
                    google.first.click(force=True)
                pop = pi.value
                pop.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(1500)
                shot(pop, "m_00_google")
                acc = pop.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
                if acc.count():
                    acc.first.click()
                    pop.wait_for_timeout(4000)
                for lab in (r"^Continue$", r"^Allow$"):
                    b = pop.get_by_role("button", name=re.compile(lab, re.I))
                    if b.count() and b.first.is_visible():
                        b.first.click()
                        pop.wait_for_timeout(2000)
                result["steps"].append("google_clicked")
            except Exception as e:
                result["steps"].append(f"google_err={e}")
                google.first.click(force=True)
                page.wait_for_timeout(5000)

        page.wait_for_timeout(3000)
        if body_has(page, r"birthday|When.?s your birth"):
            fill_birthday(page)

        # Email path if present
        if body_has(page, r"email|Phone") and page.locator("input").count():
            # Prefer email signup with gmail — user may need to verify
            try:
                if click_re(page, r"email|Email", role=None) or True:
                    email_inp = page.locator('input[type="email"], input[name*="email" i]')
                    if email_inp.count():
                        email_inp.first.fill("benoats86@gmail.com")
                        result["steps"].append("email_filled")
                        shot(page, "m_05_email")
                        print(
                            "Email entered. If TikTok asks for a code, check Gmail. Waiting 180s..."
                        )
                        page.wait_for_timeout(180000)
            except Exception as e:
                result["steps"].append(f"email_err={e}")

        # Username
        chosen = None
        if body_has(page, r"username|nickname|User name"):
            for h in HANDLES:
                if set_username(page, h):
                    chosen = h
                    break
            result["handle"] = chosen
            result["steps"].append(f"user={chosen}")

        for _ in range(5):
            if not click_re(page, r"^Skip$|^Not now$|^Maybe later$"):
                break

        page.wait_for_timeout(2000)
        shot(page, "m_09_post")

        # Try profile
        for url in (
            "https://www.tiktok.com/profile",
            "https://m.tiktok.com/profile",
            f"https://www.tiktok.com/@{chosen}" if chosen else "https://www.tiktok.com/",
        ):
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
            except Exception:
                continue

        if click_re(page, r"^Edit profile$|^Edit$"):
            page.wait_for_timeout(1500)
            result["branding"] = apply_brand(page)

        handle = result.get("handle")
        if handle:
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            result["status"] = "created_or_branded"
        elif body_has(page, r"Log in") and page.locator('text="Log in"').count():
            result["status"] = "incomplete"
            result["notes"] = (
                "Could not finish on mobile web. Use phone: install TikTok → "
                "sign up with Google (benoats86@gmail.com) → username OrbitWithBen → "
                "upload avatar from Channel-Setup/TikTok/avatar_800x800.png → paste bio.txt"
            )
        else:
            result["status"] = "partial"
            result["notes"] = "Check audit screenshots; may need phone verification."

        save(result)
        print(json.dumps(result, indent=2))
        page.wait_for_timeout(5000)
        context.close()


if __name__ == "__main__":
    main()
