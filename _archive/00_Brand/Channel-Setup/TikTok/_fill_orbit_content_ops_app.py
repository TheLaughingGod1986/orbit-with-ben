#!/usr/bin/env python3
"""Fill Orbit Content Ops TikTok developer app (basic info + products + credentials)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

APP_URL = "https://developers.tiktok.com/app/7668773508012492817/pending"
REDIRECT = "http://localhost:3000/api/oauth/tiktok/callback"
OUT = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AUDIT = OUT / "audit"
RESULT = OUT / "TIKTOK_DEV_APP.json"
ENV = Path("/Users/ben/code/Orbit-YouTube/07_Content-Ops/.env")
ICON = OUT / "app_icon_1024.png"
DESC = (
    "Orbit Content Ops schedules and publishes short-form space storytelling videos "
    "from the Orbit with Ben channel (@OrbitWithBen) to TikTok. Used privately by "
    "the channel operator for draft upload and publishing of original educational content."
)
# Prefer profiles that may already hold developer login
PROFILES = [
    "/Users/ben/code/youtube/.playwright-tiktok-from-chrome",
    "/Users/ben/code/youtube/.playwright-youtube-profile",
]


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"fill_{name}.png"), full_page=False)
        print("shot", name, flush=True)
    except Exception as e:
        print("shot fail", name, e, flush=True)


def write_env(key: str, secret: str) -> None:
    text = ENV.read_text()
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


def fill_basic(page) -> dict:
    info = {"icon": False, "category": False, "description": False, "saved": False}
    shot(page, "01_basic")

    # App icon upload
    if ICON.exists():
        file_inputs = page.locator('input[type="file"]')
        if file_inputs.count():
            try:
                file_inputs.first.set_input_files(str(ICON))
                info["icon"] = True
                page.wait_for_timeout(2000)
                print("icon uploaded via file input", flush=True)
            except Exception as e:
                print("file input fail", e, flush=True)
        if not info["icon"]:
            # Click the + icon area then set files on chooser
            try:
                with page.expect_file_chooser(timeout=4000) as fc:
                    # Try common upload affordances
                    for sel in (
                        page.locator('[class*="upload"]').first,
                        page.get_by_text(re.compile(r"1024|App icon|\+", re.I)).first,
                        page.locator("img").first,
                    ):
                        try:
                            sel.click(timeout=1500)
                            break
                        except Exception:
                            continue
                chooser = fc.value
                chooser.set_files(str(ICON))
                info["icon"] = True
                page.wait_for_timeout(2000)
                print("icon uploaded via chooser", flush=True)
            except Exception as e:
                print("icon chooser fail", e, flush=True)
    shot(page, "02_icon")

    # Category — pick first sensible option (often Entertainment / Education / Tools)
    try:
        cat = page.locator("text=Category").locator("xpath=ancestor::*[self::div or self::label][1]")
        # Open dropdown near Category label
        for cand in (
            page.get_by_role("combobox"),
            page.locator('[class*="select"]').filter(has_text=re.compile(r"category|select|please", re.I)),
            page.locator(".semi-select, .ant-select, [role='listbox'], [class*='Select']").first,
            page.get_by_text(re.compile(r"Please select|Select category|Category", re.I)),
        ):
            try:
                if cand.count() and cand.first.is_visible():
                    cand.first.click(timeout=2000)
                    page.wait_for_timeout(800)
                    break
            except Exception:
                continue
        # Prefer Education / Entertainment / Tools / Media
        picked = False
        for label in (
            r"^Education$",
            r"Education",
            r"Entertainment",
            r"Tools?",
            r"Media",
            r"Lifestyle",
            r"Other",
        ):
            opt = page.get_by_role("option", name=re.compile(label, re.I))
            if not opt.count():
                opt = page.get_by_text(re.compile(label, re.I))
            if opt.count():
                try:
                    opt.first.click(timeout=2000)
                    picked = True
                    info["category"] = label
                    print("category", label, flush=True)
                    break
                except Exception:
                    continue
        if not picked:
            # Click first visible dropdown option
            opts = page.locator('[role="option"], .semi-select-option, .ant-select-item')
            if opts.count():
                txt = opts.first.inner_text()
                opts.first.click()
                info["category"] = txt.strip()[:80]
                print("category first option", info["category"], flush=True)
    except Exception as e:
        print("category fail", e, flush=True)
    shot(page, "03_category")

    # Description
    try:
        filled = False
        for loc in (
            page.get_by_placeholder(re.compile(r"description|describe", re.I)),
            page.locator("textarea"),
            page.get_by_role("textbox").filter(has=page.locator("textarea")),
        ):
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                loc.first.fill(DESC)
                filled = True
                info["description"] = True
                print("description filled", flush=True)
                break
        if not filled:
            # Find textarea near Description label via JS
            ok = page.evaluate(
                """(desc) => {
                  const areas = [...document.querySelectorAll('textarea')];
                  for (const a of areas) {
                    if (a.offsetParent !== null) { a.focus(); a.value = desc;
                      a.dispatchEvent(new Event('input', {bubbles:true}));
                      a.dispatchEvent(new Event('change', {bubbles:true}));
                      return true;
                    }
                  }
                  return false;
                }""",
                DESC,
            )
            info["description"] = bool(ok)
            print("description js", ok, flush=True)
    except Exception as e:
        print("description fail", e, flush=True)
    shot(page, "04_desc")

    # Save
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_visible():
            save.first.click()
            page.wait_for_timeout(2500)
            info["saved"] = True
            print("saved basic info", flush=True)
    except Exception as e:
        print("save fail", e, flush=True)
    shot(page, "05_saved")
    return info


def enable_products(page) -> dict:
    out = {"login_kit": False, "content_posting": False, "redirect": False}
    # Products tab
    try:
        page.get_by_text(re.compile(r"^Products$", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(2000)
    except Exception:
        page.goto(APP_URL.replace("/pending", "") + "/product", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
    shot(page, "10_products")

    for product, key in (("Login Kit", "login_kit"), ("Content Posting", "content_posting")):
        try:
            body = page.inner_text("body")
            # Click Add / Configure near product name
            card = page.get_by_text(re.compile(product, re.I)).first
            if card.count() or page.get_by_text(re.compile(product, re.I)).count():
                page.get_by_text(re.compile(product, re.I)).first.click()
                page.wait_for_timeout(1500)
            for lab in (r"^Add$", r"^Enable$", r"^Apply$", r"^Get started$", r"^Configure$", r"^Set up$"):
                b = page.get_by_role("button", name=re.compile(lab, re.I))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    page.wait_for_timeout(1500)
                    out[key] = True
                    break
            # Also try "Add product" style
            add = page.get_by_role("button", name=re.compile(rf"Add.*{product}|{product}", re.I))
            if add.count() and add.first.is_visible() and not out[key]:
                add.first.click()
                page.wait_for_timeout(1500)
                out[key] = True
            shot(page, f"11_{key}")
        except Exception as e:
            print(product, e, flush=True)

    # Login Kit redirect URI — may be under Login Kit settings
    try:
        if page.get_by_text(re.compile(r"Login Kit", re.I)).count():
            page.get_by_text(re.compile(r"Login Kit", re.I)).first.click()
            page.wait_for_timeout(1500)
        shot(page, "12_login_kit")
        # Look for redirect URI fields
        if page.get_by_text(re.compile(r"Add.*(URI|URL|redirect)", re.I)).count():
            page.get_by_text(re.compile(r"Add.*(URI|URL|redirect)", re.I)).first.click()
            page.wait_for_timeout(800)
        for loc in (
            page.get_by_placeholder(re.compile(r"redirect|callback|https?://|uri", re.I)),
            page.locator('input[type="url"]'),
            page.locator('input[placeholder*="http" i]'),
        ):
            if loc.count() and loc.first.is_visible():
                loc.first.fill(REDIRECT)
                out["redirect"] = True
                print("redirect filled", flush=True)
                break
        if not out["redirect"]:
            # JS fill any empty http-looking input near Redirect
            ok = page.evaluate(
                """(uri) => {
                  const labels = [...document.querySelectorAll('*')].filter(n =>
                    /redirect\\s*uri|callback/i.test((n.innerText||'').slice(0,40)));
                  for (const lab of labels) {
                    const root = lab.closest('div') || lab.parentElement;
                    if (!root) continue;
                    const inp = root.querySelector('input');
                    if (inp) {
                      inp.focus(); inp.value = uri;
                      inp.dispatchEvent(new Event('input', {bubbles:true}));
                      inp.dispatchEvent(new Event('change', {bubbles:true}));
                      return true;
                    }
                  }
                  for (const inp of document.querySelectorAll('input')) {
                    const ph = (inp.placeholder||'') + (inp.name||'') + (inp.id||'');
                    if (/redirect|callback|uri|url/i.test(ph) && inp.offsetParent !== null) {
                      inp.focus(); inp.value = uri;
                      inp.dispatchEvent(new Event('input', {bubbles:true}));
                      return true;
                    }
                  }
                  return false;
                }""",
                REDIRECT,
            )
            out["redirect"] = bool(ok)
            print("redirect js", ok, flush=True)
        for lab in (r"^Save$", r"^Submit$", r"^Confirm$", r"^Add$", r"^Apply$"):
            b = page.get_by_role("button", name=re.compile(lab, re.I))
            if b.count() and b.first.is_visible() and not b.first.is_disabled():
                b.first.click()
                page.wait_for_timeout(1500)
                break
        shot(page, "13_redirect")
    except Exception as e:
        print("redirect fail", e, flush=True)
    return out


def extract_credentials(page) -> dict:
    # App details / Basic information often shows Client Key
    for tab in (r"App details", r"Basic information", r"Credentials", r"Keys"):
        try:
            if page.get_by_text(re.compile(tab, re.I)).count():
                page.get_by_text(re.compile(tab, re.I)).first.click()
                page.wait_for_timeout(1200)
        except Exception:
            pass
    for lab in (r"Show", r"Reveal", r"Copy", r"Client [Ss]ecret"):
        try:
            btns = page.get_by_role("button", name=re.compile(lab, re.I))
            for i in range(min(btns.count(), 6)):
                btns.nth(i).click(timeout=1000)
                page.wait_for_timeout(400)
        except Exception:
            pass
    shot(page, "20_keys")
    extracted = page.evaluate(
        """() => {
          const out = {};
          const body = document.body.innerText || '';
          const km = body.match(/Client Key\\s*([A-Za-z0-9]{10,})/i);
          const sm = body.match(/Client Secret\\s*([A-Za-z0-9]{10,})/i);
          if (km) out.key = km[1];
          if (sm) out.secret = sm[1];
          for (const inp of document.querySelectorAll('input')) {
            const label = ((inp.getAttribute('aria-label') || '') + (inp.name || '') + (inp.placeholder || '')).toLowerCase();
            const val = (inp.value || '').trim();
            if (!val || val.length < 8) continue;
            if (label.includes('client key') || label.includes('client_key') || label.includes('app id') === false && /key/.test(label))
              out.key = out.key || val;
            if (label.includes('secret')) out.secret = val;
          }
          // Copy buttons next to values
          const nodes = [...document.querySelectorAll('div,span,p,td')];
          for (const n of nodes) {
            const t = (n.innerText || '').trim();
            if (/^Client Key$/i.test(t)) {
              const sib = (n.parentElement && n.parentElement.innerText) || '';
              const m = sib.match(/Client Key\\s*([A-Za-z0-9]{10,})/i);
              if (m) out.key = m[1];
            }
            if (/^Client Secret$/i.test(t)) {
              const sib = (n.parentElement && n.parentElement.innerText) || '';
              const m = sib.match(/Client Secret\\s*([A-Za-z0-9\\*]{10,})/i);
              if (m && !m[1].includes('*')) out.secret = m[1];
            }
          }
          return out;
        }"""
    )
    return extracted


def try_cdp(p):
    for port in (9222, 9223, 9333):
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            print("CDP connected", port, flush=True)
            return browser
        except Exception:
            continue
    return None


def main() -> None:
    result: dict = {
        "status": "started",
        "app_url": APP_URL,
        "redirect": REDIRECT,
        "app_id": "7668773508012492817",
    }
    with sync_playwright() as p:
        browser = try_cdp(p)
        ctx = None
        page = None
        own_ctx = False

        if browser:
            # Use existing Arc/Chrome tab if possible
            for c in browser.contexts:
                for pg in c.pages:
                    if "developers.tiktok.com" in (pg.url or ""):
                        page = pg
                        ctx = c
                        print("reusing tab", pg.url, flush=True)
                        break
                if page:
                    break
            if not page and browser.contexts:
                ctx = browser.contexts[0]
                page = ctx.new_page()

        if not page:
            own_ctx = True
            last_err = None
            for profile in PROFILES:
                if not Path(profile).exists():
                    continue
                try:
                    print("launching profile", profile, flush=True)
                    ctx = p.chromium.launch_persistent_context(
                        profile,
                        headless=False,
                        viewport={"width": 1400, "height": 900},
                        args=["--disable-blink-features=AutomationControlled"],
                        ignore_default_args=["--enable-automation"],
                        slow_mo=50,
                    )
                    page = ctx.pages[0] if ctx.pages else ctx.new_page()
                    break
                except Exception as e:
                    last_err = e
                    print("profile busy?", e, flush=True)
            if not page:
                # Ephemeral headed browser — user may already be logged in via... no cookies
                print("ephemeral chromium", last_err, flush=True)
                browser = p.chromium.launch(headless=False, slow_mo=50)
                ctx = browser.new_context(viewport={"width": 1400, "height": 900})
                page = ctx.new_page()
                own_ctx = True

        page.goto(APP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        shot(page, "00")
        body = page.inner_text("body")
        if re.search(r"No access|You need to login|Log in", body, re.I) and not re.search(
            r"Orbit Content Ops|Basic information|App icon", body, re.I
        ):
            result["status"] = "needs_login"
            result["notes"] = (
                "Developer portal session not available in automation browser. "
                "Stay logged in on the open Arc tab — or log in in the Playwright window "
                "within 3 minutes."
            )
            print(result["notes"], flush=True)
            for i in range(36):
                page.wait_for_timeout(5000)
                try:
                    body = page.inner_text("body")
                except Exception:
                    continue
                if re.search(r"Orbit Content Ops|Basic information|App icon", body, re.I):
                    print("login detected", flush=True)
                    page.goto(APP_URL, wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                    break
                if i % 3 == 0:
                    shot(page, f"wait_{i}")
            else:
                RESULT.write_text(json.dumps(result, indent=2) + "\n")
                if own_ctx and ctx:
                    ctx.close()
                return

        # Ensure we're on basic info
        try:
            if page.get_by_text(re.compile(r"Basic information", re.I)).count():
                page.get_by_text(re.compile(r"Basic information", re.I)).first.click()
                page.wait_for_timeout(1000)
        except Exception:
            pass

        result["basic"] = fill_basic(page)
        result["products"] = enable_products(page)
        creds = extract_credentials(page)
        result["client_key"] = creds.get("key")
        result["client_secret"] = creds.get("secret")
        print("creds", {k: (v[:4] + "…" if v else None) for k, v in creds.items()}, flush=True)

        if result["client_key"] and result["client_secret"]:
            write_env(result["client_key"], result["client_secret"])
            result["env_written"] = True
            result["status"] = "ready"
        else:
            result["status"] = "partial"
            result["notes"] = (
                "Basic/products attempted. Copy Client Key + Secret from App details "
                "into 07_Content-Ops/.env if not auto-written. Browser staying open 90s."
            )
            print(result["notes"], flush=True)
            page.wait_for_timeout(90000)

        shot(page, "99")
        RESULT.write_text(json.dumps(result, indent=2) + "\n")
        safe = dict(result)
        if safe.get("client_secret"):
            safe["client_secret"] = str(safe["client_secret"])[:4] + "…"
        if safe.get("client_key"):
            safe["client_key"] = str(safe["client_key"])[:4] + "…"
        print(json.dumps(safe, indent=2), flush=True)
        if own_ctx and ctx:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
