#!/usr/bin/env python3
"""Apply Orbit branding to an already-logged-in TikTok account (mobile profile)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-tiktok-mobile-profile"
DESKTOP_PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
SETUP = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AVATAR = SETUP / "avatar_800x800.png"
BIO = (SETUP / "bio.txt").read_text().strip()
WEBSITE = "https://www.youtube.com/@OrbitWithBen"
DISPLAY = "Orbit with Ben"
AUDIT = SETUP / "audit"
RESULT = SETUP / "BRAND_RESULT.json"
META = SETUP / "TIKTOK_META.json"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def main() -> None:
    result = {"status": "started", "created_at": time.strftime("%Y-%m-%d")}
    with sync_playwright() as p:
        # Prefer desktop profile if user logged in there after app signup
        for profile, mobile in (
            (DESKTOP_PROFILE, False),
            (PROFILE, True),
        ):
            kwargs = {
                "headless": False,
                "args": ["--disable-blink-features=AutomationControlled"],
                "ignore_default_args": ["--enable-automation"],
            }
            if mobile:
                kwargs.update(
                    {
                        "user_agent": (
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                            "Mobile/15E148 Safari/604.1"
                        ),
                        "viewport": {"width": 390, "height": 844},
                        "is_mobile": True,
                        "has_touch": True,
                        "device_scale_factor": 3,
                    }
                )
            else:
                kwargs["viewport"] = {"width": 1280, "height": 900}

            context = p.chromium.launch_persistent_context(profile, **kwargs)
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            shot(page, "brand_00_profile")
            body = page.inner_text("body")
            if re.search(r"Log in", body, re.I) and page.locator(
                '[data-e2e="top-login-button"]'
            ).count():
                print("Not logged in on", profile)
                context.close()
                continue

            # Edit profile
            try:
                page.get_by_text(re.compile(r"^Edit profile$", re.I)).first.click(force=True)
            except Exception:
                page.goto("https://www.tiktok.com/setting", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                page.get_by_text(re.compile(r"Edit profile|Profile", re.I)).first.click(
                    force=True
                )
            page.wait_for_timeout(2000)
            shot(page, "brand_01_edit")

            # Name
            for loc in (
                page.get_by_placeholder(re.compile(r"Name|Nickname", re.I)),
                page.locator('input[name*="nick" i]'),
            ):
                if loc.count() and loc.first.is_visible():
                    loc.first.fill(DISPLAY)
                    break

            if page.locator("textarea").count():
                page.locator("textarea").first.fill(BIO)

            link = page.get_by_placeholder(re.compile(r"website|link|url", re.I))
            if link.count() and link.first.is_visible():
                link.first.fill(WEBSITE)

            fi = page.locator('input[type="file"]')
            if fi.count():
                fi.first.set_input_files(str(AVATAR))
                page.wait_for_timeout(3000)
                try:
                    page.get_by_role(
                        "button", name=re.compile(r"Apply|Confirm|Done|Save", re.I)
                    ).first.click(force=True)
                except Exception:
                    pass

            try:
                page.get_by_role("button", name=re.compile(r"^Save", re.I)).first.click(
                    force=True
                )
            except Exception:
                pass
            page.wait_for_timeout(2500)
            shot(page, "brand_02_saved")

            m = re.search(r"tiktok\.com/@([\w.]+)", page.url)
            handle = m.group(1) if m else None
            if not handle:
                try:
                    t = page.locator('[data-e2e="user-title"]').inner_text(timeout=2000)
                    m2 = re.search(r"@?([\w.]+)", t)
                    handle = m2.group(1) if m2 else None
                except Exception:
                    pass

            result.update(
                {
                    "status": "branded",
                    "handle": handle,
                    "public_url": f"https://www.tiktok.com/@{handle}" if handle else None,
                    "display_name": DISPLAY,
                    "bio": BIO,
                    "website": WEBSITE,
                }
            )
            if handle:
                page.goto(result["public_url"], wait_until="domcontentloaded")
                page.wait_for_timeout(2500)
                shot(page, "brand_99_public")

            RESULT.write_text(json.dumps(result, indent=2) + "\n")
            if META.exists():
                meta = json.loads(META.read_text())
                meta.update(
                    {
                        "handle": handle,
                        "public_url": result.get("public_url"),
                        "status": "branded",
                        "created_at": result["created_at"],
                    }
                )
                META.write_text(json.dumps(meta, indent=2) + "\n")

            print(json.dumps(result, indent=2))
            page.wait_for_timeout(5000)
            context.close()
            return

        result["status"] = "not_logged_in"
        result["notes"] = "Log into TikTok in the browser profile first, then re-run."
        RESULT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
