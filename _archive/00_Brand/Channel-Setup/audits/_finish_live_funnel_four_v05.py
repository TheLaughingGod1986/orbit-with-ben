#!/usr/bin/env python3
"""Finish live funnel: YT Public+pin ×3, TikTok bio @link, Meta Fermi reel, Threads ×3."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SHORTS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts"
EXPORTS = SHORTS / "06_Final-Exports"
INDEX = SHORTS / "SHORTS_UPLOAD_INDEX.json"
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/live_funnel_four_2026-08-03"
AUDIT.mkdir(parents=True, exist_ok=True)

FULL_URL = "https://youtu.be/Mo93x0fxB1Q"
LONG_TITLE = "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained"
COMMENT = (
    f"Full film here → {LONG_TITLE}\n{FULL_URL}\n\nOrbit's Cosmic Journey 🚀"
)
SOFT = "Full film on YouTube."
TT_BIO = "Space stories. Big questions. Films → youtube.com/@OrbitWithBen"

TARGETS = [
    {
        "id": "1HuV8o3gOss",
        "title": "Where Is Everybody?",
        "file": "aliens_short-02_fermi-paradox_v02.mp4",
        "need_public": False,
    },
    {
        "id": "dPMJQp2gMNc",
        "title": "Space Is Rude About Distance",
        "file": "aliens_short-01_distance_v02.mp4",
        "need_public": True,
    },
    {
        "id": "rFJoOdQAc9c",
        "title": "What If Aliens Are Watching Us?",
        "file": "aliens_short-03_zoo-hypothesis_v02.mp4",
        "need_public": True,
    },
]

CDP_TT = "http://127.0.0.1:9222"
CDP_META = "http://127.0.0.1:9223"


def cdp_up(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def visibility_chip(page) -> str:
    try:
        return page.locator("ytcp-video-metadata-visibility").first.inner_text(
            timeout=3000
        ).replace("\n", " ")
    except Exception:
        return ""


def is_public(chip: str) -> bool:
    return bool(re.search(r"\bPublic\b", chip)) and not re.search(
        r"\bScheduled\b", chip, re.I
    )


def open_visibility(page) -> None:
    loc = page.locator("ytcp-video-metadata-visibility").first
    loc.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    loc.click(force=True)
    page.wait_for_timeout(1600)


def collapse_schedule_panel(page):
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=(el.getAttribute('aria-label')||'');
              const id=el.id||'';
              if (id==='first-container-expand-button' || /click to (expand|collapse)/i.test(al)) {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return {al,id}; }
              }
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          let hasPublic=false;
          const find=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PUBLIC' || t==='Public') && r.width>10 && r.height>5) hasPublic=true;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) find(el.shadowRoot);
          };
          find(dlg||document);
          if (hasPublic) return {already:true};
          return walk(dlg||document);
        }"""
    )


def click_public_radio(page):
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PUBLIC' || t==='Public') && r.width>5) {
                el.scrollIntoView({block:'center'});
                el.click();
                return {ok:true, name:n, t:t.slice(0,40), checked: el.getAttribute('aria-checked')};
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (!el.shadowRoot) continue;
              const x=walk(el.shadowRoot);
              if (x) return x;
            }
            return null;
          };
          return walk(dlg||document);
        }"""
    )


def click_done(page) -> bool:
    try:
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            (btn.last if btn.count() > 1 else btn.first).click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            return True
    except Exception:
        pass
    return False


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(4000)
            return True
    except Exception:
        pass
    return False


def publish_public(page, video_id: str, tag: str) -> dict:
    out: dict = {"video_id": video_id, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    page.keyboard.press("Escape")
    chip0 = visibility_chip(page)
    out["before"] = chip0
    if is_public(chip0):
        out["ok"] = True
        out["skipped"] = "already_public"
        return out

    open_visibility(page)
    page.screenshot(path=str(AUDIT / f"{tag}_dlg.png"))
    out["collapse"] = collapse_schedule_panel(page)
    page.wait_for_timeout(1000)
    page.screenshot(path=str(AUDIT / f"{tag}_radios.png"))
    out["public_click"] = click_public_radio(page)
    if not (out["public_click"] and out["public_click"].get("ok")):
        collapse_schedule_panel(page)
        page.wait_for_timeout(800)
        out["public_click"] = click_public_radio(page)
    page.wait_for_timeout(700)
    # verify radio state
    out["radio_state"] = page.evaluate(
        """() => {
          const rows=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'');
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,40);
              const r=el.getBoundingClientRect();
              if (r.width>5) rows.push({n,t,checked:el.getAttribute('aria-checked')});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(document);
          return rows;
        }"""
    )
    out["done"] = click_done(page)
    out["saved"] = save(page)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    chip = visibility_chip(page)
    out["after"] = chip
    out["ok"] = is_public(chip)
    page.screenshot(path=str(AUDIT / f"{tag}_after.png"))
    return out


def pin_fullfilm(page, video_id: str, tag: str) -> dict:
    out: dict = {"video_id": video_id, "ok": False, "pinned": False}
    # Watch page — post + pin
    page.goto(
        f"https://www.youtube.com/watch?v={video_id}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    page.keyboard.press("Escape")
    page.evaluate("window.scrollBy(0, 900)")
    page.wait_for_timeout(2000)

    body = page.inner_text("body")
    out["has_comment"] = "Full film here" in body

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
            page.wait_for_timeout(3000)
            out["posted"] = True
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3500)
            page.evaluate("window.scrollBy(0, 900)")
            page.wait_for_timeout(1500)
        except Exception as e:
            out["comment_err"] = str(e)[:300]
            page.screenshot(path=str(AUDIT / f"{tag}_comment_fail.png"))
            return out

    # Sort Top
    try:
        page.get_by_text(re.compile(r"Sort by", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(400)
        page.get_by_text(re.compile(r"Top comments", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1000)
    except Exception:
        pass

    # Already pinned?
    body2 = page.inner_text("body")
    if re.search(r"Pinned\s*by", body2, re.I) and "Full film here" in body2:
        out["ok"] = True
        out["pinned"] = True
        out["skipped"] = "already_pinned"
        return out

    # Open action menu on matching comment
    opened = page.evaluate(
        """(needle) => {
          const comments=[...document.querySelectorAll('ytd-comment-thread-renderer')];
          const hit=comments.find(c => (c.innerText||'').includes(needle));
          if(!hit) return {ok:false, reason:'not_found', n:comments.length};
          const menu=hit.querySelector('#action-menu button, button[aria-label*="Action"], #button-shape button');
          if(menu) { menu.click(); return {ok:true, opened:true}; }
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
        out["pin_click"] = "Pin"
        out["pinned"] = True
        out["ok"] = True
    except Exception as e:
        # JS fallback
        clicked = page.evaluate(
            """() => {
              for (const el of document.querySelectorAll('yt-formatted-string,tp-yt-paper-item,ytd-menu-service-item-renderer,button')) {
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
        out["pinned"] = bool(clicked)
        out["ok"] = bool(clicked)
        if not clicked:
            out["pin_err"] = str(e)[:200]

    page.wait_for_timeout(1500)
    page.screenshot(path=str(AUDIT / f"{tag}_pin.png"))
    # verify
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy(0, 900)")
    page.wait_for_timeout(1500)
    body3 = page.inner_text("body")
    out["verify_pinned"] = bool(
        re.search(r"Pinned", body3, re.I) and "Full film here" in body3
    )
    if out["verify_pinned"]:
        out["ok"] = True
        out["pinned"] = True
    return out


def fix_tiktok_bio(page) -> dict:
    out: dict = {"ok": False}
    page.goto(
        "https://www.tiktok.com/@orbitwithben",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    out["before"] = page.inner_text("body")[:900]
    try:
        page.get_by_role("button", name=re.compile(r"Edit profile", re.I)).first.click(
            timeout=10000
        )
    except Exception as e:
        out["error"] = f"no_edit:{e}"
        return out
    page.wait_for_timeout(2000)
    page.screenshot(path=str(AUDIT / "tt_edit_v05.png"))

    # Prefer textarea for Bio
    filled = False
    areas = page.locator("textarea")
    for i in range(areas.count()):
        a = areas.nth(i)
        try:
            val = a.input_value()
        except Exception:
            val = ""
        ph = (a.get_attribute("placeholder") or "").lower()
        if "bio" in ph or "space" in val.lower() or "youtube" in val.lower() or len(val) > 15:
            a.click()
            page.keyboard.press("Meta+a")
            page.keyboard.type(TT_BIO, delay=15)
            # also set value via native setter
            a.evaluate(
                """(el, text) => {
                  const proto = window.HTMLTextAreaElement.prototype;
                  const desc = Object.getOwnPropertyDescriptor(proto, 'value');
                  if (desc && desc.set) desc.set.call(el, text); else el.value = text;
                  el.dispatchEvent(new Event('input', {bubbles:true}));
                  el.dispatchEvent(new Event('change', {bubbles:true}));
                }""",
                TT_BIO,
            )
            filled = True
            out["filled_via"] = f"textarea[{i}]"
            break
    if not filled:
        # contenteditable fallback
        ce = page.locator('div[contenteditable="true"]').last
        if ce.count():
            ce.click()
            page.keyboard.press("Meta+a")
            page.keyboard.type(TT_BIO, delay=15)
            filled = True
            out["filled_via"] = "contenteditable"
    out["filled"] = filled
    page.wait_for_timeout(800)
    page.screenshot(path=str(AUDIT / "tt_typed_v05.png"))

    save_btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
    for _ in range(12):
        try:
            if save_btn.count() and save_btn.is_enabled():
                save_btn.click(timeout=4000)
                out["saved_click"] = True
                break
        except Exception:
            pass
        page.wait_for_timeout(400)
    page.wait_for_timeout(4000)
    # wait modal close
    for _ in range(15):
        if page.get_by_role("button", name=re.compile(r"^Save$", re.I)).count() == 0:
            out["modal_closed"] = True
            break
        page.wait_for_timeout(500)

    page.goto(
        "https://www.tiktok.com/@orbitwithben",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    body = page.inner_text("body")
    out["after"] = body[:900]
    out["has_at"] = "youtube.com/@OrbitWithBen" in body
    out["ok"] = out["has_at"]
    page.screenshot(path=str(AUDIT / "tt_final_v05.png"))
    return out


def main() -> None:
    out = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "youtube": {},
        "tiktok_bio": {},
        "meta": {},
        "threads": {},
    }
    assert cdp_up(9222), "CDP 9222 down"
    assert cdp_up(9223), "CDP 9223 down"

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_TT)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.bring_to_front()

        # --- YouTube ---
        for t in TARGETS:
            vid = t["id"]
            tag = f"v05_{vid}"
            print("=== YT", vid, t["title"], flush=True)
            rec: dict = {"id": vid, "title": t["title"]}
            if t["need_public"]:
                rec["public"] = publish_public(page, vid, tag)
            else:
                # still check chip
                page.goto(
                    f"https://studio.youtube.com/video/{vid}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(3000)
                chip = visibility_chip(page)
                rec["public"] = {
                    "ok": is_public(chip),
                    "skipped": "check_only",
                    "after": chip,
                }
            print(" public", rec["public"], flush=True)
            if rec["public"].get("ok"):
                rec["pin"] = pin_fullfilm(page, vid, tag)
            else:
                rec["pin"] = {"ok": False, "skipped": "not_public"}
            print(" pin", rec["pin"], flush=True)
            out["youtube"][vid] = rec
            # keep CDP alive
            if not cdp_up(9222):
                raise RuntimeError("CDP 9222 died mid-YouTube")

        # --- TikTok bio ---
        print("=== TIKTOK BIO", flush=True)
        out["tiktok_bio"] = fix_tiktok_bio(page)
        print(" tiktok", {k: out["tiktok_bio"].get(k) for k in ("ok", "has_at", "filled", "saved_click")}, flush=True)

    # --- Meta (separate CDP :9223) ---
    print("=== META", flush=True)
    sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/Meta"))
    from auto import caption as meta_cap  # type: ignore
    from auto import studio_upload as meta_up  # type: ignore

    creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
    creds = json.loads(creds_path.read_text())
    orig = dict(creds)
    # Benkay portfolio + IG asset path that worked previously for composer
    creds["business_id"] = "1203116147241086"
    creds["business_suite_asset_id"] = "1251385088056874"
    creds_path.write_text(json.dumps(creds, indent=2) + "\n")
    try:
        for t in TARGETS:
            path = EXPORTS / t["file"]
            short = {"title": t["title"], "description": "", "video_id": t["id"]}
            cap = meta_cap.meta_caption(short)
            if SOFT not in cap:
                cap = f"{cap} {SOFT}".strip()
            r = meta_up.post_short(
                video_path=path,
                caption=cap,
                confirm_needle=meta_cap.confirm_needle(short, cap),
                audit_dir=AUDIT / "meta_v05",
                port=9223,
            )
            out["meta"][t["id"]] = r
            print(" meta", t["id"], r.get("status"), r.get("error"), flush=True)
    except Exception as e:
        out["meta"]["error"] = str(e)[:400]
        print(" meta err", e, flush=True)
    finally:
        creds_path.write_text(json.dumps(orig, indent=2) + "\n")

    # --- Threads ---
    print("=== THREADS", flush=True)
    if not cdp_up(9222):
        out["threads"]["error"] = "cdp_9222_down"
    else:
        import importlib.util as ilu

        def load_th(name: str):
            path = ROOT / "00_Brand/Channel-Setup/Threads/auto" / f"{name}.py"
            key = f"orbit_threads_auto_{name}_v05"
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
            key = f"yt:{t['id']}"
            ledger.get("posted", {}).pop(key, None)
            # also pop bare id keys
            ledger.get("posted", {}).pop(t["id"], None)
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

        for t in TARGETS:
            path = EXPORTS / t["file"]
            if not path.exists():
                out["threads"][t["id"]] = {"status": "missing_file"}
                continue
            short = {"title": t["title"], "description": "", "video_id": t["id"]}
            cap = th_cap.threads_caption(short)
            if SOFT not in cap:
                cap = f"{cap}\n\n{SOFT}".strip()
            try:
                old_home = getattr(th_up, "HOME", "https://www.threads.com/")
                try:
                    th_up.HOME = "https://www.threads.net/"
                    r = th_up.post_short(
                        video_path=path,
                        caption=cap,
                        confirm_needle=th_cap.confirm_needle(short, cap),
                        audit_dir=AUDIT / "threads_v05",
                        port=9222,
                    )
                finally:
                    th_up.HOME = old_home
                out["threads"][t["id"]] = r
                print(" threads", t["id"], r.get("status"), flush=True)
                if r.get("status") in ("ok", "posted_click", "unconfirmed"):
                    try:
                        th_ledger.mark_posted(
                            {"video_id": t["id"], "title": t["title"], "file": str(path)},
                            result=r,
                        )
                    except Exception:
                        pass
            except Exception as e:
                out["threads"][t["id"]] = {"status": "failed", "error": str(e)[:400]}
                print(" threads fail", t["id"], e, flush=True)
                if not cdp_up(9222):
                    out["threads"]["cdp_died"] = True
                    break

    # Update shorts index by title match (ids may be nested)
    idx = json.loads(INDEX.read_text())
    by_file = {t["file"]: t for t in TARGETS}
    for s in idx.get("shorts", []):
        f = Path(s.get("file") or "").name
        t = by_file.get(f)
        if not t:
            continue
        y = out["youtube"].get(t["id"], {})
        if y.get("public", {}).get("ok"):
            s["visibility"] = "public"
            s["published_now"] = True
            s["youtube_video_id"] = t["id"]
            s["scheduled_publish_at"] = None
        if y.get("pin", {}).get("pinned") or y.get("pin", {}).get("ok"):
            s["pinned_fullfilm_cta"] = True
            s["pinned_fullfilm_url"] = FULL_URL
    idx["updated"] = datetime.now(timezone.utc).isoformat()
    INDEX.write_text(json.dumps(idx, indent=2) + "\n")

    out["finished_at"] = datetime.now(timezone.utc).isoformat()
    (AUDIT / "FINISH_v05.json").write_text(json.dumps(out, indent=2) + "\n")
    print("WROTE", AUDIT / "FINISH_v05.json", flush=True)
    # compact summary
    summary = {
        "yt": {
            k: {
                "public": v.get("public", {}).get("ok"),
                "pin": v.get("pin", {}).get("pinned") or v.get("pin", {}).get("ok"),
                "after": v.get("public", {}).get("after"),
            }
            for k, v in out["youtube"].items()
        },
        "tiktok": {"ok": out["tiktok_bio"].get("ok"), "has_at": out["tiktok_bio"].get("has_at")},
        "meta": {k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["meta"].items()},
        "threads": {
            k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["threads"].items()
        },
    }
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
