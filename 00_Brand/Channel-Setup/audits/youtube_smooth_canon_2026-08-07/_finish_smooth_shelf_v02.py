raise SystemExit("DISABLED: smooth-canon shelf mutators quarantined — use FINAL_SHELF_VERIFY canonicals (3xrxdmaOwJI / JRfhE6yWom4 / L2OFjL4neOo).")

#!/usr/bin/env python3
"""Finish smooth-CFR BH shelf: publicize smooth, private old (ABC + scheduled).

Uses Playwright persistent YouTube Studio profile (NOT TikTok CDP :9222).
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-from-chrome"
HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/Schedule/"
    "_force_schedule_shorts_v01.py"
)
CLEANUP = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07/_cleanup_visibility_cdp.py"
)
OUT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_smooth_canon_2026-08-07/FINISH_V02_RESULT.json"
)
AUDIT = OUT.parent / "shots_v02"

PUBLICIZE = [
    "RCs6MMxF3ko",
    "IwpO33AJaPQ",
    "IqII5mVGdrs",
]
FORCE_PRIVATE = [
    "3xrxdmaOwJI",  # ABC block
    "tUAdhOnMW2g",
    "svYOx07OrIM",
    "B2STcIAF1lY",
    "w1ej9u0rPTA",
]
KEEP_SCHEDULED = [
    "2C-eiSMsBLc",
    "lIHb_tyxQSM",
    "wOlnj7nZWJM",
    "2uT3wXJLybw",
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def dismiss_all(page) -> list[str]:
    hit = []
    for name in (
        r"^Continue$",
        r"^Stop test$",
        r"^Stop A/B test$",
        r"^Yes$",
        r"^OK$",
        r"^Got it$",
        r"^Dismiss$",
        r"^Close$",
        r"^Not now$",
    ):
        try:
            b = page.get_by_role("button", name=re.compile(name, re.I))
            if b.count() and b.first.is_visible():
                t = b.first.inner_text(timeout=800)
                b.first.click(force=True)
                page.wait_for_timeout(900)
                hit.append(t[:40])
        except Exception:
            pass
    # Text / dialog Continue
    try:
        n = page.evaluate(
            """() => {
              const out=[];
              const re=/^(Continue|Stop test|Stop A\\/B test|Yes|OK)$/i;
              for (const b of document.querySelectorAll('button, ytcp-button, tp-yt-paper-button')) {
                const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
                if (re.test(t) && t.length<40) { b.click(); out.push(t); }
              }
              return out;
            }"""
        )
        hit.extend(n or [])
    except Exception:
        pass
    return hit


def click_private_aggressive(page) -> dict:
    """Prefer Private radio; fall back to coordinate hits inside dialog."""
    res = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || [...document.querySelectorAll('tp-yt-paper-dialog')].find(d=>/Private|Schedule|Public/i.test(d.innerText||''))
            || document.querySelector('tp-yt-paper-dialog');
          const root=dlg||document;
          const hits=[];
          const walk=(node)=>{
            for (const el of node.querySelectorAll('tp-yt-paper-radio-button,[role=radio],ytcp-radio,label,div,span')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const al=(el.getAttribute('aria-label')||'');
              if (!(t==='Private' || /^Private\\b/.test(t) || /^Private\\b/i.test(al))) continue;
              const r=el.getBoundingClientRect();
              if (r.width>20 && r.height>8 && r.height<140 && r.y>40) {
                hits.push({t:t.slice(0,50),x:r.x+Math.min(24,r.width/2),y:r.y+r.height/2,w:r.width,h:r.height,tag:el.tagName});
              }
            }
            for (const el of node.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(root);
          hits.sort((a,b)=>a.h-b.h || a.y-b.y);
          return {dlg:(dlg&&(dlg.innerText||'').slice(0,500))||'', hits:hits.slice(0,10)};
        }"""
    )
    clicked = None
    for h in res.get("hits") or []:
        try:
            page.mouse.click(h["x"], h["y"])
            page.wait_for_timeout(500)
            clicked = h
            break
        except Exception:
            continue
    if not clicked:
        try:
            page.get_by_role("radio", name=re.compile(r"^Private", re.I)).first.click(
                force=True, timeout=2500
            )
            clicked = {"via": "role"}
        except Exception as e:
            res["role_err"] = str(e)[:120]
    res["clicked"] = clicked
    return res


def set_vis(clean, force, page, video_id: str, target: str) -> dict:
    AUDIT.mkdir(parents=True, exist_ok=True)
    r: dict = {"id": video_id, "target": target, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3200)
    force.skip(page)
    force.dismiss(page)
    dismiss_all(page)

    chip0 = clean.visibility_chip(page)
    vis0 = clean.classify(chip0)
    r["before"] = {"chip": chip0[:160], "vis": vis0}
    if vis0 == target:
        r["skipped"] = f"already_{target}"
        r["ok"] = True
        return r

    try:
        force.open_visibility(page)
    except Exception:
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1200)

    page.screenshot(path=str(AUDIT / f"{video_id}_01_dialog.png"))
    if target == "private":
        priv = click_private_aggressive(page)
        r["private_click"] = {
            "clicked": priv.get("clicked"),
            "hits": (priv.get("hits") or [])[:4],
            "dlg": (priv.get("dlg") or "")[:220],
        }
    else:
        hit = clean.click_privacy_radio(page, "Public")
        r["radio_hit"] = hit

    page.wait_for_timeout(600)
    dismiss_all(page)  # ABC may appear immediately
    page.screenshot(path=str(AUDIT / f"{video_id}_02_selected.png"))

    try:
        force.click_done(page)
    except Exception:
        try:
            page.get_by_role("button", name=re.compile(r"^Done$", re.I)).first.click(timeout=2000)
        except Exception as e:
            r["done_err"] = str(e)[:120]

    page.wait_for_timeout(700)
    abc1 = dismiss_all(page)
    if abc1:
        r["abc_after_done"] = abc1
        try:
            force.click_done(page)
        except Exception:
            pass

    r["saved"] = clean.save_all(force, page)
    page.wait_for_timeout(1800)
    abc2 = dismiss_all(page)
    if abc2:
        r["abc_after_save"] = abc2
        # Save again after Continue
        r["saved2"] = clean.save_all(force, page)
        page.wait_for_timeout(1800)

    try:
        page.evaluate("() => { window.onbeforeunload=null; }")
    except Exception:
        pass
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    chip1 = clean.visibility_chip(page)
    vis1 = clean.classify(chip1)
    r["after"] = {"chip": chip1[:160], "vis": vis1}
    r["ok"] = vis1 == target
    page.screenshot(path=str(AUDIT / f"{video_id}_03_verify.png"))

    # Second pass if ABC still blocking
    if not r["ok"] and target == "private":
        try:
            force.open_visibility(page)
            page.wait_for_timeout(1000)
            click_private_aggressive(page)
            force.click_done(page)
            page.wait_for_timeout(500)
            dismiss_all(page)
            clean.save_all(force, page)
            page.wait_for_timeout(1200)
            dismiss_all(page)
            clean.save_all(force, page)
            page.wait_for_timeout(2000)
            page.goto(
                f"https://studio.youtube.com/video/{video_id}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2800)
            chip2 = clean.visibility_chip(page)
            r["after_retry"] = {"chip": chip2[:160], "vis": clean.classify(chip2)}
            r["ok"] = r["after_retry"]["vis"] == target
        except Exception as e:
            r["retry_err"] = str(e)[:160]
    return r


def main() -> None:
    force = load(HELPER, "force")
    clean = load(CLEANUP, "clean")
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"publicize": [], "private": [], "scheduled_ok": []}

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE,
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        for vid in PUBLICIZE:
            print(f"=== PUBLIC {vid} ===", flush=True)
            row = set_vis(clean, force, page, vid, "public")
            result["publicize"].append(row)
            print(json.dumps({k: row.get(k) for k in ("id", "ok", "before", "after", "after_retry", "skipped")}, indent=2), flush=True)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            try:
                row = set_vis(clean, force, page, vid, "private")
            except Exception as e:
                row = {"id": vid, "ok": False, "error": str(e)[:240]}
            result["private"].append(row)
            print(
                json.dumps(
                    {
                        k: row.get(k)
                        for k in (
                            "id",
                            "ok",
                            "before",
                            "after",
                            "after_retry",
                            "abc_after_done",
                            "abc_after_save",
                            "error",
                        )
                    },
                    indent=2,
                ),
                flush=True,
            )

        for vid in KEEP_SCHEDULED:
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2400)
            chip = clean.visibility_chip(page)
            result["scheduled_ok"].append(
                {"id": vid, "vis": clean.classify(chip), "chip": chip[:140]}
            )
            print(f"KEEP {vid} {clean.classify(chip)}", flush=True)

        context.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"]) and all(
        x.get("ok") for x in result["private"]
    )
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
