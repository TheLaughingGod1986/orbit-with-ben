#!/usr/bin/env python3
"""Collapse Schedule accordion → set Public/Private radios for remaining BH shelf."""
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
    "youtube_smooth_canon_2026-08-07/FINISH_V04_RESULT.json"
)
AUDIT = OUT.parent / "shots_v04"

PUBLICIZE = ["IqII5mVGdrs"]
FORCE_PRIVATE = ["tUAdhOnMW2g", "svYOx07OrIM", "B2STcIAF1lY", "w1ej9u0rPTA"]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def dump_radios(page) -> list[dict]:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog')||document;
          const out=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80);
              const al=el.getAttribute('aria-label')||'';
              const checked=el.getAttribute('aria-checked')||el.getAttribute('aria-selected')||'';
              const r=el.getBoundingClientRect();
              if (r.width>5 && r.height>5)
                out.push({t,al:al.slice(0,60),checked,x:r.x,y:r.y,w:r.width,h:r.height,tag:el.tagName});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg);
          return out;
        }"""
    )


def collapse_schedule(page) -> dict:
    """Collapse expanded schedule so Public/Private radios reappear."""
    info: dict = {}
    # Click expand/collapse control
    hit = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog')||document;
          const cands=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=(el.getAttribute('aria-label')||'');
              const id=el.id||'';
              if (/click to expand|click to collapse|collapse/i.test(al) || /expand-button/i.test(id)) {
                const r=el.getBoundingClientRect();
                if (r.width>5) cands.push({via:'al',al,id,x:r.x+r.width/2,y:r.y+r.height/2});
              }
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(dlg);
          return cands[0]||null;
        }"""
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(900)
        info["collapse"] = hit
    # Also try clicking the word Schedule header row (not Schedule as public)
    try:
        page.locator("tp-yt-paper-dialog").get_by_text("Schedule", exact=True).first.click(
            force=True, timeout=1200
        )
        page.wait_for_timeout(700)
        info["schedule_text_click"] = True
    except Exception:
        pass
    return info


def pick_radio(page, label: str) -> dict | None:
    radios = dump_radios(page)
    # Prefer exact short label
    for r in radios:
        t = (r.get("t") or "").strip()
        al = (r.get("al") or "").strip()
        if t == label or al.startswith(label) or t.startswith(label + " "):
            # Avoid "Schedule as public" when wanting Public — prefer pure Public
            if label == "Public" and "schedule" in (t + al).lower():
                continue
            page.mouse.click(r["x"] + min(18, r["w"] / 2), r["y"] + r["h"] / 2)
            page.wait_for_timeout(600)
            return r
    # Fallback role
    try:
        page.get_by_role("radio", name=re.compile(rf"^{label}\\b", re.I)).first.click(
            force=True, timeout=2000
        )
        return {"via": "role", "label": label}
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
    r["radios_before"] = dump_radios(page)
    r["collapse"] = collapse_schedule(page)
    page.wait_for_timeout(700)
    page.screenshot(path=str(AUDIT / f"{video_id}_02.png"))
    r["radios_after_collapse"] = dump_radios(page)

    label = "Public" if target == "public" else "Private"
    picked = pick_radio(page, label)
    r["picked"] = picked
    # If Public and still only schedule radios, try Private then Public? No — for public click Public.
    if not picked and target == "public":
        # Some UIs only expose Schedule-as-public; collapse then Public
        collapse_schedule(page)
        picked = pick_radio(page, "Public")
        r["picked2"] = picked

    page.screenshot(path=str(AUDIT / f"{video_id}_03.png"))
    force.click_done(page)
    page.wait_for_timeout(800)
    # ABC continue
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button, ytcp-button')) {
            const t=(b.innerText||'').trim();
            if (/^Continue$/i.test(t)) b.click();
          }
        }"""
    )
    r["saved"] = clean.save_all(force, page)
    page.wait_for_timeout(2000)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button, ytcp-button')) {
            const t=(b.innerText||'').trim();
            if (/^Continue$/i.test(t)) b.click();
          }
        }"""
    )
    clean.save_all(force, page)
    page.wait_for_timeout(1800)

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
            print(
                json.dumps(
                    {
                        k: row.get(k)
                        for k in (
                            "id",
                            "ok",
                            "before",
                            "after",
                            "picked",
                            "radios_after_collapse",
                            "collapse",
                        )
                    },
                    indent=2,
                )[:2000],
                flush=True,
            )
            result["publicize"].append(row)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "private")
            print(
                json.dumps(
                    {
                        k: row.get(k)
                        for k in (
                            "id",
                            "ok",
                            "before",
                            "after",
                            "picked",
                            "radios_after_collapse",
                        )
                    },
                    indent=2,
                )[:2000],
                flush=True,
            )
            result["private"].append(row)

        ctx.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"] + result["private"])
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
