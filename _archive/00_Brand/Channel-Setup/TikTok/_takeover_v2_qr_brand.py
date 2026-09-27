#!/usr/bin/env python3
"""QR-login to phone TikTok session, then apply Orbit branding."""
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


def body(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def is_logged_in(page) -> bool:
    """Strict: Log in CTA means logged out."""
    try:
        top = page.locator('[data-e2e="top-login-button"]')
        if top.count() and top.first.is_visible():
            return False
    except Exception:
        pass
    try:
        # Sidebar / header Log in buttons
        for loc in (
            page.get_by_role("button", name=re.compile(r"^Log in$", re.I)),
            page.locator('button:has-text("Log in")'),
        ):
            if loc.count():
                for i in range(min(loc.count(), 3)):
                    if loc.nth(i).is_visible():
                        return False
    except Exception:
        pass
    # Positive signals
    try:
        if page.locator('[data-e2e="nav-profile"]').count():
            return True
    except Exception:
        pass
    # Messages / upload inbox when authed
    if "/login" in page.url.lower():
        return False
    return False


def wait_qr_login(page, context, seconds: int = 180) -> bool:
    # Prefer dedicated QR login
    for url in (
        "https://www.tiktok.com/login/qrcode",
        "https://www.tiktok.com/login",
    ):
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        shot(page, "qr_00")
        # Click Use QR code if on combined login
        try:
            page.get_by_text(re.compile(r"Use QR code|QR code", re.I)).first.click(
                timeout=2000
            )
            page.wait_for_timeout(1500)
        except Exception:
            pass
        shot(page, "qr_01")
        if page.locator("canvas, img[alt*='QR' i], [class*='qr' i]").count() or re.search(
            r"QR|scan", body(page), re.I
        ):
            break

    print("=" * 60)
    print("SCAN THIS QR with your TikTok phone app:")
    print("  TikTok → Profile → ☰ menu → Settings → QR code  OR")
    print("  Open TikTok camera / scan from Profile → Scan")
    print(f"Waiting up to {seconds}s...")
    print("=" * 60)

    deadline = time.time() + seconds
    n = 0
    while time.time() < deadline:
        page.wait_for_timeout(4000)
        n += 1
        # Refresh QR screenshot periodically
        if n % 5 == 1:
            shot(page, f"qr_wait_{n}")
        # Check if redirected / logged in
        try:
            # Sometimes stays on login until refresh
            if is_logged_in(page):
                return True
            # Peek home without leaving QR too often
            if n % 3 == 0:
                cur = page.url
                page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                shot(page, f"qr_check_{n}")
                if is_logged_in(page):
                    return True
                # go back to QR if still out
                page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
        except Exception as e:
            print("poll", e)
    return False


def google_login(page, context) -> bool:
    page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    shot(page, "g_00")
    google = page.get_by_text(re.compile(r"Continue with Google", re.I))
    if not google.count():
        return False
    try:
        with context.expect_page(timeout=20000) as pi:
            google.first.click(force=True)
        pop = pi.value
    except Exception:
        return False
    pop.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    shot(pop, "g_01")
    try:
        acc = pop.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
        if acc.count():
            acc.first.click()
            pop.wait_for_timeout(4000)
        for lab in (r"^Continue$", r"^Allow$"):
            b = pop.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible():
                b.first.click()
                pop.wait_for_timeout(2000)
    except Exception as e:
        print("google", e)
    page.wait_for_timeout(4000)
    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    shot(page, "g_02")
    return is_logged_in(page)


def extract_handle(page) -> str | None:
    m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
    if m:
        return m.group(1)
    for sel in ('[data-e2e="user-title"]', '[data-e2e="user-subtitle"]', "h1", "h2"):
        try:
            t = page.locator(sel).first.inner_text(timeout=1500).strip()
            m2 = re.search(r"@([\w.]+)", t)
            if m2:
                return m2.group(1)
            if re.fullmatch(r"[\w.]+", t):
                return t
        except Exception:
            continue
    try:
        hrefs = page.eval_on_selector_all(
            'a[href*="/@"]', "els => els.map(e => e.getAttribute('href'))"
        )
        for h in hrefs or []:
            m3 = re.search(r"/@([\w.]+)", h or "")
            if m3:
                return m3.group(1)
    except Exception:
        pass
    return None


def open_edit(page) -> bool:
    page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    shot(page, "ed_00_profile")
    handle = extract_handle(page)
    print("profile handle guess:", handle)

    for attempt in range(3):
        try:
            loc = page.get_by_role("button", name=re.compile(r"Edit profile", re.I))
            if loc.count() and loc.first.is_visible():
                loc.first.click(force=True)
                page.wait_for_timeout(2500)
                shot(page, "ed_01")
                return True
        except Exception:
            pass
        try:
            loc = page.get_by_text(re.compile(r"^Edit profile$", re.I))
            if loc.count():
                loc.first.click(force=True)
                page.wait_for_timeout(2500)
                shot(page, "ed_01")
                return True
        except Exception:
            pass
        page.wait_for_timeout(1000)

    # Direct settings
    page.goto("https://www.tiktok.com/setting/profile", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    shot(page, "ed_02_settings")
    if page.locator("textarea").count() or page.locator('input[type="file"]').count():
        return True
    return False


def apply_brand(page) -> dict:
    out = {"name": False, "bio": False, "link": False, "avatar": False, "username": None}

    # Username if editable
    try:
        u = page.get_by_placeholder(re.compile(r"Username", re.I))
        if u.count() and u.first.is_visible():
            cur = u.first.input_value()
            out["username"] = cur
            if cur.lower() != "orbitwithben":
                u.first.fill("OrbitWithBen")
                page.wait_for_timeout(2000)
                if re.search(r"already taken|not available", body(page), re.I):
                    print("OrbitWithBen taken — keeping", cur)
                    u.first.fill(cur)
                else:
                    out["username"] = "OrbitWithBen"
    except Exception as e:
        print("user", e)

    # Name
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

    # Bio
    try:
        ta = page.locator("textarea")
        if ta.count() and ta.first.is_visible():
            ta.first.fill(BIO)
            out["bio"] = True
    except Exception:
        pass

    # Link
    try:
        link = page.get_by_placeholder(re.compile(r"website|link|url", re.I))
        if link.count() and link.first.is_visible():
            link.first.fill(WEBSITE)
            out["link"] = True
        else:
            add = page.get_by_text(re.compile(r"Add (a )?link|Website|Bio link", re.I))
            if add.count() and add.first.is_visible():
                add.first.click()
                page.wait_for_timeout(800)
                page.locator("input").last.fill(WEBSITE)
                out["link"] = True
    except Exception as e:
        print("link", e)

    # Avatar
    try:
        fi = page.locator('input[type="file"]')
        if fi.count():
            fi.first.set_input_files(str(AVATAR))
            page.wait_for_timeout(3500)
            shot(page, "ed_avatar")
            for lab in (r"^Apply$", r"^Confirm$", r"^Done$", r"^Save$", r"^OK$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click(force=True)
                    page.wait_for_timeout(2000)
                    break
            out["avatar"] = True
        else:
            # click change photo + file chooser
            for pat in (r"Change photo", r"Upload photo", r"Select photo", r"Edit"):
                t = page.get_by_text(re.compile(pat, re.I))
                if t.count() and t.first.is_visible():
                    try:
                        with page.expect_file_chooser(timeout=4000) as fc:
                            t.first.click()
                        fc.value.set_files(str(AVATAR))
                        page.wait_for_timeout(3000)
                        out["avatar"] = True
                        break
                    except Exception:
                        continue
    except Exception as e:
        print("avatar", e)

    shot(page, "ed_before_save")
    for lab in (r"^Save$", r"^Save changes$"):
        try:
            b = page.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible():
                # may be disabled until change
                b.first.click(force=True)
                page.wait_for_timeout(3000)
                break
        except Exception:
            pass
    shot(page, "ed_after_save")
    return out


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
            slow_mo=50,
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "t2_home")

        if not is_logged_in(page):
            # Try Google first (same account as phone signup)
            if google_login(page, context):
                result["steps"].append("google_ok")
            elif wait_qr_login(page, context, seconds=180):
                result["steps"].append("qr_ok")
            else:
                result["status"] = "awaiting_login"
                result["notes"] = (
                    "Could not link desktop session. On phone TikTok: "
                    "Profile → ☰ → Settings and privacy → Security → "
                    "manage QR / or Log in on the open browser with Google."
                )
                save(result)
                print(json.dumps(result, indent=2))
                # leave browser open a bit longer
                page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded")
                shot(page, "t2_final_qr")
                page.wait_for_timeout(60000)
                if not is_logged_in(page):
                    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                if not is_logged_in(page):
                    context.close()
                    return
                result["steps"].append("late_login")

        result["steps"].append("logged_in")
        shot(page, "t2_authed")

        if not open_edit(page):
            result["status"] = "no_edit_profile"
            result["notes"] = "Logged in but Edit profile not found. See audit/ed_*.png"
            # still try to capture handle
            page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            result["handle"] = extract_handle(page)
            if result["handle"]:
                result["public_url"] = f"https://www.tiktok.com/@{result['handle']}"
            save(result)
            print(json.dumps(result, indent=2))
            page.wait_for_timeout(10000)
            context.close()
            return

        branding = apply_brand(page)
        result["branding"] = branding
        result["steps"].append("branded")

        page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        handle = extract_handle(page) or branding.get("username")
        result["handle"] = handle
        if handle:
            result["public_url"] = f"https://www.tiktok.com/@{handle}"
            page.goto(result["public_url"], wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            shot(page, "t2_99_public")
            result["status"] = "branded"
            result["notes"] = f"Live at {result['public_url']}"
        else:
            result["status"] = "branded_unknown_handle"
            result["notes"] = f"Branding={branding}"

        save(result)
        print(json.dumps(result, indent=2))
        page.wait_for_timeout(8000)
        context.close()


if __name__ == "__main__":
    main()
