#!/usr/bin/env python3
raise SystemExit(
    "DISABLED: _cleanup_visibility_cdp.py uses INVERTED canonical IDs "
    "(promotes RCs6MMxF3ko/IwpO33AJaPQ and demotes 3xrxdmaOwJI/JRfhE6yWom4/L2OFjL4neOo). "
    "This caused shelf drift. Use APPROVED FINAL_SHELF_VERIFY canonicals only. "
    "See FULL_CATALOGUE_REPAIR_REPORT.md."
)


# --- ORIGINAL QUARANTINED SOURCE BELOW ---
#!/usr/bin/env python3
"""Orbit cleanup: restore canonical public shelf + privatize/hold duplicates.

ONE VIDEO = ONE UPLOAD. Uses Studio CDP (API lacks force-ssl update scope).

Canonical KEEP PUBLIC:
  longs:  Mo93x0fxB1Q, RCs6MMxF3ko   # RCs6 = smooth-CFR BH long
  shorts: 1HuV8o3gOss, KcKBixwmcV4, IwpO33AJaPQ  # IwpO = smooth BH launch

FORCE PRIVATE (and clear schedule):
  3xrxdmaOwJI  — old juddery BH long (pre-smooth)
  JRfhE6yWom4, L2OFjL4neOo — old BH Shorts superseded by smooth IDs
  n7CbJrOCnU0 — private sped master
  # Do NOT private RCs6MMxF3ko / IwpO33AJaPQ / smooth schedule batch
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
    "11_Upload-Package/Schedule/_force_schedule_shorts_v01.py"
)
OUT_DIR = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07"
)
OUT = OUT_DIR / "CLEANUP_VISIBILITY_RESULT.json"
AUDIT = OUT_DIR / "cdp_shots"

FORCE_PRIVATE = [
    "3xrxdmaOwJI",
    "n7CbJrOCnU0",
    "JRfhE6yWom4",
    "L2OFjL4neOo",
    "tUAdhOnMW2g",
    "svYOx07OrIM",
    "B2STcIAF1lY",
    "w1ej9u0rPTA",
]

RESTORE_PUBLIC = [
    "RCs6MMxF3ko",
    "IwpO33AJaPQ",
    "IqII5mVGdrs",
]


def load_helper():
    spec = importlib.util.spec_from_file_location("force_sched", HELPER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def visibility_chip(page) -> str:
    try:
        el = page.locator("ytcp-video-metadata-visibility").first
        el.scroll_into_view_if_needed(timeout=4000)
        return el.inner_text(timeout=4000).replace("\n", " ").strip()
    except Exception as e:
        return f"err:{e}"[:80]


def classify(chip: str) -> str:
    c = chip.lower()
    if "scheduled" in c:
        return "scheduled"
    if "private" in c:
        return "private"
    if "public" in c:
        return "public"
    if "unlisted" in c:
        return "unlisted"
    return "unknown"


def click_privacy_radio(page, label: str) -> dict | None:
    """Click Public/Private radio inside visibility dialog."""
    hit = page.evaluate(
        """(label) => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const root=dlg||document;
          const cands=[];
          const re = new RegExp('^' + label + '\\\\b', 'i');
          const walk=(node)=>{
            for (const el of node.querySelectorAll('tp-yt-paper-radio-button,[role=radio],ytcp-radio,label,div')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const al=el.getAttribute('aria-label')||'';
              if (!(t===label || re.test(t) || re.test(al))) continue;
              const r=el.getBoundingClientRect();
              if (r.width>30 && r.height>10 && r.height<120 && r.y>80) {
                cands.push({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,40)});
              }
            }
            for (const el of node.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(root);
          cands.sort((a,b)=>a.y-b.y || a.x-b.x);
          return cands[0] || null;
        }""",
        label,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(500)
    try:
        page.get_by_role("radio", name=re.compile(rf"^{label}", re.I)).first.click(
            force=True, timeout=1500
        )
    except Exception:
        pass
    return hit


def save_all(mod, page) -> bool:
    saved = False
    try:
        saved = bool(mod.save_edit(page))
    except Exception:
        saved = False
    if not saved:
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button, ytcp-button')) {
                const t=(b.innerText||'').trim();
                if (/^Save$/i.test(t) && !b.disabled) { b.click(); return t; }
              }
              return null;
            }"""
        )
        page.wait_for_timeout(2800)
        saved = True
    return saved


def set_visibility(mod, page, video_id: str, target: str) -> dict:
    """target: private | public"""
    result = {"id": video_id, "target": target, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    mod.skip(page)
    mod.dismiss(page)
    body = page.locator("body").inner_text()
    if "Sign in" in body[:800] and "Email or phone" in body:
        result["error"] = "login_wall"
        return result
    if "don't have permission" in body.lower():
        result["error"] = "no_permission"
        return result

    chip0 = visibility_chip(page)
    vis0 = classify(chip0)
    result["before"] = {"chip": chip0[:160], "vis": vis0}

    if target == "private" and vis0 == "private":
        result["skipped"] = "already_private"
        result["ok"] = True
        return result
    if target == "public" and vis0 == "public":
        result["skipped"] = "already_public"
        result["ok"] = True
        return result

    try:
        mod.open_visibility(page)
    except Exception as e:
        result["open_err"] = str(e)[:160]
        try:
            page.locator("ytcp-video-metadata-visibility").first.click(force=True)
            page.wait_for_timeout(1200)
        except Exception as e2:
            result["open_err2"] = str(e2)[:120]
            return result

    page.screenshot(path=str(AUDIT / f"{video_id}_01_dialog.png"))
    label = "Private" if target == "private" else "Public"
    hit = click_privacy_radio(page, label)
    result["radio_hit"] = hit
    page.wait_for_timeout(600)
    page.screenshot(path=str(AUDIT / f"{video_id}_02_selected.png"))

    try:
        mod.click_done(page)
    except Exception:
        try:
            page.get_by_role("button", name=re.compile(r"^Done$", re.I)).first.click(
                timeout=2000
            )
        except Exception as e:
            result["done_err"] = str(e)[:120]

    page.wait_for_timeout(800)
    result["saved"] = save_all(mod, page)
    page.wait_for_timeout(2000)

    try:
        page.evaluate("() => { window.onbeforeunload=null; }")
    except Exception:
        pass
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3200)
    chip1 = visibility_chip(page)
    vis1 = classify(chip1)
    result["after"] = {"chip": chip1[:160], "vis": vis1}
    result["ok"] = vis1 == target
    page.screenshot(path=str(AUDIT / f"{video_id}_03_verify.png"))
    return result


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    mod = load_helper()
    results: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        # Auth check
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        body = page.locator("body").inner_text()
        if "Sign in" in body[:500] or "don't have permission" in body.lower():
            OUT.write_text(json.dumps({"fatal": "not_signed_in", "snip": body[:400]}, indent=2))
            print("FATAL not_signed_in")
            return 2
        print("AUTH_OK", flush=True)

        for vid in FORCE_PRIVATE:
            print(f"PRIVATE {vid}…", flush=True)
            try:
                r = set_visibility(mod, page, vid, "private")
            except Exception as e:
                r = {"id": vid, "target": "private", "ok": False, "error": str(e)[:400]}
            results.append(r)
            print(
                f"  → ok={r.get('ok')} before={r.get('before',{}).get('vis')} after={r.get('after',{}).get('vis')} skip={r.get('skipped')}",
                flush=True,
            )
            OUT.write_text(json.dumps({"items": results}, indent=2) + "\n")

        for vid in RESTORE_PUBLIC:
            print(f"PUBLIC  {vid}…", flush=True)
            try:
                r = set_visibility(mod, page, vid, "public")
            except Exception as e:
                r = {"id": vid, "target": "public", "ok": False, "error": str(e)[:400]}
            results.append(r)
            print(
                f"  → ok={r.get('ok')} before={r.get('before',{}).get('vis')} after={r.get('after',{}).get('vis')} skip={r.get('skipped')}",
                flush=True,
            )
            OUT.write_text(json.dumps({"items": results}, indent=2) + "\n")

        try:
            page.close()
        except Exception:
            pass

    ok = all(r.get("ok") for r in results)
    payload = {
        "ok": ok,
        "force_private": FORCE_PRIVATE,
        "restore_public": RESTORE_PUBLIC,
        "items": results,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print("ALL_OK" if ok else "NEEDS_ATTENTION", OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
