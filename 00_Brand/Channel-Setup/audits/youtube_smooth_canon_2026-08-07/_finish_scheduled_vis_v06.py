#!/usr/bin/env python3
"""Set visibility by clicking Private/Public radios relative to the Schedule row."""
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
    "youtube_smooth_canon_2026-08-07/FINISH_V06_RESULT.json"
)
AUDIT = OUT.parent / "shots_v06"

PUBLICIZE = ["IqII5mVGdrs"]
FORCE_PRIVATE = ["tUAdhOnMW2g", "svYOx07OrIM", "B2STcIAF1lY", "w1ej9u0rPTA"]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def find_schedule_anchor(page) -> dict | None:
    return page.evaluate(
        """() => {
          const roots=[...document.querySelectorAll('tp-yt-paper-dialog, ytcp-video-visibility-select, ytcp-visibility-selector, [role=dialog]')];
          if (!roots.length) roots.push(document.body);
          const hits=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!=='Schedule' && t!=='Schedule as public' && !/^Schedule\\b/.test(t)) continue;
              if (t.length>40) continue;
              const r=el.getBoundingClientRect();
              if (r.width>20 && r.height>8 && r.height<80 && r.y>50)
                hits.push({t:t.slice(0,40),x:r.x,y:r.y,w:r.width,h:r.height});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          for (const r of roots) walk(r);
          hits.sort((a,b)=>a.y-b.y);
          // Prefer plain 'Schedule' over 'Schedule as public'
          const plain=hits.find(h=>h.t==='Schedule');
          return plain || hits[0] || null;
        }"""
    )


def click_target_above_schedule(page, target: str) -> dict:
    """Private is typically ~2-3 rows above Schedule; Public ~1 row above or below Unlisted."""
    info: dict = {"target": target}
    anchor = find_schedule_anchor(page)
    info["anchor"] = anchor
    if not anchor:
        return info

    # Click several candidate Y offsets above the Schedule row (radio dots are left)
    offsets = {
        "private": [ -150, -120, -90, -70, -50 ],
        "public": [ -100, -80, -60, -40, 30, 50 ],
    }[target]
    for dy in offsets:
        x = anchor["x"] + 18
        y = anchor["y"] + dy + anchor["h"] / 2
        page.mouse.click(x, y)
        page.wait_for_timeout(350)
        info.setdefault("clicks", []).append({"x": x, "y": y, "dy": dy})
        # Check if schedule date fields disappeared / chip-like change in dialog text
        txt = page.evaluate(
            """() => {
              const d=document.querySelector('tp-yt-paper-dialog,[role=dialog]');
              return (d&&d.innerText||'').slice(0,300);
            }"""
        )
        if target == "private" and "Schedule as public" not in (txt or "") and re.search(
            r"\bPrivate\b", txt or "", re.I
        ):
            info["likely"] = "private"
            break
        if target == "public" and re.search(r"\bPublic\b", txt or "", re.I) and "Schedule as public" not in (txt or ""):
            info["likely"] = "public"
            break

    # Also try explicit text
    try:
        page.get_by_text(target.capitalize(), exact=True).first.click(force=True, timeout=1500)
        info["text_click"] = True
    except Exception:
        pass
    return info


def apply(force, clean, page, video_id: str, target: str) -> dict:
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
    # Close stray Close-only dialogs
    try:
        page.get_by_role("button", name=re.compile(r"^Close$", re.I)).first.click(timeout=800)
    except Exception:
        pass

    chip0 = clean.visibility_chip(page)
    vis0 = clean.classify(chip0)
    r["before"] = {"chip": chip0[:160], "vis": vis0}
    if vis0 == target:
        r["ok"] = True
        r["skipped"] = f"already_{target}"
        return r

    # Open visibility — prefer clicking the chip text "Scheduled"
    try:
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    except Exception:
        force.open_visibility(page)
    page.wait_for_timeout(1500)
    page.screenshot(path=str(AUDIT / f"{video_id}_01.png"))

    # If we only see a Close tip, dismiss and reopen
    body = page.locator("body").inner_text()
    if "Schedule as public" not in body and "Select video privacy" not in body:
        try:
            page.get_by_role("button", name=re.compile(r"^Close$", re.I)).first.click(timeout=800)
        except Exception:
            pass
        page.wait_for_timeout(500)
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(AUDIT / f"{video_id}_01b.png"))

    r["ui"] = click_target_above_schedule(page, target)
    page.screenshot(path=str(AUDIT / f"{video_id}_02.png"))

    force.click_done(page)
    page.wait_for_timeout(800)
    page.evaluate(
        """() => { for (const b of document.querySelectorAll('button,ytcp-button')) {
          if (/^Continue$/i.test((b.innerText||'').trim())) b.click(); }}"""
    )
    clean.save_all(force, page)
    page.wait_for_timeout(1800)
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
    page.screenshot(path=str(AUDIT / f"{video_id}_03.png"))
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

        # Wait if previous finish still holding? just proceed
        for vid in PUBLICIZE:
            print(f"=== PUBLIC {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "public")
            print(json.dumps({k: row.get(k) for k in ("id","ok","before","after","ui")}, indent=2)[:2000], flush=True)
            result["publicize"].append(row)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "private")
            print(json.dumps({k: row.get(k) for k in ("id","ok","before","after","ui")}, indent=2)[:2000], flush=True)
            result["private"].append(row)

        ctx.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"] + result["private"])
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
