#!/usr/bin/env python3
"""Create / configure Orbit TikTok Developer app for Content Ops OAuth."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
OUT = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AUDIT = OUT / "audit"
RESULT = OUT / "TIKTOK_DEV_APP.json"
REDIRECT = "http://localhost:3000/api/oauth/tiktok/callback"
APP_NAME = "Orbit Content Ops"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"dev_{name}.png"), full_page=False)
        print("shot", name, flush=True)
    except Exception as e:
        print("shot fail", name, e, flush=True)


def main() -> None:
    result: dict = {"status": "started", "redirect": REDIRECT, "app_name": APP_NAME}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            slow_mo=50,
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://developers.tiktok.com/apps/", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        shot(page, "00_apps")

        # Login if needed
        if re.search(r"Log in|Sign in|Login", page.inner_text("body"), re.I) and page.get_by_role(
            "button", name=re.compile(r"Log in|Sign in", re.I)
        ).count():
            try:
                page.get_by_role("button", name=re.compile(r"Log in|Sign in", re.I)).first.click()
                page.wait_for_timeout(2000)
            except Exception:
                pass
            # Prefer Google / TikTok login
            for pat in (r"Continue with Google", r"Google", r"Log in with TikTok", r"TikTok"):
                try:
                    if page.get_by_text(re.compile(pat, re.I)).count():
                        with ctx.expect_page(timeout=15000) as pi:
                            page.get_by_text(re.compile(pat, re.I)).first.click()
                        pop = pi.value
                        pop.wait_for_load_state("domcontentloaded")
                        page.wait_for_timeout(2000)
                        shot(pop, "01_login_pop")
                        acc = pop.get_by_text(re.compile(r"benoats86@gmail\.com", re.I))
                        if acc.count():
                            acc.first.click()
                            pop.wait_for_timeout(3000)
                        for lab in (r"^Continue$", r"^Allow$", r"^Confirm$"):
                            b = pop.get_by_role("button", name=re.compile(lab, re.I))
                            if b.count() and b.first.is_visible():
                                b.first.click()
                                pop.wait_for_timeout(2000)
                        break
                except Exception as e:
                    print("login try", pat, e)
            page.wait_for_timeout(5000)
            page.goto("https://developers.tiktok.com/apps/", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            shot(page, "02_after_login")

        body = page.inner_text("body")
        # Create app if needed
        if re.search(r"Create.?app|Create an app|Register app", body, re.I):
            try:
                page.get_by_role("button", name=re.compile(r"Create.?app|Create an app", re.I)).first.click(
                    timeout=3000
                )
            except Exception:
                page.get_by_text(re.compile(r"Create.?app|Create an app", re.I)).first.click()
            page.wait_for_timeout(2000)
            shot(page, "03_create")
            # Fill app name
            for ph in (r"App name", r"Application name", r"Name"):
                loc = page.get_by_placeholder(re.compile(ph, re.I))
                if loc.count() and loc.first.is_visible():
                    loc.first.fill(APP_NAME)
                    break
            else:
                # first text input
                try:
                    page.locator('input[type="text"]').first.fill(APP_NAME)
                except Exception:
                    pass
            # Accept terms checkboxes
            for cb in page.locator('input[type="checkbox"]').all():
                try:
                    if not cb.is_checked():
                        cb.check(force=True)
                except Exception:
                    pass
            for lab in (r"^Create$", r"^Submit$", r"^Next$", r"^Confirm$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click()
                    page.wait_for_timeout(3000)
                    break
            shot(page, "04_created")

        # Open existing Orbit app if listed
        try:
            if page.get_by_text(re.compile(r"Orbit Content Ops|Orbit", re.I)).count():
                page.get_by_text(re.compile(r"Orbit Content Ops|Orbit", re.I)).first.click()
                page.wait_for_timeout(2500)
        except Exception:
            pass
        shot(page, "05_app")

        # Extract client key/secret from page
        text = page.inner_text("body")
        key = None
        secret = None
        # Common patterns
        m = re.search(r"Client [Kk]ey[:\s]+([A-Za-z0-9]{10,})", text)
        if m:
            key = m.group(1)
        m2 = re.search(r"Client [Ss]ecret[:\s]+([A-Za-z0-9]{10,})", text)
        if m2:
            secret = m2.group(1)
        # Also try input values / data attributes
        try:
            vals = page.eval_on_selector_all(
                "input, code, pre, span",
                """els => els.map(e => ({t: (e.innerText||e.value||'').trim(), ph: e.placeholder||'', name: e.name||''})).filter(x => x.t.length>=12 && x.t.length<80)""",
            )
            result["candidates"] = vals[:40]
            for v in vals:
                t = v.get("t") or ""
                n = (v.get("name") or "") + (v.get("ph") or "")
                if re.search(r"key|client_key", n, re.I) and not key:
                    key = t
                if re.search(r"secret", n, re.I) and not secret:
                    secret = t
        except Exception as e:
            print("extract", e)

        # Configure redirect URI
        try:
            if page.get_by_text(re.compile(r"Redirect|Callback|Login Kit|Products", re.I)).count():
                page.get_by_text(re.compile(r"Login Kit|Products|Basic information|Settings", re.I)).first.click()
                page.wait_for_timeout(2000)
        except Exception:
            pass
        shot(page, "06_config")

        # Try fill redirect
        try:
            redirect_inputs = page.get_by_placeholder(re.compile(r"redirect|callback|uri|url", re.I))
            if redirect_inputs.count():
                redirect_inputs.first.fill(REDIRECT)
            else:
                # look for add redirect
                if page.get_by_text(re.compile(r"Add.*(redirect|URI|URL)", re.I)).count():
                    page.get_by_text(re.compile(r"Add.*(redirect|URI|URL)", re.I)).first.click()
                    page.wait_for_timeout(1000)
                    page.locator("input").last.fill(REDIRECT)
            for lab in (r"^Save$", r"^Submit$", r"^Add$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    page.wait_for_timeout(1500)
                    break
        except Exception as e:
            print("redirect", e)

        # Enable Content Posting / Login Kit if toggles visible
        for prod in (r"Login Kit", r"Content Posting", r"Share Video"):
            try:
                if page.get_by_text(re.compile(prod, re.I)).count():
                    page.get_by_text(re.compile(prod, re.I)).first.click()
                    page.wait_for_timeout(1000)
                    shot(page, f"07_{prod.replace(' ', '_')}")
            except Exception:
                pass

        page.wait_for_timeout(2000)
        shot(page, "99_final")
        # Re-read secrets
        text2 = page.inner_text("body")
        if not key:
            m = re.search(r"Client [Kk]ey[:\s]*\n?\s*([A-Za-z0-9_-]{12,})", text2)
            if m:
                key = m.group(1)
        if not secret:
            m = re.search(r"Client [Ss]ecret[:\s]*\n?\s*([A-Za-z0-9_-]{12,})", text2)
            if m:
                secret = m.group(1)

        result.update(
            {
                "status": "configured" if key else "needs_manual_copy",
                "client_key": key,
                "client_secret": secret,
                "notes": "Copy key/secret into 07_Content-Ops/.env if not auto-written",
                "url": page.url,
            }
        )
        RESULT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k != "candidates"}, indent=2), flush=True)
        # Leave browser open briefly for manual copy if needed
        if not key or not secret:
            print("MANUAL: copy Client Key/Secret from open browser into .env", flush=True)
            page.wait_for_timeout(90000)
        else:
            page.wait_for_timeout(5000)
        ctx.close()


if __name__ == "__main__":
    main()
