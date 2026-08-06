#!/usr/bin/env python3
"""Scroll visibility dialog up → click Private/Public radio (schedule mode hides them)."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-from-chrome"
HELPER = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
    "11_Upload-Package/Schedule/_force_schedule_shorts_v01.py"
)
CLEANUP = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_cleanup_2026-08-07/_cleanup_visibility_cdp.py"
)
OUT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "youtube_smooth_canon_2026-08-07/FINISH_V05_RESULT.json"
)
AUDIT = OUT.parent / "shots_v05"

PUBLICIZE = ["IqII5mVGdrs"]
FORCE_PRIVATE = ["tUAdhOnMW2g", "svYOx07OrIM", "B2STcIAF1lY", "w1ej9u0rPTA"]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def dump_all(page) -> dict:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog');
          if (!dlg) return {err:'no_dialog'};
          const r=dlg.getBoundingClientRect();
          const radios=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio],ytcp-radio')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,100);
              const al=el.getAttribute('aria-label')||'';
              const checked=el.getAttribute('aria-checked')||'';
              const b=el.getBoundingClientRect();
              radios.push({t,al:al.slice(0,80),checked,x:b.x,y:b.y,w:b.w||b.width,h:b.h||b.height,vis:b.height>0 && b.width>0});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg);
          // also any scrollable
          let scroll=null;
          for (const el of dlg.querySelectorAll('*')) {
            if (el.scrollHeight > el.clientHeight + 20) {
              const b=el.getBoundingClientRect();
              if (b.height>80) { scroll={tag:el.tagName,sh:el.scrollHeight,ch:el.clientHeight,st:el.scrollTop}; break; }
            }
          }
          return {dlg:{x:r.x,y:r.y,w:r.width,h:r.height,text:(dlg.innerText||'').slice(0,500)}, radios, scroll};
        }"""
    )


def scroll_dialog_top(page) -> dict:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog');
          if (!dlg) return {ok:false};
          const moved=[];
          const tryScroll=(el)=>{
            if (el.scrollHeight > el.clientHeight + 10) {
              el.scrollTop = 0;
              moved.push(el.tagName+':'+el.scrollHeight);
            }
          };
          tryScroll(dlg);
          for (const el of dlg.querySelectorAll('*')) tryScroll(el);
          // mouse wheel on dialog
          return {ok:true, moved};
        }"""
    )


def pick_label(page, label: str) -> dict | None:
    # Prefer radios whose text is exactly Private/Public/Unlisted
    data = dump_all(page)
    for r in data.get("radios") or []:
        t = (r.get("t") or "").strip()
        al = (r.get("al") or "").strip()
        blob = (t + " " + al).lower()
        if label.lower() == "public" and "schedule" in blob:
            continue
        if t == label or al == label or t.startswith(label + "\n") or re.match(rf"^{label}\\b", t):
            if r.get("w", 0) < 5:
                continue
            page.mouse.click(r["x"] + 14, r["y"] + max(r.get("h", 20) / 2, 8))
            page.wait_for_timeout(600)
            return r
    # Text click inside dialog
    try:
        page.locator("tp-yt-paper-dialog").get_by_text(label, exact=True).first.click(
            force=True, timeout=2000
        )
        page.wait_for_timeout(600)
        return {"via": "text", "label": label}
    except Exception:
        pass
    try:
        page.get_by_role("radio", name=re.compile(rf"^{label}\\b", re.I)).first.click(
            force=True, timeout=2000
        )
        return {"via": "role"}
    except Exception:
        return None


def apply(force, clean, page, video_id: str, target: str) -> dict:
    AUDIT.mkdir(parents=True, exist_ok=True)
    r: dict = {"id": video_id, "target": target, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    force.skip(page)
    force.dismiss(page)
    chip0 = clean.visibility_chip(page)
    vis0 = clean.classify(chip0)
    r["before"] = {"chip": chip0[:160], "vis": vis0}
    if vis0 == target:
        r["ok"] = True
        r["skipped"] = f"already_{target}"
        return r

    force.open_visibility(page)
    page.wait_for_timeout(1200)
    page.screenshot(path=str(AUDIT / f"{video_id}_01.png"))
    r["dump0"] = dump_all(page)
    r["scroll"] = scroll_dialog_top(page)
    # Also mouse-wheel up over dialog center
    dlg = r["dump0"].get("dlg") or {}
    if dlg.get("x") is not None:
        page.mouse.move(dlg["x"] + dlg["w"] / 2, dlg["y"] + 40)
        for _ in range(8):
            page.mouse.wheel(0, -200)
            page.wait_for_timeout(120)
    page.wait_for_timeout(400)
    page.screenshot(path=str(AUDIT / f"{video_id}_02.png"))
    r["dump1"] = dump_all(page)

    label = "Public" if target == "public" else "Private"
    picked = pick_label(page, label)
    r["picked"] = picked
    if not picked:
        # PageDown reverse: click near top of dialog where radios usually sit
        if dlg.get("x") is not None:
            # Try clicking typical Private/Public radio positions from top of dialog
            for dy in (70, 100, 130, 160, 190, 220):
                page.mouse.click(dlg["x"] + 40, dlg["y"] + dy)
                page.wait_for_timeout(250)
            r["coord_scan"] = True
            picked = pick_label(page, label)
            r["picked2"] = picked

    page.screenshot(path=str(AUDIT / f"{video_id}_03.png"))
    force.click_done(page)
    page.wait_for_timeout(700)
    page.evaluate(
        """() => { for (const b of document.querySelectorAll('button,ytcp-button')) {
          if (/^Continue$/i.test((b.innerText||'').trim())) b.click(); }}"""
    )
    clean.save_all(force, page)
    page.wait_for_timeout(1600)
    page.evaluate(
        """() => { for (const b of document.querySelectorAll('button,ytcp-button')) {
          if (/^Continue$/i.test((b.innerText||'').trim())) b.click(); }}"""
    )
    clean.save_all(force, page)
    page.wait_for_timeout(1600)

    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    chip1 = clean.visibility_chip(page)
    r["after"] = {"chip": chip1[:160], "vis": clean.classify(chip1)}
    r["ok"] = r["after"]["vis"] == target
    page.screenshot(path=str(AUDIT / f"{video_id}_04.png"))
    # Trim dumps for JSON size
    for k in ("dump0", "dump1"):
        if k in r and isinstance(r[k], dict):
            r[k] = {
                "text": (r[k].get("dlg") or {}).get("text", "")[:300],
                "radios": r[k].get("radios", [])[:12],
                "scroll": r[k].get("scroll"),
            }
    return r


def main() -> None:
    force = load(HELPER, "force")
    clean = load(CLEANUP, "clean")
    result = {"publicize": [], "private": []}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        for vid in PUBLICIZE:
            print(f"=== PUBLIC {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "public")
            print(json.dumps({k: row.get(k) for k in ("id","ok","before","after","picked","dump1")}, indent=2)[:2500], flush=True)
            result["publicize"].append(row)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "private")
            print(json.dumps({k: row.get(k) for k in ("id","ok","before","after","picked","dump1")}, indent=2)[:2500], flush=True)
            result["private"].append(row)

        ctx.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"] + result["private"])
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
