#!/usr/bin/env python3
"""Keep QR login open until phone confirms, then brand Orbit TikTok."""
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
# Optional: if user already told us the handle
HINT = SETUP / "HANDLE_HINT.txt"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)
        print("shot", name, flush=True)
    except Exception as e:
        print("shot fail", name, e, flush=True)


def save(data: dict) -> None:
    RESULT.write_text(json.dumps(data, indent=2) + "\n")
    CREATE.write_text(json.dumps(data, indent=2) + "\n")
    if META.exists():
        meta = json.loads(META.read_text())
        meta.update(
            {
                "handle": data.get("handle"),
                "public_url": data.get("public_url"),
                "status": data.get("status"),
                "created_at": data.get("created_at"),
                "notes": data.get("notes"),
                "blocker": None,
                "next_step": None,
            }
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")


def is_logged_in(page) -> bool:
    try:
        top = page.locator('[data-e2e="top-login-button"]')
        if top.count() and top.first.is_visible():
            return False
    except Exception:
        pass
    try:
        btns = page.get_by_role("button", name=re.compile(r"^Log in$", re.I))
        for i in range(min(btns.count(), 4)):
            if btns.nth(i).is_visible():
                return False
    except Exception:
        pass
    # Logged-in: no Log in button + profile link or upload
    try:
        if page.locator('[data-e2e="nav-profile"]').count():
            return True
        # header avatar button
        if page.locator('button[aria-label*="Profile" i], div[data-e2e="profile-icon"]').count():
            return True
    except Exception:
        pass
    return False


def extract_handle(page) -> str | None:
    m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
    if m:
        return m.group(1)
    for sel in ('[data-e2e="user-title"]', '[data-e2e="user-subtitle"]', "h1", "h2"):
        try:
            t = page.locator(sel).first.inner_text(timeout=1200).strip()
            m2 = re.search(r"@([\w.]+)", t)
            if m2:
                return m2.group(1)
            if re.fullmatch(r"[\w.]+", t):
                return t
        except Exception:
            continue
    return None


def open_edit(page) -> bool:
    page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    shot(page, "v3_profile")
    for _ in range(3):
        try:
            b = page.get_by_role("button", name=re.compile(r"Edit profile", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True)
                page.wait_for_timeout(2500)
                shot(page, "v3_edit")
                return True
        except Exception:
            pass
        try:
            t = page.get_by_text(re.compile(r"^Edit profile$", re.I))
            if t.count():
                t.first.click(force=True)
                page.wait_for_timeout(2500)
                shot(page, "v3_edit")
                return True
        except Exception:
            pass
        page.wait_for_timeout(800)
    return False


def apply_brand(page) -> dict:
    out = {"name": False, "bio": False, "link": False, "avatar": False, "username": None}

    try:
        u = page.get_by_placeholder(re.compile(r"Username", re.I))
        if u.count() and u.first.is_visible():
            cur = u.first.input_value()
            out["username"] = cur
            if cur.lower() != "orbitwithben":
                u.first.fill("OrbitWithBen")
                page.wait_for_timeout(2000)
                if re.search(r"already taken|not available", page.inner_text("body"), re.I):
                    u.first.fill(cur)
                else:
                    out["username"] = "OrbitWithBen"
    except Exception as e:
        print("username", e)

    for loc in (
        page.get_by_placeholder(re.compile(r"^Name$|Nickname", re.I)),
        page.locator('input[placeholder*="Name" i]'),
    ):
        try:
            if loc.count() and loc.first.is_visible():
                loc.first.fill(DISPLAY)
                out["name"] = True
                break
        except Exception:
            pass

    try:
        if page.locator("textarea").count() and page.locator("textarea").first.is_visible():
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
            page.wait_for_timeout(3500)
            shot(page, "v3_avatar")
            for lab in (r"^Apply$", r"^Confirm$", r"^Done$", r"^Save$", r"^OK$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click(force=True)
                    page.wait_for_timeout(2000)
                    break
            out["avatar"] = True
    except Exception as e:
        print("avatar", e)

    shot(page, "v3_before_save")
    try:
        page.get_by_role("button", name=re.compile(r"^Save", re.I)).first.click(force=True)
        page.wait_for_timeout(3000)
    except Exception:
        pass
    shot(page, "v3_after_save")
    return out


def brand_flow(page, result: dict) -> dict:
    if not open_edit(page):
        result["status"] = "no_edit_profile"
        result["handle"] = extract_handle(page)
        if result["handle"]:
            result["public_url"] = f"https://www.tiktok.com/@{result['handle']}"
        result["notes"] = "Logged in but Edit profile missing"
        return result

    branding = apply_brand(page)
    result["branding"] = branding
    page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    handle = extract_handle(page) or branding.get("username")
    result["handle"] = handle
    if handle:
        result["public_url"] = f"https://www.tiktok.com/@{handle}"
        page.goto(result["public_url"], wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "v3_99_public")
        result["status"] = "branded"
        result["notes"] = f"Live at {result['public_url']} branding={branding}"
    else:
        result["status"] = "branded_unknown_handle"
        result["notes"] = str(branding)
    return result


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
            viewport={"width": 1100, "height": 860},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "v3_qr")

        print("=" * 64, flush=True)
        print("ACTION NEEDED — scan the QR on your Mac with TikTok:", flush=True)
        print("  1. Open TikTok on phone", flush=True)
        print("  2. Profile → ☰ → Settings and privacy → QR code", flush=True)
        print("     (or Profile → top scanner / camera → Scan)", flush=True)
        print("  3. Scan & Confirm login", flush=True)
        print("Waiting up to 5 minutes...", flush=True)
        print("=" * 64, flush=True)

        deadline = time.time() + 300
        n = 0
        logged = False
        while time.time() < deadline:
            try:
                n += 1
                page.wait_for_timeout(5000)
                if n % 4 == 1:
                    shot(page, f"v3_qr_{n}")
                # Check login via home peek every ~20s
                if n % 4 == 0:
                    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                    shot(page, f"v3_check_{n}")
                    if is_logged_in(page):
                        logged = True
                        break
                    page.goto(
                        "https://www.tiktok.com/login/qrcode",
                        wait_until="domcontentloaded",
                    )
                    page.wait_for_timeout(1500)
            except Exception as e:
                print("loop error (browser closed?):", e, flush=True)
                # relaunch context once
                try:
                    context.close()
                except Exception:
                    pass
                context = p.chromium.launch_persistent_context(
                    PROFILE,
                    headless=False,
                    viewport={"width": 1100, "height": 860},
                    args=["--disable-blink-features=AutomationControlled"],
                    ignore_default_args=["--enable-automation"],
                )
                page = context.pages[0] if context.pages else context.new_page()
                page.goto(
                    "https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded"
                )
                page.wait_for_timeout(2000)
                shot(page, "v3_qr_reopen")
                print("Browser reopened — scan the new QR", flush=True)

        if not logged:
            # hint file?
            if HINT.exists():
                hint = HINT.read_text().strip().lstrip("@")
                result["handle"] = hint
                result["public_url"] = f"https://www.tiktok.com/@{hint}"
                result["status"] = "awaiting_web_login"
                result["notes"] = (
                    f"Handle hint @{hint}. Web session not linked — brand on phone "
                    f"or scan QR and re-run."
                )
                save(result)
                print(json.dumps(result, indent=2), flush=True)
                context.close()
                return
            result["status"] = "awaiting_qr_scan"
            result["notes"] = "QR not scanned in time. Reply with @username or re-run after scanning."
            save(result)
            print(json.dumps(result, indent=2), flush=True)
            context.close()
            return

        result["steps"].append("logged_in")
        result = brand_flow(page, result)
        save(result)
        print(json.dumps(result, indent=2), flush=True)
        page.wait_for_timeout(5000)
        context.close()


if __name__ == "__main__":
    main()
