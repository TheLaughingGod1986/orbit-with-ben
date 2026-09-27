#!/usr/bin/env python3
"""Login to TikTok Developers and create Orbit Content Ops app."""
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
ENV = Path("/Users/ben/code/Orbit-YouTube/07_Content-Ops/.env")
REDIRECT = "http://localhost:3000/api/oauth/tiktok/callback"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"tdev_{name}.png"), full_page=False)
        print("shot", name, flush=True)
    except Exception as e:
        print("shot fail", name, e, flush=True)


def write_env(key: str, secret: str) -> None:
    text = ENV.read_text()
    # Uncomment / set TikTok vars
    lines = []
    seen_key = seen_secret = seen_redirect = False
    for line in text.splitlines():
        if line.startswith("TIKTOK_CLIENT_KEY=") or line.startswith("# TIKTOK_CLIENT_KEY="):
            lines.append(f"TIKTOK_CLIENT_KEY={key}")
            seen_key = True
        elif line.startswith("TIKTOK_CLIENT_SECRET=") or line.startswith("# TIKTOK_CLIENT_SECRET="):
            lines.append(f"TIKTOK_CLIENT_SECRET={secret}")
            seen_secret = True
        elif line.startswith("TIKTOK_REDIRECT_URI=") or line.startswith("# TIKTOK_REDIRECT_URI="):
            lines.append(f"TIKTOK_REDIRECT_URI={REDIRECT}")
            seen_redirect = True
        else:
            lines.append(line)
    if not seen_key:
        lines.append(f"TIKTOK_CLIENT_KEY={key}")
    if not seen_secret:
        lines.append(f"TIKTOK_CLIENT_SECRET={secret}")
    if not seen_redirect:
        lines.append(f"TIKTOK_REDIRECT_URI={REDIRECT}")
    ENV.write_text("\n".join(lines) + "\n")
    print("Wrote .env TikTok credentials", flush=True)


def main() -> None:
    result: dict = {"status": "started", "redirect": REDIRECT}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            slow_mo=60,
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        page.goto("https://developers.tiktok.com/apps/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        shot(page, "00")

        if page.get_by_role("button", name=re.compile(r"^Login$", re.I)).count():
            page.get_by_role("button", name=re.compile(r"^Login$", re.I)).first.click()
            page.wait_for_timeout(3000)
            shot(page, "01_login")

            # TikTok developer login often uses TikTok account QR or email
            # Try "Continue with TikTok" / email
            for pat in (
                r"Continue with TikTok",
                r"Log in with TikTok",
                r"Use phone / email / username",
                r"Continue with Google",
                r"Google",
            ):
                loc = page.get_by_text(re.compile(pat, re.I))
                if not loc.count():
                    continue
                print("click", pat, flush=True)
                try:
                    with ctx.expect_page(timeout=8000) as pi:
                        loc.first.click(force=True)
                    pop = pi.value
                    pop.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(2000)
                    shot(pop, "02_pop")
                    # Google account
                    if pop.get_by_text(re.compile(r"benoats86@gmail\.com", re.I)).count():
                        pop.get_by_text(re.compile(r"benoats86@gmail\.com", re.I)).first.click()
                        pop.wait_for_timeout(3000)
                    for lab in (r"^Continue$", r"^Allow$", r"^Confirm$", r"^Approve$"):
                        b = pop.get_by_role("button", name=re.compile(lab, re.I))
                        if b.count() and b.first.is_visible():
                            b.first.click()
                            pop.wait_for_timeout(2500)
                except Exception:
                    loc.first.click(force=True)
                    page.wait_for_timeout(3000)
                    shot(page, "02_same")
                break

            # Wait for login — QR likely
            print("Waiting up to 3 min for developer login (QR/approve)...", flush=True)
            for i in range(36):
                page.wait_for_timeout(5000)
                page.goto("https://developers.tiktok.com/apps/", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                if i % 3 == 0:
                    shot(page, f"wait_{i}")
                body = page.inner_text("body")
                if not re.search(r"No access|You need to login", body, re.I):
                    print("logged in", flush=True)
                    break
            else:
                result["status"] = "needs_developer_login"
                result["notes"] = (
                    "Log into https://developers.tiktok.com with the TikTok account "
                    "@orbitwithben (or Ben's developer account), create an app, then re-run."
                )
                RESULT.write_text(json.dumps(result, indent=2) + "\n")
                print(json.dumps(result, indent=2), flush=True)
                page.wait_for_timeout(30000)
                ctx.close()
                return

        shot(page, "03_apps")
        body = page.inner_text("body")

        # Create app
        created = False
        if page.get_by_role("button", name=re.compile(r"Create.?app|Register", re.I)).count() or page.get_by_text(
            re.compile(r"Create.?app", re.I)
        ).count():
            try:
                page.get_by_role("button", name=re.compile(r"Create.?app", re.I)).first.click(timeout=3000)
            except Exception:
                page.get_by_text(re.compile(r"Create.?app", re.I)).first.click()
            page.wait_for_timeout(2000)
            shot(page, "04_create_form")
            # App name
            filled = False
            for sel in (
                page.get_by_placeholder(re.compile(r"app name|name", re.I)),
                page.locator('input[name*="name" i]'),
                page.locator('input[type="text"]'),
            ):
                if sel.count() and sel.first.is_visible():
                    sel.first.fill("Orbit Content Ops")
                    filled = True
                    break
            print("name filled", filled, flush=True)
            for cb in page.locator('input[type="checkbox"]').all():
                try:
                    if not cb.is_checked():
                        cb.check(force=True)
                except Exception:
                    pass
            for lab in (r"^Create$", r"^Submit$", r"^Next$", r"^Confirm$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible() and not b.first.is_disabled():
                    b.first.click()
                    page.wait_for_timeout(3500)
                    created = True
                    break
            shot(page, "05_after_create")

        # Click into app card
        try:
            if page.get_by_text(re.compile(r"Orbit Content Ops", re.I)).count():
                page.get_by_text(re.compile(r"Orbit Content Ops", re.I)).first.click()
                page.wait_for_timeout(2500)
        except Exception:
            pass
        shot(page, "06_detail")

        # Navigate to keys / credentials / basic info
        for tab in (r"Basic information", r"Credentials", r"Keys", r"App details", r"Products"):
            try:
                if page.get_by_text(re.compile(tab, re.I)).count():
                    page.get_by_text(re.compile(tab, re.I)).first.click()
                    page.wait_for_timeout(1500)
                    shot(page, f"tab_{tab.replace(' ', '_')}")
            except Exception:
                pass

        # Extract key/secret — look for reveal buttons
        for lab in (r"Show", r"Reveal", r"Copy", r"Client [Ss]ecret"):
            try:
                btns = page.get_by_role("button", name=re.compile(lab, re.I))
                for i in range(min(btns.count(), 5)):
                    btns.nth(i).click(timeout=1000)
                    page.wait_for_timeout(500)
            except Exception:
                pass
        shot(page, "07_keys")

        text = page.content()
        # Prefer visible labeled fields via JS
        extracted = page.evaluate(
            """() => {
              const out = {};
              const walk = (root) => {
                const nodes = [...root.querySelectorAll('*')];
                for (const n of nodes) {
                  const t = (n.innerText || '').trim();
                  if (/^Client Key$/i.test(t) || /Client Key/i.test(t) && t.length < 40) {
                    const sib = n.parentElement ? n.parentElement.innerText : '';
                    const m = sib.match(/Client Key\\s*([A-Za-z0-9]{10,})/i);
                    if (m) out.key = m[1];
                  }
                  if (/Client Secret/i.test(t) && t.length < 60) {
                    const sib = n.parentElement ? n.parentElement.innerText : '';
                    const m = sib.match(/Client Secret\\s*([A-Za-z0-9]{10,})/i);
                    if (m) out.secret = m[1];
                  }
                }
              };
              walk(document.body);
              // inputs
              for (const inp of document.querySelectorAll('input')) {
                const label = (inp.getAttribute('aria-label') || inp.name || inp.placeholder || '').toLowerCase();
                if (label.includes('client key') || label.includes('client_key')) out.key = inp.value;
                if (label.includes('secret')) out.secret = inp.value;
              }
              return out;
            }"""
        )
        print("extracted", extracted, flush=True)
        key = extracted.get("key")
        secret = extracted.get("secret")
        if not key:
            m = re.search(r"client[_ ]key[\"'\\s:>]+([A-Za-z0-9]{12,})", text, re.I)
            if m:
                key = m.group(1)
        if not secret:
            m = re.search(r"client[_ ]secret[\"'\\s:>]+([A-Za-z0-9]{12,})", text, re.I)
            if m:
                secret = m.group(1)

        # Configure Login Kit redirect
        try:
            if page.get_by_text(re.compile(r"Login Kit|Products", re.I)).count():
                page.get_by_text(re.compile(r"Login Kit", re.I)).first.click()
                page.wait_for_timeout(2000)
            shot(page, "08_login_kit")
            # add redirect URI
            if page.get_by_text(re.compile(r"Add.*(URI|URL|redirect)", re.I)).count():
                page.get_by_text(re.compile(r"Add.*(URI|URL|redirect)", re.I)).first.click()
                page.wait_for_timeout(800)
            for loc in (
                page.get_by_placeholder(re.compile(r"redirect|callback|https?://", re.I)),
                page.locator('input[type="url"]'),
            ):
                if loc.count() and loc.first.is_visible():
                    loc.first.fill(REDIRECT)
                    break
            for lab in (r"^Save$", r"^Submit$", r"^Confirm$", r"^Add$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    page.wait_for_timeout(1500)
                    break
        except Exception as e:
            print("redirect cfg", e)

        # Enable Content Posting API product
        try:
            if page.get_by_text(re.compile(r"Content Posting", re.I)).count():
                page.get_by_text(re.compile(r"Content Posting", re.I)).first.click()
                page.wait_for_timeout(2000)
                shot(page, "09_content_posting")
                for lab in (r"^Add$", r"^Enable$", r"^Apply$", r"^Get started$"):
                    b = page.get_by_role("button", name=re.compile(lab, re.I))
                    if b.count() and b.first.is_visible():
                        b.first.click()
                        page.wait_for_timeout(1500)
                        break
        except Exception as e:
            print("content posting", e)

        shot(page, "99")
        result.update(
            {
                "status": "ready" if key and secret else "partial",
                "client_key": key,
                "client_secret": secret,
                "created": created,
                "url": page.url,
            }
        )
        if key and secret:
            write_env(key, secret)
            result["env_written"] = True
        else:
            result["notes"] = (
                "Could not auto-read Client Key/Secret. Copy them from the open "
                "developers.tiktok.com app page into 07_Content-Ops/.env"
            )
            print(result["notes"], flush=True)
            page.wait_for_timeout(120000)

        RESULT.write_text(json.dumps(result, indent=2) + "\n")
        # Don't print secret in full to stdout in case logs are shared — print masked
        safe = dict(result)
        if safe.get("client_secret"):
            safe["client_secret"] = safe["client_secret"][:4] + "…"
        if safe.get("client_key"):
            safe["client_key"] = safe["client_key"][:4] + "…"
        print(json.dumps(safe, indent=2), flush=True)
        ctx.close()


if __name__ == "__main__":
    main()
