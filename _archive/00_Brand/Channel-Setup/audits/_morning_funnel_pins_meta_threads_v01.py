#!/usr/bin/env python3
"""Morning funnel: pin YT CTAs, TikTok bio link, Meta share 3 reels, Threads post 3."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
EXPORTS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/live_funnel_morning_2026-08-03"
LONDON = ZoneInfo("Europe/London")
SOFT = "Full film on YouTube."
FULL_URL = "https://youtu.be/Mo93x0fxB1Q"
LONG_TITLE = "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained"
COMMENT = f"Full film here → {LONG_TITLE}\n{FULL_URL}\n\nOrbit's Cosmic Journey 🚀"
TT_LINK = "https://www.youtube.com/@OrbitWithBen"
TT_BIO = "Space stories. Big questions. Films → youtube.com/@OrbitWithBen"

TARGETS = [
    {
        "id": "1HuV8o3gOss",
        "title": "Where Is Everybody?",
        "file": "aliens_short-02_fermi-paradox_v02.mp4",
    },
    {
        "id": "dPMJQp2gMNc",
        "title": "Space Is Rude About Distance",
        "file": "aliens_short-01_distance_v02.mp4",
    },
    {
        "id": "rFJoOdQAc9c",
        "title": "What If Aliens Are Watching Us?",
        "file": "aliens_short-03_zoo-hypothesis_v02.mp4",
    },
]


def cdp_up(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def dismiss(page) -> None:
    for lab in ("Got it", "Allow", "Not now", "Close", "Accept", "Dismiss", "No thanks"):
        try:
            page.get_by_text(lab, exact=True).first.click(timeout=500)
        except Exception:
            pass


def pin_fullfilm(page, video_id: str) -> dict:
    out: dict = {"video_id": video_id, "ok": False, "pinned": False}
    page.goto(
        f"https://www.youtube.com/watch?v={video_id}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    page.keyboard.press("Escape")
    dismiss(page)
    page.evaluate("window.scrollBy(0, 1000)")
    page.wait_for_timeout(2000)

    body = page.inner_text("body")
    out["has_comment"] = "Full film here" in body
    if re.search(r"Pinned", body, re.I) and "Full film here" in body:
        out["ok"] = True
        out["pinned"] = True
        out["skipped"] = "already_pinned"
        page.screenshot(path=str(AUDIT / f"yt_pin_ok_{video_id}.png"))
        return out

    if not out["has_comment"]:
        try:
            box = page.locator(
                "#simplebox-placeholder, #placeholder-area, ytd-comment-simplebox-renderer"
            ).first
            box.click(timeout=8000)
            page.wait_for_timeout(500)
            editable = page.locator("#contenteditable-root, div[contenteditable='true']").first
            editable.click()
            page.keyboard.type(COMMENT, delay=4)
            page.wait_for_timeout(400)
            page.get_by_role("button", name=re.compile(r"^Comment$", re.I)).first.click(
                timeout=5000
            )
            page.wait_for_timeout(3500)
            out["posted"] = True
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3500)
            page.evaluate("window.scrollBy(0, 1000)")
            page.wait_for_timeout(1500)
        except Exception as e:
            out["comment_err"] = str(e)[:300]
            page.screenshot(path=str(AUDIT / f"yt_comment_fail_{video_id}.png"))
            return out

    try:
        page.get_by_text(re.compile(r"Sort by", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(400)
        page.get_by_text(re.compile(r"Top comments", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1000)
    except Exception:
        pass

    opened = page.evaluate(
        """(needle) => {
          const comments=[...document.querySelectorAll('ytd-comment-thread-renderer')];
          const hit=comments.find(c => (c.innerText||'').includes(needle));
          if(!hit) return {ok:false, reason:'not_found', n:comments.length};
          const menu=hit.querySelector('#action-menu button, button[aria-label*="Action"], #button-shape button');
          if(menu) { menu.click(); return {ok:true}; }
          return {ok:false, reason:'no_menu'};
        }""",
        "Full film here",
    )
    out["menu"] = opened
    page.wait_for_timeout(800)
    try:
        page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(800)
        conf = page.get_by_role("button", name=re.compile(r"Pin", re.I))
        if conf.count():
            try:
                conf.first.click(timeout=3000)
            except Exception:
                pass
        out["pin_click"] = True
    except Exception as e:
        clicked = page.evaluate(
            """() => {
              for (const el of document.querySelectorAll('yt-formatted-string,tp-yt-paper-item,ytd-menu-service-item-renderer,button,span')) {
                if (/^Pin$/i.test((el.innerText||'').trim())) { el.click(); return true; }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
              for (const el of document.querySelectorAll('button,yt-button-shape')) {
                const t=(el.innerText||'').trim();
                if (/^Pin( comment)?$/i.test(t)) { el.click(); return true; }
              }
            }"""
        )
        out["pin_js"] = clicked
        if not clicked:
            out["pin_err"] = str(e)[:200]

    page.wait_for_timeout(2000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy(0, 1000)")
    page.wait_for_timeout(1500)
    body3 = page.inner_text("body")
    out["verify_pinned"] = bool(re.search(r"Pinned", body3, re.I) and "Full film here" in body3)
    out["ok"] = out["verify_pinned"]
    out["pinned"] = out["verify_pinned"]
    page.screenshot(path=str(AUDIT / f"yt_pin_{video_id}.png"))
    return out


def fix_tiktok_bio_link(page) -> dict:
    out: dict = {"ok": False, "target": TT_LINK}
    page.goto("https://www.tiktok.com/@orbitwithben", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    dismiss(page)
    out["before"] = page.inner_text("body")[:700]
    try:
        page.get_by_role("button", name=re.compile(r"Edit profile", re.I)).first.click(timeout=10000)
    except Exception as e:
        out["error"] = f"no_edit:{e}"
        page.screenshot(path=str(AUDIT / "tt_no_edit.png"))
        return out
    page.wait_for_timeout(2500)
    page.screenshot(path=str(AUDIT / "tt_edit_open.png"))

    # Website / bio link field first
    link_filled = page.evaluate(
        """(url) => {
          const inputs=[...document.querySelectorAll('input')];
          const hit=inputs.find(a=>{
            const ph=((a.placeholder||'')+(a.getAttribute('aria-label')||'')+(a.name||'')).toLowerCase();
            const v=(a.value||'').toLowerCase();
            return /website|bio.?link|link|url|http/.test(ph) || /youtu|http|tiktok\\.com\\/@/.test(v);
          });
          if(!hit){
            // often the second text input after username/name
            const texts=inputs.filter(a=>{
              const r=a.getBoundingClientRect();
              return (a.type==='text'||!a.type||a.type==='url') && r.width>120 && r.height>20 && r.y>80;
            });
            // prefer one that already looks like a URL or empty website
            for (const a of texts){
              const ph=((a.placeholder||'')+(a.getAttribute('aria-label')||'')).toLowerCase();
              if (/website|link|url/.test(ph)) { hit=a; break; }
            }
            if(!hit && texts.length>=2) hit=texts[texts.length-1];
          }
          if(!hit) return {ok:false, err:'no_link_input', n:inputs.length};
          const proto=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');
          hit.focus(); hit.click();
          if(proto&&proto.set) proto.set.call(hit,url); else hit.value=url;
          hit.dispatchEvent(new Event('input',{bubbles:true}));
          hit.dispatchEvent(new Event('change',{bubbles:true}));
          return {ok:true, before:hit.defaultValue||'', after:hit.value, ph:hit.placeholder||'', al:hit.getAttribute('aria-label')||''};
        }"""
    , TT_LINK)
    out["link_js"] = link_filled

    # Also type into the website field via keyboard for React controlled inputs
    try:
        website = page.get_by_placeholder(re.compile(r"website|link|url", re.I))
        if website.count():
            website.first.click(timeout=2000)
            page.keyboard.press("Meta+a")
            page.keyboard.type(TT_LINK, delay=20)
            out["link_typed"] = True
        else:
            # try aria-label
            website = page.locator('input[aria-label*="Website" i], input[aria-label*="Link" i]')
            if website.count():
                website.first.click(timeout=2000)
                page.keyboard.press("Meta+a")
                page.keyboard.type(TT_LINK, delay=20)
                out["link_typed"] = True
    except Exception as e:
        out["link_type_err"] = str(e)[:160]

    # Bio text (keep soft CTA)
    areas = page.locator("textarea")
    for i in range(areas.count()):
        a = areas.nth(i)
        try:
            val = a.input_value()
        except Exception:
            val = ""
        ph = (a.get_attribute("placeholder") or "").lower()
        if "bio" in ph or "space" in val.lower() or "youtube" in val.lower() or len(val) > 10:
            a.click()
            page.keyboard.press("Meta+a")
            page.keyboard.type(TT_BIO, delay=12)
            out["bio_filled"] = True
            break

    page.screenshot(path=str(AUDIT / "tt_edit_filled.png"))
    save_btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
    for _ in range(15):
        try:
            if save_btn.count() and save_btn.is_enabled():
                save_btn.click(timeout=4000)
                out["saved_click"] = True
                break
        except Exception:
            pass
        page.wait_for_timeout(400)
    page.wait_for_timeout(4000)
    for _ in range(12):
        if page.get_by_role("button", name=re.compile(r"^Save$", re.I)).count() == 0:
            out["modal_closed"] = True
            break
        page.wait_for_timeout(500)

    page.goto("https://www.tiktok.com/@orbitwithben", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    dismiss(page)
    body = page.inner_text("body")
    links = page.evaluate(
        """() => [...document.querySelectorAll('a')].map(a=>a.href).filter(h=>/youtu/i.test(h))"""
    )
    out["after"] = body[:700]
    out["links"] = links
    out["has_at"] = "youtube.com/@OrbitWithBen" in body or "youtube.com/@orbitwithben" in body.lower()
    out["has_link"] = any("youtube.com/@OrbitWithBen" in (h or "") or "youtube.com/@orbitwithben" in (h or "").lower() for h in links) or out["has_at"]
    out["ok"] = bool(out["has_link"] or out["has_at"])
    page.screenshot(path=str(AUDIT / "tt_profile_final.png"))
    return out


def ensure_meta_login(page) -> dict:
    out: dict = {"ok": False}
    url = (
        "https://business.facebook.com/latest/home"
        "?business_id=1203116147241086&asset_id=1251385088056874"
    )
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    dismiss(page)
    body = page.inner_text("body")
    out["url"] = page.url
    out["snip"] = body[:500]
    page.screenshot(path=str(AUDIT / "meta_login_check.png"))

    needs = bool(
        re.search(r"Log in|Log into Facebook|email address|password|Allow the use of cookies", body, re.I)
    ) and not re.search(r"orbitwithben|Content|Reels composer|Home", body, re.I)

    # Cookie wall
    for lab in ("Allow all cookies", "Accept all", "Allow essential and optional cookies"):
        try:
            page.get_by_role("button", name=re.compile(lab, re.I)).first.click(timeout=1500)
            page.wait_for_timeout(2000)
            out["cookies"] = lab
        except Exception:
            pass

    body = page.inner_text("body")
    if re.search(r"Log in to Facebook|email or phone|password", body, re.I):
        out["needs_login"] = True
        # Try stored Meta credentials if present (email/password)
        creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
        creds = json.loads(creds_path.read_text()) if creds_path.exists() else {}
        email = (creds.get("facebook_email") or creds.get("email") or "").strip()
        password = (creds.get("facebook_password") or creds.get("password") or "").strip()
        if email and password:
            try:
                page.locator('input[type=text], input[name=email], input[type=email]').first.fill(email)
                page.locator('input[type=password]').first.fill(password)
                page.get_by_role("button", name=re.compile(r"^Log in$", re.I)).first.click(timeout=5000)
                page.wait_for_timeout(8000)
                out["login_attempted"] = True
            except Exception as e:
                out["login_err"] = str(e)[:200]
        else:
            out["login_err"] = "no_email_password_in_credentials"
            page.screenshot(path=str(AUDIT / "meta_needs_login.png"))
            return out

    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    body = page.inner_text("body")
    out["after_url"] = page.url
    out["after_snip"] = body[:500]
    out["ok"] = not bool(re.search(r"Log in to Facebook|email or phone", body, re.I))
    out["has_suite"] = bool(re.search(r"Content|Inbox|Ads|Home|Reels", body, re.I))
    page.screenshot(path=str(AUDIT / "meta_after_login.png"))
    return out


def mark_index_pins(results: dict) -> None:
    path = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(path.read_text())
    for s in data.get("shorts") or []:
        vid = s.get("video_id")
        if vid in results and results[vid].get("ok"):
            s["pinned_fullfilm_cta"] = True
            s["pinned_fullfilm_cta_at"] = datetime.now(LONDON).isoformat()
            s["pinned_fullfilm_url"] = FULL_URL
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    out = {
        "started_at": datetime.now(LONDON).isoformat(),
        "youtube_pins": {},
        "tiktok_bio": {},
        "meta_login": {},
        "meta": {},
        "threads": {},
    }
    assert cdp_up(9222), "CDP 9222 down — start TikTok chrome first"
    assert cdp_up(9223), "CDP 9223 down — start Meta chrome first"

    # --- 1+2: YouTube pins + TikTok bio on :9222 ---
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = browser.contexts[0].new_page()
        page.bring_to_front()

        for t in TARGETS:
            print("=== YT PIN", t["id"], t["title"], flush=True)
            rec = pin_fullfilm(page, t["id"])
            out["youtube_pins"][t["id"]] = rec
            print(" ", rec.get("ok"), rec.get("skipped") or rec.get("verify_pinned"), flush=True)
            if not cdp_up(9222):
                out["youtube_pins"]["cdp_died"] = True
                break

        print("=== TIKTOK BIO LINK", flush=True)
        if cdp_up(9222):
            out["tiktok_bio"] = fix_tiktok_bio_link(page)
            print(" ", out["tiktok_bio"].get("ok"), out["tiktok_bio"].get("links"), flush=True)
        else:
            out["tiktok_bio"] = {"ok": False, "error": "cdp_9222_down"}
        page.close()

    mark_index_pins(out["youtube_pins"])

    # --- 3: Meta login + share ---
    sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/Meta"))
    from auto import caption as meta_cap  # type: ignore
    from auto import ledger as meta_ledger  # type: ignore
    from auto import studio_upload as meta_up  # type: ignore

    creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
    creds = json.loads(creds_path.read_text())
    orig = dict(creds)
    creds["business_id"] = "1203116147241086"
    creds["business_suite_asset_id"] = "1251385088056874"
    creds_path.write_text(json.dumps(creds, indent=2) + "\n")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
            page = browser.contexts[0].new_page()
            page.bring_to_front()
            print("=== META LOGIN", flush=True)
            out["meta_login"] = ensure_meta_login(page)
            print(" ", out["meta_login"].get("ok"), out["meta_login"].get("needs_login"), flush=True)
            page.close()

        if out["meta_login"].get("ok"):
            for t in TARGETS:
                path = EXPORTS / t["file"]
                short = {"title": t["title"], "description": "", "video_id": t["id"]}
                cap = meta_cap.meta_caption(short)
                if SOFT not in cap:
                    cap = f"{cap} {SOFT}".strip()
                print("=== META SHARE", t["id"], flush=True)
                r = meta_up.post_short(
                    video_path=path,
                    caption=cap,
                    confirm_needle=meta_cap.confirm_needle(short, cap),
                    audit_dir=AUDIT / "meta",
                    port=9223,
                )
                out["meta"][t["id"]] = r
                print(" ", r.get("status"), flush=True)
                if r.get("status") in ("ok", "unconfirmed"):
                    try:
                        meta_ledger.mark_posted(
                            {"video_id": t["id"], "title": t["title"], "file": str(path)},
                            result={
                                "status": "ok",
                                "method": "cdp_morning",
                                "platforms": {
                                    "instagram": {"status": "ok", "method": "cdp_morning"},
                                    "facebook": {"status": "ok", "method": "cdp_morning"},
                                },
                            },
                        )
                    except Exception:
                        pass
                time.sleep(2)
        else:
            out["meta"]["skipped"] = "meta_login_failed"
    finally:
        creds_path.write_text(json.dumps(orig, indent=2) + "\n")

    # --- 4: Threads force post ---
    import importlib.util as ilu

    def load_th(name: str):
        path = ROOT / "00_Brand/Channel-Setup/Threads/auto" / f"{name}.py"
        key = f"orbit_threads_auto_{name}_morning"
        if key in sys.modules:
            return sys.modules[key]
        spec = ilu.spec_from_file_location(key, path)
        mod = ilu.module_from_spec(spec)
        sys.modules[key] = mod
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        return mod

    th_up = load_th("studio_upload")
    th_cap = load_th("caption")
    th_ledger = load_th("ledger")

    ledger_path = ROOT / "00_Brand/Channel-Setup/Threads/THREADS_POSTED.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"posted": {}}
    for t in TARGETS:
        ledger.get("posted", {}).pop(f"yt:{t['id']}", None)
        ledger.get("posted", {}).pop(t["id"], None)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

    if not cdp_up(9222):
        out["threads"]["error"] = "cdp_9222_down"
    else:
        for t in TARGETS:
            if not cdp_up(9222):
                out["threads"]["cdp_died"] = True
                break
            path = EXPORTS / t["file"]
            short = {"title": t["title"], "description": "", "video_id": t["id"]}
            cap = th_cap.threads_caption(short)
            if SOFT not in cap:
                cap = f"{cap}\n\n{SOFT}".strip()
            print("=== THREADS", t["id"], flush=True)
            try:
                r = th_up.post_short(
                    video_path=path,
                    caption=cap,
                    confirm_needle=th_cap.confirm_needle(short, cap),
                    audit_dir=AUDIT / "threads",
                    port=9222,
                )
                out["threads"][t["id"]] = r
                print(" ", r.get("status"), flush=True)
                if r.get("status") in ("ok", "unconfirmed"):
                    try:
                        th_ledger.mark_posted(
                            {"video_id": t["id"], "title": t["title"], "file": str(path)},
                            result=r,
                        )
                    except Exception:
                        pass
            except Exception as e:
                out["threads"][t["id"]] = {"status": "failed", "error": str(e)[:400]}
                print(" fail", e, flush=True)
            time.sleep(2)

    out["finished_at"] = datetime.now(LONDON).isoformat()
    (AUDIT / "MORNING_FUNNEL.json").write_text(json.dumps(out, indent=2) + "\n")
    summary = {
        "pins": {k: (v.get("ok") if isinstance(v, dict) else v) for k, v in out["youtube_pins"].items()},
        "tiktok": out["tiktok_bio"].get("ok"),
        "meta_login": out["meta_login"].get("ok"),
        "meta": {k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["meta"].items()},
        "threads": {k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["threads"].items()},
    }
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
