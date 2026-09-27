#!/usr/bin/env python3
"""Fill Orbit Content Ops TikTok app via Chrome CDP (port 9222)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

APP_URL = "https://developers.tiktok.com/app/7668773508012492817/pending"
REDIRECT = "http://localhost:3000/api/oauth/tiktok/callback"
ICON = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/app_icon_1024.png")
OUT = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok")
AUDIT = OUT / "audit"
RESULT = OUT / "TIKTOK_DEV_APP.json"
ENV = Path("/Users/ben/code/Orbit-YouTube/07_Content-Ops/.env")
DESC = (
    "Orbit Content Ops schedules and publishes short-form space storytelling videos "
    "from the Orbit with Ben channel (@OrbitWithBen) to TikTok. Used privately by "
    "the channel operator for draft upload and publishing of original educational content."
)
TOS = "https://www.youtube.com/t/terms"
PRIVACY = "https://policies.google.com/privacy"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(AUDIT / f"cdp_{name}.png"), full_page=False)
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
    print("env written", flush=True)


def main() -> None:
    result: dict = {"status": "started", "app_url": APP_URL, "redirect": REDIRECT}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if "developers.tiktok.com/app" in pg.url), None)
        if not page:
            page = ctx.new_page()
            page.goto(APP_URL, wait_until="domcontentloaded")
        page.bring_to_front()
        page.wait_for_timeout(2000)
        shot(page, "00")
        body = page.inner_text("body")
        if re.search(r"No access", body) and "Orbit Content Ops" not in body:
            result["status"] = "needs_login"
            RESULT.write_text(json.dumps(result, indent=2) + "\n")
            print("NEEDS LOGIN", flush=True)
            return

        try:
            page.get_by_text("Basic information", exact=False).first.click(timeout=3000)
            page.wait_for_timeout(800)
        except Exception:
            pass

        # Icon
        inputs = page.locator('input[type="file"]')
        target = None
        for i in range(inputs.count()):
            acc = (inputs.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "png" in acc or "jpeg" in acc:
                target = inputs.nth(i)
                break
        if target is None and inputs.count():
            target = inputs.first
        if target is not None:
            target.set_input_files(str(ICON))
            page.wait_for_timeout(3000)
            print("icon uploaded", flush=True)
        shot(page, "01_icon")

        # Category
        opened = page.evaluate(
            """() => {
          const btn = [...document.querySelectorAll('button')].find(n => {
            const r = n.getBoundingClientRect();
            return r.y >= 500 && r.y <= 650 && r.width > 300 && r.height >= 30 && r.height <= 50;
          });
          if (!btn) return 'no';
          if (/Education/i.test(btn.innerText || '')) return 'already';
          btn.click();
          return 'opened';
        }"""
        )
        print("category", opened, flush=True)
        page.wait_for_timeout(700)
        if opened != "already":
            edu = page.locator("div, span, li").filter(has_text=re.compile(r"^Education$"))
            if edu.count():
                edu.first.click(timeout=2500)
                print("education selected", flush=True)
        page.wait_for_timeout(400)

        page.evaluate(
            """(payload) => {
          const setTA = (el, val) => {
            const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
          };
          const setIN = (el, val) => {
            const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
          };
          const areas = [...document.querySelectorAll('textarea')].filter(
            t => t.offsetParent && !(t.placeholder || '').includes('Message')
          );
          if (areas[0]) setTA(areas[0], payload.desc);
          const byLabel = (labelText, value) => {
            const lab = [...document.querySelectorAll('*')].find(n => (n.innerText || '').trim() === labelText);
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
          const tos = byLabel('Terms of Service URL *', payload.tos);
          const privacy = byLabel('Privacy Policy URL *', payload.privacy);
          const boxes = [...document.querySelectorAll('input[type=checkbox]')];
          if (boxes[0] && !boxes[0].checked) boxes[0].click();
          return {tos, privacy, web: boxes[0] ? boxes[0].checked : null};
        }""",
            {"desc": DESC, "tos": TOS, "privacy": PRIVACY},
        )
        shot(page, "03_filled")

        try:
            page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(timeout=3000)
            page.wait_for_timeout(3500)
            print("saved basic", flush=True)
        except Exception as e:
            print("save err", e, flush=True)
        shot(page, "04_saved")

        # Products
        try:
            page.get_by_text(re.compile(r"^Products$")).first.click(timeout=3000)
        except Exception:
            page.locator("text=Products").first.click()
        page.wait_for_timeout(2500)
        shot(page, "10_products")

        products = {}
        for name in ("Login Kit", "Content Posting API"):
            try:
                handled = page.evaluate(
                    """(name) => {
                  const nodes = [...document.querySelectorAll('button, a, div, span')];
                  const title = nodes.find(n => (n.innerText || '').trim() === name);
                  if (!title) return 'no-title';
                  let root = title.closest('div');
                  for (let i = 0; i < 10 && root; i++) {
                    const add = [...root.querySelectorAll('button, a')].find(b =>
                      /^(Add|Enable|Apply|Get started|Configure)$/i.test((b.innerText || '').trim())
                      || /Add product/i.test(b.innerText || '')
                    );
                    if (add) {
                      add.click();
                      return 'clicked:' + (add.innerText || '').trim();
                    }
                    root = root.parentElement;
                  }
                  title.click();
                  return 'title-clicked';
                }""",
                    name,
                )
                products[name] = handled
                page.wait_for_timeout(2000)
                for lab in ("Add", "Enable", "Apply", "Confirm", "Save", "Done", "OK"):
                    b = page.get_by_role("button", name=re.compile(rf"^{lab}$", re.I))
                    if b.count() and b.first.is_visible():
                        try:
                            b.first.click(timeout=1000)
                            page.wait_for_timeout(1000)
                            products[name] += f"+{lab}"
                        except Exception:
                            pass
                shot(page, f"11_{name.replace(' ', '_')}")
            except Exception as e:
                products[name] = str(e)[:120]
        result["products"] = products
        print("products", products, flush=True)

        # Login Kit redirect
        try:
            page.get_by_text("Login Kit", exact=False).first.click(timeout=2500)
            page.wait_for_timeout(2000)
            info = page.evaluate(
                """(uri) => {
                  const addBtn = [...document.querySelectorAll('button,a,span')].find(n =>
                    /Add.*(URI|URL|redirect)/i.test((n.innerText || '').trim())
                  );
                  if (addBtn) addBtn.click();
                  const inputs = [...document.querySelectorAll('input')].filter(i => i.offsetParent !== null);
                  for (const inp of inputs) {
                    const meta = ((inp.placeholder || '') + ' ' + (inp.name || '') + ' ' +
                      ((inp.closest('div') && inp.closest('div').innerText) || '').slice(0, 100)).toLowerCase();
                    if (/redirect|callback|uri/.test(meta) || inp.type === 'url') {
                      const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                      setter.call(inp, uri);
                      inp.dispatchEvent(new Event('input', {bubbles:true}));
                      inp.dispatchEvent(new Event('change', {bubbles:true}));
                      return {ok: true, via: 'meta'};
                    }
                  }
                  for (const inp of inputs) {
                    const r = inp.getBoundingClientRect();
                    if (inp.type === 'text' && r.width > 180 && !inp.value) {
                      const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                      setter.call(inp, uri);
                      inp.dispatchEvent(new Event('input', {bubbles:true}));
                      return {ok: true, via: 'empty'};
                    }
                  }
                  return {ok: false, n: inputs.length};
                }""",
                REDIRECT,
            )
            print("redirect", info, flush=True)
            result["redirect_fill"] = info
            for lab in ("Save", "Confirm", "Add", "Apply"):
                b = page.get_by_role("button", name=re.compile(rf"^{lab}$", re.I))
                if b.count() and b.first.is_visible():
                    b.first.click()
                    page.wait_for_timeout(1500)
                    break
            shot(page, "13_redirect")
        except Exception as e:
            print("login kit err", e, flush=True)

        # Credentials
        try:
            page.get_by_text("App details", exact=False).first.click(timeout=2000)
            page.wait_for_timeout(800)
            page.get_by_text("Basic information", exact=False).first.click(timeout=2000)
            page.wait_for_timeout(1200)
        except Exception:
            page.goto(APP_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

        for lab in ("Show", "Reveal", "Copy"):
            try:
                btns = page.get_by_role("button", name=re.compile(lab, re.I))
                for i in range(min(btns.count(), 8)):
                    try:
                        btns.nth(i).click(timeout=800)
                        page.wait_for_timeout(250)
                    except Exception:
                        pass
            except Exception:
                pass
        shot(page, "20_keys")
        creds = page.evaluate(
            """() => {
              const out = {};
              const body = document.body.innerText || '';
              let m = body.match(/Client Key\\s*([A-Za-z0-9]{10,})/i);
              if (m) out.key = m[1];
              m = body.match(/Client Secret\\s*([A-Za-z0-9]{10,})/i);
              if (m && !m[1].includes('*')) out.secret = m[1];
              for (const inp of document.querySelectorAll('input')) {
                const val = (inp.value || '').trim();
                const label = ((inp.getAttribute('aria-label') || '') + inp.name + inp.placeholder).toLowerCase();
                if (val.length >= 10 && /key/.test(label)) out.key = val;
                if (val.length >= 10 && /secret/.test(label)) out.secret = val;
              }
              out.lines = body.split('\\n').filter(l => /client key|client secret|app id/i.test(l)).slice(0, 12);
              return out;
            }"""
        )
        print("creds lines", creds.get("lines"), flush=True)
        result["client_key"] = creds.get("key")
        result["client_secret"] = creds.get("secret")
        if creds.get("key") and creds.get("secret"):
            write_env(creds["key"], creds["secret"])
            result["env_written"] = True
            result["status"] = "ready"
        else:
            result["status"] = "partial"
            result["cred_lines"] = creds.get("lines")
        shot(page, "99")
        RESULT.write_text(json.dumps(result, indent=2) + "\n")
        safe = dict(result)
        if safe.get("client_secret"):
            safe["client_secret"] = str(safe["client_secret"])[:4] + "…"
        if safe.get("client_key"):
            safe["client_key"] = str(safe["client_key"])[:4] + "…"
        print(json.dumps(safe, indent=2), flush=True)


if __name__ == "__main__":
    main()
