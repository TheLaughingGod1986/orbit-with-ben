#!/usr/bin/env python3
"""Finish TikTok Orbit Content Ops app: category, icon, credentials, redirect."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

APP = "https://developers.tiktok.com/app/7668773508012492817/pending"
ICON = "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/app_icon_1024.png"
REDIRECT = "http://localhost:3000/api/oauth/tiktok/callback"
ENV = Path("/Users/ben/code/Orbit-YouTube/07_Content-Ops/.env")
OUT = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AUDIT = OUT / "audit"
DESC = (
    "Orbit Content Ops schedules and publishes short-form space storytelling videos "
    "from the Orbit with Ben channel (@OrbitWithBen) to TikTok. Used privately by "
    "the channel operator for draft upload and publishing of original educational content."
)


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"fin_{name}.png"), full_page=False)
    print("shot", name, flush=True)


def write_env(key: str, secret: str) -> None:
    text = ENV.read_text()
    lines = []
    sk = ss = sr = False
    for line in text.splitlines():
        if line.startswith("TIKTOK_CLIENT_KEY=") or line.startswith("# TIKTOK_CLIENT_KEY="):
            lines.append(f"TIKTOK_CLIENT_KEY={key}")
            sk = True
        elif line.startswith("TIKTOK_CLIENT_SECRET=") or line.startswith("# TIKTOK_CLIENT_SECRET="):
            lines.append(f"TIKTOK_CLIENT_SECRET={secret}")
            ss = True
        elif line.startswith("TIKTOK_REDIRECT_URI=") or line.startswith("# TIKTOK_REDIRECT_URI="):
            lines.append(f"TIKTOK_REDIRECT_URI={REDIRECT}")
            sr = True
        else:
            lines.append(line)
    if not sk:
        lines.append(f"TIKTOK_CLIENT_KEY={key}")
    if not ss:
        lines.append(f"TIKTOK_CLIENT_SECRET={secret}")
    if not sr:
        lines.append(f"TIKTOK_REDIRECT_URI={REDIRECT}")
    ENV.write_text("\n".join(lines) + "\n")
    print("env written", flush=True)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = next(pg for pg in browser.contexts[0].pages if "developers.tiktok.com/app" in pg.url)
        page.bring_to_front()
        page.goto(APP, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        shot(page, "00")

        try:
            page.context.grant_permissions(["clipboard-read", "clipboard-write"])
        except Exception:
            pass

        # Select Education category
        page.evaluate(
            """() => {
              const btn = [...document.querySelectorAll('button')].find(n => {
                const t = (n.innerText || '').trim();
                const r = n.getBoundingClientRect();
                return r.width > 300 && r.height >= 30 && r.height <= 48 &&
                  (/Please select/i.test(t) || /Education/i.test(t) || (r.y > 450 && r.y < 700));
              });
              if (btn && !/Education/i.test(btn.innerText || '')) btn.click();
            }"""
        )
        page.wait_for_timeout(600)
        try:
            page.get_by_text("Education", exact=True).first.click(timeout=2500)
            print("education selected", flush=True)
        except Exception as e:
            print("education fail", e, flush=True)

        # Description / URLs / Web
        page.evaluate(
            """(payload) => {
              const setTA = (el, val) => {
                const s = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
                s.call(el, val);
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
              };
              const setIN = (el, val) => {
                const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                s.call(el, val);
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
              };
              const areas = [...document.querySelectorAll('textarea')].filter(
                t => t.offsetParent && !(t.placeholder || '').includes('Message')
              );
              if (areas[0]) setTA(areas[0], payload.desc);
              const byLabel = (labelText, value) => {
                const lab = [...document.querySelectorAll('*')].find(
                  n => (n.innerText || '').trim() === labelText
                );
                if (!lab) return false;
                let root = lab.parentElement;
                for (let i = 0; i < 6 && root; i++) {
                  const inp = root.querySelector('input[type=text]');
                  if (inp && inp.value !== 'Orbit Content Ops') {
                    setIN(inp, value);
                    return true;
                  }
                  root = root.parentElement;
                }
                return false;
              };
              byLabel('Terms of Service URL *', payload.tos);
              byLabel('Privacy Policy URL *', payload.privacy);
              const boxes = [...document.querySelectorAll('input[type=checkbox]')];
              if (boxes[0] && !boxes[0].checked) boxes[0].click();
            }""",
            {
                "desc": DESC,
                "tos": "https://www.youtube.com/t/terms",
                "privacy": "https://policies.google.com/privacy",
            },
        )

        # Icon
        inputs = page.locator('input[type="file"]')
        for i in range(inputs.count()):
            acc = (inputs.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "png" in acc or "jpeg" in acc:
                inputs.nth(i).set_input_files(ICON)
                print("icon set", flush=True)
                break
        page.wait_for_timeout(2500)
        shot(page, "01_form")

        # Reveal + copy credentials
        key = secret = None
        for label in ("Client key", "Client secret"):
            try:
                parent = page.locator(f"xpath=//*[normalize-space()='{label}']/ancestor::div[3]")
                btns = parent.locator("button")
                print(label, "btn", btns.count(), flush=True)
                for i in range(btns.count()):
                    try:
                        btns.nth(i).click(timeout=800)
                        page.wait_for_timeout(250)
                    except Exception:
                        pass
                # try clipboard from last button (copy)
                if btns.count():
                    btns.nth(btns.count() - 1).click(timeout=800)
                    page.wait_for_timeout(300)
                    try:
                        clip = page.evaluate("navigator.clipboard.readText()")
                        if clip and re.fullmatch(r"[A-Za-z0-9]{10,}", clip.strip()):
                            if label == "Client key":
                                key = clip.strip()
                            else:
                                secret = clip.strip()
                            print("clipboard", label, clip[:4] + "…", flush=True)
                    except Exception as e:
                        print("clipboard err", e, flush=True)
            except Exception as e:
                print("cred row", label, e, flush=True)
        shot(page, "02_creds")

        body = page.inner_text("body")
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        for i, line in enumerate(lines):
            if line.lower() == "client key" and i + 1 < len(lines):
                cand = lines[i + 1]
                if re.fullmatch(r"[A-Za-z0-9]{12,}", cand):
                    key = key or cand
            if line.lower() == "client secret" and i + 1 < len(lines):
                cand = lines[i + 1]
                if re.fullmatch(r"[A-Za-z0-9]{12,}", cand):
                    secret = secret or cand
        tokens = [l for l in lines if re.fullmatch(r"[A-Za-z0-9]{16,}", l)]
        print("tokens", [t[:4] + "…" for t in tokens[:4]], "key", bool(key), "secret", bool(secret), flush=True)

        # Save basic info
        try:
            page.get_by_role("button", name=re.compile(r"^Save$")).first.click(timeout=2500)
            page.wait_for_timeout(3000)
            print("saved", flush=True)
        except Exception as e:
            print("save", e, flush=True)
        shot(page, "03_saved")

        # Products via sidebar (not top nav)
        try:
            page.locator("text=Products").nth(1).click(timeout=2000)
        except Exception:
            page.get_by_role("link", name=re.compile(r"Products")).first.click(timeout=2000)
        page.wait_for_timeout(2000)
        shot(page, "04_products")
        print("products", page.url, flush=True)
        print(page.inner_text("body")[:500].replace("\n", " | "), flush=True)

        # Open Login Kit config with force
        try:
            page.get_by_text("Login Kit", exact=True).first.click(force=True, timeout=3000)
            page.wait_for_timeout(2000)
            shot(page, "05_login")
            filled = page.evaluate(
                """(uri) => {
                  const add = [...document.querySelectorAll('button,a,span')].find(n =>
                    /Add.*(URI|URL|redirect)/i.test((n.innerText || '').trim())
                  );
                  if (add) add.click();
                  const inputs = [...document.querySelectorAll('input')].filter(i => i.offsetParent);
                  for (const inp of inputs) {
                    const meta = ((inp.placeholder || '') + ((inp.closest('div') || {}).innerText || '').slice(0, 100)).toLowerCase();
                    if (/redirect|callback|uri|url|http/.test(meta) || inp.type === 'url') {
                      const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                      s.call(inp, uri);
                      inp.dispatchEvent(new Event('input', {bubbles: true}));
                      return 'meta';
                    }
                  }
                  for (const inp of inputs) {
                    if (inp.type === 'text' && !inp.value && inp.getBoundingClientRect().width > 180) {
                      const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                      s.call(inp, uri);
                      inp.dispatchEvent(new Event('input', {bubbles: true}));
                      return 'empty';
                    }
                  }
                  return 'fail:' + inputs.length;
                }""",
                REDIRECT,
            )
            print("redirect", filled, flush=True)
            for lab in ("Save", "Confirm", "Add", "Apply"):
                b = page.get_by_role("button", name=re.compile(rf"^{lab}$"))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    page.wait_for_timeout(1200)
                    break
            shot(page, "06_redirect")
        except Exception as e:
            print("login kit", e, flush=True)

        result = {
            "status": "partial",
            "redirect": REDIRECT,
            "client_key": key,
            "client_secret": secret,
        }
        if key and secret:
            write_env(key, secret)
            result["status"] = "ready"
            result["env_written"] = True
        OUT.joinpath("TIKTOK_DEV_APP.json").write_text(json.dumps(result, indent=2) + "\n")
        safe = dict(result)
        if safe.get("client_key"):
            safe["client_key"] = safe["client_key"][:4] + "…"
        if safe.get("client_secret"):
            safe["client_secret"] = safe["client_secret"][:4] + "…"
        print(json.dumps(safe, indent=2), flush=True)
        shot(page, "99")


if __name__ == "__main__":
    main()
