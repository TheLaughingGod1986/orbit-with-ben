#!/usr/bin/env python3
"""Finish Orbit TikTok signup on mobile web — click through email flow."""
from __future__ import annotations

import json
import re
import secrets
import string
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-tiktok-mobile-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AVATAR = SETUP / "avatar_800x800.png"
BIO = (SETUP / "bio.txt").read_text().strip()
WEBSITE = "https://www.youtube.com/@OrbitWithBen"
DISPLAY = "Orbit with Ben"
EMAIL = "benoats86@gmail.com"
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
        print("shot", name)
    except Exception as e:
        print("shot fail", name, e)


def save(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        for k in ("handle", "public_url", "status", "created_at", "notes"):
            if data.get(k) is not None:
                meta[k] = data[k]
        # never store password in meta
        META.write_text(json.dumps(meta, indent=2) + "\n")


def body(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def has(page, pat: str) -> bool:
    return bool(re.search(pat, body(page), re.I | re.S))


def click_next(page) -> bool:
    for pat in (r"^Next$", r"^Continue$", r"^Sign up$", r"^Submit$", r"^Create$"):
        try:
            btn = page.get_by_role("button", name=re.compile(pat, re.I))
            if btn.count():
                b = btn.first
                if b.is_visible() and b.is_enabled():
                    b.click(force=True)
                    page.wait_for_timeout(2000)
                    return True
                # try force even if disabled detection wrong
                try:
                    b.click(force=True, timeout=2000)
                    page.wait_for_timeout(2000)
                    return True
                except Exception:
                    pass
        except Exception:
            pass
    # CSS fallback — red Next
    try:
        page.locator("button").filter(has_text=re.compile(r"^Next$", re.I)).first.click(
            force=True
        )
        page.wait_for_timeout(2000)
        return True
    except Exception:
        return False


def pick_dropdown(page, placeholder: str, value: str) -> None:
    page.get_by_text(placeholder, exact=True).first.click(force=True)
    page.wait_for_timeout(400)
    page.get_by_text(value, exact=True).first.click(force=True)
    page.wait_for_timeout(350)


def fill_birthday(page) -> bool:
    if not has(page, r"birthday|When.?s your birth"):
        return False
    shot(page, "f_bday")
    pick_dropdown(page, "Month", "July")
    pick_dropdown(page, "Day", "15")
    pick_dropdown(page, "Year", "1990")
    shot(page, "f_bday_done")
    return click_next(page)


def set_username(page, handle: str) -> bool:
    shot(page, f"f_user_{handle}")
    inp = None
    for loc in (
        page.get_by_placeholder(re.compile(r"username|nickname|user name", re.I)),
        page.locator("input[type='text']"),
    ):
        if loc.count() and loc.first.is_visible():
            inp = loc.first
            break
    if not inp:
        return False
    inp.fill(handle)
    page.wait_for_timeout(2000)
    if has(page, r"already taken|not available|can.?t be used"):
        print("taken", handle)
        return False
    click_next(page)
    page.wait_for_timeout(1500)
    return not has(page, r"already taken|not available")


def apply_brand(page) -> dict:
    out = {"name": False, "bio": False, "avatar": False, "link": False}
    shot(page, "f_edit")
    try:
        for loc in (
            page.get_by_placeholder(re.compile(r"Name|Nickname", re.I)),
            page.locator("input").first,
        ):
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
            page.get_by_role("button", name=re.compile(r"Apply|Confirm|Done|Save", re.I)).first.click(
                force=True
            )
            out["avatar"] = True
    except Exception as e:
        print("avatar", e)
    try:
        page.get_by_role("button", name=re.compile(r"^Save", re.I)).first.click(force=True)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    shot(page, "f_branded")
    return out


def wait_for_code_or_progress(page, seconds: int = 240) -> str:
    """Wait while user enters email/SMS code. Returns state tag."""
    print(f"Waiting up to {seconds}s for verification / next step...")
    print("If TikTok emailed a code to benoats86@gmail.com, enter it in the browser.")
    deadline = time.time() + seconds
    while time.time() < deadline:
        page.wait_for_timeout(5000)
        b = body(page)
        if re.search(r"username|nickname|Create a username", b, re.I):
            return "username"
        if re.search(r"password|Create password", b, re.I):
            return "password"
        if re.search(r"Edit profile|For You|Following", b, re.I) and not re.search(
            r"Sign up", b, re.I
        ):
            return "done"
        if re.search(r"incorrect|invalid code|try again", b, re.I):
            shot(page, "f_code_error")
        # still on code?
        if re.search(r"code|6.digit|verification", b, re.I):
            continue
    return "timeout"


def main() -> None:
    result = {
        "status": "started",
        "display_name": DISPLAY,
        "bio": BIO,
        "website": WEBSITE,
        "email": EMAIL,
        "handle": None,
        "public_url": None,
        "created_at": time.strftime("%Y-%m-%d"),
        "steps": [],
        "mode": "mobile_email_flow",
    }
    AUDIT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            **IPHONE,
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            slow_mo=50,
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto(
            "https://www.tiktok.com/signup/phone-or-email/email",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(2000)
        shot(page, "f_00")

        # Birthday gate first (sometimes)
        if has(page, r"birthday|When.?s your birth"):
            fill_birthday(page)
            result["steps"].append("birthday")
            page.wait_for_timeout(1500)
            # may land on phone/email chooser
            if has(page, r"Email") and not has(page, r"Email address|benoats"):
                try:
                    page.get_by_text("Email", exact=True).first.click()
                    page.wait_for_timeout(1000)
                except Exception:
                    page.goto(
                        "https://www.tiktok.com/signup/phone-or-email/email",
                        wait_until="domcontentloaded",
                    )
                    page.wait_for_timeout(1500)

        # Email field
        email_inp = page.locator(
            'input[type="email"], input[placeholder*="Email" i], input[name*="email" i]'
        )
        if not email_inp.count():
            email_inp = page.locator("input").first

        email_inp.first.click(force=True)
        email_inp.first.fill("")
        email_inp.first.fill(EMAIL)
        page.wait_for_timeout(800)
        shot(page, "f_01_email")
        result["steps"].append("email_filled")

        if not click_next(page):
            result["status"] = "next_failed"
            result["notes"] = "Could not click Next on email step"
            save(result)
            print(json.dumps(result, indent=2))
            page.wait_for_timeout(30000)
            context.close()
            return
        result["steps"].append("email_next")
        page.wait_for_timeout(2000)
        shot(page, "f_02_after_email")

        # Password step
        if has(page, r"password|Create password"):
            alphabet = string.ascii_letters + string.digits + "!@#$%"
            password = "Orbit!" + "".join(secrets.choice(alphabet) for _ in range(12))
            pw = page.locator('input[type="password"]')
            if pw.count():
                pw.first.fill(password)
                page.wait_for_timeout(500)
                if pw.count() > 1:
                    pw.nth(1).fill(password)
                shot(page, "f_03_password")
                click_next(page)
                result["steps"].append("password_set")
                pw_file = SETUP / ".tiktok_password_local.txt"
                pw_file.write_text(
                    f"email={EMAIL}\npassword={password}\n"
                    "Change this password after first login.\n"
                )
                pw_file.chmod(0o600)
                page.wait_for_timeout(2000)
                shot(page, "f_04_after_password")

        # Verification code
        if has(page, r"code|Enter.*digit|verification|sent.*email|sent.*code"):
            shot(page, "f_05_code")
            result["steps"].append("awaiting_code")
            result["status"] = "awaiting_email_code"
            result["notes"] = (
                "Enter the 6-digit code from benoats86@gmail.com in the open TikTok window."
            )
            save(result)
            state = wait_for_code_or_progress(page, 300)
            result["steps"].append(f"after_code={state}")
            shot(page, "f_06_after_code")
        else:
            state = "unknown"
            if has(page, r"username|nickname"):
                state = "username"
            elif has(page, r"password"):
                state = "password"

        # Maybe birthday after email
        if has(page, r"birthday|When.?s your birth"):
            fill_birthday(page)
            result["steps"].append("birthday_late")

        # Username
        chosen = None
        if has(page, r"username|nickname|User name") or state == "username":
            for h in HANDLES:
                if set_username(page, h):
                    chosen = h
                    break
            result["handle"] = chosen
            result["steps"].append(f"username={chosen}")
            shot(page, "f_07_username")

        for _ in range(6):
            try:
                b = page.get_by_role(
                    "button", name=re.compile(r"^Skip$|^Not now$|^Maybe later$", re.I)
                )
                if b.count() and b.first.is_visible():
                    b.first.click(force=True)
                    page.wait_for_timeout(1000)
                else:
                    break
            except Exception:
                break

        page.wait_for_timeout(2000)
        shot(page, "f_08_homeish")

        # Brand
        for url in (
            "https://www.tiktok.com/profile",
            "https://m.tiktok.com/profile",
        ):
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            if has(page, r"Edit profile|Edit"):
                break

        try:
            page.get_by_text(re.compile(r"^Edit profile$|^Edit$", re.I)).first.click(
                force=True
            )
            page.wait_for_timeout(1500)
            result["branding"] = apply_brand(page)
        except Exception as e:
            result["steps"].append(f"brand_skip={e}")

        handle = result.get("handle")
        if handle:
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            page.goto(result["public_url"], wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            shot(page, "f_99_public")
            result["status"] = "created"
            result["notes"] = (
                "Account created. Verify avatar/bio. "
                "Password in .tiktok_password_local.txt — change after login."
            )
        elif has(page, r"code|verification"):
            result["status"] = "awaiting_email_code"
            result["notes"] = "Stopped on verification — enter code from Gmail, then re-run branding."
        else:
            result["status"] = "partial"
            result["notes"] = "See audit/f_*.png — complete any remaining step in the open browser."

        save(result)
        print(json.dumps(result, indent=2))
        # Keep open briefly
        page.wait_for_timeout(15000)
        context.close()


if __name__ == "__main__":
    main()
