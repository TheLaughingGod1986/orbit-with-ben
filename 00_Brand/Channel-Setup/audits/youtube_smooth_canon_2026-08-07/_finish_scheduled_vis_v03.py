#!/usr/bin/env python3
"""Finish remaining BH shelf: unschedule→Public/Private via schedule accordion UI."""
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
    "youtube_smooth_canon_2026-08-07/FINISH_V03_RESULT.json"
)
AUDIT = OUT.parent / "shots_v03"

# Smooth short that should be Public now (past launch window)
PUBLICIZE = ["IqII5mVGdrs"]
# Old juddery scheduled shorts → Private (clear schedule)
FORCE_PRIVATE = ["tUAdhOnMW2g", "svYOx07OrIM", "B2STcIAF1lY", "w1ej9u0rPTA"]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def dismiss(page) -> list[str]:
    hit = []
    try:
        hit = page.evaluate(
            """() => {
              const out=[];
              const re=/^(Continue|Stop test|Stop A\\/B test|Yes|OK|Got it|Dismiss)$/i;
              for (const b of document.querySelectorAll('button, ytcp-button, tp-yt-paper-button')) {
                const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
                if (re.test(t) && t.length<40) { b.click(); out.push(t); }
              }
              return out;
            }"""
        ) or []
    except Exception:
        pass
    return hit


def set_vis_from_schedule_dialog(page, target: str) -> dict:
    """target: public | private. Handles Save-or-publish schedule accordion."""
    info: dict = {"target": target}
    # Prefer classic privacy radios if present
    radios = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          if (!dlg) return {hasRadios:false};
          const t=(dlg.innerText||'');
          return {
            hasRadios: /\\bPublic\\b/.test(t) && /\\bPrivate\\b/.test(t) && /Select video privacy|Visibility/i.test(t),
            snip: t.slice(0,300)
          };
        }"""
    )
    info["dialog"] = radios

    # Turn OFF schedule if visible (toggle / uncheck)
    off = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog') || document;
          const out=[];
          // uncheck schedule checkbox / switch
          for (const el of dlg.querySelectorAll('tp-yt-paper-checkbox, [role=checkbox], input[type=checkbox], tp-yt-toggle-button, button[role=switch], [aria-checked]')) {
            const al=((el.getAttribute('aria-label')||'') + ' ' + (el.innerText||'')).toLowerCase();
            const checked = el.getAttribute('aria-checked')==='true' || el.checked === true;
            if (/schedule/.test(al) && checked) { el.click(); out.push('toggle:'+al.slice(0,40)); }
          }
          // Also click second-container / schedule row to collapse if expanded with date fields
          return out;
        }"""
    )
    info["schedule_off"] = off
    page.wait_for_timeout(600)

    # Click visibility dropdown → Public/Private if present (new accordion UI)
    dd = page.evaluate(
        """(label) => {
          const dlg=document.querySelector('tp-yt-paper-dialog')||document;
          // Find a trigger that currently says Private/Public/Schedule
          let trigger=null;
          const walk=(root)=>{
            for (const el of root.querySelectorAll('ytcp-text-dropdown-trigger, tp-yt-paper-dropdown-menu, [aria-haspopup], button, div')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!/^(Private|Public|Unlisted)$/i.test(t) && !/^Visibility/i.test(t)) continue;
              const r=el.getBoundingClientRect();
              if (r.width>40 && r.height>12 && r.height<80) {
                trigger={x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,40)};
                return;
              }
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg);
          return trigger;
        }""",
        target,
    )
    if dd:
        page.mouse.click(dd["x"], dd["y"])
        page.wait_for_timeout(700)
        info["dropdown"] = dd
        picked = page.evaluate(
            """(label) => {
              const re=new RegExp('^'+label+'$','i');
              const hits=[];
              const walk=(root)=>{
                for (const el of root.querySelectorAll('tp-yt-paper-item, [role=option], ytcp-ve, span, div, tp-yt-paper-radio-button')) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!re.test(t)) continue;
                  const r=el.getBoundingClientRect();
                  if (r.width>30 && r.height>10 && r.height<80 && r.y>50) hits.push({x:r.x+20,y:r.y+r.height/2,t});
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
              };
              walk(document);
              hits.sort((a,b)=>a.y-b.y);
              return hits[0]||null;
            }""",
            target.capitalize(),
        )
        if picked:
            page.mouse.click(picked["x"], picked["y"])
            page.wait_for_timeout(500)
            info["picked"] = picked

    # Classic radio path
    label = "Public" if target == "public" else "Private"
    hit = page.evaluate(
        """(label) => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const hits=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio],label,div,span')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!(t===label || t.startsWith(label+' '))) continue;
              const r=el.getBoundingClientRect();
              if (r.width>30 && r.height>8 && r.height<120) hits.push({x:r.x+16,y:r.y+r.height/2,t:t.slice(0,40),h:r.height});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg||document);
          hits.sort((a,b)=>a.h-b.h);
          return hits[0]||null;
        }""",
        label,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(500)
        info["radio"] = hit

    # If schedule still expanded with date, click Private/Public radio which collapses schedule
    # Done
    try:
        page.get_by_role("button", name=re.compile(r"^Done$", re.I)).last.click(force=True, timeout=2500)
        info["done"] = True
    except Exception as e:
        info["done_err"] = str(e)[:120]
    page.wait_for_timeout(800)
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
    dismiss(page)

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
    r["ui"] = set_vis_from_schedule_dialog(page, target)
    page.screenshot(path=str(AUDIT / f"{video_id}_02.png"))
    dismiss(page)
    r["saved"] = clean.save_all(force, page)
    page.wait_for_timeout(1500)
    dismiss(page)
    # second save if ABC
    clean.save_all(force, page)
    page.wait_for_timeout(1800)

    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    chip1 = clean.visibility_chip(page)
    vis1 = clean.classify(chip1)
    r["after"] = {"chip": chip1[:160], "vis": vis1}
    r["ok"] = vis1 == target

    # Retry once with expand-schedule then Private radio if still scheduled
    if not r["ok"]:
        force.open_visibility(page)
        page.wait_for_timeout(1000)
        try:
            force.expand_schedule(page)
        except Exception:
            pass
        # Click the non-schedule Private/Public option
        page.evaluate(
            """(label) => {
              const dlg=document.querySelector('tp-yt-paper-dialog');
              for (const el of (dlg||document).querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (t===label || t.startsWith(label+' ')) { el.click(); return t; }
              }
              return null;
            }""",
            "Public" if target == "public" else "Private",
        )
        page.wait_for_timeout(500)
        force.click_done(page)
        page.wait_for_timeout(600)
        dismiss(page)
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

        for vid in PUBLICIZE:
            print(f"=== PUBLIC {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "public")
            result["publicize"].append(row)
            print(json.dumps(row, indent=2)[:1200], flush=True)

        for vid in FORCE_PRIVATE:
            print(f"=== PRIVATE {vid} ===", flush=True)
            row = apply(force, clean, page, vid, "private")
            result["private"].append(row)
            print(json.dumps(row, indent=2)[:1200], flush=True)

        ctx.close()

    result["ok"] = all(x.get("ok") for x in result["publicize"] + result["private"])
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Wrote", OUT, "ok=", result["ok"], flush=True)


if __name__ == "__main__":
    main()
